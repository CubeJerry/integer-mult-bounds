"""Audit the weighted native closure, all own diagonals, and the odd-characteristic minor."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from check import source,closure,determinant,need


def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--certificates',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args()
    g=source(x.repo);load=lambda n:json.loads((x.certificates/(n+'.json')).read_bytes());v=load('WEIGHTED');declared=Counter(t[-1] for t in v['closure']);old=load('CLOSURE');need(v['tree']==old['tree'],'same normalized spanning tree')
    # The cost transcript is sorted by cost. Rebuild the valid earlier-corner set and every geometric restriction.
    ordered=sorted(v['closure'],key=lambda t:t[-1]);trans={'tree':v['tree'],'layers':[declared[k] for k in sorted(declared)],'forced':[t[:-1] for t in ordered]}
    weights,stats=closure(g,trans)
    for edge,*_,w in v['closure']:need(weights[divmod(edge,111)]==w,'complete weighted recurrence')
    frames=load('DIAGONALS');bound={};arcs=set(weights)
    for i in range(111):
        bill,r,c=frames[str(i)];need(len(r)==len(c)==9 and len(set(r+c+[i]))==19,'true exterior 9 by 9')
        det=determinant([[g[u][v] for v in c] for u in r]);bord=determinant([[g[u][v] if u!=v else 1 for v in c+[i]] for u in r+[i]])
        support=[(u,v) for u in r+[i] for v in c+[i] if (u,v) in arcs];cost=sum(weights[e] for e in support)
        need(det%2 and not bord%2 and bill==cost,'actual canonical Schur scalar and invoice')
        bound[i]=[cost,len(support),2*cost+len(support),det,bord]
    odd=load('ODD');r,c=odd['rows'],odd['cols'];need(len(r)==len(c)==10 and len(set(r+c))==20,'disjoint odd pivot')
    D=determinant([[g[u][v] for v in c] for u in r]);e=[(u,v) for u in r for v in c if (u,v) in arcs]
    bill=sum(weights[p] for p in e);need(D==odd['det'] and abs(D)==2 and bill==odd['weight']==7,'exact odd determinant and weight')
    # A single source gauge G_i=S_i^{-1} needs the destination-column diagonal bill.
    native_h=max(weights[i,j]+1+bound[j][0] for i,j in weights)
    native_delta=max(2*weights[i,j]+1+bound[j][2] for i,j in weights)
    result={'weighted_foreign_costs':dict(Counter(weights.values())),'source_payload_SHA256':{n:sha256((x.certificates/(n+'.json')).read_bytes()).hexdigest() for n in ('WEIGHTED','DIAGONALS','ODD')},
            'diagonal_max_h_multiplier':1+max(v[0] for v in bound.values()),'diagonal_max_tree_deficit_multiplier':max(v[2] for v in bound.values()),
            'true_simultaneous_native_change_max_h_multiplier':native_h,'true_simultaneous_native_change_max_tree_deficit_multiplier':native_delta,
            'odd_det':D,'odd_weight':bill,'odd_support_count':len(e),'odd_tree_deficit_multiplier':2*bill+len(e),
            'odd_characteristic_necessary_bound':f'8h+{2*bill+len(e)}delta>=b','all_native_diagonal_frames':bound,'weighted_rectangles':stats}
    x.out.mkdir(exist_ok=True,parents=True);(x.out/'WEIGHTED-REVIEW.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print({k:h for k,h in result.items() if k not in ('all_native_diagonal_frames','source_payload_SHA256')})


if __name__=='__main__':main()
