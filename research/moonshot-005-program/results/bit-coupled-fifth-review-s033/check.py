#!/usr/bin/env python3
"""Independent GF64 check of the actual receiver gate and overlap lift."""
from pathlib import Path
import argparse, gzip, hashlib, json
import numpy as np

HERE = Path(__file__).resolve().parent
PREFIX = 'research/moonshot-005-program/results/'
INPUTS = [
    PREFIX+'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',
    PREFIX+'bit-simultaneous-d1509-s032/output/D-WORD.json.gz',
    PREFIX+'bit-d1509-coupled-repair-s032/DATA.json.gz',
    PREFIX+'bit-fifth-receiver-quotient-s032/FORCED-COLLISION.json',
]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)

def gf_product(x, y):
    result = 0
    for _ in range(6):
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result

MUL = np.array([[gf_product(x,y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0]+[next(y for y in range(1,64) if gf_product(x,y)==1) for x in range(1,64)], dtype=np.uint8)

def mm(A, B):
    A = np.asarray(A, dtype=np.uint8)
    B = np.asarray(B, dtype=np.uint8)
    out = np.zeros((A.shape[0], B.shape[1]), dtype=np.uint8)
    for k in range(A.shape[1]):
        out ^= MUL[A[:,k,None], B[None,k,:]]
    return out

def rref(A):
    A = np.array(A, dtype=np.uint8, copy=True)
    row, pivots = 0, []
    for col in range(A.shape[1]):
        nonzero = np.flatnonzero(A[row:,col])
        if not len(nonzero):
            continue
        q = row+int(nonzero[0])
        A[[row,q]] = A[[q,row]]
        A[row] = MUL[INV[A[row,col]], A[row]]
        factors = A[:,col].copy()
        factors[row] = 0
        A ^= MUL[factors[:,None], A[row,None,:]]
        pivots.append(col)
        row += 1
        if row == A.shape[0]:
            break
    return A, pivots

def rank(A):
    return len(rref(A)[1])

def inverse(A):
    n = A.shape[0]
    need(A.shape == (n,n), 'square inverse')
    R, p = rref(np.hstack([A,np.eye(n,dtype=np.uint8)]))
    need(p[:n] == list(range(n)), 'invertible matrix')
    out = R[:,n:]
    need(np.array_equal(mm(A,out), np.eye(n,dtype=np.uint8)), 'inverse product')
    return out

def null(A):
    R, p = rref(A)
    free = [i for i in range(A.shape[1]) if i not in p]
    N = np.zeros((A.shape[1],len(free)),dtype=np.uint8)
    N[free] = np.eye(len(free),dtype=np.uint8)
    for q,col in enumerate(p):
        N[col] = R[q,free]
    need(not np.any(mm(A,N)), 'kernel product')
    return N

def solve(A, B):
    _, pc = rref(A)
    AB = A[:,pc]
    _, pr = rref(AB.T)
    out = np.zeros((A.shape[1],B.shape[1]),dtype=np.uint8)
    out[pc] = mm(inverse(AB[pr]), B[pr])
    need(np.array_equal(mm(A,out),B), 'linear image membership')
    return out

def contrasts(T, z, W, I, O, J):
    B = {}
    for j in J:
        sections = [inverse(T[np.ix_(O[r],I[j])]) for r in z['retained_receivers']]
        P = np.zeros((35,32),dtype=np.uint8)
        P[I[j]] = np.hstack(sections)
        B[j] = mm(P,W)
    Z = np.hstack([B[j]^B[61] for j in J if j != 61])
    rz, ra = rank(Z), rank(np.hstack([Z,B[61]]))
    return B, Z, dict(contrast_rank=rz, augmented_rank=ra, abstract_common_response_rank=ra-rz)

def main(repo, out, candidate=None):
    out.mkdir(parents=True,exist_ok=True)
    pins = {name:hashlib.sha256((repo/name).read_bytes()).hexdigest() for name in INPUTS}
    if candidate and candidate.resolve().is_relative_to(repo):
        pins[str(candidate.resolve().relative_to(repo))] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    expected = HERE/'SOURCE-PINS.json'
    if expected.exists():
        need(pins == read(expected), 'input source pins')
    z, dw, data, collision = [read(repo/name) for name in INPUTS]
    K = np.array(collision['forced_collision'],dtype=np.uint8)
    T = np.array(dw['matrix'],dtype=np.uint8)
    L = np.array(z['common_frames'],dtype=np.uint8)
    W = np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8)
    I = {int(j):v for j,v in z['D_inputs'].items()}
    O = {int(r):v for r,v in z['D_outputs'].items()}
    J = z['donors']
    V = sorted(set(sum(I.values(),[])))
    missing = sorted(set(range(35))-set(V))
    F = [4,5,7,8]
    need(np.array_equal(mm(L,W),K) and rank(K)==4, 'forced four-space coordinates')
    need(len(V)==32 and missing==[24,29,33], 'native input union')
    B,Z,old = contrasts(T,z,W,I,O,J)
    for j in J:
        need(np.array_equal(B[j],mm(np.array(data['ingress'][str(j)],dtype=np.uint8),K)), 'old ingress')
    need(old==dict(contrast_rank=30,augmented_rank=32,abstract_common_response_rank=2), 'baseline profile')
    need(np.flatnonzero(np.any(B[61],axis=1)).tolist()==F and rank(B[61][F])==4, 'source61 four inputs')
    forced = []
    for key, system in z['systems'].items():
        j,h = map(int,key.split('/'))
        if j != 61:
            continue
        C = np.array(system['H_observation_core'],dtype=np.uint8)
        D = solve(C,K)
        forced.append(dict(system=key,H_core_rank=rank(C),K_coefficients=D.tolist()))
    need(len(forced)==4,'all source61 D parents')
    # Independent exact check of the affine-family reduction. These are image
    # identities, not a tangent calculation or a numerical interpolation test.
    intersection_records = []
    extension_dimension = 0
    for key, system in z['systems'].items():
        j,h = map(int,key.split('/'))
        C = np.array(system['H_observation_core'],dtype=np.uint8)
        X = np.hstack([C,L])
        relation = null(X)
        projected = relation[C.shape[1]:]
        fixed_j = sorted(set(I[j]) & set(F))
        E = np.zeros((32,4*len(fixed_j)),dtype=np.uint8)
        for idx,r in enumerate(z['retained_receivers']):
            E[8*idx:8*idx+8,idx*len(fixed_j):(idx+1)*len(fixed_j)] = T[np.ix_(O[r],fixed_j)]
        dim = 4*len(fixed_j)
        need(rank(E)==dim and rank(projected)==dim and rank(np.hstack([E,projected]))==dim,
             'exact H/four-frame intersection')
        oldmap = np.array(system['old_protected_map'],dtype=np.uint8)
        maps = [np.array(M,dtype=np.uint8) for M in system['receiver_ingress_to_quotient_maps']]
        old_image = np.hstack([mm(M,inverse(T[np.ix_(O[r],I[j])]))
                              for M,r in zip(maps,z['retained_receivers'])])
        need(np.array_equal(mm(oldmap,L),old_image),'old quotient frame identity')
        extension_dimension += 6*(96-rank(X))
        intersection_records.append(dict(system=key,fixed_inputs=fixed_j,intersection_dimension=dim,
                                         prescribed_input_rank=rank(X)))
    for j in J:
        local = [s for key,s in z['systems'].items() if int(key.split('/')[0])==j]
        need(len(local)==4,'four independent local source maps')
        for idx,r in enumerate(z['retained_receivers']):
            stack = np.vstack([np.array(s['receiver_ingress_to_quotient_maps'][idx],dtype=np.uint8)
                               for s in local])
            need(rank(stack)==8,'joint parent maps detect every ingress coordinate')
    retained_rows = sorted(set(sum(O.values(),[])))
    need(len(retained_rows)==22 and extension_dimension==13368,'affine dimensions')
    factors = {}
    for idx,r in enumerate(z['retained_receivers']):
        factors[r] = solve(T[np.ix_(O[r],F)],W[8*idx:8*idx+8])
    need(not np.any(factors[6]) and not np.any(factors[9]),'K uses only48 and73')
    H = factors[48]^factors[73]
    need(rank(H)==4 and np.array_equal(H,B[61][F]),'fixed four-space readout')
    relation_data = [([1,0,0,0],[12,5,10,28],[0,49,62,58]),
                     ([0,1,0,0],[43,1,0,12],[12,11,18,63])]
    relations = []
    for u,c48,c73 in relation_data:
        rows48,rows73 = [21,22,30,34],[20,23,25,30]
        need(np.array_equal(mm(np.array([c48],dtype=np.uint8),T[np.ix_(rows48,F)])[0],u),'48 coefficient')
        need(np.array_equal(mm(np.array([c73],dtype=np.uint8),T[np.ix_(rows73,F)])[0],u),'73 coefficient')
        relation = np.zeros(35,dtype=np.uint8)
        relation[rows48] ^= np.array(c48,dtype=np.uint8)
        relation[rows73] ^= np.array(c73,dtype=np.uint8)
        need(not np.any(mm(relation[None,:],T[:,F])),'relation fixes rectangle')
        relations.append(dict(u=u,rows48=rows48,coefficients48=c48,rows73=rows73,
                              coefficients73=c73,relation=relation.tolist()))
    profiles = np.vstack([T[np.ix_([10,30],F)],np.array([r[0] for r in relation_data],dtype=np.uint8)])
    need(rank(profiles)==4,'two extra profiles complement shared rows')
    # A rank-four abstract response cannot substitute for eight independent physical rows.
    z28 = np.eye(32,dtype=np.uint8)[:,:28]
    b4 = np.eye(32,dtype=np.uint8)[:,28:]
    need(rank(np.hstack([z28,b4]))-rank(z28)==4 and null(z28.T).shape[1]==4,'rank28 countermodel')
    z24 = np.eye(32,dtype=np.uint8)[:,:24]
    decoder = np.eye(32,dtype=np.uint8)[24:]
    need(rank(decoder)==8 and not np.any(mm(decoder,z24)),'rank24 abstract positive control')
    bmut = b4.copy()
    bmut[28] = 0
    need(rank(np.hstack([z28,bmut]))-rank(z28)==3,'response mutation')
    result = dict(status='PASS_ACTUAL_RECEIVER95_CONTRAST_RANK_GATE',native_inputs=V,
                  missing_inputs=missing,forced_K_dimension=4,source61_H_fixed_parent_count=4,
                  baseline=old,abstract_rank4_required_contrast_upper=28,
                  actual_receiver95_required_contrast_upper=24,
                  additional_required_contrast_rank_drop_from_baseline=6,
                  coefficient_extensions=True,
                  repeated_width_form='rank(Z_m)<=24m for8m independent actual receiver rows on32m native inputs',
                  actual_target_gate_sufficient=False,new_complete_kappa=False,
                  affine_family_review=dict(local_systems=44,fixed_coefficients=88,
                      phase_legal_D_dimension=921,free_D_dimension=833,
                      source_extension_dimension=extension_dimension),
                  controls=['rank28 q4 countermodel fails eight-row interface',
                            'rank24 permits eight independent common rows','mutated response rank rejected'])
    cert = dict(source61_H_core_decompositions=forced,H_frame_intersection_review=intersection_records,
                K_factors={str(r):v.tolist() for r,v in factors.items()},
                K_input_profile=H.tolist(),overlap_relations=relations,common_profiles=profiles.tolist())
    if candidate:
        obj = read(candidate)
        TT = np.array(obj['matrix'] if 'matrix' in obj else obj['D_matrix'],dtype=np.uint8)
        BB,ZZ,rr = contrasts(TT,z,W,I,O,J)
        need(np.array_equal(TT[np.ix_(sorted(set(sum(O.values(),[]))),F)],T[np.ix_(sorted(set(sum(O.values(),[]))),F)]),'candidate rectangle')
        cc = []
        for relation in relations:
            need(not np.any(mm(np.array([relation['relation']],dtype=np.uint8),TT[:,V])),'candidate overlap')
            cc.append(mm(np.array([relation['coefficients48']],dtype=np.uint8),TT[relation['rows48']])[0])
        A = np.vstack([TT[[10,30]],cc])
        need(not np.any(mm(A,ZZ)) and rank(mm(A,BB[61]))==4,'four-row common response')
        o95 = [10,13,16,18,30,31,32,33]
        result['candidate'] = dict(**rr,actual_common_decoder_rank=4,
            phase_ranks=[rank(TT[:19,:19]),rank(TT[19:,19:])],
            actual_receiver95_rank=rank(TT[np.ix_(o95,V)]),
            actual_receiver95_contrast_response_rank=rank(mm(TT[o95],ZZ)),
            source_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
        cert['candidate_common_decoder'] = A.tolist()
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'CERTIFICATE.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    (out/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=Path('.'))
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--candidate',type=Path)
    args = parser.parse_args()
    main(args.repo.resolve(),args.out.resolve(),args.candidate)
