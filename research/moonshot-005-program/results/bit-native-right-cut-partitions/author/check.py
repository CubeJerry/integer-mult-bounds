#!/usr/bin/env python3
"""Backward extraction of right inverse sections without any source, H or D word."""
import argparse
from collections import Counter,defaultdict
from functools import lru_cache
import gzip,hashlib,json
from pathlib import Path
import sys
import numpy as np

class Right:
    def __init__(self,args):
        base=args.repo/'research/moonshot-005-program/results';geo=json.loads(unpack(base,'geometry'))
        self.H=list(map(set,geo['A2']));self.D=list(map(set,geo['D4']));self.dual=geo['dual_D4']
        self.ph=json.loads(unpack(base,'phases'));self.rt={};self.middle=defaultdict(list)
        self.vis=defaultdict(list);roots=geo['root_table']
        self.orth={i:{j for j,t in enumerate(roots[:111])if sum(x*y for x,y in zip(roots[i],t))==0}for i in range(111)}
        for line in unpack(base,'routes').splitlines():
            z=json.loads(line);ph,role,c,h,d,k,source,sink=z;u=480*role+c+(53280 if ph=='Y'else 0)
            self.rt[u]=z;self.middle[d,ph].append(u)
            if k is not None and sink is not None:self.vis[sink,k,ph].append(u)
        for t in self.middle.values():t.sort()
        for t in self.vis.values():t.sort()
        self.planes={i:[h for h,g in enumerate(self.H)if i in g]for i in range(111)}
        self.K={code:payload(args.k/(code.upper()+'-OWNERS.json.gz'),K_PINS[code])for code in ('spread','mixed')}
        raw=gzip.decompress((args.f/'WORDS.json.gz').read_bytes())
        require(hashlib.sha256(raw).hexdigest()=='282f16cd16f99f71fe0d2ad6c97c3138e3263be4adf8e46ad9182ebd12146f01','minimum F coefficients')
        self.weights={mode.lower():{i:w for i,w in records}for mode,records in json.loads(raw).items()}
        self.V={n:np.array([[power(z,t)for t in range(n)]for z in range(1,n+1)],dtype=np.uint8)for n in (9,36,45)}
        self.ops=Arithmetic(args.library)
    def cauchy(self,r,c):
        return INV[np.array(r,dtype=np.uint8)[:,None]^(32+np.array(c,dtype=np.uint8))[None,:]]
    @lru_cache(maxsize=8)
    def body(self,i,mode,facet):
        planes=self.planes[i];half=set([h for h in planes if self.ph[str(h)]['donor_early'][str(i)]==15][:12]);outgoing={}
        if facet=='min':
            e_bands=[];y_bands=[]
            for h in planes:
                word=self.K[mode][str(h)];ee=self.vis[i,h,'X'];yy=self.vis[i,h,'Y'].copy()
                if ee:
                    require(len(ee)==len(yy)==15,'mixed early/late bands');e_bands.append(ee)
                if len(yy)==45:
                    selected=sorted(u for ph,ins,outs in word['stripes']if ph=='Y'for u in outs[:2*len(ins)//3]);yy=selected+sorted(set(yy)-set(selected))
                y_bands.extend(yy[t:t+15]for t in range(0,len(yy),15))
            require(len(y_bands)==32 and all(len(g)==15 for g in y_bands),'min terminal native bands')
            w=np.array(self.weights[mode][i],dtype=np.uint8);n=len(w)
            S=self.ops.matmul(TABLE[self.cauchy(range(32),range(n)),w[None,:]],self.cauchy(range(n),range(len(e_bands))))
            for b,ys in enumerate(y_bands):
                for t,y in enumerate(ys):
                    q=y-53280-480*i
                    outgoing.setdefault(y,np.zeros(480,dtype=np.uint8))[q]=1
                    for eb,ee in enumerate(e_bands):outgoing.setdefault(ee[t],np.zeros(480,dtype=np.uint8))[q]^=S[b,eb]
        else:
            for pos,h in enumerate(planes):
                p=self.ph[str(h)];q=p['donor_early'][str(i)];word=self.K[mode][str(h)];indices=Counter()
                for ph,ins,outs in word['stripes']:
                    n=len(ins);s=indices[ph,n];indices[ph,n]+=1
                    for t,u in enumerate(outs):
                        rz=self.rt[u];who=rz[1]if ph=='Y'else rz[7]
                        if who!=i:continue
                        _,channel,der,scale=k_row(ph,p['m'],q,i,t,n,h in half,s,0);row=np.zeros(480,dtype=np.uint8);start=16*(channel+(6 if n==36 else 0))
                        row[start:start+16]=coefficients(pos+1,der,scale);outgoing[u]=row
        rows={}
        for h in planes:
            word=self.K[mode][str(h)];z={}
            for ph,ins,outs in word['stripes']:
                for u in outs:z[u]=outgoing.get(u,np.zeros(480,dtype=np.uint8)).copy()
            for e,y in word['early_cache_to_late']:z[e]^=z[y]
            for ph,ins,outs in word['stripes']:
                blocks=self.ops.matmul(self.V[len(ins)],np.stack([z[u]for u in outs]))
                for j,t in enumerate(ins):rows[t]=blocks[j]
        return rows
    @lru_cache(maxsize=150)
    def quotient(self,i,j,mode,facet):
        r=self.body(i,mode,facet);ds=[d for d,S in enumerate(self.D)if j in S and i in self.D[self.dual[d]]]
        require(len(ds)==60 and j in self.orth[i],'true sixty-node proper restriction')
        allrows=[]
        for d in ds:
            ids=[u for u in self.middle[d,'X']+self.middle[d,'Y']if u in r];require(len(ids)==8,'eight proper K fields')
            allrows.extend(r[u]for u in ids)
        RT=np.stack(allrows);inv=inverse(RT)
        require(np.array_equal(self.ops.matmul(RT,inv),np.eye(480,dtype=np.uint8)),'native inverse readout')
        return {d:inv[:,8*q:8*q+8].T.copy()for q,d in enumerate(ds)}

def main(args):
    A=Right(args);labels=json.loads(args.witness.read_text());rec=labels['receivers'];require(rec==[3,35],"specified regular receivers")
    out={};expected={'spread_rs':[96,94],'spread_min':[415,416],'mixed_rs':[479,480],'mixed_min':[479,480]}
    for name,w in sorted(labels['cases'].items()):
        mode,facet=name.split('_');indices=w['labels'];ranks=[];dig=[]
        for i in rec:
            mats=[]
            for j,d in indices:
                require(j!=10 and i!=80 and j in A.orth[i] and j in A.D[d] and i in A.D[A.dual[d]],'common ordinary identity edge')
                Q=A.quotient(i,j,mode,facet)[d];require(rank_fast(Q)==8,'surjective eight fields')
                mats.append(Q)
            matrix=np.vstack(mats);ranks.append(rank_fast(matrix));dig.append(hashlib.sha256(matrix.tobytes()).hexdigest())
        require(ranks==w['ranks']==expected[name], 'different joint refinements for the same named labels')
        out[name]={'labels':len(indices),'receivers':rec,'base_ranks':ranks,'eight_copy_ranks':[8*v for v in ranks],'binary_ranks':[48*v for v in ranks],'stack_sha256':dig}
        print(name,ranks,flush=True)
    require(set(out)==set(expected),'four right words')
    args.out.mkdir(exist_ok=True,parents=True);(args.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ('repo','k','f','h-author','left-proof','out'):p.add_argument('--'+s,type=Path,required=True)
    p.add_argument('--witness',type=Path,default=Path(__file__).parent/'output/WITNESSES.json');p.add_argument('--library',type=Path)
    args=p.parse_args();sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.left_proof))
    from body import inverse
    from build import require,power,unpack
    from transfer import TABLE,INV,Arithmetic,rank_fast
    from rs_source import coefficients
    from terminal import K_PINS,payload,k_row
    main(args)
