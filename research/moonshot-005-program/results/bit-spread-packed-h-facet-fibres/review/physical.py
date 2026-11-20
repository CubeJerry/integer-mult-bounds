"""Native GF64 H/D/K/facet propagation from true route IDs."""
from collections import Counter,defaultdict
from functools import lru_cache
from hashlib import sha256
import ctypes,gzip,json
import numpy as np
SR={49:(3,2),97:(1,1),53:(1,2),77:(7,1),93:(1,7),8:(1,2),82:(3,1),58:(2,1),106:(1,1),31:(1,1),105:(1,2)}
FR={49:(2,1),97:(2,1),53:(1,1),77:(1,2),93:(1,1),8:(1,1),82:(1,1),58:(1,1),106:(4,1),31:(1,1),105:(1,1)}
def check(v,msg):
    if not v:raise ValueError(msg)
def payload(path,pin):
    data=gzip.decompress(path.read_bytes());check(sha256(data).hexdigest()==pin,'pinned '+path.name);return json.loads(data)
class Physical:
    def __init__(self,repo,n,f,mm_library=None):
        self.f,self.n=f,n;b=repo/'research/moonshot-005-program/results';self.K=payload(b/'bit-gf64-actual-k-atlas/author/output/SPREAD-OWNERS.json.gz','513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0')
        self.dp=payload(b/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz','9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15')
        raw=f.read_source(b,'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
        self.routes={};self.flags=defaultdict(list);self.middle=defaultdict(list);fans=defaultdict(set)
        for v in map(json.loads,raw.splitlines()):
            p,j,t,h,d,k,_,_=v;u=(p=='Y')*53280+480*j+t;self.routes[u]=v;self.middle[d].append(u)
            if h is not None:self.flags[h,d,p].append(u);fans[h].add(d)
        for bkt in (self.flags,self.middle):
            for vals in bkt.values():vals.sort()
        self.fans={h:{k:[d for d in sorted(ds) if (d in n.marked)==(k==3)] for k in (3,12)} for h,ds in fans.items()}
        self.waves={k:f.power_matrix(range(1,3*k+1),3*k) for k in (3,12)}
        self.jet={k:np.zeros_like(v)for k,v in self.waves.items()}
        for k,v in self.waves.items():self.jet[k][:,1::2]=v[:,:-1:2]
        self.fast=None
        if mm_library:
            self.fast=ctypes.CDLL(str(mm_library.resolve())).gf64_gemm
            self.fast.argtypes=[ctypes.c_void_p]*4+[ctypes.c_size_t]*3;self.fast.restype=None
    def mm(self,A,B):
        if self.fast is None:return self.f.matmul(A,B)
        A,B=np.ascontiguousarray(A),np.ascontiguousarray(B)
        check(A.dtype==B.dtype==np.uint8 and A.shape[1]==len(B),'native product')
        C=np.zeros((len(A),B.shape[1]),dtype=np.uint8)
        self.fast(A.ctypes.data,B.ctypes.data,C.ctypes.data,self.f.MUL.ctypes.data,len(A),len(B),B.shape[1]);return C
    def half(self,j):
        return set([h for h in self.n.hlist[j] if self.n.early[j,h]==15][:12])
    @lru_cache(None)
    def vm(self,node,der=False,scale=1):
        v=self.f.power_matrix([node],16)[0]
        if der:
            dr=np.zeros_like(v);dr[1::2]=v[:-1:2];v=dr
        return self.f.MUL[scale,v]
    def source(self,j):
        n=self.n;left={};first=self.half(j)
        for node,h in enumerate(n.hlist[j],1):
            members=sorted(n.H[h]&set(range(111)));m=len(members);qe={t:n.early[t,h]//15 for t in members}
            ex=sum(qe.values())//3;big=max(members,key=qe.get)
            for k in (3,12):
                size=3*k;offset=0 if k==3 else 96;cache=[]
                for ph,reps in [('X',ex),('Y',2-ex)]:
                    if m==3:owners=[t for t in members for _ in range(k)]
                    elif m==2:
                        small=next(t for t in members if t!=big)
                        owners=([big]*(2*k)+[small]*k)if ph=='X' else [small]*k+[None]*(2*k)
                    else:owners=[j if ph=='X' else None]*size
                    for s in range(reps):
                        feed=np.zeros((size,32*k),dtype=np.uint8)
                        for t,p in enumerate(owners):
                            if p!=j:continue
                            if m==1:
                                channel=t%(2*k);der=t>=2*k;scale=SR[j][k==12] if der else 1
                            elif m==2 and qe[j]==2:channel=t;der=False;scale=1
                            elif m==3 and ex==2:channel=t%k+k*s;der=False;scale=1
                            else:channel=t%k+(0 if ((ph=='X')==(h in first)) else k);der=False;scale=1
                            feed[t,16*channel:16*channel+16]=self.vm(node,der,scale)
                        Z=self.mm(self.waves[k],feed)
                        if ph=='X':cache.append(feed)
                        elif m<3:
                            coeff=self.jet[k].copy()
                            if m==2:coeff[:,2*k:]=0
                            Z^=self.mm(coeff,cache[s])
                        for dp,d in enumerate(self.fans[h][k]):
                            rid=self.flags[h,d,ph][s];v=np.zeros(480,dtype=np.uint8);v[offset:offset+32*k]=Z[dp];left[rid]=v
        return left
    @lru_cache(None)
    def dword(self,d):
        f=self.f;ids=self.middle[d];tag,m,n,w=self.dp[d];check(tag==d and m+n==len(ids) and sum(self.routes[u][0]=='X' for u in ids)==m,'true D-owner margin')
        def cauchy(x,y):
            return f.INVERSE[np.asarray(x,dtype=np.uint8)[:,None]^(32+np.asarray(y,dtype=np.uint8)[None,:])]
        A=np.zeros((m+n,m+n),dtype=np.uint8)
        A[:m,:m]=cauchy(range(m),range(m));A[m:,m:]=cauchy(range(n),range(n))
        if w:
            L=cauchy(range(n),range(n,n+len(w)));R=cauchy(range(m,m+len(w)),range(m))
            A[m:,:m]=self.mm(f.MUL[L,np.asarray(w,dtype=np.uint8)[None,:]],R)
        return A
    @lru_cache(16)
    def terminal(self,i):
        n=self.n;first=self.half(i);dual={};dc={};terminal={}
        for node,h in enumerate(n.hlist[i],1):
            chart=self.K[str(h)];cnt=Counter();size=len(n.H[h]&set(range(111)));q=n.early[i,h]//15
            for ph,ins,outs in chart['stripes']:
                k=len(ins)//3;s=cnt[ph,k];cnt[ph,k]+=1
                for t,r in enumerate(outs):
                    px,j,_,_,_,at,_,end=self.routes[r];check(px==ph and at==h,'true K moment rows')
                    take=end if ph=='X' else j;v=np.zeros(32*k,dtype=np.uint8)
                    if take==i:
                        der=False;scale=1
                        if size==3 and q==2:ch=t%k+k*s
                        elif size==2 and q==2:ch=t
                        elif size==1:
                            der=t>=2*k;ch=t%(2*k);scale=FR[i][k==12] if der else 1
                        else:ch=t%k+(0 if ((h in first)==(ph=='Y')) else k)
                        v[16*ch:16*ch+16]=self.vm(node,der,scale)
                        terminal[r]=(k,v.copy())
                    dc[r]=v
            for u,v in chart['early_cache_to_late']:dc[u]^=dc[v]
            for ph,ins,outs in chart['stripes']:
                k=len(ins)//3;A=self.mm(self.waves[k],np.vstack([dc[u] for u in outs]))
                for rid,row in zip(ins,A):dual[rid]=row
        return dual,terminal
    def propagate(self,j):
        left=self.source(j);delivered={}
        for d in {self.routes[u][4] for u in left}:
            ids=self.middle[d];spots=[t for t,r in enumerate(ids) if r in left]
            check(len(spots)==8,'complete native D-entrance section')
            Z=self.mm(self.dword(d)[:,spots],np.stack([left[ids[t]] for t in spots]));delivered.update(zip(ids,Z))
        at={}
        for h in {self.routes[r][5] for r in delivered if str(self.routes[r][5]) in self.K}:
            chart=self.K[str(h)]
            for ph,ins,outs in chart['stripes']:
                k=len(ins)//3;idx=[u for u,r in enumerate(ins)if r in delivered]
                if not idx:continue
                Z=self.mm(self.waves[k][idx].T,np.stack([delivered[ins[u]] for u in idx]));at.update(zip(outs,Z))
            for a,b in chart['early_cache_to_late']:
                if a in at:at[b]=at.get(b,np.zeros(480,dtype=np.uint8))^at[a]
        return at
    def check_binary_K(self,base):
        templates=payload(base/'bit-gf64-actual-k-atlas/author/output/TEMPLATES.json.gz','6691b46a45b253e1e48f073f2114aed0c817e786b7efe7dce3dfa440c01cc73d')
        for k,V in self.waves.items():
            work=[1<<t for t in range(18*k)]
            for dest,src in templates[str(3*k)]:work[dest]^=work[src]
            expected=[]
            for row in V.T:
                words=[0]*6
                for j,c in enumerate(row):
                    for t in range(6):
                        for bit in range(6):
                            if self.f.MUL[c,1<<t]>>bit&1:words[bit]|=1<<(6*j+t)
                expected.extend(words)
            check(work==expected,'true K binary transposed moment template')
