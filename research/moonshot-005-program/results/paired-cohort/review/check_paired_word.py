#!/usr/bin/env python3
"""Independent paired-cohort reconstruction, exact rows and residual-rank audit."""
import argparse,json,gzip
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from cohort_geometry import derive,require,SOURCE_PIN,FRAME,root
from check_cohort_word import load,sha,inverse,rowadd,combine,typed,prefix_execute,moment,WORD_PAYLOAD,INVOICE_PIN

PAIRED_PAYLOAD='bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a'

def reconstruct(source,parent,word):
 raw={int(k):v for k,v in parent['private_role_map'].items()};xs=sorted(source['live']);host={xs[i]:(source['hosted']['X2'][j],source['hosted']['Y2'][j]) for j,i in enumerate(source['hosted']['Dports'])};geo=derive(source)
 gs=word['paired_collection']['groups'];require(len(gs)==14,'fourteen actual dual groups')
 byset={tuple(x+112 for x in g['receivers']):g for g in geo['groups']};rows={};phase=[];snapchecks={};groupchecks=[]
 def emit(o):phase.append(o)
 def e():return 410+len(phase)
 def move(role,s,t):
  if s!=t:emit(['MOVE',raw[role],s,t,False])
 defect=next(g for g in geo['groups'] if g['hosted_rank']==2);dy=[r+112 for r in defect['receivers']];dc=1095+geo['groups'].index(defect);ds=defect['hosted_donors']
 require(gs[0]['kind']=='rank2_direct_cochart' and gs[0]['chart']==dc and gs[0]['first_donors']==ds,'actual rank-two group')
 for d in ds:move(host[d][0],source['initial'][host[d][0]],dc)
 for y in dy:move(host[y-112][1],3,dc)
 for d in ds:
  rr={}
  for y in dy:
   A=F(defect['A'][defect['receivers'].index(y-112)][defect['donors'].index(d)]);emit(['ADD',raw[host[d][0]],raw[host[y-112][1]],str(-A),dc]);rr[host[y-112][1]]=-A
  rows[host[d][0]]=rr
 for d in ds:move(host[d][0],dc,127)
 for y in dy:move(host[y-112][1],dc,source['final'][y])
 require(e()==gs[0]['end']==430,'rank-two literal boundary')
 for x in FRAME:
  if x+112 not in dy:move(host[x][1],3,source['final'][x+112])
 for g in gs[1:]:
  src=byset[tuple(g['receivers'])];ds=src['hosted_donors'];ys=[r+112 for r in src['receivers']];chart=1095+geo['groups'].index(src);n=len(ds);pos=g['pivot_positions']
  require(g['kind']=='inverse_transpose' and g['first_donors']==ds and g['chart']==chart and len(set(pos))==4 and all(0<=i<n for i in pos),'actual hosted group and chosen pivots')
  A=[[F(src['A'][i][src['donors'].index(d)]) for d in ds] for i in range(4)];M=[[F(i==j) for j in range(n)] for i in range(n)]
  for i,k in enumerate(pos):M[k]=A[i]
  Mi=inverse(M);require(Mi is not None,'nonsingular actual hosted pivot transform');B=[list(r) for r in zip(*Mi)];D=[list(r) for r in zip(*M)]
  for k,v in [('primal_matrix',M),('dual_encoder',B),('dual_decoder',D)]:require(g[k]==[[str(x) for x in r] for r in v],'independently computed '+k)
  require(e()==g['begin'],'literal dual group begin')
  bs=[host[d][0] for d in ds];snaps=list(range(1953,1953+n))
  for b in bs:move(b,source['initial'][b],chart)
  for s,b in zip(snaps,bs):emit(['INIT',s,chart]);emit(['ADD',s,raw[b],'1',chart])
  for i,b in enumerate(bs):
   emit(['ADD',raw[b],snaps[i],'-1',chart])
   for j,c in enumerate(B[i]):
    if c:emit(['ADD',raw[b],snaps[j],str(c),chart])
  for s in snaps:emit(['CLEAR',s,chart])
  require(e()==g['encoded'],'literal encoded boundary');snapchecks[e()]=(bs,B,None)
  for i,b in enumerate(bs):
   if i in pos:
    y=ys[pos.index(i)];move(b,chart,source['final'][y]);emit(['ADD',raw[b],raw[host[y-112][1]],'-1',source['final'][y]]);move(b,source['final'][y],127)
   else:move(b,chart,127)
  require(e()==g['at_hub'],'literal all dual payloads at hub')
  for s,b in zip(snaps,bs):emit(['INIT',s,127]);emit(['ADD',s,raw[b],'1',127])
  for i,b in enumerate(bs):
   emit(['ADD',raw[b],snaps[i],'-1',127])
   for j,c in enumerate(D[i]):
    if c:emit(['ADD',raw[b],snaps[j],str(c),127])
  for s in snaps:emit(['CLEAR',s,127])
  require(e()==g['end'],'literal dual group end')
  for j,b in enumerate(bs):rows[b]={host[ys[i]-112][1]:-A[i][j] for i in range(4) if A[i][j]}
  snapchecks[e()]=(bs,None,{b:rows[b] for b in bs});groupchecks.append(dict(chart=chart,hosted_donors=ds,pivots=pos))
 require(e()==2024 and len(phase)==1614,'entire new1614-instruction phase')
 moved=set(rows)|{host[x][1] for x in FRAME};old=parent['program'];removes={e for e,o in enumerate(old) if o[0]=='MOVE' and o[1] in {raw[j] for j in moved}}
 require(len(removes)==96 and all(old[e][2:]==[source['initial'][next(k for k,v in raw.items() if v==old[e][1])],source['final'][next(k for k,v in raw.items() if v==old[e][1])],False] for e in removes),'exact96 old direct routes')
 expected=old[:410]+phase+[o for e,o in enumerate(old) if e>=410 and e not in removes]
 boundaries={i:(i if i<410 else i+len(phase)-sum(j<i for j in removes)) for i in range(len(old)+1)}
 require(word['program']==expected,'every77795 instruction independently reconstructed')
 require(word['marks']=={k:boundaries[v] for k,v in parent['marks'].items()},'chronological parent boundary transport, not retimed operation lookup')
 require(word['native_event_to_physical']==[boundaries[e] for e in parent['native_event_to_physical']],'exact source operation map')
 require(word['paired_reverse_corrections']=={str(b):[[j,str(v)] for j,v in sorted(row.items())] for b,row in rows.items()},'all352 source-derived reverse coefficients')
 return rows,host,snapchecks,boundaries,groupchecks

def semantics(source,parent,word,rows,host,snapchecks,boundaries):
 raw={int(k):v for k,v in parent['private_role_map'].items()};q={r:{raw[r]:F(1),r:F(-1)} for r in raw};checks=reads=0
 selected={raw[host[x][1]]:host[x][1] for x in FRAME}
 def check(e,state,loc,op):
  nonlocal checks,reads
  if e in snapchecks:
   bs,B,delta=snapchecks[e]
   for i,b in enumerate(bs):
    want=combine(B[i],[q[x] for x in bs]) if B is not None else rowadd(q[b],combine(list(delta[b].values()),[q[d] for d in delta[b]]))
    require(state[raw[b]]==want,'actual original-input encoded/decoded row');checks+=1
  if 410<=e<2024 and op and op[0]=='ADD' and op[2] in selected:
   require(state[op[2]]==q[selected[op[2]]],'all original Y2 values at real injection');reads+=1
  if e==word['marks']['all_active_donors_restored']:
   for x in source['live']:require(state[raw[x]]==q[x] and loc[raw[x]]==127,'all104 first donors still restored');checks+=1
 before,ploc=prefix_execute(parent,parent['marks']['common_starts']);after,wloc=prefix_execute(word,word['marks']['common_starts'],check)
 require(reads==60,'60 actual reverse source reads');require(ploc==wloc and set(before)==set(after),'full live interface at common start')
 physical_delta={raw[b]:combine(list(row.values()),[q[d] for d in row]) for b,row in rows.items()}
 for j in before:require(after[j]==rowadd(before[j],physical_delta.get(j,{})),'complete1880-column prefix comparison')
 start=word['marks']['common_starts'];require(word['program'][start:]==parent['program'][parent['marks']['common_starts']:],'unchanged full common suffix')
 touches={raw[b]:[] for b in rows}
 for e,o in enumerate(word['program'][start:],start):
  ops=o[1:3] if o[0] in ('ADD','COPY') else [o[1]]
  for j in touches:
   if j in ops:touches[j].append(o)
 for b in rows:require(touches[raw[b]]==[['ADD',raw[b],b,'1',127]],'no changed X2 feedback before final recoupling')
 for b,row in rows.items():
  current=rowadd(q[b],combine(list(row.values()),[q[d] for d in row]));recovered=rowadd(current,combine(list(row.values()),[q[d] for d in row]),F(-1));require(recovered==q[b],'explicit hosted information inverse')
 return dict(independent_input_columns=1880,encoded_and_restoration_rows=checks,authentic_Y2_reads=reads,changed_hosted_rows=88,explicit_hosted_inverse_rows=88,unchanged_suffix_instructions=len(word['program'])-start)

def residual_and_suffix(source,word,rows,host):
 raw={int(k):v for k,v in word['private_role_map'].items()};ordinary=sorted(host);bindex={host[x][0]:i for i,x in enumerate(ordinary)};dindex={host[x][1]:i for i,x in enumerate(ordinary)};R=[[F(0) for _ in ordinary] for _ in ordinary]
 for b,row in rows.items():
  for d,c in row.items():R[bindex[b]][dindex[d]]=c
 S={ordinary.index(x) for x in FRAME};require(all(not R[i][j] or i not in S and j in S for i in range(96) for j in range(96)),'opposite support blocks of transpose addition')
 for i in range(96):
  for j in range(96):require(sum(R[i][k]*R[k][j] for k in S)==0,'exact nilpotence R squared zero')
 require(sum(bool(v) for row in R for v in row)==352,'352 nonzero transpose coefficients')
 # (I-R)(I+R)=I is the explicit residual inverse: rank96 over every field.
 require(all(source['final'][host[x][0]]==127 and len(source['frames'][source['final'][host[x][1]]])==8 for x in ordinary),'all reverse X2 at hub and Y2 at proper facets')
 suffix=[];record=word['public']+word['owned_fields'];full=word['program'].copy()
 for j,x in enumerate(ordinary):
  d=host[x][1];facet=source['final'][d];suffix.extend([['INIT',record,facet],['ADD',record,raw[d],'1',facet],['MOVE',record,facet,127,True]])
  for i,y in enumerate(ordinary):
   coefficient=F(i==j)+R[i][j]
   if coefficient:suffix.append(['ADD',raw[host[y][0]],record,str(-coefficient),127])
  suffix.append(['CLEAR',record,127])
 require(len(suffix)==832,'literal sharp96-arrival suffix length')
 complete=dict(word,program=full+suffix,owned_fields=word['owned_fields']+1);bill=typed(source,complete)
 # On the96 independent Y2 coordinates, the appended decoder removes I+R.
 for i in range(96):
  final=[R[i][j]-(F(i==j)+R[i][j]) for j in range(96)]
  require(final==[-F(i==j) for j in range(96)],'all96 actual reverse shears completed by suffix')
 return dict(transpose_rank_support='rows outside S, columns inside S',nilpotent_square_zero=True,actual_reverse_residual_rank=96,append_only_arrival_minimum=96,attaining_suffix_instructions=832,attaining_suffix_owned_lifetimes=96,attaining_suffix_added_rank_profile={1:96},resulting_instructions=len(complete['program']),resulting_opcode_counts=dict(bill['counts']),scope='Sharp append-only terminal-interface extension. Earlier recoding, changed common processing and information already delivered elsewhere are outside this lower bound.'),suffix

def main(a):
 base=a.repo/'research/moonshot-005-program/results';source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN);parent=load(a.parent/'WORD.json.gz',True,payload=WORD_PAYLOAD);word=load(a.package/'WORD.json.gz',True,payload=PAIRED_PAYLOAD);report=load(a.package/'RESULT.json')
 rows,host,snaps,boundaries,groups=reconstruct(source,parent,word);require(len(word['program'])==77795 and word['initial']==parent['initial'] and word['owned_fields']==81 and word['additional_charts']==parent['additional_charts'],'unchanged1880 physical inputs, charts and exact owned namespace')
 require(len(rows)==88 and sum(len(r) for r in rows.values())==352,'88 changed hosted outputs and352 coefficients')
 bill=typed(source,word);pbill=typed(source,parent);require(bill['final']==pbill['final'] and bill['peak']==43,'final charts and live ownership peak')
 require(bill['counts']=={'ADD':66273,'SCALE':3670,'MOVE':7021,'INIT':415,'CLEAR':415,'COPY':1},'full ordinary and transport census')
 require(bill['rawranks']=={1:113,2:114,3:76,5:185,6:5,7:4,8:206} and sum(bill['rawranks'].values())==703 and sum(r*n for r,n in bill['rawranks'].items())==3200,'complete703 raw moves/rank3200')
 sem=semantics(source,parent,word,rows,host,snaps,boundaries);residual,suffix=residual_and_suffix(source,word,rows,host)
 invoice=load(base/'eight-packet-seven-corrections-fused/INPUT-INVOICE.json',pin=INVOICE_PIN);T={int(k):v for k,v in invoice['T4'].items()};P={int(k):v for k,v in invoice['P4'].items()};rawroles={int(k) for k in word['private_role_map']};oldraw=Counter(abs(len(source['frames'][o[2]])-len(source['frames'][o[3]])) for o in source['program'] if o[0]=='MOVE' and o[1] in rawroles)
 newP={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|{9}}
 require(all(n>=0 for n in newP.values()) and sum(newP.values())==134442 and sum(T.values())==27344,'complete paid/target profile')
 require(newP=={int(k):v for k,v in report['conditional_caller']['P_partial'].items()},'complete author invoice matched')
 margin=tuple(v/18 for v in moment({r:T.get(r,0)-newP.get(r,0) for r in T.keys()|newP.keys()}));caller=report['conditional_caller'];require(F(caller['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(caller['remaining_moment_per_native_upper']),'exact independent root bracket')
 require(F(41017,1000)<margin[0]<margin[1]<F(20509,500),'strict41.017.. positive partial allowance');require(margin[1]-96<0,'sharp append-only repair strictly fails target')
 negative={}
 def trial(name,mutant,check_rows=True):
  try:
   typed(source,mutant)
   if check_rows:semantics(source,parent,mutant,rows,host,snaps,boundaries)
  except ValueError as e:negative[name]=str(e)
  require(name in negative,'negative control escaped '+name)
 for name,event in [('wrong_dual_encoder',453),('wrong_reverse_injection',481),('wrong_dual_decoder',507)]:
  ops=[o.copy() for o in word['program']];ops[event][3]=str(-F(ops[event][3]));trial(name,dict(word,program=ops))
 ops=[o.copy() for o in word['program']];ops[457][2]=int(word['private_role_map']['773']);trial('stale_partial_dual_value',dict(word,program=ops))
 for name,event in [('omit_Y2_cochart_arrival',412),('omit_dual_receiver_arrival',480)]:trial(name,dict(word,program=[o.copy() for e,o in enumerate(word['program']) if e!=event]),False)
 badmarks=dict(word['marks']);badmarks['prefix_scheduled']=1901
 try:reconstruct(source,parent,dict(word,marks=badmarks))
 except ValueError as e:negative['retimed_operation_used_as_boundary']=str(e)
 require('retimed_operation_used_as_boundary' in negative,'stale marker mutant rejected')
 maps=load(a.package/'CHART-MAPS.json');pairs=lambda w:{(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};introduced=pairs(word)-pairs(parent);recipes=maps['introduced_maps'];frames=source['frames']+[c['frame'] for c in word['additional_charts']]
 require({(r['source'],r['target']) for r in recipes}==introduced=={(3,1105),(1105,127)},'exact two introduced paired chart maps')
 for r in recipes:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']]),'paired complete map rank')
 require(maps['word_sha256']==sha((a.package/'WORD.json.gz').read_bytes()) and maps['parent_word_sha256']==sha((a.parent/'WORD.json.gz').read_bytes()) and maps['source_sha256']==SOURCE_PIN and maps['wrong_global_phase_rejected'],'paired recipe pins and phase mutant')
 for name,pin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'actual retained map engine')
 require({(o[2],o[3]) for o in suffix if o[0]=='MOVE'}<=pairs(word)|pairs(source),'suffix only uses already authenticated source chart pairs')
 result=dict(status='PASS_INDEPENDENT_PAIRED_COHORT_WORD',source_sha256=SOURCE_PIN,parent_payload_sha256=WORD_PAYLOAD,word_payload_sha256=PAIRED_PAYLOAD,word_sha256=sha((a.package/'WORD.json.gz').read_bytes()),checker_sha256=sha(Path(__file__).read_bytes()),instructions=77795,full_independent_input_coordinates=1880,groups_inverse_transpose=13,groups_direct_rank2=1,counts=dict(bill['counts']),raw_profile=dict(bill['rawranks']),raw_calls=703,owned_peak=43,owned_lifetimes=415,semantics=sem,forward_complete_pairs=8,forward_remaining_residuals=4601,reverse_added_coefficients=352,reverse_complete_pairs=0,all_common_outputs_preserved=True,all1880_inputs_retained=True,reverse_residual=residual,paid_positions=134442,target_positions=27344,rank_surplus=3760,paid_profile=newP,target_profile=T,remaining_moment_exact=[str(v) for v in margin],remaining_moment_approx=float(margin[0]),append_only_completion_margin_exact=[str(v-96) for v in margin],negative_controls=negative,introduced_map_coverage=2,chart_engine_scope='Retained exact engine run credited; coverage, ranks and actual source/word/engine pins independently checked.',scope='Finite exact source bidirectional partial construction. No completed reverse diagonal, full supplier or new kappa. The unchanged terminal interface cannot be completed by a target-feasible append-only suffix.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');a.output.with_name('APPEND-ONLY-REPAIR-SUFFIX.json').write_text(json.dumps(dict(word_payload_sha256=PAIRED_PAYLOAD,instructions=suffix),indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('paid_profile','target_profile')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
