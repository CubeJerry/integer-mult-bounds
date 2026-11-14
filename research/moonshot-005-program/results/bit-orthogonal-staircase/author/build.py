#!/usr/bin/env python3
"""Full logical BIT source from masked orthogonal-class staircases."""
import argparse,gzip,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
def need(x,s):
 if not x:raise ValueError(s)
def basis(A):
 A=[list(map(F,r)) for r in A];p=0
 for j in range(8):
  k=next((k for k in range(p,len(A)) if A[k][j]),None)
  if k is None:continue
  A[p],A[k]=A[k],A[p];c=A[p][j];A[p]=[x/c for x in A[p]]
  for i in range(len(A)):
   if i!=p and A[i][j]:c=A[i][j];A[i]=[x-c*y for x,y in zip(A[i],A[p])]
  p+=1
 return tuple(tuple(r) for r in A[:p])
def perp(A):
 B=basis(A);piv=[next(i for i,x in enumerate(r) if x) for r in B];out=[]
 for j in range(8):
  if j in piv:continue
  v=[F(0)]*8;v[j]=1
  for p,r in zip(piv,B):v[p]=-r[j]
  out.append(v)
 return basis(out)
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');n=json.loads(gzip.decompress(raw));part=a.partition.read_bytes();need(hashlib.sha256(part).hexdigest()=='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117','partition pin');groups=json.loads(part)['groups']
 need(sorted(j for g in groups for j in g)==list(range(111)),'disjoint complete partition');roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 need(all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for g in groups for i in g for j in g if i!=j),'all classes mutually orthogonal')
 ids=set(n['start'][:222])|set(n['final'][:222]);frames={i:n['frames'][str(i)] for i in sorted(ids)};key={basis(v['B']):i for i,v in frames.items()};nextid=max(map(int,n['frames']))+1;ops=[];loc=dict(enumerate(n['start'][:222]));rows={i:{i} for i in range(222)};bill=Counter();moves=Counter();rankmoves=Counter();peak=0;firstground={};markers=[]
 def chart(B):
  nonlocal nextid
  B=basis(B)
  if B in key:return key[B]
  i=nextid;nextid+=1;key[B]=i;frames[i]=dict(dim=len(B),A=[[str(x) for x in r] for r in perp(B)],B=[[str(x) for x in r] for r in B]);return i
 def flag(lo,hi):
  if lo==hi:return [lo]
  L=basis(frames[lo]['B']);H=basis(frames[hi]['B']);need(len(L)<len(H) and basis(L+H)==H,'flag inclusion');path=[lo]
  for v in H:
   B=basis(L+(v,))
   if len(B)==len(L):continue
   L=B;path.append(hi if len(L)==len(H) else chart(L))
  need(path[-1]==hi,'complete flag');return path
 def emit(o):
  nonlocal peak
  op,i=o[:2];bill[op]+=1;ops.append(o)
  if op=='ADD':
   _,i,j,c=o;need(i!=j and loc.get(i)==loc.get(j)==c,'cochart ADD');rows[i]^=rows[j]
  elif op=='MOVE':
   _,i,x,y=o;need(loc.get(i)==x,'MOVE source');delta=frames[y]['dim']-frames[x]['dim'];need(delta==(1 if i<222 else -1),'unit monotonicity');need(len(basis(frames[x]['B']+frames[y]['B']))==max(frames[x]['dim'],frames[y]['dim']),'MOVE real inclusion');loc[i]=y;moves[i]+=1;rankmoves[abs(delta)]+=1
   if i>=222 and y==0 and i not in firstground:firstground[i]=sorted(rows[i])
  elif op=='INIT':need(i>=222 and i not in loc,'fresh owned');loc[i]=o[2];rows[i]=set();peak=max(peak,len(loc)-222)
  elif op=='CLEAR':need(i>=222 and loc.get(i)==o[2],'owned erasure');del loc[i];del rows[i]
  else:raise ValueError(op)
 def move(i,c):
  x=loc[i]
  if x==c:return
  path=flag(x,c) if frames[x]['dim']<frames[c]['dim'] else list(reversed(flag(c,x)))
  for u,v in zip(path,path[1:]):emit(['MOVE',i,u,v])
 # All class-local acquisitions precede any descending packet.
 chains=[]
 for g in groups:
  s=len(g);C=[1]+[chart(perp([roots[j] for j in g[:i]])) for i in range(1,s+1)];chains.append(C)
  for i in range(1,s):emit(['ADD',111+g[i],111+g[i-1],0])
  for i,j in enumerate(g,1):move(111+j,C[i])
  for j in range(s-1):move(g[j],C[j])
  last=g[-1];move(last,C[s-1])
  for i in range(s-1,0,-1):
   emit(['ADD',111+g[i-1],last,C[i]])
   if i>1:
    move(last,C[i-1]);emit(['ADD',last,g[i-1],C[i-1]]);move(g[i-1],1)
   else:move(last,1)
  for j in g[1:-1]:emit(['ADD',last,j,1])
  need(all(rows[j]=={j} and loc[j]==1 for j in g),'class originals restored')
  for i,j in enumerate(g):need(rows[111+j]==({111+k for k in g[:i+1]}|set(g[i+1:])),'exact masked tail preload')
 need(all(rows[i]=={i} and loc[i]==1 for i in range(111)),'all111 X restored before first packet')
 prefix_end=len(ops);preloads={str(i):sorted(rows[111+i]) for i in range(111)}
 for c,(g,C) in enumerate(zip(groups,chains)):
  p=222+c;start=len(ops);emit(['INIT',p,1])
  for j in g:emit(['ADD',p,j,1])
  for i,j in enumerate(g,1):
   move(p,C[i]);need(rows[p]==({111+k for k in g[:i-1]}|set(g[i-1:])),'incoming packet invariant')
   emit(['ADD',111+j,p,C[i]]);emit(['ADD',p,111+j,C[i]])
   need(rows[111+j]=={111+j,j},'completed arbitrary-Y target');need(rows[p]==({111+k for k in g[:i]}|set(g[i:])),'outgoing packet invariant');move(111+j,n['final'][111+j])
  move(p,0);need(rows[p]=={111+j for j in g},'exact nonzero arbitrary-Y clear operand');emit(['CLEAR',p,0]);markers.append(dict(group=c,ports=g,charts=C,begin=start,end=len(ops)))
 need(set(rows)==set(range(222)) and all(loc[i]==n['final'][i] for i in rows),'all original chart endpoints');need(all(rows[i]=={i} for i in range(111)) and all(rows[111+i]=={111+i,i} for i in range(111)),'full all222-column target map')
 need(bill=={'ADD':687,'MOVE':1674,'INIT':15,'CLEAR':15} and peak==1,'full invoice');need(all(moves[i]==7 for i in range(222)) and all(moves[i]==8 for i in range(222,237)),'all route ranks')
 word=dict(schema='S011-complete-masked-orthogonal-staircase-source-v1',public=222,owned_fields=15,start=n['start'][:222],final=n['final'][:222],hub=1,frames={str(i):v for i,v in sorted(frames.items())},program=ops,groups=groups,class_chains=chains,scope='Complete finite logical222-input map;15 packets fail retained target budget. General physical compiler, recursive supplier and foundations not proved.')
 a.output.mkdir(parents=True,exist_ok=True);data=json.dumps(word,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(data,mtime=0);(a.output/'WORD.json.gz').write_bytes(blob)
 receipt=dict(status='PASS_AUTHOR_COMPLETE_ORTHOGONAL_STAIRCASE',native_sha256=hashlib.sha256(raw).hexdigest(),partition_sha256=hashlib.sha256(part).hexdigest(),word_sha256=hashlib.sha256(blob).hexdigest(),bill=dict(bill),unit_MOVE_profile=dict(rankmoves),peak_owned=peak,original_X_restored_before_packets=True,all111_Y_completed=True,input_columns=222,prefix_end=prefix_end,group_sizes=[len(g) for g in groups],preloads=preloads,first_ground_rows=firstground,class_intervals=markers,full_physical_supplier_claimed=False,new_kappa=None)
 (a.output/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps({k:receipt[k] for k in ['status','bill','peak_owned','word_sha256']}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','partition','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
