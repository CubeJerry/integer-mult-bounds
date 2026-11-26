"""Exact-rational checks for the two global binary interchange potentials."""
from fractions import Fraction as Q
from pathlib import Path
from random import Random
from runpy import run_path
import json

HERE = Path(__file__).parent
CHILD = run_path(str(HERE / "check-child-volume.py"))
R = 4096
START = R * ((1 << 17) + 2)


def switch(j):
    return R * ((3 * j + 6) * (1 << (3 * j)) + 2)


def slope(j):
    return Q(17, 4 * (1 << j))


# Each row is the left edge and slope in the interval beginning there.
intervals = [(0, Q(1, 2)), (START, slope(4))]
intervals.extend((switch(j), slope(j)) for j in range(5, 14))


def integral(y):
    total = Q(0)
    for pos, (begin, rate) in enumerate(intervals):
        if y <= begin:
            break
        end = min(y, intervals[pos + 1][0]) if pos + 1 < len(intervals) else y
        total += rate * (end - begin)
    return total


def rate_at(y):
    return next(rate for begin, rate in reversed(intervals) if y >= begin)


def check_smooth():
    lower, upper = Q(31, 64), Q(33, 32)
    assert Q(34, 37) > (2 * lower) ** 3
    assert 1 + Q(1, 1 << 17) <= upper ** 3
    assert 2 * Q(20, 17) * upper ** 3 < 3
    coeff = Q(33, 4096) + 3 / lower + Q(20, 17) * lower ** 2
    assert coeff == Q(13982555, 2158592) < Q(13, 2)
    assert 156 == Q(3, 2) * Q(13, 2) * 16 and 16 ** 3 == R
    assert Q(8, 3) * Q(13, 2) == Q(52, 3) > 2
    assert (2 * 156) ** 3 >= 1 << 24
    assert 24 * (2 * 156) ** 3 >= START
    assert 9 * 512 + 512 == 5120
    assert 9 * (1 << 18) + 128 == 2359424
    return coeff


def check_stairs():
    assert Q(37, 4096) < Q(5, 68)
    assert all(after[1] < before[1] for before, after in zip(intervals, intervals[1:]))
    for j in range(5, 14):
        begin = (3 * j + 6) * (1 << (3 * j))
        assert CHILD["geometry"](begin)[1] >= 1 << j
        v0 = 3 * j + 7
        assert (1 << (v0 - 1)) - 2 >= v0 * (1 << (3 * j))
    y13 = switch(13)
    h13 = integral(y13)
    assert (y13, h13) == (101330991615844352, 121106649321472)
    cut = (h13 - slope(13) * y13 + 13) / (Q(1, 1000) - slope(13))
    integer = -(-cut.numerator // cut.denominator)
    assert cut == Q(93574826145711104000, 657)
    assert integer == 142427437055876871 < 1 << 57
    assert integral(integer) + 13 <= Q(integer, 1000)
    assert integral(integer - 1) + 13 > Q(integer - 1, 1000)

    rng = Random(99831)
    widths = {START, integer, 1 << 57}
    for begin, _ in intervals[1:]:
        widths.update(begin + delta for delta in (-2, -1, 0, 1, 2) if begin + delta >= START)
        widths.update(begin + rng.randrange(1, 2 * begin) for _ in range(80))
    checked = 0
    for y in widths:
        for shift in (Q(y, R) - 1, Q(y, R), Q(y), Q(y, 2)):
            assert integral(y) - integral(y - shift) >= rate_at(y) * shift
            checked += 1
    return integer, checked


def check_literal_invoice():
    base = 1 << 17
    probes = {base, base + 1}
    for power in range(17, 150):
        probes.update(max(base, (1 << power) + delta) for delta in range(-2, 4))
    for j in range(4, 47):
        for v in range(10, 175):
            point = (1 << (3 * j)) * v
            if abs(CHILD["clog"](point + 2) - v) <= 1:
                probes.update(p for p in (point - 1, point, point + 1) if p >= base)
    for u in probes:
        _, d, _ = CHILD["geometry"](u)
        charge = CHILD["certificate"](u)
        lo = u - 1
        # This integer is no greater than log2(s+2), even at the lower edge.
        lower_log = (u + 1).bit_length() - 1
        assert (2 * charge) ** 3 <= 13 ** 3 * lo ** 2 * lower_log
        assert 4 * d * (charge + 2) <= 17 * lo
    return len(probes)


def main():
    coefficient = check_smooth()
    crossing, comparisons = check_stairs()
    print(json.dumps(dict(native_mass_comparison=str(coefficient), native_B=156, A_I=5120,
                          direct_threshold_log=START, last_stair=switch(13),
                          last_stair_value=int(integral(switch(13))),
                          unit_power_threshold_log=crossing, concavity_probes=comparisons,
                          literal_rounded_parameter_probes=check_literal_invoice()),
                     sort_keys=True))


if __name__ == "__main__":
    main()
