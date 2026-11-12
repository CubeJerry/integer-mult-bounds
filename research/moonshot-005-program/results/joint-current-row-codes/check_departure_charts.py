#!/usr/bin/env python3
"""Exact phase/rank receipts for changed quotient-departure maps."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
 if not q:raise ValueError(m)
def main(a):
 need(__debug__,'retained assertions needed');sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');s=json.loads(gzip.decompress(sb));pb=(a.parent/'WORD.json.gz').read_bytes();wb=(a.output/'WORD.json.gz').read_bytes();p,w=[json.loads(gzip.decompress(b)) for b in [pb,wb]];need(w['parent_word_sha256']==sha(pb),'actual changed parent');frames=s['frames']+[x['frame'] for x in w['additional_charts']]
 def mod(fn):
  f=a.repo/'research/shared-wire-split-composition/frozen'/fn;need(sha(f.read_bytes())==PINS[fn],'engine pin');spec=importlib.util.spec_from_file_location('departure_'+fn[:-3],f);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
 c,v=mod('clifford_exact.py'),mod('native_verify.py');before={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'};after={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};maps=[]
 for A,B in sorted(after-before):
  f,g=frames[A],frames[B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))));v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'quotient departure map');need(recipe['rank']==len(g)-len(f),'actual ascending rank');maps.append({'source':A,'target':B,'recipe':recipe})
 need(maps,'changed map coverage');bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;rejected=False
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
 except ValueError:rejected=True
 need(rejected,'phase mutant rejected');r={'status':'PASS_QUOTIENT_DEPARTURE_CHART_MAPS','source_sha256':sha(sb),'parent_word_sha256':sha(pb),'word_sha256':sha(wb),'engine_pins':PINS,'maps':maps,'map_count':len(maps),'wrong_global_phase_rejected':True};(a.output/'CHART-MAPS.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'],len(maps))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
