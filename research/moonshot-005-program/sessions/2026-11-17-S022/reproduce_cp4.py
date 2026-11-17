#!/usr/bin/env python3
"""Rebuild and compare all S022 fourth-checkpoint scientific outputs."""
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
    old_bit = programme / 'results/bit-six-receiver-cross-chart-carriers'
    bit = programme / 'results/bit-eight-layered-receivers'
    cx = programme / 'results/complex-joint-spectator-additions'
    parent = programme / 'results/complex-spectator-preserving-interface/author'
    jobs = []
    for name,subdir,flags in [('seven','seven',['--single']),('eight','output',[])]:
        dest = out / name
        jobs.append((name, bit/'author/build.py', ['--native',native,'--utility',old_bit/'cross-chart/build.py','--out',dest,*flags],
                     [(bit/'author'/subdir/f,dest/f) for f in ['WORD.json','RESULT.json']]))
    jobs.extend([
        ('layered-independent',bit/'review/check.py',['--repo',repo,'--engine',old_bit/'review/check.py','--seven',bit/'author/seven/WORD.json','--eight',bit/'author/output/WORD.json','--out',out/'layered-review'],
         [(bit/'review/output/RESULT.json',out/'layered-review/RESULT.json')]),
        ('second-spectator',cx/'second/check.py',['--parent',parent,'--out',out/'second'],
         [(cx/'second/output/RESULT.json',out/'second/RESULT.json')]),
        ('joint-spectator',cx/'joint/check.py',['--parent',parent,'--second',cx/'second','--out',out/'joint'],
         [(cx/'joint/output/RESULT.json',out/'joint/RESULT.json')]),
        ('review-second',cx/'review/injection.py',['--out',out/'injection.json'],
         [(cx/'review/INJECTION-RESULT.json',out/'injection.json')]),
        ('review-joint',cx/'review/joint.py',['--out',out/'joint-review.json'],
         [(cx/'review/JOINT-RESULT.json',out/'joint-review.json')])])
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
