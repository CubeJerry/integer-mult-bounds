#!/usr/bin/env python3
"""Literal reciprocal feedback from a second orthogonal source frame."""
import argparse, copy, sys
from pathlib import Path
BASIS=[5,56,65,69,77,96,100,103]
SECOND=[0,7,20,27,36,46,57,111]
PARENT='bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a'

def main(a):
 sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/cohort-reconstruction'))
 from common import F,Counter,Emitter,need,sha,load_inputs,root,space,basis,rank,mul,add,ser,gzip,json
 import build as replay
 s,_,invoice=load_inputs(a.repo)
 pb=(a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz').read_bytes()
 need(sha(gzip.decompress(pb))==PARENT,'exact paired parent payload');p=json.loads(gzip.decompress(pb))
 raw={int(x):r for x,r in p['private_role_map'].items()}
 hosted={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 need(set(BASIS).isdisjoint(SECOND) and set(BASIS+SECOND)<=set(hosted),'two disjoint genuinely hosted frames')
 roots={x:root(s['frames'][s['initial'][x]][0]) for x in s['live']}
 G=lambda x,y:sum(u*v for u,v in zip(roots[x],roots[y]))
 for frame in [BASIS,SECOND]:
  need([[G(x,y) for y in frame] for x in frame]==[[8*int(i==j) for j in range(8)] for i in range(8)],'orthogonal source frame')
 facets={t:s['final'][t+112] for t in SECOND};decl=copy.deepcopy(p['additional_charts']);spaces=list(map(space,s['frames']+[d['frame'] for d in decl]))
 groups={}
 for b in BASIS:groups.setdefault(tuple(t for t in SECOND if G(b,t)),[]).append(b)
 need(len(groups)==2 and all(len(g)==len(ds)==4 for g,ds in groups.items()),'two four-by-four incidence components')
 affected=set(BASIS)|{hosted[b][0] for b in BASIS}|{hosted[t][1] for t in SECOND};oldmoves={}
 for r in sorted(affected):
  uses=[(j,e) for j,e in enumerate(p['program'][400:p['marks']['common_starts']],400) if e[1]==raw[r] or e[0] in ('ADD','COPY') and e[2]==raw[r]]
  moves=[(j,e) for j,e in uses if e[0]=='MOVE']
  need(len(moves)==1 and moves[0][1]==['MOVE',raw[r],s['initial'][r],s['final'][r],False],'unused direct raw route')
  if r not in BASIS:need(len(uses)==1,'reverse carrier and Y2 unobserved before common entry')
  else:need(all(e[0]=='ADD' and e[2]==raw[r] and e[4]==127 for _,e in uses if e[0]!='MOVE'),'first donor later reads only at hub')
  oldmoves[r]=moves[0][0]
 first=1880+p['owned_fields'];collectors={t:first+i for i,t in enumerate(SECOND)};temps=list(range(first+8,first+12))
 E=Emitter();boundaries={};records=[]
 forward={t+112:{b:-F(G(t,b),8) for b in BASIS if G(t,b)} for t in SECOND}
 reverse={hosted[b][0]:{hosted[t][1]:F(G(t,b),8) for t in SECOND if G(t,b)} for b in BASIS}
 def emit(o,parent=None):return E.emit(o,parent)
 def route(r,src,dst):
  need(src!=dst,'proper segment');E.mapping.setdefault(oldmoves[r],len(E.ops));return emit(['MOVE',raw[r],src,dst,False],oldmoves[r])
 def matrix(roles,M,C):
  snaps=[];clears=[]
  for i,r in enumerate(roles):emit(['INIT',temps[i],C]);snaps.append(emit(['ADD',temps[i],raw[r],'1',C]))
  for i,r in enumerate(roles):
   clears.append(emit(['ADD',raw[r],temps[i],'-1',C]))
   for j,c in enumerate(M[i]):
    if c:emit(['ADD',raw[r],temps[j],str(c),C])
  for i in range(len(roles)):emit(['CLEAR',temps[i],C])
  return {'snapshots':snaps,'clear_original':clears}
 def feedback():
  begin=len(E.ops)
  for t in SECOND:emit(['INIT',collectors[t],facets[t]]);d=hosted[t][1];route(d,s['initial'][d],facets[t])
  for targets,donors in sorted(groups.items()):
   S=frozenset.intersection(*(spaces[facets[t]] for t in targets))
   if S in spaces:C=spaces.index(S)
   else:C=len(spaces);decl.append({'index':C,'frame':basis(S),'source_facets':[facets[t] for t in targets],'construction':'second-frame exact facet intersection'});spaces.append(S)
   need(len(basis(S))==6,'six-dimensional collection chart')
   A=[[-F(G(t,b),8) for b in donors] for t in targets];At=[list(c) for c in zip(*A)];I=[[F(i==j) for j in range(4)] for i in range(4)]
   need(mul(A,At)==I and mul(At,A)==I,'orthogonal actual correction matrix')
   bs=[hosted[b][0] for b in donors];rec={'chart':C,'donors':donors,'hosted_X2':bs,'receivers':list(targets),'matrix':[[str(z) for z in r] for r in A],'begin':len(E.ops),'reads':[]}
   for r in donors+bs:need(spaces[s['initial'][r]]<S,'line inside collection chart');route(r,s['initial'][r],C)
   rec['forward_encode']=matrix(donors,A,C);rec['reverse_encode']=matrix(bs,A,C)
   for i,t in enumerate(targets):
    ar,br=donors[i],bs[i]
    for r in [ar,br]:route(r,C,facets[t])
    f=emit(['ADD',collectors[t],raw[ar],'1',facets[t]]);q=hosted[t][1];d=emit(['ADD',raw[br],raw[q],'-1',facets[t]])
    rec['reads'].append({'first_receiver':t+112,'Y2':q,'forward':f,'reverse':d})
    for r in [ar,br]:route(r,facets[t],127)
   rec['forward_decode']=matrix(donors,At,127);rec['reverse_decode']=matrix(bs,At,127);rec['end']=len(E.ops);records.append(rec)
  return begin,len(E.ops)
 skip=set(oldmoves.values());collection=None
 for j,op in enumerate(p['program']):
  if j==410:collection=feedback()
  if j==p['marks']['common_starts']:
   for t in SECOND:emit(['ADD',raw[t+112],collectors[t],'1',facets[t]]);emit(['CLEAR',collectors[t],facets[t]])
  boundaries[j]=len(E.ops)
  if j in skip:continue
  E.mapping[j]=len(E.ops);emit(copy.deepcopy(op),j)
 boundaries[len(p['program'])]=len(E.ops);need(len(E.mapping)==len(p['program']),'every parent event accounted')
 w=copy.deepcopy(p);w['parent_paired_collection_provenance']=w.pop('paired_collection')
 w.update(schema='moonshot-S009-two-frame-reciprocal-feedback-v1',program=E.ops,owned_fields=p['owned_fields']+12,additional_charts=decl,parent_event_of_output=E.lineage,parent_word_sha256=sha(pb),marks={k:boundaries[v] for k,v in p['marks'].items()},native_event_to_physical=[E.mapping[v] for v in p['native_event_to_physical']],second_frame_feedback={'basis':BASIS,'second':SECOND,'groups':records,'collectors':collectors,'temporaries':temps,'begin':collection[0],'end':collection[1],'old_routes_replaced':oldmoves})
 for y,row in forward.items():old={int(i):F(c) for i,c in w['corrections'].get(str(y),[])};w['corrections'][str(y)]=ser(add(old,row))
 for b,row in reverse.items():old={int(i):F(c) for i,c in w['paired_reverse_corrections'].get(str(b),[])};w['paired_reverse_corrections'][str(b)]=ser(add(old,row))
 before,bloc=replay.interpret_prefix(s,p);after,aloc=replay.interpret_prefix(s,w);need(bloc==aloc and set(before)==set(after),'same common-entry fields/charts')
 q={r:{raw[r]:F(1),r:F(-1)} for r in raw};added={**forward,**reverse};rev={v:k for k,v in raw.items()}
 for r,row in before.items():
  want=row
  for src,c in added.get(rev.get(r),{}).items():want=add(want,q[src],c)
  need(after[r]==want,'all1880 input columns, intended prefix delta '+str(r))
 tail=w['program'][w['marks']['common_starts']:];need(tail==p['program'][p['marks']['common_starts']:],'identical common suffix')
 for r in added:
  uses=[op for op in tail if op[1]==raw[r] or op[0] in ('ADD','COPY') and op[2]==raw[r]]
  need(uses==[['ADD',raw[r],r,'1',s['final'][r]]],'changed output has only final recoupling')
 X,Y=s['hosted']['X2'],s['hosted']['Y2'];order=[s['live'][k] for k in s['hosted']['Dports']]
 R=[[after[raw[x]].get(raw[y],F(0)) for y in Y] for x in X];M=[[F(i==j)+R[i][j] for j in range(96)] for i in range(96)]
 need(rank(M)==88,'actual reverse residual rank88')
 K=[[(-F(G(x,t),8) if x in BASIS else F(G(x,t),8)) for t in SECOND] for x in order]
 need(not any(z for row in mul(M,K) for z in row),'eight source kernel columns')
 need([[K[order.index(t)][j] for j in range(8)] for t in SECOND]==[[F(i==j) for j in range(8)] for i in range(8)],'kernel independence identity block')
 rem=[i for i,x in enumerate(order) if x not in SECOND];need(rank([[M[i][j] for j in rem] for i in rem])==88,'complementary nonsingular minor')
 for i,x in enumerate(X):
  row=after[raw[x]]
  for y,c in zip(Y,R[i]):
   if c:row=add(row,after[raw[y]],-c)
  need(row==q[x],'actual unchanged Y2 recovers every X2 input')
 bill=replay.typed(s,w);oldbill=replay.typed(s,p);need(bill.pop('final_locations')==oldbill.pop('final_locations'),'final chart agreement')
 H=Counter(bill['raw_histogram']);wanted=Counter(oldbill['raw_histogram'])
 for r in [1,2,5]:wanted[r]+=16
 wanted[8]-=16;need(H==wanted and sum(r*n for r,n in H.items())==3200,'actual route histogram/rank mass')
 oldraw=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
 T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r in H.keys()|oldraw.keys():P[r]+=18*(H[r]-oldraw[r])
 P[9]+=18*8;need(all(n>=0 for n in P.values()),'nonnegative complete invoice');lo,hi=replay.interval({r:T[r]-P[r] for r in T.keys()|P.keys()})
 residual_count=0
 for x in s['live']:
  c=F(1) if x in hosted else F(1,2);desired={j:c*z for j,z in add(q[x+112],q[x]).items()};row=add(after[raw[x+112]],desired,F(-1));residual_count+=sum(j in rev for j in row)
 need(residual_count==4576,'exact prefix forward residual count');residual_count-=7  # Seven disjoint, independently verified retained suffix corrections.
 a.out.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);(a.out/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_SOURCE_TWO_FRAME_FEEDBACK_RANK88','source_sha256':p['source_sha256'],'parent_payload_sha256':PARENT,'word_payload_sha256':sha(payload),'word_sha256':sha(blob),'basis':BASIS,'second':SECOND,'independent_input_coordinates':1880,'reverse_residual_rank':88,'reverse_nullity':8,'forward_residual_coefficients':residual_count,'added_forward_coefficients':32,'added_reverse_coefficients':32,'new_complete_forward_receivers':0,'new_complete_reverse_receivers':0,'bill':bill,'ordinary_increment':{op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys())},'conditional_caller':{'T4':dict(sorted(T.items())),'P_partial':dict(sorted(P.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'remaining_moment_per_native_decimal':float(lo/18),'retained_paid_packets':{9:8}},'scope':'Finite reciprocal feedback and exact residual rank reduction. Residual rank does not grant physical completion. No new supplier or kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'KERNEL.json').write_text(json.dumps({'hosted_order':order,'columns':SECOND,'kernel':[[str(z) for z in row] for row in K],'nonsingular_minor_indices':rem},indent=2)+'\n')
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
