#!/usr/bin/env python3
"""Exact native-supported rank-three repair and terminal-span premises.

The complete public-Y factorization is rejected, not constructed. The
positive movement arithmetic below is explicitly a conditional interface.
"""
import argparse,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path
from fractions import Fraction
from algebra import SOURCE,PIN,rref,kernel,coords

BASE='research/moonshot-005-program'
GEO=f'{BASE}/results/bit-leaf-capacity-quotient/author/check.py'
PRICE=f'{BASE}/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py'
REPAIR=[(0,1),(1,0),(2,3)]

def module(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def add_profiles(*terms):
 out=Counter()
 for scalar,profile in terms:
  for d,n in profile.items():out[d]+=scalar*n
 return {d:n for d,n in sorted(out.items())if n}

def inverse_rows(rows,n):
 a=[x|(1<<(n+i))for i,x in enumerate(rows)]
 for j in range(n):
  p=next(i for i in range(j,n)if a[i]>>j&1);a[j],a[p]=a[p],a[j]
  for i in range(n):
   if i!=j and a[i]>>j&1:a[i]^=a[j]
 assert [x&((1<<n)-1)for x in a]==[1<<i for i in range(n)]
 return [x>>n for x in a]

def product(a,b):
 out=[]
 for x in a:
  y=0
  for j in coords(x):y^=b[j]
  out.append(y)
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;R=json.loads(raw)['native_roots'];n=len(R);assert n==111
 g=module(a.repo/GEO,'terminal_span_geometry');h=module(a.repo/PRICE,'terminal_span_price')
 N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
 K=[x^(1<<i)for i,x in enumerate(N)];M=N[:]
 for i,j in REPAIR:assert N[i]>>j&1;M[i]^=1<<j
 Ni,_=rref(N,n);assert len(Ni)==108
 inv=inverse_rows(M,n);assert product(M,inv)==product(inv,M)==[1<<i for i in range(n)]
 h.save(a.out/'INVERSE-CERTIFICATE.json',{'native_source_sha256':PIN,'removed_native_edges':REPAIR,'M_rows_hex':list(map(hex,M)),'inverse_rows_hex':list(map(hex,inv)),'both_products_identity':True})
 witnesses=[]
 for i,row in enumerate(M):
  chosen=[];C=()
  for j in coords(row):
   D=g.basis(C+(tuple(R[j]),))
   if len(D)>len(C):C=D;chosen.append(j)
   if len(C)==7:break
  F=g.chart({'kind':'ann','rows':[R[i]]})
  assert len(chosen)==7 and C==F
  assert all(sum(x*y for x,y in zip(R[i],R[j]))==0 for j in coords(row))
  witnesses.append({'receiver':i,'required_support_size':row.bit_count(),'seven_independent_source_roles':chosen,'full_facet_rank':7})
 # Actual raw repair capture route: each source original is used once and
 # visits its legitimate destination facet before Hub.
 assert len({j for i,j in REPAIR})==3
 captures=[]
 for i,j in REPAIR:
  L=g.chart({'kind':'span','rows':[R[j]]});F=g.chart({'kind':'ann','rows':[R[i]]});Hub=g.basis(tuple(tuple(int(x==y)for y in range(8))for x in range(8)))
  assert g.sub(L,F)and g.sub(F,Hub)and(len(L),len(F),len(Hub))==(1,7,8)
  captures.append({'receiver':i,'source':j,'literal_local_route':[['MOVE',f'X{j}',f'F{i}'],['INIT',f'REPAIR_{i}',f'F{i}'],['ADD',f'X{j}',f'REPAIR_{i}'],['MOVE',f'X{j}','Hub']],'public_movement_gaps':[6,1],'owned_movement':0})
 source={1:3,6:3,7:219,8:9};ceiling={1:780,6:3,7:108,8:9}
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 B=tuple(x/6 for x in h.moment(gate));Q=h.moment(ceiling)
 Nprof={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
 P2=add_profiles((36,Nprof),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
 T2=add_profiles((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
 finite=[]
 for m in [2,4,6,8,10,12]:
  Pm=add_profiles((m//2,P2),(-18*(m-1),Nprof),(18*(m-1),ceiling));Tm=add_profiles((m//2,T2),(-18*(m-1),H));gap=h.moment(add_profiles((1,Tm),(-1,Pm)))
  finite.append({'m':m,'target_minus_paid_movement':h.record(gap),'strictly_positive':gap[0]>0})
 assert [z['strictly_positive']for z in finite[:3]]==[False,False,True]
 controls=[]
 for omitted in range(3):
  altered=N[:]
  for pos,(i,j)in enumerate(REPAIR):
   if pos!=omitted:altered[i]^=1<<j
  rank=len(rref(altered,n)[0]);assert rank<111;controls.append({'omitted_repair':REPAIR[omitted],'rank':rank})
 # A supplied rank6 partial payload does not meet the theorem's full-span premise.
 A=[14,17,19,20];BB=[96,99,101,102];proper=[A[(i+1)%4]for i in range(3)]+[BB[(i-1)%4]for i in range(3)]
 proper=list(dict.fromkeys(proper));assert len(g.basis(tuple(tuple(R[j])for j in proper)))==6
 controls.append({'changed_partial_payload_geometric_rank':6,'terminal_gate_full_span_premise':False})
 controls.append({'changed_ground_map':'I','required_native_correction':'zero','terminal_gate_full_span_premise':False})
 result={'status':'PASS_NATIVE_MASK_RANK_THREE_REPAIR_AND_TERMINAL_SPAN_GATE_PREMISES','source_sha256':PIN,
  'native_rank':108,'native_kernel_dimension':3,'minimum_possible_additive_repair_rank':3,
  'rank_three_repair':REPAIR,'repaired_rank':111,'all111_residual_supports_span_full_facets':True,'span_witnesses':witnesses,
  'repair_capture_routes':captures,'repair_capture_movement_delta':{1:3,6:3,7:-3},
  'source_plus_direct_Y_endpoint_profile':source,'hypothetical_maximally_subdivided_Y_profile':ceiling,
  'hypothetical_movement':h.record(Q),'necessary_limiting_room_if_network_existed':h.record((B[0]-Q[1],B[1]-Q[0])),
  'finite_caller_arithmetic':finite,'first_tested_feasible_even_m':6,'public_only_network_exists':False,
  'reason':'At each final facet the full-span residual block has no nonzero proper-chart-supported row. Invertible local mixing among any fixed number of existing Y banks cannot turn proper incoming rows into that block without terminal source reads changing the residual.',
  'negative_and_boundary_controls':controls,'scope':'Exact algebraic repair and scoped multi-bank terminal-span obstruction. Favorable movement arithmetic is conditional and does not certify the obstructed network. Other ground codes, new terminal packets, changed source histories, and arbitrary owned Y-bearing communication remain open.','no_new_kappa':True}
 h.save(a.out/'RESULT.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in ['span_witnesses','finite_caller_arithmetic','repair_capture_routes']},indent=2))
if __name__=='__main__':main()
