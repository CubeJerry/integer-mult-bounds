#!/usr/bin/env python3
"""Independent all-column review of the frozen earlier-interleaving word."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
from collections import defaultdict

def solve_binary(equations):
 b={}
 for z,y in equations:
  while z:
   k=z.bit_length()-1
   if k in b:z^=b[k][0];y^=b[k][1]
   else:b[k]=(z,y);break
  if not z and y:raise ValueError('inconsistent collision equations')
 x=0
 for k,(z,y)in sorted(b.items()):
  if ((z&x).bit_count()&1)^y:x|=1<<k
 if not all(((z&x).bit_count()&1)==y for z,y in equations):raise ValueError('collision solution failure')
 return x

def bits(row):return sum(1<<j for j in row)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args();sp=importlib.util.spec_from_file_location('own_native',a.audit_module);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);check=m.insist
 raw=a.word.read_bytes();w=json.loads(raw);check(hashlib.sha256(raw).hexdigest()=='bfe5111a3d8a9f3623ca0644edd127cf427c478e3ba67a784033daf445305303','frozen earlier word');source=json.loads((a.repo/w['source_path']).read_text());check(m.sha(a.repo/w['source_path'])==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','literal root source');R=source['native_roots'];T=w['targets'];check(T==[1,3,73,76,77,80],'same six targets');U=[i for i in range(111)if i not in T];ops=w['operations'];cut=w['carrier_interface_before_operation'];marks=w['milestones'];c=w['construction'];snap=set(marks.values())|{cut}
 for k,o in enumerate(ops):
  if o[0]=='ADD'and(o[1].startswith('X')or o[2].startswith('X')):snap.add(k);snap.add(k+1)
 st,tr,C,events=m.replay(w,source,snap);N=[{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)];K=[N[i]^{i}for i in range(111)];common=set.intersection(*(N[i]for i in T));check(common==set(c['common_roles'])and len(common)==20,'literal common20');codes={int(i):j for i,j in c['code_carrier'].items()};held=set(codes.values());check(len(held)==6 and held<=common,'six distinct common originals');G=defaultdict(list)
 for j in range(111):G[tuple(i for i in T if j in N[i])].append(j)
 check([{'receivers':list(g),'donors':ds}for g,ds in sorted(G.items())]==c['groups'],'complete source cohort partition');early=marks['all_six_Y_waiting_at_facets'];ev,el=tr[early];check(all(el[f'Y{i}']==f'F{i}'for i in T)and not any(n.startswith('CANONICAL_')for n in ev),'all selectedY depart before canonical owners exist');check(early<min(k for k,o in enumerate(ops)if o[0]=='INIT'and o[1].startswith('CANONICAL_')),'literal chronology')
 for mark in ['only_six_raw_code_originals_held','canonical_ground_while_six_held']:
  v,l=tr[marks[mark]]
  for j in range(111):check(v[f'X{j}']=={j}and l[f'X{j}']==('COMMON'if j in held else'Hub'),'105 rawHub and6 rawheld')
  for i in T:check(v[f'Y{i}']==({111+i,codes[i]}^(N[i]-common))and l[f'Y{i}']==f'F{i}','exact early-Y partial payload')
 cv,cl=tr[marks['canonical_ground_while_six_held']];canon=c['canonical_fields'];basisroles=c['canonical_basis_roles'];check(len(canon)==9 and len(m.binary_basis([cv[n]for n in canon]))==9,'actual nine independent fields')
 for n,i in zip(canon,basisroles):check(cv[n]==K[i]and cl[n]=='zero','exact canonical ground packet')
 for i in T:check(cv[f'LATE_CODE_{i}']==(K[i]^common)and not(cv[f'LATE_CODE_{i}']&common),'late correction removes all20 common coefficients')
 for typ in ['canonical_hub_projections','actual_held_queries']:
  for k in w['semantic_operation_indices'][typ]:
   o=ops[k];v,l=tr[k];j=int(o[1][1:]);check(v[o[1]]=={j},'every actually queried original is raw');check(l[o[1]]==('Hub'if typ=='canonical_hub_projections'else'COMMON'),'actual source location at each query')
 for k in w['semantic_operation_indices']['late_code_restorations']:
  o=ops[k];v,l=tr[k];j=int(o[1][1:]);check(j not in common and v[o[1]]=={j}and l[o[1]]==l[o[2]]=='Hub','late inverse uses actual raw noncommon donor')
 v,l=tr[cut]
 for i in range(111):
  check(v[f'X{i}']=={i}and l[f'X{i}']=='Hub'and v[f'NATIVE_RAW_{i}']=={i}and l[f'NATIVE_RAW_{i}']==f'L{i}','all111 originals restored with native caches');check(v[f'Y{i}']==({111+i,i}if i in T else{111+i})and l[f'Y{i}']==(f'F{i}'if i in T else'zero'),'all222 exact cut columns')
 owned=[e for e in events if e[-1]];check(len(owned)==18 and sorted(e[4]for e in owned)==[3]*9+[5]*9,'exact eighteen canonical descents');check(st['counts']=={'INIT':140,'ADD':1299,'MOVE':396,'CLEAR':140}and st['dirty_clear']==140,'whole word operation invoice')
 masks=[f'MASK_{i}'for i in T];visibility={};local={}
 for n in masks:
  rows=v[n];check(rows==set(c['raw_mask_roles'][n[5:]]),'actual raw mask row');check(all(m.subset(C[f'L{j}'],C[l[n]])for j in rows),'native-local mask');visibility[n]=[i for i in U if m.subset(C[l[n]],C[f'F{i}'])];local[n]=[j for j in range(111)if m.subset(C[f'L{j}'],C[l[n]])]
 check(not any(m.subset(C[l[p]],C[l[q]])for p in masks for q in masks if p!=q),'all six masks pairwise incomparable');check(sorted(len(local[n])for n in masks)==[1,3,3,3,3,3],'one native line or three-line A2 plane')
 other=[n for n in v if not n[0]in'XY'and n not in masks and not n.startswith('NATIVE_RAW_')and n not in canon];check(len(other)==14 and all(not m.subset(C[l[n]],C[f'F{i}'])for n in other for i in U),'all other14 proper helpers invisible to every unfinished facet')
 code=[v[n]for n in canon];words=[set()]
 for z in code:words +=[x^z for x in words]
 gaps={i:min(len(z-N[i])for z in words if z and z!=K[i])for i in U};check(min(gaps.values())==18 and all(K[i]in words for i in U),'actual512 canonical words and alternative gap18');pairs={(i,h):len(N[i]-N[h])for i in U for h in U if i!=h};check(len(pairs)==10920 and min(pairs.values())==21,'all unfinished-pair native differences')
 pair=min(pairs,key=lambda q:(pairs[q],q));i,h=pair;D=sorted(N[i]-N[h]);grants=set(D[:17]);extras=set(D[17:20]);missing=D[20];visible=(N[i]&N[h])|grants|extras
 collision=solve_binary([(bits(z),0)for z in code]+[(1<<j,0)for j in sorted((N[i]-{missing})|grants)]+[(1<<i,1)])
 check((collision>>missing)&1 and not any((collision>>j)&1 for j in visible),'functional indistinguishability with17 global and3 private grants');check(not m.in_span({i},m.binary_basis(code+[{j}for j in visible]))and m.in_span({i},m.binary_basis(code+[{j}for j in N[i]])),'missing-input negative and full-native positive controls')
 collision_record={'receiver':i,'last_shared_other_receiver':h,'seventeen_global_native_grants':sorted(grants),'three_extra_private_native_inputs':sorted(extras),'missing_native_input':missing,'difference_support':[j for j in range(111)if collision>>j&1]}
 controls=[]
 labels=['native_captures','mask_captures','common_captures','group_captures','pivot_coding','early_direct_cohort_reads','masked_foreign_injections','masked_foreign_restorations','canonical_hub_projections','actual_held_queries','proper_code_captures','late_code_injections','late_code_receiver_reads','late_code_restorations']
 for typ in labels:
  k=w['semantic_operation_indices'][typ][0];bad=copy.deepcopy(w);bad['operations'].pop(k)
  try:_,bs,_,_=m.replay(bad,source,[cut-1])
  except (ValueError,KeyError)as ex:controls.append({'type':typ,'operation':k,'endpoint_or_interface_rejected':str(ex)})
  else:
   check(bs[cut-1][0]!=v,'omitted operation must change complete live-field interface');controls.append({'type':typ,'operation':k,'endpoints_can_pass_but_complete_source_rejected':True})
 q=m.moment(st['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in m.moment(gate));room=(ceiling[0]-q[1],ceiling[1]-q[0]);excess=(q[0]+18-ceiling[1],q[1]+18-ceiling[0]);check(excess[0]>0 and room[1]<9,'source budget excludes18 native origins')
 result={'status':'PASS_INDEPENDENT_EARLY_Y_LATE_CANONICAL_CONSTRUCTION','word_sha256':m.sha(a.word),'source_sha256':w['source_sha256'],'stats':st,'source_cut':cut,'milestones':marks,'actual_held_raw_originals':sorted(held),'canonical_queries_all_actual_raw_sources':True,'all222_cut_columns':True,'native_local_masks':[{'field':n,'support':sorted(v[n]),'chart_rank':len(C[l[n]]),'contained_native_lines':local[n],'unfinished_receivers_visible':visibility[n]}for n in masks],'all_masks_pairwise_incomparable':True,'union_mask_visibility':len(set().union(*(set(x)for x in visibility.values()))),'other14_proper_helpers_invisible':other,'canonical_alternative_gap':gaps,'pair_difference_minimum':min(pairs.values()),'ordered_pairs':len(pairs),'native_only_gate':{'additional_initial_native_inputs_available_after_last_shared_chart_at_most':3,'global_native_origins_excluded_through':17,'necessary_distinct_native_origins':18,'scope':'Every future owned MOVE starts at one of the111 native lines and ends at ground; arbitrary local nonlinear operations and Y-bearing stationary histories allowed under a fixed schedule.','proof':'NATIVE-LOCAL-GATE.md'},'movement':m.interval_json(q),'necessary_room':m.interval_json(room),'native_only_strict_excess':m.interval_json(excess),'negative_controls':controls,'explicit_nonlinear_collision':collision_record,'scope':'Earlier actual Y acquisition and held-source canonical queries verified for every characteristic-two field and whole-record width; six outputs only. Native-only frozen continuation excluded, arbitrary nonnative descents unresolved. No new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print(m.interval_json(q)['decimal']);print(m.interval_json(excess)['decimal'])
if __name__=='__main__':main()
