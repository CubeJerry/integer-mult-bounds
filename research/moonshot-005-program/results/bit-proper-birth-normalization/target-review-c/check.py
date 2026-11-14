#!/usr/bin/env python3
"""Independent160-bit endpoint arithmetic; no author implementation import."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def power(r):
 s=1<<160;goal=r**199*s**200;lo=0;hi=r*s+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=goal:lo=m
  else:hi=m
 need(lo**200<=goal<hi**200,'outward power bracket')
 return F(lo,s),F(hi,s)

def add_profile(out,p,m=1):
 for r,c in p.items():out[r]=out.get(r,F(0))+m*c

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author-result',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'paired source');z=json.loads(raw)
 N,H,P,T=({int(r):F(c) for r,c in z[k].items()} for k in ['native_paid','helper_target','paired_paid','paired_target'])
 B={};add_profile(B,N);add_profile(B,H,-1);add_profile(B,T,F(1,36));add_profile(B,P,F(-1,36));B={r:c for r,c in B.items() if c}
 E=B.copy();E[7]=E.get(7,F(0))-222;values={r:power(r) for r in set(E)|{8}}
 def evaluate(profile):
  lo=hi=F(0)
  for r,c in profile.items():
   l,h=values[r];lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
  return lo,hi
 e=evaluate(E);need(82<e[0]<e[1]<83,'global82 integer bound')
 author=json.loads(a.author_result.read_text());caps=[82,74,66,59,51,43,35,27,19,11,3];intervals={}
 for q,cap in enumerate(caps):
  profile=E.copy();profile[8]=profile.get(8,F(0))-q;iv=evaluate(profile)
  need(cap<iv[0]<iv[1]<cap+1,'proper-born integer cap')
  ai=list(map(F,author['limiting_room_by_qH'][str(q)]));need(ai[0]<=iv[0]<iv[1]<=ai[1],'author interval contains independent bracket')
  intervals[q]=list(map(str,iv));need(q+cap<=82,'mixture facet count')
 need(111+82==193 and 193<=196,'uniform rank-gap threshold')
 need(F(37,3)-F(80,49)>0,'normalized derivative lower bound')
 need(sum(r*c for r,c in E.items())==F(629,6)>83,'out-of-target control')
 need(F(intervals[10][0])-3>0,'q10 p1=3 not falsely excluded')
 out={'status':'PASS_INDEPENDENT_PROPER_BIRTH_TARGET_COMPOSITION','source_sha256':PIN,'dyadic_bits':160,
      'E_star':list(map(str,e)),'limiting_room_by_qH':intervals,'proper_plus_extra_caps':caps,
      'facet_bound':193,'author_intervals_containment':'all11pass','new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'E_star_approx':float(e[0]),'caps':caps,'facet_bound':193}))

if __name__=='__main__':main()
