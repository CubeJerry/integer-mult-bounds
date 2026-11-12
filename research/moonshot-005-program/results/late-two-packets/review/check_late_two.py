#!/usr/bin/env python3
"""Independent Q9 reconstruction, sparse source replay, and full late-packet bill.
No author constructor, author audit, or cohort-reconstruction helper is imported.
"""
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
PAYLOAD='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
WORD='64582bf3eb558f46bcefb62990114487cf313094b4b0609d240d92cf2ee2aeab'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
NORMALS=[7,25,52,76,97,127,42,82]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(a):
 s={0}
 for x in a:s|={y^x for y in tuple(s)}
 return frozenset(s)
def rowplus(a,b,c=F(1)):
 r=a.copy()
 for k,v in b.items():
  q=r.get(k,F(0))+c*v
  if q:r[k]=q
  else:r.pop(k,None)
 return r
def root9(v):
 T=[i for i in range(9) if v>>i&1]
 if len(T)==3:return [2 if i in T else -1 for i in range(9)]
 need(len(T)==7,'source root type');i,j=[k for k in range(9) if k not in T]
 return [3*(int(k==i)-int(k==j)) for k in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def replay(w,spaces,stop=None,arithmetic=False):
 loc=dict(enumerate(w['initial']));rows={i:{i:F(1)} for i in range(1880)} if arithmetic else None
 count=Counter();ranks=Counter();rawranks=Counter();raw=set(w['private_role_map'].values());peak=0;lifetimes=0
 for k,e in enumerate(w['program'][:stop] if stop is not None else w['program']):
  op,r=e[:2];count[op]+=1;need(0<=r<1880+w['owned_fields'],'declared role')
  if op=='INIT':
   need(r>=1880 and r not in loc,'fresh owner');loc[r]=e[2];lifetimes+=1
   if arithmetic:rows[r]={}
  elif op=='CLEAR':
   need(r>=1880 and loc.get(r)==e[2],'owned retirement');del loc[r]
   if arithmetic:del rows[r]
  elif op=='MOVE':
   x,y,o=e[2:];need(type(o)is bool and o==(r>=1880) and loc.get(r)==x,'typed route at '+str(k));need(spaces[x]<spaces[y] or o and spaces[y]<spaces[x],'proper nested route at '+str(k))
   dim=abs((len(spaces[x]).bit_length()-1)-(len(spaces[y]).bit_length()-1));ranks[dim]+=1;rawranks[dim]+=int(r in raw);loc[r]=y
  elif op=='SCALE':
   c=F(e[2]);need(c and loc.get(r)==e[3],'nonzero local scale')
   if arithmetic:rows[r]={j:c*v for j,v in rows[r].items()}
  elif op in ('ADD','COPY'):
   z,c,at=e[2:];need(z!=r and loc.get(z)==loc.get(r)==at,'cochart read at '+str(k))
   if arithmetic:
    need(op!='COPY' or not rows[r],'COPY zero guard');rows[r]=rowplus(rows[r],rows[z],F(c))
  else:raise ValueError(op)
  peak=max(peak,len(loc)-1880)
 return rows,loc,{'instructions':sum(count.values()),'opcode_counts':dict(sorted(count.items())),'move_rank_histogram':dict(sorted(ranks.items())),'raw_histogram':dict(sorted((r,n) for r,n in rawranks.items() if n)),'owned_lifetimes':lifetimes,'peak_owned':peak,'final_owned':len(loc)-1880}
def exact_bounds(rank,precision=112):
 den=1<<precision;target=rank**199*den**200;lo=0;hi=rank*den+1
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'exact dyadic price bracket')
 return F(lo,den),F(lo if lo**200==target else lo+1,den)
def interval(coeff):
 lo=hi=F(0)
 for r,c in coeff.items():
  l,h=exact_bounds(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 return lo,hi

def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
 pb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes()
 wb=a.word.read_bytes();need(sha(sb)==SOURCE and sha(pb)==PARENT and sha(gzip.decompress(pb))==PAYLOAD and sha(wb)==WORD,'frozen source and parent/word pins')
 s,p,w=[json.loads(gzip.decompress(b)) for b in (sb,pb,wb)];author=json.loads((a.word.parent/'RESULT.json').read_text())
 raw={int(k):v for k,v in p['private_role_map'].items()};xs=s['live'];hosted={xs[i] for i in s['hosted']['Dports']};coupled=set(xs)-hosted
 need(w['private_role_map']==p['private_role_map'] and w['initial']==p['initial'] and w['owned_fields']==p['owned_fields'],'same initial inputs and declared storage')
 frames=s['frames']+[d['frame'] for d in w['additional_charts']];spaces=list(map(span,frames))
 need(w['additional_charts'][:len(p['additional_charts'])]==p['additional_charts'],'unchanged earlier charts')
 need(all(len(S)==2**len(frames[i]) for i,S in enumerate(spaces)),'independent frame declarations')
 normals={x:s['frames'][s['initial'][x]][0] for x in xs};roots={x:root9(normals[x]) for x in xs};omitted=list(map(root9,NORMALS))
 need(not(set(NORMALS)&set(normals.values())),'all eight frame roots omitted')
 need(all(dot(omitted[i],omitted[j])==18*(i==j) for i in range(8) for j in range(8)),'Q9 omitted orthogonal frame')
 U=[[F(dot(r,roots[x]),18) for x in xs] for r in omitted]
 need(all(sum(bool(c) for c in row)==52 and all(not c or abs(c)==F(1,2) for c in row) for row in U),'eight52-term half-valued rows')
 need(all(sum(U[k][i]*U[k][j] for k in range(8))==F(dot(roots[x],roots[y]),18) for i,x in enumerate(xs) for j,y in enumerate(xs)),'full104-square Gram identity')
 support=[{x for x,c in zip(xs,row) if c} for row in U];s1,s2=support[6:];both=s1&s2
 need([len(s1),len(s2),len(both)]==[52,52,24],'actual late supports')
 c1=spaces.index(span([42]));c2=spaces.index(span([82]));c12=spaces.index(span([42,82]));need([c1,c2,c12]==[1111,597,1112],'actual declared late charts')
 need(all((normals[x]&z).bit_count()%2==0 for z,sup in [(42,s1),(82,s2)] for x in sup),'binary incidence of all late recipients')

 # Discover and authenticate the old packet macro from actual events.
 descents=[(i,e) for i,e in enumerate(p['program'][:p['marks']['initial_decoders']]) if e[0]=='MOVE' and e[2:]==[127,3,True]]
 need(len(descents)==8 and len({e[1] for i,e in descents})==1,'eight original downward packet lifetimes')
 packet=descents[0][1][1];begin=max(i for i,e in enumerate(p['program'][:descents[0][0]]) if e==['INIT',packet,127]);end=p['marks']['initial_decoders']
 need(p['program'][end-1]==['CLEAR',packet,3],'actual old packet macro end')
 earlyend=next(i for i in range(end,p['marks']['common_starts']) if p['program'][i][0]=='MOVE');early=list(range(end,earlyend))
 need(len(early)==164,'exact164 commuting additions')
 rawY={raw[x+112] for x in xs}
 need(all(p['program'][i][0]=='ADD' and p['program'][i][1] in rawY and p['program'][i][2]<1480 and p['program'][i][4]==3 for i in early),'authentic common-input hoists')
 before,bl,_=replay(p,spaces,begin,True);after_old,al,_=replay(p,spaces,end,True)
 need(all(before[raw[x]]=={raw[x]:F(1),x:F(-1)} and bl[raw[x]]==127 for x in xs),'all104 authentic original donors at actual packet entrance')
 need(all(before[e[2]]==after_old[e[2]] and bl[e[2]]==al[e[2]]==3 for e in (p['program'][i] for i in early)),'hoisted source rows unmodified by packet macro')
 oldroutes={};stop_records=[]
 for x in sorted(s1|s2):
  routes=[(i,e) for i,e in enumerate(p['program'][:p['marks']['common_starts']]) if e[0]=='MOVE' and e[1]==raw[x+112]]
  need(len(routes)==1,'one actual initial receiver ascent');i,e=routes[0];need(e[2]==3 and e[4] is False,'authentic initial empty receiver path')
  current=c12 if x in both else c1 if x in s1 else c2
  need(spaces[current]<spaces[e[3]],'late stop inside actual intermediate receiver stop')
  uses=[j for j,f in enumerate(p['program'][end:i],end) if f[1]==raw[x+112] or f[0] in ('ADD','COPY') and f[2]==raw[x+112]]
  need(all(j in early for j in uses),'no skipped current receiver observation')
  oldroutes[i]=(x,current,e[3]);stop_records.append({'receiver':x,'original_event':i,'actual_stop':e[3],'late_stop':current,'final_facet':s['final'][x+112]})

 # Independently reconstruct every operation; do not trust macro metadata.
 ops=[];lineage=[];new_packets=[];delivery_events=[];hoist_start=None;new_begin=None;new_end=None
 def emit(e,parent=None):
  ops.append(e);lineage.append(parent);return len(ops)-1
 def rawmove(x,start,target):
  old=next(i for i,(y,current,end0) in oldroutes.items() if y==x)
  emit(['MOVE',raw[x+112],start,target,False],old)
 def form(k):
  emit(['INIT',packet,127])
  for x,c in zip(xs,U[k]):
   if c:emit(['ADD',packet,raw[x],str(c),127])
 def deliver(k,subset,at):
  for x,c in zip(xs,U[k]):
   if x in subset:
    event=emit(['ADD',raw[x+112],packet,str(c*(F(1) if x in hosted else F(1,2))),at]);delivery_events.append((k,x,event))
 def replace():
  nonlocal hoist_start,new_begin,new_end
  hoist_start=len(ops)
  for i in early:emit(copy.deepcopy(p['program'][i]),i)
  new_begin=len(ops)
  for k in range(6):
   start=len(ops);form(k);emit(['MOVE',packet,127,3,True]);deliver(k,support[k],3);emit(['CLEAR',packet,3]);new_packets.append((start,len(ops)))
  for x in sorted(s1):rawmove(x,3,c1)
  start=len(ops);form(6);emit(['MOVE',packet,127,c1,True]);deliver(6,s1,c1);emit(['CLEAR',packet,c1]);new_packets.append((start,len(ops)))
  for x in sorted(both):rawmove(x,c1,c12)
  for x in sorted(s2-s1):rawmove(x,3,c2)
  start=len(ops);form(7);emit(['MOVE',packet,127,c12,True]);deliver(7,both,c12);emit(['MOVE',packet,c12,c2,True]);deliver(7,s2-s1,c2);emit(['CLEAR',packet,c2]);new_packets.append((start,len(ops)));new_end=len(ops)
 for i,e in enumerate(p['program']):
  if i==begin:replace()
  if begin<=i<end or i in early:continue
  if i in oldroutes:
   x,current,target=oldroutes[i];rawmove(x,current,target)
  else:emit(copy.deepcopy(e),i)
 need(ops==w['program'],'literal full78020 independently reconstructed operations')
 need(lineage==w['parent_event_of_output'],'literal independently reconstructed provenance')
 occ=defaultdict(list)
 for j,i in enumerate(lineage):
  if i is not None:occ[i].append(j)
 need(w['native_event_to_physical']==[occ[i][0] for i in p['native_event_to_physical']],'every native event preserved')
 for name,i in p['marks'].items():need(w['marks'][name]==occ[i][0],'actual retained boundary '+name)
 expected,eloc,_=replay(p,spaces,p['marks']['common_starts'],True);actual,aloc,_=replay(w,spaces,w['marks']['common_starts'],True)
 need(actual==expected and aloc==eloc,'every1880-input current row and chart identical')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'literal unchanged complete common suffix')
 _,final,bill=replay(w,spaces);_,oldfinal,oldbill=replay(p,spaces);need(final==oldfinal and set(final)==set(range(1880)),'complete identical endpoints and all owned retirement')
 need(json.loads(json.dumps(bill))==author['bill'],'independently tallied full bill')
 delta=Counter(bill['raw_histogram']);delta.subtract(oldbill['raw_histogram']);delta={r:n for r,n in delta.items() if n}
 need(delta=={1:104,5:2,6:24,7:50,8:-76},'full raw route delta')
 need(sum(r*n for r,n in bill['raw_histogram'].items())==3200,'exact raw rankmass3200')
 ordinary={op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(set(bill['opcode_counts'])|set(oldbill['opcode_counts']))}
 need(ordinary=={'ADD':-208,'CLEAR':0,'COPY':0,'INIT':0,'MOVE':105,'SCALE':0},'complete ordinary increment')
 own=Counter(abs(len(frames[e[3]])-len(frames[e[2]])) for e in ops[new_begin:new_end] if e[0]=='MOVE' and e[1]==packet)
 need(own=={1:1,7:1,8:1,9:6},'actual owned packet tariff')
 ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(ib)==INVOICE,'H4 invoice pin');invoice=json.loads(ib)
 originalraw=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
 T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r in set(bill['raw_histogram'])|set(originalraw):P[r]+=18*(bill['raw_histogram'].get(r,0)-originalraw[r])
 for r,n in own.items():P[r]+=18*n
 need({str(r):n for r,n in P.items()}==author['conditional_caller']['P_partial'],'complete recomputed caller paid histogram')
 lo,hi=interval({r:T[r]-P[r] for r in T.keys()|P.keys()});lo/=18;hi/=18
 claimed=author['conditional_caller'];need(F(claimed['remaining_moment_per_native_lower'])<=lo<=hi<=F(claimed['remaining_moment_per_native_upper']),'fresh dyadic full margin refines author interval')
 savings={9:2,8:75,7:-51,6:-24,5:-2,1:-105};sl,sh=interval(savings)
 need(sl>0 and F(claimed['saving_per_native_lower'])<=sl<=sh<=F(claimed['saving_per_native_upper']),'fresh exact positive saving interval')
 result={'status':'PASS_INDEPENDENT_ACTUAL_TWO_LATE_PACKET_SOURCE','source_sha256':SOURCE,'parent_sha256':PARENT,'word_sha256':sha(wb),'word_payload_sha256':sha(gzip.decompress(wb)),'all_input_columns':1880,'independently_reconstructed_instructions':len(ops),'basis_normals':NORMALS,'late_support_sizes':[len(s1),len(s2),len(both)],'hoisted_common_ADDs':len(early),'raw_paths_refined':len(oldroutes),'full_bill':bill,'ordinary_increment':ordinary,'paid_packet_histogram':dict(sorted(own.items())),'raw_rankmass':3200,'inherited_reverse_rank':88,'inherited_final_forward_residual':4569,'fresh_full_margin_lower':str(lo),'fresh_full_margin_upper':str(hi),'fresh_saving_lower':str(sl),'fresh_saving_upper':str(sh),'actual_stop_records':stop_records,'scope':'Independent exact finite source, tariff, and map review; no new complete supplier or kappa.'}
 mutants={}
 def reject(name,m):
  try:
   mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True);need(mr==expected and ml==eloc,'mutated exact current state')
  except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
  else:raise ValueError('unrejected mutation '+name)
 ce=next(i for k,x,i in delivery_events if x in coupled);m=copy.deepcopy(w);m['program'][ce][3]=str(2*F(m['program'][ce][3]));reject('coupled_half_factor_removed',m)
 event=next(i for i,e in enumerate(ops) if e==['MOVE',packet,127,c1,True]);m=copy.deepcopy(w);m['program'][event][3]=c2;reject('penultimate_packet_wrong_line',m)
 event=next(i for i,e in enumerate(ops) if e==['MOVE',packet,c12,c2,True]);m=copy.deepcopy(w);m['program'][event][4]=False;reject('last_owned_downstep_marked_public',m)
 event=next(i for i in range(hoist_start,new_begin) if ops[i][1] in {raw[x+112] for x in s1|s2});m=copy.deepcopy(w);e=m['program'].pop(event);m['program'].insert(new_end-1,e);reject('required_empty_chart_read_not_hoisted',m)
 event=next(i for k,x,i in delivery_events if k==7 and x in both);m=copy.deepcopy(w);m['program'][event][3]=str(-F(m['program'][event][3]));reject('shared_late_delivery_wrong_sign',m)
 event=next(i for i,e in enumerate(ops) if e==['MOVE',raw[32+112],c12,911,False]);m=copy.deepcopy(w);m['program'][event][3]=s['final'][32+112];reject('actual_intermediate_stop_replaced_by_final_facet',m)
 result['negative_controls']=mutants
 failed7=[]
 for x in support[0]:
  asc=[e for e in p['program'][:p['marks']['common_starts']] if e[0]=='MOVE' and e[1]==raw[x+112] and e[2]==3]
  need(len(asc)==1,'single old receiver ascent for omitted-root control')
  if 7 not in spaces[asc[0][3]]:
   need(7 in spaces[s['final'][x+112]],'final-facet containment passes the rejected control');failed7.append({'receiver':x,'actual_stop':asc[0][3],'final_facet':s['final'][x+112]})
 need(failed7,'omitted root7 is not automatically a legal late packet');result['final_facet_only_false_positives_for_root7']=failed7
 frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def load_engine(filename):
  path=frozen/filename;need(sha(path.read_bytes())==pins[filename],'pinned physical map engine');spec=importlib.util.spec_from_file_location('independent_late2_'+filename[:-3],path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
 c=load_engine('clifford_exact.py');v=load_engine('native_verify.py');prior={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};now={(e[2],e[3]) for e in ops if e[0]=='MOVE'};maps=[]
 for x,y in sorted(now-prior):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent actual late map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'exact introduced rank');maps.append({'source':x,'target':y,'recipe':recipe})
 need(len(maps)==82,'82 introduced distinct chart pairs')
 bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
 except ValueError:result['wrong_global_phase_rejected']=True
 else:raise ValueError('wrong global phase survived')
 result['map_count']=len(maps);result['engine_pins']=pins
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'MAPS.json').write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:result[k] for k in ['status','independently_reconstructed_instructions','map_count','fresh_full_margin_lower','fresh_full_margin_upper','fresh_saving_lower','fresh_saving_upper']},indent=2))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
