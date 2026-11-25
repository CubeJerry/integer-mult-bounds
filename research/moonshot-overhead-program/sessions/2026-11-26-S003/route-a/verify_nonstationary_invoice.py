#!/usr/bin/env python3
"""Finite checks of a literal charged-recurrence barrier, not runtime bounds."""
from decimal import Decimal as D, localcontext
from fractions import Fraction
from math import comb, prod
from pathlib import Path
import hashlib
import json
import random
import sys


def main():
    with localcontext() as context:
        context.prec = 90
        ln2 = D(2).ln()

        def log2(x):
            return D(x).ln() / ln2

        def fun(x):
            if not x:
                return D(0)
            x = D(x)
            return (x * x * log2(x + 2)) ** (D(1) / 3)

        families = [(2, 2), (2, 4), (4, 2), (4, 4), (2, 2, 2), (4, 2, 8), (2, 4, 2, 2)]
        local = 0
        for distances in families:
            p = prod(distances)
            for t in (1, 2, 4, 8):
                q = 1 << t
                incidence = comb(2 * distances[0] - 1, distances[0]) * (q - 1) * t ** (distances[0] - 1)
                for distance in distances[1:]:
                    incidence = comb(2 * distance - 1, distance) * incidence ** distance
                prev_h = prod(2 * distance - 1 for distance in distances[:-1])
                dimension = 2 + (2 * distances[-1] - 1) * ((1 << (t * prev_h)) - 1)
                assert dimension >= 23 and incidence >= 27
                for x in (2, 3, 4, 8, 16, 32, 64, 128, 512, 1024, 4096, 16384):
                    rank_lower = Fraction(1, 1 << (p * (t + 1) - 1))
                    invoice_lower = dimension * (1 + incidence) * (1 + (1 << x) * rank_lower)
                    log_invoice_lower = log2(invoice_lower.numerator) - log2(invoice_lower.denominator)
                    assert log_invoice_lower >= fun(x) / 128
                    local += 1
        inversion = 0
        for power in range(12, 121):
            x = D(2) ** power
            j = (1024 * x / log2(x)) ** (D(1) / 3)
            assert j >= 64
            assert j ** 3 * log2(j) / 128 > x
            assert x / j >= fun(x) / 16
            inversion += 1
        assert fun(4096) < 1024 and log2(23 * 28) > 9
        rng = random.Random(26791)
        minimum_margin = None
        schedules = 0
        for size in range(1, 81):
            for _ in range(8):
                ys = [rng.randrange(2, 4097) for _ in range(size)]
                increments = [y + rng.randrange(4) for y in ys]
                root_minus_base = sum(increments)
                sum_f = sum((fun(y) for y in ys), D(0))
                assert sum_f >= fun(sum(ys))
                assert D(sum(ys)) >= D(2) * root_minus_base / 5
                margin = sum_f / 128 - fun(root_minus_base) / 320
                assert margin >= 0
                minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
                schedules += 1
        y = D(4096)
        # A fast descent still has a logarithmic step O(log m), but violates
        # f>=e/(8m), so its normalized invoice may be smaller than one.
        assert 3 + fun(y) / 128 - y / 2 < 0
        assert 2 * y > y + 3
    result = dict(status="passed", scope="Literal invoice lower bounds and normalized schedule accumulation; not actual-machine lower bounds.",
                  python=sys.version.split()[0], decimal_precision=90,
                  nested_families=len(families), exact_rank_lower_invoice_cases=local,
                  local_inversion_grid_points=inversion,
                  uneven_schedules=schedules, minimum_schedule_log_margin=float(minimum_margin),
                  fast_descent_negative_controls=1,
                  limitations=["The local rank fraction is the proved lower witness, not a newly computed exact rank.",
                               "The cost recurrence is an explicitly defined positive upper invoice.",
                               "This checker does not prove a runtime lower bound or instantiate a tape algorithm."])
    source = Path(__file__)
    result["checker_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    source.with_name("nonstationary-invoice-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
