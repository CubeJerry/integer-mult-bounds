#!/usr/bin/env python3
"""Exact native class-reservoir support certificate; no author code imports."""
import argparse, gzip, hashlib, itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def echelon(rows):
    piv = {}
    for r in rows:
        while r:
            p = r.bit_length()-1
            if p in piv:
                r ^= piv[p]
            else:
                piv[p] = r
                break
    return piv


def reduce(row, piv):
    for p in sorted(piv, reverse=True):
        if row >> p & 1:
            row ^= piv[p]
    return row


def rank(rows):
    return len(echelon(rows))


def lift(row, t, V=2):
    return sum(((row >> j) & 1) << (V*j+t) for j in range(111))


def arrival(row):
    foreign = row.bit_count()-1
    return int(foreign > 36)+int(foreign > 52)


def native(path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'native byte pin')
    n = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        r = list(map(Fraction, n['frames'][str(n['start'][i])]['B'][0]))
        norm = sum(x*x for x in r)
        factor = (2 if norm == 1 else 1)*(1 if next(x for x in r if x) > 0 else -1)
        r = [x*factor for x in r]
        need(sum(x*x for x in r) == 4 and all(x.denominator == 1 for x in r), 'integer root normalization')
        roots.append(list(map(int, r)))
    support = lambda r: tuple(j for j, x in enumerate(r) if x)
    complement = lambda S: tuple(j for j in range(8) if j not in S)
    patterns = sorted({support(r) for r in roots if len(support(r)) == 4})
    pairs = [(S, complement(S)) for S in patterns if S < complement(S)]
    need(len(patterns) == 14 and len(pairs) == 7, 'native complementary support pairs')
    groups = [[] for _ in range(15)]
    for i, r in enumerate(roots):
        S = support(r)
        c = 0 if len(S) == 1 else 1+2*next(j for j, p in enumerate(pairs) if S in p)+sum(x < 0 for x in r) % 2
        groups[c].append(i)
    need([len(g) for g in groups] == [8,7,7,8,7,8,8,8,7,8,8,5,8,8,6], 'actual class sizes')
    dot = lambda i, j: sum(a*b for a, b in zip(roots[i], roots[j]))
    need(all(dot(i, j) == 0 for g in groups for i, j in itertools.combinations(g, 2)), 'class orthogonality')
    K = [sum(int(i == j or dot(i, j) == 0) << j for j in range(111)) for i in range(111)]
    U = [sum(1 << j for j in g) for g in groups]
    return K, U, groups


def exact_row_control(K, U, groups, extra):
    CV = [lift(c, t) for c in echelon(K).values() for t in range(2)]
    W = echelon(CV+extra)
    class_of = {i: c for c, group in enumerate(groups) for i in group}
    enabled = [c for c, u in enumerate(U) if all(reduce(lift(u, t), W) == 0 for t in range(2))]
    optimum = 0
    checked = 0
    singular_nonzero = 0
    for i, k in enumerate(K):
        c = class_of[i]
        best = 3
        for M in range(16):
            N = 9 ^ M
            blocks = [[(k if M >> (2*r+t) & 1 else 0) ^ (U[c] if N >> (2*r+t) & 1 else 0)
                       for t in range(2)] for r in range(2)]
            rows = [lift(blocks[r][0], 0) ^ lift(blocks[r][1], 1) for r in range(2)]
            active = blocks[0][0] | blocks[0][1] | blocks[1][0] | blocks[1][1]
            need(active.bit_count()-1 == (k.bit_count()-1 if M else len(groups[c])-1), 'exact nonzero whole-block support dichotomy')
            if M and rank([M & 3, M >> 2]) == 1:
                singular_nonzero += 1
            checked += 1
            if all(reduce(x, W) == 0 for x in rows):
                best = min(best, arrival(active))
        need(best in (0, 2), 'no intermediate arrival saving')
        optimum += best
    expected = 222-2*sum(len(groups[c]) for c in enabled)
    need(optimum == expected, 'exact permitted-space optimum')
    return {'quotient_dimension': len(W)-18, 'enabled_classes': enabled, 'ell': optimum,
            'receiver_matrix_cases': checked, 'nonzero_singular_cases': singular_nonzero}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--native', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    K, U, groups = native(a.native)
    C = echelon(K)
    need(len(C) == 9 and rank(U) == 15 and rank(list(C.values())+U) == 19, 'canonical/class code dimensions')
    full = (1 << 111)-1
    class_of = {i: c for c, g in enumerate(groups) for i in g}
    restrictions = []
    for i, k in enumerate(K):
        z = full ^ k
        r = rank([x & z for x in list(C.values())+U])
        need(r == 17, 'rank17 full reservoir restriction')
        need(rank([k, U[class_of[i]]]) == 2 and U[class_of[i]] & z == 0, 'two independent local kernel witnesses')
        restrictions.append(r)
    quotient = [reduce(u, C) for u in U]
    need(all(quotient) and all(rank([a, b]) == 2 for a, b in itertools.combinations(quotient, 2)), 'fifteen distinct nonzero quotient lines')
    best = [(-1, None) for _ in range(11)]
    count_by_rank = Counter()
    smallest_dependency = 16
    for mask in range(1 << 15):
        selected = [c for c in range(15) if mask >> c & 1]
        r = rank([quotient[c] for c in selected])
        size = sum(len(groups[c]) for c in selected)
        count_by_rank[r] += 1
        if r < len(selected):
            smallest_dependency = min(smallest_dependency, len(selected))
        for cap in range(r, 11):
            if size > best[cap][0]:
                best[cap] = (size, mask)
    need([x[0] for x in best] == [0,8,16,24,32,40,54,63,71,85,111], 'exact rank-cap coverage table')
    table = []
    tensors = []
    for cap, (size, mask) in enumerate(best):
        selected = [c for c in range(15) if mask >> c & 1]
        selected_set = set(selected)
        F = [U[class_of[i]] if class_of[i] in selected_set else k for i, k in enumerate(K)]
        ell = sum(arrival(f) for f in F)
        need(ell == 222-2*size, 'rank-cap scalar attainment')
        scalar_q = rank(F+list(C.values()))-9
        need(scalar_q <= cap, 'rank-cap quotient attainment')
        table.append({'rank_cap': cap, 'maximum_covered_receivers': size, 'minimum_ell': ell,
                      'maximizing_classes': selected, 'actual_scalar_quotient': scalar_q})
        if cap in (0, 1, 2, 10):
            for V in (1, 2, 3, 5):
                cv = [lift(c, t, V) for c in C.values() for t in range(V)]
                av = [lift(f, t, V) for f in F for t in range(V)]
                d = rank(av+cv)-9*V
                need(d == scalar_q*V, 'exact tensor quotient')
                tensors.append({'scalar_rank_cap': cap, 'V': V, 'quotient': d, 'ell': ell})
    line_free = exact_row_control(K, U, groups, [lift(U[0], 0), lift(U[1], 1), lift(U[2], 0)^lift(U[2], 1)])
    partial = exact_row_control(K, U, groups, [lift(U[0], 0), lift(U[0], 1), lift(U[1], 0)])
    need(line_free['quotient_dimension'] == partial['quotient_dimension'] == 3, 'entangled width-two control dimension')
    need(line_free['ell'] == 222 and partial['ell'] == 206, 'line-free and partial-line distinction')
    need(table[1]['maximum_covered_receivers'] < 16 and table[2]['minimum_ell'] < 206, 'meaningful false scope controls')
    out = {'status': 'PASS_EXACT_CLASS_RESERVOIR_OPERATOR_GATE', 'native_sha256': PIN,
           'C_dimension': 9, 'U_dimension': 15, 'C_plus_U_dimension': 19, 'quotient_dimension': 10,
           'groups': groups, 'class_indicators_hex': list(map(hex, U)), 'quotient_remainders_hex': list(map(hex, quotient)),
           'forbidden_restriction_rank_census': dict(Counter(restrictions)),
           'distinct_nonzero_class_quotient_lines': 15, 'subsets_checked': 1 << 15,
           'subset_rank_census': dict(sorted(count_by_rank.items())), 'smallest_dependent_class_subset': smallest_dependency,
           'rank_cap_table': table, 'tensor_attainments': tensors,
           'line_free_control': line_free, 'partial_second_line_control': partial,
           'negative_controls': ['nonzero singular M does not erase a whole block', 'one class line cannot cover16 receivers', '206 does not extend to d=2V'],
           'classification': 'fixed native rank certificate supporting the universal proof; no physical source or new kappa', 'new_kappa': None}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'restrictions': len(restrictions), 'subsets': 1 << 15,
                      'rank_cap_coverage': [x[0] for x in best], 'sub_double_width_ell_floor': 206}))


if __name__ == '__main__':
    main()
