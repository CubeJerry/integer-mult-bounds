#!/usr/bin/env python3
"""Replay the three-dimensional geometric component and its actual H word."""
from argparse import ArgumentParser
from hashlib import sha256
import ctypes
import json
from pathlib import Path
import numpy as np
import construction


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--rank-library", type=Path)
    args = parser.parse_args()
    f, a, pair = construction.context(args.repo)
    if args.rank_library:
        library = ctypes.CDLL(str(args.rank_library))
        rank = library.field_rank
        rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        rank.restype = ctypes.c_int
        def fast_rank(matrix):
            matrix = np.array(matrix, dtype=np.uint8, order="C", copy=True)
            return rank(matrix.ctypes.data, *matrix.shape, a.product.ctypes.data, a.inverse.ctypes.data)
        a.rank = fast_rank
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    data = construction.build(f, a, pair, prm)
    chart, maps = data["chart"], data["maps"]
    cuts = native_cuts = 0
    hashes = {}
    for j, rows in sorted(maps.items()):
        chart.source_views(rows, j)
        chart.early(j, rows, prm["early"][str(j)])
        cuts += len(a.adj[j])
        native_cuts += len(a.adj[j] & a.native)
        hashes[str(j)] = sha256(b"".join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
    common = native_common = 0
    wrong_control_rejections = 0
    for i, K in data["fibres"].items():
        visible = [q for q, d in enumerate(chart.ports) if a.charts[d] <= a.adj[i]]
        readouts = [a.mm(a.mm(data["Hword"][np.ix_(visible, range(3*p, 3*(p+1)))], maps[j][chart.h]), K)
                    for p, j in enumerate(chart.donors)]
        construction.require(a.rank(readouts[0]) == 3 and np.array_equal(readouts[0], readouts[1])
                             and np.array_equal(readouts[0], readouts[2]), "literal source-to-port common readout")
        common += 1
        native_common += i in a.native
        bad = maps[chart.donors[1]][chart.h].copy()
        bad[0, 0] ^= 1
        changed = a.mm(a.mm(data["Hword"][np.ix_(visible, range(3, 6))], bad), K)
        wrong_control_rejections += not np.array_equal(changed, readouts[0])
    construction.require(wrong_control_rejections > 0, "a wrong central control is rejected")
    witness_raw = (Path(__file__).parent / "output/NON-RS-WITNESSES.json").read_bytes()
    witnesses = json.loads(witness_raw)
    construction.require(set(map(int, witnesses)) == set(maps), "all three donors have source invariants")
    for j, witness in witnesses.items():
        hs = witness["planes"]
        construction.require(len(set(hs)) == 16 and set(hs) <= set(maps[int(j)]), "sixteen actual source planes")
        construction.require(a.rank(np.vstack([maps[int(j)][h] for h in hs])) == witness["rank"] == 47,
                             "non-MDS information witness")
    j, i = 0, min(a.adj[0] & a.native)
    hs = [h for h in maps[j] if a.planes[h] <= a.adj[i]]
    damaged = np.vstack([maps[j][h] for h in hs])
    damaged[:3] = 0
    construction.require(a.rank(damaged) == 45, "deleting a genuine source quotient loses three ranks")
    # Equal weights make the first quadratic annihilator nine-dimensional.
    aa = np.asarray(prm["weights"][0], dtype=np.uint8)
    degenerate = pair.null_basis(a.product[(aa ^ aa)[:, None], data["E2"]].T, a)
    construction.require(degenerate.shape[1] == 9, "equal-weight degeneration rejects the required 3+3+3 construction")
    construction.require(sum(a.quota[j, chart.h] for j in chart.donors) == 90,
                         "the actual fully early H263 owner inventory")
    construction.require(10 not in a.planes[chart.h] and not a.planes[chart.h] <= a.adj[80],
                         "this interface avoids both perturbed S028 stars")
    dependencies = ["bit-spread-disjoint-h-sources/author/families.py", "bit-spread-overlap-source/author/pair.py"]
    base = args.repo / "research/moonshot-005-program/results"
    result = {
        "status": "PASS_GEOMETRIC_QUADRATIC_H_COMPONENT", "H": chart.h, "donors": chart.donors,
        "parameters_sha256": sha256(raw).hexdigest(), "non_RS_witnesses_sha256": sha256(witness_raw).hexdigest(),
        "field": {"size": 64, "binary_modulus": 67}, "component_input_dimension": 48,
        "quotient_width": 3, "whole_fibre_span": a.rank(data["core"]), "source_geometry_cuts": cuts,
        "source_native_cuts": native_cuts, "early_bases": 3, "early_basis_dimension": 96,
        "geometric_common_fibres": common, "native_common_fibres": native_common,
        "actual_H_word_shape": list(data["Hword"].shape), "actual_H_word_rank": a.rank(data["Hword"]),
        "ports": chart.ports, "port_allocation_differs_from_inherited_marking": set(chart.ports) != set(d for d in chart.ports if d in a.marked),
        "source_coefficient_sha256": hashes,
        "matrix_sha256": {name: sha256(data[name].tobytes()).hexdigest() for name in ("E1", "E2", "T", "Hword", "core")},
        "source_stars_inequivalent_to_RS": 3,
        "negative_controls": {"deleted_quotient_rank": a.rank(damaged), "wrong_control_rejected_receivers": wrong_control_rejections,
                              "equal_weights_wrong_annihilator_dimension": degenerate.shape[1]},
        "source_pins": {str((base / path).relative_to(args.repo)): sha256((base / path).read_bytes()).hexdigest() for path in dependencies},
        "remaining_36_port_word_in_this_package": False, "complete_source_and_H_invoice_in_this_package": False,
        "common_D_K_endpoint": False, "actual_global_return_rank": None, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "source_native_cuts", "native_common_fibres", "actual_H_word_rank")}, sort_keys=True))


if __name__ == "__main__":
    main()
