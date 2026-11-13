#!/usr/bin/env python3
"""Finite semantic fixtures; not a selected compiler or a free runtime scan.

Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def transition(state, destination):
    need(state["owner"] == destination["owner"] and state["live"] and destination["live"],
         "same live owner")
    for k in ("format", "heads", "backing", "occurrence_descriptor"):
        need(state[k] == destination[k], "identical " + k)
    need(state["zero_evidence"] == "actual_stored_canonical_zero", "stored-zero evidence")
    need(all(v == 0 for v in state["payload"]), "fixture rejects forged zero evidence")
    out = deepcopy(state)
    out["frame"] = destination["frame"]
    need(out["payload"] == state["payload"], "identity payload trace")
    return out


def run():
    sources = json.loads((HERE / "SOURCES.json").read_bytes())
    for item in sources["inputs"]:
        need(sha256(Path(item["local"]).read_bytes()).hexdigest() == item["sha256"], "pinned input " + item["local"])
    state = {"owner": 885, "live": True, "frame": 3,
             "format": {"width": 16, "quantum": "1/256", "layout": "signed-real-imag-pairs",
                        "volume": 8, "selected_root_factor": 9},
             "heads": [7, 11], "backing": "same-owned-record-885",
             "occurrence_descriptor": {"path": [2, 1], "order": [0, 1, 2], "return": [2, 1, 0]},
             "payload": [0]*8, "zero_evidence": "actual_stored_canonical_zero"}
    destination = deepcopy(state)
    destination["frame"] = 189
    result = transition(state, destination)
    need(result["frame"] == 189 and result["owner"] == 885, "public positive fixture")
    ideal, old_error = [3, -5, 0, 7], [2, -3, 1, -4]
    stored = [v+e for v, e in zip(ideal, old_error)]
    snapshot = stored.copy()
    need(any(old_error) and [v-w for v, w in zip(stored, snapshot)] == [0]*4,
         "correlated stored-error cancellation")
    wrong = stored.copy()
    wrong[0] += 1
    need(any(v-w for v, w in zip(wrong, snapshot)), "intervening write invalidates cancellation")
    rejects = []
    variants = [
        ("nonzero payload", "payload", [1]+[0]*7),
        ("ideal-only zero with retained residual", "zero_evidence", "ideal_zero_only"),
        ("different owner", "owner", 886),
        ("implicit owner freeing", "live", False),
        ("changed heads", "heads", [8, 11]),
        ("changed backing", "backing", "other-record"),
        ("changed occurrence descriptor", "occurrence_descriptor", {"path": [2, 2]}),
    ]
    for label, key, value in variants:
        a, b = deepcopy(state), deepcopy(destination)
        if key in ("payload", "zero_evidence"):
            a[key] = value
        else:
            b[key] = value
        try:
            transition(a, b)
        except ValueError as e:
            rejects.append({"control": label, "rejected": True, "reason": str(e)})
        else:
            raise ValueError("invalid identity admitted: " + label)
    for key, value in (("width", 17), ("quantum", "1/512"), ("volume", 9),
                       ("layout", "different-permutation"), ("selected_root_factor", 8)):
        b = deepcopy(destination)
        b["format"][key] = value
        try:
            transition(state, b)
        except ValueError as e:
            rejects.append({"control": "different " + key, "rejected": True, "reason": str(e)})
        else:
            raise ValueError("format mutation admitted: " + key)
    compiler = HERE / "inputs/selected-clifford-exact.py"
    spec = importlib.util.spec_from_file_location("zero_rule_clifford", compiler)
    c = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = c
    spec.loader.exec_module(c)
    root = HERE.parents[1]
    import gzip
    raw = (root / "reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(raw).hexdigest() == sources["actual7481_word_sha256"], "actual source word")
    word = json.loads(gzip.decompress(raw))
    op = c.canonical_frame(9, word["frames"][3]).adjoint().then(c.canonical_frame(9, word["frames"][189]))
    recipe, rebuilt = c.lower_child(op)
    need(recipe["rank"] == 8 and rebuilt.tab == op.tab and rebuilt.zero_state() == op.zero_state(), "actual signed/phase rank8 interface")
    basis_zero = ([(1, 0)]+[(0, 0)]*511, 0)
    need(op.zero_state() != basis_zero, "identity is wrong on a nonzero basis input")
    return {"status": "PASS_CONDITIONAL_ZERO_CONTINUATION_FIXTURES",
            "authenticated_inputs": len(sources["inputs"]), "public_same_owner_identity": True,
            "correlated_previous_error_cancelled_exactly": True,
            "intervening_write_cancellation_control": True,
            "rejections": rejects, "actual_nonzero_interface_rank": 8,
            "actual_nonzero_interface_not_identity": True,
            "selected_public_zero_opcode_admitted": False,
            "selected_descriptor_join_or_numeric_tariff_proved": False}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "rejected_controls": len(result["rejections"])}))
