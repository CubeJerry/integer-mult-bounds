#!/usr/bin/env python3
"""Exact identity/source checks; @CubeJerry with OpenAI assistance. Apache-2.0.

New implementation. Retained ROOT.json credit: inputs/NOTICE.
PROOF.md, not this finite replay, establishes the theorem.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_SHA256 = "b31151c36e39c9267bcc81ec3e13d9d29df9d0c0b404830a9cfb01e21a5b8fc2"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b, c=1):
    return [[x+c*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def transpose(a):
    return [list(c) for c in zip(*a)]


def inverse(a):
    n = len(a)
    rows = [list(map(F, r))+e for r, e in zip(a, eye(n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        need(pivot is not None, "nonsingular matrix")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v/scale for v in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[j])]
    return [r[n:] for r in rows]


def rank(a):
    rows = [list(map(F, r)) for r in a]
    out = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(out, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[out], rows[pivot] = rows[pivot], rows[out]
        scale = rows[out][j]
        rows[out] = [v/scale for v in rows[out]]
        for i in range(out+1, len(rows)):
            scale = rows[i][j]
            rows[i] = [x-scale*y for x, y in zip(rows[i], rows[out])]
        out += 1
        if out == len(rows):
            break
    return out


def sign(x):
    return (x > 0)-(x < 0)


def gram(m, s):
    return [[F(sign(i-j))+s for j in range(m)] for i in range(m)]


def gram_inverse(m, s):
    return [[F((-1)**(i+j))*(sign(i-j)+s) for j in range(m)] for i in range(m)]


def polynomial_inverse_checks(m):
    """Each coefficient of (A+sJ)(B+sqq^t)=I and the reverse."""
    a, b = gram(m, F(0)), gram_inverse(m, F(0))
    j = [[F(1)]*m for _ in range(m)]
    qq = [[F((-1)**(r+c)) for c in range(m)] for r in range(m)]
    z = zero(m)
    need(mul(a, b) == eye(m) == mul(b, a), "constant inverse coefficient")
    need(add(mul(a, qq), mul(j, b)) == z, "linear inverse coefficient")
    need(add(mul(b, j), mul(qq, a)) == z, "reverse linear coefficient")
    need(mul(j, qq) == z == mul(qq, j), "quadratic inverse coefficient")
    need(sum(sum(r) for r in b) == 0 == sum(sum(r) for r in qq), "zero ones sandwich")


def obstruction_witness(m, p, s, orientation="same"):
    """Individually valid H-projectors, with necessary cross-pairing."""
    e, f = zero(m+p), zero(m+p)
    x, y = (s-1, s+1) if orientation == "same" else (F(2), F(-2))
    for i in range(m):
        e[i][i] = 1
        for j in range(p):
            e[i][m+j] = x*(-1)**i
    for j in range(p):
        f[m+j][m+j] = 1
        for i in range(m):
            f[m+j][i] = y*(-1)**j
    need(mul(e, e) == e and mul(f, f) == f, "individual idempotence")
    ef, fe = mul(e, f), mul(f, e)
    need(mul(ef, e) == zero(m+p) == mul(fe, f), "zero triple products")
    need(ef != fe, "forbidden banks cannot commute")
    need((ef == zero(m+p)) == (x == 0), "forward exceptional branch")
    need((fe == zero(m+p)) == (y == 0), "reverse exceptional branch")
    return e, f


def canonical_queries(n):
    us = [eye(n)[i] for i in range(n)] + [[F((-1)**(i+1)) for i in range(n)]]
    vs = [[F(sign(i-j)) for j in range(n)] for i in range(n)] + [[F(1)]*n]
    return [mul(transpose([u]), [v]) for u, v in zip(us, vs)], us, vs


def verify_root(data):
    n = data["fields"]
    need(n == 8, "source field count")
    rs = [[list(map(F, row)) for row in r] for r in data["queries"]]
    need(len(rs) == n+1, "shortest query count")
    us, vs = [], []
    for rmat in rs:
        need(rank(rmat) == 1 and mul(rmat, rmat) == zero(n), "nonzero rank-one nilpotent")
        j = next(j for j in range(n) if any(rmat[i][j] for i in range(n)))
        u = [rmat[i][j] for i in range(n)]
        i = next(i for i in range(n) if u[i])
        v = [x/u[i] for x in rmat[i]]
        need(mul(transpose([u]), [v]) == rmat, "query factorization")
        us.append(u)
        vs.append(v)
    scales = [F(1)] + [-1/sum(x*y for x, y in zip(vs[0], us[i])) for i in range(1, n+1)]
    h = transpose([[x*scales[i] for x in us[i]] for i in range(n)])
    hi = inverse(h)
    canonical, cus, cvs = canonical_queries(n)
    need([mul(mul(hi, rmat), h) for rmat in rs] == canonical, "canonical source normalization")
    sites, masks = data["full_sites"], data["masks"]
    need(sites == [0, 1, 2, 6, 7, 8] and len(masks) == len(sites), "source stage sites")
    ps = {i: mul(mul(hi, [[F(j == k and ((mask >> j) & 1)) for k in range(n)] for j in range(n)]), h)
          for i, mask in zip(sites, masks)}
    prefix = eye(n)
    for i, rmat in enumerate(canonical):
        prefix = mul(add(eye(n), rmat, -2), prefix)
        if i in ps:
            p = ps[i]
            need(mul(p, p) == p and mul(p, rmat) == rmat == mul(rmat, p), "actual stage support")
            need(mul(p, prefix) == mul(prefix, p), "actual prefix commutation")
    need(prefix == add(zero(n), eye(n), -1), "actual central endpoint")
    for p in ps.values():
        for q in ps.values():
            need(mul(p, q) == mul(q, p), "actual pairwise commutation")
    need([rank(ps[i]) for i in sites] == data["stage_ranks"], "recorded actual stage ranks")
    p0, pn = ps[0], ps[n]
    intersection = mul(p0, pn)
    need(rank(p0) == rank(pn) == 2 and rank(intersection) == 1, "distinct rank-two endpoints")
    hp = add(add(add(eye(n), p0, -1), pn, -1), intersection)
    e0, un = transpose([cus[0]]), transpose([cus[n]])
    a = mul(pn, e0)
    r = -mul([cvs[0]], a)[0][0]
    need(r != 0, "nonzero endpoint parameter")
    z = add(add(e0, un, r), a, -1)
    w0 = add(e0, un)
    projectors = []
    for i, face, s, factor in [(1, p0, 1/r, 1/r), (6, pn, -r, F(1))]:
        q = ps[i]
        need(ps[i+1] == q and rank(q) == 4, "actual minimal pair bank")
        e = add(q, face, -1)
        d = transpose([[row[0] for row in add(add(transpose([cus[j]]), w0, -1), z, factor)] for j in (i, i+1)])
        c = mul([cvs[j] for j in (i, i+1)], hp)
        need(mul(hp, d) == d, "forced columns lie in common kernel")
        need(mul(c, d) == gram(2, s), "actual forced pair Gram")
        need(e == mul(mul(d, gram_inverse(2, s)), c), "actual unique minimal H-projector")
        projectors.append((e, d, c))
    el, dl, cl = projectors[0]
    er, dr, cr = projectors[1]
    need(mul(cl, dr) == zero(2) == mul(cr, dl), "actual allowed L-before-R order")
    need(mul(el, er) == zero(n) == mul(er, el), "actual disjoint H projectors")
    return {"fields": n, "endpoint_parameter": str(r), "left_pair": [1, 2], "right_pair": [6, 7], "ranks": [2, 4, 4, 4, 4, 2]}


def expect_failure(fn, label):
    try:
        fn()
    except ValueError:
        return label
    raise ValueError("negative control unexpectedly passed: "+label)


def main():
    raw = (HERE/"inputs/ROOT.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == ROOT_SHA256, "retained source byte pin")
    data = json.loads(raw)
    source = verify_root(data)
    dimensions = list(range(2, 18, 2))
    for m in dimensions:
        polynomial_inverse_checks(m)
    parameters = [F(-3), F(-1), F(-1, 2), F(1, 2), F(1), F(3)]
    count = 0
    for m in (2, 4, 6):
        for p in (2, 4, 6):
            for s in parameters:
                obstruction_witness(m, p, s)
                obstruction_witness(m, p, s, "reversed")
                count += 2
    faults = []
    bad = json.loads(raw)
    bad["queries"][3] = [["0"]*8 for _ in range(8)]
    faults.append(expect_failure(lambda: verify_root(bad), "deleted query"))
    bad_mask = json.loads(raw)
    bad_mask["masks"][1] = 67
    faults.append(expect_failure(lambda: verify_root(bad_mask), "deleted common-bank coordinate"))
    faults.append(expect_failure(lambda: polynomial_inverse_checks(3), "odd block substituted"))
    for s in (F(1), F(-1)):
        e, f = obstruction_witness(2, 2, s)
        need((mul(e, f) == zero(4)) != (mul(f, e) == zero(4)), "both exceptional orientations exercised")
    faults.append(expect_failure(lambda: need(mul(gram(2, F(0)), gram(2, F(0))) == eye(2), "mutated inverse"), "inverse sign mutation"))
    result = {"status": "PASS_ENDPOINT_FACE_EVEN_BLOCK_OBSTRUCTION", "new_kappa": False,
              "source_fixture": source, "polynomial_inverse_dimensions": dimensions,
              "projector_obstruction_instances": count, "parameters": list(map(str, parameters)),
              "exceptional_parameters_checked": ["-1", "1"], "negative_controls": faults}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
