#!/usr/bin/env python3
"""One actual paired quotient departure before a six-dimensional B cohort."""
import argparse,copy,gzip,json,sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'review-star'))
from engine import Q,need,sha,load,space,add,root9,rank,interpret,interval
PARENT='54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a'
J=[78,83,85,90];EXIT=90;TARGET=0

def inverse(A):
 n=len(A);B=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  p=next((i for i in range(j,n) if B[i][j]),None);need(p is not None,'invertible block');B[j],B[p]=B[p],B[j];v=B[j][j];B[j]=[x/v for x in B[j]]
  for i in range(n):
   if i!=j:v=B[i][j];B[i]=[x-v*y for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B]
def mm(A,B):return [[sum((x*y for x,y in zip(r,c)),Q(0)) for c in zip(*B)] for r in A]
def bas(S):
 B=[];T={0}
 for v in sorted(S):
  if v not in T:B.append(v);T|={x^v for x in tuple(T)}
 need(T==set(S),'binary basis');return B

def main(a):
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.combined/'WORD.json.gz';rp=a.combined/'RESULT.json';sb,pb=sp.read_bytes(),pp.read_bytes();need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(pb)==PARENT,'combined parent pin');s,p,prior=load(sp),load(pp),load(rp);raw={int(x):r for x,r in p['private_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};need(set(J+[TARGET])<=set(host),'genuine hosted fields')
 B=p['parent_second_frame_feedback_provenance']['basis'];S=p['parent_second_frame_feedback_provenance']['second'];need(EXIT not in B+S and TARGET in S,'rank-preserving support')
 roots={x:root9(s['frames'][s['initial'][x]][0]) for x in s['live']};gram=lambda x,y:sum(v*z for v,z in zip(roots[x],roots[y]))/2;c=gram(TARGET,EXIT);need(c in (Q(-1,2),Q(1,2)),'actual correction coefficient')
 pg=p['parent_cohort_collection_provenance']['groups'][2];C=pg['chart'];dg=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==C);need(EXIT in pg['nonpivots'] and EXIT not in dg['pivot_first_donors'],'exit nonpivot in both retained blocks')
 A=[[Q(v) for v in row] for row in pg['matrix']];pos={d:i for i,d in enumerate(pg['donors'])};remain=[j for j in J if j!=EXIT];AJ=[[row[pos[j]] for j in remain] for row in A];bj=[[row[pos[EXIT]]] for row in A];pick=next(I for I in itertools.combinations(range(4),3) if rank([AJ[i] for i in I])==3);gvec=mm(inverse([AJ[i] for i in pick]),[bj[i] for i in pick]);gamma={j:gvec[i][0] for i,j in enumerate(remain)};need(mm(AJ,gvec)==bj and gamma=={78:Q(-1),83:Q(1),85:Q(1)},'exact dependent column')
 frames=s['frames']+[d['frame'] for d in p['additional_charts']];spaces=list(map(space,frames));L={0}
 for j in J:v=s['frames'][s['initial'][j]][0];L|={x^v for x in tuple(L)}
 L=frozenset(L);F=s['final'][TARGET+112];need(len(L)==8 and L<spaces[C] and L<spaces[F],'dimension3 lower cochart');decl=copy.deepcopy(p['additional_charts'])
 if L in spaces:D=spaces.index(L)
 else:D=len(spaces);decl.append({'index':D,'frame':bas(L),'construction':'exact span of four hosted donor lines','source_donors':J});spaces.append(L);frames.append(bas(L))
 ep=a.repo/'research/moonshot-005-program/results/cohort-reconstruction/eight/WORD.json.gz';dp=a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz';ew,dw=load(ep),load(dp);needleP=ew['program'][pg['begin']:pg['end']];needleD=dw['program'][dg['begin']:dg['end']]
 def locate(block):
  starts=[i for i,o in enumerate(p['program']) if o==block[0] and p['program'][i:i+len(block)]==block];need(len(starts)==1,'unique frozen literal block');return starts[0],starts[0]+len(block)
 ps,pe=locate(needleP);ds,de=locate(needleD);need(ds<de<ps<pe<p['marks']['common_starts'],'causal dual then primal order')
 at=copy.deepcopy(p);at['marks']['common_starts']=ds;entry,loc=interpret(s,at);q={x:{r:Q(1),x:Q(-1)} for x,r in raw.items()}
 for j in J:
  for r in [j,host[j][0]]:need(entry[raw[r]]==q[r] and loc[raw[r]]==s['initial'][r],'actual unread current source')
 dS=host[TARGET][1];collector=int(p['parent_second_frame_feedback_provenance']['collectors'][str(TARGET)]);need(entry[raw[dS]]==q[dS] and loc[raw[dS]]==F and collector in entry and loc[collector]==F,'authentic arrived receiver and collector')
 pre=[]
 for j in J:
  for r in [j,host[j][0]]:pre.append(['MOVE',raw[r],s['initial'][r],D,False])
 for j,g in gamma.items():pre.append(['ADD',raw[j],raw[EXIT],str(g),D])
 for j,g in gamma.items():pre.append(['ADD',raw[host[EXIT][0]],raw[host[j][0]],str(-g),D])
 pre += [['MOVE',raw[EXIT],D,F,False],['ADD',collector,raw[EXIT],str(-c),F],['MOVE',raw[EXIT],F,127,False],['MOVE',raw[host[EXIT][0]],D,F,False],['ADD',raw[host[EXIT][0]],raw[dS],str(c),F],['MOVE',raw[host[EXIT][0]],F,127,False]]
 # Rebuild only the restricted six-carrier dual block with its actual inverse.
 hs=dg['first_donors'];keep=[i for i,j in enumerate(hs) if j!=EXIT];M0=[[Q(v) for v in row] for row in dg['primal_matrix']];M=[[M0[i][j] for j in keep] for i in keep];N=inverse(M);need(mm(M,N)==[[Q(i==j) for j in range(len(M))] for i in range(len(M))],'restricted inverse');hs=[hs[i] for i in keep];roles=[host[j][0] for j in hs];dual=[];temps=p['parent_paired_collection_provenance']['temporaries'][:len(hs)]
 def dense(out,rs,M,chart):
  for i,r in enumerate(rs):out += [['INIT',temps[i],chart],['ADD',temps[i],raw[r],'1',chart]]
  for i,r in enumerate(rs):
   out.append(['ADD',raw[r],temps[i],'-1',chart])
   for j,x in enumerate(M[i]):
    if x:out.append(['ADD',raw[r],temps[j],str(x),chart])
  for temp in temps:out.append(['CLEAR',temp,chart])
 for j,r in zip(hs,roles):dual.append(['MOVE',raw[r],D if j in remain else s['initial'][r],C,False])
 dense(dual,roles,[list(z) for z in zip(*N)],C)
 piv=dg['pivot_first_donors'];ys=dg['receivers']
 for j,r in zip(hs,roles):
  if j in piv:
   y=ys[piv.index(j)];f=s['final'][y];dy=host[y-112][1];dual += [['MOVE',raw[r],C,f,False],['ADD',raw[r],raw[dy],'-1',f],['MOVE',raw[r],f,127,False]]
  else:dual.append(['MOVE',raw[r],C,127,False])
 dense(dual,roles,[list(z) for z in zip(*M)],127)
 for j,g in gamma.items():dual.append(['ADD',raw[host[EXIT][0]],raw[host[j][0]],str(g),127])
 # The primal pivot minor is unchanged. Remove exited nonpivot acquisition/
 # recovery, account for the three genuine lower-chart arrivals, then invert N.
 primal=[];removed=[];retargeted=[]
 for k,o in enumerate(needleP):
  if o[1]==raw[EXIT] or o[0] in ('ADD','COPY') and o[2]==raw[EXIT]:removed.append(o);continue
  z=copy.deepcopy(o)
  if z[0]=='MOVE' and z[1] in {raw[j] for j in remain} and z[3]==C and z[2]!=C:z[2]=D;retargeted.append(k)
  primal.append(z)
 need(len(removed)==10 and len(retargeted)==3,'exact nonpivot removal and current location changes')
 for j,g in gamma.items():primal.append(['ADD',raw[j],raw[EXIT],str(-g),127])
 need(not any(ds<i<de or ps<i<pe for i in p['marks'].values()),'no live global mark inside replaced blocks');need(not any(ds<=i<de or ps<=i<pe for i in p['native_event_to_physical']),'no native operation removed')
 ops=[];lineage=[];bound={};newblocks={};i=0
 while i<len(p['program']):
  if i in (ds,ps):
   end=de if i==ds else pe;replacement=pre+dual if i==ds else primal;start=len(ops);newblocks['dual' if i==ds else 'primal']=[start,start+len(replacement)];ops+=replacement;lineage += [None]*len(replacement)
   for oldi in range(i,end):bound[oldi]=start
   i=end;continue
  bound[i]=len(ops);ops.append(copy.deepcopy(p['program'][i]));lineage.append(i);i+=1
 bound[len(p['program'])]=len(ops)
 w=copy.deepcopy(p);w.update(schema='moonshot-S009-lower-chart-paired-quotient-departure-v1',program=ops,additional_charts=decl,parent_word_sha256=PARENT,parent_event_of_output=lineage,marks={k:bound[v] for k,v in p['marks'].items()},native_event_to_physical=[bound[v] for v in p['native_event_to_physical']],quotient_departure={'donors':J,'exit':EXIT,'receiver':TARGET,'cohort_chart':C,'lower_chart':D,'gamma':{str(j):str(g) for j,g in gamma.items()},'coefficient':str(c),'old_primal_block':[ps,pe],'old_dual_block':[ds,de],'new_blocks':newblocks,'stationary_receiver_collector':collector,'actual_dual_input':dS,'retained_source_routes_reused_once':True})
 for y,donor,coef,key in [(TARGET+112,EXIT,-c,'corrections'),(host[EXIT][0],dS,c,'paired_reverse_corrections')]:
  row={int(j):Q(v) for j,v in w[key].get(str(y),[])};row[donor]=row.get(donor,Q(0))+coef;w[key][str(y)]=[[j,str(v)] for j,v in sorted(row.items()) if v]
 before,bl=interpret(s,p);after,al=interpret(s,w);need(bl==al and set(before)==set(after),'same complete prefix interface');expected={raw[TARGET+112]:add({},q[EXIT],-c),raw[host[EXIT][0]]:add({},q[dS],c)}
 need(all(after[r]==add(row,expected.get(r,{})) for r,row in before.items()),'all1880 input coefficients: only intended two changes')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'same literal common suffix')
 for z in [TARGET+112,host[EXIT][0]]:
  uses=[o for o in w['program'][w['marks']['common_starts']:] if o[1]==raw[z] or o[0] in ('ADD','COPY') and o[2]==raw[z]];need(uses==[['ADD',raw[z],z,'1',s['final'][z]]],'no later feedback')
 need(add(after[raw[TARGET+112]],after[raw[EXIT]],c)==before[raw[TARGET+112]],'actual forward inverse');need(add(after[raw[host[EXIT][0]]],after[raw[dS]],-c)==before[raw[host[EXIT][0]]],'actual reverse inverse')
 order=list(host);R=[[Q(x==y)+after[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order] for x in order];need(rank(R)==88,'full actual reverse rank88 preserved')
 bill,final=interpret(s,w,True);oldbill,oldfinal=interpret(s,p,True);need(final==oldfinal,'all final physical charts');delta={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};dr={r:bill['raw_histogram'].get(r,0)-oldbill['raw_histogram'].get(r,0) for r in bill['raw_histogram'].keys()|oldbill['raw_histogram'].keys()};need(sum(r*n for r,n in bill['raw_histogram'].items())==3200,'raw rank mass preserved')
 need(sum(bill['move_rank_histogram'].values())-sum(oldbill['move_rank_histogram'].values())==sum(dr.values()),'no newly paid owned movement')
 PP={int(k):v for k,v in prior['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in prior['conditional_caller']['T4'].items()}
 for r,n in dr.items():PP[r]=PP.get(r,0)+18*n
 lo,hi=interval({k:T.get(k,0)-PP.get(k,0) for k in T.keys()|PP.keys()});lo/=18;hi/=18;need(lo>0,'complete target moment remains positive')
 # Exact original-basis residual count; the newly cancelled coefficient is
 # on noncoupled donor90, so both counts decrease by one.
 changed=prior['forward_residual_count_in_preconditioned_basis']-1;original=prior['forward_residual_count_in_original_difference_basis']-1
 need(c!=0 and any(j==EXIT and Q(v)==-c for j,v in w['corrections'][str(TARGET+112)]),'actual newly cancelled Gram coefficient')
 # Perturbing a required precondition sign must be rejected by full source identity.
 bad=copy.deepcopy(w);k=newblocks['dual'][0]+8;need(bad['program'][k][0]=='ADD','mutant precondition address');bad['program'][k][3]=str(-Q(bad['program'][k][3]));badrows,_=interpret(s,bad);need(any(badrows[r]!=after[r] for r in after),'wrong absorption coefficient rejected')
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_ACTUAL_PAIRED_QUOTIENT_DEPARTURE','source_sha256':sha(sb),'parent_word_sha256':PARENT,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'exact_input_columns':1880,'lower_chart':D,'lower_chart_dimension':3,'cohort_chart':C,'donors':J,'exit':EXIT,'receiver':TARGET,'gamma':{str(j):str(g) for j,g in gamma.items()},'new_coefficient':str(c),'only_changed_raw_outputs':[TARGET+112,host[EXIT][0]],'retained_forward_completions':p['newly_completed_firstY_receivers'],'coupled_reverse_complete':p['coupled_precondition']['source_roles'],'hosted_reverse_residual_rank':88,'forward_residual_count_in_preconditioned_basis':changed,'forward_residual_count_in_original_difference_basis':original,'bill':bill,'ordinary_increment':delta,'raw_move_histogram_increment':dr,'new_owned_moves':0,'conditional_caller':{'T4':T,'P_partial':PP,'paid_positions':sum(PP.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-PP.get(k,0)) for k in T.keys()|PP.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'all_eight_rank9_and_eight_rank1_packets_retained':True},'negative_controls':{'wrong_absorption_coefficient_changes_exact_source_rows':True},'scope':'One source-valid joint lower-chart primal/dual extension with actual current inputs and inverses, preserving all existing source duties. Not a global completion or new kappa.'}
 (a.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','ordinary_increment','raw_move_histogram_increment','conditional_caller']},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--combined',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
