#!/usr/bin/env python3
"""Exact algebra and live-array ledgers, not a complete tape-machine test."""
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import numpy as np


def inverse_matrix(a, p):
    n = len(a)
    b = np.concatenate((np.array(a, dtype=np.int64) % p, np.eye(n, dtype=np.int64)), axis=1)
    for c in range(n):
        pivot = next(r for r in range(c, n) if b[r, c] % p)
        b[[c, pivot]] = b[[pivot, c]]
        b[c] = b[c] * pow(int(b[c, c]), -1, p) % p
        for r in range(n):
            if r != c:
                b[r] = (b[r] - b[r, c] * b[c]) % p
    return b[:, n:]


def independent_rows(a, p, order):
    vectors, chosen = {}, []
    for i in order:
        row = a[i].copy() % p
        for column in sorted(vectors):
            row = (row - row[column] * vectors[column]) % p
        nonzero = np.flatnonzero(row)
        if len(nonzero):
            column = int(nonzero[0])
            vectors[column] = row * pow(int(row[column]), -1, p) % p
            chosen.append(int(i))
    return chosen


def push(a, permutation):
    result = np.empty_like(a)
    result[..., permutation] = a
    return result


def cube_matrix(q=4):
    words = list(product(range(q), repeat=3))
    return np.array([[int(v == w or sum(x != y for x, y in zip(v, w)) == 2)
                      for v in words] for w in words], dtype=np.int64)


def column_rectangles(p):
    return [([v], [w for w in range(len(p)) if w != v and p[w, v]])
            for v in range(len(p))]


def bit_rectangles(n, blocks=1):
    assert n % blocks == 0 and (n // blocks).bit_count() == 1
    size = n // blocks
    out = []
    for block in range(blocks):
        offset = block * size
        for bit in range(size.bit_length() - 1):
            width = 1 << bit
            for start in range(0, size, 2 * width):
                l = list(range(offset + start, offset + start + width))
                k = list(range(offset + start + width, offset + start + 2 * width))
                out.extend(((l, k), (k, l)))
    return out


def verify_case(name, pmat, rectangles, prime, m, rows, seed):
    rng = np.random.default_rng(seed)
    n, omega = len(pmat), 1 << (2 * m)
    i_basis = independent_rows(pmat, prime, rng.permutation(n))
    j_basis = independent_rows(pmat.T, prime, rng.permutation(n))
    rank = len(i_basis)
    assert len(j_basis) == rank and m * rank <= n
    middle = inverse_matrix(pmat[np.ix_(i_basis, j_basis)], prime)
    assert np.array_equal(pmat[:, j_basis] @ middle @ pmat[i_basis] % prime, pmat % prime)
    counted = np.eye(n, dtype=np.int64)
    left_degree, right_degree = np.zeros(n, dtype=np.int64), np.zeros(n, dtype=np.int64)
    for l, k in rectangles:
        assert not set(l) & set(k)
        counted[np.ix_(k, l)] += 1
        left_degree[l] += 1
        right_degree[k] += 1
    assert np.array_equal(counted, pmat)
    qmaps = []
    for j in range(m):
        qmap = np.arange(omega)
        for x in range(omega):
            if ((x >> j) ^ (x >> (m + j))) & 1:
                qmap[x] ^= (1 << j) | (1 << (m + j))
        qmaps.append(qmap)
    sources = [[rng.permutation(omega) for _ in range(n)] for _ in range(m)]
    destinations = [[sources[j][v][qmaps[j]] for v in range(n)] for j in range(m)]
    inverse_dest = [[np.argsort(a) for a in line] for line in destinations]
    fixed = [rng.permutation(omega) for _ in range(m)]
    inverse_fixed = [np.argsort(a) for a in fixed]
    original = rng.integers(0, prime, (n, rows, omega), dtype=np.int64)
    matrices = rng.integers(0, prime, (m + 1, rows, rows), dtype=np.int64)
    matrices[1, 0] = 0
    expected = np.stack([matrices[0] @ x % prime for x in original])
    for j in range(m):
        for v in range(n):
            expected[v] = (expected[v] + matrices[j + 1] @ push(original[v], qmaps[j])) % prime
    output = np.zeros_like(original)
    gather = np.zeros((m, rank, rows, omega), dtype=np.int64)
    arrangements = []
    direct_negative = np.zeros_like(original)
    max_live_units = 0
    parent = n * rows * omega
    for l, k in rectangles:
        prep_s = {v: rng.permutation(omega) for v in l}
        prep_d = {v: rng.permutation(omega) for v in k}
        common = [rng.permutation(omega) for _ in range(m)]
        arrangements.append((prep_s, prep_d, common))
        prepared_sources = {v: push(original[v], prep_s[v]) for v in l}
        prepared_dest = {v: np.zeros((rows, omega), dtype=np.int64) for v in k}
        for j in range(m):
            g, gi = common[j], np.argsort(common[j])
            total = np.zeros((rows, omega), dtype=np.int64)
            for v in l:
                remaining = g[sources[j][v][np.argsort(prep_s[v])]]
                total = (total + push(prepared_sources[v], remaining)) % prime
            scaled = matrices[j + 1] @ total % prime
            for v in k:
                remaining = prep_d[v][inverse_dest[j][v][gi]]
                prepared_dest[v] = (prepared_dest[v] - push(scaled, remaining)) % prime
            for basis_index, label in enumerate(i_basis):
                if label in k:
                    gather[j, basis_index] = (gather[j, basis_index] + push(total, fixed[j][gi])) % prime
            live = (6 * parent + m * rank * rows * omega
                    + (len(l) + len(k) + 3) * rows * omega)
            max_live_units = max(max_live_units, live)
        for v in k:
            contribution = push(prepared_dest[v], np.argsort(prep_d[v]))
            output[v] = (output[v] + contribution) % prime
            direct_negative[v] = (direct_negative[v] + contribution) % prime
    for j in range(m):
        for b, v in enumerate(i_basis):
            gather[j, b] = (gather[j, b] + push(original[v], fixed[j][sources[j][v]])) % prime
        for b, i in enumerate(i_basis):
            exact = np.zeros((rows, omega), dtype=np.int64)
            for v in range(n):
                if pmat[i, v]:
                    exact = (exact + push(original[v], fixed[j][sources[j][v]])) % prime
            assert np.array_equal(gather[j, b], exact)
    scatter = np.zeros_like(gather)
    for j in range(m):
        for k in range(rank):
            mixed = sum((int(middle[k, i]) * gather[j, i] for i in range(rank)), np.zeros((rows, omega), dtype=np.int64)) % prime
            scatter[j, k] = matrices[j + 1] @ mixed % prime
    max_live_units = max(max_live_units, 6 * parent + 2 * m * rank * rows * omega)
    for (l, k), (_, prep_d, common) in zip(rectangles, arrangements):
        prepared_dest = {v: np.zeros((rows, omega), dtype=np.int64) for v in k}
        for j in range(m):
            g, gi = common[j], np.argsort(common[j])
            total = np.zeros((rows, omega), dtype=np.int64)
            for b, label in enumerate(j_basis):
                if label in l:
                    total = (total + push(scatter[j, b], g[inverse_fixed[j]])) % prime
            for v in k:
                remaining = prep_d[v][inverse_dest[j][v][gi]]
                prepared_dest[v] = (prepared_dest[v] + push(total, remaining)) % prime
        for v in k:
            output[v] = (output[v] + push(prepared_dest[v], np.argsort(prep_d[v]))) % prime
    for j in range(m):
        for b, v in enumerate(j_basis):
            output[v] = (output[v] + push(scatter[j, b], inverse_dest[j][v][inverse_fixed[j]])) % prime
    for v in range(n):
        output[v] = (output[v] + matrices[0] @ original[v]) % prime
    assert np.array_equal(output, expected)
    assert max_live_units <= 12 * parent
    sources_count, dest_count = int(sum(left_degree)), int(sum(right_degree))
    assert sources_count + 2 * dest_count <= 2 * (sources_count + dest_count)
    negative = 0
    if prime != 2:
        assert not np.array_equal((output - 2 * direct_negative) % prime, expected)
        negative += 1
    assert not np.array_equal((output - direct_negative) % prime, expected)
    negative += 1
    wrong_fixed = scatter.copy()
    shifted_positions = np.roll(np.arange(omega), 1)
    active_query = next(j for j in range(m) if not np.array_equal(scatter[j], push(scatter[j], shifted_positions)))
    wrong_fixed[active_query] = push(wrong_fixed[active_query], shifted_positions)
    assert not np.array_equal(wrong_fixed, scatter)
    negative += 1
    assert not np.array_equal(np.stack([matrices[0] @ x % prime for x in original]), expected)
    negative += 1
    return dict(name=name, characteristic=prime, labels=n, rank=rank, queries=m,
                scalar_rows=rows, physical_positions=omega, independent_outputs=int(output.size),
                rectangles=len(rectangles), rank_payload_fraction=f"{m * rank}/{n}",
                conservative_live_payload_ratio=max_live_units / parent,
                endpoint_operations_before=sources_count + dest_count,
                endpoint_operations_after=sources_count + 2 * dest_count,
                middle_inverse_nonzeros=int(np.count_nonzero(middle)), negative_controls=negative)


def main():
    cases = [verify_case("all-ones-odd-field", np.ones((8, 8), dtype=np.int64), bit_rectangles(8), 5, 3, 3, 101),
             verify_case("two-blocks-full-occupancy", np.kron(np.eye(2, dtype=np.int64), np.ones((4, 4), dtype=np.int64)), bit_rectangles(8, 2), 2, 4, 3, 102)]
    cube = cube_matrix()
    cases.append(verify_case("actual-q4-d2-labels", cube, column_rectangles(cube), 2, 4, 2, 103))
    assert (1024 * 2) // 8 == 256
    result = dict(scope="Two-pass shared-pencil algebra and explicit local liveness/call ledgers; no tape simulation or asymptotic proof.",
                  source_openai_math="3344da59991ed94f9ba711217b29c1d760badfa6",
                  programme_start="0607d044d1d09489580da0e5828588820e1a6775",
                  python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
                  cases=cases, total_independent_outputs=sum(x["independent_outputs"] for x in cases),
                  negative_controls=sum(x["negative_controls"] for x in cases) + 1,
                  limitations=["Finite endpoint remainders are arbitrary permutations; lower triangularity is supplied by the separately checked geometry.",
                               "Liveness ledger counts the stated schedule; this is not measured tape execution.",
                               "Not a complete interchange, numerical precision or multiplication verification."])
    source = Path(__file__)
    result["checker_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    output = source.with_name("uniform-payload-pencil-verification.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
