#!/usr/bin/env python3
"""Exact checks of finite parameter formulas; no enormous label sets built."""
from math import isqrt
import json
from pathlib import Path


def ceil_log2(n):
    return (n - 1).bit_length()


def ceil_sqrt_ratio(a, b):
    c = isqrt(a // b)
    return c + (c * c * b < a)


def main():
    records = []
    for u in [16, 32, 64, 256, 1024, 65536, 131072, 1048576]:
        for side, m in [("lower", (1 << (u - 1)) + 1),
                        ("upper", (1 << u) - 1)]:
            assert ceil_log2(m) == u and m % 2 == 1
            v = ceil_log2(u + 2)
            ell = 2 * ceil_sqrt_ratio(u, v)
            q_log = 2 + (2 * u + ell - 1) // ell
            q = 1 << q_log
            dim = 1 + ell * q
            pencil = 10 * dim * (1 + q_log) ** ell
            labels = 1 << (q_log * ell)
            assert labels <= 4 * m * m * (1 << (3 * ell))
            assert m * (1 << ell) <= 1 << (q_log * (ell // 2))
            seed_log = ceil_log2(m + 1)
            depth = (u + 3) // 4
            width_log = seed_log + q_log * ell + 3 * depth
            # Width is exactly a power of two, not an approximate batch count.
            for extra in [0, 1, 7, 101]:
                assert (1 << (width_log + extra)) % (1 << width_log) == 0
            if u >= 65536:
                assert v * 256 <= u
                crude = 8 + v + 5 * (isqrt(u * v) + 1)
                assert pencil.bit_length() <= crude
                assert crude < u - 1
                assert pencil <= m and dim <= m and labels <= m ** 3
            records.append({"ceil_log2_m": u, "side": side,
                            "L": ell, "log2_q": q_log,
                            "log2_batch_width": width_log,
                            "pencil_bound_bits": pencil.bit_length(),
                            "pencil_bound_below_m": pencil <= m,
                            "label_bound_below_m_cubed": labels <= m ** 3})
    # A negative control: the convenient R_m<=m simplification is not valid
    # at every small parameter. It must have a threshold or a direct fallback.
    assert any(not x["pencil_bound_below_m"] for x in records)
    return {"status": "passed", "scope": "Integer parameter and threshold formulas, not spatial routing execution",
            "cases": records, "negative_small_parameter_control": "rejected unqualified R_m<=m"}


if __name__ == "__main__":
    result = main()
    Path(__file__).with_name("routing-parameter-verification.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(result["cases"]),
                      "scope": result["scope"],
                      "negative_control": result["negative_small_parameter_control"]}, indent=2))
