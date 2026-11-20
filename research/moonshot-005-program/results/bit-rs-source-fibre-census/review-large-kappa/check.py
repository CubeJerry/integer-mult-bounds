#!/usr/bin/env python3
"""Independent exact check of source fibres, route cuts and packing counts.

This checker imports no author or predecessor Python.  It reads authenticated
geometry, actual physical routes, the compact witness table, source receipts,
and packed-source parameters.  Polynomial fibres are obtained by synthetic
division of the full sixteen-node annihilator; ranks use descending pivots.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path


PINS = {
    "geometry": ("bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",
        "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"),
    "witnesses": ("bit-rs-source-fibre-census/author/WITNESSES.json.gz",
        "aff3bbf6ede384eab9b4a97f1aeaff4ddc8d16b3c61b9e1cb346fb5a949240e5"),
    "routes": ("bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz",
        "6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"),
    "phases": ("bit-asymmetric-balanced-atlas/author/output/PLANE-PHASES.json",
        "bae4a03a923abfc840e0d030093bdb635eb948de312697b5a08d0338bcc83cf6"),
    "target": ("bit-two-sided-covariant-target/author/output/ASSIGNMENT.json",
        "deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601"),
    "rs_proof": ("bit-spread-rs-physical-word/author/RS-SOURCE.md",
        "432e19d4d11e6068eac7bea94dba459464e804b539634be54824c30f25f7fcae"),
    "rs_source": ("bit-spread-rs-physical-word/author/rs_source.py",
        "a51189b6d5422ec07fb2fedc822dc856e3277ea8ae0631894c34464419b8c7f9"),
    "rs_receipt": ("bit-spread-rs-physical-word/author/source-output/RESULT.json",
        "aa0fdb58c57cb0aa0e876bd66a2852b8c269abdffb2505adf045937e6c24f174"),
    "packing_31": ("bit-spread-packed-source-owner-compiler/author/output-31/RESULT.json",
        "d5041dccac76a1692e77ef01dccec9de91e5cea2ac098e243d705b2f91cb06ff"),
    "packing_30": ("bit-spread-packed-source-owner-compiler/author/output-30/RESULT.json",
        "e52c1b1e4a7a063b8889ff5d051af47b5d4f73a12116e826fc3732e5d5cec251"),
    "packing_24": ("bit-spread-packed-source-owner-compiler/author/output-24/RESULT.json",
        "f554558b6fb597b5132b005c73dec5cf36a60819b18f17cb77aa0df77238234c"),
    "packing_23": ("bit-spread-packed-source-owner-compiler/author/output/RESULT.json",
        "284cb7c69878be80747d0c07d93b3ce9dcb3e2312165ad4811bdf30318630191"),
    "packing_pairs": ("bit-spread-two-centre-packing/author/output/PARAMETERS.json",
        "972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c"),
    "packing_singles": ("bit-spread-overlap-source/author/output/PARAMETERS.json",
        "9fb6002b7838d0b8102a566836e5115f923d3c1678478968f41e42741ae5ca03"),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def field_multiply(a, b):
    # Ordinary polynomial convolution followed by long division over F2.
    product = 0
    for degree in range(6):
        if (a >> degree) & 1:
            product ^= b << degree
    for degree in range(10, 5, -1):
        if (product >> degree) & 1:
            product ^= 0b1000011 << (degree - 6)
    return product


MUL = tuple(tuple(field_multiply(a, b) for b in range(64)) for a in range(64))
INV = (0,) + tuple(next(b for b in range(1, 64) if MUL[a][b] == 1)
                 for a in range(1, 64))


def row_rank(rows):
    basis = {}
    for source in rows:
        row = list(source)
        for col in sorted(basis, reverse=True):
            scale = row[col]
            if scale:
                p = basis[col]
                row = [x ^ MUL[scale][y] for x, y in zip(row, p)]
        nonzero = [c for c, x in enumerate(row) if x]
        if nonzero:
            col = nonzero[-1]
            scale = INV[row[col]]
            basis[col] = tuple(MUL[scale][x] for x in row)
    return len(basis)


def annihilator(nodes):
    coefficients = [1]
    for node in nodes:
        new = [0] * (len(coefficients) + 1)
        for power, value in enumerate(coefficients):
            new[power] ^= MUL[node][value]
            new[power + 1] ^= value
        coefficients = new
    return tuple(coefficients)


def divide_linear(polynomial, node):
    quotient = [0] * (len(polynomial) - 1)
    quotient[-1] = polynomial[-1]
    for degree in range(len(quotient) - 1, 0, -1):
        quotient[degree - 1] = polynomial[degree] ^ MUL[node][quotient[degree]]
    need(polynomial[0] == MUL[node][quotient[0]], "synthetic division remainder")
    return tuple(quotient)


def evaluate(polynomial, node):
    result = 0
    for coefficient in reversed(polynomial):
        result = MUL[result][node] ^ coefficient
    return result


def maximum_orthogonal(vertices, orthogonal):
    """Exhaustive include/exclude search, not a floating optimization claim."""
    best = []
    calls = 0

    def visit(selected, candidates):
        nonlocal best, calls
        calls += 1
        if len(selected) + len(candidates) <= len(best):
            return
        if not candidates:
            best = selected
            return
        v = min(candidates, key=lambda j: (len(orthogonal[j] & candidates), j))
        rest = candidates - {v}
        visit(selected + [v], rest & orthogonal[v])
        visit(selected, rest)

    visit([], set(vertices))
    need(all(k in orthogonal[j] for j, k in combinations(best, 2)), "clique witness")
    return sorted(best), calls


def finite_sumset_control():
    equalities = 0
    sets = list(map(frozenset, combinations(range(8), 4)))
    for left in sets:
        for right in sets:
            sums = {a ^ b for a in left for b in right}
            if len(sums) != 4:
                continue
            stabilizer_left = {t for t in range(8) if {x ^ t for x in left} == left}
            stabilizer_right = {t for t in range(8) if {x ^ t for x in right} == right}
            need(len(stabilizer_left) == 4 and stabilizer_left == stabilizer_right,
                 "finite sumset equality control")
            equalities += 1
    return {"pairs_tested": len(sets)**2, "tight_pairs": equalities,
            "scope": "finite corroboration; the general lemma is reviewed in prose"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / "research/moonshot-005-program/results"
    payloads = {}
    for key, (path, expected) in PINS.items():
        data = (base / path).read_bytes()
        data = gzip.decompress(data) if path.endswith(".gz") else data
        need(hashlib.sha256(data).hexdigest() == expected, "source hash: " + key)
        payloads[key] = data

    geometry = json.loads(payloads["geometry"])
    roots = geometry["root_table"]
    planes = list(map(frozenset, geometry["A2"]))
    middles = list(map(frozenset, geometry["D4"]))
    dual = geometry["dual_D4"]
    orthogonal = [{k for k, y in enumerate(roots) if sum(a*b for a, b in zip(x, y)) == 0}
                  for x in roots]
    need(len(roots) == 120 and all(len(x) == 8 for x in roots), "real root dimension")
    need(all(sum(v*v for v in x) == 4 for x in roots), "nonzero real roots")
    need(roots[:8] == [[2 * (i == j) for j in range(8)] for i in range(8)],
         "eight coordinate roots")
    native = set(range(111))
    stars = {j: [h for h, plane in enumerate(planes) if j in plane] for j in native}
    need(all(len(hs) == 28 for hs in stars.values()), "28 actual source planes")
    nodes = {j: {h: n+1 for n, h in enumerate(hs)} for j, hs in stars.items()}
    audiences = [native.intersection(*(orthogonal[j] for j in H)) for H in planes]
    singleton = {next(iter(H & native)) for H in planes if len(H & native) == 1}
    ordinary = native - singleton - {10}
    need(len(singleton) == 11 and len(ordinary) == 99, "ordinary source universe")
    need(set(range(8)) <= ordinary, "coordinate roots survive exclusions")
    views = {(j, i): [h for h in stars[j] if i in audiences[h]]
             for j in native for i in orthogonal[j] & native}
    need(len(views) == 6470 and all(len(v) == 16 for v in views.values()),
         "all native source views have sixteen quotients")

    # Inspect actual chronological lanes, not merely ideal unlabelled ports.
    phases = json.loads(payloads["phases"])
    routes = [json.loads(line) for line in payloads["routes"].splitlines()]
    port = defaultdict(Counter)
    incoming = Counter()
    for kind, role, local, h, d, k, line, terminal in routes:
        need(kind in {"X", "Y"} and role in native and 0 <= local < 480,
             "real owner route")
        if h is not None:
            need(planes[h] <= middles[d], "nested H to D route")
            port[h, d][kind] += 1
            if line is not None:
                need(line in planes[h] & native, "genuine native source line")
                incoming[line, h, kind] += 1
        if k is not None:
            need(planes[k] <= middles[dual[d]], "nested D to K route")
            if terminal is not None:
                need(terminal in planes[k] & native, "genuine native terminal")
    need(len(routes) == 106560 and len(port) == 1120*45, "actual route coverage")
    for d, D in enumerate(middles):
        need(set.intersection(*(orthogonal[j] for j in D)) == set(middles[dual[d]]),
             "exact middle complement")
    port_lists = [[d for d, D in enumerate(middles) if H <= D] for H in planes]
    cut_checks = 0
    for h, ds in enumerate(port_lists):
        need(len(ds) == 45, "45 physical H ports")
        p = phases[str(h)]
        for d in ds:
            need(port[h, d]["X"] == p["early"] and port[h, d]["Y"] == p["late"]
                 and sum(port[h, d].values()) == 2, "two actual chronological lanes")
        for i in audiences[h]:
            visible = [d for d in ds if middles[d] <= orthogonal[i]]
            need(len(visible) == 15, "receiver sees fifteen physical H ports")
            need(sum(sum(port[h, d].values()) for d in visible) * 8 == 240,
                 "exact combined early and late cut capacity")
            cut_checks += 1
    for j in ordinary:
        need(sum(incoming[j, h, "X"] for h in stars[j]) == 480,
             "one full early source bank")
        for h in stars[j]:
            need(incoming[j, h, "X"] + incoming[j, h, "Y"] == 30,
                 "ordinary plane quotient has 30 base owners, 240 at eight copies")
        phase_counts = Counter(incoming[j, h, "X"] for h in stars[j])
        need(phase_counts == {15: 24, 30: 4}, "ordinary mixed-phase source partition")

    # Authenticate the actual target's exceptional row and column.
    target = json.loads(payloads["target"])
    modified = [tuple(r[:2]) for r in target["row_transfers"]]
    modified += [tuple(r[:2]) for r in target["column_transfers"]]
    modified += [tuple(r) for r in target["internal_edges"]]
    need(len(set(modified)) == 123, "target has 123 modified directed blocks")
    need(all(i == 80 or j == 10 for i, j in modified), "exact identity-block domain")
    need(all(i in orthogonal[j] for i, j in modified), "all target modifications are foreign")

    @lru_cache(None)
    def full_polynomial(j, i):
        return annihilator([nodes[j][h] for h in views[j, i]])

    @lru_cache(None)
    def fibre(j, h, i):
        need(h in views[j, i], "fibre uses an actually visible plane")
        value = divide_linear(full_polynomial(j, i), nodes[j][h])
        need(len(value) == 16 and value[-1] == 1, "monic degree-fifteen inverse fibre")
        for other in views[j, i]:
            need(bool(evaluate(value, nodes[j][other])) == (other == h),
                 "fibre zero set is exactly the fifteen other visible nodes")
        return value

    nonorthogonal_pairs = {tuple(pair) for pair in combinations(sorted(ordinary), 2)
                          if pair[1] not in orthogonal[pair[0]]}
    plane_pairs = {}
    for h, H in enumerate(planes):
        for pair in combinations(sorted(H & ordinary), 2):
            need(pair not in plane_pairs, "unique shared plane of nonorthogonal pair")
            plane_pairs[pair] = h
    need(set(plane_pairs) == nonorthogonal_pairs and len(plane_pairs) == 2281,
         "complete nonorthogonal pair census")
    witnesses = json.loads(payloads["witnesses"])
    need(witnesses["singleton_donors"] == sorted(singleton)
         and witnesses["donor_excluded"] == 10 and witnesses["receiver_excluded"] == 80,
         "certificate's actual excluded domains")
    seen = set()
    ranks_histogram = Counter()
    rank16_control = None
    for record in witnesses["witnesses"]:
        pair = tuple(record["donors"])
        h = record["H"]
        receivers = record["receivers"]
        need(pair in nonorthogonal_pairs and pair not in seen, "exact donor-pair coverage")
        need(plane_pairs[pair] == h, "certificate has the real shared plane")
        need(len(receivers) == len(set(receivers)) == 16 and 80 not in receivers
             and set(receivers) <= audiences[h], "sixteen genuine permitted receivers")
        matrices = [[fibre(j, h, i) for i in receivers] for j in pair]
        ranks = [row_rank(matrix) for matrix in matrices]
        need(ranks == record["ranks"] and sorted(ranks) == [15, 16],
             "independent fibre rank discrepancy")
        seen.add(pair)
        ranks_histogram[tuple(ranks)] += 1
        if rank16_control is None:
            matrix = matrices[ranks.index(16)]
            rank16_control = row_rank([matrix[0]] + matrix[:-1])
            need(rank16_control == 15, "duplicate receiver destroys rank-sixteen witness")
    need(seen == nonorthogonal_pairs, "every nonorthogonal ordinary pair obstructed")

    pair_parameters = json.loads(payloads["packing_pairs"])
    single_parameters = json.loads(payloads["packing_singles"])
    packing_cases = [
        ("23", "output", single_parameters["native_all_views_packing"]),
        ("24", "output-24", single_parameters["extended_ordinary_packing"]),
        ("30", "output-30", pair_parameters["singleton_free_30"]["charts"]),
        ("31", "output-31", pair_parameters["complete_31"]["charts"]),
    ]
    packing_rows = []
    supplementary_hashes = {}
    for label, directory, charts in packing_cases:
        receipt_path = "bit-spread-packed-source-owner-compiler/author/" + directory + "/RESULT.json"
        receipt_bytes = (base / receipt_path).read_bytes()
        supplementary_hashes[receipt_path] = hashlib.sha256(receipt_bytes).hexdigest()
        receipt = json.loads(receipt_bytes)
        special = set().union(*(planes[h] & native for h in charts))
        need(special == set(map(int, receipt["special_donor_costs"])),
             "packing donors reconstructed from actual chart table")
        need(len(charts) == int(label) == receipt["native_chart_count"], "packing chart count")
        need(len(special) == receipt["special_donor_count"], "packing source count")
        retained = ordinary - special
        clique, calls = maximum_orthogonal(retained, orthogonal)
        packing_rows.append({"charts": int(label), "special_donors": len(special),
            "special_singletons": sorted(special & singleton), "donor_10_special": 10 in special,
            "special_in_J": len(special & ordinary), "retained_in_J": len(retained),
            "further_changes_from_global_8_bound": max(0, len(retained)-8),
            "maximum_orthogonal_retained": len(clique), "maximum_witness": clique,
            "further_changes_from_exact_retained_graph": len(retained)-len(clique),
            "clique_search_nodes": calls})
    need(packing_rows[-1]["special_in_J"] == 70
         and packing_rows[-1]["retained_in_J"] == 29, "31-centre source count")

    result = {
        "status": "PASS_INDEPENDENT_RS_SOURCE_FIBRE_CENSUS",
        "author_python_imported": False, "floating_point_used": False,
        "source_pins_decompressed": {p: h for p, h in PINS.values()},
        "packing_receipt_hashes": supplementary_hashes,
        "ordinary_donors_J": sorted(ordinary), "singleton_donors": sorted(singleton),
        "nonorthogonal_pairs": len(seen), "rank_pair_counts": {str(k): v for k, v in sorted(ranks_histogram.items())},
        "actual_physical_routes": len(routes), "actual_H_D_ports": len(port),
        "native_receiver_H_capacity_checks": cut_checks, "field_symbols_per_cut": 240,
        "bank_field_symbols": 3840, "minimum_source_changes": 91,
        "packing_counts": packing_rows,
        "controls": {"duplicate_receiver_rank": rank16_control,
                     "sumset_equality": finite_sumset_control()},
        "proof_scope": "Exact original-coordinate S028 target; separate donor bijections; fixed source quotient partitions and actual route capacities; no informative preload or additional path.",
        "new_complete_kappa": False,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(json.dumps({"pairs": len(seen), "cut_checks": cut_checks,
                      "packing_counts": packing_rows}, sort_keys=True))


if __name__ == "__main__":
    main()
