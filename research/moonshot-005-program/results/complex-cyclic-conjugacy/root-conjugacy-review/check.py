#!/usr/bin/env python3
"""Independent exact cyclic conjugacy and literal source-channel checks.

No author code imported. Finite controls supplement the universal written
spectral/rank-factorization audit; they are not an asymptotic extrapolation.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix


def norm(m):
    return m.applyfunc(s.expand)


def rank(m):
    return DomainMatrix.from_Matrix(norm(m)).convert_to(QQ_I).rank()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author-result', type=Path, required=True)
    parser.add_argument('--proof', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.author_result.read_text())

    def matrix(rows):
        return s.Matrix([[s.Rational(z[0])+s.I*s.Rational(z[1]) for z in row] for row in rows])

    p0 = s.diag(0, 0, 1)
    e01 = s.zeros(3)
    e01[0, 1] = 1

    def reconstruct(ps, ms):
        if any(norm(p*p) != p or rank(p) != 1 for p in ps):
            raise ValueError('sector_projector')
        if any(b == s.zeros(3) for row in ms for b in row):
            raise ValueError('zero_channel')
        joint = s.BlockMatrix(ms).as_explicit()
        if rank(joint) != 1:
            raise ValueError('joint_rank')
        # Independent factor normalization: choose the first nonzero row,
        # normalize its first nonzero entry to one in the LEFT column.
        pivot_row, pivot_col = next((i, j) for i in range(12) for j in range(12) if joint[i, j] != 0)
        left = joint[:, pivot_col] / joint[pivot_row, pivot_col]
        right = -joint[pivot_row, :]
        assert norm(-left*right) == joint
        qs, inverses = [], []
        for sector, p in enumerate(ps):
            u, v = left[3*sector:3*sector+3, :], right[:, 3*sector:3*sector+3]
            if norm(p*u) != s.zeros(3, 1) or norm(v*p) != s.zeros(1, 3) or norm(v*u) != s.zeros(1):
                raise ValueError('flag')
            w = next(p[:, j] for j in range(3) if p[:, j] != s.zeros(3, 1))
            j = next(j for j in range(3) if v[j] != 0)
            z = (s.eye(3)-p)[:, j]/v[j]
            inverse = norm(s.Matrix.hstack(u, z, w))
            assert rank(inverse) == 3
            q = norm(inverse.inv())
            assert norm(inverse*p0*q) == p
            qs.append(q)
            inverses.append(inverse)
        for i, j in itertools.product(range(4), repeat=2):
            assert norm(-inverses[i]*e01*qs[j]) == ms[i][j]
        return qs, inverses

    ps = [matrix(p) for p in data['P_sector_matrices']]
    ms = [[matrix(b) for b in row] for row in data['M_channel_matrices']]
    recovered, recovered_inverse = reconstruct(ps, ms)
    author_q = [matrix(q) for q in data['recovered_sector_units']]
    author_r = [matrix(q) for q in data['recovered_sector_inverses']]
    for i in range(4):
        assert norm(author_q[i]*author_r[i]) == norm(author_r[i]*author_q[i]) == s.eye(3)
        assert norm(author_r[i]*p0*author_q[i]) == ps[i]
    for i, j in itertools.product(range(4), repeat=2):
        assert norm(-author_r[i]*e01*author_q[j]) == ms[i][j]

    def fourier(table):
        return [norm(sum((s.I**(-j*k)*table[k] for k in range(4)), s.zeros(3))/4) for j in range(4)]

    def product(left, right):
        return [norm(sum((left[j]*right[(k-j)%4] for j in range(4)), s.zeros(3))) for k in range(4)]

    qpoly, rpoly = fourier(recovered), fourier(recovered_inverse)
    identity = [s.eye(3), s.zeros(3), s.zeros(3), s.zeros(3)]
    assert product(qpoly, rpoly) == product(rpoly, qpoly) == identity
    bic = [[norm(sum((s.I**(-j*u-k*v)*ms[u][v] for u, v in itertools.product(range(4), repeat=2)), s.zeros(3))/16) for k in range(4)] for j in range(4)]
    for u, v in itertools.product(range(4), repeat=2):
        assert norm(sum((s.I**(u*j+v*k)*bic[j][k] for j, k in itertools.product(range(4), repeat=2)), s.zeros(3))) == ms[u][v]

    # A separate, nontriangular family with complex coefficients exercises
    # different projectors and both directions of every phase channel.
    additional = [
        s.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        s.Matrix([[1, s.I, 1], [0, 1, 0], [1, 0, 2]]),
        s.Matrix([[0, 1, 0], [0, 0, 1], [1, 1, 0]]),
        s.Matrix([[1, 0, 1], [s.I, 1, 0], [0, 1, 1]]),
    ]
    additional_inv = [norm(q.inv()) for q in additional]
    extra_ps = [norm(additional_inv[i]*p0*additional[i]) for i in range(4)]
    extra_ms = [[norm(-additional_inv[i]*e01*additional[j]) for j in range(4)] for i in range(4)]
    reconstruct(extra_ps, extra_ms)

    controls = []
    def reject(test_ps, test_ms, expected):
        try:
            reconstruct(test_ps, test_ms)
        except ValueError as error:
            assert str(error) == expected
            controls.append(expected)
        else:
            raise AssertionError('Negative control accepted')

    incoherent = [[-(s.Rational(3, 2) if i == j == 3 else 1)*e01 for j in range(4)] for i in range(4)]
    assert all(rank(b) == 1 for row in incoherent for b in row)
    assert rank(s.BlockMatrix(incoherent).as_explicit()) == 2
    reject([p0]*4, incoherent, 'joint_rank')
    wrong_ps = list(ps)
    wrong_ps[0] = s.diag(1, 0, 0)
    reject(wrong_ps, ms, 'flag')
    wrong_ps[0] = s.zeros(3)
    reject(wrong_ps, ms, 'sector_projector')
    wrong_ms = [list(row) for row in ms]
    wrong_ms[3][3] = s.zeros(3)
    reject(ps, wrong_ms, 'zero_channel')

    # Reconstruct the literal C_b D_acd P matrix, including coefficients.
    dimension = 16
    rotation, sign, flip = s.zeros(16), s.eye(16), s.zeros(16)
    for x in range(16):
        rotation[(x >> 1) | ((x & 1) << 3), x] = 1
        sign[x, x] = -1 if (x & 13) == 13 else 1
        flip[x ^ 2, x] = 1
    actual = norm(((1+s.I)*s.eye(16)+(1-s.I)*flip)*sign*rotation/2)
    assert norm(actual.conjugate().T*actual) == s.eye(16)
    support = [(y, x) for y in range(16) for x in range(16) if actual[y, x] != 0]
    assert len(support) == 32
    beta = [
        lambda a,b,c,d: b,
        lambda a,b,c,d: c,
        lambda a,b,c,d: b ^ (c*d),
        lambda a,b,c,d: c ^ (a*b),
    ]
    channels = []
    for function in beta:
        table = [function(*[(x >> j)&1 for j in range(4)]) for x in range(16)]
        assert table.count(0) == table.count(1) == 8
        pairs = {}
        for y, x in support:
            pairs.setdefault((table[y], table[x]), (y, x))
        assert set(pairs) == {(0,0),(0,1),(1,0),(1,1)}
        for outsector, insector in itertools.product(range(4), repeat=2):
            entries = [pairs[(int(j < outsector), int(j < insector))] for j in range(3)]
            assert sum(table[y] for y,x in entries) == outsector
            assert sum(table[x] for y,x in entries) == insector
            assert s.prod(actual[y,x] for y,x in entries) != 0
        # This verifies actual Fourier coefficient phases at width one;
        # width-three witnesses above establish all sixteen channels.
        projectors = [s.diag(*[int(table[x] == k) for x in range(16)]) for k in range(4)]
        h = s.diag(*[s.I**k for k in table])
        for k in range(4):
            assert norm(sum((s.I**(-k*j)*h**j for j in range(4)), s.zeros(16))/4) == projectors[k]
        channels.append({'one_column_phase_pairs':4,'nonzero_width3_channels':16})

    # The rank-D false positive has sector projector ranks (2,0,2,0).
    # The all-width argument uses trace(h^2)=0, not these finite checks.
    import math
    rank_control = []
    for width in range(1,8):
        counts = [8**width*sum(math.comb(width,k) for k in range(width+1) if k%4 == j) for j in range(4)]
        assert 2*(counts[0]+counts[2]) == dimension**width
        rank_control.append(width)
    result = {
        'status':'PASS_ROOT_INDEPENDENT_CYCLIC_CONJUGACY',
        'author_result_sha256':hashlib.sha256(args.author_result.read_bytes()).hexdigest(),
        'proof_sha256':hashlib.sha256(args.proof.read_bytes()).hexdigest(),
        'method':'Independent SymPy/QQ(i) joint-rank factorization, explicit source matrix and Fourier arithmetic; no author code imported.',
        'author_family_cross_sector_identities':16,
        'additional_family_cross_sector_identities':16,
        'both_reconstructed_inverse_products':True,
        'double_fourier_coefficients_checked':16,
        'literal_source_nonzero_entries':len(support),
        'source_channel_controls':channels,
        'negative_controls':controls,
        'physical_rank_false_positive_widths_checked':rank_control,
        'universal_basis':'Separate spectral-support and constructive rank-one proof audit. Finite checks supplement this argument.',
        'ordinary_C_proved':False,
        'independent_421_endpoint_proved':False,
        'new_complete_kappa':False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
