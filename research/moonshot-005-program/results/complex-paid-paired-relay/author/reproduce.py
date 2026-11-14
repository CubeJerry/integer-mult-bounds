#!/usr/bin/env python3
"""Reproduce paired-relay source evidence in a new isolated output directory."""
from __future__ import annotations
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)
def main(a):
 here=Path(__file__).resolve().parent;repo=a.repo.resolve();old=repo/'research/moonshot-005-program/results/complex-omitted-line-gram/author';need(not a.work.exists(),'work directory must be new');a.work.mkdir(parents=True)
 commands=[]
 def run(argv):
  cmd=[sys.executable,'-I','-B',*map(str,argv)];p=subprocess.run(cmd,capture_output=True,text=True);commands.append({'command':cmd,'exit_code':p.returncode});need(p.returncode==0,p.stderr or p.stdout);return p.stdout
 run([here/'check_algebra.py','--output',a.work/'ALGEBRA.json']);need(json.loads((a.work/'ALGEBRA.json').read_text())==json.loads((here/'ALGEBRA.json').read_text()),'algebra receipt semantics')
 fields=['status','seed_word_sha256','native_sha256','payload_sha256','donors','receivers','rank_one_coefficients_removed_each_side','all400_input_rank','all_final_charts_equal_seed','all_original_D_restored','hosted_R_plus_L_transpose_zero','mode','relay_contents_restored','relay_initial_rows','relay_final_location_contract','relay_home_return_claimed','source_bill','raw_histogram','owned_histogram','raw_rank_mass','current_a_forward_offdiagonal_coefficients','original_coordinate_forward_debt','reverse_residual_rank','new_complete_public_target_rows','negative_controls','scope']
 results=[]
 for mode in ['dirty_echo','zero_echo','zero_roundtrip','zero_erasure','zero_output_cleanup']:
  folder=mode.replace('_','-');dest=a.work/folder
  run([here/'build.py','--seed',old/'output/WORD.json.gz','--native',here/'dependencies/native.json.gz','--engine',old/'dependencies/replay.py','--output',dest,'--mode',mode])
  got=json.loads((dest/'RESULT.json').read_text());expected=json.loads((here/folder/'RESULT.json').read_text());need(all(got[k]==expected[k]for k in fields),'source scientific receipt '+mode)
  need(gzip.decompress((dest/'WORD.json.gz').read_bytes())==gzip.decompress((here/folder/'WORD.json.gz').read_bytes()),'canonical source payload '+mode)
  run([here/'price.py','--full',here/'dependencies/FULL-RESULT.json','--engine',old/'dependencies/interval.py','--receipt',dest/'RESULT.json','--output',dest/'PRICE.json'])
  gp=json.loads((dest/'PRICE.json').read_text());ep=json.loads((here/folder/'PRICE.json').read_text());need({k:v for k,v in gp.items()if k!='word_sha256'}=={k:v for k,v in ep.items()if k!='word_sha256'},'signed invoice '+mode)
  run([here/'check_maps.py','--seed',old/'output/WORD.json.gz','--word',dest/'WORD.json.gz','--engines',old/'dependencies','--output',dest/'PHASES.json'])
  gm=json.loads((dest/'PHASES.json').read_text());em=json.loads((here/folder/'PHASES.json').read_text());need({k:v for k,v in gm.items()if k!='word_sha256'}=={k:v for k,v in em.items()if k!='word_sha256'},'signed map recipes '+mode)
  results.append({'mode':mode,'payload_sha256':got['payload_sha256'],'source_bill':got['source_bill'],'phase_maps':gm['map_count']})
 receipt={'status':'PASS_ISOLATED_PAIRED_RELAY_REPRODUCTION','source_checks':results,'commands':commands,'classification':'Author reproduction, not independent mathematical review or a new complete multiplication theorem.'};(a.work/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(receipt['status'],len(results),'source variants')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--work',type=Path,required=True);main(p.parse_args())
