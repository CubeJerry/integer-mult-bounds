"""Conditional optimistic budget from PR598 COSTS.txt; no supplier claim.

The only purpose is the bounded expansion gate. Exact lower bounds on the
moment reject a 5% improvement for the fixed C=62400 recipe and K=1..50.
Different controllers, copied ranks or mandatory data paths are not covered.
"""
from fractions import Fraction as Q
from math import isqrt

SELECTED_KAPPA = Q(836330098538459, 500000000000000000)


def log_lower(q):
    if q < 1:
        raise ValueError("log domain")
    powers = 0
    while q >= 2:
        q /= 2
        powers += 1

    def series(x):
        z = (x - 1) / (x + 1)
        return 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(24)), Q(0))

    return powers * series(Q(2)) + series(q)


def exp_lower(x):
    if x < 0:
        raise ValueError("exponential domain")
    term = Q(1)
    value = term
    for j in range(1, 5):
        term *= x / j
        value += term
    return value


def check():
    target = SELECTED_KAPPA * Q(21, 20)
    a = target / (1 - target)
    margins = []
    for k in range(1, 51):
        stages = 2 * k + 1
        m = 24 * stages + 1
        w = 2 * k * 98280
        deficit = 2 * k * 98280 - stages * 62400
        local_mass = 2 * 98280 * stages * 24
        other_mass = m * w - deficit - local_mass
        cap = isqrt(m * m // 2)
        if not (other_mass >= 0 and 24 <= cap < m):
            raise ValueError("budget domain")
        excess = (local_mass * exp_lower(a * log_lower(Q(m, 24)))
                  + other_mass * exp_lower(a * log_lower(Q(m, cap)))) - m * w
        if excess <= 0:
            raise ValueError("5-percent rejection not certified")
        margins.append(excess / (m * w))
    return {"stage_counts": 50, "copy_mass_per_call": 62400,
            "smallest_normalized_excess_lower_bound_positive": min(margins) > 0,
            "five_percent_gate": "rejected_in_fixed_optimistic_model"}


if __name__ == "__main__":
    print(check())
