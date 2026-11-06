#!/usr/bin/env python3
# Prepared for @CubeJerry with substantial OpenAI Codex assistance; Apache-2.0.
"""Read literal fixtures only; no constructor imports or regeneration."""
from collections import Counter
from copy import deepcopy
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x):
    return type(x) is int


def check_cover(record):
    b = record['b']
    require(integer(b) and 1 <= b <= 12, 'cover dimension')
    permutations = record['permutations']
    chains = record['chains']
    locator = record['locator']
    expected = comb(b, b // 2)
    require(len(permutations) == len(chains) == expected, 'central layer count')
    require(len(locator) == 1 << b, 'locator extent')
    occurrences = Counter()
    prefixes = []
    for row, chain in zip(permutations, chains):
        require(len(row) == b and all(integer(j) for j in row)
                and sorted(row) == list(range(b)), 'literal permutation')
        state = 0
        states = [state]
        for j in row:
            state |= 1 << j
            states.append(state)
        prefixes.append(states)
        require(chain and all(integer(m) and 0 <= m < 1 << b for m in chain),
                'chain mask domain')
        require(chain[0].bit_count() + chain[-1].bit_count() == b,
                'symmetric chain endpoints')
        for left, right in zip(chain, chain[1:]):
            require(left & right == left and (left ^ right).bit_count() == 1,
                    'saturated chain step')
        for mask in chain:
            require(states[mask.bit_count()] == mask, 'chain prefix embedding')
            occurrences[mask] += 1
    require(occurrences == Counter({m: 1 for m in range(1 << b)}),
            'chain partition')
    for mask, index in enumerate(locator):
        require(integer(index) and 0 <= index < len(prefixes), 'locator index')
        require(prefixes[index][mask.bit_count()] == mask, 'literal located prefix')
    return {'b': b, 'permutations': expected, 'located_masks': len(locator),
            'prefixes': sum(map(len, prefixes))}


def check_fixture(record, padding_boundary=0):
    D, b, c, copies = [record[key] for key in
                       ['groups', 'width', 'characteristic', 'copies']]
    require(all(integer(v) and v >= 1 for v in [D, b, c, copies]), 'parameters')
    require(c >= 2 and c >= D + 1, 'dirty-read padding capacity')
    require(D * comb(b, b // 2) <= c, 'permutation round capacity')
    require(copies * (D + 1) <= c, 'concatenated read capacity')
    require(record['rounds_per_group'] == comb(b, b // 2), 'declared round count')
    k, n = D * b, copies * D * b
    word = record['source_word']
    require(len(word) == n * c, 'source extent')
    require(all(integer(j) and 0 <= j < n for j in word), 'source domain')
    require(Counter(word) == Counter({j: c for j in range(n)}), 'source counts')
    for block in range(copies):
        labels = list(range(block * k, (block + 1) * k))
        for round_index in range(c):
            left = block * k * c + round_index * k
            require(sorted(word[left:left + k]) == labels, 'literal full round')
    require(integer(padding_boundary) and 0 <= padding_boundary <= len(word),
            'padding boundary')
    raw_reads = record['reads']
    require(set(raw_reads) == {str(m) for m in range(1, 1 << n)}, 'mask inventory')
    buckets = [[] for _ in range(len(word) + 1)]
    for key, reads in raw_reads.items():
        mask = int(key)
        require(0 < len(reads) <= copies * (D + 1) <= c, 'read depth')
        require(all(integer(t) and 0 <= t <= len(word) for t in reads),
                'actual boundary domain')
        require(reads == sorted(reads), 'chronological reads')
        for t in reads:
            buckets[t].append(mask)
        buckets[padding_boundary].extend([mask] * (c - len(reads)))
    # Formal independent rows: z0 and each B_j x_j in z, and distinct y_m0,
    # A_m z0, A_m B_j x_j in output m. No A/B commutation is assumed.
    z = [1] + [0] * n
    outputs = {m: [1] + [0] * (n + 1) for m in range(1, 1 << n)}
    output_counts = Counter()
    source_counts = Counter()
    for t, masks in enumerate(buckets):
        for m in masks:
            output_counts[m] += 1
            row = outputs[m]
            for j, coefficient in enumerate(z):
                row[j + 1] = (row[j + 1] + coefficient) % c
        if t < len(word):
            j = word[t]
            source_counts[j] += 1
            z[j + 1] = (z[j + 1] + 1) % c
    require(source_counts == Counter({j: c for j in range(n)}), 'executed B counts')
    require(output_counts == Counter({m: c for m in outputs}), 'executed A counts')
    require(z == [1] + [0] * n, 'arbitrary connector restored')
    for m, row in outputs.items():
        require(row == [1, 0] + [(m >> j) & 1 for j in range(n)],
                'full arbitrary-input output action')
    return {'groups': D, 'width': b, 'characteristic': c, 'copies': copies,
            'sources': n, 'masks': len(outputs),
            'complete_calls': sum(source_counts.values()) + sum(output_counts.values()),
            'formal_output_coefficients': (n + 2) * len(outputs)}


def rejected(function, argument, **kwargs):
    try:
        function(argument, **kwargs)
    except ValueError:
        return 1
    raise RuntimeError('negative control accepted')


def cover_controls(record):
    count = 0
    bad = deepcopy(record)
    bad['permutations'][0][0] = record['b']
    count += rejected(check_cover, bad)
    bad = deepcopy(record)
    bad['locator'][1] = len(record['permutations'])
    count += rejected(check_cover, bad)
    bad = deepcopy(record)
    bad['chains'][0] = bad['chains'][0][1:]
    count += rejected(check_cover, bad)
    bad = deepcopy(record)
    bad['permutations'].pop()
    count += rejected(check_cover, bad)
    if len(record['permutations']) > 1:
        bad = deepcopy(record)
        # A valid permutation index that fails the chosen nonempty prefix.
        for mask in range(1, 1 << record['b']):
            chosen = record['locator'][mask]
            for index, row in enumerate(record['permutations']):
                prefix = sum(1 << j for j in row[:mask.bit_count()])
                if index != chosen and prefix != mask:
                    bad['locator'][mask] = index
                    count += rejected(check_cover, bad)
                    return count
        raise RuntimeError('semantic locator control unavailable')
    return count


def fixture_controls(record):
    count = 0
    for change in [
        lambda x: x['source_word'].pop(),
        lambda x: x['reads'].pop('1'),
        lambda x: x['reads']['1'].append(len(x['source_word']) + 1),
        lambda x: x.__setitem__('characteristic', x['groups']),
    ]:
        bad = deepcopy(record)
        change(bad)
        count += rejected(check_fixture, bad)
    # Shift one read to the next actual source boundary without changing counts.
    bad = deepcopy(record)
    for t_index, t in enumerate(bad['reads']['1']):
        if t < len(bad['source_word']):
            bad['reads']['1'][t_index] = t + 1
            bad['reads']['1'].sort()
            break
    else:
        raise RuntimeError('semantic shifted-read control unavailable')
    count += rejected(check_fixture, bad)
    # Preserve exactly c reads, but move baseline padding to a nonzero prefix.
    require(any(len(ts) < record['characteristic'] for ts in record['reads'].values()),
            'nonzero padding control unavailable')
    count += rejected(check_fixture, record, padding_boundary=1)
    return count


def main():
    root = Path(__file__).resolve().parent
    covers = json.loads((root / 'CHAIN-COVERS.json').read_text())
    require(covers['schema'] == 'symmetric-chain-prefix-cover-v1', 'cover schema')
    require([r['b'] for r in covers['covers']] == list(range(1, 13)), 'cover range')
    fixtures = json.loads((root / 'CHAIN-FIXTURES.json').read_text())
    require(len(fixtures) == 5, 'fixture range')
    result = {'status': 'PASS_INDEPENDENT_CHAIN_COVER_REFINEMENT',
              'covers': [check_cover(r) for r in covers['covers']],
              'fixtures': [check_fixture(r) for r in fixtures],
              'negative_controls': sum(cover_controls(r) for r in covers['covers'])
              + sum(fixture_controls(r) for r in fixtures)}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
