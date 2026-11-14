#!/usr/bin/env python3
"""Independent real-chart,222-column review of actual cubic/D4 histories."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
 if not c:raise ValueError(m)
def dot(a,b):return sum(F(x)*F(y)for x,y in zip(a,b))
def basis(words):
 out={}
 for w in words:
  while w:
   p=w.bit_length()-1
   if p in out:w^=out[p]
   else:out[p]=w;break
 return out
def qr(rows):
 a=[list(map(F,r))for r in rows];r=0
 for j in range(8):
  k=next((i for i in range(r,len(a))if a[i][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[r])]
  r+=1
 return r
def load(p):return json.loads(gzip.decompress(p.read_bytes()))
def replay(w):
 rows={i:1<<i for i in range(222)};loc=dict(enumerate(w['start']));seen=set(rows);ct=Counter();moves=Counter();peak=dirty=0;checked=set()
 for e in w['program']:
  op,r=e[:2];ct[op]+=1
  if op=='INIT':need(r>=222 and r not in seen,'fresh owner');seen.add(r);rows[r]=0;loc[r]=e[2];peak=max(peak,len(rows)-222)
  elif op=='ADD':
   _,r,s,c=e;need(r!=s and loc[r]==loc[s]==c,'actual cochart');rows[r]^=rows[s]
  elif op=='MOVE':
   _,r,a,b=e;need(loc[r]==a,'actual MOVE entrance');A,B=w['frames'][str(a)],w['frames'][str(b)];delta=B['dim']-A['dim'];need(delta and(r>=222 or delta>0),'public monotonicity')
   if(a,b)not in checked:
    small,large=(A,B)if delta>0 else(B,A);need(all(dot(x,y)==0 for x in small['B']for y in large['A']),'exact real containment');checked.add((a,b))
   loc[r]=b;moves[abs(delta)]+=1
  elif op=='CLEAR':need(r>=222 and loc[r]==e[2],'actual clear');dirty+=bool(rows[r]);del rows[r];del loc[r]
  else:raise ValueError(op)
 need(sorted(r for r in rows if r>=222)==w['end_owned'],'literal terminal owners')
 return rows,loc,{'events':sum(ct.values()),'operations':dict(ct),'moves':dict(sorted(moves.items())),'peak_owned':peak,'dirty_clears':dirty}
def run(repo,package):
 p=repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';need(hashlib.sha256(p.read_bytes()).hexdigest()==PIN,'source pin');native=load(p)
 roots=[native['frames'][str(native['start'][i])]['B'][0]for i in range(111)];K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(roots))for i,r in enumerate(roots)]
 cb=list(basis(K).values());Q2=list(basis(a&b for a,b in itertools.combinations_with_replacement(cb,2)).values());need(len(cb)==9 and len(Q2)==36,'canonical and quadratic ranks')
 cases=[]
 for name,S,expected in [('cubic',(8,10,12),{1:7,2:1,3:13,4:13,5:3,6:2,7:205}),('d4',(8,10,12,13),{1:9,2:2,3:13,4:15,5:2,6:2,7:204})]:
  path=package/name/'PREFIX.json.gz';word=load(path);closedpath=package/name/'CLOSED-PARTIAL.json.gz';closed=load(closedpath)
  need(word['public']==222 and word['start']==native['start'][:222],'original interface')
  for k,frame in native['frames'].items():need(word['frames'][k]==frame,'native frame unchanged')
  for k,frame in word['frames'].items():
   if k not in native['frames']:need(qr(frame['B'])==frame['dim']and qr(frame['A'])==8-frame['dim']and all(dot(x,y)==0 for x in frame['B']for y in frame['A']),'new exact real frame')
  need(closed['program'][:len(word['program'])]==word['program']and closed['frames']==word['frames'],'literal paid closure')
  rows,loc,bill=replay(word);rr,ll,cbill=replay(closed)
  h=(1<<111)-1
  for i in S:h&=K[i]
  h^=sum(1<<i for i in S);need(h.bit_count()==(13 if name=='cubic'else 12),'section support')
  need(rows[334]==h and loc[334]==0,'genuinely acquired pure ground mode');need(rows[333]==sum(1<<(111+i)for i in S),'dirty Y residue')
  C=word['frames'][str(loc[333])];need(C['dim']==8-len(S)and all(dot(x,roots[i])==0 for x in C['B']for i in S),'exact section chart')
  for i in range(111):
   target=(1<<(111+i))^((1<<i)if i in S else 0)
   need(rows[i]==1<<i and loc[i]==native['final'][i],'all original X restored')
   need(rows[222+i]==1<<i and loc[222+i]==native['start'][i],'actual point copies')
   need(rows[111+i]==target and loc[111+i]==(native['final'][111+i]if i in S else 0),'selected target and remaining ground originals')
   need(rr[i]==1<<i and rr[111+i]==target and ll[i]==native['final'][i]and ll[111+i]==native['final'][111+i],'complete222column closed partial map')
  need(set(rr)==set(range(222))and cbill['dirty_clears']==113 and cbill['moves']==expected,'full closure and invoice')
  need(sum(k*v for k,v in cbill['moves'].items())==1562,'complete rank length')
  patches=[1<<i for i in set(range(8))|set(S)];before=len(basis(Q2+patches));after=len(basis(Q2+patches+[h]));need(after==before+1,'history outside quadratic plus patches')
  bad=json.loads(json.dumps(word));j=next(j for j,e in enumerate(bad['program'])if e[0]=='ADD'and e[1]==333);del bad['program'][j];badrows,_,_=replay(bad);need(badrows[334]!=h,'missing true acquisition control')
  cases.append({'name':name,'prefix_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'closure_sha256':hashlib.sha256(closedpath.read_bytes()).hexdigest(),'completed':S,'history_support':[i for i in range(111)if h>>i&1],'prefix':bill,'closure':cbill,'quadratic_with_patches_rank':before,'with_history_rank':after,'missing_acquisition_rejected':True})
 return{'status':'PASS_INDEPENDENT_CUBIC_AND_D4_SOURCE_REPLAY','native_sha256':PIN,'cases':cases,'all_input_columns':222,'only_partial_sources':True,'no_new_kappa':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repo,a.package);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
