#!/usr/bin/env python3
"""Literal original-owner source and fully early H263 compiler and invoice."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
import construction


def compile_H(components, helper, atlas, wires, route_payload):
    exits = defaultdict(list)
    for line in route_payload.splitlines():
        phase, donor, coordinate, h, d, _, _, _ = json.loads(line)
        if h != 263:
            continue
        construction.require(phase == "X", "H263 has only genuine early original owners")
        exits[d].extend(helper.owner_id(phase, donor, coordinate, copy) for copy in range(8))
    for values in exits.values():
        values.sort()
    construction.require(len(exits) == 45 and all(len(v) == 16 for v in exits.values()),
                         "all45 actual outgoing ports, sixteen original fields each")
    holders = sorted(x for values in exits.values() for x in values)
    construction.require(len(set(holders)) == len(holders) == 720, "all720 distinct early H owners")
    construction.require(set(holders) == set(x for j in (0, 61, 62) for x in wires[j, 263, "X"]),
                         "source inputs and physical outgoing original owners coincide")
    position = {x: p for p, x in enumerate(holders)}
    matrix = np.zeros((720, 720), dtype=np.uint8)
    source_groups = {}
    for k, data in components.items():
        prefix = 0 if k == 3 else 3
        chart, word = data["chart"], data["Hword"]
        for half in range(2):
            for lane in range(8):
                columns = [wires[j, 263, "X"][16*(prefix+t)+8*half+lane]
                           for j in chart.donors for t in range(k)]
                rows = [exits[d][8*half+lane] for d in chart.ports]
                matrix[np.ix_([position[x] for x in rows], [position[x] for x in columns])] = word
                source_groups[f"{k}/{half}/{lane}"] = {"input_holders": columns, "output_holders": rows}
    stream, price = helper.compile_invertible(matrix)
    # This tests the actual physical owner ordering, separately from abstract matrices.
    minor_ranks = []
    for i in components[3]["chart"].views:
        rows = [position[x] for d in sorted(exits) if atlas.charts[d] <= atlas.adj[i] for x in exits[d]]
        construction.require(len(rows) == 240, "every H receiver sees240 genuine fields")
        for j in (0, 61, 62):
            cols = [position[x] for x in wires[j, 263, "X"]]
            minor_ranks.append(atlas.rank(matrix[np.ix_(rows, cols)]))
    construction.require(set(minor_ranks) == {240}, "every physical donor minor invertible")
    records = {"H": 263, "holders_in_matrix_order": holders, "component_placements": source_groups,
               "exit_holders": {str(d): values for d, values in sorted(exits.items())},
               "reduce_file": "H263-REDUCE.bin.gz", "all_inputs_are_original_X": True}
    body = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    bill = {"H_forward_ADD": price, "H_inverse_ADD": price, "H_forward_and_inverse_ADD": 2*price,
            "H_INIT": 0, "H_dirty_CLEAR": 0, "H_extra_MOVE": 0,
            "physical_matrix_shape": [720, 720], "physical_receiver_donor_minors": len(minor_ranks),
            "minimum_physical_donor_minor_rank": min(minor_ranks)}
    digests = {"matrix": sha256(matrix.tobytes()).hexdigest(), "word": sha256(stream).hexdigest(),
               "holders": sha256(body).hexdigest()}
    return bill, digests, stream, body


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--emit-words", action="store_true")
    args = p.parse_args()
    base = args.repo / "research/moonshot-005-program/results"
    paths = {
        "compiler": base / "bit-spread-packed-source-owner-compiler/author/compile_pack.py",
        "helper": base / "bit-spread-source-owner-compiler/author/compile_source.py",
        "review": base / "bit-spread-overlap-source/review/check.py",
        "field": base / "bit-spread-h263-source/review/check.py",
        "background": base / "bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json",
    }
    compiler, helper, review, field = (construction.module(paths[key], "geometric_compile_" + key)
                                       for key in ("compiler", "helper", "review", "field"))
    native = review.Native(args.repo, field)
    wires, xcount = compiler.physical_slots(native, args.repo, helper)
    component, f, atlas, previous = construction.context(args.repo)
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    components = construction.build(component, f, atlas, previous, prm)
    args.out.mkdir(parents=True, exist_ok=True)
    totals, per_donor, hashes, all_y = Counter(), {}, {}, set()
    for j in (0, 61, 62):
        records, placements, costs, digests = {}, {}, Counter(), {}
        for k, data in components.items():
            chart = review.Chart(native, 263, k)
            bill, perm, late, stream = compiler.compile_one(helper, review, chart, j, data["maps"][j],
                                                           prm[str(k)]["early"][str(j)], {263}, wires, xcount, records)
            construction.require(not set(placements) & set(perm) and not all_y.intersection(late),
                                 "distinct original source owners and distinct late caches")
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
    construction.require(6*len(all_y) == totals["INIT"], "one paid cache per actual late field")
    background = json.loads(paths["background"].read_bytes())
    construction.require(set(map(int, background)) == set(range(111)), "complete frozen source invoice")
    bg = Counter()
    for j in range(111):
        if j not in (0, 61, 62):
            bg.update(background[str(j)])
    inverse = bg["early_basis_ADD"] + bg["source_owner_permutation_ADD"]
    cache = bg["snapshot_copy_ADD_INIT_dirty_CLEAR"]
    forward = inverse + cache + bg["late_evaluation_ADD"]
    source = {"donors": 111, "source_forward_ADD": forward + totals["forward_ADD"],
              "source_pure_inverse_ADD": inverse + totals["inverse_ADD"],
              "source_forward_and_inverse_ADD": forward + inverse + totals["total_ADD"],
              "source_INIT": cache + totals["INIT"], "source_dirty_CLEAR": cache + totals["dirty_CLEAR"],
              "source_extra_MOVE": 0}
    routes = helper.load_payload(base / helper.ROUTES[0], helper.ROUTES[1])
    h_bill, h_hashes, h_stream, h_body = compile_H(components, helper, atlas, wires, routes)
    if args.emit_words:
        helper.save_compressed(args.out / "H263-REDUCE.bin.gz", h_stream)
        helper.save_compressed(args.out / "H263-HOLDERS.json.gz", h_body)
    combined = {**source, "source_and_H_forward_ADD": source["source_forward_ADD"] + h_bill["H_forward_ADD"],
                "source_and_H_inverse_ADD": source["source_pure_inverse_ADD"] + h_bill["H_inverse_ADD"],
                "source_and_H_forward_and_inverse_ADD": source["source_forward_and_inverse_ADD"] + h_bill["H_forward_and_inverse_ADD"]}
    result = {"status": "PASS_PAID_GEOMETRIC_SOURCE_AND_H_COMPILER", "parameters_sha256": sha256(raw).hexdigest(),
              "source_pins": {str(path.relative_to(args.repo)): sha256(path.read_bytes()).hexdigest() for path in paths.values()},
              "routes_payload_sha256": helper.ROUTES[1], "special_donor_count": 3, "background_donor_count": 108,
              "special": dict(totals), "special_donor_costs": per_donor, "all_source_word_hashes": hashes,
              "background": dict(bg), "all111_source": source, "H263": h_bill, "H263_hashes": h_hashes,
              "combined": combined, "other_H_D_K_F_and_return_cost": None,
              "source_and_H_custody_complete_for_claimed_word": True, "new_complete_kappa": False}
    (args.out / "COST.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"source": source, "H263": h_bill, "combined": combined}, sort_keys=True))


if __name__ == "__main__":
    main()
