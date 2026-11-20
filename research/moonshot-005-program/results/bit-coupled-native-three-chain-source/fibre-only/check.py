#!/usr/bin/env python3
"""Exact source, phase and entire-fibre checks without point-table equality."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import ctypes
import json
import numpy as np
import construction as c


def accelerate(atlas, path):
    if path is None:
        return
    lib = ctypes.CDLL(str(path))
    fn = lib.field_rank
    fn.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int
    def rank(M):
        M = np.array(M, dtype=np.uint8, order="C", copy=True)
        return fn(M.ctypes.data, *M.shape, atlas.product.ctypes.data, atlas.inverse.ctypes.data)
    atlas.rank = rank


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--rank-library", type=Path)
    args = p.parse_args()
    f, a, previous = c.context(args.repo)
    accelerate(a, args.rank_library)
    raw = (Path(__file__).parent / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    result, hashes = {}, {}
    for k in (3, 12):
        charts, maps, old, groups, R, N, fibres, spaces, flexible = c.build_detailed(f, a, previous, prm["centres"], k, prm[str(k)]["seed"])
        for j, rows in maps.items():
            chart = next(C for C in charts if j in C.donors)
            chart.source_views(rows, j)
            chart.early(j, rows, prm[str(k)]["early"][str(j)], fixed_centres=prm["centres"])
            hashes[f"{j}/{k}"] = sha256(b"".join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
        for chart in charts:
            for i in chart.views:
                K = fibres[chart.h, i]
                ports = [q for q, d in enumerate(chart.ports) if a.charts[d] <= a.adj[i]]
                common = None
                for pos, j in enumerate(chart.donors):
                    off = np.vstack([maps[j][h] for h in maps[j] if h != chart.h and a.planes[h] <= a.adj[i]])
                    c.require(a.rank(off) == 15*k and not np.any(a.mm(off, K)), "entire common inverse fibre")
                    read = a.mm(a.mm(chart.V[np.ix_(ports, range(pos*k, (pos+1)*k))], maps[j][chart.h]), K)
                    c.require(a.rank(read) == k, "injective common readout")
                    if common is None:
                        common = read
                    else:
                        c.require(np.array_equal(read, common), "same complete port readout")
        changed = {}
        for (j, h), E in flexible.items():
            union = a.rank(np.vstack([old[j][h], maps[j][h]]))
            c.require(a.rank(maps[j][h]) == k and union == len(E) > k, "different actual quotient kernel")
            changed[f"{j}/{h}"] = {"annihilator_dimension": len(E), "old_rank": a.rank(old[j][h]), "new_rank": a.rank(maps[j][h]), "union_rank": union}
        # A general coefficient edit outside the permitted row space is rejected.
        damaged = maps[0][116].copy()
        damaged[0, 0] ^= 1
        c.require(a.rank(np.vstack([spaces[0, 116], damaged])) > len(spaces[0, 116]), "outside-annihilator negative control")
        result[k] = {"changed_quotient_kernels": changed,
                     "native_source_full_ranks": sum(len(a.adj[j] & a.native) for j in maps),
                     "geometric_source_full_ranks": sum(len(a.adj[j]) for j in maps),
                     "geometric_common_fibres": sum(len(C.views) for C in charts),
                     "native_common_fibres": sum(len(set(C.views) & a.native) for C in charts),
                     "actual_early_source_bases": len(maps),
                     "fibre_annihilator_dimensions": {f"{j}/{h}": len(E) for (j, h), E in spaces.items()},
                     "negative_control_rejected": True}
    out = {"status": "PASS_FIBRE_ONLY_CONNECTED_SOURCE", "parameters_sha256": sha256(raw).hexdigest(),
           "centres": prm["centres"], "source_donors": sorted(maps), "components": result,
           "source_coefficient_sha256": hashes,
           "genuinely_donor_dependent_quotient_flags": [[0, 116], [25, 394], [47, 652], [62, 643]],
           "common_D_K_endpoint": False, "actual_global_return_rank": None, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "native_common_fibres": result[3]["native_common_fibres"]}, sort_keys=True))


if __name__ == "__main__":
    main()
