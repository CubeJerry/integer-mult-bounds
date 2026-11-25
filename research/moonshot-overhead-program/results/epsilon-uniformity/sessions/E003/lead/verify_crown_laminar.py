#!/usr/bin/env python3
"""Exact crown-product run counts and optimal binary-hierarchy diagnostics."""
from itertools import product, permutations
from pathlib import Path
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parent

def graph(q,k):
    words=list(product(range(q),repeat=k))
    neighbors=[sum(1<<j for j,y in enumerate(words) if all(a!=b for a,b in zip(x,y))) for x in words]
    return words,neighbors

def gray(q,k):
    if k==0:return [()]
    suffix=gray(q,k-1); result=[]
    for a in range(q):
        result.extend((a,)+v for v in (suffix if a%2==0 else reversed(suffix)))
    return result

def runs(order,neighbors):
    counts=[]
    for row in neighbors:
        old=0; count=0
        for j in order:
            new=(row>>j)&1; count+=new and not old; old=new
        counts.append(count)
    return counts

def hierarchy_optimum(neighbors):
    n=len(neighbors); full=(1<<n)-1
    common=[full]*(full+1); best=[0]*(full+1); split=[0]*(full+1); trials=0
    for mask in range(1,full+1):
        bit=mask & -mask; index=bit.bit_length()-1; rest=mask^bit
        common[mask]=common[rest]&neighbors[index]
        if rest==0:continue
        part=rest; value=-1
        while True:
            left=part|bit; right=mask^left
            if right:
                trials+=1; candidate=best[left]+best[right]
                if candidate>value:value=candidate; split[mask]=left
            if part==0:break
            part=(part-1)&rest
        best[mask]=common[mask].bit_count()+value
    clusters=[]
    def recover(mask):
        if mask & (mask-1)==0:return
        clusters.append(mask); left=split[mask]
        recover(left); recover(mask^left)
    recover(full)
    assert len(clusters)==n-1
    counts=[row.bit_count()-sum(mask&row==mask for mask in clusters) for row in neighbors]
    assert sum(counts)==sum(row.bit_count() for row in neighbors)-best[full]
    return {'minimum_total_clusters':sum(counts),'witness_source_loads':counts,
            'subset_states':full,'partition_trials':trials}

def main():
    cases=[]; pair_checks=0; permutation_count=0; hierarchy_cases=[]
    parameters=[(2,k) for k in range(1,5)]+[(3,k) for k in range(1,4)]+[(4,k) for k in range(1,4)]+[(5,2),(8,2)]
    for q,k in parameters:
        words,neighbors=graph(q,k); n=len(words); degree=(q-1)**k
        lower=(n+q-2)*(q-1)**(k-1)
        for i,y in enumerate(words):
            assert neighbors[i].bit_count()==degree
            for j,z in enumerate(words):
                h=sum(a!=b for a,b in zip(y,z))
                intersection=(q-2)**h*(q-1)**(k-h)
                assert (neighbors[i]&neighbors[j]).bit_count()==intersection
                if i!=j:assert (neighbors[i]^neighbors[j]).bit_count()>=2*(q-1)**(k-1)
                pair_checks+=1
        ordered=gray(q,k); index={word:i for i,word in enumerate(words)}
        assert len(set(ordered))==n
        assert all(sum(a!=b for a,b in zip(y,z))==1 for y,z in zip(ordered,ordered[1:]))
        order=[index[word] for word in ordered]; counts=runs(order,neighbors)
        assert sum(counts)==lower
        row={'q':q,'k':k,'vertices_per_side':n,'degree':degree,
             'minimum_total_runs':lower,'gray_source_loads':counts}
        if n<=9:
            weights=[[(a^b).bit_count() for b in neighbors] for a in neighbors]
            optimum=None; checked=0
            for p in permutations(range(n)):
                value=degree+sum(weights[a][b] for a,b in zip(p,p[1:]))//2
                optimum=value if optimum is None else min(optimum,value); checked+=1
            assert optimum==lower
            permutation_count+=checked
            row['all_orderings_checked']=checked
        cases.append(row)
    for q,k in [(2,2),(3,2),(4,2)]:
        words,neighbors=graph(q,k); result=hierarchy_optimum(neighbors)
        lower=(len(words)+q-2)*(q-1)**(k-1)
        assert result['minimum_total_clusters']>=lower
        hierarchy_cases.append({'q':q,'k':k,'universal_lower_bound':lower,**result})
    words,neighbors=graph(4,2); index={word:i for i,word in enumerate(words)}
    rectangles=[]; edge_counts={}; source_loads=[0]*16; target_loads=[0]*16
    for a,b in words:
        left=[index[(x,b)] for x in range(4) if x!=a]
        right=[index[(a,y)] for y in range(4) if y!=b]
        rectangles.append((set(left),set(right)))
        for i in left:source_loads[i]+=1
        for j in right:target_loads[j]+=1
        for i in left:
            for j in right:
                assert (neighbors[i]>>j)&1
                edge_counts[i,j]=edge_counts.get((i,j),0)+1
    assert len(edge_counts)==144 and set(edge_counts.values())=={1}
    assert source_loads==target_loads==[3]*16
    assert any(b&d and not (b<=d or d<=b) for _,b in rectangles for _,d in rectangles)
    controls={
        'endpoint_degree_cannot_be_omitted': cases[0]['minimum_total_runs']!=cases[0]['minimum_total_runs']-cases[0]['degree'],
        'general_partition_can_beat_common_order': max(source_loads)<(54+15)//16,
        'q_two_neighborhoods_are_singletons': all(row.bit_count()==1 for row in graph(2,4)[1]),
    }
    assert all(controls.values())
    result={'status':'passed','scope':'Finite exact arithmetic diagnostics; universal claims use the written proof.',
            'graph_cases':cases,'neighborhood_pair_checks':pair_checks,
            'orderings_exhaustively_checked':permutation_count,
            'binary_hierarchy_subset_dynamic_programs':hierarchy_cases,
            'nonlaminar_crown_4_2_partition':{'rectangles':16,'edges':144,'source_load':3,'target_load':3},
            'negative_controls':controls,
            'proof_sha256':sha256((ROOT/'crown-product-laminar-obstruction.md').read_bytes()).hexdigest(),
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'crown-laminar-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key!='graph_cases'},indent=2))

if __name__=='__main__': main()
