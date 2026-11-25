#!/usr/bin/env python3
"""Exact finite checks of integer radix selection and compatible-prime witnesses.

No finite run verifies the Baker--Harman--Pintz asymptotic threshold.
The root operation is shared with the independently boundary-checked script.
"""

from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path
import json
import importlib.util

# Load the exact sibling file explicitly, including under Python isolated mode.
_spec = importlib.util.spec_from_file_location("route_c_recurrence", Path(__file__).with_name("check_recurrence.py"))
assert _spec is not None and _spec.loader is not None
_recurrence = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_recurrence)
integer_root = _recurrence.integer_root


def ceil_power_root(width: int, exponent: int) -> int:
    target = 1 << width
    root = integer_root(target, exponent)
    return root if root**exponent == target else root + 1


def prime(value: int) -> bool:
    return value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1))


def compatible_search(base: int, exponent: int, forbidden_product: int, slack_h: int | None = None):
    denominator = 2 * exponent if slack_h is None else 4 * exponent * slack_h
    stop = base + base // denominator
    tested_primes = 0
    for candidate in range(base, stop + 1):
        if prime(candidate):
            tested_primes += 1
            if gcd(candidate, forbidden_product) == 1:
                return candidate, tested_primes, candidate - base + 1
    return None, tested_primes, stop - base + 1


def main():
    parameter_cases = 0
    admitted = 0
    for width in [64, 128, 256, 512, 1024, 2048, 4096]:
        for batch_bits in [0, 4, 16, 64, 256]:
            batch = 1 << batch_bits
            for product_bits in [1, 4, 16, 64, 1024, 4096]:
                t = batch.bit_length() + 3 * product_bits.bit_length() + 3 * width.bit_length() + 10
                parameter_cases += 1
                if width < 4 * t:
                    continue
                admitted += 1
                exponent = width // t
                base = ceil_power_root(width, exponent)
                assert exponent >= 4
                assert base > batch and base >= 4 * exponent + 4
                assert base**2 >= (16 * (product_bits + 1) * exponent) ** 5
                assert (base - 1) ** exponent < 1 << width <= base**exponent
                assert (base + base // (2 * exponent)) ** exponent < 3 * (1 << width)

    witnesses = []
    for radix_bits, excluded_count, exponent in [(15, 0, 4), (18, 1, 4), (20, 3, 4), (25, 7, 4), (20, 1, 5)]:
        width = radix_bits * exponent
        base = ceil_power_root(width, exponent)
        assert base == 1 << radix_bits
        assert base**2 >= (16 * (excluded_count + 1) * exponent) ** 5
        excluded = []
        candidate = base
        while len(excluded) < excluded_count:
            if prime(candidate):
                excluded.append(candidate)
            candidate += 1
        forbidden = prod(excluded)
        selected, checked_primes, checked_integers = compatible_search(base, exponent, forbidden)
        assert selected is not None
        assert selected >= base and selected <= base + base // (2 * exponent)
        assert gcd(selected, forbidden) == 1 and prime(selected)
        assert checked_primes == excluded_count + 1
        assert 1 << width <= selected**exponent < 3 * (1 << width)
        inflation = Fraction(selected ** (2 * exponent), 1 << (2 * width))
        assert inflation < 9
        witnesses.append({
            "binary_width": width,
            "radix_digits": exponent,
            "interval_base": base,
            "excluded_primes": excluded,
            "compatibility_product": str(forbidden),
            "selected_prime": selected,
            "prime_tests_reaching_compatibility": checked_primes,
            "integers_examined": checked_integers,
            "two_field_inflation_exact": str(inflation),
            "two_field_inflation_illustration": float(inflation),
        })

    # Exhaustion is handled honestly. The small interval [64,72] has both
    # of its primes forbidden; it does not meet the sufficient size bound.
    missing, checked, _ = compatible_search(64, 4, 67 * 71)
    assert missing is None and checked == 2

    slack_cases = 0
    slack_admitted = 0
    for width in [128, 256, 512, 1024]:
        for batch_bits in [0, 16, 64]:
            batch = 1 << batch_bits
            for product_bits in [1, 16, 64]:
                for slack_h in [1, 2, 8]:
                    slack_cases += 1
                    t = batch.bit_length() + 3 * product_bits.bit_length() + 3 * width.bit_length() + 3 * slack_h.bit_length() + 13
                    if width < 4 * t:
                        continue
                    slack_admitted += 1
                    exponent = width // t
                    base = ceil_power_root(width, exponent)
                    assert exponent >= 4
                    assert base >= 8 * exponent * slack_h + 2
                    assert base >= (batch + 1) * slack_h
                    assert base**2 >= (32 * (product_bits + 1) * exponent * slack_h) ** 5
                    top = base + base // (4 * exponent * slack_h)
                    assert slack_h * top**exponent <= (slack_h + 1) * (1 << width)
                    total_padding = Fraction(top**(2 * exponent), 1 << (2 * width)) * Fraction(batch * ((top + batch - 1) // batch), top)
                    assert total_padding <= Fraction(slack_h + 1, slack_h) ** 3

    slack_witnesses = []
    for slack_h, radix_bits in [(1, 18), (2, 20), (4, 23), (8, 25), (16, 28)]:
        exponent = 4
        width = radix_bits * exponent
        base = ceil_power_root(width, exponent)
        batch = base // slack_h - 1
        assert base >= (batch + 1) * slack_h
        assert base >= 8 * exponent * slack_h + 2
        assert base**2 >= (32 * exponent * slack_h) ** 5
        selected, checked, examined = compatible_search(base, exponent, 1, slack_h)
        assert selected is not None and checked == 1 and prime(selected)
        assert slack_h * selected**exponent <= (slack_h + 1) * (1 << width)
        two_field = Fraction(selected**(2 * exponent), 1 << (2 * width))
        first_digit = Fraction(batch * ((selected + batch - 1) // batch), selected)
        assert first_digit <= Fraction(slack_h + 1, slack_h)
        assert two_field * first_digit <= Fraction(slack_h + 1, slack_h) ** 3
        slack_witnesses.append({"h": slack_h, "binary_width": width, "radix_digits": exponent, "batch_width": batch, "selected_prime": selected, "integers_examined": examined, "combined_padding_illustration": float(two_field * first_digit)})

    output = {
        "status": "finite_exact_checks_passed",
        "parameter_cases": parameter_cases,
        "admitted_parameter_cases": admitted,
        "prime_witness_cases": len(witnesses),
        "exhaustion_negative_controls": 1,
        "slack_selector_cases": slack_cases,
        "slack_selector_admitted": slack_admitted,
        "slack_prime_witness_cases": len(slack_witnesses),
        "scope": "integer-root/threshold inequalities, exact primality and compatibility, constant padding volume, finite failure flag",
        "not_verified": ["BHP threshold", "template generation cost", "uniform address-map implementation", "new multiplication bound"],
        "witnesses": witnesses,
        "slack_witnesses": slack_witnesses,
    }
    Path(__file__).with_name("dynamic-radix-verification.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k not in ["witnesses", "slack_witnesses"]}, indent=2))


if __name__ == "__main__":
    main()
