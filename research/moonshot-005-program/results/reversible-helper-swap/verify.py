#!/usr/bin/env python3
"""Exact source-bound reversible neutral-helper swap and paid q-return.

Source lineage: integer-mult-bounds selected native, programme source-row and
typed-word methods. This checker creates a partial coupling, not a full shared
native or a multiplication supplier. Prepared with OpenAI assistance.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
EVENT, DONOR, RECEIVER, HELPER = 41779, 60, 213, 1024
SOURCE_CHART, ARRIVAL_CHART, HUB = 962, 221, 127


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b, coefficient=F(1)):
    result = a.copy()
    for key, value in b.items():
        updated = result.get(key, F(0)) + coefficient * value
        if updated:
            result[key] = updated
        else:
            result.pop(key, None)
    return result


def scaled(row, coefficient):
    return {key: coefficient * value for key, value in row.items() if coefficient * value}


def encoded(row):
    return [[key, str(value)] for key, value in sorted(row.items())]


def space(frame):
    values = {0}
    for vector in frame:
        values |= {value ^ vector for value in tuple(values)}
    return frozenset(values)


def native_rows_and_pulse(w):
    rows = {i: {i: F(1)} for i in range(w["public"])}
    pulse = {i: F(0) for i in range(w["public"])}
    chart = dict(enumerate(w["initial"]))
    payload = None
    guards = []
    for t, op in enumerate(w["program"]):
        kind, r = op[:2]
        if t == EVENT:
            need(op == ["MOVE", HELPER, SOURCE_CHART, ARRIVAL_CHART, False], "actual selected helper departure")
            payload = rows[r].copy()
            pulse[r] += 1
        if kind == "INIT":
            rows[r], pulse[r], chart[r] = {}, F(0), op[2]
        elif kind == "CLEAR":
            rows.pop(r)
            pulse.pop(r)
            chart.pop(r)
        elif kind == "MOVE":
            need(chart[r] == op[2], "source location")
            chart[r] = op[3]
        elif kind == "SCALE":
            rows[r] = scaled(rows[r], F(op[2]))
            pulse[r] *= F(op[2])
        elif kind in ("ADD", "COPY"):
            s, c, at = op[2:]
            need(chart[r] == chart[s] == at, "source arithmetic cochart")
            if kind == "COPY":
                need(not rows[r], "native COPY zero guard")
                guards.append([t, str(pulse[r])])
                need(not pulse[r], "selected pulse COPY zero guard")
            rows[r] = add(rows[r], rows[s], F(c))
            pulse[r] += F(c) * pulse[s]
        else:
            raise ValueError("unknown source opcode")
    need(set(rows) == set(range(w["public"])), "native all owned roles retired")
    z = {r: value for r, value in pulse.items() if value}
    need(z and all(w["final"][r] == HUB for r in z), "nonzero response restricted to actual hub")
    need(chart == dict(enumerate(w["final"])), "native final locations")
    declared = {r: {r: F(1)} for r in range(1480)}
    inverse = {r: {r: F(1)} for r in range(1480)}
    for index, x in enumerate(w["live"]):
        y = x + 112
        if index in w["hosted"]["Dports"]:
            declared[y] = {y: F(1), x: F(1)}
            inverse[y] = {y: F(1), x: F(-1)}
        else:
            declared[x], declared[y] = {x: F(1), y: F(-1)}, {x: F(1, 2), y: F(1, 2)}
            inverse[x], inverse[y] = {x: F(1, 2), y: F(1)}, {y: F(1), x: F(-1, 2)}
    for x, y in zip(w["hosted"]["X2"], w["hosted"]["Y2"]):
        declared[x], inverse[x] = {x: F(1), y: F(-1)}, {x: F(1), y: F(1)}
    need(rows == declared, "complete declared source endpoint map")
    for r, inverse_row in inverse.items():
        rebuilt = {}
        for j, coefficient in inverse_row.items():
            rebuilt = add(rebuilt, rows[j], coefficient)
        need(rebuilt == {r: F(1)}, "complete native inverse")
    terminal_payload = {}
    for r, coefficient in payload.items():
        terminal_payload = add(terminal_payload, inverse[r], coefficient)
    offhub_payload = {r: value for r, value in terminal_payload.items() if w["final"][r] != HUB}
    need(offhub_payload, "displaced payload is not a hub-only terminal row")
    return rows, payload, z, guards, offhub_payload


def build_word(w, pulse):
    mains = sorted(set(w["live"]) | {r + 112 for r in w["live"]} | set(w["hosted"]["X2"]) | set(w["hosted"]["Y2"]))
    need(len(mains) == 400, "all400 private main roles")
    raw = {r: 1480 + j for j, r in enumerate(mains)}
    owned_q = 1880 + w["owned_fields"]
    ops = [["ADD", raw[r], r, "-1", w["initial"][r]] for r in mains]
    reservations = []
    marks = {}

    def common_role(r):
        return r + 400 if r >= 1480 else r

    for t, original in enumerate(w["program"]):
        if t == EVENT:
            marks["swap_start"] = len(ops)
            # A reversible swap with no temporary owned record.
            ops.extend([
                ["ADD", HELPER, raw[DONOR], "1", SOURCE_CHART],
                ["ADD", raw[DONOR], HELPER, "-1", SOURCE_CHART],
                ["ADD", HELPER, raw[DONOR], "1", SOURCE_CHART],
                ["SCALE", raw[DONOR], "-1", SOURCE_CHART],
            ])
        actual = original.copy()
        actual[1] = common_role(actual[1])
        if actual[0] in ("ADD", "COPY"):
            actual[2] = common_role(actual[2])
        ops.append(actual)
        if t == EVENT:
            marks["receiver_observation"] = len(ops)
            ops.extend([
                ["ADD", raw[RECEIVER], HELPER, "1", ARRIVAL_CHART],
                ["INIT", owned_q, ARRIVAL_CHART],
                ["ADD", owned_q, HELPER, "1", ARRIVAL_CHART],
                ["MOVE", owned_q, ARRIVAL_CHART, HUB, True],
            ])
        if original[0] == "MOVE" and original[1] in raw:
            reservations.append({"source_event": t, "physical_event": len(ops), "role": original[1]})
            ops.append(["MOVE", raw[original[1]], original[2], original[3], False])
    marks["common_completion"] = len(ops)
    ops.append(["ADD", owned_q, raw[DONOR], "-1", HUB])
    ops.extend(["ADD", r, owned_q, str(-c), HUB] for r, c in sorted(pulse.items()))
    ops.extend([
        ["ADD", raw[DONOR], owned_q, "1", HUB],
        ["CLEAR", owned_q, HUB],
    ])
    marks["common_and_raw_restored"] = len(ops)
    ops.extend(["ADD", raw[r], r, "1", w["final"][r]] for r in mains)
    need(len(reservations) == 1710 and len({item["source_event"] for item in reservations}) == 1710, "all original raw reservations exactly once")
    return {
        "schema": "moonshot-reversible-neutral-helper-swap-word-v1",
        "source_sha256": PIN,
        "public": 1880,
        "owned_fields": w["owned_fields"] + 1,
        "initial": w["initial"] + [w["initial"][r] for r in mains],
        "private_role_map": {str(r): q for r, q in raw.items()},
        "program": ops,
        "raw_reservations": reservations,
        "marks": marks,
        "includes_all400_entry_differences": True,
        "includes_all400_final_recouplings": True,
        "new_moves": [{"role": owned_q, "source": ARRIVAL_CHART, "target": HUB, "rank": 1}],
    }, raw, owned_q


def physical_replay(w, word, raw, q_cache, expected, payload, pulse):
    state = {i: {i: F(1)} for i in range(word["public"])}
    chart = dict(enumerate(word["initial"]))
    spaces = list(map(space, w["frames"]))
    counts, moves_by_rank = Counter(), Counter()
    lifetimes = peak = 0
    selected_q = {raw[DONOR]: F(1), DONOR: F(-1)}
    debt = add(selected_q, payload, F(-1))
    checkpoints = {}
    for t, op in enumerate(word["program"]):
        kind, r = op[:2]
        need(0 <= r < word["public"] + word["owned_fields"], "declared physical role")
        counts[kind] += 1
        if kind == "INIT":
            need(r >= word["public"] and r not in chart, "fresh owned INIT")
            state[r], chart[r] = {}, op[2]
            lifetimes += 1
        elif kind == "CLEAR":
            need(r >= word["public"] and chart.get(r) == op[2], "owned CLEAR at actual chart")
            state.pop(r)
            chart.pop(r)
        elif kind == "MOVE":
            a, b, owned = op[2:]
            need(chart.get(r) == a, "physical MOVE source")
            need(type(owned) is bool and owned == (r >= word["public"]), "physical ownership flag")
            need(spaces[a] < spaces[b] or owned and spaces[b] < spaces[a], "proper nested complete charts")
            chart[r] = b
            rank = abs(len(w["frames"][b]) - len(w["frames"][a]))
            moves_by_rank[rank] += 1
        elif kind == "SCALE":
            need(chart.get(r) == op[3] and F(op[2]) != 0, "nonzero SCALE at actual chart")
            state[r] = scaled(state[r], F(op[2]))
        elif kind in ("ADD", "COPY"):
            s, c, at = op[2:]
            need(r != s and chart.get(r) == chart.get(s) == at, "physical cochart arithmetic")
            if kind == "COPY":
                need(not state[r], "actual1880-input COPY guard")
            state[r] = add(state[r], state[s], F(c))
        else:
            raise ValueError("unknown physical instruction")
        peak = max(peak, len(chart) - word["public"])
        if t + 1 == word["marks"]["receiver_observation"]:
            need(state[HELPER] == selected_q and state[raw[DONOR]] == payload, "swap retains actual entire common row and sends pure private q")
            checkpoints["swap"] = "helper=q60; donor=actual h; all1880 input directions"
        if t + 1 == word["marks"]["common_completion"]:
            for r in range(1480):
                need(state[r] == add(expected[r], debt, pulse.get(r, F(0))), "complete dirty common endpoint identity")
            need(state[raw[DONOR]] == payload and state[q_cache] == selected_q, "both actual hub records retained through common completion")
            checkpoints["before_restoration"] = "common=T(u)+z(q60-h); donor=h; owned_return=q60"
        if t + 1 == word["marks"]["common_and_raw_restored"]:
            for r in range(1480):
                need(state[r] == expected[r], "all1480 common endpoints fully restored")
            for main, role in raw.items():
                want = {role: F(1), main: F(-1)}
                if main == RECEIVER:
                    want = add(want, selected_q)
                need(state[role] == want, "all400 raw endpoint identities")
            need(set(state) == set(range(1880)), "new owned record retired")
            checkpoints["after_restoration"] = "common=T(u); raw donor=q60; raw receiver=q213+q60; all other raw=q"
    for r in range(1480):
        need(state[r] == expected[r] and chart[r] == w["final"][r], "all final common fields exact")
    for main, role in raw.items():
        want = add(expected[main], {role: F(1), main: F(-1)})
        if main == RECEIVER:
            want = add(want, selected_q)
        need(state[role] == want and chart[role] == w["final"][main], "all recoupled private outputs and charts")
    need(len(state) == len(chart) == 1880, "all owned labels retired")
    return {
        "instructions": len(word["program"]),
        "opcode_counts": dict(sorted(counts.items())),
        "move_rank_histogram": dict(sorted(moves_by_rank.items())),
        "owned_lifetimes": lifetimes,
        "peak_owned": peak,
        "final_owned": 0,
        "checkpoints": checkpoints,
    }


def run(args):
    source_bytes = args.source.read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == PIN, "frozen source pin")
    w = json.loads(gzip.decompress(source_bytes))
    expected, payload, pulse, guards, offhub_payload = native_rows_and_pulse(w)
    word, raw, q_cache = build_word(w, pulse)
    bill = physical_replay(w, word, raw, q_cache, expected, payload, pulse)
    baseline = Counter(op[0] for op in w["program"])
    baseline["MOVE"] += 1710
    baseline["ADD"] += 800
    increment = {op: bill["opcode_counts"].get(op, 0) - baseline[op] for op in sorted(set(baseline) | set(bill["opcode_counts"]))}
    need(increment == {"ADD": len(pulse)+7, "CLEAR": 1, "COPY": 0, "INIT": 1, "MOVE": 1, "SCALE": 1}, "complete ordinary increment")
    q_row = {raw[DONOR]: F(1), DONOR: F(-1)}
    debt = add(q_row, payload, F(-1))
    witness = min(pulse)
    need(debt and pulse[witness] * debt[raw[DONOR]] != 0, "lost displaced-record mutant has nonzero private response")
    need(pulse[witness] * q_row[raw[DONOR]] != 0, "missing returned-q mutant has nonzero private response")
    common_witness = min(payload)
    need(-2 * pulse[witness] * payload[common_witness] != 0, "wrong-sign retained-record mutant has nonzero common response")
    negatives = [
        {"mutation": "do not retain h in donor; later subtract the unchanged q donor from returned q", "remaining_error": "z(q60-h)", "output": witness, "input": raw[DONOR], "coefficient": str(pulse[witness])},
        {"mutation": "omit pure-q return and use zero instead", "remaining_error": "z q60", "output": witness, "input": raw[DONOR], "coefficient": str(pulse[witness])},
        {"mutation": "form A=q60+h instead of q60-h", "remaining_error": "-2 z h", "output": witness, "input": common_witness, "coefficient": str(-2 * pulse[witness] * payload[common_witness])},
        {"mutation": "omit receiver ADD", "remaining_error": "-q60 in desired receiver gain", "output": raw[RECEIVER], "input": raw[DONOR], "coefficient": "-1"},
    ]
    correction_port = w["live"].index(RECEIVER - 112)
    donor_port = w["live"].index(DONOR)
    dot_parity = (w["ports"][correction_port] & w["ports"][donor_port]).bit_count() % 2
    receipt = {
        "schema": "moonshot-reversible-neutral-helper-swap-v1",
        "status": "PASS_ACTUAL1880_INPUT_REVERSIBLE_COUPLING_WITH_ONE_NEW_RANK1_RETURN",
        "source_sha256": PIN,
        "source_event": EVENT,
        "donor": DONOR,
        "receiver": RECEIVER,
        "helper": HELPER,
        "helper_route": [SOURCE_CHART, ARRIVAL_CHART],
        "helper_route_rank": len(w["frames"][ARRIVAL_CHART])-len(w["frames"][SOURCE_CHART]),
        "new_owned_q_return": {"source": ARRIVAL_CHART, "target": HUB, "rank": 1, "payload": "q60"},
        "raw_donor_route": [[t, op[2], op[3]] for t, op in enumerate(w["program"]) if op[:2] == ["MOVE", DONOR]],
        "raw_receiver_route": [[t, op[2], op[3]] for t, op in enumerate(w["program"]) if op[:2] == ["MOVE", RECEIVER]],
        "actual_displaced_common_row": encoded(payload),
        "neutral_hub_response": encoded(pulse),
        "displaced_common_support": len(payload),
        "displaced_payload_offhub_terminal_coefficients": encoded(offhub_payload),
        "neutral_hub_response_support": len(pulse),
        "offhub_response_support": 0,
        "copy_guards": guards,
        "receiver_gain": "1",
        "donor_receiver_E8_binary_dot_parity": dot_parity,
        "all1480_common_inputs_retained": True,
        "all400_private_inputs_retained": True,
        "all1710_original_raw_reservations_consumed_once": True,
        "all400_entry_and_final_recouplings_charged": True,
        "original_common_word_order_unchanged": True,
        "original_separate_second_owned_routes_borrowed": 0,
        "bill": bill,
        "added_ordinary_over_common_plus_raw_route_and_boundary_baseline": increment,
        "added_complete_recursive_calls": {"rank1": 1},
        "added_recursive_moment_at_t199over200": "1",
        "negative_controls": negatives,
        "scope": "An actual source-bound cross-coordinate side-information coupling with full common restoration and raw retention. The other required private-native endpoint changes remain open; the receiver gets q60, not its own paired q101. No new kappa or supplier theorem.",
        "new_complete_kappa": None,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "RESULT.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    word_bytes = (json.dumps(word, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (args.output / "SWAP-WORD.json.gz").write_bytes(gzip.compress(word_bytes, mtime=0))
    (args.output / "WORD-PIN.json").write_text(json.dumps({"decompressed_sha256": hashlib.sha256(word_bytes).hexdigest(), "instructions": len(word["program"])}, indent=2) + "\n")
    print(json.dumps({key: value for key, value in receipt.items() if key not in ("actual_displaced_common_row", "neutral_hub_response")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args())
