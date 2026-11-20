"""Tangent in the 6,470 genuine directed native coefficients via kernel and cokernel bases."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def require(ok,why):
    if not ok:raise ValueError(why)


def parity(x):return x.bit_count()&1


def bits(x):
    while x:
        bit=x&-x;yield bit.bit_length()-1;x^=bit


def rref(rows,width):
    a=list(rows);r=0;piv=[]
    for j in range(width):
        u=next((t for t in range(r,len(a)) if a[t]&(1<<j)),None)
        if u is None:continue
        a[r],a[u]=a[u],a[r]
        for t in range(len(a)):
            if t!=r and a[t]&(1<<j):a[t]^=a[r]
        r+=1;piv.append(j)
        if r==len(a):break
    return a[:r],piv


def kernel(rows,width):
    reduced,piv=rref(rows,width);pivset=set(piv);basis=[]
    for j in range(width):
        if j in pivset:continue
        v=1<<j
        for c,row in zip(piv,reduced):
            if row&(1<<j):v|=1<<c
        require(all(parity(v&row)==0 for row in rows),'right kernel')
        basis.append(v)
    return basis,piv


def rank(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return len(piv)


def transpose(rows,w):
    return [sum(((r>>c)&1)<<i for i,r in enumerate(rows)) for c in range(w)]


def normal_equations(left,right,active):
    where={p:k for k,p in enumerate(active)};enc=[]
    for v in right:
        enc.append([sum(1<<where[i,j] for j in bits(v) if (i,j) in where) for i in range(111)])
    rows=[]
    for u in left:
        for rr in enc:
            row=0
            for i in bits(u):row^=rr[i]
            rows.append(row)
    return rows


def projection_rank(a,left,right):
    return rank([sum(parity(once&v)<<j for j,v in enumerate(right)) for once in
                [xor(a[i] for i in bits(u)) for u in left]])


def xor(xx):
    z=0
    for x in xx:z^=x
    return z


def minus(cell,rankpayload,payload,K):
    # Literal binary block rank of K tensor I + A tensor N for N e_(2p+1)=e_(2p).
    full=[]
    for i,row in enumerate(K):
        for t in range(payload):
            mask=sum(1<<(j*payload+t) for j in bits(row))
            if t<2*rankpayload and t%2==0:
                mask^=sum(1<<(j*payload+t+1) for j in bits(cell[i]))
            full.append(mask)
    return rank(full)


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(path.read_bytes());digest=hashlib.sha256(raw).hexdigest();require(digest=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native source pin')
    roots=json.loads(raw)['root_table'][:111];O=[sum((sum(x*y for x,y in zip(r,s))==0)<<j for j,s in enumerate(roots)) for r in roots]
    K=[v^(1<<i) for i,v in enumerate(O)];right,pc=kernel(K,111);left,pr=kernel(transpose(K,111),111)
    require(len(pr)==len(pc)==9 and len(left)==len(right)==102,'rank-nine pivot chart')
    foreign=[(i,j) for i,row in enumerate(O) for j in bits(row)]
    require(len(foreign)==6470,'native proper variables');eq=normal_equations(left,right,foreign);rankproper=rank(eq)
    w={p:c for c,p in enumerate(foreign)}
    d=[sum(1<<w[i,j] for i,j in foreign if (i==z)^(j==z)) for z in range(111)]
    require(all(parity(r&s)==0 for r in eq for s in d),'every gauge direction in tangent')
    need_tangent=len(foreign)-rankproper;require(need_tangent==rank(d)==110,'exact gauge tangent')
    encoding=lambda v,n:hashlib.sha256(b''.join(t.to_bytes((n+7)//8,'little') for t in v)).hexdigest()
    # Diagonal freedom independently permits arbitrary left and right rank-nine endpoint rescalings.
    expanded=sorted(foreign+[(i,i) for i in range(111)]);ext_rank=rank(normal_equations(left,right,expanded))
    require(len(expanded)-ext_rank==221,'free native diagonals mutation')
    cell=[0]*111;off=foreign[0];cell[off[0]]=1<<off[1]
    pair=cell.copy();pair[off[1]]^=1<<off[0]
    common=[O[i] if i==0 else ((1<<0) if O[i]&1 else 0) for i in range(111)]
    # Rank-one E_ij is nonzero in the quotient precisely when neither of its two projected axes vanishes.
    presentL={i for i in range(111) if any((z>>i)&1 for z in left)}
    presentR={j for j in range(111) if any((z>>j)&1 for z in right)}
    require(all(i in presentL and j in presentR for i,j in foreign),'single edge defects')
    examples={}
    for label,A in [('single',cell),('reciprocal_pair',pair),('coboundary_star',common)]:
        defect=projection_rank(A,left,right);direct={}
        for b,r in [(2,1),(4,1),(5,2)]:
            found=minus(A,r,b,K);require(found==9*b+r*defect,'nilpotent exact field rank')
            direct[f'{b}/{r}']=found
        examples[label]={'quotient_rank':defect,'literal_rank_by_payload_and_nilpotent_rank':direct}
    require(examples['single']['quotient_rank']==1 and examples['reciprocal_pair']['quotient_rank']==2 and examples['coboundary_star']['quotient_rank']==0,'charged and uncharged controls')
    # There are no diagonal perturbations in the main calculation. Gauge blocks use the same role at both endpoints.
    receipt={'pinned_layout':digest,'row_pivots':pr,'column_pivots':pc,'kernel_vectors':len(right),'cokernel_rows':len(left),
             'genuine_native_edge_variables':len(foreign),'kernel_cokernel_constraints':len(eq),'rank_of_restriction':rankproper,
             'allowed_tangent_dimension':need_tangent,'incidence_gauge_rank':rank(d),'constraint_payload_SHA256':encoding(eq,len(foreign)),
             'all_6470_single_edge_controls_have_quotient_rank_one':True,'free_diagonal_tangent_dimension':len(expanded)-ext_rank,
             'negative_and_square_zero_controls':examples,'test_edge':list(off)}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(receipt)


if __name__=='__main__':main()
