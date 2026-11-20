#!/usr/bin/env python3
"""Compile paid native source words for the 23- and 24-chart packings."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def import_file(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def late_indices(frame, field):
    """Complete a half-frame by the coordinate rows at nonpivot columns."""
    A=frame.copy()
    piv=[]
    for col in range(A.shape[1]):
        p=np.flatnonzero(A[len(piv):,col])
        if not len(p):
            continue
        r=len(piv)
        i=r+int(p[0])
        A[[i,r]]=A[[r,i]]
        A[r]=field.MUL[field.INVERSE[A[r,col]],A[r]]
        rest=np.flatnonzero(A[r+1:,col])+r+1
        A[rest]^=field.MUL[A[rest,col,None],A[r][None,:]]
        piv.append(col)
        if len(piv)==len(A):
            break
    keep=[c for c in range(A.shape[1]) if c not in piv]
    require(len(keep)==len(frame),'late coordinate complement size')
    return keep

def physical_slots(n,repo,helper):
    base=repo/'research/moonshot-005-program/results'
    rows=helper.load_payload(base/helper.ROUTES[0],helper.ROUTES[1])
    wires=defaultdict(list)
    xcount=Counter()
    for line in rows.splitlines():
        p,j,c,h,_,_,line_src,_=json.loads(line)
        if h is None: continue
        if p=='X':
            xcount[h]+=1
        if line_src is not None:
            wires[line_src,h,p].extend(helper.owner_id(p,j,c,copy) for copy in range(8))
    for v in wires.values():
        v.sort()
    return wires,xcount

def compile_one(helper,review,chart,j,maps,seed,centres,wires,xcount,records,singleton=None):
    k,n=chart.k,16*chart.k
    offset=0 if k==3 else 768
    f=chart.native.f
    rows,pos,jobs=[],[],[]
    prefix=0 if k==3 else 3
    for h,F in sorted(maps.items()):
        xs,ys=wires[j,h,'X'],wires[j,h,'Y']
        quota=len(xs)//120
        require(quota in (1,2,3) and len(ys)==max(2-quota,0)*120,'actual native owner counts')
        if quota==3:
            require(singleton is not None and h==singleton[0] and singleton[1].shape==(3*k,32*k),
                    'all three genuine singleton coordinate groups')
            rows.append(singleton[1])
            pos.extend((h,3*prefix*8+d*8) for d in range(3*k))
            continue
        pair=np.kron(np.eye(2,dtype=np.uint8),F)
        if quota==2:
            rows.append(pair)
            if xcount[h]==90:
                pos.extend((h,prefix*16+degree*16+half*8) for half in range(2) for degree in range(k))
            else:
                require(xcount[h]==45,'large two-donor early input')
                pos.extend((h,prefix*16+d*8) for d in range(2*k))
            continue
        if h in centres:
            E=np.eye(2*k,dtype=np.uint8)[:k]
        else:
            E=review.pseudo(f'early/{chart.h}/{k}/{j}/{h}/{seed}',k,2*k)
        rows.append(f.matmul(E,pair))
        pos.extend((h,prefix*8+d*8) for d in range(k))
        indices=late_indices(E,f)
        if h in centres:
            require(indices==list(range(k,2*k)),'unframed genuine mixed central H word')
        for d,v in enumerate(indices):
            which,coord=divmod(v,k)
            jobs.append({'h':h,'coefficients':F[coord].tolist(),
                         'dest_and_first_X':[(ys[8*(prefix+d)+l],j*3840+offset+8*which+l)
                                             for l in range(8)]})
    A=np.vstack(rows)
    require(A.shape==(2*n,2*n),'all independent field owners')
    stream,price=helper.compile_invertible(A)
    placements=[]
    perm={}
    for l in range(8):
        group=[j*3840+offset+16*s+8*b+l for b in range(2) for s in range(n)]
        for r,(h,t) in enumerate(pos):
            dst=wires[j,h,'X'][t+l]
            require(dst not in perm,'unique early holder')
            perm[dst]=group[r]
        placements.append(group)
    file=f'REDUCE-{j}-{k}.bin.gz'
    records[f'{j}-{k}']={'reduce_file':file,'original_field_placements':placements,'before_departure_late_parities':jobs}
    write=8*sum(int(helper.WEIGHT[job['coefficients']].sum()) for job in jobs)
    late=[d for job in jobs for d,_ in job['dest_and_first_X']]
    require(len(set(late))==len(late),'unique Y injection')
    bill=Counter(basis_ADD=8*price,write_ADD=write,read_ADD=6*len(late),INIT=6*len(late),dirty_CLEAR=6*len(late))
    return bill,perm,late,stream

def main():
    p=ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--parameters',type=Path,required=True)
    p.add_argument('--background',type=Path,required=True)
    p.add_argument('--singleton-coefficients',type=Path,
                   help='select the 24-chart packing and its repaired three-group singleton inputs')
    p.add_argument('--source-compiler',type=Path)
    p.add_argument('--packing-review',type=Path)
    p.add_argument('--field-review',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--emit-words',action='store_true',help='retain every field primitive and physical address')
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    base=a.repo/'research/moonshot-005-program/results'
    helper=import_file(a.source_compiler or base/'bit-spread-source-owner-compiler/author/compile_source.py','prior_compiler')
    review=import_file(a.packing_review or base/'bit-spread-overlap-source/review/check.py','packed_independent')
    field=import_file(a.field_review or base/'bit-spread-h263-source/review/check.py','independent_gf')
    n=review.Native(a.repo,field)
    wires,xcount=physical_slots(n,a.repo,helper)
    raw=a.parameters.read_bytes()
    params=json.loads(raw)
    pair=params['pair']
    centres=set(pair['centres'])
    repairs={}
    if a.singleton_coefficients:
        singleton_raw=a.singleton_coefficients.read_bytes()
        for v in json.loads(gzip.decompress(singleton_raw)):
            repairs[v['h'],v['donor'],v['k']]=(v['singleton'],np.asarray(v['S'],dtype=np.uint8))
        roster=params['extended_ordinary_packing']
    else:
        roster=params['native_all_views_packing']
    singles={(p['H'],p['k']):p for p in params['one_centre']}
    patched=set.union(*(n.H[h] for h in roster))
    require((len(roster),len(patched))==((24,71) if repairs else (23,68)),'exact physical roster')
    totals=Counter()
    separate={}
    all_y=set()
    templates=defaultdict(dict)
    for k in (3,12):
        ps=[review.Chart(n,h,k) for h in pair['centres']]
        maps=review.paired(ps,pair[str(k)])
        for j,rows in maps.items():
            c=next(c for c in ps if j in c.donors)
            templates[j][k]=(c,rows,pair[str(k)]['early'][str(j)],centres)
        for h in roster:
            if h in centres: continue
            c=review.Chart(n,h,k)
            prm=singles[h,k]
            for j,rows in c.single(prm).items():
                require(k not in templates[j],'ordinary patch donor collision')
                templates[j][k]=(c,rows,prm['early'][str(j)],{h})
    bits={}
    for j,components in sorted(templates.items()):
        records={}
        assign={}
        costs=Counter()
        digests={}
        for k in (3,12):
            c,rows,seed,fixed=components[k]
            bill,perm,late,stream=compile_one(helper,review,c,j,rows,seed,fixed,wires,xcount,records,
                                             repairs.get((c.h,j,k)))
            require(not set(assign)&set(perm) and not all_y.intersection(late),'disjoint native holders')
            assign.update(perm)
            all_y.update(late)
            costs.update(bill)
            digests[str(k)]=sha256(stream).hexdigest()
            if a.emit_words:
                helper.save_compressed(a.out/f'REDUCE-{j}-{k}.bin.gz',stream)
        require(set(assign)==set(range(3840*j,3840*(j+1))),'every original field')
        swaps=helper.permutation_swaps(assign)
        records[f'{j}-swaps']=swaps
        costs['permutation_ADD']=18*len(swaps)
        costs['inverse_ADD']=costs['basis_ADD']+costs['permutation_ADD']
        costs['forward_ADD']=costs['inverse_ADD']+costs['write_ADD']+costs['read_ADD']
        costs['total_ADD']=costs['inverse_ADD']+costs['forward_ADD']
        jraw=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
        digests['holder']=sha256(jraw).hexdigest()
        if a.emit_words:
            helper.save_compressed(a.out/f'HOLDERS-{j}.json.gz',jraw)
        bits[str(j)]=digests
        separate[str(j)]=dict(costs)
        totals.update(costs)
    require(set(templates)==patched and len(all_y)*6==totals['INIT'],'no missing donor or late injection')
    bgraw=a.background.read_bytes()
    background=json.loads(bgraw)
    require(set(map(int,background))==set(range(111)), 'complete background scope')
    bg=Counter()
    for j in range(111):
        if j not in patched:
            bg.update(background[str(j)])
    bg_inverse=bg['early_basis_ADD']+bg['source_owner_permutation_ADD']
    bg_caches=bg['snapshot_copy_ADD_INIT_dirty_CLEAR']
    bg_fwd=bg_inverse+bg_caches+bg['late_evaluation_ADD']
    combined={'donors':111,'source_forward_ADD':bg_fwd+totals['forward_ADD'],
              'source_pure_inverse_ADD':bg_inverse+totals['inverse_ADD'],
              'source_forward_and_inverse_ADD':bg_fwd+bg_inverse+totals['total_ADD'],
              'source_INIT':bg_caches+totals['INIT'],'source_dirty_CLEAR':bg_caches+totals['dirty_CLEAR'],
              'source_extra_MOVE':0,'new_complete_kappa':False}
    result={'parameters_sha256':sha256(raw).hexdigest(),'background_sha256':sha256(bgraw).hexdigest(),
            'layout_payload':helper.LAYOUT[1],'route_payload':helper.ROUTES[1],'spread_payload':helper.SPREAD[1],
            'native_chart_count':len(roster),'special_donor_count':len(patched),'regular_donor_count':111-len(patched),
            'special':dict(totals),'special_donor_costs':separate,'all_word_hashes':bits,
            'background':dict(bg),'combined':combined}
    if repairs:
        result['singleton_compressed_sha256']=sha256(singleton_raw).hexdigest()
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(combined,sort_keys=True))

if __name__=='__main__':
    main()
