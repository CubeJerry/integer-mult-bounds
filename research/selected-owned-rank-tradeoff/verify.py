"""Source-bound owned-rank tradeoff checks. Python stdlib; no imports of predecessors."""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORD_HASH = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE_HASH = 'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def span(basis):
    out = {0}
    for v in basis:
        need(type(v) is int and 0 < v < 512, 'invalid frame vector')
        need(v not in out, 'dependent frame basis')
        out |= {x ^ v for x in tuple(out)}
    return out


def source_rows(word):
    pub = word['public']
    rows = [{i: Fraction(1)} for i in range(pub)] + [None] * word['owned_fields']
    cur = word['initial'] + [None] * word['owned_fields']
    spaces = [span(b) for b in word['frames']]
    found = []
    for k, event in enumerate(word['program']):
        op, a = event[:2]
        if op == 'INIT':
            need(rows[a] is None, 'INIT of live owner')
            rows[a], cur[a] = {}, event[2]
        elif op == 'CLEAR':
            need(rows[a] is not None and cur[a] == event[2], 'CLEAR domain')
            rows[a], cur[a] = None, None
        elif op in ('ADD', 'COPY'):
            _, a, b, c, frame = event
            need(cur[a] == frame == cur[b], 'common-chart contact')
            need(rows[a] is not None and rows[b] is not None, 'dead contact')
            c = Fraction(c)
            for col, value in tuple(rows[b].items()):
                value = rows[a].get(col, 0) + c * value
                if value:
                    rows[a][col] = value
                else:
                    rows[a].pop(col, None)
        elif op == 'SCALE':
            _, a, c, frame = event
            c = Fraction(c)
            need(c != 0 and cur[a] == frame, 'SCALE domain')
            rows[a] = {col: c * value for col, value in rows[a].items()}
        elif op == 'MOVE':
            _, a, u, v, _ = event
            need(cur[a] == u, 'MOVE source frame')
            if a >= pub and len(word['frames'][v]) > len(word['frames'][u]):
                need(spaces[u] < spaces[v], 'rise is not nested')
                data = [[i, str(c)] for i, c in sorted(rows[a].items())]
                need(data, 'zero owned input cannot establish reachability')
                found.append({
                    'event': k, 'owner': a, 'source_frame': u, 'target_frame': v,
                    'rank': len(word['frames'][v]) - len(word['frames'][u]),
                    'support': len(data), 'pivot': data[0],
                    'row_sha256': hashlib.sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest(),
                })
            cur[a] = v
        else:
            raise ValueError('unsupported opcode')
    return found


def root_interval(rank, scale=10**24):
    """A guessed enclosure is accepted only after exact integer-power checks."""
    need(type(rank) is int and rank >= 1, 'root rank')
    with localcontext() as ctx:
        ctx.prec = 90
        q = int((Decimal(rank) ** (Decimal(199) / 200)) * scale)
    value = rank**199 * scale**200
    need(q**200 <= value < (q+1)**200, 'integer-root certificate')
    return Fraction(q, scale), Fraction(q+1, scale)


def moment(histogram):
    lo = hi = Fraction(0)
    for rank, count in histogram.items():
        need(type(count) is int and count >= 0, 'histogram count')
        a, b = root_interval(int(rank))
        lo += count*a
        hi += count*b
    return lo, hi


def exact_budget(invoice, histogram):
    t0, t1 = moment(invoice['T'])
    p0, p1 = moment(invoice['P'])
    r0, r1 = moment(histogram)
    m = (t0-p1, t1-p0)
    free = (m[0]+18*r0, m[1]+18*r1)
    need(Fraction(-567716011, 10**6) < m[0] <= m[1] < Fraction(-567716010, 10**6), 'selected target deficit')
    need(Fraction(434821363, 10**6) < free[0] <= free[1] < Fraction(434821364, 10**6), 'free-rise relaxation')
    need(sum(histogram.values()) == 23 and sum(int(r)*v for r,v in histogram.items()) == 56, 'rise census')
    return {'target': '1/200', 'power': '199/200', 'raw_moment': [str(x) for x in m],
            'rise_moment_per_native': [str(r0), str(r1)],
            'free_rise_raw_moment': [str(x) for x in free]}


def mul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def check_gaussian(rows, dim):
    n = 1 << dim
    a = (Fraction(1,2), Fraction(1,2))
    b = (Fraction(1,2), Fraction(-1,2))
    for i in range(n):
        for j in range(n):
            expected = (Fraction(1), Fraction(0))
            for axis in range(dim):
                expected = mul(expected, b if ((i^j)>>axis)&1 else a)
            need(rows[i][j] == expected, 'scalar escape tensor identity')
            need(rows[i][j][0]**2+rows[i][j][1]**2 == Fraction(1,n), 'flat Gaussian row')


def reject(call, name):
    try:
        call()
    except ValueError:
        return name
    raise ValueError('missed negative control: '+name)


def scalar_escape(dim):
    """Apply one literal whole-field scalar butterfly per binary coordinate."""
    n = 1 << dim
    a = (Fraction(1,2), Fraction(1,2))
    b = (Fraction(1,2), Fraction(-1,2))
    rows = [[(Fraction(i == j), Fraction(0)) for j in range(n)] for i in range(n)]
    for axis in range(dim):
        rows = [[add(mul(a, rows[i][j]), mul(b, rows[i ^ (1<<axis)][j]))
                 for j in range(n)] for i in range(n)]
    check_gaussian(rows, dim)
    if dim == 2:
        wrong_phase = [[mul((0,1), x) for x in row] for row in rows]
        reject(lambda: check_gaussian(wrong_phase, dim), 'wrong absolute phase')
        omitted = [[(Fraction(i == j), Fraction(0)) for j in range(n)] for i in range(n)]
        omitted = [[add(mul(a, omitted[i][j]), mul(b, omitted[i^1][j])) for j in range(n)] for i in range(n)]
        reject(lambda: check_gaussian(omitted, dim), 'omitted Gaussian axis')
    return n*n


def finite_controls():
    entries = sum(scalar_escape(d) for d in range(1,7))
    cases = 0
    for r in range(1,7):
        for f in range(1,9):
            for s in range(r):
                for g in range((r-s)*f+1):
                    deficit = (r-s)*f-g
                    lower = max(Fraction(0), Fraction(1)-Fraction(2)**(-deficit))
                    if g < (r-s)*f:
                        need(lower >= Fraction(1,2), 'rank shaving error floor')
                    else:
                        need(lower == 0, 'attainable support boundary')
                    cases += 1
    # Distinguish a fixed ordinary budget from the genuine linear-work escape.
    need(1 - Fraction(2)**(3-4) == Fraction(1,2), 'three ADDs cannot replace width four rank one')
    need(1 - Fraction(2)**(4-4) == 0, 'four ADD escape must remain permitted')
    reject(lambda: span([1,1]), 'dependent frame')
    return {'tradeoff_integer_cases': cases, 'exact_gaussian_entries': entries,
            'named_controls': ['one-rank-shave', 'linear-ADD-escape', 'omitted-axis', 'wrong-phase', 'dependent-frame']}


def main():
    parser = argparse.ArgumentParser()
    root = HERE.parents[1]
    parser.add_argument('--word', type=Path, default=root/'research/shared-wire-split-composition/data/final.json.gz')
    parser.add_argument('--invoice', type=Path, default=root/'research/shared-wire-split-composition/FULL-RESULT.json')
    args = parser.parse_args()
    raw = args.word.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == WORD_HASH, 'word hash')
    iraw = args.invoice.read_bytes()
    need(hashlib.sha256(iraw).hexdigest() == INVOICE_HASH, 'invoice hash')
    word = json.loads(gzip.decompress(raw))
    rows = source_rows(word)
    expected = json.loads((HERE/'OWNED-ROWS.json').read_text())
    need(rows == expected['rises'], 'source row certificate')
    histogram = dict(sorted(Counter(x['rank'] for x in rows).items()))
    need(histogram == {1:10,2:4,3:1,4:6,5:1,6:1}, 'source rank profile')
    budget = exact_budget(json.loads(iraw)['invoice'], histogram)
    controls = finite_controls()
    print('PASS_SELECTED_OWNED_RANK_TRADEOFF '+json.dumps({
        'source_events': len(word['program']), 'owned_rises': len(rows),
        'minimum_nonzero_support': min(x['support'] for x in rows),
        'maximum_nonzero_support': max(x['support'] for x in rows),
        'budget': budget, 'controls': controls, 'new_kappa': False}, sort_keys=True))


if __name__ == '__main__':
    main()
