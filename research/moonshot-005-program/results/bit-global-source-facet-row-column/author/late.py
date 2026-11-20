"""Propagate genuine donor-labelled late source visits to all real final facets."""
from collections import defaultdict
import numpy as np


def prepare(native,transfer,facet_weights,cache):
    cache.mkdir(parents=True,exist_ok=True)
    groups=defaultdict(list)
    for u,route in native.route.items():
        if route[0]=='Y' and route[6] is not None and route[3] is not None:
            groups[route[6],route[3]].append(u)
    for slots in groups.values():slots.sort()
    facets={i:native.facet(i) for i in range(111)}
    middles={d:native.middle_matrix(d) for d in range(len(native.D))}
    for j in range(111):
        actual=sorted(u for (donor,_),rows in groups.items() if donor==j for u in rows)
        locate={u:t for t,u in enumerate(actual)};width=len(actual);left={}
        for h in native.ks[j]:
            slots=groups[j,h]
            if not slots:continue
            p=native.phase[str(h)];donors=sorted(native.H[h]&set(range(111)))
            quota={int(z):v for z,v in p['donor_early'].items()}
            if p['late']!=1 or quota[j]!=15 or len(slots)!=15:raise ValueError('true native late visits')
            used=0
            for ports in native.h_ports[h]:
                n=len(ports);k=n//3
                allocation=transfer.grouped_sources('Y',donors,p['m'],k,quota)
                powers=[t for t,donor in enumerate(allocation) if donor==j]
                if len(powers)!=k:raise ValueError('true donor late exponents')
                positions=[locate[u] for u in slots[used:used+k]];used+=k
                for t,d in enumerate(ports):
                    row=np.zeros(width,dtype=np.uint8);row[positions]=native.V[n][t,powers]
                    left[native.left_flags[h,d,'Y'][0]]=row
            if used!=len(slots):raise ValueError('complete late donor allocation')
        delivery={}
        for d,(word,owners) in middles.items():
            if j not in native.D[d]:continue
            inputs=[q for q,u in enumerate(owners) if u in left];late=[q for q,u in enumerate(owners) if native.route[u][0]=='Y']
            if inputs:
                values=native.ops.matmul(word[np.ix_(late,inputs)],np.stack([left[owners[q]] for q in inputs]))
                delivery.update(zip((owners[q] for q in late),values))
        received={}
        for h,chart in native.kr.items():
            if not native.H[int(h)]<=native.orth[j]:continue
            for kind,ins,outs in chart['stripes']:
                if kind!='Y':continue
                select=[q for q,u in enumerate(ins) if u in delivery]
                if select:
                    values=native.ops.matmul(native.V[len(ins)][select].T,np.stack([delivery[ins[q]] for q in select]))
                    received.update(zip(outs,values))
        outputs=[];zero=np.zeros(width,dtype=np.uint8)
        for i in sorted(native.orth[j]&set(range(111))):
            _,_,ys,CY=facets[i];samples=np.stack([received.get(u,zero) for u in ys]);ids=np.flatnonzero(np.any(samples,axis=1))
            outputs.append(native.ops.matmul(facet_weights[i],native.ops.matmul(CY[:,ids],samples[ids])))
        np.save(cache/f'L{j}.npy',np.array(outputs));np.save(cache/f'IDs{j}.npy',np.array(actual))
