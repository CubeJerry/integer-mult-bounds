#!/usr/bin/env python3
"""Exact 480-coordinate response of the all-RS spread proper word."""
from __future__ import annotations
import argparse,ctypes,gzip,hashlib,json
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import numpy as np
from build import COPIES,PRODUCT,field_rank,grouped_sources,power,require,unpack
from rs_source import SINGLETON_SCALE,coefficients,source_slot
from terminal import K_PINS,k_row,payload

TABLE=np.asarray(PRODUCT,dtype=np.uint8)
D_PIN="9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15"
INV=np.array([0]+[power(x,62) for x in range(1,64)],dtype=np.uint8)
BODY=480


class Arithmetic:
    def __init__(self,library=None):
        self.native=None
        if library:
            self.native=ctypes.CDLL(str(Path(library).resolve())).gf64_gemm
            self.native.argtypes=[ctypes.c_void_p]*4+[ctypes.c_size_t]*3
            self.native.restype=None

    def matmul(self,a,b):
        a=np.ascontiguousarray(a,dtype=np.uint8)
        b=np.ascontiguousarray(b,dtype=np.uint8)
        require(a.ndim==2 and b.ndim==2 and a.shape[1]==b.shape[0],"compatible GF factors")
        out=np.zeros((len(a),b.shape[1]),dtype=np.uint8)
        if self.native is not None:
            self.native(a.ctypes.data,b.ctypes.data,out.ctypes.data,TABLE.ctypes.data,
                        len(a),a.shape[1],b.shape[1])
        else:
            for k in range(a.shape[1]):
                out^=TABLE[a[:,k,None],b[k,None,:]]
        return out


class Atlas:
    """Use factors(i,j) for R, D[60,8,8], L in the same actual D boundary orders."""
    def __init__(self,repo,k_words,d_charts,library=None):
        self.ops=Arithmetic(library)
        base=Path(repo)/"research/moonshot-005-program/results"
        geo=json.loads(unpack(base,"geometry")); self.H=list(map(set,geo["A2"])); self.D=list(map(set,geo["D4"]))
        self.dual=geo["dual_D4"];roots=geo["root_table"]
        self.orth=[{j for j,y in enumerate(roots)if sum(a*b for a,b in zip(x,y))==0}for x in roots]
        self.marked=set(json.loads(unpack(base,"spread"))["selected_D"])
        self.phase=json.loads(unpack(base,"phases"))
        self.ks={i:[h for h,p in enumerate(self.H)if i in p]for i in range(111)}
        self.nodes={(i,h):s+1 for i,hs in self.ks.items()for s,h in enumerate(hs)}
        self.colours={}
        for j,hs in self.ks.items():
            self.colours[j]={"singleton":{h for h in hs if self.phase[str(h)]["m"]==1},
                             "first":set([h for h in hs if self.phase[str(h)]["donor_early"][str(j)]==15][:12])}
        self.route={};self.left_flags=defaultdict(list);self.middle=defaultdict(list)
        for l in unpack(base,"routes").splitlines():
            r=json.loads(l); phase,role,local,h,d,k,_,_=r
            fid=(53280 if phase=="Y" else 0)+480*role+local
            self.route[fid]=r; self.middle[d,phase].append(fid)
            if h is not None:self.left_flags[h,d,phase].append(fid)
        for flags in (self.left_flags,self.middle):
            for owners in flags.values():owners.sort()
        ds=defaultdict(set)
        for h,d,_ in self.left_flags:ds[h].add(d)
        self.h_ports={h:([d for d in sorted(ports)if d in self.marked],
                         [d for d in sorted(ports)if d not in self.marked]) for h,ports in ds.items()}
        self.kr=payload(Path(k_words)/"SPREAD-OWNERS.json.gz",K_PINS["spread"])
        self.dp=payload(Path(d_charts),D_PIN)
        self.All=[(n,c,t)for n in (9,36)for c in range(2*(n//3))for t in range(16)]
        self.index={(n,c):q for q,(n,c,t) in enumerate(self.All)if t==0}
        require(len(self.All)==480,"base canonical width")
        self.V={n:np.array([[power(z,t)for t in range(n)]for z in range(1,n+1)],dtype=np.uint8)for n in (9,36)}
        self.deriv={n:np.array([[power(z,t-1)if t%2 else 0 for t in range(n)]for z in range(1,n+1)],
                               dtype=np.uint8)for n in (9,36)}
        self._check_copies()

    def _check_copies(self):
        """Both physical endpoints use (component,copy,channel,power) order in their raw basis."""
        labels=[(n,e,c,t)for n in (9,36)for e in range(8)for c in range(2*(n//3))for t in range(16)]
        self.raw_to_copy_base=[(e,self.index[n,c]+t)for n,e,c,t in labels]
        require(sorted(self.raw_to_copy_base)==[(e,u)for e in range(8)for u in range(480)],"same raw I basis")
        for j in range(111):
            for h in self.ks[j]:
                p=self.phase[str(h)];q=p["donor_early"][str(j)];donors=sorted(self.H[h]&set(range(111)))
                quo={int(l):v for l,v in p["donor_early"].items()}
                for n in (9,36):
                    for kind,tag in (("X","early"),("Y","late")):
                        nc=p[tag]
                        if not nc:continue
                        gc=grouped_sources(kind,donors,p["m"],n//3,quo)
                        for t,g in enumerate(gc):
                            if g!=j:continue
                            for stripe in range(nc):
                                first=source_slot(kind,h,j,t,8*stripe,n,p,self.colours[j],q)
                                for e in range(8):
                                    got=source_slot(kind,h,j,t,8*stripe+e,n,p,self.colours[j],q)
                                    require(got==(e,*first[1:]),"source and H copy equivariance")
                words=self.kr[str(h)];cnt=Counter()
                for kind,ins,outs in words["stripes"]:
                    n=len(ins);b=cnt[kind,n];cnt[kind,n]+=1
                    for t,u in enumerate(outs):
                        rt=self.route[u];dest=rt[1]if kind=="Y"else rt[7]
                        if dest!=j:continue
                        ref=k_row(kind,p["m"],q,j,t,n,h in self.colours[j]["first"],b,0)
                        for e in range(8):
                            got=k_row(kind,p["m"],q,j,t,n,h in self.colours[j]["first"],b,e)
                            require(got==(e,*ref[1:]),"F and K copy equivariance")

    def put(self,A,r,n,c,node,der,scale):
        offset=self.index[n,c]
        A[r,offset:offset+16]=coefficients(node,der,scale)

    @lru_cache(maxsize=12)
    def left(self,j):
        """H outbound donor rows keyed by actual body-level owner ID."""
        out={}
        for h in self.ks[j]:
            p=self.phase[str(h)];whole=sorted(self.H[h]&set(range(111)));q={int(i):v for i,v in p["donor_early"].items()}
            for ds in self.h_ports[h]:
                n=len(ds);k=n//3;early={}
                for kind,tag in (("X","early"),("Y","late")):
                    if not p[tag]:continue
                    group=grouped_sources(kind,whole,p["m"],k,q)
                    for stripe in range(p[tag]):
                        coef=np.zeros((n,BODY),dtype=np.uint8)
                        for t,source in enumerate(group):
                            if source!=j:continue
                            _,c,der,scale=source_slot(kind,h,j,t,8*stripe,n,p,self.colours[j],q[j])
                            self.put(coef,t,n,c,self.nodes[j,h],der,scale)
                        values=self.ops.matmul(self.V[n],coef)
                        if kind=="X":early[stripe]=coef
                        elif p["m"] in (1,2):
                            cross=self.deriv[n].copy()
                            if p["m"]==2:cross[:,2*k:]=0
                            values^=self.ops.matmul(cross,early[stripe])
                        for a,d in enumerate(ds):out[self.left_flags[h,d,kind][stripe]]=values[a]
        return out

    @lru_cache(maxsize=12)
    def right(self,i):
        """K incoming rows of the field-dual facet transfer, keyed by actual owner."""
        out={}
        for h in self.ks[i]:
            chart=self.kr[str(h)];p=self.phase[str(h)];cnt=Counter();duals={}
            for kind,inp,output in chart["stripes"]:
                n=len(inp);s=cnt[kind,n];cnt[kind,n]+=1
                for t,u in enumerate(output):
                    rt=self.route[u];dest=rt[1]if kind=="Y"else rt[7]
                    arr=np.zeros((1,BODY),dtype=np.uint8)
                    if dest==i:
                        _,c,der,scale=k_row(kind,p["m"],p["donor_early"][str(i)],i,t,n,h in self.colours[i]["first"],s,0)
                        self.put(arr,0,n,c,self.nodes[i,h],der,scale)
                    duals[u]=arr[0]
            for early,late in chart["early_cache_to_late"]:duals[early]^=duals[late]
            for kind,inp,output in chart["stripes"]:
                values=self.ops.matmul(self.V[len(inp)],np.array([duals[u]for u in output]))
                for a,u in enumerate(inp):out[u]=values[a]
        return out

    @lru_cache(maxsize=3150)
    def middle_matrix(self,d):
        _,m,n,weights=self.dp[d];r=len(weights)
        early=self.middle[d,"X"];late=self.middle[d,"Y"]
        require((m,n)==(len(early),len(late)),"D true owner widths")
        def C(rows,cols):
            return INV[np.bitwise_xor(np.array(rows,dtype=np.uint8)[:,None],32+np.array(cols,dtype=np.uint8)[None,:])]
        M=np.zeros((m+n,m+n),dtype=np.uint8)
        M[:m,:m]=C(range(m),range(m));M[m:,m:]=C(range(n),range(n))
        if r:
            read=C(range(n),range(n,n+r))
            write=C(range(m,m+r),range(m))
            M[m:,:m]=self.ops.matmul(TABLE[read,np.array(weights,dtype=np.uint8)[None,:]],write)
        return M,early+late

    def factors(self,i,j):
        require(i in range(111)and j in self.orth[i]and j<111,"foreign native pair required")
        mids=[d for d,S in enumerate(self.D)if j in S and i in self.D[self.dual[d]]]
        require(len(mids)==60,"actual 60 D pair boundary")
        lh=self.left(j);rk=self.right(i);LP=[];M=[];RP=[]
        for d in mids:
            full,owners=self.middle_matrix(d)
            c=[a for a,u in enumerate(owners)if u in lh]
            r=[a for a,u in enumerate(owners)if u in rk]
            require(len(c)==len(r)==8,"eight actual boundary owners")
            LP.extend(lh[owners[a]]for a in c)
            RP.extend(rk[owners[a]]for a in r)
            M.append(full[np.ix_(r,c)])
        return np.array(RP,dtype=np.uint8).T,np.array(M,dtype=np.uint8),np.array(LP,dtype=np.uint8)

    def block(self,i,j):
        if j not in self.orth[i]:
            return np.zeros((480,480),dtype=np.uint8)
        R,D,L=self.factors(i,j)
        middle=np.vstack([self.ops.matmul(d,l)for d,l in zip(D,L.reshape(60,8,480))])
        return self.ops.matmul(R,middle)

    def apply(self,i,j,batch):
        R,D,L=self.factors(i,j)
        inputs=self.ops.matmul(L,batch)
        mid=np.vstack([self.ops.matmul(d,v)for d,v in zip(D,inputs.reshape(60,8,-1))])
        return self.ops.matmul(R,mid)


    @lru_cache(maxsize=16)
    def facet(self,i):
        """Explicit F matrices in stable sorted base-owner IDs: (early_ids,E^T; late_ids,Y^T)."""
        early_weights={};late_weights={}
        for h in self.ks[i]:
            p=self.phase[str(h)];cnt=Counter()
            for kind,_,outs in self.kr[str(h)]["stripes"]:
                n=len(outs);s=cnt[kind,n];cnt[kind,n]+=1
                for t,u in enumerate(outs):
                    rt=self.route[u];dest=rt[1]if kind=="Y"else rt[7]
                    if dest!=i:continue
                    _,c,der,scale=k_row(kind,p["m"],p["donor_early"][str(i)],i,t,n,h in self.colours[i]["first"],s,0)
                    arr=np.zeros((1,BODY),dtype=np.uint8)
                    self.put(arr,0,n,c,self.nodes[i,h],der,scale)
                    (late_weights if kind=="Y"else early_weights)[u]=arr[0]
        e=sorted(early_weights); y=sorted(late_weights)
        return e,np.stack([early_weights[u]for u in e]).T,y,np.stack([late_weights[u]for u in y]).T

    def terminal_inputs(self,i,j):
        """Actual F input row matrices E,Y indexed by the returned sorted physical holder IDs."""
        require(j in self.orth[i] and j<111,"native foreign pair")
        lh=self.left(j);delivery={}
        for d,S in enumerate(self.D):
            if j not in S or i not in self.D[self.dual[d]]:continue
            full,owners=self.middle_matrix(d)
            ci=[s for s,u in enumerate(owners)if u in lh]
            ro=[s for s,u in enumerate(owners)if self.route[u][5] is not None and i in self.H[self.route[u][5]]]
            require(len(ci)==len(ro)==8,"actual proper K delivery")
            batch=self.ops.matmul(full[np.ix_(ro,ci)],np.stack([lh[owners[s]]for s in ci]))
            for s,v in zip(ro,batch):delivery[owners[s]]=v
        e,_,y,_=self.facet(i); val={};z0=np.zeros(BODY,dtype=np.uint8)
        for h in self.ks[i]:
            ch=self.kr[str(h)]
            for _,ins,outs in ch["stripes"]:
                z=self.ops.matmul(self.V[len(ins)].T,np.stack([delivery.get(u,z0)for u in ins]))
                for u,v in zip(outs,z):val[u]=v
            for a,b in ch["early_cache_to_late"]:val[b]^=val[a]
        return e,np.stack([val[u]for u in e]),y,np.stack([val[u]for u in y])

def rank_fast(matrix):
    M=np.array(matrix,copy=True);rank=0
    for c in range(M.shape[1]):
        p=np.flatnonzero(M[rank:,c])
        if not len(p):continue
        u=rank+int(p[0])
        M[[rank,u]]=M[[u,rank]]
        row=TABLE[INV[M[rank,c]],M[rank,c:]]
        M[rank+1:,c:]^=TABLE[M[rank+1:,c,None],row[None,:]]
        rank+=1
        if rank==M.shape[0]:break
    return rank

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,required=True);p.add_argument("--k-words",type=Path,required=True)
    p.add_argument("--d-charts",type=Path,required=True);p.add_argument("--library",type=Path)
    p.add_argument("--block",action="append",default=[]);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();atlas=Atlas(a.repo,a.k_words,a.d_charts,a.library);a.out.mkdir(parents=True,exist_ok=True)
    rec={}
    for arg in a.block:
        i,j=map(int,arg.split(","))
        B=atlas.block(i,j);rank=rank_fast(B)
        x=np.array([[(13*c+7*t)%64 for t in range(3)]for c in range(480)],dtype=np.uint8)
        require(np.array_equal(atlas.apply(i,j,x),atlas.ops.matmul(B,x)),"matrix/application agree")
        np.save(a.out/f"B-{i}-{j}.npy",B,allow_pickle=False)
        rec[arg]={"rank":rank,"matrix_payload_sha256":hashlib.sha256(B.tobytes()).hexdigest()}
    (a.out/"RESULT.json").write_text(json.dumps(rec,sort_keys=True,indent=2)+"\n")
    print(rec)
