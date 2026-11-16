#!/usr/bin/env python3
"""Literal source, formal main-cell, and full nonlocal-ledger verification."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

WORD_PIN = "1560ba7586802dac2393d8e2c6ed2aa0df54d712bad6ef8296789fe9da527cfe"
ENGINE_PIN = "e754c182eff8604205e2cd9b8075e1186adfff5c024f4e3bcc009453454e0e74"


def through_matrix(word, charts, chart, packets):
    """Other chart arrivals are formal independent boundary inputs."""
    target = charts[chart]
    positions = {f"X{i}": f"L{i}" for i in range(111)} | {f"Y{i}": "zero" for i in range(111)}
    coeff = {n: 0 for n in positions}
    arrivals = {n: 0 for n in packets}
    departures = {}
    for op in word["operations"]:
        if op[0] == "INIT":
            _, n, c = op
            positions[n] = c
            coeff[n] = 0
        elif op[0] == "MOVE":
            _, n, c = op
            before, after = charts[positions[n]] == target, charts[c] == target
            if before and not after and n in packets:
                departures[n] = coeff[n]
            if after and not before:
                coeff[n] = 1 << packets.index(n) if n in packets else 0
                if n in packets:
                    arrivals[n] += 1
            positions[n] = c
        elif op[0] == "ADD":
            _, s, t = op
            if charts[positions[t]] == target:
                assert charts[positions[s]] == target
                coeff[t] ^= coeff[s]
        elif op[0] == "CLEAR":
            positions.pop(op[1])
            coeff.pop(op[1])
    assert all(count == 1 for count in arrivals.values())
    return [departures[n] for n in packets]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    own_engine = Path(__file__).with_name("retained") / "source_history_engine.py"
    assert hashlib.sha256(own_engine.read_bytes()).hexdigest() == ENGINE_PIN
    spec = importlib.util.spec_from_file_location("retained_independent_engine", own_engine)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    word_bytes = (args.out / "WORD.json").read_bytes()
    assert hashlib.sha256(word_bytes).hexdigest() == WORD_PIN
    word = json.loads(word_bytes)
    source_bytes = (args.repo / word["source_path"]).read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == word["source_sha256"]
    roots = json.loads(source_bytes)["native_roots"]
    seeds = [int(v, 16) for v in word["seed_rows_hex"]]
    run = engine.replay(word, roots, seeds, 15, invoice=False)
    rank = lambda rows: len(engine.basis(rows))
    assert run["count"] == {"INIT": 75, "ADD": 748, "MOVE": 391, "CLEAR": 75}
    assert run["profile"] == {1: 67, 2: 63, 3: 39, 4: 24, 5: 73, 6: 20, 7: 104, 8: 1}
    assert run["dirty_CLEAR"] == 75
    charts = run["C"]
    values = run["cuts"]["seed"]["values"]
    positions = run["cuts"]["seed"]["charts"]
    h = int(word["double_retention"]["second_value_hex"], 16)
    a3 = int(word["double_retention"]["first_value_hex"], 16)
    assert values["KEEP_C0"] == a3 and values["KEEP_L7"] == h
    assert values["P0"] == values["EARLY7"] == 1 << 7
    assert values["CORR16"] == h ^ (1 << 16)
    assert h == values["H1_0"] ^ values["Q0"]
    assert len(charts["C0"]) == 5 and len(charts["J16"]) == 4
    assert engine.contained(charts["L7"], charts["J16"])
    assert engine.contained(charts["J16"], charts["C0"])
    assert engine.contained(charts["J16"], charts["F16"])
    assert not engine.contained(charts["L16"], charts["L7"])
    assert len(engine.rref([roots[i] for i in range(111) if h >> i & 1])) == 5
    matrices = {"C0": through_matrix(word, charts, "C0", ["P0", "P1", "P2"]),
                "L7": through_matrix(word, charts, "L7", ["P0"])}
    assert matrices == {"C0": [0, 2, 4], "L7": [0]}
    observations = [int(s["row_hex"], 16) for s in run["snapshots"]]
    assert len(observations) == 170 and rank(observations) == 68
    dot = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    canonical = [(1 << i) | sum(1 << j for j in range(111) if dot(i, j) == 0) for i in range(111)]
    hh = word["singular_h"]
    singular = [canonical[i] & sum(1 << j for j in range(111) if hh[j] == hh[i]) for i in range(111)]
    assert rank(singular) == 15 and rank(canonical) == 9
    assert rank(observations + singular + canonical) == 68
    ground_names = [n for n in values if positions[n] == "zero" and not n.startswith("Y")]
    ground = [values[n] for n in ground_names]
    nonlocal_names = []
    for name, row in values.items():
        if positions[name] in ["zero", "Hub"] or name.startswith("Y"):
            continue
        if any(row >> j & 1 and not engine.contained(charts[f"L{j}"], charts[positions[name]]) for j in range(111)):
            nonlocal_names.append(name)
    assert sorted(nonlocal_names) == ["KEEP_C0", "KEEP_L7", "Q1", "Q3", "Q4"]
    normalized = ground + [values[n] for n in nonlocal_names]
    assert rank(ground) == 14 and rank(normalized) == 19
    y_rows = [values[f"Y{i}"] for i in range(111)]
    assert rank(normalized + y_rows) == 19 + 111
    fits, invisible, visible, access = [], [], [], []
    for i in range(111):
        facet = charts[f"F{i}"]
        located = [n for n in nonlocal_names if engine.contained(charts[positions[n]], facet)]
        local = [1 << j for j in range(111) if dot(i, j) == 0]
        have = ground + [values[n] for n in located]
        fit = engine.solve(have + local, 1 << i) is not None
        if fit:
            fits.append(i)
        if not located:
            invisible.append(i)
        stock = [values[n] for n in values if not n.startswith("Y") and engine.contained(charts[positions[n]], facet)]
        stock += [row for row, snap in zip(observations, run["snapshots"]) if engine.contained(charts[snap["chart"]], facet)]
        hit = engine.solve(stock, 1 << i) is not None
        if hit:
            visible.append(i)
        access.append({"receiver": i, "available_nonlocal_fields": located, "raw_local_fitting": fit, "actual_stock_and_observation_visible": hit})
    assert len(fits) == 21 and len(invisible) == 51
    assert visible == word["targets"]
    allmask = (1 << 111) - 1
    early_mask = sum(1 << i for i in word["point_targets"])
    first_puncture = allmask ^ (early_mask | (1 << 7))
    strong_puncture = allmask ^ (early_mask | h)
    partial_rank = rank(row & first_puncture for row in seeds + [a3, h])
    first_full_rank = rank(row & first_puncture for row in normalized)
    omitted_channels_rank = rank(row & strong_puncture for row in seeds + [a3, h])
    full_rank = rank(row & strong_puncture for row in normalized)
    assert (partial_rank, first_full_rank, omitted_channels_rank, full_rank) == (9, 12, 8, 11)
    predicates = [
        ("first_retention_capture", lambda o: o == ["ADD", "P0", "KEEP_C0"]),
        ("first_actual_reset", lambda o: o == ["ADD", "KEEP_C0", "P0"]),
        ("second_retention_capture", lambda o: o == ["ADD", "P0", "KEEP_L7"]),
        ("second_actual_reset", lambda o: o == ["ADD", "KEEP_L7", "P0"]),
        ("early_raw_capture", lambda o: o == ["ADD", "X7", "EARLY7"]),
        ("real_correction_capture", lambda o: o == ["ADD", "X5", "CORR16"]),
        ("new_nonlocal_receiver_read", lambda o: o == ["ADD", "KEEP_L7", "Y16"]),
        ("new_local_receiver_correction", lambda o: o == ["ADD", "CORR16", "Y16"]),
        ("old_receiver_replacement_read", lambda o: o == ["ADD", "KEEP_C0", "Y3"]),
        ("new_owned_retirement", lambda o: o == ["CLEAR", "KEEP_L7"]),
    ]
    rejected = []
    for name, predicate in predicates:
        indices = [i for i, op in enumerate(word["operations"]) if predicate(op)]
        assert indices
        mutant = copy.deepcopy(word)
        mutant["operations"].pop(indices[0])
        mutant["milestones"] = {key: -1 for key in word["milestones"]}
        mutant.pop("source_cut", None)
        try:
            engine.replay(mutant, roots, seeds, 15, invoice=False)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("accepted semantic mutant " + name)
    result = {
        "status": "PASS_ACTUAL_TWO_RETENTION_SEVENTEEN_SOURCE",
        "word_sha256": WORD_PIN,
        "native_source_sha256": word["source_sha256"],
        "retained_engine_sha256": ENGINE_PIN,
        "input_columns": 222,
        "completed_targets": word["targets"],
        "counts": run["count"],
        "profile": run["profile"],
        "dirty_CLEAR": 75,
        "main_principal_through_rows": matrices,
        "proper_cell_nullities_per_record_width": {"C0": 1, "L7": 1},
        "retained_rows": {"KEEP_C0": hex(a3), "KEEP_L7": hex(h)},
        "history_observations": 170,
        "history_rank": 68,
        "W15_and_C9_contained_in_actual_history": True,
        "all111_W_witnesses": [hex(engine.solve(observations, row)) for row in singular],
        "all111_C_witnesses": [hex(engine.solve(observations, row)) for row in canonical],
        "ground_rank": 14,
        "proper_nonlocal_inventory": [{"name": n, "chart": positions[n], "row": hex(values[n])} for n in nonlocal_names],
        "full_normalized_rank": 19,
        "normalized_rank_with_all_original_Y_nuisance_columns": 130,
        "raw_local_relaxed_fitting_receivers": fits,
        "proper_nonlocal_inventory_invisible_receivers": invisible,
        "actual_stock_and_history_visible_receivers": visible,
        "access": access,
        "punctures": {"main_bank_plus_new_kernels_after_E6_and7": partial_rank,
                      "full_ledger_after_E6_and7": first_full_rank,
                      "incomplete_ledger_after_E6_and_h_support_NOT_A_GATE": omitted_channels_rank,
                      "full_ledger_after_E6_and_h_support": full_rank},
        "semantic_negative_controls": rejected,
        "negative_controls_disable_invoice_source_cut_and_all_milestones": True,
        "scope": "Fixed native two-cell source and exact tensor lift; all paid proper cache descents retained; no complete supplier or new kappa",
    }
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.out / "HISTORY-SNAPSHOTS.json").write_text(json.dumps(run["snapshots"], indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "counts", "history_rank", "full_normalized_rank", "raw_local_relaxed_fitting_receivers", "semantic_negative_controls"]}))


if __name__ == "__main__":
    main()
