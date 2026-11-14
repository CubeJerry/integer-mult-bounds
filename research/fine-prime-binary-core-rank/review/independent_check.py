"""Independent exact algebra; no author imports or floating exponentials.

The classical transcendence theorem is a cited premise, not a finite test.
Default is read-only; --write explicitly saves a deterministic receipt.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from math import gcd, prod, isqrt
from pathlib import Path
import argparse
import json
import random


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add_term(poly, exponent, coefficient):
    poly[exponent] = poly.get(exponent, 0) + coefficient
    if not poly[exponent]:
        del poly[exponent]


def determinant(entries, zero, add_exponents):
    n = len(entries); dp = {0: {zero: 1}}
    for i in range(n):
        after = {}
        for used, poly in dp.items():
            for j in range(n):
                if used >> j & 1:
                    continue
                sign = -1 if (used >> (j + 1)).bit_count() % 2 else 1
                target = after.setdefault(used | (1 << j), {})
                for a, x in poly.items():
                    for b, y in entries[i][j].items():
                        add_term(target, add_exponents(a, b), sign * x * y)
        dp = after
    return dp[(1 << n) - 1]


def dense_det(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]; value = Fraction(1)
    for c in range(len(a)):
        pivot = next((i for i in range(c, len(a)) if a[i][c]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]; value = -value
        v = a[c][c]; value *= v
        for i in range(c + 1, len(a)):
            ratio = a[i][c] / v
            for j in range(c + 1, len(a)):
                a[i][j] -= ratio * a[c][j]
            a[i][c] = 0
    return value


def matching_matrix(order, mask):
    n = len(order)
    return [[int(order[i] ^ order[j] == mask) -
             (int(order[i-1] ^ order[j-1] == mask) if i and j else 0)
             for j in range(n)] for i in range(n)]


def paths_for_minor(matrix):
    """Use signed matrix adjacency after cancellation, not author graph data."""
    n = len(matrix); neighbors = [[j for j in range(n) if matrix[i][j]] for i in range(n)]
    unseen, paths = {i for i in range(n) if neighbors[i]}, []
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            i = stack.pop()
            if i in component:
                continue
            component.add(i); stack.extend(neighbors[i])
        unseen -= component
        ends = [i for i in component if len(neighbors[i]) == 1]
        if not ends:
            a = min(component); b = min(neighbors[a]); component -= {a, b}
            if not component:
                continue
            ends = [i for i in component if sum(j in component for j in neighbors[i]) == 1]
        need(len(ends) == 2, 'retained path endpoints')
        path, previous, current = [], None, min(ends)
        while True:
            path.append(current)
            following = [j for j in neighbors[current] if j in component and j != previous]
            if not following:
                break
            need(len(following) == 1, 'simple path')
            previous, current = current, following[0]
        need(set(path) == component and len(path) % 2 == 0, 'complete even path')
        paths.append(path)
    return paths


def trim(paths, size):
    need(size >= 0 and size % 2 == 0 and size <= sum(map(len, paths)), 'even trim domain')
    left, kept = size, []
    for path in paths:
        take = min(left, len(path)); kept.extend(path[:take]); left -= take
    need(left == 0 and len(kept) == size, 'requested trimmed size')
    return sorted(kept)


def gaussian_entries(order, kept, weights=None):
    d = (len(order) - 1).bit_length(); entries = []
    def monomial(mask):
        bits = tuple((mask >> k) & 1 for k in range(d))
        return bits if weights is None else sum(x * e for x, e in zip(bits, weights))
    for i in kept:
        row = []
        for j in kept:
            poly = {monomial(order[i] ^ order[j]): 1}
            if i and j:
                add_term(poly, monomial(order[i-1] ^ order[j-1]), -1)
            row.append(poly)
        entries.append(row)
    return entries


def weights_for(moduli, targets):
    need(len(moduli) == len(targets) and all(m >= 2 for m in moduli), 'modulus domain')
    need(all(gcd(a, b) == 1 for i, a in enumerate(moduli) for b in moduli[:i]), 'pairwise coprime moduli')
    need(all(t > 0 and gcd(t, m) == 1 for t, m in zip(targets, moduli)), 'unit targets')
    M = prod(moduli)
    return tuple(t * (M // m) for t, m in zip(targets, moduli))


def substitute(poly, moduli, targets):
    weights = weights_for(moduli, targets); seen, output = {}, {}
    for powers, coefficient in poly.items():
        need(all(0 <= a < m for a, m in zip(powers, moduli)), 'strict individual degree guard')
        power = sum(a * e for a, e in zip(powers, weights))
        need(power not in seen, 'CRT monomial injection')
        seen[power] = powers; output[power] = coefficient
    return output


def prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n) + 1))


def certified_minor(order, moduli, targets):
    n = len(order); d = len(moduli); bound = 2 * ((n + 7) // 5)
    need(n == 1 << d and all(prime(s) and s % 2 for s in moduli), 'declared prime family')
    candidates = []
    for v in range(1, n):
        matrix = matching_matrix(order, v); paths = paths_for_minor(matrix)
        candidates.append((sum(map(len, paths)), v, matrix, paths))
    available, mask, matrix, paths = max(candidates, key=lambda item: (item[0], -item[1]))
    need(available >= bound, 'inherited A9 certificate bound')
    size = min(bound, min(moduli)-1); kept = trim(paths, size)
    coefficient = dense_det([[matrix[i][j] for j in kept] for i in kept])
    need(abs(coefficient) == 1, 'trimmed unit determinant')
    poly = determinant(gaussian_entries(order, kept), (0,)*d,
                       lambda a,b: tuple(x+y for x,y in zip(a,b)))
    target = tuple(size * ((mask >> k) & 1) for k in range(d))
    need(poly.get(target) == coefficient, 'trimmed isolated coefficient')
    mapped = substitute(poly, moduli, targets)
    direct = determinant(gaussian_entries(order, kept, weights_for(moduli, targets)), 0,
                         lambda a,b: a+b)
    need(mapped == direct and mapped, 'direct univariate determinant agrees')
    return dict(N=n,rank_floor=size,mask=mask,certificate_size=available,
                monomials=len(poly),univariate_terms=len(mapped),degree=max(max(e) for e in poly))


def complete_box(moduli, targets):
    weights = weights_for(moduli, targets); seen = set()
    for powers in product(*(range(m) for m in moduli)):
        value = sum(a * e for a, e in zip(powers, weights))
        need(value not in seen, 'full finite exponent box injection'); seen.add(value)
    return len(seen)


def dense_rank(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]; row=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(row,len(a)) if a[i][c]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]; value=a[row][c]
        for i in range(row+1,len(a)):
            factor=a[i][c]/value
            for j in range(c,len(a[0])):a[i][j]-=factor*a[row][j]
        row+=1
        if row==len(a):break
    return row


def stein(matrix):
    n=len(matrix)
    return [[matrix[i][j]-(matrix[i-1][j-1] if i and j else 0)
             for j in range(n)] for i in range(n)]


def rejected(call, expected):
    try:call()
    except ValueError as error:need(str(error)==expected,'exact guard rejection')
    else:raise ValueError('missing guard: '+expected)


def control_checks():
    controls=[]
    rejected(lambda:substitute({(3,0):1,(0,5):-1},(3,5),(8,8)),
             'strict individual degree guard')
    e=weights_for((3,5),(8,8))
    need(3*e[0]==5*e[1],'actual high-degree collision')
    controls.append('Q1^3-Q2^5 vanishes after (3,5)/(8,8) substitution; degree guard is essential')
    rejected(lambda:weights_for((9,27),(8,8)),'pairwise coprime moduli')
    raw=(8*27,8*9)
    need(raw[0]==3*raw[1] and 1<9 and 3<27,'odd noncoprime low-degree collision')
    controls.append('distinct odd denominators9,27 collide already at Q1-Q2^3')
    rejected(lambda:weights_for((5,5),(8,16)),'pairwise coprime moduli')
    controls.append('repeated source prime rejected')
    rejected(lambda:weights_for((5,7),(5,7)),'unit targets')
    need(5*7==7*5,'nonunit-target exponent collision')
    controls.append('nonunit targets5,7 make Q1=Q2 despite distinct denominators5,7')
    rejected(lambda:trim([[0,1,2,3]],3),'even trim domain')
    controls.append('odd requested trim rejected')
    alpha=105; weights=weights_for((3,5,7),(8,16,32))
    scaled={alpha*alpha*sum(a*e for a,e in zip(powers,weights))
            for powers in product(range(3),range(5),range(7))}
    need(len(scaled)==105 and all(gcd(alpha,s)>1 for s in (3,5,7)), 'common alpha needs no unit guard')
    controls.append('common alpha105 shares every prime but preserves all105 exponent-box values')

    # True diagonal similarity, rather than an unrelated two-sided gauge.
    q=Fraction(1,2); order=(0,1,3,2); D=(1,2,3,4)
    K=[[q**((x^y).bit_count()) for y in order] for x in order]
    conjugated=[[K[i][j]*Fraction(D[i],D[j]) for j in range(4)] for i in range(4)]
    need(dense_rank(stein(K))==2 and dense_rank(stein(conjugated))==4,'binary similarity rank change')
    need(dense_det(stein(conjugated))==Fraction(-3,512),'binary similarity exact determinant')
    controls.append('homogeneous binary Gray core changes Stein rank2->4 under diag(1,2,3,4) similarity')
    entries=[]; D=(1,2,3)
    for i in range(3):
        row=[]
        for j in range(3):
            p={(i-j)**2:Fraction(D[i],D[j])}
            if i and j:add_term(p,(i-j)**2,-Fraction(D[i-1],D[j-1]))
            row.append(p)
        entries.append(row)
    det=determinant(entries,0,lambda a,b:a+b)
    need(det=={2:Fraction(1,12),6:Fraction(-1,12)},'symbolic Gaussian similarity witness')
    controls.append('3x3 Gaussian similarity has exact determinant q^2(1-q^4)/12')
    large=[[q**((i-j)**2) for j in range(5)] for i in range(5)]
    keep=(0,1,3,4); compressed=[[large[i][j] for j in keep] for i in keep]
    need(dense_rank(stein(large))==2 and dense_rank(stein(compressed))==4,'compression changes shift')
    controls.append('Gaussian Toeplitz5x5 rank2 has irregular4x4 section with Stein rank4; no section lifting')
    theta=Fraction(25,487);rho=1+theta;beta=theta;A=9
    missing_shift=missing_chirp=False
    for i,j in product(range(2),repeat=2):
        h=j-i;bi=beta+theta*i;bj=beta+theta*j
        physical=-A*((rho*h+bi)**2-bj**2)
        chirp=A*theta*(i*i-j*j);shift=2*A*beta*(i-j);core=-A*rho*h*h
        need(physical-chirp-shift==core,'exact source exponent normalization')
        missing_shift |= physical-chirp!=core
        missing_chirp |= physical-shift!=core
    need(missing_shift and missing_chirp,'both normalization factors necessary')
    controls.append('exact rational exponents show both shift and chirp must be removed')
    need(Fraction(3*100*8,7)>16,'coarse source-family underflow bound')
    identity=[[int(i==j) for j in range(4)] for i in range(4)]
    need(dense_rank(stein(identity))==1,'rounded identity rank')
    controls.append('alpha10,s5/7,t8/8 permits all offdiagonals below2^-16; downward16-bit rounding gives rank1')
    return controls


def source_checks(package):
    pins={
        'inputs/A9-PROOF.md':'3e87c32b9cb3695dc42c2ef10da9c05e74d1742a37e49ce0fe5890ea093463dc',
        'inputs/GAUGEFREE-INTERIORS.md':'a7fc34302a70f8453f877a6433ffe2776457bf37b5d8bb262afcb6b198a935fc',
        'inputs/FINE-PRIME-PADDING.md':'47d1b1b4df28aadda3cd6bdeb1fbc47290595e9208cd09c1a1f338520d33fdce'}
    for path,digest in pins.items():
        need(sha256((package/path).read_bytes()).hexdigest()==digest,'exact predecessor/source bytes')
    return pins


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--write',type=Path);args=parser.parse_args()
    pins=source_checks(args.package)
    orders=[(0,1,3,2,6,7,5,4),(0,1,2,3,7,5,6,4)]
    rng=random.Random(10703)
    while len(orders)<10:
        tail=list(range(1,8));rng.shuffle(tail);candidate=(0,)+tuple(tail)
        if candidate not in orders:orders.append(candidate)
    cases=[certified_minor((0,1),(3,),(8,))]
    for tail in permutations(range(1,4)):
        for primes,targets in (((3,5),(8,16)),((5,7),(8,8))):
            cases.append(certified_minor((0,)+tail,primes,targets))
    for order in orders:
        for primes,targets in (((3,5,7),(8,16,8)),((5,7,11),(8,16,8)),
                               ((7,11,13),(8,16,8)),((971,977,487),(1024,1024,512))):
            cases.append(certified_minor(order,primes,targets))
    trims=0
    for order in ((0,1,3,2),(0,1,2,3),(0,1,3,2,6,7,5,4),
                  (11,9,3,15,1,7,2,10,13,6,4,8,12,14,5,0)):
        for mask in range(1,len(order)):
            C=matching_matrix(order,mask);paths=paths_for_minor(C)
            for size in range(0,min(sum(map(len,paths)),8)+1,2):
                keep=trim(paths,size)
                need(abs(dense_det([[C[i][j] for j in keep] for i in keep]))==1,'every bounded even trim')
                trims+=1
    boxes=[]
    for m,t in (((3,5),(8,16)),((3,5,7),(8,16,8)),((5,7,11),(8,16,8)),((9,25),(8,32))):
        boxes.append(dict(moduli=m,targets=t,complete_box_size=complete_box(m,t)))
    p=3
    for t,s in ((1024,971),(1024,977),(512,487)):
        need(prime(s) and Fraction((2*p*p-1)*t,2*p*p)<s<=Fraction((4*p*p-1)*t,4*p*p),
             'exact bounded fine-prime interval witness')
    result=dict(status='PASS_INDEPENDENT_PRIME_SPECIALIZATION',source_sha256=pins,
                method='Independent signed-matrix path extraction, Fraction determinants, full multivariate/univariate subset-DP and CRT boxes.',
                minor_cases=len(cases),rank_floor_counts=dict(Counter(str(c['rank_floor']) for c in cases)),
                polynomial_terms=sum(c['monomials'] for c in cases),trimmed_minor_checks=trims,
                exponent_boxes=boxes,exponent_box_total=sum(b['complete_box_size'] for b in boxes),
                source_interval_fixture=dict(p=3,primes=[971,977,487],targets=[1024,1024,512]),
                controls=control_checks(),seed=10703,
                limitations='Finite algebra corroboration only; no floating transcendence/rank test, no physical/rounded/global source rank claim.')
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:args.write.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
