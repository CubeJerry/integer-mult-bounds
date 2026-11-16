from sympy import Matrix
from collections import Counter
from functools import lru_cache
@lru_cache(None)
def rowbasis(rows):
 m=Matrix(rows)if rows else Matrix.zeros(0,8);r,p=m.rref();return tuple(tuple(r[i,j]for j in range(8))for i in range(len(p)))
def chart(s):
 rows=tuple(tuple(r)for r in s['rows'])
 if s['kind']=='span':return rowbasis(rows)
 assert s['kind']=='ann';ns=Matrix(rows).nullspace();return rowbasis(tuple(tuple(v)for v in ns))
@lru_cache(None)
def sub(A,B):return len(rowbasis(A+B))==len(B)
def replay(z,metadata=True):
 C={n:chart(s)for n,s in z['charts'].items()};v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};own=set();born=set();counts=Counter();moves=Counter();dirty=0;peak=0;cuts={};p7=[];newreads=[];xevents=[]
 for step,o in enumerate(z['operations'],1):
  counts[o[0]]+=1
  if o[0]=='INIT':
   _,n,c=o;assert n not in v and n not in born;v[n]=0;at[n]=c;own.add(n);born.add(n)
  elif o[0]=='ADD':
   _,s,t=o;assert C[at[s]]==C[at[t]],(step,o,'colocation')
   if t=='P7':p7.append((s,v[s],at[s]))
   if s=='HKEEP_D7'and t in ['P0','Y3','Y21']:newreads.append((step,t,v[s],at[s],at[t]))
   v[t]^=v[s]
  elif o[0]=='MOVE':
   _,n,c=o;old=at[n];assert sub(C[c],C[old])if n in own else sub(C[old],C[c]),(step,o,'direction');dist=abs(len(C[c])-len(C[old]));assert dist>0;moves[dist]+=1;at[n]=c
  elif o[0]=='CLEAR':
   _,n=o;assert n in own;dirty+=bool(v[n]);own.remove(n);del v[n];del at[n]
  else:raise AssertionError(o)
  peak=max(peak,len(own))
  if (o[0]=='MOVE'and o[1].startswith('X'))or(o[0]=='ADD'and o[2].startswith('X')):xevents.append((tuple(o),tuple((n,v[n],at[n])for n in o[1:]if n.startswith('X'))))
  if metadata and step in[z['milestones']['source_cut'],z['milestones']['seed8_before_Y']]:cuts['source'if step==z['milestones']['source_cut']else'seed']=(v.copy(),at.copy())
 for i in range(111):
  assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
  assert v[f'Y{i}']==((1<<(111+i))^((1<<i)if i in z['targets']else 0))and at[f'Y{i}']==f'F{i}'
 assert not own and len(v)==222
 return {'cuts':cuts,'p7':p7,'newreads':newreads,'xevents':xevents,'counts':dict(counts),'moves':dict(sorted(moves.items())),'dirty':dirty,'peak':peak}
