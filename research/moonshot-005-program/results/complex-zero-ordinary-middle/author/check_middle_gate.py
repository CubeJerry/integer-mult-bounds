#!/usr/bin/env python3
"""Exact all-column controls for the zero-ordinary middle and its gate."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
import sympy as s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
    hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
    sp=importlib.util.spec_from_file_location('middle_gate_dyadic',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
    r,q,u,c,d,ss,tc,td,a=s.symbols('r q u c d ss tc td a',commutative=False)
    Q=s.Matrix([[r-ss,q+u,c],[ss,d,0],[r,q,c]])
    TQ=s.Matrix([[0,ss,tc],[0,td,0],[0,ss,tc]])
    K0=s.Matrix([[1,0,-1],[0,0,0],[1,1,-1]]);K1=s.Matrix([[0,0,1],[1,0,-1],[0,0,0]])
    assert all(s.expand(v)==0 for v in K0*Q*K0+K1*TQ*K1)
    K=K0+a*K1;expected=s.Matrix([[a*r-ss,a*q+u,a*c],[-a*ss,a*u,0],[0,d+u,0]])
    assert all(s.expand(v)==0 for v in K*Q-expected)
    E1=s.eye(3);E1[0,2]=-1;E2=s.eye(3);E2[1,0]=1
    assert all(s.expand(v)==0 for v in E2*E1*Q-s.Matrix([[-ss,u,0],[0,d+u,0],[r,q,c]]))
    I=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8);xa=m.monomial([j^1 for j in range(8)],[0]*8)
    cb=m.M((I.scale((1,1))+xb.scale((1,-1))).a,1).norm();xc=m.monomial([j^4 for j in range(8)],[0]*8);cc=m.M((I.scale((1,1))+xc.scale((1,-1))).a,1).norm()
    S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=cb@S;H=S.star();SS=xb@S
    assert A@H@A==SS and A@SS@A==cb@cc@xa
    cases=[]
    for V in (1,2):
        aa,hh,sv=A.tp(V),H.tp(V),SS.tp(V);ii,zz=m.eye(aa.n),m.zero(aa.n);neg=lambda x:x.scale((-1,0));bb=aa@sv@aa
        kk=m.block([[ii,zz,aa+neg(ii)],[aa,zz,neg(aa)],[ii,ii,neg(ii)]])
        q0=m.block([[neg(sv),hh,ii],[sv,ii,zz],[zz,hh,ii]])
        q0i=m.block([[neg(sv.star()),zz,sv.star()],[ii,ii,neg(ii)],[neg(hh),neg(hh),ii+hh]])
        q1=m.block([[ii+neg(sv),hh+ii,ii],[sv,zz,zz],[ii,hh,ii]])
        q1i=m.block([[zz,sv.star(),zz],[ii,ii,neg(ii)],[neg(hh),neg(sv.star())+neg(hh),ii+hh]])
        assert q0@q0i==m.eye(3*aa.n) and q0i@q0==m.eye(3*aa.n)
        assert q1@q1i==m.eye(3*aa.n) and q1i@q1==m.eye(3*aa.n)
        m0=kk@q0@kk
        expect=m.block([[aa,aa,neg(sv@aa)+neg(aa)],[neg(aa@sv),zz,neg(bb)+aa@sv],[aa,zz,neg(aa)]])
        assert m0==expect
        m1=kk@q1@kk
        low=m.block([[aa.scale((3,0)),aa,neg(sv@aa)+aa.scale((-3,0))],[neg(aa@sv),zz,aa@sv],[aa,zz,neg(aa)]])
        high=m.block([[zz,zz,aa.power(2)],[aa.power(2),zz,neg(bb)+neg(aa.power(2))],[zz,zz,zz]])
        assert m1==low+high
        assert m.gaussian_rank(bb)==2*V
        # Reproduce the actual in-place Q(I,I) chronology as a block matrix.
        def addmat(dst,src,coef):
            blocks=[[ii if i==j else zz for j in range(3)] for i in range(3)];blocks[dst][src]=coef;return m.block(blocks)
        G1=addmat(2,0,ii);G2=addmat(2,1,hh);G3=m.diagonal([sv,ii,ii]);G4=addmat(1,2,ii);G5=addmat(1,0,neg(ii));swap=m.block([[zz,ii,zz],[ii,zz,zz],[zz,zz,ii]])
        assert swap@G5@G4@G3@G2@G1==q1
        # A singular middle is a countercontrol to the unit hypothesis.
        singular=m.block([[zz,ii,zz],[zz,zz,zz],[zz,zz,zz]])
        sm=kk@singular@kk
        slow=m.block([[aa,zz,neg(aa)],[zz,zz,zz],[aa,zz,neg(aa)]])
        shigh=m.block([[zz,zz,zz],[aa.power(2),zz,neg(aa.power(2))],[zz,zz,zz]])
        assert sm==slow+shigh
        left=m.block([[ii,zz,neg(ii)],[zz,zz,zz],[zz,zz,zz]])
        assert left@slow==m.zero(3*aa.n)
        cases.append({'width':V,'all_columns':3*aa.n,'ordinary_units_and_inverses':True,'zero_ordinary_word_decomposition':True,'literal_QII_chronology':True,'singular_middle_negative_control':True})
    out={'status':'PASS_EXACT_ZERO_ORDINARY_MIDDLE_GATE_DIAGNOSTICS','proof_sha256':hashlib.sha256((base/'ZERO-ORDINARY-MIDDLE-GATE.md').read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(hp.read_bytes()).hexdigest(),'universal_noncommutative_classification_checked':True,'all_column_cases':cases,'QII_extra_ordinary_operations':{'weighted_additions_subtractions':4,'head_permutations':3,'role_swaps':1,'new_fields':0,'erasures':0},'two_native_three_role_gaussian_profile':{'1':2,'7':4,'8':2},'scope':'The exact source intermediate is constructed. The ordinary-left-kernel theorem is the written faithful-algebra proof. No independent Gaussian endpoint, complete supplier or new kappa follows.'};(base/'MIDDLE-GATE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
