"""Independently reconstruct the 3 by 6 physical blocks without importing a candidate checker."""
import argparse
from collections import Counter,defaultdict
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

ROW=[73,12,56]
COL=[15,20,33,34,39,44]
PINS={
 'geom':('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
 'routes':('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'),
 'marks':('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz','7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab')}
SCALES={49:(3,2),97:(1,1),53:(1,2),77:(7,1),93:(1,7),8:(1,2),82:(3,1),58:(2,1),106:(1,1),31:(1,1),105:(1,2)}


def need(x,s):
    if not x:raise ValueError(s)


def read(file,pin):
    raw=gzip.decompress(file.read_bytes());need(hashlib.sha256(raw).hexdigest()==pin,'pin '+file.name);return raw


def times(u,v):
    z=0
    for i in range(6):
        if u&(1<<i):z^=v<<i
    for i in range(10,5,-1):
        if (1<<i)&z:z^=67<<(i-6)
    return z


M=np.array([[times(i,j) for j in range(64)] for i in range(64)],dtype=np.uint8)
inv=np.array([0]+[next(j for j in range(1,64) if times(i,j)==1) for i in range(1,64)],dtype=np.uint8)
powers=np.ones((64,46),dtype=np.uint8)
for n in range(1,46):powers[:,n]=M[powers[:,n-1],np.arange(64)]


def times_matrix(a,b):
    need(a.shape[1]==len(b),'contraction dimensions')
    return np.bitwise_xor.reduce(M[a[:,:,None],b[None,:,:]],axis=1)


def prepared(args):
    folder=args.repo/'research/moonshot-005-program/results';src={k:read(folder/f,p) for k,(f,p) in PINS.items()}
    z=json.loads(src['geom']);s=set(json.loads(src['marks'])['selected_D']);rtl={};p_h=defaultdict(lambda:defaultdict(list));p_d=defaultdict(lambda:defaultdict(list))
    for x in src['routes'].splitlines():
        r=json.loads(x);ph,j,c,h,d,k,ln,tm=r;w=(0 if ph=='X' else 53280)+480*j+c;rtl[w]=r
        if d is not None:p_d[d][ph].append(w)
        if h is not None:p_h[h][ph,d].append(w)
    for b in list(p_h.values())+list(p_d.values()):
        for ids in b.values():ids.sort()
    Hd={};Nd={}
    for h,flag in p_h.items():
        ds=sorted({d for ph,d in flag});pos={}
        for part in ([d for d in ds if d in s],[d for d in ds if d not in s]):
            for r,d in enumerate(part):pos[d]=len(part),r+1
        Hd[h]=pos
        Nd[h]=Counter(rtl[w][1] for (ph,d),v in flag.items() if ph=='X' for w in v)
    half={};nodes={}
    for j in range(111):
        hs=[h for h,p in enumerate(z['A2']) if j in p];half[j]=set([h for h in hs if Nd[h][j]==15][:12]);nodes[j]={h:t+1 for t,h in enumerate(hs)}
    ks={}
    for name,pin in [('spread','513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0'),('mixed','8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a')]:
        ks[name]=json.loads(read(args.k_words/(name.upper()+'-OWNERS.json.gz'),pin))
    dwords=json.loads(read(args.d_words/'CHARTS.json.gz','9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15'))
    return z,rtl,p_h,p_d,Hd,Nd,half,nodes,dwords,ks


def port_form(h,d,w,j,data):
    z,rtl,p_h,p_d,Hd,Nd,half,nodes,dwords,ks=data
    phase=rtl[w][0];stripe=p_h[h][phase,d].index(w);ns=sorted(Nd[h]);card=len(ns);n,x=Hd[h][d];k=n//3
    early_count=len(p_h[h]['X',d]);basis=powers[nodes[j][h],:16]
    dest=np.zeros(480,dtype=np.uint8)
    for inputphase in ('X','Y'):
        if phase=='X' and inputphase!='X':continue
        derivative=inputphase!=phase
        if derivative and card==3:continue
        for t in range(n):
            if card==3:donor=ns[t//k]
            elif card==2:
                big=next(i for i in ns if Nd[h][i]==30);small=next(i for i in ns if i!=big)
                donor=(big if t<2*k else small) if inputphase=='X' else (small if t<k else None)
            else:donor=ns[0] if inputphase=='X' else None
            if donor!=j:continue
            if derivative and (t%2==0 or t>=(2*k if card==2 else n)):continue
            weight=powers[x,t-1 if derivative else t];vector=basis
            if card==1 and t>=2*k:
                c=t-2*k;vector=np.zeros(16,dtype=np.uint8);vector[1::2]=M[SCALES[j][n==36],basis[:15:2]]
            elif card==1 or (card==2 and Nd[h][j]==30):c=t
            elif card==3 and early_count==2:c=t%k+stripe*k
            else:c=t%k+(0 if ((h in half[j])==(inputphase=='X')) else k)
            off=(c+(6 if n==36 else 0))*16;dest[off:off+16]^=M[weight,vector]
    return dest


def donor(j,data):
    z,rtl,p_h,p_d,Hd,Nd,half,nodes,dwords,ks=data;ds=[d for d,p in enumerate(z['D4']) if j in p and set(ROW).intersection(z['D4'][z['dual_D4'][d]])]
    after={}
    for d in ds:
        tag,m,n,weights=dwords[d];need(d==tag,'D witness number');allids=p_d[d]['X']+p_d[d]['Y'];need(len(allids)==m+n,'all D owner margins')
        ins=[k for k,w in enumerate(allids) if rtl[w][3] is not None and j in z['A2'][rtl[w][3]]]
        outs=[k for k,w in enumerate(allids) if rtl[w][5] is not None and set(ROW).intersection(z['A2'][rtl[w][5]])]
        need(len(ins)==8,'complete donor D cut')
        above=np.stack([port_form(rtl[allids[k]][3],d,allids[k],j,data) for k in ins]);patch=np.zeros((len(outs),8),dtype=np.uint8)
        for y,v in enumerate(outs):
            for x,u in enumerate(ins):
                if v<m:
                    if u<m:patch[y,x]=inv[v^(32+u)]
                elif u>=m:patch[y,x]=inv[(v-m)^(32+u-m)]
                else:
                    for l,wgt in enumerate(weights):
                        patch[y,x]^=M[inv[(v-m)^(32+n+l)],M[wgt,inv[(m+l)^(32+u)]]]
        response=times_matrix(patch,above)
        for p,val in zip(outs,response):after[allids[p]]=val
    return after


def terminal(i,mode,state,data):
    z,rtl,p_h,p_d,Hd,Nd,half,nodes,dwords,ks=data;fields={};zeros=np.zeros(480,dtype=np.uint8)
    for k in nodes[i]:
        chart=ks[mode][str(k)];
        for phase,inp,out in chart['stripes']:
            n=len(inp);sel=[t for t in range(n) if inp[t] in state]
            if not sel:
                for p in out:fields[p]=zeros.copy()
                continue
            active=np.stack([state[inp[t]] for t in sel]);v=powers[np.array(sel)+1,:n].T
            for p,val in zip(out,times_matrix(v,active)):fields[p]=val
        for s,d in chart['early_cache_to_late']:fields[d]^=fields[s]
    e=[f for f in sorted(fields) if rtl[f][0]=='X' and rtl[f][7]==i]
    y=[f for f in sorted(fields) if rtl[f][0]=='Y' and rtl[f][1]==i]
    return np.stack([fields[w] for w in e]),np.stack([fields[w] for w in y])


def main():
    ap=argparse.ArgumentParser()
    for x in ('repo','d-words','k-words','out'):ap.add_argument('--'+x,type=Path,required=True)
    ap.add_argument('--compare-arrays',type=Path);ap.add_argument('--arrays-out',type=Path)
    a=ap.parse_args();data=prepared(a);counts=Counter()
    if a.arrays_out:a.arrays_out.mkdir(parents=True,exist_ok=True)
    for j in COL:
        state=donor(j,data)
        for i in ROW:
            for kind in ('spread','mixed'):
                e,y=terminal(i,kind,state,data)
                if a.compare_arrays:
                    other=np.load(a.compare_arrays/f'{kind}-{i}-{j}.npz')
                    need(np.array_equal(e,other['E']) and np.array_equal(y,other['Y']),f'actual chart composition {kind} {i} {j}')
                if a.arrays_out:np.savez_compressed(a.arrays_out/f'{kind}-{i}-{j}.npz',E=e,Y=y)
                counts[kind]+=1
    res={'matched_whole_pre_F_blocks':dict(counts),'native_donors':COL,'native_recipients':ROW,'field_coefficients_compared':2*18*(360+480)*480}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'COMPOSITION.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(res)


if __name__=='__main__':main()
