#!/usr/bin/env python3
"""Independent weighted acyclic paid-code certificate check; no author imports."""
import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

SCALE = 2**128
PINS = {
    'source': ('research/shared-wire-split-composition/data/final.json.gz', '8f248653791e44acc88aab2e149957e9c2cb3ffa5f7bb958002c9994631a16ca'),
    'routing': ('research/moonshot-005-program/results/endpoint-side-information/RESULT.json.gz', '58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139'),
    'expanded': ('research/moonshot-005-program/results/endpoint-side-information/EXPANDED.json.gz', '0df1ceb9babf6931572f7aa558ec8fadfe9ca2966540ca0d92a06a9d1b157864'),
    'invoice': ('research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json', 'b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'),
}
SOURCE_HASH = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'


def need(value, message):
    if not value:
        raise ValueError(message)


def basis(vectors):
    pivots = {}
    for vector in vectors:
        for bit in sorted(pivots, reverse=True):
            if vector >> bit & 1:
                vector ^= pivots[bit]
        if vector:
            bit = vector.bit_length() - 1
            for old in tuple(pivots):
                if pivots[old] >> bit & 1:
                    pivots[old] ^= vector
            pivots[bit] = vector
    return tuple(pivots[bit] for bit in sorted(pivots, reverse=True))


def power(rank):
    if rank == 0:
        return 0, 0
    target = rank**199 * SCALE**200
    low, high = 0, rank * SCALE + 1
    while high - low > 1:
        mid = (low + high) // 2
        if mid**200 <= target:
            low = mid
        else:
            high = mid
    need(low**200 <= target < (low + 1)**200, 'binary-search rational power bracket')
    return low, low if low**200 == target else low + 1


def topological(vertices, S):
    degree = {i: sum(S[j][i] for j in vertices) for i in vertices}
    queue = deque(i for i in vertices if not degree[i])
    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in vertices:
            if S[i][j]:
                degree[j] -= 1
                if degree[j] == 0:
                    queue.append(j)
    need(len(order) == len(vertices), 'acyclic dual set')
    return order


def main(args):
    cert_bytes = args.certificate.read_bytes()
    certificate = json.loads(cert_bytes)
    inputs = {}
    for label, (path, pin) in PINS.items():
        need(certificate['source_pins'][label]['path'] == path and certificate['source_pins'][label]['payload_sha256'] == pin, 'reviewed source identity')
        raw = (args.repo / path).read_bytes()
        if label == 'source':
            need(hashlib.sha256(raw).hexdigest() == SOURCE_HASH, 'immutable native gzip pin')
        payload = gzip.decompress(raw) if path.endswith('.gz') else raw
        need(hashlib.sha256(payload).hexdigest() == pin, label + ' payload authentication')
        inputs[label] = json.loads(payload)
    native, routing, expanded, invoice = [inputs[label] for label in ['source', 'routing', 'expanded', 'invoice']]
    xs = sorted(native['live'])
    need(len(xs) == 104 and all(data['row_order_receiver_for_X'] == xs == data['column_order_donor_X'] for data in [routing, expanded]), 'source role order')
    bases = [basis(frame) for frame in native['frames']]
    need(all(len(b) == len(f) for b, f in zip(bases, native['frames'])), 'binary frame independence')
    first = {}
    canon = []
    for index, b in enumerate(bases):
        first.setdefault(b, index)
        canon.append(first[b])
    roles = xs + [x + 112 for x in xs]
    routes = {r: [canon[native['initial'][r]]] for r in roles}
    for instruction in native['program']:
        if instruction[0] == 'MOVE' and instruction[1] in routes:
            role, source, target = instruction[1:4]
            need(routes[role][-1] == canon[source], 'source route continuity')
            routes[role].append(canon[target])
    need(all(routes[r] == routing['raw_itineraries'][str(r)] for r in roles), 'all208 source raw itineraries match reviewed receipt')
    S = expanded['variants']['main_reuse_retimed47']['matrix']
    need(len(S) == 104 and all(len(row) == 104 and all(type(v) is int and v in (0, 1) for v in row) for row in S), 'actual Boolean side-information matrix')
    need(sum(map(sum, S)) == 1746, 'reviewed expanded side-information count')
    free = [i for i in range(104) if S[i][i]]
    need([xs[i] for i in free] == [22, 44, 72, 89, 109], 'self-delivery restriction')
    active = [i for i in range(104) if i not in free]
    D, R = defaultdict(int), defaultdict(int)
    for i in active:
        for chart in routes[xs[i]]:
            D[chart] |= 1 << i
        for chart in routes[xs[i] + 112]:
            R[chart] |= 1 << i
    need(len(D) == 352 and len(R) == 283, 'encoding and decoding chart census')
    side_masks = [sum(1 << j for j, v in enumerate(row) if v) for row in S]
    weights, sets, topo_orders = [], [], []
    for item in certificate['acyclic_sets']:
        vertices = [xs.index(role) for role in item['roles']]
        need(len(set(vertices)) == len(vertices) and set(vertices) <= set(active) and vertices, 'nonempty distinct active set')
        need(type(item['weight_numerator']) is int and item['weight_numerator'] >= 0, 'nonnegative rational weight numerator')
        topo_orders.append([xs[i] for i in topological(vertices, S)])
        sets.append(sum(1 << i for i in vertices))
        weights.append(item['weight_numerator'])
    den = certificate['weights_denominator']
    need(type(den) is int and den > 0, 'positive rational weight denominator')
    objective = sum(weight * vertices.bit_count() for weight, vertices in zip(weights, sets))
    need(objective == certificate['claimed_rational_bound_numerator'] == 98992356 and den == 1000000 and len(sets) == 74, 'exact dual objective')
    ranks = set(range(10)) | {int(rank) for name in ['T4', 'P4'] for rank in invoice[name]}
    powers = {rank: power(rank) for rank in ranks}
    legs_cache = {}
    def legs(a, b):
        if (a, b) not in legs_cache:
            combined = len(basis(bases[a] + bases[b]))
            legs_cache[a, b] = (combined - len(bases[b]), combined - len(bases[a]))
        return legs_cache[a, b]
    receiver_indices = {chart: [i for i in active if mask >> i & 1] for chart, mask in R.items()}
    checked = absorbed = 0
    min_slack = None
    for a, donor_mask in D.items():
        for b, receiver_mask in R.items():
            all_known = all(donor_mask & ~side_masks[i] == 0 for i in receiver_indices[b])
            if all_known:
                absorbed += 1
                continue
            down, up = legs(a, b)
            need(down or up, 'every unabsorbed packet changes its chart')
            credit = sum(weight for weight, vertices in zip(weights, sets) if vertices & donor_mask and vertices & receiver_mask)
            low_cost = powers[down][0] + powers[up][0]
            slack = low_cost * den - credit * SCALE
            need(slack >= 0, f'weighted paid constraint encoder{a} decoder{b}')
            min_slack = slack if min_slack is None else min(min_slack, slack)
            checked += 1
    need(checked == 87079 and absorbed == 12537 and checked + absorbed == 99616, 'exhaustive chart-pair coverage')
    mutual = {i: {j for j in active if j != i and S[i][j] and S[j][i]} for i in active}
    size_counts = Counter()
    exceptions = []
    singleton_witnesses = {}
    def enumerate_cliques(chosen, candidates, encoders, decoders):
        for offset, i in enumerate(candidates):
            group = chosen + [i]
            enc = encoders.intersection(routes[xs[i]])
            dec = decoders.intersection(routes[xs[i] + 112])
            need(enc and dec, 'clique has common granted stations')
            discounts = []
            for a in sorted(enc):
                for b in sorted(dec):
                    down, up = legs(a, b)
                    lower = powers[down][0] + powers[up][0]
                    upper = powers[down][1] + powers[up][1]
                    if len(group) == 1 and down + up == 1:
                        singleton_witnesses.setdefault(xs[i], [a, b, down, up])
                    if lower < len(group) * SCALE:
                        need(upper < len(group) * SCALE, 'strict discount independently enclosed')
                        discounts.append([a, b, down, up])
            if discounts:
                need([xs[j] for j in group] == [67, 80], 'only the exceptional pair has a strict discount')
                exceptions.append({'roles': [67, 80], 'routes': discounts})
            size_counts[len(group)] += 1
            enumerate_cliques(group, [j for j in candidates[offset + 1:] if j in mutual[i]], enc, dec)
    enumerate_cliques([], active, set(D), set(R))
    need(dict(size_counts) == {1: 99, 2: 346, 3: 319, 4: 280, 5: 176, 6: 48}, 'all1268 cliques independently enumerated')
    need(exceptions == [{'roles': [67, 80], 'routes': [[749, 105, 2, 0]]}], 'unique discounted source chart pair')
    need(len(singleton_witnesses) == 99, 'actual rank1 upper witnesses for every active coordinate')
    need(len(bases[749]) == 3 and len(bases[105]) == 1 and len(basis(bases[749] + bases[105])) == 3, 'nested exceptional geometry')
    need(powers[2][0] > SCALE and powers[2][1] < 2 * SCALE, 'nonnegative exceptional clique dual and strict pair discount')
    # Every singleton price is1; doubled weights fail an actual singleton chart pair.
    doubled_witness = next(({'role': xs[i], 'route': singleton_witnesses[xs[i]], 'doubled_credit': 2 * sum(w for w, U in zip(weights, sets) if U >> i & 1)} for i in active if 2 * sum(w for w, U in zip(weights, sets) if U >> i & 1) > den), None)
    need(doubled_witness is not None, 'doubled positive dual fails a real route')
    try:
        topological([xs.index(67), xs.index(80)], S)
    except ValueError:
        cyclic_rejected = True
    else:
        cyclic_rejected = False
    need(cyclic_rejected, 'mutual pair must not be accepted as acyclic')
    T, P = [{int(rank): count for rank, count in invoice[name].items()} for name in ['T4', 'P4']]
    need(all(type(count) is int and count >= 0 and rank > 0 for profile in [T, P] for rank, count in profile.items()), 'nonnegative full invoice histograms')
    need(sum(T.values()) == 27344 and sum(P.values()) == 152424, 'complete H4 counts')
    Hlo = F(sum(count * powers[rank][0] for rank, count in T.items()) - sum(count * powers[rank][1] for rank, count in P.items()), 18 * SCALE)
    Hhi = F(sum(count * powers[rank][1] for rank, count in T.items()) - sum(count * powers[rank][0] for rank, count in P.items()), 18 * SCALE)
    bound = F(objective, den)
    need(bound > Hhi, 'strict complete H4 exclusion in the fully newly paid path model')
    receipt = {'status': 'PASS_INDEPENDENT_FULLY_PAID_SOURCE_LOCALISED_CODE_BUDGET', 'certificate_sha256': hashlib.sha256(cert_bytes).hexdigest(), 'source_sha256': SOURCE_HASH, 'source_payload_pins': {key: value[1] for key, value in PINS.items()}, 'side_information_matrix_sha256': hashlib.sha256(json.dumps(S, separators=(',', ':')).encode()).hexdigest(), 'side_information_entries': 1746, 'free_self_roles': [xs[i] for i in free], 'active_demands': 99, 'acyclic_sets': len(sets), 'weights_nonnegative': True, 'weight_denominator': den, 'exact_lower_bound': str(bound), 'chart_pairs': {'encoding': len(D), 'decoding': len(R), 'all': checked + absorbed, 'absorbed': absorbed, 'paid_checked': checked}, 'minimum_certified_slack': str(F(min_slack, den * SCALE)), 'clique_census': {'total': sum(size_counts.values()), 'size_histogram': dict(sorted(size_counts.items())), 'discounted': exceptions, 'rank1_singleton_witnesses': singleton_witnesses, 'exact_optimum': '97+2^(199/200)'}, 'H4': {'native_repetitions': 18, 'target_count': sum(T.values()), 'paid_count': sum(P.values()), 'allowance_lower': str(Hlo), 'allowance_upper': str(Hhi), 'strict_deficit_lower': str(bound - Hhi)}, 'negative_controls': {'doubled_weights_real_route': doubled_witness, 'cyclic_pair_rejected': cyclic_rejected}, 'power_engine': {'method': 'integer binary search', 'denominator': str(SCALE), 'exponent': '199/200'}, 'scope': 'Every transport leg of each one-encoder/one-decoder packet is newly charged. The reviewed S is receiver side information only; it grants no free coded transit. All block volumes and arbitrary linear packet/decoder maps. Conditional H4 profile arithmetic; no complete supplier or new kappa.'}
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ['status', 'certificate_sha256', 'exact_lower_bound', 'chart_pairs', 'minimum_certified_slack', 'H4']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
