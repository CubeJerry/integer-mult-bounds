#!/usr/bin/env python3
"""Directed integer-root half-source envelope; no floating-point decisions."""
import argparse,hashlib,json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
@lru_cache(None)
def power(r):
 den=10**50;target=r**199*den**200;lo,hi=0,r*den+1
 while lo+1<hi:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 need(lo**200<=target<hi**200,'directed200th root')
 return F(lo,den),F(hi,den)
def moment(d):
 lo=hi=F(0)
 for r,c in d.items():
  a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
def invoice(m,h,q=0):
 d={r:-112*m for r in [2,3,5,6]}
 for r,c in [(8*m+1,112*h),(8*m,112*(2-h)),(1,-112*q)]:d[r]=d.get(r,0)+c
 return d
def subtract(a,b):
 d=a.copy()
 for r,c in b.items():d[r]=d.get(r,0)-c
 return d
def enc(x):return [str(v)for v in x]
def main(out):
 pins=json.loads((HERE/'SOURCES.json').read_text())
 for n,h in pins.items():need(hashlib.sha256((HERE/'source'/n).read_bytes()).hexdigest()==h,'source '+n)
 price=json.loads((HERE/'source/HALF-PRICE.json').read_text());need(price['half_profile']=={'2':112,'3':112,'5':112,'6':112},'actual half profile')
 rows=[]
 for m in range(1,11):
  for h in range(3):
   bound=moment(invoice(m,h));feasible=bound[0]>0
   need(feasible or bound[1]<0,'strict sign resolved')
   possible=[]
   for q in range(4):
    gap=moment(invoice(m,h,q));need(gap[0]>0 or gap[1]<0,'strict query sign resolved')
    if gap[0]>0:possible.append(q)
   if h==0:need(not feasible,'body-only control')
   if h==1:need(feasible==(m<=5) and possible==([0]if m<=5 else[]),'one-head exact window')
   if h==2:need(feasible==(m<=8) and possible==([0,1]if m<=5 else[0]if m<=8 else[]),'two-head exact window')
   rows.append({'m':m,'head_jobs':h,'no_query_room':enc(bound),'allowed_complete_query_banks':possible})
 differences={str(h):enc(moment(subtract(invoice(2,h),invoice(1,h))))for h in [1,2]}
 need(all(F(x[1])<0 for x in differences.values()),'negative first differences for concave sequences')
 uniform=moment(subtract({224:1},invoice(1,2)));need(uniform[0]>0,'every family member below one modular unitary service')
 result={'status':'PASS_EXACT_UNBOUNDED_STAGE_QUERY_ENVELOPE','kappa':'1/200','source_pins':pins,'half_profile':price['half_profile'],'table':rows,'first_differences':differences,'one_modular_service_minus_global_maximum':enc(uniform),'analytic_tail_proof':'Strict concavity makes successive differences decreasing. Negative first difference and exact first-negative boundary exclude every larger integer m. Body-only analytic inequality holds for allm.','classifications':{'two_head_max_stages':8,'one_head_max_stages':5,'body_only_never_positive':True,'complete_queries_at_most':1,'two_head_one_query_max_stages':5,'one_head_never_affords_query':True},'scope':'Two fixed112-port original banks; each actual half acts onboth; distinct fresh8-axis bodies; atmostonehead/job; no productive helper credit.','new_kappa':False}
 out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'classifications':result['classifications'],'uniform_service_gap':enc(uniform)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');main(p.parse_args().output)
