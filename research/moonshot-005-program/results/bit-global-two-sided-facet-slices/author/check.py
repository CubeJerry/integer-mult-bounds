#!/usr/bin/env python3
"""Implement the published two-sided target on common actual original columns at all native edges."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np


def need(condition,message):
    if not condition:
        raise ValueError(message)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def source_target_coordinates():
    raw=np.stack([np.r_[np.arange(96*e,96*(e+1)),np.arange(768+384*e,768+384*(e+1))] for e in range(8)])
    need(sorted(raw.ravel())==list(range(3840)),'full real copy-to-original bijection')
    copy=np.empty(3840,dtype=int);body=np.empty(3840,dtype=int)
    for e,ids in enumerate(raw):copy[ids]=e;body[ids]=np.arange(480)
    return raw,copy,body


def assignment(path):
    raw=path.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601','published original target assignment pin')
    p=json.loads(raw);terms={}
    for i,j,ell in p['row_transfers']:terms[i,j]=(0,ell,np.eye(64,dtype=np.uint8))
    for i,j,ell in p['column_transfers']:terms[i,j]=(ell,0,np.eye(64,dtype=np.uint8))
    for (i,j),bitrows in zip(p['internal_edges'],p['internal_matrices_64']):
        terms[i,j]=(0,0,np.array([[(v>>c)&1 for c in range(64)] for v in bitrows],dtype=np.uint8))
    need(len(terms)==123,'two native perturbation stars on the actual 111 roles')
    return terms


def null_basis(field,M):
    piv=field.pivots(M);rows=field.pivots(M.T);free=[s for s in range(M.shape[1]) if s not in piv]
    N=np.zeros((M.shape[1],len(free)),dtype=np.uint8);N[free]=np.eye(len(free),dtype=np.uint8)
    left,_=field.invert_and_price(M[np.ix_(rows,piv)]);N[piv]=field.mm(left,M[np.ix_(rows,free)])
    need(not np.any(field.mm(M,N)),'exact contact-nullspace basis')
    return N


def previous_facet(field,prev,params,i,js,B,E,U):
    exp=params['expected'][str(i)];a=np.array(params['weights'],dtype=np.uint8);width=E.shape[1]
    need(prev.digest(E)==exp['E'] and prev.digest(B)==exp['B'],'pinned real owner arrays of preceding word')
    D,Y=prev.equations(field,js,a,i,params['tiers'],U,B,E);p=field.pivots(D.T);iv,_=field.invert_and_price(D[p]);
    S=prev.coefficients(f"shared facet/7/{i}/{params['trials'][str(i)]}",(480,width)).copy();S[:,p]^=field.mm(Y^field.mm(S,D),iv)
    G=np.bitwise_xor.reduce(field.product[B,a[js,None,None]],axis=0)^field.mm(S,np.bitwise_xor.reduce(field.product[E,a[js,None,None]],axis=0))
    inverse,_=field.invert_and_price(G);V=field.product[a[i],inverse]
    need(prev.digest(S)==exp['S'] and prev.digest(V)==exp['V'],'same fixed globally interpolating facet')
    return S,V


def one(i,js,field,prev,params,chosen,terms,US,U,labels,codes,cache):
    raw,copy,body=labels;degree=chosen['dimensions'];active=[j for j in js if (i,j) in terms]
    if not active:
        return {'active':False},None
    dest={terms[i,j][0] for j in active};need(len(dest)==1,'one actual 64-field output bank at this facet')
    ell=next(iter(dest));output_ids=np.arange(64*ell,64*(ell+1));n=len(js)
    cuts={};nonzero_edges=set()
    for e in range(8):
        target=[]
        for j in js:
            m=degree[j];part=np.zeros((64,m),dtype=np.uint8)
            if (i,j) in terms:
                _,bank,A=terms[i,j];part=field.mm(A,US[e,64*bank:64*(bank+1),:m])
                if np.any(part):nonzero_edges.add(j)
            target.append(part)
        cuts[e]=np.hstack(target)
    need(nonzero_edges==set(active),'every one of the actual target perturbations is nonzero on the selected inputs')
    T=np.hstack(list(cuts.values()));A=T[:,field.pivots(T)];rows=field.pivots(A.T);rank=A.shape[1]
    Ainv,_=field.invert_and_price(A[rows]);epochs=chosen['choices'][str(i)]
    E=np.load(cache/f'E{i}.npy',mmap_mode='r',allow_pickle=False);B=np.load(cache/f'B{i}.npy',mmap_mode='r',allow_pickle=False)
    S,V=previous_facet(field,prev,params,i,js,B,E,U);Vinv,_=field.invert_and_price(V);eheight=E.shape[1]
    reduced=field.mm(E.reshape(-1,480),U).reshape(n,eheight,8)
    freeviews=np.hstack([M[:,:degree[j]] for j,M in zip(js,reduced)])
    pp=field.pivots(freeviews.T);need(len(pp)==freeviews.shape[1],'all designated true early source observations independent')
    right,_=field.invert_and_price(freeviews[pp]);invoices=0;modified_diagonals=0;functional={};identity=np.eye(rank,dtype=np.uint8)
    for e,target in cuts.items():
        if not np.any(target):continue
        values=field.mm(Ainv,target[rows]);need(np.array_equal(field.mm(A,values),target),'true sparse target rows')
        attempt=epochs[str(e)]
        L=prev.coefficients(f'exact two-sided/{i}/{e}/{attempt}',(rank,eheight)).copy() if attempt else np.zeros((rank,eheight),dtype=np.uint8)
        L[:,pp]^=field.mm(values^field.mm(L,freeviews),right)
        need(np.array_equal(field.mm(A,field.mm(L,freeviews)),target),'every output field in this target bank agrees')
        functional[e]=L;invoices+=int(field.weights[field.mm(A,L)].sum())
        # Same-copy diagonal. The other raw coordinates of the correction are explicit cross-copy additions.
        where=np.flatnonzero(copy[output_ids]==e);part=np.zeros((480,rank),dtype=np.uint8);part[body[output_ids[where]]]=A[where]
        if np.any(part):
            for j,BE,EM in zip(js,B,E):
                old=field.mm(V,BE^field.mm(S,EM));inverse,_=field.invert_and_price(old)
                need(field.rank(identity^field.mm(L,field.mm(EM,field.mm(inverse,part))))==rank,'low-rank determinant on original complete block')
                new=old^field.mm(part,field.mm(L,EM));need(field.rank(new)==480,'direct complete same-copy determinant')
                m=degree[j];alpha=field.mm(L,field.mm(EM,U[:,:m]));expected=U[:,:m]^field.mm(part,alpha)
                need(np.array_equal(field.mm(new,U[:,:m]),expected),'actual complete diagonal output on all prescribed columns')
                modified_diagonals+=1
    need((i==80 and all(copy[output_ids]==0)) or (i!=80 and set(functional)=={0}),'whole-word triangularity at this receiver')
    # The old exhibited return kernel is represented by the contact subcodes plus a synchronized bank in each copy.
    a=np.array(params['weights'],dtype=np.uint8);Eavg=np.bitwise_xor.reduce(field.product[E,a[js,None,None]],axis=0)
    image=[]
    for e in range(8):
        L=functional.get(e)
        if L is None:
            image.append(np.zeros((rank,480+sum(N.shape[1] for _,N in codes)),dtype=np.uint8));continue
        block=[]
        for r,(Jr,N) in enumerate(codes):
            rec=np.zeros((rank,len(Jr)),dtype=np.uint8);relevant={j:t for t,j in enumerate(Jr)}
            for q,j in enumerate(js):
                if j in relevant:rec[:,relevant[j]]=field.mm(L,reduced[q,:,r:r+1])[:,0]
            block.append(field.mm(rec,N))
        block.append(field.mm(L,Eavg));image.append(np.hstack(block))
    return {'active':True,'nontrivial_target_edges':len(active),'target_output_bank':ell,'output_rank':rank,
            'changed_diagonals_directly_checked':modified_diagonals,'source_copies_with_actual_additions':sorted(functional),
            'extra_binary_ADD':invoices,'source_directions_on_all_foreign_inputs':sum(degree[j] for j in js)},np.hstack(image)

def main():
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    cli.add_argument('--cache-dir',type=Path);cli.add_argument('--previous-author',type=Path,help='Override the installed global fixture during local staging')
    args=cli.parse_args();here=Path(__file__).resolve().parent;results=args.repo/'research/moonshot-005-program/results'
    old=args.previous_author or results/'bit-global-facet-shared-coordinates/author';up=results/'bit-spread-rs-physical-word/author'
    sys.path.insert(0,str(old.resolve()));prev=module(old/'check.py','shared_native');sys.path.insert(0,str(up.resolve()));import transfer
    raw=(here/'output/PARAMETERS.json').read_bytes();need(hashlib.sha256(raw).hexdigest()=='bb8a93528338ed728d339d09d28c195b99195f02b00db4b53aea418e0d799060','literal two-sided parameter receipt')
    chosen=json.loads(raw);params=json.loads((old/'output/PARAMETERS.json').read_text());old_result=json.loads((old/'output/RESULT.json').read_text())
    need(all(m<=n for m,n in zip(chosen['dimensions'],params['tiers'])),'preceding flat constraints contain each new direction')
    terms=assignment(results/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json')
    with tempfile.TemporaryDirectory(prefix='two-sided-facet-') as tempdir:
        temp=Path(tempdir);lib=temp/'field.so'
        subprocess.run(['cc','-O3','-march=native','-shared','-fPIC',str(old/'field.c'),str(up/'gf64_matmul.c'),'-o',str(lib)],check=True)
        field=prev.Field(lib,transfer);native=transfer.Atlas(args.repo,results/'bit-gf64-actual-k-atlas/author/output',results/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz',lib)
        cache=args.cache_dir or temp/'physical'
        if not all((cache/f'{p}{i}.npy').is_file() for i in range(111) for p in ('E','B')):prev.prepare(native,cache)
        adj={i:sorted(native.orth[i]&set(range(111))) for i in range(111)};J=np.eye(111,dtype=np.uint8)
        for i,js in adj.items():J[i,js]=1
        U=prev.coefficients(params['U8_SHAKE_tag'],(480,8));raw,copy,body=source_target_coordinates()
        US=np.zeros((8,3840,8),dtype=np.uint8)
        for e,idx in enumerate(raw):US[e,idx]=U
        codes=[]
        for t in range(max(params['tiers'])):
            Jr=[j for j,m in enumerate(params['tiers']) if m>t];codes.append((Jr,null_basis(field,J[:,Jr])))
        outputs=[];per={}
        for i in range(111):
            per[i],K=one(i,adj[i],field,prev,params,chosen,terms,US,U,(raw,copy,body),codes,cache)
            if K is not None:outputs.append(K)
        full_upper=sum(d.get('output_rank',0) for d in per.values());restricted_rank=field.rank(np.vstack(outputs))
        need(restricted_rank==full_upper,'the old exhibited kernel surjects onto the entire correction image')
        active=sum(d.get('nontrivial_target_edges',0) for d in per.values());need(active==123,'all altered foreign target edges seen')
        cost=sum(d.get('extra_binary_ADD',0) for d in per.values());cases=sum(map(len,adj.values()));need(cases==6470,'all actual foreign pairs')
        extra=sum(sum(chosen['dimensions'][j] for j in js) for js in adj.values())*8
        result={'status':'PASS_TWO_SIDED_TARGET_ON_PHYSICAL_ORIGINAL_COLUMNS_AT_EVERY_FOREIGN_EDGE',
                'original_target':'published adapted 60 by 64 order on genuine raw field ordinals',
                'native_foreign_pairs':cases,'nonidentity_target_edges_exercised':active,'canonical_edges':cases-active,
                'physical_original_column_counts_by_number_of_donors':{8*m:n for m,n in Counter(chosen['dimensions']).items()},
                'original_directions_specified_summed_over_pairs':extra,'actual_active_facets':len(outputs),
                'whole_proper_change_rank_upper':full_upper,'change_rank_on_predecessor_exhibited_kernel':restricted_rank,
                'surviving_exhibited_kernel':old_result['proved_native_kernel']-restricted_rank,
                'proved_native_return_rank_upper':old_result['native_return_rank_upper']+restricted_rank,
                'proved_native_return_rank_lower':old_result['native_return_rank_lower'],'fitting_image_contains_prior_fitting_image':True,
                'additional_binary_ADD_over_predecessor':cost,'additional_MOVE':0,'additional_INIT':0,'additional_dirty_CLEAR':0,
                'additional_pure_Y_inverse_ADD':0,'complete_target':False,'new_complete_kappa':False,'facets':per}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS',cases,'native foreign pairs;',active,'nonidentity edges; return rank at most',result['proved_native_return_rank_upper'])

if __name__=='__main__':main()
