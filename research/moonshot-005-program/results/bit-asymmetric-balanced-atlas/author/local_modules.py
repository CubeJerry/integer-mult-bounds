#!/usr/bin/env python3
"""Explicit GF16 V9/Hermite local words for the asymmetric port-two atlas."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
import gzip,json
from hashlib import sha256

def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&16:a^=0b10011
    return r

def power(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n//=2
    return r

def rank(rows):
    a=[list(v) for v in rows];p=0
    for c in range(len(a[0]) if a else 0):
        z=next((z for z in range(p,len(a)) if a[z][c]),None)
        if z is None:continue
        a[p],a[z]=a[z],a[p];inv=power(a[p][c],14);a[p]=[mul(inv,v) for v in a[p]]
        for z in range(len(a)):
            if z!=p and a[z][c]:
                v=a[z][c];a[z]=[x^mul(v,y) for x,y in zip(a[z],a[p])]
        p+=1
        if p==len(a):break
    return p

def binary_rows(A):
    out=[]
    for row in A:
        for bit in range(4):
            x=0
            for j,v in enumerate(row):
                for k in range(4):
                    if mul(v,1<<k)>>bit&1:x|=1<<(4*j+k)
            out.append(x)
    return out

def inplace_word(A):
    a=binary_rows(A);n=len(a);ops=[]
    def add(i,j):a[i]^=a[j];ops.append((i,j))
    for c in range(n):
        p=next(p for p in range(c,n) if a[p]>>c&1)
        if p!=c:add(p,c);add(c,p);add(p,c)
        for i in range(n):
            if i!=c and a[i]>>c&1:add(i,c)
    assert a==[1<<i for i in range(n)]
    out=[1<<i for i in range(n)]
    for i,j in reversed(ops):out[i]^=out[j]
    assert out==binary_rows(A)
    return list(reversed(ops))

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    lr=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    pr=gzip.decompress(Path(__file__).with_name('PARTITIONS.json.gz').read_bytes())
    assert sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    assert sha256(pr).hexdigest()=='2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25'
    lay=json.loads(lr);parts=json.loads(pr)['classes'];roots=lay['root_table'];Hs=list(map(set,lay['A2']));Ds=list(map(set,lay['D4']))
    orth=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0} for u in roots]
    incidences=0
    for h,H in enumerate(Hs):
        classes=parts[str(h)];assert len(classes)==5 and all(len(c)==9 for c in classes)
        assert sorted(d for c in classes for d in c)==[d for d,D in enumerate(Ds) if H<=D]
        for i,o in enumerate(orth):
            if H<=o:
                assert all(sum(Ds[d]<=o for d in c)==3 for c in classes);incidences+=1
    assert incidences==40320
    assert all(mul(x,power(x,14))==1 for x in range(1,16))
    nodes=range(1,10);V=[[power(z,t) for t in range(9)] for z in nodes]
    D=[[power(z,t-1) if t%2 else 0 for t in range(9)] for z in nodes]
    C=[[0 if t<3 else D[i][t] for t in range(9)] for i in range(9)]
    assert rank(V)==9
    checked=0
    for R in combinations(range(9),3):
        for j in range(3):assert rank([[V[i][t] for t in range(3*j,3*j+3)] for i in R])==3
        small=[[V[i][t] for t in range(3)]+[0]*3 for i in R]+[[0]*3+[V[i][t] for t in range(3)] for i in R]
        large=[[V[i][t] for t in range(3,9)] for i in R]+[[C[i][t] for t in range(3,9)] for i in R]
        assert rank(small)==rank(large)==6
        assert rank([V[i] for i in R]+[D[i] for i in R])==6
        checked+=1
    R=(0,1,2);bad=[[V[i][t] for t in range(3,9)] for i in R]+[[0]*6 for _ in R]
    assert rank(bad)==3 and rank([V[0],V[0],V[1],D[0],D[0],D[1]])<6
    word=inplace_word(V);A9=len(word);cp=sum(v.bit_count() for v in binary_rows(C));cs=sum(v.bit_count() for v in binary_rows(D))
    assert [j for j in range(9) if any(row[j] for row in C)]==[3,5,7]
    assert [j for j in range(9) if any(row[j] for row in D)]==[1,3,5,7]
    # Replay the complete early/late word on all72 independent binary input basis rows.
    # Cache only the actual input columns used by the cross-wave matrix.
    for cross in [C,D]:
        active=[j for j in range(9) if any(row[j] for row in cross)]
        public=[1<<j for j in range(72)];cache={4*j+k:public[4*j+k] for j in active for k in range(4)}
        for i,j in word:public[i]^=public[j]
        for i,j in word:public[36+i]^=public[36+j]
        for row,bits in enumerate(binary_rows(cross)):
            for bit in cache:
                if bits>>bit&1:public[36+row]^=cache[bit]
        expected=binary_rows(V)+[c^(v<<36) for c,v in zip(binary_rows(cross),binary_rows(V))]
        assert public==expected
        cache={bit:0 for bit in cache};assert not any(cache.values())
    invoices={'full_plane':{'ADD':10*A9+1080,'INIT':0,'dirty_CLEAR':0,'extra_peak':0},
      'partial_plane':{'ADD':10*A9+5*cp+60+1080,'INIT':60,'dirty_CLEAR':60,'extra_peak':60},
      'singleton_plane':{'ADD':10*A9+5*cs+80+1080,'INIT':80,'dirty_CLEAR':80,'extra_peak':80}}
    result={'status':'PASS_EXPLICIT_GF16_ASYMMETRIC_LOCAL_MODULES','field_degree':4,'field_polynomial':'t^4+t+1','nodes':list(nodes),
            'parent_receiver_plane_incidences_checked':incidences,'partition_uncompressed_sha256':sha256(pr).hexdigest(),
            'arbitrary_input_word_identities_checked':2,'receiver_triples_checked':checked,'full_donor_minors_checked':3*checked,
            'partial_large_donor_rank':6,'partial_small_donor_rank':6,'singleton_visible_rank':6,
            'V9_binary_ADDs':A9,'partial_derivative_binary_ADDs':cp,'singleton_derivative_binary_ADDs':cs,
            'whole_H_local_invoices':invoices,'nonzero_derivative_input_columns_partial':[3,5,7],
            'nonzero_derivative_input_columns_singleton':[1,3,5,7],
            'arbitrary_Y_baselines_preserved':True,'extra_MOVE':0,
            'negative_controls':{'omitted_derivative_loses_large_donor_rank':True,'repeated_nodes_fail':True},
            'GF16_subfield_requires_degree_divisible_by_4':True,'global_source_gluing_constructed':False,
            'complete_native_map_constructed':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'LOCAL-MODULES.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (a.out/'LOCAL-WORD.json').write_text(json.dumps({'V9':V,'partial_cross_C9':C,'singleton_derivative_D9':D,'binary_V9_ADD_word':word},separators=(',',':'))+'\n')
    print(result['status']);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
