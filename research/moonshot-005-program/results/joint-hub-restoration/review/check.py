#!/usr/bin/env python3
"""Fresh independent rational controls; no author modules."""
from fractions import Fraction as F
from pathlib import Path
import json
def need(b,s):
    if not b:raise ValueError(s)
def M(a):return [[F(x) for x in row] for row in a]
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b,c=F(1)):return [[x+c*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def inv(a):
    n=len(a);r=[list(a[i])+[F(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
        j=next((j for j in range(i,n) if r[j][i]),None);need(j is not None,'invertible fixture');r[i],r[j]=r[j],r[i];c=r[i][i];r[i]=[x/c for x in r[i]]
        for j in range(n):
            if j!=i:c=r[j][i];r[j]=[x-c*y for x,y in zip(r[j],r[i])]
    return [row[n:] for row in r]
def main():
    W=M([[1,0,0],[0,1,0]]);N=M([[0,0,1]]);H=M([[1,0,1],[0,1,1]]);T=M([[1,0],[1,1]]);Z=M([['1/2','1/3'],[0,'1/2']]);Lam=M([[1,0],[0,1]]);Gam=M([[1],[1]])
    u=M([[2],[3],[5]]);q=M([[9],[11]]);hu=mul(H,u);delta=[]
    for i in range(2):delta.append([q[i][0]-hu[i][0]-sum(T[i][j]*delta[j][0] for j in range(i))])
    need(delta==M([[2],[1]]) and delta!=add(q,hu,-1),'chronology and omitted-L mutant');Y=add(mul(W,u),mul(Z,delta));G=add(T,mul(Lam,Z),-1);rhs=add(add(q,mul(Lam,Y),-1),mul(Gam,mul(N,u)),-1);d=mul(inv(G),rhs)
    need(d==delta and add(Y,mul(Z,d),-1)==mul(W,u),'joint restoration');P=add(W,mul(mul(Z,inv(T)),H),-1);v=M([[3],[-3],[7]])
    need(mul(P,v)==M([[0],[0]]) and mul(W,v)!=M([[0],[0]]),'missing-N witness');need(any(x.denominator%7==0 for row in inv(G) for x in row),'dyadic-only inverse rejection')
    # Two raw fields, one correction combination, independent W and N.
    W2=M([[1,0]]);P2=M([[1,-2]]);B2=M([[1,1]]);N2=M([[0,1]]);Rq=M([[1,1]]);u2=M([[3],[5]]);q2=M([[7],[11]])
    Y2=add(mul(P2,u2),mul(B2,q2));restored=add(add(Y2,mul(N2,u2),2),mul(Rq,q2),-1);need(restored==mul(W2,u2),'one raw combination suffices')
    dq=M([[0],[1]]);du=M([[-1],[0]]);need(add(mul(P2,du),mul(B2,dq))==M([[0]]) and mul(W2,du)==M([[-1]]),'restricted-raw necessity sign')
    need(add(mul(P2,M([[1],[0]])),mul(B2,dq))==M([[2]]),'wrong sign negative control')
    # Singular-G example: Y=q; a supplied N=u restores u despite dependent W,N.
    u3=F(5);q3=F(9);Y3=q3;N3=u3;need(N3==u3 and Y3!=u3,'dependent-N exception')
    out={'status':'PASS_FRESH_INDEPENDENT_JOINT_RESTORATION_CONTROLS','chronological_delta':['2','1'],'missing_N_displacement':[3,-3,7],'non_dyadic_inverse_detected':True,'raw_inputs':2,'sufficient_raw_combinations':1,'correct_partial_raw_displacement':[-1,0],'wrong_sign_observation_change':2,'dependent_N_exception_checked':True,'new_complete_kappa':None}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
