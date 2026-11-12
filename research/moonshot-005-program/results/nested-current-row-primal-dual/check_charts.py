#!/usr/bin/env python3
"""Introduced nested-code maps, checked with two credited retained engines."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
def need(v,m):
 if not v:raise ValueError(m)
def main(a):
 need(__debug__,'retained map engines require normal Python')
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/WORD.json.gz';sb=sp.read_bytes();pb=pp.read_bytes();wb=a.word.read_bytes()
 need(hashlib.sha256(sb).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin');need(hashlib.sha256(pb).hexdigest()=='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153','parent pin')
 s=json.loads(gzip.decompress(sb));p=json.loads(gzip.decompress(pb));w=json.loads(gzip.decompress(wb));frames=s['frames']+[r['frame'] for r in w['additional_charts']];frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def module(name):
  path=frozen/name;need(hashlib.sha256(path.read_bytes()).hexdigest()==pins[name],'retained engine pin');spec=importlib.util.spec_from_file_location('nested_'+name[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
 c=module('clifford_exact.py');v=module('native_verify.py');old={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'};new={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};cache={};records=[]
 for x,y in sorted(new-old):
  A,B=tuple(frames[x]),tuple(frames[y])
  for f in [A,B]:
   if f not in cache:cache[f]=c.canonical_frame(9,f)
  recipe,_=c.lower_child(cache[A].adjoint().then(cache[B]));v.equal(v.recipe(recipe),v.adjoint(v.frame(A,9))+v.frame(B,9),'actual nested source map');need(recipe['rank']==len(B)-len(A),'nested source rank');records.append({'source':x,'target':y,'recipe':recipe})
 need(records,'nonvacuous new chart maps');bad=copy.deepcopy(records[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong global phase')
 except ValueError:pass
 else:raise ValueError('accepted phase mutant')
 result={'status':'PASS_ALL_NESTED_INTRODUCED_CHART_MAPS','source_sha256':hashlib.sha256(sb).hexdigest(),'parent_sha256':hashlib.sha256(pb).hexdigest(),'word_sha256':hashlib.sha256(wb).hexdigest(),'engine_pins':pins,'introduced_map_count':len(records),'introduced_maps':records,'wrong_global_phase_rejected':True,'scope':'Credit retained exact Clifford lowering and signed-Pauli/global-phase engines. This is reproduction through existing engines, not a new independent engine or uniform physical supplier.'};a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(records))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['repo','word','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
