"""Exact directed binary-log intervals for the frozen R=240 whole-machine invoice."""
from fractions import Fraction
from functools import lru_cache
import json


@lru_cache(None)
def log_bounds(n, digits=112):
    """Extract log2(n) in binary by squaring brackets with outward rounding."""
    assert n > 0
    integer = n.bit_length() - 1
    precision = 4 * digits
    while True:
        scale = 1 << precision
        numerator = n * scale
        lower = numerator >> integer
        upper = (numerator + (1 << integer) - 1) >> integer
        bits = 0
        for _ in range(digits):
            lower = lower * lower // scale
            upper = (upper * upper + scale - 1) // scale
            bits *= 2
            if lower >= 2 * scale:
                bits += 1
                lower //= 2
                upper = (upper + 1) // 2
            elif upper >= 2 * scale:
                # A binary digit cannot be decided at this word precision.
                precision *= 2
                break
        else:
            denominator = 1 << digits
            return (integer + Fraction(bits, denominator),
                    integer + Fraction(bits + 1, denominator))


def sharp_sign(n, extra_bits=0):
    """Compare the exact positive logarithmic invoice with n/1000."""
    p0, p1 = log_bounds(5121)
    l0, l1 = log_bounds(n + 2)
    r0, r1 = log_bounds(n + 4)
    rest = Fraction(n, 1000) - 169 - extra_bits
    d0, d1 = rest - p1 - 4*l1, rest - p0 - 4*l0
    if d1 <= 0:
        return -1
    factor = 70**3 * (n + 2)**2
    if d0 > 0 and d0**3 > factor * r1:
        return 1
    if d1**3 < factor * r0:
        return -1
    raise ArithmeticError("Increase binary log precision to decide this sign")


def inherited_sign(n):
    """The separately published bound after freezing its additive constant."""
    residual = n - 1000 * (2**25 + 220)
    low, high = log_bounds(n + 4)
    factor = 70_000**3 * (n + 2)**2
    if residual**3 < factor * low:
        return -1
    if residual**3 > factor * high:
        return 1
    raise ArithmeticError("Increase binary log precision to decide this sign")


def piecewise_margins(n):
    """Enclose the two normalized cubic residuals in the weighted Walsh caller."""
    base = Fraction(n, 1000) - (2**25 + 220)
    intercept = Fraction(4_112_174_977_105_665, 1024)
    slope = Fraction(17, 32768)
    low, high = log_bounds(n + 4)
    residuals = ((base - 2_220_000_000_000, Fraction(48)),
                 (base - intercept - slope*(n + 2), Fraction(33, 4)))
    intervals = []
    for residual, coefficient in residuals:
        squared_size = (n + 2)**2
        scaled = (residual / coefficient)**3 / squared_size
        intervals.append((scaled - high, scaled - low))
    return intervals


def first_positive(sign):
    low, high = 2**48, 2**55
    assert sign(low) == -1 and sign(high) == 1
    while high - low > 1:
        middle = (high + low) // 2
        if sign(middle) == 1:
            high = middle
        else:
            low = middle
    assert sign(high-1) == -1 and sign(high) == 1
    return high


if __name__ == "__main__":
    older = first_positive(inherited_sign)
    assert older == 18_536_231_398_600_959
    binary = first_positive(sharp_sign)
    natural = first_positive(lambda n: sharp_sign(n, 1))
    z = 11_665_715_140_844_862
    historical, movement = piecewise_margins(z)
    previous_historical, previous_movement = piecewise_margins(z - 1)
    assert min(historical[0], previous_historical[0]) > Fraction(262, 100)
    assert Fraction(127, 10**17) < movement[0] < movement[1] < Fraction(129, 10**17)
    assert Fraction(-378, 10**16) < previous_movement[0] < previous_movement[1] < Fraction(-376, 10**16)
    print(json.dumps({"piecewise_two_invoices": z, "piecewise_binding": "movement",
                      "binary_fraction_digits": 112, "old_additive": older,
                      "actual_prefactor": binary,
                      "one_full_extra_bit": natural}, indent=2))
