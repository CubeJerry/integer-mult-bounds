#!/usr/bin/env python3
"""Exact support gate for public-Y path coding under the fixed K packet map.

The result rules out arbitrary acyclic ADD/SWAP coding among the 111 public Y
rows, provided the nine packets have already established Y=y+Kx at chart 0
and every public row is restored exactly. Extra Y-bearing owned copies are
outside this gate.
"""
import argparse
import hashlib
import json
from pathlib import Path

SUPPORT_SHA = "96530e3cb3dea91b663ea9216ee688d20d9d262e83d73304026ff43d2ba6dd75"
SCREEN_SHA = "ade07c8fdd0393f22d7a71c994af545c3d1569031b5aa617949105648ed6f77a"


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(args):
    workspace = args.repo
    if (workspace / "programme/research").exists():
        programme = workspace / "programme"
        root_work = workspace / "root-work"
        worker_c = workspace / "worker-c"
    else:
        programme = workspace
        root_work = workspace.parent / "root-work"
        worker_c = workspace / "worker-c"
    support_path = args.support if args.support else worker_c / "bit-nine-cache-chains/SUPPORT-RESULT.json"
    support_raw = support_path.read_bytes()
    need(sha(support_raw) == SUPPORT_SHA, "pinned support-dual certificate")
    support = json.loads(support_raw)
    need(support["status"] == "PASS_EXACT_ALL_RECEIVER_SINGLE_CHAIN_SUPPORT_OBSTRUCTION",
         "support certificate status")
    screen_path = args.screen if args.screen else root_work / "BIT-NINE-PACKET-SCREEN.json"
    screen_raw = screen_path.read_bytes()
    need(sha(screen_raw) == SCREEN_SHA, "pinned actual BIT packet screen")
    screen = json.loads(screen_raw)
    need(screen["native_sha256"] == support["native_sha256"], "same authenticated native source")

    rows = screen["fitting_rows"]
    tests = screen["receiver_tests"]
    receivers = support["receiver_results"]
    need(len(rows) == len(tests) == len(receivers) == 111, "111 receiver records")
    sets = []
    output_rows = []
    for i, (test, record) in enumerate(zip(tests, receivers)):
        need(test["receiver"] == record["receiver"] == i, ("receiver order", i))
        residual = rows[i] ^ (1 << i)
        contacts = set(record["contact_ports"])
        contact_mask = sum(1 << j for j in contacts)
        need(residual == contact_mask, ("contact support pins F_i", i))
        need(test["all_subchart_recoverable"], ("pooled control", i))
        max_suffix_support = record["max_contact_coordinates_present_on_any_terminal_chain"]
        need(0 < max_suffix_support < len(contacts), ("positive proper suffix support", i))
        private_candidates = [(len(contacts - set(other["contact_ports"])), h)
                              for h, other in enumerate(receivers) if h != i]
        minimum_private, closest = min(private_candidates)
        gap = minimum_private - max_suffix_support
        need(gap > 0, ("all partners leave more private contacts than any suffix chain can cover",
                       i, minimum_private, max_suffix_support))
        sets.append(contacts)
        output_rows.append({
            "receiver": i,
            "contact_count": len(contacts),
            "minimum_private_contacts_against_any_partner": minimum_private,
            "closest_partner": closest,
            "maximum_single_suffix_chain_contact_support": max_suffix_support,
            "strict_private_deficit": gap,
        })

    # A simple paired example demonstrates the tightest integer gap.
    min_gap = min(r["strict_private_deficit"] for r in output_rows)
    tight = [r for r in output_rows if r["strict_private_deficit"] == min_gap]
    need(min_gap == 4, "minimum per-output deficit control")

    # Last-interaction argument for arbitrary public-only acyclic coding:
    # follow each final output value through whole-label SWAPs and select its
    # last incoming Y<-Y ADD. After that ADD, its y row must already be e_i,
    # since later outgoing-only uses do not change it and the endpoint is
    # exact. The donor is another row in the full-rank public Y basis; modulo
    # e_i it is nonzero and must influence at least one other final output h.
    # The interaction chart C is nested in both final facets F_i and F_h:
    # recipient i follows its monotone tail, and the donor's nonzero quotient
    # component has a surviving dependency path to some h != i. Every X-cache
    # increment on those paths before C is supported inside C, hence inside
    # S_i intersect S_h. All S_i\S_h coordinates must be supplied after the
    # last incoming ADD on i's single suffix chain. The exact inequality above
    # makes this impossible. If output i has no incoming Y<-Y ADD, its entire
    # correction is the predecessor one-chain case.
    result = {
        "status": "PASS_PUBLIC_Y_LAST_INTERACTION_GATE_FIXED_K",
        "support_result_sha256": SUPPORT_SHA,
        "screen_sha256": SCREEN_SHA,
        "fixed_map_premise": "The nine packet deliveries/updates have established exactly Y=y+Kx at chart 0 before the candidate public-Y path code, or are transported through precisely the same public-row operations so this remains the net pre-correction map. The required correction is therefore F=K+I. If a different packet placement yields Y=y+Mx, this result does not apply; recompute I+M and its support geometry.",
        "scope": "Any acyclic ADD/SWAP coding among the 111 public Y rows after the fixed K map; exact endpoint restoration of the y identity; source increments only from clean independent X-only stationary histories; every public output follows its one monotone physical lineage to its actual facet; no additional Y-bearing owned copies or new X transport.",
        "receiver_count": 111,
        "all_public_Y_mix_groups_with_size_ge_2_fail": True,
        "all_unmixed_Y_outputs_fail_by_single_chain_gate": True,
        "all_output_contact_sets_have_min_private_support_over_partners_greater_than_suffix_chain_capacity": True,
        "aggregate_controls": {
            "contact_count_range": [min(r["contact_count"] for r in output_rows),
                                    max(r["contact_count"] for r in output_rows)],
            "minimum_private_contact_count_over_receiver_partner_pairs": min(
                r["minimum_private_contacts_against_any_partner"] for r in output_rows),
            "maximum_suffix_chain_contact_capacity": max(
                r["maximum_single_suffix_chain_contact_support"] for r in output_rows),
            "minimum_strict_deficit": min_gap,
            "maximum_strict_deficit": max(r["strict_private_deficit"] for r in output_rows),
            "tight_receivers": tight,
        },
        "proof": [
            "Let S_i=supp(F_i), which is the actual orthogonal-contact set for receiver i.",
            "Track each final public output through whole-label SWAPs to its last incoming public Y<-Y ADD; its y row must be e_i immediately afterward.",
            "The ADD donor is a distinct row in a full-rank public-Y basis. Modulo e_i its nonzero y component survives to some other output h, so the ADD chart is nested in both F_i and F_h.",
            "All source-cache increments before that interaction are supported inside its chart, hence inside S_i intersect S_h; no coordinate in S_i minus S_h is available there.",
            "After the last incoming ADD, output i has one suffix chain. The exact support replay bounds its S_i coverage by max_suffix_i.",
            "For every i, min_{h != i}|S_i minus S_h| > max_suffix_i. The remaining private coordinates therefore cannot be corrected.",
            "If output i has no incoming Y-Y ADD, its whole route is the predecessor one-chain case.",
        ],
        "per_receiver": output_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "contact_count_range": result["aggregate_controls"]["contact_count_range"],
        "minimum_private_contacts": result["aggregate_controls"]["minimum_private_contact_count_over_receiver_partner_pairs"],
        "maximum_suffix_chain_capacity": result["aggregate_controls"]["maximum_suffix_chain_contact_capacity"],
        "minimum_gap": min_gap,
        "tight_receivers": tight,
    }, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--support", type=Path)
    p.add_argument("--screen", type=Path)
    p.add_argument("--output", type=Path,
                    default=Path("worker-c/bit-nine-path-code-gate/RESULT.json"))
    main(p.parse_args())
