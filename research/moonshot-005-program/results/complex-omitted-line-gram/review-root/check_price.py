#!/usr/bin/env python3
"""Independent dyadic complete-caller prices for the actual omitted-line seed."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(b,s):
 if not b:raise ValueError(s)
def main(a):
 raw=a.full.read_bytes();need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full caller pin');f=json.loads(raw);r=json.loads(a.review.read_text());need(r['status']=='PASS_INDEPENDENT_ACTUAL_LINE_GRAM_DUPLEX_SEED','actual independently reviewed source')
 T,P,N,H=({int(k):F(v) for k,v in f[i][j].items()} for i,j in [('invoice','T'),('invoice','P'),('native','paid'),('native','helpers')]);Q={int(k):F(v) for k,v in r['bill']['moves'].items()}
 def add(*terms):
  d={}
  for c,p in terms:
   for k,v in p.items():d[k]=d.get(k,0)+c*v
  return {k:v for k,v in d.items() if v}
 S=add((F(1,18),T),(F(-1,18),P));B=add((1,S),(1,N),(-1,H),(-1,Q));grid=1<<144;cache={}
 def power(k):
  if k not in cache:
   n=k**199*grid**200;l,h=0,k*grid+1
   while h-l>1:
    m=(h+l)//2
    if m**200<=n:l=m
    else:h=m
   need(l**200<=n<h**200,'outward dyadic root');cache[k]=F(l,grid),F(h,grid)
  return cache[k]
 def moment(p):
  l=h=F(0)
  for k,c in p.items():
   x,y=power(k);l+=c*(x if c>0 else y);h+=c*(y if c>0 else x)
  return l,h
 pen=moment(add((-1,S)));need(pen[0]>0,'finite-m penalty positive')
 profiles={'literal_seed':{},'all200_XB_at_most3_legs':{2:200,3:400,8:-200},'all200_XB_legs5_2_1':{1:200,2:200,5:200,8:-200},'all200_XB_legs5_3':{3:200,5:200,8:-200},'XB_521_plus_oneextra_stop_eachY':{1:200,2:304,3:104,5:96,8:-200},'XB_53_plus_oneextra_stop_eachY':{2:104,3:304,5:96,8:-200},'XB_521_plus_Y_actual_1_4_splits':{1:304,2:200,4:104,5:96,8:-200}}
 out={};au=json.loads(a.author.read_text())['models']
 for name,delta in profiles.items():
  lo,hi=moment(add((1,B),(-1,delta)));m=None
  if lo>0:
   m=2
   while lo-pen[1]/(m-1)<=0:m+=1
   need(hi-pen[0]/(m-2)<0 if m>2 else True,'exact first fixedm')
  if name in au:
   al,ah=map(F,au[name]['limiting_room']);need(al<=lo<hi<=ah and m==au[name]['first_m_positive_certified'],'independent tighter interval/first multiplicity agrees')
  out[name]={'extra_profile':delta,'limiting_room':list(map(str,(lo,hi))),'first_m':m,'classification':'actual partial source' if name=='literal_seed' else 'hypothetical sufficient movement envelope; source existence open'}
 need(out['literal_seed']['first_m']==5 and out['all200_XB_at_most3_legs']['first_m']==127,'known sharp signs')
 need(F(out['XB_521_plus_oneextra_stop_eachY']['limiting_room'][1])<0 and out['XB_521_plus_Y_actual_1_4_splits']['first_m'] is not None,'a negative worst-case Y envelope is not a universal one-stop exclusion')
 result=dict(status='PASS_INDEPENDENT_LINE_GRAM_COMPLETE_CALLER_PRICES',word_sha256=r['word_sha256'],full_source_sha256=hashlib.sha256(raw).hexdigest(),grid='2^-144',actual_Q={str(k):str(v) for k,v in Q.items()},positive_finite_m_penalty=list(map(str,pen)),models=out,scope='All costs are complete retained movement invoices or explicit sufficient envelopes; ordinary/ownership/precision/compiler/strict suppliers and actual missing compiler remain owed. A negative worst-case envelope does not exclude cheaper realizations.',new_kappa=None)
 a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'models':{k:{'room':float(F(v['limiting_room'][0])),'first_m':v['first_m']} for k,v in out.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['full','review','author','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
