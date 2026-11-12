#!/usr/bin/env python3
"""Literal two-family cyclic X2/Y2 source schedule; no first-Y hoisting."""
import argparse,copy,gzip,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_quotient_departure import bas
sys.path.insert(0,str(Path(__file__).resolve().parent/'review-star'))
from engine import Q,need,sha,load,space,root9,rank,interpret,interval,add
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPIN='54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a'
FPIN='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'

def main(a):
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.parent/'WORD.json.gz';fp=a.frame/'WORD.json.gz';need(sha(sp.read_bytes())==SPIN and sha(pp.read_bytes())==PPIN and sha(fp.read_bytes())==FPIN,'immutable source/parent/frame pins');s,p,f=load(sp),load(pp),load(fp);prior=load(a.parent/'RESULT.json');raw={int(k):v for k,v in p['private_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};meta=p['parent_second_frame_feedback_provenance'];rootmeta=f['second_frame_feedback'];need(meta==rootmeta,'literal root feedback provenance');roots={x:root9(s['frames'][s['initial'][x]][0]) for x in s['live']};G=lambda x,y:sum(v*z for v,z in zip(roots[x],roots[y]))/2
 def locate(block):
  z=[i for i,o in enumerate(p['program']) if o==block[0] and p['program'][i:i+len(block)]==block];need(len(z)==1,'unique old block');return z[0]
 fblock=f['program'][rootmeta['begin']:rootmeta['end']];fb=locate(fblock);offset=fb-rootmeta['begin'];drop=set();groups=[];old_dual=[];dw=load(a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz')
 for ci,fg in zip([1,12],rootmeta['groups']):
  og=p['parent_cohort_collection_provenance']['groups'][ci];B=fg['donors'];S=fg['receivers'];T=[j for j in og['donors'] if j not in S];need(len(B)==len(S)==4 and len(T)==3 and all(j in host for j in B+S+T),'actual hosted families');need(all(G(x,y)==Q(x==y) for F in [B,S,T] for x in F for y in F),'each family orthonormal');groups.append({'B':B,'S':S,'T':T,'old_cohort':ci})
  dg=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==og['chart']);block=dw['program'][dg['begin']:dg['end']];start=locate(block);old_dual.append([start,start+len(block)]);drop.update(range(start,start+len(block)))
  # The root's literal paired block has four primal ascents, four dual
  # ascents, two dense encodes, paired receiver reads and two dense decodes.
  for i in range(fg['begin']+4,fg['begin']+8):need(f['program'][i][0]=='MOVE' and f['program'][i][1] in [raw[host[j][0]] for j in B],'actual B dual initial route');drop.add(i+offset)
  enc=fg['reverse_encode'];begin=min(enc['snapshots'])-1;end=fg['reads'][0]['forward']-2;drop.update(range(begin+offset,end+offset))
  dec=fg['reverse_decode'];begin=min(dec['snapshots'])-1;drop.update(range(begin+offset,fg['end']+offset))
  for read in fg['reads']:
   i=read['forward'];need(f['program'][i-1][0]=='MOVE' and f['program'][i+1][0]=='ADD' and f['program'][i+3][0]=='MOVE','literal paired receiver pattern');drop.update([i-1+offset,i+1+offset,i+3+offset])
 external=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==1105);need(external['first_donors']==[12,31] and external['kind']=='rank2_direct_cochart','actual external two-record duty');eblock=dw['program'][external['begin']:external['end']];eb=locate(eblock);drop.update(range(eb,eb+len(eblock)));extra=[12,31];extrasets=[{56:Q(-1,2),100:Q(1,2)},{77:Q(1,2),103:Q(-1,2)}];extreceivers=set(extrasets[0])|set(extrasets[1]);need(len(extreceivers)==4,'four live external receivers')
 allports=[j for g in groups for k in ['B','S','T'] for j in g[k]];need(len(set(allports))==22,'disjoint 22-port block')
 for j in allports:
  d=host[j][1];hits=[i for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[d]]
  if j in extreceivers:need(len(hits)==2 and set(hits)<=drop,'all real external Y2 route segments replaced')
  else:need(len(hits)==1 and p['program'][hits[0]]==['MOVE',raw[d],s['initial'][d],s['final'][d],False],'true direct Y2 path');drop.add(hits[0])
 need(all(i>=fb for i in drop),'no early dependency removed');at=copy.deepcopy(p);at['marks']['common_starts']=fb;entry,loc=interpret(s,at);q={r:{z:Q(1),r:Q(-1)} for r,z in raw.items()}
 for j in allports:
  for r in host[j]:need(entry[raw[r]]==q[r] and loc[raw[r]]==s['initial'][r],'authentic unread X2/Y2 entry')
 for j in extra:
  b=host[j][0];need(entry[raw[b]]==q[b] and loc[raw[b]]==s['initial'][b],'authentic unread external X2')
 decl=copy.deepcopy(p['additional_charts']);frames=s['frames']+[x['frame'] for x in decl];spaces=list(map(space,frames))
 def chart(js):
  L={0}
  for j in js:
   for v in frames[s['initial'][j]]:L|={x^v for x in tuple(L)}
  L=frozenset(L)
  if L in spaces:return spaces.index(L)
  k=len(spaces);spaces.append(L);fr=bas(L);frames.append(fr);decl.append({'index':k,'frame':fr,'construction':'cyclic dual donor-family span','source_donors':js});return k
 cyc=[];blockloc={};receipts=[]
 def mv(r,A,B):
  need(A!=B and spaces[A]<spaces[B],'strict ascending current route');cyc.append(['MOVE',raw[r],A,B,False]);blockloc[r]=B
 def meet(D,R,C):
  for x in D:
   for y in R:
    b,d=host[x][0],host[y][1];need(blockloc[b]==blockloc[d]==C,'actual current dual cochart');v=G(x,y);need(v in [Q(-1,2),Q(1,2)],'cross Gram coefficient');cyc.append(['ADD',raw[b],raw[d],str(v),C])
 E=chart(extra);Jextra=[chart(extra+g['S']+g['T']) for g in groups];need(len(frames[E])==2 and all(len(frames[j])==5 for j in Jextra),'external two/five dimensional charts');bplus,bminus=[host[j][0] for j in extra]
 for b in [bplus,bminus]:mv(b,s['initial'][b],E)
 cyc += [['ADD',raw[bminus],raw[bplus],'-1',E],['ADD',raw[bplus],raw[bminus],'1/2',E],['SCALE',raw[bminus],'-1/2',E]]
 for b,J in zip([bplus,bminus],Jextra):mv(b,E,J)
 for gi,g in enumerate(groups):
  B,S,T=[g[k] for k in ['B','S','T']];D={k:chart(g[k]) for k in ['B','S','T']};J={'BS':chart(B+S),'BT':chart(B+T),'ST':chart(S+T)};need(all(len(frames[c])==3 for c in D.values()) and all(len(frames[c])==4 for c in J.values()),'exact 3/4 chart dimensions')
  for pair,third in [('BS','T'),('BT','S'),('ST','B')]:
   for j in g[third]:need(spaces[J[pair]]<spaces[s['final'][host[j][1]]],'pair join in every third-family facet')
  start=len(cyc)
  for k in ['B','S','T']:
   for j in g[k]:b=host[j][0];mv(b,s['initial'][b],D[k])
  for k,dest in [('B','T'),('S','B'),('T','S')]:
   for j in g[k]:d=host[j][1];mv(d,s['initial'][d],D[dest])
  meet(T,B,D['T']);meet(B,S,D['B']);meet(S,T,D['S'])
  for k,pair in [('B','BS'),('S','ST'),('T','BT')]:
   for j in g[k]:b=host[j][0];mv(b,blockloc[b],J[pair])
  for k,pair in [('B','ST'),('S','BT'),('T','BS')]:
   for j in g[k]:d=host[j][1];mv(d,blockloc[d],J[pair])
  meet(S,B,J['ST']);meet(T,S,J['BT']);meet(B,T,J['BS'])
  for k in ['B','S','T']:
   for j in g[k]:
    b,d=host[j];mv(b,blockloc[b],127)
    if j in extrasets[gi]:mv(d,blockloc[d],Jextra[gi])
    else:mv(d,blockloc[d],s['final'][d])
  encoded=[bplus,bminus][gi]
  for j,c in extrasets[gi].items():
   d=host[j][1];need(blockloc[d]==blockloc[encoded]==Jextra[gi],'real external paired receiver');cyc.append(['ADD',raw[encoded],raw[d],str(c),Jextra[gi]]);mv(d,Jextra[gi],s['final'][d])
  mv(encoded,Jextra[gi],127)
  receipts.append({**g,'single_charts':D,'pair_charts':J,'local_begin':start,'local_end':len(cyc)})
 cyc += [['ADD',raw[bplus],raw[bminus],'1',127],['SCALE',raw[bminus],'-2',127],['ADD',raw[bminus],raw[bplus],'1',127]]
 need(not any(i in drop for i in p['native_event_to_physical']),'no native instruction deleted');ops=[];lineage=[];bound={};insert=None
 for i,o in enumerate(p['program']):
  if i==fb:insert=len(ops);ops.extend(cyc);lineage.extend([None]*len(cyc))
  bound[i]=len(ops)
  if i not in drop:ops.append(copy.deepcopy(o));lineage.append(i)
 bound[len(p['program'])]=len(ops);need(insert is not None,'cyclic insertion');w=copy.deepcopy(p);w.update(schema='moonshot-S009-cyclic-dual-hoist-v1',program=ops,additional_charts=decl,parent_word_sha256=PPIN,parent_event_of_output=lineage,marks={k:bound[v] for k,v in p['marks'].items()},native_event_to_physical=[bound[v] for v in p['native_event_to_physical']],cyclic_dual={'source_groups':receipts,'begin':insert,'end':insert+len(cyc),'removed_parent_event_indices':sorted(drop),'removed_original_dual_blocks':old_dual,'frame_parent_sha256':FPIN,'firstY_and_primal_routes_unchanged':True,'external_repair':{'source_donors':extra,'original_block':[eb,eb+len(eblock)],'initial_chart':E,'branch_charts':Jextra,'encoded_rows':[['1/2','1/2'],['1/2','-1/2']],'receiver_groups':[{str(k):str(v) for k,v in r.items()} for r in extrasets]}})
 expected={};newterms=[]
 for g in groups:
  for xs,ys in [('B','T'),('S','T'),('T','S')]:
   for x in g[xs]:
    for y in g[ys]:
     b,d=host[x][0],host[y][1];c=G(x,y);expected[raw[b]]=add(expected.get(raw[b],{}),q[d],c);newterms.append([x,y,str(c)]);row={int(z):Q(v) for z,v in w['paired_reverse_corrections'].get(str(b),[])};row[d]=row.get(d,Q(0))+c;w['paired_reverse_corrections'][str(b)]=[[z,str(v)] for z,v in sorted(row.items()) if v]
 first_raw={raw[j] for x in s['live'] for j in [x,x+112]};touches=lambda o:o[1] in first_raw or o[0] in ['ADD','COPY'] and o[2] in first_raw;need([o for o in w['program'] if touches(o)]==[o for o in p['program'] if touches(o)],'all208 first-X/first-Y instruction projection literal')
 before,bl=interpret(s,p);after,al=interpret(s,w);need(bl==al and set(before)==set(after),'same full prefix records and locations');need(all(after[r]==add(v,expected.get(r,{})) for r,v in before.items()),'all1880 prefix: precisely the 72 intended extra transpose coefficients');need(len(newterms)==72,'exact new contact count');need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'identical native suffix')
 order=list(host);R=[[Q(x==y)+after[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order] for x in order];need(rank(R)==82,'exact actual reverse rank82');K=set(allports);need(rank([[G(x,y) for y in allports] for x in allports])==8,'closed principal Gram rank8');need(all(R[order.index(x)][order.index(y)]==G(x,y) for x in allports for y in allports),'entire22port principal block is Gram');outside=[x for x in order if x not in K];need(all(R[order.index(x)][order.index(y)]==0 for x in allports for y in outside),'zero top-right block');need(all(R[order.index(x)][order.index(y)]==Q(x==y) for x in outside for y in outside),'identity remaining outside block')
 for r in expected:
  uses=[o for o in w['program'][w['marks']['common_starts']:] if o[1]==r or o[0] in ['ADD','COPY'] and o[2]==r];original=next(k for k,v in raw.items() if v==r);need(uses==[['ADD',r,original,'1',s['final'][original]]],'no changed-row native feedback')
 # The declared information inverse removes the added shears using the
 # authentic preserved Y2 fields. It is not an uncharged physical decoder.
 for r,delta in expected.items():need(add(after[r],delta,Q(-1))==before[r],'exact information inverse')
 bill,fin=interpret(s,w,True);oldbill,oldfin=interpret(s,p,True);need(fin==oldfin,'same final charts');ordinary={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};dr={k:bill['raw_histogram'].get(k,0)-oldbill['raw_histogram'].get(k,0) for k in bill['raw_histogram'].keys()|oldbill['raw_histogram'].keys()};need({k:v for k,v in dr.items() if v}=={1:34,2:2,3:20,4:20,5:-2,6:-4,8:-18},'complete predicted raw invoice');need(sum(k*v for k,v in bill['raw_histogram'].items())==3200,'raw rank mass conserved')
 for k in bill['move_rank_histogram'].keys()|oldbill['move_rank_histogram'].keys():need(bill['move_rank_histogram'].get(k,0)-bill['raw_histogram'].get(k,0)==oldbill['move_rank_histogram'].get(k,0)-oldbill['raw_histogram'].get(k,0),'no owned MOVE increment at any rank')
 PP={int(k):v for k,v in prior['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in prior['conditional_caller']['T4'].items()}
 for k,v in dr.items():PP[k]=PP.get(k,0)+18*v
 lo,hi=interval({k:T.get(k,0)-PP.get(k,0) for k in T.keys()|PP.keys()});lo/=18;hi/=18;need(lo>0,'positive retained provisional margin')
 bad=copy.deepcopy(w);x,y,c=newterms[0];needle=['ADD',raw[host[x][0]],raw[host[y][1]],c,next(o[4] for o in cyc if o[0]=='ADD' and o[1]==raw[host[x][0]] and o[2]==raw[host[y][1]])];hits=[i for i in range(insert,insert+len(cyc)) if bad['program'][i]==needle];need(len(hits)==1,'unique new-entry mutant');bad['program'][hits[0]][3]='0';br,_=interpret(s,bad);need(any(br[r]!=after[r] for r in after),'omitted new coefficient rejected');BR=[[Q(x==y)+br[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order] for x in order];mr=rank(BR);need(mr>82,'missing contact loses exact principal rank')
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_CYCLIC_DUAL_PRINCIPAL_RANK82','source_sha256':SPIN,'parent_word_sha256':PPIN,'frame_parent_sha256':FPIN,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'groups':receipts,'old_dual_blocks':old_dual,'new_transpose_coefficients':newterms,'new_coefficient_count':72,'only_changed_hosted_ports':[j for j in allports if raw[host[j][0]] in expected],'hosted_reverse_residual_rank':82,'closed_principal_ports':allports,'closed_principal_rank':8,'coupled_reverse_complete':p['coupled_precondition']['source_roles'],'forward_residual_count_in_preconditioned_basis':prior['forward_residual_count_in_preconditioned_basis'],'forward_residual_count_in_original_difference_basis':prior['forward_residual_count_in_original_difference_basis'],'retained_forward_completions':p['newly_completed_firstY_receivers'],'bill':bill,'ordinary_increment':ordinary,'raw_move_histogram_increment':dr,'new_owned_moves':0,'conditional_caller':{'T4':T,'P_partial':PP,'paid_positions':sum(PP.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-PP.get(k,0)) for k in T.keys()|PP.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'all_eight_rank9_and_eight_rank1_packets_retained':True},'negative_controls':{'one_omitted_new_contact_changes_source_map':True,'mutant_reverse_rank':mr},'scope':'Actual source-bound cyclic X2/Y2 schedule. First-Y E8 input access and all old primal code retained. No extra owned calls; rank82 is an enabling finite residual-rank result, not a complete supplier or new kappa.'};(a.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','ordinary_increment','raw_move_histogram_increment','conditional_caller']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--frame',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
