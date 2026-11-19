#!/usr/bin/env python3
"""Source and baseline omission controls on the literal binary word."""
import argparse,gzip,json
from collections import Counter
from hashlib import sha256
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 raw=gzip.decompress(args.word.read_bytes());word=json.loads(raw)
 matrices=json.loads(gzip.decompress(args.word.with_name('MATRICES.json.gz').read_bytes()))
 rp=args.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
 assert sha256(gzip.decompress(rp.read_bytes())).hexdigest()==word['public_route_pin']
 public=111*480*2*5;xend=111*480*5;ymask=((1<<public)-1)^((1<<xend)-1);expected={}
 for t in matrices['target_bit_supports']:
  v=1<<t['output_bit']
  for b in t['source_bit_indices']:v^=1<<b
  expected[t['output_bit']]=v
 def replay(omit):
  state={};owned=set();counts=Counter();dirty=0;peak=0
  def get(b):return state.get(b,1<<b)if b<public else state[b]
  for action in word['actions']:
   if action['tag']==omit:continue
   for op in action['word']:
    counts[op[0]]+=1
    if op[0]=='ADD':state[op[1]]=get(op[1])^get(op[2])
    elif op[0]=='INIT':assert op[1]not in owned;owned.add(op[1]);state[op[1]]=0;peak=max(peak,len(owned))
    elif op[0]=='CLEAR':assert op[1]in owned;dirty+=bool(state[op[1]]);owned.remove(op[1]);del state[op[1]]
    else:raise AssertionError(op)
  return {'X_restored':all(v==1<<b for b,v in state.items()if b<xend),'Y_baseline_identity':all(v&ymask==1<<b for b,v in state.items()if xend<=b<public),'exact_selected_target':all(get(b)==v for b,v in expected.items()),'all_owned_cleared':not owned,'ADD':counts['ADD'],'INIT':counts['INIT'],'CLEAR':counts['CLEAR'],'dirty_CLEAR':dirty,'peak_extra':peak}
 good=replay(None)
 assert all(good[k]for k in ['X_restored','Y_baseline_identity','exact_selected_target','all_owned_cleared'])
 assert [good[k]for k in ['ADD','INIT','CLEAR','dirty_CLEAR','peak_extra']]==[32190,340,340,340,340]
 tests=[('restore-all-X','X_restored'),('inverse-arbitrary-Y-baseline','Y_baseline_identity'),('late-H-86-0','exact_selected_target'),('D-cross-12','exact_selected_target'),('final-early-add-0','exact_selected_target')];results=[]
 for tag,failed in tests:
  assert any(a['tag']==tag for a in word['actions']);r=replay(tag);assert not r[failed],(tag,r)
  results.append({'omitted':tag,'required_failure':failed,'result':r})
 out={'status':'PASS_NATIVE_D4_TARGET_TILE_OMISSION_CONTROLS','word_decompressed_sha256':sha256(raw).hexdigest(),'complete_word':good,'omission_controls':results,'new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
