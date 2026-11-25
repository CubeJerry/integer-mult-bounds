#!/usr/bin/env python3
"""Exact checks of the finite half-angle interchange family.

Checks cyclotomic F_p-algebras, actual address swaps, and Hermite unrolling
with changing targets. The toy repair has m=4, W=16, s=2: phase fraction
1/4. Predictors use direct spectral transforms, so this checks algebra and
composition, not routing/tape time. The Hermite algebra is adapted from the
recovered batch-contraction verifier; targets and diagonalizers are new.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb, isqrt
from pathlib import Path

import numpy as np


class Cyclotomic:
    """F_p[y]/(y^d+1); the ring need not be a field."""

    def __init__(self, prime: int, degree: int):
        self.p, self.d = prime, degree
        self.zero = (0,) * degree
        self.one = (1,) + (0,) * (degree - 1)
        self.y = (0, 1) + (0,) * (degree - 2)

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def scale(self, a, scalar):
        return tuple(x * scalar % self.p for x in a)

    def sub(self, a, b):
        return self.add(a, self.scale(b, -1))

    def mul(self, a, b):
        out = [0] * self.d
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                degree = i + j
                out[degree % self.d] += x * y * (-1 if degree >= self.d else 1)
        return tuple(x % self.p for x in out)

    def power(self, a, exponent):
        result = self.one
        while exponent:
            if exponent & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            exponent //= 2
        return result


def check_ring_relations() -> int:
    cases = 0
    for prime in (3, 5, 7, 11, 17):
        for depth in (1, 2, 3):
            order = 1 << (depth + 2)
            ring = Cyclotomic(prime, order // 2)
            imaginary = ring.power(ring.y, order // 4)
            inv_imaginary = ring.scale(imaginary, -1)
            inv2 = pow(2, -1, prime)
            coeff = []
            for level in range(depth + 1):
                power = 1 << (depth - level)
                z = ring.power(ring.y, power)
                iz = ring.power(ring.y, order - power)
                a = ring.scale(ring.mul(ring.sub(z, iz), inv_imaginary), inv2)
                b = ring.scale(ring.add(z, iz), inv2)
                assert ring.add(ring.mul(a, a), ring.mul(b, b)) == ring.one
                coeff.append((a, b))
                cases += 1
            assert coeff[0] == (ring.one, ring.zero)
            for level in range(depth):
                a, b = coeff[level]
                c, d = coeff[level + 1]
                assert ring.scale(ring.mul(c, d), 2) == a
                assert ring.sub(ring.mul(d, d), ring.mul(c, c)) == b
                first = ring.add(ring.mul(d, b), ring.mul(c, a))
                second = ring.sub(ring.mul(d, a), ring.mul(c, b))
                assert ring.add(ring.mul(first, d), ring.mul(second, c)) == ring.one
                assert ring.sub(ring.mul(first, c), ring.mul(second, d)) == ring.zero
                cases += 1
    return cases


P, M, W, S, B, MAX_LEVEL = 257, 4, 16, 2, 4, 4
N = 1 << (2 * M)
INV2 = pow(2, -1, P)
GENERATOR = next(g for g in range(2, P) if pow(g, (P - 1) // 2, P) != 1)
ROOT_ORDER = 1 << (MAX_LEVEL + 2)
ROOT = pow(GENERATOR, (P - 1) // ROOT_ORDER, P)
IMAGINARY = pow(ROOT, ROOT_ORDER // 4, P)
COEFF = []
for level in range(MAX_LEVEL + 1):
    z = pow(ROOT, 1 << (MAX_LEVEL - level), P)
    iz = pow(z, -1, P)
    COEFF.append(((z - iz) * INV2 * pow(IMAGINARY, -1, P) % P,
                  (z + iz) * INV2 % P))

INDEX = np.arange(N, dtype=np.int64)
LEFT, RIGHT = INDEX >> M, INDEX & (W - 1)
K = LEFT & (RIGHT ^ (W - 1))
PARITY = np.array([1 if x.bit_count() % 2 == 0 else -1 for x in range(W)], dtype=np.int64)
SIGN = PARITY[K] % P
SWAPS, ORIENTATIONS, FIXED = [], [], []
for j in range(M):
    left, right = (LEFT >> j) & 1, (RIGHT >> j) & 1
    SWAPS.append(INDEX ^ ((left ^ right) << j) ^ ((left ^ right) << (M + j)))
    ORIENTATIONS.append(right - left)
    FIXED.append((left == right).astype(np.int64))
WHOLE_SWAP = (RIGHT << M) | LEFT
H = np.vstack((np.ones(W, dtype=np.int64), np.arange(1, W + 1, dtype=np.int64)))
PRED = np.empty((W, N), dtype=np.int64)
for beta in range(W):
    counts = np.array([(int(k) ^ beta).bit_count() for k in K], dtype=np.int64)
    PRED[beta] = PARITY[beta] * (1 - 2 * (counts - 2) ** 2) % P
NODE1, NODE2 = K + 1, (K ^ (W - 1)) + 1
INVDIFF = np.array([pow(int(x) % P, -1, P) for x in NODE2 - NODE1], dtype=np.int64)


def query(x: np.ndarray, level: int, j: int, *, drop_fixed: bool = False) -> np.ndarray:
    a, b = COEFF[level]
    result = a * x[:, SWAPS[j]] + b * x * ORIENTATIONS[j]
    if not drop_fixed:
        result += (1 - a) * x * FIXED[j]
    return result % P


def family(x: np.ndarray, level: int, *, drop_fixed: bool = False) -> np.ndarray:
    result = x.copy()
    for j in range(M):
        result = query(result, level, j, drop_fixed=drop_fixed)
    return result


def predictor(x: np.ndarray, level: int) -> np.ndarray:
    diagonal = np.tile(PRED, (x.shape[0] // W, 1))
    return family(family(x, level + 1) * diagonal % P, level + 1)


def gather(checks: np.ndarray, copies: int, labels: int) -> np.ndarray:
    """Combine B successive parent copies, preserving the routing label."""
    assert copies % B == 0
    return checks.reshape(copies // B, B, labels, 2 * S, N).transpose(0, 2, 1, 3, 4).reshape(-1, N)


def scatter(checks: np.ndarray, copies: int, labels: int, wrong_label: bool) -> np.ndarray:
    restored = checks.reshape(copies // B, labels, B, 2 * S, N).transpose(0, 2, 1, 3, 4).reshape(copies, labels, 2 * S, N)
    if wrong_label:
        restored = np.roll(restored, 1, axis=1)
    return restored.reshape(-1, N)


def transform(x: np.ndarray, level: int, depth: int, labels: int,
              stats: dict, path: str = '', *, fault: str = '') -> np.ndarray:
    rows = x.shape[0]
    if depth == 0:
        stats['terminal_rows'] += rows
        stats['terminal_calls'] += 1
        return family(x, level)
    assert rows % (W * labels * B ** depth) == 0
    groups, copies = rows // W, rows // (W * labels)
    stats['internal_rows'] += rows
    stats['internal_calls'] += 1
    events = stats['events']
    px = predictor(x, level)
    checks = []
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        pair = (H @ px[sl] % P, H @ x[sl] % P)
        checks.extend(pair[::-1] if fault == 'check_order' else pair)
    events.append((path, 'forward_start'))
    child_level = level if fault == 'same_target' else level + 1
    spectral = transform(gather(np.vstack(checks), copies, labels), child_level,
                         depth - 1, labels, stats, path + 'f', fault=fault)
    spectral = scatter(spectral, copies, labels, False)
    events.append((path, 'forward_done'))
    table_rows = []
    for group in range(groups):
        hp, hx = spectral[group * 4:group * 4 + 2], spectral[group * 4 + 2:group * 4 + 4]
        he = (hp - SIGN * hx) % P
        e1 = (NODE2 * he[0] - he[1]) * INVDIFF % P
        e2 = (he[1] - NODE1 * he[0]) * INVDIFF % P
        t1, t2 = 5 * INV2 * SIGN * e1 % P, 5 * INV2 * SIGN * e2 % P
        a1 = (t2 - t1) * INVDIFF % P
        a0 = (t1 - NODE1 * a1) % P
        a = np.vstack((a0, a1))
        table_rows.extend((a, a * SIGN % P))
    events.append((path, 'table'))
    events.append((path, 'inverse_start'))
    ordinary = transform(gather(np.vstack(table_rows), copies, labels), child_level,
                         depth - 1, labels, stats, path + 'i', fault=fault)
    ordinary = scatter(ordinary, copies, labels, fault == 'label_return')
    events.append((path, 'inverse_done'))
    lift_z, lift_fz = np.empty_like(x), np.empty_like(x)
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        lift_z[sl] = H.T @ ordinary[group * 4:group * 4 + 2] % P
        lift_fz[sl] = H.T @ ordinary[group * 4 + 2:group * 4 + 4] % P
    gp = (3 * px - predictor(predictor(px, level), level)) * INV2 % P
    events.append((path, 'finish'))
    return gp if fault == 'omit_repair' else (gp - predictor(lift_z, level) + lift_fz) % P


def new_stats() -> dict:
    return dict(terminal_rows=0, terminal_calls=0, internal_rows=0, internal_calls=0, events=[])


def check_events(events: list) -> None:
    expected = ['forward_start', 'forward_done', 'table', 'inverse_start', 'inverse_done', 'finish']
    by_path: dict[str, list[str]] = {}
    for path, event in events:
        by_path.setdefault(path, []).append(event)
    assert all(sequence == expected for sequence in by_path.values())


def run() -> dict:
    rng = np.random.default_rng(202611251417)
    tests = []
    tests.append(dict(name='cyclotomic_ring_half_angle_identities',
                      primes=[3, 5, 7, 11, 17], cases=check_ring_relations(), passed=True))
    basis = np.eye(N, dtype=np.int64)
    assert np.array_equal(family(basis, 0), basis[:, WHOLE_SWAP])
    local_cases = 0
    for level in range(MAX_LEVEL + 1):
        assert np.array_equal(family(family(basis, level), level), basis)
        for j in range(M):
            assert np.array_equal(query(query(basis, level, j), level, j), basis)
            if level < MAX_LEVEL:
                actual = query(query(query(basis, level + 1, j), level, j), level + 1, j)
                expected = basis * (ORIENTATIONS[j] + FIXED[j]) % P
                assert np.array_equal(actual, expected)
                local_cases += N
        if level < MAX_LEVEL:
            actual = family(family(family(basis, level + 1), level), level + 1)
            assert np.array_equal(actual, basis * SIGN % P)
    tests.append(dict(name='all_basis_query_and_family_closure',
                      local_basis_cases=local_cases, equal_field_addresses=int(np.count_nonzero(LEFT == RIGHT)), passed=True))
    x = rng.integers(0, P, size=(3, N), dtype=np.int64)
    matrices = rng.integers(0, P, size=(M + 1, 3, 3), dtype=np.int64)
    for level in range(MAX_LEVEL + 1):
        a, b = COEFF[level]
        lhs = matrices[0] @ x % P
        rhs = lhs.copy()
        for j in range(M):
            lhs = (lhs + matrices[j + 1] @ query(x, level, j)) % P
            diagonal = b * ORIENTATIONS[j] + (1 - a) * FIXED[j]
            rhs = (rhs + a * (matrices[j + 1] @ x[:, SWAPS[j]])
                   + matrices[j + 1] @ (x * diagonal)) % P
        assert np.array_equal(lhs, rhs)
    tests.append(dict(name='shared_pencil_plus_ordinary_diagonal_identity', levels=MAX_LEVEL + 1, passed=True))

    for m in range(4, 513):
        bound = isqrt(2 * m)
        if bound * bound < 2 * m:
            bound += 1
        low, high = m // 2 - bound, (m + 1) // 2 + bound
        tail = sum(comb(m, c) for c in range(m + 1) if not low <= c <= high)
        assert 16 * tail < 1 << m
    tests.append(dict(name='exact_constant_tail_counts', cases=509, passed=True))

    labels, copies = 3, 16
    ids = np.repeat(np.arange(copies * labels * 2 * S)[:, None], N, axis=1)
    grouped = gather(ids, copies, labels)
    for row in range(len(grouped)):
        assert int(grouped[row, 0]) // (2 * S) % labels == row // W % labels
    assert np.array_equal(scatter(grouped, copies, labels, False), ids)
    assert not np.array_equal(scatter(grouped, copies, labels, True), ids)
    tests.append(dict(name='label_preserving_gather_scatter', labels=labels, rows=len(ids),
                      wrong_return_rejected=True, passed=True))

    for start_level, depth, labels in ((0, 1, 2), (0, 2, 2), (1, 2, 2), (0, 2, 3)):
        rows = W * labels * B ** depth
        x = rng.integers(0, P, size=(rows, N), dtype=np.int64)
        stats = new_stats()
        actual = transform(x, start_level, depth, labels, stats)
        assert np.array_equal(actual, family(x, start_level))
        assert stats['terminal_rows'] == rows * Fraction(2, B) ** depth
        assert stats['internal_rows'] == rows * sum((Fraction(2, B) ** d for d in range(depth)), Fraction())
        assert stats['terminal_calls'] == 2 ** depth
        check_events(stats['events'])
        events = stats.pop('events')
        tests.append(dict(name='changing_target_full_rate_repair', start_level=start_level,
                          depth=depth, labels=labels, rows=rows, entries=rows * N,
                          event_count=len(events), statistics=stats, passed=True))

    negatives = {}
    wrong = family(family(family(basis, 2), 0), 2)
    negatives['wrong_half_angle'] = int(np.count_nonzero(wrong != basis * SIGN % P))
    wrong = family(family(basis, 1, drop_fixed=True), 1, drop_fixed=True)
    negatives['omitted_equal_field_correction'] = int(np.count_nonzero(wrong != basis))
    x = rng.integers(0, P, size=(W * 2 * B, N), dtype=np.int64)
    expected = family(x, 0)
    for fault in ('same_target', 'check_order', 'label_return', 'omit_repair'):
        wrong = transform(x, 0, 1, 2, new_stats(), fault=fault)
        negatives[fault] = int(np.count_nonzero(wrong != expected))
    assert all(value > 0 for value in negatives.values())
    reordered = [('', event) for event in
                 ('forward_start', 'forward_done', 'inverse_start', 'table', 'inverse_done', 'finish')]
    try:
        check_events(reordered)
    except AssertionError:
        phase_order_rejected = True
    else:
        raise AssertionError('invalid conversion dependency order accepted')
    tests.append(dict(name='negative_controls', mismatching_entries=negatives,
                      inverse_before_table_rejected=phase_order_rejected, passed=True))

    for depth in range(17):
        mass = sum((Fraction(1, 4) ** d for d in range(depth)), Fraction())
        assert mass == Fraction(4, 3) * (1 - Fraction(1, 4) ** depth)
    for m in range(4, 1025):
        depth = 0
        while 16 ** depth < m:
            depth += 1
        assert m <= 16 ** depth
        assert (8 ** depth) ** 4 <= 8 ** 4 * m ** 3
    tests.append(dict(name='proof_phase_one_eighth_call_and_batch_ledgers', depths=17, arities=1021, passed=True))
    return dict(status='exact finite verification passed', field_prime=P,
                primitive_root_order=ROOT_ORDER, exact_arithmetic=True,
                routed_pencil_or_physical_tape_verification=False, tests=tests)


if __name__ == '__main__':
    result = run()
    destination = Path(__file__).with_name('reflection-family-verification.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
