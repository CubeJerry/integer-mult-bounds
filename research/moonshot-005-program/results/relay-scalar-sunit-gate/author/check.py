#!/usr/bin/env python3
"""Exact source reconstruction and finite arithmetic for the scalar relay theorem.

Completeness of the 17 S-unit orbits is the separately cited number-theoretic
theorem, not inferred from the bounded enumeration performed here.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from math import gcd
from pathlib import Path


SOURCE = "research/moonshot-005-program/results/proper-chart-relay/author/20/WORD.json.gz"
NATIVE = "research/shared-wire-split-composition/data/final.json.gz"
SOURCE_SHA = "0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c"
NATIVE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"


def smooth(n: int) -> bool:
    n = abs(n)
    if n == 0:
        return False
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


def in_ring(x: F) -> bool:
    return smooth(x.denominator)


def is_unit(x: F) -> bool:
    return smooth(x.numerator) and smooth(x.denominator)


def determinant(rows: list[list[F]]) -> F:
    a = [[F(x) for x in row] for row in rows]
    answer = F(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            answer = -answer
        value = a[col][col]
        answer *= value
        for i in range(col + 1, len(a)):
            ratio = a[i][col] / value
            for j in range(col + 1, len(a)):
                a[i][j] -= ratio * a[col][j]
    return answer


def root(mask: int) -> list[int]:
    if mask.bit_count() == 3:
        return [2 if mask >> i & 1 else -1 for i in range(9)]
    assert mask.bit_count() == 7
    zeros = [i for i in range(9) if not (mask >> i & 1)]
    return [3 * (int(i == zeros[0]) - int(i == zeros[1])) for i in range(9)]


def dot(a: list, b: list) -> F:
    return sum((F(x) * F(y) for x, y in zip(a, b)), F(0))


def orbit(x: F) -> frozenset[F]:
    return frozenset((x, 1-x, 1/x, 1/(1-x), x/(x-1), (x-1)/x))


def linear_factors(lam: F) -> tuple[F, ...]:
    return tuple(1 - c*lam for c in (13, 8, 10, 9))


def quadratic(lam: F) -> F:
    return (1 - 9*lam)**2 - lam**2/2


def factor_formula(lam: F) -> F:
    result = quadratic(lam)**2
    for f in linear_factors(lam):
        result *= f
    return result


def run(repo: Path) -> dict:
    payload = (repo / SOURCE).read_bytes()
    native_payload = (repo / NATIVE).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == SOURCE_SHA
    assert hashlib.sha256(native_payload).hexdigest() == NATIVE_SHA
    word = json.loads(gzip.decompress(payload))
    native = json.loads(gzip.decompress(native_payload))
    basis = [root(z) for z in word["relay"]["ground_Gram_frame"]]
    assert [[dot(a, b) for b in basis] for a in basis] == [
        [F(18 * (i == j)) for j in range(8)] for i in range(8)]
    hosted = sorted(map(int, word["relay"]["permutation"]))
    remaining = sorted(word["relay"]["unrestored_ports"])
    restored = sorted(word["relay"]["restored_ports"])
    assert len(hosted) == 96 and len(remaining) == 76 and len(restored) == 20
    assert set(hosted) == set(remaining) | set(restored)
    assert not set(remaining) & set(restored)
    gs = []
    for h in remaining:
        compact = word["source_role_map"][str(h)]
        frame = word["frames"][word["initial"][compact]]
        assert frame == native["frames"][native["initial"][h]]
        assert len(frame) == 1
        gs.append([dot(root(frame[0]), v)/18 for v in basis])
    small = [[sum((row[i]*row[j] for row in gs), F(0))
              for j in range(8)] for i in range(8)]

    # Both sides have degree at most eight. Nine exact distinct evaluations
    # certify the polynomial identity, rather than merely sample a conjecture.
    polynomial_checks = []
    for value in range(9):
        lam = F(value)
        actual = determinant([[F(i == j) - lam*small[i][j]
                               for j in range(8)] for i in range(8)])
        assert actual == factor_formula(lam)
        polynomial_checks.append([str(lam), str(actual)])
    assert factor_formula(F(1)) == 24387048

    triples = [(a, b, a+b) for a in range(1, 65) for b in range(a, 129-a)
               if gcd(a,b) == 1 and all(smooth(z) for z in (a,b,a+b))]
    triples.sort(key=lambda t: (t[2], t[0]))
    orbits = [orbit(F(a,c)) for a,b,c in triples]
    assert len(orbits) == len(set(orbits)) == 17
    xs = set().union(*orbits)
    assert len(xs) == 99 and all(is_unit(x) and is_unit(1-x) for x in xs)
    # This is where the published complete orbit count is invoked.
    lambdas = {(1-2*x)/(8-18*x) for x in xs if 8-18*x}
    assert len(lambdas) == 98
    candidates = sorted(lam for lam in lambdas if lam and in_ring(lam)
                        and all(is_unit(f) for f in linear_factors(lam)))
    assert candidates == [F(1,18),F(1,12),F(7,64),F(1,5),F(1,4)]
    assert all(not is_unit(quadratic(lam)) for lam in candidates)
    assert all((1-8*lam)/(2*(1-9*lam)) in xs for lam in candidates)

    # Boundary and scope controls: zero is invertible; lambda need not itself
    # be a unit; singular scalars are never units; an omitted orbit loses the
    # certified complete count. Anisotropic repairs are outside this theorem.
    assert factor_formula(F(0)) == 1 and is_unit(factor_formula(F(0)))
    assert in_ring(F(7,64)) and not is_unit(F(7,64))
    assert not in_ring(F(1,7))
    assert all(factor_formula(F(1,c)) == 0 for c in (8,9,10,13))
    assert len(set(orbits[:-1])) == 16
    lam_matrix = [[F(i == j, 4) for j in range(8)] for i in range(8)]
    for i,j in ((0,2),(1,3)):
        lam_matrix[i][i] += F(1,24)
        lam_matrix[j][j] += F(1,24)
        lam_matrix[i][j] -= F(1,24)
        lam_matrix[j][i] -= F(1,24)
    anisotropic = [[F(i == j)-sum(lam_matrix[i][k]*small[k][j] for k in range(8))
                    for j in range(8)] for i in range(8)]
    anisotropic_det = determinant(anisotropic)
    assert anisotropic_det == F(3375,128) and is_unit(anisotropic_det)
    return {
        "status":"PASS_EXACT_SOURCE_AND_S_UNIT_REDUCTION",
        "classification":"Source-specific universal scalar-rescaling obstruction using a published complete S-unit theorem. No new kappa.",
        "source":SOURCE,"source_sha256":SOURCE_SHA,
        "native":NATIVE,"native_sha256":NATIVE_SHA,
        "remaining_ports":remaining,"restored_ports":restored,
        "small_Gram":[list(map(str,row)) for row in small],
        "determinant_formula":"(1-13*l)*(1-8*l)*(1-10*l)*(1-9*l)*((1-9*l)^2-l^2/2)^2",
        "polynomial_identity_degree_bound":8,"exact_evaluations":polynomial_checks,
        "external_completeness_dependency":"von Kaenel--Matschke, arXiv:1605.06079v1, Theorem A, n=3; prior de Weger result explicitly credited there",
        "independently_generated_orbit_representatives":triples,
        "S_unit_orbits":17,"S_unit_solutions":99,
        "finite_lambda_candidates":98,
        "surviving_linear_candidates":[{"lambda":str(lam),"linear_factors":list(map(str,linear_factors(lam))),"quadratic":str(quadratic(lam))} for lam in candidates],
        "scalar_family_units_nonzero":[],
        "negative_controls":{"zero_boundary_retained":True,"nonunit_lambda_7_over_64_retained":True,"outside_ring_1_over_7_rejected":True,"singular_scalars_rejected":True,"incomplete_orbit_list_rejected":True,"anisotropic_counterexample_to_overclaim":str(anisotropic_det)},
        "complete_kappa":False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,default=Path.cwd())
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    result = run(args.repo.resolve())
    encoded = json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(encoded)
    print(json.dumps({k:result[k] for k in ("status","S_unit_orbits","S_unit_solutions","surviving_linear_candidates","negative_controls","complete_kappa")},sort_keys=True))
