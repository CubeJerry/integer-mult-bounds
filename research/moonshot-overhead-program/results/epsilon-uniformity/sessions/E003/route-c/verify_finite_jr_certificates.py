#!/usr/bin/env python3
"""Replay finite JR upper certificates using integer arithmetic, without MILP."""
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def affine_certificate():
    record = json.loads((ROOT / 'affine-difference-q8-k2.json').read_text())
    t, k, q = record['t'], record['k'], record['q']
    n = q ** k
    target = {x for x in range(n) if all((x >> (t * i)) & (q - 1) for i in range(k))}
    parts = record['certificate']['affine_parts']
    covered = set()
    rows = [set() for _ in range(n)]
    left, right = [0] * n, [0] * n
    rectangle_count = nonproduct = 0
    for part in parts:
        direction, coset, representative = set(part['direction']), set(part['points']), part['representative']
        assert 0 in direction and direction
        assert len(direction) & (len(direction) - 1) == 0
        assert all(x ^ y in direction for x in direction for y in direction)
        assert coset == {representative ^ w for w in direction}
        assert coset <= target and not covered & coset
        covered.update(coset)
        seen = set()
        for u in range(n):
            if u in seen:
                continue
            source = {u ^ w for w in direction}
            dest = {x ^ representative for x in source}
            seen.update(source)
            rectangle_count += 1
            for x in source:
                assert not rows[x] & dest
                assert all(x ^ y in target for y in dest)
                rows[x].update(dest)
                left[x] += 1
            for y in dest:
                right[y] += 1
            for side in (source, dest):
                hull_size = 1
                for i in range(k):
                    hull_size *= len({(x >> (t * i)) & (q - 1) for x in side})
                nonproduct += hull_size != len(side)
    assert covered == target
    assert all(rows[x] == {y for y in range(n) if x ^ y in target} for x in range(n))
    assert set(left + right) == {len(parts)}
    assert rectangle_count == record['certificate']['rectangle_count']
    assert nonproduct == record['certificate']['nonproduct_rectangle_sides']
    return {'parts': len(parts), 'part_sizes': sorted(len(x['points']) for x in parts),
            'rectangles': rectangle_count, 'edges': sum(map(len, rows)),
            'maximum_source_load': max(left), 'maximum_destination_load': max(right),
            'nonproduct_sides': nonproduct}


def warm_certificate():
    record = json.loads((ROOT / 'c4-k3-warm-structured.json').read_text())
    words = list(product(range(4), repeat=3))
    rows, left, right = [set() for _ in words], [0] * len(words), [0] * len(words)
    certificate = record['certificate']
    for source_list, dest_list in certificate['rectangles']:
        source, dest = set(source_list), set(dest_list)
        assert len(source) == len(source_list) and len(dest) == len(dest_list)
        for side in (source, dest):
            projection = [{words[x][i] for x in side} for i in range(3)]
            assert len(side) == len(projection[0]) * len(projection[1]) * len(projection[2])
        for x in source:
            assert not rows[x] & dest
            assert all(all(a != b for a, b in zip(words[x], words[y])) for y in dest)
            rows[x].update(dest)
            left[x] += 1
        for y in dest:
            right[y] += 1
    for x, word in enumerate(words):
        assert rows[x] == {y for y, other in enumerate(words) if all(a != b for a, b in zip(word, other))}
    assert left == certificate['source_load'] and right == certificate['destination_load']
    assert max(left + right) == certificate['maximum_load'] == 6
    return {'rectangles': len(certificate['rectangles']), 'edges': sum(map(len, rows)),
            'maximum_load': 6, 'solver_status': record['solver_status'],
            'solver_bound_not_exactly_certified': record['solver_mip_bound']}


def main():
    inputs = ['affine-difference-q8-k2.json', 'c4-k3-warm-structured.json',
              'c4-k3-load5-experiment.json'] + [f'c4-k3-fixed-case{i}.json' for i in range(3)]
    inconclusive = []
    for name in inputs[2:]:
        record = json.loads((ROOT / name).read_text())
        assert record['certificate'] is None and record['solver_status'] == 1
        inconclusive.append({'file': name, 'status': record['solver_message'],
                             'time_limit_seconds': record['time_limit_seconds']})
    receipt = {'status': 'passed', 'affine_upper_certificate': affine_certificate(),
               'warm_upper_certificate': warm_certificate(), 'inconclusive_runs': inconclusive,
               'scope': 'Exact upper certificates only; no solver lower bound promoted to a mathematical obstruction.',
               'sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in inputs + ['FINITE-JR-EXPERIMENTS.md', Path(__file__).name]}}
    (ROOT / 'finite-jr-certificate-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
