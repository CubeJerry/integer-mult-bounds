"""Small exact arrowhead systems for the 3,840-dimensional profile interpolation."""
import numpy as np


def need(test,message):
    if not test:raise ValueError(message)


def transpose(blocks):
    R,C,X,Y=blocks
    return R.T,C.T,[M.T for M in Y],[M.T for M in X]


def apply(field,blocks,x):
    R,C,X,Y=blocks;B=x.reshape(8,480,-1);center=field.mm(C,B[0]);parts=[]
    for t in range(7):
        center^=field.mm(X[t],B[t+1]);parts.append(field.mm(Y[t],B[0])^field.mm(R,B[t+1]))
    return np.vstack([center]+parts)


def preimage(field,null,blocks,V):
    R,C,X,Y=blocks;rows=field.pivots(R.T);cols=field.pivots(R);G=np.zeros_like(R)
    G[np.ix_(cols,rows)]=field.invert_and_price(R[np.ix_(rows,cols)])[0]
    N=null(field,R);L=null(field,R.T).T;k=len(L);v=V.shape[1];Vs=V.reshape(8,480,v)
    top=C.copy();side=Vs[0].copy();tail=[];lower=[];right=[]
    for e in range(7):
        XG=field.mm(X[e],G);top^=field.mm(XG,Y[e]);side^=field.mm(XG,Vs[e+1])
        tail.append(field.mm(X[e],N));lower.append(field.mm(L,Y[e]));right.append(field.mm(L,Vs[e+1]))
    reduced=np.block([[top,side,np.hstack(tail)],[np.vstack(lower),np.vstack(right),np.zeros((7*k,7*k),dtype=np.uint8)]])
    solution=null(field,reduced);x0=solution[:480];h=solution[480:480+v];xs=[x0]
    for e in range(7):
        local=field.mm(Vs[e+1],h)^field.mm(Y[e],x0)
        xs.append(field.mm(G,local)^field.mm(N,solution[480+v+e*k:480+v+(e+1)*k]))
    original=np.vstack(xs)
    need(field.rank(original)==original.shape[1] and np.array_equal(apply(field,blocks,original),field.mm(V,h)),'complete native common preimage basis')
    return original


def image_and_form(i,state,field,previous,dim,weights,blocks):
    P=state['P'][:dim[i]];U=state['U'][:,:7];terms=state['terms'];raw=state['raw'];copy=state['copy'];body=state['body'];degrees=state['tiers']
    R,C,X,Y=blocks;active=[j for j in state['adj'][i] if (i,j) in terms];local=[]
    for g in range(8):
        pieces=[]
        for f in range(8):
            M=(C if f==0 else R) if f==g else X[f-1] if g==0 else Y[g-1] if f==0 else None
            observed=field.mm(P,M) if M is not None else np.zeros((len(P),480),dtype=np.uint8)
            if f==g:observed^=field.product[weights[i],P]
            target=np.zeros_like(observed)
            for j in active:target^=field.product[weights[j],previous.donor.dual_N(i,j,g,f,state,dim)]
            need(np.array_equal(observed,target),'actual aggregate has its certified two-sided output probes')
            pieces.append(observed)
        local.append(np.hstack(pieces))
    original=np.zeros((8,3840,7),dtype=np.uint8)
    for e,ids in enumerate(raw):original[e,ids]=U
    images=[np.kron(np.eye(8,dtype=np.uint8),U)]
    for j in active:
        dest,src,A=terms[i,j];ids=np.arange(64*dest,64*(dest+1));m=degrees[j]
        pulses=np.hstack([field.mm(A,original[e,64*src:64*(src+1),:m]) for e in range(8)])
        T=np.zeros((3840,pulses.shape[1]),dtype=np.uint8);T[480*copy[ids]+body[ids]]=pulses;images.append(T)
    V=np.hstack(images);V=V[:,field.pivots(V)];Q=np.vstack(local);return V,Q[field.pivots(Q.T)]
