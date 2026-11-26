#!/usr/bin/env python3
"""Exact finite checks for shared destination Fourier gauges."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb, isqrt
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parent

def parity(x): return x.bit_count() & 1

def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)

def subspaces(d):
    found={(0,)}; queue=[(0,)]
    for space in queue:
        for x in range(1<<d):
            if x not in space:
                larger=tuple(sorted(set(space)|{u^x for u in space}))
                if larger not in found:
                    found.add(larger); queue.append(larger)
    return sorted(found,key=lambda x:(len(x),x))

def perpendicular(space,d):
    return tuple(x for x in range(1<<d) if all(not parity(x&u) for u in space))

def representatives(space,d):
    unseen=set(range(1<<d)); result=[]
    while unseen:
        c=min(unseen); result.append(c)
        unseen.difference_update(c^u for u in space)
    return result

def complement_checks():
    total_spaces=degenerate=entries=states=0
    for d in range(1,6):
        for V in subspaces(d):
            total_spaces+=1; W=perpendicular(V,d)
            degenerate += len(set(V)&set(W))>1
            for c in representatives(V,d):
                for xi in representatives(W,d):
                    values=[]
                    for y in range(1<<d):
                        value=sum((-1)**(parity(xi&u)^parity((c^u)&y)) for u in V)
                        expected=len(V)*(-1)**parity(c&y) if y^xi in W else 0
                        assert value==expected
                        values.append(value); entries+=1
                    assert sum(v!=0 for v in values)==len(W)
                    assert all(Fraction(v*v,(1<<d)*len(V))==Fraction(1,len(W)) for v in values if v)
                    states+=1
    paired=bad_phase_differences=0
    d,V=2,(0,3); W=perpendicular(V,d)
    for c1,c2,xi1,xi2 in product(representatives(V,d),representatives(V,d),representatives(W,d),representatives(W,d)):
        for y1,y2 in product(range(4),repeat=2):
            shared=direct=wrong=0
            for u1,u2 in product(V,repeat=2):
                x1,x2=c1^u1,c2^u2
                inp=parity(xi1&u1)^parity(xi2&u2)
                cross=parity(x1&y2)^parity(x2&y1); phase=parity(x1&x2)
                direct+=(-1)**(cross^inp)
                shared+=(-1)**((phase^cross)^(phase^inp))
                wrong+=(-1)**(cross^phase^inp)
            assert shared==direct
            bad_phase_differences+=wrong!=direct; paired+=1
    assert bad_phase_differences>0
    return {'subspaces':total_spaces,'degenerate_subspaces':degenerate,'basis_states':states,
            'character_sum_entries':entries,'paired_phase_entries':paired,
            'omitted_phase_differences':bad_phase_differences}

def unequal_parts(t):
    result=[]
    for b in range(1,t+1):
        tail=1<<(t-b)
        for prefix in range(1<<(b-1)):
            A=tuple((prefix<<(t-b+1))+z for z in range(tail))
            B=tuple(x+tail for x in A)
            result.extend(((A,B),(B,A)))
    return result

def incidence_checks():
    cases=[]; rectangles=rank_checks=incidences=0
    for t,L in ((1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(3,2),(3,3),(4,2)):
        q=1<<t; words=list(product(range(q),repeat=L)); N=len(words)
        lookup={word:i for i,word in enumerate(words)}
        gram=[sum(1<<j for j,v in enumerate(words) if sum(a!=b for a,b in zip(w,v))%2==0) for w in words]
        D=2+L*(q-2); assert rank(gram)==D
        lam=sum(comb(L,j)*t**j for j in range(1,L+1,2))
        derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
        mu=lam+(q-1-t)*derivative
        counts=[[0]*N for _ in range(2)]; ranks=[[0]*N for _ in range(2)]
        equal=[((a,),(a,)) for a in range(q)]; unequal=unequal_parts(t)
        rect_count=0
        for j in range(1,L+1,2):
            for different in combinations(range(L),j):
                different=set(different)
                for choices in product(*(unequal if i in different else equal for i in range(L))):
                    sides=[tuple(lookup[word] for word in product(*(item[side] for item in choices))) for side in (0,1)]
                    assert len(sides[0])==len(sides[1])
                    r_formula=1+sum(len(item[1])-1 for item in choices)
                    for side in (0,1):
                        actual=rank(gram[i] for i in sides[side]); assert actual==r_formula
                        rank_checks+=1
                        for i in sides[side]:
                            counts[side][i]+=1; ranks[side][i]+=actual; incidences+=1
                    assert all(not parity(gram[i]&(1<<w)) for i in sides[0] for w in sides[1])
                    rect_count+=1
        assert all(v==lam for side in counts for v in side)
        assert all(v==mu for side in ranks for v in side)
        old=2*D*lam; new=4*mu-2*lam+2*(D-1)
        assert new>=D+2*mu
        cases.append({'t':t,'L':L,'labels':N,'D':D,'rectangles':rect_count,
                      'lambda':lam,'mu':mu,'old_free_calls':old,'new_free_calls':new})
        rectangles+=rect_count
    return {'cases':cases,'rectangles':rectangles,'rank_checks':rank_checks,'incidences':incidences}

def inequality_checks():
    derivative_guards=q_guards=integer_bounds=0
    for L in range(2,81):
        for t in range(2,81):
            q=1<<t
            derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
            assert derivative>=L*(1+t)**(L-2)
            assert 4*(q-1-t)>=q
            derivative_guards+=1; q_guards+=1
    for a in range(4,13):
        x=1<<a; m=1<<x; target=max(0,isqrt(x*a)//4-2)
        for L in range(2,49):
            for t in (1,2,3,4,6,8,12,16,24,32,48,64,96,128):
                q=1<<t; D=2+L*(q-2)
                lam=sum(comb(L,j)*t**j for j in range(1,L+1,2))
                derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
                mu=lam+(q-1-t)*derivative
                J=Fraction(D+mu)+Fraction(m*D*comb(L,L//2),q**((L+1)//2))
                assert J>=1<<target
                integer_bounds+=1
    return {'derivative_guards':derivative_guards,'q_guards':q_guards,
            'rounded_logarithmic_bound_checks':integer_bounds}

def main():
    complement=complement_checks(); incidence=incidence_checks(); inequalities=inequality_checks()
    result={'status':'pass','python':sys.version.split()[0],
            'scope':'Exact finite complement, phase, Gram-rank and incidence checks; integer lower-bound guards, not tape timing or a complete multiplier.',
            'proof_sha256':sha256((ROOT/'ROUTING-DESTINATION-GAUGE-SHARING.md').read_bytes()).hexdigest(),
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'complement':complement,'incidence':incidence,'inequalities':inequalities,
            'negative_controls':['omitting the shared auxiliary quadratic phase changes the paired map']}
    (ROOT/'ROUTING-destination-gauge-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'complement':complement,
                      'incidence_counts':{k:v for k,v in incidence.items() if k!='cases'},
                      'inequalities':inequalities},indent=2))

if __name__=='__main__':main()
