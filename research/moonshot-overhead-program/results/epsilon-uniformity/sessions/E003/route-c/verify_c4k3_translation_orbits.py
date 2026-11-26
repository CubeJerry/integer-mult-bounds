#!/usr/bin/env python3
"""Exact checks of the C(4,3) whole-translation-orbit obstruction."""
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def elements(mask):
    return [i for i in range(mask.bit_length()) if (mask >> i) & 1]


def translated(mask, h):
    return sum(1 << (x ^ h) for x in elements(mask))


def local_orbits():
    checked = 0
    profiles = set()
    for a in range(1, 16):
        for b in range(1, 16):
            if a & b:
                continue
            checked += 1
            stabilizer = [h for h in range(4) if translated(a, h) == a and translated(b, h) == b]
            orbit = {(translated(a, h), translated(b, h)) for h in range(4)}
            difference = {x ^ y for x in elements(a) for y in elements(b)}
            assert 0 not in difference
            counts = [[0] * 4 for _ in range(4)]
            source_load, dest_load = [0] * 4, [0] * 4
            for source, dest in orbit:
                for x in elements(source):
                    source_load[x] += 1
                    for y in elements(dest):
                        counts[x][y] += 1
                for y in elements(dest):
                    dest_load[y] += 1
            expected = [[int(x ^ y in difference) for y in range(4)] for x in range(4)]
            assert counts == expected
            la, lb = a.bit_count() // len(stabilizer), b.bit_count() // len(stabilizer)
            assert source_load == [la] * 4 and dest_load == [lb] * 4
            if len(difference) <= 2:
                assert la >= 1 and lb >= 1
                if len(difference) == 2:
                    u, v = sorted(difference)
                    subgroup = (1 << 0) | (1 << (u ^ v))
                    coset = sum(1 << x for x in difference)
                    assert subgroup & coset == 0
                    assert {x ^ y for x in elements(subgroup) for y in elements(coset)} == difference
            else:
                assert (la, lb) in [(1, 3), (3, 1)]
            profiles.add((a.bit_count(), b.bit_count(), len(difference), len(stabilizer), la, lb))
    assert checked == 50
    return {'local_pairs': checked, 'exact_profiles': sorted(profiles)}


def boxes():
    words = list(product(range(3), repeat=3))
    output = []
    for sides in product(range(1, 8), repeat=3):
        mask = sum(1 << j for j, w in enumerate(words) if all((s >> x) & 1 for s, x in zip(sides, w)))
        output.append((sides, mask, sum(s == 7 for s in sides)))
    return output


def volume_cases():
    all_boxes = boxes()
    by_full = [[(sides, mask) for sides, mask, full in all_boxes if full == d] for d in range(4)]
    assert list(map(len, by_full)) == [216, 108, 18, 1]
    eight = [mask for _, mask in by_full[0] if mask.bit_count() == 8]
    twelve = [mask for _, mask in by_full[1] if mask.bit_count() == 12]
    assert all(a & b for a, b in combinations(eight, 2))
    assert all(a & b for a, b in combinations(twelve, 2))
    pair_max = max(a.bit_count() + b.bit_count() for _, a in by_full[1]
                   for _, b in by_full[1] if not a & b)
    assert pair_max == 18
    checked = 0
    for _, box in by_full[1] + by_full[2]:
        allowed = [mask.bit_count() for _, mask in by_full[0] if not box & mask]
        checked += len(by_full[0])
        maximum = max(allowed, default=0)
        if box.bit_count() in (12, 18):
            assert maximum == 4
        if box.bit_count() == 9:
            assert maximum == 8
    maxima = {'one_two_full_size9': 9 + 2 * 8,
              'one_two_full_size18': 18 + 2 * 4,
              'two_one_full_boxes': pair_max + 8,
              'one_small_one_full': 6 + 2 * 8,
              'one_large_one_full': 12 + 2 * 4,
              'no_full_boxes': 8 + 4 * 4}
    assert all(value < 27 for value in maxima.values())
    # Enumerate all cost multisets permitted by (5,5), after normalizing
    # 1/2-letter coordinates. Their full-coordinate patterns must match
    # one of the six proof cases above.
    possible = [(0, 1, 1), (1, 1, 3), (1, 3, 1), (2, 3, 3)]
    budget_patterns = []
    for counts in product(range(6), repeat=len(possible)):
        ca = sum(c * a for c, (_, a, _) in zip(counts, possible))
        cb = sum(c * b for c, (_, _, b) in zip(counts, possible))
        if ca <= 5 and cb <= 5:
            assert counts[3] <= 1
            if counts[3]:
                assert counts[1] == counts[2] == 0 and counts[0] <= 2
            else:
                assert counts[1] <= 1 and counts[2] <= 1
                if counts[1] + counts[2] == 2:
                    assert counts[0] <= 1
                elif counts[1] + counts[2] == 1:
                    assert counts[0] <= 2
                else:
                    assert counts[0] <= 5
            budget_patterns.append(counts)
    return {'boxes': len(all_boxes), 'box_counts_by_full_coordinates': list(map(len, by_full)),
            'disjointness_pair_checks': checked,
            'budget_patterns': len(budget_patterns), 'case_volume_upper_bounds': maxima}


def witness():
    words = list(product(range(4), repeat=3))
    index = {w: i for i, w in enumerate(words)}
    def mask(fs):
        return sum(1 << index[w] for w in product(*fs))
    bases = [(mask(([1, 2, 3], [0], [0, 3])), mask(([0], [1, 2, 3], [1, 2]))),
             (mask(([1, 2, 3], [0], [0])), mask(([0], [1, 2, 3], [3])))]
    rectangles = set()
    for a, b in bases:
        for h in words:
            source = sum(1 << index[tuple(x ^ y for x, y in zip(words[j], h))] for j in elements(a))
            dest = sum(1 << index[tuple(x ^ y for x, y in zip(words[j], h))] for j in elements(b))
            rectangles.add((source, dest))
    assert len(rectangles) == 96
    covered, left, right = [0] * 64, [0] * 64, [0] * 64
    for source, dest in rectangles:
        for x in elements(source):
            assert covered[x] & dest == 0
            covered[x] |= dest
            left[x] += 1
        for y in elements(dest):
            right[y] += 1
    expected = [sum(1 << j for j, y in enumerate(words) if all(a != b for a, b in zip(x, y))) for x in words]
    assert covered == expected
    assert left == right == [6] * 64
    return {'rectangles': len(rectangles), 'edges': sum(row.bit_count() for row in covered),
            'source_load': 6, 'destination_load': 6}


def efficiency_shapes():
    local = [(a, b) for a in range(1, 4) for b in range(1, 4) if a + b <= 4]
    classes = set()
    for fs in product(local, repeat=3):
        a = b = 1
        for x, y in fs:
            a *= x
            b *= y
        if 3 * a * b > 8 * (a + b):
            classes.add(min(tuple(sorted(fs)), tuple(sorted((y, x) for x, y in fs))))
    assert classes == {((1, 3), (2, 2), (2, 2)),
                       ((1, 3), (2, 2), (3, 1)),
                       ((2, 2), (2, 2), (2, 2))}
    assert 8 * 640 < 3 * 1728
    return {'profiles_examined': len(local) ** 3, 'necessary_high_efficiency_shapes': sorted(classes)}


def main():
    receipt = {'status': 'passed', 'local_orbits': local_orbits(),
               'volume_case_checks': volume_cases(), 'sharp_witness': witness(),
               'broader_search_reduction': efficiency_shapes(),
               'scope': 'Exact optimum six only for whole simultaneous F2^2 translation orbits of product rectangles.',
               'sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ['C4K3-TRANSLATION-ORBIT-OBSTRUCTION.md', Path(__file__).name]}}
    (ROOT / 'c4k3-translation-orbit-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
