#!/usr/bin/env python3
"""Independent source-to-word review of the fresh one/two/three-facet words.

Imports only Worker C's independently written geometry and word machinery.
No author generator, verifier, or imported recovered helper is executed.
"""
import argparse,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from cohort_geometry import SOURCE_PIN,space,root,require
from check_cohort_word import (load,sha,typed,prefix_execute,rowadd,combine,
                              moment,PARENT_PIN,PARENT_PAYLOAD,INVOICE_PIN)

SPECS={
 'one':dict(xs=[77],payload='071e4a15a2bc3b4f4bb2ce2d357501319cc7bb7fd471616f1bb3e03cc14ab4a6',
            ops=74856,restore=611,raw=455,maps=48,residual=4937,
            rawhist={1:53,2:2,5:1,6:1,7:52,8:346}),
 'two':dict(xs=[56,77],payload='690ed9a6c4318c24c2c1d340d605b1df60b69f754366e768f8dbc481a4d3a494',
            ops=74943,restore=690,raw=485,maps=78,residual=4889,
            rawhist={1:63,2:22,5:1,6:21,7:62,8:316}),
 'three':dict(xs=[56,77,100],payload='f96e86acdec027effc88814e2f4fc522c0961bd6d826f6f12e20853bc1d51b52',
            ops=75085,restore=818,raw=508,maps=99,residual=4841,
            rawhist={1:61,2:43,3:4,5:5,6:48,7:48,8:299})
}

def data(source,name):
 xs=sorted(source['live']);selected=SPECS[name]['xs'];ys=[x+112 for x in selected]
 roots={x:root(source['frames'][source['initial'][x]][0]) for x in xs}
 A={(y,d):-F(sum(a*b for a,b in zip(roots[y-112],roots[d])),8)
    for y in ys for d in xs if d!=y-112}
 for y in ys:A[y,y-112]=F(0)
 groups=defaultdict(list)
 for d in xs:
  support=tuple(y for y in ys if A[y,d])
  if support:groups[support].append(d)
 spans=[space(frame) for frame in source['frames']];charts={};extra=[]
 for support in sorted(groups):
  target=set.intersection(*(set(spans[source['final'][y]]) for y in support))
  matches=[i for i,s in enumerate(spans) if s==target]
  if matches:charts[support]=min(matches)
  else:
   # This fixed rationally independent binary basis is checked against the
   # source-derived exact facet intersection, not trusted as an intersection.
   basis=[3,25,41,72,132,260]
   require(name=='three' and len(support)==3 and space(basis)==target,'only required added triple intersection')
   charts[support]=len(spans);spans.append(space(basis))
   extra.append(dict(index=1095,frame=basis,source_facets=[source['final'][y] for y in support],construction='exact intersection of final facets'))
  for d in groups[support]:require(space(source['frames'][source['initial'][d]])<spans[charts[support]],'each source donor fits its actual acquisition chart')
 require(all(sum(bool(A[y,d]) for d in xs)==48 for y in ys),'48 exact nonzero foreign coefficients per receiver')
 return dict(xs=xs,ys=ys,A=A,groups=dict(groups),charts=charts,extra=extra)

def emit_word(source,parent,name,d):
 old=parent['program'];raw={int(k):v for k,v in parent['private_role_map'].items()}
 hoist={o[1]:e for e,o in enumerate(old[410:514],410)}
 require(len(hoist)==104 and {raw[x] for x in d['xs']}==set(hoist),'exact original104 hoist events')
 out=old[:410].copy();lineage=list(range(410));collectors={};checks=[];reads=[]
 def emit(op,event=None):
  out.append(op);lineage.append(event);return len(out)-1
 def move(j,s,t,event):return emit(['MOVE',j,s,t,False],event)
 for support in sorted(d['groups'],key=lambda s:(len(s),s)):
  for y in support:
   owner=1937+len(collectors);collectors[support,y]=owner;emit(['INIT',owner,d['charts'][support]])
 delivery={(168,189):189,(168,212):168,(189,212):212} if name=='three' else {}
 pivots={s:min(d['groups'][s]) for s in delivery}
 for e,op in enumerate(old[410:514],410):
  donor=next(x for x in d['xs'] if raw[x]==op[1]);support=tuple(y for y in d['ys'] if d['A'][y,donor])
  if donor in pivots.values():continue
  if not support:emit(op,e);continue
  c=d['charts'][support];move(raw[donor],source['initial'][donor],c,e)
  for y in support:emit(['ADD',collectors[support,y],raw[donor],str(d['A'][y,donor]),c])
  move(raw[donor],c,127,e)
 for support,pivot in pivots.items():
  c=d['charts'][support];y=delivery[support];other=next(t for t in support if t!=y);e=hoist[raw[pivot]]
  move(raw[pivot],source['initial'][pivot],c,e)
  emit(['ADD',collectors[support,other],raw[pivot],str(d['A'][other,pivot]),c])
  emit(['SCALE',raw[pivot],str(d['A'][y,pivot]),c])
  emit(['ADD',raw[pivot],collectors[support,y],'1',c]);emit(['CLEAR',collectors[support,y],c])
  move(raw[pivot],c,source['final'][y],e)
  checks.append(dict(event=len(out),kind='encoded_pivot_at_facet',role=raw[pivot],row={x:d['A'][y,x] for x in d['groups'][support]},donor=pivot))
  emit(['ADD',collectors[(y,),y],raw[pivot],'1',source['final'][y]])
  move(raw[pivot],source['final'][y],127,e)
  for x in d['groups'][support]:
   if x!=pivot:emit(['ADD',raw[pivot],raw[x],str(-d['A'][y,x]),127])
  emit(['SCALE',raw[pivot],str(1/d['A'][y,pivot]),127])
  checks.append(dict(event=len(out),kind='restored_pivot',role=raw[pivot],row={pivot:F(1)},donor=pivot))
 restore=len(out);require(restore==SPECS[name]['restore'],'actual restoration boundary')
 for e,op in enumerate(old[514:],514):
  y=next((y for y in d['ys'] if op[0]=='MOVE' and op[1]==raw[y] and op[3]==source['final'][y]),None)
  if y is None:emit(op,e);continue
  stops=[]
  if name=='three':stops.append(tuple(d['ys']))
  if name=='two':stops.append(tuple(d['ys']))
  if name=='three':stops.append(next(s for s,t in delivery.items() if y in s and y!=t))
  stops.append((y,));current=3
  for s in stops:
   c=d['charts'][s];move(raw[y],current,c,e);current=c
   reads.append(dict(event=len(out),receiver=y,owner=collectors[s,y],support=s))
   emit(['ADD',raw[y],collectors[s,y],'1',c]);emit(['CLEAR',collectors[s,y],c])
 return out,lineage,restore,checks,reads,collectors

def semantic(source,parent,word,d,lineage,restore,checks,reads):
 raw={int(k):v for k,v in word['private_role_map'].items()};q={x:{raw[x]:F(1),x:F(-1)} for x in raw}
 checkpoints={x['event']:x for x in checks};reads_by_event={x['event']:x for x in reads};check_count=0;e8reads=[]
 xroles={raw[x]:x for x in d['xs']}
 delivery={(168,189):189,(168,212):168,(189,212):212} if len(d['ys'])==3 else {}
 def expected(coeff):return combine(list(coeff.values()),[q[x] for x in coeff])
 def observe(e,state,loc,op):
  nonlocal check_count
  if e in checkpoints:
   c=checkpoints[e];require(state[c['role']]==expected(c['row']),'actual original-input '+c['kind']);check_count+=1
  if e==restore:
   for x in d['xs']:
    require(state[raw[x]]==q[x] and loc[raw[x]]==127,'every104 raw original restored before retained E8 observations');check_count+=1
  if e in reads_by_event:
   c=reads_by_event[e];support=c['support'];y=c['receiver'];donors=set(d['groups'][support])
   if len(support)==1:
    for s,t in delivery.items():
     if t==y:donors.update(d['groups'][s])
   require(state[c['owner']]==expected({x:d['A'][y,x] for x in donors}),'actual source-derived complete collector row at consumption');check_count+=1
  if op and lineage[e] is not None and 514<=lineage[e]<parent['marks']['initial_decoders'] and op[0]=='ADD' and op[2] in xroles:
   x=xroles[op[2]];require(state[op[2]]==q[x] and loc[op[2]]==127,'actual original q at each retained E8 read');e8reads.append(e)
 before,loc0=prefix_execute(parent,parent['marks']['common_starts'])
 after,loc1=prefix_execute(word,word['marks']['common_starts'],observe)
 require(len(e8reads)==520,'all520 actual original E8 source reads')
 require(set(after)==set(before) and loc0==loc1,'identical complete public/owned prefix interface')
 deltas={raw[y]:expected({x:d['A'][y,x] for x in d['xs'] if d['A'][y,x]}) for y in d['ys']}
 for j in before:require(after[j]==rowadd(before[j],deltas.get(j,{})),'all1880-column prefix difference is exactly the source correction')
 suffix=word['program'][word['marks']['common_starts']:]
 require(suffix==parent['program'][parent['marks']['common_starts']:],'entire unchanged common-and-final suffix')
 for y in d['ys']:
  j=raw[y];touches=[]
  for op in suffix:
   operands=op[1:3] if op[0] in ('ADD','COPY') else op[1:2]
   if j in operands:touches.append(op)
  require(touches==[['ADD',j,y,'1',source['final'][y]]],'changed private receiver isolated until real final common recoupling')
 return dict(exact_input_coordinates=1880,checkpoint_rows=check_count,restored_original_donors=104,
             authentic_E8_reads=520,collector_consumptions=len(reads),pivot_checkpoints=len(checks),
             unchanged_suffix_instructions=len(suffix),changed_private_rows=len(deltas),
             full_prefix_delta_sha256=sha(json.dumps({str(j):[[i,str(v)] for i,v in sorted(row.items())] for j,row in sorted(deltas.items())},sort_keys=True).encode()))

def inverse_check(source,parent,word,d):
 logical={int(r) for r in word['private_role_map']};xs=d['xs'];roots={x:root(source['frames'][source['initial'][x]][0]) for x in xs}
 coupled=set(range(104))-set(source['hosted']['Dports']);matrix={r:{r:F(1)} for r in logical};remaining=0
 for i,x in enumerate(xs):
  y=x+112;c=F(1,2) if i in coupled else F(1);row={y:c}
  for donor in xs:
   v=c*F(sum(a*b for a,b in zip(roots[x],roots[donor])),8)
   if v:row[donor]=v
  for donor,v in parent['corrections'].get(str(y),[]):row=rowadd(row,{donor:F(v)})
  if y in d['ys']:row={y:F(1),x:F(1)}
  matrix[y]=row;remaining+=sum(bool(v) for donor,v in row.items() if donor not in (x,y))
 inverse={r:{r:F(1)} for r in logical}
 for x in xs:
  y=x+112;c=matrix[y][y];inverse[y]={y:1/c}
  for donor,v in matrix[y].items():
   if donor!=y:inverse[y][donor]=-v/c
 for r,row in inverse.items():require(combine(list(row.values()),[matrix[k] for k in row])=={r:F(1)},'explicit terminal400-row left inverse')
 serial=lambda m:{str(r):[[j,str(v)] for j,v in sorted(row.items())] for r,row in sorted(m.items())}
 return dict(rows=400,remaining_residual_coefficients=remaining,matrix_sha256=sha(json.dumps(serial(matrix),sort_keys=True).encode()),inverse_sha256=sha(json.dumps(serial(inverse),sort_keys=True).encode()))

def negative_controls(source,parent,word,d,lineage,restore,checks,reads):
 rejected={}
 def trial(name,ops,algebra=False,charts=None):
  candidate=dict(word,program=ops)
  if charts is not None:candidate['additional_charts']=charts
  try:
   typed(source,candidate)
   if algebra:semantic(source,parent,candidate,d,lineage,restore,checks,reads)
  except ValueError as e:rejected[name]=str(e)
  require(name in rejected,'negative control escaped '+name)
 def copyops():return [op.copy() for op in word['program']]
 first=next(e for e in range(410,restore) if word['program'][e][0]=='ADD')
 ops=copyops();ops[first][3]=str(-F(ops[first][3]));trial('wrong_foreign_coefficient',ops,True)
 r=reads[0];ops=copyops();ops[r['event']][3]='-1';trial('wrong_collector_read',ops,True)
 move_event=r['event']-1;ops=copyops();ops.pop(move_event);trial('omitted_actual_receiver_arrival',ops)
 # A live owned record cannot be retired before its last source observation.
 ops=copyops();clear=next(e for e in range(r['event'],len(ops)) if ops[e][:2]==['CLEAR',r['owner']]);op=ops.pop(clear);ops.insert(r['event'],op);trial('premature_collector_retirement',ops)
 if checks:
  scale=next(e for e in range(410,restore) if word['program'][e][0]=='SCALE');ops=copyops();ops[scale][2]=str(-F(ops[scale][2]));trial('wrong_live_pivot_encoding',ops,True)
  inverse_event=next(c['event']-1 for c in checks if c['kind']=='restored_pivot');ops=copyops();ops[inverse_event][2]=str(-F(ops[inverse_event][2]));trial('wrong_pivot_inverse',ops,True)
  charts=[dict(c) for c in word['additional_charts']];charts[0]['frame']=charts[0]['frame'][1:];trial('missing_triple_chart_direction',copyops(),charts=charts)
 else:
  hub=next(e for e in range(410,restore) if word['program'][e][0]=='MOVE' and word['program'][e][2] in {source['final'][y] for y in d['ys']} and word['program'][e][3]==127)
  ops=copyops();ops.pop(hub);trial('omitted_required_hub_return',ops)
 return rejected

def check_variant(a,source,parent,prior,invoice,name):
 spec=SPECS[name];package=a.packages/name;word=load(package/'WORD.json.gz',True,payload=spec['payload']);report=load(package/'RESULT.json')
 d=data(source,name);expected,lineage,restore,checks,reads,collectors=emit_word(source,parent,name,d)
 require(word['program']==expected and word['parent_event_of_output']==lineage,'every literal instruction and parent-event mapping independently emitted')
 require(len(expected)==spec['ops'] and word['initial']==parent['initial'] and word['public']==1880,'complete source and input namespace')
 require(word['private_role_map']==parent['private_role_map'] and word['additional_charts']==d['extra'],'exact role labels and independently derived added charts')
 require(word['owned_fields']==57+len(collectors),'actual owned declaration extent')
 positions={e:i for i,e in enumerate(lineage) if e is not None}
 require(word['native_event_to_physical']==[positions[e] for e in parent['native_event_to_physical']],'all71261 native event positions')
 for key,e in parent['marks'].items():require(word['marks'][key]==positions[e],'authentic inherited mark '+key)
 require(word['marks']['all_active_donors_restored']==restore,'exact original restoration marker')
 require(word['newly_completed_firstY_receivers']==d['ys'],'selected ordinary receiver claims')
 c=word['facet_collection'];require(c['receivers']==d['ys'],'source selected receivers')
 reported_groups={tuple(g['receivers']):g for g in c['support_classes']}
 require(set(reported_groups)==set(d['groups']),'all and only source-derived support classes')
 for s,donors in d['groups'].items():require(reported_groups[s]['donors']==donors and reported_groups[s]['chart']==d['charts'][s],'exact donors and actual acquisition chart')
 require(set(parent['corrections']).isdisjoint(map(str,d['ys'])),'no inherited correction double counted')
 expected_corrections=dict(parent['corrections'])
 for y in d['ys']:expected_corrections[str(y)]=[[x,str(d['A'][y,x])] for x in d['xs'] if d['A'][y,x]]
 require(word['corrections']==expected_corrections,'exact source-derived correction metadata')
 bill=typed(source,word);oldbill=typed(source,parent)
 require(bill['final']==oldbill['final'] and bill['peak']==43,'all complete final locations and actual peak occupancy')
 require(bill['counts']==report['bill']['opcode_counts'] and bill['ranks']=={int(k):v for k,v in report['bill']['move_rank_histogram'].items()},'complete exact opcode and rank bills')
 require(bill['rawranks']==spec['rawhist'] and sum(bill['rawranks'].values())==spec['raw'],'exact raw tariff profile')
 require(sum(r*n for r,n in bill['rawranks'].items())==3200,'raw rank mass preserved')
 sem=semantic(source,parent,word,d,lineage,restore,checks,reads);inv=inverse_check(source,parent,word,d)
 require(inv['remaining_residual_coefficients']==spec['residual']==4985-48*len(d['ys']),'exact48 canceled coefficients per selected ordinary receiver')
 negative=negative_controls(source,parent,word,d,lineage,restore,checks,reads)
 logical={int(k) for k in parent['private_role_map']}
 oldraw=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE' and op[1] in logical)
 require(oldraw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'original1710 raw invoice source')
 native=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE')
 extra=bill['ranks'].copy();extra.subtract(native);extra.subtract(bill['rawranks'])
 require({r:n for r,n in extra.items() if n}=={9:8},'unchanged eight paid rank9 packets counted exactly once')
 T={int(k):v for k,v in invoice['T4'].items()};P={int(k):v for k,v in invoice['P4'].items()}
 paid={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|{9}}
 require(all(n>=0 for n in paid.values()) and paid=={int(k):v for k,v in report['conditional_caller']['P_partial'].items()},'independently recomposed complete caller paid histogram')
 require(sum(T.values())==27344 and sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys())==3760,'complete target count and rank surplus')
 margin=tuple(x/18 for x in moment({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()}))
 require(F(report['conditional_caller']['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(report['conditional_caller']['remaining_moment_per_native_upper']),'independent exact directed remaining-moment interval')
 maps=load(package/'CHART-MAPS.json');beforemaps={(op[2],op[3]) for op in parent['program'] if op[0]=='MOVE'};newmaps={(op[2],op[3]) for op in expected if op[0]=='MOVE'};introduced=newmaps-beforemaps
 require({(r['source'],r['target']) for r in maps['recipes']}==introduced and len(introduced)==spec['maps'],'every actual introduced map covered')
 frames=source['frames']+[c['frame'] for c in d['extra']]
 for r in maps['recipes']:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']]),'actual introduced map rank')
 require(maps['word_sha256']==sha((package/'WORD.json.gz').read_bytes()) and maps['parent_sha256']==PARENT_PIN and maps['source_sha256']==SOURCE_PIN and maps['wrong_global_phase_rejected'],'chart engine source pins and negative global-phase control')
 for file,pin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/file).read_bytes())==pin,'retained exact chart engine pin')
 result=dict(status='PASS_INDEPENDENT_FRESH_'+name.upper()+'_WORD',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,parent_payload_sha256=PARENT_PAYLOAD,
             word_sha256=sha((package/'WORD.json.gz').read_bytes()),word_payload_sha256=spec['payload'],independent_checker_sha256=sha(Path(__file__).read_bytes()),
             literal_instructions=len(expected),source_support_classes=len(d['groups']),selected_receivers=d['ys'],counts=dict(bill['counts']),
             raw_calls=spec['raw'],raw_rank_mass=3200,raw_profile=dict(bill['rawranks']),owned_peak=43,owned_lifetimes=bill['counts']['INIT'],
             restored_original_donors_at=restore,semantics=sem,private_inverse=inv,all1480_common_outputs_preserved=True,all1880_input_directions_retained=True,
             completed_first_pairs=len(d['ys']),completed_reverse_pairs=0,remaining_residual_coefficients=spec['residual'],
             paid_positions=sum(paid.values()),target_positions=27344,rank_surplus=3760,conditional_paid_profile=paid,conditional_target_profile=T,
             remaining_moment_exact=[str(v) for v in margin],remaining_moment_approx=float(margin[0]),introduced_map_coverage=spec['maps'],negative_controls=negative,
             chart_engine_scope='Retained author exact-engine run credited through pins; actual introduced map coverage, geometry and ranks independently checked here.',
             scope='Fresh-provenance finite normalized source construction, full symbolic original-input prefix and isolated unchanged suffix. Not the lost S007 payload identity, a new raw-pivot theorem, a physical supplier, a completed reverse family or a new kappa.')
 return result

def main(a):
 parentdir=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused'
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN)
 parent=load(parentdir/'WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD)
 prior=load(parentdir/'review/REVIEW-RESULT.json',pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e')
 require(prior['all1480_common_outputs_preserved'] and prior['private_inverse_rows_preserved']==400 and prior['all_other4985_residual_coefficients_preserved'],'admitted parent facts with exact review pin')
 invoice=load(parentdir/'INPUT-INVOICE.json',pin=INVOICE_PIN)
 result={name:check_variant(a,source,parent,prior,invoice,name) for name in SPECS}
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({name:{k:v for k,v in r.items() if k in ('status','literal_instructions','raw_calls','remaining_moment_approx','remaining_residual_coefficients','negative_controls','word_payload_sha256')} for name,r in result.items()},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--packages',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
