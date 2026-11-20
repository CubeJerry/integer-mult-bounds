"""Authenticate optimal edge-disjoint three-cell repairs of the native tree."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import itertools
import json
from pathlib import Path


def check(cert,native,seed):
    cliques=cert['cliques']
    foreign={(i,j) for i,u in enumerate(native) for j,v in enumerate(native)
             if i!=j and sum(x*y for x,y in zip(u,v))==0}
    degree=Counter(i for i,_ in foreign)
    summary={}
    for i,j,paths in cert['detours']:
        if (i,j) in summary or (i,j) not in foreign:
            raise ValueError('bad repair seed')
        used=set()
        for r,s,k in paths:
            cells={(i,j),(i,s),(r,j),(r,s)}
            if len(cells)!=4 or not cells<=foreign:
                raise ValueError('bad repair rectangle')
            C=cliques[k]
            if len(set(C))!=8 or set(C)&{i,j,r,s} or any((a,b) in foreign for a,b in itertools.combinations(C,2)):
                raise ValueError('bad eight-pivot exterior')
            if any((a,c) in foreign and (c,b) in foreign for a,b in cells for c in C):
                raise ValueError('exterior correction survives')
            legs=cells-{(i,j)}
            if legs&used:raise ValueError('reused repair cell')
            used.update(legs)
        if len(paths)!=min(degree[i],degree[j])-1:raise ValueError('native degree optimum')
        summary[i,j]=len(paths)
    if set(summary)!=set(map(tuple,seed)):raise ValueError('tree not covered')
    return {'certified_tree_edges':len(summary),'pairwise_disjoint_detours_total':sum(summary.values()),
            'detour_histogram':dict(Counter(summary.values())),'minimum_detours':min(summary.values()),
            'minimum_native_degree':min(degree.values())}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    R=a.repo/'research/moonshot-005-program/results'
    source=gzip.decompress((R/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    if sha256(source).hexdigest()!='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72':
        raise ValueError('native root source')
    roots=json.loads(source)['root_table'][:111]
    seed=json.loads(gzip.decompress((R/'bit-global-native-rank-rigidity/author/output/WITNESS.json.gz').read_bytes()))['tree']
    raw=gzip.decompress((Path(__file__).resolve().parent/'output/DETOURS.json.gz').read_bytes())
    cert=json.loads(raw)
    out=check(cert,roots,seed)
    cert['detours'][0][2][1]=cert['detours'][0][2][0]
    try:check(cert,roots,seed)
    except ValueError as e:out['duplicated_detour_control']=str(e)
    else:raise ValueError('duplicate detour accepted')
    out['witness_sha256']=sha256(raw).hexdigest()
    a.out.mkdir(exist_ok=True,parents=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
