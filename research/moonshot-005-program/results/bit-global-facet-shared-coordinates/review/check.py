#!/usr/bin/env python3
"""Independent original-word, facet-linear-system, global-kernel and binary price audit."""
from argparse import ArgumentParser
from collections import Counter
import json
from hashlib import sha256,shake_256
from pathlib import Path
import numpy as np
from rebuild import mod,req
from field import Arithmetic

def rnd(tag,shape):return np.frombuffer(shake_256(tag.encode()).digest(int(np.prod(shape))),dtype=np.uint8).reshape(shape)&63

def main(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','field');r=mod(root/'bit-spread-overlap-source/review/check.py','geometry');helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','source_geometry')
    ar=Arithmetic(a.library,f,helper);n=r.Native(a.repo,f);mm=ar.mm;raw=a.parameters.read_bytes();req(sha256(raw).hexdigest()=='19c0d7278a5439bd1ce948b3fe04932fa0d974fd95150dda109f348dabef924b','native tiered interpolation')
    params=json.loads(raw);bank=480;U=rnd(params['U8_SHAKE_tag'],(480,8));tiers=np.asarray(params['tiers']);wt=np.asarray(params['weights'],dtype=np.uint8)
    req(len(ar.reduce(U))==8 and np.all(wt),'seven independent published directions and full native support')
    I=np.eye(480,dtype=np.uint8);J=np.eye(111,dtype=np.uint8)
    for i in range(111):J[i,sorted(n.adj[i]&set(range(111)))]=1
    req(len(ar.reduce(J))==9 and not mm(J,wt[:,None]).any(),'true full-support contact relation')
    sums=Counter();arms={};minsize=a.minor_roles;minor=(np.lib.format.open_memmap(a.export_minor,mode='w+',shape=(minsize*480,minsize*480),dtype=np.uint8) if a.export_minor else np.zeros((minsize*480,minsize*480),dtype=np.uint8))
    for i in range(111):
        info=params['expected'][str(i)];js=sorted(n.adj[i]&set(range(111)));e=info['early_rows']
        E,B=(np.load(a.cache/f'{tag}{i}.npy',mmap_mode='r') for tag in ('E','B'))
        req(sha256(E).hexdigest()==info['E'] and sha256(B).hexdigest()==info['B'],'all authenticated actual preterminal E and proper B')
        Eproj=mm(E.reshape(-1,480),U).reshape(len(js),e,8);Bproj=mm(B.reshape(-1,480),U).reshape(len(js),480,8)
        def central(raw,dir):
            M=raw[:,:,dir].T;weight=f.MUL[f.INVERSE[wt[i]],wt[js]][:,None];return M^mm(M,weight)
        con=[];rhs=[]
        for t in range(7):
            which=[q for q,j in enumerate(js) if tiers[j]>t];Y=central(Bproj,t);X=central(Eproj,t)
            if len(which)==len(js):
                req(not mm(X,wt[js,None]).any() and not mm(Y,wt[js,None]).any(),'removed column is a genuine native dependency')
                which.pop()
            con.append(X[:,which]);rhs.append(Y[:,which])
        D=np.hstack(con);T=np.hstack(rhs);pivot=ar.reduce(D.T);q=len(pivot)
        req(q==D.shape[1]==info['constraint_rank'],'independent actual restricted equations')
        S=rnd(f"shared facet/{max(tiers)}/{i}/{params['trials'][str(i)]}",(480,e)).copy()
        R=ar.reduce(D[pivot],True)[0];S[:,pivot]^=mm(T^mm(S,D),R)
        req(sha256(S).hexdigest()==info['S'] and np.array_equal(mm(S,D),T),'literal native stationary shear')
        # Process each actual donor separately. The weighted full C uses all 480 original columns.
        A=[B[t]^mm(S,E[t]) for t in range(len(js))]
        C=np.bitwise_xor.reduce(f.MUL[np.stack(A),wt[js,None,None]],axis=0)
        Ci,_=ar.reduce(C,True);V=f.MUL[wt[i],Ci];Vi,code=ar.reduce(V,True)
        if a.emit_gauges:
            a.emit_gauges.mkdir(exist_ok=True,parents=True);np.savez(a.emit_gauges/f'F{i}.npz',S=S,V=V)
        req(sha256(V).hexdigest()==info['V'] and np.array_equal(mm(V,C),f.MUL[wt[i],I]),'all 480 true synchronized directions')
        if i<minsize:minor[480*i:480*i+480,480*i:480*i+480]=Vi
        for j,W in zip(js,A):
            req(len(ar.reduce(W))==480 and np.array_equal(mm(V,mm(W,U[:,:tiers[j]])),U[:,:tiers[j]]),'full foreign invertibility and pointwise original identity')
            if i<minsize and j<minsize:minor[480*i:480*i+480,480*j:480*j+480]=W
        sums.update({'pairs':len(js),'columns':sum(tiers[j] for j in js),'early_ADD':int(ar.weights[S].sum()),'invertible_ADD':code})
        arms[i]={'equations':q,'word':int(code),'relative_kernel_coordinates':int(sum(tiers[j] for j in js))}
    subcodes=[];masks=[]
    for d in range(7):
        jj=np.flatnonzero(tiers>d);rr=len(ar.reduce(J[:,jj]));subcodes.append(len(jj)-rr);masks.append(len(jj))
    # Since every weight is nonzero, the synchronized body meets the span exactly in the smallest donor subspace.
    nr=480+sum(subcodes)-min(tiers);bound=8*(111*480-nr)
    small=minor[:5760,:5760].copy();r12=len(ar.reduce(small));rr=r12 if minsize==12 else (r12 if a.export_minor else len(ar.reduce(minor)))
    if a.export_minor:minor.flush()
    req(nr==1092 and r12==5702,'guaranteed full kernel and native minor')
    res={'all_foreign_invertible':int(sums['pairs']),'native_exact_input_columns_over_edges':int(8*sums['columns']),'physical_copy_count':8,'independent_directions':7,
        'weights_contact_rank':9,'direction_roster_sizes':masks,'contact_kernel_dimensions':subcodes,'synchronized_and_coded_intersection_per_copy':int(min(tiers)),
        'guaranteed_global_kernel':int(8*nr),'native_return_rank_upper':int(bound),'first12_minor_rank_per_copy':r12,'proof_minor_roles':(12 if a.export_minor else minsize),'proof_minor_rank_per_copy':rr,
        'native_return_rank_lower':8*rr,'first12_minor_sha256':sha256(small).hexdigest(),'larger_minor_sha256':sha256(minor).hexdigest(),
        'forward_cross_ADD':int(8*sums['early_ADD']),'post_gauge_each_direction_ADD':int(8*sums['invertible_ADD']),
        'additional_forward_and_inverse_ADD':int(8*(sums['early_ADD']+2*sums['invertible_ADD'])),'additional_INIT_CLEAR_MOVE':0,
        'all_original_order':'component, physical copy, polynomial channel, degree','new_complete_kappa':False,'receivers':arms}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print('PASS full lower',8*rr,'upper',bound,'conditioned on paid native return')
if __name__=='__main__':
    p=ArgumentParser()
    for t in ('repo','parameters','cache','library','out'):p.add_argument('--'+t,type=Path,required=True)
    p.add_argument('--minor-roles',type=int,default=12);p.add_argument('--export-minor',type=Path);p.add_argument('--emit-gauges',type=Path);main(p.parse_args())
