#!/usr/bin/env python3
"""Independent exact static communication cut and rational source binding.

Only Python's standard library is used. No author or predecessor module is
imported. The 1289-input source is expanded as sparse Fraction rows, unlike
the predecessor's packed integer lane evaluation. Rank pivots run in the
opposite column order and do not normalize stored pivot rows.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import gzip
from hashlib import sha256
import json
from pathlib import Path
import time

N = 400
SOURCE = 'research/moonshot-005-program/results/complex-native-contested-restoration/rail/sources'
PINS = {
    'rail-base.json.gz': 'd8f772b3b2c157da6756f29dd93170feda941a10f57af6e7043c3443ee9c6022',
    'base-correction.json.gz': '2b1c8c9ab761aac65f7097b71893fef55f8c0fe090de8f9ea722346940c3e2f5',
    'LAYOUT.json.gz': 'b0f3ebc5710e469f3e8fc5ce159cbba048b563944182b50993431ef94f4fedbf',
    'DOUBLE-CANDIDATE.json.gz': '1b1b3294e86979f1f41076fb056f3c0a08ace6df7bf80f2886bc579a22962f4b',
    'DOUBLE-APPLICATION.json.gz': '69596ca0289d3164b0149cd7b0bbed8b8775243d6af8817088006df334c8962e',
}

def require(value, message):
    if not value:
        raise ValueError(message)

@lru_cache(None)
def fraction(value):
    return Fraction(value)

def axpy(acc, scalar, row):
    for j, value in row.items():
        new = acc.get(j, 0) + scalar * value
        if new:
            acc[j] = new
        else:
            acc.pop(j, None)

def product(left, right):
    answer = []
    for row in left:
        acc = {}
        for j, scalar in row.items():
            axpy(acc, scalar, right[j])
        answer.append(acc)
    return answer

def digest(rows):
    literal = [[[j, str(x)] for j, x in sorted(row.items())] for row in rows]
    return sha256(json.dumps(literal, separators=(',', ':')).encode()).hexdigest()

def rank(rows):
    pivots = {}
    for raw in reversed(rows):
        row = raw.copy()
        while row:
            c = max(row)
            if c not in pivots:
                pivots[c] = row
                break
            axpy(row, -row[c] / pivots[c][c], pivots[c])
    return len(pivots)

def block(rows, selected_rows, selected_columns):
    return [{j: x for j, x in rows[i].items() if j in selected_columns}
            for i in sorted(selected_rows)]

def subspaces(frames):
    spans = []
    for basis in frames:
        require(all(type(v) is int and 0 < v < 512 for v in basis), 'literal F2^9 frame')
        span = {0}
        for x in basis:
            extended = {v ^ x for v in span}
            require(span.isdisjoint(extended), 'independent chart basis')
            span.update(extended)
        require(len(span) == 1 << len(basis), 'dimension of physical subspace')
        spans.append(frozenset(span))
    return spans

def replay(word):
    require(word['public'] == N and len(word['initial']) == N, '400-field rail')
    owned = word['owned_fields']
    frames = word['frames']; spans = subspaces(frames)
    sites = word['initial'][:] + [None] * owned
    values = [{j: Fraction(1)} for j in range(N)] + [None] * owned
    count = Counter(); paid = Counter(); live = peak = 0
    for op in word['program']:
        kind, a = op[:2]
        require(type(a) is int and 0 <= a < len(sites), 'valid physical owner label')
        count[kind] += 1
        if kind == 'ADD':
            _, d, s, literal, chart = op
            require(d != s and 0 <= s < len(sites), 'distinct ADD fields')
            require(sites[d] == sites[s] == chart and sites[d] is not None, 'actual cochart ADD')
            axpy(values[d], fraction(literal), values[s])
        elif kind == 'SCALE':
            _, d, literal, chart = op
            c = fraction(literal)
            require(sites[d] == chart and chart is not None and c, 'actual invertible cochart SCALE')
            values[d] = {j: c * x for j, x in values[d].items()}
        elif kind == 'INIT':
            _, d, chart = op
            require(d >= N and sites[d] is None and values[d] is None, 'INIT only inactive owned field')
            require(0 <= chart < len(frames), 'initial chart exists')
            sites[d] = chart; values[d] = {}; live += 1; peak = max(peak, live)
        elif kind == 'CLEAR':
            _, d, chart = op
            require(d >= N and sites[d] == chart and chart is not None, 'actual CLEAR ownership')
            sites[d] = None; values[d] = None; live -= 1
        elif kind == 'MOVE':
            _, d, before, after, owned_flag = op
            require(sites[d] == before and type(owned_flag) is bool, 'actual MOVE source')
            require(owned_flag == (d >= N), 'public versus owned MOVE flag')
            require(0 <= before < len(frames) and 0 <= after < len(frames), 'MOVE charts exist')
            require(spans[before] < spans[after] or (owned_flag and spans[after] < spans[before]),
                    'strict subspace inclusion and downward-owner guard')
            paid[abs(len(frames[before]) - len(frames[after]))] += 1
            sites[d] = after
        else:
            raise ValueError('unknown rail opcode ' + kind)
    require(live == 0 and all(s is None for s in sites[N:]), 'all owned fields retired')
    require(all(v is None for v in values[N:]), 'all retired values removed')
    require(count == {'ADD': 3213, 'MOVE': 803, 'INIT': 365, 'CLEAR': 365, 'SCALE': 2},
            'exact private instruction census')
    require(owned == 93 and peak == 29, 'physical liveness census')
    return values[:N], sites[:N], paid, dict(count), peak, spans

def source_transfer(data, receipt):
    n = len(data['initial'])
    require(n == 1289 and len(data['final']) == n, '1289 independent upstream inputs')
    spans = subspaces(data['frames'])
    forms = {}
    for output, terms in data['forms']:
        require(output not in forms, 'unique source form')
        row = {}
        for event, literal in terms:
            q = fraction(literal)
            require(q and event not in row, 'nonzero unique source incidence')
            row[event] = q
        forms[output] = row
    schedule = data['schedule']
    require(len(schedule) == len(forms) and set(schedule) == set(forms), 'complete source schedule')
    moves = {event: (a, b) for event, a, b in data['moves']}
    require(len(moves) == len(data['moves']) == 5707, '5707 unique source moves')
    outputs = set(range(data['first_output'], data['first_output'] + n))
    require(set(forms) == set(moves) | outputs and not (set(moves) & outputs), 'source event partition')
    location = {~j: data['initial'][j] for j in range(n)}
    values = {~j: {j: Fraction(1)} for j in range(n)}
    remaining = Counter(event for form in forms.values() for event in form)
    for event in outputs:
        remaining[event] += 1
    paid = Counter()
    for event in schedule:
        chart = moves[event][0] if event in moves else data['final'][event - data['first_output']]
        form = forms[event]
        acc = {}
        for child, scalar in form.items():
            require(child in values and location[child] == chart, 'source stock ownership and causality')
            axpy(acc, scalar, values[child])
            remaining[child] -= 1
            if remaining[child] == 0:
                del values[child]
        if event in moves:
            a, b = moves[event]
            require(spans[a] < spans[b] or spans[b] < spans[a], 'nested paid source movement')
            paid[abs(len(data['frames'][a]) - len(data['frames'][b]))] += 1
            location[event] = b
        else:
            location[event] = chart
        values[event] = acc
    require(paid == Counter({int(r): c for r, c in receipt['native']['paid_native_ranks'].items()}),
            'full upstream source movement invoice')
    return [values[data['first_output'] + j] for j in range(n)]

def bind_target(source, layout, word, final_sites, full):
    labels = layout['source_labels']
    require(len(labels) == 1289 and len(set(labels)) == 1289, 'bijective upstream source labels')
    positions = {label: j for j, label in enumerate(labels)}
    local_to_upstream = {int(local): positions[int(label)] for label, local in word['source_role_map'].items()}
    require(set(local_to_upstream) == set(range(N)), 'all local main labels')
    mains = set(local_to_upstream.values())
    require(len(mains) == N, '400 distinct main source columns')
    helper_ids = set(range(1289)) - mains
    require(len(helper_ids) == 889 and all(full[j] == {j: 1} for j in helper_ids), '889 independent helper identities')
    reverse = {upstream: local for local, upstream in local_to_upstream.items()}
    target = []
    for local in range(N):
        upstream = local_to_upstream[local]
        require(set(full[upstream]) <= mains, 'main output has no helper-column leakage')
        require(word['frames'][word['initial'][local]] == source['frames'][source['initial'][upstream]],
                'literal main birth chart binding')
        require(word['frames'][final_sites[local]] == source['frames'][source['final'][upstream]],
                'literal main terminal chart binding')
        target.append({reverse[j]: q for j, q in full[upstream].items()})
    return target

def canonicalize(spans):
    representatives = {}; labels = []
    for j, span in enumerate(spans):
        if span not in representatives:
            representatives[span] = j
        labels.append(representatives[span])
    return labels

def cut_census(word, ends, spans, cert):
    canonical = canonicalize(spans)
    inside_list = cert['inside_canonical_chart_ids']
    require(len(inside_list) == len(set(inside_list)) == 128, '128 distinct cut spaces')
    inside = set(inside_list)
    require(all(0 <= j < len(canonical) and canonical[j] == j for j in inside), 'literal canonical representatives')
    require(canonical[127] in inside and canonical[3] not in inside, 'full and empty chart sides')
    born = {j for j, c in enumerate(word['initial']) if canonical[c] in inside}
    final = {j for j, c in enumerate(ends) if canonical[c] in inside}
    require(len(born) == 172 and len(final) == 228, 'actual public endpoint partition')
    crossing = {'forward': [], 'reverse': []}
    histogram = {'forward': Counter(), 'reverse': Counter()}
    all_moves = []
    for i, op in enumerate(word['program']):
        if op[0] != 'MOVE':
            continue
        _, reg, a, b, owned = op
        side_a = canonical[a] in inside; side_b = canonical[b] in inside
        grade = abs(len(word['frames'][a]) - len(word['frames'][b]))
        all_moves.append((i, grade, side_a != side_b))
        if side_a == side_b:
            continue
        require(spans[a] != spans[b] and grade >= 1, 'real positive-grade crossing')
        direction = 'forward' if side_a else 'reverse'
        crossing[direction].append({'instruction': i, 'source': a, 'destination': b, 'register': reg, 'rank': grade})
        histogram[direction][grade] += 1
    require(len(crossing['forward']) == 8 and len(crossing['reverse']) == 64, 'two old message capacities')
    require(all(x['source'] == 127 and x['destination'] == 3 and x['rank'] == 9
                for x in crossing['forward']), 'eight literal downward full-to-empty routes')
    require(all(crosses for _, grade, crosses in all_moves if grade == 9), 'every rank-nine route is debited')
    # Any alternative ordered basis of an existing span is in the same side.
    aliases = []
    for j, basis in enumerate(word['frames']):
        alternate = list(reversed(basis))
        if len(alternate) >= 2:
            alternate[0] ^= alternate[1]
        alt_span = subspaces([alternate])[0]
        require(alt_span == spans[j], 'changed frame basis preserves space')
        aliases.append(canonical[j])
    require(aliases == canonical, 'cut invariant under frame aliases')
    return born, final, crossing, histogram, all_moves, canonical

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    package = Path(__file__).resolve().parent.parent
    objects = {}; raw_hash = {}; payload_hash = {}
    for name, expected in PINS.items():
        raw = (args.repo / SOURCE / name).read_bytes()
        require(sha256(raw).hexdigest() == expected, 'archive pin ' + name)
        payload = gzip.decompress(raw)
        raw_hash[name] = sha256(raw).hexdigest(); payload_hash[name] = sha256(payload).hexdigest()
        objects[name] = json.loads(payload)
    require(payload_hash['DOUBLE-CANDIDATE.json.gz'] == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48',
            'canonical upstream word payload')
    require(payload_hash['DOUBLE-APPLICATION.json.gz'] == '1b2d87e93ae023f5ffd464546af53281b6cb4963dfd76ae4742e0a5540b752fa',
            'canonical upstream caller payload')
    word = objects['rail-base.json.gz']; source = objects['DOUBLE-CANDIDATE.json.gz']
    application = objects['DOUBLE-APPLICATION.json.gz']
    require(application['word_sha256'] == payload_hash['DOUBLE-CANDIDATE.json.gz'], 'caller binds actual source word')
    old, ends, paid, counts, peak, spans = replay(word)
    print('PASS_INDEPENDENT_RATIONAL_RAIL_AND_ALL_OWNER_GUARDS', flush=True)
    full = source_transfer(source, application)
    target = bind_target(source, objects['LAYOUT.json.gz'], word, ends, full)
    correction = [{int(j): fraction(x) for j, x in row.items()} for row in objects['base-correction.json.gz']]
    require(product(correction, old) == target, 'exact all-column CL=E against independently expanded source')
    require(rank(target) == N and rank(old) == N, 'exact invertible target and old endpoint')
    print('PASS_INDEPENDENT_ALL_1289_SOURCE_COLUMNS_AND_CHART_BINDING', flush=True)
    cut_raw = (package / 'CUT.json').read_bytes(); cert = json.loads(cut_raw)
    born, final, crossing, histograms, all_moves, canonical = cut_census(word, ends, spans, cert)
    universe = set(range(N))
    target_blocks = [block(target, universe - final, born), block(target, final, universe - born)]
    old_blocks = [block(old, universe - final, born), block(old, final, universe - born)]
    target_ranks = list(map(rank, target_blocks)); old_ranks = list(map(rank, old_blocks))
    require(target_ranks == [90, 146], 'authentic directional target ranks')
    require(old_ranks == [8, 64], 'old endpoint saturates but obeys both capacities')
    capacities = [len(crossing[d]) for d in ['forward', 'reverse']]
    deficits = [max(0, demand - supply) for demand, supply in zip(target_ranks, capacities)]
    require(deficits == [82, 82] and sum(deficits) == 164, 'two disjoint directional deficits')
    require(len(all_moves) == 803 and sum(paid.values()) == 803, 'every paid occurrence counted once')
    require(sum(crosses for _, _, crosses in all_moves) == 72, '72 total old crossing occurrences')
    require(sum(grade == 9 for _, grade, _ in all_moves) == 8, 'exact rank-nine crossing census')
    author_raw = (package / 'author/output/RESULT.json').read_bytes(); author = json.loads(author_raw)
    require(author['old_crossings'] == crossing, 'all 72 author crossing records independently matched')
    require(author['target_cross_ranks'] == target_ranks and author['old_endpoint_cross_ranks'] == old_ranks,
            'independent rational rank comparison')
    require(author['old_cross_capacities'] == capacities and author['new_move_deficits'] == deficits,
            'independent capacity comparison')
    caller = application['caller_census']
    result = {
        'status': 'PASS_INDEPENDENT_TWO_WAY_STATIC_CUT_164',
        'new_complete_kappa': False,
        'no_author_or_predecessor_python_imported': True,
        'source_columns': 1289, 'helper_identities': 889, 'main_columns': 400,
        'rail_instruction_census': counts, 'owned_labels': word['owned_fields'], 'peak_live_owned': peak,
        'rail_endpoint_sha256': digest(old), 'upstream_target_sha256': digest(target),
        'upstream_all_column_sha256': digest(full),
        'literal_source_input_charts': word['initial'], 'literal_source_output_charts': ends,
        'inside_inputs': sorted(born), 'inside_outputs': sorted(final),
        'cut_spaces': len(cert['inside_canonical_chart_ids']), 'chart_count': len(spans),
        'distinct_chart_spaces': len(set(spans)), 'target_cross_ranks': target_ranks,
        'old_endpoint_cross_ranks': old_ranks, 'old_cross_capacities': capacities,
        'new_move_deficits': deficits, 'minimum_new_moves': sum(deficits),
        'old_crossings': crossing,
        'old_crossing_histograms': {d: dict(sorted(h.items())) for d, h in histograms.items()},
        'all_paid_ranks': dict(sorted(paid.items())),
        'all_rank_nine_moves_cross': True,
        'caller_calls': caller['calls'], 'fixed_caller_paid': caller['fixed_caller_paid'],
        'fixed_root_targets': caller['fixed_root_targets'],
        'native_paid_ranks': application['native']['paid_native_ranks'],
        'native_helper_ranks': application['native']['positive_helper_ranks'],
        'price_scope': 'Exact movement histograms exported; price inequalities reviewed separately by root.',
        'controls': ['The exactly implemented endpoint has zero directional deficit.',
                     'Reversing and shearing every chart basis preserves its cut class.',
                     'Independent Fraction expansion of all upstream columns agrees with CL=E.'],
        'compressed_source_hashes': raw_hash, 'decompressed_source_hashes': payload_hash,
        'cut_sha256': sha256(cut_raw).hexdigest(),
        'author_result_sha256': sha256(author_raw).hexdigest(),
        'seconds': round(time.monotonic() - started, 6),
    }
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    matrices = {'target': [[[j, str(x)] for j, x in sorted(row.items())] for row in target],
                'old': [[[j, str(x)] for j, x in sorted(row.items())] for row in old]}
    payload = json.dumps(matrices, sort_keys=True, separators=(',', ':')).encode()
    (args.out / 'ENDPOINTS.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    print(result['status'], sum(deficits), result['seconds'], flush=True)

if __name__ == '__main__':
    main()
