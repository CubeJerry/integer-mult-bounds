#!/usr/bin/env python3
"""Reproduce the maximum-size donor-disjoint H chart certificate."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from families import Atlas, Chart, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    atlas = Atlas(args.repo)
    raw = (root / "output/PARAMETERS.json").read_bytes()
    table = {(int(r["H"]),int(r["k"])):r for r in json.loads(raw)}
    charts = sorted({263} | {h for h,k in table})
    single = gzip.decompress((atlas.previous_path / "output/COEFFICIENTS.json.gz").read_bytes())
    old = json.loads(single)["components"]
    require(set(table) == {(h,k) for h in charts if h != 263 for k in (3,12)},
            "complete two-component witness list")
    available = {j for j in atlas.native if j != 10 and
                 atlas.algebra.polar(atlas.masks[j],atlas.masks[80])}
    eligible = [h for h,P in enumerate(atlas.planes) if P <= atlas.native
                and 10 not in P and not P <= atlas.adj[80]]
    require(len(available) == 47 and len(eligible) == 540 and
            all(len(atlas.planes[h] & available) == 2 for h in eligible),
            "dual cardinality certificate on every eligible chart")
    require(set(charts) <= set(eligible) and len(charts) == 47//2, "upper bound attained")
    used = set()
    phases = Counter()
    counts = {}
    source_rows = 0
    coefficient_digest = hashlib.sha256()
    predecessor_datasets = (atlas.algebra, atlas.planes, atlas.charts, atlas.masks, atlas.adj,
                            atlas.quota, atlas.spread)
    for h in charts:
        require(used.isdisjoint(atlas.planes[h]), "unchanged source stars are donor-disjoint")
        used.update(atlas.planes[h])
        amounts = {atlas.quota[j,h] for j in atlas.planes[h]}
        require(amounts in ({15},{30}), "matching physical chart phases for all three donors")
        phases["fully_early" if amounts == {30} else "mixed"] += 1
        for k in (3,12):
            c = Chart(atlas,h,k)
            counts[h] = len(atlas.native & set(c.views))
            if h == 263:
                native = [i for i in c.views if i in atlas.native]
                ports = [d for d,D in enumerate(atlas.charts) if atlas.planes[h] <= D]
                parts = c.donors,c.point,c.singular,native,c.views,ports
                atlas.previous.check_component(k,parts,predecessor_datasets,old[str(k)],
                                               (atlas.product,atlas.inverse))
            else:
                p = table[h,k]
                T = c.point_table(p["core"], p["fill"])
                c.check_readouts(T,c.controls)
                for x in c.singular:
                    coefficient_digest.update(T[x].tobytes())
                for donor in c.donors:
                    maps = c.maps(T,donor)
                    c.source_views(maps,donor,full_rank=False)
                    c.early(donor,maps,p["early"][str(donor)])
        source_rows += sum(len(atlas.adj[j] & atlas.native) for j in atlas.planes[h])
    generic = 0
    for donor in sorted(atlas.native-used):
        nodes = atlas.previous.ordinary_source(donor,atlas.planes,atlas.quota)
        for i in atlas.adj[donor] & atlas.native:
            row = [n for h,n in nodes.items() if atlas.planes[h] <= atlas.adj[i]]
            require(len(row) == len(set(row)) == 16, "remaining donor ordinary MDS")
            generic += 1
    require(generic + source_rows == 6470, "all native foreign sources")
    output = {"status":"PASS_23_DISJOINT_IDENTITY_SAFE_H_CHARTS","charts":charts,
              "native_H_receiver_views":sum(counts.values()),"per_chart_native_views":counts,
              "phase_classes":dict(phases),"covered_donors":len(used),"remaining_MDS_donors":111-len(used),
              "native_source_views":6470,"actual_early_bases":111,"eligible_charts":540,
              "eligible_nonorthogonal_roots":47,"maximum_disjoint_charts_in_scope":23,
              "parameters_sha256":hashlib.sha256(raw).hexdigest(),
              "additional_scalar_source_tables_sha256":coefficient_digest.hexdigest(),
              "global_D_K_endpoint":False,"new_complete_kappa":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print(output["status"],sum(counts.values()),"native receiver-chart views",dict(phases))

if __name__=="__main__":
    main()
