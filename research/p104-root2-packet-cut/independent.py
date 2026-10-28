#!/usr/bin/env python3
"""Independent two-column obstruction for the PR6144 root2 packet repair.

Uses Fraction pairs and an incremental invariant, importing no primary or
predecessor replay. Default and optimized execution are read-only. This checks
an exact finite obstruction, not the multiplication theorem or native operators.
Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import gzip
import json

Q = Fraction
ZERO = (Q(0), Q(0))
HERE = Path(__file__).resolve().parent
SOURCE_HEAD = "4f3b67e7c37ae270da9584033132866d0cf63e42"
WORD_SHA256 = "c71985d96bf3d4a35aae111aaba87e376f7367efb4a5686278ef293732757533"
WORD_BLOB = "69b70ee50c697b185ebf585fbe69f2487af32d1d"
WORD_SIZE = 119901
PACKET_READS = (13485, 13487, 13489, 13490, 13614, 13615, 13616, 13617, 13618)
ALLOWED_CHARTS = frozenset((3, 595, 738))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def serialized_pair(pair):
    return [str(value) for value in pair]


def authenticated_word(raw):
    require(len(raw) == WORD_SIZE, "immutable word size")
    require(sha256(raw).hexdigest() == WORD_SHA256, "immutable word SHA256")
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    require(sha1(header + raw).hexdigest() == WORD_BLOB, "immutable word Git blob")
    return json.loads(gzip.decompress(raw))


def validate_model(word):
    program = word["program"]
    require(word["public"] == 770 and word["owned_fields"] == 29, "source inventory")
    require(len(program) == 22818, "source event count")
    require(0 in word["live"] and 8 in word["live"], "watched main inputs")
    require(program[12913] == ["MOVE", 451, 3, 737, False], "first reader move")
    require(program[12918] == ["ADD", 451, 228, "1", 737], "old correction read")
    require(program[13481] == ["COPY", 772, 146, "1", 529], "old packet creation")
    require(program[14523] == ["MOVE", 451, 737, 738, False], "second reader move")
    actual = tuple(index for index, event in enumerate(program)
                   if event[0] == "ADD" and event[2] == 772)
    require(actual == PACKET_READS, "all nine packet reads accounted for")


def baseline_event(index, event, *, keep_copy=False, keep_old_read=False):
    if index in PACKET_READS or (index == 13481 and not keep_copy) or (index == 12918 and not keep_old_read):
        return None
    if index == 12913:
        return ["MOVE", 451, 3, 595, False]
    if index == 14523:
        return ["MOVE", 451, 595, 738, False]
    return event


def advance(rows, charts, event):
    kind, target = event[:2]
    if kind == "MOVE":
        charts[target] = event[3]
    elif kind == "INIT":
        charts[target], rows[target] = event[2], ZERO
    elif kind == "CLEAR":
        charts[target], rows[target] = None, ZERO
    elif kind == "ADD":
        factor, source = Q(event[3]), rows[event[2]]
        rows[target] = (rows[target][0] + factor * source[0], rows[target][1] + factor * source[1])
    elif kind == "COPY":
        factor, source = Q(event[3]), rows[event[2]]
        rows[target] = (factor * source[0], factor * source[1])
    elif kind == "SCALE":
        factor = Q(event[2])
        rows[target] = (factor * rows[target][0], factor * rows[target][1])
    else:
        raise ValueError("unrecognized source opcode")


def determinant(left, right):
    return left[0] * right[1] - left[1] * right[0]


def row_rank_and_witness(rows):
    first = next((index for index, row in enumerate(rows) if row != ZERO), None)
    if first is None:
        return 0, None
    for second in range(first + 1, len(rows)):
        value = determinant(rows[first], rows[second])
        if value:
            return 2, (first, second, value)
    return 1, (first,)


def simulate(word, *, allowed=ALLOWED_CHARTS, keep_copy=False, keep_old_read=False, watch=(0, 8)):
    """Prove every-cut coverage by checking initial eligible rows and each changed row.

    Between consecutive cuts only an event's destination can change its row or
    chart. The active-role set therefore gives exact coverage counts without
    scanning all799 fields at every cut, unlike the separate primary engine.
    """
    program = word["program"]
    original = [(Q(role == watch[0]), Q(role == watch[1])) for role in range(799)]
    baseline = list(original)
    original_charts = list(word["initial"]) + [None] * 29
    charts = list(original_charts)
    active = {role for role, chart in enumerate(charts) if chart in allowed}
    versions, seen_roles = [], set()
    checks = 0

    def observe_changed(cut, role):
        nonlocal checks
        checks += 1
        require(baseline[role] == ZERO, f"nonzero envelope row at cut {cut}, role {role}")
        if role not in seen_roles:
            seen_roles.add(role)
            versions.append({"first_cut": cut, "role": role, "projection": serialized_pair(baseline[role])})

    for role in sorted(active):
        observe_changed(0, role)
    observations = 0
    phase_observations = {"before_cut13679": 0, "from_cut13679": 0}
    original_checkpoints = {}
    for cut in range(len(program) + 1):
        observations += len(active)
        phase_observations["before_cut13679" if cut < 13679 else "from_cut13679"] += len(active)
        if cut == 13679:
            original_checkpoints["572_at_13679"] = serialized_pair(original[572])
        if cut == 14524:
            original_checkpoints["451_at_14524"] = serialized_pair(original[451])
        if cut == len(program):
            break
        event = program[cut]
        advance(original, original_charts, event)
        changed = baseline_event(cut, event, keep_copy=keep_copy, keep_old_read=keep_old_read)
        if changed is None:
            continue
        target = changed[1]
        advance(baseline, charts, changed)
        if charts[target] in allowed:
            active.add(target)
            observe_changed(cut + 1, target)
        else:
            active.discard(target)
    # Independently establish the two original input columns at every endpoint.
    live = set(word["live"])
    for role, actual in enumerate(original):
        expected = tuple(Q(role == source) + Q(source in live and role == source + 112)
                         if source is not None else Q(0) for source in watch)
        if role >= word["public"]:
            expected = ZERO
        require(actual == expected, f"original endpoint column check, role {role}")
    final_charts = list(word["final"]) + [None] * 29
    require(original_charts == final_charts and charts == final_charts, "complete final frame inventory")
    residual = [(expected[0] - actual[0], expected[1] - actual[1])
                for expected, actual in zip(original, baseline)]
    rank, witness = row_rank_and_witness(residual)
    return {
        "original": original, "baseline": baseline, "residual": residual,
        "rank": rank, "witness": witness, "versions": versions,
        "observation_count": observations, "phase_observations": phase_observations,
        "incremental_invariant_checks": checks, "original_checkpoints": original_checkpoints,
    }


def expect_rejection(function, label, expected_reason):
    try:
        function()
    except ValueError as error:
        require(expected_reason in str(error), f"wrong rejection reason: {label}: {error}")
        return
    raise ValueError(f"negative control accepted: {label}")


def controls(raw, word, result):
    expect_rejection(lambda: simulate(word, keep_copy=True), "omitted packet COPY deletion", "nonzero envelope row")
    expect_rejection(lambda: simulate(word, keep_old_read=True), "retained old228 read", "nonzero envelope row")
    expect_rejection(lambda: simulate(word, allowed=ALLOWED_CHARTS | {737}), "extra chart737", "nonzero envelope row")
    one_column = simulate(word, watch=(0, None))
    require(one_column["rank"] == 1, "omitted second input must lose rank-two obstruction")
    # Two independent freely injected packets repair every watched endpoint.
    q0, q8 = (Q(1), Q(0)), (Q(0), Q(1))
    for base, wanted, correction in zip(result["baseline"], result["original"], result["residual"]):
        repaired = tuple(base[column] + correction[0] * q0[column] + correction[1] * q8[column]
                         for column in range(2))
        require(repaired == wanted, "two-packet projected repair positive control")
    damaged = bytearray(raw)
    damaged[len(damaged) // 2] ^= 1
    expect_rejection(lambda: authenticated_word(bytes(damaged)), "changed immutable source", "immutable word SHA256")
    return ["missing_COPY_deletion_rejected", "retained_old228_read_rejected", "chart737_expansion_rejected",
            "one_watched_column_rank_one", "two_packet_projected_repair", "changed_immutable_word_rejected"]


def compute(raw):
    word = authenticated_word(raw)
    validate_model(word)
    result = simulate(word)
    require(result["rank"] == 2, "final correction rank")
    first, second, det = result["witness"]
    require((first, second, det) == (112, 144, Q(-1, 4)), "independent final minor")
    passed_controls = controls(raw, word, result)
    return {
        "schema": "p104-root2-independent-full-endpoint-cut/1",
        "source_head": SOURCE_HEAD, "source_sha256": WORD_SHA256,
        "source_git_blob": WORD_BLOB, "source_size": WORD_SIZE,
        "watched_initial_columns": [0, 8], "freely_granted_other_columns": 797,
        "chart_envelope": sorted(ALLOWED_CHARTS), "all_fields_including_packet": 799,
        "reference_event_count": len(word["program"]), "cuts_inclusive": [0, len(word["program"])],
        "baseline_deletions": sorted([12918, 13481, *PACKET_READS]),
        "baseline_move_replacements": {"12913": ["MOVE", 451, 3, 595, False],
                                       "14523": ["MOVE", 451, 595, 738, False]},
        "eligible_cut_role_observations": result["observation_count"],
        "observation_partition": result["phase_observations"],
        "incremental_invariant_checks": result["incremental_invariant_checks"],
        "distinct_role_projection_versions": len(result["versions"]),
        "canonical_version_sha256": sha256(canonical(result["versions"])).hexdigest(),
        "packet_free_envelope_projection": ["0", "0"],
        "original_endpoint_entries_checked": 1598,
        "original_intermediate_targets": result["original_checkpoints"],
        "final_residual_nonzero_rows": sum(row != ZERO for row in result["residual"]),
        "final_residual_rank": result["rank"],
        "final_residual_sha256": sha256(canonical([serialized_pair(row) for row in result["residual"]])).hexdigest(),
        "final_minor": {"rows": [first, second], "values": [serialized_pair(result["residual"][first]),
                                                               serialized_pair(result["residual"][second])],
                        "determinant": str(det)},
        "controls_passed": passed_controls,
        "scope": "One fixed linear packet, arbitrary recoding in the stated chart envelope, fixed outside instructions; full watched endpoints, no new kappa.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-json", action="store_true", help="emit a fresh receipt to stdout without writing files")
    args = parser.parse_args()
    result = compute((HERE / "inputs" / "pr6144-WORD.json.gz").read_bytes())
    if args.emit_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected = json.loads((HERE / "INDEPENDENT.json").read_text())
    require(canonical(expected) == canonical(result), "complete independent receipt mismatch")
    print("PASS_ROOT2_PACKET_CUT_INDEPENDENT final_rank=2 minor=-1/4 controls=6")


if __name__ == "__main__":
    main()
