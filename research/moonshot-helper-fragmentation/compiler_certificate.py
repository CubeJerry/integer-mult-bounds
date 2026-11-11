#!/usr/bin/env python3
"""Exact restored compiler specification; native and BIT inputs are UNBUILT."""
import argparse,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
H=Path(__file__).resolve().parent
PINS={'inputs/source-invoice.json':('ff3256f0d3ffbfc56b062f9ec0fdbbc7b30e76d5','d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'),'inputs/exact_arithmetic.py':('4b24a5096154736ce060474eb8c72dc64c303699','0ce7e7137422d5ffeda22085c81fa88471bbe963100fdad62e659f1e3bf89326')}
def need(x,s):
 if not x:raise ValueError(s)
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def scale(a,s):return (a[0]*s,a[1]*s) if s>=0 else (a[1]*s,a[0]*s)
def run():
 for path,(blob,digest)in PINS.items():
  z=(H/path).read_bytes();need(hashlib.sha256(z).hexdigest()==digest,'SHA256 '+path);need(hashlib.sha1(b'blob '+str(len(z)).encode()+b'\0'+z).hexdigest()==blob,'Git blob '+path)
 spec=importlib.util.spec_from_file_location('credited_exact',H/'inputs/exact_arithmetic.py');E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
 raw=json.loads((H/'inputs/source-invoice.json').read_text());old={int(k):n for k,n in raw['invoice']['T'].items()};P={int(k):n for k,n in raw['invoice']['P'].items()};helpers={int(k):n for k,n in raw['native']['helpers'].items()}
 need(helpers=={1:13,2:18,3:44,4:215,5:68,6:42,7:18,8:67,9:595},'native source')
 new=Counter(helpers)
 for r,n,parts in [(9,595,(4,5)),(8,67,(4,4)),(7,18,(3,4)),(6,42,(3,3))]:
  new[r]-=n
  for piece in parts:new[piece]+=n
 new[4]-=554;new[5]-=554;new[3]+=1662;new=+new
 need(dict(new)=={1:13,2:18,3:1808,4:408,5:109},'1276 target partition')
 T=Counter(old)
 for r,n in helpers.items():T[r]-=18*n
 for r,n in new.items():T[r]+=18*n
 T=+T;need(sum(new.values())-sum(helpers.values())==1276,'extra count')
 C=Q('.00500007');t=1-C;v=1920;c=11;b=12;u=Q(1,7)
 TT,PP=E.moment(T,t),E.moment(P,t)
 alpha=E.divide(PP,TT);gamma=E.divide(E.moment(P,t+u),E.mul(E.power(c,u),TT));lam=E.divide(E.mul(E.power(b,u),E.moment(T,t-u)),TT)
 bounds=(Q(12499990009,12500000000),Q(19,20),Q(977,1000));need(all(a[1]<q<1 for a,q in zip((alpha,gamma,lam),bounds)),'tails')
 a,g,l=bounds;norm=1/(1+v*(1-a))+2*g**v+l**v;need(norm<Q(999,1000),'paid plus discarded moment')
 B,p0,p1=sum(T.values()),sum(P.values()),sum(r*n for r,n in P.items());need((B,p0,p1)==(46360,117612,319844),'inventory')
 completion=E.divide((Q(B*b),Q(B*b)),E.mul(E.power(c,C),TT));need(completion[0]>1,'completion control')
 oldalpha=E.divide(PP,E.moment(old,t));need(oldalpha[0]>1,'unfragmented control')
 need(c**29<b**28 and 2*c**(v*29)<=153**(v*28),'honest ambient')
 theta=sub(E.log_bounds(28),E.log_bounds(29));logt=sub(E.log_bounds(t.numerator),E.log_bounds(t.denominator));base=scale(E.log_bounds(153),v*C);eta=sub(logt,base)
 p=1377;need(p*theta[1]<eta[0] and base[1]<p*E.log_bounds(2)[0],'log majorant');need((p-1)*theta[0]>=eta[1],'previous power')
 eta145=sub(logt,scale(E.log_bounds(145),v*C));wrong=1362;need(wrong*theta[1]<eta145[0] and wrong*theta[0]>=eta[1],'wrong ambient')
 step=10**8;j=58398;need((step*j+1)**p<2**j and (step*(j-1)+1)**p>=2**(j-1),'uniform grid')
 return {'status':'PASS_UNBUILT_PROFILE_COMPILER_SPECIFICATION','classification':'Sufficient arithmetic specification only; native profile and covered BIT are UNBUILT.','base_commit':'e54523517d0f03e58352e647c403a5af3e525a57','no_new_kappa':True,
  'profile':{'T':{str(r):n for r,n in sorted(T.items())},'P':{str(r):n for r,n in sorted(P.items())},'extra_per_native':1276,'extra_caller_targets':22968},
  'parameters':{'tested_saving':str(C),'v':v,'c':c,'b':b,'u':str(u),'w':str(u)},
  'moment':{'productive':E.display(TT),'paid':E.display(PP),'signed':E.display(sub(TT,PP)),'alpha':E.display(alpha),'gamma':E.display(gamma),'lambda':E.display(lam),'rational_upper_bounds':list(map(str,bounds)),'normalized_bound':E.display((norm,norm)),'strict_gap_lower':'1/1000'},
  'uniform_compiler':{'ambient':'153^1920','theta':'28/29','p':p,'log_eta':E.display(eta),'log_base':E.display(base),'log_margin':E.display(sub(eta,scale(theta,p))),'gap':'1/100000000','uniform_saving':str(C-Q(1,step)),'H':step*j,'N':f'2^{step*j}','previous_p_and_grid_fail':True},
  'counts':{'public':B,'paid_calls':p0,'paid_rank_mass':p1,'raw_product_invocations':'sum(i=0..1919,46360^(1919-i)*117612^i)','owned_specializations':'D=46360^1920-W_retained','new_initialization_and_erasure_records':'2D','split_paid_calls_upper':'319844^1920'},
  'negative_controls':{'completion':E.display(completion),'unfragmented_alpha':E.display(oldalpha),'145_ambient_power_fails_true153':wrong},
  'limits':['No native helper-cut construction or arbitrary-input admission.','No covered BIT supplier at target.','Actual new scalar/storage/precision counts need the constructed word.','All five foundational assumptions remain.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();result=run();receipt=H/'COMPILER-RESULT.json'
 if a.write:receipt.write_text(json.dumps(result,indent=2)+'\n')
 else:need(result==json.loads(receipt.read_text()),'frozen receipt')
 print(json.dumps(result,indent=2))
