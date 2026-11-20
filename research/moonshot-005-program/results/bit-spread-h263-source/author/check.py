#!/usr/bin/env python3
"""Verify the source coefficients on the native H263 spread, including genuine phases."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


BASELINE = "914097a04bb93f730b805e9d4f036b46707c8675"
INPUTS = {
    "layout": ("bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",
               "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"),
    "routes": ("bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz",
               "6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"),
    "spread": ("bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz",
               "7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab"),
    "basis": ("bit-clifford-one-evaluation-gate/author/BASIS.json",
              "d2a825f09a4d24a8a0319743ec84bed9b9e6b50656d3105a1c4577ec78fba9ab"),
    "algebra": ("bit-coupled-source-reduced-determinants/author/algebra.py",
                "c482936813c11783f88fb74bd83d683989a709733f8aac6d6f99ddad50a288ba"),
}
COEFFICIENT_SHA = "d95b4bee7265940cd8540902992e25e36a8572d7670c698bf3e1cb9a5220c028"


def require(value, message):
    if not value:
        raise ValueError(message)


def pinned(base, name):
    path, digest = INPUTS[name]
    raw = (base / path).read_bytes()
    if path.endswith(".gz"):
        raw = gzip.decompress(raw)
    require(hashlib.sha256(raw).hexdigest() == digest, "source pin " + name)
    return raw


def load_inputs(repo):
    base = repo / "research/moonshot-005-program/results"
    pinned(base, "algebra")
    spec = importlib.util.spec_from_file_location("source_algebra", base / INPUTS["algebra"][0])
    algebra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(algebra)
    layout = json.loads(pinned(base, "layout"))
    masks, _, adjacency = algebra.geometry(layout, json.loads(pinned(base, "basis")))
    quota = Counter()
    for line in pinned(base, "routes").splitlines():
        kind, owner, _, plane, _, _, source, _ = json.loads(line)
        if kind == "X" and plane is not None:
            require(owner == source, "actual original owner")
            quota[owner, plane] += 1
    require(Counter(quota.values()) == {15: 2675, 30: 422, 45: 11}, "true quota census")
    return algebra, list(map(set, layout["A2"])), list(map(set, layout["D4"])), masks, adjacency, quota, json.loads(pinned(base, "spread"))


def multiply(A, B, product):
    return np.bitwise_xor.reduce(product[A[:, :, None], B[None, :, :]], axis=1)


def power_rows(nodes, n, product):
    V = np.ones((len(nodes), n), dtype=np.uint8)
    a = np.array(nodes, dtype=np.uint8)
    for h in range(1, n):
        V[:, h] = product[V[:, h - 1], a]
    return V


def ordinary_source(j, planes, quota):
    """Canonical two-lane schedule, also used on every additional group of eight stripes."""
    labels = sorted(h for h, H in enumerate(planes) if j in H)
    nodes = {h: i + 1 for i, h in enumerate(labels)}
    require(len(nodes) == 28, "one ordinary node per source plane")
    full = [h for h in labels if quota[j, h] >= 30]
    half = [h for h in labels if quota[j, h] == 15]
    extras = [h for h in labels if quota[j, h] == 45]
    slots = [(h, nodes[h]) for h in half] + [(h, 29 + t) for t, h in enumerate(extras)]
    width = 16 - len(full)
    require(len(slots) == 2 * width, "ordinary early half-slot balance")
    for lane in range(2):
        selected = [nodes[h] for h in full] + [s for _, s in slots[lane * width:(lane + 1) * width]]
        require(len(selected) == len(set(selected)) == 16 and max(selected) < 64, "ordinary early Vandermonde")
    return nodes


def check_component(k, parts, data, constants, products):
    algebra, planes, charts, masks, adj, quota, spread = data
    product, inverse = products
    rank = lambda A: algebra.rank(A, product, inverse)
    H = 263
    donors, projected, singular, native, all_receivers, ports = parts
    chosen = set(spread["selected_D"])
    local = sorted(d for d in ports if (d in chosen) == (k == 3))
    require(len(local) == 3 * k, "local component port dimensions")
    rad = {d: sorted(set(spread["D_radicals"][d]) - {0}) for d in local}
    multiplicities = Counter(x for d in local for x in rad[d])
    require(multiplicities == {x: k // 3 for x in singular}, "share rows per other plane")
    table = {int(x): np.array(A, dtype=np.uint8) for x, A in constants["off_H"].items()}
    require(set(table) == set(singular) and all(F.shape == (k, 16*k) and np.all(F < 64) for F in table.values()), "canonical quotient table")
    V = power_rows(range(1, 3 * k + 1), 3 * k, product)
    controls = [np.eye(16 * k, dtype=np.uint8)[j*k:(j+1)*k] for j in range(3)]
    expected = {x: [] for x in singular}
    for q, d in enumerate(local):
        difference = np.zeros((2, 16*k), dtype=np.uint8)
        difference[:, :k] = V[q, :k]
        difference[0, k:2*k] = V[q, k:2*k]
        difference[1, 2*k:3*k] = V[q, 2*k:3*k]
        transform = np.asarray(constants["core_transforms"][str(d)], dtype=np.uint8)
        require(transform.shape == (2, 2) and rank(transform) == 2, "two independent secrets at every port")
        shares = np.vstack([np.zeros((1, 16*k), dtype=np.uint8), multiply(transform, difference, product)])
        shares[:, 3*k + q] = 1
        for x, row in zip(rad[d], shares):
            expected[x].append(row)
    for x, bucket in expected.items():
        require(np.array_equal(table[x][:k//3], bucket), "literal ramp shares on the chosen points")
    exts = {tuple(x for x in singular if algebra.polar(x, t)) for t in singular}
    require(len(exts) == 27, "all exterior cut types")
    for ss in exts:
        require(len(ss) == 16, "exterior sees sixteen other planes")
        require(rank(np.vstack([table[x] for x in ss])) == 16 * k, "complete exterior quotient invertibility")

    equality_checks = 0
    control_checks = {}
    for i in all_receivers:
        visible = [q for q, d in enumerate(local) if charts[d] <= adj[i]]
        xs = [x for x in singular if not algebra.polar(x, masks[i])]
        M = np.vstack([table[x] for x in xs])
        require(len(visible) == k and len(xs) == 15 and rank(M) == 15*k, "15-plane annihilator rank")
        common = None
        for j in range(3):
            A = V[np.ix_(visible, range(j*k, (j+1)*k))]
            require(rank(A) == k, "invertible H donor minor")
            hread = multiply(A, controls[j], product)
            if common is None:
                common = hread
                require(rank(np.vstack([M, common])) == 16*k, "one common H readout completes all original coordinates")
            else:
                require(rank(np.vstack([M, common ^ hread])) == 15*k, "same inverse-fibre H readout")
                equality_checks += 1
        for q, d in enumerate(local):
            require(len(set(rad[d]) & set(xs)) == (3 if q in visible else 1), "actual full-or-single incidence")
        if i == 4:
            # Release one visible point: its H view has strictly fewer than 15 independent quotient blocks.
            require(rank(M[:-k]) == 14*k, "deleting a complete source quotient visibly lowers cut rank")
            bad = common.copy()
            bad[0] ^= controls[0][0]
            require(rank(np.vstack([M, common ^ bad])) == 15*k + 1, "single false equality violates the annihilator")
            control_checks = {"omit_one_quotient_rank": 14*k, "corrupt_one_readout_rank": 15*k+1}
    actual_foreign = 0
    early_ranks = {}
    for jn, j in enumerate(donors):
        maps = {h: table[x] for h, x in projected[j].items()}
        maps[H] = controls[jn]
        for r in sorted(adj[j] & set(range(111))):
            hs = [h for h in maps if planes[h] <= adj[r]]
            require(len(hs) == 16, "every native foreign source view")
            if H in hs:
                require(r in native, "classified native H view")
            else:
                signature = tuple(sorted(projected[j][h] for h in hs))
                require(signature in exts, "covered exterior cut type")
            actual_foreign += 1
        phase_rows = []
        for h, F in sorted(maps.items()):
            q = quota[j, h]
            if q == 30:
                phase_rows.append(np.kron(np.eye(2, dtype=np.uint8), F))
            else:
                require(q == 15, "no special singleton in these actual three stars")
                E = np.asarray(constants["early"][str(j)][str(h)], dtype=np.uint8)
                L = constants["complementary_late_coordinate_rows"][str(j)][str(h)]
                require(E.shape == (k,2*k) and len(L) == k, "phase split dimensions")
                require(rank(np.vstack([E, np.eye(2*k, dtype=np.uint8)[L]])) == 2*k, "invertible canonical-to-phase frame")
                phase_rows.append(np.hstack([multiply(E[:, :k], F, product), multiply(E[:, k:], F, product)]))
        M = np.vstack(phase_rows)
        require(M.shape == (32*k, 32*k) and rank(M) == 32*k, "genuine special early source basis")
        early_ranks[j] = 32*k
    return {"geometric_H_receivers":len(all_receivers), "native_H_receivers":len(native),
            "literal_donor_readout_equalities":equality_checks, "exterior_cut_types":len(exts),
            "special_native_foreign_pairs":actual_foreign, "special_early_pair_ranks":early_ranks,
            "core_rows_per_other_plane":k//3, "scope_controls":control_checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    data = load_inputs(args.repo)
    algebra, planes, charts, masks, adj, quota, spread = data
    raw = (Path(__file__).parent / "output/COEFFICIENTS.json.gz").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == COEFFICIENT_SHA, "explicit coefficient pins")
    package = json.loads(gzip.decompress(raw))
    H = 263
    donors = sorted(planes[H])
    require(donors == package["donors"] == [0,61,62] and package["field_polynomial"] == 67, "fully early native chart/field")
    a, b = (masks[j] for j in donors[:2])
    def proj(v):
        return v ^ (a if algebra.polar(v,b) else 0) ^ (b if algebra.polar(v,a) else 0)
    projected = {}
    for j in donors:
        relative = {}
        for h, P in enumerate(planes):
            if j in P and h != H:
                vals = {proj(masks[t]) for t in P - {j}}
                require(len(vals) == 1, "other plane projects to one singular point")
                relative[h] = vals.pop()
        projected[j] = relative
    singular = sorted(set(projected[donors[0]].values()))
    require(len(singular) == 27 and all(not algebra.quadratic(x) and x for x in singular), "27 source point labels")
    require(all(len(group) == 27 and set(group.values()) == set(singular) for group in projected.values()), "same 27 points for every H donor")
    all_receivers = [i for i in range(120) if planes[H] <= adj[i]]
    native = [i for i in all_receivers if i < 111]
    require(len(all_receivers) == 36 and len(native) == 33 and 80 not in native and 10 not in donors, "all identity-target views")
    ports = [d for d,D in enumerate(charts) if planes[H] <= D]
    parts = donors, projected, singular, native, all_receivers, ports
    products = algebra.field(67)
    components = {str(k):check_component(k, parts, data, package["components"][str(k)], products) for k in (3,12)}
    generic_foreign = 0
    for j in range(111):
        if j in donors:
            continue
        nodes = ordinary_source(j, planes, quota)
        for r in sorted(adj[j] & set(range(111))):
            seen = [t for h,t in nodes.items() if planes[h] <= adj[r]]
            require(len(seen) == len(set(seen)) == 16, "ordinary foreign Vandermonde view")
            generic_foreign += 1
    require(generic_foreign + components["3"]["special_native_foreign_pairs"] == 6470, "all native foreign pairs")
    bank = 3840
    binary = bank * 6
    late = 2675 * 120 * 6
    output = {"status":"PASS_ALL33_H263_GLOBAL_GF64_SOURCE","programme_baseline":BASELINE,
              "components":components,"generic_donors":108,"generic_native_foreign_pairs":generic_foreign,
              "total_native_foreign_pairs":6470,"actual_early_bases":111,"special_donors":donors,
              "H263_native_receivers":native,"field_modulus":67,"scalar_input_by_component":[48,192],
              "ordinary_quotient_after_16_spinor_lanes":[48,192],"bank_after_16_spinor_lanes":bank,
              "compressed_coefficient_sha256":COEFFICIENT_SHA,"input_pins_decompressed":INPUTS,
              "separate_source_binary_record_bill":{"late_INIT":late,"late_dirty_CLEAR":late,
              "extra_peak_upper_bound":late,"additional_MOVE":0,"genuine_singleton_extra_field_rows":11*120,
              "forward_and_reserved_original_inverse_ADD_upper_bound":222*(binary**2+3*binary)+binary*late+late},
              "other_H_inverse_graphs":False,"common_D_K_endpoint_word":False,"strict_supplier":False,
              "new_complete_kappa":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print(output["status"], "33 native H receivers;", 6470, "global source pairs and 111 early bases")

if __name__ == "__main__":
    main()
