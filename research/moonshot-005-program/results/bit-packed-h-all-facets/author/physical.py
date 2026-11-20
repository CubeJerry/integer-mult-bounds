"""Raw genuine H and K holders and the common original-source extensions."""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import ctypes,hashlib
import numpy as np

class Physical:
    def __init__(self,args,at,inv,table,inverses,ext,reduce,panels,price,perm,comp,assignment,col):
        self.args=args;self.at=at;self.inv=inv;self.mm=at.ops.matmul;self.tbl=table;self.inverses=inverses;self.ext=ext;self.reduce=reduce
        self.hs,self.live,self.L,self.Z=panels;self.price=price;self.perm=perm;self.comp=comp;self.assignment=assignment;self.col=col;self.gauges={};self.owner={}
        lib=ctypes.CDLL(str(args.arith.resolve()));self.pivot=lib.field_pivots;self.rankfn=lib.field_rank;v=ctypes.c_void_p
        for f in (self.pivot,self.rankfn):f.restype=ctypes.c_int
        self.pivot.argtypes=[v,ctypes.c_int,ctypes.c_int,v,v,v];self.rankfn.argtypes=[v,ctypes.c_int,ctypes.c_int,v,v]
    def piv(self,A):
        M=np.array(A,dtype=np.uint8,order='C',copy=True);out=np.empty(min(M.shape),np.int32);n=self.pivot(M.ctypes.data,len(M),M.shape[1],self.tbl.ctypes.data,self.inverses.ctypes.data,out.ctypes.data);return list(out[:n])
    def rank(self,A):
        M=np.array(A,dtype=np.uint8,order='C',copy=True);return self.rankfn(M.ctypes.data,len(M),M.shape[1],self.tbl.ctypes.data,self.inverses.ctypes.data)
    @lru_cache(222)
    def holder(self,i,k):
        e,E,y,Y=self.at.facet(i);w=32*k;s=0 if k==3 else 96
        ei=np.flatnonzero(E[s:s+w].any(axis=0));yi=np.flatnonzero(Y[s:s+w].any(axis=0));F=np.hstack([E[s:s+w,ei],Y[s:s+w,yi]])
        return ei,yi,[e[t]for t in ei]+[y[t]for t in yi],F
    @lru_cache(222)
    def presource(self,i,j,k):
        e,X,y,Y=self.at.terminal_inputs(i,j);ei,yi,_,_=self.holder(i,k);s=0 if k==3 else 96;w=32*k
        return np.vstack([X[ei,s:s+w],Y[yi,s:s+w]])
    @lru_cache(220)
    def prepanel(self,i,k):
        a=self.at;hs=sorted(self.live[i]);width=2*k*len(hs);f=a.right(i)
        raw=defaultdict(lambda:np.zeros(width,np.uint8))
        for n,h in enumerate(hs):
            ds=[d for d in a.h_ports[h][k==12]if i in a.D[a.dual[d]]];assert len(ds)==k
            p=a.phase[str(h)];seq=[('X',t)for t in range(p['early'])]+[('Y',t)for t in range(p['late'])]
            for s,(phase,t)in enumerate(seq):
                for z,d in enumerate(ds):
                    word,owners=a.middle_matrix(d);c=owners.index(a.left_flags[h,d,phase][t])
                    for r,b in enumerate(owners):
                        if b in f:raw[b][n*2*k+s*k+z]^=word[r,c]
        taken={}
        for h in a.ks[i]:
            ch=a.kr[str(h)]
            for ph,ins,outs in ch['stripes']:
                if len(ins)!=3*k:continue
                taken.update(zip(outs,self.mm(a.V[len(ins)].T,np.stack([raw[b]for b in ins]))))
            for x,y in ch['early_cache_to_late']:
                if x in taken:assert y in taken;taken[y]^=taken[x]
        _,_,ids,F=self.holder(i,k);P=np.stack([taken[x]for x in ids]);assert np.array_equal(self.mm(F,P),self.Z[i,k])
        return P
    def required(self,i,j,k):
        I=np.eye(32*k,dtype=np.uint8)
        if k==3 and (i==80 or j==10):
            dest,src=(0,2)if i==80 else(self.col[i],0);assert max(dest,src)<12
            for half in range(2):
                for z in range(4):I[half*48+4*dest+z,half*48+4*src+z]^=1
        return I
    def null(self,A):
        mat,ps=self.reduce(A);cols=A.shape[1];fr=sorted(set(range(cols))-set(ps));Z=np.zeros((len(fr),cols),np.uint8)
        for n,j in enumerate(fr):Z[n,j]=1;Z[n,ps]=mat[:len(ps),j]
        return Z.T
    def source(self,j,k):
        left=[];right=[];w=32*k
        for i in self.assignment[j]:
            P=self.prepanel(i,k);A=self.presource(i,j,k);F=self.holder(i,k)[3];Y=self.mm(self.inv(self.mm(F,A)),self.Z[i,k])
            relations=self.null(P^self.mm(A,Y));left.append(self.mm(self.required(i,j,k),self.mm(self.L[i,k],relations)));right.append(self.mm(Y,relations))
        L=np.hstack(left);R=np.hstack(right);dim=L.shape[1];assert self.rank(L)==self.rank(R)==dim
        if j in (36,46,63,109):
            rng=np.random.Generator(np.random.PCG64(173+4100*j+99*k));ex=rng.integers(0,64,(w,w-dim),dtype=np.uint8);B=np.hstack([R,ex])
        else:B=self.ext(R.T)
        G=self.mm(B,self.inv(self.ext(L.T)));assert self.rank(G)==w and np.array_equal(self.mm(G,L),R)
        self.gauges[j,k]=G;return G
    def body_d(self,i,k):
        a=self.at;_,_,ids,_=self.holder(i,k);m=len(ids);eye=np.eye(m,dtype=np.uint8)
        ix={t:z for z,t in enumerate(ids)};body={}
        for h in a.ks[i]:
            ch=a.kr[str(h)];du={};strips=[(p,ins,outs)for p,ins,outs in ch['stripes']if len(ins)==3*k]
            for _,ins,outs in strips:
                for t in outs:du[t]=eye[ix[t]].copy()if t in ix else np.zeros(m,np.uint8)
            for x,y in ch['early_cache_to_late']:
                if x in du:assert y in du;du[x]^=du[y]
            for _,ins,outs in strips:body.update(zip(ins,self.mm(a.V[3*k],np.stack([du[b]for b in outs]))))
        ds=sorted({a.route[t][4]for t in body});pieces=[]
        for d in ds:
            flags=[x for x in a.middle[d,'X']+a.middle[d,'Y']if x in body];assert len(flags)==8;pieces.append(np.stack([body[t]for t in flags]).T)
        return ds,np.hstack(pieces)
    def face(self,i,j,k,record):
        A=self.presource(i,j,k);G=self.gauges[j,k];e,_,ids,old=self.holder(i,k);w=32*k
        if i==80:
            F=self.mm(self.mm(self.required(i,j,k),self.inv(self.mm(self.mm(old,A),G))),old)
        else:
            P=self.prepanel(i,k);C=np.hstack([A,P]);Q=np.hstack([self.mm(self.required(i,j,k),self.inv(G)),self.L[i,k]])
            selected=self.piv(C);base=C[:,selected];p=self.piv(base.T);free=sorted(set(range(len(C)))-set(p));m=len(C)
            iv=self.inv(np.hstack([base,np.eye(m,dtype=np.uint8)[:,free]]));F=self.mm(Q[:,selected],iv[:len(selected)])
            assert len(free)==record['free_columns']
            if free:
                rng=np.random.Generator(np.random.PCG64(1000000*i+10000*k+record['trial']));extra=rng.integers(0,64,(w,len(free)),dtype=np.uint8)
                F^=self.mm(extra,iv[len(selected):])
            assert np.array_equal(self.mm(F,C),Q)and np.array_equal(self.mm(F,P),self.L[i,k])
        assert self.rank(F[:,len(e):])==w and np.array_equal(self.mm(self.mm(F,A),G),self.required(i,j,k))
        assert hashlib.sha256(F.tobytes()).hexdigest()==record['raw_cpu_SHA256']
        ds,B=self.body_d(i,k);right=self.mm(F,B);count=0
        for donor in self.at.orth[i]&set(range(111)):
            cols=[8*z+n for z,d in enumerate(ds)if donor in self.at.D[d]for n in range(8)]
            assert len(cols)==w and self.rank(right[:,cols])==w
            count+=1
        return F,count
