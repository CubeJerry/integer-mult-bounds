#!/usr/bin/env python3
"""Check odd-parity half-slack quotient flow and complete-neighborhood receipts."""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parent
SWEEP_PATH = ROOT / "sweep.py"
RESULT_PATH = ROOT / "RESULT.json"
sweep = ModuleType("odd_parity_half_sweep")
sweep.__file__ = str(SWEEP_PATH)
exec(compile(SWEEP_PATH.read_bytes(), str(SWEEP_PATH), "exec"), sweep.__dict__)


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def decode_key(value):
    pattern, sign = value
    return tuple(pattern), sign


def verify_flow(data, record):
    cert = record["flow_certificate"]
    inputs = data["inputs"]
    outputs = data["outputs"]
    source = cert["input_supplies"]
    sink = cert["output_loads"]
    require(len(source) == len(inputs), "input supplies have wrong length")
    require(len(sink) == len(outputs), "output loads have wrong length")
    require(all(0 <= value <= inputs[i]["capacity"]
                for i, value in enumerate(source)),
            "input supply violates orbit capacity")
    require(all(0 <= value <= outputs[j]["capacity"]
                for j, value in enumerate(sink)),
            "output load violates orbit capacity")
    active = set(data["quotient_edges"])
    rows = [0] * len(inputs)
    columns = [0] * len(outputs)
    seen = set()
    for triple in cert["positive_orbit_pair_flows"]:
        require(len(triple) == 3, "malformed orbit-pair flow")
        i, j, amount = triple
        require(isinstance(i, int) and 0 <= i < len(inputs),
                "input orbit index out of range")
        require(isinstance(j, int) and 0 <= j < len(outputs),
                "output orbit index out of range")
        require(isinstance(amount, int) and amount > 0,
                "flow amount must be positive")
        require((i, j) in active, "flow uses a nonexistent orbit adjacency")
        require((i, j) not in seen, "duplicate orbit-pair flow")
        seen.add((i, j))
        rows[i] += amount
        columns[j] += amount
    require(rows == source, "input-orbit flow conservation fails")
    require(columns == sink, "output-orbit flow conservation fails")
    value = sum(source)
    require(value == sum(sink) == record["max_flow"],
            "total flow values disagree")
    require(record["feasible"] == (value == data["input_count"]),
            "saturation status disagrees")
    if record["feasible"]:
        require(source == [orbit["capacity"] for orbit in inputs],
                "a feasible flow does not saturate all inputs")
    return value


def verify_cut(data, record):
    cut = record["hall_cut"]
    input_index = {orbit["key"]: i for i, orbit in enumerate(data["inputs"])}
    output_index = {orbit["key"]: j for j, orbit in enumerate(data["outputs"])}
    source_keys = {decode_key(item["key"]) for item in cut["input_orbits"]}
    neighbor_keys = {decode_key(item["key"]) for item in cut["neighbor_orbits"]}
    require(source_keys <= set(input_index), "cut has unknown input orbit")
    require(neighbor_keys <= set(output_index), "cut has unknown output orbit")
    source = {input_index[key] for key in source_keys}
    neighbors = {output_index[key] for key in neighbor_keys}
    exact_neighbors = {j for i, j in data["quotient_edges"] if i in source}
    require(neighbors == exact_neighbors,
            "stored output set is not the complete neighborhood")
    input_mass = sum(data["inputs"][i]["capacity"] for i in source)
    neighbor_mass = sum(data["outputs"][j]["capacity"] for j in neighbors)
    require(input_mass == cut["input_capacity"], "cut input mass disagrees")
    require(neighbor_mass == cut["neighbor_capacity"],
            "cut neighbor mass disagrees")
    require(input_mass - neighbor_mass == cut["deficiency"],
            "Hall deficiency disagrees")
    require(data["input_count"] - (input_mass - neighbor_mass)
            == record["max_flow"],
            "cut deficiency does not match the recorded flow")
    return input_mass, neighbor_mass


def verify_record(record):
    data = sweep.prepare_radius(record["radius"])
    require(record["domain"]["input_count"] == data["input_count"],
            "input count disagrees")
    require(record["domain"]["input_orbit_count"] == data["input_orbit_count"],
            "input orbit count disagrees")
    require(record["domain"]["all_corner_output_count"] ==
            data["all_corner_output_count"], "corner output count disagrees")
    require(record["domain"]["accepted_output_count"] ==
            data["accepted_output_count"], "accepted output count disagrees")
    require(record["domain"]["quotient_adjacencies"] ==
            len(data["quotient_edges"]), "quotient edge count disagrees")
    for name, actual in (
        ("input_orbit_capacities", data["inputs"]),
        ("accepted_output_orbit_capacities", data["outputs"]),
    ):
        saved = record[name]
        require(len(saved) == len(actual), name + " length disagrees")
        for item, orbit in zip(saved, actual):
            require(decode_key(item["key"]) == orbit["key"],
                    name + " key ordering disagrees")
            require(item["capacity"] == orbit["capacity"],
                    name + " capacity disagrees")
    flow = verify_flow(data, record)
    t_mass, n_mass = verify_cut(data, record)
    return {
        "radius": record["radius"],
        "inputs": data["input_count"],
        "flow": flow,
        "feasible": record["feasible"],
        "hall_deficiency": t_mass - n_mass,
    }


def expect_rejection(thunk, label):
    try:
        thunk()
    except VerificationError:
        return
    raise VerificationError("negative control accepted: " + label)


def negative_controls(record):
    data = sweep.prepare_radius(record["radius"])
    flow_mutant = json.loads(json.dumps(record))
    flow_mutant["flow_certificate"]["positive_orbit_pair_flows"][0][2] += 1
    expect_rejection(lambda: verify_flow(data, flow_mutant), "incremented flow")

    cut_mutant = json.loads(json.dumps(record))
    cut_mutant["hall_cut"]["neighbor_orbits"].pop()
    expect_rejection(lambda: verify_cut(data, cut_mutant), "deleted neighbor orbit")


def main():
    receipt = json.loads(RESULT_PATH.read_text())
    require(receipt["scope"] ==
            "only odd-parity inputs, odd-parity outputs, radii 5, 9, 11, error cap one",
            "scope changed")
    require(sweep.graph_group_check()["paired_group_order"] == 192,
            "paired W(D4) group check changed")
    records = receipt["completed_radii"]
    require([record["radius"] for record in records] == [5, 9, 11],
            "the finite gate must contain exactly R=5,9,11")
    reports = [verify_record(record) for record in records]
    for record in records:
        negative_controls(record)
    print(json.dumps({
        "status": "PASS",
        "verified": reports,
        "negative_controls": [
            "incremented positive flow rejected",
            "deleted complete-neighborhood orbit rejected",
        ],
        "untouched_radii": receipt["untouched_radii"],
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
