#!/usr/bin/env python3
"""Isolated reproduction of the funded paired prefix source and complete bill."""
from __future__ import annotations
import argparse, gzip, json, subprocess, sys
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)

def main(args):
    here=Path(__file__).resolve().parent;repo=args.repo.resolve()
    old=repo/'research/moonshot-005-program/results/complex-omitted-line-gram/author'
    need(not args.work.exists(),'work directory must be new');args.work.mkdir(parents=True)
    commands=[]
    def run(argv):
        command=[sys.executable,'-I','-B',*map(str,argv)]
        result=subprocess.run(command,capture_output=True,text=True)
        commands.append({'command':command,'exit_code':result.returncode})
        need(result.returncode==0,result.stderr or result.stdout)
    def compare(name):
        got=json.loads((args.work/name).read_text());expected=json.loads((here/name).read_text())
        need({k:v for k,v in got.items() if k!='word_sha256'}=={k:v for k,v in expected.items() if k!='word_sha256'},'scientific receipt '+name)
        return got
    run([here/'check_algebra.py','--output',args.work/'ALGEBRA.json']);compare('ALGEBRA.json')
    run([here/'build.py','--native',here/'dependencies/native.json.gz','--seed',old/'output/WORD.json.gz','--engine',old/'dependencies/replay.py','--codec',old/'build.py','--flag',here/'FLAG.json','--output',args.work/'output'])
    source=compare('output/RESULT.json')
    need(gzip.decompress((args.work/'output/WORD.json.gz').read_bytes())==gzip.decompress((here/'output/WORD.json.gz').read_bytes()),'canonical source payload')
    run([here/'price.py','--full',here/'dependencies/FULL-RESULT.json','--engine',old/'dependencies/interval.py','--receipt',args.work/'output/RESULT.json','--output',args.work/'output/PRICE.json']);price=compare('output/PRICE.json')
    run([here/'check_maps.py','--seed',old/'output/WORD.json.gz','--word',args.work/'output/WORD.json.gz','--engines',old/'dependencies','--output',args.work/'output/PHASES.json']);phase=compare('output/PHASES.json')
    receipt={'status':'PASS_ISOLATED_FUNDED_PREFIX_REPRODUCTION','commands':commands,'canonical_payload_sha256':source['payload_sha256'],'source_bill':source['source_bill'],'phase_maps':phase['map_count'],'first_positive_fixed_m':price['first_positive_fixed_m'],'classification':'Author reproduction using pinned predecessor utilities; independent review and complete supplier admission remain separate. No new kappa.'}
    (args.work/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(receipt['status'],phase['map_count'],'exact chart maps')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--work',type=Path,required=True);main(p.parse_args())
