"""Rational enclosures for the full historical Walsh profile and both integer endpoints."""
from fractions import Fraction as F
from functools import cache
from itertools import count
from pathlib import Path
import json
import runpy


log_interval = cache(runpy.run_path(str(Path(__file__).with_name(
    "routing-outer-threshold.py")))["log_two_interval"])
R = 240
GAMMA = F(33, 4)
SURPLUS_COEFF = 48 - GAMMA
GRID = 1 << 80


def icbrt(n):
    if n < 2:
        return n
    v = 1 << ((n.bit_length() + 2) // 3)
    while True:
        w = (2*v + n//(v*v)) // 3
        if w >= v:
            assert v**3 <= n < (v+1)**3
            return v
        v = w


@cache
def phi(x):
    lower, upper = log_interval(x+2)
    a = x*x*GRID**3
    lo = icbrt(a*lower.numerator//lower.denominator)
    hi = icbrt(a*upper.numerator//upper.denominator) + 1
    return F(lo, GRID), F(hi, GRID)


def cap(j, stage):
    q = 3*j + (3*j+2).bit_length() + 2
    return R*(stage*q*8**j+2)


def facets():
    yield 0, F(1, 2)
    yield R*(2**17+2), F(17, 64)
    for j in count(4):
        for stage, slope in [(1, F(17, 4)), (2, F(11, 3)), (4, F(10, 3))]:
            if j != 4 or stage > 1:
                yield cap(j, stage), slope/2**j


def shape(x):
    previous, slope, height = 0, F(0), F(0)
    vertices = []
    for edge, right_slope in facets():
        if edge > x:
            break
        height += slope*(edge-previous)
        vertices.append((edge, height))
        previous, slope = edge, right_slope
    if previous != x:
        vertices.append((x, height+slope*(x-previous)))
    return vertices


def surplus_interval(x, h):
    plo, phi_hi = phi(x)
    return h - SURPLUS_COEFF*phi_hi, h - SURPLUS_COEFF*plo


def history(x):
    vertices = shape(x)
    intervals = [surplus_interval(v, h) for v, h in vertices]
    lo = max(F(0), max(s[0] for s in intervals))
    hi = max(F(0), max(s[1] for s in intervals))
    active_now = intervals[-1][0] > max(F(0), max(s[1] for s in intervals[:-1]))
    return lo, hi, active_now, len(vertices)-1


def excess(z, legacy):
    """Bounds on the raw log invoice including a bit for the natural-log source."""
    x = z+2
    slo, shi, current, corners = history(x)
    pl, ph = phi(x)
    if legacy:
        assert z+4 < 1 << 54
        al = ah = F((1 << 25)+220)
    else:
        ll, lh = log_interval(z+2)
        al, ah = 183+4*ll, 183+4*lh
    return (al+48*pl+slo, ah+48*ph+shi), current, corners


def sign(z, legacy):
    (lo, hi), _, _ = excess(z, legacy)
    target = F(z, 1000)
    if hi < target:
        return 1
    assert lo > target, "refine the logarithm or cube-root enclosure"
    return -1


def crossing(legacy):
    lower, upper = 8*10**15, 10**16
    assert sign(lower, legacy) < 0 < sign(upper, legacy)
    while lower+1 < upper:
        middle = (lower+upper)//2
        if sign(middle, legacy) < 0:
            lower = middle
        else:
            upper = middle
    (lo, _), curr_lo, _ = excess(lower, legacy)
    (_, hi), curr_hi, corners = excess(upper, legacy)
    assert curr_lo and curr_hi
    assert 0 < lo-F(lower, 1000) and 0 < F(upper, 1000)-hi
    return {"first_passing": upper, "last_failing": lower, "earlier_corners": corners,
            "current_dominates": curr_hi, "previous_gap_over_1e_9":
            int((lo-F(lower,1000))*10**9), "passing_gap_over_1e_9":
            int((F(upper,1000)-hi)*10**9)}


if __name__ == "__main__":
    old = crossing(True)
    new = crossing(False)
    assert old["first_passing"] == 8_931_803_133_527_017
    assert new["first_passing"] == 8_931_714_897_907_030
    print(json.dumps({"same_large_fixed_allowance": old, "small_high_branch_allowance": new,
                      "coarse_endpoint": 9_000_000_000_000_000,
                      "original_endpoint_reduction": 11_665_715_140_844_862-old["first_passing"]},
                     indent=2))
