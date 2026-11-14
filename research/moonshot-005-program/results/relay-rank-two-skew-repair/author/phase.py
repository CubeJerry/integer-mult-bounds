#!/usr/bin/env python3
"""Reuse authenticated independent Clifford engines for the sole new chart pair."""
from pathlib import Path
import argparse,copy,gzip,hashlib,importlib.util,json,sys
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
WORD='b32bffe0f86e12257ebb29f019b25b4c421d7ba31b8c260458937ac27a7b324c'
def need(c,m):
 if not c:raise ValueError(m)
def load(base,name):
 p=base/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[name],'retained engine hash');spec=importlib.util.spec_from_file_location('rank_two_phase_'+name[:-3],p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
pa=argparse.ArgumentParser();pa.add_argument('--engines',type=Path,required=True);pa.add_argument('--word',type=Path,required=True);pa.add_argument('--output',type=Path,required=True);args=pa.parse_args();raw=args.word.read_bytes();need(hashlib.sha256(raw).hexdigest()==WORD,'literal forward word pin');w=json.loads(gzip.decompress(raw));need(sum(e[0]=='MOVE'and e[2:4]==[127,3]and e[4] for e in w['program'])==2,'both literal new descents')
c=load(args.engines,'clifford_exact.py');v=load(args.engines,'native_verify.py');A,B=127,3;f,g=w['frames'][A],w['frames'][B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))));v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'rank-two forward moment MOVE');need(recipe['rank']==9,'full rank-nine descendant');bad=copy.deepcopy(recipe);bad['left']['phase']=(bad['left']['phase']+1)%4;rejected=False
try:v.equal(v.recipe(bad),v.adjoint(v.frame(f,9))+v.frame(g,9),'wrong global phase')
except ValueError:rejected=True
need(rejected,'signed phase control')
out={'status':'PASS_NEW_RANK_NINE_SIGNED_CHART_MAP','word_sha256':WORD,'engine_pins':PINS,'source_chart':A,'target_chart':B,'source_frame':f,'target_frame':g,'literal_occurrences':2,'rank':9,'recipe':recipe,'wrong_global_phase_rejected':True,'scope':'Exact finite signed Clifford map using retained engines; physical uniform supplier foundations remain.'};args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
