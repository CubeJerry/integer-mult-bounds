#!/usr/bin/env python3
"""Replay one native D cut, an endpoint-gauge obstruction and the binary invoices."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

WORD_HASH = 'f185c1d220f258b88159f50bcafe47c1b0fde53439320eb5d9313d06e74bc970'


def coded(source, compiler, atlas, j):
    parts, parities = [], []
    for h in atlas.ks[j]:
        S, e = source.complete(j,h,3)
        parts.append(S[:e])
        parities.extend(S[e:])
    A = np.vstack(parts)
    require(A.shape == (96,96) and rank_fast(A)==96, "true early original-owner isomorphism")
    stream, cost = compiler.compile_invertible(A)
    return {"pure_ADD_8":8*cost, "late_prepare_ADD_8":int(8*compiler.WEIGHT[np.array(parities)].sum()),
            "basis_sha256":hashlib.sha256(stream).hexdigest(), "late_fields_8":len(parities)*8}


def shuffle_cost():
    # Finished G outputs sit in the pair's canonical spinor positions.
    # The ordinary RS compiler reads contiguous 96-field groups for each copy.
    dst_src = {e*96+48*h+s: 16*s+8*h+e for e in range(8) for h in range(2) for s in range(48)}
    require(sorted(dst_src) == sorted(dst_src.values()) == list(range(768)), "physical gauge relabelling")
    seen = set()
    swaps = []
    for d in range(768):
        if d in seen:
            continue
        q,cycle = d,[]
        while q not in seen:
            seen.add(q)
            cycle.append(q)
            q = dst_src[q]
        require(q==d, "genuine input shuffle cycle")
        swaps.extend(zip(cycle,cycle[1:]))
    check = list(range(768))
    for a,b in swaps:
        check[a],check[b] = check[b],check[a]
    require(check == [dst_src[k] for k in range(768)], "all native source basis addresses")
    return len(swaps)


def native_sections(a,d):
    ids = a.middle[d,"X"] + a.middle[d,"Y"]
    donors = sorted(a.D[d] & set(range(111)))
    receivers = sorted(a.D[a.dual[d]] & set(range(111)))
    cols = {j:[q for q,t in enumerate(ids) if a.route[t][3] in a.ks[j]] for j in donors}
    rows = {i:[q for q,t in enumerate(ids) if a.route[t][5] in a.ks[i]] for i in receivers}
    require(all(len(v)==8 for v in list(cols.values())+list(rows.values())), "proper formal boundary")
    return ids, cols, rows


def main(args):
    a = Atlas(args.repo,args.k_words,args.d_charts,args.library)
    raw = gzip.decompress(args.words.read_bytes())
    require(hashlib.sha256(raw).hexdigest()==WORD_HASH, "literal repair coefficients")
    word = json.loads(raw)
    d,i = word["d"],word["i"]
    prior = SpecialSource(a,args.repo,args.source)
    fixed = SpecialSource(a,args.repo,args.source,word["frames"])
    ids,cols,rows = native_sections(a,d)
    m = len(a.middle[d,"X"])
    n = len(ids)-m
    M = np.array(word["D"],dtype=np.uint8)
    V = np.array(word["V"],dtype=np.uint8)
    omega = np.array(word["omega"],dtype=np.uint8)
    require(i==5 and d==120 and (m,n)==(19,17) and rank_fast(V)==8 and rank_fast(omega)==8, "native repair scene")
    require(M.shape==(m+n,m+n) and not np.any(M[:m,m:]), "causal D word")
    require(rank_fast(M[:m,:m])==m and rank_fast(M[m:,m:])==n, "invertible genuine early and late maps")
    minors = [rank_fast(M[np.ix_(rs,cs)]) for cs in cols.values() for rs in rows.values()]
    require(len(minors)==132 and min(minors)==8, "all 132 native D coefficient minors")
    original = [fibre(a,prior,i,j,d) for j in prior.donors]
    previous = [rank_fast(np.vstack([original[x],original[y]])) for x,y in ((0,1),(0,2),(1,2))]
    previous_all = rank_fast(np.vstack(original))
    require(previous == [14,14,14] and previous_all == 20, "fixed-frame original native obstruction")
    gauges = {z["donor"]:np.array(z["matrix"],dtype=np.uint8) for z in word["gauges"]}
    require(set(gauges) == set(cols)-set(prior.donors), "nine ordinary native gauges")
    for G in gauges.values():
        require(G.shape==(96,96) and rank_fast(G)==96, "invertible ordinary input gauge")
    formal = []
    for j in sorted(cols):
        ds, left = marked_left(a,fixed,i,j)
        if j in gauges:
            left = a.ops.matmul(left,gauges[j])
        require(rank_fast(left)==96, "full marked left matrix in the new native source")
        image = a.ops.matmul(left,V.T)
        cuts = np.split(image,len(ds))
        require(all(not np.any(c) for t,c in zip(ds,cuts) if t!=d), "all 11 other marked D vanish on this fibre")
        selected = cuts[ds.index(d)]
        require(rank_fast(selected)==8, "eight native isolated fields")
        require(np.array_equal(a.ops.matmul(M[np.ix_(rows[i],cols[j])],selected),omega), "identical physical F64 cut action")
        if j in fixed.donors:
            rawX = np.zeros((len(ids),8),dtype=np.uint8)
            rawX[cols[j]] = selected
            formal.append(rawX)
    combined = np.hstack(formal)
    target = np.tile(np.eye(8,dtype=np.uint8),(1,3))
    def intersection(rows):
        return int(rank_fast(rows)+8-rank_fast(np.vstack([rows,target])))
    early_intersection = intersection(combined[:m])
    require(early_intersection==4 and intersection(combined)==8, "early target directions and completed target")
    # Labels are all ordinary foreign identity edges in B, including the subsequent repair.
    d0 = 3
    recs = sorted(a.D[a.dual[d0]] & set(range(111)))
    require(recs==[2,3,4,5,88,89,90,91,92,93,94,95], "native receiver set for D3")
    negative = {}
    for j in [26,29]:
        require(j not in gauges and j not in fixed.donors and all(i in a.orth[j] for i in recs), "unchanged identity-edge donor")
        fs = [fibre(a,fixed,i,j,d0) for i in recs]
        negative[j] = rank_fast(np.vstack(fs))
    require(negative == {26:94,29:96}, "endpoint-gauge invariant obstruction")
    module = importlib.util.spec_from_file_location("native_binary_compiler", args.source_compiler)
    compiler = importlib.util.module_from_spec(module)
    module.loader.exec_module(compiler)
    forward_delta = inverse_delta = 0
    costs = {}
    for j in fixed.donors:
        old,new = coded(prior,compiler,a,j),coded(fixed,compiler,a,j)
        require(old["late_fields_8"]==new["late_fields_8"],"unaltered genuine Y count")
        costs[j] = {"old":old,"new":new}
        inverse_delta += new["pure_ADD_8"]-old["pure_ADD_8"]
        forward_delta += new["pure_ADD_8"]-old["pure_ADD_8"]+new["late_prepare_ADD_8"]-old["late_prepare_ADD_8"]
    gauge_costs = {}
    swaps = shuffle_cost()
    for j,G in gauges.items():
        _,pure = compiler.compile_invertible(G)
        gauge_costs[j] = 8*pure+18*swaps
    direct_A = compiler.compile_invertible(M[:m,:m])[1]
    direct_D = compiler.compile_invertible(M[m:,m:])[1]
    direct_cross = int(compiler.WEIGHT[M[m:,:m]].sum())
    actual_D = {"pure_ADD_8_one_direction":8*(direct_A+direct_D),"snapshot_prepare_ADD_8":8*direct_cross,
                "inject_ADD_8":8*n*6,"INIT":8*n*6,"dirty_CLEAR":8*n*6}
    actual_D["forward_ADD"] = actual_D["pure_ADD_8_one_direction"]+actual_D["snapshot_prepare_ADD_8"]+actual_D["inject_ADD_8"]
    actual_D["forward_and_both_pure_inverses_ADD"] = actual_D["forward_ADD"]+actual_D["pure_ADD_8_one_direction"]
    info = {"status":"one complete proper middle cut for all twelve native donors; fixed-word gauge obstruction elsewhere",
            "proper_body_width":480,"native_bank":3840,"source_coefficients_raw_sha256":hashlib.sha256(gzip.decompress(args.source.read_bytes())).hexdigest(),
            "literal_repair_raw_sha256":WORD_HASH,"D":d,"receiver":i,"true_D_phase_widths":[m,n],"native_donors":sorted(cols),
            "native_D_receivers":sorted(rows),"selected_D_receiver_owner_ids":[ids[q] for q in rows[i]],"sectional_8_by_8_minors_verified":len(minors),
            "saturated_middle_fibre_dimension_per_body":8,"saturated_middle_fibre_dimension_native":64,
            "three_special_before_pairwise_sums":previous,"three_special_before_all_sum":previous_all,
            "three_special_after_sum":8,"all_twelve_after_action":"same invertible omega on the same V, zero on all other visible D",
            "proper_early_directions_actual":early_intersection,"proper_total_directions_actual":intersection(combined),
            "D3_native_receivers":recs,"D3_summed_fibre_dimensions":negative,"D3_native_summed_dimensions":{j:8*r for j,r in negative.items()},
            "D3_GF2_native_summed_dimensions":{j:48*r for j,r in negative.items()},"small_special_source_changes":costs,
            "special_source_forward_ADD_change":forward_delta,"special_source_pure_inverse_ADD_change":inverse_delta,
            "ordinary_native_gauge_ADDs_each_direction":gauge_costs,"ordinary_native_shuffle_swaps_per_gauge":swaps,
            "all_source_forward_ADD":279093344+forward_delta+sum(gauge_costs.values()),
            "all_source_pure_inverse_ADD":178695272+inverse_delta+sum(gauge_costs.values()),
            "all_source_INIT_and_dirty_CLEAR_each":2540160,"D120":actual_D,"new_MOVE":0,
            "claims":["H263 ordinary inverse graphs persist for all 33 native receivers","All 6470 proper foreign rank tests persist by invertible local quotients, D minors, and unchanged right factors.","Exact shared twelve-donor D120 cut for i=5.","The fixed full word fails the target at D3 even after independent input and output linear gauges."],
            "open":["receiver sum across 60 middle nodes","other marked and unmarked sheets","full native target and low-rank return","recursive suppliers and foundations"]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(info,indent=2,sort_keys=True)+"\n")
    print("D120 all 12 donor actions agree;",len(minors),"native minors; gauge-invariant D3 dimensions",negative)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for name in ("repo","h-author","k-words","d-charts","source","source-compiler","out"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--words",type=Path,default=Path(__file__).parent/"output/WORDS.json.gz")
    p.add_argument("--library",type=Path)
    args = p.parse_args()
    sys.path.insert(0,str(args.h_author))
    from build import require
    from transfer import Atlas, rank_fast
    from body import SpecialSource, fibre, marked_left
    main(args)
