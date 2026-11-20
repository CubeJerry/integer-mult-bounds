#!/usr/bin/env python3
"""All nonorthogonal pairs force changes in at least 103 actual stars at each end."""
import argparse,gzip,json,hashlib
from pathlib import Path
from itertools import combinations
from collections import Counter
import numpy as np
def run(a):
    packed=gzip.decompress(a.pairs.read_bytes());W=json.loads(packed);out={}
    layout=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    assert hashlib.sha256(layout).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    roots=np.array(json.loads(layout)['root_table'][:111]);expect={(i,j)for i,j in combinations(range(111),2)if int(roots[i]@roots[j])!=0}
    assert len(expect)==2870 and all((roots[:8]@roots[:8].T-np.diag(np.diag(roots[:8]@roots[:8].T))).flatten()==0)
    for side in ('L','R'):
        rows=[t for t in W if t['side']==side]
        assert len(rows)==len(expect)and {tuple(t['pair'])for t in rows}==expect
        vals={};allg=[];costs=[]
        for h in (128,134):
            nums=[]
            for q in rows:
                g=sum(x[2]-min(x[0],x[1])for x in q['sector_ranks']);cost=q['cost']
                needed=max(0,-(-(8*g-h*cost)//64));m=sorted(q['chart_multiplicities'].values(),reverse=True)
                count=next(k for k in range(len(m)+1)if sum(m[:k])>=needed)
                nums.append(count);allg.append(g);costs.append(cost)
            assert min(nums)>0;vals[h]={'minimum_num_D_changes_to_remove_any_pair':min(nums),'max_compatible_unchanged_stars_for_fewer_changes':8,'min_changed_stars_if_fewer_D_changes':103,'all_pair_D_change_histogram':dict(Counter(nums))}
        out[side]={'native_pairs':len(rows),'minimum_body_stacked_rank_gap':min(allg),'maximum_total_edge_cost':max(costs),'bounds':vals}
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--pairs',type=Path,required=True);p.add_argument('--out',type=Path,required=True);run(p.parse_args())
