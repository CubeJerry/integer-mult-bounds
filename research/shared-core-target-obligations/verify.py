"""Replay all independent finite checks against pinned external source files."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def run(word, invoice):
    completed = []
    cases = [('exact_matrix.js', 'MATRIX-RESULT.json'),
             ('exact_invoice.js', 'INVOICE-RESULT.json')]
    for script, result in cases:
        got = json.loads(subprocess.check_output(['node', str(HERE/script)], text=True))
        if got != json.loads((HERE/result).read_text()):
            raise ValueError(script+' differs from committed receipt')
        completed.append({'script': script, 'runtime': 'node', 'status': got['status']})
    cases = [('source_census.py', 'CENSUS-RESULT.json', ['--word', str(word), '--invoice', str(invoice)]),
             ('selector_witness.py', 'SELECTOR-RESULT.json', ['--word', str(word)]),
             ('hub_witness.py', 'HUB-RESULT.json', ['--word', str(word)])]
    for script, result, args in cases:
        expected = json.loads((HERE/result).read_text())
        for optimize in (False, True):
            cmd = [sys.executable]+(['-O'] if optimize else [])+[str(HERE/script)]+args
            got = json.loads(subprocess.check_output(cmd, text=True))
            if got != expected:
                raise ValueError(script+' differs from committed receipt')
            completed.append({'script': script, 'optimized': optimize, 'status': got['status']})
    programs = ['exact_matrix.js', 'exact_invoice.js', 'source_census.py',
                'selector_witness.py', 'hub_witness.py', 'verify.py']
    return {'status': 'PASS_SHARED_CORE_INDEPENDENT_PACKAGE', 'executions': completed,
            'program_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                               for name in programs},
            'word_sha256': hashlib.sha256(word.read_bytes()).hexdigest(),
            'invoice_sha256': hashlib.sha256(invoice.read_bytes()).hexdigest(),
            'scope': 'Finite source correspondence, exact algebra/profile arithmetic, and scoped repair witnesses; no H4 word, physical supplier admission or new kappa.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--word', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/data/final.json.gz')
    p.add_argument('--invoice', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/FULL-RESULT.json')
    args = p.parse_args()
    print(json.dumps(run(args.word, args.invoice), indent=2))
