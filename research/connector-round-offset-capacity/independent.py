#!/usr/bin/env python3
"""Independent literal execution of deterministic round-offset connectors.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
No imports from the primary constructor, verifier or proof; exact integers only.
Each listed finite domain is covered completely. Construction is deterministic,
without a search or seed. Checks include two-block concatenation and correction
boundaries before, after, between, and in a productive round. This does not by
itself prove an asymptotic theorem.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def construct(D, b, c, copies=1):
    need(all(type(x) is int for x in (D, b, c, copies)), 'integer parameters')
    need(D >= 1 and b >= 1 and copies >= 1, 'positive parameters')
    need(c >= D + 1 and copies * (D + 1) <= c, 'output call budget')
    need(D * ((1 << b) - 1) <= c, 'round budget')
    k = D * b
    total_sources = copies * k
    need(total_sources <= 10 and c <= 128, 'finite checker domain')
    rows = [list(range(k)) for _ in range(c)]
    for g in range(D):
        for subset in range(1, 1 << b):
            r = g * ((1 << b) - 1) + subset - 1
            chosen = [g * b + j for j in range(b) if subset & (1 << j)]
            rows[r] = chosen + [j for j in range(k) if j not in chosen]
    local_reads = {}
    chronology = Counter()
    for mask in range(1, 1 << k):
        productive, rounds = [], []
        for g in range(D):
            subset = (mask >> (g * b)) & ((1 << b) - 1)
            if subset:
                r = g * ((1 << b) - 1) + subset - 1
                rounds.append(r)
                productive.append(r * k + subset.bit_count())
        correction = (-sum(rounds)) % c
        if correction in rounds:
            chronology['same_round'] += 1
        elif correction < min(rounds):
            chronology['before_all'] += 1
        elif correction > max(rounds):
            chronology['after_all'] += 1
        else:
            chronology['between'] += 1
        local_reads[mask] = sorted(productive + [correction * k])
    word = [copy * k + axis for copy in range(copies) for row in rows for axis in row]
    reads = {}
    for mask in range(1, 1 << total_sources):
        times = []
        for copy in range(copies):
            local_mask = (mask >> (copy * k)) & ((1 << k) - 1)
            if local_mask:
                times.extend(copy * k * c + t for t in local_reads[local_mask])
        reads[str(mask)] = sorted(times)
    return dict(groups=D, width=b, characteristic=c, copies=copies,
                source_word=word, reads=reads, chronology=dict(chronology))


def execute(data, padding_boundary=0, padding_delta=0):
    D, b, c, copies = (data[key] for key in ('groups', 'width', 'characteristic', 'copies'))
    k = D * b * copies
    need(c >= D + 1 and copies * (D + 1) <= c, 'output call budget')
    word = data['source_word']
    need(all(type(j) is int and 0 <= j < k for j in word), 'source index')
    need(Counter(word) == Counter({j: c for j in range(k)}), 'source multiplicities')
    prefixes = [[0] * k]
    for j in word:
        row = prefixes[-1].copy()
        row[j] += 1
        prefixes.append(row)
    reads = {int(mask): times for mask, times in data['reads'].items()}
    need(set(reads) == set(range(1, 1 << k)), 'all output masks')
    buckets = [[] for _ in range(len(word) + 1)]
    for mask, times in reads.items():
        need(2 <= len(times) <= copies * (D + 1) and sorted(times) == times, 'read depth/chronology')
        need(all(type(t) is int and 0 <= t <= len(word) for t in times), 'actual boundary')
        need(all(sum(prefixes[t][j] for t in times) % c == ((mask >> j) & 1)
                 for j in range(k)), 'literal prefix-mask identity')
        for t in times + [padding_boundary] * (c - len(times) + padding_delta):
            buckets[t].append(mask)
    z = [1] + [0] * k
    outputs = {mask: [1] + [0] * (k + 1) for mask in reads}
    calls = Counter()
    for t, targets in enumerate(buckets):
        for mask in targets:
            calls['A', mask] += 1
            for j, value in enumerate(z):
                outputs[mask][j + 1] = (outputs[mask][j + 1] + value) % c
        if t < len(word):
            j = word[t]
            calls['B', j] += 1
            z[j + 1] = (z[j + 1] + 1) % c
    expected = Counter({('B', j): c for j in range(k)})
    expected.update({('A', mask): c for mask in reads})
    need(calls == expected, 'every complete call count')
    need(z == [1] + [0] * k, 'arbitrary dirty baseline restored')
    for mask, row in outputs.items():
        need(row == [1, 0] + [(mask >> j) & 1 for j in range(k)], 'full arbitrary-input action')
    return dict(groups=D, width=b, c=c, copies=copies, sources=k,
                masks=len(reads), calls=sum(calls.values()), chronology=data['chronology'])


def rejects(call):
    try:
        call()
    except ValueError:
        return 1
    raise RuntimeError('negative control accepted')


def controls(fixture):
    count = 0
    bad = deepcopy(fixture)
    bad['source_word'] = bad['source_word'][:-1]
    count += rejects(lambda: execute(bad))
    bad = deepcopy(fixture)
    bad['source_word'][0], bad['source_word'][1] = bad['source_word'][1], bad['source_word'][0]
    count += rejects(lambda: execute(bad))
    bad = deepcopy(fixture)
    del bad['reads']['1']
    count += rejects(lambda: execute(bad))
    bad = deepcopy(fixture)
    bad['reads']['1'][0] += 1
    count += rejects(lambda: execute(bad))
    bad = deepcopy(fixture)
    bad['reads']['1'][-1] += 1
    count += rejects(lambda: execute(bad))
    bad = deepcopy(fixture)
    bad['reads']['1'].append(len(bad['source_word']) + 1)
    count += rejects(lambda: execute(bad))
    count += rejects(lambda: execute(fixture, padding_boundary=1))
    count += rejects(lambda: execute(fixture, padding_delta=-1))
    return count


def main():
    domain = [(1, 3, 7, 1), (2, 2, 6, 1), (2, 3, 14, 1),
              (3, 1, 4, 1), (3, 2, 9, 1), (2, 2, 6, 2)]
    data = json.loads(Path(__file__).with_name('FIXTURES.json').read_text())
    need(data == [construct(*args) for args in domain], 'exact fixture regeneration')
    results = [execute(fixture) for fixture in data]
    negative = sum(controls(fixture) for fixture in data)
    negative += rejects(lambda: construct(3, 1, 3))
    negative += rejects(lambda: construct(2, 3, 13))
    negative += rejects(lambda: construct(2, 2, 6, 3))
    chronology = Counter()
    for fixture in data:
        chronology.update(fixture['chronology'])
    need(all(chronology[name] > 0 for name in ('before_all', 'after_all', 'same_round', 'between')),
         'all correction chronology cases')
    print('PASS_INDEPENDENT_ROUND_OFFSET ' + json.dumps(
        dict(fixtures=results, negative_controls=negative, chronology=dict(chronology)), sort_keys=True))


if __name__ == '__main__':
    main()
