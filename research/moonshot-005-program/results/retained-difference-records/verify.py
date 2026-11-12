#!/usr/bin/env python3
"""Author exact rational controls for retained-delta record theorem."""
import itertools
import json
import random
from pathlib import Path
import sympy as S


def need(condition, message):
    if not condition:
        raise ValueError(message)


def vs(*matrices):
    return S.Matrix.vstack(*matrices)


def contains(base, rows):
    return vs(base, rows).rank() == base.rank()


def left_relations(matrix):
    rows = [column.T for column in matrix.T.nullspace()]
    return vs(*rows) if rows else S.zeros(0, matrix.rows)


def selected_extension(base, candidate):
    current = base
    selected = []
    rank = current.rank()
    for i in range(candidate.rows):
        row = candidate[i:i + 1, :]
        trial = vs(current, row)
        next_rank = trial.rank()
        if next_rank > rank:
            selected.append(row)
            current = trial
            rank = next_rank
    return vs(*selected) if selected else S.zeros(0, candidate.cols)


def decompose(D, QR, k):
    rows = []
    for row in D.tolist():
        solution, parameters = QR.T.gauss_jordan_solve(S.Matrix(row))
        solution = solution.subs({p: 0 for p in parameters})
        rows.append(solution.T)
    AB = vs(*rows) if rows else S.zeros(0, QR.rows)
    need(AB * QR == D, 'raw target decomposition')
    return AB[:, :k], AB[:, k:]


def evaluate(W, N, Lam, Gam, T, Q, R, D, Z, trial_K=None):
    n, k, p = W.cols, T.rows, Q.cols
    H = Lam * W + Gam * N
    E = (-T.inv() * H).row_join(T.inv() * Q)
    Y = W.row_join(S.zeros(W.rows, p)) + Z * E
    observations = vs(Y, N.row_join(S.zeros(N.rows, p)), S.zeros(R.rows, n).row_join(R))
    targets = vs(W.row_join(S.zeros(W.rows, p)), S.zeros(D.rows, n).row_join(D))
    QR = vs(Q, R)
    feasible = contains(QR, D)
    if not feasible:
        need(not contains(vs(observations, E), targets), 'impossible raw mode gate')
        return {'feasible': False}
    A, B = decompose(D, QR, k)
    G = T - Lam * Z
    UV = left_relations(QR)
    U, V = UV[:, :k], UV[:, k:]
    JK = left_relations(vs(W, N))
    J, K0 = JK[:, :W.rows], JK[:, W.rows:]
    C = vs(U * G, J * Z)
    M = vs(Z, A * G)
    # Independent source-coordinate check of the known-difference formula.
    raw_rhs = -U * Lam * Y - U * Gam * N.row_join(S.zeros(N.rows, p)) - V * S.zeros(R.rows, n).row_join(R)
    common_rhs = J * Y + K0 * N.row_join(S.zeros(N.rows, p))
    need(C * E == vs(raw_rhs, common_rhs), 'known difference identity')
    optimum = vs(C, M).rank() - C.rank()
    need(optimum == vs(observations, targets).rank() - observations.rank(), 'sharp quotient count')
    K = selected_extension(C, M)
    need(K.rows == optimum and contains(vs(observations, K * E), targets), 'attained delta combinations')
    for i in range(K.rows):
        reduced = K.copy()
        reduced.row_del(i)
        need(not contains(vs(observations, reduced * E), targets), 'every attained record is necessary')
    if trial_K is not None:
        direct = contains(vs(observations, trial_K * E), targets)
        predicted = contains(vs(C, trial_K), M)
        need(direct == predicted, 'criterion agrees with original-input observation matrix')
    coordinate_optimum = None
    for count in range(k + 1):
        for indices in itertools.combinations(range(k), count):
            rows = [S.eye(k)[i:i + 1, :] for i in indices]
            coordinate_K = vs(*rows) if rows else S.zeros(0, k)
            if contains(vs(observations, coordinate_K * E), targets):
                coordinate_optimum = count
                break
        if coordinate_optimum is not None:
            break
    need(coordinate_optimum is not None and coordinate_optimum >= optimum, 'coordinate comparison')
    if D == S.eye(p):
        need(vs(C, M).rank() == k, 'full target spans all differences modulo known data')
        need(optimum == k - C.rank() == coordinate_optimum, 'full recovery coordinate optimality')
        selected = selected_extension(C, S.eye(k))
        need(selected.rows == optimum and contains(vs(observations, selected * E), targets), 'explicit optimal coordinate set')
    return {'feasible': True, 'record_minimum': optimum, 'coordinate_minimum': coordinate_optimum, 'known_delta_rank': C.rank()}


def main():
    checks = {}
    W, N = S.eye(1), S.zeros(0, 1)
    T, Q, Lam, Gam, Z = S.Matrix([[1, 0], [1, 1]]), S.eye(2), S.Matrix([[1], [1]]), S.zeros(2, 0), S.Matrix([[1, 1]])
    for name, R in [('no_raw', S.zeros(0, 2)), ('redundant_q2', S.Matrix([[0, 1]])), ('useful_q1', S.Matrix([[1, 0]])), ('all_raw', S.eye(2))]:
        checks[name] = evaluate(W, N, Lam, Gam, T, Q, R, S.eye(2), Z, S.Matrix([[1, 1]]))
    need([checks[n]['record_minimum'] for n in ['no_raw', 'redundant_q2', 'useful_q1', 'all_raw']] == [2, 2, 1, 1], 'chronological raw-cache distinctions')
    checks['partial_sum_target'] = evaluate(W, N, S.zeros(2, 1), Gam, S.eye(2), Q, S.zeros(0, 2), S.Matrix([[1, 1]]), Z, S.Matrix([[1, 0]]))
    need(checks['partial_sum_target']['record_minimum'] == 1 and checks['partial_sum_target']['coordinate_minimum'] == 2, 'combination advantage for partial target')
    checks['repeated_raw_signal'] = evaluate(S.eye(2), S.zeros(0, 2), S.eye(2), S.zeros(2, 0), S.eye(2), S.Matrix([[1], [1]]), S.zeros(0, 1), S.eye(1), S.eye(2))
    need(checks['repeated_raw_signal']['record_minimum'] == 2, 'two erased common modes for one repeated raw input')
    checks['invisible_raw_mode'] = evaluate(W, N, S.eye(1), S.zeros(1, 0), S.eye(1), S.Matrix([[1, 1]]), S.zeros(0, 2), S.eye(2), S.eye(1))
    need(not checks['invisible_raw_mode']['feasible'], 'nonidentity signal matrix gate')
    checks['dependent_common_record'] = evaluate(W, W, Lam, S.zeros(2, 1), T, Q, S.zeros(0, 2), S.eye(2), Z)
    need(checks['dependent_common_record']['record_minimum'] == 1, 'dependent common record supplies an additional known delta combination')
    rng = random.Random(20261112)
    counts = {'independent_common': 0, 'dependent_common': 0, 'feasible': 0, 'infeasible': 0}
    def random_matrix(a, b):
        return S.Matrix(a, b, [rng.randrange(-2, 3) for _ in range(a * b)])
    for i in range(36):
        k, p, m, nr = 1 + i % 4, 1 + i % 3, 1 + (i // 3) % 3, i % 3
        if i < 24:
            t = i % 2
            n = m + t
            W = S.eye(n)[:m, :]
            N = S.eye(n)[m:, :]
            counts['independent_common'] += 1
        else:
            n = m
            W = S.eye(n)
            N = W[:1, :] if i % 2 else vs(W[:1, :], W[:1, :])
            t = N.rows
            counts['dependent_common'] += 1
        Lam, Gam, Z = random_matrix(k, m), random_matrix(k, t), random_matrix(m, k)
        T = S.eye(k)
        for a in range(k):
            for b in range(a):
                T[a, b] = rng.randrange(-2, 3)
        Q, R = random_matrix(k, p), random_matrix(nr, p)
        if i % 3 == 0:
            D = S.eye(p)
        elif i % 3 == 1:
            D = random_matrix(1, k + nr) * vs(Q, R)
        else:
            D = S.zeros(0, p)
        result = evaluate(W, N, Lam, Gam, T, Q, R, D, Z, random_matrix(i % (k + 1), k))
        counts['feasible' if result['feasible'] else 'infeasible'] += 1
    output = {'status': 'PASS_EXACT_RETAINED_DELTA_RECORD_CONTROLS', 'sympy_version': S.__version__, 'field': 'Q', 'seed': 20261112, 'named_checks': checks, 'additional_matrix_cases': counts, 'scope': 'Finite exact controls for the written quantified proof. No source construction or new kappa.'}
    Path(__file__).with_name('RECORD-CHECKS.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
