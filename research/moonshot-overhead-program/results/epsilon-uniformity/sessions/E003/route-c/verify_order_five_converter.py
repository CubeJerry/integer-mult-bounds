#!/usr/bin/env python3
"""Exact F16/F256 words, repair identities and occupied-row maps for O5."""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path


class BinaryField:
    def __init__(self, degree, modulus):
        self.degree = degree
        self.order = 1 << degree
        self.modulus = modulus

    def mul(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & self.order:
                a ^= self.modulus
        return result

    def power(self, a, e):
        if e < 0:
            a, e = self.inv(a), -e
        result = 1
        while e:
            if e & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            e >>= 1
        return result

    def inv(self, a):
        assert a
        return self.power(a, self.order - 2)

    def dot(self, xs, ys):
        result = 0
        for x, y in zip(xs, ys):
            result ^= self.mul(x, y)
        return result


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b, field):
    columns = list(zip(*b))
    return [[field.dot(row, col) for col in columns] for row in a]


def mv(a, x, field):
    return [field.dot(row, x) for row in a]


def transpose(a):
    return [list(col) for col in zip(*a)]


def inverse(a, field):
    n = len(a)
    work = [row[:] + identity for row, identity in zip(a, eye(n))]
    for col in range(n):
        pivot = next(i for i in range(col, n) if work[i][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = field.inv(work[col][col])
        work[col] = [field.mul(scale, x) for x in work[col]]
        for i in range(n):
            if i != col and work[i][col]:
                scale = work[i][col]
                work[i] = [x ^ field.mul(scale, y) for x, y in zip(work[i], work[col])]
    return [row[n:] for row in work]


def power_matrix(a, e, field):
    result = eye(len(a))
    for _ in range(e):
        result = mm(a, result, field)
    return result


def tensor(a, b, field):
    return [[field.mul(a[i][j], b[k][l]) for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]


def orbit_lift(a):
    result = eye(4)
    for i in range(2):
        for j in range(2):
            result[i + 1][j + 1] = a[i][j]
    return result


def pairwise_shifts(m):
    v, width = 1, 5
    while (width - 1) // 4 < m:
        v += 1
        width *= 5
    representatives = []
    for vector in itertools.product(range(5), repeat=v):
        first = next((entry for entry in vector if entry), None)
        if first == 1:
            representatives.append(vector)
    representatives = representatives[:m]
    seeds = list(itertools.product(range(5), repeat=v))
    return [[sum(a * b for a, b in zip(form, seed)) % 5 for form in representatives] for seed in seeds]


def main():
    field = BinaryField(4, 0x13)
    zeta = 8
    assert field.power(zeta, 5) == 1 and zeta != 1
    C = [[9, 7], [7, 14]]
    C2 = power_matrix(C, 2, field)
    A, B = [[1, 0], [0, 10]], [[14, 0], [0, 1]]
    E, D = [[12, 0], [0, 8]], [[1, 0], [0, 12]]
    S = [[7, 7], [1, 6]]
    Q = [[0, 1], [1, 0]]
    assert power_matrix(C, 5, field) == eye(2)
    assert mm(mm(A, C, field), B, field) == S
    assert mm(mm(inverse(S, field), C, field), S, field) == [[8, 0], [0, 15]]
    assert mm(mm(mm(E, C, field), D, field), C2, field) == Q
    local_cases = 0
    for r in range(1, 5):
        gate = power_matrix(C, r, field)
        gamma = gate[0][1]
        assert gamma == gate[1][0]
        lifted = orbit_lift(gate)
        swap = orbit_lift(Q)
        diagonal = [1 ^ gamma, gate[0][0], gate[1][1], 1 ^ gamma]
        rebuilt = [[field.mul(gamma, swap[i][j]) ^ (diagonal[i] if i == j else 0) for j in range(4)] for i in range(4)]
        assert lifted == rebuilt
        local_cases += 1
    # Tensor words with actual equal-field fixed points, on every basis vector.
    tensor_words = []
    for m in (1, 2, 3):
        lifted = {name: orbit_lift(matrix) for name, matrix in {"C": C, "A": A, "B": B, "E": E, "D": D, "S": S, "Q": Q}.items()}
        products = {}
        for name, matrix in lifted.items():
            out = [[1]]
            for _ in range(m):
                out = tensor(out, matrix, field)
            products[name] = out
        assert mm(mm(products["A"], products["C"], field), products["B"], field) == products["S"]
        assert mm(mm(mm(products["E"], products["C"], field), products["D"], field), power_matrix(products["C"], 2, field), field) == products["Q"]
        tensor_words.append({"pairs": m, "independent_physical_basis_inputs": 4**m})
    # The old order-three gate cannot have a one-gate diagonal eigenbasis.
    field4 = BinaryField(2, 7)
    old = [[0, 1], [1, 1]]
    forbidden = 0
    for r in (1, 2):
        for a, b, c, d in itertools.product(range(1, 4), repeat=4):
            candidate = mm(mm([[a, 0], [0, b]], power_matrix(old, r, field4), field4), [[c, 0], [0, d]], field4)
            transformed = mm(mm(inverse(candidate, field4), old, field4), candidate, field4)
            assert transformed[0][1] or transformed[1][0]
            forbidden += 1
    # Pairwise-independent shift construction; exact first two moments at examples.
    shift_cases = pair_checks = 0
    for m in (1, 2, 6, 7, 16, 32):
        shifts = pairwise_shifts(m)
        width = len(shifts)
        assert 4 * m + 1 <= width < 20 * m + 5
        for i in range(m):
            assert [sum(row[i] == a for row in shifts) for a in range(5)] == [width // 5] * 5
            for j in range(i):
                assert all(sum(row[i] == a and row[j] == b for row in shifts) == width // 25 for a in range(5) for b in range(5))
                pair_checks += 1
        for offset in (tuple(0 for _ in range(m)), tuple(i % 5 for i in range(m)), tuple((2 * i + 1) % 5 for i in range(m))):
            counts = [sum((a + b) % 5 for a, b in zip(row, offset)) for row in shifts]
            assert sum(counts) == width * 2 * m
            assert sum((count - 2 * m)**2 for count in counts) == width * 2 * m
            shift_cases += 1
    # Work in F256 with an explicit embedded F16 for 125 distinct check nodes.
    extension = BinaryField(8, 0x11B)
    alpha = next(a for a in range(2, 256) if extension.power(a, 4) ^ a ^ 1 == 0)
    embedding = []
    for a in range(16):
        value = 0
        for i in range(4):
            if (a >> i) & 1:
                value ^= extension.power(alpha, i)
        embedding.append(value)
    assert len(set(embedding)) == 16
    for a, b in itertools.product(range(16), repeat=2):
        assert embedding[field.mul(a, b)] == extension.mul(embedding[a], embedding[b])
    zeta_e = embedding[8]
    shifts = list(itertools.product(range(5), repeat=3))
    width, u, degree = len(shifts), 3, 7
    s = 14
    H = [[extension.power(node, row) for node in range(width)] for row in range(s)]
    rng = random.Random(260325)
    repair_vectors = predictor_values = minor_checks = 0
    negative_without_lift = 0
    for target_power in (1, 2, 4):
        for spectral in itertools.product(range(5), repeat=3):
            z = extension.power(zeta_e, target_power * sum(spectral) % 5)
            predictors, bad = [], []
            for index, beta in enumerate(shifts):
                count = sum((target_power * k + shift) % 5 for k, shift in zip(spectral, beta))
                residue = (count - u) & 7
                value = 0
                for h in range(degree + 1):
                    if residue & h == h:
                        value ^= extension.power(zeta_e ^ 1, h)
                value = extension.mul(extension.power(zeta_e, (u - sum(beta)) % 5), value)
                assert extension.power(value, 16) == value
                if u <= count <= u + degree:
                    assert value == z
                else:
                    bad.append(index)
                predictors.append(value)
                predictor_values += 1
            assert len(bad) == s
            V = [[H[row][index] for index in bad] for row in range(s)]
            Vinv = inverse(V, extension)
            assert mm(Vinv, V, extension) == eye(s)
            minor_checks += 1
            inputs = [[rng.randrange(256) for _ in range(width)]]
            if spectral == (0, 0, 0):
                inputs += [[int(i == j) for i in range(width)] for j in range(width)]
            for x in inputs:
                gaps = [p ^ z for p in predictors]
                check_error = mv(H, [extension.mul(gap, item) for gap, item in zip(gaps, x)], extension)
                errors = mv(Vinv, check_error, extension)
                wanted = [extension.mul(extension.power(gaps[index], 14), error) for index, error in zip(bad, errors)]
                a = mv(transpose(Vinv), wanted, extension)
                lift = mv(transpose(H), a, extension)
                output = [extension.mul(p, item) ^ extension.mul(gap, corrected) for p, item, gap, corrected in zip(predictors, x, gaps, lift)]
                assert output == [extension.mul(z, item) for item in x]
                negative_without_lift += int([extension.mul(p, item) for p, item in zip(predictors, x)] != output)
                repair_vectors += 1
    assert negative_without_lift
    # Exact occupied regrouping: 8 copies * 2 halves = 16 duplicate roles.
    regroupings = 0
    for labels, checks, module in itertools.product((1, 3), (5, 25), (1, 2, 4)):
        domain = list(itertools.product(range(labels), range(8), range(2), range(checks), range(module)))
        image = {(label, check, 2 * copy + half, row) for label, copy, half, check, row in domain}
        expected = set(itertools.product(range(labels), range(checks), range(16), range(module)))
        assert image == expected and len(image) == len(domain)
        regroupings += 1
    # Toy count has delta=14/125; actual large-m fixed budget uses delta=1/16.
    assert 4 * 14 < 125
    assert 2 * 2 * (1 / 16) == 1 / 4
    receipt = {
        "scope": "Exact finite gate, spectrum, discrepancy-repair and occupied-regrouping checks; no full tape compiler or multiplication execution.",
        "field16_modulus": "X^4+X+1", "field256_modulus": "X^8+X^4+X^3+X+1",
        "gate": C, "eigenbasis": S, "converter_diagonals": [A, B], "swap_diagonals": [E, D],
        "shared_swap_decompositions": local_cases,
        "physical_tensor_word_cases": tensor_words,
        "old_order_three_one_gate_negative_cases": forbidden,
        "pairwise_shift_pairs": pair_checks, "exact_shift_moment_cases": shift_cases,
        "field_embedding_products": 256,
        "predictor_spectral_values": predictor_values,
        "invertible_check_minors": minor_checks,
        "complete_discrepancy_repair_vectors": repair_vectors,
        "omitted_lift_negative_controls_rejected": negative_without_lift,
        "occupied_regrouping_cases": regroupings,
        "toy_repair": {"queries": 3, "shifts": 125, "window": [3, 10], "marked_rows": 14, "child_mass": "56/125"},
        "asymptotic_chosen_budget": {"marked_fraction": "1/16", "table_fraction": "1/8", "children": 2, "total_child_mass": "1/4"},
    }
    Path(__file__).with_name("order-five-converter-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
