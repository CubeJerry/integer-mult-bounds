#!/usr/bin/env python3
"""Six actual centres exclude a common Clifford fibre gauge."""
from argparse import ArgumentParser
from collections import defaultdict
import gzip
from pathlib import Path
import importlib.util, json
from hashlib import sha256
import numpy as np

def need(ok, message='exact Clifford scaffold certificate'):
    if not ok:
        raise ValueError(message)
cli = ArgumentParser(description=__doc__)
cli.add_argument('--repo', type=Path, required=True)
cli.add_argument('--out', type=Path, required=True)
args = cli.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
base = args.repo / 'research/moonshot-005-program/results'
for name, digest in json.loads(Path(__file__).with_name('SOURCE-PINS.json').read_bytes()).items():
    need(sha256((base / name).read_bytes()).hexdigest() == digest, 'exact Clifford scaffold certificate')
spec = importlib.util.spec_from_file_location('independent_context', base / 'bit-coupled-native-geometric-h-source/review-b/construct.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
ctx = helper.context(args.repo, args.out / 'field')
F, f = (ctx.field, ctx.arith)
shared = json.loads((base / 'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_bytes())
nodes = shared['H_nodes']
parameters = {int(j): {int(i): v for i, v in rows.items()} for j, rows in shared['receiver_parameters'].items()}

def gamma(v):
    out = np.zeros((16, 16), dtype=np.uint8)
    for subset in range(16):
        for k in range(4):
            if subset >> k & 1:
                if v >> 2 * k + 1 & 1:
                    out[subset ^ 1 << k, subset] ^= 1
            elif v >> 2 * k & 1:
                out[subset | 1 << k, subset] ^= 1
    return out
G = [gamma(v) for v in range(256)]
I = np.eye(16, dtype=np.uint8)
need(all((np.array_equal(F.mm(G[v], G[v]), f.q8(v) * I) for v in range(256))), 'exact Clifford scaffold certificate')
need(all((np.array_equal(F.mm(G[1 << a], G[1 << b]) ^ F.mm(G[1 << b], G[1 << a]), f.b8(1 << a, 1 << b) * I) for a in range(8) for b in range(8))), 'exact Clifford scaffold certificate')
roots = ctx.binary.roots
singleton = {next(iter(H & set(range(111)))) for H in ctx.H if len(H & set(range(111))) == 1}
ordinary = set(range(111)) - singleton - {10}
eligible = [h for h, H in enumerate(ctx.H) if H <= ordinary]
centres = [263, 4, 5, 6, 7, 8]
need(set(centres) <= set(eligible), 'exact Clifford scaffold certificate')
exits = {h: defaultdict(list) for h in centres}
for line in ctx.payload['routes'].splitlines():
    phase, role, coordinate, h, d, *_ = json.loads(line)
    if h in exits:
        exits[h][d].extend(((((phase == 'Y') * 111 + role) * 480 + coordinate) * 8 + lane for lane in range(8)))
for h, ports in exits.items():
    holders = [x for values in ports.values() for x in values]
    need(len(ports) == 45 and {len(v) for v in ports.values()} == {16} and (len(set(holders)) == len(holders) == 720), 'exact Clifford scaffold certificate')
row_basis = np.zeros((0, 256), dtype=np.uint8)
row_names = []
steps = []
local_certificates = []
for h in centres:
    donors = sorted(ctx.H[h])
    a = donors[0]
    c = nodes[h]
    receivers = [i for i in range(111) if i != 80 and ctx.H[h] <= ctx.perp[i]]
    need(all((sum((len(v) for d, v in exits[h].items() if ctx.D[d] <= ctx.perp[i])) == 240 for i in receivers)), 'exact Clifford scaffold certificate')
    Ucore = np.array([f.U(1 << p, c) for p in range(6)], dtype=np.uint8).T
    need(F.rank(Ucore) == 6, 'exact Clifford scaffold certificate')
    for v in range(64):
        coordinates = np.array([[(v >> p) & 1] for p in range(6)], dtype=np.uint8)
        need(np.array_equal(F.mm(Ucore, coordinates)[:, 0], np.array(f.U(v, c), dtype=np.uint8)), 'all normalized fibre parameters agree with their linear extension')
    local = []
    names = []
    for other in donors[1:]:
        product = F.mm(G[roots[a]], G[roots[other]])
        need(np.array_equal(F.mm(product, product) ^ product, I), 'exact Clifford scaffold certificate')
        vectors = [parameters[a][i] for i in receivers]
        graph = {v: {w for w in vectors if w != v and v ^ w in vectors} for v in vectors}
        reached = {vectors[0]}
        todo = list(reached)
        while todo:
            fresh = graph[todo.pop()] - reached
            reached.update(fresh)
            todo.extend(fresh)
        need(len(reached) == len(vectors) and f.binary_rank(vectors) == 6, 'exact Clifford scaffold certificate')
        selected = []
        images = []
        for i, v in zip(receivers, vectors):
            if f.binary_rank(selected + [v]) > len(selected):
                selected.append(v)
                images.append(parameters[other][i])
        linear = {f.xor((selected[p] for p in range(6) if mask >> p & 1)): f.xor((images[p] for p in range(6) if mask >> p & 1)) for mask in range(64)}
        need(len(linear) == 64 and all((linear[v] == parameters[other][i] for i, v in zip(receivers, vectors))), 'exact Clifford scaffold certificate')
        need(all((linear[linear[v]] ^ linear[v] ^ v == 0 for v in range(64))), 'exact Clifford scaffold certificate')
        J = np.array([[linear[1 << p] >> r & 1 for p in range(6)] for r in range(6)], dtype=np.uint8)
        need(F.rank(np.vstack([np.eye(6, dtype=np.uint8).reshape(36), J.reshape(36)])) == 2, 'exact Clifford scaffold certificate')
        local_certificates.append({'H': h, 'donors': [a, other], 'native_receivers': receivers, 'parameters': vectors, 'binary_parameter_basis': selected, 'target_basis_images': images, 'J_columns': [linear[1 << p] for p in range(6)], 'additivity_graph_connected': True, 'Ucore_rank': 6, 'I_J_span_rank': 2, 'mixed_phase_shared_H_capacity_at_bank3840': 240})
        for i in receivers:
            ua = np.array(f.U(parameters[a][i], c), dtype=np.uint8)
            ub = np.array(f.U(parameters[other][i], c), dtype=np.uint8)
            block = F.product[G[roots[a]][:, :, None], ua[None, None, :]] ^ F.product[G[roots[other]][:, :, None], ub[None, None, :]]
            local.append(block.reshape(16, 256))
            names.extend([{'H': h, 'receiver': i, 'donors': [a, other], 'output_coordinate': q} for q in range(16)])
    local = np.vstack(local)
    joined = np.vstack([row_basis, local])
    joined_names = row_names + names
    rank, _, pivots = F.reduce(joined.T)
    row_basis = joined[pivots]
    row_names = [joined_names[p] for p in pivots]
    step = {'H': h, 'donors': donors, 'native_receivers': len(receivers), 'local_equations': list(local.shape), 'global_rank': rank, 'remaining_dimension': 256 - rank}
    steps.append(step)
    print('STEP', step, flush=True)
    if rank == 256:
        break
null = F.null(row_basis)
ranks = [F.rank(null[:, j].reshape(16, 16)) for j in range(null.shape[1])]
result = {'status': 'EXACT_NORMALIZED_CLIFFORD_SCAFFOLD_SCREEN', 'steps': steps, 'constraint_rank': len(row_basis), 'nullity': null.shape[1], 'basis_solution_matrix_ranks': ranks, 'selected_equation_rows': row_names, 'basis_sha256': sha256(row_basis.tobytes()).hexdigest()}
need(result['constraint_rank'] == 256 and result['nullity'] == 0, 'exact Clifford scaffold certificate')
need([step['global_rank'] for step in steps] == [48, 96, 144, 192, 240, 256], 'exact Clifford scaffold certificate')
raw = (json.dumps({'selected_equation_rows': row_names, 'row_basis': row_basis.tolist(), 'local_certificates': local_certificates}, sort_keys=True, separators=(',', ':')) + '\n').encode()
(args.out / 'WITNESSES.json.gz').write_bytes(gzip.compress(raw, mtime=0))
result.update({'status': 'PASS_COMMON_CLIFFORD_FIBRE_SCAFFOLD_OBSTRUCTION', 'witness_payload_sha256': sha256(raw).hexdigest(), 'projective_normalization_guard': True, 'arbitrary_donor_dependent_gauge_claim': False, 'feedback_source_excluded': False, 'new_complete_kappa': False})
(args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
print(result['status'], flush=True)
