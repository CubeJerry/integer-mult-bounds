#!/usr/bin/env python3
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from pathlib import Path
import json,sympy as sp
from sympy import QQ_I as K
from check import dm,block,matrix_action,swaporder,require,support

def main():
    p=ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args()
    pin='813cb864c9d3b13ef19096fd61b66846262e9e16f09a261ad086f6a49ec42b6c';require(sha256(q.proof.read_bytes()).hexdigest()==pin,'reviewed version')
    pts=list(product(range(2),repeat=4));I=dm(sp.eye(16));Z=I*K.zero;half=K(1,0)/K(2,0);S=lambda i,j:matrix_action(pts,lambda p:(swaporder(p,i,j),1))
    R=matrix_action(pts,lambda p:((p[1],p[2],p[3],p[0]),(-1)**(p[0]*p[1]*p[3])))
    X=matrix_action(pts,lambda p:((p[0],1-p[1],p[2],p[3]),1));a=(I*K(1,1)+X*K(1,-1))*half*R;ai=dm(a.to_Matrix().H)
    L=block([[a,Z,Z],[I,a,Z],[Z,Z,I]]);U=block([[a,-a**2,Z],[Z,a,Z],[Z,Z,I]])
    Li=block([[ai,Z,Z],[-ai**2,ai,Z],[Z,Z,I]]);Ui=block([[ai,I,Z],[Z,ai,Z],[Z,Z,I]]);T=block([[I,Z,Z],[Z,I,Z],[Z,Z,I]])
    require(L*Li==Li*L==U*Ui==Ui*U==T,'both literal three-native inverses')
    require(L*U*L==block([[Z,-a**4,Z],[a**2,Z,Z],[Z,Z,I]]) and (support(a**4),support(a**2),support(I))==(16,4,1),'sharp all 48 columns')
    for n,b in [(2,a**2),(4,a**4)]:
        require(all((v*sp.conjugate(v)).expand()==sp.Rational(1,2**n) for v in b.to_Matrix() if v!=0),'sharp flat norms')
    def shear(t,s,A):
        M=[[I if i==j else Z for j in range(3)] for i in range(3)];M[t][s]=A;return block(M)
    def ent(A,i,j):return A.extract(list(range(16*i,16*i+16)),list(range(16*j,16*j+16)))
    hs=[S(0,1),S(1,2),S(0,3),S(2,3)];C=shear(0,2,hs[0])*shear(2,1,hs[1])*shear(1,0,hs[2])*shear(2,0,hs[3]);Q=shear(0,1,hs[2])*shear(1,2,hs[3])*shear(2,0,hs[0]);W=L*C*U*Q*L
    ce=lambda i,j:ent(C,i,j);qe=lambda i,j:ent(Q,i,j)
    def inside(t,s):
        return -ce(t,0)*a**2*qe(1,s)+ce(t,0)*a*qe(0,s)+ce(t,1)*a*qe(1,s)+ce(t,2)*qe(2,s)
    require(ent(W,0,1)==a*inside(0,1)*a and ent(W,0,2)==a*inside(0,2) and ent(W,2,1)==inside(2,1)*a,'three actual unrestricted input/output corners')
    require(not ent(W,0,2).is_zero_matrix and not ent(W,2,1).is_zero_matrix,'actual negative nonquartic spectator corners')
    # Distinct projective labels remain distinct under the same Gaussian left/right factors.
    one=hs;two=[x*a*y for x in hs for y in hs];four=[x*a**2*y for x in hs for y in hs]
    require(set(map(support,one))=={1} and set(map(support,two))=={2} and set(map(support,four))=={4},'inner support separation')
    probes=0
    for x,y in product([I,hs[0],hs[1]],repeat=2):
        left=ai*x*ai**2*y*a**4;right=a**4*y*ai**2*x*ai
        for z in (left,right):
            require(all(sp.expand(v*sp.conjugate(v))<=sp.Rational(1,2) for v in z.to_Matrix()),'three-factor inverse cap both sides')
        probes+=2
    q.out.write_text(json.dumps({'status':'PASS_INDEPENDENT_UNRESTRICTED_QUARTIC','source_proof_sha256':pin,'signed_actual_native_columns':48,'sharp_support_sizes':[16,4,1],'noncommuting_unrestricted_corners':3,'inverse_gram_concentration_controls':probes,'negative_control':'two modified spectator corners nonzero, excluding this factorization','scope':'literal controls plus all-width argument in QUARTIC-REVIEW.md'},indent=2)+'\n')
    print('PASS_INDEPENDENT_UNRESTRICTED_QUARTIC')
if __name__=='__main__':main()
