"""Exact complete movement prices; integer-root method credited to Worker C."""
import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

def root_floor(n, k):
    lo, hi = 0, 1 << ((n.bit_length()+k-1)//k)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**k <= n: lo = mid
        else: hi = mid
    assert lo**k <= n < (lo+1)**k
    return lo

def moment(profile, scale=10**42):
    lo = hi = Fraction(0)
    for d, n in profile.items():
        d = int(d)
        if d == 1: a = b = Fraction(1)
        else:
            q = root_floor(d**199 * scale**200, 200)
            a, b = Fraction(q, scale), Fraction(q+1, scale)
        lo += n*(a if n >= 0 else b)
        hi += n*(b if n >= 0 else a)
    return lo, hi

def record(pair):
    with localcontext() as c:
        c.prec = 80
        decimals = [str(Decimal(x.numerator)/Decimal(x.denominator)) for x in pair]
    return {'rational': list(map(str, pair)), 'decimal': decimals}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--result', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(); r = json.loads(a.result.read_text())
    old, new = r['before']['movement_profile'], r['after']['movement_profile']
    delta = {int(k): new.get(k, 0)-old.get(k, 0) for k in old | new}
    delta = {k: n for k, n in delta.items() if n}
    gate = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        gate[1+7*j] = gate.get(1+7*j, 0)+74
        gate[7*j] = gate.get(7*j, 0)-74
    limit = tuple(z/6 for z in moment(gate)); q = moment(new)
    known = r['all_live_owner_X_support_count']; unseen = 111-known
    need = (unseen+3)//4
    result = {
        'status': 'PASS_COMPLETE_COHORT_MOVEMENT_PRICE',
        'word_sha256': r['word_sha256'], 'exponent': '199/200',
        'integer_root_scale': 10**42, 'moment': record(q),
        'change': record(moment(delta)), 'signed_profile_change': delta,
        'linear_rank_change': sum(k*v for k, v in delta.items()),
        'limiting_ceiling': record(limit),
        'necessary_limiting_room': record((limit[0]-q[1], limit[1]-q[0])),
        'direct_point_same_targets': record(moment({7: 222, 1: len(r['all_targets'])})),
        'direct_known_support_reset': {
            'moment': record(moment({7: 222, 1: known})),
            'completed_count': known,
            'completed_targets': r['all_live_owner_X_support'],
            'scope': 'Every ground-copied coordinate, including61/67 when present, '
                     'is completed. No new continuation movement included.'},
        'quartet_only_repeat_screen': {
            'unseen_coordinates_at_current_owned_cut': unseen,
            'minimum_new_fixed_quartet_fields_covering_these_coordinates': need,
            'optimistic_moment_with_one_new_unit_MOVE_per_field': record((q[0]+need, q[1]+need)),
            'fails_limiting_gate_even_without_acquisition_or_public_splits': q[0]+need > limit[1],
            'scope': 'Only new nonlocal information from fixed quartet fields, '
                     'each paying at least one new rank1 MOVE. Changing fields en route, '
                     'already-paid delivery, other codes or new interfaces are outside.'},
        'scope': 'Complete partial-word movement only, not a completed native or '
                 'finite-multiplicity supplier. Reset retains no free unknown-valued source descents.'}
    a.out.write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], result['moment']['decimal'][0], result['necessary_limiting_room']['decimal'][0])

if __name__ == '__main__': main()
