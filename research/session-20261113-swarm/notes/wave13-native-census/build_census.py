#!/usr/bin/env python3
"""Regenerate a bounded recipe census from the pinned selected native archive.

This is a preflight only. It authenticates one pinned compressed source object,
then compiles every distinct ordered MOVE frame pair with the copied exact
Clifford compiler. It does not emit a tape program or claim a caller tariff.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "e54523517d0f03e58352e647c403a5af3e525a57"
SOURCE_PATH = "research/shared-wire-split-composition/data/final.json.gz"
SOURCE_BYTES = 350722
SOURCE_SHA256 = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
SOURCE_BLOB = "74563a7867d9d762b6588f65362369668841bb3e"
CANONICAL_SHA256 = "91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097"
COMPILER_PATH = HERE / "reference" / "clifford_exact.py"
COMPILER_SHA256 = "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962"
PUBLISHED_ANCHOR_RECIPE_SHA256 = {
    (3, 99): "064d51e9c347dbcfd9e172e5b5cab75f96912e0eb9a6f9537d53540cf4780ca9",
    (601, 470): "1902ee0f6e98746ff95204030bdb6251d196046a30b428307c8d698500cede93",
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def load_compiler():
    raw = COMPILER_PATH.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == COMPILER_SHA256, "compiler source drift")
    spec = importlib.util.spec_from_loader("selected_exact_clifford", loader=None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module.__name__] = module
    exec(compile(raw, str(COMPILER_PATH), "exec"), module.__dict__)
    return module


def source_archive(repo: Path) -> tuple[bytes, dict]:
    revision = f"{SOURCE_COMMIT}:{SOURCE_PATH}"
    blob = subprocess.check_output(["git", "-C", str(repo), "rev-parse", revision], text=True).strip()
    require(blob == SOURCE_BLOB, "selected source Git blob drift")
    raw = subprocess.check_output(["git", "-C", str(repo), "show", revision])
    require(len(raw) == SOURCE_BYTES, "selected source byte length drift")
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "selected source compressed hash drift")
    word = json.loads(gzip.decompress(raw))
    canonical = json.dumps(word, separators=(",", ":"), sort_keys=True).encode()
    require(hashlib.sha256(canonical).hexdigest() == CANONICAL_SHA256, "selected source canonical hash drift")
    return raw, word


def factor_stats(factors: list[dict], weights: list[int]) -> dict:
    offset_popcount = collections.Counter()
    phase = collections.Counter()
    linear_exp = collections.Counter()
    quadratic_edges = collections.Counter()
    matrix_identity = collections.Counter()
    nontrivial_matrices = set()
    nonzero_offset = 0
    nonzero_phase = 0
    phase_gate_types = collections.Counter()
    for factor, weight in zip(factors, weights):
        offset = factor["offset"]
        offset_popcount[str(offset.bit_count())] += weight
        nonzero_offset += weight * (offset != 0)
        constant = factor["phase"] % 4
        phase[str(constant)] += weight
        nonzero_phase += weight * (constant != 0)
        for exp in factor["linear_Z4"]:
            linear_exp[str(exp % 4)] += weight
            if exp % 4 == 1:
                phase_gate_types["S"] += weight
            elif exp % 4 == 2:
                phase_gate_types["Z"] += weight
            elif exp % 4 == 3:
                phase_gate_types["S_dagger"] += weight
        rows = factor["quadratic_rows"]
        edge_count = sum((rows[i] >> j) & 1 for i in range(len(rows)) for j in range(i + 1, len(rows)))
        quadratic_edges[str(edge_count)] += weight
        phase_gate_types["CZ"] += weight * edge_count
        ident = factor["matrix_rows"] == [1 << i for i in range(len(factor["matrix_rows"]))]
        matrix_identity[str(bool(ident)).lower()] += weight
        if not ident:
            nontrivial_matrices.add(tuple(factor["matrix_rows"]))
    return {
        "monomial_factor_occurrences": sum(weights),
        "offset_popcount_histogram": dict(sorted(offset_popcount.items(), key=lambda kv: int(kv[0]))),
        "nonzero_offset_factor_occurrences": nonzero_offset,
        "absolute_phase_histogram_mod4": dict(sorted(phase.items())),
        "nonzero_absolute_phase_factor_occurrences": nonzero_phase,
        "linear_phase_exponent_histogram_mod4": dict(sorted(linear_exp.items())),
        "quadratic_CZ_edge_count_histogram": dict(sorted(quadratic_edges.items(), key=lambda kv: int(kv[0]))),
        "diagonal_gate_type_counts_with_multiplicity": dict(sorted(phase_gate_types.items())),
        "binary_matrix_identity_histogram": dict(sorted(matrix_identity.items())),
        "distinct_nonidentity_binary_matrices": len(nontrivial_matrices),
        "literal_monomial_gate_types": ["X affine translations", "CNOT row additions", "S/Z single-qubit phases", "CZ quadratic phases", "global i^a phase"],
    }


def build(repo: Path, progress: bool = False) -> dict:
    _, word = source_archive(repo)
    require(len(word["program"]) == 71261, "selected word length")
    require(len(word["frames"]) == 1095, "selected frame table length")
    require(word["program"][24472] == ["MOVE", 415, 3, 99, False], "published rank-one binding event")
    require(word["frames"][3] == [] and word["frames"][99] == [239], "published rank-one frame pair")
    require(word["program"][28141] == ["MOVE", 1526, 601, 470, True], "published rank-two binding event")
    require(word["frames"][601] == [137] and word["frames"][470] == [75, 137, 265], "published rank-two frame pair")
    events = [(i, e) for i, e in enumerate(word["program"]) if e[0] == "MOVE"]
    require(len(events) == 6310, "MOVE event count")
    pair_weights = collections.Counter((event[2], event[3]) for _, event in events)
    frame_cache = {}
    compiler = load_compiler()
    cache = {}
    pair_rows = []

    def frame(fid):
        if fid not in frame_cache:
            frame_cache[fid] = compiler.canonical_frame(9, tuple(word["frames"][fid]))
        return frame_cache[fid]

    for pair_number, (start, end) in enumerate(sorted(pair_weights), start=1):
        op = frame(start).adjoint().then(frame(end))
        recipe, _ = compiler.lower_child(op)
        require(0 <= recipe["rank"] <= 8, f"invalid source central rank {start}->{end}")
        anchor_sha = PUBLISHED_ANCHOR_RECIPE_SHA256.get((start, end))
        if anchor_sha is not None:
            payload = json.dumps(recipe, separators=(",", ":"), sort_keys=True).encode()
            require(hashlib.sha256(payload).hexdigest() == anchor_sha,
                    f"published rank-1/rank-2 recipe drift for {start}->{end}")
        cache[(start, end)] = recipe
        pair_rows.append({"start_frame": start, "end_frame": end, "event_multiplicity": pair_weights[(start, end)], "recipe": recipe})
        if progress and pair_number % 250 == 0:
            print(f"compiled {pair_number}/{len(pair_weights)} frame pairs", file=sys.stderr, flush=True)

    def side_factors(recipe):
        return [recipe["left"]] + ([] if recipe["right"] is None else [recipe["right"]])

    event_rank = collections.Counter()
    pair_rank = collections.Counter()
    private_flag = collections.Counter()
    factors = []
    weights = []
    rank_factors = collections.Counter()
    rank_factor_weights = collections.Counter()
    source_frame_length = collections.Counter()
    event_source_frames = []
    for index, event in events:
        owner, start, end, private = event[1:]
        recipe = cache[(start, end)]
        event_rank[str(recipe["rank"])] += 1
        private_flag[str(bool(private)).lower()] += 1
        source_frame_length[f"{len(word['frames'][start])},{len(word['frames'][end])}"] += 1
        event_source_frames.append((index, start, end, int(bool(private)), recipe["rank"]))
    for (start, end), multiplicity in sorted(pair_weights.items()):
        recipe = cache[(start, end)]
        pair_rank[str(recipe["rank"])] += 1
        for factor in side_factors(recipe):
            factors.append(factor)
            weights.append(multiplicity)
            rank_factors[str(recipe["rank"])] += 1
            rank_factor_weights[str(recipe["rank"])] += multiplicity

    all_recipe_bytes = json.dumps(pair_rows, sort_keys=True, separators=(",", ":")).encode()
    pair_membership_bytes = json.dumps(event_source_frames, separators=(",", ":")).encode()
    rank_factor_summary = {}
    for rank in sorted(set(rank_factors) | set(rank_factor_weights), key=int):
        rank_factor_summary[rank] = {
            "monomial_factor_positions_over_distinct_pairs": rank_factors[rank],
            "monomial_factor_occurrences": rank_factor_weights[rank],
        }
    return {
        "schema": "selected-native-generic-preflight-census/1",
        "canonical_main": "e54523517d0f03e58352e647c403a5af3e525a57",
        "authenticated_selected_archive": {
            "commit": SOURCE_COMMIT,
            "path": SOURCE_PATH,
            "git_blob": SOURCE_BLOB,
            "compressed_bytes": SOURCE_BYTES,
            "compressed_sha256": SOURCE_SHA256,
            "canonical_word_sha256": CANONICAL_SHA256,
            "event_count": len(word["program"]),
            "frame_count": len(word["frames"]),
        },
        "scope": "Finite recipe census only. It does not implement a generic all-rank tape program or establish a selected physical tariff.",
        "move_events": len(events),
        "distinct_ordered_frame_pairs": len(pair_weights),
        "max_events_per_ordered_pair": max(pair_weights.values()),
        "frame_pair_rank_histograms": {
            "per_MOVE_event": dict(sorted(event_rank.items(), key=lambda kv: int(kv[0]))),
            "per_distinct_ordered_pair": dict(sorted(pair_rank.items(), key=lambda kv: int(kv[0]))),
        },
        "event_private_flag_histogram": dict(sorted(private_flag.items())),
        "source_frame_cardinalities_at_MOVE_events": dict(sorted(source_frame_length.items())),
        "monomial_recipe_summary": factor_stats(factors, weights),
        "monomial_factor_counts_by_central_rank": rank_factor_summary,
        "ordered_pair_recipe_payload_sha256": hashlib.sha256(all_recipe_bytes).hexdigest(),
        "ordered_event_to_pair_rank_payload_sha256": hashlib.sha256(pair_membership_bytes).hexdigest(),
        "note": "The digests bind deterministic full recipe/event payloads regenerated by build_census.py; only aggregate histograms are materialized here to keep the receipt compact.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path, help="Git checkout holding the pinned source object")
    parser.add_argument("--write", action="store_true", help="write CENSUS.json; default prints only")
    parser.add_argument("--progress", action="store_true", help="print bounded progress to stderr")
    args = parser.parse_args()
    require(__debug__, "run normally; the pinned exact compiler uses assertions as internal checks")
    result = build(args.repo, progress=args.progress)
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "CENSUS.json").write_text(output)
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
