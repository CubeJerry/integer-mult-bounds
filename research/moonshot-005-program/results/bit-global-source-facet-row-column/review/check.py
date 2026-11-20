#!/usr/bin/env python3
"""Audit simultaneous physical S028 left/right restrictions and complete proper blocks."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from late import mod,req
def runner(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');n=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price')
    ar=mod(a.arithmetic,'finite').Arithmetic(a.library,f,helper);prior=mod(a.previous,'s028_inputs');mm=ar.mm
    flat=json.loads(a.flat_config.read_bytes());target=json.loads(a.target_config.read_bytes());final=json.loads(a.config.read_bytes())
    original,body,copy=prior.coords();terms=prior.target_blocks(root);U=prior.rand(flat['U8_SHAKE_tag'],(480,8));P=prior.rand('globally shared native output rows 0',(8,480));t=target['dimensions'];z=final['output_dimensions']
    R=np.load(a.functional);fn={key:R[key] for key in R.files};adj=[sorted(n.adj[j]&set(range(111)))for j in range(111)]
    early=[np.load(a.cache/f'E{i}.npy',mmap_mode='r')for i in range(111)];old=[np.load(a.cache/f'B{i}.npy',mmap_mode='r')for i in range(111)]
    gauges=[np.load(a.gauges/f'F{i}.npz')for i in range(111)];V=[G['V']for G in gauges];S=[G['S']for G in gauges];total=Counter();hashes={};nontrivial=set();seen=set()
    rim=np.lib.format.open_memmap(a.rim_file,mode='w+',shape=(111*480,111*480),dtype=np.uint8) if a.rim_file else None
    if rim is not None:
        for j in range(111):rim[480*j:480*j+480,480*j:480*j+480]=np.eye(480,dtype=np.uint8)
    for j,cuts in enumerate(adj):
        settings=final['donors'][str(j)];L=np.load(a.late/f'L{j}.npy',mmap_mode='r');owners=np.load(a.late/f'IDs{j}.npy')
        req(sha256(L).hexdigest()==settings['late_transfer_sha256'] and sha256(owners).hexdigest()==settings['late_owner_ids_sha256'],'true independent late transfer and raw IDs')
        A=np.vstack([mm(P[:z[i]],l) for i,l in zip(cuts,L)]);pivot=ar.reduce(A);req(len(pivot)==len(A),'true local late-to-selected-rows map');iv=ar.reduce(A[:,pivot],True)[0]
        rhs={(0,g):[]for g in range(1,8)};rhs.update({(g,0):[]for g in range(1,8)});rhs[0,0]=[];rhs[1,1]=[];words=[]
        u=U[:,:t[j]];pu=ar.reduce(u.T);ui=ar.reduce(u[pu],True)[0]
        for i,l in zip(cuts,L):
            q=adj[i].index(j);E=early[i][q];B=mm(V[i],old[i][q]^mm(S[i],E));Pi=P[:z[i]];phase={}
            if f'A-{i}' in fn:
                Aorig=fn[f'A-{i}'];ys=fn[f'ids-{i}']
                for e in range(8):
                    name=f'Q-{i}-{e}'
                    if name not in fn:continue
                    alpha=mm(fn[name],E)
                    for g in set(copy[ys]):
                        select=copy[ys]==g;C=np.zeros((480,Aorig.shape[1]),dtype=np.uint8);C[body[ys[select]]]=Aorig[select];phase[int(g),e]=(C,alpha)
            words.append((i,l,B,phase))
            for (g,e),blocks in rhs.items():
                val=np.zeros((z[i],480),dtype=np.uint8)
                if (i,j) in terms:
                    ob,ib,W=terms[i,j];ys=np.arange(64*ob,64*(ob+1));xs=np.arange(64*ib,64*(ib+1));yi=copy[ys]==g;xi=copy[xs]==e
                    if yi.any() and xi.any():val[:,body[xs[xi]]]=mm(Pi[:,body[ys[yi]]],W[np.ix_(yi,xi)])
                    if val.any():nontrivial.add((i,j))
                if g==e:val^=Pi^mm(Pi,B)
                if (g,e) in phase:
                    X,Y=phase[g,e];val^=mm(mm(Pi,X),Y)
                blocks.append(val)
        taps={};cost=0
        for label,blocks in rhs.items():
            Z=np.vstack(blocks);req(not mm(Z,u).any(),'source change preserves every old specified direction')
            if label not in ((0,0),(1,1)):
                rows=np.flatnonzero(Z.any(axis=1))
                if len(rows):
                    H=np.zeros((A.shape[1],len(rows)),dtype=np.uint8);H[pivot]=iv[:,rows];G=Z[rows];T=mm(H,G)
                    req(np.array_equal(mm(A,T),Z) and not mm(T,u).any(),'true sparse inter-copy tap');taps[label]=(H,G);cost+=int(ar.weights[T].sum())
                continue
            tag='central' if label==(0,0) else 'rim'
            T=prior.rand(f"dual native variable row/{tag}/{j}/{settings[tag]}",(A.shape[1],480)).copy()
            T[:,pu]^=mm(mm(T,u),ui);T[pivot]^=mm(iv,Z^mm(A,T))
            req(np.array_equal(mm(A,T),Z) and not mm(T,u).any(),'true native late injection on both panels')
            taps[label]=T;cost+=(1 if tag=='central' else 7)*int(ar.weights[T].sum())
        for i,l,B,phase in words:
            m=B^mm(l,taps[1,1]);rr=ar.reduce(m);req(len(rr)==480,'invertible true complete rim proper block')
            if rim is not None:rim[480*i:480*i+480,480*j:480*j+480]=m
            Z=B^mm(l,taps[0,0])
            if (0,0) in phase:
                C,D=phase[0,0];Z^=mm(C,D)
            Mi=None
            def crossing(g,e):
                blocks=[]
                if (g,e) in phase:blocks.append(phase[g,e])
                if (g,e) in taps:
                    H,Y=taps[g,e];blocks.append((mm(l,H),Y))
                if not blocks:return None
                return np.hstack([C for C,D in blocks]),np.vstack([D for C,D in blocks])
            for e in range(1,8):
                x=crossing(0,e);y=crossing(e,0)
                if x is None or y is None:continue
                if Mi is None:Mi=ar.reduce(m,True)[0]
                C,D=x;G,H=y;Z^=mm(mm(C,mm(D,mm(Mi,G))),H)
            req(len(ar.reduce(Z))==480,'genuine center Schur after seven full rims');seen.add((i,j))
        total['ADD']+=cost;hashes[j]=int(cost)
    req(len(seen)==6470 and len(nontrivial)==123,'all proper and altered source/receiver row equations')
    result={'independently_reconstructed_late_stars':111,'all_genuine_late_owner_ids':sum(len(np.load(a.late/f'IDs{i}.npy'))for i in range(111)),
        'all_native_proper_invertible_blocks':len(seen),'nonidentity_S028_edges_seen_from_outputs':len(nontrivial),
        'original_input_directions_across_pairs':8*sum(t[j] for i,j in seen),'original_output_functions_across_pairs':8*sum(z[i]for i,j in seen),
        'actual_extra_source_binary_ADD':int(total['ADD']),'donor_source_binary_ADD':hashes,'additional_INIT_CLEAR_MOVE':0,'new_complete_kappa':False}
    if rim is not None:
        rim.flush();result['rim_global_original_sha256']=sha256(rim).hexdigest()
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print({k:v for k,v in result.items() if k!='donor_source_binary_ADD'},flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for t in ('repo','arithmetic','previous','library','flat-config','target-config','config','cache','gauges','late','functional','out'):p.add_argument('--'+t,type=Path,required=True)
    p.add_argument('--rim-file',type=Path);runner(p.parse_args())
