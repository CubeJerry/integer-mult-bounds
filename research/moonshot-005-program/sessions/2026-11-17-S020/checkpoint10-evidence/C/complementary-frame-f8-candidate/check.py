#!/usr/bin/env python3
"""A conditional F8-coefficient route: exact algebra, not an admitted BIT word."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROLES=[14,17,19,20,96,99,101,102]
NATIVE_PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
        if a&8:a^=11
    return out
def inv(a):
    assert a
    return next(b for b in range(1,8) if mul(a,b)==1)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):
    out=[[0]*len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for k,x in enumerate(a[i]):
            for j,y in enumerate(b[k]):out[i][j]^=mul(x,y)
    return out
def inverse(a):
    n=len(a);q=[row[:]+tail for row,tail in zip(a,eye(n))]
    for j in range(n):
        p=next(k for k in range(j,n) if q[k][j]);q[j],q[p]=q[p],q[j]
        c=inv(q[j][j]);q[j]=[mul(c,x) for x in q[j]]
        for k in range(n):
            if k!=j:
                c=q[k][j];q[k]=[x^mul(c,y) for x,y in zip(q[k],q[j])]
    assert [r[:n] for r in q]==eye(n)
    return [r[n:] for r in q]
def binary_expand(a):
    return [[(mul(a[i//3][j//3],1<<(j%3))>>(i%3))&1 for j in range(3*len(a[0]))] for i in range(3*len(a))]
def bmm(a,b):return [[sum(x*y for x,y in zip(row,col))%2 for col in zip(*b)] for row in a]

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,default=HERE.parent/'native.json')
    p.add_argument('--out',type=Path,default=HERE/'RESULT.json');args=p.parse_args()
    raw=args.native.read_bytes();assert sha256(raw).hexdigest()==NATIVE_PIN
    roots=json.loads(raw)['native_roots']
    assert all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for i in ROLES for j in ROLES if i!=j)
    assert all(sum(x*x for x in roots[i])>0 for i in ROLES)
    lam=2;f=inv(lam^1);g=mul(lam,f)
    assert all(mul(a,inv(a))==1 for a in range(1,8))
    assert mul(lam,7)==5  # constant three-bit lane leaves the constant subspace
    matrices=[[[1,1],[1,lam]],[[1,f],[g,1]],[[1,1],[1,inv(lam)]]]
    determinants=[mul(t[0][0],t[1][1])^mul(t[0][1],t[1][0]) for t in matrices]
    assert all(determinants)
    seed=[(i+1)%4 for i in range(4)]+[4+(j-1)%4 for j in range(4)]
    histories=[1<<j for j in seed]
    network=eye(8);events=[];history_stages=[histories[:]]
    for offset,t in enumerate(matrices):
        layer=eye(8)
        for i in range(4):
            j=4+(i+offset)%4
            for rr,row in zip((i,j),t):
                layer[rr]=[0]*8;layer[rr][i],layer[rr][j]=row
            history=histories[i]|histories[j]
            assert not (history>>i)&1 and not (history>>j)&1
            histories[i]=histories[j]=history
            events.append({'round':offset+1,'pair':[i,j],'roles':[ROLES[i],ROLES[j]],
                           'source_mask':history,'rank':history.bit_count(),'matrix':t})
        network=mm(layer,network);history_stages.append(histories[:])
    assert [m.bit_count() for m in history_stages[0]]==[1]*8
    assert [m.bit_count() for m in history_stages[1]]==[2]*8
    assert [m.bit_count() for m in history_stages[2]]==[4]*8
    assert [m.bit_count() for m in history_stages[3]]==[6]*8
    native_seed=[[int(j==seed[i]) for j in range(8)] for i in range(8)]
    payload=mm(network,native_seed)
    for i,row in enumerate(payload):
        assert row[i]==0
        ownframe=range(4) if i<4 else range(4,8)
        assert all(row[j]==1 for j in ownframe if j!=i)
        assert sum(bool(x) for x in row)==5
        assert all(not x or histories[i]>>j&1 for j,x in enumerate(row))
    precondition=inverse(network)
    assert mm(network,precondition)==mm(precondition,network)==eye(8)
    # Full arbitrary baseline identity and native source map on all 48 bits.
    N,P,X=binary_expand(network),binary_expand(precondition),binary_expand(native_seed)
    assert bmm(N,P)==eye(24)
    assert bmm(N,X)==binary_expand(payload)
    # One omitted pair interaction must not preserve the prescribed eight triples.
    rejected=0
    for omitted in range(12):
        q=eye(8);count=0
        for offset,t in enumerate(matrices):
            layer=eye(8)
            for i in range(4):
                j=4+(i+offset)%4
                if count!=omitted:
                    for rr,row in zip((i,j),t):
                        layer[rr]=[0]*8;layer[rr][i],layer[rr][j]=row
                count+=1
            q=mm(layer,q)
        x=mm(q,native_seed)
        assert any(x[i][j]!=1 for i in range(8) for j in (range(4) if i<4 else range(4,8)) if i!=j)
        rejected+=1
    result={'status':'PASS_CONDITIONAL_F8_COEFFICIENT_NETWORK','field':'F2[lambda]/(lambda^3+lambda+1)',
        'lambda':lam,'round_matrices':matrices,'determinants':determinants,
        'roles':ROLES,'native_source_sha256':NATIVE_PIN,'seed_permutation':seed,
        'events':events,'network_matrix':network,'ground_inverse':precondition,'X_payload_matrix':payload,
        'all_independent_binary_columns':48,'omitted_pair_controls':rejected,
        'public_route_ranks':[0,1,2,4,6,7],
        'eight_route_profile':{'1':24,'2':16},'increment_over_direct_eight_facets':{'1':24,'2':16,'7':-8},
        'completed_diagonal_outputs':0,'owned_MOVEs_if_local_maps_are_admitted':0,
        'local_BIT_coefficient_compiler_supplied':False,
        'constant_lane_control':{'input_bits':[1,1,1],'lambda_times_input_bits':[1,0,1],
            'whole_record_ADD_and_coordinate_permutations_alone_cannot_compile_lambda':True},
        'scope':'An exact algebraic block-coefficient escape from the scalar F2 gate. NOT an admitted primitive BIT source word or profitable supplier.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'columns':48,'controls':rejected,'compiler_supplied':False}))
if __name__=='__main__':main()
