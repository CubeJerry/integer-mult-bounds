#!/usr/bin/env python3
"""Scoped exact algebra and finite Decimal evidence; no machine lower bound."""
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import platform


def floor_cuberoot(n):
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return hi if hi ** 3 <= n else lo


def main():
    counts = dict(concavity_discriminants=0, local_cubic_contrapositions=0,
                  regular_normalized_prices=0, nonstationary_partitions=0,
                  negative_controls=0)
    for denominator in range(1, 17):
        for numerator in range(1, 129):
            x = Fraction(numerator, denominator)
            disc = x * x * ((x + 8) ** 2 - 16 * (x + 2) ** 2)
            assert disc == -3 * x ** 3 * (5 * x + 16) < 0
            counts['concavity_discriminants'] += 1

    # x=log2(m) is represented; m itself is never constructed.
    for exponent in range(24, 513):
        x = 1 << exponent
        bound_cubed = Fraction(x * x * exponent, 512)
        b = max(1, floor_cuberoot(bound_cubed.numerator // bound_cubed.denominator) - 1)
        assert b ** 3 < bound_cubed
        assert b ** 4 < x ** 3
        j = Fraction(x, b)
        assert j >= 64 and j ** 4 > x
        # log2(j)>=exponent/4 would force the opposite NI1 inequality.
        assert j ** 3 * Fraction(exponent, 512) > x
        counts['local_cubic_contrapositions'] += 1

    for power in range(1, 33):
        m, sm = 1 << (2 * power), 1 << power
        invoice = 3 + power
        child = 1 << (power + 7)
        for c0, factor in ((1, 1), (4, 2), (9, 3), (16, 4), (6, 8)):
            parent = c0 * m * child
            mass = factor * sm * invoice
            normalized_squared = Fraction(mass * mass * child, parent)
            assert normalized_squared >= invoice * invoice
            counts['regular_normalized_prices'] += 1

    ratios = []
    with localcontext() as context:
        context.prec = 100
        ln2 = Decimal(2).ln()

        def g(x):
            if x == 0:
                return Decimal(0)
            z = Decimal(x)
            return (z * z * (z + 2).ln() / ln2) ** (Decimal(1) / 3)

        for power in range(4, 129, 4):
            root = 1 << power
            partitions = [[root], [root // 2, root - root // 2]]
            for denominator in (2, 4, 16):
                remaining, parts = root, []
                while remaining > 1:
                    step = max(1, remaining // denominator)
                    parts.append(step)
                    remaining -= step
                parts.append(remaining)
                partitions.append(parts)
            for parts in partitions:
                assert sum(parts) == root and all(x > 0 for x in parts)
                total = sum((g(x) for x in parts), Decimal())
                target = g(root)
                assert total >= target - Decimal('1e-70') * target
                ratios.append(total / target)
                counts['nonstationary_partitions'] += 1
        assert 2 * g(8) > g(16)  # Reversing subadditivity is false.
        counts['negative_controls'] += 1

    # Log-drop<=2 log(m) alone does not preserve the sqrt-normalized price.
    m, sm, invoice, factor = 1 << 128, 1 << 64, 1 << 8, 8
    parent, child = m * m, 1
    mass = factor * sm * invoice
    assert Fraction(mass * mass * child, parent) < 1
    counts['negative_controls'] += 1
    # Even a regular split needs its constant normalization loss paid.
    assert Fraction((sm * invoice) ** 2, 6 * m) < invoice ** 2
    counts['negative_controls'] += 1

    source = Path(__file__)
    result = dict(status='pass', scope='Literal invoice implications and finite recurrence diagnostics; no actual-machine lower bound.',
                  counts=counts, decimal_precision=100,
                  minimum_partition_ratio=float(min(ratios)),
                  maximum_partition_ratio=float(max(ratios)),
                  python=platform.python_version(),
                  checker_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  limitations=['No label family is instantiated in the large-m inverse checks.',
                               'Decimal partition checks are evidence, not interval-certified calculus.',
                               'The fast-descent countermodel tests logical hypotheses, not realizability by the source labels.'])
    source.with_name('nonstationary-invoice-barrier-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
