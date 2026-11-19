#!/usr/bin/env python3
"""Independent obligations within the printed pair word: omission controls."""
import argparse,copy,gzip,json
from pathlib import Path
from hashlib import sha256
from build import fid,PINS,replay
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--matrices',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rr=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(rr).hexdigest()==PINS['routes'];route={fid(r[0],r[1],r[2]):r for r in map(json.loads,rr.splitlines())}
 w=json.loads(gzip.decompress(a.word.read_bytes()));m=json.loads(gzip.decompress(a.matrices.read_bytes()));results=[]
 cases=[('hub_restore','restore-all-X','all_original_X_restored',None),('ground_restore','inverse-arbitrary-Y','arbitrary_original_Y_baseline_restored',None),('late_native_capture','native-late-5-86','target_rows_correct',1),('early_source_chart','early-source-5','target_rows_correct',80),('late_H_sum','sum-Y-H-86','target_rows_correct',1)]
 # Pick the first actual donor5 native cache; labels depend on fixed H incidence.
 cases[2]=(cases[2][0],next(x['tag']for x in w['actions']if x['tag'].startswith('native-late-5-')),cases[2][2],cases[2][3])
 for label,tag,key,receiver in cases:
  actions=copy.deepcopy(w['actions']);act=next(x for x in actions if x['tag']==tag);act['word']=[op for op in act['word']if op[0]!='ADD']
  z=replay(actions,w['caches'],route,m['neighbor80_order'],w['source_donors']);value=z[key]if receiver is None else z[key][receiver];assert not value,(label,z)
  results.append({'control':label,'tag':tag,'rejected':True,'X':z['all_original_X_restored'],'Y':z['arbitrary_original_Y_baseline_restored'],'targets':z['target_rows_correct']})
 actions=copy.deepcopy(w['actions']);captures=[x for x in actions if x['tag'].startswith('native-late-5-')];actions=[x for x in actions if x not in captures];idx=next(i for i,x in enumerate(actions)if x['tag']=='early-source-5');actions[idx+1:idx+1]=captures
 z=replay(actions,w['caches'],route,m['neighbor80_order'],w['source_donors']);assert not z['target_rows_correct'][1];results.append({'control':'native_capture_after_source_chart','rejected':True,'reason':'late_target_wrong'})
 actions=copy.deepcopy(w['actions']);next(x for x in actions if x['tag']=='D12-Y-Cauchy')['stage']='X_D'
 try:replay(actions,w['caches'],route,m['neighbor80_order'],w['source_donors'])
 except AssertionError:results.append({'control':'late_D_owner_used_in_early_phase','rejected':True,'reason':'owner_location'})
 else:raise AssertionError('phase control accepted')
 a.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_SEVEN_SHARED_PAIR_NEGATIVE_CONTROLS','controls':results};(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
