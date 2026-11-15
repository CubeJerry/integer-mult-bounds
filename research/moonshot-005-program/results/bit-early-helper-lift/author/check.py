#!/usr/bin/env python3
"""Independent exact checks for the meet-funnel/early-lift bridge."""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


def binary_basis(rows):
    out = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in out:
                x ^= out[p]
            else:
                out[p] = x
                break
    return out


def reduce_binary(x, basis):
    for p in sorted(basis, reverse=True):
        if (x >> p) & 1:
            x ^= basis[p]
    return x


def solve(rows, target):
    base = {}
    for j, x in enumerate(rows):
        word = 1 << j
        while x:
            p = x.bit_length() - 1
            if p in base:
                x ^= base[p][0]
                word ^= base[p][1]
            else:
                base[p] = (x, word)
                break
    word = 0
    while target:
        p = target.bit_length() - 1
        if p not in base:
            return None
        target ^= base[p][0]
        word ^= base[p][1]
    return word


def xor_selected(rows, mask):
    out = 0
    for j, row in enumerate(rows):
        if (mask >> j) & 1:
            out ^= row
    return out


def rational_rank(rows):
    basis = {}
    for row in rows:
        x = list(map(Fraction, row))
        for p, b in basis.items():
            a = x[p]
            if a:
                x = [v-a*w for v,w in zip(x,b)]
        p = next((j for j,v in enumerate(x) if v), None)
        if p is not None:
            a = x[p]
            basis[p] = [v/a for v in x]
    return len(basis)


def subspaces(n):
    """Enumerate via span sets, independently of any author's quotient code."""
    seen = {frozenset([0])}
    frontier = list(seen)
    while frontier:
        space = frontier.pop()
        for x in range(1, 1 << n):
            if x in space:
                continue
            new = space | frozenset(y ^ x for y in space)
            if new not in seen:
                seen.add(new)
                frontier.append(new)
    return seen


def early_lift_controls():
    cases = 0
    wrong_hub_rejected = 0
    for h,d in [(1,2),(2,2),(1,3)]:
        dmask = (1 << d)-1
        for space in subspaces(h+d):
            K = list(binary_basis(space).values())
            c = len(K)
            proj = list(binary_basis(x & dmask for x in K).values())
            p = len(proj)
            lift = []
            for v in proj:
                witness = solve([x & dmask for x in K], v)
                lift.append(xor_selected(K,witness))
            kernel = list(binary_basis(x for x in space if not (x & dmask)).values())
            active = [1 << j for j in range(d) if any(v & (1 << j) for v in proj)]
            E = []
            span = proj.copy()
            for e in active:
                if solve(span,e) is None:
                    E.append(e)
                    span.append(e)
            delta = len(E)
            assert delta == len(active)-p
            # Every possible helper Hub part in these bounded test spaces.
            for hparts in itertools.product(range(1 << h), repeat=delta):
                Q = [e | (hp << d) for e,hp in zip(E,hparts)]
                arrival, canonical, wrong = Q.copy(), kernel.copy(), kernel.copy()
                for b in active:
                    if b in E:
                        continue
                    w = solve(proj+E,b)
                    pp = xor_selected(proj, w & ((1 << p)-1))
                    ee = w >> p
                    ll = xor_selected(lift, w & ((1 << p)-1))
                    qq = xor_selected(Q,ee)
                    seeded = (ll & ~dmask) ^ (qq & ~dmask)
                    value = seeded ^ b
                    corrected = value ^ qq
                    assert (corrected & dmask) == pp
                    assert corrected in space
                    canonical.append(corrected)
                    arrival.append(value)
                    wrong.append((ll & ~dmask) ^ b ^ qq)
                arrival += kernel
                assert len(binary_basis(canonical)) == c
                assert all(solve(canonical,row) is not None for row in K)
                assert len(binary_basis(arrival)) == c+delta
                if any(row not in space for row in wrong):
                    wrong_hub_rejected += 1
                cases += 1
    assert wrong_hub_rejected > 0
    return {"exact_binary_lift_cases":cases,
            "ignoring_real_helper_Hub_part_rejected":wrong_hub_rejected}


SCALE = 10**30


def power_interval(r):
    if r == 0:
        return Fraction(0), Fraction(0)
    with localcontext() as ctx:
        ctx.prec = 90
        a = int((Decimal(r) ** (Decimal(199)/200))*SCALE)
    N = pow(r,199)*pow(SCALE,200)
    while pow(a,200) > N:
        a -= 1
    while pow(a+1,200) <= N:
        a += 1
    assert pow(a,200) <= N < pow(a+1,200)
    if pow(a,200) == N:
        return Fraction(a,SCALE),Fraction(a,SCALE)
    return Fraction(a,SCALE),Fraction(a+1,SCALE)


def interval(profile):
    lo=hi=Fraction(0)
    for r,coef in profile.items():
        a,b=power_interval(r)
        lo += coef*(a if coef >= 0 else b)
        hi += coef*(b if coef >= 0 else a)
    return lo,hi


def report_interval(bounds):
    with localcontext() as ctx:
        ctx.prec=45
        return {"lower":str(Decimal(bounds[0].numerator)/Decimal(bounds[0].denominator)),
                "upper":str(Decimal(bounds[1].numerator)/Decimal(bounds[1].denominator)),
                "exact_bounds":[str(z) for z in bounds]}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    source=args.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    raw=source.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(raw)['native_roots']
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    K=[sum(1 << j for j in range(111) if i==j or dot(roots[i],roots[j])==0) for i in range(111)]
    canon=list(binary_basis(K).values())
    assert len(canon)==9
    results=[]
    configs=[([0,3,76,80],{0:3,3:14,76:60,80:59}),
             ([1,3,73,76,77,80],{1:3,3:1,73:76,76:73,77:80,80:77})]
    for I,pivots in configs:
        classes={}
        for j,row in enumerate(roots):
            S=tuple(i for i in I if dot(roots[i],row)==0)
            classes.setdefault(S,[]).append(j)
        r=rational_rank([roots[i] for i in I])
        mix=[S for S in classes if len(S)>1]
        private={i:sum(1 << j for j in classes.get((i,),[])) for i in I}
        for i,j in pivots.items():
            assert j in classes[(i,)]
        held=list(pivots.values())
        p=len(binary_basis(sum(((row >> j)&1) << t for t,j in enumerate(held)) for row in K))
        profile=Counter()
        profile[7]+=len(classes.get((),[]))
        for S,J in classes.items():
            if len(S)==1:
                profile[6]+=len(J);profile[1]+=len(J)
            elif len(S)>1:
                rs=rational_rank([roots[i]for i in S])
                profile[7-rs]+=len(J);profile[rs]+=len(J);profile[r-rs]+=1
        profile[7]+=111-len(I)+p
        profile[8-r]+=len(I);profile[r-1]+=len(I)
        profile[8]+=9-p;profile[1]+=len(pivots)
        profile.pop(0,None)
        cache=[sum(1 << j for j in classes[S])for S in mix]
        valid=[]
        for mask in range(1 << len(mix)):
            retained=[cache[j]for j in range(len(mix))if mask >> j & 1]
            if all(solve(canon+retained+[private[i]],1 << i) is not None for i in I):
                valid.append(mask)
        minimum=min(mask.bit_count()for mask in valid)
        result={"receivers":I,"chart_normal_rank":r,"pivot_rank":p,
                "Delta":len(pivots)-p,"movement_profile":dict(sorted(profile.items())),
                "movement_interval":report_interval(interval(profile)),
                "mixed_classes":[{"receivers":S,"roots":classes[S]}for S in mix],
                "minimum_cache_subset":minimum,
                "minimum_cache_subsets":[[mix[j]for j in range(len(mix))if mask >> j & 1]for mask in valid if mask.bit_count()==minimum]}
        if len(I)==6:
            triangles=[S for S in mix if len(S)==3]
            relation=0
            for S in triangles:
                relation ^= sum(1 << j for j in classes[S])
            assert relation==K[1]^K[3]==K[73]^K[76]==K[77]^K[80]
            assert relation.bit_count()==58
            assert minimum==7
            # Negative control: wrong canonical relation is not accepted.
            assert relation != K[1]^K[73]
            saved={1:1,5:16,2:16,7:-16}
            reduced=profile.copy()
            for a,z in saved.items():
                reduced[a]-=z
            result['triangle_relation_support']=58
            result['saving_size16_triangle']=report_interval(interval(saved))
            result['quotient_reduced_profile']=dict(sorted(reduced.items()))
            result['quotient_reduced_movement']=report_interval(interval(reduced))
        else:
            assert minimum==5
        results.append(result)
    I=list(range(111))
    classes={}
    for j,row in enumerate(roots):
        S=tuple(i for i in I if dot(roots[i],row)==0)
        classes.setdefault(S,[]).append(j)
        assert rational_rank([roots[i]for i in S])==7
    assert len(classes)==111 and all(len(J)==1 and len(S)>1 for S,J in classes.items())
    assert rational_rank(roots)==8
    b=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
    for j in range(1,9):
        b[1+7*j]+=Fraction(74,6);b[7*j]-=Fraction(74,6)
    B=interval(b)
    floor=interval({7:222,1:111})
    assert floor[0]>B[1]
    result={"status":"PASS_FUNNEL_BRIDGE","source_sha256":hashlib.sha256(raw).hexdigest(),
            "early_lift":early_lift_controls(),"native_cases":results,
            "full_native":{"classes":111,"source_intersection_dimension":1,"meet_dimension":0,
                           "generous_flat_floor":report_interval(floor),"limiting_allowance":report_interval(B),
                           "strict_deficit":report_interval((floor[0]-B[1],floor[1]-B[0]))},
            "scope":"Exact finite native identities and binary controls plus written universal proof; no full supplier or new kappa"}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status":result['status'],"early_lift":result['early_lift'],
                      "flat_deficit":result['full_native']['strict_deficit']['lower']}))


if __name__=='__main__':
    main()
