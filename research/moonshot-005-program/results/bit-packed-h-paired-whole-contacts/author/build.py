#!/usr/bin/env python3
"""Regenerate the 16 disjoint two-source updates against actual preterminal coordinates."""
import argparse,hashlib,json,sys
from pathlib import Path
from functools import lru_cache
import numpy as np

def setup(x):
    r=x.repo/'research/moonshot-005-program/results';x.h_author=r/'bit-spread-rs-physical-word/author';mid=r/'bit-native-complete-middle-charts/author'
    x.k_words=r/'bit-gf64-actual-k-atlas/author/output';x.d_charts=r/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz'
    x.packed_endpoint=r/'bit-spread-packed-h-facet-fibres/author';x.packing_review=r/'bit-spread-overlap-source/review/check.py';x.field_review=r/'bit-spread-h263-source/review/check.py';x.parameters=r/'bit-spread-two-centre-packing/author/output/PARAMETERS.json';x.cache=None
    src=r/'bit-packed-h-all-facets/author';sys.path[:0]=[str(src),str(x.h_author),str(mid),str(r/'bit-spread-isolated-middle-cut/author')]
    from transfer import Atlas,TABLE,INV
    from physical import Physical
    from panels import obtain,module
    from fast import Arithmetic
    from slices import extend_rows,row_reduce
    from verify import price_map,shuffle
    co=module(r/'bit-spread-source-owner-compiler/author/compile_source.py','binary_ordinary');inv=Arithmetic(x.arith.resolve()).inverse;at=Atlas(x.repo,x.k_words,x.d_charts,x.library);at.left=lru_cache(111)(at.left);at.right=lru_cache(111)(at.right)
    assign={int(j):ii for j,ii in json.loads((src/'output/ASSIGNMENT.json').read_text()).items()};col={i:l for i,j,l in json.loads((r/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json').read_text())['column_transfers']}
    return Physical(x,at,inv,TABLE,INV,extend_rows,row_reduce,obtain(x,at,inv),price_map,shuffle,co,assign,col)

def patch(fm,rec,k):
    u,v=rec['donors'];keep=rec['extra'];w=32*k;mm=fm.mm;inv=fm.inv;ps=fm.piv
    def kernel(A):
        c=ps(A);r=ps(A[:,c].T);rest=sorted(set(range(A.shape[1]))-set(c));V=np.zeros((A.shape[1],len(rest)),np.uint8)
        V[rest]=np.eye(len(rest),dtype=np.uint8);V[c]=mm(inv(A[np.ix_(r,c)]),A[np.ix_(r,rest)]);assert not mm(A,V).any();return V
    xx=[];yy=[]
    for half,j in enumerate((u,v)):
        for i in fm.assignment[j]:
            if i in keep:continue
            P=fm.prepanel(i,k);A=fm.presource(i,j,k);F=fm.holder(i,k)[3];Y=mm(inv(mm(F,A)),fm.Z[i,k])
            q=fm.null(P^mm(A,Y));b=mm(Y,q);input=np.zeros((2*w,b.shape[1]),np.uint8);input[half*w:(half+1)*w]=b
            xx.append(input);yy.append(mm(fm.L[i,k],q))
    for i in keep:
        P=fm.prepanel(i,k);n=P.shape[1];M=kernel(np.hstack([P,fm.presource(i,u,k),fm.presource(i,v,k)]));xx.append(M[n:]);yy.append(mm(fm.L[i,k],M[:n]))
    A=np.hstack(xx);B=np.hstack(yy);cols=ps(A);basis=A[:,cols];rows=ps(basis.T);free=sorted(set(range(2*w))-set(rows));iv=inv(np.hstack([basis,np.eye(2*w,dtype=np.uint8)[:,free]]))
    W=mm(B[:,cols],iv[:len(cols)]);seed=rec['seeds'][str(k)]['source_seed'];rng=np.random.Generator(np.random.PCG64(202611+10000*u+20*v+k+seed))
    if free:W^=mm(rng.integers(0,64,(w,len(free)),dtype=np.uint8),iv[len(cols):])
    assert np.array_equal(mm(W,A),B)
    source={u:W[:,:w],v:W[:,w:]};result={f'G{j}-{k}':inv(m)for j,m in source.items()}
    for i in sorted(fm.assignment[u]+fm.assignment[v]):
        ds=(u,v)if i in keep else((u,)if i in fm.assignment[u]else(v,));P=fm.prepanel(i,k);L=fm.L[i,k];C=np.hstack([fm.presource(i,j,k)for j in ds]+[P]);Q=np.hstack([source[j]for j in ds]+[L])
        use=ps(C);roots=C[:,use];p=ps(roots.T);dim=len(C);fr=sorted(set(range(dim))-set(p));iv=inv(np.hstack([roots,np.eye(dim,dtype=np.uint8)[:,fr]]))
        F=mm(Q[:,use],iv[:len(use)]);trial=rec['seeds'][str(k)]['facet_trial'][str(i)]
        if fr:
            rng=np.random.Generator(np.random.PCG64(121+600000*i+400*k+trial));F^=mm(rng.integers(0,64,(w,len(fr)),dtype=np.uint8),iv[len(use):])
        assert np.array_equal(mm(F,C),Q);result[f'F{i}-{k}']=F
    return result
def verify(x):
    fm=setup(x);p=Path(__file__).parent/'output';records=json.loads((p/'PAIR-WORDS.json').read_text());receipt=json.loads((p/'PRICE.json').read_text());params={};used=set();date={}
    for rec in records:
        u,v=rec['donors'];assert not ({u,v}&used);used|={u,v}
        for k in (3,12):
            for key,data in patch(fm,rec,k).items():
                assert key not in params and hashlib.sha256(data.tobytes()).hexdigest()==rec['sha256'][key]
                params[key]=data
        print('reconstructed joint donor obligations',u,v,flush=True)
    assert len(records)==16 and len(used)==32 and sum(len(q['extra'])for q in records)==17
    for k in (3,12):
        seed=params[f'G2-{k}'];A=fm.presource(80,2,k);orig=fm.holder(80,k)[3];B=fm.mm(orig,A);fi=fm.mm(fm.mm(fm.required(80,2,k),fm.inv(fm.mm(B,seed))),orig)
        assert np.array_equal(fm.mm(fm.mm(fi,A),seed),fm.required(80,2,k));params[f'F80-{k}']=fi
    folder=x.out/'matrices';folder.mkdir(exist_ok=True,parents=True);ws={}
    for fil in x.baseline.glob('*.npy'):
        value=params.pop(fil.stem,None)
        if value is None:value=np.load(fil)
        np.save(folder/fil.name,value);ws[fil.stem]=value
    assert not params and len(ws)==288
    src={}
    for j,ii in fm.assignment.items():
        src[str(j)]=sum(fm.price(fm.comp,ws[f'G{j}-{k}'])+18*fm.perm(16*k)for k in (3,12))
    assert src==receipt['source_G_per_donor_one_direction']
    weights=np.array([sum(int(fm.tbl[c,1<<z]).bit_count()for z in range(6))for c in range(64)],dtype=np.int64);allcost=0;nchecked=0
    for i in range(111):
        total=pure=cross=snaps=0;perm=[-1]*3840
        for k in (3,12):
            M=ws[f'F{i}-{k}'];e,_,ids,_=fm.holder(i,k);ys=ids[len(e):];w=16*k
            assert fm.rank(M[:,len(e):])==2*w
            ds,body=fm.body_d(i,k);contact=fm.mm(M,body)
            for j in fm.at.orth[i]&set(range(111)):
                cols=[8*z+t for z,d in enumerate(ds)if j in fm.at.D[d]for t in range(8)];assert len(cols)==2*w and fm.rank(contact[:,cols])==2*w;nchecked+=1
            pure+=fm.price(fm.comp,M[:,len(e):]);cross+=8*int(weights[M[:,:len(e)]].sum());snaps+=48*len(e)
            off=0 if k==3 else 768
            for z,b in enumerate(ys):
                half,s=divmod(z,w);t=b-53280-480*i
                for g in range(8):perm[8*t+g]=off+16*s+8*half+g
        assert sorted(perm)==list(range(3840));seen=set();cycles=0
        for t in range(3840):
            if t in seen:continue
            j=t;cycles+=1
            while j not in seen:seen.add(j);j=perm[j]
        movement=18*(3840-cycles);local={'pure_Y_ADD':pure,'early_to_late_ADD':cross,'stationary_snapshot_ADD_INIT_dirty_CLEAR':snaps,'terminal_owner_permutation_ADD':movement,'Ground_inverse_ADD':pure+movement,'terminal_and_ground_total_ADD':2*(pure+movement)+cross+snaps}
        assert local==receipt['facet_price'][str(i)];allcost+=local['terminal_and_ground_total_ADD']
    assert nchecked==12940 and allcost==receipt['whole_terminal_fee']['terminal_and_ground_total_ADD']
    proof={'all_verified_whole_native_contacts':128,'complete_receiving_nodes':111,'retained_H_only_three_donor_fibres':3123,'protected_native_foreign_blocks':6470,'total_prescribed_original_field_directions':749520+128*3840,'native_prescribed_pairs':2844+128,'terminal_and_ground_total_ADD':allcost}
    (x.out/'RESULT.json').write_text(json.dumps(proof,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ('repo','baseline','library','arith','out'):p.add_argument('--'+key,type=Path,required=True)
 verify(p.parse_args())
