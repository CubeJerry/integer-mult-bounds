#!/usr/bin/env python3
"""Exact actual swap-orbit controls without spectral diagonalization."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json
from verify_inverse_query_commutator import Field,eye,inverse,multiply,rank,regular
from verify_phase_block_rank import phase,boundary,block_part,complete_blocks,difference


def kron(a,b,f):
    return [[f.mul(x,y) for x in ra for y in rb] for ra in a for rb in b]


def add(mats,f):
    out=[[0]*len(mats[0][0]) for _ in mats[0]]
    for a in mats:out=[[f.add(x,y) for x,y in zip(ra,rb)] for ra,rb in zip(out,a)]
    return out


def main():
    counts=Counter();profiles=[]
    for p,r,maxm in [(2,2,4),(3,3,3),(2,4,3),(5,5,2)]:
        f=Field(p)
        for m in range(1,maxm+1):
            target=regular({(1,)*m:[[1]]},m,r,1,1,f)
            assert rank(difference(target,eye(r**m,f),f),f)==(r-1)*r**(m-1)
            counts['nonsemisimple_regular_cycle_rank_identities']+=1
    for qs in [(2,),(3,),(2,2),(2,3),(4,2),(2,2,2),(2,2,2,2)]:
        points=list(product(*(list(product(range(q),repeat=2)) for q in qs)))
        ix={a:i for i,a in enumerate(points)};n=len(points);phases=[];bad=[]
        for a in points:
            alpha=tuple(int(x>y) for x,y in a if x!=y)
            phases.append(phase(alpha,2) if alpha else 2)
            bad.append(bool(alpha) and boundary(alpha,2,1))
        fixed=1
        for q in qs:fixed*=q
        assert Counter(phases)==Counter({0:(n-fixed)//2,1:(n-fixed)//2,2:fixed})
        target=[[0]*n for _ in range(n)];queries=[[[0]*n for _ in range(n)] for _ in qs]
        for j,a in enumerate(points):
            target[ix[tuple((y,x) for x,y in a)]][j]=1
            for coord in range(len(qs)):
                changed=list(a);changed[coord]=tuple(reversed(changed[coord]))
                i=ix[tuple(changed)];queries[coord][i][j]=1
                if not bad[j]:assert phases[i]==phases[j]
                counts['actual_swap_boundary_column_checks']+=1
        dist=[Fraction(1)]
        for q in qs:
            theta=Fraction(q-1,q);nxt=[Fraction(0)]*(len(dist)+1)
            for k,v in enumerate(dist):nxt[k]+=v*(1-theta);nxt[k+1]+=v*theta
            dist=nxt
        eta=sum(dist[k]*Fraction(sum(comb(k,j) for j in range(k+1) if abs(k-2*j)<=2),2**k)
                for k in range(1,len(dist)))
        assert eta==Fraction(sum(bad),n) and dist[0]==Fraction(fixed,n)
        for p in (2,3):
            f=Field(p)
            assert rank(difference(target,eye(n,f),f),f)==(n-fixed)//2
            counts['physical_identity_exact_baselines']+=1
        profiles.append({'q':qs,'D':n,'fixed':fixed,'eta1':str(eta)})
        counts['actual_multiplicity_mixture_identities']+=1
        if n<16 or n>64:continue
        f=Field(2);w=2;ps=[p for p in phases for _ in range(w)]
        g=add([kron(queries[0],[[1,0],[0,0]],f),kron(queries[-1],[[0,0],[0,1]],f),
               kron(eye(n,f),[[0,1],[0,0]],f),kron(queries[-1],[[0,1],[0,0]],f)],f)
        gi=inverse(g,f);assert gi is not None
        gz=block_part(g,ps);delta=rank(difference(g,gz,f),f)
        assert delta<=w*sum(bad)
        completed=complete_blocks(gz,ps,3,f);ci=inverse(completed,f)
        assert rank(difference(gi,ci,f),f)<=2*delta
        target2=kron(target,eye(w,f),f)
        assert rank(difference(target2,gz,f),f)>=(n-fixed)*w//2
        port=eye(n*w,f)
        good=next(i for i,p in enumerate(ps) if p==0)
        exceptional=next(i for i,p in enumerate(ps) if p==2)
        port[good][exceptional]=1
        actual=multiply(gi,multiply(port,g,f),f)
        comparison=multiply(ci,gz,f)
        assert rank(difference(actual,comparison,f),f)<=3*delta+1
        assert rank(difference(target2,actual,f),f)+3*delta+1>=(n-fixed)*w//2
        counts['f2_inverse_and_mixed_stratum_port_controls']+=1
    for k in range(1,1001):
        assert comb(k,k//2)**2*(k+1)<=4**k
        counts['exact_binomial_atom_bounds']+=1
    f=Field(2);swap=[[0,1],[1,0]]
    assert rank(difference(swap,eye(2,f),f),f)==1
    assert [x for x in range(2) if (x*x+1)%2==0]==[1]
    result={'status':'passed','arithmetic':'actual permutations and exact F2,F3,F5 ranks',
            'counts':dict(counts),'profiles':profiles,
            'negative_control':'F2 swap has sole eigenvalue1 but rank(Q-I)=1; scalar substitution is invalid',
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Actual swap-query model; free masks, comparisons and payload permutations excluded'}
    Path('nonsemisimple-swap-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
