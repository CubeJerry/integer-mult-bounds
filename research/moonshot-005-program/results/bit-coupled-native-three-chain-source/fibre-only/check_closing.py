#!/usr/bin/env python3
"""Exclude five closing centres only when the old inverse fibres are retained."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json
import numpy as np
import construction as c
from check import accelerate


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--rank-library", type=Path)
    args = p.parse_args()
    f, a, previous = c.context(args.repo)
    accelerate(a, args.rank_library)
    directory = Path(__file__).parent / "output"
    prm = json.loads((directory / "PARAMETERS.json").read_bytes())
    raw = (directory / "CLOSING-WITNESSES.json").read_bytes()
    witnesses = json.loads(raw)
    records = {row["H"]: {"H": row["H"], "receiver": row["receiver"], "component_ranks": {}} for row in witnesses}
    for k in (3, 12):
        charts, maps, _, _, _ = c.hybrid(f, a, previous, prm["centres"], k)
        _, spaces = c.fibres_and_spaces(a, previous, charts, maps, k, native_only=True)
        donors = set(maps)
        candidates = {h for h, P in enumerate(a.planes) if P <= a.native and len(P & donors) >= 2 and h not in prm["centres"]}
        c.require(set(records) == candidates == {44, 116, 394, 643, 652}, "complete native closing census")
        for row in witnesses:
            h, i = row["H"], row["receiver"]
            flags = [tuple(flag) for flag in row["fixed_flags"]]
            c.require(i in a.native and a.planes[h] <= a.adj[i] and len(flags) == len(set(flags)) == 16, "actual receiver and sixteen distinct source observations")
            for j, q in flags:
                c.require(j in a.planes[h] and q != h and q not in prm["centres"] and a.planes[q] <= a.adj[i], "off-centre saturated flags only")
                c.require(len(spaces[j, q]) == k, "old fibres force the whole quotient row space")
            rank = a.rank(np.vstack([spaces[flag] for flag in flags]))
            c.require(rank == 16*k, "no common inverse direction survives these fixed observations")
            c.require(a.rank(np.vstack([spaces[flag] for flag in flags[1:]])) == 15*k, "deleting one witness block lowers the rank by its full width")
            records[h]["component_ranks"][k] = rank
            records[h]["existing_donors"] = sorted(a.planes[h] & donors)
    for row in records.values():
        row["full_bank_fixed_observation_rank"] = 16*sum(row["component_ranks"].values())
        row["common_inverse_kernel_dimension"] = 0
    out = {"status": "PASS_FROZEN_FIBRE_CLOSING_CENSUS", "witnesses_sha256": sha256(raw).hexdigest(),
           "centres": prm["centres"], "source_donors": sorted(donors), "closing_census": list(records.values()),
           "scope": "all linear source changes retaining the 101 specified native whole inverse fibres and native source rank; five native centres with at least two old donors",
           "retained_native_common_fibres": 101,
           "arbitrary_full_bank_mixing_allowed": True, "all_central_and_flexible_rows_ignored": True,
           "negative_control_drop_one_witness_block_rank": {"3": 45, "12": 180, "full_bank": 3600},
           "moving_old_fibres_excluded_from_claim": True, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "CLOSING-RESULT.json").write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "excluded": len(records)}, sort_keys=True))


if __name__ == "__main__":
    main()
