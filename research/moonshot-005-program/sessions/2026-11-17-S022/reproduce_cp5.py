#!/usr/bin/env python3
"""Rebuild both exact mathematical gates and the full physical all-111 source."""
import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(1<<20):
            h.update(block)
    return h.hexdigest()


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args()
    repo,out=args.repo.resolve(),args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    root=repo/'research/moonshot-005-program'
    results=root/'results';atlas=results/'bit-all111-tight-port-atlas';src=atlas/'author'
    glue=results/'bit-tight-atlas-code-obstruction';quo=results/'bit-tight-atlas-quotient-interfaces'
    rev=atlas/'physical-review';native=root/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    layout=src/'output/LAYOUT.json.gz';record=[]
    def run(command):
        r=subprocess.run(list(map(str,command)),cwd=repo,text=True,capture_output=True)
        if r.returncode:raise RuntimeError(f'{command[0]} failed: {r.stderr[-1200:]}')
        return r.stdout
    def py(script,*argv):
        return run([sys.executable,'-B',script,*argv])
    def check(original,generated):
        if original.read_bytes()!=generated.read_bytes():
            raise ValueError(f'certificate differs: {original}')
        record.append({'scientific_file':str(original.relative_to(root)),'sha256':digest(original)})
    py(src/'layout.py','--native',native,'--out',out/'layout')
    check(src/'output/LAYOUT-RESULT.json',out/'layout/LAYOUT-RESULT.json')
    if gzip.decompress(layout.read_bytes())!=gzip.decompress((out/'layout/LAYOUT.json.gz').read_bytes()):
        raise ValueError('regenerated atlas differs')
    check(layout,out/'layout/LAYOUT.json.gz')
    engines=[
        (atlas/'geometry-review/check.py',['--native',native,'--layout',layout],atlas/'geometry-review/RESULT.json'),
        (glue/'author/check.py',['--repo',repo],glue/'author/RESULT.json'),
        (glue/'author/gauge.py',['--repo',repo],glue/'author/GAUGE.json'),
        (quo/'review/check.py',['--layout',layout],quo/'review/RESULT.json')]
    for idx,(script,opts,original) in enumerate(engines):
        dest=out/f'gate-{idx}.json';py(script,*opts,'--out',dest);check(original,dest)
    for idx,(script,opts,original) in enumerate([
        (glue/'review/check.py',[native],glue/'review/CERTIFICATE.json'),
        (quo/'author/check.py',[native,layout],quo/'author/CERTIFICATE.json')]):
        dest=out/f'proof-{idx}.json';dest.write_text(py(script,*opts));check(original,dest)
    binary=out/'stream.bin'
    py(src/'physical.py','--native',native,'--layout',layout,'--out',out/'physical','--word',binary)
    check(src/'output/PHYSICAL-RESULT.json',out/'physical/PHYSICAL-RESULT.json')
    receipt=json.loads((out/'physical/PHYSICAL-RESULT.json').read_bytes())
    if digest(binary)!=receipt['stream_sha256']:raise ValueError('packed raw operation stream')
    py(rev/'geometry.py','--native',native,'--layout',layout,'--out',out/'tables')
    check(rev/'output/GEOMETRY.json',out/'tables/GEOMETRY.json')
    exe=out/'real-replay'
    run([os.environ.get('CXX','c++'),'-O3','-std=c++17',rev/'replay.cpp','-o',exe])
    dest=out/'ARBITRARY-INPUT.json';dest.write_text(run([exe,binary,out/'tables',-1,111]))
    check(rev/'output/ARBITRARY-INPUT.json',dest)
    (out/'VALIDATION.json').write_text(json.dumps({'status':'PASS','checks':record,'physical_word_sha256':digest(binary),
                    'physical_word_bytes':binary.stat().st_size,'all_original_binary_columns':319680},indent=2)+'\n')
    print('PASS geometry, palette, arbitrary-donor rigidity, middle rank interfaces, full word and all 319680 columns')

if __name__=='__main__':
    main()
