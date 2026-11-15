#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,importlib.util
import sympy as sp

def echelon(rows):
 B={};ids=[]
 for k,v in enumerate(rows):
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;ids.append(k);break
 return B,ids

def rank(rows):return len(echelon(rows)[0])
def rem(v,B):
 for p in sorted(B,reverse=True):
  if v>>p&1:v^=B[p]
 return v
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=src.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));spanners=[1,3,4,76];basis=sp.Matrix([R[i]for i in spanners]);assert basis.rank()==4;null=basis.nullspace();T=[j for j,r in enumerate(R)if all(sum(v[k]*r[k]for k in range(8))==0 for v in null)];assert T==[1,3,4,6,73,74,75,76,77,78,79,80];Z=[j for j,r in enumerate(R)if all(dot(r,R[i])==0 for i in T)];assert Z==[0,2,5,7,38,39,40,41,42,43,44,45]and not(set(T)&set(Z))
K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];_,ki=echelon(K);assert len(ki)==9;Kb=[K[i]for i in ki];outside=[j for j in range(111)if j not in T+Z];columns=[sum(((row>>j)&1)<<k for k,row in enumerate(Kb))for j in outside];_,piv=echelon(columns);minorcols=[outside[p]for p in piv];assert len(minorcols)==9
minor=[[int(Kb[i]>>j&1)for j in minorcols]for i in range(9)];det=int(sp.Matrix(minor).det());assert det%2
G=Kb+[1<<j for j in Z];rankgrant=rank(G);rankwith=rank(G+[1<<i for i in T]);assert rankgrant==21 and rankwith==33
cohorts={}
for j,r in enumerate(R):cohorts.setdefault(tuple(i for i in T if dot(r,R[i])==0),[]).append(j)
assert len(cohorts)==25 and all(len(s)>1 for s in cohorts)
cache_dims=[8-sp.Matrix([R[i]for i in s]).rank()for s in cohorts];assert Counter(cache_dims)=={5:24,4:1}
# A zero-cost native-point replacement is outside the declared common-meet input model;
# actual point copies still need one paid positive descent apiece.
controls=[]
for i in T:
 B,_=echelon(G+[1<<j for j in T if j!=i]);assert rem(1<<i,B);controls.append({'missing_target_direction':i,'not_spanned_by_other_eleven':True})
price_path=Path(__file__).parents[1]/'price.py';spec=importlib.util.spec_from_file_location('source_price',price_path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);profile={1:12,7:222,8:9};priced=mod.invoice(profile)
from fractions import Fraction as F
lower_room=F(priced['limiting_room']['lower_fraction']);upper_room=F(priced['limiting_room']['upper_fraction']);assert upper_room<0
positive_relaxation=mod.invoice({1:11,7:222,8:9});assert F(positive_relaxation['limiting_room']['lower_fraction'])>0
out={'status':'PASS_D4_SINGLE_FUNNEL_GATE','source_sha256':sha,'target_spanners':spanners,'targets':T,'free_meet_originals':Z,'common_meet_dimension':4,'cohort_count':len(cohorts),'cache_chart_dimensions':dict(Counter(cache_dims)),'canonical_basis_native_rows':ki,'outside_minor_columns':minorcols,'outside_minor_matrix':minor,'outside_minor_integer_determinant':det,'canonical_plus_free_meet_rank':rankgrant,'with_targets_rank':rankwith,'required_positive_arrival_modes_per_width':12,'optimistic_movement_profile':profile,'optimistic_price':priced,'eleven_arrival_relaxation_price':positive_relaxation,'negative_controls':controls,'scope':'Fixed stable canonical9 global service; target X access after preload only through common meet and its source arrivals; no later nonlocal private facet input. All local meet-original coordinates granted for free.','new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'minor det',det,'lower Q',priced['moment']['lower'],'upper room',priced['limiting_room']['upper'])
