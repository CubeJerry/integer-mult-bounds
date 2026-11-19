#!/usr/bin/env python3
"""Separate ternary enumeration of the source-mask bridge; no author imports."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

P = 3


def rk(A):
    a = [list(row) for row in A]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        pick = next((r for r in range(pivot, len(a)) if a[r][col] % P), None)
        if pick is None:
            continue
        a[pivot], a[pick] = a[pick], a[pivot]
        inv = pow(a[pivot][col] % P, -1, P)
        a[pivot] = [(v * inv) % P for v in a[pivot]]
        for r in range(len(a)):
            if r != pivot:
                multiple = a[r][col] % P
                a[r] = [(u - multiple*v) % P for u, v in zip(a[r], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def mats(rows, cols):
    return [tuple(tuple(v[i*cols:(i+1)*cols]) for i in range(rows))
            for v in product(range(P), repeat=rows*cols)]


def mul(A, B, cols=2):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B))) % P
                       for j in range(cols)) for i in range(len(A)))


def add(A, B):
    return tuple(tuple((u+v) % P for u, v in zip(x, y)) for x, y in zip(A, B))


def join(*As):
    return tuple(tuple(v for A in As for v in A[r]) for r in range(len(As[0])))


def main():
    ap = ArgumentParser(); ap.add_argument('--author', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True); a = ap.parse_args()
    allB = mats(2, 2); ranks = {B: rk(B) for B in allB}
    projections = [((1, 0),), ((0, 1),), ((1, 1),), ((1, 2),), ((1, 0), (0, 1))]
    criteria = minimum = leakage = 0
    rank_only_false = None
    for m in (0, 1, 2):
        Fs = [F for F in mats(m, 2) if rk(F) == m]
        for ell in (0, 1):
            Ls = mats(ell, 2)
            for C in mats(2, m):
                early = [mul(C, F) for F in Fs]
                for D in mats(2, ell):
                    late = [mul(D, L) for L in Ls]
                    possible = {add(U, V) for U in early for V in late}
                    rCD = rk(join(C, D)); rD = rk(D)
                    for B in allB:
                        good = rk(join(B, D)) == rCD == rk(join(B, C, D))
                        assert good == (B in possible)
                        if rk(join(B, D)) == rCD and not good and rank_only_false is None:
                            rank_only_false = {'C': C, 'D': D, 'B': B}
                        criteria += 1
                    for projection in projections:
                        selected = {}
                        for G in possible:
                            target = mul(projection, G)
                            selected[target] = min(selected.get(target, 3), ranks[G])
                        for target, achieved in selected.items():
                            assert achieved == max(rk(target), rCD-rD)
                            minimum += 1
                # Direct nonlinear-alphabet-sized image on the actual kernel.
                if ell == 0:
                    for F in Fs:
                        G = mul(C, F)
                        for projection in projections:
                            selected = mul(projection, G)
                            images = set()
                            for x in product(range(P), repeat=2):
                                if all(sum(v*y for v, y in zip(row, x)) % P == 0 for row in selected):
                                    images.add(tuple(sum(v*y for v, y in zip(row, x)) % P for row in G))
                            expected = rk(C)-rk(mul(projection, C, cols=m))
                            assert len(images) == P**expected
                            leakage += 1
    assert rank_only_false is not None
    # An invertible late transfer cannot erase any nonzero injected mode.
    gl = [G for G in allB if ranks[G] == 2]
    injections = 0
    for D in gl:
        for V in allB:
            assert rk(mul(D, V)) == ranks[V]
            injections += 1
    result = {'status': 'PASS_INDEPENDENT_TERNARY_SOURCE_MASK_REVIEW',
              'field': 'F3', 'full_source_criteria': criteria,
              'selected_minimum_rank_cases': minimum,
              'full_output_kernel_image_cases': leakage,
              'injective_late_transfer_cases': injections,
              'rank_only_condition_counterexample': rank_only_false,
              'proof_sha256': sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),
              'imports_author_checker': False,
              'native_literal_words_reviewed_here': False,
              'no_new_kappa': True}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict)}, sort_keys=True))


if __name__ == '__main__': main()
