#!/usr/bin/env python3
"""Exact introduced chart maps for parked dual slots, using retained engines."""
import argparse
import copy
import gzip
import importlib.util
import json
import sys
from pathlib import Path


def main(a):
    sys.path.insert(0, str(a.reconstruction))
    from common import load_inputs, need, sha
    need(__debug__, 'retained engines require enabled assertions')
    s, _, _ = load_inputs(a.repo)
    pb = a.parent.read_bytes()
    p = json.loads(gzip.decompress(pb))
    wb = (a.output / 'WORD.json.gz').read_bytes()
    w = json.loads(gzip.decompress(wb))
    need(sha(pb) == w['parent_word_sha256'], 'literal parent pin')
    need(p['additional_charts'] == w['additional_charts'], 'all frame declarations inherited unchanged')
    frames = s['frames'] + [d['frame'] for d in w['additional_charts']]
    pins = {'clifford_exact.py': '2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
            'native_verify.py': '3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}

    def module(name):
        path = a.repo / 'research/shared-wire-split-composition/frozen' / name
        need(sha(path.read_bytes()) == pins[name], 'retained engine pin')
        spec = importlib.util.spec_from_file_location('ghost_' + name[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod

    c = module('clifford_exact.py')
    v = module('native_verify.py')
    old = {(e[2], e[3]) for e in p['program'] if e[0] == 'MOVE'}
    new = {(e[2], e[3]) for e in w['program'] if e[0] == 'MOVE'}
    records = []
    for x, y in sorted(new - old):
        A, B = frames[x], frames[y]
        recipe, _ = c.lower_child(c.canonical_frame(9, tuple(A)).adjoint().then(
                                  c.canonical_frame(9, tuple(B))))
        v.equal(v.recipe(recipe), v.adjoint(v.frame(A, 9)) + v.frame(B, 9),
                'actual parked original map')
        need(recipe['rank'] == len(B) - len(A) == 8, 'actual direct parked rank-eight ascent')
        records.append({'source': x, 'target': y, 'recipe': recipe})
    need(len(records) == len(w['parked_dual_ghosts']['records']), 'exact new map coverage')
    bad = copy.deepcopy(records[0])
    bad['recipe']['left']['phase'] = (bad['recipe']['left']['phase'] + 1) % 4
    rejected = False
    try:
        v.equal(v.recipe(bad['recipe']), v.adjoint(v.frame(frames[bad['source']], 9)) +
                v.frame(frames[bad['target']], 9), 'wrong phase')
    except ValueError:
        rejected = True
    need(rejected, 'wrong global phase rejected')
    result = {'status': 'PASS_PARKED_ORIGINAL_INTRODUCED_MAPS',
              'word_sha256': sha(wb), 'parent_word_sha256': sha(pb),
              'engine_pins': pins, 'all_declared_frames_unchanged': True,
              'introduced_maps': records, 'wrong_global_phase_rejected': True,
              'scope': 'Retained exact Clifford lowering and independent signed-Pauli/phase '
                       'engine reused and credited. No physical supplier admission.'}
    (a.output / 'CHART-MAPS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'], [(x['source'], x['target']) for x in records])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--reconstruction', type=Path, required=True)
    p.add_argument('--parent', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
