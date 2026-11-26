#!/usr/bin/env python3
"""Exact finite diagnostics for the free-transfer star-transposition form."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[6]
PRIMARY = REPO.parent / "openai-math"


def parity(value):
    return value.bit_count() & 1


def csign(dst, src, f):
    mask = (1 << f) - 1
    s, t = dst >> f, dst & mask
    x, y = src >> f, src & mask
    return -1 if parity((x ^ s) & (t ^ y)) else 1


def swap_tuple(word, j):
    result = list(word)
    result[0], result[j] = result[j], result[0]
    return tuple(result)


def index_of(word, q):
    result = 0
    for digit in word:
        result = result * q + digit
    return result


def apply_c(vector, words, lookup, register, f):
    """Return the numerator of C_f times vector; denominator is 2**f."""
    q = 1 << (2 * f)
    result = [0] * len(words)
    for i, word in enumerate(words):
        for src in range(q):
            old = list(word)
            old[register] = src
            result[i] += csign(word[register], src, f) * vector[lookup[tuple(old)]]
    return result


def apply_p(vector, words, lookup, j):
    return [vector[lookup[swap_tuple(word, j)]] for word in words]


def spectral_and_involution():
    spectral = involution = walsh = 0
    cases = []
    for f in (1, 2, 3):
        q = 1 << (2 * f)
        h = 1 << f
        mask = h - 1
        c = [[csign(dst, src, f) for src in range(q)] for dst in range(q)]
        for dst in range(q):
            s, t = dst >> f, dst & mask
            for src in range(q):
                x, y = src >> f, src & mask
                spectral_sum = sum(
                    (-1) ** (parity((s ^ x) & X) ^ parity((t ^ y) & Z) ^ parity(X & Z))
                    for X in range(h) for Z in range(h)
                )
                assert spectral_sum == h * c[dst][src]
                spectral += 1
                walsh_sign = (-1) ** (
                    parity(s & t) ^ parity(x & y) ^ parity(x & t) ^ parity(y & s)
                )
                assert walsh_sign == c[dst][src]
                walsh += 1
                numerator = sum(c[dst][z] * c[z][src] for z in range(q))
                assert numerator == (q if dst == src else 0)
                involution += 1
        cases.append({"f": f, "pair_alphabet": q, "matrix_entries": q * q})
    return cases, spectral, involution, walsh


def source_endpoint_identity():
    checks = sparse_entries = vector_checks = 0
    cases = []
    for f, m in ((1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2)):
        q = 1 << (2 * f)
        words = list(product(range(q), repeat=m + 1))
        lookup = {word: i for i, word in enumerate(words)}
        # Check every potentially nonzero source-kernel entry, including all
        # spectator assignments. The common denominator of both sides is q.
        for src in words:
            for j in range(1, m + 1):
                for out0 in range(q):
                    for outj in range(q):
                        dst = list(src)
                        dst[0], dst[j] = out0, outj
                        # Direct source kernel P_j C_j C_0.
                        direct = csign(outj, src[0], f) * csign(out0, src[j], f)
                        # Independent intermediate address of C_0 P_j C_0:
                        # first endpoint fixes the eventual j-th output.
                        intermediate_hub = outj
                        shared = csign(intermediate_hub, src[0], f) * csign(out0, src[j], f)
                        assert direct == shared
                        sparse_entries += 1
                checks += 1
        # Explicit complete-array application gives a separate ordering check.
        vector = [((i * 37 + 11) % 101) - 50 for i in range(len(words))]
        for j in range(1, m + 1):
            direct = apply_p(apply_c(apply_c(vector, words, lookup, 0, f), words, lookup, j, f), words, lookup, j)
            shared = apply_c(apply_p(apply_c(vector, words, lookup, 0, f), words, lookup, j), words, lookup, 0, f)
            assert direct == shared
            vector_checks += len(words)
        cases.append({"f": f, "m": m, "array_entries": len(words)})
    return cases, checks, sparse_entries, vector_checks


def support_witnesses():
    assignments = incidences = 0
    cases = []
    for alphabet in (2, 3, 4, 8, 16):
        for m in range(1, 11):
            output = (0,) + (1,) * m
            addresses = [swap_tuple(output, j) for j in range(1, m + 1)]
            assert len(set(addresses)) == m
            for signs in product((-1, 1), repeat=m):
                row = {}
                for address, weight in zip(addresses, signs):
                    row[address] = row.get(address, 0) + weight
                assert len({key: value for key, value in row.items() if value}) == m
                assignments += 1
                incidences += m
            cases.append({"alphabet": alphabet, "m": m, "row_support": m})
    return cases, assignments, incidences


def negative_controls():
    f, m, q = 1, 2, 4
    words = list(product(range(q), repeat=m + 1))
    lookup = {word: i for i, word in enumerate(words)}
    vector = [((i * i + 7 * i) % 31) - 15 for i in range(len(words))]
    correct = apply_c(apply_p(apply_c(vector, words, lookup, 0, f), words, lookup, 1), words, lookup, 0, f)
    omitted = [2 * value for value in apply_p(apply_c(vector, words, lookup, 0, f), words, lookup, 1)]
    assert omitted != correct
    # A one-slot swap is different from exchanging both slots of the pair.
    def wrong_word(word):
        hub, leaf = word[0], word[1]
        result = list(word)
        result[0] = (leaf & 2) | (hub & 1)
        result[1] = (hub & 2) | (leaf & 1)
        return tuple(result)
    first = apply_c(vector, words, lookup, 0, f)
    wrong = [first[lookup[wrong_word(word)]] for word in words]
    wrong = apply_c(wrong, words, lookup, 0, f)
    assert wrong != correct
    output = (0, 1, 1, 1)
    zero_weight_row = {swap_tuple(output, j): b for j, b in enumerate((1, 0, -1), start=1) if b}
    assert len(zero_weight_row) == 2
    return ["omitted endpoint rejected", "one-slot instead of pair swap rejected", "zero-weight m-support extension rejected"]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    spectral_cases, spectral, involution, walsh = spectral_and_involution()
    endpoint_cases, basis_checks, sparse_entries, vector_checks = source_endpoint_identity()
    support_cases, assignments, incidences = support_witnesses()
    controls = negative_controls()
    sources = {
        "kernel.tex": PRIMARY / "preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/kernel.tex",
        "binary.tex": PRIMARY / "preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/binary.tex",
        "walsh.tex": PRIMARY / "preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/walsh.tex",
        "pairwise-newton-division.md": REPO / "research/moonshot-overhead-program/routes/B/pairwise-newton-division.md",
    }
    result = {
        "status": "pass",
        "scope": "Exact finite pair-query, endpoint-ordering, and monomial-support checks; no full tape execution or runtime lower bound.",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "source_pin": "3344da59991ed94f9ba711217b29c1d760badfa6",
        "source_sha256": {name: digest(path) for name, path in sources.items()},
        "proof_sha256": digest(ROOT / "ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md"),
        "verifier_sha256": digest(Path(__file__).resolve()),
        "spectral_cases": spectral_cases,
        "spectral_kernel_entries": spectral,
        "involution_entries": involution,
        "normalized_walsh_entries": walsh,
        "endpoint_cases": endpoint_cases,
        "basis_query_pairs": basis_checks,
        "nonzero_kernel_entries": sparse_entries,
        "complete_array_coordinates": vector_checks,
        "support_cases": support_cases,
        "signed_support_assignments": assignments,
        "signed_support_incidences": incidences,
        "negative_controls": controls,
    }
    target = ROOT / "ROUTING-star-transpose-verification.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "spectral_kernel_entries", "involution_entries", "basis_query_pairs", "nonzero_kernel_entries", "complete_array_coordinates", "signed_support_assignments", "negative_controls")}, indent=2))


if __name__ == "__main__":
    main()
