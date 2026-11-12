#!/usr/bin/env python3
"""Exact current-word extraction and closed-principal-block continuation audit.

No author constructor or earlier verifier is imported. The mathematical scope
is the coefficient interface stated in PROOF.md, not a newly generated word.
"""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
WORD_PIN = '3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
PAYLOAD_PIN = '2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
B = [5,56,65,69,77,96,100,103]
S = [0,7,20,27,36,46,57,111]


def require(q, message):
    if not q:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def addrow(a, b, c):
    out = a.copy()
    for j, v in b.items():
        n = out.get(j, F(0)) + c*v
        if n:
            out[j] = n
        else:
            out.pop(j, None)
    return out


def rank(matrix):
    a = [list(map(F, row)) for row in matrix]
    if not a:
        return 0
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        c = a[k][j]
        a[k] = [v/c for v in a[k]]
        for i in range(k+1, len(a)):
            c = a[i][j]
            if c:
                a[i] = [x-c*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def root9(normal):
    support = [i for i in range(9) if normal >> i & 1]
    if len(support) == 3:
        return [2 if i in support else -1 for i in range(9)]
    require(len(support) == 7, 'source normal root type')
    i, j = [k for k in range(9) if k not in support]
    return [3*(int(k == i)-int(k == j)) for k in range(9)]


def current_rows(word):
    rows = {i: {i: F(1)} for i in range(1880)}
    loc = dict(enumerate(word['initial']))
    for k, e in enumerate(word['program'][:word['marks']['common_starts']]):
        op, r = e[:2]
        if op == 'INIT':
            require(r not in rows and r >= 1880, 'fresh owner')
            rows[r] = {}
            loc[r] = e[2]
        elif op == 'CLEAR':
            require(r >= 1880 and loc[r] == e[2], 'owned clear')
            del rows[r]
            del loc[r]
        elif op == 'MOVE':
            require(loc[r] == e[2], 'actual MOVE source at '+str(k))
            loc[r] = e[3]
        elif op == 'SCALE':
            c = F(e[2])
            require(c and loc[r] == e[3], 'actual SCALE source')
            rows[r] = {j: c*v for j, v in rows[r].items()}
        elif op in ('ADD', 'COPY'):
            source, c, at = e[2:]
            require(r != source and loc[r] == loc[source] == at,
                    'actual cochart ADD at '+str(k))
            require(op != 'COPY' or not rows[r], 'zero COPY destination')
            rows[r] = addrow(rows[r], rows[source], F(c))
        else:
            raise ValueError(op)
    return rows


def main(args):
    source_path = args.repo/'research/shared-wire-split-composition/data/final.json.gz'
    word_path = args.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz'
    sb, wb = source_path.read_bytes(), word_path.read_bytes()
    require(digest(sb) == SOURCE_PIN and digest(wb) == WORD_PIN, 'source and word pins')
    require(digest(gzip.decompress(wb)) == PAYLOAD_PIN, 'canonical word payload pin')
    source, word = json.loads(gzip.decompress(sb)), json.loads(gzip.decompress(wb))
    H = [source['live'][i] for i in source['hosted']['Dports']]
    require(len(H) == len(set(H)) == 96, '96 distinct hosted indices')
    hosted = dict(zip(H, zip(source['hosted']['X2'], source['hosted']['Y2'])))
    raw = {int(k): v for k, v in word['private_role_map'].items()}
    roots = {h: root9(source['frames'][source['initial'][h]][0]) for h in H}
    G = {(i,j): F(sum(a*b for a,b in zip(roots[i],roots[j])),18)
         for i in H for j in H}
    require(not(set(B)&set(S)) and set(B+S) <= set(H), 'disjoint hosted frames')
    for group in (B,S):
        require(all(G[i,j] == (i == j) for i in group for j in group),
                'actual orthogonal frame')
    require(rank([roots[b] for b in B]) == 8, 'B spans source root space')
    require(all(G[i,j] == sum(G[i,b]*G[b,j] for b in B)
                for i in H for j in H), 'complete Gram factorization')

    rows = current_rows(word)
    q = {r: {raw[r]: F(1), r: F(-1)} for r in raw}
    M = {}
    for h in H:
        x = hosted[h][0]
        coeff = {j: rows[raw[x]].get(raw[hosted[j][1]],F(0)) for j in H}
        expected = q[x]
        for j,c in coeff.items():
            if c:
                expected = addrow(expected,q[hosted[j][1]],c)
        require(rows[raw[x]] == expected, 'no hidden current X2 dependence')
        M[h] = {j: c+F(h == j) for j,c in coeff.items() if c+F(h == j)}
        require(rows[raw[hosted[h][1]]] == q[hosted[h][1]], 'authentic current d')
    for i in H:
        for j in H:
            expected = (F(i == j) + (G[i,j] if j in B and i not in B else 0)
                        + (G[i,j] if i in B and j in S else 0))
            require(M[i].get(j,F(0)) == expected, 'exact admitted coefficient matrix')

    U = [h for h in H if h not in B]
    K = B+S
    outside = [h for h in H if h not in K]
    Z = {h: [(-1 if h in B else 1)*G[h,s] for s in S] for h in H}
    require(all(sum(c*Z[j][k] for j,c in M[i].items()) == 0
                for i in H for k in range(8)), 'current explicit right kernel')
    require(all(Z[s] == [F(s == t) for t in S] for s in S), 'eight kernel pivots')
    require(rank([[M[i].get(j,F(0)) for j in H] for i in H]) == 88,
            'independent exact elimination rank88')
    require(all(M[i].get(j,F(0)) == G[i,j] for i in K for j in K)
            and all(not M[i].get(j) for i in K for j in outside),
            'closed principal Gram block on B union S')
    require(all(M[i].get(j,F(0)) == (i == j) for i in outside for j in outside),
            'outside identity block')
    require(all(rank([roots[i],roots[j]]) == 2 for i,j in combinations(H,2)),
            'every hosted pair independent')

    candidates = []
    for t in outside:
        bt = [b for b in B if G[b,t]]
        st = [s for s in S if G[s,t]]
        require(len(bt) == len(st) == 4 and all(abs(G[i,t]) == F(1,2) for i in bt+st),
                'four plus four unit-half contacts')
        changes = [(h,t,G[h,t]) for h in bt+st]+[(t,s,G[t,s]) for s in st]
        require(len(changes) == len({(i,j) for i,j,c in changes}) == 12,
                'exactly twelve distinct entries')
        require(all(not M[i].get(j) for i,j,c in changes), 'all changed entries initially absent')
        N = {i: row.copy() for i,row in M.items()}
        for i,j,c in changes:
            N[i][j] = c
        principal = K+[t]
        rest = [h for h in H if h not in principal]
        pivots = S+[t]
        require(all(N[i].get(j,F(0)) == G[i,j] for i in principal for j in principal),
                'completed enlarged principal Gram block')
        require(all(not N[i].get(j) for i in principal for j in rest),
                'preserved closed principal block')
        require(all(N[i].get(j,F(0)) == (i == j) for i in rest for j in rest),
                'preserved outside identity')
        for u in pivots:
            z = {h: -G[h,u] if h in B else F(h == u) if h in pivots else G[h,u] for h in H}
            require(all(sum(c*z[j] for j,c in N[i].items()) == 0 for i in H),
                    'nine full current right-kernel vectors')
            left = {h: z[h] if h in principal else F(0) for h in H}
            require(all(sum(left[i]*N[i].get(j,F(0)) for i in principal) == 0 for j in H),
                    'nine full left-kernel vectors')
        minor = B+rest
        require(len(minor) == 87
                and all(N[i].get(j,F(0)) == (i == j) for i in B for j in minor)
                and all(N[i].get(j,F(0)) == (i == j) for i in rest for j in rest),
                'unit block-triangular87 minor')
        J = [t]+st
        require(rank([roots[h] for h in J]) == 4 and rank([Z[h] for h in J]) == 4,
                'five changed columns have root/kernel row rank4')
        require(all(roots[t][a] == sum(G[s,t]*roots[s][a] for s in st) for a in range(9)),
                'explicit four-root relation')
        candidates.append({'receiver':t, 'B_contacts':bt, 'S_contacts':st,
                           'changed_columns':J, 'column_root_rank':4, 'new_rank':87,
                           'entries':[[i,j,str(c)] for i,j,c in changes]})

    # Negative controls are actual exact matrix ranks, not parser assertions.
    t = 90
    require(t in outside, 'physical bridge witness is outside both frames')
    witness = next(c for c in candidates if c['receiver'] == t)
    full = {i: row.copy() for i,row in M.items()}
    column_only = {i: row.copy() for i,row in M.items()}
    for i,j,c in witness['entries']:
        full[i][j] = F(c)
        if j == t:
            column_only[i][j] = F(c)
    single = {i: row.copy() for i,row in M.items()}
    single[t][witness['S_contacts'][0]] = G[t,witness['S_contacts'][0]]
    wrong = {i: row.copy() for i,row in full.items()}
    wrong[t][witness['S_contacts'][0]] *= -1
    controls = {}
    for name, matrix, expected in [('all_eight_entries_only_in_t_column',column_only,88),
                                    ('single_reverse_contact',single,88),
                                    ('one_wrong_mutual_sign',wrong,88),
                                    ('complete_twelve_entry_block',full,87)]:
        got = rank([[matrix[i].get(j,F(0)) for j in H] for i in H])
        require(got == expected, 'negative-control exact rank '+name)
        controls[name] = got

    result = {'status':'PASS_EXACT_CURRENT_RANK88_PRINCIPAL_RANK87_GATE',
              'source_sha256':SOURCE_PIN, 'word_sha256':WORD_PIN,
              'word_payload_sha256':PAYLOAD_PIN, 'prefix_input_columns':1880,
              'hosted_roles':H, 'coupled_roles_excluded':8, 'B':B, 'S':S,
              'current_rank':88, 'current_right_kernel':{str(h):list(map(str,Z[h])) for h in H},
              'all_hosted_pairs_independently_tested':len(H)*(len(H)-1)//2,
              'candidate_count':len(candidates), 'each_candidate_missing_entries':12,
              'each_candidate_changed_columns':5, 'each_candidate_column_root_rank':4,
              'each_candidate_rank':87, 'negative_controls':controls,
              'scope':'Algebraic current-word continuation gate. No new physical source word, supplier or kappa.'}
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.output/'CANDIDATES.json').write_text(json.dumps(candidates,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','current_rank','candidate_count',
                      'each_candidate_missing_entries','each_candidate_rank','negative_controls')},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
