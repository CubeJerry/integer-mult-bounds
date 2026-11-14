#!/usr/bin/env python3
"""Exact lowering of every new public chart map in the transient codec."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def need(c,m):
 if not c:raise ValueError(m)
def mod(root,name):
 p=root/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[name],'retained phase engine pin');s=importlib.util.spec_from_file_location('transient_phase_'+name[:-3],p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--engines',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.word.read_bytes();w=json.loads(gzip.decompress(raw));rawp=a.parent.read_bytes();need(hashlib.sha256(rawp).hexdigest()=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','parent pin');q=json.loads(gzip.decompress(rawp));old={(o[2],o[3]) for o in q['program'] if o[0]=='MOVE'};new=sorted({(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'}-old)
 c=mod(a.engines,'clifford_exact.py');v=mod(a.engines,'native_verify.py');recipes=[]
 for A,B in new:
  f,g=w['frames'][A],w['frames'][B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))));v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'actual transient public MOVE');need(recipe['rank']==abs(len(g)-len(f)),'actual complete recursive rank');recipes.append({'source':A,'target':B,'source_frame':f,'target_frame':g,'rank':recipe['rank'],'recipe':recipe})
 need(recipes,'nonempty introduced map census');bad=copy.deepcopy(recipes[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;rejected=False
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase')
 except ValueError:rejected=True
 need(rejected,'global phase negative control')
 out={'status':'PASS_ALL_TRANSIENT_CODEC_INTRODUCED_CHART_MAPS','word_sha256':hashlib.sha256(raw).hexdigest(),'engine_pins':PINS,'new_maps':new,'map_count':len(recipes),'recipes':recipes,'wrong_global_phase_rejected':True,'scope':'Exact finite chart maps only; original source, full-field, physical compiler and uniform supplier foundations retained.'};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'],len(recipes))
