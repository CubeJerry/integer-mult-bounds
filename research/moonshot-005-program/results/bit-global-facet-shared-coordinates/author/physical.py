"""Generate proper blocks and actual preterminal early responses of the pinned native word."""
from pathlib import Path
import numpy as np


def prepare(native, cache):
    cache.mkdir(parents=True,exist_ok=True)
    neighbours={i:sorted(native.orth[i]&set(range(111))) for i in range(111)}
    facets={i:native.facet(i) for i in neighbours}
    Efiles={};Bfiles={}
    for i,js in neighbours.items():
        early_ids=facets[i][0]
        Efiles[i]=np.lib.format.open_memmap(cache/f'E{i}.npy',mode='w+',shape=(len(js),len(early_ids),480),dtype=np.uint8)
        Bfiles[i]=np.lib.format.open_memmap(cache/f'B{i}.npy',mode='w+',shape=(len(js),480,480),dtype=np.uint8)
    middle={d:native.middle_matrix(d) for d in range(len(native.D))}
    active=[int(h) for h in native.kr]
    zero=np.zeros(480,dtype=np.uint8)
    for j in range(111):
        left=native.left(j);delivery={}
        for d,(word,owners) in middle.items():
            if j not in native.D[d]:
                continue
            slots=[t for t,u in enumerate(owners) if u in left]
            if len(slots)!=8:
                raise ValueError('eight true D entrance fields')
            outputs=native.ops.matmul(word[:,slots],np.stack([left[owners[t]] for t in slots]))
            delivery.update(zip(owners,outputs))
        received={}
        for h in active:
            if not native.H[h]<=native.orth[j]:
                continue
            chart=native.kr[str(h)]
            for _,inputs,outputs in chart['stripes']:
                places=[t for t,u in enumerate(inputs) if u in delivery]
                rows=native.ops.matmul(native.V[len(inputs)][places].T,np.stack([delivery[inputs[t]] for t in places]))
                received.update(zip(outputs,rows))
            for early,late in chart['early_cache_to_late']:
                received[late]^=received[early]
        for i in neighbours[j]:
            e,CE,y,CY=facets[i]
            E=np.array([received.get(u,zero) for u in e]);Y=np.array([received.get(u,zero) for u in y])
            erows=np.flatnonzero(np.any(E,axis=1));yrows=np.flatnonzero(np.any(Y,axis=1))
            B=native.ops.matmul(CE[:,erows],E[erows])^native.ops.matmul(CY[:,yrows],Y[yrows])
            slot=neighbours[i].index(j)
            Efiles[i][slot]=E;Bfiles[i][slot]=B
    for files in (Efiles,Bfiles):
        for array in files.values():
            array.flush()
