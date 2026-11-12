#!/usr/bin/env python3
"""Two compatible quotient departures through an earlier shared code."""
import argparse,copy,gzip,json,sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_quotient_departure import inverse,mm,bas
sys.path.insert(0,str(Path(__file__).resolve().parent/'review-star'))
from engine import Q,need,sha,load,space,add,root9,rank,interpret,interval
PARENT='54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a'
EXITS={90:0,43:7};JOINT=[11,43,78,83,85,90]

def main(a):
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.combined/'WORD.json.gz';rp=a.combined/'RESULT.json';sb,pb=sp.read_bytes(),pp.read_bytes();need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(pb)==PARENT,'combined parent');s,p,prior=load(sp),load(pp),load(rp);raw={int(x):r for x,r in p['private_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};need(set(JOINT+list(EXITS.values()))<=set(host),'independent hosted fields')
 B=p['parent_second_frame_feedback_provenance']['basis'];S=p['parent_second_frame_feedback_provenance']['second'];need(set(EXITS).isdisjoint(B+S),'rank-preserving support');roots={x:root9(s['frames'][s['initial'][x]][0]) for x in s['live']};gram=lambda x,y:sum(v*z for v,z in zip(roots[x],roots[y]))/2;coef={j:gram(t,j) for j,t in EXITS.items()};need(all(c in (Q(-1,2),Q(1,2)) for c in coef.values()),'new coefficients')
 pg=p['parent_cohort_collection_provenance']['groups'][2];C=pg['chart'];dg=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==C);need(set(EXITS)<=set(pg['nonpivots']),'both primal exits nonpivot');oldA=[[Q(v) for v in r] for r in pg['matrix']];col={j:[r[i] for r in oldA] for i,j in enumerate(pg['donors'])};newcol={j:col[j] for j in pg['donors'] if j not in EXITS};newcol[83]=[x+y for x,y in zip(col[83],col[85])];newcol[85]=[-x+y for x,y in zip(col[83],col[85])]
 need(col[90]==[-x+y for x,y in zip(col[78],newcol[83])] and col[43]==[x+y for x,y in zip(col[11],newcol[85])],'two-branch quotient identities')
 decl=copy.deepcopy(p['additional_charts']);frames=s['frames']+[d['frame'] for d in decl];spaces=list(map(space,frames))
 def chart(donors):
  L={0}
  for j in donors:v=s['frames'][s['initial'][j]][0];L|={x^v for x in tuple(L)}
  L=frozenset(L)
  if L in spaces:return spaces.index(L)
  k=len(spaces);spaces.append(L);f=bas(L);frames.append(f);decl.append({'index':k,'frame':f,'construction':'exact donor-line span for reciprocal quotient','source_donors':donors});return k
 D0=chart([83,85]);D1=chart([78,83,85,90]);D2=chart([11,43,83,85]);need([len(frames[d]) for d in [D0,D1,D2]]==[2,3,3] and spaces[D0]<spaces[D1] and spaces[D0]<spaces[D2],'shared lower charts');Ds={90:D1,43:D2};Fs={j:s['final'][t+112] for j,t in EXITS.items()}
 for j,D in Ds.items():need(spaces[D]<spaces[C] and spaces[D]<spaces[Fs[j]],'actual branch containment')
 ep=a.repo/'research/moonshot-005-program/results/cohort-reconstruction/eight/WORD.json.gz';dp=a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz';ew,dw=load(ep),load(dp);oldP=ew['program'][pg['begin']:pg['end']];oldD=dw['program'][dg['begin']:dg['end']]
 def locate(block):
  starts=[i for i,o in enumerate(p['program']) if o==block[0] and p['program'][i:i+len(block)]==block];need(len(starts)==1,'unique original block');return starts[0],starts[0]+len(block)
 ps,pe=locate(oldP);ds,de=locate(oldD);at=copy.deepcopy(p);at['marks']['common_starts']=ds;entry,loc=interpret(s,at);q={x:{r:Q(1),x:Q(-1)} for x,r in raw.items()}
 for j in JOINT:
  for r in [j,host[j][0]]:need(entry[raw[r]]==q[r] and loc[raw[r]]==s['initial'][r],'actual unread donor and dual')
 collectors={j:int(p['parent_second_frame_feedback_provenance']['collectors'][str(t)]) for j,t in EXITS.items()}
 for j,t in EXITS.items():d=host[t][1];need(entry[raw[d]]==q[d] and loc[raw[d]]==Fs[j] and loc[collectors[j]]==Fs[j],'actual receiver and collector')
 pre=[]
 for j in [83,85]:
  for r in [j,host[j][0]]:pre.append(['MOVE',raw[r],s['initial'][r],D0,False])
 # T=(1/2)[[1,1],[-1,1]] on primal; T^{-T}=[[1,1],[-1,1]] on dual.
 pre += [['ADD',raw[85],raw[83],'-1',D0],['ADD',raw[83],raw[85],'1/2',D0],['SCALE',raw[85],'1/2',D0]]
 b83,b85=host[83][0],host[85][0]
 pre += [['ADD',raw[b85],raw[b83],'-1',D0],['SCALE',raw[b83],'2',D0],['ADD',raw[b83],raw[b85],'1',D0]]
 for j,D in [(83,D1),(85,D2)]:
  for r in [j,host[j][0]]:pre.append(['MOVE',raw[r],D0,D,False])
 for D,js in [(D1,[78,90]),(D2,[11,43])]:
  for j in js:
   for r in [j,host[j][0]]:pre.append(['MOVE',raw[r],s['initial'][r],D,False])
 gammas={90:{78:Q(-1),83:Q(1)},43:{11:Q(1),85:Q(1)}}
 for j,gs in gammas.items():
  D=Ds[j]
  for k,g in gs.items():pre.append(['ADD',raw[k],raw[j],str(g),D])
  for k,g in gs.items():pre.append(['ADD',raw[host[j][0]],raw[host[k][0]],str(-g),D])
  t=EXITS[j];F=Fs[j];d=host[t][1];c=coef[j];pre += [['MOVE',raw[j],D,F,False],['ADD',collectors[j],raw[j],str(-c),F],['MOVE',raw[j],F,127,False],['MOVE',raw[host[j][0]],D,F,False],['ADD',raw[host[j][0]],raw[d],str(c),F],['MOVE',raw[host[j][0]],F,127,False]]
 current={11:D2,78:D1,83:D1,85:D2};hs=[j for j in dg['first_donors'] if j not in EXITS];AH=[[newcol[j][i] for j in hs] for i in range(4)];choices=[]
 for ids in itertools.combinations(range(len(hs)),4):
  minor=[[row[k] for k in ids] for row in AH]
  if rank(minor)==4:choices.append((sum(bool(v) for row in inverse(minor) for v in row),ids))
 need(choices,'restricted hosted full rank');ids=list(min(choices)[1]);pivs=[hs[i] for i in ids];M=[[Q(i==j) for j in range(len(hs))] for i in range(len(hs))]
 for i,k in enumerate(ids):M[k]=AH[i][:]
 N=inverse(M);dual=[];temps=p['parent_paired_collection_provenance']['temporaries'][:len(hs)]
 def dense(out,rs,M,chart):
  for i,r in enumerate(rs):out += [['INIT',temps[i],chart],['ADD',temps[i],raw[r],'1',chart]]
  for i,r in enumerate(rs):
   out.append(['ADD',raw[r],temps[i],'-1',chart])
   for j,v in enumerate(M[i]):
    if v:out.append(['ADD',raw[r],temps[j],str(v),chart])
  for z in temps:out.append(['CLEAR',z,chart])
 roles=[host[j][0] for j in hs]
 for j,r in zip(hs,roles):dual.append(['MOVE',raw[r],current.get(j,s['initial'][r]),C,False])
 dense(dual,roles,[list(z) for z in zip(*N)],C)
 for j,r in zip(hs,roles):
  if j in pivs:y=dg['receivers'][pivs.index(j)];f=s['final'][y];d=host[y-112][1];dual += [['MOVE',raw[r],C,f,False],['ADD',raw[r],raw[d],'-1',f],['MOVE',raw[r],f,127,False]]
  else:dual.append(['MOVE',raw[r],C,127,False])
 dense(dual,roles,[list(z) for z in zip(*M)],127)
 for j,gs in gammas.items():
  for k,g in gs.items():dual.append(['ADD',raw[host[j][0]],raw[host[k][0]],str(g),127])
 dual += [['ADD',raw[b83],raw[b85],'-1',127],['SCALE',raw[b83],'1/2',127],['ADD',raw[b85],raw[b83],'1',127]]
 # Retain the original four primal pivots. Their matrix is unchanged, while
 # the two surviving nonpivot columns are the actual sum/difference columns.
 I=pg['pivots'];non=[j for j in pg['donors'] if j not in I and j not in EXITS];need(non==[83,85],'two actual surviving primal nonpivots');AI=[[newcol[j][i] for j in I] for i in range(4)];AIinv=inverse(AI);acc=pg['accumulator_roles'];snaps=pg['snapshot_roles'];primal=[]
 for r in acc:primal.append(['INIT',r,C])
 for j in non:
  primal.append(['MOVE',raw[j],current[j],C,False])
  for i,r in enumerate(acc):
   if newcol[j][i]:primal.append(['ADD',r,raw[j],str(newcol[j][i]),C])
  primal.append(['MOVE',raw[j],C,127,False])
 for j in I:primal.append(['MOVE',raw[j],current.get(j,s['initial'][j]),C,False])
 for r,j in zip(snaps,I):primal += [['INIT',r,C],['ADD',r,raw[j],'1',C]]
 for i,j in enumerate(I):
  primal.append(['ADD',raw[j],snaps[i],'-1',C])
  for k,r in enumerate(snaps):
   if AI[i][k]:primal.append(['ADD',raw[j],r,str(AI[i][k]),C])
  primal.append(['ADD',raw[j],acc[i],'1',C])
 for r in acc+snaps:primal.append(['CLEAR',r,C])
 for j,delivery in zip(I,pg['deliveries']):
  y=delivery['receiver'];f=s['final'][y];oldread=ew['program'][delivery['read']];need(oldread[0]=='ADD' and oldread[2]==raw[j],'true old receiver collector');primal += [['MOVE',raw[j],C,f,False],copy.deepcopy(oldread),['MOVE',raw[j],f,127,False]]
 for i,j in enumerate(I):
  for k in non:
   if newcol[k][i]:primal.append(['ADD',raw[j],raw[k],str(-newcol[k][i]),127])
 for r,j in zip(snaps,I):primal += [['INIT',r,127],['ADD',r,raw[j],'1',127]]
 for i,j in enumerate(I):
  primal.append(['ADD',raw[j],snaps[i],'-1',127])
  for k,r in enumerate(snaps):
   if AIinv[i][k]:primal.append(['ADD',raw[j],r,str(AIinv[i][k]),127])
 for r in snaps:primal.append(['CLEAR',r,127])
 for j,gs in gammas.items():
  for k,g in gs.items():primal.append(['ADD',raw[k],raw[j],str(-g),127])
 primal += [['ADD',raw[83],raw[85],'-1',127],['SCALE',raw[85],'2',127],['ADD',raw[85],raw[83],'1',127]]
 need(ds<de<ps<pe<p['marks']['common_starts'],'source chronology');need(not any(ds<i<de or ps<i<pe for i in p['marks'].values()),'no global cut inside replacement');need(not any(ds<=i<de or ps<=i<pe for i in p['native_event_to_physical']),'no native instruction replaced')
 ops=[];lineage=[];bound={};newblocks={};i=0
 while i<len(p['program']):
  if i in (ds,ps):
   end=de if i==ds else pe;rep=pre+dual if i==ds else primal;start=len(ops);newblocks['dual' if i==ds else 'primal']=[start,start+len(rep)];ops+=rep;lineage += [None]*len(rep)
   for k in range(i,end):bound[k]=start
   i=end;continue
  bound[i]=len(ops);ops.append(copy.deepcopy(p['program'][i]));lineage.append(i);i+=1
 bound[len(p['program'])]=len(ops);w=copy.deepcopy(p);w.update(schema='moonshot-S009-two-branch-current-row-quotient-v1',program=ops,additional_charts=decl,parent_word_sha256=PARENT,parent_event_of_output=lineage,marks={k:bound[v] for k,v in p['marks'].items()},native_event_to_physical=[bound[v] for v in p['native_event_to_physical']],two_branch_departure={'shared_donors':[83,85],'shared_chart':D0,'branches':{str(j):{'receiver':EXITS[j],'chart':Ds[j],'coefficient':str(coef[j]),'absorbers':{str(k):str(v) for k,v in gammas[j].items()}} for j in EXITS},'cohort_chart':C,'old_primal_block':[ps,pe],'old_dual_block':[ds,de],'new_blocks':newblocks,'reduced_hosted_pivots':pivs,'shared_transform':[['1/2','1/2'],['-1/2','1/2']],'dual_transform':[['1','1'],['-1','1']]})
 for j,t in EXITS.items():
  for y,d,c,key in [(t+112,j,-coef[j],'corrections'),(host[j][0],host[t][1],coef[j],'paired_reverse_corrections')]:
   row={int(k):Q(v) for k,v in w[key].get(str(y),[])};row[d]=row.get(d,Q(0))+c;w[key][str(y)]=[[k,str(v)] for k,v in sorted(row.items()) if v]
 before,bl=interpret(s,p);after,al=interpret(s,w);need(bl==al and set(before)==set(after),'same full prefix physical interface');changes={}
 for j,t in EXITS.items():changes[raw[t+112]]=add({},q[j],-coef[j]);changes[raw[host[j][0]]]=add({},q[host[t][1]],coef[j])
 need(all(after[r]==add(row,changes.get(r,{})) for r,row in before.items()),'all1880 current-row coefficients: exactly four intended changes');need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'same native suffix')
 for j,t in EXITS.items():
  need(add(after[raw[t+112]],after[raw[j]],coef[j])==before[raw[t+112]],'source forward inverse');need(add(after[raw[host[j][0]]],after[raw[host[t][1]]],-coef[j])==before[raw[host[j][0]]],'source reverse inverse')
 order=list(host);R=[[Q(x==y)+after[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order] for x in order];need(rank(R)==88,'actual residual remains rank88')
 tail=w['program'][w['marks']['common_starts']:]
 for r in list(EXITS.values()):
  for z in [r+112]+[host[j][0] for j,t in EXITS.items() if t==r]:
   uses=[o for o in tail if o[1]==raw[z] or o[0] in ('ADD','COPY') and o[2]==raw[z]];need(uses==[['ADD',raw[z],z,'1',s['final'][z]]],'no later changed-row feedback')
 bill,fin=interpret(s,w,True);oldbill,oldfin=interpret(s,p,True);need(fin==oldfin,'same final source charts');delta={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};dr={k:bill['raw_histogram'].get(k,0)-oldbill['raw_histogram'].get(k,0) for k in bill['raw_histogram'].keys()|oldbill['raw_histogram'].keys()};need(sum(k*v for k,v in bill['raw_histogram'].items())==3200,'same raw rank mass')
 for k in bill['move_rank_histogram'].keys()|oldbill['move_rank_histogram'].keys():need(bill['move_rank_histogram'].get(k,0)-bill['raw_histogram'].get(k,0)==oldbill['move_rank_histogram'].get(k,0)-oldbill['raw_histogram'].get(k,0),'no new owned route at any rank')
 PP={int(k):v for k,v in prior['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in prior['conditional_caller']['T4'].items()}
 for k,v in dr.items():PP[k]=PP.get(k,0)+18*v
 lo,hi=interval({k:T.get(k,0)-PP.get(k,0) for k in T.keys()|PP.keys()});lo/=18;hi/=18;need(lo>0,'strict complete provisional margin')
 bad=copy.deepcopy(w);m=newblocks['dual'][0]+5;need(bad['program'][m]==['ADD',raw[83],raw[85],'1/2',D0],'shared-code mutation site');bad['program'][m][3]='1';broken,_=interpret(s,bad);need(any(broken[r]!=after[r] for r in after),'wrong shared transform rejected')
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_TWO_COMPATIBLE_PAIRED_QUOTIENT_DEPARTURES','source_sha256':sha(sb),'parent_word_sha256':PARENT,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'shared_chart':D0,'branch_charts':Ds,'source_donor_cohort':pg['donors'],'exit_receivers':EXITS,'coefficients':{str(k):str(v) for k,v in coef.items()},'reduced_hosted_pivots':pivs,'only_changed_raw_outputs':[t+112 for t in EXITS.values()]+[host[j][0] for j in EXITS],'hosted_reverse_residual_rank':88,'coupled_reverse_complete':p['coupled_precondition']['source_roles'],'retained_forward_completions':p['newly_completed_firstY_receivers'],'forward_residual_count_in_preconditioned_basis':prior['forward_residual_count_in_preconditioned_basis']-2,'forward_residual_count_in_original_difference_basis':prior['forward_residual_count_in_original_difference_basis']-2,'bill':bill,'ordinary_increment':delta,'raw_move_histogram_increment':dr,'new_owned_moves':0,'conditional_caller':{'T4':T,'P_partial':PP,'paid_positions':sum(PP.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-PP.get(k,0)) for k in T.keys()|PP.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'all_eight_rank9_and_eight_rank1_packets_retained':True},'negative_controls':{'wrong_shared_transform_changes_exact_source_map':True},'scope':'Actual shared-prefix coding and two branches on current carriers; every original B duty restored. Two extra forward and transpose coefficients, no extra reverse nullity or complete supplier.'}
 (a.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','ordinary_increment','raw_move_histogram_increment','conditional_caller']},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--combined',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
