#!/usr/bin/env python3
"""Rebuild and compare all S022 second-checkpoint scientific outputs."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    programme = repo / 'research/moonshot-005-program'
    native = programme / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    bit = programme / 'results/bit-six-receiver-cross-chart-carriers'
    cx = programme / 'results/complex-spectator-preserving-interface'
    jobs = []
    for kind in ['point-backed', 'cross-chart']:
        dest = out / kind
        jobs.append((kind, bit/kind/'build.py', ['--native', native, '--out', dest],
                     [(bit/kind/'output'/f, dest/f) for f in ['RESULT.json','WORD.json']]))
    jobs.extend([
        ('global-gate',bit/'cross-chart/global_gate.py',['--native',native,'--out',out/'GATE.json'],
         [(bit/'cross-chart/output/GLOBAL-GATE.json',out/'GATE.json')]),
        ('independent-bit',bit/'review/check.py',['--repo',repo,'--package','signed-points',bit/'point-backed',
         '--package','cross-chart-relay',bit/'cross-chart','--out',out/'independent-bit'],
         [(bit/'review/output/RESULT.json',out/'independent-bit/RESULT.json')]),
        ('complex',cx/'author/check.py',['--repo',repo,'--out',out/'complex'],
         [(cx/'author/output/RESULT.json',out/'complex/RESULT.json')]),
        ('independent-complex',cx/'review/check.py',['--out',out/'complex-review.json'],
         [(cx/'review/RESULT.json',out/'complex-review.json')]),
        ('independent-parabolic',cx/'review/parabolic.py',['--out',out/'parabolic-review.json'],
         [(cx/'review/PARABOLIC-RESULT.json',out/'parabolic-review.json')])])
    payload={'status':'PASS','python':platform.python_version(),'checks':[]}
    for label,script,options,files in jobs:
        result = subprocess.run([sys.executable,'-B',str(script), *map(str,options)],cwd=repo,capture_output=True,text=True)
        if result.returncode: raise RuntimeError(f'{label}: {result.stderr[-1200:]}')
        assertions=[]
        for frozen,generated in files:
            old,new=frozen.read_bytes(),generated.read_bytes()
            if json.loads(old)!=json.loads(new): raise ValueError(f'Changed scientific output: {frozen}')
            assertions.append({'path':str(frozen.relative_to(programme)),'sha256':hashlib.sha256(old).hexdigest(),'byte_equal':old==new})
        payload['checks'].append({'label':label,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'outputs':assertions})
        print(label, 'PASS', flush=True)
    (out/'VALIDATION.json').write_text(json.dumps(payload,indent=2)+'\n')
if __name__=='__main__':
    main()
