#!/usr/bin/env python3
"""Separate exact Q(i) matrix and regular-representation controls."""
from pathlib import Path
from itertools import permutations,product
from argparse import ArgumentParser
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy import QQ_I


def require(v,msg):
    if not v: raise ValueError(msg)


def dm(v):return DomainMatrix.from_Matrix(v).convert_to(QQ_I).to_sparse()

def block(arr):return arr[0][0].hstack(*arr[0][1:]).vstack(*[r[0].hstack(*r[1:]) for r in arr[1:]])

def matrix_action(points,action):
    M=sp.zeros(len(points));lookup={t:j for j,t in enumerate(points)}
    for j,p in enumerate(points):
        dest,coeff=action(p);M[lookup[tuple(dest)],j]=coeff
    return dm(M)

def support(A):
    a=A.to_Matrix();n=a.rows
    rows=[sum(x!=0 for x in a.row(i)) for i in range(n)];cols=[sum(x!=0 for x in a.col(i)) for i in range(n)]
    require(len(set(rows+cols))==1,'equal support size');v=rows[0]
    require(all(x==0 or sp.expand(x*sp.conjugate(x)*v)==1 for x in a),'equal coefficient modulus')
    # A regular pointwise row group after dephasing is the character table
    # of an elementary abelian 2-group, up to row and column permutations.
    colsets={tuple(i for i in range(n) if a[i,j]!=0) for j in range(n)}
    if len(colsets)*v!=n: raise ValueError('non-partitioned column supports')
    phases=[x for x in a if x!=0]
    require(all(sp.simplify((x/phases[0])**4)==1 for x in set(phases)),'common phase up to a root of unity')
    for rr in colsets:
        cc=[j for j in range(n) if tuple(i for i in range(n) if a[i,j]!=0)==rr]
        require(len(cc)==v,'square Walsh block')
        forms={tuple(sp.simplify(a[i,j]*a[rr[0],cc[0]]/(a[i,cc[0]]*a[rr[0],j])) for j in cc) for i in rr}
        require(len(forms)==v and all(x in (-1,1) for row in forms for x in row),'dephased Walsh signs')
        require(all(tuple(x*y for x,y in zip(f,g)) in forms for f in forms for g in forms),'closed character group')
    return v

def swaporder(p,r,s):
    x=list(p);x[r],x[s]=x[s],x[r];return tuple(x)

def check():
    points=list(product(range(2),repeat=4)); eye=dm(sp.eye(16));z=eye*QQ_I.zero;half=QQ_I(1,0)/QQ_I(2,0)
    sw=lambda i,j:matrix_action(points,lambda p:(swaporder(p,i,j),1))
    R=matrix_action(points,lambda p:((p[1],p[2],p[3],p[0]),(-1)**(p[0]*p[1]*p[3])))
    X=matrix_action(points,lambda p:((p[0],p[1]^1,p[2],p[3]),1))
    a=(eye*QQ_I(1,1)+X*QQ_I(1,-1))*half*R;ai=dm(a.to_Matrix().H)
    s,s1,s2,h=sw(2,3),sw(0,3),sw(0,1),sw(1,3);r=sw(1,2)*sw(0,1)
    q=a*s*ai
    require(ai*a==eye and ai*s*a==s1 and ai*s1*a==s2,'exact source, transports')
    require(support(q)==4 and support(a*s1*ai)==1,'nonmonomial conjugation and axis control')
    qcol=[[''.join(map(str,points[j])),str(q.to_Matrix()[j,0])] for j in range(16) if q.to_Matrix()[j,0]!=0]
    cls=[support(w) for w in [a,a**2,a**3,a**4,a*s*a,a**3*s2*a,a**2*h*a,a**2*s2*h*a]]
    require(cls==[2,4,8,16,4,4,2,2],'source class sizes')
    L=block([[a,z,z],[eye,a,z],[z,z,eye]]);U=block([[a,-a**2,z],[z,a,z],[z,z,eye]])
    Oi=block([[eye,z,z],[-eye,eye,z],[-eye,eye,eye]])
    rows=[]
    for sign in [-1,1]:
        S=s*QQ_I(sign,0);P=(eye+S)*half;N=eye-P;P1=(eye+s1*QQ_I(sign,0))*half;P2=(eye+s2*QQ_I(sign,0))*half;N2=eye-P2
        C=block([[P,z,-N],[P,eye,-N],[N,z,P]])
        for label,d,d1,e,g,v,k in [('transport',s,s1,r,h,r+s2,h),('changed',h,r,s2,h,r+s2,s)]:
            K=block([[d,e,g],[z,d1,v],[z,z,k]]);M=Oi*L*C*K*U
            row=M.extract(list(range(32,48)),list(range(48)))
            require(row==block([[d*a,-d*a**2+e*a+a*d1*a,g+a*v+S*k]]),'forward')
            wanted=block([[z,z,eye]]);ptr=block([[-k*N*ai,-k*P,k*P]])
            require(ptr*M==wanted and k*k==eye,'pullback identity by left multiplication')
            require(block([[-k*P*ai,-k*P,k*P]])*M!=wanted,'swapped inverse projector rejected')
            require((a*d1==d*a)==(label=='transport'),'transport condition');rows.append([sign,label])
        V=P2+N2*h;J=N2*h*N2;T=J*QQ_I(5,0)-J**3*QQ_I(4,0);Vi=P2+T*(N2-N2*h*P2)
        Q=block([[eye,z,Vi],[z,V,z],[eye,z,z]]);E=Oi*L*C*U*Q*L
        rhs=block([[-a*N*a,-a**3*P2*a,a**2*P1*Vi],[a**2*P2-N*a+a**2*N2*h,a**2*N2*h*a,a*P1*Vi],[a**2+S*a,z,a*Vi]])
        require(E==rhs and V*Vi==Vi*V==eye,'all-input benchmark')
        require(E.extract(list(range(16)),list(range(16,32)))+a**4*half==-(a**3*s2*a)*QQ_I(sign,0)*half,'quartic coefficient')
    perm=list(permutations(range(3)));I6=dm(sp.eye(6));t=matrix_action(perm,lambda p:(swaporder(p,0,1),1));w=matrix_action(perm,lambda p:(swaporder(p,1,2),1))
    for sign in [-1,1]:
        P=(I6+t*QQ_I(sign,0))*half;N=I6-P;J=N*w*N;T=J*QQ_I(5,0)-J**3*QQ_I(4,0)
        V=P+N*w;Vi=P+T*(N-N*w*P)
        require(J*T==T*J==N and V*Vi==Vi*V==I6,'faithful regular representation: exact group algebra identity')
        require(J**2!=N,'compressed transposition is not an involution')
    return {'status':'PASS_INDEPENDENT_PULLBACK_AND_BENCHMARK','arithmetic':'exact Gaussian rationals',
       'forward_inverse_triangular_tests':rows,'AsA_inverse_on_0000':qcol,'eight_support_sizes':cls,
       'all_input_width_one_columns_per_sign':48,'S3_faithful_regular_dimension':6,
       'negative_controls':['swapped inverse projector','transport identity fails for changed sample','other conjugated axis monomial','compressed transposition does not square to N']}

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=check();a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
