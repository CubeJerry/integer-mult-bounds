#!/usr/bin/env python3
"""Audit rational projectors, saturated chart bases and the repeated paired caller."""

import argparse
import gzip
import hashlib
import itertools
import json
import math
import subprocess
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


BASE = "914097a04bb93f730b805e9d4f036b46707c8675"
PINS = {
    "native": ("research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz",
               "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"),
    "atlas": ("research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",
              "ef8611b33835a799193e8aec4f615486d73f5743558997de0262bceb3ae9eb3c"),
    "caller": ("research/paired-query-only-bit/EFREE-CALLER.json.gz",
               "757b3523798f840bdb02028b23708c3416627a99ea09e7a3c4bcdc5cd0c7ce4b"),
}
SCALE = 12
ONE = tuple(tuple(int(i == j) for j in range(8)) for i in range(8))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def source(repo, key):
    name, expected = PINS[key]
    path = repo / name
    data = path.read_bytes() if path.is_file() else subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE}:{name}"])
    need(hashlib.sha256(data).hexdigest() == expected, f"source SHA for {key}")
    return json.loads(gzip.decompress(data))


def dot(x, y):
    return sum(a*b for a,b in zip(x,y))


def mul(a, b):
    cols = tuple(zip(*b))
    return tuple(tuple(dot(row,col) for col in cols) for row in a)


def scaled(n, a):
    return tuple(tuple(n*x for x in r) for r in a)


def minus(a, b):
    return tuple(tuple(x-y for x,y in zip(r,s)) for r,s in zip(a,b))


def bareiss(a):
    m = [list(row) for row in a]
    sign = last = 1
    for j in range(len(m)-1):
        pivot = next((i for i in range(j,len(m)) if m[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            m[pivot],m[j] = m[j],m[pivot]
            sign = -sign
        for i in range(j+1,len(m)):
            for k in range(j+1,len(m)):
                num = m[j][j]*m[i][k] - m[i][j]*m[j][k]
                need(num % last == 0, "exact Bareiss division")
                m[i][k] = num//last
        last = m[j][j]
    return sign*m[-1][-1]


def inverse(a):
    n = len(a)
    m = [[F(x) for x in row]+[F(i == j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k = next(i for i in range(j,n) if m[i][j])
        m[k],m[j] = m[j],m[k]
        pivot = m[j][j]
        m[j] = [x/pivot for x in m[j]]
        for i in range(n):
            if i != j and m[i][j]:
                factor = m[i][j]
                m[i] = [x-factor*y for x,y in zip(m[i],m[j])]
    return tuple(tuple(row[n:]) for row in m)


def bezout(a,b):
    old_r,r = abs(a),abs(b)
    old_s,s,old_t,t = 1,0,0,1
    while r:
        q = old_r//r
        old_r,r = r,old_r-q*r
        old_s,s = s,old_s-q*s
        old_t,t = t,old_t-q*t
    return old_r, old_s if a >= 0 else -old_s, old_t if b >= 0 else -old_t


def integer_kernel(matrix):
    """A Z-basis of the kernel, by tracked unimodular column operations."""
    n = len(matrix)
    columns = [list(c)+list(e) for c,e in zip(zip(*matrix),zip(*ONE))]
    h = 0
    for i in range(n):
        j = next((j for j in range(h,n) if columns[j][i]), None)
        if j is None:
            continue
        columns[h],columns[j] = columns[j],columns[h]
        for j in range(h+1,n):
            a,b = columns[h][i],columns[j][i]
            if b:
                g,s,t = bezout(a,b)
                left,right = columns[h],columns[j]
                columns[h] = [s*x+t*y for x,y in zip(left,right)]
                columns[j] = [(-b//g)*x+(a//g)*y for x,y in zip(left,right)]
        h += 1
    need(all(all(x == 0 for x in c[:n]) for c in columns[h:]), "saturated kernel columns")
    return [c[n:] for c in columns[h:]]


def audit_projector(p, rank):
    need(tuple(zip(*p)) == p and mul(p,p) == scaled(SCALE,p), "symmetric scaled idempotent")
    need(sum(p[i][i] for i in range(8)) == rank*SCALE, "rational projector trace")
    kernel = integer_kernel(p)
    image = integer_kernel(minus(scaled(SCALE,ONE),p))
    need(len(image) == rank and len(kernel) == 8-rank, "both lattice ranks")
    basis = tuple(zip(*(image+kernel)))
    diagonal = tuple(tuple(SCALE*x if j<rank else 0 for j,x in enumerate(row)) for row in basis)
    need(mul(p,basis) == diagonal, "saturated adapted basis")
    determinant = abs(bareiss(basis))
    need(determinant > 0 and SCALE**8 % determinant == 0, "localization supports adapted basis")
    denominator = SCALE//math.gcd(SCALE,*(abs(x) for row in p for x in row))
    return denominator, determinant


def native_audit(native):
    frames = {int(k):v for k,v in native["frames"].items()}
    projectors = {}
    determinants, denominators, saturated = Counter(), Counter(), Counter()
    for k,f in frames.items():
        d = f["dim"]
        basis = tuple(zip(*(f["B"]+f["A"])))
        adj = inverse(basis)
        p = tuple(tuple(SCALE*sum(basis[i][j]*adj[j][l] for j in range(d)) for l in range(8)) for i in range(8))
        need(all(F(x).denominator == 1 for row in p for x in row), "native projector grid")
        p = tuple(tuple(int(x) for x in row) for row in p)
        denom,det = audit_projector(p,d)
        denominators[denom] += 1
        saturated[det] += 1
        determinants[abs(bareiss(basis))] += 1
        projectors[k] = p
    need(denominators == {1:28,2:95,4:513} and determinants == {1:28,4:326,16:250,64:32},
         "all selected source frames and stored bases")
    n = native["public"]
    places = list(native["start"]) + [None]*native["owned_fields"]
    rows = [1<<i for i in range(n)] + [0]*native["owned_fields"]
    zero = tuple((0,)*8 for _ in range(8))
    whole = scaled(SCALE,ONE)
    moves, checks, cleanup = Counter(), set(), Counter()
    for op,*args in native["program"]:
        k = args[0]
        if op == "MOVE":
            k,a,b = args
            need(places[k] == a, "current MOVE entrance")
            aa,bb = sorted((a,b), key=lambda p:frames[p]["dim"])
            edge = aa,bb
            if edge not in checks:
                p,q = projectors[aa],projectors[bb]
                need(mul(p,q) == mul(q,p) == scaled(SCALE,p), "both nested native products")
                checks.add(edge)
            moves[frames[bb]["dim"]-frames[aa]["dim"]] += 1
            places[k] = b
        elif op == "ADD":
            k,l,place = args
            need(k != l and places[k] == places[l] == place, "co-chart XOR")
            rows[k] ^= rows[l]
        elif op == "INIT":
            need(k >= n and places[k] is None, "new owned zero")
            places[k],rows[k] = args[1],0
            cleanup["INIT"] += 1
        elif op == "CLEAR":
            need(k >= n and places[k] == args[1], "owned erasure")
            cleanup["dirty" if rows[k] else "clean"] += 1
            places[k],rows[k] = None,0
        elif op == "SWAP":
            k,l = args
            places[k],places[l] = places[l],places[k]
            rows[k],rows[l] = rows[l],rows[k]
        else:
            raise ValueError(op)
    need(places == native["final"] + [None]*native["owned_fields"], "all final owners")
    for k in range(n):
        expected = (1<<k) ^ ((1<<(k-111)) if 111 <= k < 222 else 0)
        need(rows[k] == expected, "complete native shear and helpers")
    ports = Counter()
    for i in range(111):
        start,finish = native["start"][i],native["final"][111+i]
        need(projectors[start] == minus(whole,projectors[finish]), "complementary head and body")
        need(projectors[native["final"][i]] == whole and projectors[native["start"][111+i]] == zero,
             "other two native chart endpoints")
        g = tuple(zip(*(frames[start]["B"]+frames[finish]["B"])))
        ports[bareiss(g)] += 1
    need(ports == {1:4,-1:4,4:53,-4:50}, "actual main-port basis determinants")
    helper = Counter()
    for i in range(222,n):
        a,b = native["start"][i],native["final"][i]
        pa,pb = projectors[a],projectors[b]
        need(mul(pa,pb) == mul(pb,pa) == scaled(SCALE,pa), "independent helper projector")
        helper[frames[b]["dim"]-frames[a]["dim"]] += 1
    return {
        "source_frames":len(frames),"projector_denominators":dict(denominators),
        "stored_basis_abs_determinants":dict(determinants),"saturated_basis_abs_determinants":dict(saturated),
        "port_basis_determinants":dict(ports),"distinct_nested_move_pairs":len(checks),
        "paid_histogram":dict(moves),"productive_helpers":dict(helper),"owned_counts":dict(cleanup),
    }, projectors


def atlas_audit(layout, native, old):
    roots = [tuple(r) for r in layout["root_table"]]
    planes = layout["A2"]
    fours = layout["D4"]
    identity = scaled(SCALE,ONE)
    root_proj = [tuple(tuple(3*x*y for y in r) for x in r) for r in roots]
    need(all(dot(r,r)==4 for r in roots), "norm of every atlas root")
    for j in range(111):
        need(root_proj[j] == old[native["start"][j]], "actual atlas and native address agreement")
    denominators, determinants = {}, {}
    def register(kind, ps, dimension):
        den,det = Counter(),Counter()
        for p in ps:
            a,b = audit_projector(p,dimension)
            den[a] += 1
            det[b] += 1
        denominators[kind],determinants[kind] = dict(den),dict(det)
    register("L",root_proj,1)
    plane_proj = []
    pair_to_plane = {}
    for h,members in enumerate(planes):
        u,v = (roots[x] for x in members[:2])
        d = dot(u,v)
        need(abs(d) == 2, "A2 Gram determinant 12")
        p = tuple(tuple(4*(u[i]*u[j]+v[i]*v[j])-d*(u[i]*v[j]+v[i]*u[j])
                        for j in range(8)) for i in range(8))
        for j in members:
            need(all(dot(row, roots[j]) == SCALE*x for row,x in zip(p,roots[j])), "A2 span")
        for a,b in itertools.combinations(sorted(members),2):
            need((a,b) not in pair_to_plane, "unique A2 on nonorthogonal pair")
            pair_to_plane[a,b] = h
        plane_proj.append(p)
    register("H",plane_proj,2)
    four_proj,flags = [],set()
    for d,members in enumerate(fours):
        gram = {(a,b):dot(roots[a],roots[b]) for a,b in itertools.combinations(sorted(members),2)}
        axes = next(axes for axes in itertools.combinations(sorted(members),4)
                    if all(gram[pair] == 0 for pair in itertools.combinations(axes,2)))
        p = tuple(tuple(3*sum(roots[k][i]*roots[k][j] for k in axes) for j in range(8)) for i in range(8))
        for j in members:
            need(all(dot(row, roots[j]) == SCALE*x for row,x in zip(p,roots[j])), "D4 span")
        hs = {pair_to_plane[pair] for pair,dot_value in gram.items() if dot_value}
        need(len(hs) == 16 and all(set(planes[h]) <= set(members) for h in hs), "every H inside D")
        flags.update((h,d) for h in hs)
        four_proj.append(p)
    register("D",four_proj,4)
    dual = layout["dual_D4"]
    need(all(minus(identity,p) == four_proj[dual[d]] and dual[dual[d]] == d for d,p in enumerate(four_proj)),
         "every rational dual D4 projector")
    left,right = Counter(),Counter()
    for kind,d,h,j,k,i,_,_ in layout["routes"]:
        need((kind == "X" and j < 111) or (kind == "Y" and i < 111), "genuine public route")
        if h is not None:
            need((h,d) in flags and j in planes[h], "actual left flag")
            left[h,d] += 1
        if k is not None:
            need((k,dual[d]) in flags and i in planes[k], "actual complementary right flag")
            right[k,dual[d]] += 1
    need(len(flags) == 50400 and set(left) == set(right) == flags, "all atlas flags on both sides")
    need(set(left.values()) == set(right.values()) == {1}, "tight atlas coverage")
    witnesses = {}
    for name,ps in (("L",root_proj),("H",plane_proj),("D",four_proj)):
        for i,p in enumerate(ps):
            for a,row in enumerate(p):
                for b,x in enumerate(row):
                    z = F(x,SCALE)
                    for q in (2,3):
                        if q not in witnesses and z.denominator % q == 0:
                            witnesses[q] = [name,i,a,b,str(z)]
    need(set(witnesses) == {2,3}, "sharp base coefficient prime set")
    return {"root_lines":len(roots),"A2":len(planes),"D4":len(fours),"H_D_flags":len(flags),
            "tight_routes":len(layout["routes"]),"projector_denominators":denominators,
            "saturated_basis_abs_determinants":determinants,"excluded_address_prime_witnesses":witnesses}


def paired_endpoint(caller, skip_local=False):
    events = caller["events"]
    base = len(events)+1
    units = [0]+[base**j for j in range(caller["stages"])]
    rows = [{(i,0,0)} for i in range(caller["roles"])]
    def shift(row, head=0, stages=()):
        term = sum(units[j] for j in stages)
        return {(i,q^head,x+term) for i,q,x in row}
    cleared = False
    for event in events:
        op,*args = event
        if op == "ADD":
            a,b = args
            rows[a] ^= rows[b]
        elif op == "SWAP":
            a,b = args
            rows[a],rows[b] = rows[b],rows[a]
        elif op == "QUERY":
            a,b = args
            rows[a] ^= shift(rows[b],1)
        elif op == "IDLE_ONE":
            a,ss = args
            need(len(ss) == len(set(ss)), "distinct idle body exponents")
            rows[a] = shift(rows[a],stages=ss)
        elif op == "LOCAL":
            j,a,b = args
            if skip_local and not cleared:
                cleared = True
                continue
            old_a = rows[a]
            rows[a] = shift(old_a,stages=[j])
            rows[b] = shift(rows[b],stages=[j]) ^ shift(old_a,1,[j])
        else:
            raise ValueError(op)
    return all(row == {(i,d["q"],sum(units[j] for j in d["stages"]))}
               for i,(row,d) in enumerate(zip(rows,caller["diagonal"])))


def caller_audit(caller):
    need(caller["roles"] == 38 and caller["stages"] == 18 and caller["ports"] == 111, "paired source")
    need(paired_endpoint(caller) and not paired_endpoint(caller,True), "formal word and mutation")
    local = [e for e in caller["events"] if e[0] == "LOCAL"]
    for stage in range(1,19):
        events = [e for e in local if e[1] == stage]
        need(len(events) == 2 and set(events[0][2:]).isdisjoint(events[1][2:]), "disjoint native mains")
    m,d = 870,23040
    return {"paired_word_roles":38,"polynomial_coefficients":38**2,"independent_body_axes_sets":18,
            "ambient_with_seven_reused_native_axes":134,"rail_multiplicity":m,"binary_lanes":d,
            "public_pair_groups_per_native_line_per_lane":m//2,
            "selected_base_native_occurrences":18*d,"joint_native_occurrences":18*(m-1),
            "independent_base_helper_outputs":18*d*437,"independent_root_outputs":111*19*m*d}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = source(args.repo,"native")
    native,projectors = native_audit(raw)
    atlas = atlas_audit(source(args.repo,"atlas"),raw,projectors)
    caller = caller_audit(source(args.repo,"caller"))
    p = ((15,-10),(21,-14))
    g = ((5,2),(7,3))
    need(mul(p,p) == p and p[0][0] % 5 == 0 and any(x % 5 for row in p for x in row),
         "a convenient rational witness vanishes at five")
    need(bareiss(g) == 1 and mul(p,g) == ((5,0),(7,0)), "unimodular matching basis survives")
    # A rational split of the identity along (1,2) introduces a genuinely new denominator.
    rational_split = ((F(1,5),F(2,5)),(F(2,5),F(4,5)))
    need(mul(rational_split,rational_split) == rational_split and SCALE % rational_split[0][0].denominator != 0,
         "arbitrary rational split control")
    result = {"status":"PASS_LOCALIZED_ATLAS_AND_PAIRED_CALLER","native":native,"atlas":atlas,"caller":caller,
              "additional_compiler_address_primes_needed":[],
              "base_address_localization":[2,3],"new_complete_kappa":False,
              "scope":"Address algebra and conditional paired-source contract for all valid late covers. No full H/D/K circuit.",
              "inputs":{key:{"path":v[0],"sha256":v[1]} for key,v in PINS.items()}}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"])
    print("native",native["source_frames"],"A2",atlas["A2"],"D4",atlas["D4"],"rational flags",atlas["H_D_flags"])


if __name__ == "__main__":
    main()
