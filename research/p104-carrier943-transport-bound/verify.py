#!/usr/bin/env python3
"""Portable read-only polynomial separator and directed budget replay.

Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run():
    source_manifest = json.loads((HERE / "SOURCES.json").read_bytes())
    prefix = "research/p104-carrier943-transport-bound/"
    for item in source_manifest["bundled_external_inputs"]:
        need(item["path"].startswith(prefix), "local bundled path")
        path = HERE / item["path"][len(prefix):]
        need(sha256(path.read_bytes()).hexdigest() == item["sha256"], "bundled input pin: " + path.name)
    core = load_module("carrier943_independent", HERE / "independent.py")
    word, dual, compiler = (HERE / "inputs" / f for f in ("WORD.json.gz", "SEPARATOR.json", "clifford_exact.py"))
    result = core.verify(word, dual, compiler)
    geometry = result.pop("geometry")
    observations = result["direct_replay"].pop("observations")
    positive_ids = result.pop("positive_cheap_actual_frame_IDs")
    result["positive_cheap_actual_frame_IDs_sha256"] = digest(positive_ids)
    result["complete_actual_geometry_sha256"] = digest(geometry)
    result["strict_observation_records_sha256"] = digest(observations)
    result["strict_observation_count"] = len(observations)
    controls = []
    original_read = Path.read_bytes
    for path, reason in ((word, "exact source pin"), (compiler, "actual frame constructor pin")):
        original = original_read(path)
        mutated = bytes([original[0] ^ 1]) + original[1:]

        def fake_read(self, selected=path, replacement=mutated):
            return replacement if self.resolve() == selected.resolve() else original_read(self)

        Path.read_bytes = fake_read
        try:
            core.verify(word, dual, compiler)
        except ValueError as error:
            need(str(error) == reason, "expected source-mutation rejection")
            controls.append({"input": path.name, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("source mutation accepted")
        finally:
            Path.read_bytes = original_read
    price = load_module("carrier943_exact_budget", HERE / "inputs/budget_price.py")
    invoice_raw = (HERE / "inputs/CURRENT-PRICE.json").read_bytes()
    need(sha256(invoice_raw).hexdigest() == price.PIN, "complete signed invoice pin")
    invoice = json.loads(invoice_raw)
    payload = json.loads(gzip.decompress(word.read_bytes()))
    need(digest(payload) == invoice["new_native"], "invoice binds actual canonical native payload")
    target, paid = invoice["after"]["T"], invoice["after"]["P"]
    signed = {r: target.get(r, 0)-paid.get(r, 0) for r in target.keys() | paid.keys()}
    need(price.moment(signed, Q(0)) == (1424, 1424), "complete linear-surplus control")
    kappa = Q(38, 10000)
    baseline = price.moment(signed, kappa)
    f8, f4 = price.price(8, kappa), price.price(4, kappa)
    residual = (f8[0]-1+baseline[0]/17, f8[1]-1+baseline[1]/17)
    after = (baseline[0]+17*(f8[0]-1-f4[1]), baseline[1]+17*(f8[1]-1-f4[0]))
    need(f4[0] > residual[1] and after[1] < 0, "rank4 exceeds complete.0038 residual")
    result["source_mutation_controls"] = controls
    result["budget"] = {"kappa": "0.0038", "calls": 17,
                        "baseline": price.display(baseline),
                        "all_new_native_cost_ceiling": price.display(residual),
                        "minimum_rank4_network_cost": price.display(f4),
                        "rank4_optimistic_complete_moment": price.display(after)}
    result["status"] = "PASS_P104_CARRIER943_TRANSPORT_BOUND"
    expected = HERE / "EXPECTED.json"
    if expected.exists():
        need(json.loads(json.dumps(result)) == json.loads(expected.read_bytes()), "complete compact deterministic receipt")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = run()
    if args.out is not None:
        args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    print(json.dumps(result, sort_keys=True, indent=2))
