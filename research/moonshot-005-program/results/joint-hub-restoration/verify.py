"""Fresh exact rational controls for the reconstructed restoration theorem."""
import argparse
from fractions import Fraction as F
import hashlib,json
from pathlib import Path

def need(v,m):
    if not v: raise ValueError(m)
def M(a): return [[F(v) for v in r] for r in a]
def I(n): return M([[int(i==j) for j in range(n)] for i in range(n)])
def add(a,b,sign=1): return [[x+sign*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def cat(a,b): return [r+s for r,s in zip(a,b)]
def rref(a):
    a=[list(r) for r in a];p=[];k=0
    for j in range(len(a[0])):
        z=next((i for i in range(k,len(a)) if a[i][j]),None)
        if z is None: continue
        a[k],a[z]=a[z],a[k];t=a[k][j];a[k]=[v/t for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                t=a[i][j];a[i]=[v-t*w for v,w in zip(a[i],a[k])]
        p.append(j);k+=1
        if k==len(a): break
    return a,p
def rank(a): return len(rref(a)[1])
def inv(a):
    z,p=rref(cat(a,I(len(a))));need(p[:len(a)]==list(range(len(a))),'invertible')
    return [r[len(a):] for r in z]
def enc(a): return [[str(v) for v in r] for r in a]
def contains(a,b): return rank(a+b)==rank(a)
def main(args):
    checks={};W=M([[1,0,0],[0,1,0]]);H=M([[1,0,1],[0,1,1]]);T=M([[1,0],[1,1]])
    Z=M([[0,1],[1,0]]);Q=M([[1],[1]]);N=M([[0,0,1]]);Lam=I(2);Gam=M([[1],[1]])
    Ti=inv(T);P=add(W,mul(mul(Z,Ti),H),-1);B=mul(mul(Z,Ti),Q);G=add(T,mul(Lam,Z),-1);Gi=inv(G)
    R=add(I(2),mul(mul(Z,Gi),Lam));SN=mul(mul(Z,Gi),Gam);Cq=mul(mul(Z,Gi),Q)
    need(add(mul(R,P),mul(SN,N))==W and mul(R,B)==Cq,'symbolic identities')
    d=rank(P+W)-rank(P);need(d==1 and contains(P+N,W),'one N record')
    v=M([[1],[2],[1]]);need(mul(P,v)==M([[0],[0]]) and mul(W,v)==M([[1],[2]]),'missing N')
    u=M([[1],[2],[3]]);q=M([[7]]);delta=mul(Ti,add(mul(Q,q),mul(H,u),-1));Y=add(mul(W,u),mul(Z,delta))
    wrong=add(mul(Q,q),mul(H,u),-1);need(mul(T,wrong)!=add(mul(Q,q),mul(H,u),-1),'omitted L rejected')
    need(delta==M([[3],[-1]]) and Y==M([[0],[5]]),'version example')
    first=2*q[0][0]-Y[0][0]-Y[1][0]-2*u[2][0];wrong_second=q[0][0]-(Y[1][0]-first)-u[2][0]
    need(wrong_second==2 and wrong_second!=delta[1][0],'premature mutation rejected')
    checks['interacting_two_loans']={'P':enc(P),'G':enc(G),'G_inverse':enc(Gi),'d_min':d,'missing_N_kernel_vector':enc(v),'delta':enc(delta),'unsafe_second_delta':str(wrong_second)}
    W1=M([[1]]);P1=M([[0]]);N1=M([[1]])
    need(rank(W1+W1)-rank(W1)==0 and rank(P1+W1)-rank(P1)==1,'loss not nuisance');need(contains(P1+N1,W1),'dependent N rescue')
    checks['singular_dependent_N']={'H_mod_W_rank':0,'d_min':1,'N':enc(N1),'G':[['0']]}
    W2=M([[1,0]]);H2=M([[0,1],[0,1]]);Z2=M([[1,-1]]);Q2=M([[1],[1]])
    P2=add(W2,mul(Z2,H2),-1);need(P2==W2 and mul(Z2,Q2)==M([[0]]),'cancellation');need(rank(W2+H2)-rank(W2)==1,'H quotient')
    checks['cancelling_nuisance']={'H_mod_W_rank':1,'d_min':rank(P2+W2)-rank(P2)}
    P3=I(2);B3=M([[1,1],[0,0]]);C3=cat(I(2),M([[0,0],[0,0]]));Aq=cat(P3,B3)
    good=cat(M([[0,0]]),M([[1,1]]));bad=cat(M([[0,0]]),M([[1,0]]))
    need(contains(Aq+good,C3) and not contains(Aq+bad,C3),'partial raw criterion')
    vx=M([[-1],[0],[0],[1]]);need(mul(Aq+bad,vx)==M([[0],[0],[0]]) and mul(C3,vx)==M([[-1],[0]]),'negative-sign witness')
    need(mul(Aq+bad,M([[1],[0],[0],[1]]))!=M([[0],[0],[0]]),'positive-sign witness rejected')
    checks['restricted_raw']={'sufficient_Rq':[['1','1']],'insufficient_Rq':[['1','0']],'indistinguishability_vector':enc(vx)}
    need(inv(M([[7]]))==M([[F(1,7)]]),'nondyadic inverse')
    checks['scalar_service']={'G':[['7']],'inverse':[['1/7']],'dyadic':False}
    out={'status':'PASS_FRESH_EXACT_RESTORATION_CONTROLS','coefficient_domain':'Q','proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'checks':checks,'scope':'Finite controls for the quantified proof; no native replacement word or new kappa.'}
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args())
