#!/usr/bin/env python3
"""Actual two point loans, coded Y preloads, and a 17-rank52-charge fitting."""
import argparse,gzip,hashlib,json,itertools
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PREFIX_PIN='074bdf752f03f6060ebf7e9fb548d78a94f866c4425395693388dc43e7c30f47'
GEOMETRY_PIN='a4df2f5cafc8c02d3a206f49ee9ab8e5cb45bd0ef92b4acaebd0c33e1387a7c2'
def need(b,m):
 if not b:raise ValueError(m)
def dot(a,b):return sum(F(x)*F(y) for x,y in zip(a,b))
def rank(rows):
 p={}
 for r in rows:
  while r:
   k=r.bit_length()-1
   if k in p:r^=p[k]
   else:p[k]=r;break
 return len(p)
def rr(rows):
 A=[list(map(F,r)) for r in rows];z=0
 for c in range(8):
  h=next((h for h in range(z,len(A)) if A[h][c]),None)
  if h is None:continue
  A[z],A[h]=A[h],A[z];v=A[z][c];A[z]=[x/v for x in A[z]]
  for h in range(z+1,len(A)):
   v=A[h][c];A[h]=[x-v*y for x,y in zip(A[h],A[z])]
  z+=1
 return z

def replay(w,n,code,closed=False):
 loc=dict(enumerate(w['start']));rows={k:1<<k for k in range(222)};born=set(loc);count=Counter();prof=Counter();peak=0;clear=[]
 for op in w['program']:
  t,k=op[:2];count[t]+=1
  if t=='INIT':need(k>=222 and k not in born,'fresh owner');born.add(k);loc[k]=op[2];rows[k]=0;peak=max(peak,len(loc)-222)
  elif t=='ADD':_,k,l,C=op;need(k!=l and loc.get(k)==loc.get(l)==C,'actual cochart ADD');rows[k]^=rows[l]
  elif t=='MOVE':
   _,k,a,b=op;need(loc.get(k)==a,'actual MOVE source');fa,fb=w['frames'][str(a)],w['frames'][str(b)];d=fb['dim']-fa['dim'];need(d!=0,'nontrivial MOVE');sm,lg=(fa,fb) if d>0 else(fb,fa);need(all(dot(u,v)==0 for u in sm['B'] for v in lg['A']),'exact real nested MOVE');need((d>0) if k<222 else(k in[334,335,336,337] and d<0),'declared monotone physical paths');loc[k]=b;prof[abs(d)]+=1
  elif t=='CLEAR':need(k>=222 and loc.get(k)==op[2],'actual owned clear');clear.append({'record':k,'chart':op[2],'value_hex':hex(rows[k])});del loc[k];del rows[k]
  else:raise ValueError(t)
 ground=n['start'][111];T={92,15}
 for k in range(111):
  need(rows[k]==1<<k and loc[k]==n['final'][k],'original X restored')
  preload=(1<<k) if k in T else sum((1<<t) for t in T if code[k]>>t&1)
  need(rows[111+k]==(1<<(111+k))^preload,'complete222-column partial/preload map')
  need(loc[111+k]==(n['final'][111+k] if closed or k in T else ground),'actual Y endpoint')
 if closed:need(set(loc)==set(range(222)),'closed ownership')
 else:
  need(set(loc)==set(range(335))|{336,337},'exact live owners')
  for k in range(111):need(rows[222+k]==1<<k and loc[222+k]==n['start'][k],'actual stationary point copy')
  need(rows[336]==1<<92 and rows[337]==1<<15 and loc[336]==loc[337]==ground,'both paid pure source coordinates at ground')
  R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)];Ki=sum(int(k==92 or dot(R[92],R[k])==0)<<k for k in range(111));Kj=sum(int(k==54 or dot(R[54],R[k])==0)<<k for k in range(111));need(rows[333]==Ki and loc[333]==636 and rows[334]==(Ki&Kj) and loc[334]==ground,'unchanged actual purified/quadratic histories')
 return {'counts':dict(count),'profile':dict(sorted(prof.items())),'rank_length':sum(k*v for k,v in prof.items()),'peak_owned':peak,'live_owned':len(loc)-222,'clears':clear},loc,rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--prefix',type=Path,required=True);ap.add_argument('--pivot-geometry',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw));R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)];K=[sum(int(k==l or dot(R[k],R[l])==0)<<l for l in range(111)) for k in range(111)];full=(1<<111)-1;i=92;A=[K[j]&(K[i] if K[i]>>j&1 else full^K[i]) for j in range(111)];T={92,15};tm=sum(1<<t for t in T);B=[1<<j if j in T else A[j]&~tm for j in range(111)];ell=K[92]&K[54];need(rank(A)==15 and rank(A+[1<<t for t in T])==17 and rank(B)==17 and rank(B+[ell,K[92]])==18 and rank(K+B)==18,'exact rank and prefix compatibility')
 graw=a.pivot_geometry.read_bytes();need(hashlib.sha256(graw).hexdigest()==GEOMETRY_PIN,'exact predecessor geometry pin');geo=json.loads(graw);need(geo['source_sha256']==PIN and geo['pivot']==92,'source-matched predecessor covers');grows={r['receiver']:r for r in geo['rows']};georows=[];z=R[15];z=[v*(1 if dot(z,R[i])>0 else -1) for v in z];need(dot(z,R[i])==2 and dot(z,z)==4,'oriented actual point15 root')
 for j in range(111):
  need(B[j]>>j&1 and B[j]&~K[j]==0,'actual fitting zeros and own1');support=[k for k in range(111) if k!=j and B[j]>>k&1]
  if j in T:need(not support,'completed coordinate row');normals=[];chi=0
  elif K[i]>>j&1:normals=[R[i]];chi=0
  elif grows[j]['chi']==1:normals=[list(map(F,v)) for v in grows[j]['normals']];chi=1
  else:normals=[z,[u-v for u,v in zip(z,R[i])]];chi=1;need(j in[21,33,45,51,68,76,84,99] and A[j]>>15&1,'one actual loan hits every old irreducible row')
  if support:
   need(all(rr([R[j],v])==2 for v in normals),'each normal gives a proper receiver-flat');need(all(any(dot(R[k],v)==0 for v in normals) for k in support),'literal proper-chart cover');sr=rr([R[k] for k in support]);need(sr==(6 if chi==0 else 7),'exact support rank and minimal number of flats')
  else:sr=0
  georows.append({'receiver':j,'foreign_support':support,'foreign_rank':sr,'chi':chi,'normals':[[str(x) for x in v] for v in normals]})
 need(Counter(r['chi'] for r in georows)=={0:59,1:52},'exact chi52 fitting with no three-chart rows')
 praw=a.prefix.read_bytes();need(hashlib.sha256(praw).hexdigest()==PREFIX_PIN,'exact paid-prefix pin');p=json.loads(gzip.decompress(praw));ground=n['start'][111];ops=[]
 for own,t in [(336,92),(337,15)]:ops.extend([['INIT',own,n['start'][t]],['ADD',own,222+t,n['start'][t]],['MOVE',own,n['start'][t],ground]])
 ops.extend([['ADD',126,337,ground],['MOVE',126,ground,n['final'][126]]])
 for j in range(111):
  if j in T:continue
  for own,t in [(336,92),(337,15)]:
   if A[j]>>t&1:ops.append(['ADD',111+j,own,ground])
 prefix={**p,'program':p['program']+ops,'owned_fields':p['owned_fields']+[336,337],'end_owned':p['end_owned']+[336,337],'final':n['final'][:111]+[n['final'][111+k] if k in T else ground for k in range(111)],'scope':'Two completed outputs, actual paid coordinate preloads and pure modes; no full source.'}
 closing=[['MOVE',111+k,ground,n['final'][111+k]] for k in range(111) if k not in T]+[['CLEAR',222+k,n['start'][k]] for k in range(111)]+[['CLEAR',333,636],['CLEAR',334,ground],['CLEAR',336,ground],['CLEAR',337,ground]]
 closed={**prefix,'program':prefix['program']+closing,'final':n['final'][:222],'end_owned':[],'scope':'Closed partial/preloaded map; not a complete multiplier source.'};rp,loc,rows=replay(prefix,n,A);rc,_,_=replay(closed,n,A,True);need(rc['profile']=={1:31,2:32,5:32,6:27,7:164} and rc['rank_length']==1565,'two real extra rank1 source loans')
 future_roles=[k for k in range(111) if k not in{92,54,84,15}];basis=[]
 for j in future_roles:
  r=sum((K[j]>>k&1)<<a for a,k in enumerate(future_roles))
  if rank(basis+[r])>len(basis):basis.append(r)
 vals=[0]
 for b in basis:vals += [v^b for v in vals]
 spectrum=Counter(v.bit_count() for v in vals if v);need(len(basis)==9 and min(spectrum)==46 and sum((ell>>k)&1 for k in future_roles)==32,'strict-capacity punctured distance survives paid15')
 seven=[2,8,9,14,21,46,88];need(all(dot(R[u],R[v])!=0 for u,v in itertools.combinations(seven,2)) and all(not(K[92]>>t&1) for t in seven),'matching7clique avoids paid targets')
 def inside(C):return any(all(dot(v,R[t])==0 for v in prefix['frames'][str(C)]['B']) for t in seven)
 O=[rows[k] for k,C in loc.items() if inside(C)];demand=[(1<<t)^(1<<(111+t)) for t in seven];rank0=rank(O);rank1=rank(O+demand);need(rank1-rank0==7,'actual new matchingseven deficit')
 controls=[]
 for omitted in range(9):
  mutant={**prefix,'program':p['program']+[o for k,o in enumerate(ops) if k!=omitted]}
  try:replay(mutant,n,A)
  except(KeyError,ValueError):controls.append('delete extension operation'+str(omitted))
  else:raise ValueError('accepted destructive extension mutation')
 a.outdir.mkdir(parents=True,exist_ok=True);pins={}
 for name,w in [('PREFIX.json.gz',prefix),('CLOSED-PARTIAL.json.gz',closed)]:
  payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();r=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(r);pins[name]={'gzip_sha256':hashlib.sha256(r).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 out={'status':'PASS_ACTUAL_TWO_POINT_PRELOAD_AND_CHI52_FITTING','native_sha256':PIN,'input_prefix_sha256':hashlib.sha256(praw).hexdigest(),'input_geometry_sha256':hashlib.sha256(graw).hexdigest(),'completed_targets':sorted(T),'preload_counts':{str(t):sum(j not in T and bool(A[j]>>t&1) for j in range(111)) for t in T},'fitting':{'rank':17,'canonical_enlargement_rank':18,'with_actual_retained_modes_rank':18,'rows_hex':[hex(v) for v in B],'chi':52,'chi_histogram':{'0':59,'1':52},'geometry':georows},'prefix':rp,'closed_partial':rc,'future_obligations':{'matching_cut':{'receivers':seven,'observation_rank':rank0,'target_augmented_rank':rank1,'deficit':7},'punctured_roles':future_roles,'canonical_rank':9,'canonical_weight_spectrum':dict(sorted(spectrum.items())),'canonical_minimum_weight':46,'retained_ell_weight':32,'whole_V_future_events_at_least':9,'qualification':'Uses prior all-V punctured rigidity;15is outside all35seed and parity roles. No lifetime-count lower bound.'},'negative_controls':controls,'word_pins':pins,'complete_source':False,'new_kappa':None,'qualification':'Actual point loans/preloads and finite fully certified static fitting. No realization of the17-dimensional code or decoder continuation.'};(a.outdir/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'code_rank':17,'chi':52,'prefix_counts':rp['counts'],'closed_profile':rc['profile'],'preloads':out['preload_counts']}))
if __name__=='__main__':main()
