#!/usr/bin/env python3
"""Source independence, shared-chart and chronological negative controls."""
import argparse,copy,gzip,json
from pathlib import Path
from hashlib import sha256
from common import *
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rr=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(rr).hexdigest()==PINS['routes'];route={fid(r[0],r[1],r[2]):r for r in map(json.loads,rr.splitlines())};w=json.loads(gzip.decompress(a.word.read_bytes()));c=json.loads(gzip.decompress(a.certificate.read_bytes()));result=[]
 def evaluate(actions):return replay(actions,w['caches'],route,c['neighbor80_order'],w['source_donors'])
 for label,tag,key,i in [('hub_inverse','restore-all-X','all_original_X_restored',None),('ground_inverse','inverse-arbitrary-Y','arbitrary_original_Y_baseline_restored',None),('joint_source','joint-source-5','target_rows_correct',80),('late_target_sum','F1-cancel-shared-masks','target_rows_correct',1)]:
  actions=copy.deepcopy(w['actions']);act=next(x for x in actions if x['tag']==tag);act['word']=[op for op in act['word']if op[0]!='ADD'];z=evaluate(actions);assert not(z[key]if i is None else z[key][i]);result.append({'control':label,'rejected':True,'X':z['all_original_X_restored'],'Y':z['arbitrary_original_Y_baseline_restored'],'targets':z['target_rows_correct']})
 actions=copy.deepcopy(w['actions']);act=next(x for x in actions if x['tag']=='capture-F80-joint-0');assert len(act['word'])==15;act['word']=act['word'][:-5];z=evaluate(actions);assert not z['target_rows_correct'][80];result.append({'control':'omit_second_tile_at_joint_early_capture','rejected':True,'targets':z['target_rows_correct']})
 actions=copy.deepcopy(w['actions']);captures=[x for x in actions if x['tag'].startswith('capture-12-5-')];assert len(captures)==4;actions=[x for x in actions if x not in captures];idx=next(i for i,x in enumerate(actions)if x['tag']=='joint-source-5');actions[idx+1:idx+1]=captures;z=evaluate(actions);assert not z['target_rows_correct'][1];result.append({'control':'native_capture_after_joint_source_chart','rejected':True,'targets':z['target_rows_correct']})
 actions=copy.deepcopy(w['actions']);act=next(x for x in actions if x['tag']=='early-H-99-106');wrong=next(f for f,r in route.items()if r[0]=='X'and r[3]==106 and r[4]==12)
 for op in act['word']:op[1]=5*wrong+op[1]%5
 z=evaluate(actions);assert not z['target_rows_correct'][80];result.append({'control':'alias_two_D_carriers_at_shared_H','rejected':True,'targets':z['target_rows_correct']})
 failed=[]
 for j in w['shared_donors']:
  u=rows80(c['neighbor80_order'],j);p1=[[T[2][v]for v in row]for row in u];p2=[[T[3][v]for v in row]for row in u];assert [[x^y for x,y in zip(r,s)]for r,s in zip(p1,p2)]==u
  assert reduce(p1+p2)==4<8;failed.append(j)
 result.append({'control':'target_only_two_tile_lift','selected_aggregate_correct':True,'source_rank':4,'required_source_rank':8,'rejected_shared_donors':failed,'rejected':True})
 a.out.mkdir(parents=True,exist_ok=True);out={'status':'PASS_EIGHT_OVERLAP_STITCH_NEGATIVE_CONTROLS','controls':result};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
