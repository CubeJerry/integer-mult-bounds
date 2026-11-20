#!/usr/bin/env python3
"""Price and check the coupled native six-facet observer and its true proper restrictions."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np

def check(value, reason):
    if not value:
        raise ValueError(reason)

def digest(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()

def paired(matrix,w):
    zero=np.zeros_like(matrix)
    twice=np.block([[matrix,zero],[zero,matrix]])
    columns=[j*w+s*matrix.shape[1]+k for j in range(matrix.shape[1]//w) for s in range(2) for k in range(w)]
    return twice[:,columns]

class Ops:
    def __init__(self, folder, base):
        home=Path(__file__).resolve().parent
        native=base/'bit-native-rs-return-distance'
        proper=base/'bit-spread-rs-physical-word/author'
        for name,src in [('field',home/'author/kernel.c'),('mul',proper/'gf64_matmul.c'),('stream',native/'stream/stream.c')]:
            subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared','-I',str(native/'author'),str(src),'-o',str(folder/(name+'.so'))],check=True)
        sys.path.insert(0,str(proper))
        from transfer import TABLE,INV,Arithmetic
        self.table,self.inv=TABLE,INV
        self.mul_path=folder/'mul.so'
        self.mm=Arithmetic(self.mul_path).matmul
        self.lib=ctypes.CDLL(str(folder/'field.so'))
        self.kernel_fn=self.lib.right_kernel
        p=ctypes.c_void_p;n=ctypes.c_size_t
        self.kernel_fn.argtypes=[p,n,n,p,p,p];self.kernel_fn.restype=n

    def kernel(self,a):
        a=np.array(a,dtype=np.uint8,order='C',copy=True)
        n=a.shape[1];out=np.empty(n*n,np.uint8)
        nullity=self.kernel_fn(a.ctypes.data,*a.shape,self.table.ctypes.data,self.inv.ctypes.data,out.ctypes.data)
        check(nullity<=n,'GF(64) elimination allocation')
        return out[:n*nullity].reshape(n,nullity).copy()

    def rank(self,a):
        return a.shape[1]-self.kernel(a).shape[1]

    def inverse(self,a):
        eye=np.eye(len(a),dtype=np.uint8)
        k=self.kernel(np.hstack([a,eye]))
        check(np.array_equal(k[len(a):],eye),'invertible native matrix')
        return k[:len(a)]

def run(args):
    home=Path(__file__).resolve().parent;repo=args.repo.resolve()
    inputs=home/'author/sources';s=np.load(inputs/'SMALL.npz');manifest=json.loads((inputs/'MANIFEST.json').read_text())
    check(set(s.files)==set(manifest) and all(digest(s[k])==v for k,v in manifest.items()),'bound native arrays')
    dst=args.out.resolve();dst.mkdir(exist_ok=True,parents=True)
    base=repo/'research/moonshot-005-program/results'
    with tempfile.TemporaryDirectory(prefix='six-native-') as td:
        folder=Path(td);op=Ops(folder,base);mm=op.mm
        from transfer import Atlas
        atlas=Atlas(repo,base/'bit-gf64-actual-k-atlas/author/output',base/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz',op.mul_path)
        atlas.left={i:atlas.left(i)for i in range(111)}.__getitem__
        w=96;d=2*w;h=76;eye=np.eye(d,dtype=np.uint8);unit=np.eye(h,dtype=np.uint8)
        kept={t for ch in atlas.kr.values()for _,src,dst0 in ch['stripes']if len(src)==9 for t in dst0}
        if args.heavy:
            sys.path.insert(0,str(home/'author'))
            from native import replay
            replay(repo,base,folder,atlas,s)
        K=s['K'];Q=np.vstack([paired(K[i*w:(i+1)*w],w) for i in range(8)])
        for i in range(4):
            check(np.array_equal(mm(s['W'][i],s['Winv'][i]),eye),'previous genuine paired gauge')
            Q[i*d:(i+1)*d,i*d:(i+1)*d]^=s['Winv'][i]^eye
        old_null=op.kernel(Q);check(old_null.shape==(8*d,384),'four-gauge inherited kernel')
        pop=np.array([sum(int(op.table[a,1<<k]).bit_count()for k in range(6))for a in range(64)],np.int64)
        cost=lambda a:int(pop[a].sum())
        paid={};proper=0;ground=0;source_effect=[];active=[]
        for i,u in enumerate(s['factor']):
            e_all,Ec,y_all,Yc=atlas.facet(i);es=list(s['e'+str(i)]);ys=list(s['y'+str(i)])
            check(es==[t for t in e_all if t in kept] and ys==[t for t in y_all if t in kept], 'true marked K output visitors')
            fold=np.hstack([Ec[:w,[e_all.index(t)for t in es]],Yc[:w,[y_all.index(t)for t in ys]]]);check(np.array_equal(fold,s['fold'+str(i)]),'native proper output coefficients')
            S=s['sens'+str(i)];projection=K[i*w:(i+1)*w].copy();projection[:,i*w:(i+1)*w]^=np.eye(w,dtype=np.uint8)
            check(np.array_equal(mm(fold,S),projection),'source-bound actual observer on eight-role quotient')
            phi=s['phi'+str(i)];n=len(es)+len(ys);phi0,phi1=phi[:,:n],phi[:,n:]
            feature=mm(phi,paired(S,w));source_effect.append(mm(feature,old_null))
            Q[i*d:(i+1)*d]^=mm(u,feature)
            def factor(A, B):
                inv=op.inverse(B)
                return np.hstack([mm(mm(ph,A),inv) for ph in (phi0,phi1)])
            G=np.hstack([mm(ph[:,len(es):],op.inverse(fold[:,len(es):]))for ph in (phi0,phi1)])
            midd=unit^mm(G,u);gg=mm(u,op.inverse(midd));ground+=1
            paid[i]={'forward':cost(phi)+cost(u),'ground_inverse':cost(G)+cost(gg)}
            count=0
            for j in sorted(t for t in atlas.orth[i] if t<111):
                ea,E,ya,Y=atlas.terminal_inputs(i,j)
                obs=np.vstack([E[[ea.index(t)for t in es],:w],Y[[ya.index(t)for t in ys],:w]])
                B=mm(fold,obs);check(np.array_equal(B,atlas.block(i,j)[:w,:w]),'native foreign response')
                check(op.rank(unit^mm(factor(obs,B),u))==h,'retuned proper remains invertible')
                count+=1
            proper+=count;active.append(count)
        check(all(np.array_equal(x,source_effect[0])for x in source_effect)and op.rank(source_effect[0])==h,'common observable on four-facet kernel')
        X=s['kernel'];r=op.rank(Q);check(op.rank(X)==460 and not mm(Q,X).any() and r==1076,'exact changed eight-role rank')
        pair_small=(111-8)*d+r;large_pair=109*2*384
        ret=4*(pair_small+large_pair);native_bank=111*3840
        inv=sum(sum(x.values())for x in paid.values())*4;extra_lifetimes=2*6*4*h*6
        check((proper,ground,ret,inv)==(350,6,418256,29922812),'complete finite receipt')
        result={'small_sector_width':w,'h':h,'changed_roles':list(range(6)),'foreigns_by_role':active,'changed_foreign_matrices':proper,'changed_ground_matrices':ground,'total_preserved_foreign_matrices':6470,'small_8role_rank':r,'small_pair_rank':pair_small,'small_pair_nullity':460,'large_pair_rank':large_pair,'full_native_return_fields':ret,'physical_rank8_MOVEs':6*ret,'saving_binary_MOVEs_vs_frozen':6*(native_bank-ret),'extra_saving_binary_MOVEs_vs_four':6*(418560-ret),'per_small_pair_per_role_ADDs':paid,'additional_ADDS_vs_four':inv,'additional_INIT_each_and_dirty_CLEAR_each_vs_four':extra_lifetimes,'additional_MOVE_vs_four':0,'fixed_plus_changed_proper_and_reserved_inverse_ADDs':2794107640+361035496+inv,'dense_return_ADD_upper_bound':2*(6*native_bank)*(6*ret),'physical_paid_MOVE_histogram':{1:12818880,2:10386720,4:552960,8:6*ret},'native_surplus_over_m870_compatible_return':ret-34688,'complete_multiplier_supplier':False}
        (dst/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print('native return',ret,'rank-eight moves',6*ret,'additional proper ADD',inv)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--heavy',action='store_true',help='rebuild every actual source-bound observer and Schur matrix')
    run(parser.parse_args())
