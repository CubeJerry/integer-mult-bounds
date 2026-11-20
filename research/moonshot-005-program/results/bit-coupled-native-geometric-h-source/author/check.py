#!/usr/bin/env python3
"""Check the complete3+12 source and all45 actual H263 outputs."""
from argparse import ArgumentParser
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
    component, f, a, previous = construction.context(args.repo)
    if args.rank_library:
        library = ctypes.CDLL(str(args.rank_library))
        native_rank = library.field_rank
        native_rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        native_rank.restype = ctypes.c_int
        def fast_rank(matrix):
            matrix = np.array(matrix, dtype=np.uint8, order="C", copy=True)
            return native_rank(matrix.ctypes.data, *matrix.shape, a.product.ctypes.data, a.inverse.ctypes.data)
        a.rank = fast_rank
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    components = construction.build(component, f, a, previous, prm)
    stats = {}
    port_union = set()
    for k, data in components.items():
        chart, maps = data["chart"], data["maps"]
        construction.require(not port_union & set(chart.ports), "disjoint component exits")
        port_union.update(chart.ports)
        geometric_cuts = native_cuts = 0
        for j, rows in maps.items():
            chart.source_views(rows, j)
            chart.early(j, rows, prm[str(k)]["early"][str(j)])
            geometric_cuts += len(a.adj[j])
            native_cuts += len(a.adj[j] & a.native)
        for i in chart.views:
            off = np.vstack([data["points"][x] for x in chart.singular if not a.algebra.polar(x, a.masks[i])])
            K = previous.null_basis(off, a)
            construction.require(K.shape == (16*k, k), "whole component inverse fibre")
            visible = [p for p, d in enumerate(chart.ports) if a.charts[d] <= a.adj[i]]
            construction.require(len(visible) == k, "exact native component exit count")
            readouts = [a.mm(a.mm(data["Hword"][np.ix_(visible, range(p*k, (p+1)*k))], maps[j][chart.h]), K)
                        for p, j in enumerate(chart.donors)]
            construction.require(a.rank(readouts[0]) == k and np.array_equal(readouts[0], readouts[1])
                                 and np.array_equal(readouts[0], readouts[2]), "common complete component readout")
        stats[k] = {"source_geometry_cuts": geometric_cuts, "source_native_cuts": native_cuts,
                    "geometric_common_fibres": len(chart.views), "native_common_fibres": len(set(chart.views) & a.native),
                    "early_basis_dimension": 32*k, "H_word_dimension": 3*k, "ports": chart.ports,
                    "source_coefficient_sha256": {str(j): sha256(b"".join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
                                                  for j, rows in sorted(maps.items())},
                    "H_word_sha256": sha256(data["Hword"].tobytes()).hexdigest()}
    construction.require(port_union == {d for d, D in enumerate(a.charts) if a.planes[prm["H"]] <= D},
                         "every actual H exit, with no duplicated or omitted port")
    # Reuse the frozen information witnesses and verify their full-bank consequence.
    witness_path = Path(__file__).parent.parent / "component/output/NON-RS-WITNESSES.json"
    witnesses = json.loads(witness_path.read_text())
    full_witnesses = {}
    for j, witness in witnesses.items():
        ranks = {k: a.rank(np.vstack([data["maps"][int(j)][h] for h in witness["planes"]])) for k, data in components.items()}
        rank = 16*sum(ranks.values())
        construction.require(ranks[3] == 47 and rank < 3840, "genuine non-RS full-bank information loss")
        full_witnesses[j] = {"component_ranks": ranks, "whole_bank_rank": rank}
    component_dir = Path(__file__).parent.parent / "component"
    result = {"status": "PASS_COMPLETE_GEOMETRIC_RAMP_H_SOURCE", "H": prm["H"], "donors": [0, 61, 62],
              "parameters_sha256": sha256(raw).hexdigest(), "components": stats,
              "full_bank_dimension": 3840, "ordinary_quotient_width": 240, "physical_H_original_early_inputs": 720,
              "physical_H_outputs": 720, "actual_D_exits": 45, "physical_fields_per_exit": 16,
              "full_bank_native_common_fibres": 33, "full_bank_geometric_common_fibres": 36,
              "full_bank_non_RS_witnesses": full_witnesses,
              "component_pins": {str(p.resolve().relative_to(args.repo.resolve())): sha256(p.read_bytes()).hexdigest()
                                 for p in (component_dir / "construction.py", component_dir / "MANIFEST.json",
                                           component_dir / "output/PARAMETERS.json", witness_path)},
              "changed_H_component_allocation": True, "common_D_K_endpoint": False,
              "actual_global_return_rank": None, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "actual_D_exits", "full_bank_native_common_fibres")}, sort_keys=True))


if __name__ == "__main__":
    main()
