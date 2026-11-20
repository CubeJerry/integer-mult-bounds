#!/usr/bin/env python3
"""Reconstruct native readout implication without the author's code or certificate."""
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
    L = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    roots = g.roots_from_files(L, json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text()))
    H, D = [set(x) for x in L['A2']], [set(x) for x in L['D4']]
    adj = [{i for i, y in enumerate(roots) if i != j and not g.b(x, y)} for j, x in enumerate(roots)]
    raw = json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
    maps = {int(j): {int(h): np.array(M, dtype=np.uint8) for h, M in rows.items()} for j, rows in raw['maps'].items()}
    word = np.array(raw['Hwords']['263'], dtype=np.uint8)
    ports = [110, 132, 720, 810, 1509, 1735, 1994, 2621, 2836]
    donors, companions = [0, 61, 62], {0: 116, 61: 642, 62: 643}
    receivers = [i for i in range(111) if H[263] <= adj[i]]
    need(len(receivers) == 33 and 80 not in receivers and g.rank(word) == 9, 'native retained H interface')
    K = {}
    for i in receivers:
        fibres = []
        for j in donors:
            visible = [h for h in maps[j] if H[h] <= adj[i]]
            need(len(visible) == 16 and g.rank(np.vstack([maps[j][h] for h in visible])) == 48, 'full source view')
            fibres.append(g.null(np.vstack([maps[j][h] for h in visible if h != 263])))
        need(all(F.shape == (48, 3) and g.rank(np.hstack([fibres[0], F])) == 3 for F in fibres), 'three complete common inverse fibres')
        K[i] = fibres[0]
    joined = np.hstack(list(K.values()))
    S = joined[:, g.echelon(joined)[1]]
    need(S.shape == (48, 30), 'native core dimension')
    selected = g.echelon(S.T)[1]
    left = g.invert(S[selected])
    coordinates = {i: g.mm(left, F[selected]) for i, F in K.items()}
    need(all(np.array_equal(g.mm(S, coordinates[i]), K[i]) for i in receivers), 'core coordinates')
    witness = 4
    intersections, plane_lists = [], {}
    for j in donors:
        planes = [h for h in maps[j] if h not in (263, companions[j]) and H[h] <= adj[witness]]
        need(len(planes) == 14, 'fourteen other actual observations')
        plane_lists[j] = planes
        annihilators = []
        for h in planes:
            Z = np.hstack([F for i, F in K.items() if H[h] <= adj[i]])
            annihilators.append(g.null(Z.T).T)
        W = g.null(np.vstack(annihilators))
        need(W.shape == (48, 6), 'native six-dimensional intersection')
        intersections.append(W)
    W = intersections[0]
    need(all(g.rank(np.hstack([W, V])) == 6 for V in intersections), 'same W for all donors')
    need(g.rank(np.hstack([W, K[witness]])) == 6, 'witness inverse fibre inside W')
    wc = g.mm(left, W[selected])
    need(np.array_equal(g.mm(S, wc), W), 'W lies in common core')
    seen = {i: [p for p, d in enumerate(ports) if D[d] <= adj[i]] for i in receivers}
    need(all(len(v) == 3 for v in seen.values()), 'three actual native ports')
    need(all(g.rank(word[np.ix_(seen[witness], range(3*j, 3*j+3))]) == 3 for j in range(3)), 'invertible witness blocks')

    def system(tuples):
        rows = []
        for V, visible in tuples:
            for port in visible:
                for t in range(V.shape[1]):
                    factors = [g.M[word[port, 3*j:3*j+3, None], V[None, :, t]].reshape(-1) for j in range(3)]
                    zero = np.zeros(90, dtype=np.uint8)
                    rows.append(np.concatenate([factors[0], factors[1], zero]))
                    rows.append(np.concatenate([factors[0], zero, factors[2]]))
        return np.array(rows, dtype=np.uint8)

    phases = []
    current = {i: V.copy() for i, V in coordinates.items()}
    cw = wc.copy()
    for e in range(6):
        M = system([(current[i], seen[i]) for i in receivers])
        conclusion = system([(cw, seen[witness])])
        need(M.shape == (594, 270) and conclusion.shape == (36, 270), 'complete implication dimensions')
        kernel = g.null(M)
        nullity = 15 if e % 2 == 0 else 12
        need(kernel.shape == (270, nullity), 'exact native equation nullity')
        need(not np.any(g.mm(conclusion, kernel)), 'all native equations imply W equalization')
        augmented = g.rank(np.vstack([M, conclusion]))
        need(augmented == 270-nullity, 'conclusion row containment')
        bad = conclusion.copy()
        index = next(i for i in range(270) if np.any(kernel[i]))
        bad[0, index] ^= 1
        need(np.any(g.mm(bad, kernel)), 'one-entry false implication rejected')
        phases.append({'phase': e, 'rank': 270-nullity, 'nullity': nullity, 'augmented_rank': augmented, 'false_implication_rejected': True})
        current = {i: g.M[V, V] for i, V in current.items()}
        cw = g.M[cw, cw]
    kernels = [g.mm(W, g.null(g.mm(maps[j][263], W))) for j in donors]
    need(all(g.rank(K) == 3 and g.rank(np.hstack([kernels[0], K])) == 3 for K in kernels), 'literal shared companion kernel')
    result = {'status': 'PASS_ROOT_NATIVE_READOUT_RIGIDITY_SIX_PHASES', 'native_receivers': 33,
              'core_dimension': 30, 'intersection_dimension': 6, 'witness_receiver': witness,
              'phases': phases, 'literal_companion_kernel_dimension': 3,
              'fourteen_planes': plane_lists, 'author_code_or_certificate_imported': False,
              'scope': 'Fixed whole H263 fibre diagram and port word; binary-linear central maps, nonlinear off-centre functions, extensions and repeated-copy mixing.',
              'new_complete_kappa': False}
    out.mkdir(parents=True, exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], 33, 30, 6, flush=True)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    run(a.repo.resolve(), a.out.resolve())
