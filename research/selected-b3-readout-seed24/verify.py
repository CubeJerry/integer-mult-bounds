#!/usr/bin/env python3
"""Exact selected B[201:235] replacement. @CubeJerry + OpenAI Codex, Apache-2.0.

Restored target bases follow PR749/901/932. The literal cleared-work lowering
follows the retained PR558 -> PR552 -> PR531 invoice convention. No predecessor
implementation is imported. This checks a local circuit, not global admission.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import groupby
import json
from pathlib import Path
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = "research/community-frontier1094-audit/selected-replay.tar.gz"
ARCHIVE_SHA = "f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6"
PREFIX = "candidate/strict/global/base/providers/gauge44/"
PINS = {
    "CANONICAL-WORD.json.gz": "16bc0ebb04b4be6c0ade74badc6a0c0cdba4215eda86e4ff9f13abf8ecebd219",
    "LOCAL-PROGRAMS.json.gz": "241fde27d4e43f5a9cb6b128f9f76c5131a53d09f0371676163f914d0b0fef3a",
    "LOCAL-CHECKS.json": "2b8b1891a736598010232bfb26abc31973b265a53a2009a3fcfd9138b5ecadb4",
    "INDEPENDENT-LOCAL-REPLAY.json": "13dd18297162569532983db1a2ab67926b064330cd7edd3587e7b546b2dedf17",
}
WORK = ("W", 0)
GROUPS = (((179, 115, 120, 138), (664, 665, 666, 668)),
          ((117, 181, 208, 177), (672, 673, 674, 676)))
READOUT = ((-1, -1, -1, -1), (1, -1, -1, 1),
           (-1, -1, -1, 1), (1, -1, 1, 1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_sources():
    require(sha((ROOT / ARCHIVE).read_bytes()) == ARCHIVE_SHA, "archive pin")
    result = {}
    with tarfile.open(ROOT / ARCHIVE) as archive:
        for name, digest in PINS.items():
            data = archive.extractfile(PREFIX + name).read()
            require(sha(data) == digest, "member pin: " + name)
            result[name] = json.loads(gzip.decompress(data) if name.endswith(".gz") else data)
    return (result[name] for name in PINS)


def add(t, s, n=1, d=1):
    return ["add", t, s, n, d, 3]


def replacement():
    """Two restored chains; y1 -> y3 -> y2 -> y4 in each group."""
    out = []
    for targets, sources in GROUPS:
        y1, y2, y3, y4 = targets
        a, b, c, d = sources
        out += [add(y4, y2, -1), add(y2, y3, -1), add(y3, y1, -1)]
        out += [add(y1, s, -1, 2) for s in sources]
        out += [add(y3, d), add(y2, a), add(y4, c)]
        out += [add(y3, y1), add(y2, y3), add(y4, y2)]
    # The old helper pulse adds precisely L566 to target L181 and restores L676.
    out += [add(181, 566)]
    return out


def readout_map(ids, orientation):
    """Closed-form block specification, without replaying either gate list."""
    rows = {r: {r: Q(1)} for r in ids}
    terms = [(t, s, Q(READOUT[i][j], 2))
             for targets, sources in GROUPS
             for i, t in enumerate(targets) for j, s in enumerate(sources)]
    terms.append((181, 566, Q(1)))
    for target, source, coefficient in terms:
        if orientation == "backward":
            target, source, coefficient = source, target, -coefficient
        rows[("L", target)][("L", source)] = coefficient
    return rows


def event(gate, orientation):
    tag, t, s, n, d, frame = gate
    require(tag == "add" and t != s, "ADD gate contract")
    if orientation == "backward":
        t, s, n = s, t, -n
    return ["scalar", [tag, ["L", t], ["L", s], n, d], frame]


def registers(op):
    return [tuple(op[1])] + ([tuple(op[2])] if op[0] in ("add", "copy") else [])


def sparse_step(rows, op):
    """Exact scalar-macro oracle, independent of the literal primitive replay."""
    tag, t = op[0], tuple(op[1])
    if tag == "clear":
        rows[t] = {}
    elif tag == "copy":
        rows[t] = rows[tuple(op[2])].copy()
    elif tag == "scale":
        factor = Q(op[2], op[3])
        rows[t] = {j: factor * value for j, value in rows[t].items()}
    else:
        require(tag == "add", "macro opcode")
        s, factor = tuple(op[2]), Q(op[3], op[4])
        require(t != s, "distinct ADD operands")
        for j, value in rows[s].items():
            value = rows[t].get(j, Q(0)) + factor * value
            if value:
                rows[t][j] = value
            else:
                rows[t].pop(j, None)


def macro_map(events, ids):
    rows = {r: {r: Q(1)} for r in ids}
    for item in events:
        if item[0] == "scalar":
            sparse_step(rows, item[1])
    return rows


def lower(op):
    """Explicit paid instructions, with initially arbitrary coefficient work."""
    tag, target = op[0], tuple(op[1])
    if tag in ("clear", "copy"):
        return [(tag, target, tuple(op[2]))] if tag == "copy" else [(tag, target)]
    if tag == "scale":
        factor = Q(op[2], op[3])
        a, d = abs(factor.numerator), factor.denominator
        require(a and a & (a - 1) == 0 and d & (d - 1) == 0, "dyadic unit scale")
        shift = a.bit_length() - d.bit_length()
        return ([("double" if shift > 0 else "halve", target)] * abs(shift)
                + ([("negate", target)] if factor < 0 else []))
    require(tag == "add", "lowering opcode")
    source, factor = tuple(op[2]), Q(op[3], op[4])
    require(source != target and WORK not in (source, target) and factor, "lowering operands")
    require(factor.denominator & (factor.denominator - 1) == 0, "dyadic ADD")
    out = [("clear", WORK)]
    for i, bit in enumerate(bin(abs(factor.numerator))[2:]):
        if i:
            out.append(("double", WORK))
        if bit == "1":
            out.append(("add", WORK, source))
    out += [("halve", WORK)] * (factor.denominator.bit_length() - 1)
    out += [("add" if factor > 0 else "subtract", target, WORK), ("clear", WORK)]
    return out


def primitive_map(instructions, ids):
    """Dense basis-column replay of individual real-component instructions."""
    positions = {r: i for i, r in enumerate(ids)}
    matrix = [[Q(i == j) for j in range(len(ids))] for i in range(len(ids))]
    for op in instructions:
        tag, i = op[0], positions[op[1]]
        if tag == "clear":
            matrix[i] = [Q(0)] * len(ids)
        elif tag == "copy":
            matrix[i] = matrix[positions[op[2]]].copy()
        elif tag in ("double", "halve", "negate"):
            factor = {"double": Q(2), "halve": Q(1, 2), "negate": Q(-1)}[tag]
            matrix[i] = [factor * value for value in matrix[i]]
        else:
            require(tag in ("add", "subtract"), "primitive opcode")
            sign = 1 if tag == "add" else -1
            matrix[i] = [a + sign * b for a, b in zip(matrix[i], matrix[positions[op[2]]])]
    return {r: {s: matrix[i][j] for j, s in enumerate(ids) if matrix[i][j]}
            for i, r in enumerate(ids)}


def touched(item, register):
    return item[0] == "scalar" and ("L", register) in registers(item[1])


def splice(program, old_gates, new_gates, orientation, starts):
    wanted = [event(gate, orientation) for gate in old_gates]
    hits = [i for i, item in enumerate(program) if item == wanted[0]]
    require(len(hits) == 1, "unique source window")
    lo = hits[0]
    scalars, hi = [], lo
    while len(scalars) < len(wanted):
        require(hi < len(program), "complete source window")
        item = program[hi]
        if item[0] == "scalar":
            scalars.append(item)
        else:
            require(item[0] == "climb" and item[1] == "B" and item[4] == 3,
                    "only B climbs to frame 3 inside window")
        hi += 1
    require(scalars == wanted, "literal old B block")
    window = program[lo:hi]
    climbs = [item for item in window if item[0] == "climb"]
    for offset, item in enumerate(window):
        if item[0] == "climb":
            require(not any(touched(prior, item[2]) for prior in window[:offset]),
                    "hoisted climb must precede its first scalar touch")
    current = list(starts)
    for item in program[:lo]:
        if item[0] == "climb":
            require(current[item[2]] == item[3], "prefix old frame")
            current[item[2]] = item[4]
    for item in climbs:
        require(current[item[2]] == item[3], "hoisted old frame")
        current[item[2]] = item[4]
    new_events = [event(gate, orientation) for gate in new_gates]
    for item in new_events:
        require(item[2] == 3 and all(current[r[1]] == 3 for r in registers(item[1])),
                "replacement common frame")
    changed = program[:lo] + climbs + new_events + program[hi:]
    require([e for e in changed if e[0] != "scalar"] ==
            [e for e in program if e[0] != "scalar"], "ordered native events unchanged")
    return changed, {"start": lo, "stop": hi, "hoisted_climbs": climbs}


def invoice(program, n):
    """Whole-program primitive count and retained scalar positive majorant."""
    envelopes = {("L", i): Q(1) for i in range(n)}
    peak, counts, macros = Q(1), Counter(), 0
    paid = Counter()
    for item in program:
        if item[0] == "climb":
            paid[item[5]] += 1
        elif item[0] == "center":
            paid[item[4]] += 1
        if item[0] != "scalar":
            continue
        macros += 1
        for op in lower(item[1]):
            tag, target = op[:2]
            counts[tag] += 1
            if tag == "clear":
                envelopes[target] = Q(0)
            elif tag == "copy":
                envelopes[target] = envelopes[op[2]]
            elif tag in ("double", "halve", "negate"):
                envelopes[target] *= {"double": Q(2), "halve": Q(1, 2), "negate": Q(1)}[tag]
            else:
                envelopes[target] = envelopes.get(target, Q(0)) + envelopes[op[2]]
            peak = max(peak, envelopes[target])
    return {"scalar_macros": macros, "real_component_primitives": 2 * sum(counts.values()),
            "instructions_per_component": dict(sorted(counts.items())),
            "prefix_l1_upper": str(peak),
            "prefix_bits_upper": peak.numerator.bit_length() - peak.denominator.bit_length() + 1,
            "paid_profile": {str(r): count for r, count in sorted(paid.items())}}


def rejection(check, label):
    try:
        check()
    except ValueError:
        return label
    raise ValueError("control was accepted: " + label)


def verify():
    word, programs, checks, inherited = load_sources()
    runs = []
    for frame, group in groupby(enumerate(word["B"]), key=lambda pair: pair[1][-1]):
        members = list(group)
        if len(members) >= 10:
            runs.append([members[0][0], members[-1][0] + 1, frame])
    require(len(runs) == 20 and runs[24 % len(runs)] == [201, 235, 3], "seed-selected block")
    old, new = word["B"][201:235], replacement()
    require(word["frames"][3] == [51] and len(old) == 34 and len(new) == 27, "source block shape")
    require(all(g[-1] == 3 for g in old + new), "fixed frame")
    ids = [("L", i) for i in sorted({r for g in old + new for r in g[1:3]})]
    require(len(ids) == 17, "17 logical registers")
    n = 2 * word["v"] + word["R"]
    require(n == 704, "selected logical width")
    all_ids = [("L", i) for i in range(n)] + [("C", i) for i in range(8)]
    result = {"status": "PASS_SELECTED_B3_READOUT", "assignment_seed": 24,
              "source_archive_sha256": ARCHIVE_SHA, "members": PINS,
              "selection_domain": runs, "selection_index": 24 % len(runs),
              "canonical_B_slice": [201, 235], "frame_id": 3, "frame_basis": [51],
              "original_gates": old, "replacement_gates": new, "orientations": {}, "controls": []}
    emitted = {}
    for orientation in ("forward", "backward"):
        before = [event(g, orientation) for g in old]
        after = [event(g, orientation) for g in new]
        expected = readout_map(ids, orientation)
        require(macro_map(before, ids) == expected, "original block closed-form identity")
        require(macro_map(after, ids) == expected, "arbitrary dirty block identity")
        prim_old = [p for e in before for p in lower(e[1])]
        prim_new = [p for e in after for p in lower(e[1])]
        literal = primitive_map(prim_new, ids + [WORK])
        require(literal[WORK] == {} and all(literal[r] == expected[r] for r in ids),
                "literal arbitrary-work primitive identity")
        require(primitive_map(prim_old, ids + [WORK]) == literal, "independent primitive comparison")
        changed, window = splice(programs[orientation], old, new, orientation, word["start"])
        emitted[orientation] = changed
        baseline_map = macro_map(programs[orientation], all_ids)
        candidate_map = macro_map(changed, all_ids)
        require(baseline_map == candidate_map, "whole scalar program map on 712 columns")
        endpoint = {r: ({r: Q(1)} if r[0] == "L" else {}) for r in all_ids}
        for port in range(word["v"]):
            target, source, sign = (word["v"] + port, port, 1)
            if orientation == "backward":
                target, source, sign = source, target, -1
            endpoint[("L", target)][("L", source)] = Q(sign)
        require(candidate_map == endpoint, "complete scalar shear and helper return")
        baseline, candidate = invoice(programs[orientation], n), invoice(changed, n)
        source_check = checks[orientation]
        require(baseline["real_component_primitives"] == source_check["real_component_primitive_bound"],
                "baseline primitive receipt")
        require(baseline["scalar_macros"] == source_check["scalar_macros"], "baseline macro receipt")
        require(baseline["prefix_l1_upper"] == inherited["local"][orientation]["prefix_l1_upper"],
                "baseline prefix receipt")
        require(candidate["paid_profile"] == baseline["paid_profile"] == word["local_profile"],
                "paid profile retained")
        require(Q(candidate["prefix_l1_upper"]) < 2 ** inherited["local"][orientation]["charged_payload_bits"],
                "inherited scalar prefix charge")
        require(baseline["real_component_primitives"] - candidate["real_component_primitives"] ==
                2 * (len(prim_old) - len(prim_new)) > 0, "complete primitive saving")
        result["orientations"][orientation] = {
            "window": window, "baseline": baseline, "candidate": candidate,
            "block_primitives_per_component": [len(prim_old), len(prim_new)],
            "program_sha256": sha(canonical(changed)), "full_scalar_columns": len(all_ids),
            "local_primitive_columns": len(ids) + 1,
            "inherited_charged_payload_bits": inherited["local"][orientation]["charged_payload_bits"],
        }
        for label, faulty in [("missing_preparation", new[1:]),
                              ("missing_restoration", new[:10] + new[11:]),
                              ("missing_pulse_correction", new[:-1])]:
            result["controls"].append(rejection(
                lambda faulty=faulty: require(macro_map([event(g, orientation) for g in faulty], ids) == expected,
                                              "bad local identity"), orientation + ":" + label))
        bad = deepcopy(new)
        bad[-1][3] = -1
        result["controls"].append(rejection(
            lambda: require(macro_map([event(g, orientation) for g in bad], ids) == expected, "wrong pulse sign"),
            orientation + ":wrong_pulse_sign"))
        bad_frame = deepcopy(new)
        bad_frame[0][-1] = 0
        result["controls"].append(rejection(
            lambda: splice(programs[orientation], old, bad_frame, orientation, word["start"]),
            orientation + ":wrong_frame"))
        result["controls"].append(rejection(
            lambda: require(primitive_map(prim_new[:-1], ids + [WORK]) == literal, "coefficient work not erased"),
            orientation + ":missing_final_work_clear"))
    return result, emitted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write receipt to a new path; never overwrite")
    parser.add_argument("--emit", type=Path, help="write exact candidate event streams to a new directory")
    args = parser.parse_args()
    result, emitted = verify()
    if args.write:
        with args.write.open("x") as output:
            output.write(json.dumps(result, indent=2) + "\n")
    else:
        require(json.loads((HERE / "RESULT.json").read_text()) == result, "complete result certificate")
    if args.emit:
        args.emit.mkdir(parents=True, exist_ok=False)
        for name, value in [("LOCAL-PROGRAMS.json", emitted), ("RESULT.json", result)]:
            (args.emit / name).write_bytes(canonical(value) + b"\n")
    f = result["orientations"]["forward"]
    print("PASS_SELECTED_B3_READOUT gates=34->27 block_component_primitives="
          + "->".join(map(str, f["block_primitives_per_component"]))
          + " full_columns=712 orientations=2 controls=" + str(len(result["controls"]))
          + " no_new_kappa")


if __name__ == "__main__":
    main()
