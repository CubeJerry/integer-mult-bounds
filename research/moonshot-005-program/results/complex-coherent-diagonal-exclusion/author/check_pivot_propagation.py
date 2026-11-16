#!/usr/bin/env python3
"""Exact source checks for the universal column-propagation argument."""
from pathlib import Path
import argparse, hashlib, itertools, json
import sympy as s

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    I=s.eye(16);Z=s.zeros(16);P=s.zeros(16);phase=s.eye(16);X=s.zeros(16)
    for j in range(16):
        P[(j>>1)|((j&1)<<3),j]=1
        phase[j,j]=-1 if(j&13)==13 else 1
        X[j^2,j]=1
    tidy=lambda M:M.applyfunc(s.expand)
    C=tidy(((1+s.I)*I+(1-s.I)*X)/2);S=phase*P;A=tidy(C*S);A2=tidy(A*A)
    Da=s.diag(*[s.I if j&1 else 1 for j in range(16)]);Db=s.diag(*[s.I if j&2 else 1 for j in range(16)])
    assert tidy(A*Db)==tidy(Da*A)
    support=[]
    for j in range(16):
        ys=[i for i in range(16)if A2[i,j]!=0]
        assert len(ys)==4
        ab={(i&1,(i>>1)&1)for i in ys};assert ab==set(itertools.product(range(2),repeat=2))
        support.append(ys)
    # The local column-support statement is identical for all16 columns. Its
    # tensor consequence at every width follows by sums of freely chosen bits.
    sectors={V:sorted({(sum(u)%4,sum(v)%4)for u in itertools.product(range(2),repeat=V)for v in itertools.product(range(2),repeat=V)})for V in range(1,9)}
    assert all(len(sectors[V])==16 for V in range(3,9))
    assert len(sectors[1])==4 and len(sectors[2])==9
    # Literal non-diagonal ordinary escape from the propagation lemma.
    Za=Da**2;H=tidy(A2.conjugate().T*Za*A2)
    assert tidy(H*H)==I
    assert all(sum(H[i,j]!=0 for i in range(16))==1 for j in range(16))
    assert H!=s.diag(*list(H.diagonal()))
    Pplus=(I+Za)/2;Qminus=(I-H)/2
    assert Qminus.rank()==8 and tidy(Pplus*A2*Qminus)==Z
    assert tidy(A2*H)==tidy(Za*A2)
    # Exact clock parity and phase-safe unique-path support facts.
    Xc=s.zeros(16)
    for j in range(16):Xc[j^4,j]=1
    Cc=tidy(((1+s.I)*I+(1-s.I)*Xc)/2)
    Dc=s.diag(*[s.I if j&4 else 1 for j in range(16)])
    supp=lambda M:M.applyfunc(lambda x:s.Integer(x!=0))
    clock_checks=[]
    for theta in range(4):
        h=tidy(S.conjugate().T*Db**theta);HH=tidy(h*A);vv=tidy(A*HH)
        assert HH==tidy(Dc**theta*Cc)
        vsize=2 if theta%2 else 1
        assert all(sum(z!=0 for z in row)==vsize for row in vv.tolist())
        for label,left,expected in [('H',HH,4),('v',vv,4 if theta%2 else 2)]:
            paths=supp(left)*supp(A)
            assert all(z in(0,1)for z in paths)
            assert all(sum(row)==expected for row in paths.tolist())
        clock_checks.append({'theta':theta,'H_exact_Dc_theta_Cc':True,'v_support':vsize,'H_d_A_unique_paths_support4':True,'v_d_A_unique_paths_support':4 if theta%2 else 2})
    # Free noncommutative ordered formulas after the sole transport a F(y)=F(x)a.
    aa=s.Symbol('a',commutative=False)
    sb,tb,ub,sa,ta,ba,ca,da,ea,fb,gb,vv,hh=s.symbols('sb tb ub sa ta ba ca da ea fb gb v h',commutative=False)
    q=s.Matrix(3,3,lambda i,j:s.Symbol(f'q{i}{j}',commutative=False))
    L=s.Matrix([[aa,0,0],[1,aa,0],[0,0,1]])
    pre=s.Matrix([[sa*aa**2,-sa*aa**3+ba*vv,ca*aa],[sb*aa+ta*aa**2,-sb*aa**2-ta*aa**3+sb*0+da*vv,ea*aa],[ub*aa,-ub*aa**2+fb*hh*aa,gb]])
    # b(y) h a and c(y) terms in row1 are low-support and may be included as
    # independent symbols; they cannot affect the8/16-support extraction.
    low1,low2=s.symbols('low1 low2',commutative=False);pre[1,1]+=low1;pre[1,2]+=low2
    E=tidy(pre*q*L)
    def grade_term(expr):
        # Source degree of the unclocked terms only; clocked terms are removed.
        if any(expr.has(v)for v in (vv,hh,low1,low2)):return None
        return sum(int(z.exp)if z.is_Pow and z.base==aa else int(z==aa)for z in s.Mul.make_args(expr))
    def part(expr,k):return s.Add(*(z for z in s.Add.make_args(s.expand(expr))if grade_term(z)==k))
    V=s.Matrix([sa,ta,0]);W=s.Matrix([0,sb,ub])
    expected1=V*aa**2*q[0,1]*aa-W*aa**2*q[1,1]*aa
    expected0=V*(aa**2*q[0,0]*aa-aa**3*q[1,1])-W*aa**2*q[1,0]*aa
    for r in range(3):
        assert s.expand(part(E[r,1],3)-expected1[r])==0
        assert s.expand(part(E[r,0],3)-expected0[r])==0
    for r in range(3):
        for c in range(3):
            expected=-V[r]*aa**3*q[1,c]*aa if c in (0,1)else 0
            assert s.expand(part(E[r,c],4)-expected)==0
    # Residual first-column bank1 case, including the often-missed c term.
    bb,cc=s.symbols('b c',commutative=False)
    Hh=s.Symbol('H',commutative=False)
    residual=s.Matrix([[0,ba*vv,ca*aa],[ta*aa**2,-ta*aa**3+bb*Hh+da*vv,cc+ea*aa],[0,fb*Hh,gb]])
    Er=tidy((residual*q*L).subs({q[0,1]:0,q[1,2]:0}))
    def weighted_degree(expr,odd):
        total=0
        for fac in s.Mul.make_args(expr):
            if fac==aa or fac==Hh:total+=1
            elif fac==vv:total+=int(odd)
            elif fac.is_Pow and fac.base==aa:total+=int(fac.exp)
        return total
    def wp(expr,k,odd):return s.Add(*(z for z in s.Add.make_args(s.expand(expr))if weighted_degree(z,odd)==k))
    for odd in(False,True):
        assert s.expand(wp(Er[1,2],0,odd)-cc*q[2,2])==0
        assert s.expand(wp(Er[2,2],0,odd)-gb*q[2,2])==0
        assert s.expand(wp(Er[2,0],0,odd)-gb*q[2,1])==0
        assert s.expand(wp(Er[1,2],2,odd)-ta*aa**2*q[0,2])==0
        assert wp(Er[0,2],2,odd)==0 and wp(Er[2,2],2,odd)==0
    assert s.expand(wp(Er[1,0],0,True)-cc*q[2,1])==0
    assert s.expand(wp(Er[0,0],0,False)-ba*vv*q[1,1])==0
    assert s.expand(wp(Er[2,0],2,False)-fb*Hh*q[1,0]*aa)==0
    assert s.expand(wp(Er[2,1],2,False)-fb*Hh*q[1,1]*aa)==0
    oddc1=Er[:,1].subs({q[2,1]:0})
    assert s.expand(wp(oddc1[0],2,True)-ba*vv*q[1,1]*aa)==0
    assert s.expand(wp(oddc1[2],2,True)-fb*Hh*q[1,1]*aa)==0
    # Exact commuting-sector determinants establish the individual units used
    # only after the corresponding zero pattern has been proved.
    bt,ct,ft,gt,tt=s.symbols('b c f g t');R=s.Matrix([[0,bt,ct],[tt,1,2],[0,ft,gt]])
    assert s.expand(R.det()+tt*(bt*gt-ct*ft))==0
    x00,x02,x10,x11,x20=s.symbols('q00 q02 q10 q11 q20')
    QQ=s.Matrix([[x00,0,x02],[x10,x11,0],[x20,0,0]])
    assert s.expand(QQ.det()+x02*x11*x20)==0
    # A proper sector function is nonzero as a function but has no width1/2
    # sector3; this is why the universal propagation theorem starts atV3.
    assert all(3 not in {sum(bits)%4 for bits in itertools.product(range(2),repeat=V)}for V in(1,2))
    prog=a.repo/'research/moonshot-005-program';deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-source-transport/author/SOURCE-TRANSPORTED-ROUTING.md','results/complex-source-transport/author/COHERENT-FIRST-PIVOT.md','results/complex-middle-native-interface/author/PROOF.md']
    out={'status':'PASS_AUTHOR_COMPLETE_COHERENT_DIAGONAL_Q_EXCLUSION','scope':'Universal proof in PIVOT-PROPAGATION.md; finite checks are supporting source/formula evidence, not independently reviewed. No caller or kappa.','local_square_column_support':support,'joint_sector_counts_at_widths1_to8':{str(V):len(sectors[V])for V in sectors},'all_width_proof':'Every tensor column has all2^(2V) independent a/b choices, so both mod4 sums attain all16 pairs for everyV>=3.','ordered_eight_and_sixteen_support_formulas':True,'literal_clock_support_and_unique_paths':clock_checks,'residual_ordinary_and_four_support_formulas':True,'forced_sector_determinants':True,'non_diagonal_ordinary_escape':{'rank':8,'annihilation':True,'involution_table':[[i,j,str(H[i,j])]for j in range(16)for i in range(16)if H[i,j]!=0]},'negative_controls':['V1/V2 miss sector3: a nonzero four-sector function need not give column propagation.','A non-diagonal ordinary projector of rank8 annihilates the projected source square; diagonality is essential.'],'source_pins':{str(x):hashlib.sha256((prog/x).read_bytes()).hexdigest()for x in deps},'proof_sha256':hashlib.sha256(Path(__file__).with_name('PIVOT-PROPAGATION.md').read_bytes()).hexdigest()}
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k in('status','joint_sector_counts_at_widths1_to8','ordered_eight_and_sixteen_support_formulas')},indent=2))
if __name__=='__main__':main()
