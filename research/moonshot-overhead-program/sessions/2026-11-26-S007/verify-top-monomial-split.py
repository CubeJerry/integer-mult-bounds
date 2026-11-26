#!/usr/bin/env python3
"""Check the dense top hyperplane, projected child, and pairwise support on finite fields."""

import json
import random
import runpy
from itertools import combinations
from pathlib import Path

shared = runpy.run_path(str(Path(__file__).with_name("verify-grouped-words.py")))
field_modulus = shared["field_modulus"]
pmul = shared["pmul"]
pdiv = shared["pdiv"]
powers_of_sigma = shared["powers_of_sigma"]
left_inverse = shared["left_inverse"]
evaluate_small = shared["horner"]


def lin_eval(coefficients, x, mul):
    result = 0
    for coefficient in coefficients:
        result ^= mul(coefficient, x)
        x = mul(x, x)
    return result


def lin_extension(old, direction, mul):
    gap = lin_eval(old, direction, mul)
    assert gap != 0
    result = [mul(gap, value) for value in old] + [0]
    for j, value in enumerate(old):
        result[j + 1] ^= mul(value, value)
    return gap, result


def factor_product_on_points(points, mul):
    polynomial = [1]
    for point in points:
        result = [0] * (len(polynomial) + 1)
        for i, value in enumerate(polynomial):
            result[i] ^= mul(value, point)
            result[i + 1] ^= value
        polynomial = result
    return polynomial


def array_span(elements):
    points = [0]
    for x in elements:
        points.extend([a ^ x for a in points])
    return points


def sparse_remainder(inputs, h, terms, mul):
    """Ordinary long division of X^h Q by a dense/linearized monic polynomial."""
    working = {j + h: value for j, value in inputs.items()}
    quotient = {}
    high_columns = sorted(working, reverse=True)
    for j in high_columns:
        top = working.get(j, 0)
        if not top:
            continue
        shift = j - h
        quotient[shift] = top
        for e, coeff in terms.items():
            k = shift + e
            working[k] = working.get(k, 0) ^ mul(coeff, top)
        assert working[j] == 0
    return quotient, {k: x for k, x in working.items() if x}


def run(b, counts):
    c = b // 3
    h = 1 << (2 * c)
    width = 2 * c + 1
    rng = random.Random(b * 20261126)
    modulus = field_modulus(b)
    def mul(x, y):
        return pdiv(pmul(x, y), modulus)[1]

    for _ in range(10000):
        gamma = rng.randrange(1, 1 << b)
        orbit = powers_of_sigma(gamma, b, mul)
        try:
            left_inverse(orbit, b)
        except ValueError:
            continue
        break
    else:
        raise AssertionError("no normal fixture in deterministic trial sequence")
    subbasis = [orbit[j] ^ orbit[j + c] ^ orbit[j + 2*c] for j in range(c)]
    section = array_span(subbasis)[::2]
    visited = set()
    groups = []
    for alpha in section:
        s = mul(alpha, alpha) ^ alpha
        if s in visited:
            continue
        x = s
        powers = []
        while x not in visited:
            visited.add(x)
            powers.append(x)
            x = mul(x, x)
        assert x == s
        embeddings = [1]
        for _ in range(1, len(powers)):
            embeddings.append(mul(embeddings[-1], s))
        groups.append((s, len(powers), embeddings))
    assert sum(g[1] for g in groups) == (1 << (c-1))
    def frob(x, k):
        for _ in range(k):
            x = mul(x, x)
        return x

    def pow_field(x, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = mul(result, x)
            x = mul(x, x)
            exponent >>= 1
        return result

    p_directions = [orbit[j] ^ orbit[j + c] for j in range(c)] + [
        orbit[j + c] ^ orbit[j + 2 * c] for j in range(c)]
    directions = [1] + p_directions
    left_inverse(directions, b)
    target_indices = {0, 1, c, c + 1, 2 * c, 2 * c + 1}
    trace_coefficients = [int(i in target_indices) for i in range(2 * c + 2)]
    excluded_sparse = [1]
    for x in p_directions:
        _, excluded_sparse = lin_extension(excluded_sparse, x, mul)
    assert [i for i, x in enumerate(excluded_sparse) if x] == [0, c, 2 * c]
    assert lin_eval(excluded_sparse, 1, mul) == 1
    assert lin_extension(excluded_sparse, 1, mul) == (1, trace_coefficients)
    counts["excluded_sparse_hyperplane_controls"] += 1

    possible_masks = range(4, 1 << width, 4)
    if b <= 12:
        masks = list(possible_masks)
    else:
        masks = sorted({4, 1 << (width - 1), *rng.sample(possible_masks, 8)})
    exceptional_masks = set()
    if c % 3 == 2:
        sub8_basis = [shared["xor_words"](orbit[i::3]) for i in range(3)]
        for t in array_span(sub8_basis):
            if not t or t ^ frob(t, c) ^ frob(t, 2*c):
                continue
            delta = frob(pow_field(t, (1 << b) - 2), b - 1)
            normalized = 0
            polynomial = []
            for i in range(2*c + 1):
                normalized = mul(normalized, normalized) ^ (t if i in target_indices else 0)
                polynomial.append(mul(delta, normalized))
            assert polynomial[c] == 0 and polynomial[-1] == 1
            image = [lin_eval(polynomial, x, mul) for x in directions]
            assert all(y in (0, delta) for y in image)
            real_mask = sum(int(value == delta) << j for j, value in enumerate(image))
            if real_mask in possible_masks:
                exceptional_masks.add(real_mask)
        assert len(exceptional_masks) in (1, 3)
        masks = sorted(set(masks).union(exceptional_masks))
    missing_centres = set()
    nonzero_lower = []
    seen_patterns = set()
    cut_values = []
    group_selection = range(len(groups)) if b <= 12 else {0, len(groups) - 1}
    output_indices = range((1 << c) + (1 - (1 << c)) % 3, h // 2, 3)
    for mask in masks:
        pivot = (mask & -mask).bit_length() - 1
        beta = directions[pivot]
        kernel_basis = [v ^ (beta if mask >> j & 1 else 0)
                        for j, v in enumerate(directions) if j != pivot]
        polynomial = [1]
        for x in kernel_basis:
            _, polynomial = lin_extension(polynomial, x, mul)
        delta, reconstructed = lin_extension(polynomial, beta, mul)
        assert delta != 1 and reconstructed == trace_coefficients
        assert polynomial[-1] == 1 and all(value for i, value in enumerate(polynomial) if i != c)
        inverse = pow_field(delta, (1 << b) - 2)
        t = mul(inverse, inverse)
        assert t ^ frob(t, c) ^ frob(t, 2*c) == 0 and t not in (0, 1)
        assert (polynomial[c] == 0) == (frob(t, c + 1) == t)
        if polynomial[c] == 0:
            missing_centres.add(mask)
        counts["central_coefficient_classifications"] += 1
        assert lin_eval(polynomial, 1, mul) == 0
        counts["verified_hyperplanes"] += 1
        nonzero_lower.append(sum(x != 0 for x in polynomial[:-1]))
        if b <= 9:
            direct = factor_product_on_points(array_span(kernel_basis), mul)
            expected = [0] * (h + 1)
            for i, value in enumerate(polynomial):
                expected[1 << i] = value
            assert direct == expected
            counts["direct_root_products"] += 1
        exponents = [i for i, x in enumerate(polynomial[:-1]) if x and i % 2 == 0]
        pattern = tuple(exponents)
        if pattern not in seen_patterns:
            seen_patterns.add(pattern)
            if len(output_indices) < 256:
                samples = list(output_indices)
            else:
                samples = sorted({output_indices[0], output_indices[-1], *rng.sample(output_indices, 56)})
            supports = [{n - (1 << i) for i in exponents if 0 <= n - (1 << i) < h // 2}
                        for n in samples]
            assert all(len(row) >= (c + 1) // 2 and all(x % 3 == 0 for x in row)
                       for row in supports)
            for left, right in combinations(supports, 2):
                assert len(left & right) <= 1
                counts["row_pair_intersections"] += 1
            counts["support_rows"] += len(supports)
        # The simple accounting bound can be zero at small c; record it only when positive.
        bound = (len(output_indices) * (((c + 1) // 2) * sum(g[1] for g in groups)
                                        - b * len(groups)))
        cut_values.append(max(0, (bound + 1) // 2))
        if b > 9 and mask not in (masks[0], masks[-1]):
            continue
        for group_index in sorted(group_selection):
            s, degree, embeddings = groups[group_index]
            # Recover an anchor in the S006 section by solving alpha^2+alpha=s.
            # The two solutions have the same top parent, and the code deliberately
            # checks both translated children when making this local projection.
            anchors = [x for x in array_span(subbasis) if mul(x, x) ^ x == s]
            assert len(anchors) == 2
            for scalar in {t for t in polynomial[:-1] if t}:
                columns = [mul(scalar, x) for x in embeddings]
                left_inverse(columns, b)
                counts["injective_word_scalings"] += 1
            available = range(0, h // 2, 3)
            chosen = list(available) if len(available) <= 24 else rng.sample(available, 24)
            inputs = {j: evaluate_small(rng.randrange(1, 1 << degree), s, mul) for j in chosen}
            for anchor in anchors:
                constant = lin_eval(polynomial, anchor, mul)
                terms = {1 << i: value for i, value in enumerate(polynomial) if value}
                if constant:
                    terms[0] = constant
                quotient, remainder = sparse_remainder(inputs, h, terms, mul)
                assert quotient == inputs
                if b <= 12:
                    sample_rows = output_indices
                else:
                    sample_rows = sorted({output_indices[0], output_indices[-1], *rng.sample(output_indices, 32),
                                          *[n for n in remainder if n in output_indices]})
                for n in sample_rows:
                    want = 0
                    for i in exponents:
                        want ^= mul(polynomial[i], inputs.get(n - (1 << i), 0))
                    assert remainder.get(n, 0) == want
                    counts["ordinary_child_coefficients"] += 1
                counts["ordinary_top_quotients"] += 1
    assert missing_centres == exceptional_masks
    return {"b": b, "total_admissible_hyperplanes": len(possible_masks), "tested": len(masks),
            "exceptional_admissible_hyperplanes": len(missing_centres),
            "smallest_tested_offset_count": min(nonzero_lower),
            "selected_rows": len(output_indices), "algebraic_cut_bound_bits": min(cut_values)}


if __name__ == "__main__":
    counts = dict.fromkeys(["excluded_sparse_hyperplane_controls", "verified_hyperplanes",
                            "direct_root_products", "row_pair_intersections", "support_rows",
                            "injective_word_scalings", "ordinary_child_coefficients",
                            "ordinary_top_quotients", "central_coefficient_classifications"], 0)
    degrees = [run(b, counts) for b in (6, 9, 12, 15, 18, 21, 24, 27, 30)]
    print(json.dumps({"degrees": degrees, "counts": counts}, indent=2))
