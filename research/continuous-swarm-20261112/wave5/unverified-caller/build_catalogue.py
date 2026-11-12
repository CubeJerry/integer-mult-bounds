#!/usr/bin/env python3
"""Rebuild exact finite recipes and compare all bytes with accepted digests.

This is setup, not a payload operation or a new independent Clifford proof.
The separate retained native interpreter already checked these exact digests.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

from geometry import need

HERE = Path(__file__).resolve().parent


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def accepted(i):
    text = (HERE / 'reference' / f'native-catalogue-{i}.log').read_text()
    return json.loads(text[text.index('{'):])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slice', type=int, choices=range(3))
    ap.add_argument('--merge', action='store_true')
    ap.add_argument('--directory', type=Path, required=True)
    args = ap.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    if args.merge:
        records, mains = [], []
        for i in range(3):
            part = json.loads((args.directory / f'slice-{i}.json').read_text())
            expect = accepted(i)
            need(hashlib.sha256(encoded(part['maps'])).hexdigest()
                 == expect['exact_recipe_digest'], 'accepted complete map slice')
            need(hashlib.sha256(encoded(part['main'])).hexdigest()
                 == expect['main_boundary_digest'], 'accepted main boundaries')
            records += part['maps']
            mains += part['main']
        value = dict(maps=records, main=mains)
        raw = encoded(value) + b'\n'
        target = args.directory / 'catalogue.json.gz'
        target.write_bytes(gzip.compress(raw, mtime=0))
        print(json.dumps(dict(status='PASS_REBUILT_ACCEPTED_CATALOGUE',
             maps=len(records), main=len(mains), uncompressed_bytes=len(raw),
             sha256=hashlib.sha256(target.read_bytes()).hexdigest()), indent=2))
        return
    need(args.slice is not None, 'choose one slice or merge')
    need(not sys.flags.optimize, 'retained constructor assertions enabled')
    path = HERE / 'reference' / 'clifford_exact.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest()
         == '2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
         'retained constructor bytes')
    spec = importlib.util.spec_from_file_location('a5_retained_clifford', path)
    C = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = C
    spec.loader.exec_module(C)
    word = json.loads(gzip.decompress((HERE / 'reference' / 'word.json.gz').read_bytes()))
    main_fields = set(word['live']) | {x+112 for x in word['live']}
    main_fields |= set(word['hosted']['X2']) | set(word['hosted']['Y2'])
    pairs = {(e[2], e[3]) for e in word['program'] if e[0] == 'MOVE'}
    pairs |= {(word['initial'][r], word['final'][r])
              for r in range(word['public']) if r not in main_fields}
    pairs = sorted(pairs)
    expect = accepted(args.slice)
    need(hashlib.sha256(encoded(pairs)).hexdigest() == expect['catalogue_digest'],
         'actual complete map domain')
    charts = {}

    def chart(index):
        if index not in charts:
            charts[index] = C.canonical_frame(9, tuple(word['frames'][index]))
        return charts[index]

    records = []
    for i in range(expect['slice_start'], expect['slice_stop']):
        a, b = pairs[i]
        recipe, _ = C.lower_child(chart(a).adjoint().then(chart(b)))
        need(recipe['rank'] == abs(len(word['frames'][a])-len(word['frames'][b])) > 0,
             'actual positive map rank')
        records.append([a, b, recipe])
    mains = []
    if args.slice == 2:
        for x, q in zip(word['live'], word['ports']):
            a, b = word['initial'][x], word['final'][x+112]
            incoming, _ = C.lower_child(C.cgate(9, q, 1).adjoint().then(chart(a)))
            outgoing, _ = C.lower_child(chart(b).adjoint().then(
                C.cgate(9, q, -1).then(C.fourier(9))))
            need(incoming['rank'] == outgoing['rank'] == 0, 'ordinary main boundaries')
            mains.append([q, incoming, outgoing])
    need(hashlib.sha256(encoded(records)).hexdigest() == expect['exact_recipe_digest'],
         'all generated map bytes equal independently accepted recipes')
    need(hashlib.sha256(encoded(mains)).hexdigest() == expect['main_boundary_digest'],
         'all generated main boundaries equal accepted recipes')
    (args.directory / f'slice-{args.slice}.json').write_bytes(
        encoded(dict(maps=records, main=mains)) + b'\n')
    print(json.dumps(dict(status='PASS_REBUILT_ACCEPTED_SLICE', slice=args.slice,
         maps=len(records), main=len(mains), exact_recipe_digest=expect['exact_recipe_digest']),
         indent=2))


if __name__ == '__main__':
    main()
