#!/usr/bin/env python3
"""Independent exact controls for mixed retained swap records and raw returns."""
import itertools
import json
from pathlib import Path
import random
import sympy as S


def need(value, message):
    if not value:
        raise ValueError(message)


def vs(*items):
    return S.Matrix.vstack(*items)


def contains(observations, targets):
    return vs(observations, targets).rank() == observations.rank()


def left_null(matrix):
    vectors = matrix.T.nullspace()
    return vs(*(v.T for v in vectors)) if vectors else S.zeros(0, matrix.rows)


def instance(Lam, Gamma, Z, L, trial_A=None):
    k, m, hidden = Lam.rows, Lam.cols, Gamma.cols
    T = S.eye(k) + L
    common = m + hidden
    W, N = S.eye(common)[:m, :], S.eye(common)[m:, :]
    H = Lam * W + Gamma * N
    delta = (-T.inv() * H).row_join(T.inv())
    Y = W.row_join(S.zeros(m, k)) + Z * delta
    R = S.zeros(k, common).row_join(S.eye(k)) - delta
    target = vs(W.row_join(S.zeros(m, k)), S.zeros(k, common).row_join(S.eye(k)))
    K = left_null(Gamma)
    B = Lam * Z - L
    C = K * B
    need(C * delta == K * (Lam * Y - R), 'mixed-record observable identity')
    expected = k - C.rank()
    count_best = None
    witnesses = 0
    for size in range(k + 1):
        for positions in itertools.combinations(range(k), size):
            A = S.eye(k)[list(positions), :] if positions else S.zeros(0, k)
            O = vs(Y, R, S.zeros(A.rows, common).row_join(A))
            direct = contains(O, target)
            criterion = vs(C, A).rank() == k
            need(direct == criterion, 'rank criterion versus original independent input rows')
            if direct:
                count_best = size if count_best is None else min(count_best, size)
            else:
                t = vs(C, A).nullspace()[0]
                eta, parameters = Gamma.gauss_jordan_solve(B * t)
                eta = eta.subs({p: 0 for p in parameters})
                du = vs(-Z * t, eta)
                change = vs(du, t)
                need(delta * change == t, 'necessity difference variation has correct sign')
                need(O * change == S.zeros(O.rows, 1), 'retained mixed records and all actual observations fixed')
                need(target * change != S.zeros(target.rows, 1), 'requested raw output changes')
                witnesses += 1
    need(count_best == expected, 'sharp coordinate-return count')
    pivot_columns = C.rref()[1]
    indices = [i for i in range(k) if i not in pivot_columns]
    Aopt = S.eye(k)[indices, :] if indices else S.zeros(0, k)
    need(Aopt.rows == expected and contains(vs(Y, R, S.zeros(Aopt.rows, common).row_join(Aopt)), target), 'explicit optimal coordinate returns')
    if trial_A is not None:
        O = vs(Y, R, S.zeros(trial_A.rows, common).row_join(trial_A))
        need(contains(O, target) == (vs(C, trial_A).rank() == k), 'arbitrary linear raw return control')
    return {'minimum_returns': expected, 'known_delta_rank': C.rank(), 'kernel_pairs_checked': witnesses}


def main():
    named = {}
    named['hub_recoverable_single'] = instance(S.eye(1), S.zeros(1, 0), S.eye(1), S.zeros(1))
    named['outside_hub_single'] = instance(S.zeros(1, 1), S.eye(1), S.eye(1), S.zeros(1))
    need(named['hub_recoverable_single']['minimum_returns'] == 0 and named['outside_hub_single']['minimum_returns'] == 1, 'single source swap distinctions')
    Lam, Gamma, Z, L = S.eye(2), S.zeros(2, 0), S.Matrix([[1, 1], [0, -1]]), S.Matrix([[0, 0], [1, 0]])
    named['chronological_minus_sign'] = instance(Lam, Gamma, Z, L)
    need(named['chronological_minus_sign']['minimum_returns'] == 1 and (Lam * Z + L).rank() == 2, 'wrong plus-L would falsely claim zero returns')
    named['hidden_common_sign'] = instance(S.eye(2), S.Matrix([[1], [0]]), S.eye(2), S.zeros(2))
    t = S.Matrix([1, 0])
    correct_eta = S.Matrix([1])
    wrong_du = vs(-t, -correct_eta)
    H = S.Matrix([[1, 0, 1], [0, 1, 0]])
    need(t - H * wrong_du != t, 'negative eta sign violates the difference equation')
    # Omitting common-row independence is invalid: Y=q and retained R=u already suffice.
    W = N = S.eye(1)
    Lam, Gamma, Z = S.zeros(1), S.eye(1), S.eye(1)
    delta = S.Matrix([[-1, 1]])
    Y = S.Matrix([[1, 0]]) + Z * delta
    R = S.Matrix([[0, 1]]) - delta
    C = left_null(Gamma) * (Lam * Z)
    need(contains(vs(Y, R), S.eye(2)) and 1 - C.rank() == 1, 'dependent common rows are a genuine excluded case')
    named['dependent_common_rows_reject_unqualified_extension'] = True
    rng = random.Random(20261113)
    def mat(a, b):
        return S.Matrix(a, b, [rng.randrange(-2, 3) for _ in range(a * b)])
    cases = []
    for index in range(48):
        k, m, hidden = 1 + index % 4, 1 + (index // 4) % 3, (index // 12) % 4
        Lam, Gamma, Z = mat(k, m), mat(k, hidden), mat(m, k)
        L = S.zeros(k)
        for i in range(k):
            for j in range(i):
                L[i, j] = rng.randrange(-2, 3)
        cases.append(instance(Lam, Gamma, Z, L, mat(index % (k + 1), k)))
    result = {'status': 'PASS_INDEPENDENT_MIXED_SWAP_RECORD_CONTROLS', 'coefficient_field': 'Q', 'sympy_version': S.__version__, 'named_controls': named, 'additional_exact_cases': len(cases), 'explicit_kernel_pairs_checked': sum(case['kernel_pairs_checked'] for case in cases), 'return_count_histogram': {str(i): sum(case['minimum_returns'] == i for case in cases) for i in range(5)}, 'scope': 'Independent original-input observation matrices, all coordinate-return subsets, explicit necessity witnesses and arbitrary linear returns. Universal proof reviewed separately. No source swap family or physical return price.'}
    Path(__file__).with_name('MIXED-SWAP-REVIEW.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
