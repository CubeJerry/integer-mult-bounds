#!/usr/bin/env python3
"""Exact finite-field checks of batch-contraction repair.

The toy instance has m=4, W=16 and s=2, so each phase has W/4 rows.
It tests the theorem's general b=4 variant; the proof uses b=8.
Predictors are applied by an explicit Walsh matrix, not by Clifford routing:
this checks the algebra/composition, NOT the proposed asymptotic call bound.
All integer operations are exact modulo 257. No floating point is used.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

P = 257
M = 4
N = 1 << (2 * M)
W = 1 << M
S = 2
B = 4
INV2 = pow(2, -1, P)
INDEX = np.arange(N, dtype=np.int64)
K = (INDEX & (W - 1)) & (INDEX >> M)
PARITY = np.array([1 if i.bit_count() % 2 == 0 else -1 for i in range(W)], dtype=np.int64)
Z = PARITY[K] % P
PHASE = Z.copy()
SWAP = ((INDEX & (W - 1)) << M) | (INDEX >> M)
H = np.vstack((np.ones(W, dtype=np.int64), np.arange(1, W + 1, dtype=np.int64)))
PRED = np.empty((W, N), dtype=np.int64)
for beta in range(W):
    counts = np.array([(int(k) ^ beta).bit_count() for k in K], dtype=np.int64)
    PRED[beta] = PARITY[beta] * (1 - 2 * (counts - 2) ** 2) % P
NODE1 = K + 1
NODE2 = (K ^ (W - 1)) + 1
INVDIFF = np.array([pow(int(x) % P, -1, P) for x in NODE2 - NODE1], dtype=np.int64)


def walsh(x: np.ndarray) -> np.ndarray:
    """Normalized 256-point Walsh, exactly over F_257; U=U^-1."""
    y = x.copy() % P
    step = 1
    while step < N:
        view = y.reshape(y.shape[0], -1, 2 * step)
        left = view[:, :, :step].copy()
        right = view[:, :, step:].copy()
        view[:, :, :step] = (left + right) % P
        view[:, :, step:] = (left - right) % P
        step *= 2
    return y * pow(1 << M, -1, P) % P


def predictor(x: np.ndarray) -> np.ndarray:
    assert x.shape[0] % W == 0
    diagonal = np.tile(PRED, (x.shape[0] // W, 1))
    return walsh(walsh(x) * diagonal % P)


def transform(x: np.ndarray, depth: int, stats: dict[str, int], *, omit_correction: bool = False) -> np.ndarray:
    """Exact finite unrolling; two child phases executed in dependency order."""
    rows = x.shape[0]
    if depth == 0:
        stats['terminal_rows'] += rows
        stats['terminal_calls'] += 1
        return walsh(x)
    assert rows % (W * B ** depth) == 0
    stats['internal_rows'] += rows
    stats['internal_calls'] += 1
    work = x * PHASE % P
    px = predictor(work)
    groups = rows // W
    check_rows = []
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        check_rows.extend((H @ px[sl] % P, H @ work[sl] % P))
    spectral = transform(np.vstack(check_rows), depth - 1, stats)
    table_rows = []
    for group in range(groups):
        hx_p, hx = spectral[group * 4:group * 4 + 2], spectral[group * 4 + 2:group * 4 + 4]
        he = (hx_p - Z * hx) % P
        e1 = (NODE2 * he[0] - he[1]) * INVDIFF % P
        e2 = (he[1] - NODE1 * he[0]) * INVDIFF % P
        # On each exceptional beta, p=-7z. D_z(p)=-(p+2z)/2.
        t1 = (5 * INV2 * Z * e1) % P
        t2 = (5 * INV2 * Z * e2) % P
        a1 = (t2 - t1) * INVDIFF % P
        a0 = (t1 - NODE1 * a1) % P
        a = np.vstack((a0, a1))
        table_rows.extend((a, a * Z % P))
    ordinary = transform(np.vstack(table_rows), depth - 1, stats)
    lift_z = np.empty_like(work)
    lift_fz = np.empty_like(work)
    for group in range(groups):
        sl = slice(group * W, (group + 1) * W)
        lift_z[sl] = H.T @ ordinary[group * 4:group * 4 + 2] % P
        lift_fz[sl] = H.T @ ordinary[group * 4 + 2:group * 4 + 4] % P
    p3x = predictor(predictor(px))
    gp = (3 * px - p3x) * INV2 % P
    result_f = gp if omit_correction else (gp - predictor(lift_z) + lift_fz) % P
    # F=D U_swap D, hence U=P_swap D F D.
    return (result_f * PHASE % P)[:, SWAP]


def run() -> dict[str, object]:
    rng = np.random.default_rng(20261125)
    tests: list[dict[str, object]] = []
    # Source closure identity, independently of the recursive repair.
    x = rng.integers(0, P, size=(W, N), dtype=np.int64)
    f_spectral = walsh(walsh(x) * Z % P)
    f_monomial = (walsh(x * PHASE % P)[:, SWAP] * PHASE) % P
    assert np.array_equal(f_spectral, f_monomial)
    assert np.array_equal(walsh(walsh(x)), x)
    tests.append({'name': 'normalized_walsh_closure', 'passed': True})
    # Every shift/frequency satisfies exact prediction or one of two known exceptions.
    for frequency in range(N):
        exception = {int(K[frequency]), int(K[frequency]) ^ (W - 1)}
        actual = {i for i in range(W) if PRED[i, frequency] != Z[frequency]}
        assert actual == exception
    tests.append({'name': 'frequency_dependent_exception_sets', 'cases': W * N, 'passed': True})
    for depth in (1, 2):
        rows = W * B ** depth
        x = rng.integers(0, P, size=(rows, N), dtype=np.int64)
        stats = dict(terminal_rows=0, terminal_calls=0, internal_rows=0, internal_calls=0)
        out = transform(x, depth, stats)
        assert np.array_equal(out, walsh(x))
        expected_terminal = rows * Fraction(2, B) ** depth
        expected_internal = rows * sum((Fraction(2, B) ** d for d in range(depth)), Fraction())
        assert stats['terminal_rows'] == expected_terminal
        assert stats['internal_rows'] == expected_internal
        assert stats['terminal_calls'] == 2 ** depth
        tests.append({'name': 'full_rate_exact_unrolling', 'depth': depth, 'rows': rows, 'entries': rows * N, 'passed': True, 'statistics': stats})
    # Negative control: discard the correction despite its frequency-dependent support.
    x = rng.integers(0, P, size=(W * B, N), dtype=np.int64)
    stats = dict(terminal_rows=0, terminal_calls=0, internal_rows=0, internal_calls=0)
    wrong = transform(x, 1, stats, omit_correction=True)
    mismatches = int(np.count_nonzero(wrong != walsh(x)))
    assert mismatches > 0
    tests.append({'name': 'omit_repair_negative_control', 'mismatching_entries': mismatches, 'correctly_rejected': True})
    # Arithmetic ledger for the proof's q=1/8 case, using symbolic exact fractions.
    for depth in range(12):
        ratio = sum((Fraction(1, 4) ** d for d in range(depth)), Fraction())
        assert ratio == Fraction(4, 3) * (1 - Fraction(1, 4) ** depth)
        assert (16 * 8 ** depth) % 16 == 0
    tests.append({'name': 'q_one_eighth_call_ledger', 'depths': 12, 'passed': True})
    return {'status': 'finite computational verification', 'field_prime': P, 'numpy_version': np.__version__, 'exact_arithmetic': True, 'asymptotic_or_tape_verification': False, 'tests': tests}


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, indent=2))
