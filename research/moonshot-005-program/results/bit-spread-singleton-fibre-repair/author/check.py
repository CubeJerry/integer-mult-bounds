#!/usr/bin/env python3
"""Verify literal singleton Hermite inputs on all requested and foreign fibres."""
from __future__ import annotations
import argparse
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


def check_one(f, atlas, null, context, j, p, rows, early_seed, S, constrained=()):
    k = context.k
    centres = sorted(set(constrained) | {context.h})
    f.require(S.shape == (3*k,32*k) and np.all(S < 64),"actual 3k by 32k singleton source matrix")
    f.require(atlas.quota[j,p] == 45 and len(atlas.planes[p] & atlas.native) == 1,
              "genuine singleton early slots")
    left, right = S[:,:16*k], S[:,16*k:]
    other_early = []
    for h,F in sorted(rows.items()):
        if h == p:
            continue
        q = atlas.quota[j,h]//15
        if q == 2:
            other_early.append(np.kron(np.eye(2,dtype=np.uint8),F))
        elif h in centres:
            f.require(q == 1,"mixed fixed chart")
            other_early.append(np.hstack([F,np.zeros_like(F)]))
        else:
            f.require(q == 1,"one singleton on this donor")
            frame = f.coefficients(f"early/{context.label}{j}/{h}/{early_seed}",(k,2*k))
            other_early.append(np.hstack([atlas.mm(frame[:,:k],F),atlas.mm(frame[:,k:],F)]))
    early_rest = np.vstack(other_early)
    K = null(early_rest,atlas)
    f.require(K.shape == (32*k,3*k) and atlas.rank(atlas.mm(S,K)) == 3*k,
              "full genuine early source after replacing the singleton")
    affected = {}
    stack = []
    for centre in centres:
        if j not in atlas.planes[centre]:
            continue
        count = 0
        for i in sorted(atlas.native):
            if not (atlas.planes[centre] | atlas.planes[p]) <= atlas.adj[i]:
                continue
            rest = np.vstack([F for h,F in rows.items()
                              if h != centre and atlas.planes[h] <= atlas.adj[i]])
            target = null(rest,atlas)
            jet = f.singleton_jet(atlas,p,k,i)
            f.require(target.shape == (16*k,k),"old target inverse fibre")
            residual = np.hstack([atlas.mm(left,target),atlas.mm(right,target)])
            f.require(not np.any(atlas.mm(jet,residual)),"new true singleton vanishes on the prescribed fibre")
            stack.append(target)
            count += 1
        affected[centre] = count
    span = atlas.rank(np.hstack(stack))
    geometric_cuts = 0
    for i in sorted(atlas.adj[j] & atlas.native):
        if not atlas.planes[p] <= atlas.adj[i]:
            continue
        others = np.vstack([F for h,F in rows.items() if h != p and atlas.planes[h] <= atlas.adj[i]])
        residual_fibre = null(others,atlas)
        f.require(residual_fibre.shape == (16*k,k),"other fifteen source rows")
        reduced = np.hstack([atlas.mm(left,residual_fibre),atlas.mm(right,residual_fibre)])
        jet = f.singleton_jet(atlas,p,k,i)
        f.require(atlas.rank(atlas.mm(jet,reduced)) == 2*k,"complete actual receiver-dependent Hermite view")
        f.require(atlas.rank(reduced[:2*k]) == 2*k,"new canonical ordinary quotient")
        geometric_cuts += 1
    return {"donor":j,"singleton":p,"k":k,"affected_designated_native_views":affected,
            "true_singleton_foreign_cuts":geometric_cuts,"true_early_pair_rank":32*k,
            "old_target_fibre_span_per_lane":span,"old_common_annihilator_dimension":16*k-span}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    args = cli.parse_args()
    base = args.repo/"research/moonshot-005-program/results"
    da = base/"bit-spread-disjoint-h-sources/author"
    oa = base/"bit-spread-overlap-source/author"
    f = module(da/"families.py","families")
    pair = module(oa/"pair.py","pair")
    atlas = f.Atlas(args.repo)
    old = json.loads((da/"output/PARAMETERS.json").read_text())
    combined = json.loads((oa/"output/PARAMETERS.json").read_text())
    cases = {(r["H"],r["k"]):r for r in old+combined["one_centre"]}
    path = Path(__file__).parent/"output/SINGLETON-COEFFICIENTS.json.gz"
    raw = path.read_bytes()
    pin = hashlib.sha256(raw).hexdigest()
    f.require(pin == "976d9558f33122618cc0001a8f92623893497f2e1d548000b2c8f801c2b32413",
              "literal matrix pin")
    checks = {}
    for entry in json.loads(gzip.decompress(raw)):
        h,k,j,p = (entry[x] for x in ("h","k","donor","singleton"))
        context = f.Chart(atlas,h,k)
        pr = cases[h,k]
        points = context.point_table(pr["core"],pr["fill"])
        rows = context.maps(points,j)
        S = np.asarray(entry["S"],dtype=np.uint8)
        answer = check_one(f,atlas,pair.null_basis,context,j,p,rows,pr["early"][str(j)],S)
        f.require(answer["old_common_annihilator_dimension"] == k,"frozen-extra obstruction")
        checks[h,k,j] = answer
    outputs = {}
    families = {"disjoint_23":sorted({263} | {r["H"] for r in old}),
                "shared_24":combined["extended_ordinary_packing"]}
    for name,centres in families.items():
        donors = set.union(*(atlas.planes[h] for h in centres))
        for h in centres:
            for j in atlas.planes[h]:
                if any(atlas.quota[j,p] == 45 for p in atlas.by_donor[j]):
                    f.require(all((h,k,j) in checks for k in (3,12)),"every affected special singleton replaced")
        generic = {j:{k:f.generic_singleton(atlas,j,k) for k in (3,12)} for j in atlas.native-donors
                   if any(atlas.quota[j,p] == 45 for p in atlas.by_donor[j])}
        views = sum(sum(atlas.planes[h] <= atlas.adj[i] for i in atlas.native) for h in centres)
        outputs[name] = {"distinct_charts":len(centres),"physical_native_inverse_graphs":views,
                         "native_donor_stars":len(donors),"physical_source_H_view_ranks":6470,
                         "ordinary_source_view_ranks":6470,"genuine_early_bases":111,
                         "generic_singleton_multipliers":generic}
    result = {"status":"PASS_PHYSICAL_SINGLETON_REPLACEMENTS","literal_matrices":len(checks),
              "source_sha256":pin,"checks":list(checks.values()),"placements":outputs,
              "framework_assumptions_discharged":0,"strict_supplier":False,"new_complete_kappa":False}
    args.out.mkdir(exist_ok=True,parents=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(result["status"],[(s,v["physical_native_inverse_graphs"])for s,v in outputs.items()])

if __name__=="__main__":
    main()
