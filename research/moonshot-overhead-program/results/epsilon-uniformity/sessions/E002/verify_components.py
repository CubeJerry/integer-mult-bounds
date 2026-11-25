#!/usr/bin/env python3
"""Isolated finite component replays; no claim of a complete machine test."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
CHECKS = [
    'route-a/verify_height_streams.py',
    'route-c/verify_small_radix.py',
    'route-c/verify_succinct_cyclic.py',
    'route-b/verify_rational_walsh.py',
    'lead/verify_spectral_repair.py',
]

def main():
    results = []
    for name in CHECKS:
        source = ROOT / name
        with tempfile.TemporaryDirectory(prefix='epsilon-e002-') as directory:
            work = Path(directory)
            script = work / source.name
            shutil.copy2(source, script)
            start = time.monotonic()
            run = subprocess.run([sys.executable, str(script)], cwd=work,
                                 text=True, capture_output=True, timeout=180)
            receipts = {p.name: json.loads(p.read_text()) for p in work.glob('*.json')}
            item = {'source':name, 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'exit_code':run.returncode, 'wall_seconds':time.monotonic()-start,
                    'receipts':receipts, 'stdout':run.stdout, 'stderr':run.stderr}
            results.append(item)
            print(name, 'PASS' if run.returncode == 0 else 'FAIL', flush=True)
            if run.returncode:
                print(run.stdout, run.stderr, flush=True)
                break
    output = {'status':'PASS' if len(results)==len(CHECKS) and all(x['exit_code']==0 for x in results) else 'FAIL',
              'python':sys.version, 'claims':'Exact finite component identities and adverse controls only; no full machine execution or asymptotic/formal certification.',
              'runs':results}
    (ROOT/'lead-component-replays.json').write_text(json.dumps(output, indent=2)+'\n')
    if output['status'] != 'PASS':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
