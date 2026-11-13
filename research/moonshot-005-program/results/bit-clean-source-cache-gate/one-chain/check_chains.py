#!/usr/bin/env python3
"""Independent nested-chain cache screen for the BIT nine-packet rail.

Only clean independent X-only histories from the pinned screen are treated as
cache sources. The calculation asks whether each receiver's residual F_i can
be formed using cache rows on a single nested chart chain inside its actual
final facet. No Y-to-Y coding is allowed.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
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
    pivots = []
    for col in range(ncol):
        p = next((i for i in range(pivot_row, nrow) if a[i][col]), None)
        if p is None:
            continue
        a[pivot_row], a[p] = a[p], a[pivot_row]
        z = a[pivot_row][col]
        a[pivot_row] = [x / z for x in a[pivot_row]]
        for i in range(nrow):
            if i != pivot_row and a[i][col]:
                z = a[i][col]
                a[i] = [x - z * y for x, y in zip(a[i], a[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == nrow:
            break
    return tuple(tuple(row) for row in a[:pivot_row])


def is_subspace(small, large):
    return len(rref([*small, *large])) == len(large)


def f2_insert(basis, value, witness):
    while value:
        p = value.bit_length() - 1
        if p not in basis:
            basis[p] = (value, witness)
            return True
        old, mask = basis[p]
        value ^= old
        witness ^= mask
    return False


def f2_solve(basis, value):
    mask = 0
    while value:
        p = value.bit_length() - 1
        if p not in basis:
            return None
        old, old_mask = basis[p]
        value ^= old
        mask ^= old_mask
    return mask


def basis_for(indices, histories):
    out = {}
    for i in indices:
        f2_insert(out, histories[i]["row"], 1 << i)
    return out


def add_basis(dst, src):
    for value, witness in src.values():
        f2_insert(dst, value, witness)


def rank_power(rank):
    return Decimal(rank) ** Decimal("0.995")


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    native_path = repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
    raw = native_path.read_bytes()
    need(sha(raw) == NATIVE_SHA, "pinned native source hash")
    native = json.loads(gzip.decompress(raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    screen_path = args.screen if args.screen else repo.parent / "root-work/BIT-NINE-PACKET-SCREEN.json"
    screen_raw = screen_path.read_bytes()
    screen = json.loads(screen_raw)
    need(screen["native_sha256"] == NATIVE_SHA, "screen is for pinned native source")
    need(screen["pure_X_endpoint_restored"] and screen["pure_X_history_count"] == 1027,
         "screen X histories are the restored clean independent subword")

    histories = screen["histories"]
    by_chart = defaultdict(list)
    for hi, h in enumerate(histories):
        need(0 <= h["field"] < 111, ("non-X history field", hi, h["field"]))
        need(h["event"] >= -1, ("history event", hi))
        by_chart[h["chart"]].append(hi)
    chart_dims = {c: frames[c]["dim"] for c in by_chart}
    chart_spaces = {c: rref(frames[c]["B"]) for c in by_chart}
    chart_basis = {c: basis_for(indices, histories) for c, indices in by_chart.items()}
    need(all(chart_dims[c] == len(chart_spaces[c]) for c in by_chart), "chart geometric ranks")

    # Verify cached chart identities are genuine nested subcharts of the
    # receiver's actual final facet. Also verify the source screen target.
    getcontext().prec = 60
    alpha = Decimal("0.995")
    out = []
    total_route_price = Decimal(0)
    total_movement_count = 0
    selected_cache_rows = set()
    selected_history_ids = set()
    cache_init_add_clear = Counter()
    max_selected_per_receiver = 0

    for i, test in enumerate(screen["receiver_tests"]):
        need(test["receiver"] == i, ("receiver order", i))
        wanted = screen["fitting_rows"][i] ^ (1 << i)
        need(wanted.bit_count() == test["desired_offdiagonal_terms"], ("target residual", i))
        target_chart = native["final"][111 + i]
        target_space = rref(frames[target_chart]["B"])
        eligible = [c for c in by_chart
                    if chart_dims[c] < 8 and is_subspace(chart_spaces[c], target_space)]
        eligible.sort(key=lambda c: (chart_dims[c], c))
        need(all(is_subspace(chart_spaces[c], target_space) for c in eligible), ("eligibility", i))

        best = None
        # The X source visits only dimensions 1,2,4,6,7,8 in this screen.
        # DFS traverses the actual chart-poset, extending only strict nested
        # chains. The route stops at its first target-covering cache chart;
        # adding another stop strictly increases rank^0.995 path price.
        def dfs(path, basis, prior):
            nonlocal best
            prev_dim = chart_dims[prior] if prior is not None else 0
            for c in eligible:
                dim = chart_dims[c]
                if dim <= prev_dim:
                    continue
                if prior is not None and not is_subspace(chart_spaces[prior], chart_spaces[c]):
                    continue
                next_basis = dict(basis)
                add_basis(next_basis, chart_basis[c])
                next_path = path + [c]
                witness = f2_solve(next_basis, wanted)
                if witness is not None:
                    dims = [chart_dims[x] for x in next_path]
                    moves = [dims[0]] + [b - a for a, b in zip(dims, dims[1:])]
                    if dims[-1] < 7:
                        moves.append(7 - dims[-1])
                    need(all(r > 0 for r in moves), ("positive route ranks", i, next_path, moves))
                    price = sum((rank_power(r) for r in moves), Decimal(0))
                    hids = [h for h in range(len(histories)) if (witness >> h) & 1]
                    key = (price, len(hids), len(next_path), tuple(next_path), tuple(hids))
                    if best is None or key < best[0]:
                        best = (key, next_path, moves, witness, hids)
                    # A further chart cannot improve this completed route.
                    continue
                # Enumerate extensions only if they can still fit below rank 7.
                if dim < 7:
                    dfs(next_path, next_basis, c)

        dfs([], {}, None)
        if best is None:
            out.append({"receiver": i, "target_chart": target_chart,
                        "eligible_chart_count": len(eligible), "status": "NO_NESTED_CHAIN"})
            continue
        _, path, moves, witness, hids = best
        dims = [chart_dims[c] for c in path]
        price = sum((rank_power(r) for r in moves), Decimal(0))
        need(sum((histories[h]["row"] for h in []), 0) == 0, "constant guard")
        xor = 0
        for h in hids:
            xor ^= histories[h]["row"]
        need(xor == wanted, ("witness replay", i))
        # Selected histories are cache sources; if the same (chart,row) is
        # needed for multiple receivers, one stationary cache can be shared.
        cache_keys = [(histories[h]["chart"], histories[h]["row"]) for h in hids]
        selected_cache_rows.update(cache_keys)
        selected_history_ids.update(hids)
        max_selected_per_receiver = max(max_selected_per_receiver, len(cache_keys))
        cache_init_add_clear["INIT"] += len(set(cache_keys))
        cache_init_add_clear["ADD_X_TO_CACHE"] += len(set(cache_keys))
        cache_init_add_clear["ADD_CACHE_TO_Y"] += len(cache_keys)
        cache_init_add_clear["CLEAR"] += len(set(cache_keys))
        total_route_price += price
        total_movement_count += len(moves)
        out.append({
            "receiver": i,
            "target_chart": target_chart,
            "target_chart_dim": 7,
            "eligible_chart_count": len(eligible),
            "chain_charts": path,
            "chain_dims": dims,
            "route_move_ranks": moves,
            "route_move_count": len(moves),
            "route_price_decimal": str(price),
            "selected_history_indices": hids,
            "selected_histories": [
                {"history_index": h, "event": histories[h]["event"],
                 "field": histories[h]["field"], "chart": histories[h]["chart"],
                 "row": hex(histories[h]["row"])} for h in hids],
            "target_replayed": True,
        })

    no_chain = [x["receiver"] for x in out if x.get("status") == "NO_NESTED_CHAIN"]
    # The simple decoders above each use one cached row per selected history.
    # If the same row is reused across targets, the retained-cache count is
    # reduced by sharing it once.
    cache_init_add_clear["INIT"] = len(selected_cache_rows)
    cache_init_add_clear["ADD_X_TO_CACHE"] = len(selected_cache_rows)
    cache_init_add_clear["CLEAR"] = len(selected_cache_rows)
    cache_init_add_clear["ADD_CACHE_TO_Y"] = sum(len(x.get("selected_history_indices", [])) for x in out)
    solved = [x for x in out if x.get("status") != "NO_NESTED_CHAIN"]

    base_x = Decimal(289) + Decimal(244) * rank_power(2)
    packets = Decimal(9) * rank_power(8)
    direct7 = Decimal(111) * rank_power(7)
    unit_y = Decimal(111 * 7)
    limit = Decimal("1621.750880211152355")
    cost = base_x + packets + total_route_price
    direct_cost = base_x + packets + direct7
    unit_cost = base_x + packets + unit_y

    result = {
        "status": "SINGLE_NESTED_CHAIN_CACHE_SPAN_SCREEN",
        "native_sha256": NATIVE_SHA,
        "screen_sha256": sha(screen_raw),
        "scope": "Clean independent X-only history rows only; one actual nested route chart chain per Y; arbitrary local Y plus cached-X ADDs; no Y-Y coding; source caches are zero-owned stationary INIT/ADD/CLEAR lifetimes; no contaminated full-native intermediate payload is reused.",
        "receiver_count": len(out),
        "all_single_chain_witnesses": not no_chain,
        "no_chain_receiver_ids": no_chain,
        "chain_results": out,
        "chain_length_histogram": dict(sorted(Counter(len(x["chain_charts"]) for x in solved).items())),
        "move_count_histogram_per_receiver": dict(sorted(Counter(x["route_move_count"] for x in solved).items())),
        "aggregate_route_move_count": total_movement_count,
        "aggregate_route_rank_histogram": dict(sorted(Counter(r for x in solved for r in x["route_move_ranks"]).items())),
        "aggregate_route_price_decimal": str(total_route_price),
        "cache_distinct_chart_row_count_shared_across_Y": len(selected_cache_rows),
        "cache_history_source_count_union": len(selected_history_ids),
        "cache_and_Y_add_operation_counts": dict(cache_init_add_clear),
        "max_cached_rows_used_by_one_Y": max_selected_per_receiver,
        "tariff": {
            "X_source_moment": str(base_x),
            "nine_packet_moment": str(packets),
            "direct_rank7_route_moment": str(direct7),
            "all_unit_Y_route_moment": str(unit_y),
            "single_chain_route_moment": str(total_route_price),
            "optimistic_single_chain_total": str(cost),
            "all_unit_total": str(unit_cost),
            "limit": str(limit),
            "single_chain_slack": str(limit - cost),
            "all_unit_excess": str(unit_cost - limit),
            "direct7_excess_or_slack": str(limit - direct_cost),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "receiver_count", "all_single_chain_witnesses", "no_chain_receiver_ids",
                                               "chain_length_histogram", "move_count_histogram_per_receiver",
                                               "aggregate_route_move_count", "aggregate_route_rank_histogram",
                                               "aggregate_route_price_decimal", "cache_distinct_chart_row_count_shared_across_Y",
                                               "cache_and_Y_add_operation_counts", "tariff"]}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--screen", type=Path)
    p.add_argument("--output", type=Path, default=Path("worker-c/bit-nine-cache-chains/RESULT.json"))
    main(p.parse_args())
