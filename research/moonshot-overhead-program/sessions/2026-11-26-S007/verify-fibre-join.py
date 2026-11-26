#!/usr/bin/env python3
"""Check literal finite fields, directories, two fibre joins and physical marker layouts."""

from collections import Counter
from functools import cache
from itertools import chain
from random import Random
import json


def xor_product(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        a <<= 1
        b >>= 1
    return value


def divmod_binary(a, b):
    q = 0
    while a and a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def gcd_binary(a, b):
    while b:
        a, b = b, divmod_binary(a, b)[1]
    return a


def mul(a, b, modulus):
    return divmod_binary(xor_product(a, b), modulus)[1]


def power(a, n, modulus):
    result = 1
    while n:
        if n & 1:
            result = mul(result, a, modulus)
        a = mul(a, a, modulus)
        n >>= 1
    return result


@cache
def field_poly(n):
    if n == 1:
        return 3
    for p in range((1 << n) + 1, 2 << n, 2):
        a = 2
        for _ in range(n // 2):
            a = mul(a, a, p)
            if gcd_binary(a ^ 2, p) != 1:
                break
        else:
            if power(2, 1 << n, p) == 2:
                return p
    raise AssertionError(n)


def orbit(a, modulus):
    elements = [a]
    x = mul(a, a, modulus)
    while x != a:
        elements.append(x)
        x = mul(x, x, modulus)
    return elements


def basis_pivots(vectors):
    pivots = {}
    for index, vector in enumerate(vectors):
        mask = 1 << index
        while vector:
            j = vector.bit_length() - 1
            if j not in pivots:
                pivots[j] = (vector, mask)
                break
            v, m = pivots[j]
            vector ^= v
            mask ^= m
    return pivots


def coordinates(x, pivots):
    mask = 0
    while x:
        v, m = pivots[x.bit_length() - 1]
        x ^= v
        mask ^= m
    return mask


@cache
def normal(n):
    h = field_poly(n)
    random = Random(9187 + n)
    candidates = (random.randrange(1, 1 << n) for _ in range(2048))
    for x in chain(candidates, range(1, 1 << n)):
        conj = orbit(x, h)
        if len(conj) == n and len(basis_pivots(conj)) == n:
            return tuple(conj)
    raise AssertionError(n)


def from_word(word, ordered_basis):
    value = 0
    for i, z in enumerate(reversed(ordered_basis)):
        if (word >> i) & 1:
            value ^= z
    return value


def minpoly(x, field):
    coeffs = [1]
    for root in orbit(x, field):
        nxt = [0] * (len(coeffs) + 1)
        for i, u in enumerate(coeffs):
            nxt[i] ^= mul(root, u, field)
            nxt[i + 1] ^= u
        coeffs = nxt
    assert set(coeffs) <= {0, 1}
    return sum(value << i for i, value in enumerate(coeffs))


def rotate(word, offset, size):
    offset %= size
    return ((word << offset) | (word >> (size - offset))) & ((1 << size) - 1)


def min_rotation(word, size):
    return min(rotate(word, i, size) for i in range(size))


def fixed_word_orbit(word, d):
    return {rotate(word, i, d) for i in range(d)}


def field_poly_eval(poly, t, field):
    v = 0
    for j in range(poly.bit_length() - 1, -1, -1):
        v = mul(v, t, field) ^ ((poly >> j) & 1)
    return v


def power_columns(root, degree, field):
    p = 1
    cols = []
    for _ in range(degree):
        cols.append(p)
        p = mul(p, root, field)
    return cols


def fs_order(c):
    out = []
    for d in range(1, c + 1):
        if c % d:
            continue
        for word in range(1 << d):
            rotations = fixed_word_orbit(word, d)
            if len(rotations) == d and word == min(rotations):
                root = from_word(word, normal(d))
                poly = minpoly(root, field_poly(d))
                assert poly.bit_length() - 1 == d
                out.append(poly)
    assert len(out) == len(set(out))
    assert sum(h.bit_length() - 1 for h in out) == 1 << c
    return out


def make_context(c):
    b, n = 3 * c, 1 << c
    field = field_poly(b)
    gamma = normal(b)
    sub = [gamma[i] ^ gamma[i + c] ^ gamma[i + 2 * c] for i in range(c)]
    assert len(basis_pivots(sub)) == c
    assert from_word(n - 1, sub) == 1
    fs = fs_order(c)
    pairs = []
    visited = set()
    for w in range(n // 2):
        if w in visited:
            continue
        words = set()
        for u in fixed_word_orbit(w, c):
            words.add(min(u, u ^ (n - 1)))
        assert w == min(words)
        visited.update(words)
        t = from_word(w, sub)
        s = mul(t, t, field) ^ t
        d = len(orbit(s, field))
        assert d == len(words)
        h0, h1 = minpoly(t, field), minpoly(t ^ 1, field)
        twisted = h0 == h1
        assert (power(t, 1 << d, field) == (t ^ 1)) == twisted
        assert h0.bit_length() - 1 == (2*d if twisted else d)
        assert h1.bit_length() == h0.bit_length()
        e = h0.bit_length() - 1
        pairs.append(dict(anchor=w, t=t, s=s, d=d, e=e, h0=h0, h1=h1,
                          p0=basis_pivots(power_columns(t, e, field)),
                          p1=basis_pivots(power_columns(t ^ 1, e, field)),
                          ps=basis_pivots(power_columns(s, d, field))))
    assert sum(p['d'] for p in pairs) == n // 2
    assert set(fs) == {p[k] for p in pairs for k in ('h0', 'h1')}
    assert sum(1 + (p['h0'] != p['h1']) for p in pairs) == len(fs)
    return field, fs, pairs


def sparse_div(bits, half, shifts):
    mask = (1 << half) - 1
    lo, hi = bits & mask, bits >> half
    q = hi
    for shift in shifts:
        q ^= hi >> (half-shift)
    rem = lo
    for shift in shifts:
        rem ^= (q << shift) & mask
    return rem, q


def radix(bits, base, shifts, levels):
    blocks = [bits]
    for i in reversed(range(levels)):
        h = base << i
        e = [j << i for j in shifts]
        blocks = [child for parent in blocks for child in sparse_div(parent, h, e)]
    return blocks


def join_radix(blocks, base, shifts):
    blocks = blocks.copy()
    i = 0
    while len(blocks) > 1:
        h = base << i
        low = [j << i for j in shifts]
        new = []
        for rem, q in zip(blocks[::2], blocks[1::2]):
            r = rem ^ (q << h)
            for j in low:
                r ^= q << j
            new.append(r)
        blocks = new
        i += 1
    return blocks[0]


def inverse_mod(x, modulus):
    a, b, s, t = x, modulus, 1, 0
    while b:
        q, rem = divmod_binary(a, b)
        a, b = b, rem
        s, t = t, s ^ xor_product(q, t)
    assert a == 1
    return divmod_binary(s, modulus)[1]


def crt_interpolants(fs, product):
    out = []
    for h in fs:
        u, r = divmod_binary(product, h)
        assert r == 0
        out.append(xor_product(u, inverse_mod(divmod_binary(u, h)[1], h)))
    return out


def combine(A, B, t, n, field):
    a = n*n
    R = [0] * (2*a)
    for k, (u, z) in enumerate(zip(A, B)):
        q = u ^ z
        R[k] ^= u ^ mul(t, q, field)
        for shift in (1, n, a):
            R[k + shift] ^= q
    return R


def uncombine(R, t, n, field):
    a = n*n
    C, D = R[:a], R[a:]
    Q = D.copy()
    for shift in (n, 1):
        for i in range(shift):
            Q[i] ^= D[a-shift+i]
    A = [u ^ mul(t, q, field) for u, q in zip(C, Q)]
    for shift in (1, n):
        for i in range(a-shift):
            A[i+shift] ^= Q[i]
    return A, [u ^ q for u, q in zip(A,Q)]


def coefficient_remainder(raw, n, s, field):
    a, q = n*n, n**3
    poly = [((raw >> j) & 1) for j in range(q)]
    exps = set()
    for e in (1, n, a, 2, 2*n):
        if e in exps:
            exps.remove(e)
        else:
            exps.add(e)
    for j in range(q-1, 2*a-1, -1):
        lead = poly[j]
        off = j-2*a
        if not lead:
            continue
        for e in exps:
            poly[off+e] ^= lead
        poly[off] ^= mul(lead, s, field)
    return poly[:2*a]


def forward(raw, c, field, fs, pairs, counts):
    n = 1 << c
    a = n*n
    digits = radix(raw, a, [1, n], c)
    assert join_radix(digits, a, [1,n]) == raw
    polys = [sum(((block >> k) & 1) << j for j, block in enumerate(digits))
             for k in range(a)]
    # Child rows use true long remainders in the deliberately independent FS1 order.
    rows = [[divmod_binary(p, h)[1] for h in fs] for p in polys]
    slot = {h:i for i,h in enumerate(fs)}
    out = []
    for pr in pairs:
        t = pr['t']
        u = [field_poly_eval(row[slot[pr['h0']]], t, field) for row in rows]
        w = [field_poly_eval(row[slot[pr['h1']]], t ^ 1, field) for row in rows]
        if pr['h0'] == pr['h1']:
            assert all(power(x, 1 << pr['d'], field) == y for x,y in zip(u,w))
            counts['twisted_evaluation_pairs'] += a
        R = combine(u, w, t, n, field)
        assert R == coefficient_remainder(raw, n, pr['s'], field)
        coords = [coordinates(val, pr['ps']) for val in R]
        assert all(field_poly_eval(w, pr['s'], field) == v for w,v in zip(coords,R))
        out.append(coords)
        counts['direct_group_remainder_coefficients'] += len(R)
    counts['division_first_binary_child_remainders'] += a * len(fs)
    return out


def backward(inp, c, field, fs, pairs, counts):
    n = 1 << c
    a = n*n
    rems = {h:None for h in fs}
    for pr, group in zip(pairs, inp):
        R = [field_poly_eval(x, pr['s'], field) for x in group]
        A, B = uncombine(R, pr['t'], n, field)
        assert combine(A, B, pr['t'], n, field) == R
        for h, points, pivots in ((pr['h0'],A,pr['p0']), (pr['h1'],B,pr['p1'])):
            coord = [coordinates(v, pivots) for v in points]
            if rems[h] is None:
                rems[h] = coord
            else:
                assert rems[h] == coord and pr['h0'] == pr['h1']
                counts['twisted_single_factor_coefficients_recovered_twice'] += a
    assert all(rems[h] is not None for h in fs)
    product = (1 << n) ^ 2
    basis = crt_interpolants(fs, product)
    digits = [0]*n
    for k in range(a):
        my_poly = 0
        for h, v in zip(fs, basis):
            my_poly ^= xor_product(rems[h][k], v)
        my_poly = divmod_binary(my_poly, product)[1]
        assert all(divmod_binary(my_poly,h)[1] == rems[h][k] for h in fs)
        for j in range(n):
            digits[j] |= ((my_poly >> j) & 1) << k
    counts['CRT_inverse_scalar_polynomials'] += a
    return join_radix(digits, a, [1, n])


def marker_routing(c, h, counts):
    n = 1 << c
    mask = n-1
    groups = {r:[] for r in range(c)}
    seen = set()
    ref = []
    for x in range(n):
        if x in seen:
            continue
        rotations = [rotate(x,r,c) for r in range(c)]
        seen.update(rotations)
        if len(set(rotations)) != c:
            continue
        assert min(rotations)==x
        dest = min_rotation(x ^ mask, c)
        if x<=dest or x >> (c-h) or dest >> (c-h):
            continue
        r = rotations.index(max(rotations))
        assert h <= r <= c-h
        groups[r].append(x)
        ref.append((dest, x))
    produced = []
    for r, vals in groups.items():
        if not vals:
            continue
        a, b = r-h, c-r-h
        # Fill genuine records with distinct nonzero payloads (their original word+1).
        padded = [0] * (1 << (a+b))
        for x in vals:
            u, v = (x >> (b+h)) & ((1 << a)-1), x & ((1 << b)-1)
            assert x == (u << (b+h)) + (((1 << h)-1) << b) + v
            padded[(u << b) | v] = x+1
        transposed = [0] * len(padded)
        for i, word in enumerate(padded):
            u,v = i >> b, i & ((1<<b)-1)
            index = (v << a) | u
            transposed[index ^ (len(padded)-1)] = word
        run = []
        for index, payload in enumerate(transposed):
            if not payload:
                continue
            vbar,ubar = index >> a,index & ((1<<a)-1)
            dest = (vbar << (a+h)) | (((1<<h)-1)<<a) | ubar
            assert min_rotation((payload-1)^mask,c) == dest
            run.append((dest,payload-1))
        assert run == sorted(run)
        produced.extend(run)
        counts['marked_routing_filled_slots'] += len(padded)
        counts['marked_routing_genuine_records'] += len(run)
        counts['marked_routing_unequal_nonempty_swaps'] += int(bool(a and b and a!=b))
        counts['marked_routing_empty_field_groups'] += int(a==0 or b==0)
    assert sorted(produced) == sorted(ref)
    counts['marked_routing_degrees_and_thresholds'] += 1


def obstruction_embedding(length, counts):
    size = 4*length + 13
    all_ones = (1 << size)-1
    def encode(x):
        return ''.join('10' if (x >> i) & 1 else '01' for i in reversed(range(length)))
    destinations = []
    previous = -1
    for u in range(1 << length):
        for v in range(1 << length):
            lam = int('0000'+'1'+encode(u)+'0'+'11111'+'0'+encode(v)+'1',2)
            assert previous < lam
            previous = lam
            conjugates = fixed_word_orbit(lam, size)
            assert len(conjugates) == size and min(conjugates) == lam
            nu = min_rotation(lam ^ all_ones, size)
            flip = str.maketrans('01','10')
            literal = '00000'+'1'+encode(v).translate(flip)+'0'+'1111'+'0'+encode(u).translate(flip)+'1'
            assert nu == int(literal, 2) < lam
            destinations.append((nu,u,v))
    ordered = [(u,v) for _,u,v in sorted(destinations)]
    assert ordered == [(u,v) for v in reversed(range(1 << length))
                       for u in reversed(range(1 << length))]
    counts['directory_transpose_subfamily_factors'] += len(ordered)
    counts['directory_transpose_subfamily_degrees'] += 1


def main():
    rng = Random(0x5D07)
    counts = Counter()
    summaries = []
    for c in range(1,9):
        n = 1 << c
        field, fs, pairs = make_context(c)
        summaries.append(dict(c=c,child_factors=len(fs),quotient_groups=len(pairs),
                              twisted_groups=sum(p['h0']==p['h1'] for p in pairs),
                              degrees=[p['d'] for p in pairs]))
        counts['actual_directory_joins'] += len(fs)
        if c > 5:
            continue
        for raw in (1 << (n**3-1),rng.getrandbits(n**3)):
            coords = forward(raw,c,field,fs,pairs,counts)
            assert backward(coords,c,field,fs,pairs,counts)==raw
            counts['complete_forward_first_roundtrips'] += 1
        groups = [[rng.getrandbits(p['d']) for _ in range(2*n*n)] for p in pairs]
        raw = backward(groups,c,field,fs,pairs,counts)
        assert forward(raw,c,field,fs,pairs,counts)==groups
        counts['independent_grouped_inverse_first_roundtrips'] += 1
    for c in range(4,17):
        for h in {1,2,max(2,c//5)}:
            marker_routing(c,h,counts)
    for length in range(1,8):
        obstruction_embedding(length,counts)
    # Refute omitting the one high correction on a fibre with a top coefficient.
    c,n,t = 2,4,0
    field = field_poly(3*c)
    q=n*n
    A=[0]*q
    B=[0]*(q-1)+[1]
    R=combine(A,B,t,n,field)
    assert R[q:] != B
    assert uncombine(R,t,n,field)==(A,B)
    print(json.dumps(dict(counts=dict(sorted(counts.items())),cases=summaries,
                          controls={'omitting_high_correction_fails':True},
                          seed='0x5D07'),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
