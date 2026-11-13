#!/usr/bin/env python3
"""Read-only integrity check. This checks bytes, not mathematical validity."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
ROOT = P.parents[1]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def check(path, digest):
    need(path.is_file(), f'Missing {path}')
    data = path.read_bytes()
    need(hashlib.sha256(data).hexdigest() == digest, f'SHA256 mismatch: {path}')
    return data

def main():
    provenance = json.loads((P / 'PROVENANCE.json').read_text())
    imported = 0
    for package in provenance['imports']:
        for row in package['files']:
            data = check(ROOT / row['path'], row['sha256'])
            need(len(data) == row['bytes'], f"Size mismatch: {row['path']}")
            header = b'blob ' + str(len(data)).encode() + b'\0'
            need(hashlib.sha1(header + data).hexdigest() == row['git_blob'],
                 f"Git blob mismatch: {row['path']}")
            imported += 1
    manifest = json.loads((P / 'SCIENTIFIC-FILES.json').read_text())
    listed = set()
    for row in manifest['files']:
        data = check(P / row['path'], row['sha256'])
        need(len(data) == row['bytes'], f"Size mismatch: {row['path']}")
        listed.add(row['path'])
    actual = {str(f.relative_to(P)) for f in (P / 'results').rglob('*')
              if f.is_file() and '__pycache__' not in str(f)}
    need(actual == listed, 'Scientific manifest does not cover exactly the result files')
    aliases = {}
    for row in json.loads((P / 'REVIEW-PATHS.json').read_text())['aliases']:
        check(P / row['manifest'], row['manifest_sha256'])
        key = (row['manifest'], row['reviewed_path'])
        need(key not in aliases, f'Duplicate reviewed-path alias: {key}')
        destination = (ROOT / row['repository_path']).resolve()
        need(destination.is_relative_to(ROOT.resolve()),
             f'Review destination leaves repository: {destination}')
        aliases[key] = destination
    used_aliases = set()
    reviewed = 0
    for path in (P / 'results').rglob('REVIEWED-FILES.json'):
        obj = json.loads(path.read_text())
        rows = obj.get('author_files', obj.get('files', obj))
        need(isinstance(rows, dict) and bool(rows),
             f'Empty or unknown reviewed-file manifest: {path}')
        for name, digest in rows.items():
            need(isinstance(digest, str) and len(digest) == 64
                 and all(c in '0123456789abcdef' for c in digest),
                 f'Invalid reviewed digest: {path}: {name}')
            key = (str(path.relative_to(P)), name)
            destination = aliases.get(key, path.parent.parent / name)
            if key in aliases:
                used_aliases.add(key)
            check(destination, digest)
            reviewed += 1
    need(used_aliases == set(aliases), 'Unused reviewed-path alias')
    sources = {
        'research/shared-wire-split-composition/data/final.json.gz':
        '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
        'research/shared-wire-split-composition/FULL-RESULT.json':
        'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7',
        'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz':
        '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78',
    }
    for name, digest in sources.items():
        check(ROOT / name, digest)
    for path in P.rglob('*.json'):
        json.loads(path.read_text())
    print(json.dumps({'status': 'PASS_CHECKPOINT_BYTE_INTEGRITY',
                      'imported_files': imported, 'scientific_files': len(listed),
                      'reviewed_author_pins': reviewed, 'source_pins': len(sources),
                      'explicit_review_relocations': len(used_aliases),
                      'scope': 'Byte identity and record syntax only; not proof verification.'},
                     indent=2))

if __name__ == '__main__':
    main()
