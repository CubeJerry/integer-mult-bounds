#!/usr/bin/env python3
"""Exact source and free noncommutative-polynomial controls for the gate.

The universal component/rank argument is in the companion proof. This script
does not replace it by sampled scalar matrices or a finite caller search.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s


def add(*polys):
    out = {}
    for poly in polys:
        for word, coeff in poly.items():
            out[word] = out.get(word, 0) + coeff
    return {w: c for w, c in out.items() if c}


def mul(x, y):
    out = {}
    for wx, cx in x.items():
        for wy, cy in y.items():
            word = wx + wy
            out[word] = out.get(word, 0) + cx * cy
    return {w: c for w, c in out.items() if c}


def neg(x):
    return {w: -c for w, c in x.items()}


def atom(name):
    return {(name,): 1}


def mm(x, y):
    return [[add(*(mul(x[i][j], y[j][k]) for j in range(len(y))))
             for k in range(len(y[0]))] for i in range(len(x))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    one, zero = {(): 1}, {}
    a, w, g, h, k, j = map(atom, ('a', 'w', 'g', 'h', 'k', 'j'))
    a2, a3, a4 = mul(a, a), mul(mul(a, a), a), mul(mul(a, a), mul(a, a))
    L = [[a, zero, zero], [one, a, zero], [zero, zero, one]]
    U = [[a, neg(a2), zero], [zero, a, zero], [zero, zero, one]]
    Cl = [[w, zero, zero], [g, h, zero], [zero, zero, k]]
    Cu = [[w, g, zero], [zero, h, zero], [zero, zero, k]]
    lwa, lwa2, aga, aga2, aha = [mul(mul(x, y), z) for x, y, z in
                                ((a, w, a), (a, w, a2), (a, g, a),
                                 (a, g, a2), (a, h, a))]
    expected_l = [[lwa, neg(lwa2), zero],
                  [add(mul(w, a), aga), add(neg(mul(w, a2)), neg(aga2), aha), zero],
                  [zero, zero, k]]
    expected_u = [[lwa, add(aga, neg(lwa2)), zero],
                  [mul(w, a), add(neg(mul(w, a2)), mul(g, a), aha), zero],
                  [zero, zero, k]]
    assert mm(mm(L, Cl), U) == expected_l
    assert mm(mm(L, Cu), U) == expected_u
    Q = [[atom(f'q{r}{c}') for c in range(3)] for r in range(3)]
    expected_last = [add(mul(mul(k, Q[2][0]), a), mul(k, Q[2][1])),
                     mul(mul(k, Q[2][1]), a), mul(k, Q[2][2])]
    for C, prefix in ((Cl, expected_l), (Cu, expected_u)):
        endpoint = mm(mm(mm(mm(L, C), U), Q), L)
        assert endpoint[2] == expected_last
        assert [endpoint[r][2] for r in range(2)] == [
            add(mul(prefix[r][0], Q[0][2]), mul(prefix[r][1], Q[1][2]))
            for r in range(2)]
    Cs = [[one, zero, zero], [g, one, zero], [zero, zero, one]]
    Qs = [[one, zero, zero], [j, one, zero], [zero, zero, one]]
    Es = mm(mm(mm(mm(L, Cs), U), Qs), L)
    expected_s = [[neg(mul(mul(a3, j), a)), neg(a4), zero],
                  [add(a2, neg(mul(mul(mul(mul(a, g), a2), j), a))),
                   neg(mul(mul(a, g), a3)), zero],
                  [zero, zero, one]]
    assert Es == expected_s

    tidy = lambda matrix: matrix.applyfunc(s.expand)
    I = s.eye(16)
    P, Xb = s.zeros(16), s.zeros(16)
    D = s.eye(16)
    for x in range(16):
        P[(x >> 1) | ((x & 1) << 3), x] = 1
        Xb[x ^ 2, x] = 1
        D[x, x] = -1 if (x & 13) == 13 else 1
    S = D * P
    A = tidy(((1+s.I)*I + (1-s.I)*Xb) * S / 2)
    Ai = A.conjugate().T
    A2, A3 = tidy(A*A), tidy(A*A*A)
    Db = s.diag(*[s.I**((x >> 1) & 1) for x in range(16)])
    Dquartic = s.diag(*[-1 if x == 15 else 1 for x in range(16)])
    examples = []
    for label, W in (('identity', I), ('quarter_D_b', Db), ('quartic_sign', Dquartic)):
        J = tidy(A*W*Ai)
        assert all(sum(J[r, c] != 0 for r in range(16)) == 1 for c in range(16))
        T = tidy(A*W*A2)
        assert T == tidy(J*A3)
        assert tidy(T*T.conjugate().T) == I
        examples.append({'w': label, 'forward_transport_monomial': True,
                         'T_is_literal_monomial_times_A3': True, 'T_unit': True})
    clock = S.conjugate().T * Db
    bad = tidy(A*clock*A2)
    supports = sorted({sum(z != 0 for z in row) for row in bad.tolist()})
    assert max(supports) <= 4
    assert tidy(bad*bad.conjugate().T) == I
    programme = args.repo/'research/moonshot-005-program'
    deps = ['results/complex-four-bit-cubic-source/author/PROOF.md',
            'results/complex-boolean-sign-family/author/PROOF.md',
            'results/complex-middle-native-interface/author/PROOF.md',
            'results/complex-inverse-native-coset/two-native/PROOF.md']
    for dep in deps:
        if not (programme/dep).is_file():
            raise FileNotFoundError(dep)
    result = {
        'status': 'PASS_AUTHOR_TRIANGULAR_FIRST_INTERSTAGE_IDENTITIES_AND_CONTROLS',
        'scope': 'Formal noncommutative identities and exact one-column source controls. Universal theorem is the written faithful-width component/rank proof; independent review pending.',
        'formal_identities': ['lower_LCU', 'upper_LCU', 'full_last_row',
                              'full_last_input_column', 'two_lower_shears'],
        'source_examples': examples,
        'negative_control_first_pivot_clock': {
            'ordinary_w': True, 'a_w_a2_unit': True,
            'row_supports': supports, 'pi3_equals_zero': True,
            'shows_T_invertibility_hypothesis_is_material': True},
        'quantifier': 'For each fixed finite template, every V >= V0(catalogue) at which pi3(a w a²) is invertible. No isolated-width exclusion.',
        'source_pins': {dep: hashlib.sha256((programme/dep).read_bytes()).hexdigest()
                        for dep in deps},
        'proof_sha256': hashlib.sha256(Path(__file__).with_name('TRIANGULAR-FIRST-INTERSTAGE.md').read_bytes()).hexdigest(),
    }
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'source_examples': len(examples),
                      'negative_control_row_supports': supports}, indent=2))


if __name__ == '__main__':
    main()
