#!/usr/bin/env python3
"""Independent audit of PR6166 sign pruning, not its full search.

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance. Apache-2.0.
The unchanged subject implementation is credited in UPSTREAM.json.
"""
import argparse
from collections import Counter
from hashlib import sha1, sha256
import gzip
import itertools as it
import json
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORD = 'research/p104-helper470-twin-rung-removal/WORD.json.gz'
SEED = 66


def need(ok, message):
    if not ok:
        raise ValueError(message)


def partitions(n):
    """Restricted-growth strings, one per set partition."""
    def extend(prefix, largest):
        if len(prefix) == n:
            yield prefix
        else:
            for label in range(largest + 2):
                yield from extend(prefix + (label,), max(largest, label))
    yield from extend((0,), 0)


def relabel(values):
    labels = {}
    return tuple(labels.setdefault(v, len(labels)) for v in values)


def explicit_orbits(p):
    """BFS under component flips; no canonicalization predicate is used."""
    raw = set(it.product(range(3), repeat=len(p))) - {(0,) * len(p)}
    generators = [tuple(i for i, c in enumerate(p) if c == label) for label in set(p)]
    orbits = []
    while raw:
        pending = [min(raw)]; orbit = set(pending)
        while pending:
            x = pending.pop()
            for positions in generators:
                y = list(x)
                for i in positions:
                    y[i] = -y[i] % 3
                y = tuple(y)
                if y not in orbit:
                    orbit.add(y); pending.append(y)
        need(orbit <= raw, 'orbit components overlap')
        raw -= orbit; orbits.append(frozenset(orbit))
    return tuple(orbits)


def transversal(orbits, retained):
    need(set().union(*orbits) >= set(retained), 'retained vector outside domain')
    for orbit in orbits:
        need(len(orbit & retained) == 1, 'not exactly one representative per orbit')


def graph_partition(prior, support):
    """Connectivity oracle: old components and the new support hyperedge."""
    edges = [set(i for i, c in enumerate(prior) if c == label) for label in set(prior)]
    edges.append(set(support))
    todo, components = set(range(len(prior))), []
    while todo:
        component = {min(todo)}
        while True:
            grown = component | set().union(*(e for e in edges if e & component))
            if grown == component:
                break
            component = grown
        todo -= component; components.append(component)
    return tuple(next(min(c) for c in components if i in c) for i in range(len(prior)))


def blob_hash(raw):
    return sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def sources():
    upstream = json.loads((HERE / 'UPSTREAM.json').read_text())
    for row in upstream['files']:
        raw = (HERE / row['path']).read_bytes()
        need(sha256(raw).hexdigest() == row['sha256'], 'upstream SHA256: ' + row['path'])
        need(blob_hash(raw) == row['git_blob'], 'upstream Git blob: ' + row['path'])
    pins = json.loads((HERE / 'SOURCES.json').read_text())
    rows = [r for r in pins['files'] if r['usage'] == 'input']
    need([r['path'] for r in rows] == [WORD], 'exact input domain')
    raw = (ROOT / WORD).read_bytes()
    need(sha256(raw).hexdigest() == rows[0]['sha256'], 'word SHA256')
    need(blob_hash(raw) == rows[0]['git_blob'], 'word Git blob')
    word = json.loads(gzip.decompress(raw)); ports = []
    for live in sorted(word['live']):
        frame = word['frames'][word['initial'][live]]
        need(len(frame) == 1 and frame[0] != 0, 'live frame is one-dimensional')
        ports.append(frame[0])
    need(len(ports) == len(set(ports)) == 104 and
         all(isinstance(q, int) and 0 < q < 512 and q.bit_count() % 2 for q in ports),
         '104 distinct odd nine-bit ports')
    namespace = {'__name__': 'retained_code8_subject'}
    # Compile authenticated source bytes directly, never a pre-existing .pyc.
    exec(compile((HERE / 'inputs/code8.py').read_bytes(), 'retained_code8.py', 'exec'), namespace)
    model_type = namespace['Model']; model = model_type(ports)
    pivots = tuple(model.T)
    need(len(pivots) == len(set(pivots)) == 8, 'eight pivots')
    need(all((ports[i] & ports[j]).bit_count() % 2 for i in pivots for j in pivots if i != j),
         'pivot clique independently checked')
    need(model.others == [j for j in range(104) if j not in pivots], 'non-clique port domain')
    expected_blocks = {j: [t for t in pivots if (ports[t] & ports[j]).bit_count() % 2 == 0]
                       for j in model.others}
    need(model.Tj == expected_blocks, 'source support blocks match port geometry')
    blocks = sorted(set(tuple(model.Tj[j]) for j in model.others))
    need(len(model.others) == 96 and len(blocks) == 14, '96 ports on 14 support blocks')
    need(all(len(b) == 4 and tuple(t for t in pivots if t in b) == b for b in blocks),
         'actual blocks are ordered four-subsets')
    expected = {v for v in it.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1}
    need(len(expected) == 40 and set(model.OPT) == expected and len(model.OPT) == 40,
         'source OPT is exactly the 40 normalized vectors')
    return model, pivots, tuple(model.OPT), blocks, upstream, rows[0]


def swap_signs(row, mask):
    """Substitute x_i -> -x_i at mask coordinates in an F3 linear row."""
    ones, twos = row
    return ((ones & ~mask) | (twos & mask), (twos & ~mask) | (ones & mask))


def equation_covariance(model):
    """Check actual source equations under each pivot sign generator.

    Normalizing the transformed coefficient row determines d_j. Variables in
    column j must then transform too. This checks the encoded equations without
    executing the predecessor's elimination, consistency test or DFS.
    """
    row_masks = {t: sum(1 << k for (r, _), k in model.var.items() if r == t) for t in model.T}
    column_masks = {j: sum(1 << k for (_, m), k in model.var.items() if m == j) for j in model.others}
    variable_mask = (1 << model.NV) - 1
    cases = equations = 0; bad_column_detected = False
    for j in model.others:
        for c in model.OPT:
            first = model.Tj[j][next(i for i, v in enumerate(c) if v)]
            old = model.EQS[j, c]
            need(len(old) > 0 and sum(bool((a | b) & model.RHS) for a, b in old) == 1,
                 'one nonhomogeneous equation per option')
            for t in model.T:
                dj = 2 if t == first else 1
                changed = tuple(dj * v * (2 if u == t else 1) % 3 for u, v in zip(model.Tj[j], c))
                need(changed in model.OPT, 'transformed option normalized')
                mask = row_masks[t] ^ (column_masks[j] if dj == 2 else 0)
                left = Counter(swap_signs(row, mask) for row in model.EQS[j, changed])
                right = Counter(swap_signs(row, variable_mask) if dj == 2 and not ((row[0] | row[1]) & model.RHS)
                                else row for row in old)
                need(left == right, 'actual source equations are not gauge covariant')
                if dj == 2:
                    wrong = Counter(swap_signs(row, row_masks[t]) for row in model.EQS[j, changed])
                    bad_column_detected |= wrong != right
                cases += 1; equations += len(old)
    need(bad_column_detected, 'missing-column-sign control did not fail actual equations')
    return cases, equations


def reject(call, fragment):
    try:
        call()
    except ValueError as exc:
        need(fragment in str(exc), 'wrong rejection: ' + str(exc)); return
    raise ValueError('negative control accepted: ' + fragment)


def controls(orbits, model_type, pivots):
    all_one = {v for v in it.product((0, 1), repeat=4) if any(v)}
    normalized = {v for v in it.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1}
    reject(lambda: transversal(orbits[(0, 0, 0, 0)], all_one), 'one representative')
    reject(lambda: transversal(orbits[(0, 1, 2, 3)], normalized), 'one representative')
    need(frozenset({(1, 2, 0, 0), (2, 1, 0, 0)}) in orbits[(0, 0, 0, 0)], 'over-prune witness')
    need(any({(1, 1, 0, 0), (1, 2, 0, 0)} <= o for o in orbits[(0, 1, 2, 3)]), 'under-prune witness')
    prior = tuple(range(8)); expected = graph_partition(prior, (0, 1))
    reject(lambda: need(prior == expected, 'merge mismatch'), 'merge mismatch')
    reject(lambda: need((0,) * 8 == expected, 'merge mismatch'), 'merge mismatch')
    # The omitted merge allows signs (1,2) on a previously joined pair.
    old_row, bad_signs = (1, 2), (1, 2)
    moved_row = tuple(x*s % 3 for x, s in zip(old_row, bad_signs))
    need(moved_row not in {old_row, tuple(-x % 3 for x in old_row)}, 'forgotten-merge witness')
    # For c*x=1, omitting the column sign makes the transformed diagonal 2.
    c, x, dt, dj = 1, 1, 1, 2
    need((dj*c*dt)*(dt*x*dj) % 3 == 1 and (dj*c*dt)*(dt*x) % 3 == 2,
         'missing column sign witness')
    subject = SimpleNamespace(Tj={0: pivots[:4]})
    need(model_type.canonical(subject, 0, (1, 2, 0, 0), dict.fromkeys(pivots, pivots[0])),
         'source keeps opposite signs inside one component')
    return ['over_prune_all_nonzero_entries_to_one', 'under_prune_first_entry_only',
            'omit_component_merge', 'merge_untouched_components', 'omit_column_gauge_sign']


def audit():
    model, pivots, options, actual_blocks, upstream, word_pin = sources()
    model_type = type(model)
    covariance_cases, covariance_rows = equation_covariance(model)
    parts = tuple(partitions(8)); blocks = tuple(it.combinations(range(8), 4))
    need(len(parts) == len(set(parts)) == 4140 and len(blocks) == 70, 'complete partition/block domain')
    oracle = {p: explicit_orbits(p) for p in partitions(4)}
    need(len(oracle) == 15, 'Bell(4) induced partitions')
    representatives = {p: {min(o) for o in orbits} for p, orbits in oracle.items()}
    for p, orbits in oracle.items():
        transversal(orbits, representatives[p])
        for orbit in orbits:
            v = min(orbit); active = len({p[i] for i, x in enumerate(v) if x})
            need(len(orbit) == 2 ** active, 'orbit-size formula')
        formula = sum(2 ** (len(s) - len({p[i] for i in s}))
                      for k in range(1, 5) for s in it.combinations(range(4), k))
        need(formula == len(orbits), 'orbit count formula')
    supports = tuple(s for k in range(1, 5) for s in it.combinations(range(8), k))
    histogram = Counter(); states = merges = graph_cases = sign_tests = allowed_signs = 0
    for p in parts:
        # The source replay starts with cls[t] = its position in T.
        cls = {pivots[i]: p.index(p[i]) for i in range(8)}
        expected_merges = {s: graph_partition(p, s) for s in supports}
        graph_cases += len(expected_merges)
        for indices in blocks:
            subject = SimpleNamespace(Tj={0: tuple(pivots[i] for i in indices)})
            induced = relabel(p[i] for i in indices)
            retained = {c for c in options if model_type.canonical(subject, 0, c, cls)}
            need(retained == representatives[induced], 'source canonical differs from orbit oracle')
            histogram[len(retained)] += 1; states += 1
            for c in options:
                support = tuple(i for i, v in zip(indices, c) if v)
                merged = model_type.merged(subject, 0, c, cls)
                need(set(merged) == set(pivots), 'merged state domain')
                need(tuple(merged[t] for t in pivots) == expected_merges[support],
                     'source merge differs from connectivity oracle')
                merges += 1
        history = [(p.index(p[i]), i, 1 + (SEED + i) % 2)
                   for i in range(8) if i != p.index(p[i])]
        observed = set()
        for mask in range(256):
            signs = tuple(2 if mask >> i & 1 else 1 for i in range(8))
            if all((signs[a] * signs[b] * value) % 3 == value for a, b, value in history):
                observed.add(mask)
            sign_tests += 1
        generated = {sum(1 << i for i in range(8) if flips[p[i]])
                     for flips in it.product((0, 1), repeat=max(p) + 1)}
        need(observed == generated, 'history stabilizer differs from component sign group')
        allowed_signs += len(observed)
    covariance = 0
    for c, x, dt, dj, dm in it.product(range(3), range(3), (1, 2), (1, 2), (1, 2)):
        need((dj*c*dt)*(dt*x*dm) % 3 == dj*dm*c*x % 3, 'term-wise equation covariance')
        covariance += 1
    negative = controls(oracle, model_type, pivots)
    return {'status': 'PASS_CARRIER_SIGN_GAUGE_AUDIT', 'no_new_kappa': True, 'seed': SEED,
            'source_commit': upstream['files'][0]['commit'],
            'source_hashes': {r['path']: r['sha256'] for r in upstream['files']},
            'word_sha256': word_pin['sha256'], 'pivot_indices': list(pivots),
            'actual_blocks': [list(b) for b in actual_blocks],
            'domain': {'partitions_8': len(parts), 'four_subsets': len(blocks),
                       'partition_block_states': states, 'normalized_options_per_state': len(options),
                       'source_canonical_calls': states*len(options), 'source_merge_calls': merges,
                       'independent_merge_graphs': graph_cases,
                       'stabilizer_sign_tests': sign_tests, 'allowed_stabilizer_signs': allowed_signs,
                       'term_covariance_cases': covariance,
                       'actual_equation_gauges': covariance_cases, 'actual_equation_rows': covariance_rows},
            'retained_option_count_histogram': {str(k): v for k, v in sorted(histogram.items())},
            'induced_orbits': [{'partition': list(p), 'count': len(o),
                                'orbit_size_histogram': dict(sorted(Counter(map(len, o)).items()))}
                               for p, o in oracle.items()], 'negative_controls': negative}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-result', action='store_true', help='write deterministic receipt')
    args = parser.parse_args(); result = audit()
    raw = json.dumps(result, indent=2, sort_keys=True) + '\n'; path = HERE / 'RESULT.json'
    if args.write_result:
        path.write_text(raw)
    else:
        need(path.read_text() == raw, 'RESULT.json differs from recomputed evidence')
    d = result['domain']
    print(result['status'], 'states=' + str(d['partition_block_states']),
          'merges=' + str(d['source_merge_calls']), 'controls=' + str(len(result['negative_controls'])),
          'no_new_kappa')


if __name__ == '__main__':
    main()
