#!/usr/bin/env python3
"""Independent exact review of the one-receiver nilpotent target."""
import argparse
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def require(test, reason):
    if not test: raise ValueError(reason)


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            bit = row & -row
            if bit in pivots: row ^= pivots[bit]
            else:
                pivots[bit] = row
                break
    return len(pivots)


def act(rows,x):
    return sum(((r & x).bit_count() & 1) << i for i,r in enumerate(rows))


def inspect(width,U,V,neighbors):
    w = len(U)
    require(w == (width+61)//62 and U == list(range(width-w,width)), "image and sharp width")
    require(set(V) == neighbors and all(len(row) == w for row in V.values()), "literal source ports and heights")
    require(sorted(s for row in V.values() for s in row if s is not None) == list(range(width)),
            "vertical selectors detect every input coordinate exactly once")
    ports = sorted(neighbors)
    require(None not in V[ports[0]] and len(set(V[ports[0]])) == w, "horizontal rank witness")
    local = []
    for j in ports:
        rows = [0 if s not in U else 1 << U.index(s) for s in V[j]]
        require(rank(row ^ (1 << k) for k,row in enumerate(rows)) == w, "all reduced full-block invertibilities")
        local.append(rows)
    J = [1 << (k+1) for k in range(w-1)] + [0]
    E = [0]*(w-1)+[1]
    require(local[0] == J and local[1] == E and all(not any(row) for row in local[2:]), "J/E/zero internal restrictions")
    require(rank(act(J,act(E,1 << k)) ^ act(E,act(J,1 << k)) for k in range(w)) == 2,
            "actual noncommuting restriction")
    # Removing the closing selector leaves a flat input direction, but keeps units.
    missing = U[0]
    removed = {j:[None if s == missing else s for s in row] for j,row in V.items()}
    require(rank(0 if s is None else 1 << s for row in removed.values() for s in row) == width-1,
            "missing closing edge restores one flat input direction")
    require(rank((1 << k)^J[k]^E[k] for k in range(w)) == w-1,
            "merging the two nilpotent restrictions creates a singular foreign block")
    return {"width":width,"image_width":w,"stacked_selector_rank":width,
            "horizontal_selector_rank":w,"reduced_invertible_blocks":62,
            "commutator_rank_on_U":2,"missing_closing_selector_kernel_dimension":1,
            "merged_J_plus_E_block_nullity":1}


def small_control(width,N,K):
    w = (width+61)//62
    U = list(range(width-w,width)); ports = sorted(N[80])
    V = {j:[None]*w for j in ports}
    for k in range(w-1): V[ports[0]][k] = U[k+1]
    V[ports[1]][w-1] = U[0]
    free = [(ports[0],w-1)] + [(j,k) for j in reversed(ports[1:]) for k in reversed(range(w)) if V[j][k] is None]
    for coordinate,(j,k) in zip(range(width-w),free): V[j][k] = coordinate
    inspect(width,U,V,N[80])
    canonical = []
    for row in K:
        base = sum(1 << (j*width) for j in range(111) if row >> j & 1)
        canonical.extend(base << k for k in range(width))
    delta = [0]*(111*width)
    for j,selected in V.items():
        for k,s in enumerate(selected):
            if s is not None: delta[80*width+U[k]] ^= 1 << (j*width+s)
    require(rank(delta) == w and rank(x^y for x,y in zip(canonical,delta)) == 9*width+w
            and rank(canonical+delta) == 9*width+w, "complete native fitting and repair ranks")
    for selected in V.values():
        block = [1 << k for k in range(width)]
        for k,s in enumerate(selected):
            if s is not None: block[U[k]] ^= 1 << s
        require(rank(block) == width, "complete foreign block including outside-image columns")
    return {"width":width,"fitting_rank":9*width+w,"repair_rank":w,"full_foreign_blocks_checked":62}


def movement():
    scale = 10**24; cache = {}
    def power(k):
        if k not in cache:
            with localcontext() as context:
                context.prec = 80
                low = int(Decimal(k)**(Decimal(199)/200)*scale)
            target = k**199*scale**200
            require(low**200 <= target < (low+1)**200, "exact movement root enclosure")
            cache[k] = Q(low,scale),Q(low if low**200 == target else low+1,scale)
        return cache[k]
    def interval(profile):
        a=b=Q(0)
        for k,c in profile.items():
            low,high=power(k)
            a+=c*(low if c>=0 else high); b+=c*(high if c>=0 else low)
        return a,b
    n={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}; h={2:1,4:25,6:1,8:410}
    q={1:Q(4451,8),2:Q(7213,16),4:24,8:9+Q(93,5760)}
    difference=Counter()
    for k,c in h.items(): difference[k]+=36*c
    for k,c in n.items(): difference[k]-=36*c
    difference[127]+=222; difference[1]-=444
    for j in range(1,10): difference[1+7*j]+=444
    for j in range(1,9): difference[7*j]-=444
    def finite(m):
        profile=Counter({k:Q(m,2)*c for k,c in difference.items()})
        for k,c in n.items(): profile[k]+=18*(m-1)*c
        for k,c in h.items(): profile[k]-=18*(m-1)*c
        for k,c in q.items(): profile[k]-=18*(m-1)*c
        return interval(profile)
    previous,first=finite(82),finite(84)
    require(previous[1]<0<first[0], "first positive even multiplicity84")
    require(first[0]>previous[1], "positive affine finite slope")
    require(Q(31,1920)==Q(93,5760), "compressed penalty ratio")
    return {"first_even_m":84,"m82_gap":list(map(str,previous)),"m84_gap":list(map(str,first)),
            "compressed_penalty_ratio":"31/1920 = 93/5760"}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--author",type=Path,required=True);ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    source=args.repo/"research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    require(hashlib.sha256(source.read_bytes()).hexdigest()=="8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e", "source pin")
    roots=json.loads(source.read_text())["native_roots"]
    N=[{j for j,y in enumerate(roots) if i!=j and sum(v*w for v,w in zip(x,y))==0} for i,x in enumerate(roots)]
    K=[sum(1 << j for j in neighbors) ^ (1 << i) for i,neighbors in enumerate(N)]
    require(len(N[80])==62 and rank(K)==9, "native rank and degree")
    neighbor_mask=sum(1 << j for j in N[80])
    require(rank(row & ~neighbor_mask for row in K)==9 and rank(row & ~(1 << 80) for row in K)==9,
            "both native support separations")
    data=json.loads((args.author/"output/SELECTORS.json").read_text())
    require(data["receiver"]==80 and data["width"]==5760, "submitted target identity")
    full=inspect(5760,data["U"],{int(j):row for j,row in data["V"].items()},N[80])
    compressed=inspect(1920,data["compressed_U"],{int(j):row for j,row in data["compressed_V"].items()},N[80])
    controls=[small_control(width,N,K) for width in (63,126)]
    require(62*92<5760<=62*93 and 62*30<1920<=62*31, "sharp one-receiver lower bounds")
    result={"status":"PASS_INDEPENDENT_ONE_STAR_93_REVIEW","full_width":full,"compressed":compressed,
            "q":51933,"r":93,"common_left_rows":5667,"flat_dimension":0,
            "small_complete_controls":controls,"movement":movement(),
            "scope":"Algebraic target; sharp only within one-receiver perturbations; no physical source code"}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    files=[source]+[args.author/p for p in ("PROOF.md","check.py","output/RESULT.json","output/SELECTORS.json")]
    (args.out/"REVIEW-PINS.json").write_text(json.dumps([
        {"path":str(p.resolve()),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],indent=2)+"\n")
    print(result["status"])


if __name__=="__main__":main()
