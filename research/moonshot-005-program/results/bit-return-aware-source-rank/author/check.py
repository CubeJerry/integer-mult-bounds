#!/usr/bin/env python3
"""Exact finite minimization of one-source completed return rank."""
from argparse import ArgumentParser
from functools import lru_cache
from itertools import product
from pathlib import Path
from hashlib import sha256
import json


def matrices(p,n,m):
    return [tuple(tuple(v[i*m:(i+1)*m]) for i in range(n))
            for v in product(range(p),repeat=n*m)]


def rank(p,A):
    a=[list(row) for row in A]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        pivot=next((t for t in range(k,len(a)) if a[t][j]%p),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        v=pow(a[k][j]%p,-1,p);a[k]=[(x*v)%p for x in a[k]]
        for t in range(k+1,len(a)):
            v=a[t][j]%p
            a[t]=[(x-v*y)%p for x,y in zip(a[t],a[k])]
        k+=1
        if k==len(a):break
    return k


def join(*A):return tuple(tuple(x for a in A for x in a[i]) for i in range(len(A[0])))
def add(p,A,B):return tuple(tuple((x+y)%p for x,y in zip(a,b)) for a,b in zip(A,B))
def mul(p,A,B,b=2):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B)))%p
                       for j in range(b)) for i in range(len(A)))


def census(p):
    output=matrices(p,2,2);index={A:i for i,A in enumerate(output)}
    fixed=[((),())]+[((1,),(t,)) for t in range(p)]+[((0,),(1,)),((1,0),(0,1))]
    costs=[[[rank(p,join(M,add(p,A,G))) for G in output] for A in output] for M in fixed]
    checked=attainments=0;wrong_return_proxy=0
    for m in range(3):
        Fs=[F for F in matrices(p,m,2) if rank(p,F)==m]
        for ell in (0,1):
            late=matrices(p,ell,2)
            for C in matrices(p,2,m):
                early=[mul(p,C,F) for F in Fs]
                for D in matrices(p,2,ell):
                    corrections=[mul(p,D,L) for L in late]
                    possible={add(p,U,V) for U in early for V in corrections}
                    ids=[index[G] for G in possible]
                    for h,M in enumerate(fixed):
                        rM=rank(p,M);rW=rank(p,join(M,D));rWC=rank(p,join(M,D,C))
                        r=rWC-rW
                        for ia,A in enumerate(output):
                            a=rank(p,join(M,D,A))-rW
                            z=rank(p,join(M,D,C,A))-rWC
                            predicted=rM+z+max(0,r-a)
                            actual=min(costs[h][ia][k] for k in ids)
                            assert actual==predicted,(p,M,A,C,D,predicted,actual)
                            checked+=1
                            attainments+=sum(costs[h][ia][k]==actual for k in ids)
                            if h==0:
                                information=min(rank(p,G) for G in possible)
                                wrong_return_proxy+=information!=actual
    return {'field':p,'fixed_column_spaces':len(fixed),'exact_minima':checked,
            'attaining_distinct_response_matrices':attainments,
            'information_rank_differs_from_return_minimum':wrong_return_proxy}


def strict_controls():
    # z=1 and r-a=1 require two dimensions, not their maximum one.
    A=((0,0),(0,0),(1,0));C=((1,0),(0,1),(0,0))
    Fs=[F for F in matrices(2,2,2) if rank(2,F)==2]
    actual=min(rank(2,add(2,A,mul(2,C,F))) for F in Fs)
    assert actual==2
    # If both physical source transfers vanish modulo fixed columns,
    # retuning cannot change the completed rank, even with late freedom.
    M=((1,),(0,));A2=((0,0),(1,0));C2=((1,),(0,));D2=C2
    vals={rank(2,join(M,add(2,A2,add(2,mul(2,C2,F),mul(2,D2,L)))))
          for F in matrices(2,1,2) if rank(2,F)==1 for L in matrices(2,1,2)}
    assert vals=={2}
    assert not [F for F in matrices(2,3,2) if rank(2,F)==3]
    # A target constraint may forbid the unconstrained optimum.
    I=((1,0),(0,1));allfull=[F for F in matrices(2,2,2) if rank(2,F)==2]
    optimum=min(rank(2,add(2,I,F)) for F in allfull)
    prescribed=((0,1),(1,0))
    assert optimum==0 and rank(2,add(2,I,prescribed))==1
    return {'two_term_lower_bound_example':actual,
            'incorrect_max_only_formula':1,
            'fixed_quotient_zero_transfer_ranks':sorted(vals),
            'm_greater_than_b_rejected':True,
            'unconstrained_minimum':optimum,'prescribed_target_rank':1}


def main():
    ap=ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    result={'status':'PASS_EXACT_RETURN_AWARE_SOURCE_MINIMUM',
            'censuses':[census(2),census(3)],'controls':strict_controls(),
            'proof_sha256':sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),
            'native_rank_improvement_claimed':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
