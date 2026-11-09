"""Physical descriptor tests with observer-only integer/extent interpretation.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from dataclasses import replace
from hashlib import sha256
import json
from header_sources import need
from header_view import HeaderView, TABLE_REPORT, PREPARE, RELEASE, S, VIEW, PRIVATE
from source_binding import source_boundary, bind_event, Route
from fixture_tools import (values, native_values, encode, decode, put, body, hardware,
                           snapshots, restored, source_parent)


def one(parent_values, reuse=None):
    owner, work, parent = hardware() if reuse is None else reuse
    initial = encode(parent_values)
    put(parent, initial)
    ancestors = snapshots((*work, parent))
    before = sum(t.actions() for t in (*work, parent))
    prepare_steps = owner.prepare()
    result = body(owner.context.tape)
    need(decode(result) == native_values(parent_values), "all23 native-view values")
    need(result == encode(native_values(parent_values)), "exact canonical raw-binary view")
    need(body(parent) == initial and parent.head == parent.origin, "borrowed parent at native cut")
    need(all(t.head == t.origin for t in work), "all private origins at native cut")
    need(all(not body(owner.ports[role].tape) for role in PRIVATE if role != VIEW),
         "only the view is live at native cut")
    release_steps = owner.release()
    restored(work, parent, initial, ancestors)
    actions = sum(t.actions() for t in (*work, parent)) - before
    E = len(initial)
    need(prepare_steps + release_steps <= 1000 * E + 10000,
         "conservative proved descriptor instruction bill")
    need(actions <= prepare_steps + release_steps, "each physical action is a table instruction")
    report = dict(f=parent_values["f"], remainder=parent_values["remainder"],
                  K=parent_values["K"], header_bits=E, view_bits=len(result),
                  prepare_steps=prepare_steps, release_steps=release_steps,
                  physical_actions=actions, retained_cells=sum(len(t.cells) for t in work),
                  all23_equal=True, private_erased=True,
                  view_sha256=sha256(bytes(result)).hexdigest())
    return report, (owner, work, parent)


def source_chain():
    parent_values = values()
    actual, source_owner, source_work, source_input, report = source_parent(parent_values, live=True)
    # Borrow the actual physical output, with no decode/reload/conversion.
    new = HeaderView()
    new_work = [S.codec.DenseTape(4 + j % 7) for j in PRIVATE]
    new.bind(new_work, S.abi.BinaryContextPort(actual))
    actual_before = bytes(body(actual))
    new.prepare()
    need(decode(body(new.context.tape)) == native_values(parent_values),
         "actual source-produced header consumed on the same physical port")
    new.release()
    need(bytes(body(actual)) == actual_before and actual.head == actual.origin,
         "source-produced parent preserved")
    source_owner.active = True
    source_owner.release()
    need(all(all(x == 6 for x in t.cells[t.origin:]) and t.head == t.origin
             for t in (*source_work, *new_work)), "both metadata banks retired")
    return dict(report, same_physical_parent_port=True, all23_equal=True)


def source_controls():
    event, raw, route, report = source_boundary()
    adapted, _ = bind_event(event, route)
    need(adapted.fields == (3356,) and adapted.token == raw.token, "typed real source adaptation")
    mutations = [
        ("raw_owner", replace(event, fields=(236,)), route),
        ("wrong_owner", replace(event, fields=(3357,)), route),
        ("flat_token", replace(event, token=("caller-local", 0, 0) + raw.token), route),
        ("extra_nesting", replace(event, token=("caller-local", 0, 0, event.token)), route),
        ("boolean_site", replace(event, token=("caller-local", False, 0, raw.token)), route),
        ("wrong_stage", replace(event, token=("caller-local", 0, 1, raw.token)), route),
        ("wrong_frame", replace(event, token=("caller-local", 0, 0,
            ("move-in", "local", 9896, ("MOVE", 236, 4, 7, False)))), route),
        ("paid_cut", replace(event, op="PAID", rank=1), route),
        ("wrong_route_order", event, replace(route, vectors=(1, 0, *range(2, 9)))),
        ("gamma_two", event, replace(route, gamma=2)),
        ("boolean_gamma", event, replace(route, gamma=True)),
        ("wrong_route_ambient", event, replace(route, ambient=146)),
        ("after_stage_route", event, replace(route, before_helper_stage_route=False)),
    ]
    rejected = []
    for name, candidate, candidate_route in mutations:
        try:
            bind_event(candidate, candidate_route)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("source control accepted " + name)
    return dict(report, negative_controls=rejected)


def rejection_retry():
    owner, work, parent = hardware()
    valid = values()
    bad = dict(valid, f=0)
    before = encode(bad)
    put(parent, before)
    ancestors = snapshots((*work, parent))
    try:
        owner.prepare()
    except ValueError:
        pass
    else:
        raise ValueError("zero f accepted")
    restored(work, parent, before, ancestors)
    need(not owner.active, "rejected producer leaves no active view")
    retried, _ = one(valid, (owner, work, parent))
    fresh, _ = one(valid)
    need(retried["physical_actions"] == fresh["physical_actions"], "retry current-call cost")
    return dict(rejected="zero_f", valid_retry_actions=retried["physical_actions"],
                same_fresh_actions=True)


def run():
    cases = []
    state = None
    for f in (1, 2, 5):
        for rem in (0, 1, 8, 9, 13, 144):
            K = 1 + (rem % 3)
            row, state = one(values(f=f, remainder=rem, K=K, rho=K-1), state)
            cases.append(row)
    # Independent long shape descriptions need no full numerical packet.
    lengths = []
    for width in (64, 257, 1024, 4096):
        row, state = one(values(outer=(1 << width) + 7), state)
        lengths.append(dict(shape_bits=width, **row))
    large, reuse = one(values(outer=(1 << 8192) + 7))
    small, _ = one(values(f=1, remainder=0, K=1, rho=0, outer=1, rows=1, stock=1), reuse)
    fresh, _ = one(values(f=1, remainder=0, K=1, rho=0, outer=1, rows=1, stock=1))
    need(small["physical_actions"] == fresh["physical_actions"]
         and small["prepare_steps"] == fresh["prepare_steps"]
         and small["release_steps"] == fresh["release_steps"], "no historical-backing scan")
    need(small["retained_cells"] > fresh["retained_cells"], "historical backing actually retained")
    encoded_tables = json.dumps((PREPARE, RELEASE), separators=(",", ":"), sort_keys=True).encode()
    return dict(status="PASS_CURRENT_NATIVE_HEADER_DESCRIPTOR", tables=TABLE_REPORT,
                table_sha256=sha256(encoded_tables).hexdigest(), source=source_controls(),
                source_chain=source_chain(), cases=cases, long_descriptions=lengths,
                reuse=dict(large=large, small=small, fresh=fresh),
                rejection_retry=rejection_retry(), complete_numeric_parent_executed=False)


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
