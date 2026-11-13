#!/usr/bin/env python3
"""Exact bounded audit of symmetries and simple Hall-set templates.

Inputs are only the frozen R5 certificate and frozen exact verifier in the
sibling sharp-finite-gaussian-outward-slack package. This is not a matching
search and does not attempt another radius.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / "sharp-finite-gaussian-outward-slack"
CERT_PATH = PACKAGE / "R5-OPTIMUM.json.gz"
VERIFY_PATH = PACKAGE / "verify.py"
PACKED_CERT_SHA256 = "d26f615aacff4b082c316e491aa1730aabc9cb6ceb377d33fb9a279b2d7f5f16"
RAW_CERT_SHA256 = "b1fe3d866d2184227f46ec73ec2021c546bba056e98077e657e9205d9db5ad8b"
VERIFY_SHA256 = "611124563b42ec1c20d4755d190a850d1deac5ed743d6f98094ec97f7d893190"


def require(condition: bool, explanation: str) -> None:
    if not condition:
        raise RuntimeError(explanation)


def load_pinned_inputs() -> tuple[dict, dict]:
    packed = CERT_PATH.read_bytes()
    require(hashlib.sha256(packed).hexdigest() == PACKED_CERT_SHA256,
            "compressed certificate pin mismatch")
    raw = gzip.decompress(packed)
    require(hashlib.sha256(raw).hexdigest() == RAW_CERT_SHA256,
            "expanded certificate pin mismatch")
    source = VERIFY_PATH.read_bytes()
    require(hashlib.sha256(source).hexdigest() == VERIFY_SHA256,
            "frozen verifier pin mismatch")
    namespace = {
        "__name__": "pinned_exact_r5_verifier",
        "__file__": str(VERIFY_PATH),
    }
    exec(compile(source, str(VERIFY_PATH), "exec"), namespace)
    return json.loads(raw), namespace


def signed_permutations():
    """Enumerate the complete signed-permutation group W_4 (384 elements)."""
    for permutation in itertools.permutations(range(4)):
        for signs in itertools.product((-1, 1), repeat=4):
            matrix = [[0] * 4 for _ in range(4)]
            for row, column in enumerate(permutation):
                matrix[row][column] = signs[row]
            yield tuple(tuple(row) for row in matrix)


def multiply(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(4))
              for j in range(4))
        for i in range(4)
    )


def transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(4)) for j in range(4))


def is_signed_permutation(matrix) -> bool:
    return (
        len(matrix) == 4
        and all(len(row) == 4 for row in matrix)
        and all(sum(abs(value) for value in row) == 1 for row in matrix)
        and all(sum(abs(matrix[i][j]) for i in range(4)) == 1
                for j in range(4))
    )


def action(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(4))
                 for i in range(4))


def graph_automorphisms(h):
    """Return all signed-permutation pairs (A,B) satisfying B H = H A.

    Since H H^T=4I, for each input action A there is at most one possible
    output action: B=H A H^T/4. Enumerating all 384 A is exhaustive.
    """
    ht = transpose(h)
    group = []
    for a in signed_permutations():
        numerator = multiply(multiply(h, a), ht)
        if any(value % 4 for row in numerator for value in row):
            continue
        b = tuple(tuple(value // 4 for value in row) for row in numerator)
        if is_signed_permutation(b):
            require(multiply(b, h) == multiply(h, a),
                    "derived graph automorphism fails B H=H A")
            group.append((a, b))
    return group


def s5_points(verify):
    return {
        point for point in itertools.product(range(-5, 6), repeat=4)
        if verify["sqnorm"](point) <= 25
    }


def exact_strict_neighbors(point, matrix, verify):
    return {
        output
        for output, _ in verify["all_error_one_outputs"](point, matrix)
        if verify["compare_gaps"](
            verify["sqnorm"](output), verify["sqnorm"](point), 21, 19
        ) < 0
    }


def neighborhood(points, graph):
    result = set()
    for point in points:
        result.update(graph[point])
    return result


def parity_classes(points):
    classes = [set() for _ in range(16)]
    for point in points:
        mask = sum((point[i] & 1) << i for i in range(4))
        classes[mask].add(point)
    return classes


def parity_union_census(classes, graph):
    class_neighbors = [neighborhood(points, graph) for points in classes]
    outputs = sorted(set().union(*class_neighbors))
    output_index = {point: i for i, point in enumerate(outputs)}
    neighbor_bits = []
    for points in class_neighbors:
        bits = 0
        for point in points:
            bits |= 1 << output_index[point]
        neighbor_bits.append(bits)

    total = 1 << len(classes)
    union_bits = [0] * total
    input_sizes = [0] * total
    positive_deficits = 0
    best_mask = 0
    best_deficit = 0
    best_size = (0, 0)
    for mask in range(1, total):
        low_bit = mask & -mask
        index = low_bit.bit_length() - 1
        previous = mask ^ low_bit
        union_bits[mask] = union_bits[previous] | neighbor_bits[index]
        input_sizes[mask] = input_sizes[previous] + len(classes[index])
        deficit = input_sizes[mask] - union_bits[mask].bit_count()
        if deficit > 0:
            positive_deficits += 1
        if mask == 1 or deficit > best_deficit:
            best_mask = mask
            best_deficit = deficit
            best_size = (input_sizes[mask], union_bits[mask].bit_count())
    return {
        "class_count": len(classes),
        "nonempty_classes": sum(bool(points) for points in classes),
        "unions_checked": total - 1,
        "positive_deficiency_unions": positive_deficits,
        "maximum_deficit_input_minus_neighbor": best_deficit,
        "maximum_deficit_mask_hex": f"0x{best_mask:04x}",
        "maximum_deficit_input_neighbor_sizes": list(best_size),
    }


def main() -> None:
    document, verify = load_pinned_inputs()
    matrix = tuple(tuple(row) for row in document["matrix_numerator"])
    require(matrix == (
        (1, 1, 1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, -1, -1, 1),
    ), "unexpected H4 numerator")
    points = s5_points(verify)
    require(len(points) == 3121, "S5 size mismatch")
    raw_t = document["hall"]["input_set"]
    raw_n = document["hall"]["output_neighbors"]
    t = {tuple(point) for point in raw_t}
    declared_n = {tuple(point) for point in raw_n}
    require(len(t) == len(raw_t) == 1692 and t <= points,
            "certificate Hall input set is malformed")
    require(len(declared_n) == len(raw_n) == 1691,
            "certificate Hall output set is malformed")

    # Recompute the complete strict-beta graph only on S5, using the already
    # pinned exact checker routines.
    graph = {point: exact_strict_neighbors(point, matrix, verify)
             for point in points}
    actual_n = neighborhood(t, graph)
    require(actual_n == declared_n,
            "strict-beta neighborhood differs from pinned certificate")

    group = graph_automorphisms(matrix)
    identity = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    group_set = set(group)
    require(len(group) == 192, "signed graph-automorphism count changed")
    require((identity, identity) in group_set,
            "signed graph-automorphism group lacks identity")
    # The relation B H=H A is closed under pairwise composition and inverses;
    # check finite closure as a separate implementation guard.
    for a1, b1 in group:
        for a2, b2 in group:
            require((multiply(a1, a2), multiply(b1, b2)) in group_set,
                    "computed signed graph automorphisms are not closed")

    diagonal = [(a, b) for a, b in group if a == b]
    t_stabilizer = [
        (a, b) for a, b in group
        if {action(a, point) for point in t} == t
    ]
    n_stabilizer = [
        (a, b) for a, b in group
        if {action(b, point) for point in declared_n} == declared_n
    ]
    require(len(diagonal) == 8, "diagonal simultaneous symmetry count changed")
    require(t_stabilizer == [(identity, identity)],
            "Hall input stabilizer is not trivial")
    require(n_stabilizer == [(identity, identity)],
            "Hall output stabilizer is not trivial")

    ball_deficits = []
    shell_deficits = []
    for radius_sq in range(26):
        ball = {point for point in points if verify["sqnorm"](point) <= radius_sq}
        shell = {point for point in points if verify["sqnorm"](point) == radius_sq}
        if ball:
            ball_n = neighborhood(ball, graph)
            ball_deficits.append([radius_sq, len(ball), len(ball_n), len(ball) - len(ball_n)])
        if shell:
            shell_n = neighborhood(shell, graph)
            shell_deficits.append([radius_sq, len(shell), len(shell_n), len(shell) - len(shell_n)])
    require(max(row[3] for row in ball_deficits) == 0,
            "a norm ball unexpectedly gives a positive Hall deficiency")
    require(max(row[3] for row in shell_deficits) == 0,
            "a norm shell unexpectedly gives a positive Hall deficiency")

    classes = parity_classes(points)
    parity_census = parity_union_census(classes, graph)
    require(parity_census["positive_deficiency_unions"] == 0,
            "a union of coordinate-parity classes gives a Hall deficiency")
    t_per_parity = [len(t & parity_class) for parity_class in classes]
    parity_capacities = [len(parity_class) for parity_class in classes]
    require(all(0 < used < capacity
                for used, capacity in zip(t_per_parity, parity_capacities)),
            "T unexpectedly is a union of full coordinate-parity classes")

    print(json.dumps({
        "status": "PASS",
        "scope": "symmetry and bounded simple-template audit only",
        "certificate_raw_sha256": RAW_CERT_SHA256,
        "frozen_verifier_sha256": VERIFY_SHA256,
        "S5_points": len(points),
        "strict_beta_hall": {
            "T_size": len(t),
            "complete_neighbor_size": len(actual_n),
            "deficiency": len(t) - len(actual_n),
        },
        "signed_permutation_symmetry": {
            "W4_input_actions_checked": 384,
            "graph_automorphism_pairs": len(group),
            "diagonal_same_permutation_pairs": len(diagonal),
            "T_setwise_stabilizer": len(t_stabilizer),
            "N_setwise_stabilizer": len(n_stabilizer),
            "composition_closed": True,
        },
        "norm_template_audit": {
            "nonempty_squared_norm_balls": len(ball_deficits),
            "maximum_ball_deficit": max(row[3] for row in ball_deficits),
            "nonempty_squared_norm_shells": len(shell_deficits),
            "maximum_shell_deficit": max(row[3] for row in shell_deficits),
            "ball_counts": ball_deficits,
            "shell_counts": shell_deficits,
        },
        "coordinate_parity_union_audit": {
            **parity_census,
            "T_counts_per_parity_class": t_per_parity,
            "class_capacities": parity_capacities,
        },
        "conclusion": "No nontrivial graph symmetry stabilizes the supplied Hall witness; norm balls, individual shells, and unions of coordinate-parity classes do not give a positive Hall deficiency.",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
