#!/usr/bin/env python3
"""Independent all-column/rational-chart review. No author checker imports."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sympy as sp

ROOT_PATH = "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
ROOT_SHA256 = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
DONORS = [16, 19, 38, 49, 50, 56, 57]
SCALE = 1 << 160

def need(test, why):
    if not test:
        raise ValueError(why)

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def binary_basis(rows):
    out = {}
    for j, value in enumerate(rows):
        tag = 1 << j
        while value:
            pivot = value.bit_length() - 1
            if pivot in out:
                value ^= out[pivot][0]
                tag ^= out[pivot][1]
            else:
                out[pivot] = (value, tag)
                break
    return out

def solve(basis, target):
    tag = 0
    while target:
        k = target.bit_length() - 1
        if k not in basis:
            return None
        target ^= basis[k][0]
        tag ^= basis[k][1]
    return tag

def combination(rows, tag):
    out = 0
    for j, row in enumerate(rows):
        if tag >> j & 1:
            out ^= row
    return out

def support(row, n=111):
    return [j for j in range(n) if row >> j & 1]

def chart_basis(chart):
    rows = chart["rows"]
    need(all(len(row) == 8 for row in rows), "chart ambient dimension is not eight")
    need(chart["kind"] in ("ann", "span"), "unknown chart kind")
    M = sp.Matrix(rows) if rows else sp.zeros(0, 8)
    if chart["kind"] == "span":
        return tuple(tuple(x) for x in M.rowspace())
    return tuple(tuple(x) for x in M.nullspace())

def replay(word, roots):
    charts = {name: chart_basis(chart) for name, chart in word["charts"].items()}
    dims = {name: len(basis) for name, basis in charts.items()}
    @lru_cache(None)
    def contained(a, b):
        aa, bb = charts[a], charts[b]
        joined = aa + bb
        return (sp.Matrix(joined).rank() if joined else 0) == len(bb)
    need(dims["Hub"] == 8 and dims["zero"] == 0, "incorrect extreme charts")
    for j, root in enumerate(roots):
        need(dims[f"L{j}"] == 1 and dims[f"F{j}"] == 7, "root/facet dimension")
        need(chart_basis({"kind": "span", "rows": [root]}) == charts[f"L{j}"], "input root mismatch")
        need(chart_basis({"kind": "ann", "rows": [root]}) == charts[f"F{j}"], "output facet mismatch")
    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = [(dot(roots[72], root) // 2 + dot(omitted, root) // 2) % 2 for root in roots]
    W = [sum(1 << j for j, r in enumerate(roots)
             if h[j] == h[i] and (j == i or dot(r, roots[i]) == 0)) for i in range(111)]
    need(len(binary_basis(W)) == 15, "native W rank")
    values = {f"X{j}": 1 << j for j in range(111)}
    values.update({f"Y{j}": 1 << (111 + j) for j in range(111)})
    places = {f"X{j}": f"L{j}" for j in range(111)}
    places.update({f"Y{j}": "zero" for j in range(111)})
    owned, born = set(), set()
    packets = {f"P{j}" for j in range(8)}
    paths = {name: [] for name in packets}
    seed_reads = {name: [] for name in packets}
    seed_rows = {}
    counts, moves = Counter(), Counter()
    peak = dirty_clears = 0
    history, history_events, exchange, captures = [], [], [], []
    snapshots = {}
    completed = set(word["completed_targets"])
    need(completed == {9, 17, 34}, "review is scoped to completed targets9/17/34")
    def check_originals_restored():
        for j in range(111):
            need(values[f"X{j}"] == 1 << j and places[f"X{j}"] == "Hub", "original X not restored at Hub")
    for number, op in enumerate(word["operations"], 1):
        kind, name, *rest = op
        counts[kind] += 1
        changed_packet = None
        if kind == "INIT":
            need(name not in values and name not in born, "duplicate or reborn owner")
            need(len(rest) == 1 and rest[0] in charts, "unknown INIT chart")
            values[name], places[name] = 0, rest[0]
            owned.add(name)
            born.add(name)
            peak = max(peak, len(owned))
            if name in packets:
                check_originals_restored()
                need(rest[0] == "Hub", "packet not Hub-born")
                paths[name].append(dims[rest[0]])
        elif kind == "ADD":
            need(len(rest) == 1, "ADD arity")
            target = rest[0]
            need(name in values and target in values, "ADD on dead record")
            need(name != target, "self-ADD")
            need(contained(places[name], places[target]) and contained(places[target], places[name]), "noncochart ADD")
            if target in packets and places[target] == "Hub":
                need(name.startswith("X") and name[1:].isdigit(), "seed reads an unaccounted source")
                check_originals_restored()
                seed_reads[target].append(int(name[1:]))
            values[target] ^= values[name]
            if target in packets:
                changed_packet = target
            if (name == "P4" and target in {"Y9", "Y17", "Y34"}) or (target == "P4" and name in {"Y9", "Y17", "Y34"}):
                exchange.append({"operation_index": number - 1, "operation": op, "Y9": hex(values["Y9"]), "Y17": hex(values["Y17"]), "Y34": hex(values["Y34"]), "P4": hex(values["P4"]), "chart": places["P4"]})
            if target in {"PAIR_C17", "TRIPLE_C9"}:
                captures.append({"operation_index": number - 1, "source": name, "target": target, "source_row": hex(values[name]), "target_row": hex(values[target]), "chart": places[target]})
        elif kind == "MOVE":
            need(len(rest) == 1 and name in values, "MOVE arity/live record")
            dest, src = rest[0], places[name]
            need(dest in charts, "unknown MOVE destination")
            need(contained(dest, src) if name in owned else contained(src, dest), "nonmonotone MOVE")
            delta = abs(dims[src] - dims[dest])
            need(delta > 0, "zero-rank MOVE")
            moves[delta] += 1
            if name in packets:
                if src == "Hub":
                    need(name not in seed_rows, "packet returned to Hub")
                    seed_rows[name] = values[name]
                paths[name].append(dims[dest])
                changed_packet = name
            places[name] = dest
        elif kind == "CLEAR":
            need(not rest and name in owned, "CLEAR requires live owner")
            dirty_clears += bool(values[name])
            owned.remove(name)
            del values[name], places[name]
        else:
            raise ValueError(f"unknown opcode {kind}")
        if changed_packet is not None and places[changed_packet] != "Hub":
            history.append(values[changed_packet])
            history_events.append({"after_operation": number, "packet": changed_packet,
                                   "chart": places[changed_packet], "row_hex": hex(values[changed_packet])})
        for marker, count in word["markers"].items():
            if number == count:
                check_originals_restored()
                snapshots[marker] = {"owned": {name: {"chart": places[name], "value_hex": hex(values[name])} for name in sorted(owned)},
                                     "counts": dict(counts), "profile": dict(moves)}
                if marker == "Y_correction_prepared":
                    m34 = sum(1 << j for j, r in enumerate(roots) if h[j] == 1 and dot(r, roots[34]) == 0)
                    need(values["Y34"] == (1 << 145) ^ (1 << 17) ^ (1 << 9) ^ m34 and places["Y34"] == "F34", "first serial receiver not correctly prepared")
                    need(values["Y17"] == (1 << 128) ^ (1 << 145) ^ (1 << 9) and places["Y17"] == "PAIR_K", "second serial receiver not correctly prepared")
                    need(values["Y9"] == (1 << 120) ^ (1 << 128) ^ (1 << 145) and places["Y9"] == "TRIPLE_K", "third serial receiver not correctly prepared")
    check_originals_restored()
    need(set(snapshots) == set(word["markers"]), "unreached marker")
    need(snapshots["handoff"]["owned"] == word["expected_owned_at_handoff"], "handoff owner payload mismatch")
    need(paths == word["expected_packet_paths"], "packet path metadata mismatch")
    need([seed_rows[f"P{i}"] for i in range(8)] == [int(x, 16) for x in word["initial_seed_rows_hex"]], "seed metadata mismatch")
    m34 = sum(1 << j for j, r in enumerate(roots) if h[j] == 1 and dot(r, roots[34]) == 0)
    need(seed_rows["P4"] == (1 << 34) ^ (1 << 17) ^ (1 << 9) ^ m34, "P4 is not the stated serial seed")
    need(seed_reads["P4"] == support(seed_rows["P4"]), "serial seed has hidden or repeated source reads")
    need(captures == [{"operation_index": item["operation_index"], "source": "X17" if item["target"] == "PAIR_C17" else "X9", "target": item["target"], "source_row": hex(1 << (17 if item["target"] == "PAIR_C17" else 9)), "target_row": hex(1 << (17 if item["target"] == "PAIR_C17" else 9)), "chart": "F34" if item["target"] == "PAIR_C17" else "PAIR_K"} for item in captures] and len(captures) == 2, "source capture is not pure and chronological")
    for j in range(111):
        expected = (1 << (111 + j)) ^ ((1 << j) if j in completed else 0)
        destination = f"F{j}" if word["closed_partial"] or j in completed else "zero"
        need(values[f"Y{j}"] == expected, "incorrect original Y endpoint")
        need(places[f"Y{j}"] == destination, "incorrect original Y destination")
    need(len(owned) == (0 if word["closed_partial"] else len(born)), "owned endpoint mismatch")
    history_basis = binary_basis(history)
    witnesses = []
    for i, row in enumerate(W):
        tag = solve(history_basis, row)
        need(tag is not None, "native W missing from actual packet history")
        need(combination(history, tag) == row, "invalid independently derived W witness")
        witnesses.append({"receiver": i, "history_indices": support(tag, len(history))})
    y_rank = len(binary_basis([row >> 111 for row in history]))
    terminal = [int(snapshots["handoff"]["owned"][f"P{i}"]["value_hex"], 16) for i in range(8)]
    need(not any(row >> 111 for row in terminal), "terminal public-y contamination")
    need(len(binary_basis(terminal)) == 8, "terminal packet rank is not eight")
    masks = [sum(1 << j for j, r in enumerate(roots) if dot(r, roots[i])) for i in range(111)]
    fitted = [i for i, mask in enumerate(masks) if solve(binary_basis([row & mask for row in terminal]), 1 << i) is not None]
    G = terminal + [1 << j for j in DONORS]
    donor_fitted = [i for i, mask in enumerate(masks) if solve(binary_basis([row & mask for row in G]), 1 << i) is not None]
    W_terminal_intersection = 15 + 8 - len(binary_basis(W + terminal))
    return {"status": "PASS_INDEPENDENT_SERIAL_POINT_WORD", "all_original_columns": 222,
            "closed_partial": word["closed_partial"], "coupled": word["coupled"],
            "completed_targets": sorted(completed), "counts": dict(counts),
            "movement_profile": dict(sorted(moves.items())), "rank_length": sum(r * n for r, n in moves.items()),
            "owned_peak": peak, "live_owned": len(owned), "dirty_clears": dirty_clears,
            "seed_source_reads": seed_reads, "initial_seed_rank": len(binary_basis(seed_rows.values())),
            "packet_paths": paths, "history_dimension": len(history_basis),
            "history_public_y_rank": y_rank, "history_pure_X_dimension": len(history_basis) - y_rank,
            "history_W_intersection": 15, "terminal_rank": 8,
            "terminal_W_intersection": W_terminal_intersection, "terminal_fitted_roles_with_free_local_corrections": fitted,
            "terminal_plus_donors_rank": len(binary_basis(G)),
            "terminal_plus_donors_fitted_roles_with_free_local_corrections": donor_fitted,
            "exchange": exchange, "source_captures": captures, "new_complete_kappa": False,
            "history_events": history_events, "independent_W_witnesses": witnesses}

def iroot(n, k):
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // pow(x, k - 1)) // k
        if y >= x:
            break
        x = y
    while pow(x, k) > n:
        x -= 1
    while pow(x + 1, k) <= n:
        x += 1
    return x

@lru_cache(None)
def power(rank):
    integer = pow(rank, 199) * pow(SCALE, 200)
    low = iroot(integer, 200)
    need(pow(low, 200) <= integer < pow(low + 1, 200), "directed power invariant")
    return F(low, SCALE), F(low if pow(low, 200) == integer else low + 1, SCALE)

def add(*terms):
    result = Counter()
    for coefficient, profile in terms:
        for rank, count in profile.items():
            result[rank] += coefficient * count
    return dict(result)

def moment(profile):
    low = high = F(0)
    for rank, coefficient in profile.items():
        left, right = power(rank)
        low += coefficient * (left if coefficient >= 0 else right)
        high += coefficient * (right if coefficient >= 0 else left)
    return low, high

def encode(interval):
    left, right = interval
    with localcontext() as ctx:
        ctx.prec = 60
        ctx.rounding = ROUND_FLOOR
        a = str(Decimal(left.numerator) / Decimal(left.denominator))
        ctx.rounding = ROUND_CEILING
        b = str(Decimal(right.numerator) / Decimal(right.denominator))
    return {"lower": a, "upper": b,
            "lower_fraction": str(left), "upper_fraction": str(right)}

def invoice(profile):
    N = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    H = {2: 1, 4: 25, 6: 1, 8: 410}
    P2 = add((36, N), (444, {1: 1}), (444, {7*j: 1 for j in range(1, 9)}))
    T2 = add((36, H), (222, {127: 1}), (444, {1+7*j: 1 for j in range(1, 10)}))
    allowance = add((1, N), (-1, H), (F(1, 36), T2), (F(-1, 36), P2))
    displayed = {127: F(37, 6), 64: F(74, 6), 1: F(-74, 6)}
    for j in range(1, 9):
        displayed[1+7*j] = displayed.get(1+7*j, F(0)) + F(74, 6)
        displayed[7*j] = displayed.get(7*j, F(0)) - F(74, 6)
    need({r: v for r, v in allowance.items() if v} == displayed, "caller allowance cancellation")
    rows = []
    first_positive = None
    for m in range(2, 202, 2):
        paid = add((F(m, 2), P2), (-18*(m-1), N), (18*(m-1), profile))
        target = add((F(m, 2), T2), (-18*(m-1), H))
        margin = moment(add((1, target), (-1, paid)))
        if first_positive is None and margin[0] > 0:
            first_positive = m
        if m in (2, 4, 6, 8, 10, 12):
            rows.append({"m": m, "target_minus_paid": encode(margin), "strictly_positive": margin[0] > 0})
    return {"exponent": "199/200", "directed_method": "binary fixed-point scale2^160 and exact integer200th root",
            "moment": encode(moment(profile)), "limiting_allowance": encode(moment(allowance)),
            "limiting_room": encode(moment(add((1, allowance), (-1, profile)))),
            "finite_even_m_checks": rows, "first_positive_even_m_in_2_to_200": first_positive,
            "scope": "movement-only necessary interface; all remaining supplier costs retained", "new_complete_kappa": False}

def drop_operation(word, index):
    del word["operations"][index]
    for marker, count in word["markers"].items():
        if count > index:
            word["markers"][marker] -= 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    data = (args.repo / ROOT_PATH).read_bytes()
    need(hashlib.sha256(data).hexdigest() == ROOT_SHA256, "root recovery bytes changed")
    root_doc = json.loads(data)
    roots = root_doc["native_roots"]
    if isinstance(roots, dict):
        roots = [roots[str(i)] for i in range(111)]
    need(len(roots) == 111 and all(dot(r, r) == 4 for r in roots), "native root list")
    words = sorted(args.package.glob("*WORD.json"))
    need(len(words) == 2, "expected exactly two frozen open/closed serial words")
    args.out.mkdir(parents=True, exist_ok=True)
    result = {"status": "PASS_INDEPENDENT_SERIAL_POINT_REVIEW", "source_recovery_sha256": ROOT_SHA256,
              "sympy_version": sp.__version__, "words": {}, "negative_controls": {}, "new_complete_kappa": False}
    selected_closed = None
    for path in words:
        word_bytes = path.read_bytes()
        word = json.loads(word_bytes)
        receipt = replay(word, roots)
        evidence = {"history_events": receipt.pop("history_events"), "independent_W_witnesses": receipt.pop("independent_W_witnesses")}
        evidence_path = args.out / (path.stem + "-HISTORY.json")
        evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        receipt["word_sha256"] = hashlib.sha256(word_bytes).hexdigest()
        receipt["history_evidence_sha256"] = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        if word["closed_partial"]:
            receipt["invoice"] = invoice(receipt["movement_profile"])
            if word["coupled"]:
                selected_closed = word
        result["words"][path.name] = receipt
    need(selected_closed is not None, "missing coupled closed word")
    controls = {
        "omit_first_ground_y_prefix": lambda op: op == ["ADD", "Y34", "Y17"],
        "omit_second_ground_y_prefix": lambda op: op == ["ADD", "Y17", "Y9"],
        "omit_actual_x17_capture": lambda op: op == ["ADD", "X17", "PAIR_C17"],
        "omit_actual_x9_capture": lambda op: op == ["ADD", "X9", "TRIPLE_C9"],
        "omit_first_feedback": lambda op: op == ["ADD", "Y34", "P4"],
        "omit_second_feedback": lambda op: op == ["ADD", "Y17", "P4"],
        "omit_second_y_mask_retirement": lambda op: op == ["ADD", "YM17", "P4"],
        "omit_dirty_owner_retirement": lambda op: op == ["CLEAR", "R0"],
        "omit_last_receiver_delivery": lambda op: op == ["ADD", "P4", "Y9"],
    }
    for label, match in controls.items():
        mutated = copy.deepcopy(selected_closed)
        index = next(i for i, op in enumerate(mutated["operations"]) if match(op))
        drop_operation(mutated, index)
        try:
            replay(mutated, roots)
        except (ValueError, KeyError) as error:
            result["negative_controls"][label] = {"rejected": True, "reason": str(error)}
        else:
            raise ValueError("accepted semantic mutant: " + label)
    mutant = copy.deepcopy(selected_closed)
    index = next(i for i, op in enumerate(mutant["operations"]) if op == ["MOVE", "Y34", "F34"])
    mutant["operations"][index][2] = "Hub"
    try:
        replay(mutant, roots)
    except (ValueError, KeyError) as error:
        result["negative_controls"]["pretend_hub_receiver_is_at_F34"] = {"rejected": True, "reason": str(error)}
    else:
        raise ValueError("accepted wrong-chart receiver")
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "words": list(result["words"]),
                      "negative_controls": len(result["negative_controls"]), "new_complete_kappa": False}, sort_keys=True))

if __name__ == "__main__":
    main()
