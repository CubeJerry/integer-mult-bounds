#!/usr/bin/env python3
"""Independent 222-column, rational-chart interpreter; no author imports."""
import argparse,copy,hashlib,json
from pathlib import Path
from fractions import Fraction
from collections import Counter

def rref(rows,n=8):
 a=[list(map(Fraction,r))for r in rows if any(r)];k=0
 for j in range(n):
  p=next((p for p in range(k,len(a))if a[p][j]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];z=a[k][j];a[k]=[x/z for x in a[k]]
  for q in range(len(a)):
   if q!=k and a[q][j]:z=a[q][j];a[q]=[x-z*y for x,y in zip(a[q],a[k])]
  k+=1
 return tuple(tuple(r)for r in a[:k])
def null(rows):
 R=rref(rows);piv=[next(i for i,x in enumerate(r)if x)for r in R];out=[]
 for free in range(8):
  if free in piv:continue
  v=[Fraction(0)]*8;v[free]=1
  for p,r in zip(piv,R):v[p]=-r[free]
  out.append(v)
 return rref(out)
def contained(A,B):return len(rref(A+B))==len(B)
def brank(rows):
 b={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in b:v^=b[p]
   else:b[p]=v;break
 return len(b)
def read_word(w,roots,seedspace,invoice=True):
 charts={k:(rref(c['rows'])if c['kind']=='span'else null(c['rows']))for k,c in w['charts'].items()}
 for j in range(111):
  assert charts[f'L{j}']==rref([roots[j]])
  assert charts[f'F{j}']==null([roots[j]])
 assert len(charts['Hub'])==8 and not charts['zero']
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 own=set();born=set();hist=Counter();ops=Counter();dirty=0;marks={v:k for k,v in w['milestones'].items()};cut={};allsource=[]
 for index,o in enumerate(w['operations'],1):
  op=o[0];ops[op]+=1
  if op=='INIT':
   _,n,c=o;assert n not in vals and n not in born;vals[n]=0;at[n]=c;own.add(n);born.add(n)
  elif op=='ADD':
   _,s,t=o;assert s in vals and t in vals and charts[at[s]]==charts[at[t]],(index,o,at.get(s),at.get(t))
   vals[t]^=vals[s]
  elif op=='MOVE':
   _,n,c=o;assert n in vals and c in charts;old,new=charts[at[n]],charts[c]
   assert (contained(new,old)if n in own else contained(old,new)),(index,o,'direction')
   dist=abs(len(new)-len(old));assert dist>0,(index,o,'zero MOVE')
   hist[dist]+=1;at[n]=c
  elif op=='CLEAR':
   _,n=o;assert n in own;dirty+=bool(vals[n]);own.remove(n);vals.pop(n);at.pop(n)
  else:raise AssertionError(op)
  if index==w['milestones']['source_cut']:
   assert brank(vals[f'X{j}']for j in range(111))==111
   for receiver,roles in w['private_roles'].items():
    p=w['singleton_pivots'][receiver];assert vals[f'X{p}']==sum(1<<j for j in roles)
   cut['source_X_rank']=111
  if index==w['milestones']['seed8_before_Y']:
   assert all(vals[f'Y{j}']==1<<(111+j)and at[f'Y{j}']=='zero'for j in range(111))
   seeds=[vals[f'P{j}']for j in range(8)];assert seeds==[int(x,16)for x in w['seed_rows_hex']]
   assert all(at[f'P{j}']=='zero'for j in range(8))
   assert brank(seeds)==8 and brank(seeds+seedspace)==8
   for j in w['point_targets']:assert vals[f'E{j}']==1<<j and at[f'E{j}']=='zero'
   cut['seed_rank']=8;cut['actual_ground_rank']=brank(seeds+[vals[f'E{j}']for j in w['point_targets']])
  if index in marks and marks[index].startswith('completed_'):
   j=int(marks[index][10:]);assert vals[f'Y{j}']==(1<<j)^(1<<(111+j));assert at[f'Y{j}']==f'F{j}'
  if index==w['milestones']['all_X_restored']:
   assert all(vals[f'X{j}']==1<<j and at[f'X{j}']=='Hub'for j in range(111))
  allsource.append(None)
 for j in range(111):
  assert vals[f'X{j}']==1<<j and at[f'X{j}']=='Hub'
  want=(1<<(111+j))^((1<<j)if j in w['targets'] else 0)
  assert vals[f'Y{j}']==want and at[f'Y{j}']==f'F{j}',('Yendpoint',j)
 assert not own and len(vals)==222
 if invoice:
  assert dict(hist)=={1:54,2:50,3:10,4:10,5:50,6:45,7:117,8:8}
  assert dict(ops)=={'INIT':19,'ADD':421,'MOVE':344,'CLEAR':19}
 return {'operations':dict(ops),'movement':dict(sorted(hist.items())),'dirty_clears':dirty,'cuts':cut}
def without(w,index):
 z=copy.deepcopy(w);z['operations'].pop(index)
 z['milestones']={k:v-(v>index)for k,v in z['milestones'].items()}
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 raw=a.word.read_bytes();w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots'];sd=json.loads(a.seed.read_text());seedspace=[int(x,16)for x in sd['seed_rows']]
 assert sd['h_values']==w['singular_h'];positive=read_word(w,roots,seedspace)
 tests=[];O=w['operations'];predicates=[('early_capture',lambda o:o==['ADD','X1','E1']),('early_delivery',lambda o:o==['MOVE','E1','zero']),('Hub_seed',lambda o:o[0]=='ADD'and o[2]=='P1'and o[1].startswith('X')),('point_seed_correction',lambda o:o[0]=='ADD'and o[1]=='E1'and o[2]=='P0'),('common_capture',lambda o:o[0]=='ADD'and o[2]=='Q0'),('private_aggregate',lambda o:o==['ADD','X10','X1']),('cache_descent',lambda o:o[0]=='MOVE'and o[1]=='Q1'),('local_delivery',lambda o:o==['ADD','X1','Y3']),('cache_read',lambda o:o[0]=='ADD'and o[1]=='Q0'and o[2]=='Y3'),('inverse_restore',lambda o:o==['ADD','X10','X1']),('retirement',lambda o:o==['CLEAR','Q0'])]
 for name,pred in predicates:
  ids=[i for i,o in enumerate(O)if pred(o)];assert ids,name
  ix=ids[-1]if name=='inverse_restore'else ids[0];z=without(w,ix)
  try:read_word(z,roots,seedspace,invoice=False)
  except AssertionError:tests.append(name)
  else:raise AssertionError(('mutant accepted',name))
 z=copy.deepcopy(w);ix=next(i for i,o in enumerate(O)if o[0]=='MOVE'and o[1]=='Q1');z['operations'][ix][2]='Hub'
 try:read_word(z,roots,seedspace,invoice=False)
 except AssertionError:tests.append('owned_upward_MOVE')
 else:raise AssertionError('owned upward accepted')
 out={'status':'PASS_INDEPENDENT_SINGULAR_TWELVE_SOURCE','word_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashlib.sha256(src).hexdigest(),'seed_source_sha256':hashlib.sha256(a.seed.read_bytes()).hexdigest(),'all_columns':222,'positive':positive,'semantic_negative_controls':tests,'negative_controls_ignore_invoice':True,'seed_W15_link':'Word ground seed span equals separately checked source-bound S8; all111completion requires7proper modes still unacquired','scope':'Actual12completedand99unchangedoutputs; no new kappa'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k in ['status','word_sha256','all_columns','positive']}))
if __name__=='__main__':main()
