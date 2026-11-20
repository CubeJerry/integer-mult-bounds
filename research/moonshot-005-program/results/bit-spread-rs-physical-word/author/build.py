#!/usr/bin/env python3
"""Compile the two spread components on actual oriented H owners over GF(64)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

PINNED = {
    "geometry": ("bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",
                 "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"),
    "routes": ("bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz",
               "6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"),
    "phases": ("bit-asymmetric-balanced-atlas/author/output/PLANE-PHASES.json",
               "bae4a03a923abfc840e0d030093bdb635eb948de312697b5a08d0338bcc83cf6"),
    "spread": ("bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz",
               "7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab"),
}

DEGREE = 6
COPIES = 8


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mul(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 64:
            a ^= 0x43
    return value


PRODUCT = tuple(tuple(mul(a, b) for b in range(64)) for a in range(64))


@lru_cache(None)
def power(a, n):
    if not n:
        return 1
    return PRODUCT[a][power(a, n - 1)]


def field_rank(matrix):
    rows = [row[:] for row in matrix]
    pivot = 0
    if not rows:
        return 0
    for col in range(len(rows[0])):
        p = next((i for i in range(pivot, len(rows)) if rows[i][col]), None)
        if p is None:
            continue
        rows[p], rows[pivot] = rows[pivot], rows[p]
        inv = power(rows[pivot][col], 62)
        basis = [PRODUCT[inv][x] for x in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            c = rows[i][col]
            if c:
                rows[i] = [x ^ PRODUCT[c][y] for x, y in zip(rows[i], basis)]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def bit_rows(matrix):
    expanded = []
    for row in matrix:
        masks = [0] * DEGREE
        for j, coefficient in enumerate(row):
            for source_bit in range(DEGREE):
                v = PRODUCT[coefficient][1 << source_bit]
                for output_bit in range(DEGREE):
                    if v & (1 << output_bit):
                        masks[output_bit] |= 1 << (j * DEGREE + source_bit)
        expanded.extend(masks)
    return expanded


def compile_binary(original):
    rows = original[:]
    operations = []

    def add(dst, src):
        rows[dst] ^= rows[src]
        operations.append((dst, src))

    for col in range(len(rows)):
        pivot = next(i for i in range(col, len(rows)) if rows[i] & (1 << col))
        if pivot != col:
            add(col, pivot)
            add(pivot, col)
            add(col, pivot)
        for i in range(len(rows)):
            if i != col and rows[i] & (1 << col):
                add(i, col)
    identity = [1 << i for i in range(len(rows))]
    require(rows == identity, "binary elimination")
    code = operations[::-1]
    test = identity[:]
    for dst, src in code:
        test[dst] ^= test[src]
    require(test == original, "forward literal basis replay")
    for dst, src in operations:
        test[dst] ^= test[src]
    require(test == identity, "inverse literal basis replay")
    return code


def make_library(n):
    k = n // 3
    nodes = list(range(1, n + 1))
    matrix = [[power(node, t) for t in range(n)] for node in nodes]
    derivative = [[power(node, t - 1) if t % 2 else 0 for t in range(n)]
                  for node in nodes]
    partial = [[v if t < 2 * k else 0 for t, v in enumerate(row)]
               for row in derivative]
    require(field_rank(matrix) == n, "full Vandermonde rank")
    binary = bit_rows(matrix)
    code = compile_binary(binary)
    masks = {}
    for label, cross in [("two", partial), ("singleton", derivative)]:
        bits = bit_rows(cross)
        active = [j for j in range(n) if any(row[j] for row in cross)]
        total = 2 * n * DEGREE
        public = [1 << i for i in range(total)]
        saved = {DEGREE * j + t: public[DEGREE * j + t]
                 for j in active for t in range(DEGREE)}
        for dst, src in code:
            public[dst] ^= public[src]
            public[n * DEGREE + dst] ^= public[n * DEGREE + src]
        additions = 0
        for i, mask in enumerate(bits):
            for t, original_value in saved.items():
                if mask & (1 << t):
                    public[n * DEGREE + i] ^= original_value
                    additions += 1
        expect = binary + [(b << (n * DEGREE)) ^ d for b, d in zip(binary, bits)]
        require(public == expect, "full two-wave basis replay, arbitrary late baselines")
        require(additions == sum(x.bit_count() for x in bits), "all cross additions")
        masks[label] = {"cache_field_columns": active, "cross_ADD": additions,
                        "cross_coefficients": cross}
    return {"nodes": nodes, "n": n, "V": matrix, "V_binary_ADD": code, **masks}


def unpack(base, name):
    rel, pin = PINNED[name]
    content = (base / rel).read_bytes()
    if rel.endswith(".gz"):
        content = gzip.decompress(content)
    require(hashlib.sha256(content).hexdigest() == pin, "source pin " + name)
    return content


def swap_cycles(source_at_destination):
    size = len(source_at_destination)
    require(sorted(source_at_destination) == list(range(size)), "owner shuffle is a permutation")
    visited = [False] * size
    labels = list(range(size))
    swaps = 0
    for first in range(size):
        if visited[first]:
            continue
        previous = first
        visited[first] = True
        nxt = source_at_destination[previous]
        while nxt != first:
            require(not visited[nxt], "permutation cycle")
            visited[nxt] = True
            labels[previous], labels[nxt] = labels[nxt], labels[previous]
            swaps += 1
            previous = nxt
            nxt = source_at_destination[previous]
    require(labels == source_at_destination, "literal permutation replay")
    return swaps


def owner_code(kind, role, local, copy):
    return (((0 if kind == "X" else 1) * 111 + role) * 480 + local) * COPIES + copy


def grouped_sources(kind, donors, cardinality, k, early_quota):
    """For one component stripe, supply the source/ground group of each input column."""
    if cardinality == 3:
        return [donor for donor in donors for _ in range(k)]
    if cardinality == 2:
        big = max(donors, key=lambda j: early_quota[j])
        small = next(j for j in donors if j != big)
        if kind == "X":
            return [big] * (2 * k) + [small] * k
        return [small] * k + [None] * (2 * k)
    if cardinality == 1:
        return [donors[0] if kind == "X" else None] * (3 * k)
    raise ValueError("empty H uses identity")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / "research/moonshot-005-program/results"
    require(all(power(a, 63) == 1 for a in range(1, 64)),
            "all nonzero residues invertible in the declared degree-six polynomial field")
    geometry = json.loads(unpack(base, "geometry"))
    H = [frozenset(x) for x in geometry["A2"]]
    D = [frozenset(x) for x in geometry["D4"]]
    phases = json.loads(unpack(base, "phases"))
    spread = json.loads(unpack(base, "spread"))
    marked = set(spread["selected_D"])
    library = {n: make_library(n) for n in (9, 36)}
    # Group actual source or ground owners and actual output ports independently.
    routes = [json.loads(line) for line in unpack(base, "routes").splitlines()]
    by_h = defaultdict(list)
    seen = set()
    for kind, role, local, h, d, _k, line, _terminal in routes:
        owner = (kind, role, local)
        require(owner not in seen, "owner uniqueness")
        seen.add(owner)
        if h is None:
            continue
        if kind == "X":
            require(role == line, "genuine early origin")
        by_h[h].append((kind, role, local, d, line))
    require(len(seen) == 106560, "pinned native owners")
    roots = geometry["root_table"]
    orth = [{j for j, other in enumerate(roots) if sum(a*b for a, b in zip(root, other)) == 0}
            for root in roots]
    require(len(H) == 1120 and len(marked) == 630, "native sizes")
    sizes = Counter()
    actual_views = Counter()
    amounts = Counter()
    phase_amounts = Counter()
    num_sources = defaultdict(Counter)
    per_type = defaultdict(Counter)
    mapping_hash = hashlib.sha256()
    seen_small = set()
    first_views = {}
    h263 = {}
    maximum_cache = 0
    for h, plane in enumerate(H):
        p = phases[str(h)]
        donors = sorted(plane & set(range(111)))
        cardinality = len(donors)
        early_quota = {int(j): size for j, size in p["donor_early"].items()}
        phase_count = {kind: p[tag] * COPIES for kind, tag in (("X", "early"), ("Y", "late"))}
        type_name = ("empty" if not donors else "singleton" if cardinality == 1
                     else "two" if cardinality == 2 else
                     "full_early" if p["early"] == 2 else "full_mixed")
        sizes[type_name] += 1
        groups = defaultdict(list)
        outputs = defaultdict(list)
        for kind, role, local, d, line in by_h[h]:
            require(plane <= D[d] and (line is None or line in donors), "actual native H incidence")
            for copy in range(COPIES):
                wire = owner_code(kind, role, local, copy)
                groups[kind, line].append(wire)
                outputs[kind, d].append(wire)
        for wires in groups.values():
            wires.sort()
        for wires in outputs.values():
            wires.sort()
        ports = sorted({d for _, d in outputs})
        require(len(ports) == 45, "actual 45 H outputs")
        components = [[d for d in ports if d in marked], [d for d in ports if d not in marked]]
        require([len(x) for x in components] == [9, 36], "spread component widths")
        require(components[0] == spread["selected_ports_by_H"][str(h)], "port ordering pin")
        for i in range(120):
            if not plane <= orth[i]:
                continue
            actual_views["all"] += 1
            if i < 111:
                actual_views["native"] += 1
            for ds in components:
                rows = tuple(s for s, d in enumerate(ds) if D[d] <= orth[i])
                n = len(ds)
                require(len(rows) == n // 3, "balanced actual H view")
                # The algebraic proof covers every subset of distinct nonzero nodes.
                require(len({library[n]["nodes"][s] for s in rows} - {0}) == n // 3,
                        "nonzero distinct field nodes on actual view")
                if n == 9:
                    seen_small.add(rows)
                first_views.setdefault((n, type_name), rows)
            if i < 111 and cardinality:
                actual_views["active_native"] += 1
                actual_views["native_donor_projections"] += cardinality
        if not donors:
            require(not groups.get(("X", None)) and len(groups["Y", None]) == 720,
                    "empty chart has exactly its direct-ground late baselines")
            continue  # Identity, including every arbitrary Y.
        cache_at_h = 0
        for kind in ("X", "Y"):
            count = phase_count[kind]
            if not count:
                require(not any(key[0] == kind for key in groups), "absent phase")
                continue
            require(all(len(outputs[kind, d]) == count for d in ports), "true per-flag timing")
            pos = Counter()
            mapping = {}
            for component, ds in enumerate(components):
                n = len(ds)
                k = n // 3
                columns = grouped_sources(kind, donors, cardinality, k, early_quota)
                require(len(columns) == n, "complete polynomial basis at actual H")
                # Input column (source, exponent, lane) and output row (port, lane).
                for degree, group in enumerate(columns):
                    for lane in range(count):
                        slot = outputs[kind, ds[degree]][lane]
                        actual_input = groups[kind, group][pos[group]]
                        pos[group] += 1
                        mapping[slot] = actual_input
                        if group is not None:
                            num_sources[kind, group][component] += 1
                pure = count * len(library[n]["V_binary_ADD"])
                amounts["pure_field_ADD"] += pure
                per_type[type_name]["pure_field_ADD"] += pure
                if kind == "Y" and type_name in ("two", "singleton"):
                    item = library[n][type_name]
                    copies = count * DEGREE * len(item["cache_field_columns"])
                    cross = count * item["cross_ADD"]
                    amounts["cross_ADD"] += cross
                    per_type[type_name]["cross_ADD"] += cross
                    amounts["snapshot_copy_ADD_INIT_dirty_CLEAR"] += copies
                    per_type[type_name]["snapshot_copy_ADD_INIT_dirty_CLEAR"] += copies
                    cache_at_h += copies
                if h == 263:
                    h263[f"{kind}-{component}"] = {"ports":ds, "stripes":count, "donors":donors}
            require(all(pos[group] == len(wires)
                        for (phase, group), wires in groups.items() if phase == kind),
                    "all genuine source/ground inputs consumed once")
            wire_order = sorted(mapping)
            wire_index = {w: t for t, w in enumerate(wire_order)}
            permutation = [wire_index[mapping[w]] for w in wire_order]
            swaps = swap_cycles(permutation)
            permutation_add = 3 * DEGREE * swaps
            amounts["permutation_ADD"] += permutation_add
            per_type[type_name]["permutation_ADD"] += permutation_add
            phase_amounts[type_name, kind] += len(wire_order)
            mapping_hash.update(f"{h}/{kind}/".encode())
            for wire in wire_order:
                mapping_hash.update(wire.to_bytes(4, "big"))
                mapping_hash.update(mapping[wire].to_bytes(4, "big"))
        maximum_cache = max(maximum_cache, cache_at_h)
    require(sizes == {"full_early":65,"full_mixed":816,"two":227,"singleton":11,"empty":1},
            "all chart types")
    require(actual_views["all"] == 40320, "all parent receiver views")
    require(len(seen_small) == 84, "every three-subset is realized")
    for j in range(111):
        require(num_sources["X", j] == {0:768, 1:3072}, "every source's true early quotas")
    require(h263["X-0"]["donors"] == [0,61,62] and h263["X-1"]["stripes"] == 16,
            "existing fully early H263 map retained")
    controls = []
    for n in (9, 36):
        info = library[n]
        V = info["V"]
        derivative = info["singleton"]["cross_coefficients"]
        k = n // 3
        rows = first_views[n, "two"]
        jets = [V[p][:2*k] for p in rows] + [derivative[p][:2*k] for p in rows]
        require(field_rank(jets) == 2*k, "actual two-donor Hermite minor")
        require(field_rank(jets[:k] + [[0]*(2*k) for _ in rows]) == k,
                "omitting the delayed derivative loses rank")
        doubled = (rows[0],) + rows[:-1]
        mutated = [V[p][:2*k] for p in doubled] + [derivative[p][:2*k] for p in doubled]
        require(field_rank(mutated) == 2*k-2, "duplicating one node loses two dimensions")
        require(all(field_rank([V[p][j*k:(j+1)*k] for p in rows]) == k
                    for j in range(3)), "three actual full H projections")
        # Full formal late width is retained; early preview of small-donor late
        # columns would be a distinct (noncausal) operation.
        controls.append({"ports":n,"jet_rank":2*k,"omit_derivative_rank":k,
                         "duplicate_one_node_rank":2*k-2})
    pure = amounts["pure_field_ADD"] + amounts["permutation_ADD"]
    forward = pure + amounts["cross_ADD"] + amounts["snapshot_copy_ADD_INIT_dirty_CLEAR"]
    record = {"status": "PASS_ALL_NATIVE_SPREAD_H_PHASE_WORDS", "programme_baseline":
              "914097a04bb93f730b805e9d4f036b46707c8675", "field": "GF(2)[z]/(z^6+z+1)",
              "field_degree":DEGREE, "polynomial_mask":67, "bank_field_coordinates_per_donor":3840,
              "owner_copies":COPIES, "native_chart_types":dict(sizes),
              "actual_receiver_views":dict(actual_views), "phase_owners":
              {f"{t}/{p}":v for (t,p),v in phase_amounts.items()},
              "every_donor_early_component_widths":[768,3072],
              "H263":h263, "permutation_payload_sha256":mapping_hash.hexdigest(),
              "per_type_cost_sums":{t:dict(v) for t,v in per_type.items()},
              "finite_word_accounting":{
                  **dict(amounts),"pure_phase_ADD":pure,"forward_ADD":forward,
                  "additional_pure_X_at_Hub_and_pure_Y_at_Ground_inverse_ADD":pure,
                  "forward_plus_reserved_endpoint_inverses_ADD":forward+pure,
                  "INIT":amounts["snapshot_copy_ADD_INIT_dirty_CLEAR"],
                  "dirty_CLEAR":amounts["snapshot_copy_ADD_INIT_dirty_CLEAR"],
                  "extra_peak_at_one_H":maximum_cache,
                  "extra_peak_if_all_snapshots_live":amounts["snapshot_copy_ADD_INIT_dirty_CLEAR"],
                  "extra_MOVE":0},
              "controls":controls, "source_pins_decompressed":{v[0]:v[1] for v in PINNED.values()},
              "same_source_inverse_fibres_established":False,"complete_proper_endpoint":False,
              "strict_suppliers_or_new_kappa":False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
    word_spec = json.dumps(library,sort_keys=True,separators=(",",":")).encode() + b"\n"
    (args.out / "WORDS.json.gz").write_bytes(gzip.compress(word_spec,mtime=0))
    print(json.dumps({k:record[k] for k in ["status","actual_receiver_views",
                                             "finite_word_accounting","permutation_payload_sha256"]}))


if __name__ == "__main__":
    main()
