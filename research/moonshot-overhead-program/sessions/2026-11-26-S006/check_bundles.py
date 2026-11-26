"""Exact finite cross-check of stable additive bundles; dense small oracles only."""

from math import gcd
from random import Random


def span(basis):
    elements = [0]
    for member in basis:
        elements += [x ^ member for x in elements]
    return elements


def kernel(images):
    pivots = {}
    answer = []
    for index, image in enumerate(images):
        preimage = 1 << index
        while image:
            slot = image.bit_length()
            if slot not in pivots:
                pivots[slot] = (image, preimage)
                break
            row, combination = pivots[slot]
            image ^= row
            preimage ^= combination
        if image == 0:
            answer.append(preimage)
    return answer


def polynomial_field(b):
    """Small ordinary polynomial-basis oracle, including reverse division."""
    def convolution(a, v):
        out = 0
        while v:
            if v & 1:
                out ^= a
            a <<= 1
            v >>= 1
        return out

    def remainder(a, v):
        while a.bit_length() >= v.bit_length():
            a ^= v << (a.bit_length() - v.bit_length())
        return a

    def polynomial_gcd(a, v):
        while v:
            a, v = v, remainder(a, v)
        return a

    def irreducible(f):
        x = 2
        for i in range(1, b + 1):
            x = remainder(convolution(x, x), f)
            if 2*i <= b and polynomial_gcd(x ^ 2, f) != 1:
                return False
        return x == 2

    f = next(p for p in range((1 << b) + 1, 1 << (b + 1), 2) if irreducible(p))
    mask = (1 << b) - 1

    def reverse(x, length):
        out = 0
        for _ in range(length):
            out, x = 2*out + (x & 1), x >> 1
        return out

    rev = reverse(f, b + 1)
    reciprocal = 1
    for j in range(1, b):
        reciprocal |= ((convolution(reciprocal, rev) >> j) & 1) << j
    assert convolution(reciprocal, rev) & mask == 1

    def multiply(x, y):
        return remainder(convolution(x, y), f)

    def square(x):
        return multiply(x, x)

    def frobenius(x, count):
        for _ in range(count):
            x = square(x)
        return x

    def inverse(x):
        assert x
        y = 1
        for bit in bin((1 << b) - 2)[2:]:
            y = square(y)
            if bit == "1":
                y = multiply(y, x)
        assert multiply(x, y) == 1
        return y

    rng = Random(b + 1701)
    for _ in range(250):
        x, y = rng.getrandbits(b), rng.getrandbits(b)
        prod = convolution(x, y)
        k = reverse(convolution(reverse(prod, 2*b), reciprocal) & mask, b)
        assert prod ^ convolution(k, f) == multiply(x, y)
    return 1, multiply, square, frobenius, inverse


def column_orbits(width):
    """Compressed real cyclotomic basis r1,...,r_(b-1),1."""
    b = width
    polynomial = (1 << (2 * b)) | (1 << b) | 1
    one = 1 << (b - 1)
    columns = [(1 << j) ^ (1 << (2 * b - j)) ^ (1 << (b - j))
               for j in range(1, b)] + [1]

    def embed(x):
        out = 0
        while x:
            term = x & -x
            out ^= columns[term.bit_length() - 1]
            x ^= term
        return out

    def project(x):
        out = one if x & 1 else 0
        for j in range(1, b):
            out |= ((x >> (2 * b - j)) & 1) << (j - 1)
        assert embed(out) == x
        return out

    def multiply(x, y):
        p = 0
        left, right = embed(x), embed(y)
        while right:
            if right & 1:
                p ^= left
            left <<= 1
            right >>= 1
        # Independent long reduction in the ambient binary field.
        while p.bit_length() > 2 * b:
            p ^= polynomial << (p.bit_length() - 1 - 2 * b)
        return project(p)

    square_columns = [multiply(1 << i, 1 << i) for i in range(b)]

    def square(x):
        out = 0
        while x:
            bit = x & -x
            out ^= square_columns[bit.bit_length() - 1]
            x ^= bit
        return out

    def frobenius(x, count):
        for _ in range(count):
            x = square(x)
        return x

    def inv(x):
        assert x
        # Invert using x^(2^b-2), with unit and sign conventions explicit.
        y = one
        for bit in bin((1 << b) - 2)[2:]:
            y = square(y)
            if bit == "1":
                y = multiply(y, x)
        assert multiply(x, y) == one
        return y

    return one, multiply, square, frobenius, inv


def check_neighboring_stages(b, one, mul, square, inv, basis, reps, values):
    """Evaluate every adjacent basis level, then reconstruct in reverse."""
    dimension = len(basis)
    size = 1 << dimension
    directions = span(basis)

    # The small oracle constructs the subspace polynomials independently as
    # products over their roots, not by the executor's additivity recurrence.
    def subspace_value(x, level):
        acc = one
        for root in directions[:1 << level]:
            acc = mul(acc, x ^ root)
        return acc

    needed = {alpha ^ point for alpha in reps for point in directions} | set(basis)
    tables = [{x: subspace_value(x, j) for x in needed} for j in range(dimension)]
    deltas = [tables[j][basis[j]] for j in range(dimension)]
    reciprocals = [inv(delta) for delta in deltas]
    for j in range(dimension - 1):
        assert all(tables[j+1][x] == square(tables[j][x]) ^ mul(deltas[j], tables[j][x])
                   for x in needed)

    def verify_stream(stream, alpha, level):
        width = 1 << level
        for offset in range(0, size, width):
            coeffs = stream[offset:offset+width]
            for address in range(offset, offset+width):
                x = alpha ^ directions[address]
                # Direct evaluation in the global binary-product basis.
                basis_values = [one]
                for j in range(level):
                    term = tables[j][x]
                    basis_values += [mul(term, v) for v in basis_values]
                y = 0
                for coeff, term in zip(coeffs, basis_values):
                    y ^= mul(coeff, term)
                assert y == values[x]

    def layer(stream, alpha, j, inverse):
        half = 1 << j
        out = []
        for offset in range(0, size, 2*half):
            a = alpha ^ directions[offset]
            t = tables[j][a]
            first = stream[offset:offset+half]
            second = stream[offset+half:offset+2*half]
            low, high = [], []
            for x, y in zip(first, second):
                if inverse:
                    v = mul(x ^ y, reciprocals[j])
                    low.append(x ^ mul(t, v))
                    high.append(v)
                else:
                    u = x ^ mul(t, y)
                    low.append(u)
                    high.append(u ^ mul(deltas[j], y))
            out += low + high
        return out

    for alpha in reps:
        leaves = [values[alpha ^ p] for p in directions]
        levels = [leaves]
        for j in range(dimension):
            parent = layer(levels[-1], alpha, j, True)
            verify_stream(parent, alpha, j+1)
            levels.append(parent)
        run = levels[-1]
        for j in reversed(range(dimension)):
            run = layer(run, alpha, j, False)
            assert run == levels[j]
        assert run == leaves
    print(f"  {dimension} consecutive layers in both directions on {len(reps)} tested cosets; "
          "every intermediate polynomial checked on all of its roots")


def check_degree(b):
    c = b // 3
    one, mul, sq, frob, inv = column_orbits(b) if b in (3, 9, 27) else polynomial_field(b)
    rel = lambda x: x ^ frob(x, c) ^ frob(x, 2 * c)
    q = 1 << b
    rng = Random(20261126 + b)
    for _ in range(1000):
        theta = rng.randrange(q)
        normal = [frob(theta, i) for i in range(b)]
        if not kernel(normal):
            break
    else:
        raise AssertionError("finite normal-element search failed")
    ker = [normal[i] ^ normal[i+c] for i in range(2*c)]
    eta = ker[0]
    assert not kernel([one] + ker) and all(rel(x) == 0 for x in ker)
    assert len(kernel([rel(1 << i) for i in range(b)])) == 2*c
    assert frob(eta, b) == eta and all(frob(eta, i) != eta for i in range(1, b))
    assert b - len(kernel([frob(eta, i) for i in range(b)])) == 2 * c
    h_basis = [normal[i] ^ normal[i+c] ^ normal[i+2*c] for i in range(c)]
    h_words = span(h_basis)
    h_mask = (1 << c) - 1
    assert h_words[-1] == one and all(frob(x, c) == x for x in h_words)
    quotient = range(0, 1 << c, 2)

    def qshift(x):
        shifted = ((x << 1) & h_mask) | (x >> (c-1))
        return shifted ^ (h_mask if shifted & 1 else 0)

    orbits = {}
    for start in quotient:
        o, current = [], start
        for _ in range(c):
            following = qshift(current)
            assert h_words[following] ^ sq(h_words[current]) in (0, one)
            o.append(current)
            current = following
        assert current == start
        orbits[start] = o
    fixes = [sum(o[i] == x for x, o in orbits.items()) for i in range(c)]
    for i, count in enumerate(fixes):
        g = gcd(i, c)
        assert count == (1 << (g-1)) * (1 + int((c//g) % 2 == 0))
    reps = [h_words[x] for x in quotient if x == min(orbits[x])]
    expected = sum(fixes) // c
    assert len(reps) == expected and expected * c == sum(fixes)
    slots = (1 << (2 * c + 1)) * expected
    print(f"b={b} dim(V)={2*c + 1} quotient={len(quotient)} orbits={expected} "
          f"canonical_bits={b * slots} ratio={b * slots / (1 << b):g}")
    if b > 9:
        # Check the actual lower five levels in representative subcosets,
        # also outside the first subcoset if higher directions are present.
        basis = [one] + ker
        depth = min(5, len(basis))
        seeds = reps[:2]
        if len(basis) > depth:
            seeds += [s ^ basis[depth] for s in seeds]
        coefficients = [rng.randrange(2) for _ in range(2 << depth)]
        points = {s ^ v for s in seeds for v in span(basis[:depth])}
        values = {}
        for z in points:
            y = 0
            for a in reversed(coefficients):
                y = mul(z, y) ^ (one if a else 0)
            values[z] = y
        check_neighboring_stages(b, one, mul, sq, inv, basis[:depth], seeds, values)
        return

    coeffs = [rng.randrange(2) for _ in range(q)]
    values = []
    for z in range(q):
        y = 0
        for a in reversed(coeffs):
            y = mul(z, y) ^ (one if a else 0)
        values.append(y)
    assert all(values[sq(z)] == sq(values[z]) for z in range(q))
    icoef = inv(eta ^ sq(eta))

    def lagrange(points):
        # Direct Lagrange monomial interpolation, independently of the butterfly.
        result = [0] * len(points)
        for j, x in enumerate(points):
            polynomial, den = [one], one
            for i, y in enumerate(points):
                if i == j:
                    continue
                den = mul(den, x ^ y)
                nxt = [0] * (len(polynomial) + 1)
                for t, val in enumerate(polynomial):
                    nxt[t] ^= mul(val, y)
                    nxt[t + 1] ^= val
                polynomial = nxt
            scalar = mul(inv(den), values[x])
            for t, val in enumerate(polynomial):
                result[t] ^= mul(scalar, val)
        return result

    reconstructed = {}
    checks = 0
    for alpha in reps:
        local = {}
        # one and eta are the first directions; the other kernel vectors
        # sweep the four-point cosets of the chosen V-bundle.
        for nu in span(ker[1:]):
            a = alpha ^ nu
            points = [a, a ^ one, a ^ eta, a ^ eta ^ one]
            l0, l1, l2, l3 = lagrange(points)
            p1 = (l2 ^ l3, l3)
            p0 = (l0, l1 ^ p1[0])
            t0, t1 = sq(a) ^ a, sq(a ^ eta) ^ (a ^ eta)
            rows = [tuple(x ^ mul(t, y) for x, y in zip(p0, p1))
                    for t in (t0, t1)]
            assert [list(row) for row in rows] == [lagrange(points[:2]), lagrange(points[2:])]
            p1back = tuple(mul(x ^ y, icoef) for x, y in zip(*rows))
            p0back = tuple(x ^ mul(t0, y) for x, y in zip(rows[0], p1back))
            assert (p0back, p1back) == (p0, p1)
            for j, point in enumerate(points):
                low, high = rows[j // 2]
                local[point] = low ^ mul(point, high)
            checks += 1
        # Copy conjugate points to the omitted bundles; the ring arithmetic
        # must agree when a bundle orbit is shorter than the field degree.
        for z0, y0 in local.items():
            z, y = z0, y0
            for _ in range(b):
                assert z not in reconstructed or reconstructed[z] == y
                reconstructed[z] = y
                z, y = sq(z), sq(y)
    assert reconstructed == dict(enumerate(values))
    print(f"  {checks} forward/inverse four-point records; recovered all {q} binary-polynomial evaluations")
    check_neighboring_stages(b, one, mul, sq, inv, [one] + ker, reps, values)


def check_root_rounding():
    sizes = set(range(256, 65537))
    for k in range(9, 513):
        sizes.update((1 << k) + offset for offset in (-2, -1, 0, 1, 2))
    saw_padding = set()
    for n in sizes:
        digit_width = (n + 1).bit_length()
        digits = (n + digit_width - 1) // digit_width
        original = (2*digits - 1).bit_length()
        extension = 3*((original + 2)//3)
        height_floor = 2*digit_width + digits.bit_length() + 2
        height = 1 << (height_floor - 1).bit_length()
        q = 1 << extension
        saw_padding.add(extension-original)
        assert extension % 3 == 0 and 2*digits <= q < 16*digits
        assert extension <= height <= 8*extension and 4*n <= q*height < 256*n
        assert (2*digits-2) < q and digits*((1 << digit_width)-1)**2 < 1 << height
    assert saw_padding == {0, 1, 2}
    print(f"{len(sizes)} exact root-rounding checks across all three padding amounts")


if __name__ == "__main__":
    for degree in (3, 6, 9, 12, 15, 18, 27):
        check_degree(degree)
    check_root_rounding()
