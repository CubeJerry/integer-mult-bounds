#!/usr/bin/env python3
"""Exact small-field controls for replacement-bank and LR theorems."""
import argparse, gzip, hashlib, itertools, json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np

def mul4(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return c
MUL=np.array([[mul4(a,b) for b in range(4)] for a in range(4)],dtype=np.uint8)
INV=np.array([0,1,3,2],dtype=np.uint8)
def rank(a):
    a=np.array(a,dtype=np.uint8,copy=True);r=0
    for c in range(a.shape[1]):
        ps=np.flatnonzero(a[r:,c])
        if not len(ps):continue
        p=r+int(ps[0]);a[[r,p]]=a[[p,r]];a[r]=MUL[INV[a[r,c]],a[r]]
        ix=np.flatnonzero(a[:,c]);ix=ix[ix!=r]
        a[ix]^=MUL[a[ix,c,None],a[r][None,:]];r+=1
        if r==len(a):break
    return r
def product(a,b):
    z=np.zeros((a.shape[0],b.shape[1]),dtype=np.uint8)
    for k in range(a.shape[1]):z^=MUL[a[:,k,None],b[k,None,:]]
    return z
def inverse(a):
    n=len(a);z=np.concatenate([a.copy(),np.eye(n,dtype=np.uint8)],axis=1)
    for c in range(n):
        p=next(i for i in range(c,n) if z[i,c]);z[[c,p]]=z[[p,c]];z[c]=MUL[INV[z[c,c]],z[c]]
        for i in range(n):
            if i!=c and z[i,c]:z[i]^=MUL[z[i,c],z[c]]
    return z[:,n:]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);base=a.repo/'research/moonshot-005-program'
    path=base/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';raw=gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    roots=json.loads(raw)['root_table'];O=np.array([[int(sum(x*y for x,y in zip(roots[i],roots[j]))==0) for j in range(111)] for i in range(111)],dtype=np.uint8)
    K=O^np.eye(111,dtype=np.uint8);assert rank(K)==9 and rank(O)==108
    aa,bb=0,1;assert O[aa,bb]
    controls=[]
    for alpha in (1,2,3):
        delta=np.zeros_like(O);delta[:,aa]^=MUL[alpha,O[:,aa]];delta[aa,bb]^=alpha
        B=O^delta;A=np.eye(111,dtype=np.uint8)^B
        assert np.all(A.diagonal()==1) and not np.any(B[O==0])
        qa=rank(A);r=rank(np.concatenate([K,delta]))-9
        assert qa==10 and r==2
        foreign_nonzero=int(np.count_nonzero(B[O!=0]));assert foreign_nonzero==6470 if alpha!=1 else foreign_nonzero<6470
        row_intersection=9+qa-rank(np.concatenate([K,A]));assert row_intersection==8
        rec={'alpha':alpha,'q':qa,'h':qa-9,'retained_quotient_rank':r,'canonical_row_intersection':row_intersection,'nonzero_foreign_entries':foreign_nonzero,'physical_network_realization_claimed':False}
        if alpha!=1:
            D=np.eye(111,dtype=np.uint8);D[aa,aa]^=alpha
            Bp=product(B,inverse(D));Ep=Bp^O
            assert rank(Ep)==1 and rank(np.concatenate([K,Ep]))-9==1
            rec['after_permitted_column_gauge_retained_rank']=1
        controls.append(rec)
    # Literal native seed reconstruction, using the same root order.
    frame=[0,16,17,32,36,38,67,71];assert not np.any(O[np.ix_(frame,frame)])
    edge_roles=[]
    for j in range(111):
        ends=tuple(i for i,f in enumerate(frame) if O[j,f])
        if len(ends)==2:edge_roles.append((j,ends))
    edges={e for _,e in edge_roles};assert len(edges)==27
    assert edges==set(itertools.combinations(range(8),2))-{(0,4)}
    # Recheck all star noncontacts between edge roles sharing an endpoint.
    for j,e in edge_roles:
        for k,f in edge_roles:
            if j!=k and set(e)&set(f):assert not O[j,k]
    low={0,4};a0,b0,c0=Q(9,22),Q(7,22),Q(4,11)
    gs={}
    for u,v in edges:
        gs[u,v,u]=a0 if u in low else b0 if v in low else c0
        gs[u,v,v]=a0 if v in low else b0 if u in low else c0
    G={i:sum(value for (*_,j),value in gs.items() if j==i) for i in range(8)}
    for u,v in edges:
        for j in (u,v):assert G[j]==1+2*(gs[u,v,u]+gs[u,v,v])
    assert sum(G.values())==Q(216,11)
    lam=[Q(54,11),Q(42,11),Q(120,11)]
    coeff=[(4,-2,0),(-2,0,5),(0,2,1)]
    assert [sum(lam[i]*coeff[i][j] for i in range(3)) for j in range(3)]==[12,12,30]
    assert sum(lam)==Q(216,11)
    # Complete all-input return protocol on a four-role binary toy.
    R=np.array([[1,0,1,0],[0,1,0,1]],dtype=np.uint8);L=np.array([[1,0],[0,1],[1,0],[0,1]],dtype=np.uint8)
    A=product(L,R);B=A^np.eye(4,dtype=np.uint8);Gm=np.array([[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1]],dtype=np.uint8);Gi=inverse(Gm)
    success=0;omit=0;no_inverse=0;images=set()
    for xx in range(16):
        x=np.array([[(xx>>i)&1] for i in range(4)],dtype=np.uint8);sx=product(R,x);images.add(tuple(product(A,x).ravel()))
        for yy in range(16):
            y=np.array([[(yy>>i)&1] for i in range(4)],dtype=np.uint8);target=y^x
            z=product(Gi,y^product(L,sx));out=product(Gm,z)^product(B,x);assert np.array_equal(out,target);success+=1
            badsx=sx.copy();badsx[0,0]=0
            outbad=product(Gm,product(Gi,y^product(L,badsx)))^product(B,x);omit+=not np.array_equal(outbad,target)
            outbad=product(Gm,y^product(L,sx))^product(B,x);no_inverse+=not np.array_equal(outbad,target)
    assert len(images)==4 and rank(A)==2 and omit and no_inverse
    M=111*5760*30;C0=9*5760*30;C=(9*5760+202)*30
    counts={'M':M,'C0':C0,'replacement_C_at_h202':C,'ADD_upper':18*M*M+53*M+111*C0+2*M*C,'INIT_and_dirty_CLEAR_each':5*M+C,'peak_public_plus_auxiliary':7*M+C,'gap8_MOVE':C}
    result={'status':'PASS_REPLACEMENT_BANK_AND_NATIVE_LR_GATES','native_two_column_controls':controls,'native_seed':{'point_roles':frame,'edge_roles':edge_roles,'missing_edge':[0,4]},'LR':{'dual_weights':list(map(str,lam)),'sharp_relaxation_g':[str(a0),str(b0),str(c0)],'bound':str(Q(216,11)),'integer_bound_at_h202':(216*202)//11,'common_kernel_floor_at_V5760_h202':5760-(216*202)//11},'return_protocol':{'all_input_pairs':success,'target_image_cardinality':len(images),'necessary_symbols':2,'omitted_symbol_failures':omit,'missing_inverse_failures':no_inverse},'conservative_binary_invoice_at_h202':counts,'scope':'Written bridge requires an actual proper B; the native near-minimum targets are algebraic controls, not claimed physical realizations.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    files=['results/bit-saturated-star-rigidity/author/PROOF.md','results/bit-saturated-star-rigidity/ADMISSION.md','results/bit-all111-balanced-causal-atlas/author/BALANCED-PROOF.md','results/bit-seventy-common-coordinates/author/PROOF.md']
    pins=[{'path':'research/moonshot-005-program/'+p,'sha256':hashlib.sha256((base/p).read_bytes()).hexdigest()} for p in files]
    (a.out/'SOURCE-PINS.json').write_text(json.dumps({'baseline':'d8544284cbd0527cd03a0aad576a2d2c6eddcc0e','layout_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'files':pins},indent=2)+'\n')
    print(result['status'])

if __name__=='__main__':main()
