#!/usr/bin/env python3
"""Rank the exact target on selected source and facet subspaces and their paired intersection."""
from argparse import ArgumentParser
import json
from pathlib import Path
import numpy as np
from late import mod,req

def restricted(ar,adj,terms,physical,U,widths,transpose):
    data=[]
    for v in range(111):
        m=widths[v];Z=np.zeros((3840,8*m),dtype=np.uint8)
        for e,idx in enumerate(physical):Z[idx, m*e:m*e+m]=U[:,:m]
        data.append(Z)
    offsets=np.r_[0,np.cumsum([Z.shape[1]for Z in data])];largest=data[int(np.argmax(widths))]
    rows=[]
    for i in range(111):
        modified={}
        for j in adj[i]:
            key=(j,i) if transpose else (i,j)
            if key not in terms:continue
            y,x,T=terms[key]
            if transpose:y,x,T=x,y,T.T
            v=np.zeros_like(data[j]);v[64*y:64*(y+1)]=ar.mm(T,data[j][64*x:64*(x+1)]);modified[j]=v
        # Select actual output coordinates that separate the full local response of our restricted inputs.
        take=ar.reduce(np.hstack([largest,*modified.values()]).T)
        Z=np.zeros((len(take),offsets[-1]),dtype=np.uint8)
        for j in [i]+adj[i]:
            s=slice(offsets[j],offsets[j+1]);Z[:,s]=data[j][take]
            if j in modified:Z[:,s]^=modified[j][take]
        rows.append(Z)
    M=np.vstack(rows);return int(offsets[-1]),len(ar.reduce(M)),data,offsets

def main(a):
    b=a.repo/'research/moonshot-005-program/results';f=mod(b/'bit-spread-h263-source/review/check.py','gf');n=mod(b/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);h=mod(b/'bit-spread-source-owner-compiler/author/compile_source.py','price');pr=mod(a.previous,'target')
    ar=mod(a.arithmetic,'ranks').Arithmetic(a.library,f,h);phys,_,_=pr.coords();terms=pr.target_blocks(b);adj=[sorted(n.adj[j]&set(range(111)))for j in range(111)]
    in_width=json.loads(a.input_config.read_bytes())['dimensions'];out_width=json.loads(a.output_config.read_bytes())['output_dimensions'];U=pr.rand('globally shared native original-column frame 0',(480,8));P=pr.rand('globally shared native output rows 0',(8,480)).T
    cin,ri,X,io=restricted(ar,adj,terms,phys,U,in_width,False);cout,ro,Y,oo=restricted(ar,adj,terms,phys,P,out_width,True)
    parts=[]
    base=ar.mm(P.T,U)
    for i in range(111):
        Q=np.zeros((8*out_width[i],cin),dtype=np.uint8)
        for j in [i]+adj[i]:
            m,n0=out_width[i],in_width[j]
            B=np.kron(np.eye(8,dtype=np.uint8),base[:m,:n0])
            if (i,j) in terms:
                y,x,T=terms[i,j];B^=ar.mm(Y[i][64*y:64*(y+1)].T,ar.mm(T,X[j][64*x:64*(x+1)]))
            Q[:,io[j]:io[j+1]]=B
        parts.append(Q)
    rp=len(ar.reduce(np.vstack(parts)));lo=ri+ro-rp;hi=426240-max(cin-ri,cout-ro)
    res={'selected_original_global_dimension':cin,'rank_on_selected_inputs':ri,'forced_right_kernel':cin-ri,'selected_global_output_functionals':cout,
         'rank_of_selected_output_functionals':ro,'forced_left_kernel':cout-ro,'fully_constrained_paired_panel_rank':rp,'abstract_completion_minimum_rank':lo,'forced_fitting_upper':hi}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'TARGET-PANELS.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(res,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','previous','arithmetic','library','input-config','output-config','out'):p.add_argument('--'+k,type=Path,required=True)
    main(p.parse_args())
