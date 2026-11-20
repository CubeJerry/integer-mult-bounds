#!/usr/bin/env python3
"""Independent all-slot involutive-feedback extension certificates.

No predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and different pivot choices.
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


EXPONENTS = [1,2,3,4,5,6,8,9,10,12,16,17,18,20,24,32,33,34,36,40,48]
FOUR = [0,1,2,4,8,16,32]

def solve_square(A,B):
    n=len(A); rows,pivots,_=echelon(np.hstack([A,B]))
    need(pivots[:n]==list(range(n)), 'invertible square solve')
    X=rows[:n,n:].copy()
    for j in range(n-1,-1,-1):
        if j+1<n: X[j]^=mm(rows[j:j+1,j+1:n],X[j+1:])[0]
    need(np.array_equal(mm(A,X),B),'exact square solve')
    return X

def minor_certificate(A):
    _,cols,_=echelon(A); _,rows,_=echelon(A[:,cols].T)
    _,pivots,det=echelon(A[np.ix_(rows,cols)])
    need(len(pivots)==len(cols) and det!=0,'literal nonzero minor')
    return {'rank':len(cols),'rows':rows,'columns':cols,'determinant':det}

def equation_row(node,eta):
    z=np.array([power(node,p)for p in range(17)],dtype=np.uint8)
    return MUL[z[:,None],eta[None,:]].reshape(-1)

def coefficients(eta,values):
    _,rows,_=echelon(eta.T)
    need(len(rows)==21,'twenty-one independent features')
    result=solve_square(eta[rows],values[rows])
    need(np.array_equal(mm(eta,result),values),'exact feature interpolation')
    return result.T.reshape(-1)


def source_controls(parameters,c):
    I=np.eye(3,dtype=np.uint8);big=np.eye(48,dtype=np.uint8)
    A=np.zeros((3,3),dtype=np.uint8);A[0,1]=1
    B=np.zeros((3,3),dtype=np.uint8);B[2,0]=1
    V=np.zeros((3,48),dtype=np.uint8);V[:,:3]=A;V[:,9:12]=B
    need(not np.any(mm(A,B))and np.any(mm(B,A)),'genuine noncommuting all-slot control')
    outside=np.zeros((3,48),dtype=np.uint8);outside[:,:3]=A;outside[1,9]=1
    def source_column(v):
        cv=np.zeros(16,dtype=np.uint8)
        cv[0]=MUL[INV[power(v,2)],power(v,9)^power(v,18)^power(v,36)^1]^1
        for m,e in [(1,8),(2,16),(4,32),(5,4),(8,1),(14,4)]:cv[m]=MUL[INV[power(v,2)],power(v,e)]
        return kron(cv[:,None],I)
    nonzero_small=0;outside_count=0
    for v in range(1,64):
        C=source_column(v);S=mm(V,C);N=mm(C,V)
        need(rank(C)==3 and not np.any(mm(N,N))and not np.any(mm(S,V)),'all63 large-update involutions')
        need(np.array_equal(mm(big^N,big^N),big),'all63 explicit source inverses')
        nonzero_small+=bool(np.any(S))
        # A small matrix VC being square-zero is strictly weaker than the
        # required large matrix CV being square-zero.
        S2=mm(outside,C);N2=mm(C,outside)
        need(not np.any(mm(S2,S2)),'outside control small matrix remains square-zero')
        need(np.array_equal(mm(big^N2,big^N2^mm(N2,N2)),big),'outside control has a three-term source inverse')
        outside_count+=bool(np.any(mm(N2,N2)))
    need(nonzero_small>0 and outside_count>0,'strict support enlargement and hypothesis boundary')
    shift=np.zeros((16,16),dtype=np.uint8)
    for p in range(16):shift[(p+1)%16,p]=1
    Nc=shift^MUL[c,np.eye(16,dtype=np.uint8)]
    Q=kron(np.array([[power(c,p)for p in range(16)]],dtype=np.uint8),I)^MUL[power(c,16)^1,V]
    U=np.column_stack([u_polynomial(1<<p,c)for p in range(6)])
    moore=np.array([[power(1<<i,1<<j)for j in range(6)]for i in range(6)],dtype=np.uint8)
    values=np.array([mm(V,kron(U[:,p:p+1],I)).reshape(-1)for p in range(6)],dtype=np.uint8)
    linearized=solve_square(moore,values)
    need(np.any(linearized[3])and np.any(linearized[4]),'new v8 and v16 feedback amplitudes are present')
    wrong_readouts=0
    for v in sorted(set(parameters)):
        u=u_polynomial(v,c)[:,None];base=kron(u,I);b=mm(Nc,u);C=source_column(v)
        need(np.array_equal(C,MUL[INV[power(v,2)],kron(b,I)]),'normalised source column')
        K=base^mm(C,mm(V,base))
        need(np.array_equal(K,base^mm(kron(b,I),MUL[INV[power(v,2)],mm(V,base)])),'all-slot scalar normalization')
        d=power(v,8)^int(MUL[power(c,4),power(v,4)])
        need(d!=0 and np.array_equal(mm(Q,K),MUL[d,I]),'involutive central readout cancellation')
        poly=np.zeros(17,dtype=np.uint8);poly[1:]^=u[:,0];poly[:-1]^=MUL[c,u[:,0]]
        off=[a for a in range(64)if a!=c and xor(MUL[poly[p],power(a,p)]for p in range(17))==0]
        need(len(off)==15,'actual fifteen source roots')
        for a in off:
            Qa=kron(np.array([[power(a,p)for p in range(16)]],dtype=np.uint8),I)^MUL[power(a,16)^1,V]
            need(not np.any(mm(Qa,K)),'whole involutive off-H fibre')
        badQ=kron(np.array([[power(c,p)for p in range(16)]],dtype=np.uint8),I)^MUL[power(c,16)^1,outside]
        truncated=base^mm(C,mm(outside,base))
        wrong_readouts+=not np.array_equal(mm(badQ,truncated),MUL[d,I])
    need(wrong_readouts>0,'small-involution control rejects the invalid two-term fibre formula')
    return {'width':3,'source_views':63,'full_fibres_checked':len(set(parameters)),
            'noncommuting':True,'nonzero_VC_views':nonzero_small,'v8_v16_amplitudes_nonzero':True,
            'small_involution_large_noninvolution_views':outside_count,'invalid_two_term_readouts':wrong_readouts}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for path,expected in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==expected,'pinned input '+path)
    base=repo/'research/moonshot-005-program/results'
    layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots=root_coordinates(layout,basis)
    planes,charts=[set(x)for x in layout['A2']],[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    data=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes=data['H_nodes'];params={int(j):{int(i):v for i,v in row.items()}for j,row in data['receiver_parameters'].items()}
    c,h,port,donors=49,263,110,[0,61,62]
    ids=[i for i in range(111)if planes[h]<=adj[i]];aud=[i for i in ids if charts[port]<=adj[i]]
    need(nodes[h]==c and planes[h]==set(donors)and len(ids)==33 and len(aud)==12 and
         80 not in ids and 10 not in donors,'literal native identity-target H263/D110')
    need(EXPONENTS==sorted({(a+b-1)%63+1 for a in [1,2,4,8,16,32]for b in FOUR}),'product exponents')
    stars={j:[p for p,P in enumerate(planes)if j in P]for j in donors}
    off={(j,i):[p for p in stars[j]if p!=h and planes[p]<=adj[i]]for j in donors for i in ids}
    deriv={(j,i):power(params[j][i],8)^int(MUL[power(c,4),power(params[j][i],4)])for j in donors for i in ids}
    for j in donors:
        for i in ids:
            v=params[j][i]
            need(len(off[j,i])==15 and len({nodes[p]for p in off[j,i]})==15,'actual fifteen off-H nodes')
            need(np.array_equal(u_polynomial(v,c),MUL[power(v,2),root_product(nodes[p]for p in off[j,i])]),
                 'actual fifteen-root polynomial identity')
            need(deriv[j,i]!=0,'nonzero central readout')
    exits,quota={},Counter()
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,role,coordinate,plane,d,_,source,_=json.loads(line)
        if plane==h:
            need(phase=='X'and source==role and role in donors,'actual original owner')
            quota[role]+=1;exits.setdefault(d,set()).update((role,coordinate,lane)for lane in range(8))
    need(quota=={0:30,61:30,62:30}and len(exits)==45 and set(map(len,exits.values()))=={16},'physical H263 owner cut')
    need(port in exits and all(sum(len(slots)for d,slots in exits.items()if charts[d]<=adj[i])==240 for i in ids),
         'positive D110 packet and exact240-field cut')
    certificates,summaries,positive_controls=[],[],[]
    for ref in donors:
        eta=np.array([[power(params[ref][i],e)for e in EXPONENTS]for i in ids],dtype=np.uint8)
        need(rank(eta)==21,'native feature rank21')
        tau=np.array([MUL[power(params[ref][i],2),deriv[ref,i]]for i in aud],dtype=np.uint8)
        for other in donors:
            C0=np.array([equation_row(nodes[p],eta[t])for t,i in enumerate(ids)for p in off[other,i]],dtype=np.uint8)
            C1=np.array([equation_row(c,eta[ids.index(i)])for i in aud],dtype=np.uint8)
            C=np.vstack([C0,C1]);rhs=np.r_[np.zeros(len(C0),dtype=np.uint8),tau]
            if ref==other:
                values=np.array([np.r_[MUL[power(params[ref][i],2),u_polynomial(params[ref][i],c)],0]for i in ids],dtype=np.uint8)
                positive=coefficients(eta,values)
                need(np.array_equal(mm(C,positive[:,None])[:,0],rhs),'same-donor exact positive control')
                positive_controls.append({'donor':ref,'polynomial_coefficients':positive.tolist()})
                continue
            mapping,_=binary_map([params[ref][i]for i in ids],[params[other][i]for i in ids])
            poly_basis=[]
            for epsilon in [0,1]:
                for s in FOUR:
                    values=[]
                    for i in ids:
                        u=u_polynomial(params[other][i],c);value=np.r_[u,0]
                        if epsilon:
                            value=np.zeros(17,dtype=np.uint8);value[1:]^=u;value[:-1]^=MUL[c,u]
                        values.append(MUL[power(params[ref][i],s),value])
                    poly_basis.append(coefficients(eta,np.array(values,dtype=np.uint8)))
            Z=np.array(poly_basis,dtype=np.uint8).T
            need(rank(Z)==14 and not np.any(mm(C0,Z)),'fourteen explicit off-row kernel polynomials')
            need(not np.any(mm(C,Z[:,7:])),'seven central-zero kernel polynomials')
            off_minor,full_minor=minor_certificate(C0),minor_certificate(C)
            need(off_minor['rank']==343 and full_minor['rank']==348,'exact ranks343/348')
            central4=np.array([[MUL[deriv[other,i],power(params[ref][i],s)]for s in FOUR]for i in aud],dtype=np.uint8)
            five=np.column_stack([central4,tau]);_,fcols,_=echelon(five);_,chosen,_=echelon(five[:,fcols].T)
            five_matrix=five[np.ix_(chosen,fcols)];_,fp,fd=echelon(five_matrix)
            need(rank(central4)==5 and len(fp)==6 and fd!=0,'six-receiver incompatibility')
            independent=np.column_stack([C[:,full_minor['columns']],rhs]);_,selected,_=echelon(independent.T)
            need(len(selected)==349,'augmented rank349')
            target=np.zeros((349,1),dtype=np.uint8);target[-1,0]=1
            weights=np.zeros(len(C),dtype=np.uint8)
            weights[selected]=solve_square(independent[selected].T,target)[:,0]
            need(not np.any(mm(weights[None,:],C))and mm(weights[None,:],rhs[:,None])[0,0]==1,'wC=0 and wb=1')
            corrupt=weights.copy();corrupt[np.flatnonzero(weights)[0]]^=1
            need(np.any(mm(corrupt[None,:],C)),'corrupted annihilator rejected')
            summary={'reference':ref,'companion':other,'off_rank':343,'rank':348,'augmented_rank':349,
                     'matrix_shape':list(C.shape),'central_witness_receivers':[aud[t]for t in chosen],
                     'central_witness_determinant':fd,'central_witness_columns':fcols,'annihilator_nonzero_weights':int(np.count_nonzero(weights))}
            summaries.append(summary)
            certificates.append({**summary,'parameter_map_columns':[mapping[1<<p]for p in range(6)],
                                 'off_minor':off_minor,'full_minor':full_minor,'central_witness_matrix':five_matrix.tolist(),
                                 'annihilator':weights.tolist(),'C_sha256':hashlib.sha256(C.tobytes()).hexdigest(),
                                 'rhs_sha256':hashlib.sha256(rhs.tobytes()).hexdigest()})
    controls=source_controls([params[j][i]for j in donors for i in ids],c)
    result={'status':'PASS_ALL_SLOT_INVOLUTIVE_FEEDBACK_EXTENSION','H':h,'D':port,'centre':c,'donors':donors,
            'native_receivers':ids,'port_audience':aud,'feature_exponents':EXPONENTS,'feature_dimension':21,
            'all_six_orientations':summaries,'actual_polynomial_fibres':99,'actual_H_owner_fields':720,
            'actual_visible_fields':240,'actual_D_packet_fields':16,'same_donor_positive_controls':3,
            'source_controls':controls,'GF64_linear_input_gauges':True,'arbitrary_binary_linear_input_gauges':False,
            'nonlinear_H_and_downstream':True,'all_width_tensor_lift':True,
            'all_reference_slots_involutive_feedback':True,'general_conditional_feedback':False,'companion_polynomial_degree_bound':16,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    literal={'row_order':'receiver increasing, then companion off-H plane increasing; then central audience increasing',
             'column_order':'z degree0..16, then feature exponent in RESULT order',
             'off_H_planes':{str(j):{str(i):off[j,i]for i in ids}for j in donors},
             'cases':certificates,'same_donor_positive_controls':positive_controls}
    (args.out/'CERTIFICATES.json').write_text(json.dumps(literal,indent=2,sort_keys=True)+'\n')
    print(result['status'],6,343,348,349,110,flush=True)

if __name__=='__main__':main()
