#!/usr/bin/env python3
"""Independent literal/source-row audit of the dependent triple paired word."""
import argparse,json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from cohort_geometry import SOURCE_PIN,space,root,rank,bit_basis,require
from check_cohort_word import load,sha,inverse,rowadd,combine,typed,prefix_execute,moment,PARENT_PIN,PARENT_PAYLOAD,INVOICE_PIN
from selected_reverse_rank import examine,gram

WORD_PIN='19a7a89b4623f7f095833a46369fad7bf6d63eabd6bf5a7929ed52a87b55b121'
FORWARD_PIN='4be96b8164f389c69995fb202fc7194fae71d9989644ac89cd8d5622414ee3ad'
SELECTED=[0,1,98]

def setup(source):
 xs=sorted(source['live']);ys=[x+112 for x in SELECTED];roots={x:root(source['frames'][source['initial'][x]][0]) for x in xs}
 A={(y,x):F(y-112==x)-F(gram(roots,y-112,x),8) for y in ys for x in xs}
 groups={s:[] for k in (1,2) for s in combinations(ys,k)}
 for x in xs:
  support=tuple(y for y in ys if A[y,x])
  if support:require(support in groups,'actual support has two selected recipients');groups[support].append(x)
 spans=list(map(space,source['frames']));charts={};extra=[]
 for s in sorted(groups):
  C=set.intersection(*(set(spans[source['final'][y]]) for y in s));matches=[i for i,z in enumerate(spans) if z==C]
  if matches:charts[s]=min(matches)
  else:
   basis=bit_basis(C);c=1095+len(extra);charts[s]=c;extra.append(dict(index=c,frame=basis,source_facets=[source['final'][y] for y in s],construction='exact intersection of final facets'))
  for x in groups[s]:require(space(source['frames'][source['initial'][x]])<C,'actual source line inside its pair acquisition chart')
 require([len(groups[s]) for s in sorted(groups) if len(s)==2]==[24,24,24] and all(not ds for s,ds in groups.items() if len(s)==1),'three source24-donor cohorts')
 return dict(xs=xs,ys=ys,roots=roots,A=A,groups=groups,charts=charts,extra=extra)

def emit_forward(source,parent,d):
 old=parent['program'];raw={int(k):v for k,v in parent['private_role_map'].items()};hoist={o[1]:e for e,o in enumerate(old[410:514],410)}
 out=old[:410].copy();lineage=list(range(410));collectors={};checks=[];reads=[]
 def emit(op,event=None):out.append(op);lineage.append(event)
 def move(j,s,t,event):emit(['MOVE',j,s,t,False],event)
 for s in sorted(d['groups'],key=lambda s:(len(s),s)):
  for y in s:
   owner=1937+len(collectors);collectors[s,y]=owner;emit(['INIT',owner,d['charts'][s]])
 delivery={(112,113):113,(112,210):112,(113,210):210};pivots={s:min(d['groups'][s]) for s in delivery}
 for e,op in enumerate(old[410:514],410):
  x=next(x for x in d['xs'] if raw[x]==op[1]);s=tuple(y for y in d['ys'] if d['A'][y,x])
  if x in pivots.values():continue
  if not s:emit(op,e);continue
  c=d['charts'][s];move(raw[x],source['initial'][x],c,e)
  for y in s:emit(['ADD',collectors[s,y],raw[x],str(d['A'][y,x]),c])
  move(raw[x],c,127,e)
 for s,x in pivots.items():
  c=d['charts'][s];y=delivery[s];other=next(t for t in s if t!=y);e=hoist[raw[x]]
  move(raw[x],source['initial'][x],c,e);emit(['ADD',collectors[s,other],raw[x],str(d['A'][other,x]),c])
  emit(['SCALE',raw[x],str(d['A'][y,x]),c]);emit(['ADD',raw[x],collectors[s,y],'1',c]);emit(['CLEAR',collectors[s,y],c])
  move(raw[x],c,source['final'][y],e)
  checks.append(dict(event=len(out),role=raw[x],coeff={t:d['A'][y,t] for t in d['groups'][s]},kind='actual forward pivot payload'))
  emit(['ADD',collectors[(y,),y],raw[x],'1',source['final'][y]]);move(raw[x],source['final'][y],127,e)
  for donor in d['groups'][s]:
   if donor!=x:emit(['ADD',raw[x],raw[donor],str(-d['A'][y,donor]),127])
  emit(['SCALE',raw[x],str(1/d['A'][y,x]),127]);checks.append(dict(event=len(out),role=raw[x],coeff={x:F(1)},kind='actual restored forward pivot'))
 require(len(out)==823,'forward source restoration boundary823')
 for e,op in enumerate(old[514:],514):
  y=next((y for y in d['ys'] if op[0]=='MOVE' and op[1]==raw[y] and op[3]==source['final'][y]),None)
  if y is None:emit(op,e);continue
  visited=next(s for s,t in delivery.items() if y in s and y!=t);current=3
  for s in (visited,(y,)):
   c=d['charts'][s];move(raw[y],current,c,e);current=c
   donor_set=d['groups'][s] if len(s)==2 else d['groups'][next(t for t,z in delivery.items() if z==y)]
   reads.append(dict(event=len(out),role=collectors[s,y],coeff={x:d['A'][y,x] for x in donor_set},kind='actual forward collector read'))
   emit(['ADD',raw[y],collectors[s,y],'1',c]);emit(['CLEAR',collectors[s,y],c])
 return out,lineage,checks+reads

def emit_dual(source,forward,word,d):
 raw={int(k):v for k,v in forward['private_role_map'].items()};host={d['xs'][i]:(source['hosted']['X2'][j],source['hosted']['Y2'][j]) for j,i in enumerate(source['hosted']['Dports'])}
 phase=[];lineage=[];rows={};checkpoints=[];injections=[];groups=word['paired_collection']['groups']
 donors={x for s,ds in d['groups'].items() if len(s)==2 for x in ds if x in host}
 moved={host[x][0] for x in donors}|{host[x][1] for x in SELECTED}
 old=forward['program'];routes={j:next(e for e,op in enumerate(old) if op[0]=='MOVE' and op[1]==raw[j]) for j in moved}
 require(len(routes)==71 and all(sum(op[0]=='MOVE' and op[1]==raw[j] for op in old)==1 for j in moved),'all71 replaced routes really are single direct parent MOVEs')
 def event():return 410+len(phase)
 def emit(op,parent_event=None):phase.append(op);lineage.append(parent_event)
 def move(role,s,t):emit(['MOVE',raw[role],s,t,False],routes[role])
 for x in SELECTED:move(host[x][1],3,source['final'][x+112])
 actual_groups=[]
 for gi,s in enumerate(sorted(t for t in d['groups'] if len(t)==2)):
  ds=[x for x in d['groups'][s] if x in host];n=len(ds);c=d['charts'][s];A=[[d['A'][y,x] for x in ds] for y in s]
  pos=next(cols for cols in combinations(range(n),2) if inverse([[r[j] for j in cols] for r in A]) is not None)
  M=[[F(i==j) for j in range(n)] for i in range(n)]
  for i,p in enumerate(pos):M[p]=A[i]
  Mi=inverse(M);require(Mi is not None,'actual hosted encoder invertible');B=[list(r) for r in zip(*Mi)];D=[list(r) for r in zip(*M)]
  bs=[host[x][0] for x in ds];temps=list(range(1946,1946+n));g=dict(kind='inverse_transpose',begin=event(),chart=c,first_donors=ds,hosted_X2=bs,receivers=list(s),pivot_positions=list(pos),pivot_first_donors=[ds[p] for p in pos],
      primal_matrix=[[str(v) for v in r] for r in M],dual_encoder=[[str(v) for v in r] for r in B],dual_decoder=[[str(v) for v in r] for r in D])
  for b in bs:move(b,source['initial'][b],c)
  g['encoder_snapshots']=[]
  for t,b in zip(temps,bs):emit(['INIT',t,c]);g['encoder_snapshots'].append(event());emit(['ADD',t,raw[b],'1',c])
  encoder_start=event()
  for i,b in enumerate(bs):
   emit(['ADD',raw[b],temps[i],'-1',c])
   for j,v in enumerate(B[i]):
    if v:emit(['ADD',raw[b],temps[j],str(v),c])
  for t in temps:emit(['CLEAR',t,c])
  g['encoded']=event();checkpoints.append(dict(event=event(),roles=bs,matrix=B,kind='actual dual encoded rows'))
  g['injections']=[]
  for i,b in enumerate(bs):
   if i in pos:
    y=s[pos.index(i)];source_d=host[y-112][1];move(b,c,source['final'][y]);g['injections'].append(dict(carrier_X2=b,event=event(),receiver=y,source_Y2=source_d));injections.append(event());emit(['ADD',raw[b],raw[source_d],'-1',source['final'][y]]);move(b,source['final'][y],127)
   else:move(b,c,127)
  g['at_hub']=event();g['decoder_snapshots']=[]
  for t,b in zip(temps,bs):emit(['INIT',t,127]);g['decoder_snapshots'].append(event());emit(['ADD',t,raw[b],'1',127])
  decoder_start=event()
  for i,b in enumerate(bs):
   emit(['ADD',raw[b],temps[i],'-1',127])
   for j,v in enumerate(D[i]):
    if v:emit(['ADD',raw[b],temps[j],str(v),127])
  for t in temps:emit(['CLEAR',t,127])
  g['end']=event()
  for j,b in enumerate(bs):rows[b]={host[y-112][1]:-A[i][j] for i,y in enumerate(s) if A[i][j]}
  checkpoints.append(dict(event=event(),roles=bs,delta={b:rows[b] for b in bs},kind='actual dual decoded rows'))
  require(groups[gi]==g,'every group matrix, pivot, snapshot and live boundary independently reconstructed')
  actual_groups.append(dict(chart=c,encoder_start=encoder_start,decoder_start=decoder_start,injection_events=[x['event'] for x in g['injections']]))
 require(event()==1439 and len(phase)==1029,'entire actual1029-operation dual phase')
 removed=set(routes.values());expected=old[:410]+phase+[op for e,op in enumerate(old) if e>=410 and e not in removed]
 parent_events=list(range(410))+lineage+[e for e in range(410,len(old)) if e not in removed]
 boundary=lambda e:e if e<410 else e+len(phase)-sum(i<e for i in removed)
 require(word['program']==expected and word['parent_event_of_output']==parent_events,'all76039 literal instructions and lineage independently emitted')
 require(word['marks']=={k:boundary(e) for k,e in forward['marks'].items()},'all current chronological boundary markers')
 require(word['native_event_to_physical']==[boundary(e) for e in forward['native_event_to_physical']],'all71261 current native event positions')
 require(word['paired_collection']==dict(begin=410,end=1439,groups=groups,old_routes_replaced={str(j):routes[j] for j in sorted(routes)},owned_moves=0,selected_first_receivers=SELECTED,temporaries=list(range(1946,1970))),'complete current dual metadata')
 require(word['paired_reverse_corrections']=={str(b):[[j,str(v)] for j,v in sorted(row.items())] for b,row in rows.items()},'all exact source transpose coefficients')
 return rows,host,checkpoints,injections,boundary,actual_groups

def semantics(source,parent,forward,word,d,forward_lineage,forward_checks,rows,host,checkpoints,injections,boundary):
 raw={int(k):v for k,v in word['private_role_map'].items()};q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 expected=lambda coeff:combine(list(coeff.values()),[q[x] for x in coeff])
 events={c['event']:c for c in checkpoints};forward_events={boundary(c['event']):c for c in forward_checks};checks=reads=e8reads=0
 selected_d={raw[host[x][1]]:host[x][1] for x in SELECTED};xroles={raw[x]:x for x in d['xs']}
 def observe(e,state,loc,op):
  nonlocal checks,reads,e8reads
  if e in events:
   c=events[e]
   for i,b in enumerate(c['roles']):
    want=combine(c['matrix'][i],[q[t] for t in c['roles']]) if 'matrix' in c else rowadd(q[b],expected(c['delta'][b]))
    require(state[raw[b]]==want,c['kind']);checks+=1
  if e in forward_events:
   c=forward_events[e];require(state[c['role']]==expected(c['coeff']),c['kind']);checks+=1
  if e in injections:
   require(op[2] in selected_d and state[op[2]]==q[selected_d[op[2]]],'actual original Y2 at the selected facet injection');reads+=1
  if e==word['marks']['all_active_donors_restored']:
   for x in d['xs']:require(state[raw[x]]==q[x] and loc[raw[x]]==127,'every104 first raw donor restored');checks+=1
  if op and e>=1439:
   previous=word['parent_event_of_output'][e];original=forward_lineage[previous] if previous is not None else None
   if original is not None and 514<=original<parent['marks']['initial_decoders'] and op[0]=='ADD' and op[2] in xroles:
    require(state[op[2]]==q[xroles[op[2]]] and loc[op[2]]==127,'every actual original E8 read');e8reads+=1
 before,ploc=prefix_execute(parent,parent['marks']['common_starts'])
 after,wloc=prefix_execute(word,word['marks']['common_starts'],observe)
 require(reads==6 and e8reads==520,'all actual six reverse and520 retained E8 observations')
 deltas={raw[y]:expected({x:d['A'][y,x] for x in d['xs'] if d['A'][y,x]}) for y in d['ys']}
 deltas.update({raw[b]:expected(row) for b,row in rows.items()})
 require(set(after)==set(before) and ploc==wloc,'same complete live pre-common interface')
 for j in before:require(after[j]==rowadd(before[j],deltas.get(j,{})),'all1880 input columns and every full live row')
 suffix=word['program'][word['marks']['common_starts']:];require(suffix==parent['program'][parent['marks']['common_starts']:],'complete unchanged72711-instruction common suffix')
 for j in deltas:
  role=next(r for r,v in raw.items() if v==j);touches=[]
  for op in suffix:
   operands=op[1:3] if op[0] in ('ADD','COPY') else op[1:2]
   if j in operands:touches.append(op)
  require(touches==[['ADD',j,role,'1',source['final'][role]]],'no changed private field feeds common or other raw computation')
 return dict(full_independent_input_coordinates=1880,checked_live_rows=checks,actual_reverse_source_reads=reads,actual_E8_source_reads=e8reads,
             forward_changed_rows=3,reverse_changed_rows=68,changed_rows_total=71,all104_original_donors_restored=True,
             unchanged_suffix_instructions=len(suffix),all1480_common_outputs_preserved=True)

def terminal_rows(source,parent,word,d,rows,host):
 logical={int(r) for r in word['private_role_map']};coupled=set(d['xs'])-set(host);matrix={r:{r:F(1)} for r in logical};remaining=0
 for x in d['xs']:
  y=x+112;c=F(1,2) if x in coupled else F(1);row={y:c}
  for donor in d['xs']:
   v=c*F(gram(d['roots'],x,donor),8)
   if v:row[donor]=v
  for donor,v in parent['corrections'].get(str(y),[]):row=rowadd(row,{donor:F(v)})
  if y in d['ys']:row={y:F(1),x:F(1)}
  matrix[y]=row;remaining+=sum(bool(v) for donor,v in row.items() if donor not in (x,y))
 for b,row in rows.items():matrix[b]=rowadd(matrix[b],row)
 inv={r:{r:F(1)} for r in logical}
 for x in d['xs']:
  y=x+112;c=matrix[y][y];inv[y]={y:1/c}
  for donor,v in matrix[y].items():
   if donor!=y:inv[y][donor]=-v/c
 for b,row in rows.items():inv[b]=rowadd({b:F(1)},row,F(-1))
 for r,row in inv.items():require(combine(list(row.values()),[matrix[k] for k in row])=={r:F(1)},'explicit complete400-row terminal left inverse')
 require(remaining==4841,'all4841 remaining forward coefficient duties retained')
 rank_receipt,B,H,roots=examine(source,SELECTED)
 actual_R=[[rows.get(host[x][0],{}).get(host[y][1],F(0)) for y in H] for x in H]
 require(all(F(i==j)+actual_R[i][j]==B[i][j] for i in range(96) for j in range(96)),'actual source word produces exactly the selected-column residual')
 relation={0:F(1),1:F(-1),98:F(-1)}
 require(all(sum(relation.get(x,F(0))*B[i][j] for i,x in enumerate(H))==0 for j in range(96)),'left root-relation annihilates complete reverse residual')
 actual_combo=combine(list(relation.values()),[matrix[host[x][0]] for x in relation]);desired_combo={}
 for x,c in relation.items():desired_combo=rowadd(desired_combo,{host[x][0]:c,host[x][1]:-c})
 require(actual_combo==desired_combo,'one actual completed reverse target linear relation')
 require(all(B[i][i]==1 for i in range(96)),'every individual reverse obligation still has own nonzero residual')
 require(len({source['final'][host[x][1]] for x in H})==96 and all(source['final'][host[x][0]]==127 and len(source['frames'][source['final'][host[x][1]]])==8 for x in H),'96 distinct terminal source facets and common target hub')
 serial=lambda m:{str(r):[[j,str(v)] for j,v in sorted(row.items())] for r,row in sorted(m.items())}
 return dict(private_inverse_rows=400,private_matrix_sha256=sha(json.dumps(serial(matrix),sort_keys=True).encode()),private_inverse_sha256=sha(json.dumps(serial(inv),sort_keys=True).encode()),
             forward_remaining_residuals=4841,reverse_residual_rank=95,reverse_residual_nullity=1,
             reverse_null_relation=[[host[x][1],str(c)] for x,c in relation.items()],
             completed_reverse_target_relation=[[host[x][0],str(c)] for x,c in relation.items()],
             individual_reverse_pairs_completed=0,distinct_Y2_terminal_facets=96,
             terminal_new_incoming_field_lower_bound=95,terminal_new_paid_MOVE_lower_bound=96,
             terminal_bound_scope='Fixed restored terminal interface, no subsequent funded source calls. Rank95 lower-bounds incoming field information; all96 nonzero separately located source directions each need a first paid departure, even if later combined.')

def terminal_suffix(source,word,rows,host):
 raw={int(k):v for k,v in word['private_role_map'].items()};order=sorted(host);record=word['public']+word['owned_fields'];suffix=[]
 for x in order:
  d=host[x][1];facet=source['final'][d];suffix.extend([['INIT',record,facet],['ADD',record,raw[d],'1',facet],['MOVE',record,facet,127,True]])
  for y in order:
   b=host[y][0];c=F(x==y)+rows.get(b,{}).get(d,F(0))
   if c:suffix.append(['ADD',raw[b],record,str(-c),127])
  suffix.append(['CLEAR',record,127])
 require(len(suffix)==616,'sharp96-departure completion suffix has616 instructions')
 newword=dict(word,program=word['program']+suffix,owned_fields=word['owned_fields']+1);bill=typed(source,newword)
 for x in order:
  for y in order:
   original=rows.get(host[x][0],{}).get(host[y][1],F(0));require(original-(F(x==y)+original)==-F(x==y),'literal appended decoder completes every hosted reverse target')
 pairs={(op[2],op[3]) for w in (word,source) for op in w['program'] if op[0]=='MOVE'}
 require({(op[2],op[3]) for op in suffix if op[0]=='MOVE'}<=pairs,'suffix uses already authenticated chart-map pairs')
 return suffix,dict(instructions=len(newword['program']),counts=dict(bill['counts']),added_paid_profile={1:96},additional_owned_lifetimes=96,owned_peak=bill['peak'])

def negatives(source,parent,forward,word,d,fline,fchecks,rows,host,checks,injections,boundary,groups):
 rejected={}
 def trial(name,ops,algebra=False):
  candidate=dict(word,program=ops)
  try:
   typed(source,candidate)
   if algebra:semantics(source,parent,forward,candidate,d,fline,fchecks,rows,host,checks,injections,boundary)
  except ValueError as e:rejected[name]=str(e)
  require(name in rejected,'negative control escaped '+name)
 def copyops():return [op.copy() for op in word['program']]
 for name,event in [('wrong_dual_encoder',groups[0]['encoder_start']+1),('wrong_reverse_injection',injections[0]),('wrong_dual_decoder',groups[0]['decoder_start']+1)]:
  ops=copyops();require(ops[event][0]=='ADD','mutated actual arithmetic event');ops[event][3]=str(-F(ops[event][3]));trial(name,ops,True)
 first_b=int(word['private_role_map'][str(word['paired_collection']['groups'][0]['hosted_X2'][0])]);end=word['paired_collection']['groups'][0]['encoded']
 e=next(e for e in range(groups[0]['encoder_start'],end) if word['program'][e][0]=='ADD' and word['program'][e][1]!=first_b and word['program'][e][2]==1946)
 ops=copyops();ops[e][2]=first_b;trial('stale_partially_transformed_dual_donor',ops,True)
 for name,event in [('missing_original_Y2_arrival',410),('missing_dual_facet_arrival',injections[0]-1)]:
  ops=copyops();ops.pop(event);trial(name,ops)
 c=next(c for c in fchecks if c['kind']=='actual forward pivot payload');scale=next(e for e in range(boundary(c['event'])-8,boundary(c['event'])) if word['program'][e][0]=='SCALE');ops=copyops();ops[scale][2]=str(-F(ops[scale][2]));trial('wrong_live_forward_pivot',ops,True)
 bad=dict(word['marks']);bad['all_active_donors_restored']=823
 try:emit_dual(source,forward,dict(word,marks=bad),d)
 except ValueError as e:rejected['stale_forward_restoration_marker']=str(e)
 require('stale_forward_restoration_marker' in rejected,'wrong chronological marker rejected')
 return rejected

def main(a):
 parentdir=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused'
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN);parent=load(parentdir/'WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD)
 prior=load(parentdir/'review/REVIEW-RESULT.json',pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e')
 require(prior['all1480_common_outputs_preserved'] and prior['private_inverse_rows_preserved']==400 and prior['all_other4985_residual_coefficients_preserved'],'authenticated parent source map facts')
 forward=load(a.package/'FORWARD.json.gz',True,payload=FORWARD_PIN);word=load(a.package/'WORD.json.gz',True,payload=WORD_PIN);report=load(a.package/'RESULT.json')
 d=setup(source);expected,fline,fchecks=emit_forward(source,parent,d)
 require(forward['program']==expected and forward['parent_event_of_output']==fline and len(expected)==75081,'complete independently emitted75081-operation forward word')
 require(forward['additional_charts']==d['extra']==word['additional_charts'],'all three exact source facet intersections')
 fpositions={e:i for i,e in enumerate(fline) if e is not None}
 require(forward['native_event_to_physical']==[fpositions[e] for e in parent['native_event_to_physical']],'all original forward source events')
 for k,e in parent['marks'].items():require(forward['marks'][k]==fpositions[e],'actual forward inherited mark '+k)
 require(forward['marks']['all_active_donors_restored']==823,'forward restoration mark')
 require(word['initial']==forward['initial']==parent['initial'] and word['private_role_map']==forward['private_role_map']==parent['private_role_map'],'all1880 original labelled inputs')
 require(word['parent_word_sha256']==sha((a.package/'FORWARD.json.gz').read_bytes()) and forward['parent_word_sha256']==PARENT_PIN,'exact new provenance dependency chain')
 rows,host,checks,injections,boundary,groups=emit_dual(source,forward,word,d)
 require(word['public']==1880 and word['owned_fields']==90 and word['marks']['all_active_donors_restored']==1852 and word['marks']['common_starts']==3328,'complete namespace and actual boundaries')
 require(len(rows)==68 and sum(len(row) for row in rows.values())==136,'all136 transpose coefficients on68 genuine hosted carriers')
 bill=typed(source,word);fbill=typed(source,forward);pbill=typed(source,parent)
 require(bill['final']==fbill['final']==pbill['final'] and bill['peak']==43,'all authentic final charts and real ownership peak')
 require(bill['counts']=={'ADD':65061,'SCALE':3676,'MOVE':6877,'INIT':212,'CLEAR':212,'COPY':1},'complete operation bill')
 require(bill['rawranks']=={1:26,2:133,5:1,6:141,7:7,8:251} and sum(bill['rawranks'].values())==559 and sum(r*n for r,n in bill['rawranks'].items())==3200,'complete559 raw calls and rank3200')
 sem=semantics(source,parent,forward,word,d,fline,fchecks,rows,host,checks,injections,boundary)
 terminal=terminal_rows(source,parent,word,d,rows,host);suffix,suffixbill=terminal_suffix(source,word,rows,host)
 negative=negatives(source,parent,forward,word,d,fline,fchecks,rows,host,checks,injections,boundary,groups)
 inv=load(parentdir/'INPUT-INVOICE.json',pin=INVOICE_PIN);T={int(k):v for k,v in inv['T4'].items()};P={int(k):v for k,v in inv['P4'].items()};logical={int(k) for k in word['private_role_map']}
 oldraw=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE' and op[1] in logical)
 require(oldraw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'all1710 old raw reservations recomputed')
 native=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE');extra=bill['ranks'].copy();extra.subtract(native);extra.subtract(bill['rawranks'])
 require({r:n for r,n in extra.items() if n}=={9:8},'all eight original rank9 packet calls retained once')
 paid={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|{9}}
 require(all(n>=0 for n in paid.values()) and sum(paid.values())==131850 and sum(T.values())==27344,'complete nonnegative paid and target profiles')
 require(paid=={int(k):v for k,v in report['conditional_caller']['P_partial'].items()} and sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys())==3760,'exact complete caller and rank surplus')
 margin=tuple(v/18 for v in moment({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()}));c=report['conditional_caller']
 require(F(c['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(c['remaining_moment_per_native_upper']),'independent directed rational moment bracket')
 require(F(43730,1000)<margin[0]<margin[1]<F(43731,1000) and margin[1]-96<0,'positive43.730.. partial allowance and negative sharp terminal repair budget')
 maps=load(a.package/'CHART-MAPS.json');pairs=lambda w:{(op[2],op[3]) for op in w['program'] if op[0]=='MOVE'};introduced=pairs(word)-pairs(parent);recipes=maps['introduced_maps'];frames=source['frames']+[x['frame'] for x in d['extra']]
 require({(r['source'],r['target']) for r in recipes}==introduced and len(introduced)==84,'all84 new chart-map pairs covered')
 for r in recipes:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']]),'all actual new map ranks')
 require(maps['word_sha256']==sha((a.package/'WORD.json.gz').read_bytes()) and maps['parent_word_sha256']==PARENT_PIN and maps['source_sha256']==SOURCE_PIN and maps['wrong_global_phase_rejected'],'exact word and chart engine source pins')
 for name,pin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'retained chart-engine code pin')
 result=dict(status='PASS_INDEPENDENT_DEPENDENT_TRIPLE_WITH_RESIDUAL_RANK95',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,parent_payload_sha256=PARENT_PAYLOAD,
             forward_payload_sha256=FORWARD_PIN,word_payload_sha256=WORD_PIN,word_sha256=sha((a.package/'WORD.json.gz').read_bytes()),reviewer_sha256=sha(Path(__file__).read_bytes()),
             instructions=76039,counts=dict(bill['counts']),raw_calls=559,raw_profile=dict(bill['rawranks']),raw_rank_mass=3200,owned_peak=43,owned_lifetimes=212,
             new_charts=3,introduced_map_coverage=84,forward_complete_pairs=3,reverse_complete_individual_pairs=0,reverse_complete_linear_relations=1,
             forward_remaining_residual_coefficients=4841,hosted_reverse_changed_rows=68,transpose_coefficients=136,semantics=sem,terminal=terminal,
             all1880_inputs_retained=True,all1480_common_outputs_preserved=True,paid_positions=131850,target_positions=27344,rank_surplus=3760,
             conditional_paid_profile=paid,conditional_target_profile=T,remaining_moment_exact=[str(v) for v in margin],remaining_moment_approx=float(margin[0]),
             sharp_terminal_completion=suffixbill,sharp_terminal_completion_margin_exact=[str(v-96) for v in margin],negative_controls=negative,
             chart_engine_scope='Retained author exact-engine run credited with authenticated pins; introduced coverage, source geometry, and ranks independently checked here.',
             scope='Finite exact source causal construction with an independently checked nontrivial hosted reverse-residual kernel and positive remaining source moment; all original input directions retained. Individual reverse pairs, coupled reverse duties, global source family, suppliers, and foundations remain open. No new kappa.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');a.output.with_name('DEPENDENT-TRIPLE-TERMINAL-SUFFIX.json').write_text(json.dumps(dict(word_payload_sha256=WORD_PIN,instructions=suffix),indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('conditional_paid_profile','conditional_target_profile')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
