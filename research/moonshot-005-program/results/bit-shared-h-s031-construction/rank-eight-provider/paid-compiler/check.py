#!/usr/bin/env python3
"""Compile the reviewed rank-eight provider with one paid field complement."""
from argparse import ArgumentParser
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import numpy as np


def need(ok, why):
    if not ok:
        raise ValueError(why)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
here = Path(__file__).resolve().parent
base = args.repo/'research/moonshot-005-program/results'
for path, digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
g = module(base/'bit-coupled-native-geometric-cycle-source/review-c/check.py', 'independent_field')
price = module(base/'kappa-significant-gain-screen/root-review/check.py', 'reviewed_exact_price')
literal = json.loads(gzip.decompress((here.parent/'output/COEFFICIENTS.json.gz').read_bytes()))
review = json.loads(gzip.decompress((here.parent/'review-c/output/MATRICES.json.gz').read_bytes()))
P = np.array(literal['Hword'], dtype=np.uint8)
T = np.array(review['paid_extension'], dtype=np.uint8)
inverse = np.array(review['paid_extension_inverse'], dtype=np.uint8)
c = np.zeros((1, 9), dtype=np.uint8)
c[0, 0] = 1
A = np.vstack([P, c])
need(P.shape == (9, 9) and g.rank(P) == 8 and T.shape == (10, 10), 'literal rank-eight interface')
need(np.array_equal(T[:, :9], A) and g.rank(A) == 9, 'one real complement input')
need(np.array_equal(g.mm(T, inverse), np.eye(10, dtype=np.uint8)), 'full inverse extension')
need(np.array_equal(g.mm(inverse, A), np.vstack([np.eye(9, dtype=np.uint8), np.zeros((1, 9), dtype=np.uint8)])), 'original restoration and zero complement')
binary = np.array([[int(g.M[T[r//6, s//6], 1 << (s%6)]) >> (r%6) & 1 for s in range(60)] for r in range(60)], dtype=np.uint8)
reduced, operations = binary.copy(), []


def add(target, source):
    need(target != source, 'distinct owned ADD operands')
    reduced[target] ^= reduced[source]
    operations.append([target, source])


for col in range(60):
    pivot = col+int(np.flatnonzero(reduced[col:, col])[0])
    if pivot != col:
        add(col, pivot)
        add(pivot, col)
        add(col, pivot)
    for row in range(60):
        if row != col and reduced[row, col]:
            add(row, col)
need(np.array_equal(reduced, np.eye(60, dtype=np.uint8)), 'binary elementary reduction')
values = [1 << j for j in range(54)]+[0]*6
for target, source in reversed(operations):
    values[target] ^= values[source]
expected = [sum(int(binary[i, j]) << j for j in range(54)) for i in range(60)]
need(values == expected, 'literal symbolic forward outputs on real owners')
for target, source in operations:
    values[target] ^= values[source]
need(values == [1 << j for j in range(54)]+[0]*6, 'symbolic originals restored and added owners zero')
old_n = {1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
old_h = {2:1,4:25,6:1,8:410}
gap = price.hist((36,old_h),(-36,old_n),(111,price.wrapper(9)))
allowance = price.hist((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}))
for j in range(1,9):
    allowance[7*j+1] += F(37,3)
    allowance[7*j] -= F(37,3)
Q0 = {1:F(4451,8),2:F(7213,16),4:F(24)}
kappa = F(1,200)


def margin(q, total_component_defect, multiplicity):
    histogram = price.hist((1,allowance),(-1,Q0),(-F(q,3840),{8:1}),(-F(16*total_component_defect,3840),{6:1}))
    if multiplicity is not None:
        histogram = price.hist((1,histogram),(F(1,36*(multiplicity-1)),gap))
    return price.moment(histogram,kappa)


caps = []
maxima = {}
for m in (870,None):
    passing = []
    for d in range(13):
        room = margin(0,d,m)
        weight = price.power(8,kappa)
        continuous = 3840*room[0]/weight[1], 3840*room[1]/weight[0]
        cap = continuous[0].numerator//continuous[0].denominator
        need(continuous[1] < cap+1 and margin(cap,d,m)[0] > 0 and margin(cap+1,d,m)[1] < 0, 'exact strict integer cap')
        if margin(34560,d,m)[0] > 0:
            passing.append(d)
        caps.append({'m':m,'total_component_defect':d,'extra_field_exports':16*d,'return_cap':cap,'exact_continuous_cap':[str(x) for x in continuous]})
    maxima[str(m)] = max(passing)
need(maxima == {'870':10,'None':11}, 'total defect limit for these separately exported complements')
need(next(x['return_cap'] for x in caps if x['m']==870 and x['total_component_defect']==1)==34675, 'single rank-eight cap')
result = {'status':'PASS_LITERAL_RANK_EIGHT_PAID_COMPILER_AND_PRICE','field_inputs':9,'rank':8,'extra_fields_per_component':1,
          'binary_ADD_per_direction':len(operations),'sixteen_copy_replacement_ADD':32*len(operations),
          'sixteen_copy_extra_field_exports':16,'sixteen_copy_binary_INIT_MOVE_CLEAR_each':96,'MOVE_gap':6,
          'm870_return_cap':34675,'floor_slack':115,'total_component_defect_caps_at_floor':maxima,
          'movement_caps':caps,'full_bank_or_global_supplier':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True)
(args.out/'COMPILER.json').write_text(json.dumps({'T':T.tolist(),'inverse':inverse.tolist(),'elimination_ADDs':operations},indent=2)+'\n')
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],len(operations),32*len(operations),96,34675,flush=True)
