#!/usr/bin/env python3
"""Check all introduced chart recipes with two pinned existing engines."""
from common import *
import argparse,copy,importlib.util,sys
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def main(a):
 need(__debug__,'retained engines require enabled assertions');s,p,_=load_inputs(a.repo);path=a.repo/'research/shared-wire-split-composition/frozen'
 for name,pin in PINS.items():need(sha((path/name).read_bytes())==pin,'exact engine pin')
 c=module(path/'clifford_exact.py','fresh_coupling_clifford');v=module(path/'native_verify.py','fresh_coupling_native');cache={};recipes={};old={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'}
 for name in list(SELECT) if a.variant=='all' else [a.variant]:
  target=a.output/name;wb=(target/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(wb));frames=s['frames']+[d['frame'] for d in w['additional_charts']];new={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};records=[]
  for x,y in sorted(new-old):
   A,B=tuple(frames[x]),tuple(frames[y]);key=(A,B)
   if key not in recipes:
    for f in (A,B):
     if f not in cache:cache[f]=c.canonical_frame(9,f)
    recipe,_=c.lower_child(cache[A].adjoint().then(cache[B]));v.equal(v.recipe(recipe),v.adjoint(v.frame(A,9))+v.frame(B,9),'new coupling map');recipes[key]=recipe
   recipe=recipes[key];need(recipe['rank']==len(B)-len(A),'actual recursive rank');records.append({'source':x,'target':y,'recipe':recipe})
  need(records,'nonvacuous map coverage');bad=copy.deepcopy(records[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;rejected=False
  try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
  except ValueError:rejected=True
  need(rejected,'wrong phase negative control');result={'status':'PASS_ALL_INTRODUCED_MAPS','source_sha256':SPIN,'parent_sha256':PPIN,'word_sha256':sha(wb),'engine_pins':PINS,'original_frames_unchanged':True,'additional_charts':w['additional_charts'],'introduced_maps':len(records),'recipes':records,'wrong_global_phase_rejected':True,'scope':'Exact reused Clifford lowering and independently implemented signed-Pauli/global-phase engine; not a new independent engine or uniform physical supplier.'};(target/'CHART-MAPS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(name,len(records),'maps checked',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--variant',choices=['all']+list(SELECT),default='all');main(ap.parse_args())
