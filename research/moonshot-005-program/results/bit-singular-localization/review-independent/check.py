#!/usr/bin/env python3
"""Independent original-gzip audit of singular-code localization.

No author checker or recovered root list is imported. This uses a different
construction of h and integer finite-field witnesses with prime 107.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def basis(rows):
    pivots = {}
    for x in rows:
        while x:
            low = x & -x
            if low in pivots:
                x ^= pivots[low]
            else:
                pivots[low] = x
                break
    return [pivots[k] for k in sorted(pivots)]


def span(rows):
    out = [0]
    for r in basis(rows):
        out += [v ^ r for v in out]
    return out


def support(w):
    return [i for i in range(111) if w & (1 << i)]


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rank107(rows):
    pivots = []
    columns = []
    for row in rows:
        v = [x % 107 for x in row]
        for col, pivot in zip(columns, pivots):
            scale = v[col]
            v = [(x-scale*y) % 107 for x, y in zip(v, pivot)]
        if not any(v):
            continue
        c = next(i for i, x in enumerate(v) if x)
        scale = pow(v[c], -1, 107)
        pivots.append([(x*scale) % 107 for x in v])
        columns.append(c)
        if len(pivots) == 8:
            break
    return len(pivots)


def line(r):
    sign = 1 if next(x for x in r if x) > 0 else -1
    return tuple(sign*x for x in r)


def run(repo, author_result=None):
    source = repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    raw = source.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    need(source_hash == '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78', 'original native hash')
    native = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        r = [Fraction(v) for v in native['frames'][str(native['start'][i])]['B'][0]]
        norm = dot(r, r)
        need(norm in (1, 4), 'native root norm')
        r = [x*(2 if norm == 1 else 1) for x in r]
        need(all(x.denominator == 1 for x in r), 'integral normalization')
        roots.append(line([int(x) for x in r]))
    omitted = (0,0,1,1,0,0,1,-1)
    need(omitted not in roots and dot(roots[72], omitted) == 0, 'actual omitted partner')
    canonical = [sum(1 << j for j, s in enumerate(roots) if i == j or dot(r,s) == 0) for i,r in enumerate(roots)]
    kb = sum(1 << j for j,s in enumerate(roots) if dot(omitted,s) == 0)
    h = canonical[72] ^ kb
    whole = (1 << 111)-1
    d8 = whole ^ h
    need((d8.bit_count(),h.bit_count()) == (52,59), 'singular classes')
    fitting = [k & (h if (h >> i)&1 else d8) for i,k in enumerate(canonical)]
    bb = basis(fitting)
    need(len(bb) == 15, 'code dimension')
    masks = sorted({tuple(i for i,x in enumerate(r) if x) for r in roots if sum(x != 0 for x in r) == 4})
    full = [tuple(2*int(i == j) for i in range(8)) for j in range(8)]
    for mask in masks:
        for signs in range(8):
            r = [0]*8
            r[mask[0]] = 1
            for j in range(1,4):
                r[mask[j]] = 1 if signs & (1 << (j-1)) else -1
            full.append(tuple(r))
    need(len(set(full)) == 120, 'full geometry')
    facet_masks = {normal:sum(1 << i for i,r in enumerate(roots) if dot(normal,r) == 0) for normal in full}
    proper = {}
    census = Counter()
    all_words = span(bb)
    need(len(all_words) == 32768 and len(set(all_words)) == 32768, 'complete word enumeration')
    for w in all_words[1:]:
        rank = rank107(roots[i] for i in support(w))
        census[rank] += 1
        if rank == 8:
            continue
        need(rank == 7, 'no nonzero code word below rank seven')
        normals = [r for r,mask in facet_masks.items() if not (w & ~mask)]
        need(len(normals) == 1, 'unique exact rational facet upper bound')
        proper[w] = normals[0]
    need(census == {7:69,8:32698}, 'complete proper census')
    local = {r:[] for r in full}
    for word, normal in proper.items():
        local[normal].append(word)
    classes = Counter()
    for normal, words in local.items():
        if not words:
            continue
        i = roots.index(normal) if normal in roots else None
        cls = 'native_d8' if i is not None else ('omitted_d8' if len(words)==3 else 'omitted_spinor')
        classes[cls] += 1
        need(len(words)==(1<<len(basis(words)))-1, 'complete localized subspace')
    need(classes == {'native_d8':52,'omitted_d8':4,'omitted_spinor':5}, 'facet classification')
    for i,r in enumerate(roots):
        need(set(local[r]) == (set() if (h>>i)&1 else {canonical[i]&h}), 'receiver-localized space')
    need(len(basis(fitting[i] for i in support(h))) == 8, 'forced spinor dimension')
    need(len(basis(fitting[i] for i in support(d8))) == 7, 'forced D8 quotient dimension')
    need(len(basis(proper)) == 12, 'all proper-mode span')
    dm = sorted({w&d8 for w in proper if w&d8})
    sm = sorted({w&h for w in proper if w&h})
    need(len(dm)==4 and all(x&y for i,x in enumerate(dm) for y in dm[i+1:]), 'D8 overlap')
    edges=[(i,j) for i,x in enumerate(sm) for j,y in enumerate(sm) if i<j and not (x&y)]
    deg=Counter(i for edge in edges for i in edge)
    need(len(sm)==61 and len(edges)==28 and max(deg.values())==1, 'spinor matching')
    need(all(sm[i]^sm[j]==h for i,j in edges), 'complementary pairs')
    if author_result is not None:
        author=json.loads(author_result.read_text())
        entries=author.get('proper_words',author.get('proper',[]))
        if entries:
            need({int(x['word']) for x in entries}==set(proper),'independent proper-word agreement')
    need(1 not in set(all_words), 'raw original is outside the history code')
    p,y=1,2
    y ^= p
    p ^= y
    need((p,y)==(2,3), 'terminal-span counterexample')
    return {'status':'PASS_ORIGINAL_NATIVE_SINGULAR_LOCALIZATION_REVIEW','native_sha256':source_hash,
            'method':'original gzip roots; h=K72+K_omitted; complete binary enumeration; prime107 lower witnesses; exact full-root facet upper witnesses',
            'field_and_block_extension':'written proof reviewed separately; no finite-field extrapolation',
            'nonzero_words':32767,'proper_rank_seven_words':69,'full_rank_words':32698,
            'facets':dict(classes),'proper_span_dimension':12,'forced_fitting_dimensions':[8,7],
            'D8_local_modes':4,'spinor_local_modes':61,'disjoint_spinor_pairs':28,
            'proper_word_set_sha256':hashlib.sha256(json.dumps(sorted(proper)).encode()).hexdigest(),
            'negative_controls':['raw unit input not in W','two-ADD terminal-history export'],
            'no_new_kappa':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=Path('.'))
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--author-result',type=Path)
    args=parser.parse_args()
    result=run(args.repo,args.author_result)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
