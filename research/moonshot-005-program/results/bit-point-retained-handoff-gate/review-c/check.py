#!/usr/bin/env python3
"""Independent native geometry review for the point-retained handoff gate.

Uses normalized integer lines and a reversed-basis Gray-code enumeration.
No author checker, generated row census, or WIP builder is imported.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PREDECESSORS={
    'author/PROOF.md':'8c7da091d813f260b2739faa3bc514e9ba515f969ec8a563f34352c1044ce0c6',
    'review-pigeonhole/PROOF.md':'efdfaf1a0ecce87c25144e0d6b30ed0a368c26f43e9e3af22798eef9cca3253a',
    'ADMISSION.md':'d580704acd5a796cf31aef266bcec0554e9b439fe02ee2371d40517279af0c46',
}


def require(ok,why):
    if not ok:
        raise ValueError(why)


def primitive(values):
    q=list(map(Fraction,values))
    den=lcm(*(x.denominator for x in q))
    ints=[int(x*den) for x in q]
    g=gcd(*ints)
    require(g!=0,'nonzero real line')
    ints=[x//g for x in ints]
    if next(x for x in ints if x)!=abs(next(x for x in ints if x)):
        ints=[-x for x in ints]
    return tuple(ints)


def real_rank(rows):
    rows=[list(map(Fraction,row)) for row in rows]
    dim=0
    for col in range(8):
        ix=next((i for i in range(dim,len(rows)) if rows[i][col]),None)
        if ix is None:
            continue
        rows[dim],rows[ix]=rows[ix],rows[dim]
        lead=rows[dim][col]
        rows[dim]=[x/lead for x in rows[dim]]
        for i in range(dim+1,len(rows)):
            factor=rows[i][col]
            if factor:
                rows[i]=[a-factor*b for a,b in zip(rows[i],rows[dim])]
        dim+=1
    return dim


def add_basis(word,piv):
    while word:
        bit=word.bit_length()-1
        if bit in piv:
            word ^= piv[bit]
        else:
            piv[bit]=word
            return True
    return False


def bit_indices(mask):
    result=[]
    while mask:
        bit=(mask&-mask).bit_length()-1
        result.append(bit)
        mask &= mask-1
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--author-proof',type=Path,required=True)
    p.add_argument('--programme',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    blob=args.native.read_bytes()
    require(sha256(blob).hexdigest()==PIN,'native digest')
    native=json.loads(gzip.decompress(blob))
    roots=[primitive(native['frames'][str(native['start'][i])]['B'][0]) for i in range(111)]
    require(len(set(roots))==111,'all actual source lines distinct')
    for i in range(111):
        facet=native['frames'][str(native['final'][111+i])]
        rows=list(map(primitive,facet['B']))
        require(facet['dim']==7 and real_rank(rows)==7,'actual receiver facet dimension')
        require(all(sum(a*b for a,b in zip(roots[i],r))==0 for r in rows),'actual receiver facet is root perpendicular')
    orth=[[sum(a*b for a,b in zip(x,y))==0 for y in roots] for x in roots]
    K=[sum((1<<j) for j in range(111) if j==i or orth[i][j]) for i in range(111)]
    S=[K[i]^(1<<i) for i in range(111)]
    full=(1<<111)-1
    piv={}
    basis=[]
    for word in reversed(K):
        if add_basis(word,piv):
            basis.append(word)
    require(len(basis)==9,'reversed canonical basis dimension')
    words=[0]
    current=oldgray=0
    for n in range(1,1<<9):
        gray=n^(n>>1)
        change=gray^oldgray
        require(change and not change&(change-1),'Gray-code one-bit step')
        current ^= basis[change.bit_length()-1]
        words.append(current)
        oldgray=gray
    require(len(set(words))==512,'all codewords exactly once')
    rows=[]
    strict_controls=[]
    for i in range(111):
        ni=full^K[i]
        candidates=[w for w in words if w and not w>>i&1]
        require(len(candidates)==255,'diagonal-zero code dimension')
        minimum=min((w&ni).bit_count() for w in candidates)
        witness=min(w for w in candidates if (w&ni).bit_count()==minimum)
        differences=[((S[i]&~S[h]).bit_count(),h) for h in range(111) if h!=i]
        size,partner=min(differences)
        gap=size-1
        support=witness&ni
        require(support.bit_count()==minimum and not (witness&ni&~support),'strict boundary witness')
        alternative=K[i]^witness
        require(alternative>>i&1 and alternative!=K[i] and not alternative&ni&~support,'canonical rigidity can fail at equality')
        require(not K[i]&ni,'zero own-coordinate condition cannot be dropped')
        rows.append(dict(i=i,rho=minimum,gap=gap,worst_partner=partner,
                         difference=bit_indices(S[i]&~S[partner]),distance_support=bit_indices(support)))
        strict_controls.append(dict(receiver=i,T=bit_indices(support),nonzero_diagonal_zero_word=hex(witness)))
    rho=dict(sorted(Counter(r['rho'] for r in rows).items()))
    gap=dict(sorted(Counter(r['gap'] for r in rows).items()))
    require(rho=={18:7,19:24,20:52,21:16,22:11,23:1},'distance census')
    require(gap=={20:4,21:26,22:47,23:25,24:8,25:1},'one-point suffix census')
    good=[r['i'] for r in rows if r['rho']>20 and r['gap']>20]
    require(good==[0,9,15,16,17,20,29,36,37,44,46,47,50,54,60,63,65,70,77,83,90,92,107,109],'exact 24 receiver witness')
    require(len(good)>20,'pigeonhole exclusion for every T of size at most20')
    thresholds=[]
    for t in range(24):
        count=sum(r['rho']>t and r['gap']>t for r in rows)
        thresholds.append(dict(T_size=t,good_receivers=count,pigeonhole_excludes=count>t))
    require(max(x['T_size'] for x in thresholds if x['pigeonhole_excludes'])==20,'scope of this particular threshold proof')
    require(min(s.bit_count() for s in S)==55,'no-public-interaction gap at least54')
    j,k=bit_indices(S[0])[:2]
    require(roots[j]!=roots[k] and real_rank([roots[j],roots[k]])==2,'incomparable source lines')
    require(orth[0][j] and orth[0][k],'their proper two-flat lies in receiver facet')
    # Route 0,L_j,0,L_k is nested at each step, but explicitly nonmonotone.
    point_route=[[],[roots[j]],[],[roots[k]]]
    require([real_rank(x) for x in point_route]==[0,1,0,1],'paid turn permits two line visits')
    B1=[12,48,77,84,91,99]
    B2=[13,47,80,87,88,96]
    T0=sorted({0,*B1,*B2})
    require(len(T0)==13 and real_rank([roots[x] for x in B1])==3 and real_rank([roots[x] for x in B2])==3,'conditional bank supports/ranks')
    require(all(orth[i][j] for i in B1 for j in B2),'conditional bank planes perpendicular')
    pred=args.programme/'results/bit-code-decoder-robustness'
    for name,pin in PREDECESSORS.items():
        require(sha256((pred/name).read_bytes()).hexdigest()==pin,'predecessor evidence unchanged: '+name)
    result=dict(status='PASS_INDEPENDENT_POINT_RETAINED_HANDOFF_GATE',
                native_sha256=PIN,reviewed_proof_sha256=sha256(args.author_proof.read_bytes()).hexdigest(),
                predecessors_sha256=PREDECESSORS,author_checker_imported_or_run=False,
                method='Primitive integer root lines; reversed native basis and Gray-code enumeration; direct set differences.',
                distinct_lines=111,verified_actual_facets=111,codewords=512,
                rho_histogram=rho,gap_histogram=gap,good20=good,thresholds=thresholds,rows=rows,
                strict_distance_boundary_controls=strict_controls,
                point_vs_mixed_bank_control=dict(receiver=0,sources=[j,k],mixed_rank=2,
                                                geometric_turn_dimensions=[0,1,0,1],complete_word_claimed=False),
                conditional_WIP_application=dict(T0=T0,coordinate_enlargement_allowance=7,
                                                uncommitted_source_or_decoder_validated=False),
                classification='Independent universal proof review plus exact finite source premises. Monotone point-only handoff scope; no tariff, complete supplier or new kappa.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],good_receivers=len(good),
                         highest_pigeonhole_threshold=20,rho_histogram=rho,gap_histogram=gap)))


if __name__=='__main__':
    main()
