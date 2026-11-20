import argparse,gzip,hashlib,json
from pathlib import Path
import numpy as np
from basis import change
from recfield import Field
from action import unpack
from native import modes
def perm(x):
    perm=np.array(x,np.int32);n=len(x);assert sorted(x)==list(range(n));seen=set();c=0
    for i in range(n):
        if i in seen:continue
        j=i;c+=1
        while j not in seen:seen.add(j);j=perm[j]
        assert j==i
    return n-c
def main(a):
    f=Field(a.lib);f.init_price();tags=['small','large'];native={s:np.load(a.out/(s+'-owners.npz'))for s in tags};totals={}
    expected=json.loads((a.program/'output/PRICE.json').read_text());modes_rank={}
    for tag,w,d in [('small',96,168),('large',384,672)]:
        P=np.concatenate([modes(tag,j,w,d)for j in [0,1]],axis=0)
        A=change(f.b.wrap(P),f.b.rec);modes_rank[tag]=f.det(A)[0];assert modes_rank[tag]==d
    allprice={}
    for i in range(111):
        pure=cross=cache=0;permutation=[-1]*3840
        for sec,w,raw_base in [('small',96,0),('large',384,768)]:
            e=native[sec][f'{i}-X'];y=native[sec][f'{i}-Y'];raw,F=unpack(a.program/sec,i)
            A=change(F.reshape(w,len(e)+len(y)),f.b.rec)
            pure+=2*f.price(A[:,len(e):]);cross+=2*int(f.costs[A[:,:len(e)]].sum(dtype=np.int64));cache+=48*len(e)
            for z,t in enumerate(y):
                raw_idx=int(t)-53280-480*i
                for l in range(8):permutation[raw_idx*8+l]=raw_base+l*w+z
        reorder=18*perm(permutation);ground=pure+reorder
        pr={'pure_F_ADD':pure,'early_to_late_ADD':cross,'stationary_original_copy_ADD_INIT_dirty_CLEAR':cache,'F_final_owner_permutation_ADD':reorder,'Ground_inverse_ADD':ground}
        pr['actual_F_total_ADD']=sum(pr.values());assert pr==expected['facets'][str(i)],(i,pr,expected['facets'][str(i)])
        allprice[i]=pr
        if i%20==0:print('invoice',i,flush=True)
    total={k:sum(p[k]for p in allprice.values())for k in allprice[0]}
    assert total==expected['whole_atlas'];z={'independent_native_Z_seed_rank':modes_rank,'all_111_facets':allprice,'total':total,'reciprocal_modulus':hex(0x1b00001)}
    (a.out/'PRICE-REVIEW.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('program','lib','out'):p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())
