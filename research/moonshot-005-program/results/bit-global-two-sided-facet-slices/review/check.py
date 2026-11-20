#!/usr/bin/env python3
"""Independently check every true corrected S028 input direction and the rank transfer."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256,shake_256
import importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def req(v,msg):
    if not v:raise ValueError(msg)
def rand(tag,shape):return (np.frombuffer(shake_256(tag.encode()).digest(int(np.prod(shape))),dtype=np.uint8)&63).reshape(shape)
def coords():
    actual=np.full((8,480),-1,dtype=int)
    for k,off1,off8 in [(3,0,0),(12,96,768)]:
        for copy in range(8):
            for ch in range(2*k):
                for t in range(16):
                    actual[copy,off1+16*ch+t]=off8+32*k*copy+16*ch+t
    req(set(actual.flat)==set(range(3840)),'actual paid original-bank permutation')
    body=np.empty(3840,dtype=int);lane=np.empty(3840,dtype=int)
    for e,idx in enumerate(actual):lane[idx]=e;body[idx]=np.arange(480)
    return actual,body,lane
def null(A,ar):
    cols=ar.reduce(A);rows=ar.reduce(A.T);free=sorted(set(range(A.shape[1]))-set(cols))
    W=np.zeros((A.shape[1],len(free)),dtype=np.uint8);W[free]=np.eye(len(free),dtype=np.uint8)
    inv,_=ar.reduce(A[np.ix_(rows,cols)],True);W[cols]=ar.mm(inv,A[np.ix_(rows,free)]);req(not ar.mm(A,W).any(),'native kernel');return W
def target_blocks(base):
    raw=(base/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json').read_bytes();req(sha256(raw).hexdigest()=='deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601','actual S028 assignment')
    s=json.loads(raw);ds={}
    for i,j,h in s['row_transfers']:ds[i,j]=(0,h,np.eye(64,dtype=np.uint8))
    for i,j,h in s['column_transfers']:ds[i,j]=(h,0,np.eye(64,dtype=np.uint8))
    for pair,binary in zip(s['internal_edges'],s['internal_matrices_64']):
        ds[tuple(pair)]=(0,0,np.array([[(r>>t)&1 for t in range(64)] for r in binary],dtype=np.uint8))
    req(len(ds)==123,'all genuine nonidentity target edges');return ds
def main(a):
    root=a.repo/'research/moonshot-005-program/results';base=json.loads(a.previous_parameters.read_bytes());spec=a.parameters.read_bytes();req(sha256(spec).hexdigest()=='bb8a93528338ed728d339d09d28c195b99195f02b00db4b53aea418e0d799060','two-sided input')
    specs=json.loads(spec);degree=specs['dimensions'];f=mod(root/'bit-spread-h263-source/review/check.py','gf');geo=mod(root/'bit-spread-overlap-source/review/check.py','geo').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','source')
    ar=mod(a.field_code,'math').Arithmetic(a.library,f,helper);mm=ar.mm;U=rand(base['U8_SHAKE_tag'],(480,8));w=np.asarray(base['weights'],dtype=np.uint8)
    actual,body,copy=coords();ds=target_blocks(root);J=np.eye(111,dtype=np.uint8);adj={i:sorted(geo.adj[i]&set(range(111))) for i in range(111)}
    for i,js in adj.items():J[i,js]=1
    codes=[]
    for u in range(7):
        labels=[j for j,t in enumerate(base['tiers'])if t>u];codes.append((labels,null(J[:,labels],ar)))
    rect=[];total=Counter();allcols={};functionals={};native=0;bitsum=0;pair_ranks=Counter()
    for i,js in adj.items():
        native+=len(js);selected=[j for j in js if (i,j) in ds]
        if not selected:continue
        banks={ds[i,j][0] for j in selected};req(len(banks)==1,'single native bank of all perturbations')
        bank=banks.pop();ids=np.arange(64*bank,64*(bank+1));E,B=(np.load(a.cache/f'{u}{i}.npy',mmap_mode='r')for u in ('E','B'))
        req(sha256(E).hexdigest()==base['expected'][str(i)]['E'] and sha256(B).hexdigest()==base['expected'][str(i)]['B'],'previous physical arrays')
        G=np.load(a.gauges/f'F{i}.npz');S,V=G['S'],G['V']
        for key,val in [('S',S),('V',V)]:req(sha256(val.tobytes()).hexdigest()==base['expected'][str(i)][key],'verified old physical word')
        V_inv,_=ar.reduce(V,True)
        # Use the genuine block matrices on the copies. All identity vectors that follow are raw lane owners.
        Eb=mm(E.reshape(-1,480),U).reshape(len(js),E.shape[1],8)
        F=np.hstack([X[:,:degree[j]]for X,j in zip(Eb,js)]);rows=ar.reduce(F.T);req(len(rows)==F.shape[1],'actual complete early input interpolation')
        R,_=ar.reduce(F[rows],True);rhs=[];hit=set()
        for e in range(8):
            cur=[]
            for j in js:
                val=np.zeros((64,degree[j]),dtype=np.uint8)
                if (i,j) in ds:
                    _,src,N=ds[i,j];raw=np.arange(64*src,64*(src+1));nonzero=copy[raw]==e
                    if np.any(nonzero):val=mm(N[:,nonzero],U[body[raw[nonzero]],:degree[j]])
                    if val.any():hit.add(j)
                cur.append(val)
            rhs.append(np.hstack(cur))
        req(set(selected)==hit,'every actual altered target block acts nontrivially')
        T=np.hstack(rhs);A=T[:,ar.reduce(T)];rows2=ar.reduce(A.T);Ai,_=ar.reduce(A[rows2],True);rd=len(rows2)
        functionals[f"A-{i}"]=A;functionals[f"ids-{i}"]=ids
        local=np.zeros((8,480,rd),dtype=np.uint8)
        for e in range(8):
            eligible=copy[ids]==e
            if np.any(eligible):local[e,body[ids[eligible]]]=A[eligible]
        # Output range of P in the same gauge as diag(V^-1) times the old return matrix.
        canonical=np.stack([mm(V_inv,Y)for Y in local]);allcols[str(i)]=canonical
        cached=[];extra=0
        for e,Y in enumerate(rhs):
            if not Y.any():cached.append(None);continue
            K=mm(Ai,Y[rows2]);trial=specs['choices'][str(i)][str(e)]
            Q=rand(f'exact two-sided/{i}/{e}/{trial}',(rd,len(F))) if trial else np.zeros((rd,len(F)),dtype=np.uint8)
            Q[:,rows]^=mm(K^mm(Q,F),R)
            functionals[f"Q-{i}-{e}"]=Q
            update=mm(A,Q);req(np.array_equal(mm(update,F),Y),'all selected nonlinear-star actual raw outputs')
            bits=int(ar.weights[update].sum());bitsum+=bits;extra+=bits;cached.append(Q)
            if local[e].any():
                for j,BB,EE in zip(js,B,E):
                    old=mm(V,BB^mm(S,EE));new=old^mm(local[e],mm(Q,EE));req(len(ar.reduce(new))==480,'entire genuine updated copy-diagonal block')
                    req(np.array_equal(mm(old,U[:,:degree[j]]),U[:,:degree[j]]),'preceding exact original baseline from genuine inputs');pair_ranks[i]+=1
        req((i==80 and np.all(copy[ids]==0)) or (i!=80 and cached[0] is not None and all(q is None for q in cached[1:])),'physical triangularity on the complete eight-copy proper map')
        kernel=[];Eavg=np.bitwise_xor.reduce(f.MUL[np.asarray(E),w[js,None,None]],axis=0)
        for e,Q in enumerate(cached):
            if Q is None:kernel.append(np.zeros((rd,480+sum(W.shape[1]for _,W in codes)),dtype=np.uint8));continue
            imgs=[mm(Q,Eavg)]
            for t,(jj,N) in enumerate(codes):
                all_native=np.zeros((rd,len(jj)),dtype=np.uint8)
                for ix,j in enumerate(js):
                    if j in jj:all_native[:,jj.index(j)]=mm(Q,Eb[ix,:,t:t+1])[:,0]
                imgs.append(mm(all_native,N))
            kernel.append(np.hstack(imgs))
        rect.append(np.hstack(kernel));total.update({'altered_edges':len(selected),'output_bound':rd,'active_facets':1})
    Pkernel=np.vstack(rect);pk=len(ar.reduce(Pkernel));req(native==6470 and total['altered_edges']==123 and total['output_bound']==pk==369,'all native target columns and range saturation on the old exhibited kernel')
    a.out.mkdir(parents=True,exist_ok=True)
    if a.save_ranges:np.savez_compressed(a.save_ranges,**allcols)
    if a.save_functionals:np.savez_compressed(a.save_functionals,**functionals)
    facts={'all_6470_native_blocks_remain_invertible':True,'original_selected_directions_across_pairs':8*sum(degree[j]for js in adj.values() for j in js),'nonzero_native_target_edges':total['altered_edges'],'exact_genuine_early_update_ADD':bitsum,
           'complete_addition_rank':pk,'rank_on_old_exhibited_kernel':pk,'surviving_exhibited_kernel':8736-pk,'native_fitting_rank_lower':91216,'native_fitting_rank_upper':417504+pk,
           'all_active_rank_tests':sum(pair_ranks.values()),'actual_output_ranges_sha256':sha256(b''.join(v.tobytes()for v in allcols.values())).hexdigest(),'exact_addition_image_equals_that_of_the_old_kernel':True,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(facts,sort_keys=True,indent=2)+'\n');print(facts,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for key in ('repo','parameters','previous-parameters','cache','gauges','field-code','library','out'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--save-ranges',type=Path);p.add_argument('--save-functionals',type=Path);main(p.parse_args())
