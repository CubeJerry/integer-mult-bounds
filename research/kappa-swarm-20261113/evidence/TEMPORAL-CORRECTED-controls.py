#!/usr/bin/env python3
"""Exact Gaussian-rational, phase-sensitive controls for two-cache surgery."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
TEST_GRID = 2  # Synthetic Gaussian grid; not a claim about #7481's grid.
CALLS = 17
SERVICE_BOUND_PER_MACRO = 32
STEPS_PER_SERVICE_BIT = 1 << 20


def need(ok, label):
    if not ok:
        raise AssertionError(label)


def g(a=0, b=0):
    return (F(a), F(b))


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gscale(a, q):
    q = F(q)
    return (a[0] * q, a[1] * q)


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def gconj(a):
    return (a[0], -a[1])


def row_scale(row, q):
    q = F(q)
    for key in list(row):
        row[key] = gscale(row[key], q)
        if row[key] == g():
            del row[key]


def row_add(dst, src, q):
    need(dst is not src, 'ADD/COPY operands must be distinct')
    q = F(q)
    for key, value in src.items():
        result = gadd(dst.get(key, g()), gscale(value, q))
        if result != g():
            dst[key] = result
        else:
            dst.pop(key, None)


def on_test_grid(row):
    return all((TEST_GRID * z[0]).denominator == 1
               and (TEST_GRID * z[1]).denominator == 1
               for z in row.values())


def scale_by(row, q, events):
    q = F(q)
    need(q != 0, 'fixed rational scalar must be nonzero')
    row_scale(row, q)
    need(on_test_grid(row), 'exact synthetic Gaussian-grid scale')
    events['SCALE'] += 1


def copy_into_zero(dst, src, q, events):
    need(not dst, 'COPY destination must be exactly zero')
    row_add(dst, src, q)
    need(on_test_grid(dst), 'exact synthetic Gaussian-grid copy')
    events['COPY'] += 1


def add_from(dst, src, q, events):
    row_add(dst, src, q)
    need(on_test_grid(dst), 'exact synthetic Gaussian-grid ADD')
    events['ADD'] += 1


def clear_owned_zero(row):
    # This checks the formal vector; real execution must also retire all
    # physical service scratch and satisfy the owned-clear contract.
    need(not row, 'CLEAR requires the exact stored vector to be zero')
    row.clear()


def scale_row(row, q):
    out = {}
    for key, value in row.items():
        z = gscale(value, q)
        if z != g():
            out[key] = z
    return out


def identity_two():
    return {0: g(1), 3: g(1)}


def matmul(a, b):
    out = {}
    for i in range(2):
        for j in range(2):
            value = g()
            for k in range(2):
                value = gadd(value, gmul(a.get(2*i+k, g()),
                                         b.get(2*k+j, g())))
            if value != g():
                out[2*i+j] = value
    return out


def adjoint(a):
    return {2*i+j: gconj(a.get(2*j+i, g()))
            for i in range(2) for j in range(2)
            if gconj(a.get(2*j+i, g())) != g()}


def cv_one_qubit():
    # Exact C_v convention from the pinned Clifford source:
    # C_v=(1+i)I/2+(1-i)X/2.
    return {0: g(F(1, 2), F(1, 2)),
            1: g(F(1, 2), F(-1, 2)),
            2: g(F(1, 2), F(-1, 2)),
            3: g(F(1, 2), F(1, 2))}


def run_positive():
    # Each dictionary is a 2x2 matrix acting on an arbitrary input vector.
    x_a = identity_two()
    chart_c = cv_one_qubit()
    x_b = chart_c.copy()  # x_B = C_v x_A, including phase-sensitive entries.
    chart_unitary = matmul(adjoint(chart_c), chart_c) == identity_two()
    need(chart_unitary,
         'C_v chart map must be unitary')
    b1, b2 = scale_row(x_b, 2), scale_row(x_b, 3)
    a1, a2 = scale_row(x_a, 2), scale_row(x_a, 3)
    nonidentity_chart = x_a != x_b
    phase_entries_nonzero = any(z[1] for z in x_b.values())
    need(nonidentity_chart, 'chart control must be nonidentity')
    need(phase_entries_nonzero, 'chart control must retain phase data')
    need(on_test_grid(x_a) and on_test_grid(x_b), 'chart endpoints on test grid')
    events = Counter()

    # Two earlier B observations:
    # x_B = (2/7)*b1(t1)+(1/7)*b2(t2), b1=2*x_B, b2=3*x_B.
    c_b = {}  # INIT at B, first needed observation t1
    copy_into_zero(c_b, b1, 2, events)
    add_from(c_b, b2, 1, events)  # t2>t1, source-preserving
    need(b1 == scale_row(x_b, 2) and b2 == scale_row(x_b, 3),
         'B accumulator must preserve both native donor matrices')
    scale_by(c_b, F(1, 7), events)
    need(c_b == x_b, 'B cache must equal exact phase-sensitive target matrix')

    # At A, retain the source-chart matrix and clear the old owner.
    original = x_a.copy()
    c_a = {}  # INIT at A
    copy_into_zero(c_a, original, 1, events)
    add_from(original, c_a, -1, events)
    need(not original, 'old owner must be zero before CLEAR at A')
    clear_owned_zero(original)  # old MOVE removed

    # Start a fresh B lifetime with no A-to-B MOVE; restore C_v*x_A.
    original = {}  # INIT at B
    copy_into_zero(original, c_b, 1, events)
    need(original == x_b, 'B reinitialization must restore target matrix')
    add_from(c_b, original, -1, events)
    need(not c_b, 'B cache must be zero before CLEAR')
    clear_owned_zero(c_b)

    # Two strictly later A observations erase c_A:
    # x_A = (2/7)*a1(s1)+(1/7)*a2(s2), a1=2*x_A, a2=3*x_A.
    scale_by(c_a, 7, events)
    add_from(c_a, a1, -2, events)  # s1
    need(a1 == scale_row(x_a, 2), 'first A donor must remain unchanged')
    add_from(c_a, a2, -1, events)  # s2>s1
    need(a2 == scale_row(x_a, 3), 'second A donor must remain unchanged')
    need(not c_a, 'A cache must be zero before CLEAR')
    clear_owned_zero(c_a)
    post_target_exact = original == x_b
    need(post_target_exact, 'post-surgery matrix must equal old MOVE target')

    scalar_operations = sum(events.values())
    init_clear_events = 6
    macro_count = scalar_operations + init_clear_events
    service_upper = CALLS * SERVICE_BOUND_PER_MACRO * macro_count
    bitstep_coefficient = service_upper * STEPS_PER_SERVICE_BIT
    return {
        'status': 'PASS',
        'positive': {
            'chart_map': 'C_v=(1+i)I/2+(1-i)X/2',
            'chart_unitary_exact': chart_unitary,
            'nonidentity_chart': nonidentity_chart,
            'nonzero_phase_entries': phase_entries_nonzero,
            'whole_vector_dimension': 2,
            'x_A': {str(k): [str(v[0]), str(v[1])] for k, v in x_a.items()},
            'x_B': {str(k): [str(v[0]), str(v[1])] for k, v in x_b.items()},
            'earlier_B_witnesses': '(2/7)*b1(t1)+(1/7)*b2(t2), b1=2*x_B, b2=3*x_B',
            'later_A_witnesses': '(2/7)*a1(s1)+(1/7)*a2(s2), a1=2*x_A, a2=3*x_A',
            'strict_chronology': 't1<t2<old_MOVE<s1<s2',
            'denominator_7_exact_division': True,
            'all_rows_on_integer_test_grid_2': True,
            'test_grid_not_claimed_for_7481': True,
            'old_MOVE_removed': True,
            'owner_cleared_at_A_then_initialized_at_B': True,
            'post_surgery_target_exact': post_target_exact,
            'scalar_events': dict(events),
            'scalar_event_count_per_native_word': scalar_operations,
            'added_INIT_CLEAR_events_per_native_word': init_clear_events,
        },
        'wrong_witness_negative': {
            'donor_row': '6*x_B',
            'coefficient': '1/3',
            'resulting_row': '2*x_B',
        },
        'wrong_chart_bytes_negative': {
            'copied_row': 'x_A=I',
            'required_target_row': 'x_B=C_v*I',
        },
        'per_native_word': {
            'extra_owned_cache_ids': 2,
            'peak_owned_delta_upper': 2,
            'additional_lifetimes': 3,
            'added_INIT_CLEAR_events': init_clear_events,
            'deleted_paid_MOVEs': 1,
            'deleted_adapter_maps': 2,
        },
        'across_17_calls': {
            'scalar_operations': CALLS * scalar_operations,
            'INIT_CLEAR_operations': CALLS * init_clear_events,
            'cache_role_allocations': CALLS * 2,
            'additional_lifetimes': CALLS * 3,
            'paid_MOVEs_deleted': CALLS,
            'adapter_maps_deleted': CALLS * 2,
            'generic_scalar_services_upper': service_upper,
            'generic_scalar_step_coefficient_before_Cscalar_and_Vnew': bitstep_coefficient,
            'elementary_record_upper_per_deleted_adapter': '4*(n+1)^2',
            'route_record_physical_bound': 'C_move*V_new*((f*log(p))^tau+1) per record',
        },
        'scope': 'Synthetic Gaussian-rational cumulative interface control only; no #7481 grid claim, source provider, compiler admission, full budget pass, or kappa claim.',
    }


def wrong_controls():
    x_b = cv_one_qubit()
    wrong_donor = scale_row(x_b, 6)
    wrong_cache = {}
    events = Counter()
    copy_into_zero(wrong_cache, wrong_donor, 1, events)
    scale_by(wrong_cache, F(1, 3), events)
    need(wrong_cache == scale_row(x_b, 2), 'wrong witness must equal 2*x_B')
    wrong_witness_match = wrong_cache == x_b
    need(not wrong_witness_match, 'wrong witness must not equal x_B')

    nonzero_clear_rejected = False
    try:
        clear_owned_zero(wrong_cache.copy())
    except AssertionError as exc:
        need(str(exc) == 'CLEAR requires the exact stored vector to be zero',
             'CLEAR rejection must be for the exact nonzero-row condition')
        nonzero_clear_rejected = True
    need(nonzero_clear_rejected, 'CLEAR must reject nonzero stored vector')

    source_bytes = identity_two()
    need(source_bytes != x_b, 'C_v chart must change exact whole-vector bytes')
    wrong_chart_cache = {}
    copy_into_zero(wrong_chart_cache, source_bytes, 1, events)
    wrong_chart_restore = {}
    copy_into_zero(wrong_chart_restore, wrong_chart_cache, 1, events)
    wrong_chart_match = wrong_chart_restore == x_b
    need(not wrong_chart_match,
         'copying A-chart bytes as B target must fail target equality')
    return dict(wrong_witness_match=wrong_witness_match,
                wrong_chart_match=wrong_chart_match,
                nonzero_clear_rejected=nonzero_clear_rejected)


def main():
    result = run_positive()
    controls = wrong_controls()
    result['wrong_witness_negative']['exact_target_match'] = controls['wrong_witness_match']
    result['wrong_witness_negative']['nonzero_CLEAR_rejected'] = controls['nonzero_clear_rejected']
    result['wrong_witness_negative']['control_executed'] = True
    result['wrong_chart_bytes_negative']['exact_target_match'] = controls['wrong_chart_match']
    result['wrong_chart_bytes_negative']['control_executed'] = True
    (ROOT / 'CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
