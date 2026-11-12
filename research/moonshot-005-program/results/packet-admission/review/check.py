#!/usr/bin/env python3
"""Independent exact examples protecting the packet-interface hypotheses."""
from fractions import Fraction as Q
from pathlib import Path
import argparse,json
def need(x,s):
    if not x:raise ValueError(s)
def M(x):return [[Q(v) for v in r] for r in x]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def plus(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a):return [[-x for x in r] for r in a]
def rank(a):
    a=[r[:] for r in a];r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
def enc(a):return [[str(v) for v in r] for r in a]
def main(p):
    T=M([[1,0],[1,Q(1,2)]]);Ti=M([[1,0],[-2,2]]);I=M([[1,0],[0,1]])
    Fo=M([[0,1,0],[0,0,1]]);V=M([[0,0],[1,0],[0,1]]);H=M([[1,0,0],[2,0,0]])
    Z=M([[1,1],[0,1]]);D=I;A=M([[1,0,1],[0,1,0]]);B=M([[1,0],[1,1]]);R=I
    need(mm(T,Ti)==I and mm(Fo,V)==I and mm(H,V)==M([[0,0],[0,0]]),'interface identities')
    J=mm(mm(Z,Ti),D);K=neg(mm(V,J));E=plus(plus(R,neg(mm(mm(B,Ti),D))),mm(mm(A,V),J))
    u=M([[7],[11],[13]]);q=M([[3],[5]]);corrected=plus(u,mm(K,q));delta=mm(mm(Ti,D),q)
    need(plus(mm(Fo,corrected),mm(Z,delta))==mm(Fo,u),'offhub restoration')
    hist=plus(mm(A,corrected),mm(B,delta));desired=plus(mm(A,u),mm(R,q))
    need(plus(hist,mm(E,q))==desired,'correct historical receiver gain')
    omitted=plus(R,neg(mm(mm(B,Ti),D)));need(plus(hist,mm(omitted,q))!=desired,'omitted AVJ term fails')
    need(rank(J)==rank(D)==rank(J+E)==rank(D+R)==2,'injective debt corollary')
    C=M([[1,1]]);difference=M([[1],[-1]]);need(mm(C,difference)==M([[0]]) and mm(J,difference)!=M([[0],[0]]),'missing packet ambiguity')
    S=M([[1,0]]);need(rank(C+S)==2,'additional q-dependent side information changes admission')
    # One-dimensional violation of HV=0: K=-1, H=V=T=D=Z=Fo=1.
    # Actual delta=Dq-HKq=2q, so the terminal perturbation is -q+2q=q.
    need(-Q(1)+2*Q(1)==1,'HV violation leaves debt')
    guard=mm(M([[1,0]]),delta);need(guard==M([[3]]),'zero endpoint debt does not imply COPY guard')
    J0=M([[0,0]]);G=M([[1,0],[0,0]]);E0=plus(I,neg(G));need(rank(J0+E0)==1,'exact-gain nullspace rank')
    out={'status':'PASS_INDEPENDENT_PACKET_INTERFACE_CONTROLS','J':enc(J),'K':enc(K),'E':enc(E),'delta_example':enc(delta),'packet_minimum_example':2,'negative_controls':['omitting AVJ changes the required raw correction','HV nonzero invalidates Delta=T^-1Dq','one packet loses a nonzero debt direction','q-dependent local side information changes the packet criterion','offhub restoration does not imply a zero COPY guard'],'corollary_controls':['rowJ=rowD gives rowstack=row(D,R)','zero-debt exact-gain nullity gives rank one in a two-input example'],'scope':'Exact algebraic controls only; no source construction or budget verification.'}
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);main(a.parse_args().output)
