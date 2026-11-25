#!/usr/bin/env python3
"""Exact integer checks for the all-arity label profile; no giant template."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random


def ceil_log2(number: int) -> int:
    assert number >= 1
    return (number - 1).bit_length()


def parameters(x: int) -> tuple[int, int, int, int]:
    v = ceil_log2(x + 2)
    d = 2
    while d**3 * v < x:
        d *= 2
    t = 2 + (x + d*d - 1) // (d*d)
    return v, d, t, 2*d - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('all-arity-profile-verification.json'))
    args = parser.parse_args()
    random = Random(2026112604)
    samples = set()
    for power in range(40, 513):
        for offset in (-1, 0, 1, 17):
            value = (1 << power) + offset
            if value >= 1 << 40:
                samples.add(value)
    for _ in range(600):
        power = random.randrange(40, 1025)
        samples.add((1 << power) + random.getrandbits(power))
    counts = {'parameter_profiles': 0, 'rank_guards': 0, 'label_count_guards': 0,
              'dimension_guards': 0, 'exact_cubic_envelope_checks': 0}
    for x in sorted(samples):
        v, d, t, h = parameters(x)
        assert d & (d - 1) == 0
        assert d**3 * v >= x and (d // 2)**3 * v < x
        assert x + 2*d*d - 2 - t*d*d <= -2
        counts['rank_guards'] += 1
        exact_log_labels = h*h*t
        assert exact_log_labels <= 5*(x - 1)
        counts['label_count_guards'] += 1
        # D=4+2h 2^(ht)<=4h 2^(ht); this is an integer ceiling log bound.
        dimension_log_majorant = 2 + ceil_log2(h) + h*t
        assert 2*dimension_log_majorant <= x - 1
        counts['dimension_guards'] += 1
        incidence_log_majorant = h*(d + 1) + d*t + d*(d - 1)*ceil_log2(t)
        whole_log_majorant = dimension_log_majorant + 1 + incidence_log_majorant
        # Cube removes fractional powers from 64 x^(2/3) v^(1/3).
        assert whole_log_majorant**3 <= 64**3 * x*x*v
        counts['exact_cubic_envelope_checks'] += 1
        counts['parameter_profiles'] += 1
    # Omitting the rank reserve t+=2 really breaks its intended universal guard.
    x = 1 << 80
    _, d, t, _ = parameters(x)
    bad_t = t - 2
    negative = {
        'omitted_rank_reserve_rejected': x + 2*d*d - 2 - bad_t*d*d > -2,
        'overoptimistic_unit_envelope_rejected': False,
    }
    for x in sorted(samples):
        v, d, t, h = parameters(x)
        lower = d*d - 1 + d*(t - 1) + d*(d - 1)*(t.bit_length() - 1)
        if lower**3 > x*x*v:
            negative['overoptimistic_unit_envelope_rejected'] = True
            break
    assert all(negative.values())
    receipt = {'status': 'passed', 'arithmetic': 'integers only; envelope checked after cubing',
               'scope': 'finite exact parameter, rank-majorant, dimension and incidence-profile checks; no huge labels, field program or multiplier instantiated',
               'guard_log2_arity_at_least': str(1 << 40),
               'largest_log2_arity_bit_length': max(samples).bit_length(),
               'counts': counts, 'negative_controls': negative}
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
