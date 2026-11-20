#!/usr/bin/env python3
"""Verify concrete changed-source anchors against native propagation ranks.

Pinned earlier independent source constructors and field arithmetic are
reused. This is the author application checker, not its independent review.
"""
from argparse import ArgumentParser
from hashlib import sha256
import gzip
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import numpy as np

ANCHORS={
    'all111':[26,32,66,95,100,103],
    'chain':[0,25,45,47,61,62,100],
    'hybrid':[0,25,47,100],
}

def need(value,message):
    if not value:
        raise ValueError(message)

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def source_context(repo,out,label):
    base=repo/'research/moonshot-005-program/results'
    if label!='all111':
        folder='review-b' if label=='chain' else 'review-fibre-only-b'
        prior=module(base/'bit-coupled-native-three-chain-source'/folder/'construct.py','independent_source_'+label)
        return prior.context(repo,out)
    prior=module(base/'bit-coupled-native-forty-h-source/review-all-donors-b/check.py','independent_all111_source')
    box={}
    def capture(args,base,field,native,H,D,perpendicular,views,spread,wires,xcount,singleton,templates,charts,centres,repairs,author,expected_cost,payload,cpp):
        box['ctx']=SimpleNamespace(field=field,maps={key:value[1] for key,value in templates.items()},
                                   views=views,H=H,perp=perpendicular)
    # Execute its authenticated coefficient reconstruction and digest checks.
    # Capture its matrices before the separately admitted physical-cost audit;
    # no source invoice is recomputed or claimed by this application checker.
    previous_argv=sys.argv[:];previous_audit=prior.audit
    try:
        prior.audit=capture
        sys.argv=['independent-all111','--repo',str(repo),'--out',str(out)]
        prior.main()
    finally:
        sys.argv=previous_argv;prior.audit=previous_audit
    need('ctx' in box,'previous independent construction completed')
    return box['ctx']

def check_anchor(ctx,record,j):
    field=ctx.field; cache={}; components={};common_records=[]
    k,l=record['leaf_donors'];h1,h2,h3=record['centres'];i=record['final_receiver']
    need(j==record['anchor'] and {j,k}<=ctx.H[h1] and {j,l}<=ctx.H[h2] and {k,l}<=ctx.H[h3], 'literal native triangle')
    need(i!=80 and ctx.H[h3]<=ctx.perp[i] and j not in ctx.perp[i], 'final identity receiver')
    for edge in record['propagations']:
        h=edge['centre'];leaf=edge['leaf']
        need((h,leaf) in [(h1,k),(h2,l)], 'correct arbitrary leaf')
        expected={q for q in ctx.views[leaf,i] if q!=h3}
        entries=edge['quotient_propagations']
        need(len(entries)==15 and {e['leaf_plane'] for e in entries}==expected and h not in expected, 'all final off-centre leaf observations')
        for entry in entries:
            Q,R=entry['leaf_plane'],entry['anchor_plane']
            required=ctx.H[h]|ctx.H[Q]|ctx.H[R]
            receivers=[r for r in range(111) if r!=80 and required<=ctx.perp[r]]
            need(set(entry['receivers'])<=set(receivers), 'larger family contains the admitted original witnesses')
            common_records.append({'centre':h,'leaf':leaf,'leaf_plane':Q,'anchor_plane':R,'receivers':receivers})
    need(len(common_records)==30,'thirty complete propagated quotient conditions')
    for width in (3,12):
        maps=ctx.maps[j,width];ranks=[];view_count=0
        for entry in common_records:
            h,R=entry['centre'],entry['anchor_plane'];pieces=[]
            need(field.rank(maps[R])==width,'full quotient rank')
            for r in entry['receivers']:
                key=width,h,r
                if key not in cache:
                    planes=ctx.views[j,r]
                    need(len(planes)==16 and h in planes and R in planes,'actual sixteen-plane native view')
                    matrix=np.vstack([maps[q] for q in planes if q!=h])
                    fibre=field.null(matrix)
                    need(fibre.shape==(16*width,width),'complete off-H kernel dimension')
                    need(field.rank(field.mm(maps[h],fibre))==width,'central quotient completes the full native view')
                    cache[key]=fibre;view_count+=1
                fibre=cache[key]
                need(not np.any(field.mm(maps[R],fibre)),'fibre lies in the transported quotient kernel')
                pieces.append(fibre)
            combined=np.hstack(pieces)
            rank=field.rank(combined)
            need(rank==15*width,'whole quotient kernel is generated')
            ranks.append(rank)
        union=sorted(set().union(*map(set,record['distinct_anchor_plane_sets'])))
        need(len(union)==20,'twenty final transported planes')
        final_rank=field.rank(np.vstack([maps[q] for q in union]))
        need(final_rank==16*width,'incompatible final quotient-kernel partitions')
        first=next(value for (w,_,_),value in cache.items() if w==width)
        need(field.rank(first)==width<15*width,'single-fibre nonsaturation control')
        repeated=np.vstack([maps[union[0]] for _ in union])
        need(field.rank(repeated)==width,'duplicate final observations lose rank')
        components[str(width)]={'propagation_ranks':ranks,'final_union_rank':final_rank,
            'distinct_native_views':view_count,
            'source_coefficient_sha256':sha256(b''.join(maps[q].tobytes() for q in sorted(maps))).hexdigest(),
            'single_fibre_control_rank':width,'repeated_final_control_rank':width}
    return {'anchor':j,'leaves':[k,l],'centres':[h1,h2,h3],'final_receiver':i,
            'propagations':common_records,'components':components,
            'full_bank_propagation_rank':16*(45+180),'full_bank_final_union_rank':16*(48+192),
            'frozen_anchor_obstructs_arbitrary_separated_neighbours':True}

def main():
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.repo=args.repo.resolve();args.out.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parent
    pins=json.loads((here/'SOURCE-PINS.json').read_text())
    for path,entry in pins['files'].items():
        raw=(args.repo/path).read_bytes()
        need(len(raw)==entry['bytes'] and sha256(raw).hexdigest()==entry['sha256'],'application source pin '+path)
    witness=args.repo/'research/moonshot-005-program/results/bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz'
    records={r['anchor']:r for r in json.loads(gzip.decompress(witness.read_bytes()))['witnesses']}
    all_results={}
    for label,anchors in ANCHORS.items():
        ctx=source_context(args.repo,args.out/label,label)
        all_results[label]=[check_anchor(ctx,records[j],j) for j in anchors]
        print('PASS_FROZEN_CHANGED_ANCHORS',label,anchors,flush=True)
    result={'status':'PASS_SEVENTEEN_CHANGED_ARRAY_ANCHOR_OBSTRUCTIONS','source_words':3,
            'anchor_certificates':17,'quotient_width':240,'bank':3840,
            'geometric_triangle_source':'admitted single-anchor certificate',
            'each_application_uses_all_admissible_native_receivers':True,
            'results':all_results,'all_foundations_retained':True,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],flush=True)

if __name__=='__main__':
    main()
