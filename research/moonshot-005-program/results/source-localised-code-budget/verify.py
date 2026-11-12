#!/usr/bin/env python3
"""Exact paid lower bound for source-localised one-stage linear codes.

The saved positive dual is checked with integer arithmetic. No LP solver is
imported. Prepared for CubeJerry with substantial OpenAI assistance.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POWER_DEN = 10**24


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_inputs(repo, cert):
    out = {}
    for label, pin in cert['source_pins'].items():
        raw = (repo / pin['path']).read_bytes()
        payload = gzip.decompress(raw) if pin['path'].endswith('.gz') else raw
        # Only the immutable source native requires its exact gzip container.
        if label == 'source':
            need(hashlib.sha256(raw).hexdigest() == pin['file_sha256'], 'native container pin')
        need(hashlib.sha256(payload).hexdigest() == pin['payload_sha256'], label + ' payload pin')
        out[label] = json.loads(payload)
    return out


def span(frame):
    s = {0}
    for vector in frame:
        s.update(v ^ vector for v in tuple(s))
    return frozenset(s)


def root_floor(value, degree):
    x = 1 << ((value.bit_length() + degree - 1) // degree)
    while True:
        y = ((degree - 1) * x + value // x**(degree - 1)) // degree
        if y >= x:
            break
        x = y
    while (x + 1)**degree <= value:
        x += 1
    while x**degree > value:
        x -= 1
    need(x**degree <= value < (x + 1)**degree, 'integer power bracket')
    return x


def power_bounds(rank):
    if not rank:
        return (0, 0)
    target = rank**199 * POWER_DEN**200
    lo = root_floor(target, 200)
    return lo, lo if lo**200 == target else lo + 1


def source_geometry(w, receipt, expanded):
    xs = sorted(w['live'])
    need(xs == receipt['row_order_receiver_for_X'] == expanded['row_order_receiver_for_X'], 'receiver role order')
    need(xs == receipt['column_order_donor_X'] == expanded['column_order_donor_X'], 'donor role order')
    spaces = list(map(span, w['frames']))
    first, canon = {}, []
    for i, s in enumerate(spaces):
        first.setdefault(s, i)
        canon.append(first[s])
    roles = set(xs) | {x + 112 for x in xs}
    route = {r: [canon[w['initial'][r]]] for r in roles}
    for e in w['program']:
        if e[0] == 'MOVE' and e[1] in roles:
            need(route[e[1]][-1] == canon[e[2]], 'native itinerary continuity')
            route[e[1]].append(canon[e[3]])
    for r, walk in route.items():
        need(walk == receipt['raw_itineraries'][str(r)], 'authenticated original raw itinerary')
    S = expanded['variants']['main_reuse_retimed47']['matrix']
    need(len(S) == 104 and all(len(row) == 104 for row in S), '104 by104 side-information matrix')
    free = [i for i in range(104) if S[i][i]]
    need([xs[i] for i in free] == [22, 44, 72, 89, 109], 'five granted self-deliveries')
    active = [i for i in range(104) if i not in free]
    D, R = defaultdict(int), defaultdict(int)
    for i in active:
        for c in route[xs[i]]:
            D[c] |= 1 << i
        for c in route[xs[i] + 112]:
            R[c] |= 1 << i
    return xs, spaces, route, S, active, D, R


def topo(mask, S):
    order = []
    while mask:
        sinks = [i for i in range(104) if mask >> i & 1 and not any(S[i][j] for j in range(104) if mask >> j & 1)]
        need(bool(sinks), 'dual set must be acyclic')
        for i in sinks:
            mask ^= 1 << i
            order.append(i)
    return order


def legs(a, b, spaces):
    meet = len(spaces[a] & spaces[b]).bit_length() - 1
    return tuple(r for r in ((len(spaces[a]).bit_length() - 1) - meet, (len(spaces[b]).bit_length() - 1) - meet) if r)


def all_known(donors, receivers, S):
    return all(not (receivers >> i & 1) or all(not (donors >> j & 1) or S[i][j] for j in range(104)) for i in range(104))


def verify_linear(cert, xs, spaces, S, active, D, R, powers):
    idx = {r: i for i, r in enumerate(xs)}
    active_set = set(active)
    masks, numerators, orders = [], [], []
    for item in cert['acyclic_sets']:
        indices = [idx[r] for r in item['roles']]
        need(len(indices) == len(set(indices)) and set(indices) <= active_set, 'distinct active dual vertices')
        mask = sum(1 << i for i in indices)
        order = topo(mask, S)
        numerator = item['weight_numerator']
        need(type(numerator) is int and numerator > 0, 'positive integer dual weight')
        masks.append(mask)
        numerators.append(numerator)
        orders.append([xs[i] for i in order])
    den = cert['weights_denominator']
    need(type(den) is int and den > 0, 'positive dual denominator')
    lower_num = sum(n * M.bit_count() for n, M in zip(numerators, masks))
    need(lower_num == cert['claimed_rational_bound_numerator'], 'claimed dual objective')
    Dsets = {c: sum(1 << j for j, U in enumerate(masks) if U & m) for c, m in D.items()}
    Rsets = {c: sum(1 << j for j, U in enumerate(masks) if U & m) for c, m in R.items()}
    credit_cache = {0: 0}
    known_cache = {}
    checked = absorbed = 0
    min_slack = None
    def credit(mask):
        if mask not in credit_cache:
            z, value = mask, 0
            while z:
                bit = z & -z
                value += numerators[bit.bit_length() - 1]
                z ^= bit
            credit_cache[mask] = value
        return credit_cache[mask]
    for a, donors in D.items():
        for b, receivers in R.items():
            key = (donors, receivers)
            if key not in known_cache:
                known_cache[key] = all_known(donors, receivers, S)
            if known_cache[key]:
                absorbed += 1
                continue
            ranks = legs(a, b, spaces)
            need(bool(ranks), 'zero-move observations are already side information')
            amount = credit(Dsets[a] & Rsets[b])
            cost_lower = sum(powers[r][0] for r in ranks)
            slack = cost_lower * den - amount * POWER_DEN
            need(slack >= 0, f'paid dual constraint at encoder{a},decoder{b}')
            min_slack = slack if min_slack is None else min(min_slack, slack)
            checked += 1
    # The identity code is an admitted positive control of the abstract interface.
    coordinate_credits = []
    for i in active:
        value = sum(n for n, U in zip(numerators, masks) if U >> i & 1)
        need(value <= den, 'one rank1 coordinate packet positive control')
        coordinate_credits.append(value)
    # Two false enlargements must be rejected by the actual certificate.
    need(sum(numerators) > den, 'false rank1 global broadcast must violate the dual')
    doubled_rejects = any(2 * z > den for z in coordinate_credits)
    need(doubled_rejects, 'doubling the certificate weights must be rejected')
    pair = [idx[67], idx[80]]
    need(S[pair[0]][pair[1]] and S[pair[1]][pair[0]], 'mutual-pair control premise')
    rejected = False
    try:
        topo(sum(1 << i for i in pair), S)
    except ValueError:
        rejected = True
    need(rejected, 'mutual-pair false acyclicity control')
    return {'lower_bound': str(Fraction(lower_num, den)), 'lower_numerator': lower_num, 'lower_denominator': den,
            'acyclic_sets': len(masks), 'all_chart_pairs': len(D) * len(R), 'checked_paid_pairs': checked,
            'side_information_pairs_absorbed': absorbed, 'positive_control_coordinate_packets': len(active),
            'negative_controls': ['false rank1 global broadcast', 'doubled dual weights', 'cyclic dual set'],
            'dual_topological_orders': orders, 'minimum_constraint_slack_scaled': str(min_slack)}


def verify_cliques(xs, spaces, route, S, active, powers):
    adj = {i: {j for j in active if i != j and S[i][j] and S[j][i]} for i in active}
    all_charts = set(range(len(spaces)))
    sizes = Counter()
    exceptional = []
    cases = 0
    def visit(group, candidates, enc, dec):
        nonlocal cases
        for offset, i in enumerate(candidates):
            g = group + [i]
            E = enc & set(route[xs[i]])
            F = dec & set(route[xs[i] + 112])
            need(E and F, 'packet common stops exist in the overgrant')
            k = len(g)
            discount = []
            for a in E:
                for b in F:
                    rr = legs(a, b, spaces)
                    lo = sum(powers[r][0] for r in rr)
                    hi = sum(powers[r][1] for r in rr)
                    if lo < k * POWER_DEN:
                        need(hi < k * POWER_DEN, 'discount classification is exact')
                        discount.append((a, b, rr))
            if discount:
                need([xs[j] for j in g] == [67, 80], 'unique discounted clique')
                need(all(rr == (2,) for _, _, rr in discount), 'only rank2 paths discount the pair')
                exceptional.append({'roles': [67, 80], 'discounted_routes': discount})
            cases += 1
            sizes[k] += 1
            visit(g, [j for j in candidates[offset + 1:] if j in adj[i]], E, F)
    visit([], active, all_charts, all_charts)
    need(cases == 1268 and len(exceptional) == 1, 'complete clique census')
    need((749, 105, (2,)) in exceptional[0]['discounted_routes'], 'explicit discounted pair route')
    # One rank2 sum gives each of the two receivers its demand when the other
    # coordinate is granted. The other97 demands use one coordinate each.
    need(S[xs.index(67)][xs.index(80)] == S[xs.index(80)][xs.index(67)] == 1, 'two-packet decoding algebra')
    need(powers[2][1] < 2 * POWER_DEN, 'all-unit clique dual is a rejecting control')
    return {'cliques': cases, 'size_histogram': dict(sorted(sizes.items())), 'exceptional': exceptional,
            'exact_fractional_and_integral_optimum': '97+2^(199/200)',
            'optimum_numerator_bounds': [str(97 * POWER_DEN + powers[2][k]) for k in (0, 1)],
            'optimum_denominator': str(POWER_DEN)}


def verify_tariff(invoice, linear, powers):
    T = {int(r): n for r, n in invoice['T4'].items()}
    P = {int(r): n for r, n in invoice['P4'].items()}
    lo = sum(n * powers[r][0] for r, n in T.items()) - sum(n * powers[r][1] for r, n in P.items())
    hi = sum(n * powers[r][1] for r, n in T.items()) - sum(n * powers[r][0] for r, n in P.items())
    L = Fraction(linear['lower_numerator'], linear['lower_denominator'])
    Hlo, Hhi = Fraction(lo, 18 * POWER_DEN), Fraction(hi, 18 * POWER_DEN)
    need(L > Hhi, 'full H4 paid budget is excluded before reverse duties')
    need(sum(T.values()) == 27344 and sum(P.values()) == 152424, 'full H4 target/paid census')
    return {'target_count': sum(T.values()), 'base_paid_count': sum(P.values()), 'native_repetitions': 18,
            'H4_allowance_per_native_bounds': [str(Hlo), str(Hhi)], 'price_lower': str(L),
            'strict_deficit_per_native_lower': str(L - Hhi), 'all_reverse_and_other_duties_granted_free': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, default=HERE / 'CERTIFICATE.json')
    parser.add_argument('--output', type=Path)
    a = parser.parse_args()
    cert = json.loads(a.certificate.read_text())
    inputs = load_inputs(a.repo, cert)
    geometry = source_geometry(inputs['source'], inputs['routing'], inputs['expanded'])
    xs, spaces, route, S, active, D, R = geometry
    ranks = set(range(10)) | {int(r) for label in ('T4', 'P4') for r in inputs['invoice'][label]}
    powers = {r: power_bounds(r) for r in ranks}
    linear = verify_linear(cert, xs, spaces, S, active, D, R, powers)
    clique = verify_cliques(xs, spaces, route, S, active, powers)
    tariff = verify_tariff(inputs['invoice'], linear, powers)
    result = {'status': 'PASS_SOURCE_LOCALISED_LINEAR_CODE_BUDGET', 'source_sha256': cert['source_pins']['source']['file_sha256'],
              'linear_certificate': linear, 'clique_exact_optimum': clique, 'complete_H4_tariff': tariff,
              'claim': 'Scoped linear one-encoder/one-decoder code exclusion with every packet transport leg newly paid; hybrid funded transit is excluded.',
              'new_complete_kappa': None}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if a.output:
        a.output.write_text(text)
    print(json.dumps({'status': result['status'], 'linear_price_lower': linear['lower_bound'],
                      'clique_optimum': clique['exact_fractional_and_integral_optimum'],
                      'deficit_lower': tariff['strict_deficit_per_native_lower']}, sort_keys=True))


if __name__ == '__main__':
    main()
