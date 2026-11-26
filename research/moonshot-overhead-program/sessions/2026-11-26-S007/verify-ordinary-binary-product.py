#!/usr/bin/env python3
"""Replay two literal FS1 transforms, modular products, and the returned ordinary product."""
from collections import Counter
from pathlib import Path
from random import Random
import json
import runpy

plane = runpy.run_path(str(Path(__file__).with_name("verify-plane-independent.py")))
poly_div = plane["poly_div"]
poly_mul = plane["poly_mul"]


def grid_forward(ctx, operand):
    grids = {}
    for anchor in ctx.planes:
        remainder = plane["literal_plane_remainder"](ctx, operand, anchor)
        grids[anchor] = plane["plane_forward"](ctx, anchor, remainder)
    return grids


def grid_inverse(ctx, grid_values):
    planes = {t: plane["plane_inverse"](ctx, t, values) for t, values in grid_values.items()}
    return ctx.join_scalar_planes(planes)


def check_inventory(ctx):
    b = 3 * ctx.c
    by_degree = Counter(h.bit_length() - 1 for h in ctx.moduli)
    expected_counts = {}
    for degree in range(1, b + 1):
        if b % degree == 0:
            smaller = sum(d * count for d, count in expected_counts.items() if degree % d == 0)
            mass = (1 << degree) - smaller
            assert mass % degree == 0
            expected_counts[degree] = mass // degree
    assert by_degree == expected_counts
    assert len(set(ctx.moduli)) == len(ctx.moduli)
    assert sum(d * count for d, count in by_degree.items()) == ctx.q
    product = 1
    for h in ctx.moduli:
        d = h.bit_length() - 1
        x = poly_div(2, h)[1]
        square = x
        for step in range(1, d + 1):
            square = poly_div(poly_mul(square, square), h)[1]
            if step <= d // 2:
                assert plane["AR"]["gcd_binary"](h, square ^ x) == 1
        assert square == x
        product = poly_mul(product, h)
    assert product == (1 << ctx.q) | 2
    return {"b": b, "q": ctx.q, "factor_count": len(ctx.moduli),
            "counts_by_degree": dict(sorted(by_degree.items())),
            "factor_coefficients_hex_in_FS1_order": [hex(h) for h in ctx.moduli],
            "inventory_product_nonzero_degrees": [1, ctx.q]}


def reference_product(f, g, n):
    # Ordinary integer multiplication of separated bits computes exact nonnegative
    # convolution counts, all strictly below the base. Take parity coefficientwise.
    guard = n.bit_length()
    def expand(value):
        return sum(((value >> i) & 1) << (guard * i) for i in range(n))
    products = expand(f) * expand(g)
    return sum(((products >> (guard * i)) & 1) << i for i in range(2*n - 1))


def main():
    rng = Random(0xAB170)
    counts = Counter()
    roots = []
    inventories = []
    for c in range(1, 5):
        ctx = plane["Context"](c)
        b = 3*c
        inventories.append(check_inventory(ctx))
        for n in sorted({max(1, ctx.q//16 + 1), ctx.q//2 - 1, ctx.q//2}):
            least_root_degree = max(3, 3 * (((2*n - 2).bit_length() + 2)//3))
            assert least_root_degree == b
            leading_and_one = (1 << (n - 1)) | 1
            inputs = [(rng.getrandbits(n), rng.getrandbits(n)), (leading_and_one, leading_and_one)]
            if c < 3:
                inputs.extend([(0, rng.getrandbits(n)), ((1 << n) - 1, 1)])
            for f, g in inputs:
                fgrid, ggrid = grid_forward(ctx, f), grid_forward(ctx, g)
                direct = {}
                for t in ctx.planes:
                    direct[t] = [[ctx.field.mul(v, w) for v, w in zip(frow, grow)]
                                 for frow, grow in zip(fgrid[t], ggrid[t])]
                direct_result = grid_inverse(ctx, direct)
                expected = reference_product(f, g, n)
                assert direct_result == expected
                assert direct_result.bit_length() <= 2*n - 1 <= ctx.q
                counts["direct_grid_products_without_factor_directory"] += 1
                counts["selected_field_word_products"] += len(ctx.planes) * ctx.h
                counts["direct_inverse_root_grid_transforms"] += 1
                xs, ys = ctx.canonical_residues(fgrid), ctx.canonical_residues(ggrid)
                zs = [poly_div(poly_mul(v, w), h)[1] for h, v, w in zip(ctx.moduli, xs, ys)]
                result = grid_inverse(ctx, ctx.planes_from_residues(zs))
                assert result == expected
                assert result.bit_length() <= 2*n - 1 <= ctx.q
                counts["single_full_ordinary_binary_products"] += 1
                counts["full_forward_root_transforms"] += 2
                counts["full_inverse_root_transforms"] += 1
                counts["individual_modular_point_products"] += len(zs)
                counts["positions_recovered_before_truncation"] += ctx.q
            roots.append([n, b])
    print(json.dumps({"seed": "0xab170", "input_lengths_and_root_degrees": roots,
                      "counts": dict(sorted(counts.items())),
                      "actual_FS1_inventories": inventories}, indent=2))


if __name__ == "__main__":
    main()
