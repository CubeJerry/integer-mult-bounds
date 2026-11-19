#!/usr/bin/env python3
"""Finite rank controls and exact degree receipt for common-row bank rank."""
from argparse import ArgumentParser
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json


def need(value, explanation):
    if not value:
        raise AssertionError(explanation)


def rank(rows):
    pivots = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p not in pivots:
                pivots[p] = value
                break
            value ^= pivots[p]
    return len(pivots)


# GF(4)=F2[omega]/(omega^2+omega+1), in the basis(1,omega).
MUL = {0: [0, 0], 1: [1, 2], 2: [2, 3], 3: [3, 1]}


def verify_102_movement_threshold():
    powers = {}
    def bound(d):
        if d not in powers:
            scale = 10**35
            with localcontext() as context:
                context.prec = 90
                low = int(scale*Decimal(d)**(Decimal(199)/200))
            exact = d**199 * scale**200
            need(low**200 <= exact <(low+1)**200, "exact movement root enclosure")
            powers[d] = F(low, scale), F(low+(low**200 != exact), scale)
        return powers[d]
    def combine(*terms):
        result = {}
        for c, v in terms:
            for d, count in v.items():
                result[d] = result.get(d, F(0))+c*count
        return result
    def interval(v):
        lower = upper = F(0)
        for d, c in v.items():
            low, high = bound(d)
            lower += c*(low if c >=0 else high)
            upper += c*(high if c >=0 else low)
        return lower, upper
    n = {1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    h = {2:1,4:25,6:1,8:410}
    q = {1:F(4451,8),2:F(7213,16),4:24,8:9+F(102,5760)}
    p2 = combine((36,n),(1,{1:444}),(1,{7*j:444 for j in range(1,9)}))
    t2 = combine((36,h),(1,{127:222}),(1,{1+7*j:444 for j in range(1,10)}))
    slope = interval(combine((F(1,2),t2),(-F(1,2),p2),(18,n),(-18,h),(-18,q)))
    need(slope[0]>0, "positive finite-m slope")
    gaps = {}
    for m in (90,92):
        gap = interval(combine((F(m,2),t2),(-F(m,2),p2),
                               (18*(m-1),n),(-18*(m-1),h),(-18*(m-1),q)))
        gaps[str(m)] = [str(x) for x in gap]
        need(gap[1]<0 if m==90 else gap[0]>0, "exact adjacent even-m boundary")
    return {"first_even_m":92,"gap_intervals":gaps,"slope_interval":[str(x) for x in slope]}


def native_block(o, i, j, b, k, lower_shears):
    if not(o[i] >> j & 1):
        return [0] * (2*b)
    rows = [0] * (2*b)
    for target in range(b):
        for source in range(b):
            coefficient = (1 if target < k else 2) if target == source else 0
            if lower_shears and target >= k and source < k:
                coefficient ^= (127*i + 37*j + 7*target + source) % 4
            for bit in range(2):
                rows[2*target+bit] ^= MUL[coefficient][bit] << (2*source)
    return rows


def run_control(o, b, k):
    n = 111*b*2
    rows = [1 << i for i in range(n)]
    foreign = 0
    for i in range(111):
        for j in range(111):
            block = native_block(o, i, j, b, k, True)
            if o[i] >> j & 1:
                foreign += 1
                need(rank(block) == 2*b, "every foreign block is invertible")
                need(block[:2*k] == [1 << p for p in range(2*k)],
                     "all common rows, including every input column")
                need(rank([row ^ (1 << t) for t, row in enumerate(block)]) == 2*(b-k),
                     "every foreign block has maximal remaining defect")
            else:
                need(all(x == 0 for x in block), "proper support preserved")
            for local_row, bits in enumerate(block):
                rows[i*2*b+local_row] ^= bits << (j*2*b)
    actual = rank(rows)
    expected = 2*(9*k+111*(b-k))
    need(actual == expected, "exact common-row bank-rank envelope")
    need(foreign == 6470, "complete native foreign census")
    # A shear-free omega->1 replacement has only the canonical rank in its
    # bad-coordinate submatrix; it fails the needed invertibility condition.
    bad = [row ^ (1 << i) for i, row in enumerate(o)]
    need(rank(bad) == 9, "omega->1 negative control has rank9, not111")
    matrix_hash = sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()
    return {"bank_field_width": b, "common_field_rows": k,
            "binary_rank": actual, "field_rank": actual//2,
            "upper_envelope_field_rank": expected//2,
            "lower_left_shears": True, "foreign_blocks_checked": foreign,
            "all_foreign_blocks_invertible": True,
            "global_binary_matrix_sha256": matrix_hash,
            "physical_balanced_realization_claimed_for_this_fixture": False}


def main():
    parser = ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    native = None
    for pin in pins["sources"]:
        raw = (args.repo/pin["path"]).read_bytes()
        if pin["uncompressed"]:
            raw = gzip.decompress(raw)
        need(sha256(raw).hexdigest() == pin["sha256"], "source pin "+pin["path"])
        if pin["path"].endswith("LAYOUT.json.gz"):
            native = json.loads(raw)["root_table"][:111]
    need(native is not None, "authenticated native layout available")
    o = [sum(1 << j for j, y in enumerate(native)
             if sum(a*b for a, b in zip(x, y)) == 0) for x in native]
    need(rank([row^(1 << i) for i, row in enumerate(o)]) == 9, "native canonical rank9")
    need(sum(row.bit_count() for row in o) == 6470, "native edge count")
    cases = [run_control(o, b, k) for b, k in [(1, 0), (2, 1), (3, 1), (3, 2), (4, 2)]]
    q = 9*70 +111*5690
    degree = (111+6470)*5760+111*5690
    all_degree = degree+6470*5690
    need(q == 632220 and q-9*5760 == 580380, "actual-family maximal bank rank")
    need(degree == 38538150 and all_degree == 75352450 and all_degree <2**30,
         "common-field degree sufficient for all simultaneous factors")
    result = {"status": "PASS_COMMON_ROW_BANK_RANK_ENVELOPE",
              "baseline": pins["baseline"], "finite_controls": cases,
              "actual_seventy_family_existence": {
                  "bank_width": 5760, "common_rows": 70,
                  "replacement_bank_rank": q, "excess_above_nine_banks": q-9*5760,
                  "basic_joint_polynomial_degree": degree,
                  "including_all_maximal_edge_defects_degree": all_degree,
                  "field_size": 2**30,
                  "coefficient_table_materialized": False},
              "hypothetical_5759_row_code": {
                  "replacement_rank_upper_bound": 9*5760+102,
                  "movement_threshold": verify_102_movement_threshold(),
                  "actual_source_constructed": False},
              "new_complete_kappa": False,
              "full_supplier_admitted": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(result["status"])
    print(json.dumps({"finite_native_cases": len(cases), "actual_family_q": q,
                      "actual_family_excess": q-9*5760, "degree": all_degree}))


if __name__ == "__main__":
    main()
