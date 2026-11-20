#!/usr/bin/env python3
"""Replay S029 checkpoint 3 packages and match every generated receipt."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--jobs',type=int,default=1)
    p.add_argument('--only')
    a=p.parse_args()
    base=a.repo.resolve()/'research/moonshot-005-program/results'
    dest=a.out.resolve()
    dest.mkdir(parents=True,exist_ok=True)
    P=lambda name:base/name
    prior=P('bit-spread-h263-source')/'author/output/COEFFICIENTS.json.gz'
    k=P('bit-gf64-actual-k-atlas')/'author/output'
    rs=P('bit-spread-rs-physical-word')/'author'
    bg=rs/'source-output/PER-DONOR-COSTS.json'
    f=P('bit-minimum-terminal-storage')
    loc=P('bit-localized-native-addresses')
    pair=P('bit-spread-overlap-source')
    repair=P('bit-spread-singleton-fibre-repair')
    dis=P('bit-spread-disjoint-h-sources')
    packed=P('bit-spread-packed-source-owner-compiler')
    cs=P('bit-spread-source-owner-compiler')
    d=P('bit-minimum-cache-d-atlas')/'author/output/CHARTS.json.gz'
    params=pair/'author/output/PARAMETERS.json'
    coeff=repair/'author/output/SINGLETON-COEFFICIENTS.json.gz'
    plans=[
        ('disjoint',dis/'author/check.py',dis/'author/output',['RESULT.json'],[]),
        ('overlap',pair/'author/check.py',pair/'author/output',['RESULT.json'],[]),
        ('overlap-review',pair/'review/check.py',pair/'review/output',['RESULT.json'],['--parameters',params,'--extended']),
        ('repair',repair/'author/check.py',repair/'author/output',['RESULT.json'],[]),
        ('repair-review',repair/'review/check.py',repair/'review/output',['RESULT.json'],[]),
        ('source-compiler',cs/'author/compile_source.py',cs/'author/output',['RESULT.json'],['--coefficients',prior,'--background',bg]),
        ('pack23',packed/'author/compile_pack.py',packed/'author/output',['RESULT.json'],['--parameters',params,'--background',bg]),
        ('pack24',packed/'author/compile_pack.py',packed/'author/output-24',['RESULT.json'],['--parameters',params,'--background',bg,'--singleton-coefficients',coeff]),
        ('F',f/'author/construct.py',f/'author/output',['RESULT.json','WORDS.json.gz'],['--k-certs',k]),
        ('F-review',f/'review/check.py',f/'review/output',['RESULT.json'],['--k',k,'--f',f/'author/output']),
        ('localized',loc/'author/check.py',loc/'author/output',['RESULT.json'],[]),
        ('localized-review',loc/'review/check.py',loc/'review/output',['RESULT.json'],[]),
        ('eight-copies',rs/'check_transfer.py',rs/'transfer-output',['FULL-COPY-CHECK.json'],['--k-words',k,'--d-charts',d]),
    ]
    def run(item):
        name,script,reference,fns,flags=item
        out=dest/name
        out.mkdir(exist_ok=True)
        env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
        with (dest/(name+'.log')).open('w') as log:
            subprocess.run([sys.executable,'-B',script,'--repo',a.repo.resolve(),'--out',out,*flags],check=True,stdout=log,stderr=subprocess.STDOUT,env=env)
        result={}
        for fn in fns:
            def data(p):
                raw=p.read_bytes()
                return gzip.decompress(raw) if p.suffix=='.gz' else raw
            raw=data(out/fn)
            if raw!=data(reference/fn):
                raise ValueError(name+' '+fn)
            result[fn]=sha256(raw).hexdigest()
        print(name,flush=True)
        return name,result
    active=[x for x in plans if not a.only or x[0]==a.only]
    if not active:raise SystemExit('unknown job')
    with ThreadPoolExecutor(max_workers=a.jobs) as executor:
        results=dict(executor.map(run,active))
    (dest/'VALIDATION.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    main()
