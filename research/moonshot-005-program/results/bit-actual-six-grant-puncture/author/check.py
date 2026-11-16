#!/usr/bin/env python3
"""Exact archived-star admission for the current six raw point grants."""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return len(pivots)


def verify(roots, frame, edges, erased):
    dot = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    assert len(frame) == len(set(frame)) == 8 and not set(frame).intersection(erased)
    assert all(dot(i, j) != 0 for i in frame for j in frame)
    assert len({tuple(e["pair"]) for e in edges}) == len(edges)
    assert len({e["role"] for e in edges}) == len(edges)
    assert not set(frame).intersection(e["role"] for e in edges)
    degrees = [0] * 8
    incidents = [[] for _ in range(8)]
    for edge in edges:
        a, b = edge["pair"]
        j = edge["role"]
        assert 0 <= a < b < 8 and j not in erased
        assert [k for k, i in enumerate(frame) if dot(i, j) == 0] == [a, b]
        for k in [a, b]:
            degrees[k] += 1
            incidents[k].append(j)
    for group in incidents:
        assert all(dot(i, j) != 0 for i in group for j in group)
    assert min(degrees) >= 4
    return degrees


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    data = json.loads(source_bytes)
    for key in ["native_source", "archived_star", "rank_floor"]:
        raw = (args.repo / data[key + "_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == data[key + "_sha256"]
    roots = json.loads((args.repo / data["native_source_path"]).read_text())["native_roots"]
    archive = json.loads((args.repo / data["archived_star_path"]).read_text())["two_points"]["star"]
    erased = data["erased_raw_points"]
    assert data["frame"] == archive["frame"]
    assert data["retained_edges"] == [e for e in archive["edges"] if e["role"] not in erased]
    frame, edges = data["frame"], data["retained_edges"]
    degrees = verify(roots, frame, edges, erased)
    assert len(edges) == 27 and degrees == [6, 7, 7, 7, 6, 7, 7, 7]
    retained = [i for i in range(111) if i not in erased]
    mask = sum(1 << i for i in retained)
    canonical = []
    for i in retained:
        canonical.append(((1 << i) | sum(1 << j for j in range(111) if sum(x * y for x, y in zip(roots[i], roots[j])) == 0)) & mask)
    assert len(retained) == 105 and rank(canonical) == 9
    corrupt = copy.deepcopy(edges)
    corrupt[0]["role"] = frame[0]
    low_degree = [e for e in edges if 0 not in e["pair"]]
    bad_frame = [erased[0]] + frame[1:]
    tests = [("corrupted_native_edge", frame, corrupt),
             ("granted_role_in_retained_frame", bad_frame, edges),
             ("missing_degree_hypothesis", frame, low_degree)]
    rejected = []
    for name, f, e in tests:
        try:
            verify(roots, f, e, erased)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("accepted mutant " + name)
    result = {"status": "PASS_ACTUAL_SIX_GRANT_RANK_NINE_PUNCTURE",
              "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
              "native_source_sha256": data["native_source_sha256"],
              "archived_star_sha256": data["archived_star_sha256"],
              "rank_floor_sha256": data["rank_floor_sha256"],
              "erased_points": erased, "retained_roles": 105,
              "frame": frame, "edges": edges, "degrees": degrees,
              "canonical_restricted_rank": 9,
              "negative_controls_rejected": rejected,
              "scope": "All-field all-width linear fitting floor via the admitted star inequality; excludes arbitrary eight linear ground rows plus these six point grants with raw geometric locals, not new nonlocal histories, subsequent free point feedback or nonlinear encoders",
              "credit": data["inherited_credit"]}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "retained_roles", "degrees", "canonical_restricted_rank", "negative_controls_rejected"]}))


if __name__ == "__main__":
    main()
