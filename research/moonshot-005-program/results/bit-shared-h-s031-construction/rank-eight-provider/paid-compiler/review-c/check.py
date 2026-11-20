#!/usr/bin/env python3
"""Independent literal rank-eight paid compiler arithmetic review.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and different pivot choices.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise AssertionError(message)


def xor(values):
    answer = 0
    for value in values:
        answer ^= int(value)
    return answer


def product(x, y):
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result


MUL = np.array([[product(x, y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(y for y in range(1, 64) if MUL[x, y] == 1)
                           for x in range(1, 64)], dtype=np.uint8)


def power(x, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = int(MUL[answer, x])
        x = int(MUL[x, x])
        exponent >>= 1
    return answer


def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    answer = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for col in range(left.shape[1]):
        answer ^= MUL[left[:, col, None], right[col, None, :]]
    return answer


def kron(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    return MUL[left[:, None, :, None], right[None, :, None, :]].reshape(
        left.shape[0] * right.shape[0], left.shape[1] * right.shape[1])


def echelon(matrix):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    determinant = 1
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        chosen = row + int(choices[-1])
        matrix[[row, chosen]] = matrix[[chosen, row]]
        determinant = int(MUL[determinant, matrix[row, col]])
        matrix[row, col:] = MUL[INV[matrix[row, col]], matrix[row, col:]]
        if row + 1 < len(matrix):
            matrix[row + 1:, col:] ^= MUL[matrix[row + 1:, col, None], matrix[row, None, col:]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots, determinant


def rank(matrix):
    return len(echelon(matrix)[1])


def null(matrix):
    rows, pivots, _ = echelon(matrix)
    free = [j for j in range(rows.shape[1]) if j not in pivots]
    result = np.zeros((rows.shape[1], len(free)), dtype=np.uint8)
    result[free] = np.eye(len(free), dtype=np.uint8)
    for i in range(len(pivots) - 1, -1, -1):
        result[pivots[i]] = mm(rows[i:i + 1, pivots[i] + 1:], result[pivots[i] + 1:])[0]
    need(not np.any(mm(matrix, result)), 'independent nullspace identity')
    return result


def certificate(matrix):
    _, cols, _ = echelon(matrix)
    _, rows, _ = echelon(matrix[:, cols].T)
    minor = matrix[np.ix_(rows, cols)]
    _, pivots, determinant = echelon(minor)
    kernel = null(matrix)
    need(len(pivots) == len(cols) and determinant != 0, 'nonzero maximal minor')
    need(rank(kernel) == matrix.shape[1] - len(cols), 'independent upper-rank certificate')
    return {'shape': list(matrix.shape), 'rank': len(cols), 'minor_rows': rows,
            'minor_columns': cols, 'minor_determinant': determinant,
            'kernel_columns': kernel.tolist(), 'matrix_sha256': hashlib.sha256(matrix.tobytes()).hexdigest()}


def ceil_div(n, d):
    return -((-n) // d)


@lru_cache(None)
def power_interval(n, kappa):
    """Directed dyadic square roots; independent of the author's log/exp engine."""
    scale = 1 << 320
    root_lo = root_hi = n * scale
    product_lo = product_hi = scale
    remaining = Fraction(kappa)
    need(0 <= remaining < 1, 'exponent range')
    for _ in range(160):
        root_lo = isqrt(root_lo * scale)
        radicand = root_hi * scale
        root_hi = isqrt(radicand)
        if root_hi * root_hi < radicand:
            root_hi += 1
        remaining *= 2
        if remaining >= 1:
            product_lo = product_lo * root_lo // scale
            product_hi = ceil_div(product_hi * root_hi, scale)
            remaining -= 1
    if remaining:
        product_hi = ceil_div(product_hi * root_hi, scale)
    return Fraction(n * scale, product_hi), Fraction(n * scale, product_lo)


def histogram(*terms):
    result = Counter()
    for scalar, table in terms:
        for degree, count in table.items():
            result[int(degree)] += Fraction(scalar) * count
    return result


def moment(table, kappa):
    lo = hi = Fraction(0)
    for degree, coefficient in table.items():
        a, b = power_interval(degree, kappa)
        if coefficient >= 0:
            lo += coefficient * a
            hi += coefficient * b
        else:
            lo += coefficient * b
            hi += coefficient * a
    return lo, hi


def binary_expansion(A):
    return np.array([[int(MUL[A[r // 6, c // 6], 1 << (c % 6)]) >> (r % 6) & 1
                      for c in range(6 * A.shape[1])] for r in range(6 * A.shape[0])], dtype=np.uint8)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'pin '+name)
    package=here.parent;provider=package.parent
    data=json.loads((package/'output/COMPILER.json').read_text());claimed=json.loads((package/'output/RESULT.json').read_text())
    literal=json.loads(gzip.decompress((provider/'output/COEFFICIENTS.json.gz').read_bytes()))
    witness=json.loads(gzip.decompress((provider/'review-c/output/MATRICES.json.gz').read_bytes()))
    P=np.array(literal['Hword'],dtype=np.uint8);T=np.array(data['T'],dtype=np.uint8);Ti=np.array(data['inverse'],dtype=np.uint8)
    L=np.zeros((1,9),dtype=np.uint8);L[0,0]=1;A=np.vstack([P,L]);reset=np.vstack([np.eye(9,dtype=np.uint8),np.zeros((1,9),dtype=np.uint8)])
    need(P.shape==(9,9)and rank(P)==8 and rank(A)==9 and T.shape==Ti.shape==(10,10),'literal rank-defect dimensions')
    need(np.array_equal(T,witness['paid_extension'])and np.array_equal(Ti,witness['paid_extension_inverse']),'same independently reviewed extension')
    need(np.array_equal(T[:,:9],A)and np.array_equal(mm(T,Ti),np.eye(10,dtype=np.uint8))and np.array_equal(mm(Ti,A),reset),'restoration with zero added owner')
    ops=data['elimination_ADDs'];need(all(len(op)==2 and all(0<=x<60 for x in op)and op[0]!=op[1]for op in ops),'distinct owned ADD operands')
    binary=binary_expansion(T);word=np.eye(60,dtype=np.uint8)
    for target,source in reversed(ops):word[target]^=word[source]
    need(np.array_equal(word,binary),'entire literal forward word')
    for target,source in ops:word[target]^=word[source]
    need(np.array_equal(word,np.eye(60,dtype=np.uint8)),'entire literal inverse word')
    values=np.vstack([np.eye(54,dtype=np.uint8),np.zeros((6,54),dtype=np.uint8)])
    for target,source in reversed(ops):values[target]^=values[source]
    need(np.array_equal(values,binary_expansion(A)),'forward physical values from54 real inputs and6 owned zeros')
    for target,source in ops:values[target]^=values[source]
    need(np.array_equal(values,binary_expansion(reset)),'originals and6 zeros restored without side information')
    need(len(ops)==1474 and 32*len(ops)==47168,'exact literal ADD count both directions16 copies')
    need(16*6==96 and rank(binary_expansion(A)[:-1])==53,'actual96 added bit owners and missing-bit control')
    old_paid={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};old_productive={2:1,4:25,6:1,8:410}
    wrapper=Counter({127:2,1:-4})
    for j in range(1,10):wrapper[7*j+1]+=4
    for j in range(1,9):wrapper[7*j]-=4
    old_gap=histogram((36,old_productive),(-36,old_paid),(111,wrapper))
    need(moment(old_gap,Fraction(0))==(1506,1506),'retained complete caller credit')
    allowance=Counter({127:Fraction(37,6),64:Fraction(37,3),1:-Fraction(37,3)})
    for j in range(1,9):allowance[7*j+1]+=Fraction(37,3);allowance[7*j]-=Fraction(37,3)
    Q0={1:Fraction(4451,8),2:Fraction(7213,16),4:Fraction(24)};kappa=Fraction(1,200)
    def margin(q,defect,m):
        hist=histogram((1,allowance),(-1,Q0),(-Fraction(q,3840),{8:1}),(-Fraction(16*defect,3840),{6:1}))
        if m is not None:hist=histogram((1,hist),(Fraction(1,36*(m-1)),old_gap))
        return moment(hist,kappa)
    results=[];maxima={}
    for m in [870,None]:
        passing=[]
        for d in range(13):
            lo,hi=margin(0,d,m);w=power_interval(8,kappa);interval=(3840*lo/w[1],3840*hi/w[0])
            cap=interval[0].numerator//interval[0].denominator
            need(interval[1]<cap+1 and margin(cap,d,m)[0]>0 and margin(cap+1,d,m)[1]<0,'exact strict integer cap')
            original=next(row for row in claimed['movement_caps']if row['m']==m and row['total_component_defect']==d)
            need(cap==original['return_cap'],'independently reproduced cap')
            if margin(34560,d,m)[0]>0:passing.append(d)
            results.append({'m':m,'component_defect':d,'exports':16*d,'cap':cap,'interval':[str(x)for x in interval]})
        maxima[str(m)]=max(passing)
    need(maxima=={'870':10,'None':11},'finite/limiting defect budget at nine-bank floor')
    need(next(x['cap']for x in results if x['m']==870 and x['component_defect']==1)==34675,'rank-eight return cap')
    need(margin(34688,0,870)[0]>0 and margin(34688,1,870)[1]<0,'omitted complement charge changes strict sign')
    result={'status':'PASS_INDEPENDENT_RANK_EIGHT_PAID_WORD_PRICE','binary_ADD_per_direction':1474,'sixteen_copy_replacement_ADD':47168,
            'binary_INIT_MOVE_CLEAR_each':96,'field_exports':16,'export_gap':6,'m870_return_cap':34675,'floor_slack':115,
            'maximum_total_component_defects':maxima,'strict_caps':results,'missing_complement_bit_rank':53,
            'power_method':'160 directed exponent digits;320-bit integer square-root bounds','author_executable_imports':False,
            'complete_global_invoice':False,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],1474,47168,96,34675,flush=True)

if __name__=='__main__':main()
