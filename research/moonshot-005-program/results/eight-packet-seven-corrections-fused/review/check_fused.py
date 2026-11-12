#!/usr/bin/env python3
"""Independent audit of actual seven-correction fusion and its paid invoice."""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as F
import gzip,hashlib,json,importlib.util,bisect
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds'
PARENT=BASE/'worker-coupling/eight-packet-seven-corrections';PACK=BASE/'worker-coupling/eight-packet-seven-corrections-fused';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPIN='ae7a86a02b853f3166c6727d66e0a2440b0e5e4e8e3a7d35e69dae029d66942d';PPAY='3cb2c8ef4b3f3d4c85703d3d737d4a2f570f380916d91fa0f00d8c3a768900cb'
FPIN='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153';FPAY='05b503f0c2f219f328353b984ca821db9d6c3cc0225ff3380c551708d247e8d8'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def read(path,pin,compressed=False,payload=None):
 b=path.read_bytes();need(digest(b)==pin,'authenticated file '+str(path))
 if compressed:b=gzip.decompress(b)
 if payload:need(digest(b)==payload,'authenticated payload '+str(path))
 return json.loads(b)
def helper():
 p=BASE/'worker-review/route-fusion/check_fusion.py';need(digest(p.read_bytes())=='cd0a90cc2773d144a1c106245d14c5a6f6ee9fad76dca64383a5dc2d7fa04763','own independent route helper pin')
 s=importlib.util.spec_from_file_location('own_route_review',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 h=helper();source=read(REPO/'research/shared-wire-split-composition/data/final.json.gz',SPIN,True)
 parent=read(PARENT/'WORD.json.gz',PPIN,True,PPAY);word=read(PACK/'WORD.json.gz',FPIN,True,FPAY)
 parent_review=read(BASE/'worker-review/eight-packet-seven-corrections/REVIEW-RESULT.json','0afb0bec5d68b9ad2db80ee9e79e81581689072b76bcc9d33c01b499970957c3')
 need(parent_review['word_payload_sha256']==PPAY and parent_review['common_rows_restored']==1480 and parent_review['private_inverse_rows']==400 and parent_review['all_other_coefficients_unchanged'],'independently reviewed complete parent interface')
 report=read(PACK/'RESULT.json','1e94f21a4c5ed5bc92543c918777d6f20716225995b138e946c30e6d70a231b4')
 proofpin=digest((PACK/'PROOF.md').read_bytes());need(proofpin=='a3c8496bee479739b30d890640fb53cab8207bf0a384d2380ea406c2db47bf76','frozen proof')
 frames=list(map(h.space,source['frames']));raw=set(parent['private_role_map'].values());need(raw==set(range(1480,1880)),'actual400 raw roles')
 old,new=parent['program'],word['program'];lineage=word['parent_event_of_output'];records=word['private_route_blocks']
 need(parent['initial']==word['initial'] and parent['public']==word['public']==1880 and parent['owned_fields']==word['owned_fields']==57,'unchanged physical namespace and inputs')
 need(word['parent_word_sha256']==PPIN and word['source_sha256']==SPIN,'correct parent and native provenance')
 pending=defaultdict(list);derived=[];uses=defaultdict(list);moves=defaultdict(list)
 for e,o in enumerate(old):
  if o[0]=='MOVE' and o[1] in raw:pending[o[1]].append(e);moves[o[1]].append(e)
  elif o[0]!='MOVE':
   for j in h.operands(o):
    if j in raw:
     uses[j].append(e)
     if pending[j]:derived.append((j,pending[j]));pending[j]=[]
 for j,events in pending.items():
  if events:derived.append((j,events))
 derived.sort(key=lambda b:b[1][-1])
 def replacement(j,events):
  need(events and events==sorted(set(events)),'ordered distinct route segment')
  need([e for e in moves[j] if events[0]<=e<=events[-1]]==events,'every intervening same-role MOVE included')
  need(not any(events[0]<e<events[-1] for e in uses[j]),'intervening actual raw arithmetic barrier')
  start=old[events[0]][2];current=start;rank=0
  for e in events:
   o=old[e];need(o==['MOVE',j,current,o[3],False] and frames[current]<frames[o[3]],'strict continuous upward raw chain')
   rank+=len(source['frames'][o[3]])-len(source['frames'][current]);current=o[3]
  need(rank==len(source['frames'][current])-len(source['frames'][start]) and frames[start]<frames[current],'complete direct recursive rank')
  return ['MOVE',j,start,current,False]
 last={events[-1]:(j,events,replacement(j,events)) for j,events in derived}
 raw_events={e for ev in moves.values() for e in ev};expected=[];expected_lineage=[]
 for e,o in enumerate(old):
  if e not in raw_events or e in last:expected.append(last[e][2] if e in last else o);expected_lineage.append(e)
 need(new==expected and lineage==expected_lineage,'whole literal fused word independently derived from actual barriers')
 need(len(raw_events)==1710 and len(derived)==len(records)==407 and len(old)-len(new)==1303,'exact original and emitted raw calls')
 old_to_new={e:i for i,e in enumerate(lineage)};byrole=defaultdict(list)
 provenance={r['physical_event']:r for r in parent['raw_reservations']}
 for rec,(j,events) in zip(records,derived):
  pos=old_to_new[events[-1]]
  need(rec=={'emitted_at_parent_event':events[-1],'original_source_raw_events':[provenance[e]['source_event'] for e in events],'parent_events':events,'physical_event':pos,'replacement':replacement(j,events),'role':j},'exact segment and source-reservation provenance')
  byrole[j].append(rec)
 need(word['native_event_to_physical']==[old_to_new[e] for e in parent['native_event_to_physical']],'every actual common source event remains precisely mapped')
 need(word['marks']=={k:bisect.bisect_left(lineage,e) for k,e in parent['marks'].items()},'boundary marker translation')
 need(word['parent_raw_reservation_provenance']==parent['raw_reservations'],'old reservations retained only as named parent provenance')
 need(word['prefix_semantic_provenance']['parent_prefix_event_to_parent_physical']==parent['prefix_event_to_physical'],'exact semantic prefix provenance')
 need('raw_reservations' not in word and 'prefix_event_to_physical' not in word,'no stale current route or prefix grant')
 changed={'program','schema','marks','native_event_to_physical','raw_reservations','prefix_event_to_physical'}
 for k,v in parent.items():
  if k not in changed:need(word[k]==v,'unchanged inherited interface '+k)
 pcheck=h.typed(source,parent);fcheck=h.typed(source,word)
 need(pcheck['final_locations']==fcheck['final_locations'],'all final locations identical')
 need({lineage[e]:v for e,v in fcheck['raw_uses'].items()}==pcheck['raw_uses'],'every actual raw read/write keeps its chart and parent event')
 need(pcheck['peak']==fcheck['peak']==43,'unchanged physical owned occupancy')
 need({k:v for k,v in pcheck['counts'].items() if k!='MOVE'}=={k:v for k,v in fcheck['counts'].items() if k!='MOVE'},'all arithmetic and lifetime counts unchanged')
 need(dict(fcheck['counts'])==report['operations'],'literal emitted opcode census')
 oldvisits={(j,parent['initial'][j]) for j in raw}|{(o[1],o[3]) for o in old if o[0]=='MOVE' and o[1] in raw}
 newvisits={(j,word['initial'][j]) for j in raw}|{(o[1],o[3]) for o in new if o[0]=='MOVE' and o[1] in raw}
 need(newvisits<=oldvisits and len(oldvisits-newvisits)==1303,'all removed raw stops are absent from actual access')
 oldprof,newprof=pcheck['rawranks'],fcheck['rawranks'];nativeprof=Counter(abs(len(source['frames'][o[3]])-len(source['frames'][o[2]])) for o in source['program'] if o[0]=='MOVE')
 need({str(r):n for r,n in oldprof.items()}==report['old_raw_profile'] and {str(r):n for r,n in newprof.items()}==report['new_raw_profile'],'both raw rank profiles')
 need(sum(oldprof.values())==1710 and sum(newprof.values())==407 and sum(r*n for r,n in oldprof.items())==sum(r*n for r,n in newprof.items())==3200,'rank3200 and actual407 calls')
 extra={r:fcheck['ranks'][r]-newprof[r]-nativeprof[r] for r in fcheck['ranks'].keys()|newprof.keys()|nativeprof.keys()}
 extra={r:n for r,n in extra.items() if n};need(extra=={9:8},'eight actually emitted rank9 packet calls')
 names={v:int(k) for k,v in parent['private_role_map'].items()}
 routes=[]
 for j,blocks in sorted(byrole.items()):
  route=[blocks[0]['replacement'][2]]+[b['replacement'][3] for b in blocks]
  ranks=[len(source['frames'][b['replacement'][3]])-len(source['frames'][b['replacement'][2]]) for b in blocks]
  if len(blocks)>1:routes.append({'logical_role':names[j],'physical_role':j,'route':route,'ranks':ranks})
  else:need(ranks==[8],'every unobserved route is one full rank8 call')
 need({r['logical_role']:r['route'] for r in routes}=={116:[3,449,929,131],144:[3,911,157],145:[3,914,158],160:[3,911,171],161:[3,914,172],172:[3,524,183]},'exact six observation routes')
 negative={}
 for j,blocks in byrole.items():
  if len(blocks)>1:
   try:replacement(j,blocks[0]['parent_events']+blocks[1]['parent_events'])
   except ValueError as e:negative['merge_across_observation']=str(e)
   break
 need('barrier' in negative.get('merge_across_observation',''),'negative merger detected')
 rec=next(r for r in records if len(r['parent_events'])>1);mutant=[o.copy() for o in new];mutant[rec['physical_event']][2]=old[rec['parent_events'][1]][2]
 try:h.typed(source,dict(word,program=mutant))
 except ValueError as e:negative['removed_intermediate_source']=str(e)
 need('MOVE source' in negative.get('removed_intermediate_source',''),'stale intermediate chart rejected physically')
 inv=read(PACK/'INPUT-INVOICE.json',IPIN)
 need((PACK/'INPUT-INVOICE.json').read_bytes()==(REPO/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json').read_bytes(),'authentic identical source caller invoice')
 T={int(r):n for r,n in inv['T4'].items()};P={int(r):n for r,n in inv['P4'].items()}
 finalP={r:P.get(r,0)+18*(newprof[r]-oldprof[r])+18*extra.get(r,0) for r in P.keys()|oldprof.keys()|newprof.keys()|extra.keys()}
 need(all(n>=0 for n in finalP.values()),'nonnegative complete paid histogram')
 caller=report['conditional_caller']
 need(caller['T4']=={str(r):n for r,n in T.items()} and caller['P_rewritten_partial']=={str(r):n for r,n in finalP.items()},'full caller recomputation with actual8 packets and407 raw calls')
 need(caller['added_paid_per_native']=={'9':8} and caller['remaining_E8_residual_terms']==parent_review['remaining_terms']==4985 and caller['completed_firstY_receivers']==0,'honest partial invoice and residual scope')
 need(sum(T.values())==caller['target_positions']==27344 and sum(finalP.values())==caller['paid_positions']==129114,'exact target and paid call counts')
 ranksurplus=sum(r*(T.get(r,0)-finalP.get(r,0)) for r in T.keys()|finalP.keys());need(ranksurplus==caller['rank_surplus']==3760,'full rank surplus')
 powers={r:h.root_bracket(r) for r in T.keys()|P.keys()|finalP.keys()|oldprof.keys()|newprof.keys()}
 saved=h.moment_interval({r:oldprof[r]-newprof[r] for r in oldprof.keys()|newprof.keys()},powers)
 margin=tuple(v/18 for v in h.moment_interval({r:T.get(r,0)-finalP.get(r,0) for r in T.keys()|finalP.keys()},powers))
 oldmargin=tuple(v/18 for v in h.moment_interval({r:T.get(r,0)-P.get(r,0) for r in T.keys()|P.keys()},powers))
 need(F(report['saved_moment_lower'])<=saved[0]<=saved[1]<=F(report['saved_moment_upper']),'exact enclosure of route saving')
 need(F(caller['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(caller['remaining_moment_per_native_upper']),'exact enclosure of full remaining conditional moment')
 need(F(caller['original_H4_allowance_lower'])<=oldmargin[0]<=oldmargin[1]<=F(caller['original_H4_allowance_upper']),'original H4 moment independently recomputed')
 alternative=(oldmargin[0]+saved[0]-8*powers[9][1],oldmargin[1]+saved[1]-8*powers[9][0])
 need(max(margin[0],alternative[0])<=min(margin[1],alternative[1]),'full histogram and H4+saved-8*9^t agree')
 need(margin[0]>0,'strict positive conditional remaining moment')
 omitted=dict(finalP);omitted[9]-=144
 need(omitted!={int(r):n for r,n in caller['P_rewritten_partial'].items()},'omitted packet charge negative control')
 negative['omit_eight_rank9_packets']='Rejected: actual partial word emits144 caller rank9 packet calls.'
 chart=read(PACK/'CHART-MAPS.json','008b6f2551fabfcf48cefa4bae411d248edfcbddba4212f1343603166a44f336')
 oldmaps={(o[2],o[3]) for o in old if o[0]=='MOVE'};newmaps={(o[2],o[3]) for o in new if o[0]=='MOVE'};introduced=newmaps-oldmaps
 need({(r['source'],r['target']) for r in chart['recipes']}==introduced and len(chart['recipes'])==len(introduced)==209,'exact introduced recipe coverage')
 for r in chart['recipes']:need(r['recipe']['rank']==len(source['frames'][r['target']])-len(source['frames'][r['source']]),'every introduced recipe claims exact complete transport rank')
 need(chart['source_sha256']==SPIN and chart['parent_sha256']==PPIN and chart['word_sha256']==FPIN,'chart receipt exact input pins')
 for name,pin in chart['engine_pins'].items():need(digest((REPO/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'actual frozen chart engine pin')
 need(chart['wrong_global_phase_rejected'] is True,'author chart-replay negative phase receipt present')
 result={'status':'PASS_INDEPENDENT_SEVEN_CORRECTION_FUSION_AND_INVOICE','source_sha256':SPIN,'parent_compressed_sha256':PPIN,'parent_payload_sha256':PPAY,'parent_independent_review_sha256':'0afb0bec5d68b9ad2db80ee9e79e81581689072b76bcc9d33c01b499970957c3','word_compressed_sha256':FPIN,'word_payload_sha256':FPAY,'reviewed_proof_sha256':proofpin,'parent_instructions':len(old),'fused_instructions':len(new),'raw_moves_before':1710,'raw_moves_after':407,'removed_actual_raw_MOVEs':1303,'removed_actual_raw_chart_visits':len(oldvisits-newvisits),'raw_rank_sum':3200,'raw_before_profile':dict(sorted(oldprof.items())),'raw_after_profile':dict(sorted(newprof.items())),'counts':dict(fcheck['counts']),'MOVE_profile':dict(sorted(fcheck['ranks'].items())),'peak_owned':43,'actual_raw_arithmetic_instructions_preserved':len(pcheck['raw_uses']),'non_MOVE_instructions_preserved':sum(n for k,n in fcheck['counts'].items() if k!='MOVE'),'observed_receiver_routes':routes,'final_charts_identical':True,'all_non_MOVE_instructions_literal_and_ordered':True,'all1480_common_outputs_preserved':True,'exact_seven_cancelled_coefficients_preserved':True,'all_other4985_residual_coefficients_preserved':True,'private_inverse_rows_preserved':400,'conditional_paid_profile':dict(sorted(finalP.items())),'conditional_target_profile':dict(sorted(T.items())),'conditional_target_positions':27344,'conditional_paid_positions':129114,'conditional_rank_surplus':3760,'actual_packet_calls_per_native':extra,'route_saving_exact_bounds':[str(x) for x in saved],'route_saving_approximate':float(saved[0]),'conditional_remaining_exact_bounds':[str(x) for x in margin],'conditional_remaining_approximate':float(margin[0]),'negative_controls':negative,'introduced_chart_recipe_coverage':209,'chart_recipe_review_scope':'Pins, coverage and rank checked here. The existing exact Clifford/signed-Pauli recipe verification is credited to its inherited engine run, not re-authored or re-run by this checker.','physical_equivalence':'Each nested whole-field leg is C_destination C_source^-1. In a segment no other instruction touches this carrier; all other-field actions commute with the delayed move. The complete product telescopes, including phase and layout, to the one final direct move. This preserves every subsequent actual interface under the retained chart/compiler contracts.','scope':'Independent full literal fusion reconstruction from actual barriers, physical chart walk, source/parent/recipe pins, and exact full caller invoice. Full1880-input equality, seven cancellations and inverse inherit the independently authenticated parent by whole-field composition. No author code imported, no new dense baseline replay, no new general supplier or exponent. Removed stops are unavailable.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
