"""Independent construction, binary elimination and minimum-index charge checks."""
from hashlib import sha256
import json
import random


def product(p, q):
    value = 0
    while p:
        bit = p & -p
        value ^= q << (bit.bit_length() - 1)
        p -= bit
    return value


def inverse_columns(triangular):
    # Eliminate the leading ordinary coefficient of every basis polynomial.
    inverse = []
    for j, col in enumerate(triangular):
        assert col.bit_length() == j + 1
        encoded = 1 << j
        lower = col ^ encoded
        while lower:
            bit = lower & -lower
            encoded ^= inverse[bit.bit_length()-1]
            lower -= bit
        inverse.append(encoded)
    return inverse


def rank(columns):
    pivots = {}
    for col in columns:
        while col:
            i = col.bit_length() - 1
            if i not in pivots:
                pivots[i] = col
                break
            col ^= pivots[i]
    return len(pivots)


def blocks(cols, v, d):
    for i in range(d):
        h = v << i
        mask = (1 << h) - 1
        for s in range(0, len(cols), 2*h):
            yield i, s, rank((col >> s) & mask for col in cols[s+h:s+2*h])


def circuits():
    # Exhaust every two-gate wiring on eight independent inputs and sample
    # longer circuits. Select one output of each pivot for unit triangularity.
    gen = random.Random(967)
    counts = {'circuits': 0, 'circuits_with_jump': 0, 'tested_interval_charges': 0}
    for t in range(28*36 + 300):
        n = 8
        signals = [1 << i for i in range(n)]
        minimum = lambda x: (x & -x).bit_length() - 1
        jumps = []
        crossings = []
        gates = 2 if t < 28*36 else 40
        for step in range(gates):
            if t < 28*36:
                j = t // 36 if step == 0 else t % 36
                pairs = [(a,b) for a in range(len(signals)) for b in range(a+1,len(signals))]
                x,y = (signals[k] for k in pairs[j])
            else:
                x,y = gen.sample(signals, 2)
            value = x ^ y
            if value:
                a,b = sorted([minimum(x), minimum(y)])
                if a == b:
                    jumps.append((a,minimum(value)))
                else:
                    crossings.append((a,b))
                signals.append(value)
        rows = [gen.choice([s for s in signals if minimum(s)==i]) for i in range(n)]
        for offset in range(n):
            total = charge = 0
            for i in range(3):
                h = 1 << i
                for start in range(offset % (2*h)-2*h,n,2*h):
                    mask = sum(1 << k for k in range(max(0,start+h),min(n,start+2*h)))
                    rr = rank(rows[k] & mask for k in range(max(0,start),min(n,start+h)))
                    ordinary = sum(start<=a<start+h<=b<start+2*h for a,b in crossings)
                    repairs = sum(a<start<=new<start+h for a,new in jumps)
                    assert rr <= ordinary+repairs
                    total += rr
                    charge += ordinary+repairs
                    counts['tested_interval_charges'] += 1
            assert total <= charge <= gates+3*len(jumps)
        counts['circuits'] += 1
        counts['circuits_with_jump'] += bool(jumps)
    return counts


def main():
    report = {'degrees': [], 'circuit_checks': circuits()}
    for c in [2,3,4,5]:
        a = 1 << c
        v = 2*a*a
        s = sum(1 << i for i in [v,v//2,2*a,a,2,1])
        p = 1
        cols = []
        for _ in range(a//2):
            cols.extend(p << k for k in range(v))
            p = product(p,s)
        inv = inverse_columns(cols)
        out = list(blocks(cols,v,c-1))
        back = list(blocks(inv,v,c-1))
        assert back == out
        assert all(count == (v-1)*(1 << i) for i,_,count in out)
        for i in range(c-1):
            assert sum(count for lev,_,count in out if i==lev) == len(cols)//2*(v-1)//v
        report['degrees'].append({'b':3*c, 'columns_each_way':len(cols), 'windows_each_way':len(out),
                                  'odd_parent_windows':(len(out)-1)//2,
                                  'rank_digest':sha256(repr(out).encode()).hexdigest()})
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
