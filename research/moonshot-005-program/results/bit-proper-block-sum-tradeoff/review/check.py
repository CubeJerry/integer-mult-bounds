#!/usr/bin/env python3
"""Independent set-intersection census for the proper-block tradeoff."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path

SUPPORT = '012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963'


def independent_rank(vectors):
    # Reduced echelon rows, using low coordinates first (independent of the
    # author's high-pivot dictionary implementation).
    rows = list(vectors)
    pivot = 0
    for coordinate in range(9):
        hit = next((j for j in range(pivot, len(rows)) if rows[j] & (1 << coordinate)), None)
        if hit is None:
            continue
        rows[pivot], rows[hit] = rows[hit], rows[pivot]
        for j in range(pivot+1, len(rows)):
            if rows[j] & (1 << coordinate):
                rows[j] ^= rows[pivot]
        pivot += 1
    return pivot


def dot(x, y):
    return (x & y).bit_count() % 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--support', type=Path, required=True)
    parser.add_argument('--author', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    raw = args.support.read_bytes()
    assert sha256(raw).hexdigest() == SUPPORT
    words = json.loads(raw)['all_nonzero_words']
    proper = sorted(w['binary_code_mask'] for w in words if w['real_support_rank'] == 7)
    assert len(proper) == 25
    all_proper = (1 << 25) - 1
    orthogonal_sets = [sum(1 << j for j, y in enumerate(proper) if dot(x, y) == 0)
                       for x in proper]
    author = json.loads((args.author / 'output/CERTIFICATE.json').read_text())
    assert author['support_sha256'] == SUPPORT and author['proper_directions'] == proper

    @lru_cache(None)
    def kernel_proper_rank(mask):
        return independent_rank([p for j, p in enumerate(proper) if mask & (1 << j)])

    results = []
    for k, ceiling in [(3, 7), (4, 7), (5, 6), (6, 5)]:
        histogram = Counter()
        total = 0
        for selected in combinations(range(25), k):
            total += 1
            if independent_rank([proper[i] for i in selected]) != k:
                continue
            prefix = [all_proper]
            for i in selected:
                prefix.append(prefix[-1] & orthogonal_sets[i])
            suffix = [all_proper] * (k+1)
            for j in range(k-1, -1, -1):
                suffix[j] = suffix[j+1] & orthogonal_sets[selected[j]]
            singleton_count = sum(bool(prefix[j] & suffix[j+1] &
                                       (all_proper ^ orthogonal_sets[selected[j]]))
                                  for j in range(k))
            score = singleton_count + kernel_proper_rank(prefix[k])
            histogram[score] += 1
        assert total == comb(25, k)
        assert max(histogram) == ceiling
        target = next(c for c in author['subset_certificates']
                      if c['proper_decoder_subset_size'] == k)
        assert total == target['all_subsets']
        assert sum(histogram.values()) == target['independent_subsets']
        assert {str(r): n for r, n in histogram.items()} == target['histogram']
        witness = target['tight_completed_basis']
        decoder, payload = witness['decoder_basis'], witness['payload_basis']
        assert len(decoder) == len(payload) == 9
        assert independent_rank(decoder) == independent_rank(payload) == 9
        assert all(dot(x, y) == int(i == j) for i, x in enumerate(decoder)
                   for j, y in enumerate(payload))
        p = sum(x in proper for x in decoder)
        q = sum(x in proper for x in payload)
        assert p == witness['proper_decoders'] and q == witness['proper_payloads'] == ceiling
        assert p >= k
        results.append({'subset_size': k, 'all_subsets': total,
                        'independent_subsets': sum(histogram.values()),
                        'maximum_proper_opposite_blocks': ceiling,
                        'histogram': dict(sorted(histogram.items())),
                        'verified_witness': witness})
    allowed_counts = []
    for p in range(10):
        for q in range(10):
            if all((p < k or q <= maximum) and (q < k or p <= maximum)
                   for k, maximum in [(3, 7), (4, 7), (5, 6), (6, 5)]):
                assert p + q <= 11
                allowed_counts.append([p, q])
    assert any(r['verified_witness']['proper_decoders'] +
               r['verified_witness']['proper_payloads'] == 11 for r in results)
    result = {
        'status': 'PASS_INDEPENDENT_PROPER_BLOCK_SUM_BOUND',
        'support_sha256': SUPPORT,
        'author_file_sha256': {f: sha256((args.author / f).read_bytes()).hexdigest()
                               for f in ['PROOF.md', 'check.py', 'output/CERTIFICATE.json']},
        'method': 'Independent low-pivot elimination and bitset intersections of orthogonality sets; author checker not imported or executed.',
        'subset_censuses': results,
        'admissible_proper_block_count_pairs_from_tables': allowed_counts,
        'sharp_sum_bound': 11,
        'scope': 'b=1, exactly nine width-V receiver-downset events; arbitrary characteristic-two field and noncommuting vertex gauges; ground destinations allowed. No b>1 scaling or movement tariff.',
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])
    for r in results:
        print(r['subset_size'], r['all_subsets'], r['independent_subsets'],
              r['maximum_proper_opposite_blocks'])


if __name__ == '__main__':
    main()
