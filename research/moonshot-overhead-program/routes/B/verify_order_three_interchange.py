#!/usr/bin/env python3
"""Exact finite checks of characteristic-two order-three repair closure.

The toy has m=3, 27 shifts, two exceptional rows, phase fraction4/27.
All arithmetic is in F_256; its F_4 subfield supplies C,D. Predictors are
evaluated through direct converters, not routed matrix-root pencils.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np


def multiply_byte(a, b):
    out = 0
    for _ in range(8):
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 256:
            a ^= 0x11B
    return out


MUL = np.array([[multiply_byte(a, b) for b in range(256)] for a in range(256)], dtype=np.uint8)


def fpow(a, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = int(MUL[result, a])
        a = int(MUL[a, a])
        exponent //= 2
    return result


INV = np.array([0] + [fpow(a, 254) for a in range(1, 256)], dtype=np.uint8)
OMEGA = next(a for a in range(2, 256) if fpow(a, 3) == 1)
OMEGA2 = fpow(OMEGA, 2)
POW3 = np.array([1, OMEGA, OMEGA2], dtype=np.uint8)


def matmul(a, b):
    return np.bitwise_xor.reduce(MUL[a[:, :, None], b[None, :, :]], axis=1)


I2 = np.eye(2, dtype=np.uint8)
C = np.array([[0, 1], [1, 1]], dtype=np.uint8)
D = np.diag(np.array([OMEGA, OMEGA2], dtype=np.uint8))
Q = np.array([[0, 1], [1, 0]], dtype=np.uint8)
GATES = {'C': C, 'c': matmul(C, C), 'D': D, 'd': matmul(D, D)}


def word(w):
    out = I2.copy()
    for letter in w:
        out = matmul(out, GATES[letter])
    return out


M, W, N, S = 3, 27, 64, 2
INDEX = np.arange(N, dtype=np.int64)
LEFT, RIGHT = INDEX >> M, INDEX & ((1 << M) - 1)
SWAPS, LOW, HIGH, FIXED, K = [], [], [], [], []
for j in range(M):
    left, right = (LEFT >> j) & 1, (RIGHT >> j) & 1
    SWAPS.append(INDEX ^ ((left ^ right) << j) ^ ((left ^ right) << (M + j)))
    LOW.append(left < right)
    HIGH.append(left > right)
    FIXED.append(left == right)
    K.append(np.where(left == right, 0, np.where(left < right, 1, 2)))
K = np.array(K)
DELTA = POW3[np.sum(K, axis=0) % 3]
DELTAINV = INV[DELTA]
WHOLE_SWAP = (RIGHT << M) | LEFT
NODES = np.arange(1, W + 1, dtype=np.uint8)
H = np.vstack((np.ones(W, dtype=np.uint8), NODES))


def direct(x, sign=1, *, wrong_fixed=False):
    out = x.copy()
    for j in range(M):
        mask = HIGH[j] if sign == 1 else LOW[j]
        out = out[:, SWAPS[j]] ^ np.where(mask, out, 0).astype(np.uint8)
        if wrong_fixed:
            out[:, FIXED[j]] = 0
    return out


def direct_converter(x, inverse=False):
    if inverse:
        out = MUL[DELTA, direct(x, 1)]
        return MUL[DELTA, direct(out, 1)]
    out = direct(MUL[DELTAINV, x], -1)
    return direct(MUL[DELTAINV, out], -1)


PRED, ZVALUES, EXCEPTIONS = {}, {}, {}
for sign in (1, -1):
    zvalues = POW3[(sign * np.sum(K, axis=0)) % 3]
    prediction = np.empty((W, N), dtype=np.uint8)
    for beta in range(W):
        digits = np.array([(beta // (3 ** j)) % 3 for j in range(M)])
        counts = np.sum((sign * K + digits[:, None]) % 3, axis=0)
        scale = int(POW3[(1 - int(np.sum(digits))) % 3])
        for frequency, count in enumerate(counts):
            value = 0
            degree = int(count) - 1
            for power in range(5):
                coefficient = (comb(degree, power) if degree >= power else 0) if degree >= 0 else comb(-degree + power - 1, power)
                if coefficient & 1:
                    value ^= int(POW3[(2 * power) % 3])
            prediction[beta, frequency] = MUL[scale, value]
    j1 = np.sum(((-sign * K) % 3) * np.array([3 ** j for j in range(M)])[:, None], axis=0)
    j2 = np.sum(((2 - sign * K) % 3) * np.array([3 ** j for j in range(M)])[:, None], axis=0)
    assert all(set(np.flatnonzero(prediction[:, f] != zvalues[f])) == {int(j1[f]), int(j2[f])} for f in range(N))
    PRED[sign], ZVALUES[sign], EXCEPTIONS[sign] = prediction, zvalues, (j1, j2)


def predictor(x, sign):
    diagonal = np.tile(PRED[sign], (x.shape[0] // W, 1))
    return direct_converter(MUL[direct_converter(x), diagonal], inverse=True)


def gather(checks, copies, labels):
    assert copies % W == 0
    groups = copies // W
    out = checks.reshape(groups, W, labels, 4, N).transpose(0, 2, 1, 3, 4)
    return out.reshape(groups, labels, 4, W, N).transpose(0, 2, 1, 3, 4).reshape(-1, N)


def scatter(checks, copies, labels, wrong_label=False):
    groups = copies // W
    out = checks.reshape(groups, 4, labels, W, N).transpose(0, 2, 1, 3, 4)
    out = out.reshape(groups, labels, W, 4, N).transpose(0, 2, 1, 3, 4).reshape(copies, labels, 4, N)
    if wrong_label:
        out = np.roll(out, 1, axis=1)
    return out.reshape(-1, N)


def fresh_stats():
    return dict(internal_rows=0, internal_calls=0, terminal_rows=0, terminal_calls=0, events=[])


def transform(x, sign, depth, labels, stats, path='', fault=''):
    rows = len(x)
    if depth == 0:
        stats['terminal_rows'] += rows
        stats['terminal_calls'] += 1
        return direct(x, sign)
    assert rows % (W * labels * W ** depth) == 0
    groups, copies = rows // W, rows // (W * labels)
    stats['internal_rows'] += rows
    stats['internal_calls'] += 1
    events = stats['events']
    px = predictor(x, sign)
    checks = []
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        pair = (matmul(H, px[sl]), matmul(H, x[sl]))
        checks.extend(pair[::-1] if fault == 'check_order' else pair)
    forward = gather(np.vstack(checks), copies, labels)
    events.append((path, 'forward_1'))
    forward = transform(MUL[DELTAINV, forward], -1, depth - 1, labels, stats, path + 'a', fault)
    events.append((path, 'forward_2'))
    if fault != 'omit_diagonal':
        forward = MUL[DELTAINV, forward]
    forward = transform(forward, -1, depth - 1, labels, stats, path + 'b', fault)
    spectral = scatter(forward, copies, labels)
    events.append((path, 'table'))
    z = ZVALUES[sign]
    j1, j2 = EXCEPTIONS[sign]
    n1, n2 = NODES[j1], NODES[j2]
    inverse_difference = INV[n1 ^ n2]
    p1, p2 = PRED[sign][j1, INDEX], PRED[sign][j2, INDEX]
    d1, d2 = MUL[p1 ^ z, p1 ^ z], MUL[p2 ^ z, p2 ^ z]
    table_rows = []
    for group in range(groups):
        hp, hx = spectral[group * 4:group * 4 + 2], spectral[group * 4 + 2:group * 4 + 4]
        he = hp ^ MUL[z, hx]
        e1 = MUL[MUL[n2, he[0]] ^ he[1], inverse_difference]
        e2 = MUL[he[1] ^ MUL[n1, he[0]], inverse_difference]
        t1, t2 = MUL[d1, e1], MUL[d2, e2]
        a1 = MUL[t2 ^ t1, inverse_difference]
        a0 = t1 ^ MUL[n1, a1]
        a = np.vstack((a0, a1))
        table_rows.extend((a, MUL[z, a]))
    inverse = gather(np.vstack(table_rows), copies, labels)
    events.append((path, 'inverse_1'))
    inverse = transform(inverse, 1, depth - 1, labels, stats, path + 'c', fault)
    inverse = MUL[DELTA, inverse]
    events.append((path, 'inverse_2'))
    inverse = transform(inverse, 1, depth - 1, labels, stats, path + 'd', fault)
    ordinary = scatter(MUL[DELTA, inverse], copies, labels, fault == 'label_return')
    lift_z, lift_fz = np.empty_like(x), np.empty_like(x)
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        lift_z[sl] = matmul(H.T, ordinary[group * 4:group * 4 + 2])
        lift_fz[sl] = matmul(H.T, ordinary[group * 4 + 2:group * 4 + 4])
    events.append((path, 'finish'))
    return px if fault == 'omit_repair' else px ^ predictor(lift_z, sign) ^ lift_fz


def polynomial_remainder(a, modulus):
    while a.bit_length() >= modulus.bit_length():
        a ^= modulus << (a.bit_length() - modulus.bit_length())
    return a


def polynomial_gcd(a, b):
    while b:
        a, b = b, polynomial_remainder(a, b)
    return a


def check_root_differences():
    cases = 0
    for exponent in (1, 2, 3):
        third = 3 ** (exponent - 1)
        modulus = (1 << (2 * third)) | (1 << third) | 1
        powers = [polynomial_remainder(1 << j, modulus) for j in range(3 * third)]
        assert polynomial_remainder((1 << (3 * third)) ^ 1, modulus) == 0
        for i in range(len(powers)):
            for j in range(i):
                assert polynomial_gcd(powers[i] ^ powers[j], modulus) == 1
                cases += 1
    return cases


def check_events(events):
    expected = ['forward_1', 'forward_2', 'table', 'inverse_1', 'inverse_2', 'finish']
    by_path = {}
    for path, event in events:
        by_path.setdefault(path, []).append(event)
    assert all(sequence == expected for sequence in by_path.values())


def swap_program(x, depth, labels, stats):
    out = transform(MUL[DELTA, x], 1, depth, labels, stats, 'q0')
    out = transform(MUL[DELTAINV, out], -1, depth, labels, stats, 'q1')
    return transform(MUL[DELTA, out], 1, depth, labels, stats, 'q2')


def run():
    rng = np.random.default_rng(202611251451)
    tests = []
    assert all(int(MUL[a, INV[a]]) == 1 for a in range(1, 256))
    assert np.array_equal(word('CCC'), I2) and np.array_equal(word('DDD'), I2)
    s, t = word('DCDC'), word('cdcd')
    assert np.array_equal(matmul(s, t), I2)
    assert np.array_equal(matmul(matmul(t, C), s), D)
    assert np.array_equal(word('CDcdCD'), Q)
    tests.append(dict(name='exact_F4_group_words', omega=OMEGA, passed=True))
    tests.append(dict(name='three_power_cyclotomic_unit_differences', cases=check_root_differences(), passed=True))
    basis = np.eye(N, dtype=np.uint8)
    assert np.array_equal(direct(direct(direct(basis))), basis)
    assert np.array_equal(direct_converter(direct_converter(basis), True), basis)
    for sign in (1, -1):
        actual = direct_converter(direct(direct_converter(basis, True), sign))
        assert np.array_equal(actual, MUL[ZVALUES[sign], basis])
    assert np.array_equal(swap_program(basis, 0, 1, fresh_stats()), basis[:, WHOLE_SWAP])
    tests.append(dict(name='all_basis_physical_field_orbits', basis_rows=N,
                      equal_field_addresses=int(np.count_nonzero(LEFT == RIGHT)), passed=True))
    x = rng.integers(0, 256, size=(3, N), dtype=np.uint8)
    matrices = rng.integers(0, 256, size=(2 * M + 1, 3, 3), dtype=np.uint8)
    lhs = matmul(matrices[0], x)
    rhs = lhs.copy()
    for j in range(M):
        first, second = matrices[2 * j + 1], matrices[2 * j + 2]
        lower = np.where(HIGH[j], x, 0).astype(np.uint8)
        upper = np.where(LOW[j], x, 0).astype(np.uint8)
        lhs ^= matmul(first, x[:, SWAPS[j]] ^ lower) ^ matmul(second, x[:, SWAPS[j]] ^ upper)
        rhs ^= matmul(first ^ second, x[:, SWAPS[j]]) ^ matmul(first, lower) ^ matmul(second, upper)
    assert np.array_equal(lhs, rhs)
    tests.append(dict(name='one_shared_swap_pencil_identity', passed=True))
    tests.append(dict(name='all_shift_frequency_predictions', cases=2 * W * N,
                      exception_rows_per_frequency=2, passed=True))
    for sign in (1, -1):
        squared = MUL[PRED[sign], PRED[sign]]
        assert np.array_equal(MUL[squared, squared], PRED[sign])
    tests.append(dict(name='four_element_predictor_P4_equals_P', predictor_applications_per_repair=2, passed=True))
    ids = np.repeat(np.arange(W * 3 * 4, dtype=np.int64)[:, None], N, axis=1)
    grouped = gather(ids, W, 3)
    assert np.array_equal(scatter(grouped, W, 3), ids)
    assert all(int(grouped[row, 0]) // 4 % 3 == row // W % 3 for row in range(len(grouped)))
    tests.append(dict(name='three_label_gather_scatter', rows=len(ids), passed=True))
    for sign, depth, labels in ((1, 1, 2), (-1, 1, 2), (1, 2, 1), (-1, 2, 1)):
        rows = W * labels * W ** depth
        x = rng.integers(0, 256, size=(rows, N), dtype=np.uint8)
        stats = fresh_stats()
        actual = transform(x, sign, depth, labels, stats)
        assert np.array_equal(actual, direct(x, sign))
        ratio = Fraction(16, W)
        assert stats['terminal_rows'] == rows * ratio ** depth
        assert stats['internal_rows'] == rows * sum((ratio ** d for d in range(depth)), Fraction())
        assert stats['terminal_calls'] == 4 ** depth
        check_events(stats['events'])
        events = len(stats.pop('events'))
        tests.append(dict(name='full_rate_order_three_repair', sign=sign, depth=depth,
                          labels=labels, rows=rows, entries=rows * N,
                          event_count=events, statistics=stats, passed=True))
    x = rng.integers(0, 256, size=(W * 2 * W, N), dtype=np.uint8)
    stats = fresh_stats()
    swapped = swap_program(x, 1, 2, stats)
    assert np.array_equal(swapped, x[:, WHOLE_SWAP])
    check_events(stats['events'])
    tests.append(dict(name='full_rate_final_swap_word', rows=len(x), entries=x.size,
                      full_transform_factors=3, passed=True))
    negatives = {}
    negatives['wrong_group_word'] = int(np.count_nonzero(word('CDcCD') != Q))
    negatives['omitted_equal_field_identity'] = int(np.count_nonzero(direct(basis, wrong_fixed=True) != direct(basis)))
    for fault in ('check_order', 'omit_diagonal', 'label_return', 'omit_repair'):
        wrong = transform(x, 1, 1, 2, fresh_stats(), fault=fault)
        negatives[fault] = int(np.count_nonzero(wrong != direct(x)))
    assert all(value > 0 for value in negatives.values())
    bad_order = [('', e) for e in ('forward_1', 'forward_2', 'inverse_1', 'table', 'inverse_2', 'finish')]
    try:
        check_events(bad_order)
    except AssertionError:
        phase_rejected = True
    else:
        raise AssertionError('wrong dependency order accepted')
    tests.append(dict(name='negative_controls', mismatches=negatives,
                      inverse_before_table_rejected=phase_rejected, passed=True))
    for depth in range(16):
        assert sum((Fraction(1, 4) ** j for j in range(depth)), Fraction()) == Fraction(4, 3) * (1 - Fraction(1, 4) ** depth)
    tests.append(dict(name='proof_four_children_one_sixteenth_ledger', depths=16, passed=True))
    return dict(status='exact finite checks passed', field_size=256, query_order=3,
                toy_phase_fraction='4/27', proof_phase_fraction='1/16',
                physical_routing_or_generic_module_verified=False, tests=tests)


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('order-three-interchange-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
