#!/usr/bin/env python3
"""Exact finite controls for the proved fresh-body grading lemma."""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def mat(a, b, c, d):
    return ((F(a), F(b)), (F(c), F(d)))

I = mat(1, 0, 0, 1)
Z = mat(0, 0, 0, 0)
def add(A, B):
    return tuple(tuple(A[i][j] + B[i][j] for j in range(2)) for i in range(2))
def scale(a, A):
    return tuple(tuple(a * x for x in row) for row in A)
def mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def prod(*args):
    out = I
    for a in args:
        out = mul(out, a)
    return out
def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]
def rank(A):
    return 2 if det(A) else int(A != Z)

def run():
    C1, C2 = mat(0, 0, F(3, 2), 0), mat(0, F(-2, 3), 0, 0)
    cases = 0
    for a0, a1, a2 in itertools.product((-2, -1, 1, 2), repeat=3):
        G0, G1, G2 = mat(1, 0, a0, 1), mat(1, a1, 0, 1), mat(1, 0, a2, 1)
        walsh = Z
        homogeneous = Z
        for s1, s2 in itertools.product((-1, 1), repeat=2):
            W = prod(G2, add(scale(s2, I), C2), G1, add(scale(s1, I), C1), G0)
            need(det(W) != 0, 'invertible mixed word')
            walsh = add(walsh, scale(F(s2, 4), W))
            H = prod(G2, scale(s2, add(I, C2)), G1, scale(s1, add(I, C1)), G0)
            homogeneous = add(homogeneous, scale(F(s2, 4), H))
        expected = prod(G2, G1, C1, G0)
        need(walsh == expected and rank(walsh) == 1, 'nonzero incomplete component')
        need(homogeneous == Z, 'homogeneous positive control')
        cases += 1
    for s in (-1, 1):
        need(prod(add(scale(s, I), C1), add(scale(s, I), scale(-1, C1))) == I, 'repeated body control')
    P = mat(1, 0, 0, 0)
    need(mul(P, C1) == Z and det(P) == 0, 'singular projection loses input')
    # Exact complex arithmetic as pairs of rational numbers.
    def cmul(a, b):
        return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    def cadd(a, b):
        return (a[0]+b[0], a[1]+b[1])
    aa, bb = (F(1,2), F(1,2)), (F(1,2), F(-1,2))
    for d in ((F(1), F(0)), (F(0), F(1))):
        rhs = cadd(aa, cmul(bb, cmul(d, d)))
        need(rhs == d and rhs != (-d[0], -d[1]), 'actual even-algebra sign substitution fails')
    return {'status':'PASS', 'classification':'proved in explicit graded model; no physical exclusion inferred', 'interleavings':cases, 'sign_evaluations':4*cases, 'walsh_rank':1, 'controls':['repeated body cancellation','homogeneous source','singular projection loses inputs','actual matrix violates formal sign substitution'], 'new_kappa':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='RESULT.json')
    args = parser.parse_args()
    data = run()
    Path(args.output).write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    print(json.dumps(data, sort_keys=True))
