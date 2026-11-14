#!/usr/bin/env python3
"""E-free two-chain caller, literal QUERY-only lowering.
Chain/idle geometry: DreamingOfClouds' p104-chain-nested-root.
Parity-uniform E-free middle: this package. Three-query gadget: CubeJerry's p104-query-only-interval, specialized to an involution.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import argparse,json,gzip,hashlib
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def columns(vs):return [list(r)for r in zip(*vs)]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def mul(A,B):return [[sum(x*y for x,y in zip(row,col))for col in zip(*B)]for row in A]
def inv(A):
    n=len(A);a=[list(map(F,row))+r for row,r in zip(A,eye(n))]
    for j in range(n):
        k=next(k for k in range(j,n)if a[k][j]);a[j],a[k]=a[k],a[j]
        q=a[j][j];a[j]=[v/q for v in a[j]]
        for k in range(n):
            if k!=j and a[k][j]:
                q=a[k][j];a[k]=[v-q*w for v,w in zip(a[k],a[j])]
    need([r[:n]for r in a]==eye(n),'matrix inverse')
    return [r[n:]for r in a]
def rankone(x,y,c):return [[F(i==j)+c*x[i]*y[j]for j in range(len(x))]for i in range(len(x))]
def vec(n,*pairs):
    v=[F(0)]*n
    for i,c in pairs:v[i]+=c
    return v

def thin(a,n,off):
    eps=(-1)**a;A=off;ff=list(range(off+1,off+a+1));hh=list(range(off+a+1,off+2*a+1))
    w=vec(n,(A,1),*[(i,1)for i in ff],*[(i,-1)for i in hh]);e=vec(n,(A,1))
    v=vec(n,(A,-1),*[(i,2)for i in hh])
    y=vec(n,(A,1-eps),*[(i,-eps*((-1)**j))for j,i in enumerate(ff,1)],*[(i,-((-1)**j))for j,i in enumerate(hh,1)])
    need(dot(e,w)==1 and dot(y,v)==0 and dot(y,w)==0,'E-free thin pairings')
    return w,e,v,y

def complete(x,y):
    n=len(x);need(dot(y,x)==0,'query nilpotence')
    aa=next(i for i in range(n)if abs(y[i])==1)
    bb=next(i for i in range(n)if abs(x[i])==1 and i!=aa)
    z=vec(n,(aa,1/y[aa]));l=vec(n,(bb,1/x[bb]));vs=[x,z]
    for j in range(n):
        if j in(aa,bb):continue
        e=vec(n,(j,1));vs.append([e[i]-y[j]*z[i]-l[j]*x[i]for i in range(n)])
    C=columns(vs);need(mul(inv(C),C)==eye(n),'query basis invertible')
    return C

class Builder:
    def __init__(self,a,b):self.a=a;self.b=b;self.n=4*a+2;self.L=2*a+1;self.events=[]
    def emit(self,*e):self.events.append(list(e))
    def mix(self,A):
        n=self.n;a=[list(map(F,row))for row in A];ops=[]
        for j in range(n):
            while True:
                k=next(k for k in range(j,n)if a[k][j])
                if k!=j:a[j],a[k]=a[k],a[j];ops.append(['SWAP',j,k])
                k=next((k for k in range(j+1,n)if a[k][j]),None)
                if k is None:break
                q=a[k][j]//a[j][j]
                if q:
                    a[k]=[x-q*y for x,y in zip(a[k],a[j])];ops.append(['ADD',k,j,str(-q)])
                if a[k][j]:a[j],a[k]=a[k],a[j];ops.append(['SWAP',j,k])
            need(abs(a[j][j])==1,'unimodular unit pivot')
            if a[j][j]==-1:a[j]=[-x for x in a[j]];ops.append(['SCALE',j,'-1'])
            for k in range(j):
                if a[k][j]:
                    q=-a[k][j];a[k]=[x+q*y for x,y in zip(a[k],a[j])];ops.append(['ADD',k,j,str(q)])
        need(a==eye(n),'complete ordinary elimination')
        for e in reversed(ops):
            if e[0]=='ADD':e[-1]=str(-F(e[-1]))
            self.events.append(e)
    def squery(self,d,s):
        self.emit('LAMBDA',d,-1);self.emit('QUERY',d,s,-1);self.emit('LAMBDA',d,1)
    def host(self,stage):
        self.emit('LAMBDA',0,-1)
        self.emit('LAMBDA',self.L,1);self.emit('SCALE',self.L,'-1')
        self.emit('HOST2',stage,1,0,self.L,self.L+1)
        self.emit('LAMBDA',0,1)
        self.emit('SCALE',self.L,'-1');self.emit('LAMBDA',self.L,-1)
        self.emit('ADD',0,1,'-1');self.emit('ADD',self.L,self.L+1,'-1')
    def stage_basis(self,side,i):
        n=self.n;a=self.a;L=self.L;Cs=[]
        for off in(0,L):
            A=off;ff=list(range(off+1,off+a+1));hh=list(range(off+a+1,off+2*a+1))
            if side=='L':
                x=vec(n,(A,1),(ff[i],1),*[(ff[j],2)for j in range(i)])
                w=vec(n,(A,1),*[(ff[j],2)for j in range(i)])
                idle=ff[:i];used={A,ff[i],*idle}
            else:
                x=vec(n,(A,-1),(hh[i],1),*[(hh[j],2)for j in range(i+1,a)])
                w=vec(n,(A,1),*[(hh[j],-2)for j in range(i+1,a)])
                idle=hh[i+1:];used={A,hh[i],*idle}
            local=[x,w]+[vec(n,(j,1))for j in idle]+[vec(n,(j,1))for j in range(off,off+L)if j not in used]
            need(len(local)==L,'stage local basis size');Cs+=local
        return columns(Cs)
    def middle(self):
        a=self.a;n=self.n;L=self.L
        wA,eA,vA,yA=thin(a,n,0);wB,eB,vB,yB=thin(a,n,L)
        sA=[x+y for x,y in zip(vA,wA)]
        idx=list(range(1,L));p=next(j for j in idx if abs(yA[j])==1);r=next(j for j in idx if j!=p)
        z=vec(n,(p,1/yA[p]));vs=[wA,wB,sA,z]
        for j in idx:
            if j in(p,r):continue
            e=vec(n,(j,1));vs.append([e[i]-yA[j]*z[i]for i in range(n)])
        vs += [vec(n,(j,1))for j in range(L+1,n)]
        B=columns(vs);Bi=inv(B)
        need(Bi[0]==eA and Bi[1]==eB and Bi[3]==yA,'middle coordinate functionals')
        self.mix(Bi);self.emit('ADD',0,3,'-1')
        self.emit('SWAP',0,2);self.emit('SWAP',1,2);self.emit('ADD',1,3,'1');self.emit('ADD',2,0,'1')
        self.squery(0,1)
        self.emit('ADD',2,0,'-1');self.squery(1,2);self.emit('ADD',2,0,'1')
        self.emit('ADD',3,1,'-1');self.squery(2,3);self.emit('ADD',3,1,'1')
        self.emit('ADD',0,2,'-1');self.mix(B)
        C=complete(vB,yB);self.mix(inv(C));self.squery(0,1);self.mix(C)
        self.mix(rankone(vA,yA,F(-1)));self.mix(rankone(vB,yB,F(-1)))
    def run(self):
        a=self.a;L=self.L
        for i in range(a):
            C=self.stage_basis('L',i);self.mix(inv(C));self.host(i+1)
            if i>=1:
                stages=list(range(i+1,a+1));self.emit('IDLE_ONE',i+1,stages);self.emit('IDLE_ONE',L+i+1,stages)
            self.mix(C)
        self.middle()
        for i in range(a):
            C=self.stage_basis('R',i);self.mix(inv(C));self.host(a+i+1)
            if i==0:
                for j in range(a-1):
                    stages=list(range(a+1,a+j+2));self.emit('IDLE_ONE',2+j,stages);self.emit('IDLE_ONE',L+2+j,stages)
            self.mix(C)
        for r in range(self.n):self.emit('LAMBDA',r,-1)
        masks=[]
        for off in(0,L):
            masks.append(list(range(1,2*a+1)))
            masks += [list(range(i+1,a+1))for i in range(a)]
            masks += [list(range(a+1,a+j+2))for j in range(a)]
        need(len(masks)==self.n,'all productive masks')
        counts=Counter(e[0]for e in self.events)
        need(counts['HOST2']==2*a and counts['QUERY']==4 and counts['IDLE_ONE']==4*(a-1),'complete caller counts')
        T=Counter(1+self.b*len(m)for m in masks);P=Counter({1:4})
        for e in self.events:
            if e[0]=='IDLE_ONE':P[self.b*len(e[2])]+=1
        return dict(schema='S012-E-free-short-caller/1',arms=a,stages=2*a,roles=self.n,
            native_dimension=self.b+1,body_dimension=self.b,ambient_cap=self.b+1+2*a*self.b,
            port_type='all type A; four distinct native mains per port per invocation',
            head_relation='Q^4=I',endpoint=[dict(role=r,head_exponent=-1,stages=m)for r,m in enumerate(masks)],
            events=self.events,counts=dict(sorted(counts.items())),
            wrapper_invoice_per_port=dict(T=dict(sorted(T.items())),P=dict(sorted(P.items()))))

def main(out,a,b):
    C=Builder(a,b).run();out.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(C,sort_keys=True,separators=(',',':')).encode();(out/'CALLER.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    meta={k:v for k,v in C.items()if k not in('events','endpoint')};meta['canonical_sha256']=hashlib.sha256(raw).hexdigest()
    (out/'BUILD.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n');print(json.dumps(meta,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--arms',type=int,default=4);p.add_argument('--body',type=int,default=17);p.add_argument('--out',type=Path,default=HERE/'a4-h18');a=p.parse_args();need(a.arms>=1 and a.body>=1,'positive shape');main(a.out,a.arms,a.body)
