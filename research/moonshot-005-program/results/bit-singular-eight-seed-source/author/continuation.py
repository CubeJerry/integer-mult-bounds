#!/usr/bin/env python3
"""Exact W15 continuation quotient; directions here are not acquired fields."""
from pathlib import Path
import argparse,json
from check import basis,rank,intersection_dimension
from price import invoice,encode,moment,add

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=w['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];S=[int(v,16)for v in w['seed_rows_hex']];W=basis(A);assert len(W)==15;current=S[:];completion=[];proper=[];native_kernels=[]
 for i in range(111):
  allowed=sum(1<<j for j in range(111)if dot(R[i],R[j])==0);B={};local=[]
  for k,row in enumerate(W):
   p=row&~allowed;c=1<<k
   while p:
    q=p.bit_length()-1
    if q in B:p^=B[q][0];c^=B[q][1]
    else:B[q]=(p,c);break
   if p:continue
   v=0
   for k,t in enumerate(W):
    if c>>k&1:v^=t
   assert v&~allowed==0 and rank(W+[v])==15;proper.append(v);local.append(v)
   if rank(current+[v])>rank(current):
    current.append(v);completion.append({'native_facet':i,'row_hex':hex(v),'support':[j for j in range(111)if v>>j&1],'W_basis_coefficient_hex':hex(c),'rank_after':rank(current)})
  native_kernels.append({'native_facet':i,'proper_kernel_dimension':rank(local),'outside_projection_rank':len(B),'rows_hex':[hex(v)for v in local]});assert len(B)+rank(local)==15
 native_completion=completion;native_rank=rank(current);native_proper_rank=rank(proper)
 data=json.loads(Path(__file__).with_name("SEED-SOURCE.json").read_text());completion=data["proper_completion_rows"];proper=[int(c["row_hex"],16)for c in completion]
 import sympy as sp
 for c,v in zip(completion,proper):
  support=[j for j in range(111)if v>>j&1];assert support==c["support"] and any(c["normal"]) and all(dot(R[j],c["normal"])==0 for j in support);assert sp.Matrix([R[j]for j in support]).rank()==7 and rank(W+[v])==15
 assert len(completion)==7 and rank(S+proper)==15
 inv=json.loads((a.out/'INVENTORY.json').read_text());cut=inv['seed8_before_Y'];available=[int(v['row_hex'],16)for v in cut['fields'].values()];ground=[int(cut['fields'][n]['row_hex'],16)for n in cut['groups']['ground']];assert intersection_dimension(A,available)==8 and rank(available+S)==rank(available)
 out={'claim':'Seven proper W15 directions complete the eight-seed rowspace algebraically; none is claimed acquired by the current word.','seed_rank':rank(S),'W15_rank':rank(W),'seven_chosen_proper_span_rank':rank(proper),'native_facet_proper_span_rank':native_proper_rank,'native_facet_kernels':native_kernels,'seed_plus_native_facet_proper_rank':native_rank,'seed_plus_all_proper_rank':rank(S+proper),'W_basis_rows_hex':[hex(v)for v in W],'completion_rows':completion,'actual_available_inventory_rank':rank(available),'actual_available_W15_intersection':intersection_dimension(A,available),'actual_ground_rank':rank(ground),'actual_ground_W15_intersection':intersection_dimension(A,ground),'actual_W15_quotient_deficiency':15-intersection_dimension(A,available),'each_completion_in_actual_inventory':[rank(available+[int(c['row_hex'],16)])==rank(available)for c in completion],'status':'exact finite source-bound algebraic continuation obligation; no acquired innovation certificate','new_complete_kappa':False}
 (a.out/'PROPER-COMPLETION.json').write_text(json.dumps(out,indent=2)+'\n')
 prof={int(k):v for k,v in json.loads((a.out/'RESULT.json').read_text())['movement_profile'].items()};direct={1:12,7:222,8:8};delta=moment(add((1,direct),(-1,prof)));assert delta[0]>0;cmp={'same_seed_control_profile':direct,'same_seed_control_Q':encode(moment(direct)),'candidate_Q':encode(moment(prof)),'control_minus_candidate':encode(delta),'comparison_scope':'Both partial words retain the same eight singular fitting seeds and complete the same twelve receiver endpoints; other ninety-nine remain unchanged.','direct_control_construction':'Copy twelve original point values at their native lines and descend each one rank; send every original X directly to Hub, acquire all eight S8 seeds there and descend them to ground; add point copies to the twelve selected original Y, send every Y directly to its facet, clear all twenty owners.','new_complete_kappa':False};(a.out/'SAME-SEED-CONTROL.json').write_text(json.dumps(cmp,indent=2)+'\n');print('native-facet proper span',native_proper_rank,'seed-plus-native-proper',native_rank,'actual deficiency',out['actual_W15_quotient_deficiency']);print('same-seed saving',cmp['control_minus_candidate']['lower'])
if __name__=='__main__':main()
