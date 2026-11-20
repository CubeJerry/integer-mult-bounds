"""Independent reconstruction of the simultaneous three-centre coefficient array.

The geometry and exact field implementation are reused from pinned independent
reviews. No author constructor, source checker or owner compiler is imported.
"""
from collections import Counter, defaultdict
import gzip
from hashlib import sha256, shake_256
import importlib.util
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import numpy as np

PINS = {
    'geometry': ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz', '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
    'routes': ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz', '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'),
    'spread': ('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz', '7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab'),
    'field': ('bit-spread-h263-source/review/check.py', 'db16cd8dcedfca40f6b9f29155de33d1211d8b77b0eff06c3072f6ffd50a3129'),
    'geometry_review': ('bit-spread-overlap-source/review/check.py', 'ba369d2f9d27726607b62287707b29f9719971810a7e9893592d1035093e7e4f'),
    'engine': ('bit-coupled-native-forty-h-source/review-all-donors-b/check.py', '7fd50803ec6f7f29b4c3548b90521b57348db73af50102f1fbeb79fd92fdfbd8'),
    'engine_cpp': ('bit-coupled-native-forty-h-source/review-all-donors-b/linear64.cpp', '2599b17e402dd043dd96b7ae872cf5e800b212ebbf1c3e0daa3cba33565afcb0'),
    'RS_review': ('bit-spread-rs-physical-word/review/check.py', '522e6e371559a61e9ee5ccb5cd14ec6b1b8b603dd63c6116de9c97b7df4cbf57'),
    'RS_review_result': ('bit-spread-rs-physical-word/review/output/RESULT.json', '656d3355e35aaf698654eb9d08c854e088ac8e36f34318c71be654a0e30f4d28'),
    'RS_result': ('bit-spread-rs-physical-word/author/source-output/RESULT.json', 'aa0fdb58c57cb0aa0e876bd66a2852b8c269abdffb2505adf045937e6c24f174'),
    'background_costs': ('bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json', '2e2d3dc68799357a571e1ae6f984a195148ab4a8eea61cc5d1694e6a9e05f513'),
    'parameters': ('bit-coupled-native-three-chain-source/author/output/PARAMETERS.json', '2b2e533d780e3cfbc14a34f7734d7a8ecfd2e1e4c7d0d76bf2644c545fc1da03'),
    'non_RS': ('bit-coupled-native-three-chain-source/author/output/NON-RS-WITNESSES.json', 'e8ddd68f2ea58e5c38786c703ef56d0ffe6602820d033525cbc1949ca297388f'),
    'cost': ('bit-coupled-native-three-chain-source/author/output/COST.json', '38cd024be52418fef41e1685b2a83cca558e6d80470d55336fb35d1be787e078'),
    'author_result': ('bit-coupled-native-three-chain-source/author/output/RESULT.json', '208ca0871a3561788adf8fc7127ad937964b40fd5c8501d1b8b4a782ca8880ad'),
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

def pseudo(tag, rows, columns):
    return np.frombuffer(shake_256(tag.encode('ascii')).digest(rows*columns), dtype=np.uint8).reshape(rows, columns) & 63

def context(repo, out):
    base = repo / 'research/moonshot-005-program/results'
    payload = {}
    for key, (name, expected) in PINS.items():
        raw = (base/name).read_bytes()
        if name.endswith('.gz'):
            raw = gzip.decompress(raw)
        need(sha256(raw).hexdigest() == expected, 'source pin ' + key)
        payload[key] = raw
    out.mkdir(parents=True, exist_ok=True)
    library = out / 'linear64.so'
    subprocess.run(['c++', '-O3', '-std=c++17', '-shared', '-fPIC', str(base/PINS['engine_cpp'][0]), '-o', str(library)], check=True)
    engine = module(base/PINS['engine'][0], 'earlier_independent_field_engine')
    field = engine.Field(library)
    oldfield = module(base/PINS['field'][0], 'earlier_independent_GF64')
    geom = module(base/PINS['geometry_review'][0], 'earlier_independent_geometry')
    need(np.array_equal(field.product, oldfield.MUL), 'independent field tables agree')
    native = geom.Native(repo, oldfield)
    layout = json.loads(payload['geometry']); H = list(map(frozenset, layout['A2'])); D = list(map(frozenset, layout['D4']))
    roots = layout['root_table']
    perp = [{j for j, y in enumerate(roots) if sum(a*b for a, b in zip(x, y)) == 0} for x in roots]
    need(all(set(native.adj[i]) == perp[i] for i in range(120)), 'actual real orthogonality')
    stars = {j: [h for h, P in enumerate(H) if j in P] for j in range(111)}
    views = {(j, i): [h for h in stars[j] if H[h] <= perp[i]] for j in range(111) for i in perp[j]}
    need(all(len(hs) == 16 for hs in views.values()), 'all geometric receiver views')
    wires = defaultdict(list); xcount = Counter(); owners = set()
    for line in payload['routes'].splitlines():
        phase, role, coordinate, h, d, k, source, terminal = json.loads(line)
        need((phase, role, coordinate) not in owners, 'one route per actual original owner')
        owners.add((phase, role, coordinate))
        if phase == 'X':
            need(role == source, 'early owner belongs to actual donor'); xcount[h] += 1
        if h is not None and source is not None:
            wires[source, h, phase].extend((((phase == 'Y')*111+role)*480+coordinate)*8+c for c in range(8))
    need(len(owners) == 106560, 'all physical X and Y routes')
    for holders in wires.values():
        holders.sort(); need(len(holders) == len(set(holders)), 'distinct actual source slots')
    parameters = json.loads(payload['parameters']); centres = parameters['centres']
    need(centres == [263, 642, 135], 'literal connected chain')
    donors = sorted(set.union(*(set(H[h]) for h in centres)))
    need(donors == [0, 25, 45, 47, 61, 62, 100] and H[263] & H[642] == {61}
         and H[642] & H[135] == {45} and not H[263] & H[135], 'different shared donor on each chain edge')
    need(all(max(len(wires[j, h, 'X']) for h in stars[j]) <= 240 for j in donors), 'all seven source stars are ordinary')
    charts = {(h, k): geom.Chart(native, h, k) for h in centres for k in (3, 12)}
    ctx = SimpleNamespace(repo=repo, base=base, payload=payload, field=field, native=native, H=H, D=D,
                          perp=perp, stars=stars, views=views, wires=wires, xcount=xcount, parameters=parameters,
                          centres=centres, donors=donors, charts=charts, maps={}, components={})
    for k in (3, 12):
        build(ctx, k)
    return ctx

def build(ctx, k):
    # Compute connected components of flag identifications, using an explicit
    # adjacency graph rather than the author's union/find implementation.
    flags = [(j, h) for j in ctx.donors for h in ctx.stars[j]]
    adjacent = {flag: set() for flag in flags}
    for h in ctx.centres:
        chart = ctx.charts[h, k]
        for x in chart.xs:
            triplet = [(j, next(q for q, p in chart.point[j].items() if p == x)) for j in chart.donors]
            for flag in triplet:
                adjacent[flag].update(set(triplet) - {flag})
    unseen = set(flags); components = []
    while unseen:
        first = min(unseen); group = {first}; todo = [first]; unseen.remove(first)
        while todo:
            flag = todo.pop()
            fresh = adjacent[flag] & unseen
            unseen.difference_update(fresh); group.update(fresh); todo.extend(fresh)
        components.append(sorted(group))
    components.sort(key=lambda group: group[0])
    group_id = {flag: i for i, group in enumerate(components) for flag in group}
    need(len(components) == 34 and len(group_id) == 196, '34 simultaneous quotient classes on 196 actual flags')
    need(all(len({group_id[j, h] for h in ctx.stars[j]}) == 28 for j in ctx.donors), 'no two planes of one source are identified')
    seed = ctx.parameters[str(k)]['seed']; F = ctx.field
    equations = []; coefficient_ranks = Counter(); changes = []
    for side, h in enumerate(ctx.centres):
        chart = ctx.charts[h, k]; control = [group_id[j, h] for j in chart.donors]
        need(len(chart.ports) == 3*k, 'component port count')
        for ordinal, port in enumerate(chart.ports):
            for attempt in range(100):
                U = pseudo(f'core/{h}/{k}/{seed}/{port}/{attempt}', 2, 2)
                determinant = int(F.product[U[0, 0], U[1, 1]] ^ F.product[U[0, 1], U[1, 0]])
                if determinant:
                    break
            else:
                raise ValueError('no invertible contrast frame')
            changes.append((h, port, attempt))
            rows = np.zeros((2, 34*k), dtype=np.uint8)
            for a in range(2):
                scales = [int(U[a, 0] ^ U[a, 1]), int(U[a, 0]), int(U[a, 1])]
                for donor in range(3):
                    sl = slice(control[donor]*k, (control[donor]+1)*k)
                    rows[a, sl] ^= F.product[scales[donor], chart.V[ordinal, donor*k:(donor+1)*k]]
            first = chart.donors[0]
            for point in sorted(ctx.native.rad[port]):
                q = next(q for q, x in chart.point[first].items() if x == point)
                group = group_id[first, q]
                coefficient = pseudo(f'general-relations/{ctx.centres}/{k}/{seed}/{side}/{port}/{point}', 2, k)
                coefficient_ranks[F.rank(coefficient)] += 1
                rows[:, group*k:(group+1)*k] ^= coefficient
            equations.extend(rows)
    relation = np.vstack(equations)
    need(relation.shape == (18*k, 34*k) and F.rank(relation) == 18*k, 'independent joint equations')
    embedding = F.null(relation)
    need(embedding.shape == (34*k, 16*k) and not np.any(F.mm(relation, embedding)), 'one common original-coordinate kernel basis')
    author = json.loads(ctx.payload['author_result'])
    expected = author['components'][str(k)]
    need(sha256(relation.tobytes()).hexdigest() == expected['constraint_sha256'], 'independent constraint bytes')
    need(sha256(embedding.tobytes()).hexdigest() == expected['embedding_sha256'], 'unique RREF kernel bytes')
    for j in ctx.donors:
        rows = {h: embedding[group_id[j, h]*k:(group_id[j, h]+1)*k] for h in ctx.stars[j]}
        actual = sha256(b''.join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
        need(actual == author['source_coefficient_sha256'][f'{j}/{k}'], 'all source coefficients independently reconstructed')
        ctx.maps[j, k] = rows
    ctx.components[k] = {'classes': components, 'group_id': group_id, 'relation': relation, 'embedding': embedding,
                         'point_coefficient_rank_census': dict(coefficient_ranks), 'contrast_frame_attempts': changes}
