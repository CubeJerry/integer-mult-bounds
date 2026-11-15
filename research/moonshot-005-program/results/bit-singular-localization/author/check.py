#!/usr/bin/env python3
"""Independent exact singular-code localization and scoped acquisition checks.

This checks a fixed rational 111-line source. The all-field and block-width
statements are proved in PROOF.md, not inferred from finite field sampling.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

SOURCE_SHA256 = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
SOURCE_GIT_BLOB = "8eba43d142c819c206dce5df87ea4571aaead287"
BASELINE = "9fb0a34adad2f5903d3169fee7f7a7fcb6f03e3a"
PRIME = 103


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ValueError(label)


def bitset(indices) -> int:
    return sum(1 << i for i in indices)


def positions(word: int):
    while word:
        bit = word & -word
        yield bit.bit_length() - 1
        word ^= bit


def binary_basis(rows) -> list[int]:
    pivots = {}
    for row in rows:
        while row:
            lead = row.bit_length() - 1
            if lead in pivots:
                row ^= pivots[lead]
            else:
                pivots[lead] = row
                break
    return list(pivots.values())


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def primitive_normal(vector) -> tuple[int, ...]:
    denominators = [Fraction(x).denominator for x in vector]
    multiplier = math.lcm(*denominators)
    integer = [int(Fraction(x) * multiplier) for x in vector]
    divisor = math.gcd(*integer)
    integer = [x // divisor for x in integer]
    if next(x for x in integer if x) < 0:
        integer = [-x for x in integer]
    return tuple(integer)


def rational_null_vector(rows) -> tuple[int, ...]:
    matrix = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    pivots = []
    for column in range(8):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [x / scale for x in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank:
                continue
            scale = matrix[i][column]
            if scale:
                matrix[i] = [x - scale * y for x, y in zip(matrix[i], matrix[rank])]
        pivots.append(column)
        rank += 1
    require(rank == 7, "proper support has exact rational rank seven")
    free = next(i for i in range(8) if i not in pivots)
    normal = [Fraction(0)] * 8
    normal[free] = 1
    for i, column in enumerate(pivots):
        normal[column] = -matrix[i][free]
    return primitive_normal(normal)


def check(source: Path) -> dict:
    raw = source.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "source SHA-256")
    require(
        hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == SOURCE_GIT_BLOB,
        "source Git blob",
    )
    geometry = json.loads(raw)
    roots = geometry["native_roots"]
    require(len(roots) == 111 and all(dot(r, r) == 4 for r in roots), "native source")
    require(len({primitive_normal(r) for r in roots}) == 111, "distinct source lines")
    frame = [0, 1, 2, 4, 8, 14, 30, 59]
    gram = [bitset(k for k, j in enumerate(frame) if dot(roots[i], roots[j]) // 2 % 2) for i in frame]
    require(len(binary_basis(gram)) == 8, "nondegenerate binary frame")
    coordinate_inverse = {
        tuple((row & x).bit_count() % 2 for row in gram): x for x in range(256)
    }
    coordinates = [
        coordinate_inverse[tuple(dot(r, roots[i]) // 2 % 2 for i in frame)] for r in roots
    ]
    h = bitset(i for i, x in enumerate(coordinates) if (x & 189).bit_count() % 2)
    all_columns = (1 << 111) - 1
    d8 = all_columns ^ h
    require((d8.bit_count(), h.bit_count()) == (52, 59), "native singular classes")
    canonical = [
        bitset(j for j, t in enumerate(roots) if i == j or dot(r, t) == 0)
        for i, r in enumerate(roots)
    ]
    split = [row & (h if h >> i & 1 else d8) for i, row in enumerate(canonical)]
    code = binary_basis(split)
    require(len(code) == 15, "singular code dimension")
    require(len(binary_basis(w & d8 for w in code)) == 7, "D8 dimension")
    require(len(binary_basis(w & h for w in code)) == 8, "spinor dimension")

    inverse = [0] + [pow(i, -1, PRIME) for i in range(1, PRIME)]

    def modular_support_rank(word):
        basis = {}
        witnesses = []
        for index in positions(word):
            vector = [x % PRIME for x in roots[index]]
            for column, pivot in basis.items():
                coefficient = vector[column]
                if coefficient:
                    vector = [(x - coefficient * y) % PRIME for x, y in zip(vector, pivot)]
            for column, coefficient in enumerate(vector):
                if coefficient:
                    basis[column] = [x * inverse[coefficient] % PRIME for x in vector]
                    witnesses.append(index)
                    break
            if len(basis) == 8:
                break
        return len(basis), witnesses

    proper = []
    rank_histogram = Counter()
    rank_digest = hashlib.sha256()
    word = 0
    previous_gray = 0
    for integer in range(1, 1 << 15):
        gray = integer ^ (integer >> 1)
        change = gray ^ previous_gray
        previous_gray = gray
        word ^= code[change.bit_length() - 1]
        rank, witnesses = modular_support_rank(word)
        rank_histogram[rank] += 1
        rank_digest.update(bytes([rank]))
        if rank < 8:
            normal = rational_null_vector([roots[i] for i in witnesses])
            require(all(dot(roots[i], normal) == 0 for i in positions(word)), "exact support containment")
            require(rank == 7, "no localized word below real dimension seven")
            proper.append(
                {
                    "word": str(word),
                    "code_coordinates": gray,
                    "support": list(positions(word)),
                    "normal": list(normal),
                    "independent_support_rows_mod_103": witnesses,
                }
            )
    require(rank_histogram == {7: 69, 8: 32698}, "complete scalar word census")
    localized = {}
    for entry in proper:
        localized.setdefault(tuple(entry["normal"]), []).append(int(entry["word"]))
    require(len(localized) == 61, "sixty-one real facet localizations")
    require(Counter(len(words) for words in localized.values()) == {1: 57, 3: 4}, "local subcode dimensions")
    for words in localized.values():
        require(len(words) == (1 << len(binary_basis(words))) - 1, "complete local binary subspace")

    # Reconstruct the full root geometry from the native coordinate support set.
    masks = sorted({bitset(i for i, x in enumerate(r) if x) for r in roots if sum(x != 0 for x in r) == 4})
    require(len(masks) == 14, "full root support masks")
    full = [[2 if i == j else 0 for i in range(8)] for j in range(8)]
    for mask in masks:
        indices = list(positions(mask))
        for signs in range(8):
            row = [0] * 8
            row[indices[0]] = 1
            for k in range(1, 4):
                row[indices[k]] = -1 if signs >> (k - 1) & 1 else 1
            full.append(row)
    full_by_line = {primitive_normal(row): row for row in full}
    native_by_line = {primitive_normal(row): i for i, row in enumerate(roots)}
    require(len(full_by_line) == 120 and set(localized) <= set(full_by_line), "all localizing normals are full root lines")
    chart_counts = Counter()
    charts = []
    for normal, words in sorted(localized.items()):
        root = full_by_line[normal]
        binary = coordinate_inverse[tuple(dot(root, roots[i]) // 2 % 2 for i in frame)]
        cls = (binary & 189).bit_count() % 2
        native_index = native_by_line.get(normal)
        dimension = len(binary_basis(words))
        label = ("native" if native_index is not None else "omitted") + ("_spinor" if cls else "_d8")
        chart_counts[label] += 1
        require(dimension == (2 if label == "omitted_d8" else 1), "chart dimension by source status")
        charts.append({"normal": list(normal), "native_index": native_index, "type": label, "dimension": dimension, "words": [str(w) for w in words]})
    require(chart_counts == {"native_d8": 52, "omitted_d8": 4, "omitted_spinor": 5}, "full facet classification")

    receiver_dimensions = []
    for i, root in enumerate(roots):
        local_rows = localized.get(primitive_normal(root), [])
        dimension = len(binary_basis(local_rows))
        receiver_dimensions.append(dimension)
        if h >> i & 1:
            require(dimension == 0, "spinor receiver has zero local subcode")
        else:
            require(dimension == 1 and local_rows == [canonical[i] & h], "native D8 local mode exactly hK_i")
    require(len(binary_basis(split[i] for i in positions(h))) == 8, "forced spinor fitting rows span eight")
    require(len(binary_basis(split[i] for i in positions(d8))) == 7, "forced D8 quotient rows span seven")

    all_proper = [int(entry["word"]) for entry in proper]
    d8_modes = sorted({w & d8 for w in all_proper if w & d8})
    spinor_modes = sorted({w & h for w in all_proper if w & h})
    require(len(d8_modes) == 4 and len(binary_basis(d8_modes)) == 4, "four independent D8 localized modes")
    require(len(spinor_modes) == 61 and len(binary_basis(spinor_modes)) == 8, "sixty-one spinor localized modes")
    require(all(u & v for i, u in enumerate(d8_modes) for v in d8_modes[i + 1:]), "D8 localized supports always intersect")
    disjoint_pairs = [(i, j) for i, u in enumerate(spinor_modes) for j, v in enumerate(spinor_modes) if i < j and not (u & v)]
    require(len(disjoint_pairs) == 28, "twenty-eight disjoint spinor pairs")
    degree = Counter(i for pair in disjoint_pairs for i in pair)
    require(all(value == 1 for value in degree.values()), "disjointness graph is a matching")
    require(all(spinor_modes[i] ^ spinor_modes[j] == h for i, j in disjoint_pairs), "all disjoint pairs are complementary")

    # Sharpness of the algebraic direct-acquisition capacity 3.
    omitted = primitive_normal([0, 0, 1, 1, 0, 0, 1, -1])
    partner = primitive_normal(roots[72])
    omitted_modes = localized[omitted]
    partner_modes = localized[partner]
    omitted_support = 0
    for row in omitted_modes:
        omitted_support |= row
    require(len(binary_basis(omitted_modes)) == 2 and len(partner_modes) == 1, "two-plus-one acquisition witness")
    require(not (omitted_support & partner_modes[0]), "witness source supports disjoint")
    require(len(binary_basis(omitted_modes + partner_modes)) == 3, "witness innovation dimension three")
    complement = []
    span = binary_basis(omitted_modes + partner_modes)
    for row in code:
        if len(binary_basis(span + [row])) > len(span):
            complement.append(row)
            span = binary_basis(span + [row])
    require(len(complement) == 12 and len(span) == 15, "twelve abstract seeds make acquisition dimension bound sharp")

    # A literal two-ADD negative control for the false terminal-span shortcut.
    # Coefficient bits are u=1 and independent y=2.
    packet, receiver = 1, 2
    receiver ^= packet
    packet ^= receiver
    require((packet, receiver) == (2, 3), "Y export loses the packet's X direction")
    require(not (packet & 1) and bool(receiver & 1), "terminal packet X span omits retained receiver history")

    return {
        "status": "PASS_SINGULAR_LOCALIZATION_AND_ACQUISITION",
        "baseline_commit": BASELINE,
        "source_sha256": SOURCE_SHA256,
        "source_git_blob": SOURCE_GIT_BLOB,
        "source_qualification": geometry["qualification"],
        "source_native_sha256": geometry["native_source_sha256"],
        "code_basis": [str(w) for w in code],
        "enumerated_nonzero_words": (1 << 15) - 1,
        "exact_real_rank_histogram": dict(rank_histogram),
        "gray_order_rank_sha256": rank_digest.hexdigest(),
        "proper_word_span_dimension": len(binary_basis(all_proper)),
        "chart_classification": dict(chart_counts),
        "native_receiver_local_dimensions": dict(Counter(receiver_dimensions)),
        "fitting_rigidity_dimensions": {"forced_spinor": 8, "forced_d8_quotient": 7, "total": 15},
        "direct_acquisition": {
            "d8_mode_count": len(d8_modes),
            "d8_modes_pairwise_overlap": True,
            "spinor_mode_count": len(spinor_modes),
            "spinor_disjoint_pairs": len(disjoint_pairs),
            "spinor_disjointness_is_matching": True,
            "maximum_dimension_per_scalar_coordinate": 3,
            "sharp_witness_omitted_normal": list(omitted),
            "sharp_witness_native_partner": 72,
            "sharp_witness_omitted_modes": [str(w) for w in omitted_modes],
            "sharp_witness_partner_mode": str(partner_modes[0]),
            "abstract_seed_complement": [str(w) for w in complement],
            "minimum_seed_widths_in_declared_model": 12,
        },
        "terminal_span_negative_control": {
            "initial": {"P": "u", "Y": "y"},
            "operations": ["Y += P", "P += Y"],
            "final": {"P": "y", "Y": "y+u"},
            "packet_terminal_X_rank": 0,
            "receiver_retained_X_rank": 1,
            "claimed_as_complete_decoder": False,
        },
        "proper_words": proper,
        "charts": charts,
        "full_uniform_supplier": False,
        "new_complete_kappa": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = check(arguments.source)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
