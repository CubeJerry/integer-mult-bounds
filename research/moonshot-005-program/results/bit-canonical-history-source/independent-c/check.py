#!/usr/bin/env python3
"""Independent literal replay of the changed-code canonical-history source."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ENGINE_PIN = "e754c182eff8604205e2cd9b8075e1186adfff5c024f4e3bcc009453454e0e74"
WORD_PIN = "1da8ac07063da93aaf002fa6feeb6de4ec1aa327a7740f3f61747abd559d14d0"
CODE_PIN = "bf797489826e125716cc368fb87219e3edf19028ea83b93e389b6182c57f408f"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--word", type=Path, required=True)
    parser.add_argument("--snapshots", type=Path, required=True)
    parser.add_argument("--code", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    engine_path = Path(__file__).with_name("retained") / "source_history_engine.py"
    assert hashlib.sha256(engine_path.read_bytes()).hexdigest() == ENGINE_PIN
    spec = importlib.util.spec_from_file_location("independent_source_history_engine", engine_path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    raw = args.word.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == WORD_PIN
    word = json.loads(raw)
    code_bytes = args.code.read_bytes()
    assert hashlib.sha256(code_bytes).hexdigest() == CODE_PIN
    code = json.loads(code_bytes)
    U = [int(row, 16) for row in code["active_six_rows_hex"] + code["canonical_pair_hex"]]
    source_bytes = (args.repo / word["source_path"]).read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == word["source_sha256"] == code["native_source_sha256"]
    roots = json.loads(source_bytes)["native_roots"]
    run = engine.replay(word, roots, U, 15, invoice=False)
    assert run["count"] == {"INIT": 71, "ADD": 730, "MOVE": 381, "CLEAR": 71}
    assert run["profile"] == {1: 58, 2: 63, 3: 30, 4: 30, 5: 74, 6: 20, 7: 105, 8: 1}
    assert run["dirty_CLEAR"] == 71
    reported_bytes = args.snapshots.read_bytes()
    reported = json.loads(reported_bytes)
    assert run["snapshots"] == reported and len(reported) == 159
    observations = [int(s["row_hex"], 16) for s in reported]
    rank = lambda rows: len(engine.basis(rows))
    dot = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    binary_frame = [0, 1, 2, 4, 8, 14, 30, 59]
    gram = [sum(int(i != j and dot(i, j) != 0) << k for k, j in enumerate(binary_frame)) for i in binary_frame]
    labels = [engine.solve(gram, sum(int(i != j and dot(i, j) != 0) << k for k, i in enumerate(binary_frame))) for j in range(111)]
    h = [(label & 189).bit_count() % 2 for label in labels]
    assert h == word["singular_h"]
    C9 = [(1 << i) | sum(1 << j for j in range(111) if dot(i, j) == 0) for i in range(111)]
    W15 = [C9[i] & sum(1 << j for j in range(111) if h[j] == h[i]) for i in range(111)]
    assert rank(C9) == 9 and rank(W15) == 15 and rank(C9 + W15) == 16
    assert rank(observations) == rank(observations + C9 + W15) == 66
    C = run["C"]
    seed = run["cuts"]["seed"]
    values, charts = seed["values"], seed["charts"]
    proper = [values[n] for n in values if charts[n] != "Hub" and not n.startswith("Y")]
    assert rank(proper) == 70
    assert rank(proper + C9 + W15) == 70
    nuisance = proper + [values[f"Y{i}"] for i in range(111)]
    assert rank(nuisance) + 16 - rank(nuisance + C9 + W15) == 16
    filters = [int(m["row_hex"], 16) for m in word["history_cache_metadata"]]
    assert len(filters) == rank(filters) == 52
    assert rank(U + filters) == 59 and rank(U + filters + C9 + W15) == 59
    filter_witnesses = []
    for metadata in word["history_cache_metadata"]:
        name = metadata["name"]
        assert values[name] == int(metadata["row_hex"], 16) and charts[name] == metadata["chart"]
        pairs = []
        for k, before in enumerate(reported[:-1]):
            after = reported[k + 1]
            if before["phase"] == "before" and after["phase"] == "after" and before["step"] == after["step"]:
                op = word["operations"][before["step"] - 1]
                if op[0] == "ADD" and op[1] == name:
                    assert int(before["row_hex"], 16) ^ int(after["row_hex"], 16) == values[name]
                    pairs.append([k, k + 1])
        assert len(pairs) == 1
        filter_witnesses.append({"cache": name, "observation_pair": pairs[0]})
    available, fitting, access = [], [], []
    ground = [values[n] for n in values if charts[n] == "zero" and not n.startswith("Y")]
    for i in range(111):
        facet = C[f"F{i}"]
        visible = [values[n] for n in values if not n.startswith("Y") and engine.contained(C[charts[n]], facet)]
        visible += [row for row, snap in zip(observations, reported) if engine.contained(C[snap["chart"]], facet)]
        hit = engine.solve(visible, 1 << i) is not None
        if hit:
            available.append(i)
        local = [1 << j for j in range(111) if dot(i, j) == 0]
        fit = engine.solve(ground + local, 1 << i) is not None
        if fit:
            fitting.append(i)
        access.append({"receiver": i, "visible_rank": rank(visible), "visible_target": hit, "ground_fitting": fit})
    assert available == sorted(word["targets"])
    assert fitting == code["optional_point_set"]
    predicates = [
        ("new_X8_filter_capture", lambda o: o[0] == "ADD" and o[1] == "X8" and o[2].startswith("Hnew")),
        ("new_displaced_filter_query", lambda o: o[0] == "ADD" and o[1].startswith("Hnew") and o[2].startswith("P")),
        ("new_filter_retirement", lambda o: o[0] == "CLEAR" and o[1].startswith("Hnew")),
        ("old_filtered_capture", lambda o: o[0] == "ADD" and o[2] == "H0_0"),
        ("early_point_capture", lambda o: o == ["ADD", "X1", "E1"]),
        ("held_seed_query", lambda o: o[0] == "ADD" and o[1] == "X21" and o[2].startswith("P")),
        ("paired_donor_production", lambda o: o == ["ADD", "X10", "X1"]),
        ("paired_donor_mask", lambda o: o == ["ADD", "E1", "Y21"]),
        ("structural_cache_retirement", lambda o: o == ["CLEAR", "Q0"]),
    ]
    rejected = []
    for name, predicate in predicates:
        indices = [i for i, op in enumerate(word["operations"]) if predicate(op)]
        assert indices, name
        mutant = engine.delete(word, indices[0])
        try:
            engine.replay(mutant, roots, U, 15, invoice=False)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("accepted semantic mutant " + name)
    result = {
        "status": "PASS_INDEPENDENT_CHANGED_CODE_CANONICAL_HISTORY_REVIEW",
        "word_sha256": WORD_PIN,
        "native_source_sha256": word["source_sha256"],
        "own_retained_interpreter_sha256": ENGINE_PIN,
        "changed_code_source_sha256": CODE_PIN,
        "reported_snapshot_sha256": hashlib.sha256(reported_bytes).hexdigest(),
        "columns": 222,
        "counts": run["count"],
        "movement_profile": run["profile"],
        "dirty_CLEAR": 71,
        "actual_principal_observations": 159,
        "actual_history_rank": 66,
        "W15_contained": True,
        "C9_contained": True,
        "live_proper_inventory_rank": 70,
        "joint_W_C_rank": 16,
        "joint_W_C_intersection_with_Y_nuisance": 16,
        "filter_rank": 52,
        "ground_U_plus_filter_rank": 59,
        "all_111_W_witnesses": [hex(engine.solve(observations, row)) for row in W15],
        "all_111_C_witnesses": [hex(engine.solve(observations, row)) for row in C9],
        "filter_difference_witnesses": filter_witnesses,
        "optimistically_visible_completed_receivers": available,
        "ground_fitting_receivers": fitting,
        "access": access,
        "negative_controls": rejected,
        "negative_controls_disable_invoice_and_source_cut_metadata": True,
        "scope": "Actual principal observations at actual charts plus simultaneous actual fields; arbitrary incompatible receiver order generously ignored; no extra original-history captures or transports; no new kappa",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "columns", "counts", "actual_principal_observations", "actual_history_rank", "W15_contained", "C9_contained", "negative_controls"]}))


if __name__ == "__main__":
    main()
