#!/usr/bin/env python3
"""One literal mixed C2 return from the stripped eight-ferry source."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter

def load_module(path):
 spec=importlib.util.spec_from_file_location('c2_exact_source_engine',path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
def main(a):
 e=load_module(a.engine);w=e.load(a.four,e.FOUR);q=e.load(a.parent,e.PARENT);s=e.load(a.native,e.NATIVE)
 parentops=[(old,op) for op,old in zip(w['program'],w['parent_event_of_output']) if old is None or old<q['consumer']['begin']]
 oldrows,oldloc,oldbill=e.replay(w,[op for old,op in parentops]);roles={int(k):v for k,v in w['source_role_map'].items()};host={s['live'][k]:(roles[b],roles[d]) for k,b,d in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 B1,D1=host[1];B106,D106=host[106];e.need((B1,B106)==(209,298),'source B pair');e.need(w['frames'][1]==[19] and w['frames'][99]==[239],'actual initial lines')
 C=len(w['frames']);frames=w['frames']+[[19,239]];space=e.span(frames[C]);e.need(len(space)==4 and space<e.span(frames[1095]),'C2 common source chart')
 selected=w['funded_cross_pair']['pairs'][:2];e.need([int(z['target_port']) for z in selected]==[1,106] and all(F(z['coefficient'])==-1 for z in selected),'actual compensated pair')
 alpha=Counter()
 for z in selected:
  for src,c in z['packet']['alpha'].items():alpha[int(src)]+=F(c)
 alpha={src:c for src,c in alpha.items() if c}
 cache=400+w['owned_fields'];outops=[];lineage=[];markers={};target={B1:F(1),B106:F(1),D1:F(-1),D106:F(-1)}
 def emit(op,old=None):outops.append(op);lineage.append(old)
 for old,op in parentops:
  if old==530:
   e.need(op==['MOVE',B1,1,1095,False],'first B1 move');markers['B1_enter_C2']=len(outops);emit(['MOVE',B1,1,C,False],old)
  elif old==534:
   e.need(op==['MOVE',B106,99,1095,False],'first B106 move');markers['B106_enter_C2']=len(outops);emit(['MOVE',B106,99,C,False],old)
   markers['snapshot_begin']=len(outops);emit(['INIT',cache,C]);emit(['ADD',cache,B1,'1',C]);emit(['ADD',cache,B106,'1',C]);emit(['MOVE',cache,C,127,True])
   for src,c in sorted(alpha.items()):emit(['ADD',cache,src,str(c),127])
   markers['snapshot_target_ready']=len(outops)-1
   emit(['MOVE',B1,C,1095,False]);emit(['MOVE',B106,C,1095,False]);markers['original_dual_resume']=len(outops)
  else:emit(list(op),old)
 markers['consume_begin']=len(outops);emit(['ADD',cache,B1,'-1',127]);emit(['ADD',cache,B106,'-1',127]);markers['effective_innovation_ready']=len(outops)-1;emit(['ADD',B1,cache,'1',127]);emit(['CLEAR',cache,127])
 out=copy.deepcopy(w);out['schema']='moonshot-S011-one-actual-C2-mixed-target-difference-v1';out['frames']=frames;out['owned_fields']=w['owned_fields']+1;out['program']=outops;out.pop('parent_event_of_output',None);out['stripped_four_old_parent_event']=lineage;out['C2_observation']={'source_sha256':e.FOUR,'base_without31returns':True,'ports':[1,106],'B_roles':[B1,B106],'D_roles':[D1,D106],'chart':C,'frame':[19,239],'cache':cache,'known_controller_combination':{str(i):str(v) for i,v in sorted(alpha.items())},'markers':markers}
 captures={}
 def capture(t,op,rows,loc):
  if t in (markers['snapshot_target_ready'],markers['effective_innovation_ready']):captures[t]=dict(rows[cache])
 new,loc,bill=e.replay(out,outops,capture);e.need(loc==oldloc,'all public final charts retained');e.need(captures[markers['snapshot_target_ready']]==target,'actual paid mixed snapshot is exact target sum after known-controller removal')
 want=copy.deepcopy(oldrows);want[B1]=e.add(target,oldrows[B106],F(-1));e.need(new==want,'only stated B1 output shear on all400 inputs')
 def residual(rows):return {h:e.add(rows[b],{b:F(1),d:F(-1)},F(-1)) for h,(b,d) in host.items()}
 E0,E1=residual(oldrows),residual(new);e.need(e.exact_rank(E0.values())==82 and e.exact_rank(E1.values())==81,'actual stripped rank82 to81');e.need(e.add(E1[1],E1[106])=={},'one completed target-sum relation');e.need(captures[markers['effective_innovation_ready']]==e.scale(e.add(E0[1],E0[106]),F(-1)),'actual current-Hub innovation')
 desired_delta={1:2,4:2,5:-2,7:1};delta={r:bill['moves'].get(r,0)-oldbill['moves'].get(r,0) for r in set(bill['moves'])|set(oldbill['moves'])};delta={r:v for r,v in delta.items() if v};e.need(delta==desired_delta,'full MOVE debit')
 before_complete=[h for h,r in E0.items() if not r];after_complete=[h for h,r in E1.items() if not r];e.need(before_complete==after_complete==[],'no individual hosted endpoint silently credited')
 debt=0
 for h in s['live']:
  c=F(1) if h in host else F(1,2);j=roles[h+112];ideal={roles[h]:c,roles[h+112]:c};debt+=len(e.add(new[j],ideal,F(-1)))
 e.need(debt==4920,'forward debt retained')
 # Substantive mutants: controller and actual co-location are both necessary.
 controls=[]
 for name in ('missing_controller','missing_other_B_subtraction','missing_B106_stop'):
  bad=copy.deepcopy(out)
  if name=='missing_controller':
   ix=markers['snapshot_begin']+4;e.need(bad['program'][ix][0]=='ADD','controller mutant');bad['program'][ix][3]='0'
  elif name=='missing_other_B_subtraction':bad['program'][markers['consume_begin']+1][3]='0'
  else:bad['program'][markers['B106_enter_C2']][3]=1095
  rejected=False
  try:
   rr,ll,bb=e.replay(bad,bad['program']);rejected=rr!=new or ll!=loc
  except ValueError:rejected=True
  e.need(rejected,name+' must reject');controls.append(name)
 out['scope']='Actual source-bound preterminal C2 target-sum observation and final consumption; residual82 to81 only. Every first-X/first-Y/D endpoint unchanged, forward debt4920, no uniform supplier, no new kappa.'
 payload=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 receipt={'status':'PASS_ACTUAL_C2_TARGET_DIFFERENCE_RANK81','native_sha256':e.NATIVE,'four_ferry_sha256':e.FOUR,'source_parent_sha256':e.PARENT,'engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'input_directions':400,'former_reverse_rank':82,'new_reverse_rank':81,'all_firstX_firstY_D_rows_exact_predecessor':True,'every_other_B_exact_predecessor':True,'new_completed_individual_hosted_rows':0,'old_original_coordinate_forward_debt':4920,'forward_debt':debt,'full_bill':bill,'old_stripped_bill':oldbill,'move_delta':delta,'ordinary_delta':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in set(bill['counts'])|set(oldbill['counts'])},'capture_target':{str(k):str(v) for k,v in captures[markers['snapshot_target_ready']].items()},'effective_innovation':{str(k):str(v) for k,v in captures[markers['effective_innovation_ready']].items()},'markers':markers,'new_chart':{'id':C,'frame':[19,239],'span':sorted(space)},'negative_controls':controls,'scope':out['scope']}
 (a.output/'RESULT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,sort_keys=True,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--four',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
