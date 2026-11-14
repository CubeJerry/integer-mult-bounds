#!/usr/bin/env python3
"""Independent actual all-route historical-coordinate extraction from native BIT words.
No producer or theorem-author implementation is imported. Finite evidence only.
"""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
def need(b,m):
 if not b:raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def rref(a):
 a=[list(map(F,row)) for row in a];j=0
 for c in range(8):
  k=next((k for k in range(j,len(a)) if a[k][c]),None)
  if k is None:continue
  a[j],a[k]=a[k],a[j];q=a[j][c];a[j]=[v/q for v in a[j]]
  for k in range(len(a)):
   if k!=j:
    q=a[k][c];a[k]=[v-q*w for v,w in zip(a[k],a[j])]
  j+=1
 return tuple(tuple(row) for row in a[:j])
def contained(a,b):return len(rref(a+b))==len(b)
def basis(rows):
 b={}
 for row in rows:
  while row:
   p=row.bit_length()-1
   if p in b:row^=b[p]
   else:b[p]=row;break
 return b
def rank(rows):return len(basis(rows))
def in_span(row,b):
 while row:
  p=row.bit_length()-1
  if p not in b:return False
  row^=b[p]
 return True
def linear(mask,rows):
 z=0
 while mask:
  a=mask&-mask;z^=rows[a.bit_length()-1];mask^=a
 return z
def inverse(rows):
 n=len(rows);left=rows[:];right=[1<<j for j in range(n)]
 for j in range(n):
  k=next((k for k in range(j,n) if left[k]>>j&1),None)
  need(k is not None,'invertible complement matrix')
  left[j],left[k]=left[k],left[j];right[j],right[k]=right[k],right[j]
  for k in range(n):
   if k!=j and left[k]>>j&1:left[k]^=left[j];right[k]^=right[j]
 need(left==[1<<j for j in range(n)],'inverse elimination')
 return right
def complement(M,n):
 selected=[];rowbasis=[]
 for j,row in enumerate(M):
  if not in_span(row,basis(rowbasis)):selected.append(j);rowbasis.append(row)
 r=len(rowbasis);h=[]
 for j in range(n):
  if not in_span(1<<j,basis(rowbasis+h)):h.append(1<<j)
 A=rowbasis+h;need(len(A)==n,'complete dual basis');Ai=inverse(A)
 R=[sum(1<<selected[j] for j in range(r) if row>>j&1) for row in Ai]
 J=[row>>r for row in Ai]
 for j in range(n):need(linear(R[j],M)^linear(J[j],h)==1<<j,'RM+Jh=I')
 need(all(linear(row,J)==0 for row in M),'MJ=0')
 need([linear(row,J) for row in h]==[1<<j for j in range(n-r)],'hJ=I')
 need(all(linear(row,R)==0 for row in h),'hR=0')
 return R,J,h
def replay(w,n):
 need(w['start']==n['start'][:222] and w['public']==222,'native input signature')
 frames={int(k):rref(v['B']) for k,v in w['frames'].items()}
 for k,f in w['frames'].items():
  B=frames[int(k)];A=rref(f['A'])
  need(len(B)==f['dim'] and len(A)+len(B)==8,'chart dimension')
  need(all(sum(x*y for x,y in zip(a,b))==0 for a in A for b in B),'exact chart annihilator')
 for k in set(n['start'][:222]+n['final'][:222])&frames.keys():
  need(frames[k]==rref(n['frames'][str(k)]['B']),'native endpoint space')
 loc=dict(enumerate(w['start']));val={i:1<<i for i in range(222)}
 seen=set(loc);history=[(frames[loc[i]],val[i],-1,i) for i in range(222)]
 events=[];counts=Counter();moves=Counter();peak=0;clears=[];pairchecks=set()
 for k,op in enumerate(w['program']):
  typ,i=op[:2];counts[typ]+=1
  if typ=='INIT':
   need(i>=222 and i not in seen,'fresh zero lifetime');seen.add(i);loc[i]=op[2];val[i]=0
   peak=max(peak,len(loc)-222);ev=dict(op=typ,i=i,C=frames[loc[i]])
  elif typ=='ADD':
   _,i,j,c=op;need(i!=j and loc.get(i)==loc.get(j)==c,'actual simultaneous cochart')
   val[i]^=val[j];ev=dict(op=typ,i=i,j=j,C=frames[c])
  elif typ=='CLEAR':
   need(i>=222 and loc.get(i)==op[2],'owned retirement')
   ev=dict(op=typ,i=i,C=frames[loc[i]],value=val[i]);clears.append((k,i,loc[i],val[i]))
   del loc[i];del val[i]
  elif typ=='MOVE':
   _,i,c,d=op;need(loc.get(i)==c,'actual move entrance')
   A,B=frames[c],frames[d];delta=len(B)-len(A)
   if (A,B) not in pairchecks:
    need(contained(A,B) if delta>=0 else contained(B,A),'nested physical movement');pairchecks.add((A,B))
   ev=dict(op=typ,i=i,C=A,Cnext=B,value=val[i],delta=delta,owned=i>=222)
   loc[i]=d;moves[abs(delta)]+=1
  else:raise ValueError('unsupported opcode '+typ)
  events.append(ev)
  if typ!='CLEAR':history.append((frames[loc[i]],val[i],k,i))
 need([loc[i] for i in range(222)]==w['final'],'declared actual endpoints')
 return dict(frames=frames,loc=loc,val=val,events=events,history=history,counts=counts,moves=moves,peak=peak,clears=clears)
def normalize(w,n,re):
 events=re['events'];frames=re['frames'];proper={C for C in frames.values() if 0<len(C)<8}
 Z=[e['value'] for e in events if e['op']=='MOVE' and e['delta']<0 and not e['Cnext']]
 G=Z[:];cells=[]
 for C in sorted(proper,key=lambda c:(len(c),c)):
  U=[];Pin=[];arrivals={};initial={}
  for i,c in enumerate(w['start']):
   if frames[c]==C:initial[i]=len(U);U.append(1<<i)
  for k,e in enumerate(events):
   if e['op']=='MOVE' and e['delta'] and e['Cnext']==C:
    down=e['delta']<0;slot=len(Pin) if down else len(U)
    arrivals[k]=(down,slot);(Pin if down else U).append(e['value'])
  if not Pin and not arrivals and not initial and not any(e.get('C')==C and e['op']=='INIT' for e in events):continue
  formal={i:1<<j for i,j in initial.items()};out=[];actual=[]
  for k,e in enumerate(events):
   typ=e['op'];i=e['i']
   if typ=='MOVE':
    if not e['delta']:continue
    if e['C']==C:
     if e['delta']<0:out.append(formal[i]);actual.append(e['value'])
     del formal[i]
    if e['Cnext']==C:
     down,j=arrivals[k];formal[i]=1<<(j+(len(U) if down else 0))
   elif e['C']==C:
    if typ=='INIT':formal[i]=0
    elif typ=='ADD':formal[i]^=formal[e['j']]
    elif typ=='CLEAR':del formal[i]
  N=[row&((1<<len(U))-1) for row in out];M=[row>>len(U) for row in out]
  need(actual==[linear(a,U)^linear(b,Pin) for a,b in zip(N,M)],'actual cell equation')
  R,J,h=complement(M,len(Pin));T=[linear(row,Pin) for row in h]
  rhs=[v^linear(a,U) for v,a in zip(actual,N)]
  need(Pin==[linear(r,rhs)^linear(j,T) for r,j in zip(R,J)],'occurrence reconstruction')
  need(actual==[linear(a,U)^linear(linear(b,R),rhs) for a,b in zip(N,M)],'actual image equation')
  G+=T
  if Pin or out:cells.append(dict(dimension=len(C),incoming=len(Pin),outgoing=len(out),rank=rank(M),kernel_dimension=len(h),kernel_x_rank=rank([x&((1<<111)-1) for x in T])))
 D=sum(e['op']=='MOVE' and e['delta']<0 for e in events)
 Dp=sum(e['op']=='MOVE' and not e['owned'] and e['delta']<0 for e in events)
 O=sum(e['op']=='MOVE' and e['owned'] and e['delta']!=0 for e in events)
 need(D==len(Z)+sum(c['incoming'] for c in cells),'downward occurrence partition')
 need(len(G)<=D,'G dimension bound')
 y=[1<<i for i in range(111,222)];cache={};checked=0
 for C,row,k,i in re['history']:
  if len(C)==8:continue
  if C not in cache:
   local=[1<<j for j,c in enumerate(w['start'][:111]) if contained(frames[c],C)]
   cache[C]=basis(G+y+local)
  need(in_span(row,cache[C]),f'normal form at actual event {k} record {i}');checked+=1
 incidences=sum(e['op']=='MOVE' and e['owned'] and ((e['delta']>0 and len(e['Cnext'])==7) or (e['delta']<0 and len(e['C'])==7)) for e in events)
 need(incidences<=O,'injective owned facet charges')
 return dict(owned_moves=O,owned_downward_moves=D-Dp,public_downward_moves=Dp,all_downward_moves=D,ground_arrivals=len(Z),historical_coordinates=len(G),historical_x_rank=rank([x&((1<<111)-1) for x in G]),historical_full_rank=rank(G),actual_proper_histories_checked=checked,owned_facet_incidences=incidences,cells=cells),G
def main(a):
 need(digest(a.native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
 n=read(a.native);w=read(a.word);re=replay(w,n);norm,G=normalize(w,n,re)
 receipt=dict(status='PASS_INDEPENDENT_ACTUAL_ALL_ROUTE_OCCURRENCE_NORMALIZATION',native_sha256=digest(a.native),word_sha256=digest(a.word),public_columns=222,counts=dict(re['counts']),move_profile=dict(re['moves']),peak_owned=re['peak'],normalization=norm,scope='Exact finite all-input symbolic word and actual local-history normal forms; universal theorem requires the separately reviewed written argument.',new_kappa=None)
 a.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:receipt[k] for k in ['status','counts','peak_owned']}));print(json.dumps({k:v for k,v in norm.items() if k!='cells'}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','word','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
