#!/usr/bin/env python3
"""Independent literal three-facet rewrite, pivot recovery, and physical map audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import copy,hashlib,importlib.util,json,sys
BASE=Path('/workspace/scratch/6a77123a1d61');OUT=Path(__file__).resolve().parent;PACK=BASE/'worker-coupling/three-facet-pivot-completion'
WPIN='2ad32467f783106631c5d64e73e7a6b12351c5b563558eae71c3b0e903a0d0a8'
WPAY='b9ece249b5032b44fa0dc6c82cfc14448cf8cc547b4b12b2e996d72f69a4b67f'
def helper():
 p=BASE/'worker-review/one-facet-completion/check_facet.py'
 if hashlib.sha256(p.read_bytes()).hexdigest()!='68fae3bd5a9a4f15a496f1e8b7b170880dfab6e66261cdd6d1455dc9a8c5f995':raise ValueError('own helper pin')
 spec=importlib.util.spec_from_file_location('own_prior_facet',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 f=helper();need,add,load=f.need,f.add,f.load
 h=f.own('route-fusion/check_fusion.py','cd0a90cc2773d144a1c106245d14c5a6f6ee9fad76dca64383a5dc2d7fa04763')
 e8=f.own('eight-packet-one-correction/check_composition.py','a089410089d0c57549379cc51c3dd09829b3cc9f0ee209d3e0ab2d53462aa473')
 s=load(f.REPO/'research/shared-wire-split-composition/data/final.json.gz',f.SPIN);p=load(f.PARENT/'WORD.json.gz',f.PPIN,f.PPAY);w=load(PACK/'WORD.json.gz',WPIN,WPAY)
 report=load(PACK/'RESULT.json','92e9c0e5e97ea3df7c4c8459298f80e53bb2c94eb63889d1489fdfaeab23c825')
 proofpin='f27b496fb97b28a49628d01f0f544f7307a8d227d7b0828b94f5dede1614bfe4';need(f.digest((PACK/'PROOF.md').read_bytes())==proofpin,'frozen proof')
 pr=load(BASE/'worker-review/eight-packet-seven-corrections-fused/REVIEW-RESULT.json','a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e');need(pr['word_payload_sha256']==f.PPAY,'independent parent interface')
 raw={int(r):j for r,j in p['private_role_map'].items()};xs=s['live'];roots=[e8.gram_root(v) for v in s['ports']];G=[[sum(a*b for a,b in zip(u,v)) for v in roots] for u in roots];c={x:(F(1) if i in s['hosted']['Dports'] else F(1,2)) for i,x in enumerate(xs)}
 ys=[168,189,212];facets={168:179,189:198,212:220};weights={}
 for y in ys:
  x=y-112;i=xs.index(x);need(c[x]==1 and s['final'][y]==facets[y],'ordinary receiver target');weights[y]={d:-F(G[i][j],8) for j,d in enumerate(xs) if d!=x and G[i][j]}
 need(all(len(row)==48 and set(row.values())=={F(-1,2),F(1,2)} for row in weights.values()),'144 exact foreign coefficients')
 donors=set().union(*(set(a) for a in weights.values()));groups={d:tuple(y for y in ys if d in weights[y]) for d in donors};classes={g:sorted(d for d in donors if groups[d]==g) for g in set(groups.values())}
 need(len(donors)==92 and {g:len(v) for g,v in classes.items()}=={(168,):14,(189,):14,(212,):16,(168,189):16,(168,212):14,(189,212):14,(168,189,212):4},'exact support partition')
 sites={(168,):179,(189,):198,(212,):220,(168,189):955,(168,212):904,(189,212):957,(168,189,212):1095}
 frame=[3,25,41,72,132,260];decl=[{'construction':'exact intersection of final facets','frame':frame,'index':1095,'source_facets':[179,198,220]}]
 need(len(s['frames'])==1095 and w['additional_charts']==decl,'explicit single new chart declaration')
 extended=dict(s,frames=s['frames']+[frame]);spaces=list(map(h.space,extended['frames']))
 for g,chart in sites.items():
  inter=set.intersection(*(spaces[facets[y]] for y in g));need(spaces[chart]==inter and len(inter)==2**(9-len(g)),'exact full intersection chart')
 need(len(spaces[1095])==64 and classes[(168,189,212)]==[12,17,31,38],'independent triple frame and real triple donors')
 need(all(spaces[s['initial'][d]]<spaces[sites[groups[d]]]<spaces[127] for d in donors),'every acquisition lies on its actual donor chain')
 owners={};ownerchart={};ownerinfo={};k=1937
 for g in sorted(classes,key=lambda g:(len(g),g)):
  for y in g:owners[g,y]=k;ownerchart[k]=sites[g];ownerinfo[k]=(g,y);k+=1
 need(k==1949,'twelve actual stationary collectors')
 pivots=[10,0,6];deliver={10:189,0:168,6:212};visitpair={168:(168,189),189:(189,212),212:(168,212)}
 need(all(len(groups[d])==2 and deliver[d] in groups[d] and weights[deliver[d]][d] for d in pivots),'three invertible exact-pair pivots')
 need(len({groups[d] for d in pivots})==3 and not set(pivots)&{36,37,47,110,111},'disjoint cohorts and unchanged controller acquisitions')
 old,new=p['program'],w['program'];reverse_raw={j:r for r,j in raw.items()};rawxs={raw[x] for x in xs}
 hoists=[(e,reverse_raw[o[1]]) for e,o in enumerate(old) if o[0]=='MOVE' and o[1] in rawxs]
 need(len(hoists)==104 and [e for e,d in hoists]==list(range(410,514)) and len({d for e,d in hoists})==104,'pure consecutive original104 donor MOVE block')
 for e,d in hoists:need(old[e]==['MOVE',raw[d],s['initial'][d],127,False],'one original donor line-to-hub reservation')
 oldevent={d:e for e,d in hoists};byhoist=dict(hoists);receiver_events={}
 for y in ys:
  moves=[e for e,o in enumerate(old) if o[0]=='MOVE' and o[1]==raw[y]]
  need(len(moves)==1 and old[moves[0]]==['MOVE',raw[y],3,facets[y],False],'one original receiver direct route');receiver_events[moves[0]]=y
 expected=[];lineage=[];mapping={};terms=[];routes=[];inits={};clears={};restored=None
 def emit(op,parent=None):
  e=len(expected);expected.append(op);lineage.append(parent);return e
 def ordinary_donor(d,e):
  g=groups[d];chart=sites[g];first=emit(['MOVE',raw[d],s['initial'][d],chart,False],e);enc=[]
  for y in g:
   owner=owners[g,y];at=emit(['ADD',owner,raw[d],str(weights[y][d]),chart]);enc.append({'coefficient':str(weights[y][d]),'event':at,'owner':owner,'receiver':y})
  last=emit(['MOVE',raw[d],chart,127,False],e)
  terms.append({'donor':d,'encoding':enc,'first_move_event':first,'hub_move_event':last,'parent_move_event':e,'route':[s['initial'][d],chart,127],'support':list(g)})
 def pivot_donor(d):
  g=groups[d];chart=sites[g];y=deliver[d];z=next(a for a in g if a!=y);e=oldevent[d];mapping[e]=len(expected);a=weights[y][d]
  first=emit(['MOVE',raw[d],s['initial'][d],chart,False],e);at=emit(['ADD',owners[g,z],raw[d],str(weights[z][d]),chart]);enc=[{'coefficient':str(weights[z][d]),'event':at,'owner':owners[g,z],'receiver':z}]
  scale=emit(['SCALE',raw[d],str(a),chart]);acc=emit(['ADD',raw[d],owners[g,y],'1',chart]);clears[owners[g,y]]=emit(['CLEAR',owners[g,y],chart])
  facet=emit(['MOVE',raw[d],chart,facets[y],False],e);delivery=emit(['ADD',owners[(y,),y],raw[d],'1',facets[y]]);hub=emit(['MOVE',raw[d],facets[y],127,False],e);recover=[]
  for v in classes[g]:
   if v==d:continue
   coefficient=-weights[y][v];at=emit(['ADD',raw[d],raw[v],str(coefficient),127]);recover.append({'coefficient':str(coefficient),'event':at,'source_donor':v})
  inv=emit(['SCALE',raw[d],str(1/a),127])
  terms.append({'delivered_receiver':y,'donor':d,'encoding':enc,'facet_delivery_event':delivery,'facet_move_event':facet,'first_move_event':first,'hub_move_event':hub,'hub_recovery_events':recover,'inverse_scale_event':inv,'parent_move_event':e,'pivot':True,'pivot_accumulate_event':acc,'pivot_coefficient':str(a),'pivot_scale_event':scale,'route':[s['initial'][d],chart,facets[y],127],'support':list(g),'visiting_receiver':z})
 for e,o in enumerate(old):
  if e==410:
   for owner,chart in ownerchart.items():inits[owner]=emit(['INIT',owner,chart])
  if e in byhoist and byhoist[e] in pivots:continue
  mapping[e]=len(expected)
  if e in byhoist and byhoist[e] in donors:ordinary_donor(byhoist[e],e)
  elif e in receiver_events:
   y=receiver_events[e];previous=3;path=[3];reads=[]
   for g in [(168,189,212),visitpair[y],(y,)]:
    chart=sites[g];owner=owners[g,y];move=emit(['MOVE',raw[y],previous,chart,False],e);read=emit(['ADD',raw[y],owner,'1',chart]);clears[owner]=emit(['CLEAR',owner,chart]);reads.append({'chart':chart,'move_event':move,'owner':owner,'read_event':read,'support':list(g)});path.append(chart);previous=chart
   routes.append({'parent_move_event':e,'reads':reads,'receiver':y,'route':path})
  else:emit(o,e)
  if e==513:
   for d in pivots:pivot_donor(d)
   restored=len(expected)
 need(expected==new and lineage==w['parent_event_of_output'],'entire75085-instruction rewrite independently derived')
 need(len(mapping)==len(old) and restored==w['marks']['all_active_donors_restored']==818,'every parent event accounted and donors restored boundary')
 collectors=[{'chart':chart,'clear_event':clears[owner],'init_event':inits[owner],'owner':owner,'receiver':ownerinfo[owner][1],'support':list(ownerinfo[owner][0])} for owner,chart in ownerchart.items()]
 collection={'collectors':collectors,'donor_terms':terms,'facets':{str(y):facets[y] for y in ys},'owned_moves':0,'parent_hoist_block':[410,513],'pivots':[{'donor':d,'support':list(groups[d])} for d in pivots],'receiver_routes':routes,'receivers':ys,'support_classes':[{'chart':sites[g],'donors':classes[g],'receivers':list(g)} for g in sorted(classes)],'triple_intersection':1095}
 need(collection==w['facet_collection'],'all acquisition, pivot, receiver and lifetime metadata reconstructed')
 need(w['owned_fields']==p['owned_fields']+12==69 and w['public']==1880 and w['initial']==p['initial'],'twelve actual new owners with unchanged public inputs')
 need(w['native_event_to_physical']==[mapping[e] for e in p['native_event_to_physical']],'all71261 native operations retain order and bytes')
 for k,e in p['marks'].items():need(w['marks'][k]==mapping[e],'old marker translation '+k)
 for y in ys:need(w['marks']['receiver_corrected_'+str(y)]==clears[owners[(y,),y]],'actual receiver completion event')
 need(max(clears.values())<w['marks']['common_starts'],'every new owner retired before common processing')
 changed={'program','marks','owned_fields','native_event_to_physical','corrections','schema','parent_event_of_output','parent_word_sha256','private_route_blocks'}
 for k,v in p.items():
  if k not in changed:need(w[k]==v,'retained parent interface '+k)
 need(w['parent_word_sha256']==f.PPIN and w['parent_fused_route_provenance']==p['private_route_blocks'] and 'private_route_blocks' not in w,'single compatible rewrite, old stops only provenance')
 corr=dict(p['corrections'])
 for y in ys:corr[str(y)]=[[d,str(a)] for d,a in sorted(weights[y].items())]
 need(w['corrections']==corr and w['newly_completed_firstY_receivers']==ys,'precisely144 new coefficients declared')
 # New exact full1880-coordinate prefix interpretation with event-level witnesses.
 state={j:{j:F(1)} for j in range(1480)};locations=dict(enumerate(w['initial']))
 for r,j in raw.items():state[j]={r:F(1),j:F(1)}
 enc={a['event']:t['donor'] for t in terms for a in t['encoding']}
 pivotterms=[t for t in terms if t.get('pivot')];deliveries={t['facet_delivery_event']:t for t in pivotterms};accumulates={t['pivot_accumulate_event']:t for t in pivotterms};inverses={t['inverse_scale_event']:t for t in pivotterms};recoveries={a['event']:a['source_donor'] for t in pivotterms for a in t['hub_recovery_events']}
 delivered_rows={};source_reads=[];recovery_sources=0
 for e,o in enumerate(new[:w['marks']['common_starts']]):
  kind,j=o[:2]
  if e==restored:need(all(state[raw[x]]=={raw[x]:F(1)} and locations[raw[x]]==127 for x in xs),'all104 original qX simultaneously restored at818')
  if e in enc:need(state[o[2]]=={raw[enc[e]]:F(1)},'all actual acquisitions read original q')
  if e in accumulates:
   t=accumulates[e];d=t['donor'];y=t['delivered_receiver'];a=weights[y][d];other={raw[v]:weights[y][v] for v in classes[groups[d]] if v!=d}
   need(state[j]=={raw[d]:a} and state[o[2]]==other,'real aggregate acquired without an independent pivot record')
  if e in deliveries:
   t=deliveries[e];d=t['donor'];y=t['delivered_receiver'];want={raw[v]:weights[y][v] for v in classes[groups[d]]}
   need(state[o[2]]==want and locations[o[2]]==facets[y],'full exact-pair aggregate delivered on its actual raw pivot');delivered_rows[d]=want.copy()
  if e in recoveries:need(state[o[2]]=={raw[recoveries[e]]:F(1)} and locations[o[2]]==127,'each original recovery source physically at hub');recovery_sources+=1
  if e>=restored and lineage[e] is not None and kind=='ADD' and o[2] in rawxs:
   need(state[o[2]]=={o[2]:F(1)} and locations[o[2]]==127,'every actual E8 source read sees original donor at hub');source_reads.append(e)
  if kind=='INIT':state[j]={};locations[j]=o[2]
  elif kind=='CLEAR':del state[j];del locations[j]
  elif kind=='ADD':add(state[j],state[o[2]],F(o[3]))
  elif kind=='SCALE':state[j]={r:F(o[2])*a for r,a in state[j].items()}
  elif kind=='MOVE':locations[j]=o[3]
  else:raise ValueError(kind)
  if e in inverses:need(state[j]=={raw[inverses[e]['donor']]:F(1)},'each pivot recovered immediately after its inverse scale')
 need(source_reads and recovery_sources==41 and set(delivered_rows)==set(pivots),'nonvacuous source reads and41 original-source inverse operations')
 before,_=f.prefix(p);need(set(before)==set(state),'all12 new owners absent at common entry')
 for j,row in before.items():
  want=row.copy()
  for y in ys:
   if j==raw[y]:add(want,{raw[d]:a for d,a in weights[y].items()})
  need(state[j]==want,'full1880-coordinate prefix differs only in three intended receiver rows')
 for y in ys:
  need(state[raw[y]]=={raw[y]:F(1),raw[y-112]:F(1)},'completed exact ordinary raw row')
  uses=[o for o in new[w['marks']['common_starts']:] if o[1]==raw[y] or o[0] in ('ADD','COPY') and o[2]==raw[y]]
  need(uses==[['ADD',raw[y],y,'1',facets[y]]],'no later receiver feedback except final recoupling')
 L={r:{r:F(1)} for r in raw}
 for i,x in enumerate(xs):
  L[x+112]={x+112:c[x]}
  for j,d in enumerate(xs):
   if G[i][j]:L[x+112][d]=c[x]*F(G[i][j],8)
 for y,terms0 in p['corrections'].items():add(L[int(y)],{d:F(a) for d,a in terms0})
 N={r:row.copy() for r,row in L.items()}
 for y in ys:add(N[y],weights[y])
 remaining=sum(d in xs and d!=x and a!=0 for x in xs for d,a in N[x+112].items());complete=[x+112 for x in xs if N[x+112]=={x+112:c[x],x:c[x]}]
 need(remaining==4841 and complete==ys and all(N[r]==L[r] for r in raw if r not in ys),'only144 designated residual coefficients removed')
 for r in raw:
  row=N[r].copy()
  if r-112 in c:
   for d,a in tuple(row.items()):
    if d in xs:add(row,N[d],-a)
   row={j:a/c[r-112] for j,a in row.items()}
  need(row=={r:F(1)},'explicit400-row global private inverse')
 pc=h.typed(s,p);nc=h.typed(extended,w)
 need(pc['final_locations']==nc['final_locations'] and pc['peak']==nc['peak']==43,'all actual types, final charts and owned peak')
 need({lineage[e]:v for e,v in nc['raw_uses'].items() if lineage[e] is not None}==pc['raw_uses'],'all retained raw arithmetic accesses keep actual charts')
 need(dict(nc['counts'])==report['bill']['opcode_counts'] and {str(r):n for r,n in nc['ranks'].items()}==report['bill']['move_rank_histogram'],'all physical operation counts')
 delta={k:nc['counts'][k]-pc['counts'][k] for k in set(nc['counts'])|set(pc['counts'])}
 need(delta==report['increment_over_fused_parent']=={'ADD':197,'SCALE':6,'MOVE':101,'INIT':12,'CLEAR':12,'COPY':0},'all328 additional instructions billed')
 rawexpected=Counter({1:61,2:43,3:4,5:5,6:48,7:48,8:299})
 need(nc['rawranks']==rawexpected and sum(rawexpected.values())==508 and sum(r*n for r,n in rawexpected.items())==3200,'exact508-call rank3200 raw profile')
 rawdelta={r:nc['rawranks'][r]-pc['rawranks'][r] for r in set(nc['rawranks'])|set(pc['rawranks'])}
 need(rawdelta=={1:56,2:41,3:4,5:4,6:47,7:44,8:-95},'source-class-derived route increments')
 need(not any(o[0]=='MOVE' and o[1] in ownerchart for o in new),'zero collector MOVEs')
 nativeprof=Counter(abs(len(s['frames'][o[3]])-len(s['frames'][o[2]])) for o in s['program'] if o[0]=='MOVE')
 need(nc['ranks']==nativeprof+rawexpected+Counter({9:8}),'all native calls plus raw calls plus eight paid rank9 packets')
 iv=load(f.REPO/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json','b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248')
 T={int(r):n for r,n in iv['T4'].items()};P={int(r):n for r,n in iv['P4'].items()};oldraw=Counter(abs(len(s['frames'][o[3]])-len(s['frames'][o[2]])) for o in s['program'] if o[0]=='MOVE' and o[1] in raw)
 paid={r:P.get(r,0)+18*(rawexpected[r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|rawexpected.keys()|{9}};bill=report['conditional_caller']
 need({str(r):n for r,n in paid.items()}==bill['P_partial'] and {str(r):n for r,n in T.items()}==bill['T4'],'full conditional caller rebuilt from actual MOVEs')
 need(all(n>=0 for n in paid.values()) and sum(paid.values())==130932 and sum(T.values())==27344 and sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys())==3760,'caller counts and rank surplus')
 powers={r:h.root_bracket(r) for r in T.keys()|P.keys()|paid.keys()};margin=tuple(v/18 for v in h.moment_interval({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()},powers));extra=h.moment_interval(rawdelta,powers)
 need(F(bill['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(bill['remaining_moment_per_native_upper']),'directed exact remaining moment')
 need(F(report['new_collection_raw_moment_lower'])<=extra[0]<=extra[1]<=F(report['new_collection_raw_moment_upper']),'directed exact extra route moment')
 charts=load(PACK/'CHART-MAPS.json','b691741e3e7db0b60f4e22831b60575507c88ecbcb537d46a612c84d4689c79c')
 oldmaps={(o[2],o[3]) for o in old if o[0]=='MOVE'};newmaps={(o[2],o[3]) for o in new if o[0]=='MOVE'}
 need(len(charts['recipes'])==99 and {(r['source'],r['target']) for r in charts['recipes']}==newmaps-oldmaps,'all99 introduced actual chart pairs covered exactly')
 need(charts['source_sha256']==f.SPIN and charts['parent_sha256']==f.PPIN and charts['word_sha256']==WPIN and charts['additional_charts']==decl and charts['original_frames_unchanged'],'new-map exact source and frame scope')
 for name,pin in charts['engine_pins'].items():need(f.digest((f.REPO/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'retained exact engine pin')
 vp=f.REPO/'research/shared-wire-split-composition/frozen/native_verify.py'
 need(f.digest(vp.read_bytes())=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','retained independent signed-Pauli/global-phase checker')
 vspec=importlib.util.spec_from_file_location('retained_exact_verifier',vp);v=importlib.util.module_from_spec(vspec);vspec.loader.exec_module(v)
 for r in charts['recipes']:
  a,b=r['source'],r['target'];need(r['recipe']['rank']==abs(len(extended['frames'][b])-len(extended['frames'][a])),'actual introduced recursive rank')
  v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(extended['frames'][a],9))+v.frame(extended['frames'][b],9),'reviewed introduced chart map')
 bad=copy.deepcopy(charts['recipes'][0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;phase_rejected=False
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(extended['frames'][bad['source']],9))+v.frame(extended['frames'][bad['target']],9),'review wrong global phase')
 except ValueError:phase_rejected=True
 need(phase_rejected,'nonvacuous independent retained-engine phase rejection')
 failures={};t=pivotterms[0];d=t['donor'];y=t['delivered_receiver'];a=F(t['pivot_coefficient'])
 mutant=[o.copy() for o in new];mutant[t['inverse_scale_event']][2]=str(2/a);z,_=f.prefix(dict(w,program=mutant));need(z[raw[d]]=={raw[d]:F(2)},'wrong inverse scale fails original donor restoration');failures['wrong_inverse_scale']='original q10 becomes2*q10'
 rec=t['hub_recovery_events'][0];mutant=[o.copy() for o in new];mutant[rec['event']][3]='0';z,_=f.prefix(dict(w,program=mutant));err=z[raw[d]].copy();add(err,state[raw[d]],F(-1));need(err=={raw[rec['source_donor']]:-F(rec['coefficient'])/a},'omitted hub cancellation leaves explicit unwanted donor');failures['omitted_hub_cancellation']={str(k):str(a) for k,a in err.items()}
 mutant=[o.copy() for o in new];mutant[t['facet_delivery_event']][3]='-1';z,_=f.prefix(dict(w,program=mutant));err=z[raw[y]].copy();add(err,state[raw[y]],F(-1));need(err=={k:-2*a for k,a in delivered_rows[d].items()},'wrong facet delivery sign corrupts exact intended row');failures['wrong_facet_delivery_sign_nonzero_terms']=len(err)
 mutant=[o.copy() for o in new];mutant[t['facet_move_event']][3]=127
 try:h.typed(extended,dict(w,program=mutant))
 except ValueError as err:failures['omitted_pivot_facet_stop']=str(err)
 need('cochart' in failures.get('omitted_pivot_facet_stop',''),'missing pivot facet stop rejected physically')
 wrongframe=frame.copy();wrongframe[0]=1;wrongsource=dict(s,frames=s['frames']+[wrongframe])
 try:h.typed(wrongsource,w)
 except ValueError as err:failures['wrong_new_chart']=str(err)
 need('nested' in failures.get('wrong_new_chart',''),'wrong new chart rejected by actual nested routes')
 failures['wrong_chart_recipe_global_phase_rejected']=phase_rejected
 result={
  'status':'PASS_INDEPENDENT_THREE_FACET_REVERSIBLE_RAW_PIVOTS','source_sha256':f.SPIN,'parent_compressed_sha256':f.PPIN,'word_compressed_sha256':WPIN,'word_payload_sha256':WPAY,'reviewed_proof_sha256':proofpin,
  'literal_parent_instructions_accounted':len(old),'exact_prefix_input_coordinates':1880,'native_instructions_preserved':71261,
  'support_class_counts':{','.join(map(str,g)):len(ds) for g,ds in sorted(classes.items())},'actual_pivot_donors':pivots,'pivot_delivery_receivers':deliver,'pivot_coefficients':{d:str(weights[deliver[d]][d]) for d in pivots},
  'distinct_donors':92,'new_chart':decl[0],'all_original_chart_frames_unchanged':True,
  'stationary_collectors':12,'collector_MOVEs':0,'all_collectors_retired_before_common':True,
  'original_qX_restoration_boundary':restored,'all104_original_donors_at_hub_before_E8':True,'exact_E8_source_reads_checked':len(source_reads),'actual_original_hub_recovery_source_reads':41,'all_three_delivered_aggregate_rows_checked':True,
  'prefix_delta_receiver_roles':ys,'completed_ordinary_blocks':[[y-112,y] for y in ys],'previous_seven_corrections_preserved':True,'all1480_common_outputs_preserved':True,'all_other4841_residual_coefficients_unchanged':True,
  'private_inverse_rows':400,'global_inverse_reason':'Invertible common Tu first recovers u; subtract its main rows from private endpoints to obtain Nq; explicit400-row inverse recovers q, hence v=u+q. No pivot original-value side record is granted.',
  'instructions':len(new),'counts':dict(nc['counts']),'MOVE_profile':dict(sorted(nc['ranks'].items())),'increment_over_fused_parent':delta,'peak_owned':43,'raw_profile':dict(sorted(rawexpected.items())),'raw_calls':508,'raw_rank_sum':3200,'retained_paid_packet_profile':{9:8},
  'conditional_paid_profile':dict(sorted(paid.items())),'conditional_paid_positions':130932,'conditional_target_positions':27344,'conditional_rank_surplus':3760,'extra_raw_moment_exact_bounds':[str(v) for v in extra],'extra_raw_moment_approximate':float(extra[0]),'remaining_conditional_moment_exact_bounds':[str(v) for v in margin],'remaining_conditional_moment_approximate':float(margin[0]),
  'introduced_chart_pair_coverage_and_rank':99,'introduced_chart_maps_freshly_checked_with_retained_signed_Pauli_global_phase_engine':99,'retained_phase_verifier_sha256':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','negative_controls':failures,
  'scope':'Independent entire compatible rewrite from the pinned fused seven-correction parent, exact1880-coordinate prefix delta and actual pivot/packet read witnesses, source-derived coefficients,400-row inverse, full physical route/type walk,99 exact map recipes freshly checked by the retained verifier, and complete conditional invoice. Parent common restoration/COPY guard and native invertibility are inherited from its independent review through the identical suffix. This is not a new chart engine or a full supplier proof. Remaining4841 foreign residuals and private reverse duties remain open.'
 }
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'completed':ys,'remaining':remaining,'E8_source_reads':len(source_reads),'counts':result['counts'],'raw_calls':508,'margin':float(margin[0]),'introduced_exact_maps':99,'negative_controls':failures},indent=2))
if __name__=='__main__':main()
