#!/usr/bin/env python3
"""Independent finite controls for the simultaneous-restoration theorem.

No author code is imported.  Exhaustive binary subspace checks supplement,
but do not substitute for, the separate review of the universal proof.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def basis(rows):
    b = {}
    for r in rows:
        while r:
            p = r.bit_length()-1
            if p in b:
                r ^= b[p]
            else:
                b[p] = r
                break
    for p in sorted(b):
        for q in sorted(b):
            if q > p and b[q] >> p & 1:
                b[q] ^= b[p]
    return tuple(b[p] for p in sorted(b, reverse=True))


def combine(coeff, rows):
    out = 0
    for j, r in enumerate(rows):
        if coeff >> j & 1:
            out ^= r
    return out


def product(left, right):
    return tuple(combine(r, right) for r in left)


def dot(row, x):
    return (row & x).bit_count() & 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proof", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    census = []
    examples = []
    for h in (1,2,3):
        mats = list(itertools.product(range(1 << h), repeat=h))
        gl = [m for m in mats if len(basis(m)) == h]
        spaces = sorted({basis(m) for m in mats})
        yes = no = 0
        for A in mats:
            for C in spaces:
                criterion = len(basis(A+C)) == h
                K = [x for x in range(1,1 << h) if all(dot(r,x)==0 for r in A+C)]
                if criterion != (not K):
                    raise ValueError("rank/kernel disagreement")
                coeff = {combine(v,C):v for v in range(1 << len(C))}
                found = None
                for U in gl:
                    UA = product(U,A)
                    E = tuple((1 << j)^UA[j] for j in range(h))
                    if all(r in coeff for r in E):
                        V = tuple(coeff[r] for r in E)
                        found = U,V
                        break
                if (found is not None) != criterion:
                    raise ValueError(("sufficiency/existence disagreement", h,A,C))
                if found:
                    yes += 1
                    U,V = found
                    if tuple(x^y for x,y in zip(product(U,A),product(V,C))) != tuple(1 << j for j in range(h)):
                        raise ValueError("restoration identity")
                    # Direct coefficient replay with two arbitrary nuisance
                    # source columns selected deterministically for this case.
                    B = tuple(((A[j] << 1)^j^len(C)) & 3 for j in range(h))
                    D = tuple(((C[j] << 1)^j^h) & 3 for j in range(len(C)))
                    W = tuple(x^y for x,y in zip(product(U,B),product(V,D)))
                    z = tuple(A[j] | (B[j] << h) for j in range(h))
                    side = tuple(C[j] | (D[j] << h) for j in range(len(C)))
                    raw = (1 << h, 1 << (h+1))
                    end = tuple(x^y^z for x,y,z in zip(product(U,z),product(V,side),product(W,raw)))
                    if end != tuple(1 << j for j in range(h)):
                        raise ValueError("all-column nuisance restoration")
                else:
                    no += 1
                    v = K[0]
                    # Inputs0 andv have the same observations at fixed r0.
                    if any(dot(row,v) for row in A+C):
                        raise ValueError("failed collision witness")
                if h == 2 and A == (3,3) and C in ((),(1,)):
                    examples.append({"A":A,"C":C,"criterion":criterion,
                                     "U_V":found,"collision":K[0] if K else None})
        census.append({"h":h,"matrices":len(mats),"side_subspaces":len(spaces),
                       "invertible_candidate_U":len(gl),"positive":yes,"negative":no,
                       "all_cases":yes+no})
    result = {
        "status":"PASS_INDEPENDENT_RESTORATION_INTERFACE_CONTROLS",
        "proof_sha256":hashlib.sha256(a.proof.read_bytes()).hexdigest(),
        "method":"Independent exhaustive binary matrices, canonical side subspaces and invertibleU search; explicit nuisance coefficient replay for every positive case and nonzero input-collision witnesses for every negative case. No author code imported.",
        "census":census,"cases":sum(c["all_cases"] for c in census),
        "essential_examples":examples,
        "scope":"Finite controls only. The all-field and all-width claims rely on the separately reviewed universal proof, not enumeration. Actual side-information custody and paid ordinary implementation remain application obligations.",
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"],result["cases"],census)


if __name__ == "__main__":
    main()
