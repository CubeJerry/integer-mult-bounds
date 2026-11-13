#!/usr/bin/env python3
"""Authenticate every new standalone-rail chart map, including global phase."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

PINS = {
    'clifford_exact.py': '2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
    'native_verify.py': '3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38',
}
PARENT_PIN = 'ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
WORD_PIN = '90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2'

def need(value, message):
    if not value:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main(args):
    need(__debug__, 'Frozen Clifford modules require assertions enabled')
    p = args.repo/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz'
    pb, wb = p.read_bytes(), (args.output/'rail-repaired.json.gz').read_bytes()
    need(digest(pb) == PARENT_PIN, 'Parent source pin')
    need(digest(wb) == WORD_PIN, 'Standalone word pin')
    parent, word = [json.loads(gzip.decompress(b)) for b in (pb, wb)]
    def module(name):
        path = args.repo/'research/shared-wire-split-composition/frozen'/name
        need(digest(path.read_bytes()) == PINS[name], 'Exact engine pin')
        spec = importlib.util.spec_from_file_location('rail_'+name[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod
    c, v = module('clifford_exact.py'), module('native_verify.py')
    old = {(o[2],o[3]) for o in parent['program'] if o[0] == 'MOVE'}
    new = {(o[2],o[3]) for o in word['program'] if o[0] == 'MOVE'}
    frames, receipts = word['frames'], []
    for a,b in sorted(new-old):
        f,g = frames[a], frames[b]
        recipe,_ = c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
        v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'standalone downward repair map')
        need(recipe['rank'] == abs(len(g)-len(f)) == 1, 'Exact downward rank')
        receipts.append({'source':a,'target':b,'recipe':recipe})
    need(len(receipts) == 6, 'Every one of the six new maps covered')
    mutant = copy.deepcopy(receipts[0])
    mutant['recipe']['left']['phase'] = (mutant['recipe']['left']['phase']+1)%4
    rejected = False
    try:
        v.equal(v.recipe(mutant['recipe']),v.adjoint(v.frame(frames[mutant['source']],9))+v.frame(frames[mutant['target']],9),'wrong phase')
    except ValueError:
        rejected = True
    need(rejected, 'Wrong global phase must fail')
    result = {'status':'PASS_STANDALONE_RAIL_CHART_MAPS','word_sha256':digest(wb),'parent_sha256':digest(pb),
              'engine_pins':PINS,'inherited_distinct_pairs':len(new&old),'new_distinct_pairs':len(receipts),
              'new_maps':receipts,'wrong_global_phase_rejected':rejected,
              'scope':'Exact frozen chart conventions; uniform compiler and physical primitives remain assumptions.'}
    (args.output/'CHART-MAPS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'], result['new_distinct_pairs'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    main(parser.parse_args())
