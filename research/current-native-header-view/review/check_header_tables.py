"""Source-aware independent review of the fixed nine-vector header producer.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
All integer/header decoding below is an observer, never production execution.
"""
import argparse
from dataclasses import replace
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table_machine import SCHEMA, Tape, decode, encode, execute, expected_view, require


def load_module(name, path):
    require(name not in sys.modules, "cold independent-review import")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def snapshot(package):
    names = ("header_view.py", "header_sources.py", "source_binding.py", "DEPENDENCIES.json")
    return {name: sha256((package / name).read_bytes()).hexdigest() for name in names}


def fixture(f, remainder, K=2, G=1):
    """Exact syntax/local-layout fixture; not a complete supplier admission.

    Full global precision/stock/carving/root-production contracts are not
    inferred from these observer-generated metadata values.
    """
    e = 145 * f + remainder
    d = e + 29
    H = d * G
    entry = 2 * H + 5
    active = entry + remainder * K
    back = entry + e * K + 11
    a = back + H + 7
    values = dict(outer=3, rows=6, stock=3, row_bits=60 << a, within_bits=a,
                  record_bits=60, p=max(4096, d), d=d, K=K, G=G, H=H,
                  q0=3, qF=4, qB=5, D=d, f=f, rho=K - 1,
                  active_start=active, back_start=back, selected_axes=e,
                  entry_start=entry, remainder=remainder, cutoff=145)
    require(values["active_start"] == values["entry_start"] + remainder * K,
            "ordinary source-derived active offset")
    require(0 <= remainder < 145 and e == 145 * f + remainder,
            "ordinary source division")
    require(entry >= 2 * H and entry + e * K <= back and back + H <= a,
            "complete local front/active/back/spectator layout")
    return values


def make_tapes(module, values, translated=0):
    tapes = [Tape(origin=translated + (7 * i) % 11) for i in range(40)]
    tapes[module.PARENT] = Tape(encode(values), origin=translated + 3, readonly=True)
    return tapes


def totals(tapes):
    return {op: sum(t.counts[op] for t in tapes) for op in ("read", "write", "move")}


def successful_call(module, values, tapes=None, translated=0):
    tapes = make_tapes(module, values, translated) if tapes is None else tapes
    original = encode(values)
    before = totals(tapes)
    prepared = execute(module.PREPARE, tapes)
    observed = tapes[module.VIEW].inspect()
    require(decode(observed) == expected_view(values), "all 23 independent header values")
    require(observed == encode(expected_view(values)), "exact canonical returned bytes")
    for i, tape in enumerate(tapes):
        tape.quiescent(original if i == module.PARENT else observed if i == module.VIEW else "")
    released = execute(module.RELEASE, tapes)
    for i, tape in enumerate(tapes):
        tape.quiescent(original if i == module.PARENT else "")
    after = totals(tapes)
    bill = {op: after[op] - before[op] for op in after}
    return tapes, dict(input_bits=len(original), output_bits=len(observed),
                       f=values["f"], remainder=values["remainder"], K=values["K"],
                       primitive_actions=bill, prepare_dispatches=sum(prepared.values()),
                       release_dispatches=sum(released.values()),
                       preserved_fields=20, changed_fields=["selected_axes", "entry_start", "remainder"])


def require_detection(action, label):
    try:
        action()
    except ValueError:
        return label
    raise ValueError("independent reviewer did not detect " + label)


def table_controls(module):
    controls = []
    values = fixture(2, 13)

    def wrong_multiplier():
        old = module.NATIVE_RANK
        try:
            module.NATIVE_RANK = 8
            mutated = module.compile_prepare()
        finally:
            module.NATIVE_RANK = old
        tapes = make_tapes(module, values)
        execute(mutated, tapes)
        require(decode(tapes[module.VIEW].inspect()) == expected_view(values),
                "wrong multiplier survived exact header oracle")

    controls.append(require_detection(wrong_multiplier, "compiled multiplier 8 instead of 9"))

    def wrong_entry():
        old = module.ROLES["active_start"]
        try:
            module.ROLES["active_start"] = module.ROLES["back_start"]
            mutated = module.compile_prepare()
        finally:
            module.ROLES["active_start"] = old
        tapes = make_tapes(module, values)
        execute(mutated, tapes)
        require(decode(tapes[module.VIEW].inspect()) == expected_view(values),
                "wrong entry origin survived exact header oracle")

    controls.append(require_detection(wrong_entry, "compiled entry copied from back_start"))

    def missing_retirement():
        mutated = list(module.RELEASE)
        index = next(i for i, row in enumerate(mutated) if row == ("write", module.VIEW, "_"))
        mutated[index] = ("write", module.VIEW, "0")
        tapes = make_tapes(module, values)
        execute(module.PREPARE, tapes)
        execute(mutated, tapes)
        tapes[module.VIEW].quiescent("")

    controls.append(require_detection(missing_retirement, "compiled view-retirement writes zero"))

    for name, body in (("truncated final field", encode(values)[:-1]),
                       ("empty descriptor", ""),
                       ("zero multiplicity", encode(dict(values, f=0)))):
        tapes = make_tapes(module, values)
        tapes[module.PARENT] = Tape(body, origin=3, readonly=True)
        controls.append(require_detection(lambda: execute(module.PREPARE, tapes), name))
        execute(module.RELEASE, tapes)
        for i, tape in enumerate(tapes):
            tape.quiescent(body if i == module.PARENT else "")
    return controls


def source_controls(module, package):
    binding = load_module("review_header_source_binding", package / "source_binding.py")
    phase = package / "vendor/phase"
    word = json.loads(gzip.decompress((phase / "vendor/selected/WORD.json.gz").read_bytes()))
    caller = json.loads((package / "vendor/CONTROLLER.json").read_text())
    require(caller["physical_events"][0] == ["LOCAL", 0, 0, False], "actual first local caller site")
    raw = tuple(word["program"][9896])
    require(raw == ("MOVE", 236, 3, 7, False), "actual selected raw MOVE")
    main = set(word["live"]) | {x + 112 for x in word["live"]}
    helpers = sorted(set(range(word["public"])) - main)
    owner = 32 * len(word["live"]) + helpers.index(236)
    require(owner == 3356, "independently reconstructed caller helper owner")
    # Source constructor and binder share the authenticated IR class. Expected
    # token/owner values here come directly from the raw source and map formula.
    binding.source_boundary()
    ir = sys.modules["selected_phase_current_ir"]
    token = ("caller-local", 0, 0, ("move-in", "local", 9896, raw))
    event = ir.Event("SERVICE", (owner,), token, 0)
    route = binding.Route()
    adapted, report = binding.bind_event(event, route)
    require(adapted.fields == (owner,) and adapted.token == token[3] and adapted.rank == 0,
            "owner retained and exactly designated wrapper removed")
    require(report["normalized_route_is_input_contract"]
            and not report["complete_caller_or_fourier_executed"], "exact source-proof scope")
    variants = [
        ("raw owner instead of caller owner", replace(event, fields=(236,)), route),
        ("adjacent helper owner", replace(event, fields=(3357,)), route),
        ("flat token", replace(event, token=("caller-local", 0, 0) + token[3]), route),
        ("untyped caller boolean", replace(event, token=("caller-local", False, 0, token[3])), route),
        ("other source cut", replace(event, token=("caller-local", 1, 0, token[3])), route),
        ("buried raw token", replace(event, token=("caller-local", 0, 0, ("extra", token[3]))), route),
        ("untyped raw flag", replace(event, token=("caller-local", 0, 0,
            ("move-in", "local", 9896, ("MOVE", 236, 3, 7, 0)))), route),
        ("untyped rank", replace(event, rank=False), route),
        ("wrong gamma", event, replace(route, gamma=2)),
        ("boolean gamma", event, replace(route, gamma=True)),
        ("wrong ambient", event, replace(route, ambient=265)),
        ("wrong source frame", event, replace(route, source_frame=4)),
        ("reverse vectors", event, replace(route, vectors=tuple(reversed(range(9))))),
        ("after stage route", event, replace(route, before_helper_stage_route=False)),
    ]
    rejected = [require_detection(lambda e=e, r=r: binding.bind_event(e, r), label)
                for label, e, r in variants]
    return dict(owner=owner, raw_record=list(raw), helpers=len(helpers),
                actual_source_prefix=True, source_payload_not_executed=True,
                rejected=rejected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    package = args.package.resolve()
    pins_before = snapshot(package)
    sys.path.insert(0, str(package))
    module = load_module("review_header_view", package / "header_view.py")
    require(module.SCHEMA == SCHEMA and module.PARENT == 13 and module.VIEW == 14
            and tuple(module.PRIVATE) == tuple(i for i in range(40) if i != 13),
            "published 23-field and fixed physical-role ABI")
    cases = []
    for i, (f, remainder, K) in enumerate((
        (1, 0, 1), (1, 8, 2), (1, 9, 3), (1, 144, 2),
        (2, 0, 2), (2, 13, 2), (3, 144, 5), (7, 9, 3),
    )):
        _, result = successful_call(module, fixture(f, remainder, K), translated=(0, 5, 19)[i % 3])
        cases.append(result)
    small, large = fixture(1, 0, 1), fixture(17, 144, 5)
    history, _ = successful_call(module, large, translated=7)
    old_backing = sum(t.written_maximum - t.origin for i, t in enumerate(history) if i != 13)
    history[13] = Tape(encode(small), origin=10, readonly=True)
    _, reused = successful_call(module, small, tapes=history)
    fresh, fresh_result = successful_call(module, small, translated=7)
    fresh_backing = sum(t.written_maximum - t.origin for i, t in enumerate(fresh) if i != 13)
    require(reused["primitive_actions"] == fresh_result["primitive_actions"]
            and reused["prepare_dispatches"] == fresh_result["prepare_dispatches"]
            and reused["release_dispatches"] == fresh_result["release_dispatches"],
            "short call must traverse current extents, independent of old backing")
    require(old_backing > fresh_backing, "historical backing remains charged")
    controls = table_controls(module)
    source = source_controls(module, package)
    require(snapshot(package) == pins_before, "unchanged producer source bytes during review")
    table_hash = sha256(json.dumps([module.PREPARE, module.RELEASE], sort_keys=True,
                                  separators=(",", ":")).encode()).hexdigest()
    result = dict(status="INDEPENDENT_NATIVE_HEADER_TABLES_PASS", source_pins=pins_before,
                  table_sha256=table_hash, prepare_rows=len(module.PREPARE),
                  release_rows=len(module.RELEASE), success_cases=cases,
                  history=dict(retained_private_cells=old_backing, fresh_private_cells=fresh_backing,
                               short_call_actions=reused["primitive_actions"]),
                  table_controls=controls, source_binding=source,
                  scope="Independent emitted-table interpretation and exact typed source binding; no numerical parent field, native endpoint, or compiler assumption discharged.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "table_controls": len(controls), "source_controls": len(source["rejected"]),
                      "output_sha256": sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
