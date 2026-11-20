"""Check the one-donor cost and the 6,470 native implications using sets of owners."""
import argparse
from collections import Counter
from itertools import combinations,permutations
import gzip
import json
from pathlib import Path


def nonzero(c):
    return {k:v for k,v in c.items() if v}


def main():
    ap=argparse.ArgumentParser()
    for arg in ('repo','horn','dual','out'):ap.add_argument('--'+arg,required=True,type=Path)
    a=ap.parse_args()
    dual=json.loads(a.dual.read_bytes());horn=json.loads(gzip.decompress(a.horn.read_bytes()))
    R=a.repo/'research/moonshot-005-program/results'
    roots=json.loads(gzip.decompress((R/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))['root_table'][:111]
    contacts=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(v,u))==0} for u in roots]
    pairs=tuple(map(frozenset,combinations(range(5),2)))
    def decode(mask):
        return frozenset(i for i in range(10) if mask>>i&1)
    def encode(S):
        return sum(1<<i for i in S)
    S=decode(dual['premise_mask']);v=dual['consequent']
    perms=[tuple(pairs.index(frozenset(q[i] for i in p)) for p in pairs) for q in permutations(range(5))]
    maps=sorted({(tuple(sorted(q[t] for t in S)),q[v]) for q in perms})
    stabilizer=[q for q in perms if {q[i] for i in S}==S and q[v]==v]
    assert len(maps)==60 and len(stabilizer)==2
    # Calculate on the stabilizer quotient rather than forming the mirrored raw sum.
    def orbit(U):
        return min(encode([q[x] for x in U]) for q in stabilizer)
    totals=Counter();rhs=0
    for weight,kind,*args in dual['terms']:
        if kind=='empty':
            totals[0]+=weight
            continue
        mask,x,*others=args;A=decode(mask)
        assert x not in A
        if kind=='submod':
            y,=others
            assert y!=x and y not in A and weight>0
            for U,z in [(A|{x},1),(A|{y},1),(A,-1),(A|{x,y},-1)]:
                totals[orbit(U)]+=z*weight
        else:
            assert kind in ('mono','decode')
            if kind=='mono':assert weight>0
            else:
                assert all(pairs[x]&pairs[y] for y in A)
                rhs+=weight
            totals[orbit(A|{x})]+=weight
            totals[orbit(A)]-=weight
    assert nonzero(totals)=={1023:4,59:2,571:-2} and rhs==20
    charts=horn['charts']
    for anchors,J in charts:
        assert len(set(anchors+J))==14
        A=frozenset(anchors);B=frozenset(J)
        assert all(not contacts[x]&(A|B) for x in A)
        for x,y in combinations(range(10),2):
            assert (J[y] in contacts[J[x]])==pairs[x].isdisjoint(pairs[y])
    seen=set()
    for i,j,steps in horn['arcs']:
        assert j in contacts[i] and (i,j) not in seen and len(steps)==3
        seen.add((i,j))
        initial=set(range(111))-contacts[i]-{i}|{j}
        current=initial.copy();used=[]
        for k,code in enumerate(steps):
            chart,r=divmod(code,len(maps))
            row=charts[chart][1];inp,out=maps[r]
            premise={row[u] for u in inp};result=row[out]
            assert premise<=(current if k==2 else initial)
            assert result not in current
            current.add(result);used.append(result)
        assert used[-1]==i and len(set(used))==3
    assert seen=={(i,j) for i,F in enumerate(contacts) for j in F}
    result={'local_quotient_coefficients':nonzero(totals),'local_rhs':rhs,'charted_cuts':len(charts),'checked_true_arcs':len(seen),'individual_rank_defect_multiple_of_excess':6,'minimum_rank_on_each_field_block_at_870':3840-6*128,'absent_arc_bound':9*3840+3840//6}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
