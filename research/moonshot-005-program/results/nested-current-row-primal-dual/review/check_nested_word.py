#!/usr/bin/env python3
"""Independent all-input/current-row audit of the nested source word.

The author generator and author validation modules are not imported.
"""
import argparse,json,copy
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from cohort_geometry import SOURCE_PIN,space,root,rank,require
from check_cohort_word import load,sha,inverse,combine,rowadd,typed,prefix_execute,moment,PARENT_PIN,PARENT_PAYLOAD,INVOICE_PIN

WORD_PIN='77d2e907d74c2539b115d8ad60367ee74939cca2eda9e10bcf28fb2b4e7ee42c'
SELECTED=[0,1,2,98,99,103]
FULL=[0,1,98]

def source_data(source):
 X=sorted(source['live']);host={X[i]:(source['hosted']['X2'][j],source['hosted']['Y2'][j]) for j,i in enumerate(source['hosted']['Dports'])}
 V={x:root(source['frames'][source['initial'][x]][0]) for x in X};G={(x,y):sum(a*b for a,b in zip(V[x],V[y])) for x in X for y in X}
 groups=defaultdict(list)
 for x in X:
  support=tuple(y for y in SELECTED if y!=x and G[y,x])
  if support:groups[support].append(x)
 require(len(groups)==7,'seven source-derived primitive cohorts')
 wanted_partial={2:{(0,1,2),(2,99,103)},99:{(0,98,99)},103:{(1,98,103)}}
 forward={}
 for x in SELECTED:
  donors=[y for y in X if y!=x and G[x,y] and (x in FULL or tuple(t for t in SELECTED if t!=y and G[t,y]) in wanted_partial[x])]
  forward[x+112]={y:-F(G[x,y],8) for y in donors}
 reverse=defaultdict(dict)
 for y,row in forward.items():
  for x,c in row.items():
   if x in host:reverse[host[x][0]][host[y-112][1]]=-c
 require([len(forward[x+112]) for x in SELECTED]==[48,48,26,48,13,13] and sum(map(len,forward.values()))==196,'exact source-derived full and partial forward correction supports')
 require(sum(map(len,reverse.values()))==183,'exact hosted transpose183 coefficients')
 return dict(X=X,host=host,V=V,G=G,groups=dict(groups),forward=forward,reverse=dict(reverse))

def geometry(source,word,d):
 charts=word['additional_charts'];records=word['nested_acquisition']['records'];require(len(charts)==len(records)==10,'seven primitive and three nested charts')
 for gi,(support,donors) in enumerate(sorted(d['groups'].items())):
  g=records[gi];C=set.intersection(*(set(space(source['frames'][source['final'][x+112]])) for x in support));c=charts[gi]
  require(g['chart']==c['index']==1095+gi and c['source_facets']==[source['final'][x+112] for x in support] and space(c['frame'])==C and len(c['frame'])==6,'exact source-derived primitive acquisition chart')
  H=[x for x in donors if x in d['host']];U=[x for x in donors if x not in d['host']]
  require(g['support']==[x+112 for x in support] and g['hosted_donors']==H and g['coupled_controls']==U,'actual hosted and coupled source partition')
  require(all(space(source['frames'][source['initial'][x]])<C for x in donors),'all actual source lines fit the primitive chart')
  M=[list(map(F,row)) for row in g['primal_encoder']['matrix']];I=[H.index(x) for x in g['pivot_first_donors']];targets=g['target_rows']
  require(len(I)==len(targets) and len(set(I))==len(I),'independent primitive pivot assignment')
  for i,x in enumerate(H):
   wanted=[-F(d['G'][targets[I.index(i)]-112,y],8) for y in H] if i in I else [F(i==j) for j in range(len(H))]
   require(M[i]==wanted,'primal primitive row exactly source correction or retained identity')
  require(g['primal_encoder']['roles']==H and g['dual_encoder']['roles']==[d['host'][x][0] for x in H],'independent genuine hosted banks')
 for gi,pair in enumerate(((112,113),(112,210),(113,210)),7):
  g=records[gi];c=charts[gi];C=set.intersection(*(set(space(source['frames'][source['final'][y]])) for y in pair))
  require(g['pair']==list(pair) and g['chart']==c['index']==1095+gi and c['source_facets']==[source['final'][y] for y in pair] and space(c['frame'])==C and len(c['frame'])==7,'exact nested pair join chart')
  require(len(g['four_current_carriers'])==len(g['four_current_dual_carriers'])==4,'four actual current carriers in each nested bank')
  require(g['four_current_dual_carriers']==[d['host'][x][0] for x in g['four_current_carriers']],'actual nested dual bank roles')
 for g in records:
  M=[list(map(F,r)) for r in g['primal_encoder']['matrix']];Mi=inverse(M);require(Mi is not None,'actual local primal matrix nonsingular')
  require(g['dual_encoder']['matrix']==[[str(v) for v in row] for row in zip(*Mi)],'every dual matrix is the exact inverse transpose')
 return records

def semantic(source,parent,word,d,records):
 raw={int(k):v for k,v in word['private_role_map'].items()};q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 make=lambda row:combine(list(row.values()),[q[r] for r in row])
 starts=defaultdict(list);ends=defaultdict(list);macros=[];snapshots={};nested={};counts=Counter();cache_rows={};cache_uses=Counter()
 for g in records:
  for name in ('primal_encoder','dual_encoder'):
   m=g[name];k=len(macros);macros.append(m);starts[m['begin']].append(k);ends[m['end']].append(k)
  if 'before_primal' in g:nested[g['before_primal']]=g
 cache={c['event']:c for c in word['nested_acquisition']['cache_declarations']};owner_info={c['owner']:c for c in cache.values()}
 ds={raw[b]:b for x,(a,b) in d['host'].items()};coupled={raw[x]:x for x in d['X'] if x not in d['host']};xs={raw[x]:x for x in d['X']}
 def check(e,state,loc,op):
  for k in ends[e]:
   m=macros[k];M=[list(map(F,r)) for r in m['matrix']]
   for i,r in enumerate(m['roles']):require(state[raw[r]]==combine(M[i],snapshots[k]),'actual current-row matrix macro '+m['kind']);counts['macro_output_rows']+=1
  for k in starts[e]:
   m=macros[k];require(all(loc[raw[r]]==m['chart'] for r in m['roles']),'actual macro input cochart');snapshots[k]=[state[raw[r]].copy() for r in m['roles']]
  if e in nested:
   g=nested[e]
   for roles,rows in ((g['four_current_carriers'],g['incoming_current_rows']),(g['four_current_dual_carriers'],g['incoming_dual_rows'])):
    for r,row in zip(roles,rows):require(state[raw[r]]==make({j:F(c) for j,c in row}),'actual nested input row, with pending dual corrections retained');counts['nested_input_rows']+=1
  if e in cache:
   c=cache[e];require(op==['ADD',c['owner'],raw[c['carrier']],c['coefficient'],c['chart']] and state[c['owner']]=={},'real declared cache acquisition')
   row=state[raw[c['carrier']]];coeff={x:row.get(raw[x],F(0)) for x in d['X']};coeff={x:v for x,v in coeff.items() if v}
   require(row==make(coeff) and all(v==-F(d['G'][c['receiver']-112,x],8) for x,v in coeff.items()),'cache is an exact source correction subrow, not stale original data')
   cache_rows[c['owner']]=row;counts['cache_acquisitions']+=1
  if op and op[0]=='ADD' and op[2] in owner_info:
   c=owner_info[op[2]];require(op==['ADD',raw[c['receiver']],c['owner'],'1',c['chart']] and state[c['owner']]==cache_rows[c['owner']],'authentic cache consumption at the receiver chart');cache_uses[c['owner']]+=1
  if op and 410<=e<3077 and op[0]=='ADD' and op[2] in ds:
   require(state[op[2]]==q[ds[op[2]]],'actual original Y2 at every reverse injection');counts['original_Y2_reads']+=1
  if op and 410<=e<3077 and op[0]=='ADD' and op[2] in coupled:
   require(state[op[2]]==q[coupled[op[2]]],'actual original coupled control at every read');counts['coupled_original_reads']+=1
  if e==3077:
   for x in d['X']:require(state[raw[x]]==q[x] and loc[raw[x]]==127,'all104 original first-X donors restored');counts['restored_first_X_rows']+=1
  if op and e>=3077:
   old=word['parent_event_of_output'][e]
   if old is not None and 514<=old<parent['marks']['initial_decoders'] and op[0]=='ADD' and op[2] in xs:
    require(state[op[2]]==q[xs[op[2]]] and loc[op[2]]==127,'actual retained E8 read is original');counts['authentic_E8_reads']+=1
 before,loc0=prefix_execute(parent,parent['marks']['common_starts']);after,loc1=prefix_execute(word,word['marks']['common_starts'],check)
 require(counts['authentic_E8_reads']==520 and counts['restored_first_X_rows']==104 and counts['nested_input_rows']==24,'complete source observations and nested checkpoints')
 require(len(cache_rows)==10 and set(cache_uses)==set(cache_rows) and all(v==1 for v in cache_uses.values()),'ten exactly once physically consumed caches')
 require(loc0==loc1 and set(before)==set(after),'complete common-start interface')
 delta={raw[y]:make(row) for y,row in d['forward'].items()};delta.update({raw[b]:make(row) for b,row in d['reverse'].items()})
 for j in before:require(after[j]==rowadd(before[j],delta.get(j,{})),'all1880 independent input columns in every current row')
 for x,(_,b) in d['host'].items():require(after[raw[b]]==q[b],'all96 original Y2 values retained')
 suffix=word['program'][word['marks']['common_starts']:];require(suffix==parent['program'][parent['marks']['common_starts']:],'literal complete72711-instruction common/final suffix')
 for j in delta:
  r=next(r for r,v in raw.items() if v==j);touches=[]
  for op in suffix:
   operands=op[1:3] if op[0] in ('ADD','COPY') else op[1:2]
   if j in operands:touches.append(op)
  require(touches==[['ADD',j,r,'1',source['final'][r]]],'no changed private feedback before final common recoupling')
 return dict(counts),macros,cache_rows

def terminal(source,parent,word,d):
 logical={int(r) for r in word['private_role_map']};M={r:{r:F(1)} for r in logical};remaining=0
 for x in d['X']:
  y=x+112;c=F(1) if x in d['host'] else F(1,2);row={y:c}
  for j in d['X']:
   v=c*F(d['G'][x,j],8)
   if v:row[j]=v
  for j,v in parent['corrections'].get(str(y),[]):row=rowadd(row,{j:F(v)})
  row=rowadd(row,d['forward'].get(y,{}));M[y]=row
  remaining+=sum(j not in (x,y) for j in row)
 for b,row in d['reverse'].items():M[b]=rowadd(M[b],row)
 inv={r:{r:F(1)} for r in logical}
 for x in d['X']:
  y=x+112;c=M[y][y];inv[y]={y:1/c}
  for j,v in M[y].items():
   if j!=y:inv[y][j]=-v/c
 for b,row in d['reverse'].items():inv[b]=rowadd({b:F(1)},row,F(-1))
 for r,row in inv.items():require(combine(list(row.values()),[M[j] for j in row])=={r:F(1)},'explicit complete400-row private inverse')
 require(remaining==4789,'exact residual4789 source coefficient duties')
 complete=[x+112 for x in d['X'] if M[x+112]=={x+112:F(1),x:F(1)}];require(complete==[112,113,210],'all and only the three completed ordinary first pairs')
 H=sorted(d['host']);R=[[d['reverse'].get(d['host'][x][0],{}).get(d['host'][y][1],F(0)) for y in H] for x in H];B=[[F(i==j)+R[i][j] for j in range(96)] for i in range(96)]
 require(rank(B)==95 and all(B[i][i]==1 for i in range(96)),'actual global reverse residual rank95 with no completed individual diagonal')
 v=[F(1) if x==0 else F(-1) if x in (1,98) else F(0) for x in H]
 require(all(sum(B[i][j]*v[j] for j in range(96))==0 for i in range(96)) and all(sum(v[i]*B[i][j] for i in range(96))==0 for j in range(96)),'exact preserved right and left dependent-triple relations')
 require(len({source['final'][d['host'][x][1]] for x in H})==96,'all96 original Y2s still separate at terminal facets')
 serial=lambda m:{str(r):[[j,str(v)] for j,v in sorted(row.items())] for r,row in sorted(m.items())}
 return dict(private_inverse_rows=400,matrix_sha256=sha(json.dumps(serial(M),sort_keys=True).encode()),inverse_sha256=sha(json.dumps(serial(inv),sort_keys=True).encode()),
             forward_complete_receivers=complete,forward_remaining_coefficients=remaining,reverse_changed_hosted_rows=len(d['reverse']),reverse_coefficients=183,
             reverse_residual_rank=95,reverse_complete_individual_pairs=0,reverse_complete_target_relations=1,
             retained_target_relation=[[d['host'][x][0],str(c)] for x,c in ((0,F(1)),(1,F(-1)),(98,F(-1)))],
             terminal_new_paid_MOVE_lower_bound=96,terminal_scope='Inherited separated-source terminal theorem applies because all other private rows are independent of hosted b/d, all96 d inputs remain separate, and every residual column has nonzero diagonal. This is no new complete reverse family.')

def metadata(parent,word,d):
 n=word['nested_acquisition'];serialize=lambda rows:{str(r):[[j,str(v)] for j,v in sorted(row.items())] for r,row in sorted(rows.items())}
 require(n['forward_correction_rows']==serialize(d['forward']) and n['reverse_correction_rows']==serialize(d['reverse']),'source-derived correction metadata')
 require(n['selected_roots']==SELECTED and n['old_completed_roots']==FULL and n['new_partial_roots']==[2,99,103] and n['begin']==410 and n['restored']==3077,'actual selected sets and nested phase boundaries')
 require(word['initial']==parent['initial'] and word['private_role_map']==parent['private_role_map'] and word['public']==1880 and word['owned_fields']==80,'complete original1880 input namespace')
 require(word['program'][:410]==parent['program'][:410],'unchanged actual entry differences and five real cache acquisitions')
 require(word['marks']['all_active_donors_restored']==3077 and word['marks']['common_starts']==4551 and word['marks']['initial_decoders']==4149 and word['marks']['prefix_scheduled']==4443,'current chronological named boundaries')
 require(word['native_event_to_physical']==[e+2505 for e in parent['native_event_to_physical']],'every actual retained native source event')
 for key,e in parent['marks'].items():
  if e>=parent['marks']['common_starts']:require(word['marks'][key]==e+2505,'actual retained common-history marker '+key)
 for key in ('initial_decoders','prefix_scheduled','common_starts'):
  actual=word['marks'][key];old=parent['marks'][key];require(word['parent_event_of_output'][actual]==old and word['program'][actual]==parent['program'][old],'actual boundary anchor '+key)
 require('private_route_blocks' not in word and word['parent_fused_route_provenance']==parent['private_route_blocks'],'inherited route receipts explicitly labelled provenance')
 corrections=dict(parent['corrections']);corrections.update(serialize(d['forward']));require(word['corrections']==corrections,'all old and newly paid correction rows exposed')
 require(word['parent_word_sha256']==PARENT_PIN and word['parent_payload_sha256']==PARENT_PAYLOAD,'exact parent identity')

def negatives(source,parent,word,d,records):
 rejected={};raw={int(r):v for r,v in word['private_role_map'].items()}
 def trial(name,candidate,algebra=True):
  try:
   typed(source,candidate)
   if algebra:semantic(source,parent,candidate,d,candidate['nested_acquisition']['records'])
  except ValueError as e:rejected[name]=str(e)
  require(name in rejected,'negative control escaped '+name)
 def coefficient(name,begin,end,targets=None):
  candidate=copy.deepcopy(word)
  e=next(e for e in range(begin,end) if candidate['program'][e][0]=='ADD' and (targets is None or candidate['program'][e][1] in targets))
  candidate['program'][e][3]=str(-F(candidate['program'][e][3]));trial(name,candidate)
 for name,g,mname in [('wrong_primitive_encoder',records[0],'primal_encoder'),('wrong_primitive_dual',records[0],'dual_encoder'),('wrong_nested_encoder',records[7],'primal_encoder'),('wrong_nested_dual',records[7],'dual_encoder')]:
  m=g[mname];coefficient(name,m['begin'],m['end'],{raw[r] for r in m['roles']})
 candidate=copy.deepcopy(word);g=candidate['nested_acquisition']['records'][7];g['incoming_current_rows'][0]=[[g['four_current_carriers'][0],'1']];trial('stale_original_row_at_nested_join',candidate)
 candidate=copy.deepcopy(word);ds={raw[pair[1]] for pair in d['host'].values()};e=next(e for e in range(410,3077) if candidate['program'][e][0]=='MOVE' and candidate['program'][e][1] in ds);candidate['program'].pop(e);trial('missing_actual_Y2_arrival',candidate,False)
 coefficient('wrong_final_primal_restore',1888,3077,{raw[x] for x in d['X']})
 candidate=copy.deepcopy(word);candidate['marks']['all_active_donors_restored']-=1
 try:metadata(parent,candidate,d)
 except ValueError as e:rejected['stale_boundary_marker']=str(e)
 require('stale_boundary_marker' in rejected,'stale boundary marker rejected')
 candidate=copy.deepcopy(word);candidate['additional_charts'][0]['frame'].pop()
 try:geometry(source,candidate,d)
 except ValueError as e:rejected['wrong_acquisition_subspace']=str(e)
 require('wrong_acquisition_subspace' in rejected,'wrong acquisition subspace rejected')
 return rejected

def main(a):
 base=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused'
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN);parent=load(base/'WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD)
 prior=load(base/'review/REVIEW-RESULT.json',pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e')
 require(prior['all1480_common_outputs_preserved'] and prior['private_inverse_rows_preserved']==400 and prior['all_other4985_residual_coefficients_preserved'],'authenticated parent map facts')
 word=load(a.package/'WORD.json.gz',True,payload=WORD_PIN);report=load(a.package/'RESULT.json');d=source_data(source);records=geometry(source,word,d);metadata(parent,word,d)
 sem,macros,caches=semantic(source,parent,word,d,records);end=terminal(source,parent,word,d)
 bill=typed(source,word);pbill=typed(source,parent)
 require(bill['final']==pbill['final'] and bill['peak']==43,'complete final charts and actual owned peak')
 require(len(word['program'])==77262 and bill['counts']=={'ADD':65785,'SCALE':3670,'MOVE':6932,'INIT':437,'CLEAR':437,'COPY':1},'complete operation bill')
 require(bill['rawranks']=={1:49,2:28,3:137,5:164,6:7,7:10,8:219} and sum(bill['rawranks'].values())==614 and sum(r*n for r,n in bill['rawranks'].items())==3200,'all614 raw calls and rank3200')
 invoice=load(base/'INPUT-INVOICE.json',pin=INVOICE_PIN);T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()};logical={int(r) for r in word['private_role_map']}
 oldraw=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE' and op[1] in logical)
 require(oldraw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'complete1710 old raw reservations')
 native=Counter(abs(len(source['frames'][op[3]])-len(source['frames'][op[2]])) for op in source['program'] if op[0]=='MOVE');extra=bill['ranks'].copy();extra.subtract(native);extra.subtract(bill['rawranks'])
 require({r:n for r,n in extra.items() if n}=={9:8},'all eight original rank9 packet calls retained exactly once, no additional owned MOVE')
 paid={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|{9}}
 require(all(n>=0 for n in paid.values()) and sum(paid.values())==132840 and sum(T.values())==27344,'complete nonnegative paid and target profiles')
 require(paid=={int(r):n for r,n in report['conditional_caller']['P_partial'].items()} and sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys())==3760,'exact caller and retained rank surplus')
 margin=tuple(v/18 for v in moment({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()}));bracket=report['conditional_caller']['remaining_moment_per_native_bounds']
 require(F(bracket[0])<=margin[0]<=margin[1]<=F(bracket[1]) and F(42172,1000)<margin[0]<margin[1]<F(42173,1000),'independent directed rational positive42.172.. source moment')
 require(margin[1]-96<0,'inherited separated-source terminal96-call repair is outside allowance')
 maps=load(a.package/'CHART-MAPS.json');pairs=lambda w:{(op[2],op[3]) for op in w['program'] if op[0]=='MOVE'};introduced=pairs(word)-pairs(parent);recipes=maps['introduced_maps'];frames=source['frames']+[c['frame'] for c in word['additional_charts']]
 require({(r['source'],r['target']) for r in recipes}==introduced and len(introduced)==117,'all117 introduced chart-map pairs covered')
 for r in recipes:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']]),'actual map rank')
 require(maps['word_sha256']==sha((a.package/'WORD.json.gz').read_bytes()) and maps['parent_sha256']==PARENT_PIN and maps['source_sha256']==SOURCE_PIN and maps['wrong_global_phase_rejected'],'exact source/word/map provenance and phase control')
 for name,pin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'retained chart-engine source pin')
 negative=negatives(source,parent,word,d,records)
 result=dict(status='PASS_INDEPENDENT_NESTED_CURRENT_ROW_WORD',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,parent_payload_sha256=PARENT_PAYLOAD,
             word_payload_sha256=WORD_PIN,word_sha256=sha((a.package/'WORD.json.gz').read_bytes()),operations_sha256=sha(json.dumps(word['program'],sort_keys=True,separators=(',',':')).encode()),
             reviewer_sha256=sha(Path(__file__).read_bytes()),reviewer_dependencies={name:sha(Path(__file__).with_name(name).read_bytes()) for name in ('check_cohort_word.py','cohort_geometry.py')},
             instructions=77262,counts=dict(bill['counts']),raw_calls=614,raw_profile=dict(bill['rawranks']),raw_rank_mass=3200,owned_peak=43,owned_lifetimes=437,new_owned_MOVEs=0,
             new_charts=10,primitive_cohorts=7,nested_current_row_recodings=3,introduced_map_coverage=117,independently_interpreted_input_columns=1880,
             actual_local_matrix_macros=len(macros),actual_checkpoint_counts=sem,all104_original_first_X_restored=True,all96_original_Y2_retained=True,
             all1480_common_outputs_preserved=True,unchanged_common_final_suffix_instructions=72711,terminal=end,
             new_forward_correction_coefficients=196,full_forward_receivers=[112,113,210],partial_forward_receivers={114:26,211:13,215:13},hosted_reverse_coefficients=183,
             paid_positions=132840,target_positions=27344,rank_surplus=3760,conditional_paid_profile=paid,conditional_target_profile=T,
             remaining_moment_exact=[str(v) for v in margin],remaining_moment_approx=float(margin[0]),terminal96_move_margin_exact=[str(v-96) for v in margin],negative_controls=negative,
             chart_engine_scope='Existing exact Clifford and phase engines credited with pinned author run; pair coverage, actual geometry, and ranks independently checked here.',
             scope='Finite exact causal source word, with actual staged current rows and all1880 input columns checked. Three full forward pairs,52 further coefficients,183 hosted reverse coefficients and the already known single reverse relation. Reverse residual rank95; no individual reverse pair. No full native family, supplier, foundation discharge, or new kappa.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('conditional_paid_profile','conditional_target_profile')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
