#!/usr/bin/env python3
"""Exact U<=2 price gate and original-port caps on full descending chains.

The clean X histories are pinned to the authenticated BIT native. For each
chart we union the supports of all observed source rows there, then compute
the maximum original-input port union on a single nested history-chart chain.
For each possible low-rank up-turn A->B, a second DP restricts the descending
chain to the interval B down to A. These are support relaxations, not cache
words or decoders.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


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
    return (dims[a] < dims[b] and all(in_span(row, spaces[b]) for row in spaces[a])) or \
           (dims[b] < dims[a] and all(in_span(row, spaces[a]) for row in spaces[b]))


def pop(x):
    return x.bit_count()


def root_interval_inverse8(bits=192):
    """Return directed rational bounds for 8^(-1/200)."""
    den = 1 << bits
    target = den ** 200
    lo, hi = 0, den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if 8 * mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(8 * lo ** 200 <= target < 8 * (lo + 1) ** 200, "directed inverse-eighth root")
    up = lo if 8 * lo ** 200 == target else lo + 1
    return F(lo, den), F(up, den)


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    native_raw = (repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz").read_bytes()
    need(sha(native_raw) == PIN, "native source pin")
    native = json.loads(gzip.decompress(native_raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    spaces = {c: rref(frames[c]["B"]) for c in frames}
    dims = {c: frames[c]["dim"] for c in frames}
    inc = {}
    def sub(a, b):
        key = (a, b)
        if key not in inc:
            inc[key] = dims[a] <= dims[b] and all(in_span(row, spaces[b]) for row in spaces[a])
        return inc[key]

    screen_path = args.screen or (repo.parent / "root-work/BIT-NINE-PACKET-SCREEN.json")
    screen_raw = screen_path.read_bytes()
    screen = json.loads(screen_raw)
    need(screen["native_sha256"] == PIN and screen["pure_X_endpoint_restored"], "clean independent X source")
    histories = screen["histories"]

    # Recreate every retained source history directly from the native's X/X
    # and X-MOVE subword. The screen file is used only as a byte-for-byte
    # negative control, not as the authority for row chronology.
    native_x_rows = [1 << i for i in range(111)]
    native_x_where = list(native["start"][:111])
    replayed_histories = []
    seen_histories = set()
    def observe(event, field):
        key = (native_x_where[field], native_x_rows[field])
        if key not in seen_histories:
            seen_histories.add(key)
            replayed_histories.append({"event": event, "field": field,
                                      "chart": native_x_where[field], "row": native_x_rows[field]})
    for i in range(111):
        observe(-1, i)
    source_add_swap = 0
    source_move_profile = Counter()
    for event, instruction in enumerate(native["program"]):
        op, a = instruction[:2]
        if a >= 111:
            continue
        if op in ("ADD", "SWAP"):
            b = instruction[2]
            if b >= 111:
                continue
            if op == "ADD":
                need(native_x_where[a] == native_x_where[b] == instruction[3],
                     ("native clean X ADD chart", event, instruction))
                native_x_rows[a] ^= native_x_rows[b]
            else:
                native_x_rows[a], native_x_rows[b] = native_x_rows[b], native_x_rows[a]
                native_x_where[a], native_x_where[b] = native_x_where[b], native_x_where[a]
            source_add_swap += 1
            observe(event, a)
            if op == "SWAP":
                observe(event, b)
        elif op == "MOVE":
            src, dst = instruction[2:]
            need(native_x_where[a] == src, ("native clean X MOVE source", event, instruction))
            need(dims[src] != dims[dst] and nested(frames, dims, spaces, src, dst),
                 ("native clean X MOVE nesting", event, instruction))
            source_move_profile[abs(dims[dst] - dims[src])] += 1
            native_x_where[a] = dst
            observe(event, a)
    need(native_x_rows == [1 << i for i in range(111)], "replayed clean X endpoint value identity")
    need(native_x_where == native["final"][:111], "replayed clean X endpoint charts")
    need(replayed_histories == histories, "clean X history screen exactly replayed from native")
    need(source_add_swap == 628 and dict(sorted(source_move_profile.items())) == {1: 289, 2: 244},
         ("replayed clean X paid interface", source_add_swap, source_move_profile))

    by_chart = defaultdict(list)
    support = defaultdict(int)
    for hi, h in enumerate(histories):
        need(0 <= h["field"] < 111 and h["event"] >= -1, ("history provenance", hi))
        c = h["chart"]
        by_chart[c].append(h)
        support[c] |= h["row"]
        for j, line_chart in enumerate(native["start"][:111]):
            if h["row"] >> j & 1:
                need(in_span(spaces[line_chart][0], spaces[c]), ("original support contained in chart", hi, c, j))
    source_charts = sorted(by_chart, key=lambda c: (dims[c], c))

    # The global full-descending-chain DP: each state is a visited source
    # history chart; one may next visit any strict nested history subchart.
    child = {c: [] for c in source_charts}
    parent = {c: [] for c in source_charts}
    for c in source_charts:
        for d in source_charts:
            if dims[d] < dims[c] and sub(d, c):
                child[c].append(d)
                parent[d].append(c)
    global_best = {}
    global_chain = {}
    global_strict = {}
    global_strict_chain = {}
    for c in source_charts:
        best, chain = support[c], [c]
        for d in child[c]:
            m = support[c] | global_best[d]
            p = [c] + global_chain[d]
            if (pop(m), tuple(-z for z in p)) > (pop(best), tuple(-z for z in chain)):
                best, chain = m, p
        global_best[c], global_chain[c] = best, chain
        if child[c]:
            d = max(child[c], key=lambda z: (pop(global_best[z]), tuple(-q for q in global_chain[z])))
            global_strict[c], global_strict_chain[c] = global_best[d], global_chain[d]
        else:
            global_strict[c], global_strict_chain[c] = 0, []

    # Per-dimension caps for an entire source-history descending chain.
    dim_summary = {}
    for d in sorted({dims[c] for c in source_charts}):
        cs = [c for c in source_charts if dims[c] == d]
        single = [pop(support[c]) for c in cs]
        full = [pop(global_best[c]) for c in cs]
        strict = [pop(global_strict[c]) for c in cs]
        i_full = full.index(max(full))
        i_strict = strict.index(max(strict))
        i_single = single.index(max(single))
        dim_summary[str(d)] = {
            "history_charts": len(cs),
            "support_union_at_one_chart_min_max": [min(single), max(single)],
            "entire_descending_chain_union_with_start_min_max": [min(full), max(full)],
            "entire_descending_chain_union_strictly_below_start_min_max": [min(strict), max(strict)],
            "max_at_one_chart_witness": {"chart": cs[i_single], "ports": [j for j in range(111) if support[cs[i_single]] >> j & 1]},
            "max_whole_chain_witness": {"start_chart": cs[i_full], "chain": global_chain[cs[i_full]],
                                        "port_count": full[i_full], "ports": [j for j in range(111) if global_best[cs[i_full]] >> j & 1]},
            "max_strict_descendant_chain_witness": {"start_chart": cs[i_strict], "chain": global_strict_chain[cs[i_strict]],
                                                    "port_count": strict[i_strict], "ports": [j for j in range(111) if global_strict[cs[i_strict]] >> j & 1]},
        }

    # For every possible upper chart, including frames with no history row,
    # compute the largest source-port union on one nested history chain below
    # it. A nonhistory chart contributes no row of its own.
    any_upper_best = {}
    any_upper_path = {}
    for upper in frames:
        choices = [c for c in source_charts if dims[c] <= dims[upper] and sub(c, upper)]
        if not choices:
            any_upper_best[upper], any_upper_path[upper] = 0, []
        else:
            c = max(choices, key=lambda z: (pop(global_best[z]), tuple(-q for q in global_chain[z])))
            any_upper_best[upper], any_upper_path[upper] = global_best[c], global_chain[c]
    any_upper_summary = {}
    for d in sorted(set(dims.values())):
        cs = [c for c in frames if dims[c] == d]
        vals = [pop(any_upper_best[c]) for c in cs]
        j = vals.index(max(vals))
        any_upper_summary[str(d)] = {
            "frame_count": len(cs),
            "whole_descending_chain_union_min_max": [min(vals), max(vals)],
            "max_witness_upper_chart": cs[j],
            "max_witness_source_chain": any_upper_path[cs[j]],
            "max_witness_ports": [i for i in range(111) if any_upper_best[cs[j]] >> i & 1],
        }

    # Possible lower endpoints for an upturn are any actual chart A with
    # dim(B)-dim(A)=1 or2 and A⊂B. The upper endpoint B need not itself have a
    # source history: after the turn the packet could descend into a history
    # chart C⊂B that does not contain A. For a target-first read at A we also
    # compute the stricter B-to-A interval chain, where every cache chart must
    # contain A.
    dim_to_frames = defaultdict(list)
    for c in frames:
        dim_to_frames[dims[c]].append(c)
    edge_classes = defaultdict(list)
    target_best = defaultdict(dict)
    edge_counts = Counter()
    for upper in frames:
        du = dims[upper]
        for up_rank in (1, 2):
            dl = du - up_rank
            for lower in dim_to_frames[dl]:
                if not sub(lower, upper):
                    continue
                # Eligible histories lie in the interval [A,B]. Since source
                # chart dimensions are only1,2,4,6,7,8 and B-A<=2, at most
                # three levels occur. DP still checks exact nested containment.
                eligible = [c for c in source_charts
                            if dl <= dims[c] <= du and sub(lower, c) and sub(c, upper)]
                eligible.sort(key=lambda c: (dims[c], c))
                best, path = {}, {}
                for c in eligible:
                    m, p = support[c], [c]
                    for d in eligible:
                        if dims[d] >= dims[c] or not sub(d, c):
                            continue
                        mm = support[c] | best[d]
                        pp = [c] + path[d]
                        if (pop(mm), tuple(-z for z in pp)) > (pop(m), tuple(-z for z in p)):
                            m, p = mm, pp
                    best[c], path[c] = m, p
                if upper in best:
                    whole = best[upper]
                    full_path = path[upper]
                elif best:
                    c = max(best, key=lambda z: (pop(best[z]), tuple(-q for q in path[z])))
                    whole, full_path = best[c], path[c]
                else:
                    whole, full_path = 0, []
                # Cache reads strictly after arrival at B are isolated as a
                # negative-control profile; they cannot include the B rows.
                strict_mask, strict_path = 0, []
                for c in eligible:
                    if c == upper or dims[c] >= du:
                        continue
                    if pop(best[c]) > pop(strict_mask):
                        strict_mask, strict_path = best[c], path[c]
                # No source-history read exists at B's lower geometric chart
                # unless that exact chart has a recorded row. The path ends
                # at A after its final available history read.
                # Receiver incidence is exact: a target facet contains A.
                facet_ids = [i for i, f in enumerate(native["final"][111:222]) if sub(lower, f)]
                record = {
                    "up_rank": up_rank,
                    "lower_chart": lower,
                    "lower_dim": dl,
                    "upper_chart": upper,
                    "upper_dim": du,
                    "facet_ids_containing_lower": facet_ids,
                    "whole_chain_port_mask": hex(whole),
                    "whole_chain_port_count": pop(whole),
                    "whole_chain_source_chart_path": full_path,
                    "strict_below_upper_port_mask": hex(strict_mask),
                    "strict_below_upper_port_count": pop(strict_mask),
                    "strict_below_upper_source_chart_path": strict_path,
                }
                edge_classes[(up_rank, dl, du)].append(record)
                edge_counts[up_rank] += 1
                for i in facet_ids:
                    rows = target_best[i].setdefault(up_rank, [])
                    rows.append(record)

    def maxrec(records, key):
        return max(records, key=lambda r: (r[key], -r["lower_chart"], -r["upper_chart"]))

    class_summary = []
    for (up_rank, dl, du), records in sorted(edge_classes.items()):
        hi = maxrec(records, "whole_chain_port_count")
        lo = maxrec(records, "strict_below_upper_port_count")
        incidence = max(records, key=lambda r: (len(r["facet_ids_containing_lower"]), -r["lower_chart"]))
        class_summary.append({
            "up_rank": up_rank, "lower_dim": dl, "upper_dim": du,
            "edge_count": len(records),
            "max_facets_containing_lower": len(incidence["facet_ids_containing_lower"]),
            "max_incidence_witness": {k: incidence[k] for k in ("lower_chart", "upper_chart", "facet_ids_containing_lower")},
            "whole_chain_union_max": {k: hi[k] for k in ("lower_chart", "upper_chart", "whole_chain_port_count", "whole_chain_port_mask", "whole_chain_source_chart_path", "facet_ids_containing_lower")},
            "strict_below_upper_union_max": {k: lo[k] for k in ("lower_chart", "upper_chart", "strict_below_upper_port_count", "strict_below_upper_port_mask", "strict_below_upper_source_chart_path", "facet_ids_containing_lower")},
        })

    # Target-first U<=2 caps: for a fixed receiver i, choose either one rank2
    # upturn or two rank1 upturns whose lower endpoints lie in F_i. This is a
    # support-union relaxation over endpoint chains. It does not say two
    # source rows realize all ports in the union.
    target_caps = []
    for i, facet in enumerate(native["final"][111:222]):
        r1 = target_best[i].get(1, [])
        r2 = target_best[i].get(2, [])
        one_options = r1 + r2
        one = maxrec(one_options, "whole_chain_port_count") if one_options else None
        best_pair = None
        best_pair_mask = 0
        for x, a in enumerate(r1):
            ma = int(a["whole_chain_port_mask"], 16)
            for b in r1[x:]:
                mb = int(b["whole_chain_port_mask"], 16)
                u = ma | mb
                if pop(u) > pop(best_pair_mask):
                    best_pair_mask = u
                    best_pair = (a, b)
        if one and one["whole_chain_port_count"] > pop(best_pair_mask):
            best_pair_mask = int(one["whole_chain_port_mask"], 16)
            best_pair = (one,)
        strict_single_options = r1 + r2
        strict_single = maxrec(strict_single_options, "strict_below_upper_port_count") if strict_single_options else None
        strict_pair_mask = 0
        strict_pair = None
        for x, a in enumerate(r1):
            ma = int(a["strict_below_upper_port_mask"], 16)
            for b in r1[x:]:
                mb = int(b["strict_below_upper_port_mask"], 16)
                u = ma | mb
                if pop(u) > pop(strict_pair_mask):
                    strict_pair_mask, strict_pair = u, (a, b)
        if strict_single and strict_single["strict_below_upper_port_count"] > pop(strict_pair_mask):
            strict_pair_mask = int(strict_single["strict_below_upper_port_mask"], 16)
            strict_pair = (strict_single,)
        target_caps.append({
            "receiver": i,
            "facet_chart": facet,
            "best_one_turn_union_count": one["whole_chain_port_count"] if one else 0,
            "best_one_turn_witness": ({k: one[k] for k in ("up_rank", "lower_chart", "upper_chart", "whole_chain_port_count", "whole_chain_source_chart_path")} if one else None),
            "best_U_le2_union_count": pop(best_pair_mask),
            "best_U_le2_union_ports": [j for j in range(111) if best_pair_mask >> j & 1],
            "best_U_le2_witness": [{k: r[k] for k in ("up_rank", "lower_chart", "upper_chart", "whole_chain_port_count", "whole_chain_source_chart_path")} for r in best_pair] if best_pair else [],
            "best_strict_below_upper_one_turn_union_count": strict_single["strict_below_upper_port_count"] if strict_single else 0,
            "best_strict_below_upper_U_le2_union_count": pop(strict_pair_mask),
            "best_strict_below_upper_U_le2_union_ports": [j for j in range(111) if strict_pair_mask >> j & 1],
            "best_strict_below_upper_U_le2_witness": [{k: r[k] for k in ("up_rank", "lower_chart", "upper_chart", "strict_below_upper_port_count", "strict_below_upper_source_chart_path")} for r in strict_pair] if strict_pair else [],
        })

    # Exact movement gate. With total upward rank U, a Hub8->zero path family
    # has downward rank at least72+U and upward rank U: total packet MOVE rank
    # is at least72+2U. For q<=8, q^(199/200)>=q*8^(-1/200).
    root_lo, root_hi = root_interval_inverse8()
    budget_raw = (repo.parent / "root-work/BIT-CACHE-BUDGET-RESULT.json").read_bytes()
    budget = json.loads(budget_raw)
    room_hi = F(budget["maximum_additional_allowance"]["upper"])
    u3_lo = 6 * root_lo
    u2_hi = 4 * root_hi
    need(u3_lo > room_hi, "U=3 movement lower bound exceeds directed Q room")
    movement = {
        "exponent": "199/200",
        "rank_price_inequality": "q^(199/200) >= q*8^(-1/200) for every integer MOVE rank q in1..8",
        "nine_packet_baseline_total_MOVE_rank": 72,
        "total_packet_MOVE_rank_with_up_rank_U": "72+2U",
        "8^(-1/200)_lower": str(root_lo),
        "8^(-1/200)_upper": str(root_hi),
        "extra_movement_lower_at_U3": str(u3_lo),
        "limiting_complete_Q_room_upper": str(room_hi),
        "U3_excess_over_room_lower": str(u3_lo-room_hi),
        "extra_movement_upper_at_U2": str(u2_hi),
        "conclusion": "The retained-nine fixed-clean-X/minimal-Y caller requires integer total upward MOVE rank U<=2. Every finite even-m ceiling is smaller than the limiting ceiling used here.",
    }

    out = {
        "status": "PASS_U2_DIRECTED_MOVEMENT_AND_FULL_DESCENDING_CHAIN_SOURCE_CAPS",
        "native_sha256": PIN,
        "screen_sha256": sha(screen_raw),
        "movement_budget_result_sha256": sha(budget_raw),
        "source_history_rows": len(histories),
        "source_history_charts": len(source_charts),
        "all_native_charts": len(frames),
        "independent_native_source_replay": {
            "history_rows_recreated": len(replayed_histories),
            "ADD_SWAP_count": source_add_swap,
            "MOVE_profile": {str(k): v for k, v in sorted(source_move_profile.items())},
            "endpoint_values_identity": True,
            "endpoint_charts_match": True,
            "row_history_matches_pinned_screen": True,
        },
        "source_dimensions": sorted({dims[c] for c in source_charts}),
        "source_chain_support_caps_by_dimension": dim_summary,
        "whole_descending_chain_caps_for_any_upper_frame": any_upper_summary,
        "up_turn_edge_counts_by_rank": {str(k): edge_counts[k] for k in sorted(edge_counts)},
        "up_turn_edge_class_caps": class_summary,
        "target_first_U_le2_port_union_caps": target_caps,
        "movement_price_gate": movement,
                "scope": "All source-row supports are independently reconstructed from the exact native X/X and MOVE subword and checked to lie in the corresponding real chart. Up-turn edges use every native frame as a possible endpoint; only actual history rows supply new X information. The chain DP permits the union of every observed source row at each visited history chart, even if retaining/combining them would cost extra. The target-first interval result requires every visited cache chart to contain the turn's lower endpoint; unrestricted lower branches are not confused with that case. An upper-endpoint cache read is included in the whole-chain cap and separately excluded below. Target-first U<=2 unions are optimistic port unions, not one row, a coding solution, or a causal complete word. The U price gate is necessary only for the retained nine-packet caller and its fixed budget terms.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({
        "status": out["status"],
        "source_replay": out["independent_native_source_replay"],
        "whole_chain_caps_by_start_dimension": {
            d: {"full": v["entire_descending_chain_union_with_start_min_max"],
                "strict": v["entire_descending_chain_union_strictly_below_start_min_max"]}
            for d, v in dim_summary.items()},
        "whole_chain_caps_any_upper": {
            d: v["whole_descending_chain_union_min_max"]
            for d, v in any_upper_summary.items()},
        "turn_classes": [{"up_rank": x["up_rank"], "lower_dim": x["lower_dim"],
                          "upper_dim": x["upper_dim"], "edge_count": x["edge_count"],
                          "max_facets": x["max_facets_containing_lower"],
                          "full_chain_cap": x["whole_chain_union_max"]["whole_chain_port_count"],
                          "strict_below_upper_cap": x["strict_below_upper_union_max"]["strict_below_upper_port_count"]}
                         for x in class_summary],
        "max_target_strict_U2_port_union": max(x["best_strict_below_upper_U_le2_union_count"] for x in target_caps),
        "movement_price_gate": movement,
    }, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--screen", type=Path)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
