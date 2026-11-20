#!/usr/bin/env python3
"""Construct the minimum-width cross-phase mixers on every native D chart."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
from pathlib import Path


LAYOUT = ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
          '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
ROUTES = ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
          '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
MODULUS = 0x43
DEGREE = 6


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def payload(base, spec):
    raw = gzip.decompress((base / spec[0]).read_bytes())
    need(hashlib.sha256(raw).hexdigest() == spec[1], spec[0])
    return raw


def multiply(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 64:
            a ^= MODULUS
        b >>= 1
    return out


MUL = [[multiply(a, b) for b in range(64)] for a in range(64)]
INV = [0] + [MUL[a].index(1) for a in range(1, 64)]


def cauchy(row, col):
    return INV[row ^ (32 + col)]


@lru_cache(maxsize=16000)
def minor(rows, cols):
    """Cauchy determinant from its pairwise differences in characteristic two."""
    need(len(rows) == len(cols), 'non-square Cauchy minor')
    num = den = 1
    for group in (rows, cols):
        for a, b in itertools.combinations(group, 2):
            num = MUL[num][a ^ b]
    for row in rows:
        for col in cols:
            den = MUL[den][row ^ (32 + col)]
    need(num and den, 'colliding nodes in Cauchy determinant')
    return MUL[num][INV[den]]


def owner(route):
    return (53280 if route[0] == 'Y' else 0) + 480 * route[1] + route[2]


@lru_cache(maxsize=None)
def pure_add_count(n):
    """Literal binary Gauss-Jordan word length, on the polynomial basis."""
    rows = []
    for a in range(n):
        group = [0] * DEGREE
        for b in range(n):
            z = cauchy(a, b)
            for u in range(DEGREE):
                v = MUL[z][1 << u]
                for s in range(DEGREE):
                    if (v >> s) & 1:
                        group[s] |= 1 << (DEGREE * b + u)
        rows.extend(group)
    count = 0
    for pivot in range(len(rows)):
        source = next(j for j in range(pivot, len(rows)) if (rows[j] >> pivot) & 1)
        if pivot != source:
            rows[pivot], rows[source] = rows[source], rows[pivot]
            count += 3
        for j in range(len(rows)):
            if j != pivot and (rows[j] >> pivot) & 1:
                rows[j] ^= rows[pivot]
                count += 1
    need(rows == [1 << j for j in range(DEGREE*n)], 'pure inverse')
    return count


WEIGHT = [sum(MUL[z][1 << b].bit_count() for b in range(DEGREE)) for z in range(64)]


def selector(polys, rank):
    """Enumerate normalized nonzero weights; constant monomials never vanish."""
    if not rank:
        return (), 1
    attempts = 0
    for tail in itertools.product(range(1, 64), repeat=rank-1):
        w = (1,) + tail
        attempts += 1
        products = [1]
        for weight in w:
            products += [MUL[x][weight] for x in products]
        for terms in polys:
            value = 0
            for mask, coeff in terms:
                value ^= MUL[coeff][products[mask]]
            if not value:
                break
        else:
            return w, attempts
    raise ValueError('fixed Cauchy parameters admit no normalized diagonal weights')


def solve_chart(index, rows, planes, donors, receivers):
    rows = sorted(rows, key=owner)
    early = [row for row in rows if row[0] == 'X']
    late = [row for row in rows if row[0] == 'Y']
    m, n = len(early), len(late)

    def selected(group, role, pos):
        return tuple(s for s, row in enumerate(group)
                     if row[pos] is not None and role in planes[row[pos]])

    inputs = [(selected(early, j, 3), selected(late, j, 3)) for j in donors]
    outputs = [(selected(early, i, 5), selected(late, i, 5)) for i in receivers]
    need(all(len(e) + len(l) == 8 for e, l in inputs + outputs), 'eight-owner proper cut')
    deficits = Counter(len(ce) - len(re) for ce, cl in inputs for re, rl in outputs)
    rank = max(deficits)
    need(min(deficits) >= 0 and m+rank <= 32 and n+rank <= 32, 'causal cut and field sizes')
    subsets = {d: list(itertools.combinations(range(rank), d)) for d in deficits}
    polys = []
    for ce, cl in inputs:
        for re, rl in outputs:
            d = len(ce) - len(re)
            if d == 0 or d == rank:
                continue
            terms = []
            for sub in subsets[d]:
                left = minor(re + tuple(m+i for i in sub), ce)
                right = minor(rl, cl + tuple(n+i for i in sub))
                terms.append((sum(1 << i for i in sub), MUL[left][right]))
            polys.append(terms)
    weights, attempts = selector(polys, rank)
    before = sum(WEIGHT[cauchy(m+i, e)] for i in range(rank) for e in range(m))
    after = sum(WEIGHT[MUL[weights[i]][cauchy(l, n+i)]] for i in range(rank) for l in range(n))
    pure = pure_add_count(m) + pure_add_count(n)
    return ([index, m, n, list(weights)], deficits, attempts,
            {'pure_forward_ADD': pure, 'pure_inverse_ADD': pure,
             'snapshot_write_ADD': before, 'snapshot_read_ADD': after,
             'INIT': DEGREE*rank, 'dirty_CLEAR': DEGREE*rank})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    base = args.repo / 'research/moonshot-005-program/results'
    layout = json.loads(payload(base, LAYOUT))
    groups = defaultdict(list)
    for line in payload(base, ROUTES).splitlines():
        row = json.loads(line)
        if row[4] is not None:
            groups[row[4]].append(row)
    planes = [set(H) for H in layout['A2']]
    spaces = layout['D4']
    charts, ranks, delta, prices, trials = [], Counter(), Counter(), Counter(), Counter()
    for d in range(len(spaces)):
        donors = [j for j in spaces[d] if j < 111]
        receivers = [i for i in spaces[layout['dual_D4'][d]] if i < 111]
        word, ds, tries, counts = solve_chart(d, groups[d], planes, donors, receivers)
        charts.append(word)
        ranks[len(word[-1])] += 1
        delta.update(ds)
        prices.update(counts)
        trials[tries] += 1
    total_add = sum(v for k, v in prices.items() if k.endswith('_ADD'))
    need(len(charts) == 3150 and sum(delta.values()) == 388200, 'native coverage')
    need(sum(r*n for r,n in ranks.items()) == 4942, 'minimum storage census')
    word = json.dumps(charts, separators=(',', ':')).encode()
    summary = {'field_modulus': MODULUS, 'layout_payload': LAYOUT[1], 'route_payload': ROUTES[1],
               'chart_count': len(charts), 'native_donor_receiver_minors': sum(delta.values()),
               'deficit_histogram': dict(sorted(delta.items())), 'cache_rank_histogram': dict(sorted(ranks.items())),
               'total_cache_symbols_bank480': sum(r*n for r,n in ranks.items()),
               'maximum_selector_trials': max(trials), 'one_body': dict(prices) | {'total_ADD': total_add},
               'bank3840': {k: 8*v for k, v in dict(prices, total_ADD=total_add).items()},
               'extra_MOVE': 0, 'chart_list_sha256': hashlib.sha256(word).hexdigest(),
               'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'CHARTS.json.gz').write_bytes(gzip.compress(word, mtime=0))
    (args.out/'RESULT.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
