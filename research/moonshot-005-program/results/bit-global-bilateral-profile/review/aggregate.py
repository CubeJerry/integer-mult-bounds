#!/usr/bin/env python3
"""Rebuild 111 native weighted eight-copy arrowheads from original late and early owner arrays."""
from argparse import ArgumentParser
from hashlib import sha256
import importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def req(v,m):
    if not v:raise ValueError(m)

def run(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');n=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price')
    ar=mod(a.arithmetic,'field').Arithmetic(a.library,f,helper);pr=mod(a.previous,'initial');mm=ar.mm;_,body,copy=pr.coords();terms=pr.target_blocks(root)
    flat,first,last=[json.loads(p.read_bytes()) for p in (a.flat_config,a.input_config,a.output_config)]
    profile=json.loads(a.profile.read_bytes()) if a.profile else {}
    P=pr.rand('globally shared native output rows 0',(8,480));U=pr.rand(flat['U8_SHAKE_tag'],(480,8));w=np.array(flat['weights'],dtype=np.uint8);t=first['dimensions'];z=last['output_dimensions'];adj=[sorted(n.adj[i]&set(range(111))) for i in range(111)]
    D=np.load(a.functional);fn={key:D[key] for key in D.files};E=[np.load(a.cache/f'E{i}.npy',mmap_mode='r')for i in range(111)];B=[np.load(a.cache/f'B{i}.npy',mmap_mode='r')for i in range(111)]
    gauges=[np.load(a.gauges/f'F{i}.npz')for i in range(111)];PV=[mm(P[:z[i]],G['V']) for i,G in enumerate(gauges)];PVS=[mm(X,G['S']) for X,G in zip(PV,gauges)]
    labels=[(1,1),(0,0)]+[(0,e) for e in range(1,8)]+[(g,0) for g in range(1,8)];owner={l:q for q,l in enumerate(labels)}
    early={};totals=[];a.aggregate.mkdir(exist_ok=True,parents=True)
    if a.taps:a.taps.mkdir(parents=True,exist_ok=True)
    for i,js in enumerate(adj):
        total=None if a.taps_only else np.lib.format.open_memmap(a.aggregate/f'W{i:03}.npy',mode='w+',dtype=np.uint8,shape=(16,480,480));totals.append(total)
        if total is not None:
            for p in (0,1):total[p]=f.MUL[w[i],np.eye(480,dtype=np.uint8)]
        early[i]={}
        if f'A-{i}' not in fn:continue
        amp=fn[f'A-{i}'];ys=fn[f'ids-{i}'];weighted=np.bitwise_xor.reduce(f.MUL[w[js,None,None],E[i]],axis=0)
        for e in range(8):
            key=f'Q-{i}-{e}'
            if key not in fn:continue
            Q=fn[key]
            for g in set(copy[ys]):
                ii=copy[ys]==g;ix=body[ys[ii]];C=amp[ii];pair=(int(g),e);pp=mm(P[:z[i],ix],C);early[i][pair]=mm(pp,Q)
                if total is not None:total[owner[pair],ix]^=mm(C,mm(Q,weighted))
    for j,js in enumerate(adj):
        l=np.load(a.late/f'L{j}.npy',mmap_mode='r');specific=last['donors'][str(j)];aorig=np.load(a.late/f'IDs{j}.npy');req(sha256(l).hexdigest()==specific['late_transfer_sha256'] and sha256(aorig).hexdigest()==specific['late_owner_ids_sha256'],'original late visits')
        A=np.vstack([mm(P[:z[i]],ll)for i,ll in zip(js,l)]);pc=ar.reduce(A);req(len(pc)==len(A),'full actual selected late probes');inv=ar.reduce(A[:,pc],True)[0]
        saved={};rhs={p:[]for p in labels};u=U[:,:t[j]];ur=ar.reduce(u.T);ui=ar.reduce(u[ur],True)[0]
        for i in js:
            q=adj[i].index(j);ee=E[i][q];pB=mm(PV[i],B[i][q])^mm(PVS[i],ee);Pi=P[:z[i]]
            for g,e in labels:
                v=np.zeros((len(Pi),480),dtype=np.uint8)
                if (i,j) in terms:
                    out,src,T=terms[i,j];iy=np.arange(64*out,64*out+64);ix=np.arange(64*src,64*src+64);cc=copy[iy]==g;dd=copy[ix]==e
                    if cc.any() and dd.any():v[:,body[ix[dd]]]=mm(Pi[:,body[iy[cc]]],T[np.ix_(cc,dd)])
                if g==e:v^=Pi^pB
                if (g,e) in early[i]:v^=mm(early[i][g,e],ee)
                rhs[g,e].append(v)
        for pair,fragments in rhs.items():
            b=np.vstack(fragments);req(not mm(b,u).any(),'old selected genuine inputs invariant')
            d=owner[pair]
            if pair in ((0,0),(1,1)):
                tag='central' if pair==(0,0) else 'rim';T=pr.rand(f"dual native variable row/{tag}/{j}/{specific[tag]}",(A.shape[1],480)).copy()
                T[:,ur]^=mm(mm(T,u),ui);T[pc]^=mm(inv,b^mm(A,T));req(np.array_equal(mm(A,T),b),'native diagonal source orientation')
                saved[tag]=T
                if not a.taps_only:
                    for i,ll in zip(js,l):totals[i][d]^=f.MUL[w[j],mm(ll,T)]
            else:
                used=np.flatnonzero(b.any(axis=1))
                if not len(used):continue
                H=np.zeros((A.shape[1],len(used)),dtype=np.uint8);H[pc]=inv[:,used];G=b[used]
                g,e=pair;saved[f'H-{g}-{e}']=H;saved[f'G-{g}-{e}']=G
                if not a.taps_only:
                    for i,ll in zip(js,l):totals[i][d]^=f.MUL[w[j],mm(mm(ll,H),G)]
        if a.taps:np.savez(a.taps/f'T{j}.npz',**saved)
    if a.taps_only:return
    pins={}
    for i,M in enumerate(totals):
        M.flush();pins[str(i)]=sha256(M).hexdigest()
    req(pins==profile['aggregate_sha256'],'genuine full arrowheads independently reconstructed')
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'AGGREGATES.json').write_text(json.dumps({'native_aggregates':len(pins),'native_arrows_per_receiver':16,'all_native_parameter_pins':pins},sort_keys=True,indent=2)+'\n');print('PASS',len(pins),'independent full-bank weighted arrowheads',flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','arithmetic','library','previous','flat-config','input-config','output-config','functional','cache','gauges','late','aggregate','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--profile',type=Path);p.add_argument('--taps',type=Path);p.add_argument('--taps-only',action='store_true');run(p.parse_args())
