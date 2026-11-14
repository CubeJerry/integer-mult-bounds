#!/usr/bin/env python3
"""Exact signed-Clifford lowering of every new singular-Gram chart pair."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path

PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
      'native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
SEED='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'
def need(ok,message):
    if not ok:raise ValueError(message)
def module(root,name):
    path=root/name;need(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[name],'retained phase engine pin')
    spec=importlib.util.spec_from_file_location('singular_gram_phase_'+name[:-3],path)
    result=importlib.util.module_from_spec(spec);sys.modules[spec.name]=result;spec.loader.exec_module(result);return result
def main(args):
    raw=args.seed.read_bytes();need(hashlib.sha256(raw).hexdigest()==SEED,'seed word pin');seed=json.loads(gzip.decompress(raw))
    raw=args.word.read_bytes();word=json.loads(gzip.decompress(raw));need(word['frames'][:len(seed['frames'])]==seed['frames'],'literal retained chart prefix')
    c=module(args.engines,'clifford_exact.py');v=module(args.engines,'native_verify.py')
    old={(op[2],op[3])for op in seed['program']if op[0]=='MOVE'}
    new=sorted({(op[2],op[3])for op in word['program']if op[0]=='MOVE'}-old);recipes=[]
    for a,b in new:
        f,g=word['frames'][a],word['frames'][b]
        recipe,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
        v.equal(v.recipe(recipe),v.adjoint(v.frame(f,9))+v.frame(g,9),'actual singular-Gram MOVE including global phase')
        need(recipe['rank']==abs(len(g)-len(f)),'true nested recursive rank')
        recipes.append({'source':a,'target':b,'source_frame':f,'target_frame':g,'rank':recipe['rank'],'recipe':recipe})
    need(recipes,'actual introduced chart pairs')
    bad=copy.deepcopy(recipes[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase');rejected=False
    except ValueError:rejected=True
    need(rejected,'wrong global phase rejected')
    out={'status':'PASS_ALL_SINGULAR_GRAM_HISTORY_INTRODUCED_MAPS','word_sha256':hashlib.sha256(raw).hexdigest(),
         'native_basis_ports':word['singular_history']['native_basis_ports'],'engine_pins':PINS,'map_count':len(recipes),'recipes':recipes,
         'wrong_global_phase_rejected':True,'scope':'Exact finite source chart recipes via retained engines; reproduction, not independent review or uniform supplier admission.'}
    args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'],len(recipes))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
    p.add_argument('--engines',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
