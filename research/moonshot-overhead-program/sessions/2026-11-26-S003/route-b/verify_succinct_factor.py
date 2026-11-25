#!/usr/bin/env python3
"""Exact F4 sparse-factor replay; no numerical tolerances or full tape claim."""
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path


def fm(a, b):
    z = 0
    while b:
        if b & 1:
            z ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return z

ZERO = {}
ONE = {(0, 0): 1}

def pa(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) ^ v
        if out[k] == 0:
            del out[k]
    return out

def pm(a, b):
    out = {}
    for i, u in a.items():
        for j, v in b.items():
            k = (i[0]+j[0], i[1]+j[1])
            out[k] = out.get(k, 0) ^ fm(u, v)
            if out[k] == 0:
                del out[k]
    return out

def ps(a, c):
    return {k: fm(v, c) for k, v in a.items() if fm(v, c)}

@dataclass
class Node:
    kind: str
    left: object = None
    right: object = None
    d: int = 1
    val: object = None
    gid: int = -1
    r: int = 1


def leaf(c=0, x=0, y=0):
    p = {}
    for k, v in [((0,0),c), ((1,0),x), ((0,1),y)]:
        if v:
            p[k]=v
    return Node('leaf', val=p)

def pad(a,d):
    assert d>=a.d
    return a if d==a.d else Node('pad',a,d=d,r=a.r)

def add(a,b,d=None):
    d=max(a.d,b.d) if d is None else d
    assert d & (d-1)==0
    return Node('add',pad(a,d),pad(b,d),d=d,r=d*a.r*b.r)

def mul(a,b):
    return Node('mul',a,b,d=a.d+b.d,r=a.r*b.r)

def scale(a,c):
    return Node('scale',a,d=a.d,val=c,r=a.r)

def annotate(n,rad):
    if n.kind=='add':
        n.gid=len(rad); rad.append(n.d)
    if n.left: annotate(n.left,rad)
    if n.right: annotate(n.right,rad)

def poly(n):
    if n.kind=='leaf': return n.val
    if n.kind=='pad': return poly(n.left)
    if n.kind=='scale': return ps(poly(n.left),n.val)
    return (pa if n.kind=='add' else pm)(poly(n.left),poly(n.right))

def madd_entry(a,key,p):
    z=pa(a.get(key,ZERO),p)
    if z: a[key]=z
    else: a.pop(key,None)

def kron(a,ra,b,rb):
    out={}
    for (i,j),p in a.items():
        for (k,l),q in b.items():
            z=pm(p,q)
            if z: out[(i*rb+k,j*rb+l)]=z
    return out

def eye(r): return {(i,i):ONE for i in range(r)}

def matrices(n):
    if n.kind=='leaf': return [{(0,0):n.val} if n.val else {}]
    A=matrices(n.left)
    if n.kind=='pad': return A+[eye(n.r) for _ in range(n.d-n.left.d)]
    if n.kind=='scale':
        return [{k:ps(v,n.val) for k,v in A[0].items() if ps(v,n.val)}]+A[1:]
    B=matrices(n.right)
    if n.kind=='mul':
        return [kron(a,n.left.r,eye(n.right.r),n.right.r) for a in A]+[kron(eye(n.left.r),n.left.r,b,n.right.r) for b in B]
    # Construct the total-grade-restricted tensor sum directly.
    out=[]; r=n.left.r; s=n.right.r; d=n.d
    for t in range(d):
        M={}
        for i in range(d):
            j=(t-i)%d
            for (u1,u0),p in A[i].items():
                for v in range(s):
                    madd_entry(M,((((i+1)%d)*r+u1)*s+v,(i*r+u0)*s+v),p)
            for (v1,v0),p in B[j].items():
                for u in range(r):
                    madd_entry(M,((i*r+u)*s+v1,(i*r+u)*s+v0),p)
        out.append(M)
    return out

def tokens(n,path=()):
    if n.kind=='leaf': return [path]
    if n.kind=='pad': return [path+('I',)]+tokens(n.left,path+('C',))
    if n.kind=='scale': return tokens(n.left,path+('C',))
    return tokens(n.left,path+('L',))+tokens(n.right,path+('R',))

def eval_token(n,path,t,coords,weight=1,rot=()):
    if n.kind=='leaf': return ps(n.val,weight),rot
    side=path[0]; path=path[1:]
    if n.kind=='pad':
        if side=='I': return (ps(ONE,weight) if t>=n.left.d else ZERO),rot
        if t>=n.left.d: return ZERO,rot
        return eval_token(n.left,path,t,coords,weight,rot)
    if n.kind=='scale':
        return eval_token(n.left,path,t,coords,fm(weight,n.val) if t==0 else weight,rot)
    if n.kind=='mul':
        if (side=='L') != (t<n.left.d): return ZERO,rot
        return eval_token(n.left if side=='L' else n.right,path,t if side=='L' else t-n.left.d,coords,weight,rot)
    i=coords[n.gid]
    return eval_token(n.left if side=='L' else n.right,path,i if side=='L' else (t-i)%n.d,coords,weight,rot+(n.gid,) if side=='L' else rot)

def encode(coords,rad):
    z=0
    for x,d in zip(coords,rad): z=z*d+x
    return z

def compile_sparse(n,rad,wrong_order=False):
    out=[]
    coords=list(product(*(range(d) for d in rad)))
    for t in range(n.d):
        M={}
        for path in tokens(n):
            for x in coords:
                p,rot=eval_token(n,path,t,x)
                y=list(x)
                for g in rot: y[g]=(y[g]+1)%rad[g]
                if wrong_order:
                    p,_=eval_token(n,path,t,tuple(y))
                if p: madd_entry(M,(encode(y,rad),encode(x,rad)),p)
        out.append(M)
    return out

def matmul(A,B):
    rows={}
    for (k,j),q in B.items(): rows.setdefault(k,[]).append((j,q))
    out={}
    for (i,k),p in A.items():
        for j,q in rows.get(k,[]): madd_entry(out,(i,j),pm(p,q))
    return out

def check(n):
    rad=[]; annotate(n,rad)
    assert n.r == __import__('math').prod(rad)
    A=matrices(n); C=compile_sparse(n,rad)
    assert A==C
    expected={(i,i):poly(n) for i in range(n.r) if poly(n)}
    for start in range(n.d):
        acc=eye(n.r)
        for k in range(n.d): acc=matmul(A[(start+k)%n.d],acc)
        assert acc==expected,(n,start)
    return len(A)*n.r, n.d, compile_sparse(n,rad,True)!=A

cases=[]
# Independent copies avoid aliasing the formula's grade-coordinate nodes.
for a,b in product(range(4),repeat=2):
    cases.extend([
        add(pad(leaf(a,1,0),2),pad(leaf(b,0,1),2),2),
        add(mul(leaf(a,1,0),leaf(b,0,1)),pad(leaf(1,1,1),2),2),
        scale(add(pad(leaf(a,1,0),2),pad(leaf(b,0,1),2),2),a),
    ])
# Unequal lengths, zero, nested sums, and a non-power-two final product.
cases.extend([
    add(pad(leaf(0,1,0),4),mul(pad(leaf(1,0,1),2),pad(leaf(2,1,1),2)),4),
    add(mul(add(leaf(1,1,0),leaf(2,0,1),1),leaf(3,1,1)),pad(leaf(),2),2),
    mul(add(pad(leaf(1,1,0),2),pad(leaf(2,0,1),2),2),leaf(3,1,1)),
    add(add(pad(leaf(1,1,0),2),pad(leaf(2,0,1),2),2),add(pad(leaf(0,1,1),2),pad(leaf(3),2),2),2),
])
columns=cycles=bad=0
for n in cases:
    a,b,c=check(n); columns+=a; cycles+=b; bad+=c
assert bad>0
result={
 'status':'passed', 'arithmetic':'exact formal polynomials over F4 in two commuting variables',
 'cases':len(cases),'factor_columns_checked':columns,'whole_identity_cyclic_products_checked':cycles,
 'wrong_mask_order_negative_controls_rejected':bad,
 'scope':'Dense graded construction equals succinct masked rotations; all cyclic products equal scalar whole identity. Does not execute physical tape routing or prove an asymptotic bound.',
}
Path(__file__).with_name('succinct-factor-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
