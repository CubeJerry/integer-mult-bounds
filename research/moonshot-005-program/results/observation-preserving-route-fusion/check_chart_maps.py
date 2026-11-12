#!/usr/bin/env python3
"""Authenticate every introduced fused map with the pinned exact chart engines."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

ENGINE_PINS = {
    'clifford_exact.py': '2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
    'native_verify.py': '3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main(args):
    need(__debug__, 'Retained exact Clifford compiler requires assertions enabled')
    package = args.repo / 'research/shared-wire-split-composition'
    paths = {name: package / 'frozen' / name for name in ('clifford_exact.py', 'native_verify.py')}
    for name, path in paths.items():
        need(hashlib.sha256(path.read_bytes()).hexdigest() == ENGINE_PINS[name], 'retained exact engine pin: ' + name)
    c = load(paths['clifford_exact.py'], 'fusion_pinned_clifford')
    v = load(paths['native_verify.py'], 'fusion_pinned_native')
    source_bytes = (package / 'data/final.json.gz').read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'native pin')
    native = json.loads(gzip.decompress(source_bytes))
    parent = json.loads(gzip.decompress(args.parent.read_bytes()))
    word_bytes = args.word.read_bytes()
    word = json.loads(gzip.decompress(word_bytes))
    old = {(e[2], e[3]) for e in parent['program'] if e[0] == 'MOVE'}
    new = {(e[2], e[3]) for e in word['program'] if e[0] == 'MOVE'}
    introduced = sorted(new - old)
    charts = {}
    records = []
    start = time.monotonic()
    def chart(index):
        if index not in charts:
            charts[index] = c.canonical_frame(9, tuple(native['frames'][index]))
        return charts[index]
    for index, (a, b) in enumerate(introduced):
        recipe, _ = c.lower_child(chart(a).adjoint().then(chart(b)))
        expected = v.adjoint(v.frame(native['frames'][a], 9)) + v.frame(native['frames'][b], 9)
        v.equal(v.recipe(recipe), expected, 'introduced fused chart map')
        need(recipe['rank'] == len(native['frames'][b]) - len(native['frames'][a]), 'exact lowered recursive rank')
        records.append({'source': a, 'target': b, 'recipe': recipe})
        if index % 25 == 0:
            print('checked', index + 1, 'of', len(introduced), 'introduced maps', flush=True)
    need(records, 'nonvacuous introduced maps')
    bad = copy.deepcopy(records[0]['recipe'])
    bad['left']['phase'] = (bad['left']['phase'] + 1) % 4
    a, b = records[0]['source'], records[0]['target']
    rejected = False
    try:
        v.equal(v.recipe(bad), v.adjoint(v.frame(native['frames'][a], 9)) + v.frame(native['frames'][b], 9), 'wrong global phase')
    except ValueError:
        rejected = True
    need(rejected, 'wrong phase negative control')
    receipt = dict(status='PASS_ALL_INTRODUCED_FUSION_CHART_MAPS', source_sha256=hashlib.sha256(source_bytes).hexdigest(),
                   parent_sha256=hashlib.sha256(args.parent.read_bytes()).hexdigest(), word_sha256=hashlib.sha256(word_bytes).hexdigest(),
                   engine_pins={name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()},
                   old_maps=len(old), new_maps=len(new), introduced_maps=len(introduced), retired_maps=len(old-new),
                   recipes=records, wrong_global_phase_rejected=rejected,
                   method='Retained exact Clifford compiler plus its separately implemented signed-Pauli/global-phase checker, reused explicitly; this is not a new independent engine or an all-column physical supplier proof.')
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['status'], len(introduced), 'elapsed', round(time.monotonic()-start, 2), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--parent', type=Path, required=True)
    ap.add_argument('--word', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args())
