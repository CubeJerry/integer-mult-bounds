#!/usr/bin/env python3
"""Independent integer-bit interpreter for the literal BIT exchange bus.

This does not import or invoke the retained word replay. It reconstructs all
field values over F2, checks every MOVE and co-chart ADD, records the seven
mode exchanges, and runs the four stated negative controls.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
WORD_SHA = "9caac6d9b939c60bbfe54937bd30f2b2f6b2037a99f6e3a35ec10ac2794341be"


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rref(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return tuple()
    p = 0
    for c in range(len(a[0])):
        q = next((i for i in range(p, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        z = a[p][c]
        a[p] = [x / z for x in a[p]]
        for i in range(len(a)):
            if i != p and a[i][c]:
                z = a[i][c]
                a[i] = [x - z * y for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return tuple(tuple(row) for row in a[:p])


def in_span(v, basis):
    x = list(map(F, v))
    for row in basis:
        pivot = next(i for i, z in enumerate(row) if z)
        if x[pivot]:
            q = x[pivot]
            x = [a - q * b for a, b in zip(x, row)]
    return not any(x)


def nested(frames, dims, spaces, a, b):
    return (dims[a] <= dims[b] and all(in_span(row, spaces[b]) for row in spaces[a])) or \
           (dims[b] <= dims[a] and all(in_span(row, spaces[a]) for row in spaces[b]))


def rank_f2(rows):
    basis = {}
    for original in rows:
        x = original
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def replay(word, check_snapshots=True):
    frames = {int(k): v for k, v in word["frames"].items()}
    dims = {c: int(v["dim"]) for c, v in frames.items()}
    spaces = {c: rref(v["B"]) for c, v in frames.items()}
    for c in frames:
        need(len(spaces[c]) == dims[c], ("chart dimension", c))

    n_public = word["public"]
    n_owned = word["owned_fields"]
    active = {}
    values = {i: 1 << i for i in range(n_public)}
    where = {i: word["start"][i] for i in range(n_public)}
    counts = Counter()
    paid = Counter()
    move_pairs = set()
    retired = 0
    peak_owned = 0
    clear_rows = []
    states = {}
    observed_y = {}
    check_by_padd = {}
    check_by_hub = {}
    if check_snapshots:
        for checkpoint in word.get("_expected_checkpoints", []):
            check_by_padd[checkpoint["packet_add_index"]] = checkpoint
            check_by_hub[checkpoint["hub_restore_index"]] = checkpoint

    for event, op in enumerate(word["program"]):
        kind, target = op[:2]
        need(target in range(n_public) or target in range(n_public, n_public + n_owned),
             ("target field range", event, op))
        if kind == "MOVE":
            _, field, src, dst = op
            need(field in where and where[field] == src, ("MOVE source chart", event, op, where.get(field)))
            need(src in frames and dst in frames, ("MOVE chart ids", event, op))
            need(dims[src] != dims[dst], ("zero-rank/alias MOVE", event, op))
            need(nested(frames, dims, spaces, src, dst), ("MOVE chart nesting", event, op))
            rank = abs(dims[dst] - dims[src])
            need(1 <= rank <= 8, ("MOVE rank", event, op, rank))
            paid[rank] += 1
            move_pairs.add((src, dst))
            where[field] = dst
            counts["MOVE"] += 1
        elif kind == "INIT":
            _, field, chart = op
            need(n_public <= field < n_public + n_owned, ("INIT only owned field", event, op))
            need(field not in active, ("INIT fresh lifetime", event, op))
            need(chart in frames, ("INIT chart", event, op))
            active[field] = chart
            values[field] = 0
            where[field] = chart
            peak_owned = max(peak_owned, len(active))
            counts["INIT"] += 1
        elif kind == "ADD":
            _, dst, src, chart = op
            need(dst in values and src in values, ("ADD active fields", event, op))
            need(where[dst] == where[src] == chart, ("ADD cochart", event, op, where.get(dst), where.get(src)))
            values[dst] ^= values[src]
            counts["ADD"] += 1
            if check_snapshots and event in check_by_padd:
                cp = check_by_padd[event]
                p = cp["packet_field"]
                s = cp["captured_role"]
                need(values[p] == cp["packet_after"], ("packet checkpoint", event, cp, values[p]))
                need(values[s] == cp["source_after"], ("captured source checkpoint", event, cp, values[s]))
                observed_y[cp["served_role"]] = values[111 + cp["served_role"]]
            if check_snapshots and event in check_by_hub:
                cp = check_by_hub[event]
                s = cp["captured_role"]
                need(values[s] == 1 << s, ("source restored at Hub", event, cp, values[s]))
        elif kind == "CLEAR":
            _, field, chart = op
            need(field in active, ("CLEAR active owned field", event, op))
            need(where[field] == chart, ("CLEAR chart", event, op, where.get(field)))
            clear_rows.append({"event": event, "field": field, "value": values[field]})
            del active[field]
            del values[field]
            del where[field]
            retired += 1
            counts["CLEAR"] += 1
        else:
            raise AssertionError(("unsupported operation", event, op))

        if event in (0, 2, 7, 8, 9, 10, 15, 16, 18, 66):
            states[str(event)] = {
                "op": op,
                "packet_value": values.get(n_public + n_owned - 1),
                "active_owned": sorted(active),
                "served_Y7": values.get(n_public + 7),
                "captured_X6": values.get(6),
                "chart_X6": where.get(6),
            }

    need(not active, ("all owned lifetimes retired", sorted(active)))
    need(counts["MOVE"] + counts["INIT"] + counts["ADD"] + counts["CLEAR"] == len(word["program"]), "operation count")
    need(where == {i: word["final"][i] for i in range(n_public)}, "all public endpoint charts")
    expected = [1 << i for i in range(n_public)]
    for i in range(8):
        expected[111 + i] ^= 1 << i
    actual = [values[i] for i in range(n_public)]
    need(actual == expected, "all 222 final value rows")
    need(rank_f2(actual) == n_public, "all 222 independent input directions restored/preserved")
    need(dict(sorted(paid.items())) == {1: 12, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 210},
         ("recomputed MOVE profile", dict(paid)))
    need(dict(counts) == {"MOVE": 242, "INIT": 1, "ADD": 30, "CLEAR": 1}, ("op counts", dict(counts)))
    need(retired == 1 and peak_owned == 1, ("owned lifetime/peak", retired, peak_owned))
    need(len(clear_rows) == 1 and clear_rows[0]["value"] == 1, ("nonzero owned CLEAR", clear_rows))
    return {
        "final_rows": actual,
        "where": where,
        "counts": dict(counts),
        "paid_profile": dict(sorted(paid.items())),
        "retired_lifetimes": retired,
        "peak_owned": peak_owned,
        "clear_rows": clear_rows,
        "nested_move_pair_count": len(move_pairs),
        "selected_states": states,
        "checkpoint_y_outputs": observed_y,
    }


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    native_raw = (repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz").read_bytes()
    need(sha(native_raw) == PIN, "authenticated native pin")
    native = json.loads(gzip.decompress(native_raw))
    bus_dir = args.bus_dir or Path("root-work/bit-exchange-bus")
    word_raw = (bus_dir / "WORD.json.gz").read_bytes()
    need(sha(word_raw) == WORD_SHA, "literal word source pin")
    word = json.loads(gzip.decompress(word_raw))
    result = json.loads((bus_dir / "RESULT.json").read_text())
    need(result["native_sha256"] == PIN and result["word_sha256"] == WORD_SHA, "author result pins")
    need(word["start"] == native["start"][:222], "all 222 initial charts match native")
    need(word["final"][:111] == native["final"][:111], "all X endpoint charts match native")
    need(word["final"][119:222] == native["final"][119:222], "103 unchanged Y endpoint charts match native")

    checkpoints = result["actual_exchange_observations"]
    for cp in checkpoints:
        cp["packet_field"] = 222
        k, j = cp["served_role"], cp["captured_role"]
        need(j == k - 1, ("consecutive mode roles", cp))
        need(cp["packet_after"] == 1 << j and cp["source_after"] == (1 << j) ^ (1 << k),
             ("independent exchange value formula", cp))
        program = word["program"]
        need(program[cp["source_add_index"]] == ["ADD", j, 222, cp["chart"]],
             ("source addition index", cp))
        need(program[cp["packet_add_index"]] == ["ADD", 222, j, cp["chart"]],
             ("packet handoff index", cp))
        need(program[cp["hub_restore_index"]] == ["ADD", j, k, word["final"][0]],
             ("Hub restoration index", cp))
    word_with_checkpoints = dict(word)
    word_with_checkpoints["_expected_checkpoints"] = checkpoints
    base = replay(word_with_checkpoints)

    # Independently apply the four claimed perturbations. The first three are
    # syntactically valid but must fail the public endpoint value map; the last
    # attempts an ADD before the owned field/source cochart lifecycle exists.
    controls = []
    for name, index, action in (
        ("omit_first_source_restoration", checkpoints[0]["hub_restore_index"], "delete"),
        ("omit_first_packet_handoff", checkpoints[0]["packet_add_index"], "delete"),
        ("reverse_first_feedback_order", checkpoints[0]["source_add_index"], "swap"),
    ):
        bad = json.loads(json.dumps(word))
        if action == "delete":
            del bad["program"][index]
        else:
            bad["program"][index], bad["program"][index + 1] = bad["program"][index + 1], bad["program"][index]
        try:
            # Relax the expected profile/final-map asserts; this returns the
            # altered public map when the word remains structurally legal.
            altered = replay_relaxed(bad)
            expected = [1 << i for i in range(222)]
            for i in range(8):
                expected[111 + i] ^= 1 << i
            wrong = [i for i, (a, b) in enumerate(zip(altered["final_rows"], expected)) if a != b]
            need(wrong, ("negative control unexpectedly passes", name))
            controls.append({"name": name, "rejected": True, "wrong_public_rows": wrong})
        except ValueError as e:
            controls.append({"name": name, "rejected": True, "failure": str(e)})

    bad = json.loads(json.dumps(word))
    bad["program"][0], bad["program"][2] = bad["program"][2], bad["program"][0]
    try:
        replay_relaxed(bad)
    except ValueError as e:
        controls.append({"name": "form_packet_before_source_reaches_Hub", "rejected": True, "failure": str(e)})
    else:
        raise AssertionError("invalid early acquisition was accepted")
    need(len(controls) == 4, "four independent negative controls")
    need(controls[0]["wrong_public_rows"] == [0, 1, 2, 3, 4, 5, 6], "source-restore control outputs")
    need(controls[1]["wrong_public_rows"] == [0, 1, 2, 3, 4, 5, 117], "handoff control outputs")
    need(controls[2]["wrong_public_rows"] == [0, 1, 2, 3, 4, 5, 6, 117], "feedback-order control outputs")

    need(base["checkpoint_y_outputs"] == {k: (1 << (111 + k)) ^ (1 << k) for k in range(1, 8)},
         ("eight target output capture", base["checkpoint_y_outputs"]))
    # Role0 is updated at zero after the packet is returned and cleared.
    need(base["final_rows"][111] == (1 << 111) ^ 1, "Y0 receives x0 at zero")
    need(all(base["final_rows"][111+i] == (1 << (111+i)) ^ (1 << i) for i in range(8)), "eight completed Y targets")
    need(all(base["final_rows"][111+i] == 1 << (111+i) for i in range(8, 111)), "103 untouched Y targets")
    need(all(base["final_rows"][i] == 1 << i for i in range(111)), "all111 X rows restored")

    # The optimistic plain-tiling price is checked independently with exact
    # 160-bit directed 200th-root intervals, against the pinned complete-Q
    # limiting allowance. This calculation does not assert the tiling premise
    # against coded cross-frame buses.
    budget = json.loads((repo / "research/moonshot-005-program/results/bit-rank-nine-shared-interface/BUDGET.json").read_text())
    ceiling = budget["at_t_199_over_200"]["limiting_Q_allowance"]
    ceiling_lo, ceiling_hi = F(ceiling["exact_lower"]), F(ceiling["exact_upper"])
    def pwr(rank):
        den = 1 << 160
        target = rank ** 199 * den ** 200
        lo, hi = 0, rank * den + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid ** 200 <= target:
                lo = mid
            else:
                hi = mid
        need(lo ** 200 <= target < (lo + 1) ** 200, ("directed rank root", rank))
        up = lo if lo ** 200 == target else lo + 1
        return F(lo, den), F(up, den)
    def price(profile):
        lo = hi = F(0)
        for r, c in profile.items():
            a, b = pwr(r)
            if c >= 0:
                lo += c * a
                hi += c * b
            else:
                lo += c * b
                hi += c * a
        return lo, hi
    tiling = price({7: 222, 8: 14})
    deficit = tiling[0] - ceiling_hi, tiling[1] - ceiling_lo
    need(deficit[0] > F("28.0442595295"), ("orthogonal tiling price deficit", deficit))
    need(result["plain_uncoded_orthogonal_bus_tiling_minimum_packets"] == 14, "reported uncoded packet count")

    out = {
        "status": "PASS_INDEPENDENT_LITERAL_BIT_EXCHANGE_BUS_REPLAY",
        "native_sha256": PIN,
        "word_sha256": WORD_SHA,
        "author_result_sha256": sha((bus_dir / "RESULT.json").read_bytes()),
        "program_operations": len(word["program"]),
        "replayed_bill": {
            "counts": base["counts"],
            "paid_profile": {str(k): v for k, v in base["paid_profile"].items()},
            "retired_lifetimes": base["retired_lifetimes"],
            "peak_owned": base["peak_owned"],
            "distinct_nested_move_pairs": base["nested_move_pair_count"],
        },
        "all_222_final_rows_exact": True,
        "all_222_directions_independent": True,
        "x_rows_restored": 111,
        "completed_y_roles": list(range(8)),
        "unchanged_y_roles": list(range(8, 111)),
        "exchange_checkpoints": base["checkpoint_y_outputs"],
        "owned_clear_values": base["clear_rows"],
        "negative_controls": controls,
        "plain_tiling_price_audit": {
            "profile": {"7": 222, "8": 14},
            "price_lower": str(tiling[0]),
            "price_upper": str(tiling[1]),
            "Q_ceiling_lower": str(ceiling_lo),
            "Q_ceiling_upper": str(ceiling_hi),
            "deficit_lower": str(deficit[0]),
            "scope": "Arithmetic verified conditional on the independent uncoded-tiling minimum14; it does not constrain coded cross-frame buses.",
        },
        "scope": "Literal finite F2 word and the universal identity ADD(a,ADD(a,b))=b. Replays every operation independently with exact rational chart geometry. No complete111-output word, compiler/erasure/uniformity admission, supplier, or new kappa.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in (
        "status", "program_operations", "replayed_bill", "x_rows_restored",
        "completed_y_roles", "unchanged_y_roles", "negative_controls",
        "plain_tiling_price_audit")}, indent=2))


def replay_relaxed(word):
    """Independent replay that accepts a valid altered program and returns it."""
    frames = {int(k): v for k, v in word["frames"].items()}
    dims = {c: int(v["dim"]) for c, v in frames.items()}
    spaces = {c: rref(v["B"]) for c, v in frames.items()}
    n_public, n_owned = word["public"], word["owned_fields"]
    values = {i: 1 << i for i in range(n_public)}
    where = {i: word["start"][i] for i in range(n_public)}
    active = set()
    for event, op in enumerate(word["program"]):
        if op[0] == "MOVE":
            _, f, src, dst = op
            if f not in where or where[f] != src or src not in frames or dst not in frames:
                raise ValueError("MOVE source/lifecycle")
            if dims[src] == dims[dst] or not nested(frames, dims, spaces, src, dst):
                raise ValueError("MOVE nesting/rank")
            where[f] = dst
        elif op[0] == "INIT":
            _, f, c = op
            if not (n_public <= f < n_public+n_owned) or f in active or c not in frames:
                raise ValueError("INIT lifecycle")
            active.add(f); values[f] = 0; where[f] = c
        elif op[0] == "ADD":
            _, a, b, c = op
            if a not in values or b not in values:
                raise ValueError("ADD inactive field")
            if where[a] != where[b] or where[a] != c:
                raise ValueError("ADD cochart/lifecycle")
            values[a] ^= values[b]
        elif op[0] == "CLEAR":
            _, f, chart = op
            if f not in active:
                raise ValueError("CLEAR inactive owned field")
            if where[f] != chart:
                raise ValueError("CLEAR chart")
            active.remove(f); del values[f]; del where[f]
        else:
            raise ValueError("unknown operation")
    if active:
        raise ValueError("owned lifetime not retired")
    return {"final_rows": [values[i] for i in range(n_public)], "where": where}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--bus-dir", type=Path)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
