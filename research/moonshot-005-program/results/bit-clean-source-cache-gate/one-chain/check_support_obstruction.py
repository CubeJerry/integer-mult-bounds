#!/usr/bin/env python3
"""Exact support/dual obstruction to one-chain BIT residual correction.

Replays the clean independent X-only subword from the authenticated native,
then proves that no receiver's F_i=(K+I)_i can be formed from stationary X
caches on one nested chart chain. This deliberately permits arbitrary row
fusions among cache rows and imposes no cache-count or ordinary-operation cap.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return tuple()
    nrow, ncol = len(a), len(a[0])
    pivot_row = 0
    for col in range(ncol):
        pivot = next((i for i in range(pivot_row, nrow) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        z = a[pivot_row][col]
        a[pivot_row] = [x / z for x in a[pivot_row]]
        for i in range(nrow):
            if i != pivot_row and a[i][col]:
                z = a[i][col]
                a[i] = [x - z * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == nrow:
            break
    return tuple(tuple(row) for row in a[:pivot_row])


def rank(rows):
    return len(rref(rows))


def is_subspace(small, large):
    """Whether rowspace(small) is a subspace of rowspace(large)."""
    return rank([*small, *large]) == rank(large)


def f2_insert(basis, value):
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            basis[pivot] = value
            return True
        value ^= basis[pivot]
    return False


def f2_contains(basis, value):
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return False
        value ^= basis[pivot]
    return True


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    native_path = repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
    native_raw = native_path.read_bytes()
    need(sha(native_raw) == NATIVE_SHA, "authenticated native source")
    native = json.loads(gzip.decompress(native_raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    need(native["start"][111:222] == [0] * 111 and frames[0]["dim"] == 0,
         "all Y rows start at actual zero chart")

    screen_path = args.screen if args.screen else repo.parent / "root-work/BIT-NINE-PACKET-SCREEN.json"
    screen_raw = screen_path.read_bytes()
    screen = json.loads(screen_raw)
    need(screen["native_sha256"] == NATIVE_SHA, "screen source pin")
    need(screen["pure_X_endpoint_restored"] and screen["pure_X_history_count"] == 1027,
         "screen describes 1027 clean X-only histories")
    need(screen["all_subchart_complete_receiver_count"] == 111,
         "pooled-subchart relaxation completes all receivers")
    need(screen["exact_final_facet_complete_receiver_count"] == 0,
         "no final-facet-only completion in source screen")

    # Rebuild screen history from scratch: execute only X/X arithmetic and
    # X-owned moves as a new circuit, with 111 independent source inputs.
    rows = [1 << i for i in range(111)]
    where = native["start"][:111].copy()
    histories = []
    seen = set()

    def observe(event, field):
        key = (where[field], rows[field])
        if key not in seen:
            seen.add(key)
            histories.append({"event": event, "field": field,
                              "chart": where[field], "row": rows[field]})

    for i in range(111):
        observe(-1, i)
    x_add_swap = 0
    x_move_profile = Counter()
    for event, ins in enumerate(native["program"]):
        op, a = ins[:2]
        if a >= 111:
            continue
        if op in ("ADD", "SWAP"):
            b = ins[2]
            if b >= 111:
                continue
            need(op == "SWAP" or where[a] == where[b] == ins[3],
                 ("X/X ADD cochart", event, ins))
            if op == "ADD":
                rows[a] ^= rows[b]
            else:
                rows[a], rows[b] = rows[b], rows[a]
                where[a], where[b] = where[b], where[a]
            x_add_swap += 1
            observe(event, a)
            if op == "SWAP":
                observe(event, b)
        elif op == "MOVE":
            src, dst = ins[2:]
            need(where[a] == src, ("X route source", event, ins))
            need(frames[src]["dim"] < frames[dst]["dim"],
                 ("clean X route monotonicity", event, ins))
            need(is_subspace(frames[src]["B"], frames[dst]["B"]),
                 ("clean X route nested chart", event, ins))
            x_move_profile[frames[dst]["dim"] - frames[src]["dim"]] += 1
            where[a] = dst
            observe(event, a)
        else:
            raise AssertionError(("unexpected X-subword op", event, ins))

    need(rows == [1 << i for i in range(111)], "independent X-only word identity map")
    need(where == native["final"][:111], "independent X-only word reaches Hub")
    need(histories == screen["histories"], "screen histories exactly replayed")
    need(x_add_swap == screen["pure_X_main_ADD_SWAP_count"], "X arithmetic count")
    need(dict(sorted(x_move_profile.items())) == {int(k): v for k, v in screen["pure_X_paid_profile"].items()},
         "X MOVE profile")

    # The support invariant is the source-row certificate: if coefficient j
    # appears in a current X row at chart C, the original root line L_j is
    # contained in C. ADD is co-charted, MOVE is upward/nested, and SWAP moves
    # the chart label together with the value.
    initial_line_chart = native["start"][:111]
    for hidx, h in enumerate(histories):
        c = h["chart"]
        for j in range(111):
            if (h["row"] >> j) & 1:
                need(is_subspace(frames[initial_line_chart[j]]["B"], frames[c]["B"]),
                     ("history support lies in chart", hidx, c, j))

    need(all(frames[c]["dim"] == 1 and rank(frames[c]["B"]) == 1
             for c in initial_line_chart), "all 111 X entrance charts are genuine lines")
    line_reps = [[Fraction(x) for x in frames[c]["B"][0]] for c in initial_line_chart]
    by_chart = defaultdict(list)
    for h in histories:
        by_chart[h["chart"]].append(h)
    spaces = {c: rref(frames[c]["B"]) for c in by_chart}

    @lru_cache(None)
    def chart_nested(smaller, larger):
        return (len(spaces[smaller]) < len(spaces[larger])
                and is_subspace(spaces[smaller], spaces[larger]))

    chart_support = {}
    for c, entries in by_chart.items():
        support = 0
        for h in entries:
            support |= h["row"]
        chart_support[c] = support

    receiver_results = []
    all_facets_support_rank7 = True
    all_residuals_match_contacts = True
    chart_source_max_dim = Counter()
    total_terminal_chains = 0
    all_terminal_chains_have_coordinate_dual = True
    all_pooled_relaxations_pass = True
    receiver_chain_count_range = [10**9, 0]
    for i in range(111):
        facet = native["final"][111 + i]
        facet_frame = frames[facet]
        facet_space = rref(facet_frame["B"])
        normal = [Fraction(x) for x in facet_frame["A"][0]]
        need(facet_frame["dim"] == 7 and rank(facet_frame["B"]) == 7,
             ("final receiver facet rank", i))
        need(rank(facet_frame["B"] + facet_frame["A"]) == 8
             and rank([normal, line_reps[i]]) == 1,
             ("final facet is the orthogonal complement of its actual source line", i))
        need(all(dot(normal, [Fraction(x) for x in row]) == 0 for row in facet_frame["B"]),
             ("facet orthogonal to its source normal", i))

        contacts = [j for j, root in enumerate(line_reps)
                    if j != i and dot(normal, root) == 0]
        contact_mask = sum(1 << j for j in contacts)
        residual = screen["fitting_rows"][i] ^ (1 << i)
        need(residual == contact_mask, ("F_i support equals actual orthogonal contacts", i))
        all_residuals_match_contacts &= (residual == contact_mask)
        need(all(is_subspace(frames[initial_line_chart[j]]["B"], facet_frame["B"])
                for j in contacts), ("contact roots lie in actual facet", i))
        contact_rank = rank([line_reps[j] for j in contacts])
        need(contact_rank == 7, ("contacts span full receiver facet", i, len(contacts), contact_rank))
        all_facets_support_rank7 &= contact_rank == 7

        # Compare geometric B-subspaces, not only chart IDs. Several receiver
        # facets do have an X history at the endpoint; their cached rows still
        # need to be joined to rows from nested subcharts.
        same_geometry = [c for c, sp in spaces.items() if sp == facet_space]
        eligible = [c for c, sp in spaces.items()
                    if len(sp) <= 7 and is_subspace(sp, facet_space)]
        need(all(len(spaces[c]) <= 7 for c in eligible), ("eligible cache charts within facet", i))
        need(all(is_subspace(frames[0]["B"], frames[c]["B"]) for c in eligible),
             ("each eligible cache chart is reachable from Y's zero chart", i))
        pooled_basis = {}
        for c in eligible:
            for h in by_chart[c]:
                f2_insert(pooled_basis, h["row"])
        pooled_pass = f2_contains(pooled_basis, residual)
        need(pooled_pass, ("all-subchart pooled relaxation control", i))
        all_pooled_relaxations_pass &= pooled_pass
        max_dim = max((len(spaces[c]) for c in eligible), default=0)
        chart_source_max_dim[max_dim] += 1

        # Enumerate every upward-terminal continuation beginning at every
        # actual cache chart. Every feasible cache chain is a prefix of at
        # least one such continuation. A missing contact coordinate on the
        # continuation is therefore also missing on its prefix.
        terminal_count = 0
        max_support_weight = 0
        min_missing_count = len(contacts) + 1
        dual_example = None

        def explore(path, previous, support):
            nonlocal terminal_count, max_support_weight, min_missing_count, dual_example
            prev_dim = len(spaces[previous]) if previous is not None else -1
            next_charts = [c for c in eligible
                           if len(spaces[c]) > prev_dim
                           and (previous is None or chart_nested(previous, c))]
            next_charts.sort(key=lambda c: (len(spaces[c]), c))
            if not next_charts:
                if not path:
                    return
                terminal_count += 1
                chain_support = support & ((1 << 111) - 1)
                missing = residual & ~chain_support
                missing_count = missing.bit_count()
                need(missing_count > 0,
                     ("terminal chart chain has a missing residual coordinate", i, path))
                dual_port = (missing & -missing).bit_length() - 1
                for c in path:
                    for h in by_chart[c]:
                        need(((h["row"] >> dual_port) & 1) == 0,
                             ("terminal coordinate dual annihilates chain cache", i, path, dual_port))
                need((residual >> dual_port) & 1,
                     ("terminal coordinate dual pairs to one", i, path, dual_port))
                max_support_weight = max(max_support_weight, (chain_support & residual).bit_count())
                if missing_count < min_missing_count:
                    min_missing_count = missing_count
                    dual_example = {"chain_charts": path,
                                    "chain_dimensions": [len(spaces[c]) for c in path],
                                    "dual_port": dual_port,
                                    "dual_mask_hex": hex(1 << dual_port),
                                    "missing_contact_count": missing_count,
                                    "target_pairing": 1}
                return
            for c in next_charts:
                explore(path + [c], c, support | chart_support[c])

        explore([], None, 0)
        need(terminal_count > 0, ("at least one terminal source-chart chain", i))
        total_terminal_chains += terminal_count
        receiver_chain_count_range[0] = min(receiver_chain_count_range[0], terminal_count)
        receiver_chain_count_range[1] = max(receiver_chain_count_range[1], terminal_count)
        all_terminal_chains_have_coordinate_dual &= min_missing_count > 0

        receiver_results.append({
            "receiver": i,
            "final_facet_chart": facet,
            "contact_count": len(contacts),
            "contact_ports": contacts,
            "contact_root_span_rank": contact_rank,
            "final_facet_dimension": 7,
            "same_geometry_source_history_charts": same_geometry,
            "eligible_stationary_cache_chart_count": len(eligible),
            "largest_eligible_cache_dimension": max_dim,
            "upward_terminal_chain_count": terminal_count,
            "max_contact_coordinates_present_on_any_terminal_chain": max_support_weight,
            "minimum_missing_contact_coordinates_over_terminal_chains": min_missing_count,
            "coordinate_dual_example": dual_example,
            "one_nested_chain_impossible": True,
        })

    need(all_facets_support_rank7 and all_residuals_match_contacts,
         "all receiver-specific support premises")
    need(all_terminal_chains_have_coordinate_dual,
         "every possible nested chart chain misses a target coordinate")

    # Smallest explicit counterexample dual: receiver 0, actual nested chain
    # 3 < 212 < 266 (dimensions 1,2,4), and e_3. The exact chain rows all have
    # bit 3 zero, whereas the requested F_0 coefficient at X_3 is one.
    example_i = 0
    example_chain = [3, 212, 266]
    example_dual_port = 3
    for a, b in zip(example_chain, example_chain[1:]):
        need(is_subspace(frames[a]["B"], frames[b]["B"]), ("example nested chain", a, b))
    need(all(is_subspace(spaces[c], rref(frames[native["final"][111 + example_i]]["B"]))
             for c in example_chain), "example chain lies in receiver facet")
    for c in example_chain:
        need(all(((h["row"] >> example_dual_port) & 1) == 0 for h in by_chart[c]),
             ("example e3 annihilator", c))
    need((screen["fitting_rows"][example_i] ^ (1 << example_i)) >> example_dual_port & 1,
         "example e3 pairs with target")

    result = {
        "status": "PASS_EXACT_ALL_RECEIVER_SINGLE_CHAIN_SUPPORT_OBSTRUCTION",
        "native_sha256": NATIVE_SHA,
        "screen_sha256": sha(screen_raw),
        "scope": "Exact scalar F2 correction F_i=(K+I)_i; X-source cache rows are restricted to clean independent X-only subword histories at genuine visited charts; each Y follows one nested 0-to-facet chain; unlimited stationary caches and arbitrary local ADD fusion are allowed; no Y-Y coding and no new X transport to unvisited charts.",
        "replay": {
            "source_inputs": 111,
            "independent_X_only_ADD_SWAP": x_add_swap,
            "independent_X_only_move_profile": dict(sorted(x_move_profile.items())),
            "history_count": len(histories),
            "history_log_exactly_matches_source_screen": True,
            "all_history_row_supports_lie_in_their_chart": True,
        },
        "all_receiver_premises": {
            "F_i_is_exactly_actual_orthogonal_contact_set": all_residuals_match_contacts,
            "contact_root_count_range": [min(x["contact_count"] for x in receiver_results),
                                         max(x["contact_count"] for x in receiver_results)],
            "contact_roots_span_each_seven_dimensional_facet": all_facets_support_rank7,
            "receiver_facets_with_same_geometry_X_history_count": sum(bool(x["same_geometry_source_history_charts"]) for x in receiver_results),
            "all_subchart_pooled_rows_recover_all_residuals": all_pooled_relaxations_pass,
            "all_upward_terminal_chains_miss_a_target_support_coordinate": all_terminal_chains_have_coordinate_dual,
            "one_nested_chain_fails_every_receiver": True,
        },
        "terminal_chain_search": {
            "interpretation": "Every feasible finite cache chain is a prefix of one of the enumerated upward-terminal nested continuations from its first cache chart. Each such continuation has an explicit missing-coordinate dual, so every prefix also fails.",
            "all_receivers_terminal_chain_count": total_terminal_chains,
            "per_receiver_terminal_chain_count_range": receiver_chain_count_range,
            "terminal_chains_with_full_residual_support": 0,
        },
        "max_eligible_cache_dimension_histogram": dict(sorted(chart_source_max_dim.items())),
        "example_dual": {
            "receiver": example_i,
            "chain_charts": example_chain,
            "chain_dimensions": [frames[c]["dim"] for c in example_chain],
            "dual_coordinate": example_dual_port,
            "dual_mask_hex": hex(1 << example_dual_port),
            "residual_hex": hex(screen["fitting_rows"][example_i] ^ (1 << example_i)),
            "dual_cache_pairing": 0,
            "dual_target_pairing": 1,
        },
        "receiver_results": receiver_results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "history_count": len(histories),
        "contact_count_range": result["all_receiver_premises"]["contact_root_count_range"],
        "contact_root_span_rank": 7,
        "receiver_facets_with_history": result["all_receiver_premises"]["receiver_facets_with_same_geometry_X_history_count"],
        "terminal_chain_total": total_terminal_chains,
        "terminal_chain_count_range": receiver_chain_count_range,
        "all_terminal_chains_have_coordinate_dual": all_terminal_chains_have_coordinate_dual,
        "one_chain_fails": True,
        "max_eligible_cache_dimension_histogram": result["max_eligible_cache_dimension_histogram"],
        "example_dual": result["example_dual"],
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--screen", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path("worker-c/bit-nine-cache-chains/SUPPORT-RESULT.json"))
    main(parser.parse_args())
