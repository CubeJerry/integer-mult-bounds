#!/usr/bin/env python3
"""Exact finite checks of the optional classical-SCD round refinement.

Prepared for @CubeJerry with OpenAI Codex assistance; Apache-2.0.
Checks actual chain partitions, permutation prefixes, source words and all
formal output coefficients. verify_chains_independent.py provides independent replay.
"""
from collections import Counter
from copy import deepcopy
from math import comb
from pathlib import Path
import json
from chain_construct import chain_cover, connector
from chain_bounds import check_bounds


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check_cover(cover):
    b = cover['b']
    need(type(b) is int and 1 <= b <= 12, 'cover dimension')
    chains = cover['chains']; orders = cover['permutations']; loc = cover['locator']
    minimal = comb(b, b // 2)
    need(len(chains) == len(orders) == minimal, 'minimal chain count')
    need(len(loc) == 1 << b, 'locator coverage')
    members = Counter()
    for chain in chains:
        need(len(chain) > 0 and all(type(v) is int and 0 <= v < 1 << b for v in chain), 'chain members')
        need(chain[0].bit_count() + chain[-1].bit_count() == b, 'rank symmetry')
        for a, z in zip(chain, chain[1:]):
            need(a & z == a and (a ^ z).bit_count() == 1, 'saturated chain')
        members.update(chain)
    need(members == Counter({v: 1 for v in range(1 << b)}), 'Boolean lattice partition')
    prefix_rows = []
    for order in orders:
        need(all(type(j) is int for j in order) and sorted(order) == list(range(b)), 'maximal-chain permutation')
        prefix = [0]
        for j in order:
            prefix.append(prefix[-1] | (1 << j))
        prefix_rows.append(prefix)
    for subset, index in enumerate(loc):
        need(type(index) is int and 0 <= index < minimal, 'locator index')
        need(prefix_rows[index][subset.bit_count()] == subset, 'actual prefix locator')
    rank = max(1, b // 2)
    central = {row[rank] for row in prefix_rows}
    need(len(central) == comb(b, rank) == minimal, 'middle-rank lower-bound witnesses')
    return minimal


def check_word(fixture, pad_boundary=0, pad_delta=0):
    D, b, c, copies = (fixture[key] for key in ('groups', 'width', 'characteristic', 'copies'))
    k = D * b * copies
    need(c >= D + 1 and copies * (D + 1) <= c, 'read budget')
    need(D * comb(b, b // 2) <= c, 'chain-round budget')
    word = fixture['source_word']
    need(all(type(j) is int and 0 <= j < k for j in word), 'source labels')
    need(Counter(word) == Counter({j: c for j in range(k)}), 'complete source counts')
    rows = [[0] * k]
    for j in word:
        row = rows[-1].copy(); row[j] += 1; rows.append(row)
    reads = {int(mask): times for mask, times in fixture['reads'].items()}
    need(set(reads) == set(range(1, 1 << k)), 'all output masks')
    buckets = [[] for _ in range(len(word) + 1)]
    for mask, times in reads.items():
        need(2 <= len(times) <= copies * (D + 1) and times == sorted(times), 'ordered read budget')
        need(all(type(t) is int and 0 <= t <= len(word) for t in times), 'actual source boundary')
        need(all(sum(rows[t][j] for t in times) % c == ((mask >> j) & 1) for j in range(k)), 'literal prefix delivery')
        for t in times + [pad_boundary] * (c - len(times) + pad_delta): buckets[t].append(mask)
    z = [1] + [0] * k
    outputs = {m: [1] + [0] * (k + 1) for m in reads}
    calls = Counter()
    for t, targets in enumerate(buckets):
        for m in targets:
            calls['A', m] += 1
            for j, value in enumerate(z): outputs[m][j + 1] = (outputs[m][j + 1] + value) % c
        if t < len(word):
            j = word[t]; calls['B', j] += 1; z[j + 1] = (z[j + 1] + 1) % c
    expected = Counter({('B', j): c for j in range(k)})
    expected.update({('A', m): c for m in reads})
    need(calls == expected, 'complete call multiplicities')
    need(z == [1] + [0] * k, 'arbitrary dirty connector restored')
    for m, row in outputs.items(): need(row == [1, 0] + [(m >> j) & 1 for j in range(k)], 'full operator identity')
    return dict(groups=D, width=b, c=c, copies=copies, masks=len(reads), calls=sum(calls.values()))


def rejects(call):
    try:
        call()
    except ValueError:
        return 1
    raise RuntimeError('negative control accepted')


def main():
    path = Path(__file__).resolve().parent
    bundle = json.loads((path / 'CHAIN-COVERS.json').read_text())
    covers = bundle['covers']
    need(bundle['schema'] == 'symmetric-chain-prefix-cover-v1' and [x['b'] for x in covers] == list(range(1, 13)), 'cover inventory')
    need(covers == [chain_cover(b) for b in range(1, 13)], 'deterministic cover regeneration')
    counts = [check_cover(cover) for cover in covers]
    controls = 0
    for cover in covers:
        bad = deepcopy(cover); bad['permutations'][0].append(0)
        controls += rejects(lambda: check_cover(bad))
        bad = deepcopy(cover); bad['chains'][0][0] = bad['chains'][0][-1]
        controls += rejects(lambda: check_cover(bad))
        bad = deepcopy(cover); subset = (1 << max(1, cover['b'] // 2)) - 1
        bad['locator'][subset] = (bad['locator'][subset] + 1) % max(2, len(bad['permutations']))
        controls += rejects(lambda: check_cover(bad))
    fixtures = json.loads((path / 'CHAIN-FIXTURES.json').read_text())
    domain = [(1,3,3,1),(2,3,6,1),(3,2,6,1),(3,3,9,1),(2,3,6,2)]
    need(fixtures == [connector(covers[b-1], D, c, copies) for D,b,c,copies in domain], 'deterministic connector regeneration')
    results = [check_word(x) for x in fixtures]
    for fixture in fixtures:
        bad = deepcopy(fixture); bad['source_word'] = bad['source_word'][:-1]
        controls += rejects(lambda: check_word(bad))
        bad = deepcopy(fixture); bad['source_word'][0],bad['source_word'][1] = bad['source_word'][1],bad['source_word'][0]
        controls += rejects(lambda: check_word(bad))
        bad = deepcopy(fixture); bad['reads']['1'][0] += 1
        controls += rejects(lambda: check_word(bad))
        bad = deepcopy(fixture); del bad['reads']['1']
        controls += rejects(lambda: check_word(bad))
        controls += rejects(lambda: check_word(fixture, pad_boundary=1))
        controls += rejects(lambda: check_word(fixture, pad_delta=-1))
    controls += rejects(lambda: connector(covers[0],3,3))
    controls += rejects(lambda: connector(covers[2],2,5))
    controls += rejects(lambda: connector(covers[2],2,6,3))
    print('PASS_CHAIN_ROUND_REFINEMENT '+json.dumps(dict(
        dimensions=12, subsets=sum(1 << b for b in range(1,13)), minimal_chain_counts=counts,
        exact_bounds=check_bounds(),
        fixtures=results, negative_controls=controls),sort_keys=True))


if __name__ == '__main__': main()
