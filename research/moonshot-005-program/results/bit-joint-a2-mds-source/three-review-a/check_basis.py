#!/usr/bin/env python3
"""Independent finite candidate-family minimum and adapted readout check."""
from pathlib import Path
import argparse,json,hashlib

def basis(rows):
    piv={}
    for r in rows:
        while r:
            j=r.bit_length()-1
            if j in piv:r^=piv[j]
            else:piv[j]=r;break
    return piv
def rank(rows):return len(basis(rows))
def xor(rows):
    r=0
    for x in rows:r^=x
    return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args()
    roots=json.loads((a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots']
    word=json.loads((a.source/'WORD.json').read_text())
    names=[f'X{j}_{k}' for j in range(111) for k in range(4)]
    y=[f'Y{j}_{k}' for j in range(111) for k in range(4)]
    val={n:1<<i for i,n in enumerate(names+y)}
    for tag,n,*z in word['operations'][:word['milestones']['joint_source_aggregate_cut']]:
        if tag=='INIT':val[n]=0
        elif tag=='ADD':val[z[0]]^=val[n]
        elif tag=='MOVE':pass
        else:raise AssertionError(tag)
    piv={}
    for i,n in enumerate(names):
        r,c=val[n],1<<i
        while r:
            q=r.bit_length()-1
            if q in piv:r^=piv[q][0];c^=piv[q][1]
            else:piv[q]=(r,c);break
    assert len(piv)==444
    def coordinates(row):
        c=0
        while row:
            q=row.bit_length()-1;row^=piv[q][0];c^=piv[q][1]
        return c
    held=[names.index(n) for n in word['direct_query_originals']]
    heldmask=sum(1<<i for i in held)
    canonical=[sum(1<<j for j,r in enumerate(roots) if i==j or sum(x*y for x,y in zip(roots[i],r))==0) for i in range(111)]
    scalar_basis=list(basis(canonical).values());assert len(scalar_basis)==9
    candidates=[]
    for m in range(1,512):
        scalar=xor(r for q,r in enumerate(scalar_basis) if m>>q&1)
        for bank in range(1,16):
            row=sum(1<<(4*j+k) for j in range(111) if scalar>>j&1 for k in range(4) if bank>>k&1)
            coeff=coordinates(row)
            proj=sum(((coeff>>j)&1)<<q for q,j in enumerate(held))
            weight=(coeff&~heldmask).bit_count()
            candidates.append((weight,row,proj))
    assert len(candidates)==len({r for w,r,p in candidates})==7665
    zero=sorted((w,r) for w,r,p in candidates if p==0)
    assert len(zero)==105 and rank([r for w,r in zero])==12
    greedy=[];greedy_weights=[];pivzero={}
    for weight,row in zero:
        r=row
        while r:
            q=r.bit_length()-1
            if q in pivzero:r^=pivzero[q]
            else:
                pivzero[q]=r;greedy.append(row);greedy_weights.append(weight);break
        if len(greedy)==12:break
    unit_min={p:min(w for w,r,q in candidates if q==p) for p in tuple(1<<i for i in range(24))}
    total=sum(greedy_weights)+sum(unit_min.values())
    assert total==3276
    seeds=word['canonical_seeds'];assert len(seeds)==36
    actual_zero=[];actual_units={}
    for seed in seeds:
        row=int(seed['canonical_row_hex'],16);coeff=coordinates(row)
        proj=sum(((coeff>>j)&1)<<q for q,j in enumerate(held))
        weight=(coeff&~heldmask).bit_count()
        assert weight==len(seed['Hub_reads'])
        if proj:actual_units[proj]=weight
        else:actual_zero.append((weight,row))
    assert actual_units==unit_min and len(actual_zero)==rank([r for w,r in actual_zero])==12
    assert sum(w for w,r in actual_zero)==sum(greedy_weights)
    out={'status':'INDEPENDENT_CONSTRAINED_CANDIDATE_BASIS_PASS','word_sha256':hashlib.sha256((a.source/'WORD.json').read_bytes()).hexdigest(),
         'candidate_count':7665,'zero_projection_count':105,'kernel_rank':12,
         'minimum_kernel_basis_Hub_read_sum':sum(greedy_weights),'minimum_unit_projection_weights':unit_min,
         'total_Hub_read_sum':total,'actual_basis_attains_constrained_minimum':True,
         'scope':'Minimum only within the7665 nonzero scalar-canonical-times-bank-vector candidates,12 kernel rows and one row for each unit held projection. No universal source/circuit optimality.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'BASIS-RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],total,unit_min)

if __name__=='__main__':main()
