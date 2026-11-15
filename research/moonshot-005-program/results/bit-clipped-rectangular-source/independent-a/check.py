#!/usr/bin/env python3
"""Independent finite controls for the universal clipped filtration proof.

No author checker, matrix utility, or certificate imports.  Finite cases do not
replace the all-field kernel-filtration argument in REVIEW.md.
"""
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import hashlib
import json
import random


def rank(a, p):
    a = [[x % p for x in r] for r in a]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(row, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        z = pow(a[row][col], -1, p)
        a[row] = [(x * z) % p for x in a[row]]
        for j in range(row + 1, len(a)):
            if a[j][col]:
                z = a[j][col]
                a[j] = [(x-z*y) % p for x, y in zip(a[j], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def offsets(sizes):
    out = [0]
    for x in sizes:
        out.append(out[-1] + x)
    return out


def make_case(k, width, p, seed):
    rng = random.Random(seed)
    ni = [rng.randint(1, 2) for _ in range(k)]
    mi = [rng.randint(0, 4) for _ in range(k)]
    while sum(mi) > 2*sum(ni):
        i = rng.choice([i for i, m in enumerate(mi) if m])
        mi[i] -= 1
    xoff = offsets([n*width for n in ni])
    yoff = offsets([m*width for m in mi])
    n, m = xoff[-1], yoff[-1]
    u = [[0]*m for _ in range(n)]
    matp = [[0]*n for _ in range(m)]
    supports = [[] for _ in range(k)]
    for i in range(k):
        for x in range(xoff[i], xoff[i+1]):
            for y in range(yoff[i], yoff[i+1]):
                u[x][y] = rng.randrange(p)
        for a in range(mi[i]):
            candidates = [j for j in range(k) if j != i]
            selected = rng.sample(candidates, rng.randint(0, min(3, k-1)))
            ystart = yoff[i] + a*width
            for j in selected:
                for y in range(ystart, ystart+width):
                    for x in range(xoff[j], xoff[j+1]):
                        matp[y][x] = rng.randrange(p)
            actual = [j for j in selected if any(matp[y][x]
                       for y in range(ystart, ystart+width)
                       for x in range(xoff[j], xoff[j+1]))]
            supports[i].append(actual)
    a = [[((x == z)-sum(u[x][y]*matp[y][z] for y in range(m))) % p
          for z in range(n)] for x in range(n)]
    actual_rank = rank(a, p)
    best, witness = -1, None
    for order in permutations(range(k)):
        pos = {i: j for j, i in enumerate(order)}
        clipped = sum(max(0, ni[i]-mi[i]+sum(
            all(pos[i] < pos[j] for j in s) for s in supports[i]))
            for i in range(k))
        if clipped > best:
            best, witness = clipped, order
    cheap = (119*sum(ni)+1249)//1250
    assert actual_rank >= width*best >= width*cheap
    return {"cohorts": k, "width": width, "field": p, "seed": seed,
            "target_sizes": ni, "acquisition_sizes": mi,
            "actual_rank": actual_rank, "clipped_bound": width*best,
            "rational_bound": width*cheap, "maximizing_order": witness}


def controls():
    n = 12
    low = (119*n+1249)//1250
    assert low == 2
    # With own-cohort copying, U=P=I and the residual is zero.
    own = [[0]*n for _ in range(n)]
    assert rank(own, 2) == 0 < low
    # P is a cycle, U its inverse: only U violates cohort block diagonality.
    pmat = [[int(j == (i+1) % n) for j in range(n)] for i in range(n)]
    umat = [[int(j == (i-1) % n) for j in range(n)] for i in range(n)]
    residual = [[((i == j)-sum(umat[i][h]*pmat[h][j] for h in range(n))) % 2
                 for j in range(n)] for i in range(n)]
    assert rank(residual, 2) == 0 < low
    # Four disjoint groups of <=3 foreign cohorts per source. U remains local,
    # but m=4n exceeds the 2n cap. The residual is the all-ones matrix over F2.
    groups = []
    for i in range(n):
        foreign = [j for j in range(n) if j != i]
        groups.append([foreign[h:h+3] for h in range(0, n-1, 3)])
    assert all(len(g) == 4 and all(len(s) <= 3 for s in g) for g in groups)
    residual = [[((i == j)+sum(j in s for s in groups[i])) % 2
                 for j in range(n)] for i in range(n)]
    assert residual == [[1]*n for _ in range(n)]
    assert rank(residual, 2) == 1 < low
    # One row reads all eleven foreign cohorts: only the degree-three premise
    # fails, and again the residual is all ones.
    assert rank([[1]*n for _ in range(n)], 2) == 1 < low
    return ["own_cohort_exclusion", "block_diagonal_encoder",
            "physical_channel_cap", "three_foreign_cohort_limit"]


def main():
    cases = [make_case(k, v, p, 10000*k+1000*v+100*p+r)
             for k in range(2, 6) for v in (1, 2) for p in (2, 3)
             for r in range(8)]
    a = Fraction(4, 5)
    integral = (Fraction(1, 2)-1) - (a**4/Fraction(2)-a)
    assert integral == Fraction(119, 1250)
    assert a**3 > Fraction(1, 2)
    native = {str(b): {"required_global_modes": (13209*b+1249)//1250,
                       "canonical_modes": 9*b}
              for b in (1, 2, 4, 16, 80)}
    assert all(x["required_global_modes"] > x["canonical_modes"]
               for x in native.values())
    root = Path(__file__).resolve().parents[2] / "root/rectangular-chart-source-gate"
    pins = {f: hashlib.sha256((root/f).read_bytes()).hexdigest()
            for f in ("PROOF.md", "DISJOINT-COHORTS.md")}
    result = {"status": "INDEPENDENT_FINITE_CONTROLS_PASS",
              "universal_proof_review": "REVIEW.md",
              "author_source_pins": pins, "cases": cases,
              "case_count": len(cases), "negative_controls": controls(),
              "exact_integral": str(integral), "native_examples": native,
              "scope": "Finite controls supplement a separate all-field proof review; no new kappa."}
    (Path(__file__).resolve().parent/"RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "controls": len(result["negative_controls"]), "native": native}))


if __name__ == "__main__":
    main()
