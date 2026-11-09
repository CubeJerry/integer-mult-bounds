"""Real selected phase controls consuming the physically produced view.

No complete parent packet or Fourier child is executed. The bound public
field below is unused by this control fixture; it is not a fake numerical
supplier. Every observed phase comes from the unchanged encoded phase engine.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from contextlib import ExitStack
from hashlib import sha256
import json
import sys
from header_view import NativeEntrance, S
from header_sources import need
from source_binding import source_boundary
from fixture_tools import values, encode, put, body, snapshots

from check_fixture import factory
from codec import execution
from cardinal_counts import Count
from session import sealed_constructors


def expected(recipe, columns):
    phase = len(columns) * recipe["phase"]
    for x in columns:
        phase += sum(v for i, v in enumerate(recipe["linear_Z4"]) if (x >> i) & 1)
        phase += 2 * sum(1 for i in range(9) for j in range(i + 1, 9)
                         if (x >> i) & 1 and (x >> j) & 1 and (recipe["quadratic_rows"][i] >> j) & 1)
    return phase % 4


def run():
    event, _raw, route, source_report = source_boundary()
    entrance = NativeEntrance(event, route, factory)
    work = [S.codec.DenseTape(3 + i % 5) for i in range(entrance.port_count)]
    context = S.codec.DenseTape(9)
    unused_field = S.codec.DenseTape(11)
    for tape in (*work, context, unused_field):
        for j in range(tape.origin - 1):
            tape.cells[j] = j % 2
    entrance.bind(work, {3356: S.abi.CodedPort(unused_field)}, S.abi.BinaryContextPort(context))
    owner = entrance.native.provider
    _entry, _leave, record, _report = S.selected.source_boundary()
    recipe = record["right"]
    cases = []
    wrong_rho = repeated_constant = False
    for f, rem, K, rho, columns in (
        (2, 13, 1, 0, (0, 0)),
        (2, 9, 2, 1, (1, 0)),
    ):
        parent = values(f=f, remainder=rem, K=K, rho=rho)
        # This is an admitted local native-layout control, not a full global
        # root reservation instance. Complete N=145*f+r extents stay present;
        # H=f-1 suffices for the actual phase provider's compact reservation.
        H = f - 1
        parent.update(H=H, entry_start=2*H+5, active_start=2*H+5+rem*K,
                      back_start=2*H+5+parent["selected_axes"]*K+11)
        parent["within_bits"] = parent["back_start"] + H + 3
        parent["row_bits"] = parent["record_bits"] << parent["within_bits"]
        print("actual phase-control start", f, rem, K, rho, file=sys.stderr, flush=True)
        initial = encode(parent)
        put(context, initial)
        tapes = (*work, context, unused_field)
        ancestors = snapshots(tapes)
        before = sum(t.actions() for t in tapes)
        descriptor_steps = entrance.view.prepare()
        view_before = bytes(body(entrance.view.context.tape))
        owner.cohort.start()
        try:
            with owner.scope.installed(), ExitStack() as cleanup:
                state = {}
                mask = sum(1 << (f * K - 1 - (j * K + rho)) for j in range(f))
                for i, name in enumerate(owner.vectors):
                    value = ((1 << (f * K)) - 1) ^ mask
                    for j, column in enumerate(columns):
                        value |= ((column >> i) & 1) << (f * K - 1 - (j * K + rho))
                    state[name] = Count.literal(value)
                    cleanup.callback(state[name].close)
                h, one = Count.literal(4), Count.literal(1)
                cleanup.callback(h.close)
                cleanup.callback(one.close)
                with sealed_constructors(), execution():
                    header = owner.read_header(entrance.view.context)
                    for value in header.values():
                        cleanup.callback(value.close)
                    _widths, native_rho, _coefficients, _rows = owner.prepare(header, h, cleanup)
                    phase = owner.engine.recipe.phase(state, header["f"], header["K"], native_rho)
                    inverse = owner.engine.recipe.phase(state, header["f"], header["K"], native_rho, True)
                    need(phase == expected(recipe, columns) and inverse == -phase % 4,
                         "real selected phase through source-bound physical native view")
                    wrong = owner.engine.recipe.phase(state, header["f"], header["K"], header["rho"])
                    wrong_rho |= wrong != phase
                    if f == 2 and not any(columns):
                        once = owner.engine.recipe.phase(state, one, header["K"], native_rho)
                        repeated_constant = once != phase == 2
            owner.pool.empty()
        finally:
            owner.cohort.finish()
        need(bytes(body(entrance.view.context.tape)) == view_before,
             "native phase controls borrow exact produced view")
        descriptor_steps += entrance.view.release()
        need(body(context) == initial and context.head == context.origin,
             "original full ordinary context preserved")
        need(all(t.head == t.origin and all(x == 6 for x in t.cells[t.origin:]) for t in work),
             "both actual metadata and phase-control private banks erased")
        need(snapshots(tapes) == ancestors and not body(unused_field),
             "all ancestors preserved and no numeric packet consumed")
        actions = sum(t.actions() for t in tapes) - before
        cases.append(dict(f=f, ordinary_remainder=rem, K=K, rho=rho,
                          columns=columns, phase=phase, inverse=inverse,
                          physical_actions=actions, descriptor_steps=descriptor_steps,
                          full_context_bits=len(initial), view_sha256=sha256(view_before).hexdigest()))
        print("actual phase-control returned", f, rem, K, rho, actions,
              file=sys.stderr, flush=True)
    need(wrong_rho and repeated_constant, "residue and repeated-constant controls discriminate")
    need(owner.calls == 0, "no full monomial invocation claimed by phase-control fixtures")
    return dict(status="PASS_SOURCE_BOUND_NATIVE_HEADER_PHASE_CONTROLS", source=source_report,
                cases=cases, fixed_total_ports=entrance.port_count,
                descriptor_ports=entrance.view.port_count,
                actual_phase_engine=True, synthetic_numeric_callback=False,
                full_global_reservation_admission=False,
                full_native_invocations=owner.calls, complete_parent_packet_executed=False,
                fourier_child_executed=False,
                controls=["wrong_current_rho", "copied_one_column_constant"])


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
