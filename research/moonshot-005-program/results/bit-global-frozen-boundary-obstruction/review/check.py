#!/usr/bin/env python3
"""Use the actual restricted S028 transfer on all 6,470 frozen-boundary quotient spaces."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util,json,sys
from pathlib import Path
import numpy as np
def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def req(x,m):
    if not x:raise ValueError(m)
def main(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');n=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price')
    ar=mod(a.arithmetic,'field').Arithmetic(a.library,f,helper);pr=mod(a.previous,'previous');mm=ar.mm;_,body,lane=pr.coords();terms=pr.target_blocks(root);sys.path.insert(0,str(a.rank_code.resolve().parent));rank=mod(a.rank_code,'blocked').runner(a.rank_library,f)
    adj=[sorted(n.adj[i]&set(range(111))) for i in range(111)];late=[np.load(a.late/f'L{j}.npy',mmap_mode='r')for j in range(111)];fold=json.loads(a.flat_config.read_bytes())['expected'];pars=json.loads(a.output_config.read_bytes())['donors']
    for j,L in enumerate(late):req(sha256(L).hexdigest()==pars[str(j)]['late_transfer_sha256'],'native late owner map')
    complete={};altered={};baseline={};hist=Counter();flat=Counter();affected=Counter();improved=Counter();ex={}
    for i,js in enumerate(adj):
        E,B=[np.load(a.cache/f'{k}{i}.npy',mmap_mode='r')for k in ('E','B')];V=np.load(a.gauges/f'F{i}.npz')['V']
        for key,item in [('E',E),('B',B),('V',V)]:req(sha256(item).hexdigest()==fold[str(i)][key],'all genuine fixed phase and facet matrices')
        for p,j in enumerate(js):
            change=(i,j) in terms
            if a.only_changed and not change:continue
            ee,bb=E[p],B[p];L=late[j][adj[j].index(i)];K=pr.null(ee,ar);rL=len(ar.reduce(L))
            restricted=mm(V,mm(bb,K))^K
            naked=len(ar.reduce(np.hstack([L,restricted])))-rL;baseline[i,j]=naked
            if change:
                Q=pr.null(L.T,ar).T;R=mm(Q,restricted);req(len(ar.reduce(R))==naked,'independent direct quotient and augmented image ranks')
                ob,ib,T=terms[i,j];oy=np.arange(64*ob,64*(ob+1));ix=np.arange(64*ib,64*(ib+1));m,k=R.shape
                left=np.zeros((8*m,64),dtype=np.uint8);right=np.zeros((64,8*k),dtype=np.uint8)
                for g in range(8):
                    o=lane[oy]==g;x=lane[ix]==g
                    if o.any():left[g*m:(g+1)*m,o]=Q[:,body[oy[o]]]
                    if x.any():right[x,g*k:(g+1)*k]=K[body[ix[x]]]
                D=np.kron(np.eye(8,dtype=np.uint8),R)^mm(left,mm(T,right));v=int(rank(D,48,1));req(abs(v-8*naked)<=len(ar.reduce(T)),'physical target-bank perturbation rank interlacing')
                altered[i,j]=v;affected[v]+=1;improved[v-8*naked]+=1
            else:v=8*naked;flat[naked]+=1
            complete[i,j]=v;hist[v]+=1
            if (i,j)==(0,5):ex={'native_early_kernel':K.shape[1],'native_late_image':rL,'one_copy_residual':naked,'complete_error_lower':v}
    req(len(altered)==123,'complete native S028 nonflat assignment')
    if not a.only_changed:req(len(complete)==6470,'every native proper pair exactly once')
    def digest(d):return sha256(np.asarray([d[k]for k in sorted(d)],dtype='<u2')).hexdigest()
    res={'native_edges':len(complete),'maximum_error_rank_lower':max(hist),'minimum_error_rank_lower':min(hist),'canonical_edges':sum(flat.values()),'canonical_native_histogram':flat,'canonical_single_copy_sha256':digest({k:v for k,v in baseline.items()if k not in terms}),'actual_nonflat_edges':len(altered),'nonflat_error_rank_histogram':affected,'nonflat_change_in_quotient_rank':improved,'actual_nonflat_digest':digest(altered),'all_native_target_digest':digest(complete),'example':ex,'target_error_rank_lower_at_each_pair':min(hist),'maximum_exact_agreement_dimension_per_pair':3840-min(hist),'native_linear_double_boundary_only':True,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);stem='NONFLAT' if a.only_changed else 'RESULT';(a.out/(stem+'.json')).write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(stem,len(complete),min(hist),max(hist),len(altered),flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','arithmetic','library','previous','rank-code','rank-library','flat-config','output-config','cache','gauges','late','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--only-changed',action='store_true');main(p.parse_args())
