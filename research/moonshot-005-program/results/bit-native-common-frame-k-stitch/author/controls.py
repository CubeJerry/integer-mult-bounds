#!/usr/bin/env python3
"""Frame/interface controls that retain correct original-X/Y baselines."""
from common import *
import copy
def restore_inverses(actions):
 early=[a['word']for a in actions if a['stage']in ['X_H','X_D','X_K']or a['stage']=='X_NATIVE'and a['tag'].startswith('joint-source-')]
 late=[a['word']for a in actions if a['stage']in ['Y_H','Y_D','Y_K']or a['stage']=='Y_F'and not a['tag'].startswith('F80-cancel-')]
 next(a for a in actions if a['tag']=='restore-all-X')['word']=[op for word in reversed(early)for op in reversed(word)]
 next(a for a in actions if a['tag']=='inverse-arbitrary-Y')['word']=[op for word in reversed(late)for op in reversed(word)]
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rr=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(rr).hexdigest()==PINS['routes'];route={fid(r[0],r[1],r[2]):r for r in map(json.loads,rr.splitlines())};w=json.loads(gzip.decompress(a.word.read_bytes()));c=json.loads(gzip.decompress(a.certificate.read_bytes()));results=[]
 for name in ['D_frame_row_order','early_K_missing_tile','late_K_missing_tile','final_frame_weight','native_capture_order']:
  actions=copy.deepcopy(w['actions']);receiver=80
  if name=='D_frame_row_order':
   fields=[next(f for f,r in route.items()if r[0]=='X'and r[4]==12 and r[5]==k)for k in [370,371]];next(x for x in actions if x['tag']=='Cauchy-X-12')['word']+=swap_field(*fields)
  elif name in ['early_K_missing_tile','late_K_missing_tile']:
   kind='X'if name.startswith('early')else'Y';receiver=80 if kind=='X'else 1;act=next(x for x in actions if x['tag']==f'aggregate-{kind}-K-370');assert all(op[0]=='ADD'for op in act['word'][-5:]);act['word']=act['word'][:-5]
  elif name=='final_frame_weight':
   act=next(x for x in actions if x['tag']=='capture-F80-frame-0');cache=act['word'][0][1]//5;src=next(x['output_field']for x in c['early_K_aggregates']if x['K']==370);act['word']+=add_field(cache,src)
  else:
   receiver=1;captures=[x for x in actions if x['tag'].startswith('capture-12-7-')];assert len(captures)==4;actions=[x for x in actions if x not in captures];index=next(k for k,x in enumerate(actions)if x['tag']=='joint-source-7');actions[index+1:index+1]=captures
  restore_inverses(actions);z=replay(actions,w['caches'],route,c['neighbor80_order'],w['source_donors']);assert z['all_original_X_restored']and z['arbitrary_original_Y_baseline_restored']and not z['target_rows_correct'][receiver],(name,z)
  results.append({'control':name,'rejected':True,'all_X_restored':True,'all_Y_baseline_identity':True,'target_rows':z['target_rows_correct']})
 failed=[]
 for j in w['shared_donors']:
  copies=sum(1 for x in c['matrices']if x['donor']==j);u=rows80(c['neighbor80_order'],j);assert reduce(u*copies)==4<4*copies;failed.append({'donor':j,'target_only_rank':4,'required_early_rank':4*copies})
 results.append({'control':'independent_target_only_tile_lifts','rejected':True,'failures':failed})
 a.out.mkdir(parents=True,exist_ok=True);out={'status':'PASS_SIX_FRAME_SOURCE_NEGATIVE_CONTROLS','controls':results};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({**out,'controls':[{k:v for k,v in x.items()if k!='failures'}for x in results]},indent=2))
if __name__=='__main__':main()
