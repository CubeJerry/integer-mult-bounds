#!/usr/bin/env python3
"""Exact two-source proper-D cut obstruction for the frozen full45 H pair.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and last available pivot rows.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise AssertionError(message)


def xor(values):
    answer = 0
    for value in values:
        answer ^= int(value)
    return answer


def product(x, y):
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result


MUL = np.array([[product(x, y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(y for y in range(1, 64) if MUL[x, y] == 1)
                           for x in range(1, 64)], dtype=np.uint8)


def power(x, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = int(MUL[answer, x])
        x = int(MUL[x, x])
        exponent >>= 1
    return answer


def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    answer = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for col in range(left.shape[1]):
        answer ^= MUL[left[:, col, None], right[col, None, :]]
    return answer


def kron(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    return MUL[left[:, None, :, None], right[None, :, None, :]].reshape(
        left.shape[0] * right.shape[0], left.shape[1] * right.shape[1])


def echelon(matrix):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    determinant = 1
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        chosen = row + int(choices[-1])
        matrix[[row, chosen]] = matrix[[chosen, row]]
        determinant = int(MUL[determinant, matrix[row, col]])
        matrix[row, col:] = MUL[INV[matrix[row, col]], matrix[row, col:]]
        if row + 1 < len(matrix):
            matrix[row + 1:, col:] ^= MUL[matrix[row + 1:, col, None], matrix[row, None, col:]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots, determinant


def rank(matrix):
    return len(echelon(matrix)[1])


def null(matrix):
    rows, pivots, _ = echelon(matrix)
    free = [j for j in range(rows.shape[1]) if j not in pivots]
    result = np.zeros((rows.shape[1], len(free)), dtype=np.uint8)
    result[free] = np.eye(len(free), dtype=np.uint8)
    for i in range(len(pivots) - 1, -1, -1):
        result[pivots[i]] = mm(rows[i:i + 1, pivots[i] + 1:], result[pivots[i] + 1:])[0]
    need(not np.any(mm(matrix, result)), 'independent nullspace identity')
    return result


def certificate(matrix):
    _, cols, _ = echelon(matrix)
    _, rows, _ = echelon(matrix[:, cols].T)
    minor = matrix[np.ix_(rows, cols)]
    _, pivots, determinant = echelon(minor)
    kernel = null(matrix)
    need(len(pivots) == len(cols) and determinant != 0, 'nonzero maximal minor')
    need(rank(kernel) == matrix.shape[1] - len(cols), 'independent upper-rank certificate')
    return {'shape': list(matrix.shape), 'rank': len(cols), 'minor_rows': rows,
            'minor_columns': cols, 'minor_determinant': determinant,
            'kernel_columns': kernel.tolist(), 'matrix_sha256': hashlib.sha256(matrix.tobytes()).hexdigest()}


def quadratic(x):
    return ((x & (x >> 1)) & 85).bit_count() & 1


def polar(x, y):
    return (x & (((y & 85) << 1) | ((y & 170) >> 1))).bit_count() & 1


def root_coordinates(layout, basis):
    columns = basis['lattice_basis_columns']
    lattice = [[columns[j][i] for j in range(8)] for i in range(8)]
    hyperbolic = basis['hyperbolic_basis_masks']
    reverse = {xor(hyperbolic[j] for j in range(8) if mask >> j & 1): mask for mask in range(256)}
    need(len(reverse) == 256, 'binary lattice coordinate isomorphism')
    roots = []
    for original in layout['root_table']:
        coordinates = [0] * 8
        for i in range(7, -1, -1):
            coordinates[i], remainder = divmod(original[i] - sum(lattice[i][j] * coordinates[j]
                                                               for j in range(i + 1, 8)), lattice[i][i])
            need(remainder == 0, 'exact integral root coordinates')
        roots.append(reverse[sum((x & 1) << i for i, x in enumerate(coordinates))])
    need(len(set(roots)) == 120 and set(roots) == {x for x in range(256) if quadratic(x)},
         'all actual anisotropic root labels')
    return roots


def u_polynomial(v, centre):
    numerator = np.zeros(17, dtype=np.uint8)
    for degree, coefficient in [(8, v), (16, power(v, 2)), (14, power(v, 4)),
                                (5, power(v, 4)), (1, power(v, 8)),
                                (2, power(v, 16)), (4, power(v, 32))]:
        numerator[degree] ^= coefficient
    numerator[0] = xor(MUL[numerator[d], power(centre, d)] for d in range(1, 17))
    answer = np.zeros(16, dtype=np.uint8)
    answer[15] = numerator[16]
    for d in range(14, -1, -1):
        answer[d] = numerator[d + 1] ^ MUL[centre, answer[d + 1]]
    need(numerator[0] == MUL[centre, answer[0]], 'exact division by z+centre')
    return answer


def root_product(nodes):
    result = np.array([1], dtype=np.uint8)
    for node in sorted(nodes):
        new = np.zeros(len(result) + 1, dtype=np.uint8)
        new[1:] ^= result
        new[:-1] ^= MUL[node, result]
        result = new
    return result


def binary_map(inputs, outputs):
    pairs = dict(zip(inputs, outputs))
    basis, span = [], {0: 0}
    for v in inputs:
        if v not in span:
            basis.append(v)
            span.update({w ^ v: image ^ pairs[v] for w, image in list(span.items())})
    need(len(basis) == 6 and len(span) == len(set(span.values())) == 64,
         'independent full binary parameter isomorphism')
    need(all(span[v] == w for v, w in zip(inputs, outputs)), 'all native parameter images')
    return span, basis


def inverse(A):
    n = len(A)
    R, pivots, _ = echelon(np.hstack((A, np.eye(n, dtype=np.uint8))))
    need(pivots == list(range(n)), 'invertible square matrix')
    for i in range(n - 1, -1, -1):
        R[:i, i:] ^= MUL[R[:i, i, None], R[i, None, i:]]
    answer = R[:, n:]
    need(np.array_equal(mm(A, answer), np.eye(n, dtype=np.uint8)), 'inverse residual')
    return answer


def q(x):
    return power(x, 9) ^ power(x, 18) ^ power(x, 36)


def field_polar(x, y):
    return q(x ^ y) ^ q(x) ^ q(y)


def witt(space, form):
    space, answer = set(space), []
    while len(space) > 1:
        b = lambda x, y: form(x ^ y) ^ form(x) ^ form(y)
        zeros = sorted(x for x in space if x and not form(x))
        if zeros:
            first = zeros[0]
            second = next(x for x in zeros if b(first, x))
        else:
            first = min(space - {0})
            second = min(space - {0, first})
        answer += [first, second]
        space = {x for x in space if not b(x, first) and not b(x, second)}
    return answer


def binary_span(values):
    span = {0}
    for value in values:
        span |= {x ^ value for x in list(span)}
    return span


def read_json(path):
    raw = path.read_bytes()
    if path.suffix == '.gz':
        raw = gzip.decompress(raw)
    return json.loads(raw), raw


def coefficients(tag,shape):
    return np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(int(np.prod(shape))),dtype=np.uint8).reshape(shape)&63

def block_diag(matrices):
    answer=np.zeros((sum(len(M)for M in matrices),sum(M.shape[1]for M in matrices)),dtype=np.uint8)
    r=c=0
    for M in matrices:
        answer[r:r+len(M),c:c+M.shape[1]]=M;r+=len(M);c+=M.shape[1]
    return answer

def hermite(node):
    return np.array([[power(node,d-s)if(d&s)==s else 0 for d in range(30)]for s in range(2)],dtype=np.uint8)

def binary_rank(rows):
    basis={}
    for row in rows:
        x=int(row)
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return len(basis)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'frozen input '+name)
    base=repo/'research/moonshot-005-program/results';parent=here.parent.parent/'author'
    coeff,_=read_json(parent/'output/COEFFICIENTS.json.gz');fibres,_=read_json(parent/'output/FIBRES.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots=root_coordinates(layout,basis);planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    routes=[json.loads(row)for row in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
    maps={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in coeff['source_maps'].items()}
    common=sorted(set(coeff['H']['263']['ports'])&set(coeff['H']['642']['ports']))
    need(common==[296,733,825,1509,1852],'five actual common D charts')
    canonical_indices=[0,1,2,4,8,9,14,30,59]
    canonical_all=[(1<<i)|sum(1<<j for j in adj[i]if j<111)for i in range(111)]
    canonical=[canonical_all[i]for i in canonical_indices]
    need(binary_rank(canonical)==binary_rank(canonical_all)==9,'actual retained rank-nine canonical space')
    witness_list=[]
    for i,d,other_d,want in [(4,733,825,20),(6,1509,302,30)]:
        h=263;comparison_h=642;source=0;comparison_source=45
        need(source in planes[h]and comparison_source not in planes[h]and comparison_source in planes[comparison_h], 'separate source and comparison centres')
        need(charts[d]<=adj[i]and charts[other_d]<=adj[i]and d!=other_d and (planes[h]|planes[comparison_h])<=charts[d],'actual visible distinct D flags')
        outside=[j for j in range(111)if j not in adj[i]];mask=sum(1<<j for j in outside)
        need(binary_rank([row&mask for row in canonical])==9,'outside foreign set neutralizes all nine canonical fields')
        visible={j:[a for a in maps[j]if planes[a]<=adj[i]]for j in [source,comparison_source]}
        for j in visible:need(len(visible[j])==16 and rank(np.vstack([maps[j][a]for a in visible[j]]))==240,'complete240-dimensional source cut')
        entry=fibres[str(h)][str(i)];K=np.array(entry['kernel'],dtype=np.uint8);R=np.array(entry['readout'],dtype=np.uint8)
        need(K.shape==(240,15)and rank(K)==15 and rank(R)==15,'whole source fibre and full common H readout')
        p=entry['ports'].index(d);v=mm(K,inverse(R)[:,p:p+1]);need(rank(v)==1,'nonzero isolated direction')
        zero_planes=[a for a in visible[source]if a!=h]
        need(len(zero_planes)==15 and not np.any(mm(np.vstack([maps[source][a]for a in zero_planes]),v)),'all other visible source emissions vanish')
        H=coeff['H'][str(h)];P=np.array(H['word'],dtype=np.uint8);s=H['donors'].index(source);visible_rows=[q for q,D in enumerate(H['ports'])if charts[D]<=adj[i]]
        image=mm(P[np.ix_(visible_rows,range(15*s,15*s+15))],mm(maps[source][h],v));unit=np.zeros((15,1),dtype=np.uint8)
        unit[[q for q,D in enumerate([H['ports'][t]for t in visible_rows])if D==d]]=1
        need(np.array_equal(image,unit),'exactly one visible H packet at D')
        B=coeff['H'][str(comparison_h)];Q=np.array(B['word'],dtype=np.uint8);s=B['donors'].index(comparison_source);q=B['ports'].index(other_d)
        functional=mm(Q[q:q+1,15*s:15*s+15],maps[comparison_source][comparison_h])
        value=int(mm(functional,v)[0,0]);need(value==want and value!=0,'nonzero outside-D comparison packet')
        left_boundary=[(t,row)for t,row in enumerate(routes)if row[3]in visible[comparison_source]and charts[row[4]]<=adj[i]]
        need(len(left_boundary)==480,'all480 physical left-boundary fields')
        groups=Counter(row[4]for _,row in left_boundary);need(len(groups)==60 and set(groups.values())=={8}and groups[d]==8,'sixty disjoint8-field groups')
        outputs=[(t,row)for t,row in enumerate(routes)if row[4]==d and row[5]is not None and i in planes[row[5]]]
        outgoing_K=sorted({row[5]for _,row in outputs});need(len(outgoing_K)==4 and len(outputs)==8,'four-K eight-field proper capacity')
        need(all(sum(row[5]==k for _,row in outputs)==2 for k in outgoing_K),'two fields on each actual right flag')
        early_count=sum(row[0]=='X'for _,row in outputs);late_count=sum(row[0]=='Y'for _,row in outputs)
        closures=[(t,row)for t,row in enumerate(routes)if row[4]==d and row[0]=='X'and row[5]is None]
        for centre in [h,comparison_h]:
            h_routes=[row for row in routes if row[3]==centre]
            need(len(h_routes)==90 and all(row[0]=='X'for row in h_routes),'both frozen H words fully early; no late H-to-D slots')
        component='complementary12'if not np.any(v[:48])else 'protected3'
        need(component==('complementary12'if d==733 else 'protected3'),'separate component witness')
        if component=='protected3':need(not np.any(v[48:])and not np.any(functional[:,48:]),'protected-only witness')
        else:need(not np.any(functional[:,:48]),'complement-only witness')
        witness_list.append({'receiver':i,'D':d,'source_H':h,'source_donor':source,'comparison_H':comparison_h,'comparison_donor':comparison_source,
          'other_D':other_d,'component':component,'nonzero_pairing':value,'direction':v[:,0].tolist(),'functional':functional[0].tolist(),
          'source_zero_planes':zero_planes,'comparison_visible_planes':visible[comparison_source],
          'source_H_visible_ports':[H['ports'][q]for q in visible_rows],'source_H_packet_values':image[:,0].tolist(),
          'source_readout_determinant':echelon(R)[2],'native_foreign_set':sorted(adj[i]&set(range(111))),
          'canonical_outside_columns':outside,'canonical_outside_rank':9,'physical_boundary_groups':dict(sorted(groups.items())),
          'proper_K':outgoing_K,'proper_output_route_ids':[t for t,_ in outputs],'proper_output_routes':[row for _,row in outputs],
          'early_proper_fields':early_count,'late_proper_fields':late_count,'early_Hub_closure_routes':closures,
          'base_required_fields':10,'base_capacity_fields':8,'bank3840_required_fields':80,'bank3840_capacity_fields':64})
        print('EXACT_SHARED_D_WITNESS',i,d,other_d,value,component,early_count,late_count,flush=True)
    census=[]
    for d in common:
        viewers=[i for i in range(111)if charts[d]<=adj[i]];failed=[]
        for i in viewers:
            e=fibres['263'][str(i)];K=np.array(e['kernel'],dtype=np.uint8);R=np.array(e['readout'],dtype=np.uint8);p=e['ports'].index(d);v=mm(K,inverse(R)[:,p:p+1])
            B=coeff['H']['642'];Q=np.array(B['word'],dtype=np.uint8);s=B['donors'].index(45);others=[q for q,D in enumerate(B['ports'])if D!=d and charts[D]<=adj[i]]
            z=mm(Q[np.ix_(others,range(15*s,15*s+15))],mm(maps[45][642],v));nz=np.flatnonzero(z[:,0]);need(len(nz)>0,'gate at every common-D native cut')
            q=int(nz[0]);failed.append({'receiver':i,'other_D':B['ports'][others[q]],'nonzero_pairing':int(z[q,0])})
        census.append({'D':d,'native_receiver_count':len(viewers),'witnesses':failed})
    need(sum(r['native_receiver_count']for r in census)==57,'all57 common-D native cuts')
    args.out.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps({'minimal_witnesses':witness_list,'census':census,'canonical_basis_indices':canonical_indices},sort_keys=True,separators=(',',':'))+'\n').encode()
    (args.out/'WITNESS.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    result={'status':'PASS_FROZEN_PAIR_SHARED_D_OBSTRUCTION','primary_witness':[4,733,825,20],'protected_control':[6,1509,302,30],
      'common_D':common,'native_cuts_failed':57,'bank3840_proper_fields_required':80,'bank3840_proper_fields_available':64,
      'arbitrary_remaining_H_D_K_F_functions':True,'arbitrary_copy_mixing':True,'fixed_five_sources_and_two_H_words':True,
      'requires_no_extra_informative_nonproper_channel':True,'canonical_neutralization_checked':True,
      'new_complete_kappa':False,'witness_payload_sha256':hashlib.sha256(payload).hexdigest()}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],4,733,825,20,57,80,64,flush=True)

if __name__=='__main__':main()
