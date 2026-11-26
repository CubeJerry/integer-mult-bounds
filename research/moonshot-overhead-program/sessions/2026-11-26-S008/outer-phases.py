"""Exact dyadic phase compiler with an independent arbitrary-precision DFT replay."""
from functools import lru_cache
from math import isqrt
import json
import mpmath as mp


def trunc(num, den):
    return num // den if num >= 0 else -((-num) // den)


@lru_cache(None)
def pi_fixed(g):
    q = 1 << g
    def arctan(d):
        result, power = 0, d
        for i in range(g + 3):
            value = q // ((2 * i + 1) * power)
            if not value:
                break
            result += (-1 if i % 2 else 1) * value
            power *= d * d
        return result
    return 16 * arctan(5) - 4 * arctan(239)


@lru_cache(None)
def root(p, n, d):
    g = p + 2 * (p + 8).bit_length() + 40
    q = 1 << g
    angle = (2 * pi_fixed(g) * (n % d)) // d
    term = (q, 0)
    total = [q, 0]
    for j in range(1, 16 * (p + 1) + 65):
        term = (trunc(-term[1] * angle, q * j), trunc(term[0] * angle, q * j))
        if term == (0, 0):
            break
        total[0] += term[0]
        total[1] += term[1]
    return tuple(trunc(v, 1 << (g - p)) for v in total)


class Grid:
    def __init__(self, p):
        self.q = 1 << p
        self.p = p

    def mul(self, x, y):
        a, b = x
        c, d = y
        return (trunc(a*c-b*d, self.q), trunc(a*d+b*c, self.q))

    def div(self, x, y):
        a, b = x
        c, d = y
        h = c*c + d*d
        assert 16*h >= self.q**2 - 100*self.q
        return trunc((a*c+b*d)*self.q, h), trunc((b*c-a*d)*self.q, h)

    def mag(self, x):
        return isqrt(x[0]*x[0] + x[1]*x[1])

    def invroot(self, a):
        return (isqrt(self.q*self.q // a), 0)

    def z(self, a, r, j):
        total = [0, 0]
        for h in range(1-a, a):
            v = root(self.p, -h*h*r + 2*a*j*h, 2*a*r)
            total[0] += v[0]
            total[1] += v[1]
        lam = self.mul(total, self.invroot(a))
        return self.mul(lam, (root(self.p, 1, 516)[1], 0))

    def d2(self, a, j):
        total = [0, 0]
        for h in range(a):
            v = root(self.p, -h*h - (a % 2)*h + 2*j*h, 2*a)
            total[0] += v[0]
            total[1] += v[1]
        return self.mul(total, self.invroot(a))

    def pair(self, z):
        a, b = z
        v = isqrt(self.q*self.q-a*a-b*b)
        h = self.invroot(2)
        q00 = self.mul(h, (a+v, b))
        q01 = self.mul(h, (v-a, b))
        q10 = self.mul(h, (a-v, b))
        c, s = self.mag(q00), self.mag(q01)
        gamma = self.div(q00, (c, 0))
        den = self.mul((0, s), gamma)
        return (gamma, self.div(q10, (0, s))), ((c,s), (c,-s)), ((self.q,0), self.div(q01, den))


def dft(n):
    return mp.matrix([[mp.expjpi(mp.mpf(2)*j*h/n)/mp.sqrt(n)
                       for h in range(n)] for j in range(n)])


def adj(m):
    return m.transpose_conj()


def run(a, p=96):
    t = Grid(p)
    r = 1 << (2*a-2).bit_length()
    n = 2*r
    def convert(v):
        return mp.mpc(v[0], v[1]) / t.q
    def extend(active):
        return mp.diag([convert(v) for v in active] + [1]*(n-len(active)))
    h2 = dft(2)
    pair = mp.zeros(n)
    pair_error = mp.mpf(0)
    for j in range(r):
        z = t.z(a, r, j)
        out, mid, inp = t.pair(z)
        def diagonal(vs):
            return mp.diag([convert(v) for v in vs])
        block = h2*diagonal(out)*h2*diagonal(mid)*h2*diagonal(inp)
        ideal_z = sum(mp.expjpi(mp.mpf(-h*h*r+2*a*j*h)/(a*r))
                      for h in range(1-a,a))/mp.sqrt(a)*mp.sin(mp.pi/258)
        v = mp.sqrt(1-abs(ideal_z)**2)
        ideal = mp.matrix([[ideal_z, v],[v, -mp.conj(ideal_z)]])
        pair_error = max(pair_error, mp.norm(block-ideal))
        for b in range(2):
            for c in range(2):
                pair[j+b*r, j+c*r] = block[b,c]
    ur = mp.eye(n)
    ur[:r,:r] = dft(r)
    chirp = extend([root(p,j*j,2*a) for j in range(a)])
    v = chirp*adj(ur)*pair*ur*chirp
    proj = mp.diag([1]*a+[0]*(n-a))
    reflection = mp.eye(n)-2*proj
    step = (-v*reflection*adj(v))*reflection
    b = step**64*v
    d1 = extend([root(p,j*j+(a%2)*j,2*a) for j in range(a)])
    d2 = extend([t.d2(a,j) for j in range(a)])
    d3 = extend([root(p,j*j-(a%2)*j,2*a) for j in range(a)])
    actual = d1*adj(b)*d2*b*d3
    target = mp.eye(n)
    target[:a,:a] = dft(a)
    error = mp.norm(actual-target)
    assert error < mp.mpf(2)**(-p+17)
    assert pair_error < mp.mpf(2)**(-p+8)
    return dict(a=a, r=r, occupied_complement=n-a, phase_bits=p,
                full_matrix_error=float(error), pair_error=float(pair_error))


if __name__ == "__main__":
    mp.mp.prec=180
    print(json.dumps([run(a) for a in (2,3,4,5,7)], indent=2))

