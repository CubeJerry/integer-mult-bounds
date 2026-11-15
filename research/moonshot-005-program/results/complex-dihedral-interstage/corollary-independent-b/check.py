#!/usr/bin/env python3
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
import sympy as s

def main():
    base=Path(__file__).parent
    ap=argparse.ArgumentParser();ap.add_argument('--proof',type=Path,default=base.parents[1]/'root/dihedral-shadow-review/ALL-HEAD-CYCLIC-COROLLARY.md');ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=base/'RESULT.json');ar=ap.parse_args()
    assert hashlib.sha256(ar.proof.read_bytes()).hexdigest()=='badaa718685c53c771b236023cd6ad5aeb6afdfe0376ba6d7fe6fece82bcb81b'
    hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
    sp=importlib.util.spec_from_file_location('all_fixed_head_review',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
    physical=[]
    for d in range(2,6):
        n=1<<d;I=m.eye(n);Xs=[m.monomial([x^(1<<j) for x in range(n)],[0]*n) for j in range(d)]
        Cs=[m.M((I.scale((1,1))+X.scale((1,-1))).a,1).norm() for X in Xs]
        p=[sum(((x>>j)&1)<<((j-1)%d) for j in range(d)) for x in range(n)]
        S=m.monomial(p,[0]*n);A=Cs[1]@S
        assert S@Cs[1]@S.star()==Cs[0]
        assert Cs[0].star()@S@Cs[1]@S==S.power(2)
        C=I;X=I
        for c,x in zip(Cs,Xs):C=C@c;X=X@x
        assert A.power(d)==C and A.power(2*d)==X and A.power(4*d)==I
        rr=[m.gaussian_rank(A.power(k)) for k in range(2*d)]
        assert rr==[min(k,2*d-k) for k in range(2*d)]
        physical.append({'heads':d,'all_source_columns':n,'actual_gauge':True,'physical_power_identities':True,'gaussian_rank_cycle':rr})
    auxiliary=[]
    for d in range(2,11):
        n=2*d;X=s.zeros(n);T=s.zeros(n)
        for j in range(n):X[(j+1)%n,j]=1;T[(d-1-j)%n,j]=1
        P=s.diag(*([1]*d+[-1]*d))
        assert T*T==s.eye(n) and T*X*T==X.inv() and T*P==P*T
        rr=[(X**k-P*X**k*P).rank() for k in range(n)]
        assert rr==[2*min(k,n-k) for k in range(n)]
        auxiliary.append({'heads':d,'auxiliary_dimension':n,'power_difference_ranks':rr})
    out={'status':'PASS_INDEPENDENT_ALL_FIXED_HEAD_SHADOW_COROLLARY_CONTROLS',
         'reviewed_proof_sha256':hashlib.sha256(ar.proof.read_bytes()).hexdigest(),
         'helper_sha256':hashlib.sha256(hp.read_bytes()).hexdigest(),
         'actual_source_checks':physical,'dihedral_checks':auxiliary,
         'scope':'Independent universal proof review plus finite exact source/rank diagnostics; fixed d only, full spectator volume retained, no new kappa.'}
    ar.out.parent.mkdir(parents=True,exist_ok=True);ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
