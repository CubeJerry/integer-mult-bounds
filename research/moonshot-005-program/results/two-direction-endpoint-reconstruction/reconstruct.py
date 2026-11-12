#!/usr/bin/env python3
"""Reconstruct and audit the interrupted two-direction endpoint candidate.

Independent S008 implementation from the published S007 reconstruction
specification. It imports no predecessor scientific Python. Source operations
and the retained normalized MOVE/owned-erasure contract are explicit inputs.
Prepared for CubeJerry with OpenAI assistance; Apache-2.0.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path
import time

SOURCE_PIN = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
INVOICE_PIN = "b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248"
HISTORICAL_WORD_PIN = "306984ce47b7d5827704ad6b813e45d681087f33c66538d3d5a6c901cc0b5147"

def need(test, why):
    if not test:
        raise ValueError(why)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def span(basis):
    out = {0}
    for v in basis:
        out |= {x ^ v for x in tuple(out)}
    return frozenset(out)

def addto(dst, src, scalar=Q(1)):
    need(dst is not src, "distinct row operands")
    for j, value in src.items():
        value = dst.get(j, Q(0)) + scalar * value
        if value:
            dst[j] = value
        else:
            dst.pop(j, None)

def root(v):
    """Integer coordinates, derived directly from the four published cases."""
    support = {i for i in range(9) if v & (1 << i)}
    if len(support) == 3:
        if 8 in support:
            return [2 if i in support else 0 for i in range(8)]
        return [1 if i in support else -1 for i in range(8)]
    need(len(support) == 7, "E8 port weight")
    i, j = sorted(set(range(9)) - support)
    if j == 8:
        return [1 if k == i else -1 for k in range(8)]
    return [2 * (int(k == i) - int(k == j)) for k in range(8)]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def rref_rank(rows):
    pivots = {}
    for row in rows:
        cur = {j: Q(x) for j, x in enumerate(row) if x}
        while cur:
            j = min(cur)
            if j not in pivots:
                s = cur[j]
                pivots[j] = {k: x / s for k, x in cur.items()}
                break
            addto(cur, pivots[j], -cur[j])
    return len(pivots)

def inverse(a):
    n = len(a)
    rows = [[Q(x) for x in row] + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    det = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        need(pivot is not None, "invertible square matrix")
        if pivot != j:
            rows[pivot], rows[j] = rows[j], rows[pivot]
            det = -det
        value = rows[j][j]
        det *= value
        rows[j] = [x / value for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                c = rows[i][j]
                rows[i] = [x - c * y for x, y in zip(rows[i], rows[j])]
    return [r[n:] for r in rows], det

def sets(w):
    xs = sorted(w["live"])
    dports = set(w["hosted"]["Dports"])
    coupled = sorted(set(range(104)) - dports)
    forward_y = [x + 112 for x in xs]
    byport = {i: (x, y) for i, x, y in zip(w["hosted"]["Dports"], w["hosted"]["X2"], w["hosted"]["Y2"])}
    reverse_x = [byport[i][0] if i in dports else xs[i] for i in range(104)]
    reverse_y = [byport[i][1] if i in dports else forward_y[i] for i in range(104)]
    xall = sorted(set(xs) | set(w["hosted"]["X2"]))
    yall = sorted(set(forward_y) | set(w["hosted"]["Y2"]))
    mains = sorted(set(xall) | set(yall))
    need(len(xs) == 104 and len(xall) == len(yall) == 200 and len(mains) == 400, "main partition")
    need(len(coupled) == 8 and set(xall).isdisjoint(yall), "coupled and X/Y partition")
    roots = [root(w["frames"][w["initial"][r]][0]) for r in xs]
    gram = [[Q(dot(a, b), 8) for b in roots] for a in roots]
    need(all(gram[i][i] == 1 for i in range(104)), "normalized Gram diagonal")
    need(rref_rank(roots) == 8 and rref_rank(gram) == 8, "rank-eight code")
    need(sum(bool(x) for row in roots for x in row) == 520, "actual encoder support")
    return xs, forward_y, reverse_x, reverse_y, xall, yall, mains, coupled, roots, gram

def exact_native_target(w):
    rows = {i: {i: Q(1)} for i in range(w["public"])}
    xs, fy, rx, ry, _, _, _, coupled, _, _ = sets(w)
    for i, x in enumerate(xs):
        rows[fy[i]] = {fy[i]: Q(1, 2) if i in coupled else Q(1),
                       x: Q(1, 2) if i in coupled else Q(1)}
    for x, y in zip(rx, ry):
        rows[x] = {x: Q(1), y: Q(-1)}
    return rows

def symbolic_walk(w, word, verify_copy=True):
    spaces = list(map(span, w["frames"]))
    rows = {i: {i: Q(1)} for i in range(word["public"])}
    loc = dict(enumerate(word["initial"]))
    counts, ranks = Counter(), Counter()
    peak = lifetimes = copies = 0
    all_pairs = set()
    for event, op in enumerate(word["program"]):
        kind, dst = op[:2]
        counts[kind] += 1
        need(0 <= dst < word["public"] + word["owned_fields"], f"role bound at {event}")
        if kind == "INIT":
            need(dst >= word["public"] and dst not in loc, f"fresh owned at {event}")
            rows[dst] = {}
            loc[dst] = op[2]
            lifetimes += 1
        elif kind == "CLEAR":
            need(dst >= word["public"] and loc.get(dst) == op[2], f"owned erasure at {event}")
            del rows[dst], loc[dst]
        elif kind == "MOVE":
            a, b, owned = op[2:]
            need(type(owned) is bool and owned == (dst >= word["public"]) and loc.get(dst) == a, f"MOVE type at {event}")
            need(spaces[a] < spaces[b] or owned and spaces[b] < spaces[a], f"nested MOVE at {event}")
            rank = abs(len(w["frames"][b]) - len(w["frames"][a]))
            need(rank > 0, "positive MOVE rank")
            ranks[rank] += 1
            all_pairs.add((a, b))
            loc[dst] = b
        elif kind in ("ADD", "COPY"):
            src, scalar, chart = op[2:]
            need(dst != src and loc.get(dst) == loc.get(src) == chart and Q(scalar), f"cochart ADD at {event}")
            if kind == "COPY":
                need(not verify_copy or not rows[dst], "COPY destination is zero on all inputs")
                copies += 1
            addto(rows[dst], rows[src], Q(scalar))
        elif kind == "SCALE":
            need(loc.get(dst) == op[3] and Q(op[2]), f"typed nonzero SCALE at {event}")
            rows[dst] = {j: Q(op[2]) * x for j, x in rows[dst].items()}
        else:
            raise ValueError("unsupported operation " + kind)
        peak = max(peak, len(loc) - word["public"])
    need(set(rows) == set(range(word["public"])), "all owned records retired")
    return rows, loc, {"counts": dict(sorted(counts.items())), "move_histogram": dict(sorted(ranks.items())),
                       "peak_owned": peak, "owned_lifetimes": lifetimes, "copy_guards": copies,
                       "map_pairs": sorted(all_pairs)}

def build(w):
    xs, fy, rx, ry, xall, yall, mains, coupled, roots, gram = sets(w)
    private = {r: 1480 + i for i, r in enumerate(mains)}
    qlabel = {0: "common", 1: "difference"}
    ops, marks = [], []
    def emit(op, purpose):
        marks.append({"event": len(ops), "purpose": purpose})
        ops.append(op)
    for r in mains:
        emit(["ADD", private[r], r, "-1", w["initial"][r]], "input_difference")
    for r in range(1480):
        if r not in private:
            emit(["MOVE", r, w["initial"][r], w["final"][r], False], "direct_helper_identity")
    pass_marks = []
    for bank in (0, 1):
        physical = lambda r: r if bank == 0 else private[r]
        start = len(ops)
        # Retain original reverse Y values before either coupled input changes.
        for k in range(8):
            packet = 1880 + k
            emit(["INIT", packet, 3], "reverse_init")
            for r, a in zip(ry, roots):
                if a[k]:
                    emit(["ADD", packet, physical(r), str(a[k]), 3], "reverse_encode_original_Y")
        for r in xall:
            emit(["MOVE", physical(r), w["initial"][r], w["final"][r], False], "direct_X")
        for i in coupled:
            emit(["SCALE", physical(fy[i]), "1/2", 3], "coupled_Y_normalization")
        for k in range(8):
            packet = 1888
            emit(["INIT", packet, 127], "forward_init")
            for r, a in zip(xs, roots):
                if a[k]:
                    emit(["ADD", packet, physical(r), str(a[k]), 127], "forward_encode_original_X")
            emit(["MOVE", packet, 127, 3, True], "forward_rank9")
            for i, (r, a) in enumerate(zip(fy, roots)):
                if a[k]:
                    c = Q(1, 2) if i in coupled else Q(1)
                    emit(["ADD", physical(r), packet, str(c * a[k] / 8), 3], "forward_decode")
            emit(["CLEAR", packet, 3], "forward_retirement")
        for k in range(8):
            packet = 1880 + k
            emit(["MOVE", packet, 3, 127, True], "reverse_rank9")
            for r, a in zip(rx, roots):
                if a[k]:
                    emit(["ADD", physical(r), packet, str(-Q(a[k], 8)), 127], "reverse_decode")
            emit(["CLEAR", packet, 127], "reverse_retirement")
        for r in yall:
            emit(["MOVE", physical(r), w["initial"][r], w["final"][r], False], "direct_Y")
        pass_marks.append({"bank": qlabel[bank], "start": start, "stop": len(ops)})
    for r in mains:
        emit(["ADD", private[r], r, "1", w["final"][r]], "output_recoupling")
    return {"schema": "moonshot-two-direction-endpoint-S008-v1", "source_sha256": SOURCE_PIN,
            "public": 1880, "owned_fields": 9, "initial": w["initial"] + [w["initial"][r] for r in mains],
            "final": w["final"] + [w["final"][r] for r in mains],
            "difference_role_map": {str(r): p for r, p in private.items()}, "program": ops,
            "marks": marks, "bank_passes": pass_marks,
            "scope": "Partial exact endpoint code; all residual correction and supplier obligations remain."}, private

def approx_map(w):
    xs, fy, rx, ry, _, _, mains, coupled, _, p = sets(w)
    rows = {r: {r: Q(1)} for r in mains}
    for i, y in enumerate(fy):
        c = Q(1, 2) if i in coupled else Q(1)
        rows[y] = {y: c}
        for j, x in enumerate(xs):
            if p[i][j]:
                addto(rows[y], {x: Q(1)}, c * p[i][j])
    for i, x in enumerate(rx):
        rows[x] = {x: Q(1)}
        for j, y in enumerate(ry):
            if p[i][j]:
                addto(rows[x], {y: Q(1)}, -p[i][j])
    return rows

def verify_main_inverse(w, a):
    xs, fy, rx, ry, _, _, mains, coupled, _, p = sets(w)
    hosted = sorted(set(range(104)) - set(coupled))
    p0 = [[p[i][j] for j in coupled] for i in coupled]
    bmat = [[Q(i == j) + sum(p0[i][k] * p0[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
    inv, det = inverse(bmat)
    need(det == Q(1384497, 4096), "recorded coupled inverse determinant")
    # Symbolic inverse in final-output coordinates; unaffected hosted rows first.
    recovered = {xs[i]: {xs[i]: Q(1)} for i in hosted}
    recovered.update({ry[i]: {ry[i]: Q(1)} for i in hosted})
    avec, bvec = [], []
    for i in coupled:
        ar = {xs[i]: Q(1)}
        br = {fy[i]: Q(2)}
        for j in hosted:
            if p[i][j]:
                addto(ar, recovered[ry[j]], p[i][j])
                addto(br, recovered[xs[j]], -p[i][j])
        avec.append(ar); bvec.append(br)
    rhs = []
    for i in range(8):
        row = bvec[i].copy()
        for j in range(8):
            if p0[i][j]:
                addto(row, avec[j], -p0[i][j])
        rhs.append(row)
    for i, port in enumerate(coupled):
        yr = {}
        for j in range(8):
            if inv[i][j]:
                addto(yr, rhs[j], inv[i][j])
        recovered[fy[port]] = yr
    for i, port in enumerate(coupled):
        xr = avec[i].copy()
        for j, qport in enumerate(coupled):
            if p0[i][j]:
                addto(xr, recovered[fy[qport]], p0[i][j])
        recovered[xs[port]] = xr
    # All remaining hosted reverse X and forward Y follow from recovered opposite banks.
    for i in hosted:
        row = {rx[i]: Q(1)}
        for j in range(104):
            if p[i][j]:
                addto(row, recovered[ry[j]], p[i][j])
        recovered[rx[i]] = row
        row = {fy[i]: Q(1)}
        for j in range(104):
            if p[i][j]:
                addto(row, recovered[xs[j]], -p[i][j])
        recovered[fy[i]] = row
    need(set(recovered) == set(mains), "all400 inverse rows")
    for r, expression in recovered.items():
        row = {}
        for j, coefficient in expression.items():
            addto(row, a[j], coefficient)
        need(row == {r: Q(1)}, "exact all-input inverse row " + str(r))
    return {"inverse_rows": 400, "coupled_matrix_determinant": str(det),
            "scope": "Rational information inverse, not a free physical inverse."}

def power_bracket(rank):
    scale = 10 ** 32
    target = rank ** 199 * scale ** 200
    lo, hi = 0, rank * scale + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, "integer power certificate")
    return Q(lo, scale), Q(lo if lo ** 200 == target else lo + 1, scale)

def signed_interval(hist):
    lo = hi = Q(0)
    for rank, count in hist.items():
        a, b = power_bracket(rank)
        lo += count * (a if count >= 0 else b)
        hi += count * (b if count >= 0 else a)
    return lo, hi

def complete_invoice(w, word, invoice, bill):
    old_native = Counter(abs(len(w["frames"][op[3]]) - len(w["frames"][op[2]])) for op in w["program"] if op[0] == "MOVE")
    mains = set(sets(w)[6])
    old_raw = Counter(abs(len(w["frames"][op[3]]) - len(w["frames"][op[2]])) for op in w["program"] if op[0] == "MOVE" and op[1] in mains)
    new_native = Counter({int(r): c for r, c in bill["move_histogram"].items()})
    target = {int(r): c for r, c in invoice["T4"].items()}
    oldpaid = {int(r): c for r, c in invoice["P4"].items()}
    paid = {r: oldpaid.get(r, 0) + 18 * (new_native[r] - old_native[r] - old_raw[r])
            for r in oldpaid.keys() | new_native.keys() | old_native.keys() | old_raw.keys()}
    need(all(c >= 0 for c in paid.values()), "nonnegative full paid histogram")
    need(sum(paid.values()) == 42480 and sum(target.values()) == 27344, "complete paid/target counts")
    surplus = sum(r * (target.get(r, 0) - paid.get(r, 0)) for r in target.keys() | paid.keys())
    need(surplus == 1888, "full rank surplus")
    interval = tuple(x / 18 for x in signed_interval({r: target.get(r, 0) - paid.get(r, 0) for r in target.keys() | paid.keys()}))
    need(14 < interval[0] <= interval[1] < 15, "14-additional-positive-rank-call ceiling")
    return {"old_common_native_MOVE_histogram": dict(sorted(old_native.items())),
            "old_raw_main_MOVE_histogram": dict(sorted(old_raw.items())),
            "new_complete_native_MOVE_histogram": dict(sorted(new_native.items())),
            "formula": "P_new = P4 + 18 * (P_candidate_native - P_original_common_native - P_original_raw_main)",
            "paid_histogram": dict(sorted(paid.items())), "target_histogram": dict(sorted(target.items())),
            "paid_positions": sum(paid.values()), "target_positions": sum(target.values()),
            "rank_surplus": surplus, "remaining_paid_moment_per_native_bounds": list(map(str, interval)),
            "remaining_paid_moment_approximate": float(interval[0]), "strict_additional_positive_rank_call_ceiling": 14,
            "reconstruction_formula_correction": "S007 prose defines C_native as common-public and R_old as owned, omitting the old raw-main subtraction. Its reported numeric bill matches this corrected whole-word difference.",
            "scope": "Conditional complete H4 histogram for a partial native; not complete supplier admission."}

def main(args):
    args.outdir.mkdir(parents=True, exist_ok=True)
    native_bytes = args.source.read_bytes()
    need(digest(native_bytes) == SOURCE_PIN, "authenticated native")
    invoice_bytes = args.invoice.read_bytes()
    need(digest(invoice_bytes) == INVOICE_PIN, "authenticated H4 invoice")
    w = json.loads(gzip.decompress(native_bytes))
    invoice = json.loads(invoice_bytes)
    need(w["public"] == 1480 and len(w["program"]) == 71261, "source dimensions")
    start = time.monotonic()
    word, private = build(w)
    rows, loc, bill = symbolic_walk(w, word)
    local = approx_map(w)
    expected = {i: {i: Q(1)} for i in range(1480)}
    expected.update(local)
    for r, p in private.items():
        expected[p] = {private[j]: c for j, c in local[r].items()}
    need(rows == expected, "full1880-input candidate endpoint map")
    need(loc == dict(enumerate(word["final"])), "all1880 exact final charts")
    need(bill["counts"] == {"ADD": 4960, "CLEAR": 32, "INIT": 32, "MOVE": 1912, "SCALE": 16}, "literal source counts")
    need(bill["peak_owned"] == 9 and bill["owned_lifetimes"] == 32, "actual owned lifetime bound")
    inverse_result = verify_main_inverse(w, local)
    target = exact_native_target(w)
    residual = {}
    for r in local:
        row = local[r].copy()
        addto(row, target[r], Q(-1))
        if row:
            residual[r] = row
    need(len(residual) == 208 and sum(map(len, residual.values())) == 9984, "per-copy residual rows and nonzeros")
    residual_full = {str(r): {str(j): str(c) for j, c in row.items()} for r, row in residual.items()}
    residual_full.update({str(private[r]): {str(private[j]): str(c) for j, c in row.items()} for r, row in residual.items()})
    # Mutation checks execute actual malformed words and test typing or exact endpoint.
    mutations = []
    for label, purpose, kind in [
        ("wrong_reverse_sign", "reverse_decode", "sign"),
        ("missing_reverse_MOVE", "reverse_rank9", "omit"),
        ("public_forward_descent", "forward_rank9", "public"),
        ("missing_coupled_scale", "coupled_Y_normalization", "omit"),
        ("missing_helper_route", "direct_helper_identity", "omit"),
        ("missing_input_difference", "input_difference", "omit"),
        ("missing_recoupling", "output_recoupling", "omit"),
    ]:
        event = next(m["event"] for m in word["marks"] if m["purpose"] == purpose)
        bad = dict(word, program=[op.copy() for op in word["program"]])
        if kind == "omit":
            del bad["program"][event]
        elif kind == "sign":
            bad["program"][event][3] = str(-Q(bad["program"][event][3]))
        else:
            bad["program"][event][4] = False
        try:
            rr, ll, _ = symbolic_walk(w, bad)
            need(rr == expected and ll == loc, "exact complete endpoint mismatch")
        except ValueError as err:
            mutations.append({"mutation": label, "event": event, "rejection": str(err)})
        else:
            raise ValueError("accepted mutant " + label)
    cost = complete_invoice(w, word, invoice, bill)
    payload = (json.dumps(word, sort_keys=True, separators=(",", ":")) + "\n").encode()
    compressed = gzip.compress(payload, mtime=0)
    (args.outdir / "WORD.json.gz").write_bytes(compressed)
    (args.outdir / "RESIDUALS.json.gz").write_bytes(gzip.compress((json.dumps(residual_full, sort_keys=True, separators=(",", ":")) + "\n").encode(), mtime=0))
    report = {"status": "PASS_RECONSTRUCTED_TWO_DIRECTION_PARTIAL_WORD", "source_sha256": SOURCE_PIN,
              "invoice_sha256": INVOICE_PIN, "word_payload_sha256": digest(payload),
              "word_compressed_sha256": digest(compressed), "historical_unavailable_word_sha256": HISTORICAL_WORD_PIN,
              "historical_word_bytes_reproduced": digest(compressed) == HISTORICAL_WORD_PIN,
              "reconstruction_scope": "New independent implementation of the preserved recipe; not byte recovery of missing S007 builder.",
              "independent_public_inputs": 1880, "instructions": len(word["program"]), "physical_word": bill,
              "information_inverse": inverse_result, "common_and_second_copy_decoupled": True,
              "all1080_helpers_identity_under_candidate": True,
              "unpaid_residual_rows_both_copies": 2 * len(residual),
              "unpaid_residual_coefficients_both_copies": 2 * sum(map(len, residual.values())),
              "invoice": cost, "negative_controls": mutations,
              "foundational_assumptions": ["native_all_columns", "owned_erasure", "compiler", "precision_tape", "analytic_recovery"],
              "source_full_map_audit": "Reported separately in SOURCE-AUDIT.json; this reconstruction does not substitute for that full-source audit.",
              "seconds": time.monotonic() - start,
              "classification": "Exact finite partial normalized word and conditional profile; no complete supplier or new kappa."}
    (args.outdir / "RESULT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "instructions", "independent_public_inputs", "unpaid_residual_coefficients_both_copies", "seconds")}, indent=2))
    print("remaining_moment", cost["remaining_paid_moment_approximate"], flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--invoice", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    main(parser.parse_args())

