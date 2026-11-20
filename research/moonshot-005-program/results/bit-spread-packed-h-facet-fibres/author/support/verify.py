#!/usr/bin/env python3
"""Verify common source gauges and actual terminal readouts on a labelled set of native cuts."""
import argparse
from collections import Counter,defaultdict
import gzip,hashlib,json,importlib.util
from pathlib import Path
import sys
import numpy as np

def sha(x):
    return hashlib.sha256(x).hexdigest()

def shuffle(length):
    assert length in (48,192)
    dst_src={2*length*e+length*h+s:16*s+8*h+e for e in range(8)for h in range(2)for s in range(length)}
    seen=set();swaps=0
    for d in range(16*length):
        if d in seen:continue
        ptr=d
        while ptr not in seen:
            seen.add(ptr);ptr=dst_src[ptr];swaps+=1
        assert ptr==d
        swaps-=1
    return swaps

def anchor_readout(slicer,i):
    a=slicer.a
    left=slicer.src.left(0);right=a.right(i)
    ds=[d for d in range(len(a.D))if 0 in a.D[d]and i in a.D[a.dual[d]]]
    blocks=[];contributions={}
    for d in ds:
        M,cols,rows=slicer.members(d);ids=a.middle[d,"X"]+a.middle[d,"Y"]
        take=cols[0];observe=rows[i];L=np.stack([left[ids[q]]for q in take]);R=np.stack([right[ids[q]]for q in observe]).T
        C=M[np.ix_(observe,take)]
        contributions[d]=a.ops.matmul(R,C)
        blocks.append(a.ops.matmul(contributions[d],L))
    full=np.bitwise_xor.reduce(np.stack(blocks),axis=0)
    assert not np.any(full[:96,96:]) and not np.any(full[96:,:96])
    O=np.zeros_like(full);O[:96,:96]=inverse(full[:96,:96]);O[96:,96:]=inverse(full[96:,96:])
    assert np.array_equal(a.ops.matmul(O,full),np.eye(480,dtype=np.uint8))
    return O,contributions

def price_map(comp,G):
    if comp is None:
        # Gauss–Jordan on the literal binary expansion of its native scalar map.
        # At six bits per field, one square block needs at most n(n−1)+3n row ADD.
        N=len(G)*6
        return 8*(N*(N-1)+3*N)
    return 8*comp.compile_invertible(G)[1]

def main(args):
    a=Atlas(args.repo,args.k_words,args.d_charts,args.library)
    raw=gzip.decompress(args.repair.read_bytes())
    require(sha(raw)=='f185c1d220f258b88159f50bcafe47c1b0fde53439320eb5d9313d06e74bc970','repair parent')
    word=json.loads(raw)
    astar=SpecialSource(a,args.repo,args.source,word['frames'])
    ap=args.repo/'research/moonshot-005-program/results/bit-two-sided-covariant-target/author/output/ASSIGNMENT.json'
    require(sha(ap.read_bytes())=='deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601','two-sided target')
    assign=json.loads(ap.read_text())
    S=Slices(a,astar,word,assign)
    selected=json.loads(args.cuts.read_text())
    cuts={int(i):sorted(v)for i,v in selected['cuts'].items()if v}
    comp=None
    if args.source_compiler:
        mod=importlib.util.spec_from_file_location('source_compiler',args.source_compiler)
        comp=importlib.util.module_from_spec(mod);mod.loader.exec_module(comp)
    demands=defaultdict(lambda:[[],[]]);readouts={};prices={};counts={};perpair=Counter();rawtags=hashlib.sha256()
    for i in sorted(cuts):
        keep,eq=S.receiver(i,cuts[i])
        O,R0=anchor_readout(S,i)
        pin=sha(O.tobytes());readouts[i]=pin
        prices[f'output_{i}']=sum(price_map(comp,O[p:q,p:q])+18*shuffle((q-p)//2) for p,q in ((0,96),(96,480)))
        anchor=S.left(i,0,keep)
        for d in sorted(keep):
            dom=anchor[d];pad=np.zeros((480,8),dtype=np.uint8);start=0 if d in a.marked else 96;pad[start:start+len(dom.T)]=dom.T
            assert np.array_equal(a.ops.matmul(O,R0[d]),pad)
            for j in sorted(a.D[d]&set(range(111))):
                perpair[i,j]+=1
                if j in astar.donors:continue
                key,U,Q=matched(assign,i,j,d,*eq[d,j])
                demands[key][0].append(U);demands[key][1].append(Q)
                rawtags.update(bytes([i,j]));rawtags.update(d.to_bytes(2,'little'));rawtags.update(U.tobytes());rawtags.update(Q.tobytes())
        counts[i]=[len(keep),sum(len(a.D[d]&set(range(111)))for d in keep)]
        print('cut equations and terminal',i,counts[i],flush=True)
    data={}
    for key,(U,Q) in sorted(demands.items()):
        j,n=key;G,r=common_gauge(a,U,Q)
        sh=shuffle(48)+shuffle(192) if n==480 else shuffle(n//2)
        prices[f'input_{j}_{n}']=price_map(comp,G)+18*sh
        data[f'{j}/{n}']={'rank':r,'width':n,'equations':len(U)*8,'native_gauge_sha256':sha(G.tobytes())}
    result={'status':'simultaneous genuine proper target restrictions, in fixed native input/output coordinates',
            'receivers':sorted(cuts),'accepted_cuts_by_receiver':counts,
            'cut_receiver_count':sum(v[0]for v in counts.values()),'native_cut_donor_receiver_sections':sum(v[1]for v in counts.values()),
            'normalised_entire_donor_0_blocks':len(cuts),'unique_proper_blocks_touched':len(perpair),
            'native_constrained_coordinates_by_section':64*sum(perpair.values()),'full_native_input_width':3840,
            'input_gauges':data,'output_gauge_hashes':readouts,'independent_demand_stream_sha256':rawtags.hexdigest(),
            'per_donor_receiver_body_target_dimensions':{f'{i}/{j}':8*c for (i,j),c in perpair.items()},
            'prices_type':'exact binary elimination' if comp else 'permutation exact plus native binary elimination upper bounds',
            'ADD_each_direction_per_gauge':prices,'all_input_gauges_one_direction_ADD':sum(v for k,v in prices.items()if k.startswith('input')),
            'all_output_gauges_one_direction_ADD':sum(v for k,v in prices.items()if k.startswith('output')),
            'additional_MOVE_INIT_CLEAR':0,'unresolved':'uncovered source directions and other receivers; full target, proper inverse return, suppliers, foundations'}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('verified',result['cut_receiver_count'],result['native_cut_donor_receiver_sections'],flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('repo','h-author','isolated-author','k-words','d-charts','source','repair','cuts','out'):
        p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--library',type=Path);p.add_argument('--source-compiler',type=Path);p.add_argument('--inverse-library',type=Path)
    args=p.parse_args()
    sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.isolated_author))
    from build import require
    from transfer import Atlas
    from body import SpecialSource,inverse
    from slices import Slices,matched,common_gauge
    if args.inverse_library:
        import slices
        from fast import Arithmetic
        machine=Arithmetic(args.inverse_library.resolve());inverse=machine.inverse;slices.inverse=inverse
    main(args)
