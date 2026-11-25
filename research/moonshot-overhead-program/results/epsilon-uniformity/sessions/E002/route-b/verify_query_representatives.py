#!/usr/bin/env python3
"""Exact finite Gram-functional checks, not a tape lower bound."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def gamma(v, w):
    return (1 + sum(a != b for a, b in zip(v, w))) & 1


def main():
    counts = dict(distinct_label_probes=0, unchanged_probe_controls=0,
                  canonical_free_rectangles=0, query_slot_conflicts=0,
                  binary_noninjectivity_controls=0,
                  canonical_source_partitions=0,
                  partitioned_source_labels=0,
                  minimum_changed_source_streams=0)
    for q in (3, 4, 8):
        for length in (1, 2, 3):
            labels = list(itertools.product(range(q), repeat=length))
            for v, w in itertools.combinations(labels, 2):
                first = next(i for i in range(length) if v[i] != w[i])
                probe = [v[i] if v[i] == w[i] else
                         next(a for a in range(q) if a not in (v[i], w[i]))
                         for i in range(length)]
                assert gamma(v, probe) == gamma(w, probe)
                counts["unchanged_probe_controls"] += 1
                probe[first] = v[first]
                assert gamma(v, probe) != gamma(w, probe)
                counts["distinct_label_probes"] += 1
    for q in (4, 8, 16):
        for length in (2, 3, 4, 8, 16):
            left = [(a,)+(0,)*(length-1) for a in (0, 1)]
            right = [(a,)+(0,)*(length-1) for a in (2, 3)]
            assert all(gamma(v, w) == 0 for v in left for w in right)
            assert all(gamma(v, v) == 1 for v in left+right)
            x = left[0]
            assert [gamma(v, x) for v in left] == [1, 0]
            counts["canonical_free_rectangles"] += 1
            counts["query_slot_conflicts"] += 1
    for q, length in itertools.product((4, 8, 16), (2, 3)):
        for coordinate in range(length):
            seen = set()
            rectangles = 0
            for other in itertools.product(range(q), repeat=length-1):
                for block in range(0, q, 4):
                    for offset in (0, 2):
                        source = []
                        destination = []
                        for delta in (0, 1):
                            v = list(other)
                            v.insert(coordinate, block+offset+delta)
                            source.append(tuple(v))
                            w = list(other)
                            w.insert(coordinate, block+(2-offset)+delta)
                            destination.append(tuple(w))
                        assert all(gamma(v, w) == 0
                                   for v in source for w in destination)
                        assert gamma(source[0], source[0]) == 1
                        assert gamma(source[1], source[0]) == 0
                        assert all(v not in seen for v in source)
                        seen.update(source)
                        rectangles += 1
            assert len(seen) == q**length
            assert 2*rectangles == q**length
            counts["canonical_source_partitions"] += 1
            counts["partitioned_source_labels"] += len(seen)
            counts["minimum_changed_source_streams"] += rectangles
    for length in range(2, 9):
        v = (0,)*length
        w = (1, 1)+(0,)*(length-2)
        assert v != w
        assert all(gamma(v, z) == gamma(w, z)
                   for z in itertools.product(range(2), repeat=length))
        counts["binary_noninjectivity_controls"] += 1
    report = {
        "status": "PASS_SCOPED_GRAM_FUNCTIONAL_TESTS",
        "counts": counts,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(
            (ROOT/"query-representative-obstruction.md").read_bytes()).hexdigest(),
        "scope": (
            "Finite binary Fourier Gram identities and canonical free-rectangle "
            "query-coordinate conflicts. The written nondegeneracy argument "
            "proves the universal auxiliary-only-layout obstruction. These "
            "tests do not lower-bound tape operations, rule out shared maps, "
            "or execute the numerical Fourier algorithm."),
    }
    (ROOT/"query-representative-verification.json").write_text(
        json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
