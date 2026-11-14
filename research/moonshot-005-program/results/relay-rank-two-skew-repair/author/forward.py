#!/usr/bin/env python3
"""Actually deliver the rank-two skew forward correction; no full supplier claim."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,copy,gzip,hashlib,json
from build import need,prepare,expected,replay,combine,plus,dot,mm,trans,eye
CORE='66815ff5d01f76f19e61b3f14cb12bf90ceef07c17801b6c681dacb628e19f12'
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==CORE,'exact skew source');core=json.loads(gzip.decompress(raw));w=copy.deepcopy(core);rm,T,S,H,P,U,g,L,B,D=prepare(w)
tail=w['program'][-208:];need(all(e[0]=='MOVE'and not e[-1]for e in tail),'literal final public tail');xm=[e for e in tail if e[1]<104];ym=[e for e in tail if 104<=e[1]<208];need(len(xm)==len(ym)==104 and all(e[3]==127 for e in xm)and all(e[2]==3 for e in ym),'all X to Hub and all Y from ground')
u=list(map(F,['1','1/2','2','1/2','9/2','-3/2','1/2','-5/2']));v=list(map(F,['0','1','0','-1','1/2','1/2','-1/2','1/2']));features=[[dot(g[h],z)for h in P]for z in[v,u]];receivers=[[dot(g[h],u),-dot(g[h],v)]for h in P];Gamma=mm(receivers,features);K=[[L[i][j]-int(i==j)for j in range(8)]for i in range(8)];need(Gamma==mm(mm([g[h]for h in P],K),trans([g[h]for h in P])),'two-mode skew factorization')
ops=[['INIT',400+k,127]for k in range(2)]
for k,feature in enumerate(features):
 for h,c in zip(P,feature):
  if c:ops.append(['ADD',400+k,rm[h],str(c),127])
ops += [['MOVE',400+k,127,3,True]for k in range(2)]
for h,cs in zip(P,receivers):
 for k,c in enumerate(cs):
  if c:ops.append(['ADD',rm[h+112],400+k,str(c),3])
ops += [['CLEAR',400+k,3]for k in range(2)]
w['program'][-208:]=xm+ops+ym;w['schema']='moonshot-rank-two-skew-relay-with-actual-forward-v1';w['source_pins']['skew_core_word']=CORE;w['skew_forward']={'actual_added_events':len(ops),'owned_Hub_to_ground_moves':2,'rank':2,'full_native_forward_completed':False,'all_forward_skew_terms_acquired':True,'X_current_rows':'a_h=x_h, except coupled a_h=x_h-y_h'}
want=expected(core);current_x=[want[rm[h]]for h in P]
for h,row in zip(P,Gamma):want[rm[h+112]]=plus(want[rm[h+112]],combine(row,current_x))
rows,loc,bill=replay(w);oldrows,oldloc,oldbill=replay(core);need(rows==want,'all400 modified endpoint rows');need(loc==oldloc,'all public endpoints preserved');need(bill['public_moves']==oldbill['public_moves'],'unchanged public movement');need(bill['owned_moves']==dict(sorted({**oldbill['owned_moves'],9:2}.items())),'exactly two added rank9 moves');need(bill['lifetimes']==oldbill['lifetimes']+2 and bill['dirty_retirements']==oldbill['dirty_retirements']+2,'both moment histories counted');need(bill['odd_prefix_lcm']==1,'exact dyadic scalar prefixes')
# Omitting one real acquisition gives the wrong actual Y outputs.
bad=copy.deepcopy(w);idx=len(core['program'])-208+104;first=next(i for i in range(idx,idx+len(ops))if bad['program'][i][0]=='ADD');del bad['program'][first];badrows,_,_=replay(bad);need(badrows!=want,'missing acquisition negative control')
args.out.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();word=args.out/'WORD.json.gz';word.write_bytes(gzip.compress(payload,mtime=0));result={'status':'PASS_ACTUAL_RANK_TWO_SKEW_FORWARD_SERVICE','core_sha256':CORE,'word_sha256':hashlib.sha256(word.read_bytes()).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'actual_added_events':len(ops),'added_event_counts':dict(Counter(e[0]for e in ops)),'bill':bill,'remaining_original_D':76,'remaining_forward_matrix':'I-G on current a, before any residual completion; actual added Gamma=g K g^T only','all_original_X_rows_preserved':True,'no_extra_public_moves':True,'both_moment_acquisitions_and_dirty_retirements_charged':True,'missing_capture_rejected':True,'phase_review':'new existing-chart Hub-to-ground MOVE still requires independent physical signed-phase review','no_new_kappa':True};(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
