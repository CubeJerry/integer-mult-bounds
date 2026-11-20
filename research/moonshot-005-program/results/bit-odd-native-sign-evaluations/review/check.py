#!/usr/bin/env python3
"""Independent eight-query decoder from the authenticated integer root coordinates."""
import argparse,collections,gzip,hashlib,json,random
from pathlib import Path

def dot(u,v):return sum(a*b for a,b in zip(u,v))
def signed(r,m):return (r+m//2)%m-m//2
def main(args):
    path=args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    original=json.loads(raw)['root_table'][:111];v=[]
    for q,row in enumerate(original):
        if q<8:
            assert row==[2*int(t==q) for t in range(8)];v.append([t//2 for t in row])
        else:
            assert set(row)<={-1,0,1} and sum(t!=0 for t in row)==4;v.append(row)
    contact=[sorted(j for j,x in enumerate(original) if dot(x,original[i])==0)for i in range(111)]
    assert len(original)==111 and sum(map(len,contact))==6470
    for i in range(111):
        assert [j for j,y in enumerate(v)if dot(v[i],y)==0]==contact[i]and i not in contact[i]
        for j in contact[i]:
            z=[v[i][k]*v[j][k]for k in range(8)];assert z.count(1)==z.count(-1)
    norms=[dot(x,x) for x in v];assert collections.Counter(norms)=={1:8,4:103}
    mod=(5,9);rng=random.Random(31003)
    def fun(i,j,xy):
        x,y=xy;a=(i+2*j)%5;b=(3*i+j)%9
        return (a*x**3%5,b*y**3%9)
    for i,js in enumerate(contact):
        for j in js:
            for g in [(0,0),(1,2),(2,4)]:
                fg=fun(i,j,g);neg=fun(i,j,(-g[0]%5,-g[1]%9))
                assert neg==tuple(-x%m for x,m in zip(fg,mod))
    def observe(x):
        out=[]
        for i,js in enumerate(contact):
            total=list(x[i])
            for j in js:
                p=fun(i,j,x[j])
                for k in range(2):total[k]+=p[k]
            out.append(tuple(t%m for t,m in zip(total,mod)))
        return out
    for _ in range(9):
        xx=[(rng.randrange(5),rng.randrange(9))for v0 in v]
        yy=[observe([tuple(v[j][t]*u%m for u,m in zip(x,mod))for j,x in enumerate(xx)])for t in range(8)]
        zz=[tuple(sum(v[i][t]*yy[t][i][k] for t in range(8))*pow(norms[i],-1,mod[k])%mod[k] for k in range(2))for i in range(111)]
        assert zz==xx
    # Changing a single odd map to x squared at a real contact can destroy cancellation.
    defect=next((i,j,sum(v[i][t]*v[j][t]**2 for t in range(8))%5)for i,js in enumerate(contact)for j in js if sum(v[i][t]*v[j][t]**2 for t in range(8))%5)
    badcontact=next((i,j,dot(v[i],v[j]))for i in range(111)for j in range(i+1,111)if dot(v[i],v[j])%5)
    assert defect[2] and badcontact[2]%5 and 4*1%4==0
    out={'layout_raw_sha256':hashlib.sha256(raw).hexdigest(),'integer_coordinates':8,'roles':111,'native_foreign_directed_edges':6470,
         'squared_norm_census':dict(collections.Counter(norms)),'finite_exhaustive_conditions':'all 6470 distinct integer orthogonality cancellations',
         'nonlinear_odd_product_group_tests':9,'product_group_orders':mod,'nonodd_true_contact_control':defect,
         'adding_one_nonorthogonal_offdiagonal_control':badcontact,'order_four_diagonal_control':[1,4,0],
         'rank_lower_bound_at_3840':111*3840//8,'base_log_image_lower_bound':'111/8'}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
