#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the finite complementary-frame companion of the pinned PR2305 word.

The predecessor constructors are retained verbatim in the source archive.
No search, owner reassignment, or repair inferred from an incorrect endpoint.
Prepared for @CubeJerry with substantial OpenAI Codex assistance.
"""
from fractions import Fraction
from functools import lru_cache
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("p104_dual_build_sources", HERE / "sources.py")
S = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(S)


def basis(vectors):
    generated, result = {0}, []
    for x in sorted(vectors):
        if x not in generated:
            result.append(x)
            generated |= {x ^ y for y in tuple(generated)}
    return result


@lru_cache(None)
def complement(frame):
    """Binary nullspace by elimination, distinct from the replay's 512-point scan."""
    rows = list(frame)
    pivots, pivot_row = [], 0
    for column in range(9):
        found = next((i for i in range(pivot_row, len(rows)) if rows[i] >> column & 1), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        for i in range(len(rows)):
            if i != pivot_row and rows[i] >> column & 1:
                rows[i] ^= rows[pivot_row]
        pivots.append(column)
        pivot_row += 1
    S.require(pivot_row == len(rows), "generator frame basis is dependent")
    null_basis = []
    for column in range(9):
        if column not in pivots:
            null_basis.append((1 << column) | sum(((row >> column) & 1) << p
                                                 for p, row in zip(pivots, rows)))
    values = {0}
    for x in null_basis:
        values |= {x ^ y for y in tuple(values)}
    return tuple(basis(values))


def forward(root):
    directory = root / "research/p104-interleaved-search"
    coalesced = S.module("source_coalesced", directory / "coalesced.py")
    compose = S.module("source_compose", root / "research/p104-coalesced-private-reuse/compose.py")
    built = compose.construct(coalesced)
    live = [i for i in range(112) if i not in coalesced.QC.REMOVED]
    result = dict(schema="p104-framed-word-v1", orientation="forward", public_registers=735,
                  port_pairs=[[i, i + 112, p] for i, p in zip(live, built["ports"])],
                  initial=[basis(f) for f in built["initial"]],
                  final=[basis(f) for f in built["final"]], events=[])
    for event in built["scalar_operations"]:
        kind = event["kind"]
        if kind == "transport":
            edge = built["transport_edges"][event["occurrence"]]
            translated = [kind, edge["register"], edge["source_frame"], edge["target_frame"],
                          edge["rank"], edge["private"]]
        elif kind in ("private_init", "private_discard"):
            translated = ["zero" if kind == "private_init" else "drop",
                          event["register"], event["frame"]]
        elif kind == "scale":
            translated = [kind, event["registers"][0], event["coefficient"], event["frame"]]
        else:
            S.require(kind in ("add", "private_copy"), "unknown predecessor event")
            translated = ["copy" if kind == "private_copy" else "add",
                          *event["registers"], event["coefficient"], event["frame"]]
        result["events"].append(translated)
    return result


def dual(word):
    """Reverse, transpose, complement, then conjugate by a fixed public sign gauge."""
    signed = {pair[0] for pair in word["port_pairs"]}
    cf = lambda f: list(complement(tuple(f)))
    result = dict(word, orientation="backward" if word["orientation"] == "forward" else "forward",
                  initial=[cf(f) for f in word["final"]], final=[cf(f) for f in word["initial"]],
                  events=[])
    for event in reversed(word["events"]):
        kind = event[0]
        if kind == "transport":
            changed = [kind, event[1], cf(event[3]), cf(event[2]), event[4], event[5]]
        elif kind in ("zero", "drop"):
            changed = ["drop" if kind == "zero" else "zero", event[1], cf(event[2])]
        elif kind == "scale":
            changed = [kind, event[1], event[2], cf(event[3])]
        else:
            S.require(kind in ("add", "copy"), "unknown dual event")
            coefficient = Fraction(event[3]) * (-1 if (event[1] in signed) != (event[2] in signed) else 1)
            changed = ["add", event[2], event[1], str(coefficient), cf(event[4])]
        result["events"].append(changed)
    return result


def regenerate():
    with S.predecessor() as root:
        original = forward(root)
    return original, dual(original)


if __name__ == "__main__":
    import argparse
    import gzip
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True, help="Fresh output directory")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    for name, value in zip(("FORWARD.json.gz", "BACKWARD.json.gz"), regenerate()):
        (args.out_dir / name).write_bytes(gzip.compress(S.canonical(value), mtime=0))
    print("PASS_REGENERATED_P104_COMPLEMENTARY_DUAL")
