"""Actual selected recipe on encoded current context/phase-control ports.

This executes physical phase accumulation at f>1. It does not execute the
exponentially large complete nine-coordinate selected packet. Phase algebra
is inherited; these controls test this format/context/codec implementation.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from contextlib import ExitStack
import json
from phase_binding import need
from selected_service import Service, source_boundary
from check_fixture import factory, DenseTape, load, body, header_bits
from phase_adapter import S
from codec import execution
from cardinal_counts import Count
from session import sealed_constructors


def expected(recipe, columns):
    value = len(columns) * recipe["phase"]
    for x in columns:
        value += sum(v for i, v in enumerate(recipe["linear_Z4"]) if x >> i & 1)
        value += 2 * sum(1 for i in range(9) for j in range(i + 1, 9)
                         if x >> i & 1 and x >> j & 1 and recipe["quadratic_rows"][i] >> j & 1)
    return value % 4


def run():
    entry, leave, record, report = source_boundary()
    service = Service(entry, factory)
    owner = service.provider
    work = [DenseTape(3 + i % 5) for i in range(owner.port_count)]
    owner.bind(work)
    context = DenseTape(9)
    for tape in (*work, context):
        for i in range(tape.origin - 1):
            tape.cells[i] = i % 2
    ancestors = [bytes(t.cells[:t.origin]) for t in (*work, context)]
    rows, wrong_residue, repeated_constant = [], False, False
    cases = ((2, 2, 0, (0, 0)), (3, 2, 0, (0, 0, 0)),
             (2, 3, 2, (1, 20)), (4, 2, 1, (5, 16, 4, 3)))
    for f, K, rho, columns in cases:
        H = f - 1
        a = 3 * H + 9 * f * K
        b = 6 * 2 * (4 + 1)
        values = dict(outer=2, rows=3, stock=1, row_bits=(1 << a) * b,
            within_bits=a, record_bits=b, p=9 * f, d=9 * f, K=K, G=1, H=H,
            q0=3, qF=0, qB=0, D=9 * f, f=f, rho=rho, active_start=2 * H,
            back_start=2 * H + 9 * f * K, selected_axes=9 * f,
            entry_start=2 * H, remainder=0, cutoff=9)
        bits = header_bits(values)
        load(context, bits)
        before = sum(t.actions() for t in (*work, context))
        owner.cohort.start()
        try:
            with owner.scope.installed(), ExitStack() as cleanup:
                state = {}
                # Finite fixture input serialization, before the sealed call.
                selected_mask = sum(1 << (f * K - 1 - (j * K + rho)) for j in range(f))
                for i, name in enumerate(owner.vectors):
                    value = ((1 << (f * K)) - 1) ^ selected_mask
                    for j, column in enumerate(columns):
                        value |= ((column >> i) & 1) << (f * K - 1 - (j * K + rho))
                    state[name] = Count.literal(value)
                    cleanup.callback(state[name].close)
                h = Count.literal(4)
                one = Count.literal(1)
                cleanup.callback(h.close); cleanup.callback(one.close)
                with sealed_constructors(), execution():
                    header = owner.read_header(S.abi.BinaryContextPort(context))
                    for value in header.values():
                        cleanup.callback(value.close)
                    _widths, native_rho, _coefficients, _rows = owner.prepare(header, h, cleanup)
                    value = owner.engine.recipe.phase(state, header["f"], header["K"], native_rho)
                    inverse = owner.engine.recipe.phase(state, header["f"], header["K"], native_rho, True)
                    need(value == expected(record["right"], columns) and inverse == -value % 4,
                         "actual selected recipe through current physical context/phase ports")
                    wrong = owner.engine.recipe.phase(state, header["f"], header["K"], header["rho"])
                    wrong_residue |= wrong != value
                    if not any(columns) and f == 2:
                        once = owner.engine.recipe.phase(state, one, header["K"], native_rho)
                        repeated_constant = once != value == 2
            owner.pool.empty()
        finally:
            owner.cohort.finish()
        need(body(context) == bits and context.head == context.origin, "actual 23-field context is borrowed")
        need(all(t.head == t.origin and all(x == 6 for x in t.cells[t.origin:]) for t in work),
             "all current coded phase-control work erased")
        need(all(bytes(t.cells[:t.origin]) == original for t, original in zip((*work, context), ancestors)),
             "control calls preserve ancestor cells")
        rows.append(dict(f=f, K=K, current_rho=rho, columns=columns, phase=value,
            physical_actions=sum(t.actions() for t in (*work, context)) - before))
    need(wrong_residue and repeated_constant, "wrong residue and copied constant controls discriminate")
    bad = type(entry)(entry.op, entry.fields, ("move-in", "local", 9896, ("MOVE", 236, 4, 7, False)))
    try:
        Service(bad, factory)
    except ValueError:
        rejected_frame = True
    else:
        rejected_frame = False
    need(rejected_frame, "wrong current source frame rejected before payload")
    return dict(status="PASS_CURRENT_SELECTED_PHASE_CONTROL", source=report,
        cases=rows, source_service_compiled=True, complete_selected_packet_executed=False,
        current_physical_phase_controls=True, negative_controls=["unconverted_current_rho",
        "copied_width_one_constant", "wrong_source_frame"], native_ports=owner.port_count)


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
