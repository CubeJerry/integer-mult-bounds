"""Independent reviewer binary linear algebra and native gamma reconstruction."""
from fractions import Fraction

def require(ok,message):
    if not ok:raise ValueError(message)
def identity(n):return [1<<i for i in range(n)]
def transpose(A,n=None):
    width=len(A)if n is None else n
    return [sum(((A[i]>>j)&1)<<i for i in range(len(A)))for j in range(width)]
def multiply(A,B):
    return [xor(B[k]for k in range(len(B))if row>>k&1)for row in A]
def xor(values):
    z=0
    for v in values:z^=v
    return z
def plus(A,B):return [a^b for a,b in zip(A,B)]
def tensor(A,B):
    m=len(B)
    return [sum(br<<(j*m)for j in range(len(A))if ar>>j&1)for ar in A for br in B]
def matrix_rank(rows):
    piv={}
    for r in rows:
        for k in sorted(piv,reverse=True):
            if r>>k&1:r^=piv[k]
        if r:piv[r.bit_length()-1]=r
    return len(piv)
def inverse(A):
    n=len(A);w=[row|1<<(n+i)for i,row in enumerate(A)]
    for c in range(n):
        r=next((i for i in range(c,n)if w[i]>>c&1),None)
        require(r is not None,'binary inverse pivot')
        w[c],w[r]=w[r],w[c]
        for i in range(n):
            if i!=c and w[i]>>c&1:w[i]^=w[c]
    require([r&((1<<n)-1)for r in w]==identity(n),'binary inverse reduction')
    return [r>>n for r in w]
def rational_inverse(A):
    n=len(A);w=[[Fraction(x)for x in row]+[Fraction(i==j)for j in range(n)]for i,row in enumerate(A)]
    for c in range(n):
        r=next(i for i in range(c,n)if w[i][c]);w[c],w[r]=w[r],w[c]
        z=w[c][c];w[c]=[x/z for x in w[c]]
        for i in range(n):
            if i!=c:
                z=w[i][c];w[i]=[x-z*y for x,y in zip(w[i],w[c])]
    return [row[n:]for row in w]
def native(layout,basis):
    cols=basis['lattice_basis_columns']
    inv=rational_inverse([[cols[j][i]for j in range(8)]for i in range(8)])
    change={xor(basis['hyperbolic_basis_masks'][k]for k in range(8)if x>>k&1):x for x in range(256)}
    require(len(change)==256,'hyperbolic basis')
    primitive=[]
    for k in range(4):
        create=[0]*16;annihilate=[0]*16
        for x in range(16):
            if x>>k&1:annihilate[x^(1<<k)]|=1<<x
            else:create[x^(1<<k)]|=1<<x
        primitive.extend([create,annihilate])
    gammas=[]
    for root in layout['root_table']:
        coordinates=[sum(c*x for c,x in zip(row,root))for row in inv]
        require(all(c.denominator==1 for c in coordinates),'integral lattice coordinates')
        mask=sum((int(c)&1)<<k for k,c in enumerate(coordinates));v=change[mask]
        gammas.append([xor(primitive[k][r]for k in range(8)if v>>k&1)for r in range(16)])
    roots=layout['root_table'][:111]
    neighbors=[{j for j,y in enumerate(roots)if i!=j and sum(a*b for a,b in zip(x,y))==0}for i,x in enumerate(roots)]
    for i in range(120):require(multiply(gammas[i],gammas[i])==identity(16),'root gamma square')
    for i in range(111):
        for j in range(i):
            wanted=[0]*16 if j in neighbors[i]else identity(16)
            require(plus(multiply(gammas[i],gammas[j]),multiply(gammas[j],gammas[i]))==wanted,'actual Clifford relation')
    return gammas,neighbors
