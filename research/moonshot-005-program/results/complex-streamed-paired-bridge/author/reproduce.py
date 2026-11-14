#!/usr/bin/env python3
"""Reproduce streamed-paired source evidence in a new isolated output directory."""
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
 results=[]
 for mode in ['streaming','independent']:
  folder=mode.replace('_','-');dest=a.work/folder
  run([here/'build.py','--seed',old/'output/WORD.json.gz','--native',here/'dependencies/native.json.gz','--engine',old/'dependencies/replay.py','--output',dest,'--mode',mode])
  got=json.loads((dest/'RESULT.json').read_text());expected=json.loads((here/folder/'RESULT.json').read_text());need({k:v for k,v in got.items()if k!='word_sha256'}=={k:v for k,v in expected.items()if k!='word_sha256'},'source scientific receipt '+mode)
  need(gzip.decompress((dest/'WORD.json.gz').read_bytes())==gzip.decompress((here/folder/'WORD.json.gz').read_bytes()),'canonical source payload '+mode)
  run([here/'price.py','--full',here/'dependencies/FULL-RESULT.json','--engine',old/'dependencies/interval.py','--receipt',dest/'RESULT.json','--output',dest/'PRICE.json'])
  gp=json.loads((dest/'PRICE.json').read_text());ep=json.loads((here/folder/'PRICE.json').read_text());need({k:v for k,v in gp.items()if k!='word_sha256'}=={k:v for k,v in ep.items()if k!='word_sha256'},'signed invoice '+mode)
  run([here/'check_maps.py','--seed',old/'output/WORD.json.gz','--word',dest/'WORD.json.gz','--engines',old/'dependencies','--output',dest/'PHASES.json'])
  gm=json.loads((dest/'PHASES.json').read_text());em=json.loads((here/folder/'PHASES.json').read_text());need({k:v for k,v in gm.items()if k!='word_sha256'}=={k:v for k,v in em.items()if k!='word_sha256'},'signed map recipes '+mode)
  results.append({'mode':mode,'payload_sha256':got['payload_sha256'],'source_bill':got['source_bill'],'phase_maps':gm['map_count']})
 run([here/'preflight.py','--native',here/'dependencies/native.json.gz','--seed',old/'output/WORD.json.gz','--engine',old/'dependencies/replay.py','--price',a.work/'streaming/PRICE.json','--output',a.work/'PREFLIGHT.json'])
 need(json.loads((a.work/'PREFLIGHT.json').read_text())==json.loads((here/'PREFLIGHT.json').read_text()),'global separated-bridge preflight')
 receipt={'status':'PASS_ISOLATED_STREAMED_PAIRED_REPRODUCTION','source_checks':results,'global_preflight':'PASS_COUPLED_CORRECTION_AND_SEPARATED_BRIDGE_PREFLIGHT','commands':commands,'classification':'Author reproduction, not independent mathematical review or a new complete multiplication theorem.'};(a.work/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(receipt['status'],len(results),'source variants')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--work',type=Path,required=True);main(p.parse_args())
