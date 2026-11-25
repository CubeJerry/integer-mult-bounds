"""Exact finite checks for FR1--FR4; this is not a tape simulation."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def letter_rectangles(q):
    s = q.bit_length() - 1
    assert q == 1 << s
    result = []
    for bit in range(s):
        tail = 1 << (s - bit - 1)
        for prefix in range(1 << bit):
            start = prefix * 2 * tail
            left = tuple(range(start, start + tail))
            right = tuple(range(start + tail, start + 2 * tail))
            result.extend(((left, right), (right, left)))
    assert len(result) == 2 * (q - 1)
    return result


def predictor(L, k):
    value = Fraction(1)
    for r in range(1, L // 2 + 1):
        value *= 1 - Fraction(k, 2 * r)
    return value


def main():
    counts = Counter()
    receipts = []
    for L, q in ((2, 2), (2, 4), (2, 8), (2, 16),
                 (4, 2), (4, 4), (6, 2)):
        s = q.bit_length() - 1
        words = tuple(product(range(q), repeat=L))
        source_count = Counter()
        destination_count = Counter()
        covered = set()
        rects = letter_rectangles(q)
        rectangle_count = 0
        for k in range(1, L + 1, 2):
            assert predictor(L, k) != 0
            for unequal in combinations(range(L), k):
                unequal = set(unequal)
                equal = [i for i in range(L) if i not in unequal]
                for common in product(range(q), repeat=len(equal)):
                    fixed = dict(zip(equal, common))
                    for choices in product(rects, repeat=k):
                        slots = iter(choices)
                        factors = [(next(slots) if i in unequal
                                    else ((fixed[i],), (fixed[i],)))
                                   for i in range(L)]
                        left = tuple(product(*(factor[0] for factor in factors)))
                        right = tuple(product(*(factor[1] for factor in factors)))
                        rectangle_count += 1
                        source_count.update(left)
                        destination_count.update(right)
                        for v, w in product(left, right):
                            assert sum(a != b for a, b in zip(v, w)) == k
                            edge = (v, w)
                            assert edge not in covered
                            covered.add(edge)
        incidence = sum(comb(L, k) * s**k for k in range(1, L + 1, 2))
        expected_r = sum(comb(L, k) * q**(L-k) * (2*(q-1))**k
                         for k in range(1, L + 1, 2))
        assert expected_r == ((3*q-2)**L - (2-q)**L) // 2
        assert rectangle_count == expected_r
        assert set(source_count) == set(words) == set(destination_count)
        assert set(source_count.values()) == {incidence}
        assert set(destination_count.values()) == {incidence}
        assert 2 * rectangle_count <= 3**L * q**L
        assert incidence >= L * s**(L-1)
        degree = L // 2
        coefficients = []
        for j in range(degree + 1):
            coefficients.append(predictor(L, L-j) - sum(
                coefficients[i] * comb(j, i) for i in range(j)))
        charged_bound = sum(comb(L, j) * q**j for j in range(degree + 1))
        assert charged_bound <= 2**L * q**degree
        for k in range(L + 1):
            value = sum(coefficients[j] * comb(L-k, j)
                        for j in range(min(degree, L-k) + 1))
            assert value == predictor(L, k)
            assert (value != 0) == (k == 0 or k % 2 == 1)
            counts['predictor_values'] += 1
        for v, w in product(words, repeat=2):
            k = sum(a != b for a, b in zip(v, w))
            assert ((v, w) in covered) == (k % 2 == 1)
            value = predictor(L, k)
            free = -value if k % 2 else 0
            assert value + free == int(v == w)
            if k % 2:
                assert value - free != int(v == w)
                counts['wrong_free_sign_rejections'] += 1
            counts['label_pairs'] += 1
        assert (words[0], words[0]) not in covered
        counts['even_support_rejections'] += 1
        first_word = words[0]
        altered = dict(source_count)
        altered[first_word] -= 1
        assert set(altered.values()) != {incidence}
        counts['deleted_incidence_rejections'] += 1
        counts['cases'] += 1
        counts['rectangles'] += rectangle_count
        counts['covered_edges'] += len(covered)
        counts['regular_labels_both_sides'] += 2 * len(words)
        receipts.append({'L': L, 'q': q, 'labels': len(words),
                         'rectangles': rectangle_count,
                         'incidence_per_side': incidence,
                         'covered_edges': len(covered),
                         'charged_rectangle_majorant': charged_bound})
    path = Path(__file__).resolve()
    note = path.with_name('fourier-free-rectangle-counts.md')
    report = {'status': 'PASS_EXACT_FINITE_COUNTS', 'counts': dict(counts),
              'cases': receipts,
              'checker_sha256': sha256(path.read_bytes()).hexdigest(),
              'note_sha256': sha256(note.read_bytes()).hexdigest(),
              'scope': 'Exact finite source partitions and weights; not a physical rectangle-volume executor or an asymptotic proof.'}
    path.with_name('fourier-rectangle-counts-verification.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
