#!/usr/bin/env python3
"""Independent all-column/rational-chart review. No author checker imports."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sympy as sp

ROOT_PATH = "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
ROOT_SHA256 = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
DONORS = [16, 19, 38, 49, 50, 56, 57]
SCALE = 1 << 160

def need(test, why):
    if not test:
        raise ValueError(why)

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def binary_basis(rows):
    out = {}
    for j, value in enumerate(rows):
        tag = 1 << j
        while value:
            pivot = value.bit_length() - 1
            if pivot in out:
                value ^= out[pivot][0]
                tag ^= out[pivot][1]
            else:
                out[pivot] = (value, tag)
                break
    return out

def solve(basis, target):
    tag = 0
    while target:
        k = target.bit_length() - 1
        if k not in basis:
            return None
        target ^= basis[k][0]
        tag ^= basis[k][1]
    return tag

def combination(rows, tag):
    out = 0
    for j, row in enumerate(rows):
        if tag >> j & 1:
            out ^= row
    return out

def support(row, n=111):
    return [j for j in range(n) if row >> j & 1]

def chart_basis(chart):
    rows = chart["rows"]
    need(all(len(row) == 8 for row in rows), "chart ambient dimension is not eight")
    need(chart["kind"] in ("ann", "span"), "unknown chart kind")
    M = sp.Matrix(rows) if rows else sp.zeros(0, 8)
    if chart["kind"] == "span":
        return tuple(tuple(x) for x in M.rowspace())
    return tuple(tuple(x) for x in M.nullspace())

def finite_control():
    import itertools
    def span(vectors):
        s={0}
        for v in vectors:s|={x^v for x in tuple(s)}
        return sum(1<<v for v in s)
    spaces=sorted({span(S)for d in range(4)for S in itertools.combinations(range(1,8),d)})
    need(len(spaces)==16,'F2^3 subspaces')
    dim={s:s.bit_count().bit_length()-1 for s in spaces}
    join={(s,t):span([v for v in range(8)if(s|t)>>v&1])for s in spaces for t in spaces}
    contained=lambda s,t:s&t==s
    checked=feasible=0;bad_free_grant=None;bad_ignored_grant=None
    for D in spaces:
        sub=[s for s in spaces if contained(s,D)]
        for N,G in itertools.product(sub,repeat=2):
            n=dim[N];NG=join[N,G]
            for W in spaces:
                DW=join[D,W];r=dim[DW]-dim[D]
                for q in range(4):
                    good=[T for T in spaces if dim[T]<=q and contained(N,T)and contained(W,join[D,T])]
                    for E in spaces:
                        checked+=1
                        k=dim[NG&E];z=dim[E&DW]-dim[E&D]
                        actual=max((dim[join[T,G]&E]for T in good),default=None)
                        expected=None if q<n+r else min(dim[E],k+z+q-n-r)
                        need(actual==expected,'fixed-kernel quotient finite mismatch')
                        if actual is not None:
                            feasible+=1
                            wrong=min(dim[E],k+z+q-n-r+dim[G])
                            if wrong!=actual and bad_free_grant is None:
                                bad_free_grant={'D':D,'N':N,'G':G,'W':W,'E':E,'q':q,'actual':actual,'wrong_added_free_seed_dimension':wrong}
                            wrong=min(dim[E],dim[N&E]+z+q-n-r)
                            if wrong!=actual and bad_ignored_grant is None:
                                bad_ignored_grant={'D':D,'N':N,'G':G,'W':W,'E':E,'q':q,'actual':actual,'wrong_omitted_fixed_intersection':wrong}
    need(bad_free_grant is not None and bad_ignored_grant is not None,'negative control missing')
    return {'ambient':'F2^3','all_subspaces':16,'all_valid_cases':checked,'feasible_cases':feasible,
        'free_seed_double_count_rejected':bad_free_grant,'omitted_intersection_rejected':bad_ignored_grant,
        'scope':'finite controls; universal statement is established by the exact complement proof'}

def source_dimensions(repo,wordpath):
    raw=(repo/ROOT_PATH).read_bytes();need(hashlib.sha256(raw).hexdigest()==ROOT_SHA256,'root pin')
    roots=json.loads(raw)['native_roots'];roots=[roots[str(i)]for i in range(111)]if isinstance(roots,dict)else roots
    wb=wordpath.read_bytes();need(hashlib.sha256(wb).hexdigest()=='2586e9eb28e25b241305d4237ffd59914cd2a7ed30bd2aacc193d45107b6e8ac','word pin')
    w=json.loads(wb);raws={n:v[1]for n,v in w['expected'].items()if n.startswith('C')};D=list(raws.values())
    C=[sum(1<<j for j,r in enumerate(roots)if i==j or dot(roots[i],r)==0)for i in range(111)]
    h=C[0]^C[4];W=[v&(h if h>>i&1 else((1<<111)-1)^h)for i,v in enumerate(C)]
    rk=lambda rows:len(binary_basis(rows))
    cap=lambda X,Y:rk(X)+rk(Y)-rk(X+Y)
    R0=0
    for n,v in raws.items():
        if n.startswith('C0_')and n.endswith('_0'):R0^=v
    g=1^R0;need(solve(binary_basis(D),g)is not None,'fixed kernel not actually in D')
    common={'D':rk(D),'W':rk(W),'C':rk(C),'DcapW':cap(D,W),'DcapC':cap(D,C),'DplusWcapC':cap(D+W,C)}
    need(common=={'D':40,'W':15,'C':9,'DcapW':8,'DcapC':5,'DplusWcapC':8},'colored dimensions changed')
    records=[]
    for L in range(1,8):
        N=0
        for n,v in raws.items():
            if n.startswith('C0_')and n.endswith('_1')and int(n.split('_')[1])>=L:N^=v
        n=int(N!=0);q=7+n;r=rk(D+W)-rk(D);z=cap(C,D+W)-cap(C,D);k=cap([N,g],C)
        need(solve(binary_basis(D),N)is not None,'mandatory suffix not in D')
        maximum=min(9,k+z+q-n-r)
        records.append({'depth':L,'mandatory_terminal_hex':hex(N),'fixed_kernel_hex':hex(g),'mandatory_rank':n,'actual_terminal_budget':q,
            'mandatory_plus_kernel_rank':rk([N,g]),'mandatory_plus_kernel_C_intersection':k,'r':r,'z':z,'canonical_cap':maximum})
    need(records[3]['mandatory_plus_kernel_rank']==2 and records[3]['mandatory_plus_kernel_C_intersection']==0 and records[3]['canonical_cap']==3,'depth4 formula')
    need(all(rec['mandatory_rank']==0 and rec['actual_terminal_budget']==7 and rec['canonical_cap']==3 for rec in records[4:]),'zero-terminal depths')
    return {'source_word_sha256':hashlib.sha256(wb).hexdigest(),'common_dimensions':common,'depth_records':records,
        'scope':'Exact coefficient-space premises only; not a delayed-source chronological admission or a bound on gauge-canonical fittings.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result={'status':'PASS_INDEPENDENT_FIXED_KERNEL_QUOTIENT','finite_control':finite_control(),'source_dimensions':source_dimensions(a.repo,a.word),'new_complete_kappa':False}
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'finite_cases':result['finite_control']['all_valid_cases'],'source':result['source_dimensions']['common_dimensions']},sort_keys=True))
if __name__=='__main__':main()

