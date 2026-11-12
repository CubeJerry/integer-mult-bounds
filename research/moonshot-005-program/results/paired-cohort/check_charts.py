#!/usr/bin/env python3
"""New paired source chart maps, using explicitly pinned existing engines."""
import argparse,sys,importlib.util,copy
from pathlib import Path
def main(a):
 sys.path.insert(0,str(a.reconstruction));from common import need,load_inputs,sha,gzip,json
 need(__debug__,'retained engines need assertions');s,_,_=load_inputs(a.repo);pb=(a.reconstruction/'eight/WORD.json.gz').read_bytes();p=json.loads(gzip.decompress(pb));wb=(a.output/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(wb));frames=s['frames']+[d['frame'] for d in w['additional_charts']];frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def module(name):
  path=frozen/name;need(sha(path.read_bytes())==pins[name],'engine pin');spec=importlib.util.spec_from_file_location('paired_'+name[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
 c=module('clifford_exact.py');v=module('native_verify.py');old={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};new={(e[2],e[3]) for e in w['program'] if e[0]=='MOVE'};records=[]
 for x,y in sorted(new-old):
  A,B=frames[x],frames[y];recipe,_=c.lower_child(c.canonical_frame(9,tuple(A)).adjoint().then(c.canonical_frame(9,tuple(B))));v.equal(v.recipe(recipe),v.adjoint(v.frame(A,9))+v.frame(B,9),'actual paired map');need(recipe['rank']==len(B)-len(A),'actual paired rank');records.append({'source':x,'target':y,'recipe':recipe})
 need(len(records)==2,'two actual new maps');bad=copy.deepcopy(records[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;rejected=False
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
 except ValueError:rejected=True
 need(rejected,'wrong phase rejected');r={'status':'PASS_PAIRED_INTRODUCED_MAPS','source_sha256':s.get('source_sha256',w['source_sha256']),'parent_word_sha256':sha(pb),'word_sha256':sha(wb),'engine_pins':pins,'original_and_cohort_frames_unchanged':True,'introduced_maps':records,'wrong_global_phase_rejected':True,'scope':'Reused exact engine plus independently implemented signed-Pauli/global-phase checker, not a new engine or physical supplier.'};(a.output/'CHART-MAPS.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'],[(z['source'],z['target']) for z in records])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--reconstruction',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
