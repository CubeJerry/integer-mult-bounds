"""Exact binary Clifford data reused from the S027 covariant target author.
Shared author algebra; independent review is recorded separately.
"""
from fractions import Fraction

LAYOUT_PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
def need(value,label):
    if not value: raise ValueError(label)
def rank(rows):
    piv={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k not in piv: piv[k]=x; break
            x^=piv[k]
    return len(piv)
def independent(rows):
    piv={};out=[]
    for row in rows:
        x=row
        while x:
            k=x.bit_length()-1
            if k not in piv: piv[k]=x;out.append(row);break
            x^=piv[k]
    return out
def tr(rows,n=None):
    n=len(rows) if n is None else n;out=[0]*n
    for i,x in enumerate(rows):
        while x:
            z=x&-x;out[z.bit_length()-1]^=1<<i;x^=z
    return out
def mm(A,B):
    out=[]
    for x in A:
        z=0
        while x:
            low=x&-x;z^=B[low.bit_length()-1];x^=low
        out.append(z)
    return out
def add(A,B):return [x^y for x,y in zip(A,B)]
def action(A,x):return sum(((row&x).bit_count()%2)<<i for i,row in enumerate(A))
def eye(n):return [1<<i for i in range(n)]
def power(A,n):
    out=eye(len(A))
    while n:
        if n&1:out=mm(out,A)
        A=mm(A,A);n>>=1
    return out
def inverse_binary(A):
    n=len(A);rows=[x|(1<<(n+i))for i,x in enumerate(A)]
    for c in range(n):
        k=next(k for k in range(c,n)if rows[k]>>c&1)
        rows[c],rows[k]=rows[k],rows[c]
        for k in range(n):
            if k!=c and rows[k]>>c&1:rows[k]^=rows[c]
    need([x&((1<<n)-1)for x in rows]==eye(n),'binary inverse left identity')
    return [x>>n for x in rows]
def inverse_rational(A):
    n=len(A);rows=[[Fraction(x)for x in r]+[Fraction(i==j)for j in range(n)]for i,r in enumerate(A)]
    for c in range(n):
        k=next(k for k in range(c,n)if rows[k][c]);rows[c],rows[k]=rows[k],rows[c]
        z=rows[c][c];rows[c]=[x/z for x in rows[c]]
        for k in range(n):
            if k!=c and rows[k][c]:
                z=rows[k][c];rows[k]=[x-z*y for x,y in zip(rows[k],rows[c])]
    return [r[n:]for r in rows]

def geometry(layout,basis):
    roots=layout['root_table'];cols=basis['lattice_basis_columns']
    inv=inverse_rational([[cols[j][i]for j in range(8)]for i in range(8)])
    hyp=basis['hyperbolic_basis_masks'];lookup={}
    for v in range(256):
        z=0
        for k in range(8):
            if v>>k&1:z^=hyp[k]
        lookup[z]=v
    need(len(lookup)==256,'hyperbolic coordinate basis')
    prim=[]
    for k in range(4):
        C=[0]*16;D=[0]*16
        for j in range(16):
            if j>>k&1:D[j^(1<<k)]^=1<<j
            else:C[j|(1<<k)]^=1<<j
        prim.extend([C,D])
    gam=[]
    for root in roots:
        cs=[sum(c*x for c,x in zip(r,root))for r in inv]
        need(all(c.denominator==1 for c in cs),'integral root coordinates')
        v=sum((int(c)%2)<<i for i,c in enumerate(cs));g=[0]*16
        for k in range(8):
            if lookup[v]>>k&1:g=add(g,prim[k])
        need(mm(g,g)==eye(16),'native gamma square');gam.append(g)
    adj=[{j for j,y in enumerate(roots[:111])if i!=j and sum(u*v for u,v in zip(x,y))==0}
         for i,x in enumerate(roots[:111])]
    for i in range(111):
        for j in range(i):
            expected=[0]*16 if j in adj[i] else eye(16)
            need(add(mm(gam[i],gam[j]),mm(gam[j],gam[i]))==expected,'actual native Clifford pair')
    K=[(1<<i)|sum(1<<j for j in adj[i])for i in range(111)]
    need(rank(K)==9 and sum(map(len,adj))==6470,'native rank and edge census')
    need(10 not in adj[80] and [len(adj[80]),len(adj[10])]==[62,61],'native separated stars')
    seen={0};todo=[0]
    while todo:
        for j in adj[todo.pop()]-seen:seen.add(j);todo.append(j)
    need(len(seen)==111,'native connectivity')
    for support in [adj[80]|{10},adj[10]|{80}]:
        mask=((1<<111)-1)^sum(1<<j for j in support)
        need(rank([x&mask for x in K])==9,'native exact support separation')
    return gam,adj,K

