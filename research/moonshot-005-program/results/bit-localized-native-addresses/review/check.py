#!/usr/bin/env python3
"""Independently compute native address projectors and Smith gluing groups."""
import argparse
from collections import Counter
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

NATIVE=("research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz","51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78")
ATLAS=("research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz","ef8611b33835a799193e8aec4f615486d73f5743558997de0262bceb3ae9eb3c")
I=np.eye(8,dtype=np.int64)

def read(base,source):
    data=(base/source[0]).read_bytes()
    if hashlib.sha256(data).hexdigest()!=source[1]:
        raise ValueError(source[0])
    return json.loads(gzip.decompress(data))

@lru_cache(None)
def gram_inverse(key):
    mat=Matrix(key)
    if not mat.det():
        return None
    inv=mat.inv()
    d=math.lcm(*(int(a.q) for a in inv))
    return np.array(d*inv,dtype=np.int64),d

def projector(rows,r):
    if r in (0,8):
        return (I.copy() if r else 0*I),1
    basis=[]
    for v in rows:
        M=np.array([*basis,v],dtype=np.int64)
        g=M@M.T
        inverse=gram_inverse(tuple(tuple(map(int,z)) for z in g))
        if inverse is None:
            continue
        basis.append(v)
        if len(basis)==r:
            break
    if len(basis)!=r:
        raise ValueError("rational span dimension")
    num,d=inverse
    E=M.T@num@M
    c=math.gcd(d,*map(int,E.flat))
    E,d=E//c,d//c
    V=np.array(rows,dtype=np.int64)
    if not np.array_equal(V@E,d*V) or not np.array_equal(E@E,d*E):
        raise ValueError("span or idempotence")
    return E,d

def group(E,d):
    if d==1:
        return ()
    sm=smith_normal_form(Matrix(E.tolist()),domain=ZZ).diagonal()
    orders=[d//math.gcd(d,int(a)) for a in sm]
    return tuple(sorted(t for t in orders if t>1))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    args=p.parse_args()
    layout,native=read(args.repo,ATLAS),read(args.repo,NATIVE)
    roots=np.array(layout['root_table'],dtype=np.int64)
    stats,denoms={},{}
    def record(name,rows):
        counts,ds=Counter(),Counter()
        matrices=[]
        for r,basis in rows:
            E,d=projector(basis,r)
            orders=group(E,d)
            if 12%d or math.lcm(*orders)!=d or len(orders)>min(r,8-r):
                raise ValueError("sharp lattice bound")
            counts[','.join(map(str,orders)) or 'trivial']+=1
            ds[d]+=1
            matrices.append(E*(12//d))
        stats[name],denoms[name]=dict(counts),dict(ds)
        return matrices
    L=record('L',((1,[v]) for v in roots))
    H=record('H',((2,roots[g]) for g in layout['A2']))
    D=record('D',((4,roots[g]) for g in layout['D4']))
    f=native['frames']
    ks=sorted(f,key=int)
    native_p=dict(zip(ks,record('native',((f[k]['dim'],f[k]['B']) for k in ks))))
    for j in range(111):
        if not np.array_equal(native_p[str(native['start'][j])],L[j]):
            raise ValueError("native entrance")
    pairs={pair:h for h,m in enumerate(layout['A2']) for pair in itertools.combinations(sorted(m),2)}
    flags=0
    for k,m in enumerate(layout['D4']):
        if not np.array_equal(D[k]+D[layout['dual_D4'][k]],12*I):
            raise ValueError("dual")
        hs={pairs[pair] for pair in itertools.combinations(sorted(m),2) if pair in pairs}
        if len(hs)!=16:
            raise ValueError("D flags")
        for h in hs:
            if not np.array_equal(H[h]@D[k],12*H[h]) or not np.array_equal(D[k]@H[h],12*H[h]):
                raise ValueError("two-sided nesting")
            flags+=1
    if flags!=50400 or math.lcm(*(x for ds in denoms.values() for x in ds))!=12:
        raise ValueError("catalogue coverage")
    E,d=projector([[1,2,0,0,0,0,0,0]],1)
    if group(E,d)!=(5,):
        raise ValueError("out-of-catalogue control")
    res={'source_sha256':[NATIVE[1],ATLAS[1]],'gluing_invariant_orders':stats,
         'reduced_denominators':denoms,'two_sided_flags':flags,
         'sharp_actual_address_primes':[2,3],'out_of_catalogue_control':[5]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print(stats)

if __name__=='__main__':
    main()
