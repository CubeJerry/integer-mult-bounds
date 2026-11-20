#!/usr/bin/env python3
"""Reconstruct a five-receiver nonlinear obstruction from actual node products.

Uses an authenticated S030 review's field and atlas primitives. It does not
import either S031 gate checker or use their saved fibres/derivatives.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np


def need(ok, why):
    if not ok:
        raise AssertionError(why)


def run(repo, out):
    here = Path(__file__).resolve().parent
    base = repo/'research/moonshot-005-program/results'
    for path, digest in json.loads((here/'SOURCE-PINS.json').read_text()).items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
    spec = importlib.util.spec_from_file_location('s030_independent_arithmetic', base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    layout = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis = json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots = a.roots_from_files(layout, basis)
    H = [set(x) for x in layout['A2']]
    D = [set(x) for x in layout['D4']]
    adj = [{i for i, y in enumerate(roots) if i != j and not a.b(x, y)} for j, x in enumerate(roots)]
    data = json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes, params = data['H_nodes'], data['receiver_parameters']
    donors, receivers = [0, 61, 62], [5, 76, 52, 56, 97]
    c = nodes[263]
    need(H[263] == set(donors) and c == 49, 'literal central source')
    need(all(H[263] <= adj[i] for i in receivers), 'five actual native receivers')
    need(all(D[108] <= adj[i] for i in receivers[:2]), 'shared D108 at both collision receivers')
    fibres, derivatives, directions = {}, {}, {}
    for j in donors:
        fibres[j], derivatives[j], directions[j] = {}, {}, []
        star = [h for h, P in enumerate(H) if j in P]
        for i in receivers:
            visible = [h for h in star if H[h] <= adj[i]]
            values = [nodes[h] for h in visible]
            need(len(values) == len(set(values)) == 16 and c in values, 'actual distinct source nodes')
            v = params[str(j)][str(i)]
            # Product of the fifteen actual off-centre node factors.
            poly = np.array([a.power(v, 2)], dtype=np.uint8)
            for z in values:
                if z == c:
                    continue
                nxt = np.zeros(len(poly)+1, dtype=np.uint8)
                nxt[1:] ^= poly
                nxt[:-1] ^= a.M[z, poly]
                poly = nxt
            need(len(poly) == 16 and poly[-1] == a.power(v, 2), 'normalized literal inverse polynomial')
            evaluate = lambda z: a.xor(a.M[int(x), a.power(z, n)] for n, x in enumerate(poly))
            need(all(evaluate(z) == 0 for z in values if z != c), 'every actual off-source quotient vanishes')
            d = evaluate(c)
            need(d != 0, 'full source cut and invertible central readout')
            need(d == a.power(v, 8)^int(a.M[a.power(c, 4), a.power(v, 4)]), 'independent derivative formula')
            fibres[j][i], derivatives[j][i] = poly, d
            directions[j].append(v)
        x, y, z, xz, yz = [fibres[j][i] for i in receivers]
        need(a.rank(np.column_stack([x, y, z])) == 3, 'three independent core axes')
        need(np.array_equal(x^z, xz) and np.array_equal(y^z, yz), 'two literal additive fibre triangles')
    need(directions[0] == [3, 39, 5, 6, 34], 'five-direction witness')
    rows = [[derivatives[j][i] for j in donors] for i in receivers[:2]]
    need(rows == [[30, 18, 12], [38, 18, 52]], 'actual derivative collision')
    need(rows[0][0]^rows[1][0] == 56 and int(a.M[56, a.INV[56]]) == 1, 'invertible difference scalar')
    owners = Counter()
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase, role, coordinate, h, d, _, source, _ = json.loads(line)
        if h == 263:
            need(phase == 'X' and source == role and role in donors, 'genuine early original owner')
            for lane in range(8):
                owners[d, role, coordinate, lane] += 1
    need(set(owners.values()) == {1}, 'no duplicate native owners')
    capacities = Counter()
    for d, _, _, _ in owners:
        capacities[d] += 1
    need(len(capacities) == 45 and set(capacities.values()) == {16}, '45 positive sixteen-field ports')
    need(all(sum(n for d, n in capacities.items() if D[d] <= adj[i]) == 240 for i in receivers), 'five tight native H cuts')
    out.mkdir(parents=True, exist_ok=True)
    result = {'status': 'PASS_ROOT_FIVE_RECEIVER_NONLINEAR_GAP15_REVIEW', 'donors': donors,
              'receivers': receivers, 'directions': directions, 'core_axis_count': 3,
              'triangles': [[5, 52, 56], [76, 52, 97]], 'literal_scalar_fibres_checked': 15,
              'collision_derivatives': rows, 'difference_scalar': 56, 'D': 108,
              'native_port_fields': 16, 'native_receiver_cut_fields': 240,
              'arbitrary_separate_bank_bijections_excluded': True,
              'universal_step': 'Reviewed all-width gap15 core theorem plus the finite coset lemma; not extrapolation from this scalar check.',
              'new_complete_kappa': False}
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], 15, 3, 56, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.repo.resolve(), args.out.resolve())
