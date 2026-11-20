#!/usr/bin/env python3
"""Owned complement compiler and exact retained movement price."""
import argparse, hashlib, importlib.util, itertools, json
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import numpy as np


def need(ok, why):
    if not ok:
        raise AssertionError(why)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def show(interval):
    with localcontext() as ctx:
        ctx.prec = 35
        return [str(Decimal(v.numerator)/Decimal(v.denominator)) for v in interval]


def run(repo, out):
    base = repo/'research/moonshot-005-program/results'
    here = Path(__file__).resolve().parent
    for path,digest in json.loads((here/'SOURCE-PINS.json').read_text()).items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
    g = load(base/'bit-coupled-native-geometric-cycle-source/review-c/check.py', 'independent_field')
    price = load(base/'kappa-significant-gain-screen/root-review/check.py', 'reviewed_price')
    E = np.array([[g.power(a,d) for d in range(3)] for a in range(1,10)], dtype=np.uint8)
    need(all(g.rank(E[list(rows)]) == 3 for rows in itertools.combinations(range(9),3)), 'every three marked outputs recover the sum')
    P = g.mm(E,np.hstack([np.eye(3,dtype=np.uint8)]*3))
    L = np.eye(9,dtype=np.uint8)[:6]
    A = np.vstack([P,L])
    need(g.rank(P) == 3 and g.rank(A) == 9, 'rank loss and full complement')
    need(g.rank(A[:-1]) == 8, 'one missing complement loses information')
    T = A.copy()
    appended = []
    for row in range(15):
        column = np.eye(15,dtype=np.uint8)[:,row:row+1]
        if g.rank(np.hstack([T,column])) > T.shape[1]:
            T = np.hstack([T,column]); appended.append(row)
        if T.shape[1] == 15:
            break
    need(T.shape == (15,15) and len(appended) == 6, 'invertible owned extension')
    inverse = g.invert(T)
    need(np.array_equal(g.mm(inverse,A),np.vstack([np.eye(9,dtype=np.uint8),np.zeros((6,9),dtype=np.uint8)])), 'restore originals and zero added owners')
    binary = np.array([[int(g.M[T[r//6,c//6],1<<(c%6)])>>(r%6)&1 for c in range(90)] for r in range(90)],dtype=np.uint8)
    reduced = binary.copy(); ops = []
    def add(target,source):
        reduced[target] ^= reduced[source]; ops.append([target,source])
    for c in range(90):
        choices = np.flatnonzero(reduced[c:,c])
        need(len(choices)>0,'binary pivot')
        row = c+int(choices[0])
        if row != c:
            add(c,row);add(row,c);add(c,row)
        for row in range(90):
            if row != c and reduced[row,c]:
                add(row,c)
    need(np.array_equal(reduced,np.eye(90,dtype=np.uint8)), 'binary reduction')
    replay = np.eye(90,dtype=np.uint8)
    for target,source in reversed(ops):
        replay[target] ^= replay[source]
    need(np.array_equal(replay,binary), 'exact forward whole-record ADD word')
    old_n = {1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    old_h = {2:1,4:25,6:1,8:410}
    old_gap = price.hist((36,old_h),(-36,old_n),(111,price.wrapper(9)))
    allowance = price.hist((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}))
    for j in range(1,9):
        allowance[7*j+1] += F(37,3); allowance[7*j] -= F(37,3)
    Q0 = {1:F(4451,8),2:F(7213,16),4:F(24)}
    def margin(k,q,e,m):
        h = price.hist((1,allowance),(-1,Q0),(-F(q,3840),{8:1}),(-F(e,3840),{6:1}))
        if m is not None:
            h = price.hist((1,h),(F(1,36*(m-1)),old_gap))
        return price.moment(h,k)
    table = []
    for kappa in ['.005','.0043']:
        k = F(kappa)
        for m in [870,None]:
            for e in [0,16,96,192]:
                lo,hi = margin(k,0,e,m); p8 = price.power(8,k)
                cap = (3840*lo/p8[1],3840*hi/p8[0])
                integer = cap[0].numerator//cap[0].denominator
                need(cap[1] < integer+1 and margin(k,integer,e,m)[0] > 0 and margin(k,integer+1,e,m)[1] < 0, 'strict integer return cap')
                table.append({'kappa':kappa,'m':m,'extra_field_exports':e,'return_cap':integer,
                              'continuous_cap':show(cap),'exact_cap_interval':[str(x) for x in cap]})
    at = lambda k,m,e:next(x for x in table if (x['kappa'],x['m'],x['extra_field_exports']) == (k,m,e))
    need(at('.005',870,0)['return_cap'] == 34688 and at('.005',870,96)['return_cap'] == 34615, 'retained and one-complement caps')
    need(margin(F('.005'),34560,192,None)[1] < 0, 'two six-dimensional component complements fail even the limiting floor')
    need(margin(F('.005'),34688,96,870)[1] < 0, 'omitting the complement price is detected')
    out.mkdir(parents=True,exist_ok=True)
    matrices = {'P':P.tolist(),'L':L.tolist(),'T':T.tolist(),'T_inverse':inverse.tolist(),
                'completion_unit_rows':appended,'binary_elimination_adds':ops}
    (out/'COMPILER.json').write_text(json.dumps(matrices,indent=2)+'\n')
    result = {'status':'PASS_PAID_EARLY_H_COMPLEMENT_COMPILER_AND_PRICE',
              'example_input_fields':9,'example_output_rank':3,'extra_fields_per_component':6,
              'exact_binary_ADD_per_direction':len(ops),
              'sixteen_copy_replacement_ADD_forward_and_inverse':32*len(ops),
              'sixteen_copy_extra_field_exports':96,'sixteen_copy_extra_binary_INIT_MOVE_CLEAR_each':576,
              'extra_MOVE_gap':6,'movement_caps':table,'full_source_word_constructed':False,
              'all_other_costs_retained':True,'new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],len(ops),34615,flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    run(args.repo.resolve(),args.out.resolve())
