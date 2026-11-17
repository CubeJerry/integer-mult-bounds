#!/usr/bin/env python3
"""Reproduce S020 checkpoint 1; evidence is separate from universal proofs.

Run with Python 3.11+ and SymPy installed. All other checks use the standard
library. Output is an explicit fresh directory; committed evidence is read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Use an empty output directory')
    out.mkdir(parents=True, exist_ok=True)
    programme = repo / 'research/moonshot-005-program'
    session = programme / 'sessions/2026-11-17-S020'
    evidence = session / 'checkpoint1-evidence'
    native = programme / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    old_word = programme / 'sessions/2026-11-17-S019/checkpoint3-evidence/A/native57-masked-hub/WORD.json'
    word = evidence / 'A/direct-known57/WORD.json'
    entropy = evidence / 'R/entropy54/CERTIFICATE.json'
    nine = evidence / 'A/immutable-code-gate/CERTIFICATE.json'
    flag = evidence / 'R/canonical-flag-gate/output/CERTIFICATE.json'
    pins = json.loads((session / 'SOURCE-PINS-CP1.json').read_text())
    for item in pins['files']:
        if digest(repo / item['path']) != item['sha256']:
            raise ValueError('Source pin mismatch: ' + item['path'])

    commands = [
        ('author-source', evidence / 'A/build_all54_source.py',
         ['--repo', repo, '--matching', evidence / 'A/ALL54-MATCHING.json']),
        ('independent-source', evidence / 'R/review_all54_source.py',
         ['--repo', repo, '--word', word]),
        ('static-linear', evidence / 'C/static54-rank9/check.py',
         ['--repo', repo]),
        ('entropy-dual', evidence / 'R/entropy54/check.py',
         ['--repo', repo, '--certificate', entropy]),
        ('independent-entropy', evidence / 'C/entropy54-review/check.py',
         ['--native', native, '--certificate', entropy,
          '--old-word', old_word, '--new-word', word]),
        ('nine-packet', evidence / 'A/check_immutable_code_gate.py',
         ['--repo', repo, '--source-word', word]),
        ('independent-nine-packet', evidence / 'C/immutable-code-review/check.py',
         ['--native', native, '--word', word, '--certificate', nine]),
        ('any-packet-flag', evidence / 'R/canonical-flag-gate/check.py',
         ['--repo', repo, '--word', word]),
        ('independent-any-packet-flag', evidence / 'C/canonical-flag-review/check.py',
         ['--native', native, '--word', word, '--certificate', flag]),
        ('ordinary-capacity', evidence / 'C/ordinary-module-capacity/check.py', []),
        ('independent-ordinary-capacity', evidence / 'B/capacity-independent-review/check.py',
         ['--source', evidence / 'C/ordinary-module-capacity']),
    ]
    records = []
    for name, script, options in commands:
        command = [sys.executable, '-B', str(script), *map(str, options),
                   '--out', str(out / name)]
        completed = subprocess.run(command, cwd=repo, capture_output=True, text=True)
        (out / (name + '.log')).write_text(completed.stdout + completed.stderr)
        record = {'name': name, 'script': str(script.relative_to(repo)),
                  'script_sha256': digest(script), 'exit_code': completed.returncode}
        records.append(record)
        print(name, 'PASS' if completed.returncode == 0 else 'FAIL', flush=True)
        if completed.returncode:
            print(completed.stderr[-5000:])
            raise RuntimeError('Reproduction failed: ' + name)

    comparisons = [
        ('author-source/WORD.json', 'A/direct-known57/WORD.json'),
        ('author-source/CUT-INVENTORY.json', 'A/direct-known57/CUT-INVENTORY.json'),
        ('static-linear/CERTIFICATE.json', 'C/static54-rank9/output/CERTIFICATE.json'),
        ('entropy-dual/RESULT.json', 'R/entropy54/output/RESULT.json'),
        ('independent-entropy/EXPANDED-DUAL.json', 'C/entropy54-review/output/EXPANDED-DUAL.json'),
        ('nine-packet/CERTIFICATE.json', 'A/immutable-code-gate/CERTIFICATE.json'),
        ('any-packet-flag/CERTIFICATE.json', 'R/canonical-flag-gate/output/CERTIFICATE.json'),
        ('ordinary-capacity/ALGEBRAIC-CONTROLS.json', 'C/ordinary-module-capacity/output/ALGEBRAIC-CONTROLS.json'),
    ]
    reproduced = []
    for fresh, frozen in comparisons:
        actual = digest(out / fresh)
        expected = digest(evidence / frozen)
        if actual != expected:
            raise ValueError('Exact reproduction mismatch: ' + frozen)
        reproduced.append({'path': frozen, 'sha256': actual})
    result = {
        'status': 'PASS_S020_CHECKPOINT1_FOCUSED_REPRODUCTION',
        'checks': records,
        'exact_reproductions': reproduced,
        'source_pins_sha256': digest(session / 'SOURCE-PINS-CP1.json'),
        'interpretation': 'Reexecution confirms frozen evidence. Independent mathematical reviews are separately attributed; rerunning an author checker is not independent proof.',
        'new_complete_kappa': False,
    }
    (out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])


if __name__ == '__main__':
    main()
