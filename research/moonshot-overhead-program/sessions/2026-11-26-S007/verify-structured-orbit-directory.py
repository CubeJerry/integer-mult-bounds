#!/usr/bin/env python3
"""Compare the physical orbit-index maps to ordinary division and independent FS1 records."""
from collections import defaultdict
from functools import cache
from pathlib import Path
from random import Random
import json
import runpy

base = runpy.run_path(str(Path(__file__).with_name('verify-factor-directory.py')))
Field, fs1, from_bits = (base[name] for name in ('Field', 'fs1', 'from_bits'))
pdiv, projected_remainder, compose = (base[name] for name in ('pdiv', 'projected_remainder', 'compose'))


def bits(value, length):
    return tuple(value >> (length - k - 1) & 1 for k in range(length))


def integer(values):
    out = 0
    for v in values:
        out = 2 * out + v
    return out


def right(word, length, shift=1):
    shift %= length
    return ((word >> shift) | (word << (length - shift))) & ((1 << length) - 1)


def canonical(word, length):
    rotations = [right(word, length, j) for j in range(length)]
    smallest = min(rotations)
    return smallest, next(j for j in range(length) if right(smallest, length, j) == word), len(set(rotations))


def binary_apply(rows, x):
    return sum(((row & x).bit_count() & 1) << i for i, row in enumerate(rows))


def inverse(rows):
    n = len(rows)
    mat = [x | (1 << (n + i)) for i, x in enumerate(rows)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if mat[j] >> i & 1)
        mat[i], mat[pivot] = mat[pivot], mat[i]
        for j in range(n):
            if j != i and mat[j] >> i & 1:
                mat[j] ^= mat[i]
    return [x >> n for x in mat]


def triangular_levels(mat, lower, start=0):
    n = len(mat)
    if n < 2:
        return []
    u = n // 2
    left_mask = (1 << u) - 1
    left = [row & left_mask for row in mat[:u]]
    right_rows = [row >> u for row in mat[u:]]
    x = triangular_levels(left, lower, start)
    y = triangular_levels(right_rows, lower, start + u)
    height = max(len(x), len(y))
    levels = [(x[i] if i < len(x) else []) + (y[i] if i < len(y) else []) for i in range(height)]
    if lower:
        cross = [row & left_mask for row in mat[u:]]
        subinv, source, target = inverse(left), start, start + u
    else:
        cross = [row >> u for row in mat[:u]]
        subinv, source, target = inverse(right_rows), start + u, start
    final = []
    for i, crossrow in enumerate(cross):
        controls = 0
        for j, row in enumerate(subinv):
            if crossrow >> j & 1:
                controls ^= row
        if controls:
            final.append((target + i, controls << source))
    return levels + [final]


@cache
def compiled_affine(rows, offset):
    # Independent PA=LU followed by recursive simultaneous cross-block shears.
    n = len(rows)
    upper, lower, p = list(rows), [1 << i for i in range(n)], list(range(n))
    for i in range(n):
        pivot = next(j for j in range(i, n) if upper[j] >> i & 1)
        if pivot != i:
            upper[i], upper[pivot] = upper[pivot], upper[i]
            p[i], p[pivot] = p[pivot], p[i]
            low = (1 << i) - 1
            x, y = lower[i] & low, lower[pivot] & low
            lower[i] = (lower[i] & ~low) | y
            lower[pivot] = (lower[pivot] & ~low) | x
        for j in range(i + 1, n):
            if upper[j] >> i & 1:
                upper[j] ^= upper[i]
                lower[j] |= 1 << i
    stages = triangular_levels(upper, False) + triangular_levels(lower, True)
    for changes in stages:
        sources = 0
        for _, use in changes:
            sources |= use
        assert all(not (sources >> target & 1) for target, _ in changes)
    table = []
    for x in range(1 << n):
        image = x
        for changes in stages:
            update = sum(((image & controls).bit_count() & 1) << target for target, controls in changes)
            image ^= update
        image = sum((image >> i & 1) << p[i] for i in range(n)) ^ offset
        assert image == binary_apply(rows, x) ^ offset
        table.append(image)
    assert len(set(table)) == 1 << n
    return table


def compile_map(function, n):
    offset = function(0)
    columns = [function(1 << j) ^ offset for j in range(n)]
    rows = tuple(sum(((col >> i) & 1) << j for j, col in enumerate(columns)) for i in range(n))
    return compiled_affine(rows, offset)


def stable_j_radix(rows, js, b):
    flags = []
    values, keys = list(rows), list(js)
    for k in range((b - 1).bit_length()):
        decision = [j >> k & 1 for j in keys]
        flags.append(decision)
        order = [i for bit in (0, 1) for i, chosen in enumerate(decision) if chosen == bit]
        values, keys = [values[i] for i in order], [keys[i] for i in order]
    assert keys == sorted(js)
    return values, flags


def unradix(rows, flags):
    rows = list(rows)
    for decision in flags[::-1]:
        zero, one = 0, decision.count(0)
        combined = []
        for chosen in decision:
            if chosen:
                combined.append(rows[one])
                one += 1
            else:
                combined.append(rows[zero])
                zero += 1
        rows = combined
    return rows


@cache
def half_plan(b, prefix, half):
    h = (b - 1).bit_length()
    offsets = range(0, b // 2) if half == 0 else range(b // 2, b)
    active = sorted({(j + k) % b for j in offsets for k in range(h)})
    spectator = [k for k in range(b) if k not in active]
    emitted, keys = [], []
    for pat in range(1 << len(active)):
        entered = {pos: val for pos, val in zip(active, bits(pat, len(active)))}
        matches = [j for j in offsets if integer(entered[(j + k) % b] for k in range(h)) == prefix]
        if not matches:
            continue
        row = []
        for spect in range(1 << len(spectator)):
            word = entered | dict(zip(spectator, bits(spect, len(spectator))))
            row.append(integer(word[i] for i in range(b)))
        emitted.extend([row] * len(matches))
        keys.extend(matches)
    routed, flags = stable_j_radix(emitted, keys, b)
    assert unradix(routed, flags) == emitted
    slices = {}
    for j in offsets:
        holes = {(j + k) % b for k in range(h)}
        old = [k for k in active if k not in holes] + spectator
        order = [(j + h + k) % b for k in range(b - h)]
        reorder = compile_map(lambda x: integer(bits(x, b - h)[old.index(k)] for k in order), b - h)
        slices[j] = reorder
    return emitted, keys, routed, flags, slices


def gather_prefix(ambient, b, p):
    h = (b - 1).bit_length()
    count = 1 << (b - h)
    result = [[0] * b for _ in range(count)]
    for half in (0, 1):
        _, keys, routed, _, slices = half_plan(b, p, half)
        cursor = 0
        for j, perm in slices.items():
            size = keys.count(j)
            raw = [ambient[u] for row in routed[cursor:cursor + size] for u in row]
            for old, tail in enumerate(perm):
                result[tail][j] = raw[old]
            cursor += size
    # Independent direct rotation lookup, outside the implemented half-window route.
    for tail, values in enumerate(result):
        word = (p << (b - h)) | tail
        assert values == [ambient[right(word, b, j)] for j in range(b)]
    return result


def scatter_prefix(data, b, p):
    ambient = [0] * (1 << b)
    for half in (0, 1):
        emitted, keys, routed, flags, slices = half_plan(b, p, half)
        cursor, sorted_payload = 0, []
        for j, perm in slices.items():
            raw = [data[t][j] for t in perm]
            for _ in range(keys.count(j)):
                width = len(routed[cursor])
                sorted_payload.append(raw[:width])
                raw = raw[width:]
                cursor += 1
            assert not raw
        origins = unradix(sorted_payload, flags)
        for source, payload in zip(emitted, origins, strict=True):
            for original, value in zip(source, payload, strict=True):
                ambient[original] ^= value
    return ambient


class Geometry:
    def __init__(self, c):
        self.c, self.b = c, 3 * c
        self.a, self.q = 1 << c, 1 << self.b
        self.h = (self.b - 1).bit_length()
        self.ext, self.external = Field(self.b), Field(self.b, True)
        self.directory = fs1(self.b)
        ext, ext0, b, a, q = self.ext, self.external, self.b, self.a, self.q
        fsbasis = ext0.normal()
        iso_root = next(x for x in range(q) if ext0.horner(ext.modulus, x) == 0)
        isopowers = [ext0.pow(iso_root, i) for i in range(b)]
        self.fs_normal = {from_bits(bits(word, b), fsbasis): word for word in range(q)}
        self.word = [self.fs_normal[from_bits(((z >> i) & 1 for i in range(b)), isopowers)] for z in range(q)]
        self.F = [ext.mul(z, z) for z in range(q)]
        assert self.word[1] == q - 1
        assert all(self.word[self.F[z]] == right(self.word[z], b) for z in range(q))
        self.normal_to_ambient = {w: z for z, w in enumerate(self.word)}
        self.canonical = [canonical(w, b) for w in range(q)]
        self.fc = [self.frob(z, c) for z in range(q)]
        self.trace = [z ^ self.fc[z] ^ self.fc[self.fc[z]] for z in range(q)]
        sub = [z for z in range(q) if self.fc[z] == z]
        subbasis = []
        for x in sub:
            if base['rank'](subbasis + [x]) > len(subbasis):
                subbasis.append(x)
        self.y = [from_bits(bits(i, c), subbasis) for i in range(a)]
        self.yindex = {z: i for i, z in enumerate(self.y)}
        generator = next(z for z in sub if z and len({ext.pow(z, i) for i in range(a - 1)}) == a - 1)
        self.logorder = [ext.pow(generator, i) for i in range(a - 1)] + [0]
        assert set(self.logorder) == set(sub) == set(self.y)
        reps, _ = base['plane_order'](ext, c)
        self.marked = [alpha ^ eps for alpha in reps for eps in (0, 1)]
        kernel = [z for z in range(q) if self.trace[z] == 0]
        v = next(z for z in kernel if z)
        span = {ext.mul(v, z) for z in sub}
        w = next(z for z in kernel if z not in span)
        self.yv = [ext.mul(v, z) for z in self.y]
        self.zw = [ext.mul(w, z) for z in self.y]
        self.xbyyz = {t: [t ^ self.yv[y] ^ self.zw[z] for y in range(a) for z in range(a)] for t in self.marked}
        self.yzbyx = {t: {x: yz for yz, x in enumerate(row)} for t, row in self.xbyyz.items()}
        self.actual_yz = [self.yindex[y] * a + self.yindex[z] for y in self.logorder for z in self.logorder]
        self.actual_x = [self.xbyyz[t][yz] for t in self.marked for yz in self.actual_yz]
        self.monomial = {z: ext.minimal_by_roots(z) for z in self.actual_x}
        self.regular_t = {t for t in self.marked if self.regular_trace_word(self.word[t] & (a - 1))}
        self.planes = {}
        for t in self.regular_t:
            for j in range(c):
                s = self.word[self.frob(t, j)] & (a - 1)
                assert s not in self.planes
                mapping = compile_map(lambda yz: self.word[self.frob(self.xbyyz[t][yz], j)] >> c, 2 * c)
                self.planes[s] = t, j, mapping
        self.full_map = compile_map(lambda z: self.full_word(z >> (2*c), (z >> c) & (a-1), z & (a-1)), b)
        for s, (t, j, mapping) in self.planes.items():
            for yz, m in enumerate(mapping):
                assert self.full_map[s * a * a + m] == self.word[self.frob(self.xbyyz[t][yz], j)]
        self.rotation_yz = {t: compile_map(lambda yz: self.yzbyx[t][self.fc[self.xbyyz[t][yz]]], 2 * c)
                            for t in self.regular_t}

    def frob(self, z, j):
        for _ in range(j):
            z = self.F[z]
        return z

    def full_word(self, trace, x, y):
        return (x << (2 * self.c)) | (y << self.c) | (trace ^ x ^ y)

    def regular_trace_word(self, s):
        rs = {right(s, self.c, j) for j in range(self.c)}
        return len(rs) == self.c and (s ^ (self.a - 1)) not in rs

    def regular_label(self, word, limit):
        lam, _, d = self.canonical[word]
        s = (word ^ (word >> self.c) ^ (word >> (2*self.c))) & (self.a - 1)
        return d == self.b and self.regular_trace_word(s) and lam >> (self.b - self.h) < limit

    def key_at_full_label(self, label):
        return self.ext.minimal_by_roots(self.normal_to_ambient[label])

    def forward_raw(self, proposed, limit, sign=1):
        # Starting array proposed[t, multiplicative y, multiplicative z] holds full r words.
        compact = {}
        by_t = {t: vals for t, vals in zip(self.marked, proposed)}
        for t in self.regular_t:
            original = by_t[t]
            additive = [None] * (self.a * self.a)
            for yz, r in zip(self.actual_yz, original, strict=True):
                additive[yz] = r
            compact[t] = []
            for yz, x in enumerate(self.xbyyz[t]):
                word = self.word[x]
                _, k, _ = self.canonical[word]
                compact[t].append([int(self.regular_label(word, limit)) * (additive[yz] >> ((k + sign * j) % self.b) & 1)
                                   for j in range(self.c)])
        normal = [0] * self.q
        for s, (t, j, mapping) in sorted(self.planes.items()):
            at_trace = [0] * (self.a ** 2)
            for yz, m in enumerate(mapping):
                at_trace[m] = compact[t][yz][j]
            for m, bit in enumerate(at_trace):
                normal[self.full_map[s * self.a**2 + m]] = bit
        return normal

    def encode_fs1(self, ambient, exception, limit):
        admitted = {}
        for p in range(limit):
            rows = gather_prefix(ambient, self.b, p)
            for tail, fields in enumerate(rows):
                word = (p << (self.b - self.h)) | tail
                if self.canonical[word][0] == word and self.regular_label(word, limit):
                    admitted[word] = sum(bit << j for j, bit in enumerate(fields))
        result = []
        for d, key, m in self.directory:
            result.append(admitted[integer(key)] if d == self.b and self.regular_label(integer(key), limit) else exception[m])
        return result

    def decode_fs1(self, replies, limit):
        groups, exception = {}, {}
        for (d, key, m), r in zip(self.directory, replies, strict=True):
            word = integer(key)
            if d == self.b and self.regular_label(word, limit):
                groups[word] = r
            else:
                exception[m] = r
        ambient = [0] * self.q
        for p in range(limit):
            rows = []
            for tail in range(1 << (self.b - self.h)):
                word = p << (self.b - self.h) | tail
                r = groups.get(word, 0)
                rows.append([r >> j & 1 for j in range(self.b)])
            added = scatter_prefix(rows, self.b, p)
            ambient = [x ^ y for x, y in zip(ambient, added, strict=True)]
        return ambient, exception

    def restore_points(self, ambient, exception, limit):
        slices = {t: [[None] * self.c for _ in range(self.a ** 2)] for t in self.regular_t}
        for s, (t, j, mapping) in self.planes.items():
            at_trace = [ambient[self.full_map[s * self.a**2 + m]] for m in range(self.a**2)]
            for yz, m in enumerate(mapping):
                slices[t][yz][j] = at_trace[m]
        output, wrong_single = [], 0
        for t in self.marked:
            for yz in self.actual_yz:
                x = self.xbyyz[t][yz]
                word = self.word[x]
                if self.regular_label(word, limit):
                    _, k, _ = self.canonical[word]
                    r, r_single = 0, 0
                    other = yz
                    for rotation in range(3):
                        for j, bit in enumerate(slices[t][other]):
                            position = (k + rotation * self.c + j) % self.b
                            r |= bit << position
                            r_single |= slices[t][yz][j] << position
                        other = self.rotation_yz[t][other]
                    assert other == yz
                    wrong_single += int(r != r_single)
                else:
                    r = exception[self.monomial[x]]
                output.append(compose(self.ext, r, x))
        return output, wrong_single


def trial(c, limits):
    g = Geometry(c)
    q, b = g.q, g.b
    rng = Random(194300 + b)
    poly = rng.getrandbits(q)
    original = [pdiv(poly, m)[1] for _, _, m in g.directory]
    target = {m: r for (_, _, m), r in zip(g.directory, original, strict=True)}
    values = [g.ext.horner(target[g.monomial[x]], x) for x in g.actual_x]
    for index in rng.sample(range(len(values)), min(7, len(values))):
        assert values[index] == g.ext.horner(poly, g.actual_x[index])
    proposals = []
    for x, y in zip(g.actual_x, values, strict=True):
        m, r, _ = projected_remainder(g.ext, x, y)
        assert m == g.monomial[x] and r == target[m]
        proposals.append(r)
    block = g.a * g.a
    proposals = [proposals[start:start+block] for start in range(0, len(proposals), block)]
    independent = [rng.getrandbits(d) for d, _, _ in g.directory]
    independent_map = {m: r for (_, _, m), r in zip(g.directory, independent, strict=True)}
    independent_points = [g.ext.horner(independent_map[g.monomial[x]], x) for x in g.actual_x]
    cases = []
    for limit in limits:
        assert 0 <= limit <= 1 << g.h
        accepted = [(integer(key), m) for d,key,m in g.directory if d == b and g.regular_label(integer(key), limit)]
        sparse = {m: r for (_, key, m), r in zip(g.directory, original, strict=True)
                  if m not in {u for _,u in accepted}}
        dense = g.forward_raw(proposals, limit)
        oracle = [0] * q
        for key, m in accepted:
            assert g.key_at_full_label(key) == m
            for j in range(b):
                oracle[right(key, b, j)] = target[m] >> j & 1
        assert dense == oracle
        assert g.encode_fs1(dense, sparse, limit) == original
        wrong_signed = sum(a != z for a,z in zip(g.forward_raw(proposals, limit, -1), oracle, strict=True))
        inv_raw, exceptions = g.decode_fs1(independent, limit)
        projected, wrong_single = g.restore_points(inv_raw, exceptions, limit)
        assert projected == independent_points
        assert g.encode_fs1(inv_raw, exceptions, limit) == independent
        proper = sum(1 for d, _, _ in g.directory if d != b)
        bad_trace = sum(1 for d, key, _ in g.directory if d == b and not g.regular_label(integer(key), 1 << g.h))
        high_prefix = len(g.directory) - len(accepted) - proper - bad_trace
        cases.append({'finite_prefix_threshold': limit, 'regular_full_factors': len(accepted),
                      'proper_factors': proper, 'irregular_trace_full_factors': bad_trace,
                      'high_prefix_full_factors': high_prefix, 'raw_orbit_bits': b * len(accepted),
                      'wrong_Frobenius_sign_bits': wrong_signed, 'repeating_single_slice_wrong_points': wrong_single})
    return {'b': b, 'c': c, 'q': q, 'ambient_field_poly': g.ext.modulus, 'FS1_field_poly': g.external.modulus,
            'marked_planes': len(g.marked), 'regular_marked_planes': len(g.regular_t), 'point_occurrences': len(g.actual_x),
            'true_FS1_factors': len(g.directory), 'cases': cases}


def unit_tests():
    rng = Random(55071)
    count = 0
    for d in range(1, 10):
        for _ in range(10):
            rows = [1 << i for i in range(d)]
            if d > 1:
                for _ in range(3*d):
                    i, j = rng.sample(range(d), 2)
                    if rng.randrange(2):
                        rows[i] ^= rows[j]
                    else:
                        rows[i], rows[j] = rows[j], rows[i]
            table = compiled_affine(tuple(rows), rng.randrange(1 << d))
            assert len(set(table)) == 1 << d
            count += len(table)
    # Prefix windows often overlap and wrap through index zero. Their adjoint must XOR all true paths.
    comparisons = 0
    for b in range(3, 13):
        h = (b - 1).bit_length()
        for p in {0, (1 << h) - 1, (1 << (h-1)) - 1}:
            a = [rng.getrandbits(1) for _ in range(1 << b)]
            matrix = gather_prefix(a, b, p)
            arbitrary = [[rng.getrandbits(1) for _ in row] for row in matrix]
            back = scatter_prefix(arbitrary, b, p)
            expected = [0] * (1 << b)
            for tail, row in enumerate(arbitrary):
                root = p << (b-h) | tail
                for j, bit in enumerate(row):
                    expected[right(root,b,j)] ^= bit
            assert expected == back
            assert (sum(x*y for x,y in zip(a,back)) & 1) == (sum(x*y for av,bv in zip(matrix,arbitrary)
                                                               for x,y in zip(av,bv)) & 1)
            comparisons += (1 << b) + len(matrix) * b
    return count, comparisons


if __name__ == '__main__':
    affine_cases, window_comparisons = unit_tests()
    trials = [trial(c, limits) for c, limits in [(1, (1,4)), (2, (1,8)), (3, (1,3,16)), (4, (1,3,16))]]
    assert any(z['high_prefix_full_factors'] for t in trials for z in t['cases'])
    assert sum(z['wrong_Frobenius_sign_bits'] for t in trials for z in t['cases']) > 0
    assert sum(z['repeating_single_slice_wrong_points'] for t in trials for z in t['cases']) > 0
    print(json.dumps({'affine_addresses_checked_against_direct_matrix': affine_cases,
                      'half_window_forward_and_adjoint_scalar_checks': window_comparisons,
                      'cases': trials}, indent=2))
