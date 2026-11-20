"""Exact GF(64) field operations in the polynomial basis."""
import numpy as np

def need(x, label):
    if not x:
        raise ValueError(label)

def field():
    m=np.zeros((64,64),dtype=np.uint8)
    for a in range(64):
        for b in range(64):
            x,y=a,b
            while y:
                if y&1: m[a,b]^=x
                x<<=1
                if x&64: x^=0x43
                y>>=1
    inv=np.array([0]+[np.nonzero(m[t]==1)[0][0] for t in range(1,64)],dtype=np.uint8)
    pw=np.ones((64,64),dtype=np.uint8)
    for i in range(1,64):
        pw[:,i]=m[pw[:,i-1],np.arange(64)]
    return m,inv,pw

MUL,INV,POWER=field()

def mm(a,b):
    need(a.shape[1]==b.shape[0],"field product shape")
    out=np.zeros((len(a),b.shape[1]),dtype=np.uint8)
    for k in range(a.shape[1]):
        out^=MUL[a[:,k,None],b[None,k,:]]
    return out

def echelon(a):
    """Exact elimination with pivot columns and determinant if square."""
    x=np.array(a,copy=True,order="C")
    n,w=x.shape
    piv=[];det=1
    for c in range(w):
        t=len(piv)
        if t==n: break
        hits=np.flatnonzero(x[t:,c])
        if not len(hits): continue
        p=t+int(hits[0])
        if p!=t: x[[t,p]]=x[[p,t]]
        v=x[t,c];det=int(MUL[det,v])
        if t+1<n:
            co=MUL[x[t+1:,c].copy(),INV[v]]
            x[t+1:,c:] ^= MUL[co[:,None],x[t:t+1,c:]]
        piv.append(c)
    return piv,det if n==w and len(piv)==n else 0

def cauchy(rows,cols):
    return INV[np.asarray(rows,dtype=np.uint8)[:,None]^(32+np.asarray(cols,dtype=np.uint8)[None,:])]

def jet(node,derivative,scale):
    v=POWER[node,:16].copy()
    if derivative:
        v[0::2]=0;v[1::2]=MUL[scale,POWER[node,0:16:2]]
    return v
