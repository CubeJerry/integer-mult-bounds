"""Exact endpoint certificates for the complete numerical cost transfer."""

from fractions import Fraction
import json


def compare(excess, log_bound, coefficient=832, guard_bits=100):
    z = 1 << guard_bits
    additive = (1 << 25) + 4 * (guard_bits + 1)
    numerator, denominator = excess.as_integer_ratio()
    log_numerator, log_denominator = log_bound.as_integer_ratio()
    residual = numerator * z - denominator * additive
    assert residual > 0
    left = log_denominator * residual**3
    right = (coefficient * denominator)**3 * (z + 2)**2 * log_numerator
    return {
        "excess": [numerator, denominator],
        "phase_coefficient": coefficient,
        "guard_log": guard_bits,
        "log_bound": [log_numerator, log_denominator],
        "difference": str(left - right),
        "ratio_millionths_floor": 10**6 * left // right,
    }


def check():
    coarse = Fraction(101)
    precise = Fraction(102401, 1024)
    trials = [
        compare(Fraction(1, 10**6), coarse),
        compare(Fraction(1, 2_500_000), coarse),
        compare(Fraction(357, 10**9), precise),
        compare(Fraction(35_683, 10**11), precise),
        compare(Fraction(8_449, 10**11), precise, 197),
        compare(Fraction(1, 1000), Fraction(60), 197, 59),
        compare(Fraction(7_077, 10**11), precise, 165),
        compare(Fraction(1, 1000), Fraction(59), 165, 58),
    ]
    assert all(int(row["difference"]) > 0 for row in trials)
    assert 35_682**3 * (1 << 100) < (832 * 10**11)**3 * 100
    assert 3 * 2**48 + 2 < 2**55
    assert (1 + 5120).bit_length() == 13
    assert 3 * 5120 * 2**84 < 2**110
    assert 8_192 * 21 * 10 * 8 * 7 * 3 < 2**29
    return {
        "endpoints": trials,
        "exact_last_length_failures": check_packing(),
        "positive_invoice_lower_control": True,
    }


def address_width(length):
    digit_bits = (length - 1).bit_length()
    digit_count = (length + digit_bits - 1) // digit_bits
    return (4 * digit_count - 1).bit_length()


def check_packing():
    tested = 0
    for z in range(3, 13):
        required = 1 << z
        unit = 1 << (required - 3)
        last_digit_width = required + z - 2
        last_failure = unit * last_digit_width
        assert (last_failure - 1).bit_length() == last_digit_width
        assert address_width(last_failure) == required - 1
        assert address_width(last_failure + 1) == required
        for digit_width in range(last_digit_width + 1, last_digit_width + 100):
            assert address_width((1 << (digit_width - 1)) + 1) >= required
            tested += 1
        if z <= 4:
            for length in range(2, 2 * last_failure + 1):
                if address_width(length) < required:
                    assert length <= last_failure
                tested += 1
    return tested


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
