#!/usr/bin/env python3
"""Compose the coupled preconditioner with the actual rank88 two-frame source."""
import argparse,copy,gzip,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'review-star'))
from engine import Q,need,sha,load,add,interpret,rank,root9,interval
U=(17,19,30,38,40,47,52,60)
PARENT='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'

def main(a):
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.frame/'output/WORD.json.gz';rp=a.frame/'output/RESULT.json';sb,pb=sp.read_bytes(),pp.read_bytes();need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(pb)==PARENT,'exact two-frame parent');s,p,oldresult=load(sp),load(pp),load(rp);raw={int(x):r for x,r in p['private_role_map'].items()};host={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};need(tuple(x for x in s['live'] if x not in host)==U,'coupled source roles')
 need(all(e==['ADD',raw[x],x,'-1',s['initial'][x]] for x,e in zip(sorted(raw),p['program'][:400])),'actual complete400 difference boundary');skip={}
 for x in U:
  y=x+112;first=next((i,o) for i,o in enumerate(p['program'][400:],400) if o[1]==raw[y] or o[0] in ('ADD','COPY') and o[2]==raw[y]);need(first[1]==['SCALE',raw[y],'1/2',3],'first coupled Y use is half-scale');skip[first[0]]=x
 ops=[];lineage=[];boundaries={};eventmap={};preloads=[]
 for i,o in enumerate(p['program']):
  if i==400:
   for x in U:
    y=x+112;L=s['initial'][x];start=len(ops);block=[['INIT',1880,3],['ADD',1880,raw[y],'1',3],['MOVE',1880,3,L,True],['ADD',raw[x],1880,'-1',L],['CLEAR',1880,L]];ops+=block;lineage += [None]*5;preloads.append({'X':x,'Y':y,'line':L,'first_event':start,'instructions':5})
  boundaries[i]=len(ops)
  if i in skip:continue
  eventmap[i]=len(ops);ops.append(copy.deepcopy(o));lineage.append(i)
 boundaries[len(p['program'])]=len(ops)
 w=copy.deepcopy(p);w['parent_second_frame_feedback_provenance']=w.pop('second_frame_feedback');w.update(schema='moonshot-S009-rank88-with-preterminal-coupled-eight-v1',program=ops,parent_word_sha256=PARENT,parent_event_of_output=lineage,native_event_to_physical=[eventmap[i] for i in p['native_event_to_physical']],marks={k:boundaries[v] for k,v in p['marks'].items()},coupled_precondition={'source_roles':list(U),'formula':'x_tilde=x-y; y_tilde=2y','realized_double_half_cancellation':True,'temporary':1880,'preloads':preloads,'deleted_parent_half_scales':sorted(skip),'prior_source_marks_semantics':'Raw first-X originals/restoration marks now refer to the preconditioned x_tilde; hosted X2/Y2 and common inputs are unchanged.'})
 w['marks']['all_preconditioned_donors_restored']=w['marks'].pop('all_active_donors_restored')
 def subst(row):
  change={}
  for x in U:y=x+112;change[raw[x]]={raw[x]:Q(1),raw[y]:Q(-1),y:Q(1)};change[raw[y]]={raw[y]:Q(2),y:Q(-1)}
  out={}
  for j,c in row.items():out=add(out,change.get(j,{j:Q(1)}),c)
  return out
 before,bl=interpret(s,p);after,al=interpret(s,w);need(bl==al and set(before)==set(after),'same physical prefix interface');need(all(after[r]==subst(row) for r,row in before.items()),'all1880 prefix coefficients precomposed')
 q={x:{r:Q(1),x:Q(-1)} for x,r in raw.items()}
 for x in U:need(after[raw[x]]==add(q[x],q[x+112],Q(-1)),'eight true coupled reverse values')
 for y in p['newly_completed_firstY_receivers']:need(after[raw[y]]==add(q[y],q[y-112]),'eight previous complete forward receivers')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'literal inherited common suffix')
 order=list(host);R=[]
 for x in order:
  need(after[raw[host[x][0]]]==before[raw[host[x][0]]],'all actual hosted reverse rows unchanged')
  need(after[raw[host[x][1]]]==before[raw[host[x][1]]],'all actual hosted Y2 unchanged')
  R.append([Q(x==y)+after[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order])
 need(rank(R)==88,'actual hosted residual rank88')
 bill,loc=interpret(s,w,True);oldbill,oldloc=interpret(s,p,True);need(loc==oldloc and bill['raw_histogram']==oldbill['raw_histogram'],'every final chart and raw route retained');delta={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};need({k:v for k,v in delta.items() if v}=={'ADD':16,'MOVE':8,'INIT':8,'CLEAR':8,'SCALE':-8},'exact ordinary increment');need(bill['instructions']==78155,'actual combined length')
 PP={int(k):v for k,v in oldresult['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in oldresult['conditional_caller']['T4'].items()};PP[1]+=144;lo,hi=interval({k:T.get(k,0)-PP.get(k,0) for k in T.keys()|PP.keys()});lo/=18;hi/=18
 roots={x:root9(s['frames'][s['initial'][x]][0]) for x in s['live']};H={}
 for x in s['live']:
  c=Q(1) if x in host else Q(1,2);row={d:c*sum(v*z for v,z in zip(roots[x],roots[d]))/2-c*int(x==d) for d in s['live']}
  for d,v in p['corrections'].get(str(x+112),[]):row[d]+=Q(v)
  H[x]={d:v for d,v in row.items() if v}
 count=sum(map(len,H.values()));expanded=count+sum(sum(d in U for d in row) for row in H.values());need(count==4569 and expanded==4920,'basis-explicit residual accounting')
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_COMBINED_RANK88_AND_PRETERMINAL_COUPLED_EIGHT','source_sha256':sha(sb),'parent_word_sha256':PARENT,'parent_payload_sha256':sha(gzip.decompress(pb)),'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'prefix_rows_compared':len(after),'all_common_and_hosted_rows_compose_exactly':True,'coupled_reverse_complete':list(U),'hosted_reverse_residual_rank':88,'preserved_complete_forward_receivers':p['newly_completed_firstY_receivers'],'forward_residual_count_in_preconditioned_basis':count,'forward_residual_count_in_original_difference_basis':expanded,'bill':bill,'ordinary_increment':delta,'new_owned_histogram':{'1':8},'conditional_caller':{'T4':T,'P_partial':PP,'paid_positions':sum(PP.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-PP.get(k,0)) for k in T.keys()|PP.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'all_eight_rank9_packets_retained':True},'scope':'Literal composition of two reviewed mechanisms on arbitrary1880 inputs. Eight coupled reverse duties complete, hosted residual rank88, physical completion and all suppliers/foundations remain. No new kappa.'}
 (a.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],bill['instructions'],float(lo),'remaining',expanded,'original-basis residual entries')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--frame',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
