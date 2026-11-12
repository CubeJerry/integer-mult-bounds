#!/usr/bin/env python3
"""Eight actual initial rank-one maps, checked by two pinned retained engines."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def need(ok,why):
    if not ok: raise ValueError(why)
def sha(b): return hashlib.sha256(b).hexdigest()
def main(a):
    need(__debug__,'retained engines require assertions')
    base=a.repo/'research/shared-wire-split-composition'
    sb=(base/'data/final.json.gz').read_bytes()
    need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
    s=json.loads(gzip.decompress(sb)); wb=(a.output/'WORD.json.gz').read_bytes(); w=json.loads(gzip.decompress(wb))
    def mod(filename):
        path=base/'frozen'/filename;need(sha(path.read_bytes())==PINS[filename],'engine pin')
        spec=importlib.util.spec_from_file_location('coupled8_'+filename[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
    c,v=mod('clifford_exact.py'),mod('native_verify.py');records=[]
    for p in w['coupled_precondition']['preloads']:
        A,B=s['frames'][3],s['frames'][p['line']]
        recipe,_=c.lower_child(c.canonical_frame(9,tuple(A)).adjoint().then(c.canonical_frame(9,tuple(B))))
        v.equal(v.recipe(recipe),v.adjoint(v.frame(A,9))+v.frame(B,9),'preterminal input route')
        need(recipe['rank']==1,'rank-one source route')
        records.append({'source':3,'target':p['line'],'coupled_X':p['X'],'recipe':recipe})
    need(len(records)==8,'eight maps')
    bad=copy.deepcopy(records[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
    rejected=False
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(s['frames'][3],9))+v.frame(s['frames'][bad['target']],9),'wrong global phase')
    except ValueError:rejected=True
    need(rejected,'wrong global phase control')
    result={'status':'PASS_EIGHT_PRETERMINAL_RANK_ONE_MAPS','source_sha256':sha(sb),'word_sha256':sha(wb),'engine_pins':PINS,'maps':records,'wrong_global_phase_rejected':True,'scope':'Exact retained Clifford lowering checked by separately implemented signed-Pauli/global-phase engine; not new all-size physical supplier.'}
    (a.output/'CHART-MAPS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
