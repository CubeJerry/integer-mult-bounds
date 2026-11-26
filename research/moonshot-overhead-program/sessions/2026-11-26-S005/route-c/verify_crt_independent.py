#!/usr/bin/env python3
"""Independent finite CRT replay, with deliberately brute/dense test oracles.
This does not implement fast CRT or a tape compiler; no route-a code is read.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
RNG = random.Random(2026112605)
COUNTS = {}

def hit(k):
    COUNTS[k] = COUNTS.get(k, 0) + 1

def brem(x, g):
    while x and x.bit_length() >= g.bit_length():
        x ^= g << (x.bit_length() - g.bit_length())
    return x

def irreducibles(d):
    return [f for f in range(1 << d, 1 << (d + 1))
            if all(brem(f, g) for e in range(1, d // 2 + 1)
                   for g in range(1 << e, 1 << (e + 1)))]

def factors(b):
    gs = [[(g >> j) & 1 for j in range(d + 1)]
          for d in range(1, b + 1) if b % d == 0
          for g in irreducibles(d)]
    assert sum(len(g) - 1 for g in gs) == 1 << b
    return gs

def conv(a, b, mod):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % mod
    return c

def rem(a, g, mod):
    d = len(g) - 1
    a = [x % mod for x in a]
    for j in range(len(a) - 1, d - 1, -1):
        v = a[j]
        for i in range(d + 1):
            a[j-d+i] = (a[j-d+i] - v * g[i]) % mod
    return (a + [0] * d)[:d]

def image(a, gs, mod):
    return [v for g in gs for v in rem(a, g, mod)]

def matrix(gs, mod):
    n = sum(len(g) - 1 for g in gs)
    return [list(row) for row in zip(*[image([0]*j+[1], gs, mod) for j in range(n)])]

def inverse(a, mod):
    n = len(a)
    c = [a[i][:] + [int(i == j) for j in range(n)] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if c[i][j] % 2)
        c[p], c[j] = c[j], c[p]
        z = pow(c[j][j], -1, mod)
        c[j] = [x*z % mod for x in c[j]]
        for i in range(n):
            if i != j:
                z = c[i][j]
                c[i] = [(x-z*y) % mod for x,y in zip(c[i],c[j])]
    assert all(c[i][j] == int(i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in c]

def mv(a, v, mod):
    return [sum(x*y for x,y in zip(row,v)) % mod for row in a]

def newton(f, length, mod):
    assert f[0] == 1
    u = [1]
    while len(u) < length:
        size = min(length, 2*len(u))
        fu = (conv(f[:size],u,mod)+[0]*size)[:size]
        c = [(-x) % mod for x in fu]
        c[0] = (2-fu[0]) % mod
        u = (conv(u,c,mod)+[0]*size)[:size]
        assert (conv(f,u,mod)+[0]*size)[:size] == [1]+[0]*(size-1)
    return u

def newton_rem(a, g, mod):
    d, length = len(g)-1, len(a)-len(g)+1
    if length <= 0:
        return (a+[0]*d)[:d]
    u = newton(g[::-1],length,mod)
    qr = (conv(a[::-1],u,mod)+[0]*length)[:length]
    qg = conv(qr[::-1],g,mod)
    r = [(x-y) % mod for x,y in zip(a,qg)]
    assert all(x == 0 for x in r[d:])
    return r[:d]

def ring_checks():
    for b in range(1,6):
        gs, n = factors(b), 1 << b
        for h in (1,2,3,4,8):
            mod = 1 << h
            a = matrix(gs,mod)
            inv = inverse(a,mod)
            for j in range(n):
                e = [int(i == j) for i in range(n)]
                assert mv(inv,mv(a,e,mod),mod) == e
            hit('full_module_inverses')
            for _ in range(8):
                f = [RNG.randrange(mod) for _ in range(n)]
                assert mv(inv,image(f,gs,mod),mod) == f
                hit('arbitrary_coefficient_roundtrips')
            for g in gs:
                d = len(g)-1
                for _ in range(3):
                    x,y = [[RNG.randrange(mod) for _ in range(d)] for _ in range(2)]
                    w = 2*h+d.bit_length()+2
                    px = sum(v << (w*j) for j,v in enumerate(x))
                    py = sum(v << (w*j) for j,v in enumerate(y))
                    packed = px*py
                    c = [(packed >> (w*j)) & ((1 << w)-1) for j in range(2*d-1)]
                    assert c == conv(x,y,1 << (w+1))
                    c = [v % mod for v in c]
                    assert newton_rem(c,g,mod) == rem(c,g,mod)
                    hit('packed_newton_quotient_products')
        for t in (1,2,4):
            lo,hi = 1 << t, 1 << (2*t)
            il,ih = inverse(matrix(gs,lo),lo),inverse(matrix(gs,hi),hi)
            for _ in range(12):
                f0,f1 = [[RNG.randrange(lo) for _ in range(n)] for _ in range(2)]
                carry = [v//lo for v in image(f0,gs,hi)]
                a0,a1 = image(f0,gs,lo),image(f1,gs,lo)
                joined = [x+lo*y for x,y in zip(f0,f1)]
                predicted = [x+lo*((c+y)%lo) for x,c,y in zip(a0,carry,a1)]
                assert image(joined,gs,hi) == predicted
                y0,y1 = [v%lo for v in predicted],[v//lo for v in predicted]
                r0 = mv(il,y0,lo)
                rc = [v//lo for v in image(r0,gs,hi)]
                r1 = mv(il,[(x-c)%lo for x,c in zip(y1,rc)],lo)
                assert r0 == f0 and r1 == f1
                assert mv(ih,predicted,hi) == joined
                hit('forward_and_inverse_precision_lifts')
                if any(carry):
                    assert [x+lo*y for x,y in zip(a0,a1)] != predicted
                    hit('nonzero_carry_negative_controls')
    p = [1]
    for g in factors(2):
        p = conv(p,g,4)
    assert p == [0,1,2,2,1] and p != [0,3,0,0,1]
    hit('literal_lift_not_frobenius_binomial')

def integer_checks():
    for b in range(1,6):
        gs,q = factors(b),1 << b
        h = q//2
        for width in (1,2,3,5):
            guard = 2*width+h.bit_length()+2
            H = 1 << (guard-1).bit_length()
            mod = 1 << H
            inv = inverse(matrix(gs,mod),mod)
            for _ in range(4):
                x,y = [[RNG.randrange(1 << width) for _ in range(h)] for _ in range(2)]
                rx,ry = image(x,gs,mod),image(y,gs,mod)
                prod,at = [],0
                for g in gs:
                    d = len(g)-1
                    prod.extend(rem(conv(rx[at:at+d],ry[at:at+d],mod),g,mod))
                    at += d
                actual = mv(inv,prod,mod)
                exact = conv(x,y,mod)
                assert actual == exact+[0]*(q-len(exact))
                carry,digits = 0,[]
                for z in actual:
                    total = z+carry
                    digits.append(total % (1 << width))
                    carry = total >> width
                    assert carry <= h*((1 << width)-1)
                assert carry == 0
                xx = sum(v << (width*j) for j,v in enumerate(x))
                yy = sum(v << (width*j) for j,v in enumerate(y))
                zz = sum(v << (width*j) for j,v in enumerate(digits))
                assert zz == xx*yy
                hit('integer_products_and_carry_bounds')

def fmul(x,y,field):
    z = 0
    while y:
        if y & 1:
            z ^= x
        x <<= 1
        y >>= 1
    return brem(z,field)

def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length()-1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return len(pivots)

def fconv(a,b,field):
    out = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] ^= fmul(x,y,field)
    return out

def duval(d):
    w = [-1]
    while w:
        w[-1] += 1
        yield tuple(w)
        m = len(w)
        while len(w) < d:
            w.append(w[-m])
        while w and w[-1] == 1:
            w.pop()

def packed_field_product(a,b,field,d):
    m = max(len(a),len(b))
    stride = 2*d-1
    width = (m*d).bit_length()+1
    def pack(v):
        return sum(((x >> j)&1) << (width*(i*stride+j))
                   for i,x in enumerate(v) for j in range(d))
    product = pack(a)*pack(b)
    out = []
    for i in range(len(a)+len(b)-1):
        raw = 0
        for j in range(stride):
            count = (product >> (width*(i*stride+j))) & ((1 << width)-1)
            assert count <= m*d
            raw |= (count&1) << j
        out.append(brem(raw,field))
    return out

def factor_checks():
    for d in range(1,9):
        expected = irreducibles(d)
        field = expected[0]
        for theta in range(1,1 << d):
            basis,v = [],theta
            for _ in range(d):
                basis.append(v)
                v = fmul(v,v,field)
            if rank(basis) == d:
                break
        else:
            raise AssertionError('finite normal basis not found')
        words = list(duval(d))
        brute = []
        for length in range(1,d+1):
            for w in itertools.product((0,1),repeat=length):
                if all(w < w[k:]+w[:k] for k in range(1,length)):
                    brute.append(w)
        assert words == sorted(brute)
        hit('complete_duval_enumerations')
        got = []
        for w in words:
            if len(w) != d:
                continue
            gamma = 0
            for bit,col in zip(w,basis):
                if bit:
                    gamma ^= col
            roots,v = [],gamma
            for _ in range(d):
                roots.append(v)
                v = fmul(v,v,field)
            assert len(set(roots)) == d and v == gamma
            nodes = [[v,1] for v in roots]
            while len(nodes) > 1:
                level = []
                for i in range(0,len(nodes),2):
                    if i+1 == len(nodes):
                        level.append(nodes[i])
                    else:
                        z = packed_field_product(nodes[i],nodes[i+1],field,d)
                        assert z == fconv(nodes[i],nodes[i+1],field)
                        level.append(z)
                        hit('two_dimensional_packed_field_products')
                nodes = level
            poly = nodes[0]
            assert all(x in (0,1) for x in poly)
            got.append(sum(x << i for i,x in enumerate(poly)))
            hit('normal_basis_lyndon_irreducibles')
        assert sorted(got) == expected and len(got) == len(set(got))
        for m in range(1,d+1):
            for _ in range(4):
                a,b = [[RNG.randrange(1 << d) for _ in range(m)] for _ in range(2)]
                assert packed_field_product(a,b,field,d) == fconv(a,b,field)
                hit('two_dimensional_packed_field_products')

def carry_polarization_checks():
    for b in range(1,6):
        gs,n = factors(b),1 << b
        actual = matrix(gs,4)
        a0 = [[x % 2 for x in row] for row in actual]
        a1 = [[x // 2 for x in row] for row in actual]
        def carry(x):
            return [v//2 for v in image(x,gs,4)]
        for _ in range(30):
            x,y = [[RNG.randrange(2) for _ in range(n)] for _ in range(2)]
            xy = [a*b for a,b in zip(x,y)]
            plus = [a^b for a,b in zip(x,y)]
            kx,ky,kp = carry(x),carry(y),carry(plus)
            ex,ey,exy = image(x,gs,2),image(y,gs,2),image(xy,gs,2)
            lhs = [a^b^c for a,b,c in zip(kx,ky,kp)]
            assert lhs == [(a*b)^c for a,b,c in zip(ex,ey,exy)]
            quadratic = []
            for row in a0:
                selected = sum(a*b for a,b in zip(row,x))
                quadratic.append((selected*(selected-1)//2) % 2)
            assert kx == [a^b for a,b in zip(mv(a1,x,2),quadratic)]
            hit('first_carry_polarization_and_coordinate_formula')
            if any(xy):
                assert lhs != [a*b for a,b in zip(ex,ey)]
                hit('overlapping_support_correction_negative_controls')

if __name__ == '__main__':
    ring_checks()
    integer_checks()
    factor_checks()
    carry_polarization_checks()
    proofs = ['unramified-polynomial-crt-caller.md','binary-factor-stream-compiler.md']
    payload = {
        'status':'PASS',
        'scope':'Independent finite algebra replay only; dense inverse and brute irreducibles are test oracles, not fast suppliers or tape implementations.',
        'counts':COUNTS,
        'proof_sha256':{name:hashlib.sha256((HERE.parent/'route-a'/name).read_bytes()).hexdigest() for name in proofs},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'seed':2026112605,
    }
    (HERE/'crt-independent-verification.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))
