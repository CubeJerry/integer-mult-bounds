"""Independently certify the whole-integer crossover with binary logarithm digit extraction."""
from fractions import Fraction as F
import json


def log2_bounds(n, digits=112, scratch_width=400):
    """Outward fixed-grid interval with exact, certified log-base-two bit decisions."""
    k = n.bit_length() - 1
    unit = 1 << scratch_width
    numerator = n * unit
    denominator = 1 << k
    lower = numerator // denominator
    upper = -(-numerator // denominator)
    fraction = 0
    for _ in range(digits):
        lower = lower * lower // unit
        upper = -(-(upper * upper) // unit)
        fraction <<= 1
        if lower >= 2 * unit:
            fraction |= 1
            lower //= 2
            upper = -(-upper // 2)
        else:
            assert upper < 2 * unit, "actual next logarithmic digit is not resolved on this grid"
    base = 1 << digits
    return F(k * base + fraction, base), F(k * base + fraction + 1, base)


def amounts():
    y = 240 * ((1 << 17) + 2)
    h = F(y, 2)
    height_before_final = 0
    for j in range(4, 13):
        z = 240 * ((3 * (j + 1) + 6) * (1 << (3 * (j + 1)))) + 480
        if j == 12:
            height_before_final = h
        h += F(17, 4 * (1 << j)) * (z - y)
        y = z
    assert (height_before_final, y, h) == (1654234951920, 5937362789990880, 7096092733680)
    alpha = F(17, 32768)
    beta = h - alpha * y
    lower, upper = log2_bounds(y + 2)
    cap = 2220000000000
    assert (h - cap) ** 3 < F(159, 4) ** 3 * y * y * lower
    assert beta == F(4112174977105665, 1024)
    return alpha, beta, cap


def compare(z):
    alpha, beta, cap = amounts()
    scale = F(z, 1000) - (1 << 25) - 220
    targets = (scale - cap, scale - beta - alpha * (z + 2))
    powers = (F(48), F(33, 4))
    lo, hi = log2_bounds(z + 4)
    signs = []
    for target, c in zip(targets, powers):
        assert target > 0
        if target ** 3 > c ** 3 * (z + 2) ** 2 * hi:
            signs.append(1)
        else:
            assert target ** 3 < c ** 3 * (z + 2) ** 2 * lo
            signs.append(-1)
    return tuple(signs)


def main():
    # Check the binary logarithm enclosure against exact powers of two.
    for k in range(1, 122, 7):
        lo, hi = log2_bounds(1 << k)
        assert lo == k and hi > k
    left = 11665715140844862
    results = [compare(t) for t in (left - 1, left, 11700000000000000)]
    assert results == [(1, -1), (1, 1), (1, 1)]
    print(json.dumps(dict(guard=left, prior=results[0], at=results[1], rounded=results[2],
                          log_bits=112, square_grid_bits=400, historical_cap=2220000000000),
                     sort_keys=True))


if __name__ == "__main__":
    main()
