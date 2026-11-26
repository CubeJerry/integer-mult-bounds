"""The three frozen label-slope pieces and their two adjacent clock signs."""
from fractions import Fraction as F
from itertools import count
from pathlib import Path
import json
import runpy

previous = runpy.run_path(str(Path(__file__).with_name("routing-refined-walsh.py")))
phi = previous["phi"]
log_interval = previous["log_interval"]
SURPLUS = F(159, 4)
Z = 7_519_517_465_920_988
SIMPLE = 7_600_000_000_000_000
HEIGHT_CAP = 630_000_000_000
ANCHOR = 6_201_245_580_657_120


def q(j):
    return 3*j+(3*j+2).bit_length()+2


def e_upper(j):
    return F(j+(8*q(j+1)).bit_length()+3, q(j))


def edges():
    yield 0, F(1, 2)
    yield 240*(2**17+2), (3+e_upper(4))/16
    for j in count(4):
        for a in (1, 2, 4):
            if j == 4 and a == 1:
                continue
            yield 240*(a*q(j)*8**j+2), (3+e_upper(j)/a)/2**j


def vertices(x):
    height = F(0)
    prev, slope = 0, F(0)
    for start, next_slope in edges():
        if start > x:
            break
        height += slope*(start-prev)
        yield start, height, next_slope
        prev, slope = start, next_slope
    if prev != x:
        yield x, height+slope*(x-prev), slope


def check_adjacent(z):
    data = list(vertices(z+2))
    intervals = []
    for x, h, _ in data:
        lower, upper = phi(x)
        intervals.append((h-SURPLUS*upper, h-SURPLUS*lower, x))
    lower, upper, arg = max(intervals)
    assert arg == ANCHOR
    assert all(a_high < lower for _, a_high, v in intervals if v != ANCHOR)
    pl, ph = phi(z+2)
    ll, lh = log_interval(z+2)
    residual = (F(z,1000)-183-4*lh-48*ph-upper, F(z,1000)-183-4*ll-48*pl-lower)
    return residual, data, (lower,upper)


def simple():
    for x, height, _ in vertices(SIMPLE+2):
        floorlog = (x+2).bit_length()-1
        assert height <= HEIGHT_CAP or (height-HEIGHT_CAP)**3 <= SURPLUS**3*x*x*floorlog
    assert SIMPLE+4 < 1 << 53
    residual = F(SIMPLE,1000)-(183+4*53)-HEIGHT_CAP
    assert residual > 0 and residual**3 > 48**3*(SIMPLE+2)**2*53


if __name__ == "__main__":
    simple()
    lost, low_data, _ = check_adjacent(Z-1)
    won, high_data, hot = check_adjacent(Z)
    assert 0 < won[0] and lost[1] < 0
    assert len(low_data) == len(high_data) == 30
    h_anchor = next(h for x,h,_ in high_data if x == ANCHOR)
    assert h_anchor == F(890362700843914785456,158055205)
    assert 177**2 <= 2**16 and 185**2 <= 2*177**2
    print(json.dumps({"endpoint": Z, "last_failing": Z-1, "simple_endpoint": SIMPLE,
                      "active_historical_knot": ANCHOR, "height": str(h_anchor),
                      "earlier_vertices": len(high_data)-1, "historical_upper_integer": -(-hot[1]//1),
                      "passing_gap_above_trillionths": int(won[0]*10**12),
                      "previous_gap_above_trillionths": int(-lost[1]*10**12),
                      "reduction_from_previous_endpoint": 8_931_714_897_907_030-Z}, indent=2))
