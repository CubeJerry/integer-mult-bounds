#!/usr/bin/env python3
"""Verify a paid native F word, its 6,470 ranks and its shared return kernel."""
import argparse
from collections import Counter
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
from physical import prepare


def need(condition,message):
    if not condition:
        raise ValueError(message)


def digest(a):
    return hashlib.sha256(a).hexdigest()


def coefficients(tag,shape):
    size=int(np.prod(shape))
    return np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(size),dtype=np.uint8).reshape(shape)&63


class Field:
    def __init__(self,library,transfer):
        self.lib=ctypes.CDLL(str(library.resolve()))
        self.product=transfer.TABLE;self.inv=transfer.INV
        self.mm=transfer.Arithmetic(library).matmul
        ptr=ctypes.c_void_p;size=ctypes.c_size_t
        self.lib.ordered_rank.argtypes=[ptr,size,size,ptr,ptr,ptr,ptr]
        self.lib.ordered_rank.restype=size
        self.lib.invert_and_price.argtypes=[ptr,size,ptr,ptr,ptr]
        self.lib.invert_and_price.restype=ctypes.c_uint64
        self.weights=np.array([sum(int(self.product[q,1<<t]).bit_count() for t in range(6)) for q in range(64)])

    def pivots(self,A):
        A=np.array(A,dtype=np.uint8,copy=True,order='C');h,w=A.shape
        rows=np.empty(h,dtype=np.uint32);cols=np.empty(min(h,w),dtype=np.uint32)
        r=self.lib.ordered_rank(A.ctypes.data,h,w,self.product.ctypes.data,self.inv.ctypes.data,rows.ctypes.data,cols.ctypes.data)
        return cols[:r]

    def invert_and_price(self,A):
        n=len(A);need(A.shape==(n,n),'square coefficient matrix')
        work=np.hstack([A,np.eye(n,dtype=np.uint8)]);inverse=np.empty((n,n),dtype=np.uint8)
        price=int(self.lib.invert_and_price(work.ctypes.data,n,self.product.ctypes.data,self.inv.ctypes.data,inverse.ctypes.data))
        need(price!=2**64-1,'invertible finite pivot word')
        return inverse,price

    def rank(self,A):
        return len(self.pivots(A))


def equations(field,js,weights,i,tiers,origins,base,early):
    e=early.shape[1];p=origins.shape[1]
    E=field.mm(early.reshape(-1,480),origins).reshape(len(js),e,p).transpose(1,0,2)
    B=field.mm(base.reshape(-1,480),origins).reshape(len(js),480,p).transpose(1,0,2)
    src=[];dst=[];normalized=field.product[field.inv[weights[i]],weights[js]][:,None]
    for k in range(max(tiers)):
        inds=[t for t,j in enumerate(js) if tiers[j]>k]
        if not inds:
            continue
        Er=E[:,:,k];Br=B[:,:,k];Em=field.mm(Er,normalized);Bm=field.mm(Br,normalized)
        if len(inds)==len(js):
            inds=inds[:-1]
        src.append(Er[:,inds]^Em);dst.append(Br[:,inds]^Bm)
    return np.hstack(src),np.hstack(dst)


def apply_facet(field,i,js,params,cache,U,minor):
    expected=params['expected'][str(i)];tiers=params['tiers'];a=np.array(params['weights'],dtype=np.uint8)
    E=np.load(cache/f'E{i}.npy',mmap_mode='r',allow_pickle=False);B=np.load(cache/f'B{i}.npy',mmap_mode='r',allow_pickle=False)
    e=E.shape[1]
    need(E.shape==(len(js),e,480) and B.shape==(len(js),480,480) and e==expected['early_rows'],'real facet and donor sizes')
    need(digest(E)==expected['E'] and digest(B)==expected['B'],'actual full owner transfer matrix pins')
    D,Y=equations(field,js,a,i,tiers,U,B,E);piv=field.pivots(D.T);q=D.shape[1]
    need(len(piv)==q==expected['constraint_rank'],'all forced early equations independent')
    right,_=field.invert_and_price(D[piv]);trial=params['trials'][str(i)]
    S=coefficients(f'shared facet/{max(tiers)}/{i}/{trial}',(480,e)).copy()
    S[:,piv]^=field.mm(Y^field.mm(S,D),right)
    need(digest(S)==expected['S'] and np.array_equal(field.mm(S,D),Y),'constructed early coefficients')
    fullB=np.ascontiguousarray(B.transpose(1,0,2)).reshape(480,-1)
    fullE=np.ascontiguousarray(E.transpose(1,0,2)).reshape(e,-1)
    changed=(fullB^field.mm(S,fullE)).reshape(480,len(js),480).transpose(1,0,2)
    C=np.bitwise_xor.reduce(field.product[changed,a[js,None,None]],axis=0)
    Cinv,_=field.invert_and_price(C);V=field.product[a[i],Cinv];Vinv,word=field.invert_and_price(V)
    need(digest(V)==expected['V'] and np.array_equal(field.mm(V,C),field.product[a[i],np.eye(480,dtype=np.uint8)]),'actual synchronized profile')
    if i<len(minor)//480:
        minor[480*i:480*(i+1),480*i:480*(i+1)]=Vinv
    for j,new in zip(js,changed):
        m=tiers[j];A=U[:,:m]
        need(field.rank(new)==480,'actual invertible proper block before the invertible V')
        need(np.array_equal(field.mm(V,field.mm(new,A)),A),'identity on this donor\'s actual original columns')
        if max(i,j)<len(minor)//480:
            minor[480*i:480*(i+1),480*j:480*(j+1)]=new
    if i==0:
        j=js[0];A=U[:,:tiers[j]]
        need(not np.array_equal(field.mm(V,field.mm(B[0],A)),A),'negative control omitting the actual early contribution')
        damaged=S.copy();damaged[:,[0,1]]=damaged[:,[1,0]]
        need(not np.array_equal(field.mm(damaged,D),Y),'negative control swapping genuine early holders')
    cross=int(field.weights[S].sum())
    return {'native_foreign_pairs':len(js),'true_early_records':e,'constraint_rank':q,
            'source_columns_interpolated':sum(tiers[j] for j in js),'cross_ADD_per_copy':cross,'facet_diagonal_ADD_per_copy':word}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--cache-dir',type=Path,help='Reuse complete preterminal arrays from an earlier verified run')
    args=parser.parse_args();author=Path(__file__).resolve().parent
    base=args.repo/'research/moonshot-005-program/results';up=base/'bit-spread-rs-physical-word/author'
    sys.path.insert(0,str(up.resolve()));import transfer
    raw=(author/'output/PARAMETERS.json').read_bytes()
    need(digest(raw)=='19c0d7278a5439bd1ce948b3fe04932fa0d974fd95150dda109f348dabef924b','literal compact parameter receipt')
    params=json.loads(raw);tiers=params['tiers'];a=np.array(params['weights'],dtype=np.uint8)
    with tempfile.TemporaryDirectory(prefix='native-facet-') as directory:
        temp=Path(directory);library=temp/'field.so'
        subprocess.run(['cc','-O3','-march=native','-shared','-fPIC',str(author/'field.c'),str(up/'gf64_matmul.c'),'-o',str(library)],check=True)
        field=Field(library,transfer)
        native=transfer.Atlas(args.repo,base/'bit-gf64-actual-k-atlas/author/output',base/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz',library)
        cache=args.cache_dir or temp/'physical'
        if not all((cache/f'{prefix}{i}.npy').is_file() for i in range(111) for prefix in ('E','B')):
            prepare(native,cache)
        neighbours={i:sorted(native.orth[i]&set(range(111))) for i in range(111)}
        J=np.eye(111,dtype=np.uint8)
        for i,js in neighbours.items():J[i,js]=1
        need(field.rank(J)==9 and not np.any(field.mm(J,a[:,None])) and np.all(a),'full-support return relation in the native contact geometry')
        U=coefficients(params['U8_SHAKE_tag'],(480,8))
        need(field.rank(U)==8 and min(tiers)==5 and max(tiers)==7,'independent original directions on each physical copy')
        minor=np.zeros((12*480,12*480),dtype=np.uint8)
        receipts={i:apply_facet(field,i,neighbours[i],params,cache,U,minor) for i in range(111)}
        classes=[]
        for r in range(max(tiers)):
            donors=[j for j,m in enumerate(tiers) if m>r]
            rk=field.rank(J[:,donors]);classes.append({'direction':r,'donors':len(donors),'contact_rank':rk,'kernel':len(donors)-rk})
        nullity=sum(x['kernel'] for x in classes)+480-min(tiers);minor_rank=field.rank(minor)
        need(minor_rank>9*480+480//30,'actual minor exceeds the target return price for this word')
        n=sum(v['native_foreign_pairs'] for v in receipts.values());need(n==6470,'all foreign ranks tested')
        cross=8*sum(v['cross_ADD_per_copy'] for v in receipts.values());pure=8*sum(v['facet_diagonal_ADD_per_copy'] for v in receipts.values())
        result={'status':'PASS_ACTUAL_SHARED_INPUT_COORDINATES_AND_RETURN_KERNEL','field_modulus':67,'bank':3840,'physical_copies':8,
                'native_foreign_pairs':n,'donor_dimension_histogram':dict(Counter(tiers)),'shared_contact_subcodes':classes,
                'exact_prescribed_original_field_columns_aggregated_over_foreign_pairs':8*sum(v['source_columns_interpolated'] for v in receipts.values()),
                'synchronized_profile_dimension_per_copy':480,'intersection_dimension_per_copy':min(tiers),
                'proved_kernel_per_copy':nullity,'proved_native_kernel':8*nullity,'native_return_rank_upper':8*(111*480-nullity),
                'actual_first_twelve_receivers_donors_minor_rank_per_copy':minor_rank,'native_return_rank_lower':8*minor_rank,
                'minor_transformed_sha256':digest(minor),'new_cross_ADD':cross,'new_facet_diagonal_ADD':pure,'new_reserved_pure_Y_inverse_ADD':pure,
                'new_forward_plus_reserved_inverse_ADD':cross+2*pure,'additional_INIT':0,'additional_dirty_CLEAR':0,'additional_MOVE':0,
                'new_complete_kappa':False,'per_facet':receipts}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS',n,'foreign ranks, kernel',8*nullity,'return upper',result['native_return_rank_upper'],'lower',result['native_return_rank_lower'])

if __name__=='__main__':
    main()
