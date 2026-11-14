#!/usr/bin/env python3
"""Independent exact pivot caller screen from native/previously admitted invoices."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
 if not x:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 need(sha(a.caller)=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','caller pin')
 need(sha(a.native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
 need(sha(a.word)=='8fc6d916178b788c1b21077c0e9e3e81602aaf0789c5fd32f7ce8397128b72ba','closed pivot word pin')
 c=json.loads(a.caller.read_text());n=json.loads(gzip.decompress(a.native.read_bytes()));w=json.loads(gzip.decompress(a.word.read_bytes()));au=json.loads(a.author.read_text())
 N,H,P,T=({int(r):F(v)for r,v in c[k].items()}for k in['native_paid','helper_target','paired_paid','paired_target'])
 def mix(*pairs):
  out=Counter()
  for z,p in pairs:
   for k,v in p.items():out[k]+=z*v
  return{k:v for k,v in out.items()if v}
 actual=Counter(abs(n['frames'][str(o[3])]['dim']-n['frames'][str(o[2])]['dim'])for o in n['program']if o[0]=='MOVE');need(actual==N,'native movement invoice')
 nc=Counter(o[0]for o in n['program']);need(nc=={'INIT':237,'ADD':30789,'SWAP':3,'MOVE':2871,'CLEAR':237},'native ordinary work')
 S=mix((F(1,36),T),(F(-1,36),P));limit=mix((1,N),(-1,H),(1,S))
 pending={};Q=Counter();byrecord={}
 def finish(i):
  if i not in pending:return
  b,d=pending.pop(i);q=abs(d-b);need(q>0,'strict positive call');Q[q]+=1;byrecord.setdefault(i,[]).append(q)
 def dim(c):return w['frames'][str(c)]['dim']
 for op in w['program']:
  tag,i=op[:2]
  if tag=='MOVE':
   b,d=map(dim,op[2:4])
   if i not in pending:pending[i]=(b,d)
   else:
    s,t=pending[i];need(t==b,'continuous record route')
    if(t-s)*(d-b)>0:pending[i]=(s,d)
    else:finish(i);pending[i]=(b,d)
  else:
   finish(i)
   if tag=='ADD':finish(op[2])
 for i in list(pending):finish(i)
 need(Q=={1:57,6:56,7:167,8:2},'actual accesses force full profile')
 need(Counter(tuple(byrecord[i])for i in range(111))=={(6,1):56,(7,):55},'original X full physical stops')
 need(all(byrecord[i]==[7]for i in range(111,222)),'all Y rank7')
 need(sum(q*v for q,v in Q.items())==1578,'complete rank length')
 grid=1<<176;cache={}
 def root(r):
  if r not in cache:
   z=r**199*grid**200;l,h=0,r*grid+1
   while h-l>1:
    m=(l+h)//2
    if m**200<=z:l=m
    else:h=m
   need(l**200<=z<h**200,'outward root');cache[r]=(F(l,grid),F(h,grid))
  return cache[r]
 def moment(p):
  lo=hi=F(0)
  for k,v in p.items():
   l,h=root(k);lo+=v*(l if v>0 else h);hi+=v*(h if v>0 else l)
  return lo,hi
 def enclosed(v,rec):need(F(rec['lower_rational'])<=v[0]<=v[1]<=F(rec['upper_rational']),'tighter independent bounds')
 enclosed(moment(Q),au['actual_partial_moment']);enclosed(moment(limit),au['limiting_allowance']);enclosed(moment(S),au['finite_m_correction_numerator']);need(moment(S)[1]<0,'fixed-m monotonic penalty')
 cases={}
 for q,first in [(6,4),(7,6)]:
  total=mix((1,Q),(q,{8:1}));lim=mix((1,limit),(-1,total));fixed={m:moment(mix((1,lim),(F(1,m-1),S)))for m in range(2,first+1,2)}
  need(fixed[first][0]>0 and all(v[1]<0 for m,v in fixed.items()if m<first),'exact first even threshold')
  A=au['conditional_future_Hub_modes'][str(q)];enclosed(moment(total),A['moment']);enclosed(moment(lim),A['limiting_extra_moment_room'])
  cases[str(q)]={'hypothetical_future_modes':q,'complete_profile_if_no_other_movement':dict(total),'moment':list(map(str,moment(total))),'limiting_room':list(map(str,moment(lim))),'first_even_m_before_decoder_expense':first,'fixed_even_margins':{str(m):list(map(str,v))for m,v in fixed.items()}}
 wc=Counter(o[0]for o in w['program']);need(wc=={'INIT':117,'ADD':575,'MOVE':1578,'CLEAR':117},'partial ordinary invoice')
 out={'status':'PASS_INDEPENDENT_RETAINED_PIVOT_FULL_CALLER_SCREEN','native_sha256':sha(a.native),'caller_sha256':sha(a.caller),'word_sha256':sha(a.word),'grid':'2^-176','actual_profile':dict(Q),'actual_counts':dict(wc),'native_ordinary_counts':dict(nc),'limiting_allowance':list(map(str,moment(limit))),'finite_m_correction':list(map(str,moment(S))),'cases':cases,'ordinary_formula':'30789 + (m-1)(444 + A_Q) ADD, native3 SWAP retained;237+(m-1)L_Q owned lifetimes; all continuation work and114 final retained retirements remain explicit.','scope':'Exact conditional cost screen only. Physical six-mode completion and additional histories outside C+e0 are absent. This is not a target supplier admission.','new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'six_modes_room':float(F(cases['6']['limiting_room'][0])),'first_even_m':4}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in['native','caller','word','author','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
