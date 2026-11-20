#!/usr/bin/env python3
"""Construct causal field words on the exact physical K owners at every plane."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

DEGREE = 6
MODULUS = 0x43
LAYOUT = ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
          '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
ROUTES = ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
          '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')


def need(condition, label):
    if not condition:
        raise ValueError(label)


def payload(base, path, digest):
    raw = gzip.decompress((base/path).read_bytes())
    need(hashlib.sha256(raw).hexdigest() == digest, path)
    return raw


def multiply(a, b):
    v = 0
    while b:
        if b & 1:
            v ^= a
        a <<= 1
        if a & 64:
            a ^= MODULUS
        b >>= 1
    return v


MUL = [[multiply(a,b) for b in range(64)] for a in range(64)]
need(all(set(row) == set(range(64)) for row in MUL[1:]), 'field inverses')


@lru_cache(maxsize=None)
def vandermonde_T(n):
    field = [[1]*n]
    for _ in range(n-1):
        field.append([MUL[z][j+1] for j, z in enumerate(field[-1])])
    bits = [0]*(DEGREE*n)
    for i, row in enumerate(field):
        for j, z in enumerate(row):
            for b in range(DEGREE):
                m = MUL[z][1<<b]
                for a in range(DEGREE):
                    if (m>>a)&1:
                        bits[DEGREE*i+a] |= 1<<(DEGREE*j+b)
    work = bits.copy()
    operations = []
    def add(dst, src):
        work[dst] ^= work[src]
        operations.append([dst, src])
    for i in range(len(bits)):
        k = next(k for k in range(i, len(bits)) if (work[k]>>i)&1)
        if k != i:
            add(k,i)
            add(i,k)
            add(k,i)
        for j in range(len(bits)):
            if j != i and (work[j]>>i)&1:
                add(j,i)
    identity = [1<<i for i in range(len(bits))]
    need(work == identity, 'binary elimination')
    operations.reverse()
    for dst,src in operations:
        work[dst] ^= work[src]
    need(work == bits, 'forward template on all binary inputs')
    for dst,src in reversed(operations):
        work[dst] ^= work[src]
    need(work == identity, 'inverse template')
    return operations


def fid(route):
    return (53280 if route[0]=='Y' else 0) + 480*route[1]+route[2]


def swap_count(perm):
    need(set(perm) == set(perm.values()), 'in-place physical permutation')
    visited = set()
    swaps = 0
    for u in sorted(perm):
        if u in visited:
            continue
        v = u
        while v not in visited:
            visited.add(v)
            v = perm[v]
            swaps += 1
        need(v == u, 'disjoint cycles')
        swaps -= 1
    return swaps


def build_chart(rows, native, marked, split):
    native = sorted(native)
    ne = sum(r[0] == 'X' for r in rows)
    if not native:
        need(len(rows) == ne == 90, 'empty K has only passthrough owners')
        return {}, Counter(), 0
    mixed = len(native) < 3
    ds = sorted({r[4] for r in rows})
    groups = [[d for d in ds if d in marked], [d for d in ds if d not in marked]] if split else [ds]
    need([len(g) for g in groups] == ([9,36] if split else [45]), 'spread incidence')
    by_d = defaultdict(list)
    recipients = defaultdict(list)
    for r in rows:
        phase = r[0]
        by_d[phase,r[4]].append(fid(r))
        i = r[7] if phase == 'X' else r[1]
        recipients[phase,i if i in native else None].append(fid(r))
    for values in by_d.values():
        values.sort()
    recipients = {key: sorted(value,reverse=True) for key,value in recipients.items()}
    if len(native)==2:
        small = next(i for i in native if len(recipients.get(('X',i),[]))==15)
        large = next(i for i in native if i!=small)
    phases = ('Y',) if ne==0 else ('X','Y')
    words = []
    snapshot_pairs = []
    perm = defaultdict(dict)
    costs = Counter()
    for ds_component in groups:
        n = len(ds_component)
        k = n//3
        for phase in phases:
            stripes = len(by_d[phase,ds_component[0]])
            need(all(len(by_d[phase,d])==stripes for d in ds_component), 'uniform D flags at K')
            for stripe in range(stripes):
                inp = [by_d[phase,d][stripe] for d in ds_component]
                out = []
                for t in range(n):
                    if len(native)==3:
                        receiver = native[t//k]
                    elif len(native)==2:
                        receiver = small if t>=2*k else (large if phase=='Y' else None)
                    else:
                        receiver = native[0] if phase=='Y' else None
                    out.append(recipients[phase,receiver].pop())
                words.append([phase, inp, out])
                perm[phase].update(zip(inp,out))
                costs['template_forward_ADD'] += len(vandermonde_T(n))
                if phase=='Y' and mixed:
                    early_word = words[-2]
                    need(early_word[0]=='X' and len(early_word[1])==n, 'paired phase order')
                    for t in range(1,2*k,2):
                        snapshot_pairs.append([early_word[2][t-1],out[t]])
    need(all(not a for a in recipients.values()), 'all terminal and transit owners used')
    for phase in phases:
        costs['permutation_forward_ADD'] += swap_count(perm[phase])*3*DEGREE
    ns = len(snapshot_pairs)
    need(ns == (15 if mixed else 0), 'minimum snapshot')
    costs['snapshot_write_ADD'] += DEGREE*ns
    costs['snapshot_read_ADD'] += DEGREE*ns
    costs['pure_inverse_ADD'] += costs['template_forward_ADD']+costs['permutation_forward_ADD']
    costs['INIT'] += DEGREE*ns
    costs['dirty_CLEAR'] += DEGREE*ns
    data = {'stripes': words,'early_cache_to_late': snapshot_pairs}
    return data,costs,ns


def dump(path, obj):
    raw = json.dumps(obj,separators=(',',':')).encode()
    path.write_bytes(gzip.compress(raw,mtime=0))
    return hashlib.sha256(raw).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args=p.parse_args()
    base=args.repo/'research/moonshot-005-program/results'
    layout=json.loads(payload(base,*LAYOUT))
    raw=gzip.decompress((base/'bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz').read_bytes())
    marked=set(json.loads(raw)['selected_D'])
    need(len(marked)==630, 'spread certificate')
    groups=defaultdict(list)
    for line in payload(base,*ROUTES).splitlines():
        r=json.loads(line)
        if r[5] is not None:
            groups[r[5]].append(r)
    args.out.mkdir(parents=True,exist_ok=True)
    summary={'field_modulus':MODULUS, 'layout_payload':LAYOUT[1], 'routes_payload':ROUTES[1],
             'spread_payload':hashlib.sha256(raw).hexdigest(),'new_complete_kappa':False}
    foreign=0
    roots=layout['root_table']
    for k,K in enumerate(layout['A2']):
        if any(i<111 for i in K):
            source=[j for j in range(111) if all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for i in K)]
            foreign += len(source)*sum(i<111 for i in K)
    summary['native_K_receiver_donor_triples']=foreign
    for variant,split in [('spread',True),('mixed',False)]:
        prices=Counter()
        chart_words={}
        ranks=Counter()
        for k, K in enumerate(layout['A2']):
            native = [i for i in K if i<111]
            words,cost,ns=build_chart(groups[k],native,marked,split)
            if words:
                chart_words[k]=words
            ranks[ns]+=1
            prices.update(cost)
        prices['total_ADD']=sum(v for key,v in prices.items() if key.endswith('_ADD'))
        summary[variant]={'number_active_K':len(chart_words),'stationary_symbols_per_K':dict(ranks),
                          'total_cache_symbols_bank480':sum(n*x for x,n in ranks.items()),
                          'one_body':dict(prices),'bank3840':{key:8*val for key,val in prices.items()},
                          'extra_MOVE':0, 'word_payload':dump(args.out/(variant.upper()+'-OWNERS.json.gz'),chart_words)}
    summary['template_payload']=dump(args.out/'TEMPLATES.json.gz',{n:vandermonde_T(n) for n in (9,36,45)})
    (args.out/'RESULT.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':
    main()
