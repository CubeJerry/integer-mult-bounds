#!/usr/bin/env python3
"""Independent geometry, field, holder and literal-word review.

No author implementation is imported. The submitted certificates are checked
against exact root incidence; GF(32) uses carryless multiplication followed by
polynomial long division; actual holder permutations are compiled and replayed.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path


def require(test, reason):
    if not test:
        raise ValueError(reason)


def product(a, b):
    polynomial = 0
    for i in range(5):
        if b >> i & 1:
            polynomial ^= a << i
    while polynomial.bit_length() > 5:
        polynomial ^= 0b100101 << (polynomial.bit_length()-6)
    return polynomial


TIMES = [[product(a,b) for b in range(32)] for a in range(32)]
INVERSE = {a:next(b for b in range(1,32) if TIMES[a][b] == 1) for a in range(1,32)}


def power(a, n):
    answer = 1
    for _ in range(n):
        answer = TIMES[answer][a]
    return answer


def rank(matrix):
    pivots = {}
    for row in matrix:
        row = list(row)
        for column in range(len(row)):
            if row[column] == 0:
                continue
            if column in pivots:
                scalar = row[column]
                row = [x ^ TIMES[scalar][y] for x,y in zip(row,pivots[column])]
            else:
                inverse = INVERSE[row[column]]
                pivots[column] = [TIMES[inverse][x] for x in row]
                break
    return len(pivots)


def binary(matrix):
    rows = []
    for coefficients in matrix:
        for output_bit in range(5):
            row = 0
            for column, coefficient in enumerate(coefficients):
                for input_bit in range(5):
                    if TIMES[coefficient][1 << input_bit] >> output_bit & 1:
                        row ^= 1 << (5*column+input_bit)
            rows.append(row)
    return rows


def apply_word(values, word):
    values = list(values)
    for destination,source in word:
        require(0 <= destination < len(values) and 0 <= source < len(values)
                and destination != source, "legal distinct co-located ADD operands")
        values[destination] ^= values[source]
    return values


def physical_permutation(physical, logical, first_input=0):
    require(len(set(physical)) == len(physical) and set(physical) == set(logical),
            "one actual holder for every stripe input")
    label_index = {label:i for i,label in enumerate(logical)}
    values = [1 << (first_input + 5*label_index[label]+bit)
              for label in physical for bit in range(5)]
    labels = list(physical)
    word = []
    for target,wanted in enumerate(logical):
        source = labels.index(wanted)
        if source == target:
            continue
        for bit in range(5):
            x,y = 5*target+bit,5*source+bit
            word.extend(((x,y),(y,x),(x,y)))
        labels[target],labels[source] = labels[source],labels[target]
    require(labels == logical and len(word) <= 15*(len(logical)-1), "literal permutation bound")
    values = apply_word(values,word)
    require(values == [1 << (first_input+k) for k in range(5*len(logical))],
            "actual holder permutation gives declared source-column order")
    return values,len(word)


def add_matrix(destination, source, matrix):
    result = list(destination)
    for i,row in enumerate(matrix):
        while row:
            bit = row & -row
            result[i] ^= source[bit.bit_length()-1]
            row ^= bit
    return result


def geometry(repo, author):
    pg = repo / "research/moonshot-005-program"
    layout_path = pg / "results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz"
    layout_raw = gzip.decompress(layout_path.read_bytes())
    require(hashlib.sha256(layout_raw).hexdigest() ==
            "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72", "layout pin")
    source_path = pg / "sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    source_raw = source_path.read_bytes()
    require(hashlib.sha256(source_raw).hexdigest() ==
            "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e", "native pin")
    factor_path = pg / "results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json"
    factor_raw = factor_path.read_bytes()
    require(hashlib.sha256(factor_raw).hexdigest() ==
            "346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7", "factor pin")
    layout = json.loads(layout_raw)
    roots = layout["root_table"]
    require(roots[:111] == json.loads(source_raw)["native_roots"], "native index recovery agrees")
    dots = [[sum(x*y for x,y in zip(u,v)) for v in roots] for u in roots]
    require(all(dots[i][i] == 4 for i in range(120)), "root norm")
    planes = [tuple(sorted(h)) for h in layout["A2"]]
    plane_types = Counter(sum(j < 111 for j in plane) for plane in planes)
    require(plane_types == {0:1,1:11,2:227,3:881}, "active native plane census for invoice")
    reconstructed = set()
    for i,j,k in itertools.combinations(range(120),3):
        p,q,r = dots[i][j],dots[i][k],dots[j][k]
        if abs(p) == abs(q) == abs(r) == 2 and 64-4*(p*p+q*q+r*r)+2*p*q*r == 0:
            reconstructed.add((i,j,k))
    require(set(planes) == reconstructed and len(planes) == 1120, "independent A2 Gram reconstruction")
    d4 = [tuple(sorted(d)) for d in layout["D4"]]
    require(len(d4) == len(set(d4)) == 3150, "authenticated distinct D4 exits")
    plane_id = {h:i for i,h in enumerate(planes)}
    port_id = {d:i for i,d in enumerate(d4)}
    orthogonal = [{j for j in range(120) if dots[i][j] == 0} for i in range(120)]
    dsets = list(map(set,d4))
    ports = [[d for d,ds in enumerate(dsets) if set(h) <= ds] for h in planes]
    receivers = [[i for i,orth in enumerate(orthogonal) if set(h) <= orth] for h in planes]
    require(all(len(v) == 45 for v in ports) and all(len(v) == 36 for v in receivers),
            "literal plane ports and perpendicular receiver counts")
    certificate = json.loads(gzip.decompress((author/"output/PARTITIONS.json.gz").read_bytes()))
    classes = {int(h):rows for h,rows in certificate["classes"].items()}
    predecessors = {int(h):edge for h,edge in certificate["predecessors"].items()}
    require(set(classes) == set(range(1120)) == set(predecessors), "all native-completion planes certified")
    base = json.loads((author/"BASE-PARTITION.json").read_text())
    start = certificate["base_plane"]
    require(start == base["H"] == 3 and predecessors[start] is None, "base identity")
    require(base["ports"] == ports[start] and base["receivers"] == receivers[start], "base literal incidence")
    require(classes[start] == [[base["ports"][i] for i in group] for group in base["classes"]], "base class witness")

    def canonical(vector):
        for coordinate in vector:
            if coordinate:
                return tuple(vector if coordinate > 0 else [-x for x in vector])
        raise ValueError("zero reflected root")
    root_id = {canonical(root):i for i,root in enumerate(roots)}
    reflections = []
    for generator,s in enumerate(roots):
        permutation = []
        for j,v in enumerate(roots):
            require(dots[generator][j] % 2 == 0, "integral reflection")
            reflected = [x-(dots[generator][j]//2)*y for x,y in zip(v,s)]
            permutation.append(root_id[canonical(reflected)])
        require(sorted(permutation) == list(range(120)), "reflection permutes actual root lines")
        reflections.append(permutation)
    for h,edge in predecessors.items():
        if edge is None:
            require(h == start, "unique orbit base")
            continue
        parent,generator = edge
        permutation = reflections[generator]
        require(plane_id[tuple(sorted(permutation[j] for j in planes[parent]))] == h,
                "predecessor sends its actual plane to the target")
        transported = [[port_id[tuple(sorted(permutation[j] for j in d4[d]))] for d in group]
                       for group in classes[parent]]
        require([sorted(group) for group in transported] == classes[h], "actual reflected class transport")
        seen = set()
        current = h
        while current != start:
            require(current not in seen, "acyclic predecessor reaches base")
            seen.add(current)
            current = predecessors[current][0]
    native_counts = Counter()
    used_triples = set()
    for h in range(1120):
        group = classes[h]
        require(len(group) == 5 and all(len(g) == len(set(g)) == 9 for g in group), "five nine-port classes")
        require(sorted(itertools.chain.from_iterable(group)) == ports[h], "partition of actual 45 exits")
        m = sum(j < 111 for j in planes[h])
        for receiver in receivers[h]:
            visible = {d for d in ports[h] if dsets[d] <= orthogonal[receiver]}
            require(len(visible) == 15, "receiver sees literal fifteen exits")
            for cl in group:
                triple = tuple(i for i,d in enumerate(cl) if d in visible)
                require(len(triple) == 3, "each actual receiver sees three exits per class")
                used_triples.add(triple)
            if receiver < 111:
                native_counts[m] += 1
    require(native_counts == {0:33,1:360,2:7549,3:29354}, "native receiver-plane incidence census")
    factor = dict(json.loads(factor_raw)["factors"])
    early = {h:12//sum(j<111 for j in plane)+factor.get(h,0)
             for h,plane in enumerate(planes) if any(j<111 for j in plane)}
    require(all(45*sum(early[h] for h,plane in enumerate(planes) if j in plane) == 5760
                for j in range(111)), "all donor early totals")
    require(Counter(early[h] for h,plane in enumerate(planes) if all(j<111 for j in plane))
            == {4:709,5:84,6:88}, "full-plane early colors")
    require(all(early[h] == 6 for h,plane in enumerate(planes) if sum(j<111 for j in plane) == 2)
            and all(early[h] == 12 for h,plane in enumerate(planes) if sum(j<111 for j in plane) == 1),
            "literal punctured and singleton source splits")
    # Swapping exits preserves the partition sizes but can break receiver balance.
    corrupted = None
    for x in classes[start][0]:
        for y in classes[start][1]:
            changed = [list(cl) for cl in classes[start]]
            changed[0][changed[0].index(x)] = y
            changed[1][changed[1].index(y)] = x
            if any(sum(dsets[d] <= orthogonal[i] for d in changed[0]) != 3 for i in receivers[start]):
                corrupted = [x,y]
                break
        if corrupted: break
    require(corrupted is not None, "balanced-partition negative control")
    return {"planes":1120,"native_plane_census":dict(plane_types),"parent_receiver_plane_checks":40320,"native_incidence":dict(native_counts),
            "all_84_triples_occur":len(used_triples) == 84,"reflection_edges_checked":1119,
            "corrupt_size_preserving_swap_rejected":corrupted}, [layout_path,source_path,factor_path]


def field_and_holders(author):
    require(len(INVERSE) == 31 and all(TIMES[a][INVERSE[a]] == 1 for a in INVERSE), "GF32 all nonzero elements invertible")
    v9 = [[power(a,t) for t in range(9)] for a in range(1,10)]
    v18 = [[power(a,t) for t in range(18)] for a in range(1,19)]
    derivative = [[power(a,t-1) if t%2 else 0 for t in range(18)] for a in range(1,19)]
    require(rank(v9) == 9 and rank(v18) == 18, "full Vandermonde invertibility")
    c = json.loads((author/"UNIVERSAL-C.json").read_text())["matrix"]
    require(len(c) == 18 and all(len(row) == 18 for row in c) and
            all(type(x) is int and 0 <= x < 32 for row in c for x in row), "submitted C18 field matrix")
    for triple in itertools.combinations(range(9),3):
        for donor in range(3):
            require(rank([row[3*donor:3*donor+3] for k,row in enumerate(v9) if k in triple]) == 3,
                    "all V9 donor projections")
        rows = [2*p+s for p in triple for s in (0,1)]
        for donor in range(2):
            early = [v18[r][9*donor:9*donor+9] for r in rows]
            late = [v18[r][3*donor:3*donor+3] for r in rows]
            require(rank(early) == 6 and rank(late) == 3, "punctured component ranks")
            transfer = [row+[0]*3 for row in early] + [c[r][9*donor:9*donor+9]+late[k] for k,r in enumerate(rows)]
            require(rank(transfer) == 12, "all universal crosswave minors")
            zero = [row+[0]*3 for row in early] + [[0]*9+row for row in late]
            require(rank(zero) == 9, "zero-crosswave negative control")
        hermite = [v18[r][:12] for r in rows] + [derivative[r][:12] for r in rows]
        require(rank(hermite) == 12, "all Hermite value/derivative minors")
        require(rank([v18[r][:12] for r in rows]) == 6, "omitted-derivative negative control")
    words = json.loads(gzip.decompress((author/"output/ADD-WORDS.json.gz").read_bytes()))
    b9,b18,bc,bd = map(binary,(v9,v18,c,derivative))
    for name,expected in (("V9",b9),("V18",b18)):
        actual = apply_word([1 << i for i in range(len(expected))],words[name])
        require(actual == expected, "submitted literal binary word")
        require(apply_word(actual,list(reversed(words[name]))) == [1 << i for i in range(len(expected))],
                "literal wave inverse")
    full_stripes = 0
    full_permutation_max = 0
    for t in (2,3,4,5,6):
        strata = [[] for _ in range(3*t)]
        universe = {(j,p,s) for j in range(3) for p in range(9) for s in range(t)}
        for holder in universe:
            j,p,s = holder
            strata[s+t*((j+p)%3)].append(holder)
        require(set(itertools.chain.from_iterable(strata)) == universe, "all real full-plane phase holders used")
        for stripe in strata:
            physical = sorted(stripe,key=lambda x:x[1])
            logical = sorted(stripe)
            require([p for j,p,s in physical] == list(range(9)) and Counter(j for j,p,s in stripe) == {0:3,1:3,2:3},
                    "full-plane donor and port counts")
            permuted,count = physical_permutation(physical,logical)
            require(apply_word(permuted,words["V9"]) == b9, "full physical holder word")
            full_permutation_max = max(full_permutation_max,count)
            full_stripes += 1
    late_stripes = [[] for _ in range(6)]
    for j in range(2):
        for p in range(9):
            for s in range(2):
                late_stripes[s+2*((j+p)%3)].append(("L",j,p,s))
    ground_used = Counter()
    late_holder_set = set()
    permutation_max = 0
    cache_before = [1 << i for i in range(90)]
    for stripe_id,stripe in enumerate(late_stripes):
        early_physical = [("E",j,p,stripe_id) for p in range(9) for j in range(2)]
        early_logical = sorted(early_physical,key=lambda x:(x[1],x[2]))
        values,count = physical_permutation(early_physical,early_logical)
        early_output = apply_word(values,words["V18"])
        require(early_output == b18, "punctured early holder word")
        physical = []
        for p in range(9):
            local = [holder for holder in stripe if holder[2] == p]
            require(len(local) <= 1, "at most one native late holder per port and stripe")
            physical.extend(local)
            for _ in range(2-len(local)):
                physical.append(("Z",p,ground_used[p]))
                ground_used[p] += 1
        logical = sorted(stripe,key=lambda x:(x[1],x[2])) + sorted(h for h in physical if h[0] == "Z")
        require(Counter(h[1] for h in stripe) == {0:3,1:3} and len(logical) == 18, "punctured source-column classes")
        require(not late_holder_set.intersection(physical), "no late holder reused across stripes")
        late_holder_set.update(physical)
        late,count_late = physical_permutation(physical,logical,first_input=90)
        late = apply_word(late,words["V18"])
        late = add_matrix(late,cache_before,bc)
        require(late == [(v << 90)^x for v,x in zip(b18,bc)], "all 180 public input columns in actual two-wave holders")
        require(cache_before == [1 << i for i in range(90)], "stationary cache remains dirty and intact")
        permutation_max = max(permutation_max,count,count_late)
    require(ground_used == {p:8 for p in range(9)}, "exactly eight actual direct-ground holders per port")
    require(len(late_holder_set) == 108, "all punctured late holders used once")
    # Taking the cache after the early map gives a different, incorrect C term.
    require(add_matrix([0]*90,b18,bc) != bc, "wrong cache timing rejected")
    odd = [5*j+bit for j in range(1,18,2) for bit in range(5)]
    require(len(odd) == 45 and all(row & ~sum(1 << i for i in odd) == 0 for row in bd), "derivative uses only actual odd coefficient cache")
    late = [1 << (90+i) for i in range(90)]
    available = {i:1 << i for i in odd}
    for destination,row in enumerate(bd):
        for i in odd:
            if row >> i & 1:
                late[destination] ^= available[i]
    require(late == [(1 << (90+i))^row for i,row in enumerate(bd)], "singleton arbitrary-baseline replay")
    counts = {"V9":len(words["V9"]),"V18":len(words["V18"]),
              "C18":sum(row.bit_count() for row in bc),"D18":sum(row.bit_count() for row in bd)}
    require(counts == {"V9":850,"V18":3554,"C18":4064,"D18":1878}, "all literal coefficient costs")
    full = 120*(counts["V9"]+15*8)
    punctured = 30*(2*counts["V18"]+2*15*17+counts["C18"]+90)
    singleton = 30*(counts["V18"]+counts["D18"]+45)
    invoice = {"full_ADD_per_plane":full,"two_donor_ADD_per_plane":punctured,
               "singleton_ADD_per_plane":singleton,"ADD_total":881*full+227*punctured+11*singleton,
               "INIT_total":227*2700+11*1350,"CLEAR_total":227*2700+11*1350,"extra_MOVE":0}
    require(invoice["ADD_total"] == 184523130 and invoice["INIT_total"] == 627750, "whole local invoice")
    return {"V9_donor_minors":252,"C18_transfer_minors":168,"Hermite_minors":84,
            "field_nonzero_inverses":31,"full_actual_holder_stripes":full_stripes,
            "two_donor_actual_holder_stripes":6,"independent_public_binary_inputs_per_crosswave":180,
            "full_permutation_max_ADD":full_permutation_max,"punctured_permutation_max_ADD":permutation_max,
            "literal_word_counts":counts,"invoice":invoice,
            "negative_controls":["all C=0 transfers lose three ranks","omitted derivative loses six ranks",
                                 "cache after early map gives wrong C term","size-preserving partition swap fails"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--author",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args()
    geo,sources = geometry(args.repo,args.author)
    local = field_and_holders(args.author)
    result = {"status":"PASS_INDEPENDENT_NATIVE_NINE_PORT_REVIEW","geometry":geo,"local":local,
              "scope":"Explicit causal local modules only; common-original-donor global gluing remains open"}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    files = sources + [args.author/p for p in ("PROOF.md","check.py","BASE-PARTITION.json",
              "UNIVERSAL-C.json","output/PARTITIONS.json.gz","output/ADD-WORDS.json.gz","output/RESULT.json")]
    (args.out/"REVIEW-PINS.json").write_text(json.dumps([
        {"path":str(p.resolve()),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],indent=2)+"\n")
    print(result["status"])


if __name__ == "__main__":
    main()
