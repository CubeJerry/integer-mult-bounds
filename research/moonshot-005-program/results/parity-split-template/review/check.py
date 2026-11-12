#!/usr/bin/env python3
"""Independent GF(2) verification of every source facet hyperplane.

No author or predecessor checker is imported.  This verifies the finite
geometric premise of the scoped support argument, not a general coded-route
lower bound.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
PARENT = "1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153"


def require(value, message):
    if not value:
        raise ValueError(message)


def dot(a, b):
    return (a & b).bit_count() % 2


def basis(values):
    pivots = {}
    for value in values:
        x = value
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return [pivots[k] for k in sorted(pivots)]


def span(values):
    out = {0}
    for value in basis(values):
        out |= {x ^ value for x in tuple(out)}
    return out


def main(args):
    sb = args.source.read_bytes()
    pb = args.parent.read_bytes()
    require(hashlib.sha256(sb).hexdigest() == SOURCE, "source pin")
    require(hashlib.sha256(pb).hexdigest() == PARENT, "parent pin")
    source = json.loads(gzip.decompress(sb))
    parent = json.loads(gzip.decompress(pb))
    roles = sorted(source["live"])
    lines = {}
    for role in roles:
        frame = source["frames"][source["initial"][role]]
        require(len(frame) == 1, "actual initial line")
        lines[role] = frame[0]
    require(len(roles) == 104 and len(set(lines.values())) == 104, "distinct ports")
    require(all(dot(v, 511) for v in lines.values()), "odd source lines")
    counts = Counter()
    after = Counter()
    cases = []
    counterexample = None
    for role in roles:
        v = lines[role]
        facet = {x for x in range(512) if not dot(v, x)}
        require(facet == span(source["frames"][source["final"][role + 112]]), "actual final facet")
        donors = [j for j in roles if lines[j] in facet]
        require(len(donors) == 48 and role not in donors, "48 foreign donors")
        omitted = {j for j, _ in parent["corrections"].get(str(role + 112), [])}
        require(omitted <= set(donors), "inherited cancellation support")
        normals = [f for f in range(1, 512) if f != v and f < (f ^ v)]
        require(len(normals) == 255, "dual quotient enumerates all hyperplanes")
        seen = set()
        for f in normals:
            chart = frozenset(x for x in facet if not dot(f, x))
            require(len(chart) == 128 and chart not in seen, "distinct hyperplane")
            seen.add(chart)
            outside = [lines[j] for j in donors if dot(f, lines[j])]
            residual = [lines[j] for j in donors if j not in omitted and dot(f, lines[j])]
            full_span, residual_span = span(outside), span(residual)
            even = chart == frozenset(x for x in facet if not dot(511, x))
            expected = facet if even else {x for x in facet if not dot(f ^ 511, x)}
            require(full_span == expected and residual_span == expected, "exact parity-complement span")
            dimension = len(basis(outside))
            counts[dimension] += 1
            after[len(basis(residual))] += 1
            cases.append([role, f, len(outside), len(residual), dimension])
            if not even and counterexample is None:
                counterexample = {"receiver": role + 112, "normal": f,
                                  "outside_span_dimension": dimension,
                                  "outside_donor_count": len(outside),
                                  "even_form_removed_identity_fails": any(dot(f, x) for x in outside)}
    require(counts == Counter({7: 26416, 8: 104}) and after == counts, "complete census")
    require(lines[0] ^ lines[1] ^ lines[98] == 511, "dependent-triple parity relation")
    triple = []
    for i, j, k in [(0, 1, 98), (1, 0, 98), (98, 0, 1)]:
        neighbors = {x for x in roles if not dot(lines[i], lines[x])}
        left = {x for x in neighbors if not dot(lines[j], lines[x])}
        right = {x for x in neighbors if not dot(lines[k], lines[x])}
        require(not left & right and left | right == neighbors and len(left) == len(right) == 24,
                "actual24+24 complementary donor partition")
        triple.append({"receiver": i + 112, "left": sorted(left), "right": sorted(right)})
    result = {"status": "PASS_INDEPENDENT_ALL_HYPERPLANE_PARITY_GEOMETRY",
              "source_sha256": SOURCE, "parent_sha256": PARENT,
              "receivers": 104, "hyperplanes_per_receiver": 255,
              "outside_span_dimensions": dict(sorted(counts.items())),
              "after_seven_cancellations": dict(sorted(after.items())),
              "case_sha256": hashlib.sha256(json.dumps(cases, separators=(",", ":")).encode()).hexdigest(),
              "universal_rank8_counterexample": counterexample,
              "dependent_triple_partitions": triple,
              "scope": "Exact finite geometry plus the separately reviewed support-template proof; not arbitrary two-way coded X/Y feedback or a new kappa."}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"], len(cases), "cases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args())
