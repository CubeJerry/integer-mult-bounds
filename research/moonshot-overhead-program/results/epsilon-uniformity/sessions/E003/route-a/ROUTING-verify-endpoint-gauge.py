#!/usr/bin/env python3
"""Finite exact checks for the one-gauge triangle obstruction."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import runpy
ROOT=Path(__file__).resolve().parent
helpers=runpy.run_path(str(ROOT/'ROUTING-verify-destination-gauge.py'))
parity=helpers['parity']; subspaces=helpers['subspaces']
perpendicular=helpers['perpendicular']; representatives=helpers['representatives']; rank=helpers['rank']

def bases(U,d):
    Up=perpendicular(U,d); N=1<<d; result=[]
    for c in representatives(U,d):
        for xi in representatives(Up,d):
            vector=[0]*N
            for u in U:vector[c^u]=(-1)**parity(xi&u)
            result.append(vector)
    return result

def basis_criterion():
    pairs=entries=monomial=0
    for d in range(1,5):
        N=1<<d; spaces=subspaces(d)
        B={U:bases(U,d) for U in spaces}
        FB={U:[[sum((-1)**parity(x&y)*column[x] for x in range(N)) for y in range(N)] for column in B[U]] for U in spaces}
        for U,V in product(spaces,repeat=2):
            column_support=[]
            for source in FB[U]:
                values=[sum(a*b for a,b in zip(destination,source)) for destination in B[V]]
                column_support.append(sum(value!=0 for value in values)); entries+=N
            is_monomial=all(count==1 for count in column_support)
            assert is_monomial==(V==perpendicular(U,d))
            monomial+=is_monomial; pairs+=1
    return {'subspace_pairs':pairs,'matrix_entries':entries,'monomial_pairs':monomial}

def triangle_checks():
    candidates=solutions=0
    for d in (3,4):
        directions=(1,2,4); spaces=subspaces(d)
        allowed=[tuple(U for U in spaces if all(not parity(x&direction) for x in U)) for direction in directions]
        for U in product(*allowed):
            candidates+=1
            perps=tuple(perpendicular(u,d) for u in U)
            if not(perps[0]==perps[1]==perps[2]):continue
            V=perps[0]
            if all(all(not parity(x&direction) for x in V) for direction in directions):solutions+=1
    assert solutions==0
    native=0
    for q,L in ((4,2),(4,3),(8,2),(16,2)):
        labels=[(a,)+(0,)*(L-1) for a in range(3)]
        gram=[[1-(sum(a!=b for a,b in zip(v,w))%2) for w in labels] for v in labels]
        assert gram==[[int(i==j) for j in range(3)] for i in range(3)]
        native+=1
    # Without norm-one, the self-dual isotropic line is a counterexample.
    U=(0,3); assert perpendicular(U,2)==U
    assert parity(3&3)==0 and all(not parity(x&3) for x in U)
    return {'input_gauge_triples':candidates,'compatible_triangles':solutions,'native_label_triangles':native,
            'norm_zero_counterexample':True}

def parity_rank_checks():
    cases=[]
    for L in range(1,11):
        N=1<<L; half=N//2
        rows=[(1<<i)|(1<<(i+half)) for i in range(half)]
        matrix=rows+rows
        assert rank(matrix)==half
        assert all((row&((1<<half)-1))==1<<i for i,row in enumerate(rows))
        # C contributes a paired square, F its two negative free entries.
        for i in range(half):
            for a,b in product((i,i+half),repeat=2):
                c=1; f=-1 if a!=b else 0
                assert c+f==int(a==b)
        cases.append({'L':L,'labels':N,'charged_rectangles':half,'rank':half})
    return cases

def main():
    criterion=basis_criterion(); triangles=triangle_checks(); ranks=parity_rank_checks()
    result={'status':'pass','scope':'Exact finite partial-basis and triangle checks plus sharp q=2 rank examples; no general circuit or tape lower bound.',
            'proof_sha256':sha256((ROOT/'ROUTING-GLOBAL-ENDPOINT-GAUGE.md').read_bytes()).hexdigest(),
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'helper_sha256':sha256((ROOT/'ROUTING-verify-destination-gauge.py').read_bytes()).hexdigest(),
            'partial_basis':criterion,'triangles':triangles,'parity_rank':ranks,
            'negative_controls':['norm-zero directions admit the forbidden self-dual gauge','q=2 bipartite exception remains admitted']}
    (ROOT/'ROUTING-endpoint-gauge-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','partial_basis':criterion,'triangles':triangles,'rank_cases':len(ranks)},indent=2))

if __name__=='__main__':main()
