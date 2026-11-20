#!/usr/bin/env python3
"""Verify every source cut, early basis, and common fibre on the closed cycle."""
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
    geometric, f, a, previous = construction.context(args.repo)
    if args.rank_library:
        library = ctypes.CDLL(str(args.rank_library))
        native_rank = library.field_rank
        native_rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        native_rank.restype = ctypes.c_int
        def fast_rank(matrix):
            matrix = np.array(matrix, dtype=np.uint8, order="C", copy=True)
            return native_rank(matrix.ctypes.data, *matrix.shape, a.product.ctypes.data, a.inverse.ctypes.data)
        a.rank = fast_rank
    here = Path(__file__).parent
    raw = (here / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    local, embeddings, maps, bases = construction.build(geometric, f, a, previous, prm)
    coefficient_raw = (here / "output/COEFFICIENTS.json").read_bytes()
    saved = json.loads(coefficient_raw)
    hashes = {}
    cuts = native_cuts = 0
    for j, rows in maps.items():
        construction.require(set(map(int, saved[str(j)])) == set(rows), "every actual source flag recorded")
        construction.require(all(np.array_equal(rows[h], np.asarray(saved[str(j)][str(h)], dtype=np.uint8)) for h in rows),
                             "literal frozen source coefficient table")
        chart = next(data["chart"] for data in local.values() if j in data["chart"].donors)
        chart.source_views(rows, j)
        chart.early(j, rows, prm["early"][str(j)], fixed_centres=prm["centres"])
        cuts += len(a.adj[j])
        native_cuts += len(a.adj[j] & a.native)
        hashes[j] = sha256(b"".join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
    fibre_counts = {}
    different_kernel_ranks = Counter()
    for h, data in local.items():
        chart = data["chart"]
        for i, Z in data["coordinates"].items():
            K = a.mm(embeddings[h], Z)
            construction.require(a.rank(K) == 3, "whole common fibre injection")
            visible = [q for q, d in enumerate(chart.ports) if a.charts[d] <= a.adj[i]]
            images = []
            for p, j in enumerate(chart.donors):
                off = np.vstack([rows for q, rows in maps[j].items() if q != h and a.planes[q] <= a.adj[i]])
                construction.require(a.rank(off) == 45 and not np.any(a.mm(off, K)),
                                     "same complete original-coordinate inverse fibre for every donor")
                images.append(a.mm(a.mm(data["Hword"][np.ix_(visible, range(3*p, 3*(p+1)))], maps[j][h]), K))
            construction.require(a.rank(images[0]) == 3 and np.array_equal(images[0], images[1])
                                 and np.array_equal(images[0], images[2]), "common injective actual-port readout")
        fibre_counts[h] = {"geometric": len(chart.views), "native": len(set(chart.views) & a.native)}
        for x in chart.singular:
            flags = [(j, next(q for q, point in chart.point[j].items() if point == x)) for j in chart.donors]
            for first, second in ((0, 1), (0, 2), (1, 2)):
                j, p = flags[first]; k, q = flags[second]
                different_kernel_ranks[a.rank(np.vstack([maps[j][p], maps[k][q]]))] += 1
    witness_raw = (here / "output/NON-RS-WITNESSES.json").read_bytes()
    witnesses = json.loads(witness_raw)
    construction.require(set(map(int, witnesses)) == set(maps), "all eight non-RS source witnesses")
    for j, witness in witnesses.items():
        planes = witness["planes"]
        construction.require(len(set(planes)) == 16 and set(planes) <= set(maps[int(j)]), "sixteen actual quotient observations")
        construction.require(a.rank(np.vstack([maps[int(j)][h] for h in planes])) == witness["rank"] == 47,
                             "source invariant defeats arbitrary RS input/output bijections")
    i = min(a.adj[0] & a.native)
    damaged = np.vstack([F for h, F in maps[0].items() if a.planes[h] <= a.adj[i]])
    damaged[:3] = 0
    construction.require(a.rank(damaged) == 45, "source deletion negative control")
    collapsed = np.hstack([embeddings[263], embeddings[263]])
    construction.require(a.rank(collapsed) == 18 < 36, "identified incident cores fail source prescription")
    phases = {h: sum(a.quota[j, h] for j in a.planes[h]) for h in prm["centres"]}
    construction.require(phases == {263: 90, 642: 90, 135: 45, 44: 45}, "two fully early and two mixed native centres")
    construction.require(all(10 not in a.planes[h] and not a.planes[h] <= a.adj[80] for h in prm["centres"]),
                         "all designated interfaces avoid the perturbed stars")
    port_decisions = {}
    for h, data in local.items():
        for d, D in enumerate(a.charts):
            if a.planes[h] <= D:
                port_decisions.setdefault(d, set()).add(d in data["chart"].ports)
    construction.require(all(len(values) == 1 for values in port_decisions.values()),
                         "the component allocation agrees at every shared D exit")
    predecessor = args.repo / "research/moonshot-005-program/results/bit-coupled-native-geometric-h-source/component"
    result = {"status": "PASS_GEOMETRIC_CLOSED_FOUR_CENTRE_COMPONENT", "centres": prm["centres"],
              "donors": sorted(maps), "source_geometry_cuts": cuts, "source_native_cuts": native_cuts,
              "actual_early_bases": 8, "early_basis_dimension": 96, "source_dimension": 48, "quotient_width": 3,
              "common_fibres": fibre_counts, "geometric_common_fibres": sum(v["geometric"] for v in fibre_counts.values()),
              "native_common_fibres": sum(v["native"] for v in fibre_counts.values()), "actual_H_early_slots": phases,
              "consistent_shared_D_component_allocation": True,
              "off_centre_pair_rowspace_union_ranks": dict(different_kernel_ranks),
              "source_stars_inequivalent_to_RS": 8, "source_coefficient_sha256": hashes,
              "parameters_sha256": sha256(raw).hexdigest(), "coefficients_sha256": sha256(coefficient_raw).hexdigest(),
              "non_RS_witnesses_sha256": sha256(witness_raw).hexdigest(),
              "predecessor_pins": {str(p.relative_to(args.repo)): sha256(p.read_bytes()).hexdigest()
                                   for p in (predecessor / "construction.py", predecessor / "MANIFEST.json")},
              "negative_controls": {"source_deletion_rank": a.rank(damaged), "collapsed_two_core_rank": a.rank(collapsed)},
              "full_bank_companion_built": False, "complete_physical_invoice": None,
              "all_other_H_D_K_F_and_return": None, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "source_native_cuts", "native_common_fibres", "off_centre_pair_rowspace_union_ranks")}, sort_keys=True))


if __name__ == "__main__":
    main()
