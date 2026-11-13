#!/usr/bin/env python3
"""Read-only source replay for the fixed-history 40710 preparation barrier.

This does not emit a native word or admit a zero-reframe instruction.
Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
WORD = ROOT / "reference/pr7481/WORD.json.gz"
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
COMPILER = ROOT / "worker-a/selected/frozen/clifford_exact.py"
COMPILER_PIN = "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def operands(event):
    return event[1:3] if event[0] in ("ADD", "COPY") else event[1:2]


def barrier(word, cut=40710):
    need(word["program"][cut] == ["MOVE", 885, 3, 189, False], "candidate event")
    need(word["initial"][885] == 3 and word["frames"][3] == [], "empty entrance of 885")
    need(word["initial"][1459] == 189 and len(word["frames"][189]) == 8,
         "demoted helper requires destination frame")
    need(len(word["frames"][word["final"][1459]]) == 9, "lost rank-one helper target")
    prefix = word["program"][:cut]
    touches = {r: [(i, e) for i, e in enumerate(prefix) if r in operands(e)]
               for r in (885, 1459)}
    need(touches[885] == [(30780, ["ADD", 885, 943, "1/2", 3])],
         "885 is never read or transported before candidate")
    need(not touches[1459], "1459 has no earlier original computation")

    # An exact normalized scalar native replay. The nonzero probe satisfies
    # -x1459-x705+x885=0; the original demoted entrance value is then excluded
    # from free available history. Nothing else is assumed to be zero in the
    # claimed algorithm: one valid probe is enough for a dependency obstruction.
    cur = list(word["initial"]) + [None] * word["owned_fields"]
    values = [Q(0)] * len(cur)
    values[885] = values[1459] = Q(1)
    max_support = 2
    for i, e in enumerate(prefix):
        op, r = e[:2]
        if op == "INIT":
            need(cur[r] is None, "INIT active")
            cur[r], values[r] = e[2], Q(0)
        elif op == "CLEAR":
            need(cur[r] == e[2], "CLEAR frame")
            cur[r], values[r] = None, Q(0)
        elif op == "MOVE":
            need(cur[r] == e[2], "MOVE frame")
            cur[r] = e[3]
        elif op == "SCALE":
            need(cur[r] == e[-1], "SCALE frame")
            values[r] *= Q(e[2])
        else:
            need(op in ("ADD", "COPY"), "known native instruction")
            s, q = e[2], Q(e[3])
            need(cur[r] == cur[s] == e[-1], "scalar common frame")
            values[r] = (values[r] if op == "ADD" else Q(0)) + q * values[s]
        need(all(v == 0 for j, v in enumerate(values) if j not in (885, 1459)),
             "probe escaped to an original carrier at event " + str(i))
        need(values[885] == values[1459] == 1, "probe values retained")
    need(cur[885] == 3 and cur[1459] == 189, "probe cut frames")
    return {
        "cut": cut, "instruction": word["program"][cut],
        "probe": {"885": "1", "1459": "1"},
        "relation_evaluation": "0",
        "prefix_events_checked": len(prefix),
        "nonzero_original_fields_at_every_prefix_cut": [885, 1459],
        "demoted_1459_is_not_free_backing": True,
        "available_nonzero_frame_after_removing_demoted_entrance": 3,
        "885_touches_before_cut": [{"event": i, "instruction": e} for i, e in touches[885]],
        "1459_touches_before_cut": [],
        "maximum_probe_support": max_support,
    }


def run():
    need(sha(WORD) == PIN, "word pin")
    need(sha(COMPILER) == COMPILER_PIN, "exact Clifford compiler pin")
    word = json.loads(gzip.decompress(WORD.read_bytes()))
    proof = barrier(word)
    compiler = module("public_cache_clifford", COMPILER)
    recipes = []
    for a, b, expected in ((3, 189, 8), (3, 105, 1), (105, 189, 7)):
        op = compiler.canonical_frame(9, word["frames"][a]).adjoint().then(
            compiler.canonical_frame(9, word["frames"][b]))
        recipe, rebuilt = compiler.lower_child(op)
        need(recipe["rank"] == expected, "actual paid child rank")
        need(op.tab == rebuilt.tab and op.zero_state() == rebuilt.zero_state(),
             "signed tableau and absolute phase")
        recipes.append({"source": a, "destination": b, "rank": expected,
                        "signed_tableau_equal": True, "absolute_phase_equal": True,
                        "recipe": recipe})
    budget = module("public_cache_budget", ROOT / "budget_price.py")
    raw = budget.INVOICE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == budget.PIN, "complete invoice pin")
    invoice = json.loads(raw)
    target, paid = invoice["after"]["T"], invoice["after"]["P"]
    signed = {r: target.get(r, 0)-paid.get(r, 0) for r in target.keys() | paid.keys()}
    native_hist = Counter()
    for e in word["program"]:
        if e[0] == "MOVE":
            native_hist[abs(len(word["frames"][e[3]])-len(word["frames"][e[2]]))] += 1
    records = []
    for text in ("0.00363005817", "0.003647081039689", "0.0038"):
        kappa = Q(text)
        before = budget.moment(signed, kappa)
        # Grant the best possible tariff f8 for supplying the compulsory path:
        # deleted f8 - lost f1 - new cost >=f8 is at most -f1=-1 per call.
        upper = (before[0]-17, before[1]-17)
        need(upper[1] < 0, "scoped optimistic complete moment fails")
        records.append({"kappa": text, "baseline": budget.display(before),
                        "fixed_history_optimistic_moment_upper": budget.display(upper)})
    controls = []
    for label, edit in (
        ("new_885_read_is_outside_fixed_history_scope", "read"),
        ("free_demoted_entrance_is_not_a_preparation", "entrance"),
    ):
        mutant = deepcopy(word)
        if edit == "read":
            mutant["program"].insert(30781, ["ADD", 943, 885, "1", 3])
            cut = 40711
        else:
            mutant["initial"][885] = 189
            cut = 40710
        try:
            barrier(mutant, cut)
        except ValueError as error:
            controls.append({"name": label, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("negative scope control accepted: " + label)
    return {
        "status": "PASS_SCOPED_FIXED_HISTORY_PREPARATION_OBSTRUCTION",
        "source_head": "89eaa9d8cae37c1540de98f2d29a3abaabb96a2b",
        "word_sha256": PIN, "word_payload_sha256": hashlib.sha256(
            json.dumps(word, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "compiler_sha256": COMPILER_PIN, "invoice_sha256": budget.PIN,
        "replay": proof, "actual_child_interfaces": recipes,
        "native_paid": dict(sorted(native_hist.items())),
        "full_calls": 17, "native_gain_upper": "-1", "budgets": records,
        "controls": controls,
        "scope": "Whole-field scalar ADD/COPY/SCALE and nested MOVE preparation; original carrier histories fixed; original demoted input is not free; ordinary/retag/cache/erasure granted free. Not a general multiplication lower bound or a changed-producer obstruction.",
        "physical_zero_reframe_admitted": False,
        "changed_native_word_emitted": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = run()
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "prefix_events_checked": 40710,
                      "native_gain_upper": result["native_gain_upper"],
                      "controls": len(result["controls"]),
                      "phase_checked_interfaces": len(result["actual_child_interfaces"])}))
