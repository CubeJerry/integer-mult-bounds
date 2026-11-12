#!/usr/bin/env python3
"""Actual dependent-triple source code with one reverse residual mode removed.

The forward word is retained. This adds inverse-transpose coding on independent
hosted X2 carriers, with all Y2 readings at actual charts and full restoration.
It is a partial bidirectional code, not a completed shared native or new kappa.
"""
import argparse,sys,importlib.util,copy
from pathlib import Path

def main(a):
 sys.path.insert(0,str(a.reconstruction));from common import F,Counter,need,sha,load_inputs,source_data,SELECT,rank,inverse,mul,add,Emitter,ser,gzip,json,root
 import build as basebuild
 s,original,invoice=load_inputs(a.repo);selected=[0,1,98];from forward import build as make_forward
 p=make_forward(s,original,selected);forward_result=basebuild.verify(s,original,p,invoice);pb=gzip.compress(json.dumps(p,sort_keys=True,separators=(',',':')).encode(),mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'FORWARD.json.gz').write_bytes(pb);(a.output/'FORWARD-RESULT.json').write_text(json.dumps(forward_result,indent=2,sort_keys=True)+'\n')
 raw,W,Fc,classes,spaces=source_data(s,p,selected);hosted={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};groups=[g for g in p['facet_collection']['support_classes'] if g['donors']];need(all(x in hosted for x in selected),'independent selected Y2 bank')
 Hgroups=[(g,[d for d in g['donors'] if d in hosted]) for g in groups];need(len(groups)==3 and all(len(g['receivers'])==2 and len(g['donors'])==24 and rank([[W[y][d] for d in H] for y in g['receivers']])==2 for g,H in Hgroups),'three full-rank hosted pair groups');max_group=max(len(H) for g,H in Hgroups)
 affectedB={hosted[d][0] for g,H in Hgroups for d in H};affectedD={hosted[x][1] for x in selected};affected=affectedB|affectedD;oldmoves={}
 for r in affected:
  uses=[(t,e) for t,e in enumerate(p['program'][400:p['marks']['common_starts']],400) if e[1]==raw[r] or e[0] in ('ADD','COPY') and e[2]==raw[r]]
  need(len(uses)==1 and uses[0][1]==['MOVE',raw[r],s['initial'][r],s['final'][r],False],'affected raw carrier has exactly one unread direct prefix route');oldmoves[r]=uses[0][0]
 E=Emitter();meta=[];temps=list(range(1880+p['owned_fields'],1880+p['owned_fields']+max_group));allreverse={hosted[d][0]:{} for g,H in Hgroups for d in H};cutbegin=None;cutend=None
 def emit(o,parent=None):return E.emit(o,parent)
 def source_reroute(r,from_,to):
  E.mapping.setdefault(oldmoves[r],len(E.ops));return emit(['MOVE',raw[r],from_,to,False],oldmoves[r])
 def apply_dense(roles,M,C):
  n=len(roles);records=[]
  for i,r in enumerate(roles):emit(['INIT',temps[i],C]);records.append(emit(['ADD',temps[i],raw[r],'1',C]))
  for i,r in enumerate(roles):
   emit(['ADD',raw[r],temps[i],'-1',C])
   for j in range(n):
    if M[i][j]:emit(['ADD',raw[r],temps[j],str(M[i][j]),C])
  for i in range(n):emit(['CLEAR',temps[i],C])
  return records
 def position_sources():
  for x in selected:r=hosted[x][1];source_reroute(r,3,s['final'][r])
 def dual(g,H):
  from itertools import combinations
  C=g['chart'];ys=g['receivers'];n=len(H);m=len(ys);AH=[[W[y][d] for d in H] for y in ys];choices=[]
  for J in combinations(range(n),m):
   B=[[r[j] for j in J] for r in AH]
   if rank(B)==m:choices.append((sum(bool(x) for r in inverse(B) for x in r),J))
  need(choices,'full hosted row rank');J=list(min(choices)[1]);I=[H[j] for j in J];M=[[F(i==j) for j in range(n)] for i in range(n)]
  for i,j in enumerate(J):M[j]=AH[i].copy()
  Minv=inverse(M);Mt=[list(c) for c in zip(*M)];dualM=[list(c) for c in zip(*Minv)];unit=[[F(i==j) for j in range(n)] for i in range(n)];need(mul(Minv,M)==unit and mul(M,Minv)==unit,'actual inverse')
  roles=[hosted[d][0] for d in H];rec={'kind':'inverse_transpose','chart':C,'receivers':ys,'first_donors':H,'hosted_X2':roles,'pivot_first_donors':I,'pivot_positions':J,'primal_matrix':[[str(x) for x in r] for r in M],'dual_encoder':[[str(x) for x in r] for r in dualM],'dual_decoder':[[str(x) for x in r] for r in Mt],'begin':len(E.ops),'injections':[]}
  for r in roles:source_reroute(r,s['initial'][r],C)
  rec['encoder_snapshots']=apply_dense(roles,dualM,C);rec['encoded']=len(E.ops)
  for d in H:
   r=hosted[d][0]
   if d in I:
    y=ys[I.index(d)];q=hosted[y-112][1];source_reroute(r,C,Fc[y]);t=emit(['ADD',raw[r],raw[q],'-1',Fc[y]]);rec['injections'].append({'event':t,'receiver':y,'source_Y2':q,'carrier_X2':r});source_reroute(r,Fc[y],127)
   else:source_reroute(r,C,127)
  rec['at_hub']=len(E.ops);rec['decoder_snapshots']=apply_dense(roles,Mt,127);rec['end']=len(E.ops)
  for d in H:
   for y in ys:allreverse[hosted[d][0]][hosted[y-112][1]]=-W[y][d]
  meta.append(rec)
 skip=set(oldmoves.values());boundaries={}
 for t,o in enumerate(p['program']):
  if t==410:
   cutbegin=len(E.ops);position_sources()
   for g,H in Hgroups:dual(g,H)
   cutend=len(E.ops)
  boundaries[t]=len(E.ops)
  if t in skip:continue
  E.mapping[t]=len(E.ops);emit(copy.deepcopy(o),t)
 need(len(E.mapping)==len(p['program']),'every parent operation or route accounted')
 w=copy.deepcopy(p);w['parent_forward_collection_provenance']=w.pop('facet_collection');w.update(schema='moonshot-S008-dependent-triple-primal-dual-v1',program=E.ops,owned_fields=p['owned_fields']+max_group,parent_event_of_output=E.lineage,parent_word_sha256=sha(pb),marks={k:boundaries[v] for k,v in p['marks'].items()},native_event_to_physical=[E.mapping[v] for v in p['native_event_to_physical']],paired_reverse_corrections={str(r):ser(row) for r,row in sorted(allreverse.items())},paired_collection={'begin':cutbegin,'end':cutend,'temporaries':temps,'groups':meta,'old_routes_replaced':{str(r):e for r,e in sorted(oldmoves.items())},'owned_moves':0,'selected_first_receivers':selected})
 old,oldloc=basebuild.interpret_prefix(s,p);new,newloc=basebuild.interpret_prefix(s,w);need(oldloc==newloc and set(old)==set(new),'same prefix state and locations');q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 for j,row in old.items():
  want=row
  for b,coeff in allreverse.items():
   if j==raw[b]:
    for d,c in coeff.items():want=add(want,q[d],c)
  need(new[j]==want,'all1880 input rows differ only by exact transposed hosted correction')
 tail=w['program'][w['marks']['common_starts']:];need(tail==p['program'][p['marks']['common_starts']:],'literal common suffix unchanged')
 for b in affectedB:
  uses=[e for e in tail if e[1]==raw[b] or e[0] in ('ADD','COPY') and e[2]==raw[b]];need(uses==[['ADD',raw[b],b,'1',127]],'no changed reverse carrier feedback after common entry')
 for b,coeff in allreverse.items():
  row=new[raw[b]]
  for d,c in coeff.items():row=add(row,new[raw[d]],-c)
  need(row==q[b],'explicit hosted triangular inverse')
 roots={x:root(s['frames'][s['initial'][x]][0]) for x in selected};gram=[[sum(q*r for q,r in zip(roots[x],roots[y])) for y in selected] for x in selected];need(rank(gram)==2,'rank-two source triple Gram');X=s['hosted']['X2'];Y=s['hosted']['Y2'];iy={r:i for i,r in enumerate(Y)};response=[[F(0) for _ in Y] for _ in X]
 for i,x in enumerate(X):
  for y,c in allreverse.get(x,{}).items():response[i][iy[y]]=c
 residual=[[F(i==j)+response[i][j] for j in range(96)] for i in range(96)];need(rank(residual)==95,'actual full hosted residual rank95')
 from itertools import product
 relation=next(h for h in product([-1,1],repeat=3) if h[0]==1 and all(sum(h[j]*roots[selected[j]][k] for j in range(3))==0 for k in range(8)));kernel=[F(0) for _ in Y]
 for x,c in zip(selected,relation):kernel[iy[hosted[x][1]]]=F(c)
 need(all(sum(c*d for c,d in zip(row,kernel))==0 for row in residual),'explicit actual residual kernel direction')
 bill=basebuild.typed(s,w);oldbill=basebuild.typed(s,p);need(bill.pop('final_locations')==oldbill.pop('final_locations'),'identical final public charts');R=Counter(bill['raw_histogram']);Rold=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw);T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r in R.keys()|Rold.keys():P[r]+=18*(R[r]-Rold[r])
 P[9]+=18*8;lo,hi=basebuild.interval({r:T[r]-P[r] for r in T.keys()|P.keys()});need(all(n>=0 for n in P.values()),'complete nonnegative invoice')
 a.output.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();wb=gzip.compress(payload,mtime=0,compresslevel=9);(a.output/'WORD.json.gz').write_bytes(wb)
 result={'status':'PASS_ACTUAL_DEPENDENT_TRIPLE_WITH_REVERSE_RESIDUAL_RANK95','source_sha256':p['source_sha256'],'parent_word_sha256':sha(pb),'word_sha256':sha(wb),'word_payload_sha256':sha(payload),'independent_input_coordinates':1880,'forward_completed_receivers':p['newly_completed_firstY_receivers'],'forward_residual_coefficients':4841,'hosted_donors_changed':len(allreverse),'transposed_correction_coefficients':sum(map(len,allreverse.values())),'ordinary_reverse_complete_pairs':0,'reverse_target_rank':95,'reverse_kernel_dimension':1,'selected_first_X':selected,'source_Gram':gram,'source_Gram_rank':2,'reverse_input_kernel':{str(y):str(c) for y,c in zip(Y,kernel) if c},'coupled_reverse_corrections_supplied':0,'bill':bill,'increment_over_forward_triple':{k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()},'all104_first_donors_restored_before_E8':True,'all_common_fields_preserved_by_literal_suffix_composition':True,'hosted_inverse_rows':len(allreverse),'conditional_caller':{'T4':dict(sorted(T.items())),'P_partial':dict(sorted(P.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'remaining_moment_per_native_decimal':float(lo/18),'retained_paid_packets':{9:8}},'scope':'Coherent source-restricted paired partial code. Reverse additions are the transpose of the three dependent forward offdiagonal correction rows on hosted columns; no reverse diagonal is completed. Remaining global construction and all supplier/foundational obligations remain. No new kappa.'};(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','hosted_donors_changed','transposed_correction_coefficients','bill','conditional_caller']},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--reconstruction',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
