"""Independent check of the native three-donor propagation and unidentified erasures."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(gzip.decompress(path.read_bytes()))


def main():
    p=argparse.ArgumentParser()
    for n in ('repo','charts','detours','out'):
        p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args()
    root=a.repo/'research/moonshot-005-program/results'
    source=gzip.decompress((root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    require(sha256(source).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','original native root source')
    v=json.loads(source)['root_table'][:111]
    foreign=[{j for j,u in enumerate(v) if sum(r*s for r,s in zip(w,u))==0} for w in v]
    def allowed(i,r,C):
        require(i!=r and not {i,r}&set(C) and len(C)==len(set(C))==8,'distinct exterior row roles')
        require(all(not foreign[c]&set(C) for c in C),'independent auxiliary roles')
        cand=foreign[i]&foreign[r]-set(C)
        for c in C:
            if c in foreign[i] or c in foreign[r]:
                cand=cand-foreign[c]
        return cand
    witness=read(a.charts)
    known={tuple(e) for e in witness['tree']}
    linear=read(root/'bit-global-native-rank-rigidity/author/output/WITNESS.json.gz')
    require(known==set(map(tuple,linear['tree'])),'common certified tree')
    components=[{r} for r in range(111)]
    steps=0
    for i,r,C,pivot,pex in witness['charts']:
        cells=allowed(i,r,C)
        require(pivot in cells and {(i,pivot),(r,pivot)}<=known,'two known native pivot maps')
        if pex:
            ref,p,q,s=pex
            require(ref in (i,r) and p==pivot and len({p,q,s})==3 and {p,q,s}<=cells,'three reference donors')
            require(all((ref,x) in known for x in (p,q,s)),'three bijective projections')
            require(components[i].isdisjoint(components[r]),'fresh additive connection')
            together=components[i]|components[r]
            for u in together:components[u]=together
            steps+=1
        require(components[i]==components[r],'genuine additive transition')
        for c in cells:
            if (i,c) in known or (r,c) in known:
                known.update([(i,c),(r,c)])
    require(steps==110 and known=={(i,j) for i in range(111) for j in foreign[i]},'all native functions and rows')
    w=read(a.detours)
    counts=[];degrees=Counter()
    table=w['cliques']
    for i,p,paths in w['detours']:
        previous=set()
        for r,q,k in paths:
            D=allowed(i,r,table[k])
            require({p,q}<=D,'matched two-donor detour')
            third=D-{p,q}
            require(third,'independent third donor exists')
            # Role r is known on p,q,s and row i is known on q. No test at (i,s).
            s=min(third)
            legs={(r,p),(r,q),(i,q),(r,s)}
            require(len(legs)==4 and not previous&legs,'four disjoint relied-on proper cells')
            previous|=legs
            degrees[len(D)]+=1
        counts.append(len(paths))
        require(len(paths)==min(len(foreign[i]),len(foreign[p]))-1,'optimal distinct detours per native endpoint')
    require(set((i,j) for i,j,_ in w['detours'])==set(map(tuple,linear['tree'])),'every native seed repairable')
    out={'triple_charts':len(witness['charts']),'additive_transitions':steps,'proper_functions':len(known),
         'all_erasures_up_to':min(counts),'detour_count':sum(counts),'third_donor_widths':dict(degrees),
         'detour_histogram':dict(Counter(counts)),'compressed_charts_sha256':sha256(a.charts.read_bytes()).hexdigest(),
         'compressed_detours_sha256':sha256(a.detours.read_bytes()).hexdigest()}
    a.out.mkdir(exist_ok=True,parents=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')


if __name__=='__main__':
    main()
