#!/usr/bin/env python3
"""Prove simultaneous genuine source and receiver star changes with arbitrary singular foreign maps."""
from pathlib import Path
import argparse,collections,gzip,json,random
def partition(adj,seed):
    rng=random.Random(seed);left=set(range(111));groups=[]
    while left:
        choices=left.copy();q=[]
        while choices:
            u=max(choices,key=lambda z:len(adj[z]&choices)+rng.random()*4)
            q.append(u);left.remove(u);choices&=adj[u]
        groups.append(sorted(q))
    return groups
def run(a):
    pairs=json.loads(gzip.decompress(a.pairs.read_bytes()));choose=json.loads(a.verify.read_text())if a.verify else None;result={}
    for s in ('L','R'):
      for h in (49,56):
       delta=7*h//5
       for dd in (0,1,4):
        name=f'{s}-{h}-{dd}';adj=[set()for i in range(111)]
        for z in pairs:
            if z['side']!=s:continue
            c=z['cost'];g=sum(q[2]-min(q[:2])for q in z['sector_ranks']);weights=sorted(z['chart_multiplicities'].values(),reverse=True)
            if 8*g<=c*h+(2*c+16)*delta+64*sum(weights[:dd]):continue
            u,v=z['pair'];adj[u].add(v);adj[v].add(u)
        groups=choose[name]['partition_into_conflicting_cliques']if choose else min((partition(adj,t)for t in range(30)),key=len)
        assert sorted(j for q in groups for j in q)==list(range(111))
        assert all(all(y in adj[x]for x in q for y in q if x!=y)for q in groups)
        result[name]={'actual_conflict_pairs':sum(map(len,adj))//2,'min_unchanged_words_to_modify':111-len(groups),'partition_into_conflicting_cliques':groups}
        print(name,111-len(groups),flush=True)
    if choose:assert result==choose
    a.out.write_text(json.dumps(result,indent=1,sort_keys=True)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--pairs',type=Path,required=True);p.add_argument('--verify',type=Path);p.add_argument('--out',type=Path,required=True);run(p.parse_args())
