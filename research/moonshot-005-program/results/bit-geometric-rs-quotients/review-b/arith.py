"""Independent GF64 log-table arithmetic and exact finite polynomial checks."""
from itertools import combinations

def need(value,message):
    if not value:
        raise ValueError(message)

EXP=[];LOG={};value=1
for exponent in range(63):
    need(value not in LOG,'primitive field generator has no early cycle')
    EXP.append(value);LOG[value]=exponent
    value<<=1
    if value&64:
        value^=0x43
need(value==1 and set(EXP)==set(range(1,64)),'all nonzero GF64 elements generated')
MUL=tuple(tuple(0 if not a or not b else EXP[(LOG[a]+LOG[b])%63] for b in range(64)) for a in range(64))
INV=(0,)+tuple(EXP[-LOG[a]%63] for a in range(1,64))

def power(a,n):
    return 1 if n==0 else (0 if not a else EXP[(LOG[a]*n)%63])

def q6(a):
    return power(a,9)^power(a,18)^power(a,36)

def b6(a,b):
    return q6(a^b)^q6(a)^q6(b)

def q8(mask):
    return sum(((mask>>(2*i))&1)*((mask>>(2*i+1))&1) for i in range(4))%2

def b8(a,b):
    return q8(a^b)^q8(a)^q8(b)

def xor(values):
    result=0
    for value in values:
        result^=value
    return result

def binary_rank(values):
    pivots={}
    for value in values:
        while value:
            bit=value.bit_length()-1
            if bit not in pivots:
                pivots[bit]=value;break
            value^=pivots[bit]
    return len(pivots)

def rank(rows):
    basis={}
    for source in rows:
        row=list(source)
        for pivot in sorted(basis,reverse=True):
            if row[pivot]:
                scalar=MUL[row[pivot]]
                row=[x^scalar[y] for x,y in zip(row,basis[pivot])]
        support=[i for i,x in enumerate(row) if x]
        if support:
            pivot=support[-1];table=MUL[INV[row[pivot]]]
            basis[pivot]=[table[x] for x in row]
    return len(basis)

def polynomial(nodes):
    p=[1]
    for node in nodes:
        out=[0]*(len(p)+1)
        for i,c in enumerate(p):
            out[i]^=MUL[node][c];out[i+1]^=c
        p=out
    return tuple(p)

def evaluate(p,x):
    value=0
    for c in reversed(p):
        value=MUL[value][x]^c
    return value

def divide(p,node):
    result=[0]*(len(p)-1);result[-1]=p[-1]
    for i in range(len(result)-1,0,-1):
        result[i-1]=p[i]^MUL[node][result[i]]
    need(p[0]==MUL[node][result[0]],'exact polynomial division remainder')
    return tuple(result)

def L(v):
    p=[0]*17
    for degree,coefficient in ((1,power(v,8)),(2,power(v,16)),(4,power(v,32)),
                               (5,power(v,4)),(8,v),(14,power(v,4)),(16,power(v,2))):
        p[degree]=coefficient
    return tuple(p)

def block_formula(v):
    need(v!=0,'nonzero field receiver parameter')
    p=list(L(v));p[0]=q6(v)^1;scale=INV[power(v,2)]
    return tuple(MUL[scale][x] for x in p)

def U(v,c):
    p=list(L(v));p[0]^=b6(v,c)
    return divide(p,c)
