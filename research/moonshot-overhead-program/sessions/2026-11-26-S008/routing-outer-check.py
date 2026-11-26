"""Finite exact checks for source guarded permutations and the S008 numerical charges."""

from itertools import permutations, product
from math import prod
from random import Random
import json


def benes(perm):
    """Return layers (target bit, switch keyed by the other bits of the wire)."""
    n = len(perm)
    assert n >= 2 and n & (n - 1) == 0 and sorted(perm) == list(range(n))
    h = n // 2
    if h == 1:
        return [(0, {0: perm[0]})]
    inv = [None] * n
    for x, y in enumerate(perm):
        inv[y] = x
    color = [-1] * n
    for root in range(n):
        x, c = root, 0
        while color[x] < 0:
            color[x] = c
            x = x ^ h if c == 0 else inv[perm[x] ^ h]
            c ^= 1
    assert all(color[x] != color[x ^ h] and color[x] != color[inv[perm[x] ^ h]] for x in range(n))
    first = {x: color[x] for x in range(h)}
    last = {y: color[inv[y]] for y in range(h)}
    child = [[0] * h for _ in (0, 1)]
    for x, y in enumerate(perm):
        child[color[x]][x % h] = y % h
    inner = []
    for (bit, zero), (bit1, one) in zip(benes(child[0]), benes(child[1])):
        assert bit == bit1
        inner.append((bit, zero | {h + x: flip for x, flip in one.items()}))
    return [(h.bit_length() - 1, first), *inner, (h.bit_length() - 1, last)]


def apply(layers, x):
    for j, table in layers:
        if table[x & ~(1 << j)]:
            x ^= 1 << j
    return x


def network_checks(rng):
    samples = [*permutations(range(2)), *permutations(range(4))]
    for n in (8, 16, 32):
        for _ in range(64):
            p = list(range(n))
            rng.shuffle(p)
            samples.append(p)
    checks = 0
    for p in samples:
        layers = benes(p)
        assert len(layers) == 2 * (len(p).bit_length() - 1) - 1
        for x, y in enumerate(p):
            assert apply(layers, x) == y
            assert apply(reversed(layers), y) == x
            checks += 2
    return {'permutations': len(samples), 'forward_and_inverse_wires': checks}


# (target register 0 for Y or 1 for Z, required parity on the other, sign)
SHIFTS = [(0, 0, -1), (1, 0, -1), (0, 0, 1), (1, 0, 1),
          (1, 1, 1), (0, 1, 1), (1, 1, -1), (0, 1, -1)]


def shift(y, z, u, positions, controls, inverse=False):
    pair = [y, z]
    for i, parity, sign in reversed(SHIFTS) if inverse else SHIFTS:
        offset = sum(c << j for c, j in zip(controls, positions) if (pair[1-i] >> j) & 1 == parity)
        pair[i] = (pair[i] + (-sign if inverse else sign) * offset) % (1 << u)
    return tuple(pair)


def exceptional(y, z, guard_width, positions):
    q = 1 << (guard_width - 1)
    return any(v < 10 or v >= q - 10 for word in (y, z) for j in positions
               for v in [(word >> (j + 1)) % q])


def guard_checks(rng):
    checks = safe = moved = 0
    for g, u, positions in ((6, 6, [0]), (6, 12, [0, 6]), (7, 16, [1, 9])):
        controls_list = list(product((0, 1), repeat=len(positions)))
        sample = (product(range(1 << u), repeat=2) if u == g else
                  ((rng.randrange(1 << u), rng.randrange(1 << u)) for _ in range(8192)))
        for y, z in sample:
            for c in controls_list:
                actual = shift(y, z, u, positions, c)
                mask = sum(cj << j for j, cj in zip(positions, c))
                desired = y ^ mask, z
                assert exceptional(*actual, g, positions) == exceptional(y, z, g, positions)
                if not exceptional(*actual, g, positions):
                    assert actual == desired
                    safe += 1
                else:
                    old_y, old_z = shift(*actual, u, positions, c, inverse=True)
                    assert (old_y ^ mask, old_z) == desired
                    moved += actual != desired
                checks += 1
    assert safe and moved
    return {'executions': checks, 'nonexceptional': safe, 'nonidentity_repairs': moved}


def crt_checks():
    valid = all_addresses = table_calls = 0
    for axes in ((3, 5, 4), (7, 5, 3, 4), (5, 7, 11, 3, 2)):
        ext = [1 << (a-1).bit_length() for a in axes]
        prefix = [prod(axes[:i]) for i in range(len(axes))]
        mu = [pow(p, -1, a) for p, a in zip(prefix, axes)]
        def intervals(lo, hi, depth, levels):
            if hi - lo <= 1:
                return
            mid = lo + (hi-lo)//2
            levels.setdefault(depth, []).append((lo, mid, hi))
            intervals(lo, mid, depth+1, levels)
            intervals(mid, hi, depth+1, levels)
        levels = {}
        intervals(0, len(axes), 0, levels)
        cache = {}
        def transform(x, inv):
            nonlocal table_calls
            x = list(x)
            for level in sorted(levels, reverse=not inv):
                for lo, mid, hi in levels[level]:
                    acc = 0
                    good = all(x[i] < axes[i] for i in range(lo, mid))
                    if good:
                        for j in range(lo, mid):
                            acc += prefix[j] * ((x[j] - mu[j] * acc) % axes[j])
                    for i in range(mid, hi):
                        rot = (mu[i] * acc * (-1 if inv else 1)) % axes[i]
                        key = (i, rot)
                        if key not in cache:
                            table = [(v + rot) % axes[i] if v < axes[i] else v for v in range(ext[i])]
                            cache[key] = benes(table)
                        x[i] = apply(cache[key], x[i])
                        table_calls += 1
            return tuple(x)
        images = set()
        for x in product(*(range(a) for a in ext)):
            out = transform(x, False)
            assert transform(out, True) == x and out not in images
            images.add(out)
            if all(d < a for d, a in zip(x, axes)):
                value = sum(p*d for p, d in zip(prefix, x))
                assert out == tuple(m*value % a for m, a in zip(mu, axes))
                valid += 1
            all_addresses += 1
    return {'valid_residue_addresses': valid, 'all_padded_addresses': all_addresses,
            'actual_block_table_applications': table_calls}


def bounds():
    points = {1 << 32}
    for e in range(32, 160):
        points.update(x for x in ((1 << e)-1, 1 << e, (1 << e)+1) if x >= 1 << 32)
    for k in points:
        b = (2*k-1).bit_length()
        g = 2048*b
        h = k // (64*g)
        assert k >= 128*g and (k+h-1)//h <= 129*g
        assert 140*b*h <= k//512 and 2*g*h <= k//32
        assert 4*(2*g*h + 140*b*h) <= k
        p = (2*k)**140
        a = 4096*(k+1)**3*(p+1)**2
        w = 8*k+8
        assert p <= k**150 and a <= k**304 and a.bit_length() < k
        assert 2**14*(a+1)*(w+1)**5 <= k**311
        ops = 2**16*(k+1)**4*(p+1)**3
        assert ops <= k**455
        assert 16*ops*k**311 + 4*(a+1)*(w+1) <= k**1024
        assert 129*2048*280 < 2**27 and 1125*k.bit_length() < k
    return len(points)


if __name__ == '__main__':
    rng = Random(410049)
    print(json.dumps(dict(network=network_checks(rng), guarded=guard_checks(rng),
                          crt=crt_checks(), exact_guard_cases=bounds()), sort_keys=True, indent=2))
