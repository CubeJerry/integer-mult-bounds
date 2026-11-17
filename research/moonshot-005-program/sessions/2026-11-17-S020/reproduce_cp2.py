#!/usr/bin/env python3
"""Reproduce S020 checkpoint2, using Python 3.11+ with SymPy installed.

Use a fresh output directory. Frozen evidence is read-only. Exact finite
reexecution supports, but does not replace, the separately reviewed proofs.
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
    parser.add_argument('--only', action='append', help='Run selected named checks; default runs all')
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Use an empty output directory')
    out.mkdir(parents=True, exist_ok=True)
    session = repo / 'research/moonshot-005-program/sessions/2026-11-17-S020'
    evidence = session / 'checkpoint2-evidence'
    pins_path = session / 'SOURCE-PINS-CP2.json'
    for pin in json.loads(pins_path.read_text())['files']:
        if digest(repo / pin['path']) != pin['sha256']:
            raise ValueError('Source pin mismatch: ' + pin['path'])
    author = evidence / 'A'
    one = author / 'quartet-source-ground/WORD.json'
    two = author / 'hierarchy-source-ground/WORD.json'
    half = evidence / 'R/half-sum-code-gate/output/CERTIFICATE.json'
    commands = [
        ('author-hub', author / 'build_quartet_compression_source.py',
         ['--repo', repo]),
        ('author-ground', author / 'build_quartet_compression_source.py',
         ['--repo', repo, '--ground-code']),
        ('author-hierarchy', author / 'build_hierarchical_quartet_source.py',
         ['--repo', repo, '--ground-code']),
        ('independent-hub', evidence / 'R/review_quartet_sources.py',
         ['--repo', repo, '--word', author / 'quartet-source-hub/WORD.json', '--kind', 'hub']),
        ('independent-ground', evidence / 'R/review_quartet_sources.py',
         ['--repo', repo, '--word', one, '--kind', 'ground']),
        ('independent-hierarchy', evidence / 'R/review_quartet_sources.py',
         ['--repo', repo, '--word', two, '--kind', 'hierarchical']),
        ('coordinate-gate', evidence / 'R/canonical-coordinate-gate/check.py',
         ['--repo', repo, '--one-stage', one, '--two-stage', two]),
        ('independent-coordinate-gate', author / 'check_fixed_cut_raw_extension_gate.py',
         ['--inputs', author]),
        ('half-sum-gate', evidence / 'R/half-sum-code-gate/check.py',
         ['--repo', repo, '--word', two]),
        ('independent-half-sum-gate', author / 'review_half_sum_gate.py',
         ['--inputs', author, '--author-certificate', half]),
        ('klein-interface', evidence / 'B/klein-three-bank-interface/check.py',
         ['--repo', repo]),
        ('independent-klein-interface', evidence / 'C/klein-interface-review/check.py',
         ['--repo', repo, '--author', evidence / 'B/klein-three-bank-interface']),
        ('author-fourplane', author / 'build_four_plane_correction.py',
         ['--repo', repo]),
        ('independent-fourplane', evidence / 'C/four-plane-review/check.py',
         ['--native', author / 'SOURCE-RECOVERY.json',
          '--word', author / 'four-plane-correction/WORD.json']),
    ]
    selected = set(args.only or [row[0] for row in commands])
    if not selected <= {row[0] for row in commands}:
        raise ValueError('Unknown selected check')
    records = []
    for name, script, options in commands:
        if name not in selected:
            continue
        command = [sys.executable, '-B', str(script), *map(str, options),
                   '--out', str(out / name)]
        completed = subprocess.run(command, cwd=repo, capture_output=True, text=True)
        (out / (name + '.log')).write_text(completed.stdout + completed.stderr)
        records.append({'name': name, 'script': str(script.relative_to(repo)),
                        'script_sha256': digest(script), 'exit_code': completed.returncode})
        print(name, 'PASS' if completed.returncode == 0 else 'FAIL', flush=True)
        if completed.returncode:
            print(completed.stderr[-5000:])
            raise RuntimeError('Reproduction failed: ' + name)

    comparisons = []
    for name, folder in [('hub', 'quartet-source-hub'), ('ground', 'quartet-source-ground'),
                         ('hierarchy', 'hierarchy-source-ground')]:
        for filename in ['WORD.json', 'CUT-INVENTORY.json', 'RESULT.json']:
            comparisons.append((f'author-{name}/{filename}', f'A/{folder}/{filename}'))
    for name, folder in [('hub', 'hub'), ('ground', 'ground'), ('hierarchy', 'hierarchical')]:
        for filename in ['RESULT.json', 'SOURCE-CONTRACT.json']:
            comparisons.append((f'independent-{name}/{filename}',
                                f'R/quartet-source-review/{folder}/{filename}'))
    comparisons += [
        ('coordinate-gate/CERTIFICATE.json', 'R/canonical-coordinate-gate/output/CERTIFICATE.json'),
        ('independent-coordinate-gate/FIXED-CUT-RAW-EXTENSION-REVIEW.json', 'A/coordinate-gate-reproduction/FIXED-CUT-RAW-EXTENSION-REVIEW.json'),
        ('half-sum-gate/CERTIFICATE.json', 'R/half-sum-code-gate/output/CERTIFICATE.json'),
        ('independent-half-sum-gate/RESULT.json', 'A/half-sum-gate-review/RESULT.json'),
        ('klein-interface/WORDS.json', 'B/klein-three-bank-interface/WORDS.json'),
        ('klein-interface/RESULT.json', 'B/klein-three-bank-interface/RESULT.json'),
        ('independent-klein-interface/CHARACTERS.json', 'C/klein-interface-review/output/CHARACTERS.json'),
        ('independent-klein-interface/TABLES.json', 'C/klein-interface-review/output/TABLES.json'),
        ('author-fourplane/WORD.json', 'A/four-plane-correction/WORD.json'),
        ('author-fourplane/RESULT.json', 'A/four-plane-correction/RESULT.json'),
        ('author-fourplane/CUT-INVENTORY.json', 'A/four-plane-correction/CUT-INVENTORY.json'),
        ('independent-fourplane/RESULT.json', 'C/four-plane-review/output/RESULT.json'),
        ('independent-fourplane/INDEPENDENT-CUT.json', 'C/four-plane-review/output/INDEPENDENT-CUT.json'),
    ]
    reproduced = []
    for fresh, frozen in comparisons:
        if fresh.split('/')[0] not in selected:
            continue
        actual = digest(out / fresh)
        if actual != digest(evidence / frozen):
            raise ValueError('Exact reproduction mismatch: ' + frozen)
        reproduced.append({'path': frozen, 'sha256': actual})
    result = {
        'status': 'PASS_S020_CHECKPOINT2_FOCUSED_REPRODUCTION',
        'checks': records, 'exact_reproductions': reproduced,
        'source_pins_sha256': digest(pins_path),
        'independence': 'Source author A is reviewed by root. Root code gates are independently reviewed by A using different elimination/enumeration. B Klein interface is reviewed by C without B engine imports. Reexecution itself is not independent proof.',
        'new_complete_kappa': False,
    }
    (out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], len(reproduced), 'byte-identical outputs')


if __name__ == '__main__':
    main()
