#!/usr/bin/env python3
"""Exact native port quotients and unavoidable loss for the frozen full45 pair.

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

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'frozen source input '+name)
    base=repo/'research/moonshot-005-program/results';parent=here.parent.parent/'author'
    coefficient,_=read_json(parent/'output/COEFFICIENTS.json.gz');literal_fibres,_=read_json(parent/'output/FIBRES.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots=root_coordinates(layout,basis);planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    maps={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in coefficient['source_maps'].items()}
    proof={};receipts=[];supports=[]
    for h in [263,642]:
        H=coefficient['H'][str(h)];donors=sorted(planes[h]);ports=[d for d,D in enumerate(charts)if planes[h]<=D];word=np.array(H['word'],dtype=np.uint8)
        need(donors==H['donors']and ports==H['ports']and word.shape==(45,45),'actual frozen full H interface')
        viewers=[i for i in range(111)if planes[h]<=adj[i]];need(80 not in viewers and 10 not in donors,'identity target')
        D={};constraints={}
        for i in viewers:
            K=np.array(literal_fibres[str(h)][str(i)]['kernel'],dtype=np.uint8);need(K.shape==(240,15)and rank(K)==15,'literal entire fibre basis')
            D[i]=[]
            for j in donors:
                off=[a for a in maps[j]if a!=h and planes[a]<=adj[i]];X=np.vstack([maps[j][a]for a in off])
                need(X.shape==(225,240)and rank(X)==225 and not np.any(mm(X,K)),'complete off-H kernel at each actual donor')
                central=mm(maps[j][h],K);need(rank(central)==15,'full free H input at fixed off-H side information');D[i].append(central)
            zero=np.zeros((15,15),dtype=np.uint8)
            constraints[i]=np.vstack([np.hstack([D[i][0].T,D[i][1].T,zero]),np.hstack([D[i][0].T,zero,D[i][2].T])])
            need(rank(constraints[i])==30,'one zero-sum translation subspace dimension30')
            rows=[q for q,d in enumerate(ports)if charts[d]<=adj[i]];need(len(rows)==15,'fifteen actual native packets')
            R=[mm(word[np.ix_(rows,range(15*s,15*s+15))],D[i][s])for s in range(3)]
            need(rank(R[0])==15 and all(np.array_equal(R[0],x)for x in R[1:]),'canonical invertible native receiver readout')
        certificates=[];all_rows=[];hist=Counter()
        for q,d in enumerate(ports):
            audience=[i for i in viewers if charts[d]<=adj[i]];need(len(audience)>0,'every physical port has a native audience')
            C=np.vstack([constraints[i]for i in audience]);ell=word[q:q+1]
            need(rank(C)==44 and not np.any(mm(C,ell.T))and rank(ell)==1,'exact one-field common port quotient')
            chosen=[];current_rank=0
            for i in audience:
                proposed=chosen+[i];trial_rank=rank(np.vstack([constraints[v]for v in proposed]))
                if trial_rank>current_rank:chosen=proposed;current_rank=trial_rank
                if current_rank==44:break
            for i in list(chosen):
                reduced=[v for v in chosen if v!=i]
                if reduced and rank(np.vstack([constraints[v]for v in reduced]))==44:chosen=reduced
            small=np.vstack([constraints[i]for i in chosen]);need(rank(small)==44,'small native support reaches same quotient')
            _,cols,_=echelon(small);_,rows,_=echelon(small[:,cols].T);minor=small[np.ix_(rows,cols)]
            need(minor.shape==(44,44)and echelon(minor)[2]!=0,'literal44 minor witnesses exact annihilator dimension')
            basis=null(C).T;need(basis.shape==(1,45)and rank(np.vstack([basis,ell]))==1,'canonical packet generates all admissible linear forms')
            hist[len(chosen)]+=1;all_rows.append(ell);supports.append(len(chosen))
            certificates.append({'D':d,'native_audience':audience,'witness_receivers':chosen,'constraint_rank':44,'constraint_minor_rows':rows,
                                 'constraint_minor_columns':cols,'constraint_minor_determinant':echelon(minor)[2],
                                 'canonical_packet':ell[0].tolist(),'normalized_kernel':basis[0].tolist()})
        joined=np.vstack(all_rows);rk=rank(joined);need(rk==(45 if h==263 else 44),'global ranks of all forced port quotients')
        expected_kernel=np.zeros((45,1),dtype=np.uint8);expected_kernel[[0,15,30]]=1
        if h==642:
            need(not np.any(mm(joined,expected_kernel))and null(joined).shape==(45,1),'one exact information-loss direction')
            complement=np.eye(45,dtype=np.uint8)[0:1];need(rank(np.vstack([joined,complement]))==45,'one independent complement suffices')
        corrupted=joined.copy();corrupted[0,0]^=1;first_audience=certificates[0]['native_audience'];C0=np.vstack([constraints[i]for i in first_audience])
        need(np.any(mm(C0,corrupted[0:1].T)),'changed first packet violates native invariance')
        proof[str(h)]={'donors':donors,'ports':ports,'native_receivers':viewers,'port_certificates':certificates,
                       'global_provider_certificate':certificate(joined)}
        receipts.append({'H':h,'native_receiver_count':len(viewers),'physical_ports':45,'each_port_quotient_dimension':1,
                         'joint_quotient_rank':rk,'information_defect':45-rk,'small_support_histogram':dict(sorted(hist.items()))})
        print('EXACT_NATIVE_PORT_QUOTIENTS',h,len(viewers),45,rk,dict(sorted(hist.items())),flush=True)
    args.out.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps(proof,sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'CERTIFICATES.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    result={'status':'PASS_FULL45_NATIVE_PORT_RIGIDITY','H':receipts,'certificates':90,'constraint_rank':44,
            'maximum_witness_receivers':max(supports),'minimum_required_extra_fields_at_bank3840':16,
            'arbitrary_nonlinear_H_functions':True,'arbitrary_mixing_of_tensor_copies':True,
            'separate_nonlinear_input_bank_gauges':False,'changed_sources':False,
            'complete_downstream_word':False,'new_complete_kappa':False,'payload_sha256':hashlib.sha256(payload).hexdigest()}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],90,44,45,44,16,flush=True)

if __name__=='__main__':main()
