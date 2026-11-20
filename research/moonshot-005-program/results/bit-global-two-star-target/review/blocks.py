"""Independent genuine eight-copy proper star factorization and its reversible local bill."""
import numpy as np
from hashlib import sha256

def req(v,m):
    if not v:raise ValueError(m)
class Proper:
    def __init__(self,ar,ee,b,l,tap,phase):
        self.ar=ar;mm=ar.mm;self.r=b^mm(l,tap['rim']);self.c=b^mm(l,tap['central'])
        for key in tap.files:
            if key.startswith('H-'):
                _,g,e=key.split('-');phase.setdefault((int(g),int(e)),[]).append((mm(l,tap[key]),tap['G-'+g+'-'+e]))
        def combine(label):
            out=np.zeros((480,480),dtype=np.uint8)
            for u,v in phase.get(label,[]):out^=mm(u,v)
            return out
        self.c^=combine((0,0));self.x=[combine((0,g))for g in range(1,8)];self.y=[combine((g,0))for g in range(1,8)]
        self.ri,rprice=ar.reduce(self.r,True);self.upper=[mm(x,self.ri)for x in self.x];self.lower=[mm(self.ri,y)for y in self.y]
        s=self.c.copy()
        for u,y in zip(self.upper,self.y):s^=mm(u,y)
        self.s=s;self.si,sprice=ar.reduce(s,True)
        for u,y,x,v in zip(self.upper,self.y,self.x,self.lower):
            req(np.array_equal(mm(u,self.r),x) and np.array_equal(mm(self.r,v),y),'actual complete off-centre coefficient blocks')
        req(np.array_equal(mm(s,self.si),np.eye(480,dtype=np.uint8)) and np.array_equal(mm(self.r,self.ri),np.eye(480,dtype=np.uint8)),'two complete real diagonal inverses')
        self.price=int(sprice+7*rprice+sum(ar.weights[m].sum()for m in self.upper+self.lower));self.sha=sha256(b''.join(v.tobytes()for v in [self.r,self.c,*self.x,*self.y])).hexdigest()
    def apply(self,X,inv=False,transpose=False):
        mm=self.ar.mm;a=X.reshape(8,480,-1);x=a[0].copy();rr=[q.copy()for q in a[1:]]
        if not inv:
            b=self.c.T if transpose else self.c;m=self.r.T if transpose else self.r
            U=[y.T for y in self.y] if transpose else self.x;V=[t.T for t in self.x]if transpose else self.y
            ctr=mm(b,x)
            for u,v in zip(U,rr):ctr^=mm(u,v)
            return np.vstack([ctr]+[mm(m,v)^mm(h,x)for h,v in zip(V,rr)])
        us=[z.T for z in self.lower]if transpose else self.upper;vs=[z.T for z in self.upper]if transpose else self.lower
        for u,v in zip(us,rr):x^=mm(u,v)
        x=mm(self.si.T if transpose else self.si,x);ri=self.ri.T if transpose else self.ri
        return np.vstack([x]+[mm(ri,v)^mm(h,x)for h,v in zip(vs,rr)])
class Target:
    def __init__(self,ar,body,lane,out,src,T):
        self.ar=ar;self.T=T;iy=np.arange(64*out,64*(out+1));ix=np.arange(64*src,64*(src+1));self.oy=480*lane[iy]+body[iy];self.ix=480*lane[ix]+body[ix]
        if out==src:
            K=T^np.eye(64,dtype=np.uint8);iv,self.price=ar.reduce(K,True);self.it=iv^np.eye(64,dtype=np.uint8)
        else:self.it=T;self.price=int(ar.weights[T].sum())
    def apply(self,X,inv=False,transpose=False):
        z=X.copy();t=self.it if inv else self.T;i,j=self.oy,self.ix
        if transpose:i,j,t=j,i,t.T
        z[i]^=self.ar.mm(t,X[j]);return z
