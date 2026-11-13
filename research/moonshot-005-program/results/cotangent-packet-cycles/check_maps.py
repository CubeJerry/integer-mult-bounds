#!/usr/bin/env python3
"""Exact Clifford and signed/global-phase check of the new up-return pair."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
    def module(name):
        p=a.repo/'research/shared-wire-split-composition/frozen'/name;assert sha(p.read_bytes())==PINS[name]
        spec=importlib.util.spec_from_file_location('packet_cycle_'+name[:-3],p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
    c,v=module('clifford_exact.py'),module('native_verify.py');pb=(a.parent/'rail-consumer.json.gz').read_bytes();p=json.loads(gzip.decompress(pb));before={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'};maps=[];words=[]
    for path in a.word:
        blob=path.read_bytes();w=json.loads(gzip.decompress(blob));words.append({'path':str(path),'sha256':sha(blob)})
        pairs={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};assert pairs-before=={(3,127)}
    f,g=p['frames'][3],p['frames'][127];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
    v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'actual packet up-return');assert recipe['rank']==9
    bad=copy.deepcopy(recipe);bad['left']['phase']=(bad['left']['phase']+1)%4
    try:v.equal(v.recipe(bad),v.adjoint(v.frame(f,9))+v.frame(g,9),'wrong phase');raise AssertionError('wrong phase accepted')
    except ValueError:pass
    r={'status':'PASS_EXACT_PACKET_CYCLE_UP_RETURN_MAP','parent_rail_sha256':sha(pb),'engine_pins':PINS,'words':words,'source':3,'target':127,'rank':9,'recipe':recipe,'wrong_global_phase_rejected':True,'all_other_pairs_inherited_from_parent':True}
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--word',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
