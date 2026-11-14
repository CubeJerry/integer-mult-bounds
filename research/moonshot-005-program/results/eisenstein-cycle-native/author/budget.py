#!/usr/bin/env python3
"""Exact all-arm price gates for two explicit, conditional cycle-native caller reductions."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json

def need(c,m):
 if not c:raise ValueError(m)
S=10**34;cache={}
def pw(n):
 if n not in cache:
  z=n**199*S**200;l=0;u=max(1,n)*S
  while u-l>1:
   m=(u+l)//2
   if m**200<=z:l=m
   else:u=m
  need(l**200<=z<=u**200,'power enclosure');cache[n]=(F(l,S),F(u,S))
 return cache[n]
def add(*xs):return sum((x[0]for x in xs),F(0)),sum((x[1]for x in xs),F(0))
def scale(c,x):return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def W(a,c=1,b=8):return add(scale(2,pw(c+2*a*b)),*(scale(4,pw(c+j*b))for j in range(1,a+1)),scale(-4,pw(c)),*(scale(-4,pw(j*b))for j in range(1,a)))
def H(a):return add(scale(a,W(a+1)),scale(-a-1,W(a)))
def enc(x):return {'exact':[str(v)for v in x],'approximate_midpoint':float(sum(x)/2)}
pa=argparse.ArgumentParser();pa.add_argument('--output',type=Path,default=Path(__file__).with_name('BUDGET.json'));a=pa.parse_args();native=scale(240,add(pw(1),pw(7),pw(8)));L=scale(10,W(6));room=add(L,scale(-1,native));direct=scale(240,pw(2));unitary=pw(480);need(H(5)[0]>0 and H(6)[1]<0,'global optimum signs');need(unitary[0]>room[1]and direct[0]>room[1],'service price gate');h3_upper=add(scale(2,pw(3)),scale(4,pw(6)));perport=scale(F(1,120),native);need(perport[0]>h3_upper[1],'common three-head template gate');out={'status':'PASS_EXACT_CONDITIONAL_ALL_ARM_PREFLIGHT','t':'199/200','native_profile':{'1':240,'7':240,'8':240},'native_cost':enc(native),'body8_global_optimal_a':6,'body8_optimizer_H5':enc(H(5)),'body8_optimizer_H6':enc(H(6)),'body8_max_per_native_allowance':enc(L),'body8_remaining_room':enc(room),'two_independent_normalizers_direct_rank2_cost':enc(direct),'two_bank_joint_unitary_no_credit_rank_mass_floor':480,'two_bank_joint_unitary_no_credit_moment_floor':enc(unitary),'common_three_head_six_body_all_arm_upper_perport':enc(h3_upper),'native_perport_cost':enc(perport),'scope':['body8 proof assumes the new orthogonal-R paid-normalizer reduction really supplies the physical caller','unitary gate retains o(V) ordinary port entropy and disallows productive helper credit','head3/body6 gate excludes only the displayed same-template accounting, even granting compatible operators','no lower bound for arbitrary nonunitary changed caller or shared helpers'],'caller_admission':False,'no_new_kappa':True};a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
