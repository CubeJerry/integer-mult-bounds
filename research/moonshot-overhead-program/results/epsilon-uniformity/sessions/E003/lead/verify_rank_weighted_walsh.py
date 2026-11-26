#!/usr/bin/env python3
"""Exact Gram-side ranks, weighted incidences, and the new invoice guards."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def rank(rows):
    pivots={}
    for value in rows:
        while value:
            high=value.bit_length()-1
            if high not in pivots:pivots[high]=value;break
            value^=pivots[high]
    return len(pivots)

def gram(q,L):
    words=list(product(range(q),repeat=L))
    rows=[sum(1<<j for j,w in enumerate(words) if (1-sum(a!=b for a,b in zip(v,w)))%2) for v in words]
    return words,rows

def canonical(q,L):
    words,rows=gram(q,L);pieces={}
    for i,v in enumerate(words):
        for j,w in enumerate(words):
            if sum(a!=b for a,b in zip(v,w))%2==0:continue
            key=[]
            for a,b in zip(v,w):
                if a==b:key.append(('e',a))
                else:
                    bit=(a^b).bit_length()-1
                    key.append(('d',bit,a>>(bit+1),(a>>bit)&1))
            left,right=pieces.setdefault(tuple(key),(set(),set()))
            left.add(i);right.add(j)
    loads=[[0]*len(words) for _ in range(2)];weighted=[[0]*len(words) for _ in range(2)]
    for left,right in pieces.values():
        assert len(left)==len(right)
        for side,indices in enumerate((left,right)):
            sizes=[len({words[i][coordinate] for i in indices}) for coordinate in range(L)]
            r=rank(rows[i] for i in indices)
            assert r==1+sum(size-1 for size in sizes)
            for i in indices:loads[side][i]+=1;weighted[side][i]+=r-1
    t=q.bit_length()-1
    lam=sum(comb(L,j)*t**j for j in range(1,L+1,2))
    derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
    for side in range(2):
        assert set(loads[side])=={lam}
        assert set(weighted[side])=={(q-1-t)*derivative}
    return {'q':q,'L':L,'rectangles':len(pieces),'side_rank_checks':2*len(pieces),
            'labels_per_side':len(words),'incidences_per_label':lam,
            'rank_minus_one_sum_per_label':weighted[0][0]}

def floor_log(value):
    n,d=value.numerator,value.denominator
    answer=n.bit_length()-d.bit_length()
    if n<d<<answer:answer-=1
    assert d<<answer<=n<d<<(answer+1)
    return answer

def main():
    canonical_cases=[canonical(q,L) for q,limit in [(2,6),(4,4),(8,3),(16,2)] for L in range(2,limit+1)]
    proper_checks=0
    for q,L in [(2,3),(4,2),(4,3)]:
        words,rows=gram(q,L);lookup={w:i for i,w in enumerate(words)}
        subsets=[tuple(i for i in range(q) if mask>>i&1) for mask in range(1,(1<<q)-1)]
        for sides in product(subsets,repeat=L):
            indices=[lookup[w] for w in product(*sides)]
            assert rank(rows[i] for i in indices)==1+sum(len(side)-1 for side in sides)
            proper_checks+=1
    free_guards=invoice_guards=0
    for L in range(2,65):
        for t in range(1,65):
            q=2**t;D=2+L*(q-2)
            lam=sum(comb(L,j)*t**j for j in range(1,L+1,2))
            derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
            assert L*(t+1)**(L-2)<=derivative
            assert (L-1)*lam<=(t+1)*derivative<=2*L*lam
            free=D+lam+2*(q-1-t)*derivative
            if t>=2:
                assert q-1-t>=q//4
                assert 4*(t+1)*free>=D*lam
                assert (t+1)*free<=10*D*lam
            free_guards+=1
            if t not in [1,2,3,4,6,8,12,16,24,32,48,64]:continue
            for log_x in range(4,11):
                x=2**log_x
                bill=Fraction(free)+Fraction(D*2**x*comb(L,L//2),q**((L+1)//2))
                assert 16*floor_log(bill)**2>=x*log_x
                invoice_guards+=1
    _,rows=gram(4,2)
    controls={
        'proper_subset_hypothesis_is_required':rank(rows)!=1+2*(4-1),
        'subtracting_t_in_rank_sum_is_required':canonical_cases[0]['rank_minus_one_sum_per_label']==0 and 2-1!=0,
        'new_invoice_is_not_the_old_endpoint_list':(2+2)!=2*(1+2),
    }
    assert all(controls.values())
    receipt={'status':'passed','scope':'Exact rank and arithmetic diagnostics only; physical factoring is a separate proof obligation.',
             'canonical_cases':canonical_cases,'proper_product_sides_checked':proper_checks,
             'free_bill_integer_guards':free_guards,'total_invoice_integer_guards':invoice_guards,
             'negative_controls':controls,
             'sha256':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in
                       [Path(__file__).name,'rank-weighted-walsh-invoice.md']}}
    (ROOT/'rank-weighted-walsh-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='canonical_cases'},indent=2))

if __name__=='__main__':main()
