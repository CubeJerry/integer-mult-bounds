"""Typed first caller-local source cut; no recursive token searching.

The route describes the already-proved #6878 normalized base-nine helper
placement. It does not execute a new route or certify a numeric field by
inspecting its values. Gamma is exactly one and the ambient is exactly145.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from dataclasses import dataclass, fields, replace
import gzip
from hashlib import sha256
import json
import sys
from header_sources import HERE, activate, need

S = activate()
_boundary = None


def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, tuple):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, Route):
        return all(typed_equal(getattr(left, f.name), getattr(right, f.name)) for f in fields(Route))
    return left == right


@dataclass(frozen=True)
class Route:
    kind: str = "first-caller-local-base-nine"
    caller_site: int = 0
    caller_stage: int = 0
    raw_owner: int = 236
    owner: int = 3356
    ambient: int = 145
    vectors: tuple = tuple(range(9))
    gamma: int = 1
    source_frame: int = 3
    destination_frame: int = 7
    before_helper_stage_route: bool = True


class Captured(Exception):
    pass


def source_boundary():
    global _boundary
    if _boundary is not None:
        return _boundary
    raw, _leave, record, predecessor = S.selected.source_boundary()
    ir = sys.modules["selected_phase_current_ir"]
    word_path = S.phase / "vendor/selected/WORD.json.gz"
    word = json.loads(gzip.decompress(word_path.read_bytes()))
    caller_path = HERE / "vendor/CONTROLLER.json"
    caller = json.loads(caller_path.read_text())
    original, captured = ir.remap, {}

    def observe(event, names, context=(), rank_factor=1):
        emitted = original(event, names, context, rank_factor)
        if event.op == "SERVICE" and typed_equal(event.token, raw.token):
            captured.update(event=emitted, context=context, owner=names[236],
                            mapped_roles=len(names))
            raise Captured
        return emitted

    # Instrumentation observes the authentic source constructor's prefix.
    # Every emitted event before the capture is computed by the original remap.
    ir.remap = observe
    try:
        ir.current_caller(word, caller)
    except Captured:
        pass
    finally:
        ir.remap = original
    need(captured and typed_equal(captured["context"], ("caller-local", 0, 0)),
         "actual first caller-local source cut")
    event = captured["event"]
    need(typed_equal(event.fields, (3356,))
         and typed_equal(event.token, ("caller-local", 0, 0, raw.token)),
         "exact nested source token and actual owner")
    main = set(word["live"]) | {x + 112 for x in word["live"]}
    helpers = sorted(set(range(word["public"])) - main)
    need(helpers.index(236) == 28 and captured["owner"] == 32 * 104 + 28,
         "source-generated helper identity")
    need(word["frames"][word["initial"][236]] == []
         and len(word["frames"][word["final"][236]]) == 9
         and len(record["right"]["matrix_rows"]) == 9,
         "source helper starts empty and has base-nine target/monomial")
    report = dict(owner=3356, raw_owner=236, event=9896, caller_site=0, caller_stage=0,
                  parent_ambient=145, native_variables=9, gamma=1,
                  mapped_roles=captured["mapped_roles"], token=event.token,
                  raw_token=raw.token, rank=event.rank,
                  source_frame=3, destination_frame=7,
                  right_constant_phase=record["right"]["phase"],
                  inherited_record_sha256=predecessor["record_sha256"],
                  caller_sha256=sha256(caller_path.read_bytes()).hexdigest(),
                  geometry_head="41febf890fbbb852c6059d4c0cc8c593ae9dfa5c",
                  normalized_route_is_input_contract=True,
                  complete_caller_or_fourier_executed=False)
    _boundary = event, raw, Route(), report
    return _boundary


def bind_event(event, route):
    expected, raw, expected_route, report = source_boundary()
    need(type(event) is type(expected)
         and all(typed_equal(getattr(event, name), getattr(expected, name))
                 for name in ("op", "fields", "token", "rank")),
         "exact typed nested caller-local event and owner")
    need(typed_equal(route, expected_route),
         "exact normalized first-helper route, gamma one, ambient145")
    return replace(raw, fields=event.fields), dict(report)
