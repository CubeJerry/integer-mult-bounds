"""Exact phase-retaining three-head Walsh-monomial group (512 x 168).

All matrices fix the zero Walsh frequency with eigenvalue one, so no scalar
phase quotient is taken. A group coefficient identity tensors literally.
"""
import itertools

IDP=tuple(range(7));ZERO=(0,)*7;ONE=(ZERO,IDP)
def app(A,v):
    x=0
    for j,c in enumerate(A):
        if (v>>j)&1:x^=c
    return x
def rank(vs):
    piv={}
    for v in vs:
        while v:
            j=v.bit_length()-1
            if j not in piv:piv[j]=v;break
            v^=piv[j]
    return len(piv)
def compose(p,q):return tuple(p[j] for j in q)
def inverse_perm(p):return tuple(p.index(j) for j in range(7))
def mul(g,h):
    u,p=g;v,q=h;pi=inverse_perm(p)
    return tuple((u[j]+v[pi[j]])%4 for j in range(7)),compose(p,q)
def inv(g):
    u,p=g;pi=inverse_perm(p)
    return tuple((-u[p[j]])%4 for j in range(7)),pi
def power(g,n):
    if n<0:g,n=inv(g),-n
    z=ONE
    while n:
        if n&1:z=mul(z,g)
        g=mul(g,g);n>>=1
    return z
def gaussian(v):return tuple((v&j).bit_count()%2 for j in range(1,8)),IDP
def linear(A):return ZERO,tuple(app(A,j)-1 for j in range(1,8))
def all_linear():return [linear(A) for A in itertools.product(range(1,8),repeat=3) if rank(A)==3]
def ordinary(g):
    u,p=g
    return any(u==tuple(2*((v&j).bit_count()%2) for j in range(1,8)) for v in range(8))
def gaussian_rank(g):
    q=g[0];Q=lambda v:0 if not v else q[v-1]
    diag=[Q(1<<i)%2 for i in range(3)];B=[]
    for i in range(3):
        col=diag[i]<<i
        for j in range(3):
            if i!=j:
                delta=Q(1<<i)+Q(1<<j)-Q((1<<i)|(1<<j));assert delta%2==0
                col|=((delta//2)%2)<<j
        B.append(col)
    return rank(B)
def source():
    S=linear((4,1,2))
    return mul(gaussian(2),S)
def phase_group():
    # Coefficients of q(x)=sum linear_i*x_i+2*sum quadratic_ij*x_ix_j.
    out=[]
    for a in itertools.product(range(4),repeat=3):
        for b in itertools.product(range(2),repeat=3):
            q=[]
            for x in range(1,8):
                xx=[(x>>i)&1 for i in range(3)]
                q.append((sum(a[i]*xx[i] for i in range(3))+2*(b[0]*xx[0]*xx[1]+b[1]*xx[0]*xx[2]+b[2]*xx[1]*xx[2]))%4)
            out.append((tuple(q),IDP))
    assert len(set(out))==512
    return out
def physical(g,m):
    u,p=g;pi=inverse_perm(p);rows=[];phases=((1,0),(0,1),(-1,0),(0,-1))
    for x in range(8):
        row=[]
        for y in range(8):
            re,im=1,0
            for freq in range(1,8):
                pre=pi[freq-1]+1;sg=-1 if ((x&freq).bit_count()+(y&pre).bit_count())%2 else 1
                c,d=phases[u[freq-1]];re+=sg*c;im+=sg*d
            row.append((re,im))
        rows.append(tuple(row))
    return m.M(tuple(rows),3).norm()
