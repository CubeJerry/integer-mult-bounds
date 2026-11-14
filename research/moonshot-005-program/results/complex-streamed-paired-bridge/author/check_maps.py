#!/usr/bin/env python3
"""Reuse credited exact signed-phase engines on introduced streamed_paired MOVE pairs."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def need(ok,message):
 if not ok:raise ValueError(message)
def loadmod(root,name):
 p=root/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[name],'retained engine pin');s=importlib.util.spec_from_file_location('streamed_paired_phase_'+name[:-3],p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m

def main(a):
 seed_raw=a.seed.read_bytes();need(hashlib.sha256(seed_raw).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','seed pin');seed=json.loads(gzip.decompress(seed_raw));raw=a.word.read_bytes();w=json.loads(gzip.decompress(raw));need(w['frames'][:len(seed['frames'])]==seed['frames'],'retained literal frame prefix')
 old={(o[2],o[3])for o in seed['program']if o[0]=='MOVE'};new=sorted({(o[2],o[3])for o in w['program']if o[0]=='MOVE'}-old);c=loadmod(a.engines,'clifford_exact.py');v=loadmod(a.engines,'native_verify.py');recipes=[]
 for A,B in new:
  f,g=w['frames'][A],w['frames'][B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))));v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'actual streamed_paired MOVE with signed/global phase');need(recipe['rank']==abs(len(g)-len(f)),'actual nested recursive rank');recipes.append({'source':A,'target':B,'source_frame':f,'target_frame':g,'rank':recipe['rank'],'recipe':recipe})
 need(recipes,'introduced map census');bad=copy.deepcopy(recipes[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase');reject=False
 except ValueError:reject=True
 need(reject,'global phase control');out={'status':'PASS_ALL_STREAMED_PAIRED_INTRODUCED_MAPS','word_sha256':hashlib.sha256(raw).hexdigest(),'engine_pins':PINS,'map_count':len(recipes),'recipes':recipes,'wrong_global_phase_rejected':True,'scope':'Exact finite map lowering via retained engines; reproduction, not independent-agent verification or full uniform physical supplier admission.'};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'],len(recipes))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engines',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
