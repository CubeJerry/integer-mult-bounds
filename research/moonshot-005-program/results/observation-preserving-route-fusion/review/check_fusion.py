#!/usr/bin/env python3
"""Independent certificate check of observation-preserving raw route fusion."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
from collections import Counter,defaultdict
import gzip,hashlib,json,bisect
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'root-research/route_fusion';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPIN='c75f595393d32f0ddefed906e9dab02e6e09b764730684541375d6979c6c349c'
FPIN='6e647902f0685e1217ee2df5529714a3d4bec92d3ad3f1024cf12c02ece154bb'
PAYLOAD='d6fe8441505d834913e282af5c595b81c0c2e15f3d0f646d14ac1442fc56e400'
def need(a,b):
 if not a:raise ValueError(b)
def load_gz(path,pin):
 b=path.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'file pin '+str(path));return json.loads(gzip.decompress(b))
def space(vs):
 s={0}
 for v in vs:s.update([x^v for x in s.copy()])
 return s
def operands(op):return op[1:3] if op[0] in ('ADD','COPY') else [op[1]]
def root_bracket(r):
 D=1<<160;target=r**199*D**200
 with localcontext() as ctx:
  ctx.prec=100;guess=int((Decimal(r)**(Decimal(199)/200))*D)
 while guess**200>target:guess-=1
 while (guess+1)**200<=target:guess+=1
 need(guess**200<=target<(guess+1)**200,'certified exact integer power bracket')
 return F(guess,D),F(guess if guess**200==target else guess+1,D)
def moment_interval(profile,powers):
 lo=hi=F(0)
 for r,c in profile.items():
  a,b=powers[r];lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi

def typed(source,word):
 loc=dict(enumerate(word['initial']));counts=Counter();ranks=Counter();rawranks=Counter();peak=0;frames=list(map(space,source['frames']));uses={}
 for event,op in enumerate(word['program']):
  kind,j=op[:2];counts[kind]+=1;need(0<=j<word['public']+word['owned_fields'],'role namespace')
  if kind=='INIT':need(j>=word['public'] and j not in loc,'owned INIT');loc[j]=op[2]
  elif kind=='CLEAR':need(j>=word['public'] and loc.get(j)==op[2],'owned CLEAR');del loc[j]
  elif kind=='MOVE':
   a,b,owned=op[2:];need(loc.get(j)==a and type(owned)is bool and owned==(j>=word['public']),'MOVE source location/owner')
   need(frames[a]<frames[b] or owned and frames[b]<frames[a],'proper nested MOVE')
   rank=abs(len(source['frames'][a])-len(source['frames'][b]));ranks[rank]+=1
   if 1480<=j<1880:rawranks[rank]+=1;need(not owned and frames[a]<frames[b],'public raw upward MOVE')
   loc[j]=b
  elif kind in ('ADD','COPY'):
   r,c,chart=op[2:];need(j!=r and loc.get(j)==loc.get(r)==chart,'actual cochart arithmetic');F(c)
  elif kind=='SCALE':need(loc.get(j)==op[3] and F(op[2]),'actual cochart SCALE')
  else:raise ValueError(kind)
  if kind!='MOVE':
   touched=[r for r in operands(op) if 1480<=r<1880]
   if touched:uses[event]={r:loc[r] for r in touched}
  peak=max(peak,len(loc)-word['public'])
 need(set(loc)==set(range(word['public'])),'all owned lifetimes close')
 return {'counts':counts,'ranks':ranks,'rawranks':rawranks,'peak':peak,'final_locations':loc,'raw_uses':uses}

def main():
 source=load_gz(REPO/'research/shared-wire-split-composition/data/final.json.gz',SPIN)
 parent=load_gz(REPO/'research/moonshot-005-program/results/unit17-precompensation/WORD.json.gz',PPIN)
 word=load_gz(PACK/'WORD.json.gz',FPIN)
 need(hashlib.sha256(gzip.decompress((PACK/'WORD.json.gz').read_bytes())).hexdigest()==PAYLOAD,'fused payload pin')
 report=json.loads((PACK/'RESULT.json').read_text());proof_bytes=(PACK/'PROOF.md').read_bytes();frames=list(map(space,source['frames']))
 raw=set(parent['difference_role_map'].values());need(raw==set(range(1480,1880)),'all actual raw carriers')
 old,new=parent['program'],word['program'];lineage=word['parent_event_of_output'];records=word['private_route_blocks']
 need(word['source_sha256']==SPIN and word['parent_word_sha256']==PPIN,'inherited source and parent pins')
 need(len(lineage)==len(new) and lineage==sorted(set(lineage)) and all(0<=i<len(old) for i in lineage),'strict complete event lineage')
 need(parent['initial']==word['initial'] and parent['public']==word['public']==1880 and parent['owned_fields']==word['owned_fields']==181,'unchanged physical field interface')
 uses=defaultdict(list);moves=defaultdict(list)
 for i,op in enumerate(old):
  if op[0]=='MOVE' and op[1] in raw:moves[op[1]].append(i)
  elif op[0]!='MOVE':
   for r in operands(op):
    if r in raw:uses[r].append(i)
 def validate_segment(role,events):
  need(events and events==sorted(set(events)),'ordered route segment')
  actual=moves[role][bisect.bisect_left(moves[role],events[0]):bisect.bisect_right(moves[role],events[-1])]
  need(actual==events,'all intervening same-carrier MOVEs included')
  u=uses[role];idx=bisect.bisect_left(u,events[0])
  need(idx==len(u) or u[idx]>events[-1],'intervening non-MOVE use role '+str(role)+' event '+str(u[idx] if idx<len(u) else None))
  start=old[events[0]][2];current=start
  for event in events:
   op=old[event];need(op==['MOVE',role,current,op[3],False] and frames[current]<frames[op[3]],'exact strictly ascending parent chain')
   current=op[3]
  need(frames[start]<frames[current],'direct transport is proper upward nesting')
  return ['MOVE',role,start,current,False]
 covered=[];emitted={};byrole=defaultdict(list)
 for rec in records:
  role=rec['role'];events=rec['parent_events'];need(role in raw,'raw segment owner')
  expected=validate_segment(role,events);pos=rec['physical_event']
  need(rec['emitted_at_parent_event']==events[-1] and lineage[pos]==events[-1] and rec['replacement']==new[pos]==expected,'replacement at final old MOVE')
  need(pos not in emitted,'unique emitted MOVE');emitted[pos]=rec;covered+=events;byrole[role].append(rec)
 all_old_raw={i for rows in moves.values() for i in rows}
 need(len(covered)==len(set(covered))==1710 and set(covered)==all_old_raw,'all original raw MOVEs partitioned exactly once')
 need(set(emitted)=={i for i,op in enumerate(new) if op[0]=='MOVE' and op[1] in raw},'exactly one emitted call per block')
 retained=set(lineage);removed=set(range(len(old)))-retained
 need(len(removed)==1305 and removed<=all_old_raw,'only authenticated raw MOVEs removed')
 for pos,original in enumerate(lineage):
  if pos not in emitted:need(new[pos]==old[original] and word['marks'][pos]==parent['marks'][original],'every other literal instruction retained')
  else:need(word['marks'][pos]=='fused_private_route','fused instruction marker')
 for key,value in parent.items():
  if key not in ['program','marks','funded_raw_reservations','schema']:need(word[key]==value,'unchanged inherited metadata '+key)
 need('funded_raw_reservations' not in word,'removed reservations are not retained as a free route grant')
 pcheck=typed(source,parent);fcheck=typed(source,word)
 need(pcheck['final_locations']==fcheck['final_locations'],'all final physical charts preserved')
 need({lineage[i]:v for i,v in fcheck['raw_uses'].items()}==pcheck['raw_uses'],'every actual raw access at same chart')
 need(pcheck['peak']==fcheck['peak']==121,'owned occupancy unchanged')
 need({op:n for op,n in pcheck['counts'].items() if op!='MOVE'}=={op:n for op,n in fcheck['counts'].items() if op!='MOVE'},'non-MOVE counts unchanged')
 need(dict(fcheck['counts'])==report['operations'],'actual total instruction counts')
 oldprof=pcheck['rawranks'];newprof=fcheck['rawranks']
 need({str(k):v for k,v in oldprof.items()}==report['old_raw_profile'] and {str(k):v for k,v in newprof.items()}==report['new_raw_profile'],'exact raw rank profiles')
 need(sum(oldprof.values())==1710 and sum(newprof.values())==405 and sum(r*n for r,n in oldprof.items())==sum(r*n for r,n in newprof.items())==3200,'complete raw call and rank census')
 oldvisits={(r,sourcechart) for r,sourcechart in enumerate(parent['initial']) if r in raw}|{(op[1],op[3]) for op in old if op[0]=='MOVE' and op[1] in raw}
 newvisits={(r,sourcechart) for r,sourcechart in enumerate(word['initial']) if r in raw}|{(op[1],op[3]) for op in new if op[0]=='MOVE' and op[1] in raw}
 need(newvisits<=oldvisits and len(oldvisits-newvisits)==1305,'removed stops are actually absent')
 forbidden_merge=None
 for role,blocks in byrole.items():
  blocks.sort(key=lambda b:b['parent_events'][0])
  if len(blocks)>1:
   try:validate_segment(role,blocks[0]['parent_events']+blocks[1]['parent_events'])
   except ValueError as e:forbidden_merge=str(e)
   break
 need(forbidden_merge and 'non-MOVE' in forbidden_merge,'negative merger crosses an actual read/write barrier')
 record=next(r for r in records if len(r['parent_events'])>1);mutant=list(new);bad=list(mutant[record['physical_event']]);bad[2]=old[record['parent_events'][1]][2];mutant[record['physical_event']]=bad
 bad_source=None
 try:typed(source,dict(word,program=mutant))
 except ValueError as e:bad_source=str(e)
 need(bad_source and 'MOVE source' in bad_source,'negative stale intermediate source chart rejected')
 native_profile=Counter(abs(len(source['frames'][o[2]])-len(source['frames'][o[3]])) for o in source['program'] if o[0]=='MOVE')
 extra={r:pcheck['ranks'][r]-oldprof[r]-native_profile[r] for r in pcheck['ranks'].keys()|oldprof.keys()|native_profile.keys()}
 need({r:n for r,n in extra.items() if n}=={1:17},'seventeen actually emitted extra packet calls')
 invoice_path=REPO/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json';ib=invoice_path.read_bytes()
 need(hashlib.sha256(ib).hexdigest()=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','H4 invoice source pin')
 invoice=json.loads(ib);T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()}
 changed={r:P.get(r,0)+18*(newprof[r]-oldprof[r])+18*(17 if r==1 else 0) for r in P.keys()|newprof.keys()|oldprof.keys()}
 need(all(n>=0 for n in changed.values()),'nonnegative actual paid profile')
 caller=report['conditional_caller'];need({str(r):n for r,n in changed.items()}==caller['P_rewritten_partial'] and {str(r):n for r,n in T.items()}==caller['T4'],'literal changed caller invoice')
 powers={r:root_bracket(r) for r in T.keys()|P.keys()|changed.keys()|oldprof.keys()|newprof.keys()}
 saved=moment_interval({r:oldprof[r]-newprof[r] for r in oldprof.keys()|newprof.keys()},powers)
 need(F(report['saved_moment_lower'])<=saved[0]<=saved[1]<=F(report['saved_moment_upper']),'root saved-moment enclosure independently certified')
 margin=tuple(x/18 for x in moment_interval({r:T.get(r,0)-changed.get(r,0) for r in T.keys()|changed.keys()},powers))
 oldmargin=tuple(x/18 for x in moment_interval({r:T.get(r,0)-P.get(r,0) for r in T.keys()|P.keys()},powers))
 need(F(caller['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(caller['remaining_moment_per_native_upper']),'conditional remaining-moment enclosure')
 need(F(caller['original_H4_allowance_lower'])<=oldmargin[0]<=oldmargin[1]<=F(caller['original_H4_allowance_upper']),'original H4 allowance enclosure')
 need(sum(T.values())==caller['target_positions']==27344 and sum(changed.values())==caller['paid_positions']==129240,'complete target/paid position counts')
 need(sum(r*(T.get(r,0)-changed.get(r,0)) for r in T.keys()|changed.keys())==caller['rank_surplus']==4750,'conditional exact rank surplus')
 name={v:int(k) for k,v in parent['difference_role_map'].items()}
 multisegments=[{'raw_role':role,'logical_role':name[role],'segments':len(blocks),'ranks':[len(source['frames'][r['replacement'][3]])-len(source['frames'][r['replacement'][2]]) for r in sorted(blocks,key=lambda b:b['parent_events'][0])]} for role,blocks in sorted(byrole.items()) if len(blocks)>1]
 result={'status':'PASS_INDEPENDENT_OBSERVATION_PRESERVING_ROUTE_FUSION','source_sha256':SPIN,'parent_compressed_sha256':PPIN,'fused_compressed_sha256':FPIN,'fused_payload_sha256':PAYLOAD,'reviewed_proof_sha256':hashlib.sha256(proof_bytes).hexdigest(),'parent_instructions':len(old),'new_instructions':len(new),'removed_moves':len(removed),'route_segments':len(records),'old_raw_profile':dict(sorted(oldprof.items())),'new_raw_profile':dict(sorted(newprof.items())),'unchanged_raw_rank':3200,'non_MOVE_instructions_preserved':sum(n for op,n in pcheck['counts'].items() if op!='MOVE'),'actual_raw_use_instructions_preserved':len(pcheck['raw_uses']),'peak_owned':fcheck['peak'],'removed_raw_chart_visits':len(oldvisits-newvisits),'multi_segment_raw_roles':multisegments,'counts':dict(fcheck['counts']),'MOVE_rank_histogram':dict(sorted(fcheck['ranks'].items())),'saved_moment_exact_bounds':[str(x) for x in saved],'saved_moment_approximate':float(saved[0]),'remaining_conditional_moment_bounds':[str(x) for x in margin],'remaining_conditional_moment_approximate':float(margin[0]),'paid_positions':sum(changed.values()),'target_positions':sum(T.values()),'conditional_rank_surplus':4750,'negative_controls':{'merge_across_real_use':forbidden_merge,'stale_intermediate_source':bad_source},'physical_composition':'Under the retained exact chart representation C_c, each leg is C_destination C_source^(-1). Adjacent factors telescope exactly, including phase and layout, to the directly emitted proper nested transport. Scalar equality alone is not being substituted for that contract.','scope':'Independent literal lineage, barrier, geometry, type and exact invoice verification. Universal full-input equivalence follows compositionally from the authenticated parent and retained chart contracts; this checker does not rerun its dense1880-column replay or establish new physical/compiler foundations. Removed stops are unavailable without priced reinstatement.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
