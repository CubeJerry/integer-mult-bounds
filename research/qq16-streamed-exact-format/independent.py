#!/usr/bin/env python3
"""No-import numeric-depth oracle for the complete cut certificate.

The primary uses formal polynomials/max-affine frontiers. This checker derives
each tensor kernel's component row sum and denominator directly from Gaussian
integer coefficients and binomial multiplicities, then uses scalar rational
recurrences. It imports no primary or predecessor executable.
@CubeJerry, OpenAI Codex assistance; Apache-2.0.
"""
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
RETAINED_DIGEST = "1fb806b834d5d56cf094f433601a13aa81ded2338b5f0dd986f2e160b27b92f5"
SOURCES_DIGEST = "837f5d9dc0121369714bb18d4b6bd8db41bd1847e2f84daaf12be337906cf21a"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def multiply(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def power(value, exponent):
    result = (1, 0)
    for _ in range(exponent):
        result = multiply(result, value)
    return result


@lru_cache(maxsize=64)
def kernel_certificate(depth, sign):
    """All coefficients, grouped by subset cardinality; no floating point."""
    mass = Fraction(0)
    denominator = 0
    coefficients = []
    for j in range(depth + 1):
        z = multiply(power((1, sign), depth - j), power((1, -sign), j))
        coefficient = tuple(Fraction(x, 2 ** depth) for x in z)
        multiplicity = comb(depth, j)
        mass += multiplicity * sum(abs(x) for x in coefficient)
        for x in coefficient:
            denominator = max(denominator, x.denominator.bit_length() - 1)
            require(x.denominator & (x.denominator - 1) == 0, "dyadic coefficient")
        coefficients.append((multiplicity, coefficient))
    require(sum(m for m, _ in coefficients) == 2 ** depth, "complete kernel row")
    require(mass == 2 ** ((depth + 1) // 2), "sharp real-component row sum")
    require(denominator == (depth + 1) // 2, "sharp dyadic denominator")
    # A delta input attains a coefficient requiring the full denominator.
    require(any(x.denominator == 2 ** denominator for _, z in coefficients for x in z),
            "denominator witness")
    return mass, denominator


def authenticate():
    raw = (BASE / "RETAINED.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == RETAINED_DIGEST, "retained manifest")
    inventory = json.loads(raw)
    for row in inventory["files"]:
        raw = (BASE / row["path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row["sha256"], "retained byte pin")
    raw = (BASE / "SOURCES.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCES_DIGEST, "source manifest")
    sources = json.loads(raw)
    for row in sources["files"]:
        if row["usage"] == "input":
            require(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"],
                    "canonical byte pin")


def numeric_trace(word, depth):
    amplitude, loss = kernel_certificate(depth, 1)
    require(kernel_certificate(depth, -1) == (amplitude, loss), "both signed kernels")
    state = {prefix + str(i): (Fraction(1), 0) for prefix in ("X", "Y") for i in range(112)}
    rows = []
    for index, event in enumerate(word):
        operation = event[0]
        if operation in ("begin", "end", "checkpoint"):
            continue
        destination = event[1]
        if operation == "clear":
            out = (Fraction(0), 0)
        elif operation == "add":
            magnitude, grid = state[destination]
            other, other_grid = state[event[2]]
            coefficient = abs(Fraction(event[3]))
            product = coefficient * other
            product_grid = other_grid + (2 if coefficient == Fraction(1, 4) else 0)
            out = (magnitude + product,
                   max(grid, product_grid) if magnitude and product else
                   grid if magnitude else product_grid if product else 0)
        elif operation == "map":
            out = state[destination]
        elif operation == "line":
            magnitude, grid = state[destination]
            if magnitude:
                # Coarse common interior bound used by the primary certificate.
                interior = (4 * amplitude * magnitude, grid + loss)
                for j in range(1, depth + 1):
                    previous_mass, previous_grid = kernel_certificate(j - 1, 1)
                    require(4 * previous_mass * magnitude <= interior[0], "each numerator magnitude")
                    # For even depth the penultimate prefix has the final grid;
                    # the primary's interior grid must also retain that case.
                    require(grid + previous_grid <= grid + loss, "each numerator lattice")
                out = (amplitude * magnitude, grid + loss)
            else:
                interior = out = (Fraction(0), 0)
            rows.append((index, "cross_numerator", interior))
        else:
            raise ValueError("unexpected word operation")
        state[destination] = out
        rows.append((index, "completed", out))
    return rows, state


def evaluate(specification, depth):
    t = (depth + 1) // 2 - 1
    magnitude = sum(Fraction(c) * 2 ** (a * t) for a, c in enumerate(specification["poly"]))
    grid = max((c + a * t for c, a in specification["grid"]), default=0)
    return magnitude, grid


def main():
    authenticate()
    receipt = json.loads((BASE / "RESULT.json").read_bytes())
    cuts = json.loads((BASE / "TRACE.json").read_bytes())
    words = {"streamed": json.loads((BASE / "retained/PR4015-WORD.json").read_bytes()),
             "original": json.loads((ROOT / "research/qq16-line-normalized-decoder/WORD.json").read_bytes())}
    comparisons = 0
    for name, word in words.items():
        encoded = json.dumps(cuts[name], sort_keys=True, separators=(",", ":")).encode()
        require(hashlib.sha256(encoded).hexdigest() == receipt[name]["trace_sha256"], "trace receipt binding")
        for depth in (1, 2, 3, 4, 7, 8, 15, 16):
            rows, state = numeric_trace(word, depth)
            require(len(rows) == len(cuts[name]), "all cut rows")
            for actual, expected in zip(rows, cuts[name]):
                require(actual[:2] == tuple(expected[:2]), "cut position/type")
                require(actual[2] == evaluate(expected[2], depth), "independent cut bound")
                comparisons += 1
            for field, specification in receipt[name]["final_outputs"].items():
                require(state[field] == evaluate(specification, depth), "all final output bounds")
    print("PASS_INDEPENDENT_STREAMED_FORMAT", "cut_comparisons=" + str(comparisons),
          "depths=1,2,3,4,7,8,15,16 no_new_kappa")


if __name__ == "__main__":
    main()
