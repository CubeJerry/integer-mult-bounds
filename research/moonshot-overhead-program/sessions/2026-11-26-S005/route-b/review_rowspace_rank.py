#!/usr/bin/env python3
"""Independent exact checks for the lead's row-space/Walsh gate."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def parity(x):
    return x.bit_count() & 1


def binary_rank(rows):
    pivots = {}
    for value in rows:
        v = value
        while v:
            bit = v.bit_length()-1
            if bit not in pivots:
                pivots[bit] = v
                break
            v ^= pivots[bit]
    return len(pivots)


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def exact_rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    rank = 0
    for j in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        z = a[rank][j]
        a[rank] = [x/z for x in a[rank]]
        for i in range(rank+1, len(a)):
            z = a[i][j]
            if z:
                a[i] = [x-z*y for x,y in zip(a[i], a[rank])]
        rank += 1
    return rank


def cofactor_counts():
    out = []
    for A in range(2, 5):
        counts = Counter()
        total = 2**(A*(A-1))
        for B in product(range(2**A), repeat=A-1):
            if binary_rank(B) != A-1:
                continue
            vectors = [c for c in range(1, 2**A)
                       if all(parity(c & b) == 0 for b in B)]
            assert len(vectors) == 1
            counts[vectors[0]] += 1
        assert set(counts) == set(range(1, 2**A))
        assert len(set(counts.values())) == 1
        alpha = Fraction(1)
        for j in range(2, A+1):
            alpha *= 1-Fraction(1, 2**j)
        assert Fraction(sum(counts.values()), total) == alpha
        beta = alpha*Fraction(3*2**(A-1)-1, 4*(2**A-1))
        assert beta > Fraction(3, 16)
        for f in range(A, A+3):
            Q = 2**f
            rank = sum(number*(Q//2 if parity(c) else Q//4)
                       for c, number in counts.items())
            rank *= 2**((A-1)*(f-A))
            assert rank == 2**(A*f)*beta
        out.append({'A':A, 'full_rank_B0': sum(counts.values()),
                    'cofactor_multiplicity':next(iter(counts.values())),
                    'alpha':str(alpha), 'beta':str(beta)})
    return out


def halfspace_checks():
    checks = 0
    rank_checks = 0
    for f in range(1, 7):
        Q = 2**f
        for c in range(1, Q):
            U = [y for y in range(Q) if parity(c & y) == 0]
            V = [x for x in range(Q) if parity(c & x) == 1]
            M = [[(-1)**parity(y & x) for x in V] for y in U]
            gram = matmul(M, list(map(list, zip(*M))))
            t = 1 if parity(c) else 2
            gram_squared = matmul(gram, gram)
            assert gram_squared == [[(Q*t//2)*x for x in row] for row in gram]
            # Forming M M^T proves positivity; this exact polynomial identity
            # makes each nonzero normalized eigenvalue t/2.
            trace = sum(gram[i][i] for i in range(len(U)))
            assert Fraction(trace, Q*t//2) == Q//(2*t)
            if f <= 4:
                assert exact_rank(M) == Q//(2*t)
                rank_checks += 1
            checks += 1
    # Omitted-radical control: c=11 has rank 1, not Q/2=2.
    f, c = 2, 3
    U, V = [0, 3], [1, 2]
    M = [[(-1)**parity(y & x) for x in V] for y in U]
    assert exact_rank(M) == 1 != 2
    return {'character_gram_checks':checks, 'literal_rational_rank_checks':rank_checks,
            'isotropic_radical_control':True}


def separator_checks():
    cases = 0
    for A in (2, 3):
        f = A
        invertible = [g for g in product(range(2**A), repeat=A) if binary_rank(g) == A]
        for rows in product(range(2**f), repeat=A):
            determinant = int(binary_rank(rows) == A)
            for g in invertible:
                transformed = []
                for g_row in g:
                    word = 0
                    for i, row in enumerate(rows):
                        if g_row >> i & 1:
                            word ^= row
                    transformed.append(word)
                assert int(binary_rank(transformed) == A) == determinant
                cases += 1
    return {'explicit_GL_separator_checks':cases}


def main():
    proof = HERE.parent/'lead/rowspace-walsh-rank-gate.md'
    receipt = {'status':'PASS', 'independent_method':'Integer character Gram idempotence, rational ranks, binary kernel counts.',
               'scope':'Finite independent evidence for RG; no tape time or asymptotic execution.',
               'cofactors':cofactor_counts(), 'halfspaces':halfspace_checks(), 'separator':separator_checks(),
               'source_sha256':{str(proof.relative_to(HERE.parent)):sha256(proof.read_bytes()).hexdigest(),
                                Path(__file__).name:sha256(Path(__file__).read_bytes()).hexdigest()}}
    (HERE/'rowspace-rank-independent-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__ == '__main__':
    main()
