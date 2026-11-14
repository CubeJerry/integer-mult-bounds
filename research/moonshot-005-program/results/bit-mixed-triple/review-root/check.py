#!/usr/bin/env python3
"""Independent extension of lead's sparse-set joint-word verifier."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,gzip,hashlib,json
def need(x,s):
 if not x:raise ValueError(s)
def rank(rows):
 b={}
 for row in rows:
  r=list(map(F,row))
  for p,v in sorted(b.items()):
   if r[p]:c=r[p];r=[x-c*y for x,y in zip(r,v)]
  p=next((p for p,x in enumerate(r) if x),None)
  if p is not None:c=r[p];b[p]=[x/c for x in r]
 return len(b)
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');n=json.loads(gzip.decompress(raw));packed=a.word.read_bytes();w=json.loads(gzip.decompress(packed))
 need(w['public']==222 and w['start']==n['start'][:222] and w['final']==n['final'][:222] and w['owned_fields']==3,'original source interface')
 roots=[[F(x) for x in n['frames'][str(n['start'][i])]['B'][0]] for i in range(111)]
 groups=Counter(tuple(i for i in range(3) if r[i]==0) for r in roots[8:]);need(groups=={():7,(0,):12,(1,):16,(2,):16,(0,1):15,(0,2):15,(1,2):15,(0,1,2):7},'exact zero-mask geometry')
 frames={int(k):v for k,v in w['frames'].items()}
 for v in frames.values():
  A=[[F(x) for x in r] for r in v['A']];B=[[F(x) for x in r] for r in v['B']];need(rank(A)==8-v['dim'] and rank(B)==v['dim'] and all(sum(x*y for x,y in zip(r,s))==0 for r in A for s in B),'exact chart complement')
 pairs={tuple(o[2:]) for o in w['program'] if o[0]=='MOVE'}
 for x,y in pairs:need(abs(frames[x]['dim']-frames[y]['dim'])==1 and rank(frames[x]['B']+frames[y]['B'])==max(frames[x]['dim'],frames[y]['dim']),'nested unit map')
 K=[{j for j,r in enumerate(roots) if i==j or sum(x*y for x,y in zip(roots[i],r))==0} for i in range(3)];H=[K[i]^{i} for i in range(3)];hub=w['hub'];ground=n['start'][111];facets=n['final'][111:114]
 def replay(ops,contract=True):
  rows={i:{i} for i in range(222)};loc=dict(enumerate(w['start']));counts=Counter();moves=Counter();births=[];peak=0;arr=[[],[],[]];erased=[]
  for o in ops:
   op,i=o[:2];counts[op]+=1
   if op=='INIT':
    need(222<=i<225 and i not in rows and i not in births and o[2]==hub,'sequential packet birth');births.append(i);j=i-222
    need(all(rows[r]=={r} and loc[r]==hub for r in range(111)),'all111 X restored before every packet birth');need(rows[111+j]==({111+j}|H[j]),'actual preloaded mixed Y');rows[i]=set();loc[i]=hub;peak=max(peak,len(rows)-222)
   elif op=='MOVE':
    _,i,x,y=o;need(loc.get(i)==x and (x,y) in pairs,'actual nested MOVE');d=frames[y]['dim']-frames[x]['dim'];need(d==(1 if i<222 else -1),'single monotone original/packet route')
    if i>=222:
     j=i-222
     if x==hub:need(rows[i]==K[j],'paid current-Hub canonical payload')
     if x==facets[j]:need(rows[111+j]=={111+j,j} and rows[i]==({111+j}|H[j]),'masked singular exchange')
    for j,f in enumerate(facets):
     if i<111 and y==f:arr[j].append(i)
    loc[i]=y;moves[i]+=1
   elif op=='ADD':
    _,i,j,c=o;need(i!=j and i in rows and j in rows and loc[i]==loc[j]==c,'actual cochart read');rows[i]^=rows[j]
   elif op=='CLEAR':
    j=i-222;need(0<=j<3 and loc[i]==o[2]==ground and rows[i]==({111+j}|H[j]),'paid nonzero unknown-Y erasure');erased.append({'field':i,'input_columns':sorted(rows[i])});del rows[i];del loc[i]
   else:raise ValueError(op)
  need(set(rows)==set(range(222)) and all(loc[i]==w['final'][i] for i in rows),'all public final charts')
  need(all(rows[i]=={i} for i in range(111)) and all(rows[111+i]==({111+i,i} if i<3 else {111+i}) for i in range(111)),'full222-column endpoint map')
  if contract:
   need(counts=={'MOVE':1578,'ADD':391,'INIT':3,'CLEAR':3} and peak==1,'full partial invoice');need(all(moves[i]==7 for i in range(222)) and all(moves[i]==8 for i in range(222,225)),'all path totals');need([sorted(v) for v in arr]==[[1,8],[2,14],[0,22]],'two actual X facet arrivals each')
  return dict(counts=dict(counts),peak_owned=peak,facet_X_arrivals=arr,nonzero_erasure_rows=erased)
 result=replay(w['program']);ops=w['program'];mutants=[]
 # Delete an actual deposition in each original-Y stage and each final exchange.
 for j in range(3):
  inds=[t for t,o in enumerate(ops) if o[0]=='ADD' and o[1]==111+j and o[2]<111]
  for k,t in enumerate(inds):mutants.append((f'missing_Y{j}_local_read_{k}',ops[:t]+ops[t+1:]))
  p=222+j;inds=[t for t,o in enumerate(ops) if o[0]=='ADD' and o[3]==facets[j] and (o[1]==p or o[2]==p)];need(len(inds)==2,'two-ADD exchange only');bad=[o[:] for o in ops];x,y=inds;bad[x],bad[y]=bad[y],bad[x];mutants.append((f'reversed_exchange_{j}',bad))
 t=next(t for t,o in enumerate(ops) if o[0]=='ADD' and o[1]==3 and o[3]==hub);mutants.append(('missing_borrowed_X3_restoration',ops[:t]+ops[t+1:]))
 rejected=[]
 for label,bad in mutants:
  try:replay(bad,False)
  except ValueError as err:rejected.append({'name':label,'reason':str(err)})
  else:raise ValueError('mutant accepted '+label)
 out=dict(status='PASS_INDEPENDENT_THREE_TARGET_WORD',native_sha256=hashlib.sha256(raw).hexdigest(),word_sha256=hashlib.sha256(packed).hexdigest(),zero_masks={str(k):v for k,v in groups.items()},chart_count=len(frames),nested_pairs=len(pairs),result=result,negative_controls=rejected,scope='Finite exact222-column scalar logical word; arbitrary-input identities tensor in characteristic two.108 Y outputs, physical uniform compiler and full supplier remain open.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'counts':result['counts'],'negative_controls':len(rejected)}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','word','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
