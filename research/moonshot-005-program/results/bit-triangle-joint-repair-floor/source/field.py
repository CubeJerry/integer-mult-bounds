"""Exact GF(32) arithmetic used by this package's replay and builder."""
def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1;a<<=1
        if a&32:a^=0b100101
    return c

def power(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n>>=1
    return r

def rank(rows):
    a=[list(r)for r in rows]
    if not a:return 0
    p=0
    for j in range(len(a[0])):
        k=next((k for k in range(p,len(a))if a[k][j]),None)
        if k is None:continue
        a[p],a[k]=a[k],a[p];v=power(a[p][j],30)
        a[p]=[mul(v,x)for x in a[p]]
        for k in range(p+1,len(a)):
            if a[k][j]:
                v=a[k][j];a[k]=[x^mul(v,y)for x,y in zip(a[k],a[p])]
        p+=1
        if p==len(a):break
    return p

def inv(a):
    n=len(a)
    a=[list(row)+[int(i==j)for j in range(n)]for i,row in enumerate(a)]
    for j in range(n):
        k=next((k for k in range(j,n)if a[k][j]),None)
        if k is None:raise ValueError('singular')
        a[j],a[k]=a[k],a[j]
        v=power(a[j][j],30);a[j]=[mul(v,x)for x in a[j]]
        for k in range(n):
            if k!=j and a[k][j]:
                v=a[k][j];a[k]=[x^mul(v,y)for x,y in zip(a[k],a[j])]
    return [row[n:]for row in a]

def xor(values):
    a=0
    for v in values:a^=v
    return a

def mm(a,b):
    return [[xor(mul(x,y)for x,y in zip(row,col))for col in zip(*b)]for row in a]
