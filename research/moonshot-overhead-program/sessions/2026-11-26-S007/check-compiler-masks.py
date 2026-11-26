"""Independent GF(4) test of masked pairs compiled into two full tensor Pascals."""
from itertools import product
from math import prod
from random import Random
import json


def mul(x, y):
    """GF(2)[w]/(w²+w+1), in the ordered power basis."""
    z = (x if y & 1 else 0) ^ (x << 1 if y & 2 else 0)
    return z ^ 7 if z & 4 else z


def local(values, dims, rules):
    """Physical native reference. A rule is (target, source, multiplier)."""
    out = values.copy()
    for g, pairs in enumerate(rules):
        stride = prod(dims[g+1:])
        for start in range(0, len(out), dims[g]*stride):
            for dst, src, coeff in pairs:
                for j in range(stride):
                    out[start+dst*stride+j] ^= mul(coeff, out[start+src*stride+j])
    return out


def phases(dims, tables):
    out = []
    for point in product(*(range(d) for d in dims)):
        s = 1
        for d, t in zip(point, tables):
            s = mul(s, t[d])
        out.append(s)
    return out


def prepare(dims, rules):
    labels = []
    left, mid, right = [], [], []
    for d, pairs in zip(dims, rules):
        used, slots, coefficients = set(), [], []
        for dst, src, coeff in pairs:
            assert dst != src and not {dst, src} & used and coeff
            used.update((dst, src))
            slots.extend((dst, src))
            coefficients.append(coeff)
        slots.extend(i for i in range(d) if i not in used)
        labels.append(slots)
        coefficients.extend([0]*(d//2-len(coefficients)))
        a, m, b = [], [], []
        for z in coefficients:
            s, t = (mul(2,z),mul(3,z)) if z else (1,1)
            assert s ^ t == z
            a.extend((s, 1))
            m.extend((mul(mul(s,s),t), 1))
            b.extend((mul(t,t), 1))
        left.append(a)
        mid.append(m)
        right.append(b)
    strides = [prod(dims[g+1:]) for g in range(len(dims))]
    slots = [sum(i*j for i,j in zip(p,strides)) for p in product(*labels)]
    full = [[(j,j+1,1) for j in range(0,d,2)] for d in dims]
    return slots, full, [phases(dims,t) for t in (right,mid,left)]


def compiled(values, dims, program, drop_second=False):
    order, pairs, tables = program
    v = [values[i] for i in order]
    for round_no, weights in enumerate(tables):
        v = [mul(x,a) for x,a in zip(v,weights)]
        if round_no == 0 or (round_no == 1 and not drop_second):
            v = local(v, dims, pairs)
    result = [0]*len(v)
    for i,x in zip(order,v):
        result[i] = x
    return result


def masks():
    counts = dict(masks=0, basis_columns=0, field_entries=0, detected_phase_omissions=0)
    for g in range(1,7):
        n = 2**g
        dims = (2,)*g
        for mask in range(n):
            rules = [[(i%2,1-i%2,1+i%3)] if mask>>i & 1 else [] for i in range(g)]
            program = prepare(dims, rules)
            counts['masks'] += 1
            for j in range(n):
                basis = [0]*n
                basis[j] = 1
                assert compiled(basis,dims,program) == local(basis,dims,rules)
                counts['basis_columns'] += 1
                counts['field_entries'] += n
            if mask == 0:
                assert compiled(basis,dims,program,True) != basis
                counts['detected_phase_omissions'] += 1
    return counts


def bumped():
    rng = Random(20261126)
    counts = dict(basis_columns=0, mixed_payloads=0, field_entries=0,
                  dirty_hole_changes=0, hole_to_native_leaks=0)
    for native in ((3,5), (5,7), (3,5,7)):
        g = len(native)
        dims = [1<<(a*g-1).bit_length() for a in native]
        copies = [d//a for d,a in zip(dims,native)]
        n = prod(dims)
        rules = []
        for a,m in zip(native,copies):
            order = list(range(a))
            rng.shuffle(order)
            rules.append([(s*a+order[i],s*a+order[i+1],1+rng.randrange(3))
                          for s in range(m) for i in range(0,a-1,2)])
        program = prepare(dims,rules)
        holes = [any(i>=a*m for i,a,m in zip(p,native,copies))
                 for p in product(*(range(d) for d in dims))]
        if g == 2:
            for j in range(n):
                v = [0]*n
                v[j] = 1
                assert compiled(v,dims,program) == local(v,dims,rules)
                counts['basis_columns'] += 1
                counts['field_entries'] += n
        for _ in range(4):
            v = [rng.randrange(4) for i in range(n)]
            dirt = [x if h else 0 for h,x in zip(holes,v)]
            out = compiled(dirt,dims,program)
            assert out == local(dirt,dims,rules)
            changes = sum(x != y for x,y,h in zip(dirt,out,holes) if h)
            leaks = sum(bool(x) for x,h in zip(out,holes) if not h)
            assert changes and not leaks
            counts['dirty_hole_changes'] += changes
            counts['hole_to_native_leaks'] += leaks
            for w in (v,[0 if h else x for h,x in zip(holes,v)]):
                assert compiled(w,dims,program) == local(w,dims,rules)
                counts['mixed_payloads'] += 1
                counts['field_entries'] += n
    return counts


if __name__ == '__main__':
    print(json.dumps(dict(all_masks=masks(), native_fields=bumped()),indent=2,sort_keys=True))
