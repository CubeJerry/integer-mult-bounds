#!/usr/bin/env python3
"""An explicit degree-15 GF64 evaluation source on all true H inputs."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from build import (COPIES, DEGREE, PRODUCT, PINNED, bit_rows, compile_binary,
                   field_rank, grouped_sources, owner_code, power, require,
                   swap_cycles, unpack)

# Scalar on the k derivative channels at the unique singleton of donor j.
# Entries are ordered by n=9 then n=36.
SINGLETON_SCALE = {
    49: (3, 2), 97: (1, 1), 53: (1, 2), 77: (7, 1), 93: (1, 7),
    8: (1, 2), 82: (3, 1), 58: (2, 1), 106: (1, 1), 31: (1, 1),
    105: (1, 2),
}


@lru_cache(None)
def coefficients(node, derivative, scale):
    if derivative:
        return tuple(PRODUCT[scale][power(node, d-1)] if d % 2 else 0 for d in range(16))
    return tuple(power(node, d) for d in range(16))


@lru_cache(None)
def row_cost(node, derivative, scale):
    return sum(mask.bit_count() for mask in bit_rows([coefficients(node, derivative, scale)]))


@lru_cache(None)
def compile_constraints(descriptions):
    matrix = [list(coefficients(*desc)) for desc in descriptions]
    require(len(matrix) == 16 and field_rank(matrix) == 16, "confluent source channel basis")
    code = compile_binary(bit_rows(matrix))
    digest = hashlib.sha256(bytes(v for pair in code for v in pair)).hexdigest()
    return len(code), digest


def jet_minor(nodes, k, coefficient):
    matrix = []
    for derivative in (False, True):
        for z in nodes:
            def monomial(t):
                if derivative:
                    return power(z, t-1) if t % 2 else 0
                return power(z, t)
            matrix.append([monomial(c) ^ (PRODUCT[coefficient][monomial(2*k+c)] if c < k else 0)
                           for c in range(2*k)])
    return matrix


def source_slot(kind, h, donor, degree, lane, n, phase, green, quota):
    """Return (base stripe, original channel, derivative, scale) for this real holder."""
    k = n // 3
    cardinality = phase["m"]
    if cardinality == 3 and phase["early"] == 2:
        require(kind == "X", "fully early phase")
        return lane % COPIES, degree % k + k*(lane >= COPIES), False, 1
    if cardinality == 2 and quota == 30:
        require(kind == "X" and degree < 2*k, "large donor full early coordinates")
        return lane, degree, False, 1
    if cardinality == 1:
        require(kind == "X" and h in green["singleton"], "true singleton early")
        if degree < 2*k:
            return lane, degree, False, 1
        scale = SINGLETON_SCALE[donor][n == 36]
        return lane, degree - 2*k, True, scale
    # Small donor or ordinary full H. Exactly one half is early.
    require(quota == 15, "ordinary half-early source slot")
    early_first = h in green["first"]
    first = early_first if kind == "X" else not early_first
    return lane, degree % k + (0 if first else k), False, 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / "research/moonshot-005-program/results"
    geo = json.loads(unpack(base, "geometry"))
    phase = json.loads(unpack(base, "phases"))
    spread = set(json.loads(unpack(base, "spread"))["selected_D"])
    routes = [json.loads(line) for line in unpack(base, "routes").splitlines()]
    H = list(map(frozenset, geo["A2"]))
    D = list(map(frozenset, geo["D4"]))
    orth = [{j for j, y in enumerate(geo["root_table"]) if sum(a*b for a,b in zip(x,y)) == 0}
            for x in geo["root_table"]]
    native = set(range(111))
    mats = {j: [h for h, plane in enumerate(H) if j in plane] for j in native}
    node = {(j,h): idx+1 for j, hs in mats.items() for idx,h in enumerate(hs)}
    colours = {}
    for j, hs in mats.items():
        singleton = [h for h in hs if phase[str(h)]["m"] == 1]
        half = [h for h in hs if phase[str(h)]["donor_early"][str(j)] == 15]
        full = [h for h in hs if phase[str(h)]["donor_early"][str(j)] == 30]
        require(len(hs) == 28 and len(singleton) == int(j in SINGLETON_SCALE),
                "at most one true singleton per donor")
        require((len(half),len(full)) == ((25,2) if singleton else (24,4)),
                "ordinary source phases")
        colours[j] = {"first":set(half[:12]),"singleton":set(singleton)}
    by_h = defaultdict(list)
    for kind, role, local, h, d, k, line, terminal in routes:
        if h is not None:
            by_h[h].append((kind,role,local,d,line))
    metrics = Counter()
    by_donor_cost = defaultdict(Counter)
    # Per-channel early constraints (h, derivative, scale, actual output owner).
    rows = defaultdict(list)
    late_owner_hash = hashlib.sha256()
    assigned = set()
    input_sizes = Counter()
    for h, plane in enumerate(H):
        p = phase[str(h)]
        donors = sorted(plane & native)
        if not donors:
            continue
        actual = defaultdict(list)
        for kind,role,local,d,line in by_h[h]:
            for lane in range(COPIES):
                actual[kind,line].append(owner_code(kind,role,local,lane))
        for group in actual.values():
            group.sort()
        quo = {int(j):v for j,v in p["donor_early"].items()}
        for kind, tag in (("X","early"),("Y","late")):
            lanes = p[tag]*COPIES
            if not lanes:
                continue
            at = Counter()
            for n in (9,36):
                groups = grouped_sources(kind,donors,len(donors),n//3,quo)
                for degree, j in enumerate(groups):
                    for lane in range(lanes):
                        holder = actual[kind,j][at[j]]
                        at[j] += 1
                        if j is None:
                            continue
                        stripe, c, der, scale = source_slot(kind,h,j,degree,lane,n,p,colours[j],quo[j])
                        require((holder,kind) not in assigned,"actual source holder reused")
                        assigned.add((holder,kind))
                        input_sizes[kind] += 1
                        if kind == "X":
                            rows[j,n,stripe,c].append((h,der,scale,holder))
                        else:
                            require(not der and scale == 1,"late taps use ordinary evaluations")
                            metrics["late_evaluation_ADD"] += row_cost(node[j,h],der,scale)
                            by_donor_cost[j]["late_evaluation_ADD"] += row_cost(node[j,h],der,scale)
                            late_owner_hash.update(f"{holder}/{j}/{h}/{n}/{stripe}/{c}\n".encode())
            require(all(at[j] == len(values) for (k,j),values in actual.items() if k == kind),
                    "all H groups including ground consumed")
    require(input_sizes == {"X":111*3840,"Y":40125*8},"genuine early owners and late line taps")
    register_hash = hashlib.sha256()
    cached_codes = {}
    for j in sorted(native):
        out_to_source = [-1]*3840
        raw = 0
        for n in (9,36):
            k = n//3
            for stripe in range(COPIES):
                for c in range(2*k):
                    ordered = sorted(rows[j,n,stripe,c])  # h, then value before derivative
                    require(len(ordered) == 16,"exact number of early conditions for each channel")
                    descriptions = tuple((node[j,h],der,scale) for h,der,scale,holder in ordered)
                    cost, digest = compile_constraints(descriptions)
                    metrics["early_basis_ADD"] += cost
                    by_donor_cost[j]["early_basis_ADD"] += cost
                    cached_codes[digest] = cost
                    for h, der, scale, holder in ordered:
                        dest = holder - j*3840
                        require(0 <= dest < 3840 and out_to_source[dest] == -1,"source-to-actual-X")
                        out_to_source[dest] = raw
                        raw += 1
        require(raw == 3840,"all source coefficients and outputs")
        swaps = swap_cycles(out_to_source)
        metrics["source_owner_permutation_ADD"] += 3*DEGREE*swaps
        by_donor_cost[j]["source_owner_permutation_ADD"] = 3*DEGREE*swaps
        by_donor_cost[j]["snapshot_copy_ADD_INIT_dirty_CLEAR"] = 3840*DEGREE
        register_hash.update(b"".join(x.to_bytes(2,"big") for x in out_to_source))
    # Foreign rank proof reduces to H local invertibility or one explicitly checked jets minor.
    allpairs = ordinary = singlepairs = 0
    jet_records = []
    bad_default = None
    for j in sorted(native):
        singleton = next(iter(colours[j]["singleton"]),None)
        if singleton is not None:
            ports = [d for d, roots in enumerate(D) if H[singleton] <= roots]
            parts = ([d for d in ports if d in spread],[d for d in ports if d not in spread])
        for i in sorted(orth[j] & native):
            hs = [h for h in mats[j] if H[h] <= orth[i]]
            ids = [node[j,h] for h in hs]
            require(len(hs) == len(set(ids)) == 16,"16 distinct actual evaluation nodes")
            allpairs += 1
            if singleton not in hs:
                ordinary += 1
                continue
            singlepairs += 1
            x0 = node[j,singleton]
            ratio = 0
            for x in ids:
                if x != x0:
                    ratio ^= power(x^x0,62)
            for ordinal,ds in enumerate(parts):
                n = len(ds)
                k = n//3
                xs = tuple(r+1 for r,d in enumerate(ds) if D[d] <= orth[i])
                require(len(xs) == k,"singleton receiver port count")
                delta = SINGLETON_SCALE[j][ordinal]
                matrix = jet_minor(xs,k,PRODUCT[ratio][delta])
                rank = field_rank(matrix)
                require(rank == 2*k, "singleton restricted kernel is injective")
                jet_records.append([i,j,singleton,n,ratio,delta,list(xs),rank])
                if bad_default is None and delta != 1:
                    defective = field_rank(jet_minor(xs,k,ratio))
                    if defective != 2*k:
                        bad_default = {"i":i,"j":j,"h":singleton,"ports":n,
                                       "required_rank":2*k,"unscaled_rank":defective}
    require((allpairs,ordinary,singlepairs,len(jet_records)) == (6470,6110,360,720),
            "complete foreign rank coverage")
    require(bad_default is not None,"unscaled singleton can actually be deficient")
    # A degenerate derivative value leaves an all-zero row in the early source basis.
    j = min(SINGLETON_SCALE)
    desc = sorted(rows[j,9,0,0])
    mutant = [list(coefficients(node[j,h],der,0 if der else scale)) for h,der,scale,_ in desc]
    require(field_rank(mutant) == 15,"a zero singleton derivative loses an actual early direction")
    snapshot = 111*3840*DEGREE
    metrics["snapshot_copy_ADD_INIT_dirty_CLEAR"] = snapshot
    pure = metrics["early_basis_ADD"] + metrics["source_owner_permutation_ADD"]
    forward = pure + metrics["late_evaluation_ADD"] + snapshot
    facts = {
        "status":"PASS_ACTUAL_GF64_SOURCE_TO_ALL_FOREIGN_H_BOUNDARIES",
        "programme_baseline":"914097a04bb93f730b805e9d4f036b46707c8675",
        "source_pins_decompressed":{v[0]:v[1] for v in PINNED.values()},
        "field":"GF(2)[z]/(z^6+z+1)", "bank":3840,"channels_per_donor":240,
        "polynomial_coefficients_per_channel":16,
        "true_early_owners":input_sizes["X"],"true_late_line_visits":input_sizes["Y"],
        "source_early_channel_bases":len(rows),"distinct_compiled_early_ADD_word_hashes":len(cached_codes),
        "foreign_pairs":allpairs,"ordinary_interpolation_pairs":ordinary,
        "singleton_kernel_pairs":singlepairs,"singleton_component_minors":len(jet_records),
        "chosen_singleton_scales":SINGLETON_SCALE,
        "all_foreign_H_observation_ranks":3840,
        "source_owner_permutations_sha256":register_hash.hexdigest(),
        "late_tap_assignments_sha256":late_owner_hash.hexdigest(),
        "controls":{"all_derivative_scales_one_fails":bad_default,
                    "zero_singleton_derivative_early_rank":15,"positive_early_rank":16},
        "finite_source_costs":{**dict(metrics),"forward_ADD":forward,
                               "pure_X_Hub_inverse_ADD":pure,
                               "forward_plus_reserved_pure_inverse_ADD":forward+pure,
                               "INIT":snapshot,"dirty_CLEAR":snapshot,
                               "extra_peak_one_donor":3840*DEGREE,
                               "extra_peak_all_donors":snapshot,"extra_MOVE":0},
        "common_endpoint_inverse_fibres":False,"complete_proper_target_or_new_kappa":False,
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(facts,indent=2,sort_keys=True)+"\n")
    (args.out/"PER-DONOR-COSTS.json").write_text(json.dumps(by_donor_cost,sort_keys=True,indent=2)+"\n")
    (args.out/"SINGLETON-MINORS.json").write_text(json.dumps(jet_records,separators=(",",":"))+"\n")
    (args.out/"SOURCE-WORD-HASHES.json").write_text(json.dumps(cached_codes,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:facts[k] for k in ["status","foreign_pairs","controls","finite_source_costs"]}))


if __name__ == "__main__":
    main()
