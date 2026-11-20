#!/usr/bin/env python3
"""Replay a protected two-centre source word on the actual native atlas."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np


def require(condition,message):
    if not condition:
        raise ValueError(message)


def run(repo,out):
    out.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parent
    pins=here/'SOURCE-PINS.json'
    if pins.exists():
        for p,d in json.loads(pins.read_text()).items():
            require(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'source pin '+p)
    spec=importlib.util.spec_from_file_location('moving_construction',here/'construction.py')
    build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
    data=build.build(repo)
    a,p=data['atlas'],data['previous']
    first,second=data['first'],data['second']
    eye=np.eye(3,dtype=np.uint8)
    source=[]
    maps=data['maps']
    for j,rows in sorted(maps.items()):
        chart=data['charts'][first] if j in data['charts'][first].donors else data['charts'][second]
        require(max(a.quota[j,h] for h in a.by_donor[j])==30,'all five donors are ordinary, not singleton')
        require(set(data['base_nodes'][j].values())=={x for x in range(64) if not data['geometric'].quadratic(x,a)},'all28 base nodes')
        changed=[h for h in rows if not np.array_equal(rows[h],np.kron(a.vandermonde([data['base_nodes'][j][h]],16),eye))]
        expected=[first,data['companions'][j]] if j in data['charts'][first].donors else [second]
        require(set(changed)==set(expected) and 1<=len(changed)<=2,'exact one/two quotient edits')
        chart.source_views(rows,j)
        chart.early(j,rows,data['actual_early_seeds'][j],fixed_centres=(first,second))
        source.append({'donor':j,'geometric_cuts':len(a.adj[j]),'native_cuts':len(a.adj[j]&a.native),
                       'source_dimension':48,'quotient_width':3,'actual_early_basis_rank':96,
                       'actual_early_seed':data['actual_early_seeds'][j],'edited_planes':sorted(changed),
                       'uniform_propagation_upper':42 if len(changed)==2 else 30,'saturation_threshold':45})
    H=[];fibre_certificate={}
    for h,chart in data['charts'].items():
        require(10 not in chart.donors and 80 not in chart.views,'exact unperturbed native target roles')
        word=data['Hwords'][h]
        require(word.shape==(9,9) and a.rank(word)==9,'invertible actual H provider')
        geometric_count=native_count=moved=native_moved=0
        fibre_certificate[str(h)]={}
        for i in chart.views:
            kernels=[]
            for j in chart.donors:
                off=[z for z in a.by_donor[j] if z!=h and a.planes[z]<=a.adj[i]]
                kernel=p.null_basis(np.vstack([maps[j][z] for z in off]),a)
                require(kernel.shape==(48,3),'whole off-H inverse fibre')
                kernels.append(kernel)
            require(all(a.rank(np.hstack((kernels[0],K)))==3 for K in kernels),'common entire donor uncertainty spaces')
            K=kernels[0]
            visible=[q for q,d in enumerate(chart.ports) if a.charts[d]<=a.adj[i]]
            require(len(visible)==3,'actual visible marked D ports')
            readouts=[a.mm(word[np.ix_(visible,range(3*s,3*s+3))],a.mm(maps[j][h],K)) for s,j in enumerate(chart.donors)]
            require(a.rank(readouts[0])==3 and all(np.array_equal(readouts[0],R) for R in readouts),'common invertible physical H readout')
            changed=False
            if h==first:
                points=[x for x in chart.singular if not a.algebra.polar(x,a.masks[i])]
                old=p.null_basis(np.vstack([data['first_old_points'][x] for x in points]),a)
                changed=a.rank(np.hstack((K,old)))>3
                moved+=changed;native_moved+=changed and i in a.native
            else:
                require(a.rank(np.hstack((K,data['second_old_fibres'][i])))==3,'second-centre old fibres retained')
            fibre_certificate[str(h)][str(i)]={'kernel':K.tolist(),'readout':readouts[0].tolist(),'moved_from_geometric_base':changed}
            geometric_count+=1;native_count+=i in a.native
        H.append({'H':h,'donors':chart.donors,'ports':chart.ports,'geometric_common_fibres':geometric_count,
                  'native_common_fibres':native_count,'moved_geometric_fibres':moved,'moved_native_fibres':native_moved})
    require([x['moved_geometric_fibres'] for x in H]==[20,0],'a genuine moving-fibre continuation')
    # Omit one reflected copy of the companion edit. The first H now has unequal fibres.
    fault_donor=0;fault_h=data['companions'][fault_donor]
    fault_maps=dict(maps[fault_donor])
    fault_maps[fault_h]=np.kron(a.vandermonde([data['base_nodes'][fault_donor][fault_h]],16),eye)
    unequal=[]
    chart=data['charts'][first]
    for i in chart.views:
        off=[z for z in a.by_donor[fault_donor] if z!=first and a.planes[z]<=a.adj[i]]
        K=p.null_basis(np.vstack([fault_maps[z] for z in off]),a)
        other=chart.donors[1]
        off2=[z for z in a.by_donor[other] if z!=first and a.planes[z]<=a.adj[i]]
        L=p.null_basis(np.vstack([maps[other][z] for z in off2]),a)
        if a.rank(np.hstack((K,L)))>3:unequal.append(i)
    require(len(unequal)==20,'omitting a copied edit breaks exactly the affected first-centre fibres')
    # Removing a genuine quotient loses its three information dimensions.
    donor=61;receiver=next(iter(sorted(a.adj[donor]&a.native)))
    visible=[h for h in a.by_donor[donor] if a.planes[h]<=a.adj[receiver]]
    rank_before=a.rank(np.vstack([maps[donor][h] for h in visible]))
    rank_after=a.rank(np.vstack([maps[donor][h] for h in visible[:-1]]))
    require((rank_before,rank_after)==(48,45),'deleted real quotient negative control')
    coefficients={'maps':{str(j):{str(h):M.tolist() for h,M in sorted(rows.items())} for j,rows in sorted(maps.items())},
                  'Hwords':{str(h):W.tolist() for h,W in data['Hwords'].items()},
                  'base_nodes':{str(j):{str(h):int(v) for h,v in sorted(rows.items())} for j,rows in sorted(data['base_nodes'].items())},
                  'companions':data['companions'],'field_unit_basis':data['field_unit_basis'],
                  'actual_early_seeds':data['actual_early_seeds']}
    raw=(json.dumps(coefficients,sort_keys=True,separators=(',',':'))+'\n').encode()
    (out/'COEFFICIENTS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    fibres=(json.dumps(fibre_certificate,sort_keys=True,separators=(',',':'))+'\n').encode()
    (out/'FIBRES.json.gz').write_bytes(gzip.compress(fibres,mtime=0))
    result={'status':'PASS_PROTECTED_TWO_H_MOVING_FIBRES','source_cuts':sum(r['geometric_cuts'] for r in source),
            'native_source_cuts':sum(r['native_cuts'] for r in source),'sources':source,'H':H,
            'omitted_companion_edit_failures':unequal,'deleted_quotient_ranks':[rank_before,rank_after],
            'coefficient_payload_sha256':hashlib.sha256(raw).hexdigest(),'fibre_payload_sha256':hashlib.sha256(fibres).hexdigest(),
            'all_word_costs_computed':False,'complete_shared_D_K_facet_word':False,'new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],result['source_cuts'],result['native_source_cuts'],flush=True)


if __name__=='__main__':
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args()
    run(args.repo.resolve(),args.out.resolve())
