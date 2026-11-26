#!/usr/bin/env python3
"""Check the two-prefix physical root-directory route using distinct finite fields."""
from collections import Counter, defaultdict
from heapq import merge
from operator import itemgetter
from pathlib import Path
from random import Random
import json
import runpy

fns = runpy.run_path(str(Path(__file__).with_name("verify-factor-directory.py")))


def dot(mask, value):
    return (mask & value).bit_count() % 2


def apply(rows, value):
    return sum(dot(row, value) << i for i, row in enumerate(rows))


def row_product(left, right):
    output = []
    for row in left:
        value = 0
        for i, part in enumerate(right):
            if row >> i & 1:
                value ^= part
        output.append(value)
    return output


def inverse(rows):
    n = len(rows)
    aug = [v | (1 << (n + i)) for i, v in enumerate(rows)]
    for col in range(n):
        pivot = next(j for j in range(col, n) if aug[j] >> col & 1)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for j in range(n):
            if j != col and aug[j] >> col & 1:
                aug[j] ^= aug[col]
    assert all(v & ((1 << n) - 1) == 1 << j for j, v in enumerate(aug))
    return [v >> n for v in aug]


def affine_parts(function, n, m):
    offset = function(0)
    columns = [function(1 << i) ^ offset for i in range(n)]
    rows = [sum(((v >> j) & 1) << i for i, v in enumerate(columns)) for j in range(m)]
    return rows, offset


def ldu(rows):
    n = len(rows)
    if n <= 1:
        assert all(r == 1 << j for j, r in enumerate(rows))
        return lambda x: x
    low = n // 2
    mask = (1 << low) - 1
    selected = []
    for j, row in enumerate(rows):
        current = [rows[i] & mask for i in selected] + [row & mask]
        if fns["rank"](current) > len(selected):
            selected.append(j)
    assert len(selected) == low
    order = selected + [j for j in range(n) if j not in selected]
    sorted_rows = [rows[j] for j in order]
    A = [row & mask for row in sorted_rows[:low]]
    B = [row >> low for row in sorted_rows[:low]]
    C = [row & mask for row in sorted_rows[low:]]
    D = [row >> low for row in sorted_rows[low:]]
    ai = inverse(A)
    AB = row_product(ai, B)
    CA = row_product(C, ai)
    S = [d ^ cab for d, cab in zip(D, row_product(C, AB), strict=True)]
    child_a = ldu(A)
    child_s = ldu(S)

    def change(value):
        hi = value >> low
        lo = child_a((value & mask) ^ apply(AB, hi))
        hi = child_s(hi) ^ apply(CA, lo)
        tmp = lo | (hi << low)
        return sum(((tmp >> i) & 1) << j for i, j in enumerate(order))

    return change


class AffineSet:
    """Rightmost-pivot compression and enumeration by carries of the free counter."""
    def __init__(self, equations, width):
        rows = [mask | (rhs << width) for mask, rhs in equations]
        pivots = []
        free = []
        r = 0
        for col in range(width):
            choice = next((i for i in range(r, len(rows)) if rows[i] >> col & 1), None)
            if choice is None:
                free.append(col)
                continue
            rows[choice], rows[r] = rows[r], rows[choice]
            for i in range(len(rows)):
                if i != r and rows[i] >> col & 1:
                    rows[i] ^= rows[r]
            pivots.append(col)
            r += 1
        assert len(rows) == r
        self.free = free
        self.width = width
        self.offset = sum((row >> width) << p for p, row in zip(pivots, rows, strict=True))
        self.columns = []
        for pos in free:
            column = (1 << pos) | sum(((row >> pos) & 1) << p for p, row in zip(pivots, rows, strict=True))
            self.columns.append(column)
        assert all(((row & ((1 << width)-1)) & ((1 << p)-1)) == 0
                   for p, row in zip(pivots, rows, strict=True))

    def compress(self, word):
        return sum(((word >> j) & 1) << i for i, j in enumerate(self.free))

    def words(self):
        value = self.offset
        yield value
        for k in range(1, 1 << len(self.free)):
            flips = k ^ (k - 1)
            for j in range(flips.bit_length()):
                value ^= self.columns[j]
            yield value


def rotate(x, shift, width):
    return ((x << shift) | (x >> (width - shift))) & ((1 << width) - 1)


def rank_minimum(word, width):
    ranks = [word >> (width - 1 - i) & 1 for i in range(width)]
    length = 1
    while length < width:
        pairs = [(ranks[i], ranks[(i + length) % width]) for i in range(width)]
        ordered = {pair: rank for rank, pair in enumerate(sorted(set(pairs)))}
        ranks = [ordered[pair] for pair in pairs]
        length *= 2
    shift = ranks.index(0)
    low = rotate(word, shift, width)
    assert low == min(rotate(word, j, width) for j in range(width))
    assert width % ranks.count(0) == 0
    return low, shift, width // ranks.count(0)


def from_word(word, basis):
    width = len(basis)
    out = 0
    for j, v in enumerate(basis):
        if (word >> (width-1-j)) & 1:
            out ^= v
    return out


def from_tuple(bits):
    result = 0
    for bit in bits:
        result = 2 * result + bit
    return result


class Geometry:
    def __init__(self, c, rng):
        self.c, self.b = c, 3*c
        b = self.b
        self.a, self.q = 1 << c, 1 << b
        a, q = self.a, self.q
        ext = self.ext = fns["Field"](b)
        other = self.other = fns["Field"](b, True)
        # Small exhaustive oracle for the defining-polynomial isomorphism.
        image = next(x for x in range(q) if ext.horner(other.modulus, x) == 0)
        ambient_basis = [ext.horner(w, image) for w in other.normal()]
        self.word = {from_word(i, ambient_basis): i for i in range(q)}
        assert len(self.word) == q
        sub = [z for z in range(q) if ext.pow(z, a) == z]
        subbasis = next(ext.orbit(z) for z in sub if len(ext.orbit(z)) == c and fns["rank"](ext.orbit(z)) == c)
        subvalues = [from_word(i, subbasis) for i in range(a)]
        toword = {val:i for i, val in enumerate(subvalues)}
        kernel = [x for x in range(q) if x ^ ext.pow(x, a) ^ ext.pow(x, a*a) == 0]
        v = next(x for x in kernel if x)
        vline = {ext.mul(v, z) for z in subvalues}
        w = next(x for x in kernel if x not in vline)
        vy = [ext.mul(v, x) for x in subvalues]
        wz = [ext.mul(w, x) for x in subvalues]
        self.at = [t ^ y ^ z for t in subvalues for y in vy for z in wz]
        assert len(set(self.at)) == q
        rep_values, geometric = fns["plane_order"](ext, c)
        additive_s = [(toword[alpha ^ side] << (2*c)) | (y << c) | z
                      for alpha in rep_values for side in (0,1) for y in range(a) for z in range(a)]
        assert [self.at[s] for s in additive_s] == geometric
        order = a-1
        divs = [p for p in range(2,order+1) if order%p == 0 and all(p%j for j in range(2,p))]
        generator = next(x for x in sub if x and all(ext.pow(x,order//p)!=1 for p in divs))
        self.multiplicative = [toword[ext.pow(generator,j)] for j in range(a-1)]+[toword[0]]
        assert sorted(self.multiplicative)==list(range(a))
        self.trace_order = [toword[alpha ^ side] for alpha in rep_values for side in (0,1)]
        self.s_geometric = [(t << (2*c)) | (y << c) | z for t in self.trace_order
                            for y in self.multiplicative for z in self.multiplicative]
        assert set(self.s_geometric)==set(additive_s)
        self.source = self.reorder(self.s_geometric, False)
        assert self.source==sorted(set(additive_s))
        assert self.reorder(self.source, True)==self.s_geometric
        dtable = fns["fs1"](b)
        self.table = [(d, from_tuple(k), h) for d, k, h in dtable]
        by_poly = {h:(d,k) for d,k,h in self.table}
        f = rng.getrandbits(q)
        self.replies = {h:fns["pdiv"](f,h)[1] for _,_,h in self.table}
        self.second = {h:rng.getrandbits(d) for d,_,h in self.table}
        self.root = {}
        samples = set(rng.sample(self.s_geometric,min(12,len(self.s_geometric))))
        for s in self.s_geometric:
            x = self.at[s]
            h = ext.minimal_by_roots(x)
            actual_key = by_poly[h]
            key, r, degree = rank_minimum(self.word[x],b)
            assert degree == actual_key[0]
            if degree == b:
                assert key == actual_key[1]
            reply = self.replies[h]
            y = ext.horner(reply,x)
            mh, extracted, _ = fns["projected_remainder"](ext,x,y)
            assert (mh,extracted) == (h, reply)
            if s in samples:
                assert ext.horner(f,x) == y
            self.root[s] = (h, actual_key, key, r, degree, extracted)
        self.base,_ = affine_parts(lambda s:self.word[self.at[s]],b,b)
        assert all(apply(self.base,s) == self.word[self.at[s]] for s in range(q))


    def reorder(self, items, backwards):
        """Plane-key rows and two actual wide axis shuffles, with explicit transposes."""
        a,c = self.a,self.c
        trace_keys = sorted(self.trace_order) if backwards else self.trace_order
        axes = list(range(a)) if backwards else self.multiplicative
        target_rank = ({v:i for i,v in enumerate(self.multiplicative)} if backwards else
                       {i:i for i in range(a)})
        trace_rank = ({v:i for i,v in enumerate(self.trace_order)} if backwards else
                      {v:v for v in self.trace_order})
        order = sorted(range(a),key=lambda i:target_rank[axes[i]])
        planes = []
        for i,t in enumerate(trace_keys):
            chunk = items[i*a*a:(i+1)*a*a]
            rows = [chunk[y*a:(y+1)*a] for y in order]
            cols = list(zip(*rows,strict=True))
            rows = zip(*(cols[z] for z in order),strict=True)
            planes.append((trace_rank[t],[p for row in rows for p in row]))
        return [x for _,plane in sorted(planes) for x in plane]


def merge_runs(runs):
    while len(runs)>1:
        joined=[]
        for i in range(0,len(runs),2):
            if i+1==len(runs):
                joined.append(runs[i])
            else:
                joined.append(list(merge(runs[i],runs[i+1],key=itemgetter(0))))
        runs=joined
    return next(iter(runs),[])


class SubspaceRoute:
    def __init__(self, geo, mark, e, shift, counts):
        b = geo.b
        first = range(b-mark,b)
        rotrows,_ = affine_parts(lambda s:rotate(apply(geo.base,s),shift,b),b,b)
        revrows = inverse(rotrows)
        src = AffineSet([(1<<i,e) for i in first]+[(rotrows[i],0) for i in first],b)
        dst = AffineSet([(revrows[i],e) for i in first]+[(1<<i,0) for i in first],b)
        self.source = list(src.words())
        self.target = list(dst.words())
        dimension = b-2*mark
        assert len(self.source)==len(self.target)==1<<dimension
        assert self.source==sorted(set(self.source)) and self.target==sorted(set(self.target))
        assert [src.compress(v) for v in self.source]==list(range(1<<dimension))
        assert [dst.compress(v) for v in self.target]==list(range(1<<dimension))
        func = lambda i:dst.compress(apply(rotrows,self.source[i]))
        matrix,off = affine_parts(func,dimension,dimension)
        lut = ldu(matrix)
        inv_lut = ldu(inverse(matrix))
        self.forward = [lut(i)^off for i in range(1<<dimension)]
        self.backward = [inv_lut(i^off) for i in range(1<<dimension)]
        assert all(j==func(i) and self.backward[j]==i and self.target[j]==apply(rotrows,s)
                   for i,(s,j) in enumerate(zip(self.source,self.forward,strict=True)))
        counts["forward_and_reverse_affine_address_checks"] += 2<<dimension
        counts["independent_prefix_systems"] += 1

    def route(self, items, backwards=False):
        source,target,perm = ((self.target,self.source,self.backward) if backwards else
                              (self.source,self.target,self.forward))
        k = 0
        dense = [None]*len(source)
        for i,w in enumerate(source):
            if k<len(items) and w == items[k][0]:
                dense[perm[i]] = items[k][1]
                k += 1
        assert k == len(items)
        return [(w,x) for w,x in zip(target,dense,strict=True) if x is not None]


def trial(geo, mark):
    counts = Counter()
    b,c = geo.b,geo.c
    mask = (1<<mark)-1
    forward = defaultdict(list)
    tail = []
    for s in geo.source:
        h,actual_key,m,r,period,reply = geo.root[s]
        prefix = s >> (b-mark)
        item = (s,h,actual_key,reply)
        if period<b or prefix not in (0,mask) or m>>(b-mark):
            tail.append((actual_key,item,None))
        else:
            forward[prefix==mask,r].append((s,item))
    runs = [sorted(tail,key=itemgetter(0))]
    maps = {}
    for e in (0,1):
        for r in range(b):
            tag = (e,r)
            maps[tag] = SubspaceRoute(geo,mark,e,r,counts)
            run = maps[tag].route(forward[tag])
            out=[]
            for m,item in run:
                s,h,key,reply = item
                assert key == (b,m)
                out.append((key,item,tag))
            runs.append(out)
    sorted_rows=merge_runs(runs)
    result=[]
    keyset=set()
    invgroups=defaultdict(list)
    exception_values=[]
    sorted_outputs=[]
    for key,item,tag in sorted_rows:
        s,h,found_key,reply = item
        assert found_key == key
        if key not in keyset:
            keyset.add(key)
            result.append((key[0],key[1],h,reply))
        second = geo.second[h]
        if tag is None:
            exception_values.append((s,geo.ext.horner(second,geo.at[s])))
        else:
            invgroups[tag].append((key[1],(s,second)))
    assert result == [(d,k,h,geo.replies[h]) for d,k,h in geo.table]
    sorted_outputs.append(sorted(exception_values))
    for tag,rows in invgroups.items():
        out=[]
        for s,(old,second) in maps[tag].route(rows,True):
            assert old==s
            out.append((s,fns["compose"](geo.ext,second,geo.at[s])))
        sorted_outputs.append(out)
    restored=geo.reorder(merge_runs(sorted_outputs),True)
    assert [s for s,_ in restored]==geo.s_geometric
    for s,x in restored:
        assert x==geo.ext.horner(geo.second[geo.root[s][0]],geo.at[s])
    counts["FS1_factors_in_exact_order"]+=len(result)
    counts["actual_geometric_occurrences_each_way"]+=len(geo.s_geometric)
    counts["duplicate_occurrences"]+=len(geo.s_geometric)-len(result)
    counts["main_occurrences_e0"]+=sum(len(x) for (e,_),x in forward.items() if not e)
    counts["main_occurrences_e1"]+=sum(len(x) for (e,_),x in forward.items() if e)
    counts["exception_occurrences"]+=len(tail)
    counts["proper_degree_occurrences"]+=sum(rec[4]<b for rec in geo.root.values())
    counts["actual_multiplicative_grid_positions_restored"]+=len(restored)
    counts["independent_inverse_bits"]+=geo.q
    return {"c":c,"b":b,"marker":mark,"ambient_modulus":geo.ext.modulus,
            "FS1_modulus":geo.other.modulus,"counts":dict(sorted(counts.items()))}


def main():
    rng=Random(0xA00B17)
    cases=[]
    for c in range(1,5):
        geo=Geometry(c,rng)
        for h in sorted(set([1,min(2,c),c])):
            cases.append(trial(geo,h))
    totals=Counter()
    for case in cases: totals.update(case["counts"])
    assert all(totals[key]>0 for key in ("main_occurrences_e0","main_occurrences_e1","exception_occurrences"))
    print(json.dumps({"seed":"0xa00b17","cases":cases,"totals":dict(sorted(totals.items()))},indent=2))


if __name__=="__main__":
    main()
