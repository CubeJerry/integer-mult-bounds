"""Certify adjacent integer cutoffs for the priced integer clock using rationals."""

from fractions import Fraction
import json


def log_ratio_interval(t):
    """Return lower/upper bounds on log((1+t)/(1-t)), 0 <= t <= 1/3."""
    assert 0 <= t <= Fraction(1, 3)
    square = t * t
    power = t
    total = Fraction(0)
    for index in range(24):
        total += 2 * power / (2 * index + 1)
        power *= square
    tail = 2 * power / (49 * (1 - square))
    return total, total + tail


LOG_TWO = log_ratio_interval(Fraction(1, 3))


def log_two_interval(value):
    exponent = value.bit_length() - 1
    unit = 1 << exponent
    lower, upper = log_ratio_interval(Fraction(value - unit, value + unit))
    return exponent + lower / LOG_TWO[1], exponent + upper / LOG_TWO[0]


def certified_sign(z, coefficient, additive):
    residual = z - 1000 * additive
    if residual <= 0:
        return -1
    lower, upper = log_two_interval(z + 4)
    factor = (1000 * coefficient)**3 * (z + 2)**2
    exact = residual**3
    if exact > factor * upper:
        return 1
    assert exact < factor * lower, "increase the fixed rational series length"
    return -1


def crossing(coefficient, additive):
    lower = 1 << 48
    upper = 1 << 55
    assert certified_sign(lower, coefficient, additive) == -1
    assert certified_sign(upper, coefficient, additive) == 1
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if certified_sign(middle, coefficient, additive) == 1:
            upper = middle
        else:
            lower = middle
    assert certified_sign(upper - 1, coefficient, additive) == -1
    assert certified_sign(upper, coefficient, additive) == 1
    return upper


if __name__ == "__main__":
    old_prefactor = (1 << 25) + 220
    z = crossing(70, old_prefactor)
    assert z == 18_536_231_398_600_959
    assert z + 4 < 1 << 55
    assert z > (1 << 48) + 1
    print(json.dumps({"coefficient": 70, "additive": old_prefactor,
                      "first_integer_for_invoice": z,
                      "predecessor_sign": -1, "threshold_sign": 1,
                      "log_series_terms": 24}, indent=2))
