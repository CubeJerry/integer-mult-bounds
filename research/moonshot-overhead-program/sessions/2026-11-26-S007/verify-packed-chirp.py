"""Replay the literal c-lane CRT, using one carryless convolution per packet."""
from collections import Counter
from pathlib import Path
from random import Random
import json
import runpy

shared = runpy.run_path(str(Path(__file__).with_name("verify-fibre-join.py")))
mul = shared["mul"]
power = shared["power"]
field_poly = shared["field_poly"]
divmod_binary = shared["divmod_binary"]
xor_product = shared["xor_product"]
minpoly = shared["minpoly"]
fs_order = shared["fs_order"]


def primitive(field):
    m = (1 << (field.bit_length()-1)) - 1
    if m == 1:
        return 1
    factors = [p for p in range(2,m+1) if m % p == 0 and
               all(p % t for t in range(2,int(p**0.5)+1))]
    return next(x for x in range(2,m+1)
                if all(power(x,m//p,field) != 1 for p in factors))


def binary_product_blocks(x, kernel, c, field):
    m = len(x)
    stride = 2*c-1
    def pack(words):
        return sum(word << (stride*i) for i,word in enumerate(words))
    product = xor_product(pack(x),pack(kernel))
    rawmask = (1 << stride)-1
    result = [0]*m
    for i in range(2*m-1):
        raw = (product >> (i*stride)) & rawmask
        result[i % m] ^= divmod_binary(raw,field)[1]
    return result


def dft_chirp(values, g, field, c, inverse=False):
    m = len(values)
    if m == 1:
        return list(values)
    half = (m+1)//2
    sign = -1 if inverse else 1
    chirp = [power(g,sign*half*i*i % m,field) for i in range(m)]
    kernel = [power(g,-sign*half*i*i % m,field) for i in range(m)]
    scaled = [mul(u,v,field) for u,v in zip(values,chirp)]
    result = binary_product_blocks(scaled,kernel,c,field)
    return [mul(u,v,field) for u,v in zip(result,chirp)]


def evaluate(coeffs, t, field):
    out = 0
    for val in reversed(coeffs):
        out = mul(out,t,field) ^ val
    return out


def interpolate(roots, values, field):
    # Independent Gaussian inverse of the orbit Vandermonde over K.
    n = len(roots)
    mat = [[power(root,j,field) for j in range(n)]+[val]
           for root,val in zip(roots,values)]
    for j in range(n):
        pivot = next(i for i in range(j,n) if mat[i][j])
        mat[j],mat[pivot] = mat[pivot],mat[j]
        inverse = power(mat[j][j],(1 << (field.bit_length()-1))-2,field)
        mat[j] = [mul(u,inverse,field) for u in mat[j]]
        for i in range(n):
            if i != j and mat[i][j]:
                factor = mat[i][j]
                mat[i] = [x ^ mul(factor,y,field) for x,y in zip(mat[i],mat[j])]
    return [row[-1] for row in mat]


def directory(c, field, g):
    m = 2**c-1
    groups = {factor:[] for factor in fs_order(c)}
    for i in range(m+1):
        t = 0 if i == m else power(g,i,field)
        groups[minpoly(t,field)].append((i,t))
    for factor,items in groups.items():
        assert len(items) == factor.bit_length()-1
    return groups


def packet_forward(inputs, c, field, g, groups):
    assert 1 <= len(inputs) <= c
    m = 2**c-1
    coeffs = [sum(((f >> j) & 1) << u for u,f in enumerate(inputs))
              for j in range(m+1)]
    packed = [coeffs[0]^coeffs[m],*coeffs[1:m]]
    evals = dft_chirp(packed,g,field,c)+[coeffs[0]]
    roots = [power(g,i,field) for i in range(m)]+[0]
    assert evals == [evaluate(coeffs,t,field) for t in roots]
    result = {}
    for factor,items in groups.items():
        residual = interpolate([t for _,t in items],[evals[i] for i,_ in items],field)
        assert all(z < 1 << len(inputs) for z in residual)
        result[factor] = [sum(((z >> u)&1) << j for j,z in enumerate(residual))
                          for u in range(len(inputs))]
    return result


def packet_inverse(records, c, field, g, groups):
    m = 2**c-1
    used = len(next(iter(records.values())))
    assert list(records) == list(groups)
    evals = [0]*(m+1)
    for factor,items in groups.items():
        coeffs = [sum(((f >> j)&1) << u for u,f in enumerate(records[factor]))
                  for j in range(factor.bit_length()-1)]
        for i,t in items:
            evals[i] = evaluate(coeffs,t,field)
    folded = dft_chirp(evals[:m],g,field,c,inverse=True)
    coeffs = [evals[m],*folded[1:],folded[0]^evals[m]]
    assert all(z < 1 << used for z in coeffs)
    return [sum(((z >> u)&1) << j for j,z in enumerate(coeffs))
            for u in range(used)]


def main():
    rng = Random(0x3C71)
    counts = Counter()
    for c in range(1,8):
        field = field_poly(c)
        g = primitive(field)
        groups = directory(c,field,g)
        n = 2**c
        for width in sorted({1,c,max(1,c-1)}):
            sets = [[0]*width,[(1 << n)-1]*width,
                    [1 << (n-1) for _ in range(width)],
                    [rng.getrandbits(n) for _ in range(width)]]
            if c <= 3:
                for bit in range(width*n):
                    sets.append([1 << (bit % n) if u == bit//n else 0 for u in range(width)])
                    counts["independent_input_basis_bits"] += 1
            for polys in sets:
                records = packet_forward(polys,c,field,g,groups)
                direct = {h:[divmod_binary(f,h)[1] for f in polys] for h in groups}
                assert direct == records
                assert packet_inverse(records,c,field,g,groups) == polys
                counts["literal_residue_bits"] += width*n
                counts["forward_first_packets"] += 1
            records = {h:[rng.getrandbits(h.bit_length()-1) for _ in range(width)] for h in groups}
            recovered = packet_inverse(records,c,field,g,groups)
            assert all(divmod_binary(f,h)[1] == r
                       for h,rs in records.items() for f,r in zip(recovered,rs))
            assert packet_forward(recovered,c,field,g,groups) == records
            counts["arbitrary_residue_bits_inverse_first"] += width*n
            counts["inverse_first_packets"] += 1
            if width < c:
                counts["ragged_widths"] += 1
        if c > 1:
            # Replacing the carryless operation by the integer product fails.
            assert xor_product(3,3) != 3*3
        counts["degrees_checked"] += 1
    print(json.dumps(dict(sorted(counts.items())),indent=2))


if __name__ == "__main__":
    main()
