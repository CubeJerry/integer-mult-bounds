#!/usr/bin/env python3
"""Exact rank/global-phase recipes for the actual kernel-reunion chart."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
    def module(name):
        p=a.repo/'research/shared-wire-split-composition/frozen'/name;assert sha(p.read_bytes())==PINS[name];spec=importlib.util.spec_from_file_location('kernel_lane_'+name[:-3],p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
    c,v=module('clifford_exact.py'),module('native_verify.py');pb=(a.parent/'rail-consumer.json.gz').read_bytes();assert sha(pb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc';p=json.loads(gzip.decompress(pb));old={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'};maps={};words=[]
    for path in a.word:
        blob=path.read_bytes();w=json.loads(gzip.decompress(blob));pairs={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'}-old;words.append({'sha256':sha(blob),'new_pairs':sorted(pairs)})
        for A,B in pairs:
            if (A,B) in maps:continue
            f,g=w['frames'][A],w['frames'][B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
            v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'kernel-lane actual map');assert recipe['rank']==len(g)-len(f)
            maps[A,B]={'source':A,'target':B,'rank':recipe['rank'],'recipe':recipe,'source_frame':f,'target_frame':g}
    assert len(maps)==6;bad=copy.deepcopy(next(iter(maps.values())));bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase');raise AssertionError('wrong phase accepted')
    except ValueError:pass
    r={'status':'PASS_EXACT_KERNEL_LANE_CHART_MAPS','parent_rail_sha256':sha(pb),'engine_pins':PINS,'words':words,'maps':list(maps.values()),'wrong_global_phase_rejected':True};a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'],len(maps))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--word',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
