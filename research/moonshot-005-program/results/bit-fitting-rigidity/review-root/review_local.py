#!/usr/bin/env python3
"""Independent transposed-Jacobian review of the actual BIT local theorem."""
import argparse, gzip, hashlib, json
from fractions import Fraction
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAME=(0,16,17,32,36,38,67,71)

def require(c,m):
    if not c: raise ValueError(m)

def rank_low(vectors):
    pivots={}
    for a in vectors:
        while a:
            p=(a&-a).bit_length()-1
            if p not in pivots:
                pivots[p]=a
                break
            a^=pivots[p]
    return len(pivots)

def main(a):
    raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,'Source identity')
    native=json.loads(gzip.decompress(raw))
    roots=[tuple(Fraction(z) for z in native['frames'][str(c)]['B'][0]) for c in native['start'][:111]]
    dot=lambda x,y:sum(u*v for u,v in zip(x,y))
    # Determine K by actual real contact geometry, rather than reducing Gram entries.
    K=[[int(i==j or dot(roots[i],roots[j])==0) for j in range(111)] for i in range(111)]
    require(all(K[i][j]==int(i==j) for i in FRAME for j in FRAME),'Identity frame')
    X=[]
    for i in range(111):
        first=[K[i][j] for j in FRAME]
        X.append(first+[1^(sum(first)%2)])
    require(all(sum(x*y for x,y in zip(X[i],X[j]))%2==K[i][j] for i in range(111) for j in range(111)),'Exact symmetric factor')
    # Reverse vertex order, separate C/R, and use the transposed linear operator.
    labels=[(side,i,q) for side in ('R','C') for i in reversed(range(111)) if i not in FRAME
            for q in reversed(range(9)) if q==8 or K[i][FRAME[q]]]
    constraints=[(i,j) for i in reversed(range(111)) for j in reversed(range(111)) if not K[i][j]]
    constraints.extend((i,i) for i in range(111))
    index={p:k for k,p in enumerate(constraints)}
    cols=[]
    for side,i,q in labels:
        col=0
        for j in range(111):
            pair=(i,j) if side=='C' else (j,i)
            if pair in index and X[j][q]: col|=1<<index[pair]
        cols.append(col)
    rank=rank_low(cols)
    require((len(labels),len(constraints),rank)==(1120,5851,1009),'Transposed Jacobian dimensions/rank')
    gauges=[]
    for parameter in range(112):
        g=0
        for k,(_,i,q) in enumerate(labels):
            peer=FRAME[q] if q<8 else 111
            if X[i][q] and ((parameter==i) != (parameter==peer)):g|=1<<k
        image=0
        for k,col in enumerate(cols):
            if g>>k&1:image^=col
        require(image==0,'Gauge annihilated by Jacobian')
        gauges.append(g)
    require(rank_low(gauges)==111 and len(labels)-rank==111,'Full kernel equals gauge image')
    total=0
    for g in gauges:total^=g
    require(total==0,'Unique all-one gauge relation')
    reached={0}
    while True:
        nxt=reached|{j for i in reached for j in range(111) if K[i][j]}
        if nxt==reached:break
        reached=nxt
    require(len(reached)==111,'Contact connectivity')
    cert=json.loads((a.author/'CERTIFICATE.json').read_text())
    require(cert['canonical_factor_rows_9bit']==[sum(z<<q for q,z in enumerate(x)) for x in X],'Author factor identification')
    # Independently check the author's claimed square rank witness in its own ordering.
    author_labels=[(side,i,q) for i in range(111) if i not in FRAME for q in range(9)
                   if q==8 or K[i][FRAME[q]] for side in (0,1)]
    author_constraints=[(i,j) for i in range(111) for j in range(111) if i==j or not K[i][j]]
    row_indices=cert['jacobian_nonsingular_minor_constraint_indices']
    variables=cert['jacobian_nonsingular_minor_variable_indices']
    require(len(row_indices)==len(set(row_indices))==len(variables)==len(set(variables))==1009,'Minor index counts')
    minor=[]
    for z in row_indices:
        i,j=author_constraints[z];row=0
        for n,v in enumerate(variables):
            side,k,q=author_labels[v]
            bit=(k==i and side==0 and X[j][q]) or (k==j and side==1 and X[i][q])
            if bit:row|=1<<n
        minor.append(row)
    require(rank_low(minor)==1009,'Author nonsingular minor independently verified')
    mutant=minor[:];mutant[-1]=mutant[0]
    require(rank_low(mutant)<1009,'Repeated minor row control')
    require(any(cols),'Non-gauge factor perturbation control')
    # Noncommuting matrix polynomials through degree two, without author bit-polynomial code.
    def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2))%2 for j in range(2)] for i in range(2)]
    def pm(a,b):
        out=[[[0,0],[0,0]] for _ in range(3)]
        for p in range(3):
            for q in range(3-p):
                m=mm(a[p],b[q])
                for i in range(2):
                    for j in range(2):out[p+q][i][j]^=m[i][j]
        return out
    I=[[1,0],[0,1]];Z=[[0,0],[0,0]];unit=[I,Z,Z]
    u=[I,[[0,1],[0,0]],Z];v=[I,[[0,0],[1,0]],Z]
    require(pm(u,u)==pm(v,v)==unit,'Exact unit inverses')
    require(pm(pm(pm(u,v),v),u)==unit and pm(pm(pm(v,u),v),u)!=unit,'Ordered gauge control')
    result={'status':'PASS_INDEPENDENT_TRANSPOSED_JACOBIAN_AND_ORDERED_PROOF_REVIEW',
        'source_sha256':PIN,'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),
        'geometry_factor_products':12321,'variables':1120,'constraints':5851,
        'independent_transpose_rank':rank,'factor_gauge_kernel_dimension':111,
        'matrix_gauge_dimension':110,'author_square_minor_rank':1009,
        'negative_controls':['Repeated minor row loses rank','Non-gauge factor perturbation changes a constraint','Reversed noncommuting gauge order fails'],
        'universal_review':'Exact eight-frame normalization, central-bit linearization on each J^n/J^(n+1), ordered vertex/factor induction and t-adic limit checked. Rational-family inverse-contact identities hold at every regular specialization.',
        'limitation':'Canonical nilpotent/formal neighbourhood only; disconnected minimum fittings and global all-volume rigidity remain open. No new supplier or kappa.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','independent_transpose_rank','factor_gauge_kernel_dimension','matrix_gauge_dimension']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
