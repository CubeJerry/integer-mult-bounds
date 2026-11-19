#!/usr/bin/env python3
"""Independent exact review: replacement rank and common-row envelope."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

def basis(rows):
    pivots={}
    for row in rows:
        while row:
            k=row.bit_length()-1
            if k not in pivots:
                pivots[k]=row
                break
            row ^= pivots[k]
    return list(pivots.values())

def rank(rows): return len(basis(rows))
def action(rows,x): return sum(((row & x).bit_count()%2) << i for i,row in enumerate(rows))
def mul(x,y):
    value=0
    while y:
        if y&1: value ^= x
        y >>= 1
        x <<= 1
        if x&4: x ^= 7
    return value
def expand(matrix):
    out=[]
    for row in matrix:
        for s in range(2):
            bits=0
            for j,value in enumerate(row):
                for t in range(2):
                    if (mul(value,1 << t) >> s)&1: bits ^= 1 << (2*j+t)
            out.append(bits)
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('--repo',type=Path,required=True); p.add_argument('--out',type=Path,required=True); args=p.parse_args()
    programme=args.repo/'research/moonshot-005-program'
    src=programme/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    roots=json.loads(src.read_text())['native_roots']
    adj=[[int(i!=j and sum(x*y for x,y in zip(a,b))==0) for j,b in enumerate(roots)] for i,a in enumerate(roots)]
    K=[[v ^ int(i==j) for j,v in enumerate(row)] for i,row in enumerate(adj)]
    kbasis=basis([sum(v << j for j,v in enumerate(row)) for row in K]); assert len(kbasis)==9
    weights=[]
    for coefficients in range(1,512):
        word=0
        for i,row in enumerate(kbasis):
            if (coefficients >> i)&1: word ^= row
        weights.append(word.bit_count())
    assert min(weights)>2
    native=[]; H=expand(K)
    pairs=[(i,j) for i in range(111) for j in range(i+1,111) if adj[i][j]]
    for a,b in pairs[::max(1,len(pairs)//12)]:
        for alpha in (1,2,3):
            A=[row[:] for row in K]
            for i in range(111):
                if adj[i][a]: A[i][a] ^= alpha
            A[a][b] ^= alpha
            rows=expand(A)
            assert rank(rows)==20 and rank(rows+H)==22
            assert all(A[i][i]==1 for i in range(111))
            assert all(A[i][j]==0 for i in range(111) for j in range(111) if i!=j and not adj[i][j])
            if alpha!=1: assert all(A[i][j]!=0 for i in range(111) for j in range(111) if adj[i][j])
            native.append([a,b,alpha])
    envelope=[]
    for width,good in [(1,0),(2,0),(2,1),(3,1),(3,2),(3,3)]:
        n=111*width; A=[[0]*n for _ in range(n)]
        for i in range(111):
            for t in range(width): A[i*width+t][i*width+t]=1
            for j in range(111):
                if not adj[i][j]: continue
                for t in range(width): A[i*width+t][j*width+t]=1 if t<good else 2
                for t in range(good,width):
                    for u in range(good): A[i*width+t][j*width+u]=(13*i+7*j+3*t+u)%4
        expected=9*good+111*(width-good); observed=rank(expand(A))
        assert observed==2*expected
        envelope.append({'width':width,'good':good,'field_rank':expected,'binary_rank':observed})
    GL=[list(rows) for rows in itertools.product(range(8),repeat=3) if rank(rows)==3]; assert len(GL)==168
    count=0; lower=0
    for offdiag in range(64):
        B=[0]*3; bit=0
        for i in range(3):
            for j in range(3):
                if i!=j:
                    B[i] |= ((offdiag >> bit)&1) << j; bit += 1
        A=[B[i] ^ (1 << i) for i in range(3)]; R=basis(A); decode={}
        for x in range(8):
            m=action(R,x); value=action(A,x)
            assert m not in decode or decode[m]==value
            decode[m]=value
        assert len(decode)==len(set(decode.values()))==1 << rank(A)
        if R:
            short={}
            for x in range(8): short.setdefault(action(R[:-1],x),set()).add(action(A,x))
            assert any(len(values)>1 for values in short.values()); lower += 1
        for G in GL:
            inverse={action(G,z):z for z in range(8)}
            for x in range(8):
                message=action(R,x)
                for y in range(8):
                    preload=inverse[y ^ decode[message]]
                    assert action(G,preload) ^ action(B,x)==y ^ x
                    count += 1
    dual=[Fraction(54,11),Fraction(42,11),Fraction(120,11)]
    inequalities=[(4,-2,0),(-2,0,5),(0,2,1)]
    assert [sum(dual[j]*inequalities[j][i] for j in range(3)) for i in range(3)]==[12,12,30]
    assert sum(dual)==Fraction(216,11)
    point=[Fraction(9,22),Fraction(7,22),Fraction(4,11)]
    assert all(sum(x*y for x,y in zip(row,point))==1 for row in inequalities)
    assert (216*202)//11==3966 and 5760-3966==1794
    degree=(111+6470)*5760+111*5690
    assert degree==38538150
    assert degree+6470*5690==75352450 < 2**30
    assert 9*70+111*5690==632220
    budget=json.loads((programme/'results/bit-canonical-quotient-repair/author/output/BUDGET.json').read_text())
    assert budget['every_r_zero_through_203'][102]['first_even_m']==92
    result={'status':'PASS_INDEPENDENT_REPLACEMENT_AND_COMMON_ROW_REVIEW','native_rank':9,
            'native_minimum_nonzero_binary_codeword_weight':min(weights),'native_two_column_controls':native,
            'common_row_envelope_controls':envelope,'complete_small_protocol_cases':count,
            'shorter_message_negative_controls':lower,'LR_coefficient':'216/11',
            'seed_common_kernel_lower_bound_at_h202':1794,'actual_affine_product_degree':degree,
            'with_maximal_edge_defects_degree':degree+6470*5690,
            'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'physical_low_defect_source_code_constructed':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'protocol_cases':count,'min_weight':min(weights)}))
if __name__=='__main__': main()
