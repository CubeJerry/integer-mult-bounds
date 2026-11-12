#!/usr/bin/env python3
"""Actual two-level current-row primal/dual source construction.

The retained E8 prefix and common native remain literal. Seven dimension-six
acquisition groups feed three dimension-seven four-carrier recombinations.
No new owned MOVE is introduced. No complete global code or new kappa.
"""
import argparse,copy,hashlib,itertools,sys
from pathlib import Path

def main(a):
 utility_pins={'common.py':'c80bfa6edf54ec67535f4183cc5eeb3162d8965dd11dec3cb4abdd980ac4a9ed','build.py':'17e5c44cf46fe5873c393f0de32ac80837cd34fc9686007fcc15dd4956021bdd'}
 for name,pin in utility_pins.items():
  if hashlib.sha256((a.utilities/name).read_bytes()).hexdigest()!=pin:raise ValueError('retained utility pin '+name)
 sys.path.insert(0,str(a.utilities))
 from common import F,Counter,need,sha,load_inputs,source_data,space,basis,rank,inverse,mul,add,ser,gzip,json,Emitter,PPIN,PPAY
 import build as base
 s,parent,invoice=load_inputs(a.repo)
 selected=[0,1,2,98,99,103];oldX=[0,1,98];newX=[2,99,103]
 raw,W,Fc,classes,spaces=source_data(s,parent,selected)
 hosted={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 need(all(x in hosted for x in selected),'six independent hosted receiver pairs')
 oldY=[x+112 for x in oldX];newY=[x+112 for x in newX]
 pairs=[(oldY[0],oldY[1]),(oldY[0],oldY[2]),(oldY[1],oldY[2])]
 delivered={pairs[0]:oldY[1],pairs[1]:oldY[0],pairs[2]:oldY[2]}
 visits={oldY[0]:pairs[0],oldY[1]:pairs[2],oldY[2]:pairs[1]}
 declarations=[]
 def chart(g):
  S=frozenset.intersection(*(spaces[Fc[y]] for y in g))
  if S in spaces:return spaces.index(S)
  c=len(spaces);spaces.append(S);declarations.append({'index':c,'frame':basis(S),'source_facets':[Fc[y] for y in g],'construction':'exact intersection of source receiver facets'});return c
 sites={g:chart(g) for g in sorted(classes)};join={g:chart(g) for g in pairs}
 need(len(classes)==7 and all(len(spaces[c])==64 for c in sites.values()),'seven six-dimensional acquisition charts')
 need(all(len(spaces[c])==128 for c in join.values()),'three seven-dimensional recombination charts')
 pair_data=[];used=set()
 for pair in pairs:
  gs=[g for g in classes if set(pair)<=set(g)]
  need(len(gs)==2,'one star plus one cycle per old pair')
  star=next(g for g in gs if len(g)==3);cycle=next(g for g in gs if len(g)==4)
  need(len(classes[star])==13 and len(classes[cycle])==11,'actual A3 cohort populations')
  new=next(y for y in star if y not in oldY)
  extra=next(y for y in cycle if y not in oldY)
  pair_data.append({'pair':pair,'star':star,'cycle':cycle,'new':new,'extra':extra});used|={star,cycle}
 fourth=next(g for g in classes if g not in used)
 need(fourth==tuple(newY),'fourth star on the new receiver triple')
 primitive={}
 for g,donors in sorted(classes.items()):
  H=[d for d in donors if d in hosted];U=[d for d in donors if d not in hosted]
  if g==fourth:targets=[newY[0]]
  else:
   pd=next(p for p in pair_data if g in [p['star'],p['cycle']])
   targets=[pd['pair'][0]] if g==pd['star'] else list(pd['pair'])+[pd['extra']]
  rows=[[W[y][d] for d in H] for y in targets];m=len(targets)
  need(rank(rows)==m,'hosted acquisition rows stay independent')
  J=next(J for J in itertools.combinations(range(len(H)),m) if rank([[row[j] for j in J] for row in rows])==m)
  M=[[F(i==j) for j in range(len(H))] for i in range(len(H))]
  for i,j in enumerate(J):M[j]=rows[i].copy()
  Mi=inverse(M);need(mul(M,Mi)==[[F(i==j) for j in range(len(H))] for i in range(len(H))],'primitive invertible current-row encoder')
  primitive[g]={'g':g,'donors':donors,'hosted':H,'controls':U,'targets':targets,'pivot_positions':list(J),'pivots':[H[j] for j in J],'matrix':M,'inverse':Mi,'chart':sites[g]}
 # Every affected second-bank carrier has only its literal direct route before
 # the common word. Its initial difference value is therefore available.
 affectedB={hosted[d][0] for p in primitive.values() for d in p['hosted']}
 affectedD={hosted[x][1] for x in selected};affected=affectedB|affectedD
 oldmove={}
 for r in affected|set(s['live']):
  if r in s['live']:uses=[(t,o) for t,o in enumerate(parent['program'][400:parent['marks']['common_starts']],400) if o[0]=='MOVE' and o[1]==raw[r]]
  else:uses=[(t,o) for t,o in enumerate(parent['program'][400:parent['marks']['common_starts']],400) if o[1]==raw[r] or o[0] in ('ADD','COPY') and o[2]==raw[r]]
  need(len(uses)==1 and uses[0][1]==['MOVE',raw[r],s['initial'][r],s['final'][r],False],'unread direct source carrier '+str(r))
  oldmove[r]=uses[0][0]
 receive_move={}
 for y in oldY+newY:
  es=[t for t,o in enumerate(parent['program']) if o[0]=='MOVE' and o[1]==raw[y]]
  need(len(es)==1 and parent['program'][es[0]]==['MOVE',raw[y],3,Fc[y],False],'unread first receiver direct route')
  receive_move[es[0]]=y
 E=Emitter();temp=list(range(1880+parent['owned_fields'],1880+parent['owned_fields']+max(len(p['hosted']) for p in primitive.values())))
 next_label=temp[-1]+1;cache={};cache_declarations=[];records=[];boundaries={};restored=None
 def emit(o,parent_event=None):return E.emit(o,parent_event)
 def route(r,a0,b0):
  t=emit(['MOVE',raw[r],a0,b0,False],oldmove.get(r));E.mapping.setdefault(oldmove.get(r),t);return t
 def dense(roles,M,C,label):
  start=len(E.ops)
  for i,r in enumerate(roles):emit(['INIT',temp[i],C]);emit(['ADD',temp[i],raw[r],'1',C])
  for i,r in enumerate(roles):
   emit(['ADD',raw[r],temp[i],'-1',C])
   for j,c in enumerate(M[i]):
    if c:emit(['ADD',raw[r],temp[j],str(c),C])
  for i in range(len(roles)):emit(['CLEAR',temp[i],C])
  return {'kind':label,'begin':start,'end':len(E.ops),'roles':roles,'chart':C,'matrix':[[str(c) for c in row] for row in M]}
 def record(y,C,donor,coef=F(1),label='observation'):
  nonlocal next_label
  h=next_label;next_label+=1;emit(['INIT',h,C]);t=emit(['ADD',h,raw[donor],str(coef),C]);cache.setdefault(y,[]).append((C,h));cache_declarations.append({'owner':h,'chart':C,'receiver':y,'event':t,'carrier':donor,'coefficient':str(coef),'kind':label});return h
 def dual_injection(y,C,donor,coef=F(1)):
  return emit(['ADD',raw[hosted[donor][0]],raw[hosted[y-112][1]],str(-coef),C])
 def ratio(y,ref,g):
  ds=classes[g];r=W[y][ds[0]]/W[ref][ds[0]];need(all(W[y][d]==r*W[ref][d] for d in ds),'rank-one star multiplier');return r
 forward={y:{} for y in oldY+newY};reverse={b:{} for b in affectedB}
 def declare_correction(y,donors):
  for d in donors:
   need(d not in forward[y],'no duplicated correction coefficient');c=W[y][d];forward[y][d]=c
   if d in hosted:reverse[hosted[d][0]][hosted[y-112][1]]=-c
 def network():
  nonlocal restored
  start=len(E.ops)
  for p in primitive.values():
   C=p['chart'];entry={'support':list(p['g']),'chart':C,'begin':len(E.ops),'hosted_donors':p['hosted'],'coupled_controls':p['controls'],'pivot_first_donors':p['pivots'],'target_rows':p['targets']}
   for d in p['donors']:route(d,s['initial'][d],C)
   for d in p['hosted']:b=hosted[d][0];route(b,s['initial'][b],C)
   entry['primal_encoder']=dense(p['hosted'],p['matrix'],C,'primitive_primal')
   for d,y in zip(p['pivots'],p['targets']):
    for u in p['controls']:emit(['ADD',raw[d],raw[u],str(W[y][u]),C])
   entry['dual_encoder']=dense([hosted[d][0] for d in p['hosted']],list(map(list,zip(*p['inverse']))),C,'primitive_dual')
   if p['g']!=fourth and len(p['g'])==3:
    pd=next(pd for pd in pair_data if pd['star']==p['g']);y=pd['new'];d=p['pivots'][0];coef=ratio(y,p['targets'][0],p['g']);q=hosted[y-112][1]
    route(q,3,C);record(y,C,d,coef,'new_receiver_star_read');dual_injection(y,C,d,coef);route(q,C,Fc[y]);declare_correction(y,p['donors'])
   for d in p['controls']:route(d,C,127)
   for d in p['hosted']:
    if d not in p['pivots']:route(d,C,127);route(hosted[d][0],C,127)
   entry['end']=len(E.ops);records.append(entry)
  for pd in pair_data:
   g=pd['pair'];C=join[g];ps=primitive[pd['star']];pc=primitive[pd['cycle']];roles=ps['pivots']+pc['pivots'];need(len(roles)==4,'four actual incoming encoded carriers')
   for d in roles:
    C0=ps['chart'] if d in ps['pivots'] else pc['chart'];route(d,C0,C);route(hosted[d][0],C0,C)
   expected=[];expected_dual=[]
   for p in [ps,pc]:
    for y in p['targets']:expected.append({d:W[y][d] for d in p['donors']})
    D=list(map(list,zip(*p['inverse'])))
    for j in p['pivot_positions']:
     row={hosted[h][0]:D[j][k] for k,h in enumerate(p['hosted']) if D[j][k]}
     if p is ps:row[hosted[pd['new']-112][1]]=-ratio(pd['new'],p['targets'][0],p['g'])
     expected_dual.append(row)
   alpha=[ratio(y,ps['targets'][0],pd['star']) for y in g]
   M=[[alpha[0],F(1),F(0),F(0)],[alpha[1],F(0),F(1),F(0)],[F(1),F(0),F(0),F(0)],[F(0),F(0),F(0),F(1)]]
   Mi=inverse(M);pd.update(roles=roles,matrix=M,inverse=Mi)
   entry={'pair':list(g),'chart':C,'four_current_carriers':roles,'four_current_dual_carriers':[hosted[d][0] for d in roles],'incoming_current_rows':[ser(r) for r in expected],'incoming_dual_rows':[ser(r) for r in expected_dual],'before_primal':len(E.ops)}
   entry['primal_encoder']=dense(roles,M,C,'nested_primal')
   entry['dual_encoder']=dense([hosted[d][0] for d in roles],list(map(list,zip(*Mi))),C,'nested_dual')
   vis=next(y for y in g if y!=delivered[g]);q=hosted[vis-112][1];route(q,3,C)
   for i,y in enumerate(g):
    d=roles[i]
    if y==vis:record(y,C,d,label='old_receiver_join_read');dual_injection(y,C,d)
   route(q,C,Fc[vis]);entry['end']=len(E.ops);records.append(entry)
   for y in g:declare_correction(y,ps['donors']+pc['donors'])
  # All reverse source values now stand at their final facets. Every delivery
  # below reads an actual unchanged current Y2 value, before separation loses it.
  for pd in pair_data:
   C=join[pd['pair']];y=delivered[pd['pair']];j=list(pd['pair']).index(y)
   for i,d in enumerate(pd['roles']):
    if i==j:
     route(d,C,Fc[y]);route(hosted[d][0],C,Fc[y]);record(y,Fc[y],d,label='old_receiver_facet_read');dual_injection(y,Fc[y],d);route(d,Fc[y],127);route(hosted[d][0],Fc[y],127)
    else:route(d,C,127);route(hosted[d][0],C,127)
  p=primitive[fourth];d=p['pivots'][0];C=p['chart'];y=newY[0]
  route(d,C,Fc[y]);route(hosted[d][0],C,Fc[y]);record(y,Fc[y],d,label='fourth_star_facet_read');dual_injection(y,Fc[y],d);route(d,Fc[y],127);route(hosted[d][0],Fc[y],127);declare_correction(y,p['donors'])
  processed=set().union(*(set(p['donors']) for p in primitive.values()))
  for d in s['live']:
   if d not in processed:route(d,s['initial'][d],127)
  for pd in pair_data:
   dense(pd['roles'],pd['inverse'],127,'nested_primal_inverse');dense([hosted[d][0] for d in pd['roles']],list(map(list,zip(*pd['matrix']))),127,'nested_dual_decoder')
  for p in primitive.values():
   for d,y in zip(p['pivots'],p['targets']):
    for u in p['controls']:emit(['ADD',raw[d],raw[u],str(-W[y][u]),127])
   dense(p['hosted'],p['inverse'],127,'primitive_primal_inverse');dense([hosted[d][0] for d in p['hosted']],list(map(list,zip(*p['matrix']))),127,'primitive_dual_decoder')
  restored=len(E.ops);return start,restored
 skip=set(oldmove.values());bounds=None
 for t,o in enumerate(parent['program']):
  if t==410:bounds=network()
  boundaries[t]=len(E.ops)
  if t in skip:continue
  E.mapping[t]=len(E.ops)
  if t in receive_move:
   y=receive_move[t];prev=3
   for C,h in sorted(cache[y],key=lambda item:len(spaces[item[0]])):
    if C!=prev:emit(['MOVE',raw[y],prev,C,False],t);prev=C
    emit(['ADD',raw[y],h,'1',C]);emit(['CLEAR',h,C])
   if prev!=Fc[y]:emit(['MOVE',raw[y],prev,Fc[y],False],t)
  else:emit(copy.deepcopy(o),t)
 need(None not in E.mapping and len(E.mapping)==len(parent['program']),'every original event accounted')
 w=copy.deepcopy(parent);w.update(schema='moonshot-S008-nested-current-row-primal-dual-v1',program=E.ops,owned_fields=next_label-1880,additional_charts=declarations,parent_word_sha256=PPIN,parent_payload_sha256=PPAY,retained_utility_sha256=utility_pins,parent_event_of_output=E.lineage,marks={k:boundaries[v] for k,v in parent['marks'].items()},native_event_to_physical=[E.mapping[v] for v in parent['native_event_to_physical']])
 w['parent_fused_route_provenance']=w.pop('private_route_blocks')
 w['inherited_provenance_scope']='parent_fused_route_provenance, parent_raw_reservation_provenance, prefix_semantic_provenance and prefix_decompressed_sha256 describe pinned ancestor artifacts only. Their event numbers are not current word indices; current instruction maps are native_event_to_physical and nested_acquisition.'
 w['parent_fused_correction_provenance']=copy.deepcopy(w['corrections'])
 w['corrections'].update({str(y):ser(r) for y,r in forward.items()})
 w['newly_completed_firstY_receivers']=oldY;w['partially_corrected_firstY_receivers']={str(y):len(forward[y]) for y in newY}
 w['reservation_accounting']='All400 raw source paths are replaced by the emitted nested profile. Every emitted MOVE is included in the complete invoice; removed ancestor stops cannot be reused for free. The common native remains literal.'
 w['marks']['all_active_donors_restored']=restored
 w['nested_acquisition']={'selected_roots':selected,'old_completed_roots':oldX,'new_partial_roots':newX,'begin':bounds[0],'restored':bounds[1],'records':records,'forward_correction_rows':{str(y):ser(r) for y,r in forward.items()},'reverse_correction_rows':{str(b):ser(r) for b,r in reverse.items() if r},'cache_declarations':cache_declarations,'temporary_fields':temp,'new_owned_MOVEs':0,'source_types':'All400 raw roles remain arbitrary independent differences. Coupled first-X fields are unchanged controls; hosted second-X fields are a separate inverse-transpose bank. Original hosted second-Y values are routed before departure and read at actual matching charts.'}
 w['scope']='Exact finite nested current-row partial primal/dual code; three new full forward receivers,52 additional source coefficients, and their hosted transpose supplied. Full target map and supplier/foundation obligations remain. No new kappa.'
 # Fresh actual prefix replay through every new matrix and every paired source
 # reading; the existing interpreter is disclosed, not called independent.
 old,oldloc=base.interpret_prefix(s,parent);new,newloc=base.interpret_prefix(s,w);q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 need(oldloc==newloc and set(old)==set(new),'identical live prefix interface')
 for r,row in old.items():
  want=row
  for y,coeff in forward.items():
   if r==raw[y]:
    for d,c in coeff.items():want=add(want,q[d],c)
  for b,coeff in reverse.items():
   if r==raw[b]:
    for d,c in coeff.items():want=add(want,q[d],c)
  need(new[r]==want,'all1880 actual prefix rows match declared primal and dual deltas')
 for y in oldY:need(new[raw[y]]==add(q[y],q[y-112]),'three authentic complete ordinary first-Y rows')
 need([len(forward[y]) for y in newY]==[26,13,13] and all(len(forward[y])==48 for y in oldY),'exact52 additional forward coefficients')
 tail=w['program'][w['marks']['common_starts']:];need(tail==parent['program'][parent['marks']['common_starts']:],'literal common suffix preserved')
 for r in set(oldY+newY)|affectedB|affectedD:
  uses=[o for o in tail if o[1]==raw[r] or o[0] in ('ADD','COPY') and o[2]==raw[r]]
  need(uses==[['ADD',raw[r],r,'1',s['final'][r]]],'changed raw rows have no later feedback')
 bill=base.typed(s,w);before=base.typed(s,parent);need(bill.pop('final_locations')==before.pop('final_locations'),'final public charts identical')
 R=Counter(bill['raw_histogram']);Rold=Counter(abs(len(s['frames'][o[3]])-len(s['frames'][o[2]])) for o in s['program'] if o[0]=='MOVE' and o[1] in raw);P=Counter({int(k):v for k,v in invoice['P4'].items()});T=Counter({int(k):v for k,v in invoice['T4'].items()})
 for r in R.keys()|Rold.keys():P[r]+=18*(R[r]-Rold[r])
 P[9]+=18*8;lo,hi=base.interval({r:T[r]-P[r] for r in T.keys()|P.keys()});need(all(n>=0 for n in P.values()) and sum(r*n for r,n in R.items())==3200,'full nonnegative invoice and monotone raw rankmass')
 X=s['hosted']['X2'];Y=s['hosted']['Y2'];iy={r:i for i,r in enumerate(Y)};residual=[[F(i==j)+reverse.get(b,{}).get(d,F(0)) for j,d in enumerate(Y)] for i,b in enumerate(X)]
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_ACTUAL_NESTED_CURRENT_ROW_PRIMAL_DUAL','source_sha256':w['source_sha256'],'base_parent_sha256':PPIN,'base_parent_payload_sha256':PPAY,'retained_utility_sha256':utility_pins,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_coordinates':1880,'completed_firstY_receivers':oldY,'partial_firstY_coefficients':{str(y):len(forward[y]) for y in newY},'new_forward_coefficients':sum(map(len,forward.values())),'remaining_forward_coefficients':4985-sum(map(len,forward.values())),'new_reverse_coefficients':sum(map(len,reverse.values())),'hosted_reverse_residual_rank':rank(residual),'all104_first_X_originals_restored_before_E8':True,'all96_second_Y_values_unchanged':True,'common_native_literal_suffix_unchanged':True,'primitive_acquisition_charts':7,'nested_four_current_carrier_charts':3,'new_owned_MOVEs':0,'bill':bill,'conditional_caller':{'P_partial':dict(sorted(P.items())),'T4':dict(sorted(T.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_bounds':[str(lo/18),str(hi/18)],'remaining_moment_per_native_approximate':float(lo/18)},'scope':w['scope'],'source_access':'Every reverse injection reads the unchanged original hosted second-Y value at its actual current chart before departure; no final-rank-to-communication inference is used.'}
 (a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--utilities',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
