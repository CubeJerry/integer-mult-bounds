#!/usr/bin/env python3
"""Compile the H263 source on its native X/Y holders, at bank 3840 over GF64."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import struct
import numpy as np

MODULUS = 0x43
COPIES = 8
DEGREE = 6
BANK = 3840
LAYOUT = ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
          '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
SPREAD = ('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz',
          '7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab')
ROUTES = ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
          '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
COEFFICIENTS = '66fe6820e16e2a1a221cc59656b6356087f92b685ff121ef174a67c7c4890a0e'
ITEM = struct.Struct('<BHHB')

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load_payload(path, expected):
    raw = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(raw).hexdigest()==expected, f'source payload {path.name}')
    return raw

def gf_mul(a,b):
    res = 0
    for _ in range(DEGREE):
        if b & 1:
            res ^= a
        b >>= 1
        a <<= 1
        if a & 64:
            a ^= MODULUS
    return res

T = np.array([[gf_mul(a,b) for b in range(64)] for a in range(64)],dtype=np.uint8)
INV = np.zeros(64,dtype=np.uint8)
for z in range(1,64):
    inv = np.flatnonzero(T[z]==1)
    require(len(inv)==1, 'GF64 nonzero inverse')
    INV[z] = int(inv[0])

def binary_rows(z):
    return [sum(((int(T[z,1<<b])>>t)&1)<<b for b in range(DEGREE)) for t in range(DEGREE)]

def binary_scale(z):
    """ADD primitives, in forward order, for multiplication by z on six bits."""
    rows = binary_rows(z)
    ops = []
    def add(d,s):
        rows[d] ^= rows[s]
        ops.append((d,s))
    for c in range(DEGREE):
        p = next(u for u in range(c,DEGREE) if (rows[u]>>c)&1)
        if p!=c:
            add(p,c)
            add(c,p)
            add(p,c)
        for u in range(DEGREE):
            if u!=c and (rows[u]>>c)&1:
                add(u,c)
    require(rows == [1<<t for t in range(DEGREE)],'local multiplier reduction')
    for d,s in reversed(ops):
        rows[d] ^= rows[s]
    require(rows==binary_rows(z), 'six-bit multiplier basis replay')
    return ops[::-1]

SCALES = {z:binary_scale(z) for z in range(1,64)}
WEIGHT = np.array([sum(row.bit_count() for row in binary_rows(z)) for z in range(64)],dtype=np.int64)

def field_product(A,B):
    C = np.zeros((len(A),B.shape[1]),dtype=np.uint8)
    for t in range(A.shape[1]):
        C ^= T[A[:,t,None],B[t,None,:]]
    return C

def compile_invertible(target):
    """Return packed field primitives reducing target to I and their ADD count.

    0 = add c*row_s into row_d, 1 = multiply row_d by c, 2 = swap rows d,s.
    Reverse the underlying binary ADDs of this reduction for the forward map.
    """
    n = len(target)
    A = target.copy()
    stream = bytearray()
    count = 0
    for c in range(n):
        choices = np.flatnonzero(A[c:,c])
        require(len(choices),'invertible native early block')
        p = c+int(choices[0])
        if p!=c:
            A[[c,p]] = A[[p,c]]
            stream.extend(ITEM.pack(2,c,p,0))
            count += 3*DEGREE
        if A[c,c]!=1:
            z = int(INV[A[c,c]])
            stream.extend(ITEM.pack(1,c,0,z))
            A[c] = T[z,A[c]]
            count += len(SCALES[z])
        active = np.flatnonzero(A[:,c])
        active = active[active!=c]
        coeffs = A[active,c].copy()
        count += int(WEIGHT[coeffs].sum())
        for u,z in zip(active,coeffs):
            stream.extend(ITEM.pack(0,int(u),c,int(z)))
        A[active] ^= T[coeffs[:,None],A[c][None,:]]
    require(np.array_equal(A,np.eye(n,dtype=np.uint8)), 'field reduction reaches I')
    # Execute the emitted inverse stream from I on actual field basis vectors.
    for p in range(len(stream)-ITEM.size,-1,-ITEM.size):
        op,d,s,z = ITEM.unpack_from(stream,p)
        if op==0:
            A[d] ^= T[z,A[s]]
        elif op==1:
            A[d] = T[INV[z],A[d]]
        else:
            A[[s,d]] = A[[d,s]]
    require(np.array_equal(A,target),'all original basis fields of forward map')
    return bytes(stream), count

def owner_id(phase,j,coord,copy):
    return (((phase=='Y')*111+j)*480+coord)*COPIES+copy

def permutation_swaps(perm):
    require(len(perm)==BANK and set(perm)==set(perm.values()), 'permutation of all donor Xs')
    done = set()
    swaps = []
    for a in sorted(perm):
        if a in done: continue
        cycle = []
        q = a
        while q not in done:
            done.add(q)
            cycle.append(q)
            q = perm[q]
        require(q==a,'disjoint cycles')
        # perm[dst] names the source of the final value. Left rotate this cycle.
        swaps.extend(zip(cycle,cycle[1:]))
    original = {u:u for u in perm}
    for a,b in swaps:
        original[a],original[b] = original[b],original[a]
    require(original==perm,'field-owner swap schedule')
    return swaps

def native_context(base, coeff):
    layout = json.loads(load_payload(base/LAYOUT[0],LAYOUT[1]))
    spread = json.loads(load_payload(base/SPREAD[0],SPREAD[1]))
    H = [set(row) for row in layout['A2']]
    D = [set(row) for row in layout['D4']]
    chart = coeff['H']
    donors = coeff['donors']
    require(sorted(H[chart])==donors,'specified native triple')
    ports = [d for d,roots in enumerate(D) if H[chart]<=roots]
    radicals = [set(v)-{0} for v in spread['D_radicals']]
    point = {}
    for j in donors:
        for h,plane in enumerate(H):
            if j not in plane or h==chart:
                continue
            ds = [d for d in ports if plane<=D[d]]
            require(len(ds)==5,'five charts identify an off-plane')
            ids = set.intersection(*(radicals[d] for d in ds))
            require(len(ids)==1,'unique native point')
            point[j,h]=ids.pop()
    early = Counter()
    wires = defaultdict(list)
    for line in load_payload(base/ROUTES[0],ROUTES[1]).splitlines():
        phase,role,c,h,_,_,source,_ = json.loads(line)
        if h is None:
            continue
        if phase=='X':
            early[h]+=1
            require(role==source,'correct early source')
        if source in donors:
            wires[source,h,phase].extend(owner_id(phase,role,c,u) for u in range(COPIES))
    for group in wires.values():
        group.sort()
        require(len(set(group))==len(group),'physical holder multiplicity')
    require(early[chart]==90,'designated fully early H')
    return H,point,early,wires


def component_word(k, j, context, coeff, records):
    H,points,early,wires = context
    spec = coeff['components'][str(k)]
    di = coeff['donors'].index(j)
    offset = 0 if k==3 else 48*16
    n = 16*k
    native = sorted(h for h,plane in enumerate(H) if j in plane)
    early_rows = []
    early_slots = []
    late_jobs = []
    matrices = {}
    for h in native:
        if h==coeff['H']:
            F = np.eye(n,dtype=np.uint8)[di*k:(di+1)*k]
        else:
            F = np.asarray(spec['off_H'][str(points[j,h])],dtype=np.uint8)
        require(F.shape==(k,n),'native quotient width')
        pair = np.kron(np.eye(2,dtype=np.uint8),F)
        xs = wires[j,h,'X']
        ys = wires[j,h,'Y']
        quota = len(xs)//(15*COPIES)
        require(quota in (1,2) and len(ys)==(2-quota)*15*COPIES,'special star without singleton')
        prefix = 0 if k==3 else 3
        if quota == 1:
            E = np.asarray(spec['early'][str(j)][str(h)],dtype=np.uint8)
            early_rows.append(field_product(E,pair))
            early_slots.extend((h,prefix*8+t*8) for t in range(k))
            late_select = spec['complementary_late_coordinate_rows'][str(j)][str(h)]
            require(sorted(late_select)==sorted(set(late_select)) and len(late_select)==k,'late basis rows')
            for r,choice in enumerate(late_select):
                lane_top,t = divmod(choice,k)
                symbols = F[t].tolist()
                # A parity row template has fixed original sources and eight
                # copies on separate spinor lanes. Each Y receives a distinct cache.
                jobs = []
                for l in range(COPIES):
                    receiver = ys[(prefix+r)*8+l]
                    shift = j*BANK+offset+l+COPIES*lane_top
                    jobs.append((receiver,shift))
                late_jobs.append({'h':h,'coefficients':symbols,'dest_and_first_X':jobs})
        else:
            early_rows.append(pair)
            if early[h]==90:
                early_slots.extend((h,prefix*16+t*16+half*8)
                                   for half in range(2) for t in range(k))
            else:
                require(early[h]==45,'mixed two-donor fully early source incidence')
                early_slots.extend((h,prefix*16+t*8) for t in range(2*k))
        matrices[h] = F
    complete = np.vstack(early_rows)
    require(complete.shape==(2*n,2*n),'full square early block')
    stream, pure = compile_invertible(complete)
    placements = []
    assign = {}
    for l in range(COPIES):
        storage = [j*BANK+offset+16*s+l+8*half for half in range(2) for s in range(n)]
        placements.append(storage)
        for logical,(h,idx) in enumerate(early_slots):
            dst = wires[j,h,'X'][idx+l]
            require(dst not in assign,'one early use per true original')
            assign[dst] = storage[logical]
    cache_write = COPIES*sum(int(WEIGHT[job['coefficients']].sum()) for job in late_jobs)
    destinations = [dst for job in late_jobs for dst,_ in job['dest_and_first_X']]
    require(len(set(destinations))==len(destinations),'distinct genuine Y visits')
    source_ids = [x for placement in placements for x in placement]
    require(len(set(source_ids))==256*k,'all original component fields')
    records[f'{j}-{k}'] = {'reduce_file':f'REDUCE-{j}-{k}.bin.gz',
                             'original_field_placements':placements,
                             'before_departure_late_parities':late_jobs}
    info = {'one_pair_binary_ADD':pure,'early_field_primitives':len(stream)//ITEM.size,
            'all_eight_pairs_pure_ADD':pure*COPIES,'cache_write_ADD':cache_write,
            'cache_read_ADD':len(destinations)*DEGREE,'late_fields':len(destinations),
            'early_template_payload':hashlib.sha256(stream).hexdigest()}
    return info,assign,destinations,stream

def save_compressed(path, raw):
    path.write_bytes(gzip.compress(raw,mtime=0))
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--coefficients',type=Path,required=True)
    p.add_argument('--background',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    coeff = json.loads(load_payload(args.coefficients,COEFFICIENTS))
    require(coeff['field_polynomial']==MODULUS and coeff['donors']==[0,61,62] and coeff['H']==263,
            'source coefficient contract')
    context = native_context(args.repo/'research/moonshot-005-program/results',coeff)
    donors = coeff['donors']
    metadata = {}
    full = Counter()
    per_donor = {}
    all_y = set()
    for j in donors:
        stats = Counter()
        per_donor[j] = {'components':{}}
        perm = {}
        for k in (3,12):
            info,assign,dst,stream = component_word(k,j,context,coeff,metadata)
            require(not set(assign)&set(perm) and not all_y.intersection(dst),'disjoint original allocations')
            all_y.update(dst)
            perm.update(assign)
            per_donor[j]['components'][k]=info
            save_compressed(args.out/f'REDUCE-{j}-{k}.bin.gz',stream)
            stats['basis_ADD'] += info['all_eight_pairs_pure_ADD']
            stats['write_ADD'] += info['cache_write_ADD']
            for field in ('read_ADD','INIT','dirty_CLEAR'):
                stats[field] += info['cache_read_ADD']
        require(set(perm)==set(range(BANK*j,BANK*(j+1))),'all true X-owner outputs')
        swaps = permutation_swaps(perm)
        metadata[f'{j}-swaps']=swaps
        stats['permutation_ADD']=len(swaps)*3*DEGREE
        stats['inverse_ADD']=stats['basis_ADD']+stats['permutation_ADD']
        stats['forward_ADD']=stats['inverse_ADD']+stats['write_ADD']+stats['read_ADD']
        stats['total_ADD']=stats['forward_ADD']+stats['inverse_ADD']
        per_donor[j]['one_genuine_native_traversal'] = dict(stats)
        full.update(stats)
    require(len(all_y)==3*24*15*COPIES, 'three donor late quota and unique Y')
    bgraw = args.background.read_bytes()
    bg = json.loads(bgraw)
    require(set(map(int,bg))==set(range(111)), 'all background donor charges present')
    bgstats = Counter()
    for key,record in bg.items():
        if int(key) not in donors:
            bgstats.update(record)
    inv = bgstats['early_basis_ADD']+bgstats['source_owner_permutation_ADD']
    copies = bgstats['snapshot_copy_ADD_INIT_dirty_CLEAR']
    fwd = inv+copies+bgstats['late_evaluation_ADD']
    combined = {'source_forward_ADD':fwd+full['forward_ADD'],
                'source_pure_inverse_ADD':inv+full['inverse_ADD'],
                'source_all_ADD':fwd+inv+full['total_ADD'],
                'source_INIT':copies+full['INIT'],
                'source_dirty_CLEAR':copies+full['dirty_CLEAR'],'source_extra_MOVE':0,
                'all_caches_overlapping_upper_bound':copies+full['INIT']}
    raw = json.dumps(metadata,separators=(',',':'),sort_keys=True).encode()
    digest = save_compressed(args.out/'HOLDER-WORDS.json.gz',raw)
    result = {'field':MODULUS,'bank_field_width':BANK,'special_donors':donors,
              'coefficient_payload':COEFFICIENTS,'route_payload':ROUTES[1],
              'layout_payload':LAYOUT[1],'spread_payload':SPREAD[1],
              'holder_word_payload':digest,'background_price_file_sha256':hashlib.sha256(bgraw).hexdigest(),
              'special_three':dict(full),'by_donor':per_donor,'background_108':dict(bgstats),
              'combined_physical_source':combined,'complete_target_realization':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'special_three':dict(full),'combined':combined},sort_keys=True))

if __name__=='__main__':
    main()
