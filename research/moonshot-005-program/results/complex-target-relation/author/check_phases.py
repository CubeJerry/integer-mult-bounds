#!/usr/bin/env python3
"""Verify all introduced C2 maps with retained exact Clifford/Pauli engines."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def need(x,m):
 if not x:raise ValueError(m)
def module(root,name):
 p=root/name;b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'phase engine pin');s=importlib.util.spec_from_file_location('c2_phase_'+name[:-3],p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
def main(a):
 c=module(a.engines,'clifford_exact.py');v=module(a.engines,'native_verify.py')
 raw=a.word.read_bytes();w=json.loads(gzip.decompress(raw));base=json.loads(gzip.decompress(a.four.read_bytes()));need(hashlib.sha256(a.four.read_bytes()).hexdigest()=='20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f','four pin')
 old={(o[2],o[3]) for o in base['program'] if o[0]=='MOVE'};pairs=sorted({(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'}-old);expected=[] if 'actual-C6-' in w['schema'] else [(1,1125),(99,1125),(1125,127),(1125,1095)];need(pairs==expected,'all introduced physical maps')
 checked_pairs=sorted(set(pairs)|{(int(w['C2_observation']['chart']),127)})
 recipes=[]
 for A,B in checked_pairs:
  f,g=w['frames'][A],w['frames'][B];recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
  v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'actual C2 map');need(recipe['rank']==abs(len(g)-len(f)),'rank');recipes.append({'source':A,'destination':B,'rank':recipe['rank'],'recipe':recipe,'source_frame':f,'target_frame':g})
 bad=copy.deepcopy(recipes[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 rejected=False
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase')
 except ValueError:rejected=True
 need(rejected,'global phase mutant must fail')
 result={'status':'PASS_ALL_INTRODUCED_MIXED_RETURN_PHASE_MAPS','word_sha256':hashlib.sha256(raw).hexdigest(),'engine_pins':PINS,'introduced_pairs':pairs,'maps':recipes,'wrong_global_phase_rejected':True,'scope':'All introduced finite chart maps and the map for the new return operation, including inherited map reuse; other old maps inherit predecessor verification.'};a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--engines',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--four',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
