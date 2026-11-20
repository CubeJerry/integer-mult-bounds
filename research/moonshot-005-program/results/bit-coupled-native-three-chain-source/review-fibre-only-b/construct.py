"""Independent hybrid reconstruction, using only earlier independent geometry.

The author constructor is neither imported nor executed. The quotient-class
graph and field arithmetic are inherited from the pinned independent review.
"""
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

def need(ok, message):
    if not ok:
        raise ValueError(message)

PINS = {
    'author_manifest': ('fibre-only/MANIFEST.json', '0ad3869c70f335497c93e2afaa7ab7aa31c49930d789181e7083105608c4914a'),
    'previous_construct': ('review-b/construct.py', '010266cb6d710ab94e740c8977798c5f5d6b7117e1402c90713e7ac71e132d80'),
    'previous_check': ('review-b/check.py', 'b96daa69e849bd59451ce14b0f1d03ef202985901139888668853b3a27f101a0'),
    'parameters': ('fibre-only/output/PARAMETERS.json', '7b29f8e5a0394fc0a6c6b50f0b12beba233017398301bb32140077ccd445810b'),
    'author_result': ('fibre-only/output/RESULT.json', '1e781649d82a0816393d8375cfa4dbc283f8d5230a16388da4ca6de0b173a618'),
    'cost': ('fibre-only/output/COST.json', '05c3977e59dd373d3ea7b9fc0a0ab9d53b7e889bac8dc15b0697e4cd011e430f'),
    'closing_witnesses': ('fibre-only/output/CLOSING-WITNESSES.json', 'd7c8432312822f64e68f64a898bb7c401a7de6629897342bb9955b4b0e137f43'),
    'closing_result': ('fibre-only/output/CLOSING-RESULT.json', 'f1b707af22ad753acfafca8853b64058e309b113eba7bb930e290f55834ef469'),
}

def context(repo, out):
    folder = repo/'research/moonshot-005-program/results/bit-coupled-native-three-chain-source'
    payload = {}
    for key, (name, digest) in PINS.items():
        raw = (folder/name).read_bytes()
        need(sha256(raw).hexdigest() == digest, 'frozen source pin ' + key)
        payload[key] = raw
    manifest = json.loads(payload['author_manifest'])
    need(len(manifest['files']) == 11, 'all eleven author scientific files')
    for name, digest in manifest['files'].items():
        need(sha256((folder/'fibre-only'/name).read_bytes()).hexdigest() == digest, 'frozen author file ' + name)
    previous = load(folder/PINS['previous_construct'][0], 'independent_chain_base')
    ctx = previous.context(repo, out)
    ctx.previous = previous
    ctx.audit = load(folder/PINS['previous_check'][0], 'independent_chain_physical_audit')
    ctx.payload.update(payload)
    ctx.parameters = json.loads(payload['parameters'])
    need(ctx.parameters['centres'] == ctx.centres and ctx.parameters['hybrid_base_seed'] == 0
         and ctx.parameters['rank_one_ramp_centre'] == 642, 'literal hybrid family')
    ctx.before = {}; ctx.fibres = {}; ctx.spaces = {}; ctx.hybrid = {}
    for k in (3, 12):
        build(ctx, k)
    return ctx

def build(ctx, k):
    F = ctx.field; pseudo = ctx.previous.pseudo
    groups = ctx.components[k]['group_id']; equations = []; w = k//3
    for side, h in enumerate(ctx.centres):
        chart = ctx.charts[h, k]; controls = [groups[j, h] for j in chart.donors]
        used = Counter(); first = chart.donors[0]
        for ordinal, port in enumerate(chart.ports):
            for attempt in range(100):
                U = pseudo(f'core/{h}/{k}/0/{port}/{attempt}', 2, 2)
                if F.product[U[0, 0], U[1, 1]] != F.product[U[0, 1], U[1, 0]]:
                    break
            else:
                raise ValueError('invertible contrast unavailable')
            rows = np.zeros((2, 34*k), dtype=np.uint8)
            for a in range(2):
                scales = [int(U[a, 0] ^ U[a, 1]), int(U[a, 0]), int(U[a, 1])]
                for donor in range(3):
                    block = slice(controls[donor]*k, (controls[donor]+1)*k)
                    rows[a, block] ^= F.product[scales[donor], chart.V[ordinal, donor*k:(donor+1)*k]]
            positions = []
            for point in sorted(ctx.native.rad[port]):
                q = next(q for q, p in chart.point[first].items() if p == point)
                group = groups[first, q]
                if h == 642:
                    positions.append(group*k + side*w + used[point])
                else:
                    A = pseudo(f'general-relations/{ctx.centres}/{k}/0/{side}/{port}/{point}', 2, k)
                    rows[:, group*k:(group+1)*k] ^= A
                used[point] += 1
            if h == 642:
                for a in range(2):
                    rows[a, positions[0]] ^= 1; rows[a, positions[a+1]] ^= 1
            equations.extend(rows)
        need(set(used) == set(chart.xs) and set(used.values()) == {w}, 'exact radical occurrence coordinates')
    relation = np.vstack(equations)
    need(relation.shape == (18*k, 34*k) and F.rank(relation) == 18*k, 'independent hybrid equations')
    embedding = F.null(relation)
    need(embedding.shape == (34*k, 16*k) and not np.any(F.mm(relation, embedding)), 'entire original source bank')
    for j in ctx.donors:
        ctx.before[j, k] = {h: embedding[groups[j, h]*k:(groups[j, h]+1)*k].copy() for h in ctx.stars[j]}
    ctx.hybrid[k] = {'relation': relation, 'embedding': embedding}
    # Normalize each whole inverse lift by its actual H readout, rather than
    # using the author's chosen nullspace basis for the retained fibre.
    fibres = {}; constraints = {'geometric': defaultdict(list), 'native': defaultdict(list)}
    for h in ctx.centres:
        chart = ctx.charts[h, k]; first = chart.donors[0]
        for i in chart.receivers:
            pos = [n for n, d in enumerate(chart.ports) if ctx.D[d] <= ctx.perp[i]]
            need(len(pos) == k, 'actual component ports of receiver')
            V = chart.V[pos]
            off = [q for q in ctx.views[first, i] if q != h]
            annihilator = np.vstack([ctx.before[first, k][q] for q in off])
            readout = F.mm(V[:, :k], ctx.before[first, k][h])
            rhs = np.zeros((16*k, k), dtype=np.uint8); rhs[:k] = np.eye(k, dtype=np.uint8)
            K = F.solve(np.vstack([readout, annihilator]), rhs)
            need(F.rank(K) == k and F.rank(annihilator) == 15*k, 'whole original hybrid inverse fibre')
            fibres[h, i] = K
            for ordinal, j in enumerate(chart.donors):
                qs = [q for q in ctx.views[j, i] if q != h]
                old_off = np.vstack([ctx.before[j, k][q] for q in qs])
                need(F.rank(old_off) == 15*k, 'all old off-centre kernels')
                need(not np.any(F.mm(old_off, K)), 'old common fibre at every donor')
                A = F.mm(V[:, ordinal*k:(ordinal+1)*k], ctx.before[j, k][h])
                need(np.array_equal(F.mm(A, K), np.eye(k, dtype=np.uint8)), 'old common complete readout')
                for q in qs:
                    constraints['geometric'][j, q].append(K)
                    if i < 111:
                        constraints['native'][j, q].append(K)
    spaces = {}
    for scope, flags in constraints.items():
        spaces[scope] = {}
        for flag, pieces in sorted(flags.items()):
            span = np.hstack(pieces)
            E = F.null(span.T).T
            need(not np.any(F.mm(E, span)), 'entire dual of the retained fibre span')
            j, q = flag
            need(F.rank(np.vstack([E, ctx.before[j, k][q]])) == len(E), 'old quotient lies in the permitted dual')
            spaces[scope][flag] = E
    flexible = {flag: E for flag, E in spaces['geometric'].items() if len(E) > k and flag[1] not in ctx.centres}
    need(set(flexible) == {(0, 116), (25, 394), (47, 652), (62, 643)}, 'exact four noncentral flexible flags')
    need({len(E) for E in flexible.values()} == {6 if k == 3 else 20}, 'exact quotient freedom')
    for j in ctx.donors:
        ctx.maps[j, k] = {h: A.copy() for h, A in ctx.before[j, k].items()}
    for (j, q), E in flexible.items():
        C = pseudo(f'fibre-only/{k}/{ctx.parameters[str(k)]["seed"]}/{j}/{q}', k, len(E))
        ctx.maps[j, k][q] = F.mm(C, E)
    author = json.loads(ctx.payload['author_result'])
    for j in ctx.donors:
        actual = sha256(b''.join(ctx.maps[j, k][q].tobytes() for q in sorted(ctx.stars[j]))).hexdigest()
        need(actual == author['source_coefficient_sha256'][f'{j}/{k}'], 'all independent hybrid source bytes')
    need({f'{j}/{q}': len(E) for (j, q), E in spaces['geometric'].items()}
         == author['components'][str(k)]['fibre_annihilator_dimensions'], 'complete geometric dual census')
    ctx.fibres[k] = fibres; ctx.spaces[k] = spaces
    ctx.hybrid[k]['flexible'] = flexible
