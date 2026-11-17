#!/usr/bin/env python3
"""Decode the frozen atlas from its flat bases and derive the independent target formula."""
import argparse,gzip,json,struct
from collections import Counter,defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
LAYOUT='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'

def dot(x,y):return sum(a*b for a,b in zip(x,y))

def echelon(rows):
    basis={}
    for row in rows:
        r=list(map(Fraction,row))
        for p,a in sorted(basis.items()):
            v=r[p]
            if v:r=[x-v*y for x,y in zip(r,a)]
        piv=next((j for j,v in enumerate(r) if v),None)
        if piv is not None:basis[piv]=[x/r[piv] for x in r]
    return basis

def make(native,layout,out):
    nr=native.read_bytes();lr=gzip.decompress(layout.read_bytes());assert sha256(nr).hexdigest()==NATIVE and sha256(lr).hexdigest()==LAYOUT
    raw=json.loads(nr)['native_roots'];w=json.loads(lr);R=w['root_table'];A=w['A2'];D=w['D4'];routes=w['routes']
    assert R[:111]==raw and len(set(map(tuple,R)))==120 and all(dot(r,r)==4 for r in R)
    Aset=list(map(set,A));Dset=list(map(set,D));orth=[set(j for j,r in enumerate(R) if dot(rt,r)==0) for rt in R]
    assert len(Aset)==1120 and len(Dset)==3150 and all(len(x)==3 for x in Aset) and all(len(x)==12 for x in Dset)
    assert all(len(echelon([R[j]for j in x]))==2 for x in Aset) and all(len(echelon([R[j]for j in x]))==4 for x in Dset)
    # Every site is encoded by the full set of root lines it contains. Verify double orthogonality,
    # so every nesting decision below also holds for the actual rational spans.
    def per(x):return set.intersection(*(orth[j] for j in x))
    allr=set(range(120)); assert all(per(per(a))==a for a in Aset+Dset)
    assert all(per(x)==Dset[w['dual_D4'][k]] for k,x in enumerate(Dset))
    sites=[set(),allr]+[{j} for j in range(111)]+Aset+Dset+[per(a) for a in Aset]+orth[:111]
    depths=[0,8]+[1]*111+[2]*1120+[4]*3150+[6]*1120+[7]*111
    # For each rank-6 and facet, the root representation really spans its annihilator.
    assert all(len(echelon(R[j] for j in a))==6 for a in sites[4383:5503])
    assert all(len(echelon(R[j] for j in a))==7 for a in sites[5503:])
    canonical=[[int(i==j or j in orth[i]) for j in range(111)]for i in range(111)]
    pairset=[];pairs=defaultdict(list);moves=Counter();edges={};cuts=Counter();donors=defaultdict(set);recips=defaultdict(set);origins=Counter();terminals=Counter()
    expectedX=defaultdict(set);expectedY=defaultdict(set)
    for n,(kind,d,h,j,k,i,sc,dc) in enumerate(routes):
        isx=kind=='X';slist=[2+j] if isx else [0]
        if not isx and j is not None and j<111:slist.append(2+j)
        if h is not None:slist.append(113+h)
        slist.append(1233+d)
        if k is not None:slist.append(4383+k)
        if i is not None and i<111:slist.append(5503+i)
        if isx:slist.append(1)
        for pre,post in zip(slist,slist[1:]):
            assert sites[pre]<sites[post] and depths[pre]<depths[post]
            k0=(pre,post);edges[k0]=depths[post]-depths[pre];moves[edges[k0]]+=6
        if h is not None:donors[h,d].add(n)
        if k is not None:recips[d,k].add(n)
        if isx:origins[j]+=1; expectedX[j,sc[1]].add(sc[0]);assert 0<=j<111
        else:terminals[i]+=1; expectedY[i,dc[1]].add(dc[0]);assert 0<=i<111
        if dc is None:continue
        if sc is None and h is None:
            pre=routes[n-1];assert kind=='Y' and pre[0]=='X' and pre[1]==d and pre[4] is None and pre[6] is not None
            j=pre[3];sc=pre[6];cuts['early_D_snapshots']+=1
        if sc is None:continue
        assert j in orth[i];al,s=sc;be,t=dc;pairs[i,j].append((s,al,t,be));pairset.append((i,j,s,al,t,be))
    assert len(donors)==len(recips)==50400 and all(len(v)==1 for v in list(donors.values())+list(recips.values()))
    assert set(origins.values())==set(terminals.values())=={240} and len(origins)==len(terminals)==111
    assert all(len(v)==16 for v in list(expectedX.values())+list(expectedY.values()))
    assert len(expectedX)==len(expectedY)==1665
    ranks=Counter()
    for i in range(111):
        for j in sorted(orth[i]&set(range(111))):
            p=pairs[i,j];src={(s,a)for s,a,t,b in p};dst={(t,b)for s,a,t,b in p}
            assert len(src)==len(dst)==len(p) and max(Counter(s for s,a in src).values(),default=0)<=16 and max(Counter(t for t,b in dst).values(),default=0)<=16
            ranks[len(p)]+=1
    assert sum(ranks.values())==6470 and len(pairset)==42840
    moves[8]+=12960;edges[1,0]=8
    out.mkdir(parents=True,exist_ok=True)
    (out/'allowed.dat').write_bytes(b''.join(struct.pack('<HHB',u,v,e)for (u,v),e in sorted(edges.items())))
    (out/'canonical.dat').write_bytes(bytes(sum(canonical,[])))
    (out/'terms.dat').write_bytes(b''.join(bytes(t)for t in sorted(pairset)))
    ans={'sites':len(sites),'geometry_arcs':len(edges),'whole_root_spans_checked':1120+3150+1120+111,
         'ordered_foreign_pairs':sum(ranks.values()),'rank_histogram':dict(sorted(ranks.items())),
         'early_X_snapshot_with_Y_beginning_at_D4':cuts['early_D_snapshots'],'binary_moves':dict(sorted(moves.items())),
         'expected_individual_rank_sum':sum(k*v for k,v in ranks.items())}
    (out/'GEOMETRY.json').write_text(json.dumps(ans,indent=2)+'\n');print(ans)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--layout',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();make(a.native,a.layout,a.out)
