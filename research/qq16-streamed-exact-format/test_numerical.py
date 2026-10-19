#!/usr/bin/env python3
"""Bounded signed-integer execution versus a Gaussian-rational oracle.

Small full-word fixtures instantiate the numerical permutation/kernel contract.
Their owner/payload permutations are deliberately synthetic, NOT the actual
73-axis QQ16 cover. Exact source operator semantics remain inherited.
@CubeJerry, OpenAI Codex assistance; Apache-2.0.
"""
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys
import paired_kernel

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("format_verifier", HERE / "verify.py")
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def fits(value, width):
    require(type(value) is int, "integer register")
    require(-(1 << (width - 1)) <= value < (1 << (width - 1)), "signed overflow")
    return value


def exact_divide(value, divisor, width):
    require(value % divisor == 0, "inexact division on common grid")
    return fits(value // divisor, width)


def integer_pair(a, b, sign, width):
    # Every real sum/difference and numerator is checked, not only outputs.
    ar, ai = a
    br, bi = b
    sr, si = fits(ar + br, width), fits(ai + bi, width)
    dr, di = fits(ar - br, width), fits(ai - bi, width)
    raw = (fits(sr - sign * di, width), fits(si + sign * dr, width),
           fits(sr + sign * di, width), fits(si - sign * dr, width))
    result = tuple(exact_divide(v, 2, width) for v in raw)
    return result[:2], result[2:]


def rational_pair(a, b, sign):
    # Independently multiply by (1 +/- i)/2 rather than reusing sum/difference code.
    def product(z, coefficient):
        r, i = z
        c, d = coefficient
        return r * c - i * d, r * d + i * c

    def plus(x, y):
        return x[0] + y[0], x[1] + y[1]

    high, low = (F(1, 2), F(sign, 2)), (F(1, 2), F(-sign, 2))
    return plus(product(a, high), product(b, low)), plus(product(a, low), product(b, high))


def permutation(size, stage, port, backwards):
    bits = size.bit_length() - 1
    shift = stage % bits
    mask = (port * 5 + stage) % size
    forward = [(((x << shift) | (x >> (bits - shift))) & (size - 1)) ^ mask for x in range(size)]
    require(len(set(forward)) == size, "synthetic full-owner permutation")
    if not backwards:
        return forward
    inverse = [0] * size
    for x, y in enumerate(forward):
        inverse[y] = x
    return inverse


def run_fixture(word, depth, seed):
    local_axes = 2
    size = 1 << (local_axes * depth + 1)  # two toy owners, full small payloads
    k = (depth + 1) // 2
    grid, width = 3 * k + 6, 3 + 6 * k + 22
    scale = 1 << grid
    rng = random.Random(seed)
    reference, machine = {}, {}
    for prefix in "XYZWFG":
        for index in range(8 if prefix in "FG" else 112):
            name = prefix + str(index)
            if prefix in "XY":
                values = [(rng.randrange(-7, 8), rng.randrange(-7, 8)) for _ in range(size)]
                reference[name] = [tuple(F(x) for x in z) for z in values]
                machine[name] = [tuple(x * scale for x in z) for z in values]
            else:
                # Include the most negative representable owned dirt. CLEAR
                # must discard it without abs(), arithmetic or normalization.
                reference[name] = [(F(0), F(0))] * size
                machine[name] = [(-(1 << (width - 1)), (1 << (width - 1)) - 1)] * size
    original_inputs = {k: list(v) for k, v in machine.items() if k[0] in "XY"}
    completed_cuts = pair_calls = 0
    for event in word:
        op = event[0]
        if op in ("begin", "end", "checkpoint"):
            continue
        destination = event[1]
        if op == "clear":
            machine[destination] = [(0, 0)] * size
            reference[destination] = [(F(0), F(0))] * size
        elif op == "add":
            source, coefficient = event[2], F(event[3])
            sign, divisor = coefficient.numerator, coefficient.denominator
            out, exact = [], []
            for d, s, rd, rs in zip(machine[destination], machine[source],
                                     reference[destination], reference[source]):
                product = tuple(exact_divide(v, divisor, width) for v in s)
                out.append(tuple(fits(d[j] + sign * product[j], width) for j in range(2)))
                exact.append(tuple(rd[j] + coefficient * rs[j] for j in range(2)))
            machine[destination], reference[destination] = out, exact
        elif op == "map":
            order = permutation(size, event[2], event[3], event[4])
            machine[destination] = [machine[destination][i] for i in order]
            reference[destination] = [reference[destination][i] for i in order]
        elif op == "line":
            q = 1 + event[2] % 3  # each nonzero two-axis direction occurs
            fused = list(machine[destination])
            sequential = list(machine[destination])
            directions = [q << (local_axes * layer) for layer in range(depth)]
            for data, paired in ((fused, True), (sequential, False)):
                counts = paired_kernel.transform(data, directions, event[3], width, paired)
                require(counts == paired_kernel.expected(depth, size, paired), "complete native invoice")
            for layer in range(depth):
                displacement = q << (local_axes * layer)
                for i in range(size):
                    j = i ^ displacement
                    if i >= j:
                        continue
                    a, b = integer_pair(machine[destination][i], machine[destination][j], event[3], width)
                    ra, rb = rational_pair(reference[destination][i], reference[destination][j], event[3])
                    machine[destination][i], machine[destination][j] = a, b
                    reference[destination][i], reference[destination][j] = ra, rb
                    require(a == tuple(v * scale for v in ra) and b == tuple(v * scale for v in rb),
                            "each exact signed pair")
                    pair_calls += 1
            require(fused == sequential == machine[destination], "paired lowering at every native cut")
        else:
            raise ValueError("unknown fixture instruction")
        require(machine[destination] == [tuple(v * scale for v in z) for z in reference[destination]],
                "complete-word cut equality")
        completed_cuts += 1
    require(all(machine[k] == v for k, v in original_inputs.items()), "borrowed input return")
    require(all(z == (0, 0) for k, row in machine.items() if k[0] in "FG" for z in row), "scratch zero return")
    return completed_cuts, pair_calls


def rejection(action, text):
    try:
        action()
    except ValueError as error:
        require(text in str(error), "wrong rejection: " + str(error))
    else:
        raise ValueError("negative control was accepted: " + text)


def lowering_receipt():
    """Same-input operation-count benchmark, not Python runtime timing."""
    rows = []
    for depth in (1, 2, 3, 4, 7, 8):
        k, size = (depth + 1) // 2, 1 << depth
        scale, width = 1 << k, 2 * k + 8
        rng = random.Random(53 + depth)
        entry = [(rng.randrange(-7, 8) * scale, rng.randrange(-7, 8) * scale)
                 for _ in range(size)]
        outputs, invoices = [], []
        for paired in (False, True):
            data = list(entry)
            counts = paired_kernel.transform(data, [1 << j for j in range(depth)],
                                             -1, width, paired)
            require(counts == paired_kernel.expected(depth, size, paired), "benchmark full invoice")
            outputs.append(data)
            invoices.append(dict(sorted(counts.items())))
        require(outputs[0] == outputs[1], "same-input benchmark equality")
        saving = sum(invoices[0][x] - invoices[1][x] for x in ("add", "halve", "clear"))
        require(224 * saving == (1344 * size * (depth // 2) - 896 if depth >= 2 else 0),
                "complete native arithmetic and cleanup delta")
        rows.append({"depth": depth, "complex_coordinates": size, "seed": 53 + depth,
                     "sequential": invoices[0], "paired": invoices[1],
                     "saving_across_224_natives": 224 * saving, "same_outputs": True})
    return {"schema_version": 1, "kind": "same-input abstract scalar operation counts",
            "excludes": "address/control, physical bit/tape movement, wrappers, covers, caller admission",
            "rows": rows}


def main():
    checker.authenticate()
    word = json.loads((HERE / "retained/PR4015-WORD.json").read_bytes())
    checker.validate_word(word)
    require(checker.typed(lowering_receipt()) == checker.typed(json.loads((HERE / "LOWERING.json").read_bytes())),
            "complete typed lowering receipt")
    # Exhaust all small pair inputs for both signs on an adequate common grid.
    pair_cases = 0
    for components in itertools.product(range(-2, 3), repeat=4):
        a, b = components[:2], components[2:]
        for sign in (-1, 1):
            actual = integer_pair(tuple(4 * x for x in a), tuple(4 * x for x in b), sign, 8)
            expected = rational_pair(tuple(map(F, a)), tuple(map(F, b)), sign)
            require(actual == tuple(tuple(4 * x for x in z) for z in expected), "Gaussian pair oracle")
            pair_cases += 1
    # Actual denominator and sign-sensitive controls; these are arithmetic
    # failures, not a claim that the global sufficient format is necessary.
    rejection(lambda: integer_pair((1, 0), (0, 0), 1, 8), "inexact division")
    rejection(lambda: integer_pair((1, 1), (1, -1), 1, 3), "signed overflow")
    rejection(lambda: exact_divide(2, 4, 8), "inexact division")
    positive = integer_pair((4, 0), (0, 0), 1, 8)
    negative = integer_pair((4, 0), (0, 0), -1, 8)
    require(positive != negative, "wrong native sign must be observable")
    # The fused block needs one denominator bit, whereas two naive divisions
    # need not each be legal on arbitrary inputs. Check a sharp delta and an
    # inexact-grid rejection, plus its larger scratch cleanup invoice.
    fused_impulse = [(2, 0), (0, 0), (0, 0), (0, 0)]
    counts = paired_kernel.transform(fused_impulse, [1, 2], 1, 5)
    require(fused_impulse == [(0, 1), (1, 0), (1, 0), (0, -1)], "two-axis impulse")
    require(counts["clear"] == 9 and counts["clear"] != 5, "charge enlarged scalar scratch return")
    rejection(lambda: paired_kernel.transform([(1, 0), (0, 0), (0, 0), (0, 0)],
                                               [1, 2], 1, 5), "inexact halving")
    rejection(lambda: paired_kernel.transform([(0, 0)] * 4, [1, 1], 1, 5), "disjoint")
    quad_cases = 0
    for components in itertools.product((-2, 0, 2), repeat=8):
        for sign in (-1, 1):
            data = [components[j:j+2] for j in range(0, 8, 2)]
            expected = list(data)
            # Four independently coded complex-rational pair kernels.
            for delta in (1, 2):
                for a in range(4):
                    b = a ^ delta
                    if a < b:
                        expected[a], expected[b] = rational_pair(expected[a], expected[b], sign)
            invoice = paired_kernel.transform(data, [1, 2], sign, 6)
            require(data == expected, "exhaustive two-axis oracle")
            require(invoice == paired_kernel.expected(2, 4, True), "two-axis full invoice")
            quad_cases += 1
    # Initialization / ownership / terminal restoration controls on real word.
    missing_clear = [list(e) for e in word]
    del missing_clear[0]
    rejection(lambda: checker.validate_word(missing_clear), "uninitialized destination")
    borrowed_write = [list(e) for e in word]
    borrowed_write[0][1] = "X0"
    rejection(lambda: checker.validate_word(borrowed_write), "borrowed input write")
    missing_return = [list(e) for e in word]
    last_clear = max(i for i, e in enumerate(word) if e[:2] == ["clear", "F0"])
    del missing_return[last_clear]
    rejection(lambda: checker.validate_word(missing_return), "private zero return")
    non_dyadic = [list(e) for e in word]
    non_dyadic[1][3] = "1/3"
    rejection(lambda: checker.validate_word(non_dyadic), "scalar alphabet")
    totals = [0, 0]
    for depth in (1, 2, 3):
        for offset in (0, 1):
            cuts, pairs = run_fixture(word, depth, 53 + 10 * depth + offset)
            totals[0] += cuts
            totals[1] += pairs
    print("PASS_STREAMED_FORMAT_NUMERICAL", "fixtures=6", "cuts=" + str(totals[0]),
          "tensor_pairs=" + str(totals[1]), "small_pair_cases=" + str(pair_cases),
          "small_quad_cases=" + str(quad_cases), "controls=12 no_new_kappa")


if __name__ == "__main__":
    main()
