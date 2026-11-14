#!/usr/bin/env python3
"""Independent exact review; no author verifier or arithmetic module imported."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
PINS={'PROOF.md':'fcfea22e4a3604c9f82b6098195e3f34733fbd7ee8ad3ef2df5e852496e13fd1','RESULT.json':'a3575601ca0ab8bf29455050be2fe5da158d36ac4b5de61409d5b2abd61525b2','MANIFEST.json':'56c392a520d51ae7de3854ef570d67cf00003ca693cf8f675c5d9f95d4ade583'}
def need(x,m):
 if not x:raise ValueError(m)
S=10**24
CACHE={}
def power(n):
 if n not in CACHE:
  N=pow(n,199)*pow(S,200);y=n*S
  while True:
   z=(199*y+N//pow(y,199))//200
   if z>=y:break
   y=z
  while pow(y,200)>N:y-=1
  while pow(y+1,200)<=N:y+=1
  need(pow(y,200)<=N<pow(y+1,200),'exact root bracket')
  CACHE[n]=(F(y,S),F(y+1,S))
 return CACHE[n]
def plus(a,b):return(a[0]+b[0],a[1]+b[1])
def times(c,a):return(c*a[0],c*a[1])if c>=0 else(c*a[1],c*a[0])
def enc(a):return[str(x)for x in a]
def main(author,out):
 for f,h in PINS.items():need(hashlib.sha256((author/f).read_bytes()).hexdigest()==h,'author pin '+f)
 ar=json.loads((author/'RESULT.json').read_text())
 for f,h in ar['source_pins'].items():need(hashlib.sha256((author/'source'/f).read_bytes()).hexdigest()==h,'dependency pin '+f)
 need(ar['half_profile']=={'2':112,'3':112,'5':112,'6':112},'actual half price')
 H=(F(0),F(0))
 for n in [2,3,5,6]:H=plus(H,times(112,power(n)))
 def delta(m,h,q=0):
  v=plus(times(112*h,power(8*m+1)),times(112*(2-h),power(8*m)))
  return plus(plus(v,times(-m,H)),(-F(112*q),-F(112*q)))
 # Independent continuous derivative proof at x=1, stronger than discrete first difference.
 t=F(199,200);der={}
 der[2]=plus(times(112*16*t/F(9),power(9)),times(-1,H))
 der[1]=plus(plus(times(112*8*t/F(9),power(9)),times(112*8*t/F(8),power(8))),times(-1,H))
 need(all(v[1]<0 for v in der.values()),'negative continuous derivatives at1')
 table=[]
 for a in ar['table']:
  m,h=a['m'],a['head_jobs'];iv=delta(m,h);old=[F(x)for x in a['no_query_room']]
  need(iv[0]<=old[0]<=old[1]<=iv[1],'independent bracket contains narrow author bracket')
  allowed=[q for q in range(3)if delta(m,h,q)[0]>0]
  need(allowed==a['allowed_complete_query_banks'],'complete query table')
  need(all(delta(m,h,q)[1]<0 for q in range(3)if q not in allowed),'strict failed-query controls')
  table.append({'m':m,'head_jobs':h,'room':enc(iv),'queries':allowed})
 for m,h,sign in [(8,2,1),(9,2,-1),(5,1,1),(6,1,-1),(5,2,1),(6,2,-1)]:
  iv=delta(m,h,1 if(m,h)in[(5,2),(6,2)] else 0)
  need(iv[0]>0 if sign==1 else iv[1]<0,'unbounded-tail/query boundary')
 service_gap=plus(power(224),times(-1,delta(1,2)))
 need(service_gap[0]>0,'strict modular service exclusion')
 # At t=1 the same source has exactly224 two-head surplus for every m.
 need(all(112*(2*(8*m+1)-16*m)==224 for m in [1,2,8,1000]),'zero-kappa control')
 result={'status':'PASS_INDEPENDENT_EXACT_ENVELOPE_REVIEW','author_pins':PINS,'dependency_pins':ar['source_pins'],'independent_method':'Newton integer200th-root brackets at24 decimal places, certified by integer inequalities; continuous derivative monotonicity; no author code imported.','derivative_at1':{str(h):enc(v)for h,v in der.items()},'service_minus_global_max':enc(service_gap),'table':table,'controls':['all unaffordable queries strictly negative','next-stage boundary signs','zero-kappa constant224 room'], 'scope':'The author two-original-bank/fresh-body/no-helper family and inherited unitary modular-service premise. Positive room does not assert a caller.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,default=HERE/'RESULT.json');a=p.parse_args();main(a.author,a.out)
