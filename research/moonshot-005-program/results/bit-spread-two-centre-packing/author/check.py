#!/usr/bin/env python3
"""Verify two attainable packing bounds and every physical native singleton repair."""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np


def module(path,name):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo",required=True,type=Path)
    cli.add_argument("--out",required=True,type=Path)
    args = cli.parse_args()
    base = args.repo/"research/moonshot-005-program/results"
    f = module(base/"bit-spread-disjoint-h-sources/author/families.py","families")
    pair = module(base/"bit-spread-overlap-source/author/pair.py","paired_source")
    patch = module(base/"bit-spread-singleton-fibre-repair/author/check.py","singleton_source")
    atlas = f.Atlas(args.repo)
    directory = Path(__file__).resolve().parent/"output"
    pbytes = (directory/"PARAMETERS.json").read_bytes()
    sbytes = (directory/"SINGLETONS.json.gz").read_bytes()
    f.require(hashlib.sha256(pbytes).hexdigest() == "972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c",
              "all pair parameter bytes")
    f.require(hashlib.sha256(sbytes).hexdigest() == "107eb64f87489ee31b2fae02f3f93d512bd5a5cf2485d78181dd825d35d21526",
              "literal singleton replacements")
    doc = json.loads(pbytes)
    changed = {(r["h"],r["k"],r["donor"]):r for r in json.loads(gzip.decompress(sbytes))}
    params = {tuple(r["centres"]):r for r in doc["pairs"]}
    single_donors = {j for (j,p),n in atlas.quota.items() if n == 45}
    eligible = {j for j in atlas.native if j != 10 and atlas.algebra.polar(atlas.masks[j],atlas.masks[80])}
    f.require(len(eligible) == 47 and len(eligible-single_donors) == 46, "packing resources")
    dual_eligibility = [h for h,P in enumerate(atlas.planes) if P<=atlas.native
                        and 10 not in P and not P<=atlas.adj[80]]
    f.require(all(len(atlas.planes[h] & eligible) == 2 for h in dual_eligibility),
              "two units of the packing resource in every eligible chart")
    covered = set()
    summary = {}
    details = {}
    singleton_results = []
    for name in ("singleton_free_30","complete_31"):
        placement = doc[name]
        used, charts = set(), []
        for h,q,j in placement["pairs"]:
            par = params[h,q]
            U = atlas.planes[h] | atlas.planes[q]
            f.require(j == par["shared_donor"] and h in dual_eligibility and q in dual_eligibility
                      and j in eligible and len(U) == 5 and not (U & used),
                      "disjoint two-centre structures with a nonorthogonal common donor")
            used.update(U)
            charts.extend((h,q))
            for k in (3,12):
                key = h,q,k
                if key in covered:
                    continue
                contexts, rows, status = pair.pair_source(atlas,f,k,par)
                for ctx in contexts:
                    for donor in ctx.donors:
                        if donor not in single_donors:
                            continue
                        f.require(donor != j,"the physical singleton is on a leaf donor")
                        r = changed[ctx.h,k,donor]
                        ans = patch.check_one(f,atlas,pair.null_basis,ctx,donor,r["singleton"],rows[donor],
                                              par[str(k)]["early"][str(donor)],np.asarray(r["S"],dtype=np.uint8))
                        singleton_results.append(ans)
                covered.add(key)
            details[f"{h}/{q}"] = {"shared_donor":j,"donor_roots":sorted(U)}
        for h in placement["singles"]:
            f.require(h == 138 and not (atlas.planes[h] & used)
                      and not (atlas.planes[h] & single_donors), "one admissible independent centre")
            used.update(atlas.planes[h])
            charts.append(h)
            for k in (3,12):
                ctx = f.Chart(atlas,h,k)
                r = doc["one_centre"][str(k)]
                table = ctx.point_table(r["core"],r["fill"])
                ctx.check_readouts(table,ctx.controls)
                for donor in ctx.donors:
                    rows = ctx.maps(table,donor)
                    ctx.early(donor,rows,r["early"][str(donor)])
                    ctx.source_views(rows,donor,full_rank=False)
        available = eligible-single_donors if name == "singleton_free_30" else eligible
        f.require(set(charts) == set(placement["charts"]) and len(charts) == (2*len(available))//3,
                  "attains the one/two-centre packing ceiling")
        if name == "singleton_free_30":
            f.require(not (used & single_donors),"no selected donor ever enters a singleton chart")
        generic = {}
        for donor in atlas.native-used:
            atlas.previous.ordinary_source(donor,atlas.planes,atlas.quota)
            if donor in single_donors:
                generic[donor] = {k:f.generic_singleton(atlas,donor,k) for k in (3,12)}
        counts = {h:sum(atlas.planes[h] <= atlas.adj[i] for i in atlas.native) for h in charts}
        phases = Counter("fully_early" if all(atlas.quota[j,h] == 30 for j in atlas.planes[h])
                         else "mixed" for h in charts)
        number = sum(len(atlas.adj[j] & atlas.native) for j in used)
        summary[name] = {"H_charts":len(charts),"native_H_inverse_graphs":sum(counts.values()),
                         "native_foreign_blocks_on_designated_H_fibres":3*sum(counts.values()),
                         "per_chart_native_views":counts,"centre_phases":dict(phases),
                         "source_stars":len(used),"remaining_generic_donors":111-len(used),
                         "physical_foreign_cuts_special":number,"physical_foreign_cuts_generic":6470-number,
                         "all_actual_source_H_foreign_ranks":6470,"actual_early_bases":111,
                         "packing_resource":len(available),"sharp_class_ceiling":(2*len(available))//3,
                         "generic_singletons":generic}
    f.require(len(singleton_results) == len(changed) == 16, "coverage of every changed singleton")
    result = {"status":"PASS_SHARP_30_AND_31_PHYSICAL_H_CHART_PACKINGS","placements":summary,
              "individually_replayed_chart_pairs":len(covered)//2,"pair_components":details,
              "physical_singleton_replacements":singleton_results,"shared_D_K_endpoint":False,
              "new_complete_kappa":False}
    args.out.mkdir(exist_ok=True,parents=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"],[(name,data["native_H_inverse_graphs"])for name,data in summary.items()])

if __name__=="__main__":
    main()
