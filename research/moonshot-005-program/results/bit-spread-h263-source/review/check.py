#!/usr/bin/env python3
"""Independent H263 review using field arrays and the actual owner routes."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip
import json
import numpy as np

def require(t, msg):
    if not t: raise ValueError(msg)

def field():
    log = np.full(64, -1, dtype=int)
    anti = np.zeros(126, dtype=np.uint8)
    a = 1
    for t in range(63):
        require(log[a] == -1, 'multiplicative repeat')
        log[a] = t
        anti[t] = a
        a *= 2
        if a & 64: a ^= 0x43
    require(a == 1 and np.all(log[1:] >= 0), 'GF64 multiplicative group')
    anti[63:] = anti[:63]
    prod = np.zeros((64, 64), dtype=np.uint8)
    prod[1:, 1:] = anti[log[1:, None] + log[None, 1:]]
    inv = np.zeros(64, dtype=np.uint8)
    inv[1:] = anti[63-log[1:]]
    return prod, inv

MUL, INVERSE = field()

def eliminate(A, B=None):
    """Rank and transformed RHS using the independently rebuilt field."""
    A = np.asarray(A, dtype=np.uint8)
    n, w = A.shape
    M = A.copy() if B is None else np.hstack((A, B)).astype(np.uint8)
    r = 0
    for col in range(w):
        inds = np.nonzero(M[r:, col])[0]
        if not len(inds): continue
        p = r + int(inds[-1])
        if p != r: M[[p, r]] = M[[r, p]]
        M[r] = MUL[INVERSE[M[r, col]], M[r]]
        use = np.flatnonzero(M[:, col]) if B is not None else np.flatnonzero(M[r+1:, col]) + r + 1
        use = use[use != r]
        if len(use): M[use] ^= MUL[M[use, col, None], M[r][None, :]]
        r += 1
        if r == n: break
    return r, M[:, w:]

def matmul(A, B):
    A, B = np.asarray(A,dtype=np.uint8), np.asarray(B,dtype=np.uint8)
    out = np.zeros((len(A), B.shape[1]),dtype=np.uint8)
    for u in range(A.shape[1]):
        use = np.flatnonzero(A[:, u])
        out[use] ^= MUL[A[use, u, None], B[u, None, :]]
    return out

def power_matrix(nodes, n):
    V = np.ones((len(nodes),n),dtype=np.uint8)
    x = np.array(nodes,dtype=np.uint8)
    for i in range(1,n): V[:,i] = MUL[V[:,i-1],x]
    return V

def read_source(base, name, digest):
    raw = gzip.decompress((base/name).read_bytes())
    require(sha256(raw).hexdigest() == digest, f'source payload {name}')
    return raw

def geometry(base):
    layout = json.loads(read_source(base, 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
        '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'))
    spread = json.loads(read_source(base, 'bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz',
        '7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab'))
    routes_raw = read_source(base, 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
        '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    roots = np.array(layout['root_table'],dtype=int)
    perp = [frozenset(np.flatnonzero(row)) for row in roots @ roots.T == 0]
    H, D = list(map(frozenset,layout['A2'])), list(map(frozenset,layout['D4']))
    donors = sorted(H[263])
    require(donors == [0,61,62], 'special roots')
    ports = [d for d,C in enumerate(D) if H[263] <= C]
    recipients = [i for i in range(120) if H[263] <= perp[i]]
    live = [i for i in recipients if i < 111]
    require(len(ports)==45 and len(live)==33 and len(recipients)==36, 'H263 counts')
    require(80 not in live and 10 not in donors, 'unchanged target edges')
    visible = {i:[d for d in ports if D[d]<=perp[i]] for i in recipients}
    marked = set(spread['selected_D'])
    parts = {3:sorted(set(ports)&marked),12:sorted(set(ports)-marked)}
    rad = {d:frozenset(spread['D_radicals'][d])-{0} for d in ports}
    point = {}
    for j in donors:
        point[j] = {}
        for h,plane in enumerate(H):
            if j not in plane or h == 263: continue
            incident = [d for d in ports if plane <= D[d]]
            require(len(incident)==5, 'five incident H263 ports')
            label = set.intersection(*(set(rad[d]) for d in incident))
            require(len(label)==1, 'unique coordinate-free off-plane label')
            point[j][h] = label.pop()
        require(len(point[j])==len(set(point[j].values()))==27, 'bijective 27 points')
    require(len(set.intersection(*(set(p.values()) for p in point.values())))==27, 'common off-H point dictionary')
    views = {(j,int(i)):sorted(h for h,P in enumerate(H) if j in P and P <= perp[i]) for j in donors for i in perp[j]}
    require(all(len(hs)==16 for hs in views.values()), '16 native/geometric planes of each view')
    for i in recipients:
        sets = [set(point[j][h] for h in views[j,i] if h!=263) for j in donors]
        require(len(sets[0]) == 15 and sets[0]==sets[1]==sets[2], 'three native off-H kernels share one view')
        for d in ports: require(len(sets[0]&rad[d])==(3 if d in visible[i] else 1), 'one or three shares')
        require(all(len(set(visible[i])&set(parts[k]))==k for k in (3,12)), 'spread view count')
    counts, hflags = Counter(), Counter()
    slots = set()
    h_actual = []
    for line in routes_raw.splitlines():
        phase,j,c,h,d,*_ = json.loads(line)
        if phase=='X':
            require((j,c) not in slots, 'original owner used twice')
            slots.add((j,c))
            counts[j,h] += 1
        if h==263:
            hflags[phase,d]+=1
            h_actual.append((j,c,d))
    require(len(slots)==111*480, 'original X extents')
    require(hflags==Counter({('X',d):2 for d in ports}), 'fully early physical cut')
    require(all(counts[j,263]==30 and sum(counts[j,h] for h in point[j])==450 for j in donors),
            'true early quotas')
    return donors, recipients, visible, parts, point, views, counts, rad, h_actual, (H,perp)

def read_matrix(rows, shape):
    M = np.asarray(rows)
    require(M.shape == shape and M.dtype.kind in 'ui' and M.min() >= 0 and M.max() < 64,
            'matrix field, shape and range')
    return M.astype(np.uint8)

def compare_physical_h(donors, parts, rows):
    # Layout required by the independently supplied fully-early V word.
    # Each donor in ascending exponent order supplies 16 consecutive spinor
    # lanes. Actual port records in each flag are sorted independently.
    at_input = {j:sorted((j,coord,c) for root,coord,d in rows if root==j for c in range(8)) for j in donors}
    at_output = {d:sorted((j,coord,c) for j,coord,dd in rows if d==dd for c in range(8))
                 for ds in parts.values() for d in ds}
    mapping = {}
    for k,offset in [(3,0),(12,3*16)]:
        for p,d in enumerate(parts[k]):
            donor,degree = divmod(p,k)
            for spin in range(16):
                mapping[at_output[d][spin]] = at_input[donors[donor]][offset+degree*16+spin]
    require(set(mapping)==set(mapping.values()) and len(mapping)==720, 'genuine 720-owner H263 column/row bijection')
    return sha256(json.dumps(sorted(mapping.items()),separators=(',',':')).encode()).hexdigest()

def verify_component(k, package, geometry_data):
    donors, rec, visible, parts, points, views, counts, rad, _, _ = geometry_data
    N = 16*k
    eye = np.eye(N,dtype=np.uint8)
    source, coef = {}, {}
    F = {int(x):read_matrix(a,(k,N)) for x,a in package['off_H'].items()}
    require(set(F)==set(points[donors[0]].values()), 'all 27 published off-plane arrays')
    for di,j in enumerate(donors):
        source[j] = {h:F[x] for h,x in points[j].items()}
        source[j][263] = eye[di*k:(di+1)*k]
        coef[j] = {int(h):read_matrix(a,(k,2*k)) for h,a in package['early'][str(j)].items()}
    # Direct field solves check the inverse, not only dimensions or screens.
    n_native, n_all, same, native_same = 0,0,0,0
    fibre_sha = sha256()
    cache_ranks = {}
    native_fail = None
    gauge_failure = None
    for (j,i), hs in sorted(views.items()):
        if 263 not in hs:
            key=tuple(sorted(points[j][p] for p in hs))
            if key not in cache_ranks: cache_ranks[key]=eliminate(np.vstack([F[x] for x in key]))[0]
            require(cache_ranks[key]==N,'exterior native/parent full rank')
        n_native += int(i<111)
        n_all += 1
    for i in rec:
        vis_ord = [p for p,d in enumerate(parts[k]) if d in visible[i]]
        V = power_matrix([p+1 for p in vis_ord],3*k)
        lifts = []
        for di,j in enumerate(donors):
            hs = [h for h in views[j,i] if h!=263]
            M = V[:,di*k:(di+1)*k]
            rank, inv = eliminate(M,np.eye(k,dtype=np.uint8))
            require(rank==k and np.array_equal(matmul(M,inv),np.eye(k,dtype=np.uint8)), 'actual H donor submatrix inverse')
            # Rank and solve the full native stacked map, with the H263 block first.
            A = np.vstack([source[j][263]]+[source[j][h] for h in hs])
            B = np.zeros((N,k),dtype=np.uint8)
            B[:k] = inv
            r,L = eliminate(A,B)
            require(r==N and np.array_equal(matmul(A,L),B), 'original-coordinate inverse with honest H and off-H')
            if j==donors[0] and i==rec[0]:
                mutant = L.copy()
                mutant[di*k] ^= 1
                require(not np.array_equal(matmul(A,mutant),B),'faulty original-coordinate lift')
                native_fail = True
                # A nontrivial bijective relabelling of donor zero's H quotient
                # keeps every view and pure early rank but breaks this frozen word.
                bad_A = A.copy()
                bad_A[:k] = MUL[2,bad_A[:k]]
                br,bl = eliminate(bad_A,B)
                gauge_failure = br==N and not np.array_equal(bl,L)
                require(gauge_failure,'rank-preserving one-donor relabel breaks common graph')
            lifts.append(L)
        require(np.array_equal(lifts[0],lifts[1]) and np.array_equal(lifts[0],lifts[2]), 'three ORIGINAL-COORDINATE lifts equal')
        same += 1
        native_same += int(i<111)
        fibre_sha.update(lifts[0].tobytes())
    require(n_native==174 and same==36 and native_same==33 and native_fail, 'full intended H263 coverage')
    early_ranks, early_counts = {},Counter()
    for j in donors:
        halves = {h for h in source[j] if counts[j,h]==15}
        require(set(coef[j]) == halves, 'one true half-frame at every actual half incidence')
        all_rows = []
        for h,S in sorted(source[j].items()):
            diag = np.kron(np.eye(2,dtype=np.uint8),S)
            if h in halves:
                E = coef[j][h]
                tails = package['complementary_late_coordinate_rows'][str(j)][str(h)]
                require(len(set(tails))==len(tails)==k and all(0<=v<2*k for v in tails), 'complementary late inputs')
                completion = np.vstack([E,np.eye(2*k,dtype=np.uint8)[tails]])
                require(eliminate(completion)[0]==2*k,'actual late supplement preserves quotient')
                all_rows.append(matmul(E,diag))
            else:
                require(counts[j,h]==30, 'full early special incidence')
                all_rows.append(diag)
            early_counts[counts[j,h]] += 1
        A = np.vstack(all_rows)
        require(A.shape==(2*N,2*N), 'pair-lane early owner count')
        early_ranks[j]=eliminate(A)[0]
        require(early_ranks[j]==2*N, 'genuine early source bijection')
    # Dynamics of the 16 common coefficient blocks on the copy axis. One
    # nonzero commutator defeats global pairwise commutation in these coordinates.
    key = None
    for x,A in sorted(F.items()):
        blocks = np.split(A,16,axis=1)
        for s in range(16):
            for t in range(s):
                comm = matmul(blocks[s],blocks[t]) ^ matmul(blocks[t],blocks[s])
                if np.any(comm):
                    key = {'point':x,'s':s,'t':t,'rank':eliminate(comm)[0]}
                    break
            if key: break
        if key: break
    require(key is not None, 'commuting-source gate requires an actual noncommutation witness')
    return {'k':k,'native_foreign_views':n_native,'parent_foreign_views':n_all,
            'distinct_exterior_types':len(cache_ranks),'joint_tight_graphs':native_same,
            'geometric_graphs':same,'canonical_lift_sha256':fibre_sha.hexdigest(),
            'actual_early_ranks_per_two_spinor_lanes':early_ranks,
            'early_quota_histogram':dict(early_counts),'noncommuting_copy_block':key,
            'rank_preserving_donor_relabel_breaks_common_fibre':gauge_failure}

def generic_and_dense_invoice(data):
    donors = data[0]
    count = data[6]
    H,perp = data[9]
    profile = Counter(count.values())
    require(profile=={15:2675,30:422,45:11},'all actual donor-plane genuine quotas')
    generic_views = 0
    early_checks = 0
    for j in range(111):
        if j in donors: continue
        labels = sorted(h for h,P in enumerate(H) if j in P)
        nodes = {h:t+1 for t,h in enumerate(labels)}
        require(len(labels)==28,'complete ordinary donor star')
        for i in perp[j].intersection(range(111)):
            selected = [nodes[h] for h in labels if H[h]<=perp[i]]
            require(len(set(selected))==16, 'ordinary interpolation chart')
            generic_views += 1
        both = [nodes[h] for h in labels if count[j,h]>=30]
        split = [nodes[h] for h in labels if count[j,h]==15]
        split.extend(29+r for r,h in enumerate(h for h in labels if count[j,h]==45))
        n = 16-len(both)
        require(len(split)==2*n, 'exact number of true early half slots')
        for subset in (split[:n],split[n:]):
            require(len(set(both+subset))==16 and eliminate(power_matrix(both+subset,16))[0]==16,
                    'genuine ordinary early matrix')
            early_checks += 1
    require(generic_views==6296 and early_checks==216,'remaining generic donors')
    M = 6*3840
    L = profile[15]*120*6
    dense = 2*111*(M*M+3*M)+L*(M+1)
    return {'ordinary_native_quotient_views_other_108':generic_views,'ordinary_two_lane_checks':early_checks,
            'late_INIT_and_dirty_CLEAR_each':L,'dense_source_ADD_upper_bound':dense,
            'singleton_extra_genuine_early_fields':profile[45]*120}

def main():
    p = ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--author',type=Path,default=Path(__file__).resolve().parents[1]/'author')
    p.add_argument('--out',type=Path,required=True)
    args = p.parse_args()
    base = args.repo/'research/moonshot-005-program/results'
    data = geometry(base)
    cpath = args.author/'output/COEFFICIENTS.json.gz'
    raw = gzip.decompress(cpath.read_bytes())
    co = json.loads(raw)
    require(co['H']==263 and co['donors']==data[0] and co['field_polynomial']==0x43, 'coefficient header')
    physical = compare_physical_h(data[0],data[3],data[8])
    report = {'review':'PASS_H263_ORIGINAL_COORDINATE_AND_PHYSICAL_SOURCE',
              'coefficient_payload_sha256':sha256(raw).hexdigest(),
              'H263_sorted_owner_bijection_sha256':physical,'new_complete_kappa':False,
              'all_source_and_dense_invoice':generic_and_dense_invoice(data),
              'components':[verify_component(k,co['components'][str(k)],data) for k in (3,12)]}
    args.out.mkdir(exist_ok=True,parents=True)
    (args.out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':
    main()
