#!/usr/bin/env python3
"""Exact source-bound audit of the normalized BIT endpoint rank cut.

The universal result is proved in PROOF.md. This script has no author scientific
imports. It audits finite source facts, all finite lifts listed, exact tariff
bounds, exhaustive tiny local transitions and premise-breaking controls.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path

NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
NATIVE_BLOB = "b718d6b2848215ad785022106dfa9f871a3d1c0c"
SOURCE_BASE = "e54523517d0f03e58352e647c403a5af3e525a57"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def gf2_rank(rows):
    basis = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def cut_rank(rows, charts):
    return gf2_rank(row for row, chart in zip(rows, charts)
                    if chart is not None and chart <= 7)


def rational_rank(rows):
    rr = [[Fraction(v) for v in row] for row in rows]
    rank = 0
    for col in range(8):
        hit = next((i for i in range(rank, len(rr)) if rr[i][col]), None)
        if hit is None:
            continue
        rr[rank], rr[hit] = rr[hit], rr[rank]
        p = rr[rank][col]
        rr[rank] = [v / p for v in rr[rank]]
        for i in range(rank + 1, len(rr)):
            q = rr[i][col]
            if q:
                rr[i] = [a - q*b for a, b in zip(rr[i], rr[rank])]
        rank += 1
    return rank


def exact_root(n, degree):
    lo, hi = 0, 1 << ((n.bit_length() + degree - 1) // degree)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**degree <= n:
            lo = mid
        else:
            hi = mid
    need(lo**degree <= n < (lo+1)**degree, "integer root enclosure")
    return lo


def interval(profile, scale):
    lower = upper = 0
    for rank, count in sorted(profile.items()):
        z = rank**199 * scale**200
        lo = exact_root(z, 200)
        hi = lo if lo**200 == z else lo+1
        lower += count * (lo if count >= 0 else hi)
        upper += count * (hi if count >= 0 else lo)
    return [lower, upper]


def census(w):
    dim = lambda f: w['frames'][str(f)]['dim']
    rows = [1 << i for i in range(w['public'])] + [0] * w['owned_fields']
    current = list(w['start']) + [None] * w['owned_fields']
    main_rows = [1 << i for i in range(222)]
    main_paid, core_paid, helpers = Counter(), Counter(), Counter()
    swaps = resets = 0
    main_configurations = 1
    min_gap = min(dim(f) for f in current[:111])-max(dim(f) for f in current[111:222])
    main_adds = 0
    for e in w['program']:
        op, a = e[:2]
        if op == 'ADD':
            b, frame = e[2:]
            need(current[a] == current[b] == frame, "source cochart ADD")
            rows[a] ^= rows[b]
            if a < 222 and b < 222:
                need(a < 111 and b < 111, "all original main-only ADDs stay on X")
                main_adds += 1
                main_rows[a] ^= main_rows[b]
        elif op == 'SWAP':
            b = e[2]
            need((a < 222) == (b < 222), "no cross-class SWAP")
            swaps += 1
            rows[a], rows[b] = rows[b], rows[a]
            current[a], current[b] = current[b], current[a]
            if a < 222:
                main_rows[a], main_rows[b] = main_rows[b], main_rows[a]
        elif op == 'MOVE':
            u, v = e[2:]
            need(current[a] == u, "source MOVE entrance")
            r = abs(dim(u)-dim(v))
            need(r > 0, "positive source MOVE")
            (main_paid if a < 222 else core_paid)[r] += 1
            current[a] = v
            if a < 222:
                main_configurations += 1
                gap=min(dim(f) for f in current[:111])-max(dim(f) for f in current[111:222])
                min_gap=min(min_gap,gap)
        elif op == 'INIT':
            need(a >= 222 and current[a] is None, "owned zero INIT")
            current[a] = e[2]
            rows[a] = 0
            resets += 1
        elif op == 'CLEAR':
            need(a >= 222 and current[a] == e[2], "owned CLEAR")
            current[a] = None
            rows[a] = 0
            resets += 1
        else:
            raise ValueError(op)
    need(current == list(w['final'])+[None]*w['owned_fields'], "all source final charts")
    for a in range(w['public']):
        wanted = (1 << a) ^ ((1 << (a-111)) if 111 <= a < 222 else 0)
        need(rows[a] == wanted, "source public endpoint")
    need(main_rows == [1 << i for i in range(222)], "main-only identity")
    need(all(dim(w['final'][i]) == 8 for i in range(111)), "all X high")
    need(all(dim(w['final'][111+i]) == 7 for i in range(111)), "all Y low")
    low_helpers = Counter(dim(w['final'][i]) for i in range(222, w['public']))
    need(low_helpers == {8:434,4:2,6:1}, "complete helper boundary census")
    for a in range(222, w['public']):
        helpers[abs(dim(w['start'][a])-dim(w['final'][a]))] += 1
    need(0 not in helpers, "positive helper targets")
    # Needed final body frames are rational independent codimension-one spaces.
    for frame in set(w['final'][:222]):
        f = w['frames'][str(frame)]
        need(rational_rank(f['B']) == f['dim'], "boundary B rank")
        need(rational_rank(f['A']) == 8-f['dim'], "boundary annihilator rank")
        need(all(sum(Fraction(x)*Fraction(y) for x,y in zip(a,b)) == 0
                 for a in f['A'] for b in f['B']), "boundary orthogonality")
    need(w['frames']['1']['B'] == [[int(i==j) for j in range(8)] for i in range(8)],
         "literal full chart")
    need(main_configurations == 755 and min_gap == 1 and main_adds == 628, "frozen trajectory separation")
    return main_paid, core_paid, helpers, dict(sorted(low_helpers.items())), swaps, resets, {
        'main_frame_configurations':main_configurations,
        'minimum_X_dimension_minus_maximum_Y_dimension':min_gap,
        'main_only_ADDs':main_adds,
        'all_main_only_ADDs_on_X':True,
        'scope':'All 34138 source cuts covered by 755 constant-main-frame intervals.'}


def lifted_cut(w, m):
    public = 222*m+437
    total = public+w['owned_fields']+1
    def owner(a, plane=0):
        return 222*plane+a if a < 222 else 222*m+a-222
    rows = [0]*total
    charts = [None]*total
    dim = lambda f: w['frames'][str(f)]['dim']
    for i in range(m):
        for j in range(222):
            a = owner(j,i)
            rows[a] = 1 << (111*i+j) if j < 111 else 0
            charts[a] = w['start'][j]
    for j in range(222,w['public']):
        charts[owner(j)] = w['start'][j]
    def emit(e):
        op,a = e[:2]
        if op == 'ADD':
            need(charts[a] == charts[e[2]] == e[3], "lift cochart ADD")
            rows[a] ^= rows[e[2]]
        elif op == 'SWAP':
            b=e[2]; rows[a],rows[b]=rows[b],rows[a]
            charts[a],charts[b]=charts[b],charts[a]
        elif op == 'MOVE':
            need(charts[a] == e[2], "lift MOVE entrance")
            charts[a] = e[3]
        elif op == 'INIT':
            need(charts[a] is None, "lift fresh INIT")
            rows[a]=0;charts[a]=e[2]
        elif op == 'CLEAR':
            need(charts[a] == e[2], "lift CLEAR entrance")
            rows[a]=0;charts[a]=None
        else:
            raise ValueError(op)
    for e in w['program']:
        op,a=e[:2]
        planes=range(m) if a < 222 else (0,)
        for i in planes:
            out=[op,owner(a,i),*e[2:]]
            if op in ('ADD','SWAP'):
                out[2]=owner(e[2],i if a < 222 and e[2] < 222 else 0)
            emit(out)
    dimensions=lambda: [dim(f) if f is not None else None for f in charts]
    for i in range(m):
        for j in range(111):
            need(rows[owner(j,i)] == 1 << (111*i+j), "lift unchanged X")
            need(rows[owner(111+j,i)] == 1 << j, "lift Y source projection")
    need(all(v == 0 for v in rows[222*m:]), "no hidden helper/scratch X leakage")
    entry_rank=cut_rank(rows,dimensions())
    need(entry_rank==111, "actual entry cut rank")
    temp=total-1
    downward=events=rank_gains=0
    for i in range(1,m):
        for j in range(111):
            xi,x1,y=owner(j,i),owner(j,0),owner(111+j,i)
            full,body=charts[xi],charts[y]
            need(dim(full)==8 and dim(body)==7 and charts[x1]==full, "repair chart boundary")
            for e in [['INIT',temp,full],['ADD',temp,xi,full],['ADD',temp,x1,full]]:
                emit(e);events+=1
            before=cut_rank(rows,dimensions())
            emit(['MOVE',temp,full,body]);events+=1;downward+=1
            after=cut_rank(rows,dimensions())
            need(after-before==1, "each repair crossing gives one new independent row")
            rank_gains += after-before
            emit(['ADD',y,temp,body]);emit(['CLEAR',temp,body]);events+=2
            need(cut_rank(rows,dimensions())==after, "repair retirement retains rank")
    final_rank=cut_rank(rows,dimensions())
    need(final_rank==111*m and downward==111*(m-1), "sharp source cut bound")
    for i in range(m):
        for j in range(111):
            need(rows[owner(111+j,i)]==1<<(111*i+j), "all corrected source directions")
    return {'m':m,'entry_cut_rank':entry_rank,'exit_cut_rank':final_rank,
            'repair_down_crossings':downward,'rank_gains':rank_gains,
            'rank_one_paid_moment':downward,'literal_repair_events':events}


def small_transition_checks():
    checks=0
    for rows in product(range(8),repeat=3):
        for high in product((False,True),repeat=3):
            dims=[8 if x else 7 for x in high]
            r=cut_rank(rows,dims)
            for a in range(3):
                rr=list(rows);dd=list(dims);dd[a]=15-dd[a]
                down=dims[a]==8
                need(cut_rank(rr,dd)-r<=int(down),'local MOVE rank increase')
                checks+=1
                rr=list(rows);rr[a]=0
                need(cut_rank(rr,dims)<=r,'local erasure')
                checks+=1
                for b in range(a):
                    rr=list(rows);dd=list(dims)
                    rr[a],rr[b]=rr[b],rr[a];dd[a],dd[b]=dd[b],dd[a]
                    need(cut_rank(rr,dd)==r,'field/chart SWAP')
                    checks+=1
                for b in range(3):
                    if a!=b and dims[a]==dims[b]:
                        rr=list(rows);rr[a]^=rr[b]
                        need(cut_rank(rr,dims)<=r,'cochart ADD rank')
                        checks+=1
            for d in (0,7,8,12):
                need(cut_rank([*rows,0],[*dims,d])==r,'zero INIT')
                checks+=1
    # Premise-breaking controls: the extra power must remain excluded/paid.
    need(cut_rank([1,0],[8,7])==0 and cut_rank([1,1],[8,7])==1,'free cross-chart ADD counterexample')
    need(cut_rank([0,1],[8,7])==1,'value-only cross-chart SWAP counterexample')
    need(cut_rank([1,1,0],[8,7,7])==1,'preloaded helper leakage')
    need(cut_rank([1,1,1],[8,7,7])==1,'leaked helper gives free output')
    return {'tiny_states':4096,'local_transition_checks':checks,
            'negative_controls':['free cross-chart ADD increases rank without MOVE',
                                 'value-only unequal-chart SWAP violates pairing premise',
                                 'X-dependent low-side helper increases entry rank'],
            'universal_proof':'PROOF.md Theorem 1, not finite extrapolation'}


def caller_census(path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == "3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e", "caller SHA256")
    need(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest() == "cf55f4271009a06ad192a070d330a4466b6d44fa", "caller Git blob")
    c = json.loads(raw)
    targets, paid, natives = Counter(), Counter(), Counter()
    for event in c['events']:
        if event[0] == 'J':
            natives[event[1]] += 2
        elif event[0] == 'A' and event[1] == 'QUERY':
            paid[1] += 111
        elif event[0] == 'A' and event[1] == 'IDLE_ONE':
            paid[7*len(event[3])] += 111
    need(natives == {j:2 for j in range(1,19)}, "36 native calls at 18 stages")
    for row in c['types']['A']['diagonal']:
        need(row[0] % 2 == 1 and all(v in (0,1) for v in row[2:]) and any(row[2:]), "nonempty BIT root target")
        targets[1+7*sum(row[2:])] += 111
    target_expected = Counter({127:222})
    paid_expected = Counter({1:444})
    for j in range(1,10): target_expected[1+7*j] += 444
    for j in range(1,9): paid_expected[7*j] += 444
    need(targets == target_expected and paid == paid_expected, "complete literal root invoice")
    return targets, paid


def run(word, caller):
    raw=word.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==NATIVE_SHA,'native SHA256')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==NATIVE_BLOB,'native Git blob')
    w=json.loads(gzip.decompress(raw))
    need((w['public'],w['owned_fields'],len(w['program']))==(659,237,34137),'source dimensions')
    main,core,helper,ends,swaps,resets,chronology=census(w)
    signed=Counter()
    for r in set(main)|set(core)|set(helper):
        signed[r] += 36*(helper[r]-main[r]-core[r])
    root_targets, root_paid = caller_census(caller)
    for r, count in root_targets.items(): signed[r] += count
    for r, count in root_paid.items(): signed[r] -= count
    delta=Counter({r:core[r]-helper[r] for r in set(core)|set(helper)})
    scale=10**30
    m2=interval(signed,scale);d=interval(delta,scale)
    need(m2[1]<-444*scale and d[1]<88*scale,'complete target moment bounds')
    need(m2[0]+18*d[0]>0,'omitted-repair false positive control')
    return {'status':'PASS_SELECTOR_BOUNDARY_REPAIR_FLOOR','source_base':SOURCE_BASE,
            'source_sha256':NATIVE_SHA,'source_git_blob':NATIVE_BLOB,
            'source_public_coefficients':659**2,'main_only_identity':True,'chronology':chronology,
            'helper_endpoint_dimensions':ends,'source_swaps':swaps,'owned_reset_events':resets,
            'main_paid':dict(sorted(main.items())),'core_paid':dict(sorted(core.items())),
            'helper_targets':dict(sorted(helper.items())),
            'root_targets':dict(sorted(root_targets.items())),
            'root_paid':dict(sorted(root_paid.items())),
            'finite_lifts':[lifted_cut(w,m) for m in (2,4,6)],
            'exact_moments':{'scale':str(scale),'M2':list(map(str,m2)),
                             'D':list(map(str,d)),'M2_upper':'-444','D_upper':'88',
                             'unrepaired_m2_positive':True},
            'small_checks':small_transition_checks(),
            'all_m_theorem':'paid repair >= 111*(m-1) for all integers m>=2 and all real t>0',
            'rank_limited_q_core_bound':'M(m,q)<-222*m-414*(m-q) for even m>=2 and 1<=q<=m',
            'scope':'Normalized linear boundary correction grammar; no changed-prefix or universal shared-core exclusion.',
            'new_kappa':None}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--word',type=Path,required=True)
    parser.add_argument('--caller',type=Path,required=True)
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args()
    result=run(args.word,args.caller)
    if args.expected:
        need(json.loads(json.dumps(result))==json.loads(args.expected.read_text()),'frozen receipt mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
