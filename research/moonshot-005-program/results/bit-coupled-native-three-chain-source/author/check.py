#!/usr/bin/env python3
"""Check all source cuts, whole inverse fibres, phases and non-RS witnesses."""
from __future__ import annotations

from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import ctypes
import json
from pathlib import Path
import numpy as np
import construction


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--rank-library", type=Path)
    args = p.parse_args()
    f, atlas, previous = construction.context(args.repo)
    if args.rank_library:
        library = ctypes.CDLL(str(args.rank_library))
        native_rank = library.field_rank
        native_rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        native_rank.restype = ctypes.c_int
        def fast_rank(matrix):
            matrix = np.array(matrix, dtype=np.uint8, order="C", copy=True)
            return native_rank(matrix.ctypes.data, *matrix.shape, atlas.product.ctypes.data, atlas.inverse.ctypes.data)
        atlas.rank = fast_rank
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    centres = prm["centres"]
    source_hashes, component_stats, fibre_counts = {}, {}, {}
    all_maps, all_charts = {}, {}
    for k in (3, 12):
        charts, maps, groups, constraint, embedding = construction.build(f, atlas, previous, centres, k, prm[str(k)]["seed"])
        cuts = native_cuts = 0
        for j, rows in sorted(maps.items()):
            chart = next(chart for chart in charts if j in chart.donors)
            chart.source_views(rows, j)
            chart.early(j, rows, prm[str(k)]["early"][str(j)], fixed_centres=centres)
            cuts += len(atlas.adj[j])
            native_cuts += len(atlas.adj[j] & atlas.native)
            source_hashes[f"{j}/{k}"] = sha256(b"".join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
        for chart in charts:
            j = chart.donors[0]
            points = {x: maps[j][h] for h, x in chart.point[j].items()}
            construction.require(all(np.array_equal(maps[t][h], points[x]) for t in chart.donors for h, x in chart.point[t].items()),
                                 "one common point quotient across all three actual donors")
            chart.check_readouts(points, [maps[t][chart.h] for t in chart.donors])
            fibre_counts[chart.h] = len(set(chart.views) & atlas.native)
        component_stats[k] = {"constraint_shape": list(constraint.shape), "constraint_rank": atlas.rank(constraint),
                              "input_dimension": embedding.shape[1], "quotient_classes": len(set(groups.values())),
                              "geometry_foreign_full_ranks": cuts, "native_foreign_full_ranks": native_cuts,
                              "constraint_sha256": sha256(constraint.tobytes()).hexdigest(),
                              "embedding_sha256": sha256(embedding.tobytes()).hexdigest()}
        all_maps[k], all_charts[k] = maps, charts
    witness_raw = (Path(__file__).parent / "output/NON-RS-WITNESSES.json").read_bytes()
    witnesses = json.loads(witness_raw)
    construction.require(set(map(int, witnesses)) == set(all_maps[3]), "every changed source has a non-RS witness")
    for j, witness in witnesses.items():
        rows = all_maps[3][int(j)]
        planes = witness["planes"]
        construction.require(len(planes) == len(set(planes)) == 16 and set(planes) <= set(rows), "sixteen actual source planes")
        rank = atlas.rank(np.vstack([rows[h] for h in planes]))
        construction.require(rank == witness["rank"] < 48, "genuine non-MDS observation")
    # A cut must see every real quotient; deleting one is detected immediately.
    j, i = 0, min(atlas.adj[0] & atlas.native)
    hs = [h for h in all_maps[3][j] if atlas.planes[h] <= atlas.adj[i]]
    original = np.vstack([all_maps[3][j][h] for h in hs])
    damaged = original.copy(); damaged[:3] = 0
    construction.require(atlas.rank(original) == 48 and atlas.rank(damaged) < 48, "source deletion negative control")
    # A wrong donor control must fail the whole-fibre common-port equality.
    chart = all_charts[3][0]
    first = chart.donors[0]
    points = {x: all_maps[3][first][h] for h, x in chart.point[first].items()}
    bad = [all_maps[3][t][chart.h].copy() for t in chart.donors]
    bad[1][0, 0] ^= 1
    try:
        chart.check_readouts(points, bad)
    except ValueError:
        rejected = True
    else:
        rejected = False
    construction.require(rejected, "wrong common control negative control")
    phases = {h: sum(atlas.quota[j, h] for j in atlas.planes[h]) for h in centres}
    construction.require(all(10 not in atlas.planes[h] and not atlas.planes[h] <= atlas.adj[80]
                             for h in centres), "no designated interface lies on either S028 perturbed star")
    dependencies = ["bit-spread-disjoint-h-sources/author/families.py", "bit-spread-overlap-source/author/pair.py"]
    base = args.repo / "research/moonshot-005-program/results"
    out = {"status": "PASS_CONNECTED_THREE_CENTRE_SOURCE", "parameters_sha256": sha256(raw).hexdigest(),
           "non_RS_witnesses_sha256": sha256(witness_raw).hexdigest(), "centres": centres,
           "centre_donors": {h: sorted(atlas.planes[h]) for h in centres}, "early_original_slots_per_centre": phases,
           "source_donors": sorted(all_maps[3]), "components": component_stats,
           "source_coefficient_sha256": source_hashes, "native_common_inverse_fibres": sum(fibre_counts.values()),
           "native_donor_inverse_fibres": 3*sum(fibre_counts.values()), "per_centre_native_receivers": fibre_counts,
           "source_stars_inequivalent_to_RS": len(witnesses), "actual_early_source_bases": len(all_maps[3]),
           "designated_interfaces_avoid_donor10_and_receiver80": True,
           "negative_controls": [{"mutation": "delete_real_source_quotient", "donor": j, "receiver": i,
                                  "original_rank": atlas.rank(original), "damaged_rank": atlas.rank(damaged)},
                                 {"mutation": "change_one_donor_control", "rejected": rejected}],
           "source_pins": {str((base / name).relative_to(args.repo)): sha256((base / name).read_bytes()).hexdigest() for name in dependencies},
           "endpoint_target": "canonical foreign identity on the three designated H interfaces",
           "common_D_K_endpoint": False, "actual_global_return_rank": None,
           "S028_perturbed_target_not_asserted": True, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: out[key] for key in ("status", "native_common_inverse_fibres", "native_donor_inverse_fibres", "source_stars_inequivalent_to_RS")}, sort_keys=True))


if __name__ == "__main__":
    main()
