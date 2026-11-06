#!/usr/bin/env python3
"""Independent exact endpoint-face review; stdlib only, no author imports.

Prepared for @CubeJerry with substantial OpenAI Codex assistance.
Apache-2.0. Source root retains its original authors' attribution and license.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile

SOURCE_SHA = "b31151c36e39c9267bcc81ec3e13d9d29df9d0c0b404830a9cfb01e21a5b8fc2"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def reduce(x, p):
    return x if p is None else x % p


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def mul(a, b, p=None):
    return [[reduce(sum(x * y for x, y in zip(row, col)), p)
             for col in zip(*b)] for row in a]


def add(a, b, p=None, scale=1):
    return [[reduce(x + scale * y, p) for x, y in zip(ar, br)]
            for ar, br in zip(a, b)]


def smul(s, a, p=None):
    return [[reduce(s * x, p) for x in row] for row in a]


def trace(a, p=None):
    return reduce(sum(a[i][i] for i in range(len(a))), p)


def inverse(a, p=None):
    n = len(a)
    rows = [[Fraction(x) if p is None else x % p for x in row] + eye(n)[i]
            for i, row in enumerate(a)]
    det = 1
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            return 0, None
        if pivot != j:
            rows[j], rows[pivot] = rows[pivot], rows[j]
            det = reduce(-det, p)
        x = rows[j][j]
        det = reduce(det * x, p)
        recip = 1 / x if p is None else pow(x, -1, p)
        rows[j] = [reduce(y * recip, p) for y in rows[j]]
        for i in range(n):
            if i != j:
                x = rows[i][j]
                rows[i] = [reduce(u - x * v, p) for u, v in zip(rows[i], rows[j])]
    return det, [row[n:] for row in rows]


def sign(x):
    return (x > 0) - (x < 0)


def gram(m, s, p):
    return [[(sign(i - j) + s) % p for j in range(m)] for i in range(m)]


def canonical(n, p=None):
    result = []
    for i in range(n + 1):
        u = [int(i == j) for j in range(n)] if i < n else [(-1) ** (j + 1) for j in range(n)]
        v = [sign(i - j) for j in range(n)] if i < n else [1] * n
        result.append(mul(transpose([u]), [v], p))
    return result


def gram_checks():
    count, singular = 0, 0
    for p in (2, 3, 5, 7, 11):
        for m in range(1, 17):
            q = [[(-1) ** i % p] for i in range(m)]
            b = [[((-1) ** (i + j) * sign(i - j)) % p for j in range(m)] for i in range(m)]
            for s in range(p):
                count += 1
                k = gram(m, s, p)
                det, ki = inverse(k, p)
                need(det == (s if m % 2 else 1), "Gram determinant")
                if m % 2 and not s:
                    need(ki is None, "odd zero parameter must be singular")
                    singular += 1
                    continue
                coeff = pow(s, -1, p) if m % 2 else s
                proposed = add(b, smul(coeff, mul(q, transpose(q), p), p), p)
                need(ki == proposed, "independent elimination disagrees with inverse")
                sandwich = sum(map(sum, ki)) % p
                need(sandwich == (coeff if m % 2 else 0), "ones sandwich")
                if m % 2:
                    need(mul(ki, [[1]] * m, p) == smul(coeff, q, p), "odd inverse column")
                    need(mul([[1] * m], ki, p) == smul(coeff, transpose(q), p), "odd inverse row")
                else:
                    need(mul(ki, [[1]] * m, p) == q, "even inverse column")
                    need(mul([[1] * m], ki, p) == smul(-1, transpose(q), p), "even inverse row")
    return {"cases": count, "odd_zero_parameter_singular": singular,
            "fields": [2, 3, 5, 7, 11], "group_sizes": [1, 16]}


def abstract_banks(m, n, s, t, x, y, p):
    # D_I,D_J are separate coordinate embeddings. Rows C_I,C_J are
    # assembled independently from their stipulated within/cross pairings.
    _, ki = inverse(gram(m, s, p), p)
    _, kj = inverse(gram(n, t, p), p)
    ci = [gram(m, s, p)[i] + [x % p] * n for i in range(m)]
    cj = [[y % p] * m + gram(n, t, p)[i] for i in range(n)]
    e = mul(ki, ci, p) + [[0] * (m + n) for _ in range(n)]
    f = [[0] * (m + n) for _ in range(m)] + mul(kj, cj, p)
    need(mul(e, e, p) == e and mul(f, f, p) == f, "individual idempotents")
    return e, f


def rank_one_product_checks():
    same_count = reverse_count = 0
    for p in (3, 5, 7, 11):
        for m in (1, 2, 3, 4, 6):
            for n in (1, 2, 3, 4, 6):
                for s in range(1, p):
                    e, f = abstract_banks(m, n, s, s, s - 1, s + 1, p)
                    ef, fe = mul(e, f, p), mul(f, e, p)
                    expected = (1 - pow(s, -2, p)) % p if m % 2 and n % 2 else 0
                    need(trace(ef, p) == expected, "same-face trace")
                    need(mul(ef, ef, p) == smul(expected, ef, p), "rank-one square identity")
                    need(ef != fe, "same faces cannot commute")
                    same_count += 1
                    e, f = abstract_banks(m, n, -s, pow(s, -1, p), -2, 2, p)
                    ef, fe = mul(e, f, p), mul(f, e, p)
                    expected = 4 % p if m % 2 and n % 2 else 0
                    need(trace(ef, p) == expected, "reverse-face trace")
                    if p != 3 or not (m % 2 and n % 2):
                        need(mul(ef, ef, p) != ef, "forbidden reverse product is not idempotent")
                        need(ef != fe, "forbidden reversed banks cannot commute")
                    reverse_count += 1
    # Characteristic two is a real excluded degeneracy in the block mechanism.
    e, f = abstract_banks(2, 2, 1, 1, 0, 0, 2)
    need(mul(e, f, 2) == mul(f, e, 2), "characteristic-two scope control")
    return {"same_face_cases": same_count, "reverse_face_cases": reverse_count,
            "characteristic_two_commuting_control": True}


def diagonal_mask(n, mask):
    return [[int(i == j and mask & (1 << i) != 0) for j in range(n)] for i in range(n)]


def characteristic_three_witness():
    p, n = 3, 4
    cols = [[0, 2, 2, 0], [1, 1, 1, 0], [1, 1, 0, 2], [0, 2, 1, 0]]
    basis = transpose(cols)
    det, bi = inverse(basis, p)
    need(det != 0, "char3 joint basis")
    masks = [3, 5, 13, 11]
    banks = [mul(mul(basis, diagonal_mask(n, mask), p), bi, p) for mask in masks]
    rs = canonical(n, p)
    for bank, site in zip(banks, (0, 4, 1, 2)):
        need(mul(bank, bank, p) == bank, "char3 idempotent")
        need(mul(bank, rs[site], p) == rs[site] == mul(rs[site], bank, p), "char3 two-sided query support")
        for other in banks:
            need(mul(bank, other, p) == mul(other, bank, p), "char3 banks commute")
    prefix = eye(n)
    failures = []
    for site, r in enumerate(rs):
        prefix = mul(add(eye(n), r, p, -2), prefix, p)
        if site in (0, 1, 2, 4):
            bank = banks[{0: 0, 4: 1, 1: 2, 2: 3}[site]]
            if mul(bank, prefix, p) != mul(prefix, bank, p):
                failures.append(site)
    need(failures, "scope control is not a fully certified native root")
    return {"field": 3, "n": n, "r": 1, "z": [0, 2, 0, 1],
            "basis_columns_a_b_c_h": cols, "masks_P0_Pn_R_L": masks,
            "right_group": [1], "left_group": [2],
            "prefix_commutation_fails_at": failures,
            "projectors_P0_Pn_R_L": banks,
            "scope": "Canonical support and commuting banks only; not a native caller root."}


def root_check(path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, "source SHA256")
    data = json.loads(raw)
    n = data["fields"]
    rs = [[[Fraction(x) for x in row] for row in r] for r in data["queries"]]
    u0 = next([row[j] for row in rs[0]] for j in range(n) if any(row[j] for row in rs[0]))
    cols = [u0] + [[row[0] for row in mul(r, transpose([u0]))] for r in rs[1:n]]
    h = transpose(cols)
    det, hi = inverse(h)
    need(det != 0, "source root Krylov-style normalization basis")
    need([mul(mul(hi, r), h) for r in rs] == canonical(n), "all source canonical queries")
    banks = {site: mul(mul(hi, diagonal_mask(n, mask)), h)
             for site, mask in zip(data["full_sites"], data["masks"])}
    a = [row[0] for row in banks[n]]
    r = sum(a[1:])
    need(r == -1, "source endpoint parameter")
    need(banks[1] == banks[2] and banks[6] == banks[7], "source pair banks")
    return {"source_sha256": SOURCE_SHA, "canonical_queries_checked": n + 1,
            "normalization": "u0 a nonzero source R0 column, then Ri*u0",
            "r": str(r), "pair_sites": [[1, 2], [6, 7]]}


def fault_controls(source):
    # The odd inverse cannot use the even coefficient s in place of 1/s.
    m, s, p = 3, 2, 5
    _, actual = inverse(gram(m, s, p), p)
    q = [[1], [-1], [1]]
    b = [[((-1) ** (i + j) * sign(i - j)) % p for j in range(m)] for i in range(m)]
    wrong = add(b, smul(s, mul(q, transpose(q), p), p), p)
    need(actual != wrong, "wrong odd inverse coefficient must fail")
    # The exceptional same-face parameter must not be silently omitted.
    e, f = abstract_banks(2, 2, 1, 1, 0, 2, 5)
    need(not any(map(any, mul(e, f, 5))) and any(map(any, mul(f, e, 5))),
         "s=1 has zero forward and nonzero reverse product")
    # A real fixture mutation must be rejected by the source-bound entrypoint.
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "mutated-root.json"
        data = json.loads(source.read_bytes())
        data["queries"][1][0][0] = "2"
        path.write_text(json.dumps(data), encoding="utf-8")
        try:
            root_check(path)
        except ValueError as error:
            need(str(error) == "source SHA256", "mutation rejected at source pin")
        else:
            raise ValueError("mutated fixture accepted")
    return ["wrong odd inverse coefficient rejected", "s=1 asymmetric products detected",
            "mutated source fixture rejected", "odd zero parameter singular",
            "characteristic two permits abstract commuting blocks",
            "characteristic three admits reversed support-only banks but fails native prefixes"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    result = {"gram": gram_checks(), "products": rank_one_product_checks(),
              "char3_witness": characteristic_three_witness(), "source": root_check(args.source),
              "controls": fault_controls(args.source)}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_INDEPENDENT_ENDPOINT_FACE_REVIEW")


if __name__ == "__main__":
    main()
