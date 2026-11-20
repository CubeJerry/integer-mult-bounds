"""Exact convex incidence bounds from the two star censuses and all canonical four-cycles."""
from functools import lru_cache
from math import comb


@lru_cache(None)
def degree_pairs(count,edges):
    if not count:return 0 if not edges else 10**12
    q,r=divmod(edges,count);return count*q*(q-1)//2+r*q


@lru_cache(None)
def rectangle(rows,cols):
    lo,hi=0,rows*cols+1
    while hi-lo>1:
        n=(lo+hi)//2
        if degree_pairs(rows,n)<=comb(cols,2) and degree_pairs(cols,n)<=comb(rows,2):lo=n
        else:hi=n
    return lo


def split_minimum(m,k,cap):
    if not k:return degree_pairs(110,m)
    return min(degree_pairs(k,s)+degree_pairs(110-k,m-s)for s in range(min(cap,m)+1))


def bound():
    scores={};full=None
    for u in range(63):
        for v in range(62):
            bridge=int(bool(u*v));touch=(110-v if u else 0)+(110-u if v else 0)+bridge
            lo,hi=0,min(rectangle(110,110),touch+rectangle(110-v,110-u))+1
            while hi-lo>1:
                n=(lo+hi)//2
                a=split_minimum(n,v,110-u+int(bool(u)));b=split_minimum(n,u,110-v+int(bool(v)))
                if a<=comb(110,2)-comb(u,2) and b<=comb(110,2)-comb(v,2):lo=n
                else:hi=n
            scores[u,v]=u+v+lo
    maximum=max(scores.values());at=[list(k)for k,v in scores.items()if v==maximum]
    return {'nonisolated_original_flat_donors':110,'nonisolated_original_flat_facets':110,'flat_correct_upper':rectangle(110,110),
            'arbitrary_retention_global_whole_correct_upper':maximum,'minimum_failed_original_blocks':6470-maximum,
            'only_retained_counts_achieving_combinatorial_upper':at,'all_marked_retained_total_correct_upper':scores[62,61],
            'all_marked_retained_minimum_failed_global_blocks':6470-scores[62,61],'outside_marked_union_canonical_upper':rectangle(49,48),'degree_cases':len(scores)}

if __name__=='__main__':
    import argparse
    import json
    from pathlib import Path
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);args=p.parse_args();root=Path(__file__).resolve().parent
    if not (root/'output/ALL-FLAT-RESULT.json').exists():raise ValueError('upstream all-canonical numerical census required')
    result=bound();assert result['arbitrary_retention_global_whole_correct_upper']==1220 and result['all_marked_retained_total_correct_upper']==578
    args.out.mkdir(exist_ok=True,parents=True);(args.out/'EXTREMAL.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',result['degree_cases'],result['minimum_failed_original_blocks'])
