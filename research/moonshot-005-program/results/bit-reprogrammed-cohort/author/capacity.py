#!/usr/bin/env python3
"""Finite exact certificates for the cohort projection-capacity theorem."""
import argparse,json,hashlib
from pathlib import Path
from itertools import combinations
from build import rank,independent,xor,ROOT,ROOT_SHA

def span(rows):
 out={0}
 for r in rows:out|={v^r for v in list(out)}
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rb=(a.repo/ROOT).read_bytes();assert hashlib.sha256(rb).hexdigest()==ROOT_SHA;R=json.loads(rb)['native_roots'];w=json.loads(a.word.read_text());W=[int(x,16)for x in w['W_rows_hex']];hm=int(w['W_pivot_h_hex'],16);ones=(1<<111)-1
 W0=independent([row&(ones^hm)for row in W]);W1=independent([row&hm for row in W]);assert len(W0)==7 and len(W1)==8
 groups=w['cohorts'];local=[];A=[];H=span([24,32,64]);plane=span([24,32]);incidence={};runidx=[]
 for g in groups:
  S=g['sources'];z=hm>>S[0]&1;r=len(g['runs']);M=sum(1<<i for i in S);P=[row&M for row in (W1 if z else W0)]
  forms=[int(x,16)for x in g['run_rows_hex']];pivots=[g['carrier']]+g['donors']
  assert len(forms)==r and rank(forms)==r and all(row&~M==0 for row in forms)
  assert all(bool(row>>j&1)==(i==t)for i,row in enumerate(forms)for t,j in enumerate(pivots))
  assert len(g['restore_add_indices'])==sum(row.bit_count()-1 for row in forms)
  for t,(run,row)in enumerate(zip(g['runs'],forms)):
   idx=len(runidx);runidx.append({'cohort_first_role':S[0],'carrier':pivots[t],'run':run,'row_hex':hex(row)})
   for pos,q in enumerate(run):
    name=f'C{q}_{len(run)-pos}_{z}';incidence[name]=incidence.get(name,0)^(1<<idx)
  data={'first_role':S[0],'roles':S,'h_class':z,'run_capacity':r,'full_W_projection_rank':rank(P),'actual_run_rows_hex':[hex(x)for x in forms]}
  if z==0 and r==2:
   cols=[sum(1<<i for i,row in enumerate(W0)if row>>j&1)for j in S];dual=span(cols)
   assert len(dual)==8 and len(dual&H)==4 and len(dual&plane)>=2
   data.update(local_dual_vectors=sorted(dual),intersection_H_vectors=sorted(dual&H),intersection_scalar_plane=sorted(dual&plane));A.append((S[0],dual))
  local.append(data)
 assert len(runidx)==40 and len(incidence)==80 and rank(list(incidence.values()))==40
 assert [i for i,_ in A]==[81,66,46,30]
 assert set.intersection(*(v for _,v in A[:3]))=={0}
 assert set.intersection(*(v for _,v in A))=={0}
 g52=next(g for g in groups if g['sources'][0]==52);g22=next(g for g in groups if g['sources'][0]==22)
 pairmask=sum(1<<i for i in g52['sources']+g22['sources']);assert len(g52['runs'])==len(g22['runs'])==1 and rank([v&pairmask for v in W1])==6
 D=[v[1]for n,v in w['expected'].items()if n.startswith('C')];assert rank(D)==40 and rank(D)+15-rank(D+W)==9
 D0=[v&(ones^hm)for v in D];D1=[v&hm for v in D]
 assert rank(D0)+7-rank(D0+W0)==5 and rank(D1)+8-rank(D1+W1)==4
 rows0=[int(v,16)for v in w['reprogramming']['h0_target_rows_hex']]
 assert rank(D+rows0)==40
 out={'status':'PASS_EXACT_COHORT_CAPACITY_CERTIFICATES','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'native_sha256':ROOT_SHA,
 'h0_W_basis_hex':[hex(x)for x in W0],'h1_W_basis_hex':[hex(x)for x in W1],
 'h0_common_three_space_H':sorted(H),'h0_scalar_annihilator_plane':sorted(plane),'h0_three_local_duals_have_zero_intersection':[81,66,46],
 'h1_two_run1_projection_rank6':[52,22],'cohorts':local,'read_incidence_rows_hex':{n:hex(v)for n,v in incidence.items()},'read_incidence_column_order':runidx,'read_incidence_rank':40,
 'scalar_source_D_rank':40,'scalar_source_D_W_intersection':9,'scalar_source_class_intersections':[5,4],
 'block_capacity_theorem':'max dim(D intersection (W tensor k^V)) = 9V+floor(V/2), within independent cohort run spaces of capacity r_S V; no block compiler admission asserted',
 'physical_scalar_local_ADD_count':2*sum(len(g['restore_add_indices'])for g in groups),'new_complete_kappa':False}
 a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':main()
