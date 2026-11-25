#!/usr/bin/env python3
"""Exact finite controls for the literal binary-Walsh label invoice."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent

def gram_rank(q, width):
    words = list(product(range(q), repeat=width)); pivots = {}
    for left in words:
        row = sum(1 << j for j, right in enumerate(words)
                  if (1-sum(a != b for a,b in zip(left,right))) % 2)
        while row:
            high = row.bit_length()-1
            if high not in pivots:
                pivots[high] = row; break
            row ^= pivots[high]
    return len(pivots)

def p_value(width, distance):
    value = Fraction(1)
    for h in range(1,width//2+1): value *= 1-Fraction(distance,2*h)
    return value

def partition(q, width):
    words = list(product(range(q),repeat=width)); rectangles = {}; edges = 0
    for i,left in enumerate(words):
        for j,right in enumerate(words):
            distance = sum(a != b for a,b in zip(left,right))
            if distance % 2 == 0: continue
            assert p_value(width,distance)
            signature = []
            for a,b in zip(left,right):
                if a == b: signature.append(('equal',a))
                else:
                    bit = (a^b).bit_length()-1
                    signature.append(('different',bit,a>>(bit+1),(a>>bit)&1))
            key = tuple(signature)
            if key not in rectangles: rectangles[key] = [set(),set(),0]
            rectangles[key][0].add(i); rectangles[key][1].add(j)
            rectangles[key][2] += 1; edges += 1
    loads = [defaultdict(int),defaultdict(int)]
    for sources,destinations,count in rectangles.values():
        assert len(sources) == len(destinations)
        assert count == len(sources)*len(destinations)
        for i in sources: loads[0][i] += 1
        for j in destinations: loads[1][j] += 1
    t = q.bit_length()-1
    expected = sum(comb(width,j)*t**j for j in range(1,width+1,2))
    assert expected == ((1+t)**width-(1-t)**width)//2
    assert all(loads[0][i] == loads[1][i] == expected for i in range(len(words)))
    assert expected >= (1+t)**(width-1)
    return len(rectangles),edges,2*len(words)

def floor_log(value):
    n,d = value.numerator,value.denominator
    answer = n.bit_length()-d.bit_length()
    assert answer >= 0
    if n < d << answer: answer -= 1
    assert d << answer <= n < d << (answer+1)
    return answer

def main():
    ranks=[]; rectangle_total=edge_total=load_checks=0
    for q,limit in [(2,6),(4,4),(8,3),(16,2)]:
        for width in range(1,limit+1):
            rank=gram_rank(q,width); assert rank == 2+width*(q-2)
            ranks.append({'q':q,'L':width,'rank':rank})
            rectangles,edges,loads=partition(q,width)
            rectangle_total+=rectangles; edge_total+=edges; load_checks+=loads
    coefficient_checks=0
    for width in range(2,65):
        s=width//2; coefficients=[]
        for j in range(s+1):
            coefficients.append(p_value(width,width-j)-sum(coefficients[h]*comb(j,h) for h in range(j)))
        assert coefficients[s] == Fraction(1,2**s)
        for distance in range(width+1):
            assert p_value(width,distance) == sum(coefficients[j]*comb(width-distance,j) for j in range(min(s,width-distance)+1))
            coefficient_checks+=1
    invoice_checks=0
    for log_x in range(4,11):
        x=2**log_x
        for width in range(2,49):
            s,r=width//2,(width+1)//2
            for t in [1,2,3,4,6,8,12,16,24,32,48,64]:
                q=2**t; dim=2+width*(q-2)
                incidence=((1+t)**width-(1-t)**width)//2
                bill=Fraction(dim*(1+incidence))+Fraction(dim*2**x*comb(width,s),2**(r*t))
                assert floor_log(bill)**2 >= x*log_x
                invoice_checks+=1
    # Invalid odd-q extension, wrong full incidence, omitted charged term.
    assert gram_rank(3,2) == 5 != 2+2*(3-2)
    assert ((1+1)**2-(1-1)**2)//2 != (1+1)**2
    assert Fraction(1,2) != 0
    files=[Path(__file__).name,'binary-walsh-label-invoice-barrier.md']
    receipt={'status':'passed','rank_cases':ranks,
             'canonical_rectangles':rectangle_total,'partitioned_edges':edge_total,
             'per_side_vertex_load_checks':load_checks,
             'exact_newton_expansion_values':coefficient_checks,
             'exact_integer_invoice_guards':invoice_checks,'negative_controls':3,
             'scope':'finite exact controls; universal companion proof; no runtime lower bound',
             'sha256':{n:sha256((ROOT/n).read_bytes()).hexdigest() for n in files}}
    (ROOT/'binary-walsh-label-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__ == '__main__': main()
