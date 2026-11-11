#!/usr/bin/env python3
"""Separate dyadic reconstruction of both relay-acquisition provisional profiles."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def powers(r):
 D=1<<96;target=pow(r,199)*pow(D,200);lo,hi=0,r*D+1
 while hi-lo>1:
  m=(lo+hi)//2
  if pow(m,200)<=target:lo=m
  else:hi=m
 need(pow(lo,200)<=target<pow(lo+1,200),'exact root bracketing')
 return F(lo,D),F(lo+1,D)
def weighted(c,B):
 a=b=F(0)
 for r,n in c.items():
  x,y=B[r];a+=n*(x if n>=0 else y);b+=n*(y if n>=0 else x)
 return a,b
def intersect(x,y):return max(x[0],F(y[0]))<=min(x[1],F(y[1]))
def span(b):
 s={0}
 for x in b:s|={v^x for v in tuple(s)}
 return frozenset(s)
def run(a):
 need(sha(a.source)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin')
 need(sha(a.invoice)=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','invoice pin')
 src=json.load(gzip.open(a.source,'rt'));word=json.load(gzip.open(a.lifetime_word,'rt'));invoice=json.loads(a.invoice.read_text());author=json.loads((a.author/'RESULT.json').read_text())
 need(hashlib.sha256(gzip.decompress(a.lifetime_word.read_bytes())).hexdigest()==author['eight_word_payload_sha256'],'literal eight word payload')
 def owned(w):
  out=collections.Counter()
  for e in w['program']:
   if e[0]=='MOVE' and e[4]:out[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
  return out
 O=owned(src);R=owned(word);S=O-R
 need(dict(S)=={1:6,2:3,3:1,4:2,5:1,6:1},'source and actual eight-word route census')
 T={int(k):v for k,v in invoice['T4'].items()};P=collections.Counter({int(k):v for k,v in invoice['P4'].items()})
 for r,n in R.items():P[r]+=18*n
 need(dict(T)=={int(k):v for k,v in author['new_T'].items()},'unchanged complete targets')
 allr=set(T)|set(P)|{1,2,3,7,9};B={r:powers(r) for r in allr};base=weighted({r:T.get(r,0)-P.get(r,0) for r in allr},B)
 need(intersect(base,author['S8_raw_margin_interval']),'S8 independent interval agreement')
 ans={}
 for name,c in [('four_aggregates',{7:2,2:2}),('eight_facet_copies',{1:8,2:2})]:
  Q=P.copy()
  for r,n in c.items():Q[r]+=18*n
  v=author['variants'][name];need(dict(Q)=={int(k):n for k,n in v['new_P'].items()},'all eighteen calls charged')
  margin=weighted({r:T.get(r,0)-Q.get(r,0) for r in allr},B);fee=weighted(c,B);head=tuple(x/18 for x in margin)
  need(margin[0]>0 and intersect(margin,v['raw_margin_interval']) and intersect(fee,v['per_native_added_paid_moment_interval']) and intersect(head,v['remaining_paid_moment_per_native_interval']),'positive margins and all independently bounded prices')
  paid=sum(Q.values());targets=sum(T.values());surplus=sum(r*(T.get(r,0)-Q.get(r,0)) for r in allr)
  need((paid,targets,surplus)==(v['paid_positions'],v['target_positions'],v['rank_surplus']),'complete integer counts')
  need(head[0]//1==head[1]//1==v['further_positive_rank_arrival_ceiling'],'integer additional-arrival ceiling')
  ans[name]={'paid_positions':paid,'target_positions':targets,'rank_surplus':surplus,'fee_interval':list(map(str,fee)),'headroom_interval':list(map(str,head))}
 C=list(map(span,src['frames']));M=set(src['live'])|{i+112 for i in src['live']}|set(src['hosted']['X2'])|set(src['hosted']['Y2']);nonentry=[i for i in M if len(C[src['initial'][i]])>1]
 need(len(nonentry)==200 and all(C[src['final'][i]]==C[127] for i in nonentry),'all nonentry funded final hub')
 need(C[3]<C[541]<C[127] and (len(src['frames'][3]),len(src['frames'][541]),len(src['frames'][127]))==(0,7,9),'proper nested new routes')
 for i,f in author['entry_support_final_facets'].items():need(src['final'][int(i)]==f and len(C[src['initial'][int(i)]])==1 and C[f]<C[127] and len(src['frames'][f])==8,'entry final facet')
 direct=tuple(F(x) for x in ans['four_aggregates']['headroom_interval']);facet=tuple(F(x) for x in ans['eight_facet_copies']['headroom_interval'])
 need(direct[1]-2*B[2][0]<0,'negative control: no extra paused repair on direct variant')
 need(direct[1]-B[3][0]<0 and facet[1]-B[9][0]<0,'negative controls: additional rank3/rank9 unaffordable')
 return {'status':'PASS_INDEPENDENT_DYADIC_RELAY_ACQUISITION_BUDGET','grid':'2^96','source_owned_histogram':dict(sorted(O.items())),'eight_retained_owned_histogram':dict(sorted(R.items())),'variants':ans,'geometry':'200 nonentry carriers end at127; eight declared entry carriers end at rank8 subspaces;3<541<127','controls':['all eighteen repetitions checked in every rank bin','direct plus two rank2 repairs strictly fails','direct plus rank3 strictly fails','facet plus rank9 strictly fails'],'scope':'Conditional complete paid profiles only. Typed acquisition and full shared continuation are separate; no ordinary/compiler fee or new kappa is inferred.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--invoice',type=Path,required=True);p.add_argument('--lifetime-word',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
