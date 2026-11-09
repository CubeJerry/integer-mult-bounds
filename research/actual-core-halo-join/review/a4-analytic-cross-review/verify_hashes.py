#!/usr/bin/env python3
"""Recheck only the exact sources of an independent analytic review.

Prepared for @CubeJerry with substantial OpenAI assistance.
No reviewed module is imported; no numerical or physical payload is executed.
"""
import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    need(path.is_file() and not path.is_symlink(), 'regular file: ' + str(path))
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest(),
                git_blob=sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest_path = here / 'SOURCE-HASHES.json'
    manifest = json.loads(manifest_path.read_text())
    need(manifest['physical_execution_performed'] is False, 'hash-only scope')
    need(manifest['implementation_sources_stable'] is True, 'implementation source stability')
    need(manifest['reviewed_final_sources'] is True, 'final source review completed')
    dependencies = {row['retained']: row for row in
                    json.loads((args.package / 'DEPENDENCIES.json').read_text())['files']}
    paths = set()
    primary, retained = {}, 0
    for row in manifest['files']:
        name = row['path']
        relative = Path(name)
        need(not relative.is_absolute() and '..' not in relative.parts, 'relative source path')
        need(name not in paths, 'distinct review source path')
        paths.add(name)
        actual = digest(args.package / relative)
        for key, value in actual.items():
            need(row[key] == value, 'reviewed bytes changed: ' + name + ' ' + key)
        if 'initial_sha256' in row:
            if actual['sha256'] == row['initial_sha256']:
                need(row['stable_since_start'] is True, 'initial source stability flag')
            else:
                need(name == 'PROOF.md' and row['stable_since_start'] is False
                     and row.get('reviewed_documentation_revision') is True,
                     'unreviewed primary source change: ' + name)
                revisions = [r for r in manifest['reviewed_revisions'] if r['path'] == name]
                need(len(revisions) == 1 and revisions[0]['old_sha256'] == row['initial_sha256']
                     and revisions[0]['new_sha256'] == actual['sha256'],
                     'exact reviewed documentation revision')
            primary[name] = actual['sha256']
        if 'retained_origin' in row:
            pinned = dependencies[name]
            for key, value in actual.items():
                need(pinned[key] == value, 'retained dependency pin: ' + name + ' ' + key)
            for key, value in row['retained_origin'].items():
                need(pinned[key] == value, 'retained source origin: ' + name + ' ' + key)
            retained += 1
    need(set(primary) == {'PROOF.md', 'attachment.py', 'format_bridge.py', 'source_geometry.py'},
         'complete four-primary-file review')
    print(json.dumps(dict(
        disposition='PASS: exact reviewed bytes; analytic derivation is written in REVIEW.md',
        checked_files=len(paths), retained_pins_matched=retained,
        implementation_sources_stable=True, primary_sources=primary,
        reviewed_documentation_revisions=manifest['reviewed_revisions'],
        physical_execution_performed=False, complete_physical_acceptance=False,
        review_sha256=digest(here / 'REVIEW.md')['sha256'],
        manifest_sha256=digest(manifest_path)['sha256'],
        verifier_sha256=digest(Path(__file__).resolve())['sha256'],
    ), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
