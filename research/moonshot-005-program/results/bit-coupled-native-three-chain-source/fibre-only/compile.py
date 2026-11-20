#!/usr/bin/env python3
"""Compile the donor-dependent fibre-only source and price all original owners."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import construction


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--emit-words", action="store_true")
    args = parser.parse_args()
    base = args.repo / "research/moonshot-005-program/results"
    paths = {
        "compiler": base / "bit-spread-packed-source-owner-compiler/author/compile_pack.py",
        "helper": base / "bit-spread-source-owner-compiler/author/compile_source.py",
        "review": base / "bit-spread-overlap-source/review/check.py",
        "field": base / "bit-spread-h263-source/review/check.py",
        "background": base / "bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json",
    }
    compiler, helper, review, field = (construction.module(paths[key], "chain_compile_" + key)
                                       for key in ("compiler", "helper", "review", "field"))
    native = review.Native(args.repo, field)
    wires, xcount = compiler.physical_slots(native, args.repo, helper)
    f, atlas, previous = construction.context(args.repo)
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    centres = prm["centres"]
    templates = {}
    for k in (3, 12):
        charts, maps, _, _, _ = construction.build(f, atlas, previous, centres, k, prm[str(k)]["seed"])
        for j, rows in maps.items():
            h = next(chart.h for chart in charts if j in chart.donors)
            chart = review.Chart(native, h, k)
            templates.setdefault(j, {})[k] = chart, rows, prm[str(k)]["early"][str(j)]
    args.out.mkdir(parents=True, exist_ok=True)
    totals, per_donor, hashes, all_y = Counter(), {}, {}, set()
    for j, parts in sorted(templates.items()):
        records, placements, costs, digests = {}, {}, Counter(), {}
        for k in (3, 12):
            chart, rows, seed = parts[k]
            bill, perm, late, stream = compiler.compile_one(helper, review, chart, j, rows, seed,
                                                           set(centres), wires, xcount, records)
            construction.require(not set(placements) & set(perm) and not all_y.intersection(late),
                                 "distinct original owners and distinct late caches")
            placements.update(perm)
            all_y.update(late)
            costs.update(bill)
            digests[str(k)] = sha256(stream).hexdigest()
            if args.emit_words:
                helper.save_compressed(args.out / f"REDUCE-{j}-{k}.bin.gz", stream)
        construction.require(set(placements) == set(range(3840*j, 3840*(j+1))), "every original donor field")
        swaps = helper.permutation_swaps(placements)
        records[f"{j}-swaps"] = swaps
        costs["permutation_ADD"] = 18*len(swaps)
        costs["inverse_ADD"] = costs["basis_ADD"] + costs["permutation_ADD"]
        costs["forward_ADD"] = costs["inverse_ADD"] + costs["write_ADD"] + costs["read_ADD"]
        costs["total_ADD"] = costs["inverse_ADD"] + costs["forward_ADD"]
        body = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
        digests["holder"] = sha256(body).hexdigest()
        if args.emit_words:
            helper.save_compressed(args.out / f"HOLDERS-{j}.json.gz", body)
        hashes[j], per_donor[j] = digests, dict(costs)
        totals.update(costs)
    construction.require(6*len(all_y) == totals["INIT"], "one paid cache per late field")
    background_raw = paths["background"].read_bytes()
    background = json.loads(background_raw)
    construction.require(set(map(int, background)) == set(range(111)), "complete original source invoice")
    bg = Counter()
    for j in range(111):
        if j not in templates:
            bg.update(background[str(j)])
    inverse = bg["early_basis_ADD"] + bg["source_owner_permutation_ADD"]
    cache = bg["snapshot_copy_ADD_INIT_dirty_CLEAR"]
    forward = inverse + cache + bg["late_evaluation_ADD"]
    combined = {"donors": 111, "source_forward_ADD": forward + totals["forward_ADD"],
                "source_pure_inverse_ADD": inverse + totals["inverse_ADD"],
                "source_forward_and_inverse_ADD": forward + inverse + totals["total_ADD"],
                "source_INIT": cache + totals["INIT"], "source_dirty_CLEAR": cache + totals["dirty_CLEAR"],
                "source_extra_MOVE": 0, "new_complete_kappa": False}
    result = {"status": "PASS_PAID_FIBRE_ONLY_CONNECTED_SOURCE_COMPILER",
              "parameters_sha256": sha256(raw).hexdigest(),
              "source_pins": {str(path.relative_to(args.repo)): sha256(path.read_bytes()).hexdigest() for path in paths.values()},
              "native_chart_count": 3, "special_donor_count": 7, "regular_donor_count": 104,
              "special": dict(totals), "special_donor_costs": per_donor, "all_word_hashes": hashes,
              "background": dict(bg), "combined": combined,
              "full_D_K_F_and_return_cost": None,
              "separate_from_all111_forty_four_centre_source_word": True}
    (args.out / "COST.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"special": dict(totals), "combined": combined}, sort_keys=True))


if __name__ == "__main__":
    main()
