#!/usr/bin/env python3
"""Fresh exact subset ranks and minimum target-rank prices by prefix ranks."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
REBUILT = OUT / "REBUILT-ROWS.json"
STRUCTURE = OUT / "STRUCTURE.json"


def need(ok, label):
    if not ok:
        raise AssertionError(label)


def add_sparse(dst, src, q):
    for k, v in src.items():
        z = dst.get(k, Q(0)) + q * v
        if z:
            dst[k] = z
        else:
            dst.pop(k, None)


def rank_q(rows):
    basis = {}
    for row in rows:
        v = {k: Q(x) for k, x in row.items() if x}
        while v:
            p = min(v)
            old = basis.get(p)
            if old is None:
                scale = 1 / v[p]
                basis[p] = {k: x * scale for k, x in v.items() if x * scale}
                break
            add_sparse(v, old, -v[p])
    return len(basis)


def min_column_basis_rank_sum(rows, targets):
    """Exact weighted column basis via rank-prefix formula, not greedy columns."""
    columns = set().union(*(set(r) for r in rows))
    need(columns and columns <= set(targets), "missing target weights")
    rho = rank_q(rows)
    prefix_ranks = []
    for k in range(1, 9):
        eligible = {h for h in columns if targets[h] <= k}
        restricted = [{h: v for h, v in row.items() if h in eligible} for row in rows]
        prefix_ranks.append(rank_q(restricted))
    minimum = 9 * rho - sum(prefix_ranks)
    # The unrestricted columns must span the original rows.
    need(rank_q(rows) == rho, "rank changed during prefix evaluation")
    need(minimum >= rho, "invalid positive target rank sum")
    return rho, minimum, prefix_ranks


def min_price_control(rows, targets):
    return min_column_basis_rank_sum(rows, targets)[1]


def controls():
    # Overlapping column supports do not invalidate the Laplace lower bound.
    overlap_rows = [{0: Q(1), 1: Q(1)}, {0: Q(1), 1: Q(-1)}]
    overlap_targets = {0: 1, 1: 2}
    overlap_local = sum(min_price_control([r], overlap_targets) for r in overlap_rows)
    overlap_global = min_price_control(overlap_rows, overlap_targets)
    need(overlap_rows[0].keys() & overlap_rows[1].keys(), "overlap fixture lost shared columns")
    need(rank_q(overlap_rows) == 2 and overlap_global == 3 and overlap_local == 2 and
         overlap_global >= overlap_local, "overlap/Laplace positive control")

    # A false direct-sum split is rejected because cross-block dependence lowers rank.
    false_rows = [{0: Q(1), 1: Q(1)}, {0: Q(2), 1: Q(2)}]
    false_component_sum = sum(rank_q([r]) for r in false_rows)
    false_global = rank_q(false_rows)
    need(false_component_sum == 2 and false_global == 1 and
         false_global != false_component_sum, "false direct-sum control")

    # Underpriced target coordinates must fail the dependent-set envelope.
    under_rows = [{0: Q(1), 1: Q(1)}, {0: Q(1), 1: Q(-1)}]
    under_targets = {0: 1, 1: 1}
    under_beta = min_price_control(under_rows, under_targets)
    under_paid = 4
    under_margin = 6 * under_beta - 11 * under_paid
    need(under_margin < 0, "underpriced-target mutant was not rejected")
    need(9 * 6**4 < 11**4, "strict quarter-power envelope")
    return {
        "overlapping_support_direct_sum_laplace_bound": {
            "local_min_basis_price_sum": overlap_local,
            "global_min_basis_price": overlap_global,
            "passed": overlap_global >= overlap_local,
        },
        "false_direct_sum_rejected": {
            "false_component_rank_sum": false_component_sum,
            "true_global_rank": false_global,
            "rejected": True,
        },
        "underpriced_target_rejected": {
            "minimum_basis_target_rank_sum": under_beta,
            "paid_rank_sum": under_paid,
            "quarter_envelope_margin": under_margin,
            "rejected": under_margin < 0,
        },
        "strict_integer_power_envelope": "9*6^4 < 11^4",
    }


def main():
    rd = json.loads(REBUILT.read_text())
    sd = json.loads(STRUCTURE.read_text())
    need(rd["source_sha256"] == sd["source_sha256"], "row/structure source mismatch")
    need(rd["b_rows_sha256"] == sd["b_rows_sha256"], "row/structure artifact mismatch")
    rows_by_event = {r["event"]: {int(h): Q(v) for h, v in r["row"].items()}
                     for r in rd["records"]}
    paid = {r["event"]: int(r["rank"]) for r in rd["records"]}
    targets = {int(h): int(q) for h, q in rd["helper_targets"].items()}
    blocks = [b["events"] for b in sd["matroid_dependent_blocks"]]
    need(sorted(map(len, blocks), reverse=True) == [11, 5, 5, 5], "dependent block sizes")
    control_receipt = controls()

    subset_count = independent_count = dependent_count = 0
    total_paid = total_basis = 0
    checks = []
    block_summaries = []
    ratios = []
    for block_id, block in enumerate(blocks):
        ordered = sorted(block)
        block_rank = rank_q([rows_by_event[e] for e in ordered])
        block_independent = block_dependent = 0
        for mask in range(1, 1 << len(ordered)):
            selected = [e for j, e in enumerate(ordered) if (mask >> j) & 1]
            selected_rows = [rows_by_event[e] for e in selected]
            rho = rank_q(selected_rows)
            paid_sum = sum(paid[e] for e in selected)
            subset_count += 1
            if rho == len(selected):
                independent_count += 1
                block_independent += 1
                continue
            dependent_count += 1
            block_dependent += 1
            rho2, basis_sum, prefix_ranks = min_column_basis_rank_sum(selected_rows, targets)
            need(rho2 == rho, "subset rank mismatch in prefix calculation")
            margin = 6 * basis_sum - 11 * paid_sum
            need(margin >= 0, f"underfunded dependent subset: {selected}")
            ratios.append((Q(basis_sum, paid_sum), block_id, selected, basis_sum, paid_sum))
            total_paid += paid_sum
            total_basis += basis_sum
            checks.append({
                "block_id": block_id,
                "mask": mask,
                "events": selected,
                "rank_Q": rho,
                "paid_rank_sum": paid_sum,
                "prefix_ranks_for_target_rank_le_1_to_8": prefix_ranks,
                "minimum_column_basis_target_rank_sum": basis_sum,
                "quarter_envelope_margin_6B_minus_11P": margin,
            })
        block_summaries.append({
            "block_id": block_id,
            "events": ordered,
            "rows": len(ordered),
            "rank_Q": block_rank,
            "nonempty_subsets": (1 << len(ordered)) - 1,
            "independent_subsets": block_independent,
            "dependent_subsets": block_dependent,
        })

    need(subset_count == 2140 and independent_count == 2109 and dependent_count == 31,
         "local subset census")
    need(ratios and min(r[0] for r in ratios) == Q(11, 6), "minimum dependent price ratio")
    witness = next(x for x in ratios if x[0] == Q(11, 6))
    need(witness[3:] == (44, 24), "exact 11/6 witness sums")
    need(6 * total_basis >= 11 * total_paid, "summed dependent-block envelope")

    out = {
        "status": "PASS_INDEPENDENT_LOCAL_SUBSET_FUNDING",
        "source_sha256": rd["source_sha256"],
        "comparison_b_rows_sha256": rd["b_rows_sha256"],
        "global_rank_Q": sd["exact_global_rank_Q"],
        "dependent_block_count": len(blocks),
        "nonempty_local_subsets": subset_count,
        "independent_subsets": independent_count,
        "dependent_subsets": dependent_count,
        "all_468_row_supports_dominate_paid_rank": rd["all_468_paid_ranks_le_support_target_ranks"],
        "dependent_subset_coarse_funding": {
            "rule": "6*minimum_basis_target_rank_sum >= 11*paid_rank_sum",
            "all_pass": True,
            "aggregate_minimum_basis_sum": total_basis,
            "aggregate_paid_rank_sum": total_paid,
            "minimum_basis_to_paid_ratio": "11/6",
            "witness": {
                "block_id": witness[1],
                "events": witness[2],
                "minimum_basis_target_rank_sum": witness[3],
                "paid_rank_sum": witness[4],
            },
            "strict_power_envelope": "9*6^4 < 11^4, hence R^(1-kappa)>=(6/11)R for 1<=R<=9 and 0<=kappa<=1/4",
        },
        "blocks": block_summaries,
        "dependent_subset_details": checks,
        "controls": control_receipt,
        "method": "Exact-Q row-rank tests for every nonempty subset; for the 31 dependent subsets, minimum column-basis linear rank price is computed only by 9*rho - sum_{k=1..8}rank(M restricted to target ranks <=k). No author's greedy column-basis output is read.",
        "scope": "Frozen native source, main-free helper MOVE rows, retained original helper coordinates, and optimistic free preparation/lifetime charges only.",
    }
    (OUT / "SUBSET-RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "dependent_subset_details"}, indent=2))


if __name__ == "__main__":
    main()
