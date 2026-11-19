#!/usr/bin/env python3
"""Explicit semantic and owner-location negative controls."""
import argparse,copy,gzip,json
from pathlib import Path
from build import fid,replay,PINS
from hashlib import sha256
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--routing',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 r=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(r).hexdigest()==PINS['routes']
 route={fid(x[0],x[1],x[2]):x for x in map(json.loads,r.splitlines())};word=json.loads(gzip.decompress(a.word.read_bytes()));cert=json.loads(gzip.decompress(a.routing.read_bytes()))
 controls=[]
 cases=[('no_hub_inverse','restore-all-X','all_original_X_restored'),('no_ground_inverse','inverse-arbitrary-Y-baseline','arbitrary_original_Y_baseline_restored'),('no_first_native_injection','inject-native-8-0','all_62_donor_target_rows_exact'),('no_flow_accumulation','final-flow-accumulation','all_62_donor_target_rows_exact'),('no_one_H_permutation',next(x['tag']for x in word['actions']if x['tag'].startswith('flow-H-')),'all_62_donor_target_rows_exact')]
 for label,tag,key in cases:
  actions=copy.deepcopy(word['actions']);found=False
  for act in actions:
   if act['tag']==tag:act['word']=[op for op in act['word']if op[0]!='ADD'];found=True
  assert found
  z=replay(actions,word['caches'],route,cert['all_neighbors']);assert not z[key],(label,z)
  controls.append({'control':label,'omitted_ADD_tag':tag,'required_failure':key,'rejected':True,'all_X':z['all_original_X_restored'],'all_Y':z['arbitrary_original_Y_baseline_restored'],'target':z['all_62_donor_target_rows_exact']})
 for label,tag,chart in [('native_cache_relocated','inject-native-8-0',['L',9]),('flow_permutation_relocated',next(x['tag']for x in word['actions']if x['tag'].startswith('flow-D-')),['D',12])]:
  actions=copy.deepcopy(word['actions']);next(x for x in actions if x['tag']==tag)['chart']=chart
  try:replay(actions,word['caches'],route,cert['all_neighbors'])
  except AssertionError:controls.append({'control':label,'rejected':True,'reason':'owner_location'})
  else:raise AssertionError(label)
 a.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_SEVEN_NEGATIVE_CONTROLS','controls':controls};(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
