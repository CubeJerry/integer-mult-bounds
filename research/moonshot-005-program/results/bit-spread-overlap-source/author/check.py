#!/usr/bin/env python3
"""Rebuild the source shared by H263 and H642 and its two global placements."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
from pair import pair_source


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    args = cli.parse_args()
    path = args.repo / "research/moonshot-005-program/results/bit-spread-disjoint-h-sources/author/families.py"
    spec = importlib.util.spec_from_file_location("source_families",path)
    f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    atlas = f.Atlas(args.repo)
    raw = (Path(__file__).parent/"output/PARAMETERS.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    f.require(digest == "9fb6002b7838d0b8102a566836e5115f923d3c1678478968f41e42741ae5ca03",
              "frozen source parameter table")
    doc = json.loads(raw)
    solo = {(r["H"],r["k"]):r for r in doc["one_centre"]}
    receipt = {"status":"PASS_COMMON_SOURCE_AT_TWO_OVERLAPPING_H_CHARTS","parameters_sha256":digest,
               "pair":{},"placements":{},"common_D_K_endpoint":False,"new_complete_kappa":False}
    f.require(doc["pair"]["centres"] == [263,642] and doc["pair"]["shared_donor"] == 61,
              "reference coupled centres")
    shared = doc["pair"]["shared_donor"]
    centres = doc["pair"]["centres"]
    used_pair = set.union(*(atlas.planes[h] for h in centres))
    verified = set()
    extra_by_star = Counter(j for (j,h),z in atlas.quota.items() if z == 45)
    for k in (3,12):
        charts, maps, status = pair_source(atlas,f,k,doc["pair"])
        f.require(set(maps) == used_pair and len(maps[shared]) == 28,"all five actual donor stars")
        receipt["pair"][str(k)] = status
    for label in ("native_all_views_packing","extended_ordinary_packing"):
        used = set(used_pair)
        counts = {h:len(atlas.native & {i for i in range(120) if atlas.planes[h] <= atlas.adj[i]})
                  for h in centres}
        physical_unaffected = sum(counts.values())
        for h in doc[label]:
            if h in centres:
                continue
            f.require(not (used & atlas.planes[h]),"only the two designated centres meet")
            used.update(atlas.planes[h])
            f.require(10 not in atlas.planes[h] and not atlas.planes[h] <= atlas.adj[80],
                      "all designated native target blocks identity")
            for k in (3,12):
                chart = f.Chart(atlas,h,k)
                if (h,k) not in verified:
                    p = solo[h,k]
                    point_maps = chart.point_table(p["core"],p["fill"])
                    chart.check_readouts(point_maps,chart.controls)
                    for j in chart.donors:
                        rows = chart.maps(point_maps,j)
                        chart.early(j,rows,p["early"][str(j)])
                        chart.source_views(rows,j,full_rank=False)
                    verified.add((h,k))
            visible = set(chart.views) & atlas.native
            counts[h] = len(visible)
            singles = {p for j in chart.donors for p in atlas.by_donor[j] if atlas.quota[j,p] == 45}
            physical_unaffected += sum(not any(atlas.planes[p] <= atlas.adj[i] for p in singles)
                                       for i in visible)
        exceptions = sorted(used & set(extra_by_star))
        if label == "native_all_views_packing":
            f.require(not exceptions, "no singleton on any designated donor star")
        generic_rows = {}
        for j in atlas.native - used:
            atlas.previous.ordinary_source(j,atlas.planes,atlas.quota)
            if j in extra_by_star:
                generic_rows[j] = {k:f.generic_singleton(atlas,j,k) for k in (3,12)}
        special_n = sum(len(atlas.adj[j] & atlas.native) for j in used)
        total = sum(len(atlas.adj[j] & atlas.native) for j in atlas.native)
        f.require(total == 6470,"all native sources counted")
        receipt["placements"][label] = {"native_H_charts":len(counts),"per_chart_H_views":counts,
               "native_H_ordinary_inverse_graphs":sum(counts.values()),"donor_stars":len(used),
               "ordinary_source_views_special":special_n,"ordinary_source_views_generic":total-special_n,
               "fully_verified_native_H_inverse_fibres_before_singleton_repair":physical_unaffected,
               "selected_donors_with_singletons":exceptions,"generic_singleton_physical_checks":generic_rows,
               "actual_early_bases":111}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print(receipt["status"],[(v["native_H_charts"],v["native_H_ordinary_inverse_graphs"])
                           for v in receipt["placements"].values()])

if __name__=="__main__":
    main()
