#!/usr/bin/env python3
"""Independent coefficient identities from raw incidence and literal sources."""
from argparse import ArgumentParser
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import numpy as np


def need(ok, why):
    if not ok:
        raise ValueError(why)


def run(repo, out):
    base = repo/'research/moonshot-005-program/results'
    here = Path(__file__).resolve().parent
    for path, digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
    spec = importlib.util.spec_from_file_location('independent_s030_field', base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    layout = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    roots = g.roots_from_files(layout, json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text()))
    H, D = [set(x) for x in layout['A2']], [set(x) for x in layout['D4']]
    adj = [{i for i, y in enumerate(roots) if i != j and not g.b(x, y)} for j, x in enumerate(roots)]
    raw = json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
    cert = json.loads(gzip.decompress((here.parent/'output/CERTIFICATE.json.gz').read_bytes()))
    nodes = {int(j): {int(h): n for h, n in table.items()} for j, table in raw['base_nodes'].items()}
    identity = np.eye(3, dtype=np.uint8)
    maps = {j: {h: np.kron(np.array([[g.power(n, e) for e in range(16)]], dtype=np.uint8), identity) for h, n in table.items()} for j, table in nodes.items()}
    for j in (0, 61, 62):
        maps[j][263] = np.array(raw['maps'][str(j)]['263'], dtype=np.uint8)
    views = {j: {i: sorted(h for h in table if H[h] <= adj[i]) for i in sorted(adj[j])} for j, table in maps.items()}
    inverses = {j: {i: g.invert(np.vstack([maps[j][h] for h in visible])) for i, visible in views[j].items()} for j in (0, 61)}

    def fibre(j, i, h):
        position = views[j][i].index(h)
        return inverses[j][i][:, 3*position:3*position+3]

    def basis(M):
        return M[:, g.echelon(M)[1]]

    A = {i: fibre(0, i, 263) for i, view in views[0].items() if 263 in view}
    B = {i: fibre(61, i, 642) for i, view in views[61].items() if i < 111 and i != 80 and 642 in view}
    C = {i: fibre(0, i, 116) for i, view in views[0].items() if i < 111 and i != 80 and 116 in view}
    S0, Sb = basis(np.hstack(list(A.values()))), basis(np.hstack(list(B.values())))
    ann0 = g.null(S0.T).T
    need(S0.shape == Sb.shape == (48, 18) and g.rank(np.hstack([S0, Sb])) == 30, 'two cores and exact intersection')
    need(len(B) == 34 and len(C) == 32 and all(g.rank(np.hstack([Sb, K])) == 18 for K in C.values()), 'complete native companion families')
    R = np.array(cert['effective_tail_rows'], dtype=np.uint8)
    need(R.shape == (12, 48) and not np.any(g.mm(R, S0)) and g.rank(g.mm(R, Sb)) == 12, 'complete effective tail coordinates')
    coefficients = {}
    for i, K in C.items():
        blocks = np.zeros((37, 48, 3), dtype=np.uint8)
        blocks[0] = K
        if i in A:
            values = g.mm(R, K)
            for u in range(3):
                for v in range(12):
                    blocks[1+12*u+v] = g.M[A[i][:, u, None], values[v, None, :]]
        coefficients[i] = blocks
    planes = views[45][22]
    need(planes == cert['planes'] and len(planes) == 16 and 45 in adj[22], 'actual distant sixteen-message view')
    need(not any(H[h] <= adj[22] for h in (116, 263, 642)), 'witness sees none of the named H centres')
    Y = np.array(cert['universal_kernel_coefficients'], dtype=np.uint8)
    need(Y.shape == (37, 48, 3), 'full affine kernel certificate')
    need(all(not np.any(g.mm(ann0, X)) for X in Y[1:]), 'all variable terms vanish modulo S0')
    need(g.rank(g.mm(ann0, Y[0])) == 3, 'uniform nonvanishing rank in quotient')
    identities = []
    for h in planes:
        columns, origins = [], []
        if h != 642:
            for i, K in B.items():
                if H[h] <= adj[i]:
                    blocks = np.zeros((37, 48, 3), dtype=np.uint8)
                    blocks[0] = K
                    columns.append(blocks)
                    origins.extend([642, i, p] for p in range(3))
        if h != 116:
            for i, blocks in coefficients.items():
                if H[h] <= adj[i]:
                    columns.append(blocks)
                    origins.extend([116, i, p] for p in range(3))
        need(origins == cert['origins'][str(h)], 'complete literal generators with no omitted native receiver')
        Z = np.concatenate(columns, axis=2).reshape(1776, -1)
        combination = np.array(cert['constant_combinations'][str(h)], dtype=np.uint8)
        need(np.array_equal(g.mm(Z, combination), Y.reshape(1776, 3)), 'all37 coefficient identities at plane '+str(h))
        forged = combination.copy()
        nz = next(k for k in range(Z.shape[1]) if np.any(Z[:, k]))
        forged[nz, 0] ^= 1
        need(not np.array_equal(g.mm(Z, forged), Y.reshape(1776, 3)), 'forged generator combination rejected')
        identities.append({'plane': h, 'generators': Z.shape[1], 'coefficient_blocks_checked': 37})

    delta = np.array(cert['sample_delta'], dtype=np.uint8)
    need(delta.shape == (3, 48) and not np.any(g.mm(delta, S0)), 'sample allowed tail')
    sample = {j: {h: M.copy() for h, M in table.items()} for j, table in maps.items()}
    sample[0][263] ^= delta
    newC = {i: K ^ (g.mm(A[i], g.mm(delta, K)) if i in A else np.zeros_like(K)) for i, K in C.items()}
    for i, K in newC.items():
        off = np.vstack([sample[0][h] for h in views[0][i] if h != 116])
        need(g.rank(off) == 45 and g.rank(K) == 3 and not np.any(g.mm(off, K)), 'entire affine companion inverse fibre')
    need(g.rank(np.hstack([B[4], newC[4]])) == 6, 'direct old collision removed')
    annihilators = {}
    for h in maps[45]:
        columns = [K for centre, family in [(642, B), (116, newC)] for i, K in family.items() if h != centre and H[h] <= adj[i]]
        Z = np.hstack(columns) if columns else np.zeros((48, 0), dtype=np.uint8)
        annihilators[h] = g.null(Z.T).T
    defects = {i: 48-g.rank(np.vstack([annihilators[h] for h in views[45][i]])) for i in (4, 22)}
    need(defects == {4: 0, 22: 6}, 'local escape and distant failure controls')
    source_count = 0
    for j, table in sample.items():
        for visible in views[j].values():
            need(len(visible) == 16 and g.rank(np.vstack([table[h] for h in visible])) == 48, 'sample complete source cut')
            source_count += 1
    need(source_count == 315, 'all five source charts')
    ports = {263: [110,132,720,810,1509,1735,1994,2621,2836], 642: [302,594,673,1089,1297,1509,1726,2230,3067]}
    counts = {}
    for h in (263, 642):
        word = np.array(cert['sample_Hwords'][str(h)], dtype=np.uint8)
        need(g.rank(word) == (9 if h == 263 else 3), 'actual provider rank')
        count = 0
        for i in range(120):
            if not H[h] <= adj[i]:
                continue
            donors = sorted(H[h])
            K = g.null(np.vstack([sample[donors[0]][q] for q in views[donors[0]][i] if q != h]))
            visible = [p for p, d in enumerate(ports[h]) if D[d] <= adj[i]]
            need(len(visible) == 3, 'actual marked receiver ports')
            readouts = []
            for j, donor in enumerate(donors):
                off = np.vstack([sample[donor][q] for q in views[donor][i] if q != h])
                need(g.rank(off) == 45 and not np.any(g.mm(off, K)), 'same complete source fibre')
                readouts.append(g.mm(word[np.ix_(visible, range(3*j, 3*j+3))], g.mm(sample[donor][h], K)))
            need(g.rank(readouts[0]) == 3 and all(np.array_equal(readouts[0], X) for X in readouts), 'same injective three-port readout')
            count += 1
        counts[h] = count
    need(counts == {263: 36, 642: 36}, 'all geometric readouts')
    result = {'status': 'PASS_ROOT_UNIVERSAL_PAID_TAIL_KERNEL_REVIEW',
              'effective_parameters': 36, 'coefficient_blocks': 37, 'witness_receiver': 22,
              'planes': planes, 'uniform_translation_kernel_dimension': 3,
              'constant_quotient_rank': 3, 'constant_generator_identities': identities,
              'sample_source_cuts': source_count, 'sample_provider_ranks': [9,3],
              'sample_readout_counts': counts, 'sample_defects': defects,
              'author_executables_imported': False, 'certificate_read_as_data_only': True,
              'scope': 'Any field-linear tail annihilating S0, extensions and arbitrary noncommuting repeated-copy blocks, with the other anchor and off-centre observations fixed.',
              'new_complete_kappa': False}
    out.mkdir(parents=True, exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], 36, 37, 3, 22, flush=True)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    run(a.repo.resolve(), a.out.resolve())
