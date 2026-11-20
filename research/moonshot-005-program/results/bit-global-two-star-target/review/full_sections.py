#!/usr/bin/env python3
"""Use the entire verified donor-10 column and facet-80 row in the native fitting."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from check import mod,req
def main(a):
    b=a.repo/'research/moonshot-005-program/results';f=mod(b/'bit-spread-h263-source/review/check.py','gf');n=mod(b/'bit-spread-overlap-source/review/check.py','geo').Native(a.repo,f);h=mod(b/'bit-spread-source-owner-compiler/author/compile_source.py','price');pr=mod(a.previous,'prior');ar=mod(a.arithmetic,'field').Arithmetic(a.library,f,h);mm=ar.mm;terms=pr.target_blocks(b);true,body,lane=pr.coords();adj=[set(n.adj[i])&set(range(111))for i in range(111)];width=json.loads(a.config.read_bytes())['output_dimensions'];res={}
    for dual in (False,True):
        target={(j,i):(s,d,T.T)for (i,j),(d,s,T)in terms.items()}if dual else terms;k=80 if dual else 10
        C=pr.rand('globally shared native output rows 0',(8,480)).T if dual else pr.rand('globally shared native original-column frame 0',(480,8));w=width if dual else [5]*111
        def cols(m):
            W=np.zeros((3840,7*m),dtype=np.uint8)
            for e in range(1,8):W[true[e],(e-1)*m:e*m]=C[:,:m]
            return W
        V=[cols(m) for m in w];common=cols(max(w));js=[j for j in range(111) if j!=k];offs=np.r_[0,np.cumsum([V[j].shape[1]for j in js])];parts=[]
        # Role k gives a complete identity pivot. Its other coefficients are canonical on the seven chosen physical copies.
        req(not any((k,j) in target for j in js),'dual/source pivot row is entirely proper identity or zero')
        for i in js:
            add={}
            for j in adj[i]:
                if j==k or (i,j) not in target:continue
                d,s,t=target[i,j];m=np.zeros_like(V[j]);m[64*d:64*(d+1)]=mm(t,V[j][64*s:64*(s+1)]);add[j]=m
            if k in adj[i]:
                d,s,t=target[i,k];req(not mm(t,common[64*s:64*(s+1)]).any(),'all seven copies in entire eliminated pivot column avoid the actual nonflat source bank')
            rows=ar.reduce(np.hstack([common,*add.values()]).T);out=np.zeros((len(rows),offs[-1]),dtype=np.uint8)
            for idx,j in enumerate(js):
                y=np.zeros((len(rows),V[j].shape[1]),dtype=np.uint8)
                if (i==j or j in adj[i]) ^ (k in adj[i] and j in adj[k]):y^=V[j][rows]
                if j in add:y^=add[j][rows]
                out[:,offs[idx]:offs[idx+1]]=y
            parts.append(out)
        R=np.vstack(parts);r=len(ar.reduce(R));domain=int(3840+offs[-1]);res['entire_receiver_row' if dual else 'entire_donor_column']={'full_original_role':k,'total_restricted_original_dimensions':domain,'exact_target_fitting_rank':3840+r,'forced_kernel':domain-3840-r,'remaining_compact_rows':len(R),'eliminated_3840_pivot_schur_sha256':sha256(R).hexdigest()}
    res['native_fitting_upper']=426240-max(v['forced_kernel']for v in res.values());a.out.mkdir(parents=True,exist_ok=True);(a.out/'FULL-ROLE-TARGET-SECTIONS.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(res,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for x in ('repo','arithmetic','library','previous','config','out'):p.add_argument('--'+x,type=Path,required=True)
    main(p.parse_args())
