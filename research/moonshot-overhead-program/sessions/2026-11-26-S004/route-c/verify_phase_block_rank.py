#!/usr/bin/env python3
"""Independent exact controls for equivariant phase-block rank invoices."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib, json, random
from verify_inverse_query_commutator import Field, eye, inverse, multiply, rank, regular


def phase(alpha, r):
    counts = [alpha.count(j) for j in range(r)]
    anchor, maximum = alpha[0], max(counts)
    return (anchor+min((j-anchor) % r for j, v in enumerate(counts) if v == maximum)) % r


def boundary(alpha, r, t):
    c = sorted((alpha.count(j) for j in range(r)), reverse=True)
    return c[0]-c[1] <= 2*t


def difference(a, b, f):
    return [[f.sub(x, y) for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def complete_invertible(a, f):
    n = len(a)
    z = [row[:] + eye(n, f)[i] for i, row in enumerate(a)]
    pivots = []
    for col in range(n):
        k = len(pivots)
        found = next((i for i in range(k, n) if z[i][col]), None)
        if found is None:
            continue
        z[k], z[found] = z[found], z[k]
        scale = f.inv(z[k][col])
        z[k] = [f.mul(x, scale) for x in z[k]]
        for i in range(n):
            if i != k and z[i][col]:
                c = z[i][col]
                z[i] = [f.sub(x, f.mul(c, y)) for x, y in zip(z[i], z[k])]
        pivots.append(col)
    reduced, transform = [row[:n] for row in z], [row[n:] for row in z]
    for offset, col in enumerate(j for j in range(n) if j not in pivots):
        reduced[len(pivots)+offset][col] = 1
    out = multiply(inverse(transform, f), reduced, f)
    assert rank(out, f) == n
    assert rank(difference(out, a, f), f) == n-len(pivots)
    return out


def block_part(a, phases):
    return [[v if phases[i] == phases[j] else 0 for j, v in enumerate(row)] for i, row in enumerate(a)]


def complete_blocks(a, phases, r, f):
    out = [row[:] for row in a]
    for p in range(r):
        indices = [i for i, v in enumerate(phases) if v == p]
        block = [[a[i][j] for j in indices] for i in indices]
        done = complete_invertible(block, f)
        for i, row in zip(indices, done):
            for j, value in zip(indices, row):
                out[i][j] = value
    return out


def main():
    checks, rng = Counter(), random.Random(2026112508)
    for r in (2, 3, 4, 5):
        for m in range(1, 8 if r <= 3 else 5):
            alphas = list(product(range(r), repeat=m))
            phases = {a: phase(a, r) for a in alphas}
            changes = {t: [b for b in alphas if sum(x != 0 for x in b) <= t] for t in range(min(2, m)+1)}
            assert set(Counter(phases.values()).values()) == {r**(m-1)}
            for a in alphas:
                shifted = tuple((x+1) % r for x in a)
                assert phases[shifted] == (phases[a]+1) % r
                checks['equivariant_phase_assignments'] += 1
                for t, terms in changes.items():
                    if boundary(a, r, t):
                        continue
                    for b in terms:
                        gamma = tuple((x+y) % r for x, y in zip(a, b))
                        assert phases[gamma] == phases[a]
                        checks['off_boundary_phase_preservation'] += 1
    for r, f in ((2, Field(5)), (3, Field(4))):
        for m in range(1, 4):
            alphas = list(product(range(r), repeat=m))
            n, w = r**m, 3
            phases = [phase(a, r) for a in alphas for _ in range(w)]
            q = {(0,)*m: [[0]*w for _ in range(w)]}
            for i in range(w):
                exponent = tuple(int(j == i % m) for j in range(m))
                q.setdefault(exponent, [[0]*w for _ in range(w)])
                q[exponent][i][i] = 1
                if i+1 < w:
                    q[exponent][i][i+1] = q[(0,)*m][i][i+1] = 1
            reg = regular(q, m, r, w, w, f)
            inv = inverse(reg, f)
            assert inv is not None
            diag = block_part(reg, phases)
            delta = rank(difference(reg, diag, f), f)
            bsize = sum(boundary(a, r, 1) for a in alphas)
            assert delta <= w*bsize
            nullity = n*w-rank(diag, f)
            assert nullity <= delta
            completed = complete_blocks(diag, phases, r, f)
            inv_comparison = inverse(completed, f)
            assert rank(difference(reg, completed, f), f) <= 2*delta
            assert rank(difference(inv, inv_comparison, f), f) <= 2*delta
            checks['inverse_pencil_block_completions'] += 1
            checks['genuinely_singular_block_parts'] += nullity > 0
            target = regular({(1,)*m: eye(w, f)}, m, r, w, w, f)
            assert rank(difference(target, eye(n*w, f), f), f)*r == (r-1)*n*w
            checks['sharp_cyclic_distance_witnesses'] += 1
            for rep in range(3):
                a = {alpha: [[rng.randrange(f.order) for _ in range(w)] for _ in range(w)]
                     for alpha in alphas if sum(x != 0 for x in alpha) <= 1}
                av = regular(a, m, r, w, w, f)
                az = block_part(av, phases)
                da = rank(difference(av, az, f), f)
                assert da <= w*bsize
                assert rank(difference(target, az, f), f)*r >= (r-1)*n*w
                for left in (False, True):
                    p = multiply(inv, av, f) if left else multiply(av, inv, f)
                    z = multiply(inv_comparison, az, f) if left else multiply(az, inv_comparison, f)
                    assert z == block_part(z, phases)
                    assert rank(difference(p, z, f), f) <= da+2*delta
                    assert (rank(difference(target, p, f), f)+da+2*delta)*r >= (r-1)*n*w
                    checks['noncommuting_fraction_bounds'] += 1
                checks['block_diagonal_cyclic_distance_bounds'] += 1
    a = (0, 1, 2)
    shifted = tuple((x+1) % 3 for x in a)
    naive = lambda x: min(range(3), key=lambda j: -x.count(j))
    assert naive(shifted) != (naive(a)+1) % 3
    result = dict(status='passed', arithmetic='exact F4, F5 and integer combinatorics',
                  seed=2026112508, counts=dict(checks),
                  negative_control='least-index tie rule fails cyclic equivariance on (0,1,2)',
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  helper_sha256=hashlib.sha256(Path(__file__).with_name('verify_inverse_query_commutator.py').read_bytes()).hexdigest(),
                  scope='Finite phase, rank-completion and fraction tests; no physical inverse or tape-time lower bound')
    Path('phase-block-rank-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
