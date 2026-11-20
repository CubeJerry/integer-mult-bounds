#!/usr/bin/env python3
"""Exact native global-Hermite fibre compatibility and Frobenius twists."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
import gzip
from pathlib import Path
import importlib.util, json, sys, time
import numpy as np

def need(ok, message='exact finite certificate condition'):
    if not ok:
        raise ValueError(message)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def setup(repo, out):
    global ctx, F, f, b, nodes, params, witnesses
    base = repo / 'research/moonshot-005-program/results'
    pins = json.loads(Path(__file__).with_name('SOURCE-PINS.json').read_bytes())
    for name, digest in pins.items():
        need(sha256((base / name).read_bytes()).hexdigest() == digest, 'frozen primary input ' + name)
    b = load(base / 'bit-coupled-native-geometric-h-source/review-b/construct.py', 'independent_H_geometry')
    ctx = b.context(repo, out / 'field')
    F, f = (ctx.field, ctx.arith)
    data = json.loads((base / 'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes = data['H_nodes']
    params = {int(j): {int(i): v for i, v in d.items()} for j, d in data['receiver_parameters'].items()}
    need(nodes[263] == 49 and ctx.H[263] == {0, 61, 62}, 'exact finite certificate condition')
    need(10 not in ctx.H[263] and (not ctx.H[263] <= ctx.perp[80]), 'exact finite certificate condition')
    need(all((len({nodes[h] for h in ctx.stars[j]}) == 28 for j in (0, 61, 62))), 'exact finite certificate condition')
    exits = defaultdict(list)
    for line in ctx.payload['routes'].splitlines():
        phase, role, coordinate, h, d, *_ = json.loads(line)
        if h == 263:
            need(phase == 'X', 'exact finite certificate condition')
            exits[d].extend(((role * 480 + coordinate) * 8 + lane for lane in range(8)))
    need(len(exits) == 45 and {len(v) for v in exits.values()} == {16}, 'exact finite certificate condition')
    for i in range(111):
        if ctx.H[263] <= ctx.perp[i]:
            need(sum((len(v) for d, v in exits.items() if ctx.D[d] <= ctx.perp[i])) == 240, 'exact finite certificate condition')
    witnesses = {}

def mul(p, q):
    out = np.zeros(len(p) + len(q) - 1, dtype=np.uint8)
    for k, x in enumerate(p):
        out[k:k + len(q)] ^= F.product[x, q]
    return out

def hermite(x, k):
    row = b.powers(F, [x], 16 * k)[0]
    return np.array([[row[c - r] if r <= c and r & c == r else 0 for c in range(16 * k)] for r in range(k)], dtype=np.uint8)

def field_fibre(h, donor, i, k, mode):
    off = [nodes[q] for q in ctx.views[donor, i] if q != h]
    g = np.array(f.polynomial(off), dtype=np.uint8)
    if mode == 'tensor':
        K = np.kron(g[:, None], np.eye(k, dtype=np.uint8))
        E = np.vstack([np.kron(b.powers(F, [x], 16), np.eye(k, dtype=np.uint8)) for x in off])
    else:
        power = np.array([1], dtype=np.uint8)
        for _ in range(k):
            power = mul(power, g)
        K = np.zeros((16 * k, k), dtype=np.uint8)
        for c in range(k):
            K[c:c + len(power), c] = power
        E = np.vstack([hermite(x, k) for x in off])
    need(E.shape == (15 * k, 16 * k) and F.rank(E) == 15 * k and (F.rank(K) == k) and (not np.any(F.mm(E, K))), 'exact finite certificate condition')
    return (K, off)

def screen(h=263, k=3, mode='hermite', native=True):
    donors = sorted(ctx.H[h])
    a, c = donors[:2]
    receivers = [i for i in range(111 if native else 120) if (not native or i != 80) and ctx.H[h] <= ctx.perp[i]]
    pairs = []
    Kby = {}
    J = {}
    intersections = []
    triple_ranks = []
    for i in receivers:
        allK = []
        off = []
        for j in donors:
            K, g = field_fibre(h, j, i, k, mode)
            v = params[j][i]
            field_block = {a for a in range(64) if f.q6(a) == 0 and f.b6(v, a) == (f.q6(v) ^ 1)}
            need(set(g) | {nodes[h]} == field_block and len(field_block) == 16, 'actual observed nodes equal the exact global field block')
            if v in Kby:
                need(np.array_equal(Kby[v], K), 'exact finite certificate condition')
            Kby[v] = K
            allK.append(K)
            off.append(g)
        v, w = (params[a][i], params[c][i])
        J[v] = w
        need(v != w and v ^ w == params[donors[2]][i], 'exact finite certificate condition')
        intersections.append(len(set(off[0]) & set(off[1])))
        triple_ranks.append(F.rank(np.hstack(allK)))
        pairs.append((F.rank(np.hstack(allK[:2])), i))
    order = sorted(J)
    need(len(J) == len(set(J.values())) == len(receivers) == 33, 'all actual native receiver correspondences')
    joint = np.hstack([Kby[v] for v in order])
    rank, _, pivots = F.reduce(joint)
    S = joint[:, pivots]
    _, _, rows = F.reduce(S.T)
    Sinv = F.solve(S[rows], np.eye(rank, dtype=np.uint8))
    coords = {v: F.mm(Sinv, K[rows]) for v, K in Kby.items()}
    need(all((np.array_equal(F.mm(S, coords[v]), K) for v, K in Kby.items())), 'exact finite certificate condition')
    C = np.hstack([coords[v] for v in order])
    need(F.rank(np.hstack([coords[J[v]] for v in order])) == rank, 'target family spans the same whole fibre core')
    R = F.null(C)
    need(np.array_equal(F.mm(S, C), joint), 'exact finite certificate condition')
    blocks = []
    for n, v in enumerate(order):
        A = coords[J[v]]
        B = R[n * k:(n + 1) * k]
        block = F.product[A[:, :, None, None], B[None, None, :, :]].transpose(0, 3, 1, 2).reshape(rank * R.shape[1], k * k)
        blocks.append(block)
    E = np.hstack(blocks)
    Z = F.null(E)
    best = 0
    witness = None
    for trial in range(min(Z.shape[1], 12) + 8 if Z.shape[1] else 0):
        if Z.shape[1] == 0:
            break
        vector = Z[:, trial] if trial < Z.shape[1] else F.mm(Z, b.pseudo(f'global-H-intertwiner/{h}/{k}/{mode}/{trial}', Z.shape[1], 1))[:, 0]
        matrices = vector.reshape(len(order), k, k)
        target = np.hstack([F.mm(coords[J[v]], matrices[n]) for n, v in enumerate(order)])
        need(not np.any(F.mm(target, R)), 'exact finite certificate condition')
        T = target[:, pivots]
        need(np.array_equal(F.mm(T, C), target), 'exact finite certificate condition')
        r = F.rank(T)
        if r > best:
            best = r
            witness = T
    result = {'H': h, 'node': nodes[h], 'donors': donors, 'width': k, 'mode': mode, 'receivers': len(receivers), 'native_receivers': sum((i < 111 and i != 80 for i in receivers)), 'off_node_intersections': sorted(set(intersections)), 'pair_union_ranks': sorted({r for r, i in pairs}), 'triple_union_ranks': sorted(set(triple_ranks)), 'fibre_span_rank': rank, 'intertwiner_equations': list(E.shape), 'intertwiner_nullity': Z.shape[1], 'best_core_map_rank': best, 'component_bank': 16 * k, 'first_native_receiver': next((i for i in receivers if i < 111 and i != 80))}
    if mode == 'hermite' and k == 3:
        twist = []
        certificates = []
        for power in range(6):
            blocks = []
            for n, v in enumerate(order):
                A = coords[J[v]].copy()
                B = R[n * k:(n + 1) * k]
                for _ in range(power):
                    A = F.product[A, A]
                blocks.append(F.product[A[:, :, None, None], B[None, None, :, :]].transpose(0, 3, 1, 2).reshape(rank * R.shape[1], k * k))
            twisted = np.hstack(blocks)
            d = twisted.shape[1] - F.rank(twisted)
            twist.append(d)
            need(d == 0 and twisted.shape == (2268, 297), 'exact finite certificate condition')
            _, _, selected = F.reduce(twisted.T)
            minor = twisted[selected]
            need(minor.shape == (297, 297) and F.rank(minor) == 297, 'exact finite certificate condition')
            certificates.append({'relative_Frobenius_power': power, 'equations_sha256': sha256(twisted.tobytes()).hexdigest(), 'square_minor_rows': selected, 'minor_sha256': sha256(minor.tobytes()).hexdigest(), 'minor_rank': 297})
        result['all_six_relative_Frobenius_intertwiner_nullities'] = twist
        witnesses.update({'H': h, 'donors': donors, 'receivers': receivers, 'parameter_order': order, 'parameter_permutation': J, 'basis_columns': pivots, 'basis_rows': rows, 'core_basis': S.tolist(), 'relations': R.tolist(), 'fibres_by_parameter': {str(v): K.tolist() for v, K in Kby.items()}, 'rank_certificates': certificates})
    print(json.dumps(result, sort_keys=True), flush=True)
    return result

def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    setup(args.repo, args.out)
    results = [screen(263, k, mode) for mode, k in [('tensor', 1), ('tensor', 3), ('hermite', 2), ('hermite', 3)]]
    need([(x['intertwiner_nullity'], x['best_core_map_rank']) for x in results] == [(1, 6), (9, 18), (4, 12), (0, 0)], 'exact finite certificate condition')
    raw = (json.dumps(witnesses, sort_keys=True, separators=(',', ':')) + '\n').encode()
    (args.out / 'WITNESSES.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    result = {'status': 'PASS_GLOBAL_HERMITE3_BINARY_GAUGE_OBSTRUCTION', 'H': 263, 'donors_used': [0, 61], 'native_identity_receivers': 33, 'component_bank_GF64': 48, 'component_quotient_GF64': 3, 'all_six_Frobenius_intertwiner_ranks': [297] * 6, 'intertwiner_equation_shape': [2268, 297], 'witness_payload_sha256': sha256(raw).hexdigest(), 'experiments': results, 'allowed_source_coordinate_gauge': 'arbitrary invertible binary-linear map, independently at each bank', 'extension_scope': 'every finite extension of GF64 and arbitrary positive repetition', 'Hermite3_plus_12_bank3840_corollary': True, 'arbitrary_nonlinear_input_bijection_claim': False, 'feedback_or_other_changed_quotient_family_excluded': False, 'new_complete_kappa': False}
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(result['status'], flush=True)
if __name__ == '__main__':
    main()
