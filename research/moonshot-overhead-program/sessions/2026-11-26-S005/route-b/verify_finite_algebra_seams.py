#!/usr/bin/env python3
"""Fresh exact scalar and word checks; no historical-suite rerun."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
counts = Counter()


def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def power(a, n):
    out = 1
    for _ in range(n):
        out = mul(out, a)
    return out


def om(n):
    return power(2, n % 3)


def mm(a, b):
    out = [[0] * len(b[0]) for _ in a]
    for i, j, k in product(range(len(a)), range(len(b[0])), range(len(b))):
        out[i][j] ^= mul(a[i][k], b[k][j])
    return out


def word(*matrices):
    out = [[1, 0], [0, 1]]
    for matrix in matrices:
        out = mm(out, matrix)
    return out


I, Q, C, D = [[1, 0], [0, 1]], [[0, 1], [1, 0]], [[0, 1], [1, 1]], [[2, 0], [0, 3]]
Ci, Di = mm(C, C), mm(D, D)
S, T = word(D, C, D, C), word(Ci, Di, Ci, Di)
assert S == [[1, 1], [2, 3]] and T == [[3, 1], [2, 1]]
assert word(T, S) == word(S, T) == I
assert word(T, C, S) == D and word(T, Ci, S) == Di
assert word(C, D, Ci, Di, C, D) == Q
assert word(C, C, C) == word(D, D, D) == I
assert word(I, I, I, I, I, I) == I
counts['order_three_word_checks'] = 9

# Degree-four total-grade restriction, with noncommuting internal factors.
# Both the whole-row identity and the literal input-grade orientation are tested.
def smul(c, matrix):
    return [[mul(c, x) for x in row] for row in matrix]


for a_scalar, b_scalar in product((0, 1), (1, 2)):
    aa = [smul(a_scalar, C), D, mm(Ci, Di), I]
    bb = [smul(b_scalar, Q), C, mm(Q, Ci), I]
    factors = []
    for phase in range(4):
        fast = [[0] * 16 for _ in range(16)]
        lifted = [[0] * 16 for _ in range(16)]
        wrong = [[0] * 16 for _ in range(16)]
        for i, u, v in product(range(4), range(2), range(2)):
            col = 4 * i + 2 * u + v
            for out_u in range(2):
                row = 4 * ((i + 1) % 4) + 2 * out_u + v
                fast[row][col] ^= aa[i][out_u][u]
                wrong[row][col] ^= aa[i][out_u][u]
            for out_v in range(2):
                row = 4 * i + 2 * u + out_v
                fast[row][col] ^= bb[(phase - i) % 4][out_v][v]
                wrong[row][col] ^= bb[(phase + i) % 4][out_v][v]
        for i, j, u, v in product(range(4), range(4), range(2), range(2)):
            if (i + j) % 4 != phase:
                continue
            col = 4 * i + 2 * u + v
            for out_u in range(2):
                out_i = (i + 1) % 4
                assert (out_i + j) % 4 == (phase + 1) % 4
                lifted[4 * out_i + 2 * out_u + v][col] ^= aa[i][out_u][u]
            for out_v in range(2):
                out_j = (j + 1) % 4
                assert (i + out_j) % 4 == (phase + 1) % 4
                lifted[4 * i + 2 * u + out_v][col] ^= bb[j][out_v][v]
        assert fast == lifted
        counts['literal_total_grade_entries'] += 16 * 16
        counts['wrong_complement_negative_entries'] += sum(x != y for row, bad in zip(fast, wrong) for x, y in zip(row, bad))
        factors.append(fast)
    target = a_scalar ^ b_scalar
    for start in range(4):
        product_matrix = [[int(i == j) for j in range(16)] for i in range(16)]
        for step in range(4):
            product_matrix = mm(factors[(start + step) % 4], product_matrix)
        assert product_matrix == [[target if i == j else 0 for j in range(16)] for i in range(16)]
        counts['whole_cyclic_identity_columns'] += 16
assert counts['wrong_complement_negative_entries'] > 0

for k, beta, b in product(range(3), range(3), (1, 2)):
    indicator = 1 ^ mul(om(beta - b), om(k)) ^ mul(om(2 * (beta - b)), om(2 * k))
    assert indicator == int((k + beta) % 3 == b)
    counts['affine_indicator_cases'] += 1

directions, seeds = ((1, 0), (0, 1), (1, 1), (1, 2)), tuple(product(range(3), repeat=2))
for k in product(range(3), repeat=4):
    totals = [sum((k[j] + sum(a * t for a, t in zip(directions[j], seed))) % 3 for j in range(4)) for seed in seeds]
    assert sum(totals) == 36 and 3 * sum((c - 4) ** 2 for c in totals) == 72
    counts['pairwise_shift_moment_cases'] += 1
for c, offset, exponent in product(range(17), range(-7, 8), range(1, 5)):
    period, residue = 1 << exponent, (c - offset) % (1 << exponent)
    predictor = om(offset)
    for bit in range(exponent):
        predictor = mul(predictor, 1 ^ (power(3, 1 << bit) if (residue >> bit) & 1 else 0))
    assert predictor == om(offset + residue)
    gap = predictor ^ om(c)
    if offset <= c < offset + period:
        assert gap == 0
    elif gap == 0:
        counts['outside_window_zero_gaps'] += 1
    for datum in range(4):
        correction = mul(mul(gap, gap), mul(gap, datum))
        assert mul(gap, datum ^ correction) == 0
        counts['four_element_gap_repairs'] += 1
    counts['negative_offset_factored_predictors'] += 1
for exponent, w in product(range(6, 22), (1, 3, 1 << 100)):
    B, s0 = 3 ** exponent, 3 ** exponent // 32
    assert 75 * s0 >= 2 * B
    assert 32 * s0 * w + (B - 32 * s0) * w == B * w
    assert 16 * (2 * B * w) == 32 * B * w
    counts['coarse_module_padding_ledgers'] += 1

receipt = {'status': 'passed', 'utc': datetime.now(timezone.utc).isoformat(),
           'scope': 'fresh scalar, total-grade cyclic, spectral-word and integer-role controls only; no historical-suite rerun',
           'counts': dict(sorted(counts.items())),
           'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT / 'finite-algebra-seams-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
