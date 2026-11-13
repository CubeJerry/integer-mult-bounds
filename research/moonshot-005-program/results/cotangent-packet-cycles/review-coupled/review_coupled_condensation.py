#!/usr/bin/env python3
"""Independent source-root review of the proposed coupled Schur interface.

No author checker, receipt, or programme helper is imported. Exact Fraction
elimination is performed on Gram matrices rebuilt from the pinned native word.
"""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

SOURCE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
BASIS = (5, 56, 69, 100, 65, 77, 96, 103)


def need(test, message):
    if not test:
        raise ValueError(message)


def rank(rows):
    pivots = {}
    for raw in rows:
        row = [F(x) for x in raw]
        for p, old in sorted(pivots.items()):
            if row[p]:
                scalar = row[p]
                row = [x - scalar * y for x, y in zip(row, old)]
        p = next((j for j, x in enumerate(row) if x), None)
        if p is not None:
            scalar = row[p]
            pivots[p] = [x / scalar for x in row]
    return len(pivots)


def determinant(rows):
    a = [[F(x) for x in row] for row in rows]
    n, answer = len(a), F(1)
    need(all(len(row) == n for row in a), 'Square determinant')
    for j in range(n):
        k = next((k for k in range(j, n) if a[k][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[j], a[k] = a[k], a[j]
            answer = -answer
        pivot = a[j][j]
        answer *= pivot
        for k in range(j + 1, n):
            scalar = a[k][j] / pivot
            a[k] = [x - scalar * y for x, y in zip(a[k], a[j])]
    return answer


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def main(args):
    raw = (args.repo / 'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE, 'Pinned native source')
    source = json.loads(gzip.decompress(raw))
    h = sorted(source['live'][j] for j in source['hosted']['Dports'])
    u = sorted(set(source['live']) - set(h))
    need(len(h) == 96 and u == [17, 19, 30, 38, 40, 47, 52, 60], 'Actual hosted/coupled partition')
    roots = {}
    for i in h + u:
        normal = source['frames'][source['initial'][i]][0]
        ones = [j for j in range(9) if normal & (1 << j)]
        if len(ones) == 3:
            roots[i] = [2 if j in ones else -1 for j in range(9)]
        else:
            need(len(ones) == 7, 'Root chart normal')
            p, q = [j for j in range(9) if j not in ones]
            roots[i] = [3 * (int(j == p) - int(j == q)) for j in range(9)]
    gram = lambda left, right: [[F(sum(x * y for x, y in zip(roots[i], roots[j])), 18)
                                  for j in right] for i in left]
    gh, a, t, gu = gram(h, h), gram(h, u), gram(u, h), gram(u, u)
    need(gram(BASIS, BASIS) == [[F(i == j) for j in range(8)] for i in range(8)], 'Genuine orthoframe')
    c = [[gram(BASIS, u)[BASIS.index(i)][j] if i in BASIS else F(0)
          for j in range(8)] for i in h]
    d = [[gram(u, BASIS)[i][BASIS.index(j)] if j in BASIS else F(0)
          for j in h] for i in range(8)]
    need(mul(gh, c) == a and mul(d, gh) == t and mul(d, a) == gu, 'Schur containment and product identities')
    eye = [[F(i == j) for j in range(8)] for i in range(8)]
    z8 = [[F(0)] * 8 for _ in range(8)]
    z96_8 = [[F(0)] * 8 for _ in range(96)]
    z8_96 = [[F(0)] * 96 for _ in range(8)]

    def joint(cross_a, cross_t, s):
        return [left + right for left, right in zip(gh, cross_a)] + [left + [x+y for x,y in zip(erow,srow)]
                for left, erow, srow in zip(cross_t, eye, s)]

    required_s = [[x-y for x,y in zip(row, irow)] for row,irow in zip(gu,eye)]
    minus_eye = [[-x for x in row] for row in eye]
    matrices = {'independent_unchanged': joint(z96_8, z8_96, z8),
                'native_cross_only': joint(a, t, z8),
                'native_cross_negative_identity': joint(a, t, minus_eye),
                'full_native_Gram': joint(a, t, required_s)}
    ranks = {name: rank(matrix) for name,matrix in matrices.items()}
    need(ranks == {'independent_unchanged':16, 'native_cross_only':16,
                   'native_cross_negative_identity':15, 'full_native_Gram':8}, 'Joint target ranks')
    kernel = [1,-1,0,-1,1,0,0,0]
    need(all(sum(x*y for x,y in zip(row,kernel)) == 0 for row in gu+a), 'Actual invisible coupled mode')
    need([sum(x*y for x,y in zip(row,kernel)) for row in required_s] == [-x for x in kernel], 'Required local action on invisible mode')
    det = determinant([[-x for x in row] for row in required_s])
    need(det == F(-7,64) and rank(gu) == 7, 'Coupled block determinant and rank')
    o = [row + [F(0)] * 8 for row in mul(gu,t)]
    returns = [left+right for left,right in zip(gram(BASIS,h),gram(BASIS,u))]
    cache_ranks = [rank(o), rank(o+returns), rank(o+returns+matrices['native_cross_only'])]
    y17 = [F(0)] * 104
    y17[96] = 1
    need(cache_ranks == [7,15,16], 'Conditional pure-cache information dimensions')
    need(rank(o+returns+[y17]) == 16 and rank(o+returns+[y17]+matrices['native_cross_only']) == 16,
         'Original y17 complements the missing information dimension')

    # A mixed observation identical to z has an apparently nonzero s block,
    # but its effective coefficient after conditioning on z is exactly zero.
    r_small, p_small, q_small = [[F(2)]], [[F(1)]], [[F(2)]]
    effective = [[q_small[0][0] - mul(p_small,r_small)[0][0]]]
    need(rank(q_small) == 1 and rank(effective) == 0, 'Raw-rank false-positive control')
    result = {'status':'PASS_INDEPENDENT_COUPLED_CONDENSATION_REVIEW',
              'native_sha256':SOURCE, 'hosted_ports':h, 'coupled_ports':u,
              'basis':list(BASIS), 'coupled_Gram':[[str(x) for x in row] for row in gu],
              'joint_ranks':ranks, 'coupled_Gram_rank':7,
              'det_I_minus_coupled_Gram':str(det), 'kernel':kernel,
              'conditional_cache_ranks':cache_ranks,
              'original_y17_completes_information':True,
              'negative_controls':{'coupled_set_is_not_orthogonal':gu != eye,
                                   'wrong_negative_identity_self_response_rank':ranks['native_cross_negative_identity'],
                                   'raw_mixed_observation_rank':rank(q_small),
                                   'effective_mixed_observation_rank':rank(effective)},
              'observation_contract':'Given z=n+R*s, every raw observation P*n+Q*s must be reduced to (Q-P*R)*s before computing correction capacity. Pure observations are the special case P=0.',
              'scope':'Exact characteristic-zero information gate for a proposed complete interface; no actual native response, cache, acquisition chronology, tariff, supplier or new kappa is supplied.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'joint_ranks':ranks,'cache_ranks':cache_ranks,'determinant':str(det)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
