#!/usr/bin/env python3
"""Exact phase-sensitive recipes for every new ordered source chart pair."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
      'native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
PARENTS={'complete':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
         'partial':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'}
def need(ok,label):
    if not ok:raise ValueError(label)
def module(root,name):
    p=root/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[name],'phase engine pin')
    sp=importlib.util.spec_from_file_location('native_repartition_phase_'+name[:-3],p)
    obj=importlib.util.module_from_spec(sp);sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def main(args):
    raw=args.parent.read_bytes();need(hashlib.sha256(raw).hexdigest()==PARENTS[args.kind],'actual chart-parent pin')
    parent=json.loads(gzip.decompress(raw));raw=args.word.read_bytes();word=json.loads(gzip.decompress(raw))
    need(word['frames'][:len(parent['frames'])]==parent['frames'],'literal retained chart prefix')
    c=module(args.engines,'clifford_exact.py');v=module(args.engines,'native_verify.py')
    old={(op[2],op[3])for op in parent['program']if op[0]=='MOVE'}
    allpairs={(op[2],op[3])for op in word['program']if op[0]=='MOVE'};new=sorted(allpairs-old)
    recipes=[]
    def recipe(a,b):
        f,g=word['frames'][a],word['frames'][b]
        r,_=c.lower_child(c.canonical_frame(9,tuple(f)).adjoint().then(c.canonical_frame(9,tuple(g))))
        v.equal(v.recipe(r),v.adjoint(v.frame(f,9))+v.frame(g,9),'literal source MOVE with signed global phase')
        need(r['rank']==abs(len(g)-len(f)),'exact recursive movement rank')
        return {'source':a,'target':b,'source_frame':f,'target_frame':g,'rank':r['rank'],'recipe':r}
    for a,b in new:recipes.append(recipe(a,b))
    test=copy.deepcopy(recipes[0]if recipes else recipe(*min(allpairs)))
    test['recipe']['left']['phase']=(test['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(test['recipe']),v.adjoint(v.frame(test['source_frame'],9))+v.frame(test['target_frame'],9),'wrong global phase');bad=False
    except ValueError:bad=True
    need(bad,'wrong global phase rejected')
    result={'status':'PASS_ALL_INTRODUCED_ORDERED_CHART_MAPS','word_sha256':hashlib.sha256(raw).hexdigest(),
        'chart_parent_sha256':PARENTS[args.kind],'engine_pins':PINS,'introduced_maps':len(recipes),
        'inherited_ordered_maps_used':len(allpairs&old),'recipes':recipes,'wrong_global_phase_rejected':True,
        'scope':'Finite exact lowering of new ordered maps. Retained chart pairs inherit pinned parent evidence; uniform compiler assumptions remain.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],len(recipes))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
    p.add_argument('--kind',choices=PARENTS,required=True);p.add_argument('--engines',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);main(p.parse_args())
