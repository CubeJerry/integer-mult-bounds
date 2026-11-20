"""Recover the genuine full pair operator and price or apply its reversible arrowhead factorization."""
import hashlib
import numpy as np


def source_pin(rim,center,cross):
    h=hashlib.sha256();h.update(rim);h.update(center)
    for key,(a,b) in sorted(cross.items()):
        h.update(bytes(key));h.update(np.ascontiguousarray(a));h.update(np.ascontiguousarray(b))
    return h.hexdigest()


def cached(path):
    with np.load(path,allow_pickle=False) as z:
        cross={tuple(map(int,k[1:].split('_'))):(z[k],z['G'+k[1:]]) for k in z.files if k.startswith('H')}
        return z['rim'],z['central'],cross


def whole(field,state,i,j,L,program):
    mm=field.mm;rim,center,cross=program;index=state['adj'][i].index(j);E=state['E'][i][index];B=state['B'][i][index];V,S=state['VS'][i]
    original=mm(V,B^mm(S,E));updates=state['updates'].get(i,{})
    def off(pair):
        mix=np.zeros((480,480),dtype=np.uint8)
        if pair in updates:
            ids,A=updates[pair];mix[ids]^=mm(A,E)
        if pair in cross:
            H,G=cross[pair];mix^=mm(mm(L,H),G)
        return mix
    return original^mm(L,rim),original^mm(L,center)^off((0,0)),[off((0,e)) for e in range(1,8)],[off((e,0)) for e in range(1,8)]


def apply(field,blocks,input):
    R,C,X,Y=blocks;B=input.reshape(8,480,-1);center=field.mm(C,B[0]);others=[]
    for e in range(7):center^=field.mm(X[e],B[e+1]);others.append(field.mm(Y[e],B[0])^field.mm(R,B[e+1]))
    return np.vstack([center]+others)


def adjoint(z):return z[0].T,z[1].T,[a.T for a in z[3]],[a.T for a in z[2]]


def price(field,blocks):
    R,C,X,Y=blocks;inv,cr=field.invert_and_price(R);S=C.copy();shear=0
    for x,y in zip(X,Y):
        up=field.mm(x,inv);low=field.mm(inv,y);S^=field.mm(up,y)
        shear+=int(field.weights[up].sum())+int(field.weights[low].sum())
    _,cs=field.invert_and_price(S)
    return {'rim_ADD':cr,'central_Schur_ADD':cs,'two_direction_shears_ADD':shear,'native_forward_or_inverse_ADD':7*cr+cs+shear,
            'native_rim_sha256':hashlib.sha256(R).hexdigest(),'native_Schur_sha256':hashlib.sha256(S).hexdigest()}


def target(field,source,term,state,transpose=False):
    out=source.copy()
    if term is None:return out
    dest,src,N=term
    if transpose:dest,src,N=src,dest,N.T
    t=np.arange(64*dest,64*(dest+1));s=np.arange(64*src,64*(src+1));out[480*state['copy'][t]+state['body'][t]]^=field.mm(N,source[480*state['copy'][s]+state['body'][s]])
    return out


def target_price(field,term):
    if term is None:return 0
    dest,src,N=term
    if dest==src:return field.invert_and_price(np.eye(64,dtype=np.uint8)^N)[1]
    return int(field.weights[N].sum())
