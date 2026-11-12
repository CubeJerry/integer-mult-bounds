#!/usr/bin/env python3
"""Independent literal principal extension, exact current rows and rank87 proof.
Uses this reviewer's own copied independent engine, never author modules.
"""
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from independent_engine import span,root9,dot,replay,rowplus,interval,need,sha
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
WORD='b30716372b682b2f3da37f89a12d64e90f7640c408b393e1828770fbd33d817d'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111];T=90
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
 pb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes()
 wb=a.word.read_bytes();need(sha(sb)==SOURCE and sha(pb)==PARENT and sha(wb)==WORD,'frozen source and exact word pins')
 src,p,w=[json.loads(gzip.decompress(b)) for b in (sb,pb,wb)];author=json.loads((a.word.parent/'RESULT.json').read_text())
 raw={int(k):v for k,v in p['private_role_map'].items()};H=[src['live'][i] for i in src['hosted']['Dports']]
 host={h:(x,y) for h,x,y in zip(H,src['hosted']['X2'],src['hosted']['Y2'])}
 need(T in H and T not in B+S and set(B+S)<=set(H),'all indices genuinely hosted')
 roots={h:root9(src['frames'][src['initial'][h]][0]) for h in H};G={(h,j):F(dot(roots[h],roots[j]),18) for h in H for j in H}
 ss=[s for s in S if G[T,s]];ks=[s for s in B+S if G[T,s]]
 need(len(ss)==4 and len(ks)==8,'independent source contact sets')
 need(w['initial']==p['initial'] and w['additional_charts']==p['additional_charts'] and w['private_role_map']==p['private_role_map'] and w['owned_fields']==p['owned_fields'],'preserved declarations and source inputs')
 frames=src['frames']+[d['frame'] for d in w['additional_charts']];spaces=list(map(span,frames));line=src['initial'][T]
 need(src['initial'][host[T][0]]==line,'authentic paired line')
 oldroutes={}
 for s in ss:
  role=host[s][1];events=[i for i,e in enumerate(p['program']) if e[0]=='MOVE' and e[1]==raw[role]]
  need(len(events)==1,'one genuine raw Y2 route');i=events[0]
  need(p['program'][i]==['MOVE',raw[role],3,src['final'][role],False],'unchanged source direct route')
  need(spaces[line]<spaces[src['final'][role]],'initial T line inside actual S facet');oldroutes[i]=s
 q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 rows0,loc0,_=replay(p,spaces,400,True)
 need(rows0[raw[host[T][0]]]==q[host[T][0]] and loc0[raw[host[T][0]]]==line,'authentic current dual at initial line')
 need(all(rows0[raw[host[s][1]]]==q[host[s][1]] and loc0[raw[host[s][1]]]==3 for s in ss),'four authentic current reverse sources at empty chart')
 ops=[];lineage=[];early=[];feedback=[];bound={}
 def emit(e,parent=None):ops.append(e);lineage.append(parent);return len(ops)-1
 def preload():
  for i,s in sorted(oldroutes.items()):
   early.append(emit(['MOVE',raw[host[s][1]],3,line,False],i))
   early.append(emit(['ADD',raw[host[T][0]],raw[host[s][1]],str(G[T,s]),line]))
 def finishcolumn():
  f=src['final'][host[T][1]]
  feedback.append(emit(['INIT',1880,f]));feedback.append(emit(['ADD',1880,raw[host[T][1]],'1',f]));feedback.append(emit(['MOVE',1880,f,127,True]))
  for k in ks:feedback.append(emit(['ADD',raw[host[k][0]],1880,str(G[k,T]),127]))
  feedback.append(emit(['CLEAR',1880,127]))
 for i,e in enumerate(p['program']):
  if i==400:preload()
  if i==p['marks']['common_starts']:finishcolumn()
  bound[i]=len(ops)
  if i in oldroutes:emit(['MOVE',e[1],line,e[3],False],i)
  else:emit(copy.deepcopy(e),i)
 need(ops==w['program'],'all78143 operations independently reconstructed')
 need(lineage==w['parent_event_of_output'],'exact independently reconstructed lineage')
 occ=defaultdict(list)
 for j,i in enumerate(lineage):
  if i is not None:occ[i].append(j)
 need(w['native_event_to_physical']==[occ[i][0] for i in p['native_event_to_physical']],'actual native event map')
 need(w['marks']=={name:bound[i] for name,i in p['marks'].items()},'actual retained boundary map')
 parent_rows,parent_loc,_=replay(p,spaces,p['marks']['common_starts'],True)
 # Prove the source premises of every alternative one-port template directly.
 # This does not claim that successive templates can reuse a consumed route.
 need(all(parent_rows[r].get(raw[host[h][0]],F(0))==(r==raw[host[h][0]])
          for h in H for r in parent_rows),'all96 independent b columns are identity on every live parent field')
 all_s_routes={}
 for s in S:
  role=raw[host[s][1]];events=[i for i,e in enumerate(p['program']) if e[0]=='MOVE' and e[1]==role]
  need(len(events)==1,'unique raw d_S route for full family');i=events[0]
  need(p['program'][i]==['MOVE',role,3,src['final'][host[s][1]],False],'genuine family direct route')
  need(not any(e[1]==role or e[0] in ('ADD','COPY') and e[2]==role for e in p['program'][400:i]),'no intervening source observation before hoist')
  need(rows0[role]==q[host[s][1]] and loc0[role]==3,'all eight authentic initial d_S')
  all_s_routes[s]=i
 retained_owned={r:c for r,c in parent_loc.items() if r>=1880}
 need(retained_owned=={1932:33,1933:34,1934:43,1935:103,1936:104},'five retained parent caches at common entry')
 need(1880 not in parent_loc,'one reused owned slot free at exact final cut')
 family=[];family_pairs=set()
 for t in H:
  if t in B+S:continue
  line_t=src['initial'][t];contacts=[s for s in S if G[t,s]];outputs=[k for k in B+S if G[k,t]]
  need(len(contacts)==4 and len(outputs)==8,'every one-port family has4+8 contacts')
  need(rows0[raw[host[t][0]]]==q[host[t][0]] and loc0[raw[host[t][0]]]==line_t,'every candidate authentic initial dual line')
  need(all(spaces[line_t]<spaces[src['final'][host[s][1]]] for s in contacts),'every family raw subdivision is legal')
  need(parent_rows[raw[host[t][1]]]==q[host[t][1]] and parent_loc[raw[host[t][1]]]==src['final'][host[t][1]],'every genuine current return source at actual facet')
  need(all(parent_loc[raw[host[k][0]]]==127 for k in outputs),'every actual current output available at hub')
  family_pairs.add((3,line_t));family_pairs.add((src['final'][host[t][1]],127))
  family_pairs.update((line_t,src['final'][host[s][1]]) for s in contacts)
  family.append({'port':t,'initial_line':line_t,'early_S_contacts':contacts,'hub_column_contacts':outputs,'return_facet':src['final'][host[t][1]],'alternative_template_rank':87})
 need(len(family)==80,'80 alternative one-port source templates')
 actual,locations,_=replay(w,spaces,w['marks']['common_starts'],True);want={r:v.copy() for r,v in parent_rows.items()}
 for s in ss:want[raw[host[T][0]]]=rowplus(want[raw[host[T][0]]],q[host[s][1]],G[T,s])
 for k in ks:want[raw[host[k][0]]]=rowplus(want[raw[host[k][0]]],q[host[T][1]],G[k,T])
 need(actual==want and locations==parent_loc,'exact all1880 coefficients and current charts')
 need(all(actual[raw[x+112]]==parent_rows[raw[x+112]] for x in src['live']),'all forward rows unchanged')
 suffix=w['program'][w['marks']['common_starts']:];need(suffix==p['program'][p['marks']['common_starts']:],'literal unchanged common suffix')
 for k in [T]+ks:
  x=host[k][0];uses=[e for e in suffix if e[1]==raw[x] or e[0] in ('ADD','COPY') and e[2]==raw[x]]
  need(uses==[['ADD',raw[x],x,'1',src['final'][x]]],'changed reverse row only recouples later')
 M={}
 for h in H:
  x=host[h][0];coeff={j:actual[raw[x]].get(raw[host[j][1]],F(0)) for j in H};inverse=actual[raw[x]]
  need({int(r):F(c) for r,c in w['paired_reverse_corrections'][str(x)]}=={host[j][1]:c for j,c in coeff.items() if c},'all96 current reverse metadata rows match interpreted coefficients')
  for j,c in coeff.items():
   if c:inverse=rowplus(inverse,actual[raw[host[j][1]]],-c)
  need(inverse==q[x],'explicit full current b inverse using authentic retained d')
  M[h]={j:c+F(h==j) for j,c in coeff.items() if c+F(h==j)}
 need(all(actual[raw[host[h][1]]]==q[host[h][1]] for h in H),'all96 authentic Y2 retained')
 K=B+S+[T];outside=[h for h in H if h not in K]
 need(all(M[i].get(j,F(0))==G[i,j] for i in K for j in K) and all(not M[i].get(j) for i in K for j in outside),'closed principal Gram block')
 kernel=[]
 for u in S+[T]:
  z={h:-G[h,u] if h in B else F(h==u) if h in S+[T] else G[h,u] for h in H}
  need(all(sum(c*z[j] for j,c in M[i].items())==0 for i in H),'actual full residual kernel')
  kernel.append({str(h):str(c) for h,c in z.items() if c})
 minor=B+outside
 need(len(minor)==87 and all(M[i].get(j,F(0))==(i==j) for i in B for j in minor) and all(M[i].get(j,F(0))==(i==j) for i in outside for j in outside),'unit block-triangular87 minor')
 _,final,bill=replay(w,spaces);_,parent_final,oldbill=replay(p,spaces);need(final==parent_final and set(final)==set(range(1880)),'all final charts and owned retirement')
 need(json.loads(json.dumps(bill))==author['bill'],'independent whole-word bill')
 delta=Counter(bill['raw_histogram']);delta.subtract(oldbill['raw_histogram']);delta={r:n for r,n in delta.items() if n}
 need(delta=={1:4,7:4,8:-4},'all four raw refinements charged')
 ordinary={op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(set(bill['opcode_counts'])|set(oldbill['opcode_counts']))}
 need(ordinary=={'ADD':13,'CLEAR':1,'COPY':0,'INIT':1,'MOVE':5,'SCALE':0},'exact complete ordinary increment')
 ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(ib)==INVOICE,'original caller invoice pin');iv=json.loads(ib)
 originalraw=Counter(abs(len(src['frames'][e[3]])-len(src['frames'][e[2]])) for e in src['program'] if e[0]=='MOVE' and e[1] in raw)
 targets=Counter({int(k):v for k,v in iv['T4'].items()});paid=Counter({int(k):v for k,v in iv['P4'].items()})
 for r in set(originalraw)|set(bill['raw_histogram']):paid[r]+=18*(bill['raw_histogram'].get(r,0)-originalraw[r])
 paid[9]+=144;paid[1]+=18
 need({str(r):n for r,n in paid.items()}==author['conditional_caller']['P_partial'],'independently rebuilt complete H4 invoice')
 lo,hi=interval({r:targets[r]-paid[r] for r in targets.keys()|paid.keys()});lo/=18;hi/=18;claimed=author['conditional_caller']
 need(F(claimed['remaining_moment_per_native_lower'])<=lo<=hi<=F(claimed['remaining_moment_per_native_upper']),'fresh dyadic complete margin')
 result={'status':'PASS_INDEPENDENT_ACTUAL_PRINCIPAL_RANK87','source_sha256':SOURCE,'parent_sha256':PARENT,'word_sha256':sha(wb),'word_payload_sha256':sha(gzip.decompress(wb)),'all_input_columns':1880,'independently_reconstructed_operations':len(ops),'new_port':T,'early_S_contacts':ss,'hub_column_contacts':ks,'new_reverse_coefficients':12,'actual_reverse_rank':87,'explicit_kernel_basis':kernel,'unit87_minor_order':minor,'forward_rows_unchanged':True,'inherited_forward_residual_coefficients':4569,'full_bill':bill,'ordinary_increment':ordinary,'raw_increment':delta,'new_owned_packet_histogram':{1:1},'fresh_margin_lower':str(lo),'fresh_margin_upper':str(hi),'scope':'Finite current-source rank87 construction and full provisional invoice. No complete supplier or kappa.'}
 mutants={}
 def reject(name,m):
  try:
   mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True);need(mr==want and ml==parent_loc,'mutated full source state')
  except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
  else:raise ValueError('unrejected source mutant '+name)
 m=copy.deepcopy(w);m['program'][early[1]][3]=str(-F(m['program'][early[1]][3]));reject('wrong_initial_dual_shear_sign',m)
 m=copy.deepcopy(w);m['program'][early[0]][3]=src['final'][host[ss[0]][1]];reject('dual_skips_initial_acquisition_line',m)
 m=copy.deepcopy(w);m['program'][feedback[2]][4]=False;reject('owned_return_marked_public',m)
 m=copy.deepcopy(w);m['program'][feedback[3]][3]='0';reject('one_required_hub_entry_omitted',m)
 m=copy.deepcopy(w);m['program'][feedback[1]][3]='0';reject('return_packet_does_not_copy_authentic_d',m)
 m=copy.deepcopy(w);i=p['marks']['common_starts'];at=w['marks']['common_starts'];m['program'].insert(at,copy.deepcopy(p['program'][next(iter(oldroutes))]));m['marks']['common_starts']+=1;reject('spent_original_direct_route_reused',m)
 result['negative_controls']=mutants
 def rank(A):
  A=[row.copy() for row in A];k=0
  for j in range(len(A[0])):
   i=next((i for i in range(k,len(A)) if A[i][j]),None)
   if i is None:continue
   A[k],A[i]=A[i],A[k];c=A[k][j];A[k]=[v/c for v in A[k]]
   for i in range(k+1,len(A)):
    c=A[i][j]
    if c:A[i]=[u-c*v for u,v in zip(A[i],A[k])]
   k+=1
   if k==len(A):break
  return k
 m=copy.deepcopy(w)
 for event in early[1::2]:m['program'][event][3]='0'
 mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True)
 pure_column=[[F(i==j)+mr[raw[host[i][0]]].get(raw[host[j][1]],F(0)) for j in H] for i in H]
 need(rank(pure_column)==88,'actual otherwise valid eight-entry single-column word cannot lower rank')
 result['without_four_early_shears_actual_rank']=88
 frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def load_engine(filename):
  path=frozen/filename;need(sha(path.read_bytes())==pins[filename],'frozen physical engine pin');spec=importlib.util.spec_from_file_location('independent_principal_'+filename[:-3],path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
 c=load_engine('clifford_exact.py');v=load_engine('native_verify.py');prior={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};now={(e[2],e[3]) for e in ops if e[0]=='MOVE'};maps=[]
 for x,y in sorted(now-prior):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent actual principal map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'new exact rank');maps.append({'source':x,'target':y,'recipe':recipe})
 bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
 except ValueError:result['wrong_global_phase_rejected']=True
 else:raise ValueError('wrong global phase survived')
 result['new_map_count']=len(maps);result['engine_pins']=pins
 family_maps=[]
 for x,y in sorted(family_pairs-prior):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent family map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'exact alternative template map rank');family_maps.append({'source':x,'target':y,'recipe':recipe})
 result['alternative_one_port_template_count']=80;result['alternative_template_new_map_count']=len(family_maps)
 result['retained_parent_owned_caches_at_common_entry']=retained_owned;result['local_owned_peak_during_new_return']=len(retained_owned)+1
 result['alternative_template_scope']='80 alternative applications to the same rank88 parent, not serial reuse of consumed raw routes. Complete word artifact is t90 only.'
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'MAPS.json').write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n');(a.output/'FAMILY.json').write_text(json.dumps({'templates':family,'new_maps':family_maps},indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:result[k] for k in ['status','independently_reconstructed_operations','actual_reverse_rank','new_map_count','fresh_margin_lower','fresh_margin_upper']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
