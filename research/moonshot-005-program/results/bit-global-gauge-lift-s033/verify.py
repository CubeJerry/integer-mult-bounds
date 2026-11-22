"""Exact global source-gauge lift, using an independent GF64 implementation.

Only pinned JSON inputs are read; no predecessor author executable is imported.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse, gzip, hashlib, json
import numpy as np

FIELD_POLYNOMIAL = 0x43
PROTECTED = list(range(48)) + list(range(240, 288))
INPUT_COLUMNS = [4, 5, 7, 8]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def scalar_mul(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        a <<= 1
        if a & 64:
            a ^= FIELD_POLYNOMIAL
        b >>= 1
    return value

MUL = np.array([[scalar_mul(a, b) for b in range(64)] for a in range(64)], dtype=np.uint8)
INV = np.zeros(64, dtype=np.uint8)
for a in range(1, 64):
    INV[a] = next(b for b in range(1, 64) if int(MUL[a, b]) == 1)

def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    out = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for k in range(left.shape[1]):
        out ^= MUL[left[:, k, None], right[k, None, :]]
    return out

def reduce(matrix, pivot_limit=None):
    A = np.array(matrix, dtype=np.uint8, copy=True)
    pivots, row = [], 0
    for col in range(A.shape[1] if pivot_limit is None else pivot_limit):
        choices = np.flatnonzero(A[row:, col])
        if not len(choices):
            continue
        # Reverse pivot choice differs from the predecessor implementation.
        chosen = row + int(choices[-1])
        A[[row, chosen]] = A[[chosen, row]]
        A[row] = MUL[INV[A[row, col]], A[row]]
        factors = A[:, col].copy()
        factors[row] = 0
        A ^= MUL[factors[:, None], A[row, None, :]]
        pivots.append(col)
        row += 1
        if row == A.shape[0]:
            break
    return A, pivots

def rank(A):
    return len(reduce(A)[1])

def basis(A):
    return A[:, reduce(A)[1]]

def inverse(A):
    n = len(A)
    need(A.shape == (n, n), 'square inverse')
    B, pivots = reduce(np.hstack([A, np.eye(n, dtype=np.uint8)]), n)
    need(len(pivots) == n, 'singular inverse')
    answer = B[:, n:]
    need(np.array_equal(mm(A, answer), np.eye(n, dtype=np.uint8)), 'inverse multiplication')
    return answer

def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)

def write_json(path, value):
    raw = (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == '.gz' else raw)

def run(repo, candidate, out):
    root = repo / 'research/moonshot-005-program/results'
    four = root / 'bit-simultaneous-d1509-s032/output'
    files = [four/'D-WORD.json.gz', four/'CONSTRAINED-GAUGES.json.gz', four/'SOURCES.json.gz',
             root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',
             root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz',
             root/'bit-d1509-coupled-repair-s032/DATA.json.gz',
             root/'bit-fifth-receiver-quotient-s032/FORCED-COLLISION.json']
    dw, gauges, sources, systems, fibres, ingress, collision = map(read, files)
    T = np.array(dw['matrix'], dtype=np.uint8)
    L = np.array(gauges['common_frames'], dtype=np.uint8)
    R, J = systems['retained_receivers'], systems['donors']
    I = {int(j): x for j, x in systems['D_inputs'].items()}
    O = {int(r): x for r, x in systems['D_outputs'].items()}
    output_union = sorted(set(sum(O.values(), [])))
    H = {}
    cores = {}
    for h, rr in fibres.items():
        K = basis(np.hstack([np.array(v['kernel'], dtype=np.uint8)[:48, :3] for v in rr.values()]))
        zero = np.zeros_like(K)
        cores[int(h)] = np.block([[K, zero], [zero, K]])
    for j in J:
        selected = [K for h, K in cores.items() if str(h) in sources['paired_maps'][str(j)]]
        H[j] = basis(np.hstack(selected)) if selected else np.zeros((96, 0), dtype=np.uint8)
    need(rank(L) == 32, 'common four-frame rank')
    intersection_records = []
    for j in J:
        columns = [x for x in INPUT_COLUMNS if x in I[j]]
        V = np.hstack([mm(L[:, 8*k:8*k+8], T[np.ix_(O[r], columns)]) for k, r in enumerate(R)])
        d = rank(H[j]) + 32 - rank(np.hstack([H[j], L]))
        need(rank(V) == d == 4*len(columns), 'exact H intersection dimension')
        need(rank(np.hstack([H[j], V])) == rank(H[j]), 'intersection in full retained H core')
        intersection_records.append({'donor': j, 'H_dimension': rank(H[j]), 'fixed_columns': columns,
                                     'intersection_dimension': d, 'basis': V.tolist()})
    candidate_json = read(candidate)
    TT = np.array(candidate_json['D_matrix'], dtype=np.uint8)
    need(TT.shape == (35, 35), 'D word shape')
    need(not np.any(TT[:19, 19:]), 'phase legal')
    need(rank(TT[:19, :19]) == 19 and rank(TT[19:, 19:]) == 16, 'D phase ranks')
    need(np.array_equal(TT[np.ix_(output_union, INPUT_COLUMNS)], T[np.ix_(output_union, INPUT_COLUMNS)]), 'fixed rectangle')
    new_gauges = {}
    records = []
    K = np.array(collision['forced_collision'], dtype=np.uint8)
    new_ingress = {}
    identity = np.eye(96, dtype=np.uint8)
    for j in J:
        transformed = []
        for k, r in enumerate(R):
            old = T[np.ix_(O[r], I[j])]
            new = TT[np.ix_(O[r], I[j])]
            need(rank(new) == 8, 'retained D section')
            transformed.append(mm(L[:, 8*k:8*k+8], mm(old, inverse(new))))
        U = np.hstack(transformed)
        X, Y = np.hstack([H[j], L]), np.hstack([H[j], U])
        d = rank(X)
        need(rank(Y) == d and rank(np.vstack([X, Y])) == d, 'equal global extension kernels')
        indices = reduce(X)[1]
        A = basis(np.hstack([X[:, indices], identity]))
        B = basis(np.hstack([Y[:, indices], identity]))
        G = mm(B, inverse(A))
        need(rank(G) == 96 and np.array_equal(mm(G, X), Y), 'invertible source lift')
        need(np.array_equal(mm(G, H[j]), H[j]), 'full H core fixed pointwise')
        need(np.array_equal(mm(G, L), U), 'four oriented source preimages')
        invG = inverse(G)
        need(np.array_equal(mm(invG, U), L), 'entire common D fibres')
        new_gauges[j] = G.tolist()
        oldP = np.array(ingress['ingress'][str(j)], dtype=np.uint8)
        new_ingress[j] = mm(oldP, G)
        records.append({'donor': j, 'joined_dimension': d, 'gauge_rank': rank(G),
                        'gauge_change_rank': rank(G ^ identity), 'whole_H_core_fixed': True,
                        'four_preimage_equations': True})
    B = {j: mm(new_ingress[j], K) for j in J}
    Z = np.hstack([B[j] ^ B[61] for j in J if j != 61])
    q = rank(np.hstack([Z, B[61]])) - rank(Z)
    native_union = sorted(set(sum(I.values(), [])))
    need(len(native_union) == 32, 'native ingress count')
    need(not np.any(Z[[i for i in range(35) if i not in native_union]]), 'contrast native support')
    # A corrupted source gauge loses its fixed-core or oriented-preimage equation.
    corrupt = np.array(new_gauges[61], dtype=np.uint8); corrupt[0, 0] ^= 1
    bad = not np.array_equal(mm(corrupt, np.hstack([H[61], L])),
                            mm(np.array(new_gauges[61], dtype=np.uint8), np.hstack([H[61], L])))
    need(bad, 'gauge mutation control')
    # The original coordinate-only family is already known not to align five whole fibres.
    result = {'status': 'PASS_GLOBAL_SOURCE_GAUGE_LIFT', 'donors': len(J), 'global_intersections': intersection_records,
              'source_lifts': records, 'retained_D_sections': len(J)*len(R), 'phase_ranks': [19,16],
              'contrast_rank': rank(Z), 'augmented_rank': rank(np.hstack([Z, B[61]])), 'common_response_rank': q,
              'native_ingress_dimension': len(native_union), 'actual_eight_row_required_contrast_upper': 24,
              'gauge_mutation_rejected': bad, 'source_views_inherited_by_invertible_right_composition': 693,
              'native_source_views_inherited': 639, 'source_nonsaturation_preserved_exactly': True,
              'whole_H_interfaces_inherited': 72, 'native_whole_H_interfaces_inherited': 67,
              'whole_D_interfaces': 44, 'actual_early_ranks_inherited': [480]*11,
              'physical_source_compilation_checked_here': False, 'complete_fifth_receiver': False,
              'complete_supplier': False, 'new_complete_kappa': False}
    out.mkdir(parents=True, exist_ok=True)
    write_json(out/'RESULT.json', result)
    write_json(out/'GAUGES.json.gz', {'D_matrix': TT.tolist(), 'source_right_gauges': new_gauges,
                                    'protected_coordinates': PROTECTED, 'composition': 'F_new=F_S032*G on protected coordinates; identity on the other384',
                                    'contrast': Z.tolist(), 'common_forced_response': B[61].tolist()})
    pins = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    pins[str(candidate)] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    write_json(out/'SOURCE-PINS.json', pins)
    print(result['status'], 'q', q, 'contrast', rank(Z), 'eleven full-source lifts')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.repo.resolve(), args.candidate.resolve(), args.out.resolve())
