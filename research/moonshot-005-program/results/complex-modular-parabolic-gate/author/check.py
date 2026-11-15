#!/usr/bin/env python3
"""Exact modular-filtration checks; finite controls, not the universal proof."""
import argparse, hashlib, json, random
from fractions import Fraction as F
from pathlib import Path


def ident(n): return tuple(1 << i for i in range(n))
def add(a,b): return tuple(x^y for x,y in zip(a,b))
def act(a,x):
    out=0
    while x:
        b=x&-x;out^=a[b.bit_length()-1];x^=b
    return out
def mul(a,b): return tuple(act(a,x) for x in b)
def power(a,k):
    out=ident(len(a))
    for _ in range(k):out=mul(out,a)
    return out
def rank(cols):
    piv={}
    for x in cols:
        while x:
            k=x.bit_length()-1
            if k not in piv:piv[k]=x;break
            x^=piv[k]
    return len(piv)
def inverse(a):
    n=len(a);rows=[]
    for i in range(n):rows.append(sum(((a[j]>>i)&1)<<j for j in range(n))|(1<<(n+i)))
    for j in range(n):
        p=next(i for i in range(j,n) if rows[i]>>j&1)
        rows[j],rows[p]=rows[p],rows[j]
        for i in range(n):
            if i!=j and rows[i]>>j&1:rows[i]^=rows[j]
    ri=[r>>n for r in rows]
    return tuple(sum(((ri[i]>>j)&1)<<i for i in range(n)) for j in range(n))
def omega(x,y,d):
    mask=(1<<d)-1
    return (((x&mask)&(y>>d)).bit_count()+((y&mask)&(x>>d)).bit_count())%2

def transvection(v,d):return tuple((1<<j)^(v if omega(v,1<<j,d) else 0) for j in range(2*d))
def is_symp(a,d):
    return all(omega(a[i],a[j],d)==int(abs(i-j)==d) for i in range(2*d) for j in range(2*d))
def parabolic_generators(d):
    out=[];I=ident(2*d)
    for i in range(d):
        a=list(I);a[i]^=1<<(d+i);out.append(tuple(a))
    for i in range(d):
        for j in range(i):
            a=list(I);a[i]^=1<<(d+j);a[j]^=1<<(d+i);out.append(tuple(a))
    for i in range(d):
        for j in range(d):
            if i!=j:
                a=list(I);a[j]^=1<<i;a[d+i]^=1<<(d+j);out.append(tuple(a))
    return out

def crossing(a,d,R=1):
    outs=[bank*2*d+i for bank in range(R) for i in range(d)]
    ins=[bank*2*d+d+i for bank in range(R) for i in range(d)]
    return rank(tuple(sum(((a[j]>>i)&1)<<k for k,i in enumerate(outs)) for j in ins))

def stage(d,R,blocks):
    n=2*d;out=[0]*(n*R)
    for (row,col),a in blocks.items():
        for j,c in enumerate(a):out[col*n+j]^=c<<(row*n)
    return tuple(out)
def diagstage(d,R,values):return stage(d,R,{(i,i):values[i] for i in range(R)})
def native(a,d,R,u,v,square):
    blocks={(i,i):ident(2*d) for i in range(R)}
    blocks[(u,u)]=a;blocks[(v,v)]=a;blocks[(u,v)]=power(a,2) if square else ident(2*d)
    return stage(d,R,blocks)
def shear(g,d,R,u,v):
    blocks={(i,i):ident(2*d) for i in range(R)};blocks[(u,v)]=g
    return stage(d,R,blocks)

def random_symp(rng,d,steps=8):
    a=ident(2*d)
    for _ in range(steps):a=mul(transvection(rng.randrange(1,1<<(2*d)),d),a)
    return a

def admitted_head(d):
    # A=C_b S; the cycle sends b to a. In d=3 the exact source has D_b CZ_ac.
    p=[d-1]+list(range(d-1))
    cols=tuple([1<<p[j] for j in range(d)]+[1<<(d+p[j]) for j in range(d)])
    phase=list(ident(2*d));phase[1]^=1<<(d+1)
    if d>=3:phase[0]^=1<<(d+2);phase[2]^=1<<d
    S=mul(tuple(phase),cols)
    return mul(transvection(1<<1,d),S)

# Small exact Gaussian arithmetic, for the invariant lattice control only.
def z(a=0,b=0):return (F(a),F(b))
def za(x,y):return (x[0]+y[0],x[1]+y[1])
def zn(x):return (-x[0],-x[1])
def zm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def mm(a,b):
    return tuple(tuple(sumz(zm(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def sumz(xs):
    a=z()
    for x in xs:a=za(a,x)
    return a

def lattice_control():
    a=z(F(1,2),F(-1,2));b=z(F(1,2),F(1,2));i=z(0,1)
    C=((b,a),(a,b));D=((z(1),z()),(z(),i))
    B=((a,z()),(a,z(1)));Bi=((z(1,1),z()),(z(-1),z(1)))
    Cp=mm(mm(Bi,C),B);Dp=mm(mm(Bi,D),B)
    assert Cp==((z(1),z(1)),(z(),i))
    assert Dp==((z(1),z()),(i,i))
    assert mm(Bi,B)==((z(1),z()),(z(),z(1)))
    assert any(v.denominator==2 for row in C for x in row for v in x)
    def red(x):
        assert all(v.denominator%2 for v in x)
        return (int(x[0].numerator)%2+int(x[1].numerator)%2)%2
    cr=tuple(sum(red(Cp[row][col])<<row for row in range(2)) for col in range(2))
    dr=tuple(sum(red(Dp[row][col])<<row for row in range(2)) for col in range(2))
    assert rank(cr)==rank(dr)==2
    assert power(cr,2)==power(dr,2)==ident(2)
    rejected=False
    try:red(C[0][0])
    except AssertionError:rejected=True
    assert rejected
    return {'C_integral_basis':[[[str(v) for v in x] for x in row] for row in Cp],
            'D_integral_basis':[[[str(v) for v in x] for x in row] for row in Dp],
            'residue_columns':[cr,dr],'naive_standard_basis_reduction_rejected':True}

def routing_control():
    # J_h for the actual two-bit CZ involution. Its physical matrix is a permutation.
    h=(1,1,1,-1);n=8;Q=[[F(0) for _ in range(n)] for _ in range(n)]
    for j,e in enumerate(h):
        pp=F(1+e,2);pm=F(1-e,2)
        Q[j][j]=Q[j+4][j+4]=pp;Q[j+4][j]=Q[j][j+4]=pm
    assert all(sum(row)==1 for row in Q)
    assert all(sum(Q[i][j] for i in range(n))==1 for j in range(n))
    Q2=[[sum(Q[i][k]*Q[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    assert Q2==[[int(i==j) for j in range(n)] for i in range(n)]
    assert [[4*x for x in row] for row in Q2]!=Q2
    return {'conditional_permutation':True,'omitting_half_rejected':True,'permutation':[next(i for i in range(n) if Q[i][j]) for j in range(n)]}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    here=Path(__file__).resolve().parent
    deps=json.loads((here/'DEPENDENCIES.json').read_text())
    for p in deps['sources']:
        assert hashlib.sha256((args.repo/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
    rng=random.Random(160015);total=0;nat=0;queries=0;word_cases=[]
    for d in range(2,6):
        H=parabolic_generators(d);assert all(is_symp(h,d) and crossing(h,d)==0 for h in H)
        a=admitted_head(d);assert is_symp(a,d) and crossing(a,d)==1 and crossing(power(a,2),d)==2
        for R in (2,3,4):
            for trial in range(12):
                W=ident(2*d*R);budget=0
                for step in range(15):
                    u,v=rng.sample(range(R),2);kind=rng.randrange(4)
                    if kind==0:
                        h=ident(2*d)
                        for _ in range(4):h=mul(rng.choice(H),h)
                        T=shear(h,d,R,u,v);assert crossing(T,d,R)==0
                    elif kind==1:
                        T=native(a,d,R,u,v,bool(rng.randrange(2)))
                        if rng.randrange(2):T=inverse(T)
                        assert crossing(T,d,R)==2;budget+=2;nat+=1
                    elif kind==2:
                        g=random_symp(rng,d);q=crossing(g,d)
                        if rng.randrange(2):T=shear(g,d,R,u,v)
                        else:
                            vals=[ident(2*d) for _ in range(R)];vals[u]=g;T=diagstage(d,R,vals)
                        assert crossing(T,d,R)==q;budget+=q;queries+=1
                    else:
                        vals=[]
                        for bank in range(R):
                            h=ident(2*d)
                            for _ in range(3):h=mul(rng.choice(H),h)
                            vals.append(h)
                        T=diagstage(d,R,vals);assert crossing(T,d,R)==0
                    assert crossing(mul(T,W),d,R)<=crossing(T,d,R)+crossing(W,d,R)
                    W=mul(T,W);assert rank(W)==2*d*R and crossing(W,d,R)<=budget
                    assert crossing(inverse(W),d,R)==crossing(W,d,R)
                    total+=1
                word_cases.append({'d':d,'roles':R,'crossing':crossing(W,d,R),'upper':budget})
        # Sharp two-native cancellation control, over the residue field.
        N=native(a,d,2,0,1,True);endpoint=mul(N,N)
        assert endpoint==diagstage(d,2,[power(a,2),power(a,2)])
        assert crossing(endpoint,d,2)==4
    a=admitted_head(3)
    rr=[crossing(power(a,k),3) for k in range(15)]
    assert rr==[0,1,2,3,3,2,3,3,3,3,2,3,3,2,1] and power(a,15)==ident(6)
    ordinary_mutant=transvection(1,3)
    assert crossing(ordinary_mutant,3)==1
    # Its uncharged crossing would already violate the zero-call bound.
    assert not (crossing(ordinary_mutant,3)<=0)
    result={'status':'PASS_MODULAR_PARABOLIC_CONTROLS','checks':total,'native_checks':nat,'query_checks':queries,
            'word_cases':len(word_cases),'dimensions':[2,3,4,5],'actual_order15_ranks':rr,
            'lattice':lattice_control(),'routing':routing_control(),
            'negative_controls':['nonordinary uncharged stage','naive Gaussian standard-basis reduction','routing without 1/2'],
            'scope':'finite controls for written all-field/all-call theorem; no profitable caller or new kappa'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','checks','native_checks','query_checks','word_cases','actual_order15_ranks')},sort_keys=True))
if __name__=='__main__':main()
