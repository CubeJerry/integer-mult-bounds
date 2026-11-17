#!/usr/bin/env python3
"""Independent short certificate for the proper decoder/dual coupling bound."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def rank(vectors):
    pivots = {}
    for original in vectors:
        v = original
        while v:
            k = v.bit_length() - 1
            if k in pivots:
                v ^= pivots[k]
            else:
                pivots[k] = v
                break
    return len(pivots)


def dot(a, b):
    return (a & b).bit_count() % 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--support', type=Path, required=True)
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    support = json.loads(a.support.read_text())
    words = support['all_nonzero_words']
    assert sorted(w['binary_code_mask'] for w in words) == list(range(1, 512))
    proper = sorted(w['binary_code_mask'] for w in words if w['real_support_rank'] == 7)
    assert len(proper) == 25
    assert all(w['real_support_rank'] in [7, 8] for w in words)
    certificate = []
    for triple in combinations(proper, 3):
        # Independent versus distinct matters in the dual-basis application.
        assert rank(triple) == 3
        annihilating = [v for v in proper if all(dot(v, u) == 0 for u in triple)]
        r = rank(annihilating)
        assert r <= 5
        certificate.append({'triple': triple, 'proper_common_annihilator': annihilating,
                            'common_annihilator_span_rank': r})
    assert len(certificate) == 2300
    author = json.loads((a.author / 'RESULT.json').read_text())
    basis = author['decoder_basis']
    dual = author['payload_basis']
    assert len(basis) == len(dual) == 9
    assert len(set(basis)) == 9 and all(x in proper for x in basis)
    assert rank(basis) == rank(dual) == 9
    assert all(dot(x, y) == int(i == j) for i, x in enumerate(basis)
               for j, y in enumerate(dual))
    actual_full = [u for u in dual if u not in proper]
    assert len(actual_full) == 7
    # Root's claimed full enumeration is not needed for the theorem. The short
    # certificate independently proves its minimum and the displayed attainment.
    author_triples = json.loads((a.author / 'TRIPLE-RANKS.json').read_text())
    hist = Counter(c['common_annihilator_span_rank'] for c in certificate)
    assert {str(k): v for k, v in hist.items()} == author_triples['zero_subspace_rank_histogram']
    assert author['minimum_full_span_payloads'] == len(actual_full)
    result = {
        'status': 'PASS',
        'support_certificate_sha256': sha256(a.support.read_bytes()).hexdigest(),
        'author_result_sha256': sha256((a.author / 'RESULT.json').read_bytes()).hexdigest(),
        'proper_direction_count': len(proper),
        'independent_proper_triples': len(certificate),
        'proper_common_annihilator_rank_histogram': dict(sorted(hist.items())),
        'universal_upper_bound_on_proper_duals': 2,
        'universal_lower_bound_on_full_span_duals': 7,
        'tight_decoder_basis': basis,
        'tight_payload_dual_basis': dual,
        'tight_full_span_payloads': actual_full,
        'tight_proper_payloads': [u for u in dual if u in proper],
        'scope': 'b=1; nine whole-record descent events, all nonzero proper-line destinations; arbitrary V and characteristic-two vertex gauges',
        'not_claimed': ['b>1 multiplication', 'Hub births', 'formation tariff',
                        'independent verification of all-nine-subset histogram'],
    }
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    (a.out / 'TRIPLE-CERTIFICATE.json').write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
