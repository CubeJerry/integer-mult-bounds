"""Eight-class independent arithmetic check of the depth-27 relaxation.

No import of the primary optimization, its greedy allocator, its census or
the integer lift. The eight classes are proved in INDEPENDENT_REVIEW.md.
Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""

import json
from fractions import Fraction


def require(value, message):
    if not value:
        raise ValueError(message)


def check():
    a = Fraction(51_008_161, 50_979_600)
    d = Fraction(50_983_170, 50_979_600)
    require(1 < d and d**3 < a, "two-level allocation premise")
    base = 3*a + 12*a*a
    classes = [
        (0, [15]),
        (1, [7, 8]),
        (2, [7, 0, 8]),
        (2, [3, 8, 4]),
        (3, [7, 0, 0, 8]),
        (3, [3, 4, 4, 4]),
        (3, [3, 0, 12, 0]),
        (3, [1, 6, 6, 2]),
    ]
    values = []
    for count, histogram in classes:
        require(sum(histogram) == 15, "nonzero-domain count")
        require(sum(i*n for i, n in enumerate(histogram)) == 8*count,
                "functional incidence count")
        extra = 12 - count
        value = Fraction(0)
        for incidence, number in enumerate(histogram):
            selected = min(extra, number)
            extra -= selected
            value += (selected*a*a + (number-selected)*a) * d**incidence
        require(extra == 0, "allocation exhausted")
        require(value == base if count == 0 else value > base, "eight-class minimum")
        values.append({"y": count, "histogram": histogram,
                       "gap_numerator": (value-base).numerator,
                       "gap_denominator": (value-base).denominator})
    require(d**8 > a, "AM-GM monotonicity")
    require(15**15 * a**23 * d**32 > base**15, "AM-GM at first omitted class")
    # The losing one-full-rank-block class makes the sharpness check
    # discriminate a proposed upward shift in the claimed optimum.
    losing = base + Fraction(values[1]["gap_numerator"], values[1]["gap_denominator"])
    require(base < losing, "nonoptimal one-full-rank candidate rejected")
    return {"schema": "depth27-eight-histogram-audit-v1", "classes": values,
            "positive_y_classes": 7, "tail": "all integer y>=4 through27",
            "method": "closed rank/multiplicity classification; exact two-level exchange"}


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
    print("PASS_INDEPENDENT_EIGHT_HISTOGRAMS")
