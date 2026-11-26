"""Exact integer and interval checks for the native piecewise Walsh transfer."""

from fractions import Fraction as F
from pathlib import Path
import json
import runpy


log_two_interval = runpy.run_path(
    str(Path(__file__).with_name("routing-outer-threshold.py"))
)["log_two_interval"]

ROOT_DEGREE = 240
HISTORICAL_BOUND = 2_220_000_000_000
CALLER_ADD = (1 << 25) + 220
LOCAL_COEFFICIENT = F(33, 4)
FINAL_SLOPE = F(17, 32768)


def native_breakpoints():
    edges = [(0, F(1, 2)),
             (ROOT_DEGREE * (2**17 + 2), F(17, 64))]
    for j in range(5, 14):
        y = ROOT_DEGREE * ((3 * j + 6) * 8**j + 2)
        edges.append((y, F(17, 4 * 2**j)))
    height = F(0)
    result = []
    for i, (y, slope) in enumerate(edges):
        if i:
            previous, previous_slope = edges[i - 1]
            height += previous_slope * (y - previous)
        result.append((y, slope, height))
    return result


def endpoint_comparison(z, intercept, log_bound):
    factor = (z + 2)**2 * log_bound
    left = (F(z, 1000) - CALLER_ADD - HISTORICAL_BOUND,
            F(z, 1000) - CALLER_ADD - intercept - FINAL_SLOPE * (z + 2))
    return tuple(
        residue > 0 and residue**3 > coefficient**3 * factor
        for residue, coefficient in zip(left, (48, LOCAL_COEFFICIENT))
    )


def sign(z, intercept):
    lower, upper = log_two_interval(z + 4)
    if all(endpoint_comparison(z, intercept, upper)):
        return 1
    assert not all(endpoint_comparison(z, intercept, lower))
    return -1


def check():
    edges = native_breakpoints()
    assert all(value <= HISTORICAL_BOUND for _, _, value in edges[:-1])
    y, slope, height = edges[-1]
    assert (y, slope, height) == (5_937_362_789_990_880, FINAL_SLOPE,
                                  7_096_092_733_680)
    assert (y + 2)**8 > 2**419
    assert 8 * (4 * (height - HISTORICAL_BOUND))**3 < 159**3 * y**2 * 419
    intercept = height - y * slope
    assert intercept == F(4_112_174_977_105_665, 1024)

    clean = 11_700_000_000_000_000
    assert (clean + 4).bit_length() == 54
    assert all(endpoint_comparison(clean, intercept, F(54)))
    assert 70_000**3 * 53 > clean

    lower, upper = y, clean
    assert sign(lower, intercept) == -1 and sign(upper, intercept) == 1
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if sign(middle, intercept) > 0:
            upper = middle
        else:
            lower = middle
    assert sign(upper - 1, intercept) < 0 and sign(upper, intercept) > 0
    return {
        "root_degree": ROOT_DEGREE,
        "breakpoints": len(edges),
        "last_breakpoint": y,
        "last_height": int(height),
        "historical_upper_bound": HISTORICAL_BOUND,
        "simple_loglog_threshold": clean,
        "first_integer_for_two_invoices": upper,
        "improvement_over_smooth_threshold": 18_536_231_398_600_959 - upper,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
