"""Lead's reverse-adjoint BIT source and independent exact-price review.

No new worker or predecessor scientific module is imported. Universal scope is
the normalized cut theorem; this finite replay checks its source premises.
"""
from pathlib import Path
from collections import Counter
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def adjoint(w, program):
    n = w['public']
    columns = [1 << i for i in range(n)] + [0] * w['owned_fields']
    for e in reversed(program):
        op, a = e[:2]
        if op == 'ADD':
            columns[e[2]] ^= columns[a]
        elif op == 'SWAP':
            b = e[2]; columns[a], columns[b] = columns[b], columns[a]
        elif op in ('INIT', 'CLEAR'):
            columns[a] = 0
        elif op != 'MOVE':
            raise ValueError(op)
    return columns[:n]


def root200(n):
    x = 1 << ((n.bit_length()+199)//200)
    while True:
        y = (199*x+n//x**199)//200
        if y >= x:
            break
        x = y
    while x**200 > n:
        x -= 1
    while (x+1)**200 <= n:
        x += 1
    need(x**200 <= n < (x+1)**200, 'outward integer root')
    return x


def bounds(hist):
    den = 10**18; lo = hi = 0
    for r, count in hist.items():
        n = r**199 * den**200; a = root200(n); b = a+(a**200 != n)
        lo += count*(a if count >= 0 else b)
        hi += count*(b if count >= 0 else a)
    return [lo,hi,den]


def main():
    raw = (ROOT/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78', 'source pin')
    w = json.loads(gzip.decompress(raw)); n = w['public']; program = w['program']
    expected = [1 << i for i in range(n)]
    for i in range(111):
        expected[i] ^= 1 << (111+i)
    need(adjoint(w,program) == expected, 'full reverse native columns')
    skeleton = [e for e in program if e[1] < 222 and
                (e[0] not in ('ADD','SWAP') or e[2] < 222)]
    need(adjoint(w,skeleton) == [1 << i for i in range(n)], 'main skeleton identity')
    last_add = max(i for i,e in enumerate(program) if e[0] == 'ADD')
    need(adjoint(w,program[:last_add]+program[last_add+1:]) != expected, 'omitted ADD mutant')
    dims = {int(k):f['dim'] for k,f in w['frames'].items()}
    need({dims[f] for f in w['final'][:111]} == {8}, 'X endpoint chart')
    need({dims[f] for f in w['final'][111:222]} == {7}, 'Y endpoint chart')
    need(all(expected[i] == 1 << i for i in range(222,n)), 'all helpers X-independent')
    paid_main,paid_core,H = Counter(),Counter(),Counter()
    for e in program:
        if e[0] == 'MOVE':
            rank = abs(dims[e[2]]-dims[e[3]])
            need(rank > 0, 'positive MOVE rank')
            (paid_main if e[1] < 222 else paid_core)[rank] += 1
    for i in range(222,n):
        H[abs(dims[w['final'][i]]-dims[w['start'][i]])] += 1
    caller_raw=(ROOT/'research/paired-query-only-bit/data/query_only_6980.json').read_bytes()
    need(hashlib.sha256(caller_raw).hexdigest() == '3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e','caller pin')
    caller=json.loads(caller_raw); signed=Counter()
    for r in H: signed[r] += 36*H[r]
    for r in paid_main: signed[r] -= 36*paid_main[r]
    for r in paid_core: signed[r] -= 36*paid_core[r]
    for row in caller['types']['A']['diagonal']:
        need(any(row[2:]), 'no empty root credit')
        signed[1+7*sum(row[2:])] += 111
    for e in caller['events']:
        if e[:2] == ['A','QUERY']: signed[1] -= 111
        if e[:2] == ['A','IDLE_ONE']: signed[7*len(e[3])] -= 111
    M=bounds(signed); D=bounds({r:paid_core[r]-H[r] for r in set(paid_core)|set(H)})
    need(M[1] < -444*M[2] and D[1] < 88*D[2], 'strict full budget bounds')
    print(json.dumps({'status':'PASS_LEAD_REVERSE_BIT_CUT_REVIEW','public_matrix_coefficients':n*n,
        'source_events':len(program),'M2_interval':list(map(str,M)),'D_interval':list(map(str,D)),
        'rank_cut_argument':'Every low-side rank increase requires a downward MOVE; 111m-111 new directions.',
        'controls':['deleted final ADD rejected','no empty root credit','all low helpers included'],
        'scope':'Normalized linear boundary grammar; not arbitrary physical or changed-prefix lower bound.'},indent=2))


if __name__ == '__main__':
    main()
