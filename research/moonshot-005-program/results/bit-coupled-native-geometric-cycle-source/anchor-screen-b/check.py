#!/usr/bin/env python3
"""Exact all-plane propagation screen of the frozen width-three cycle sources."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import numpy as np

def need(ok,message):
    if not ok:raise ValueError(message)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def point_map(ctx,centre,j):
    f=ctx.arith;roots=ctx.binary.roots
    a,b=(roots[x] for x in sorted(ctx.H[centre])[:2])
    out={}
    for h in ctx.stars[j]:
        if h==centre:continue
        points={roots[u]^(a if f.b8(roots[u],b) else 0)^(b if f.b8(roots[u],a) else 0) for u in ctx.H[h]-{j}}
        need(len(points)==1,'off-plane projection is well-defined')
        out[h]=points.pop()
    need(len(out)==len(set(out.values()))==27,'geometric source-point bijection')
    return out

def main():
    cli=ArgumentParser(description=__doc__);cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    base=args.repo/'research/moonshot-005-program/results'
    pins=json.loads(Path(__file__).with_name('SOURCE-PINS.json').read_bytes())
    for name,digest in pins.items():need(sha256((base/name).read_bytes()).hexdigest()==digest,'inherited independent source '+name)
    parent=base/'bit-coupled-native-geometric-cycle-source/component/output'
    expected={'COEFFICIENTS.json':'ccb6bf73cca1fe793fa5ec20d6c2007e8f886a518b57451a11bb19a85f7d1fee',
              'PARAMETERS.json':'a9a34bcad5866ac3d3facf1953b2543279a8d5920760c38bdd26b64b59756dec'}
    for name,digest in expected.items():need(sha256((parent/name).read_bytes()).hexdigest()==digest,'frozen literal cycle '+name)
    raw=json.loads((parent/'COEFFICIENTS.json').read_bytes());params=json.loads((parent/'PARAMETERS.json').read_bytes())
    builder=load(base/'bit-coupled-native-geometric-h-source/review-b/construct.py','independent_geometry_and_fields')
    ctx=builder.context(args.repo,args.out/'geometry')
    arithmetic=load(base/'bit-array-anchor-degeneracy/applications/review-b/check.py','independent_reverse_kernel_arithmetic')
    library=args.out/'reverse-linear64.so';cpp=base/'bit-array-anchor-degeneracy/applications/review-b/linear64.cpp'
    subprocess.run(['c++','-O3','-std=c++17','-shared','-fPIC',str(cpp),'-o',str(library)],check=True)
    F=arithmetic.IndependentField(library,ctx.field.product)
    arrays={int(j):{int(h):np.array(A,dtype=np.uint8) for h,A in maps.items()} for j,maps in raw.items()}
    need(sorted(arrays)==[0,25,26,45,47,61,62,100], 'all eight frozen anchors')
    singletons={next(iter(H&set(range(111)))) for H in ctx.H if len(H&set(range(111)))==1}
    eligible=set(range(111))-singletons-{10};need(len(eligible)==99 and set(arrays)<=eligible,'ordinary anchor scope')
    pair_plane={tuple(sorted(pair)):h for h,H in enumerate(ctx.H) for pair in itertools.combinations(H,2)}
    results=[];cuts=0;native_cuts=0
    for j,maps in sorted(arrays.items()):
        need(set(maps)==set(ctx.stars[j]) and all(A.shape==(3,48) for A in maps.values()),'complete width-three source array')
        for r in ctx.perp[j]:
            view=np.vstack([maps[h] for h in ctx.views[j,r]])
            need(F.rank(view)==48,'entire geometric source cut');cuts+=1;native_cuts+=(r<111)
        kernels={};families={};ranks={}
        for h in ctx.stars[j]:
            for r in sorted(ctx.perp[j]&set(range(111))-{80}):
                if h not in ctx.views[j,r]:continue
                off=np.vstack([maps[q] for q in ctx.views[j,r] if q!=h])
                K=F.kernel(off,3);need(F.rank(F.mm(maps[h],K))==3,'central block restores full source rank')
                kernels[h,r]=K
            for R in ctx.stars[j]:
                if R==h:continue
                receivers=[r for hh,r in kernels if hh==h and R in ctx.views[j,r]]
                need(receivers,'nonempty native pair family')
                need(all(not np.any(F.mm(maps[R],kernels[h,r])) for r in receivers),'pair span lies in actual R kernel')
                families[h,R]=receivers;ranks[h,R]=F.rank(np.hstack([kernels[h,r] for r in receivers]))
        projections={h:{leaf:point_map(ctx,h,leaf) for leaf in sorted(ctx.H[h]&eligible)} for h in ctx.stars[j]}
        candidates=[(h,leaf) for h in ctx.stars[j] for leaf in sorted((ctx.H[h]&eligible)-{j})]
        witness=None;tries=0
        for (h1,left),(h2,right) in itertools.combinations(candidates,2):
            if h1==h2 or left==right:continue
            h3=pair_plane.get(tuple(sorted((left,right))))
            if h3 is None or len({h1,h2,h3})!=3:continue
            final_receivers=[r for r in range(111) if r!=80 and ctx.H[h3]<=ctx.perp[r] and j not in ctx.perp[r]]
            inverse=[{x:q for q,x in projections[h][j].items()} for h in (h1,h2)]
            for i in final_receivers:
                tries+=1;branches=[];mapped=[];good=True
                for side,(h,leaf) in enumerate(((h1,left),(h2,right))):
                    qs=[Q for Q in ctx.views[leaf,i] if Q!=h3]
                    need(len(qs)==15 and h not in qs,'fifteen actual final off-centre leaf quotients')
                    entries=[];transferred=[]
                    for Q in qs:
                        R=inverse[side][projections[h][leaf][Q]]
                        if ranks[h,R]!=45:good=False;break
                        rec=families[h,R]
                        need(all((ctx.H[h]|ctx.H[Q]|ctx.H[R])<=ctx.perp[r] for r in rec),'every propagation uses actual common native receivers')
                        entries.append({'leaf_plane':Q,'anchor_plane':R,'receivers':rec,'rank':45});transferred.append(R)
                    if not good:break
                    need(len(set(transferred))==15,'fifteen distinct transported anchor planes')
                    branches.append({'centre':h,'leaf':leaf,'quotient_propagations':entries});mapped.append(transferred)
                if not good:continue
                union=sorted(set(mapped[0])|set(mapped[1]));rank=F.rank(np.vstack([maps[q] for q in union]))
                if rank<=45:continue
                witness={'anchor':j,'leaf_donors':[left,right],'centres':[h1,h2,h3],'final_receiver':i,
                         'propagations':branches,'distinct_anchor_plane_sets':mapped,'final_union_rank':rank}
                break
            if witness is not None:break
        row={'anchor':j,'source_coefficient_sha256':sha256(b''.join(maps[h].tobytes() for h in sorted(maps))).hexdigest(),
             'pair_span_histogram':dict(sorted(Counter(ranks.values()).items())),
             'saturated_pairs':sum(v==45 for v in ranks.values()),'all_pairs':len(ranks),'cached_native_kernels':len(kernels),
             'protected_centres':{str(h):max(ranks[h,R] for R in ctx.stars[j] if R!=h) for h in params['centres'] if j in ctx.H[h]},
             'triangle_candidates_tried':tries,'component_obstruction_witness':witness}
        results.append(row);print('ANCHOR_SCREEN',j,row['saturated_pairs'],None if witness is None else witness['centres'],flush=True)
    result={'status':'PASS_EXACT_CYCLE_COMPONENT_ANCHOR_SCREEN','source_pins':expected,'width':3,'bank_dimension':48,
            'geometric_source_cuts':cuts,'native_source_cuts':native_cuts,'results':results,
            'standalone_component_obstructed_anchors':[r['anchor'] for r in results if r['component_obstruction_witness']],
            'full_bank_companion_built':False,'full_bank_obstruction_claim':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'obstructed_anchors':result['standalone_component_obstructed_anchors']},sort_keys=True),flush=True)

if __name__=='__main__':main()
