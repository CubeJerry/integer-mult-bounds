"""Direct reconstruction of K words on original owners. Requires NumPy."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_pin(path, digest):
    data = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(data).hexdigest() == digest, f'payload hash: {path}')
    return data


def field():
    # Enumerate powers of the residue z. Its complete 63-cycle verifies this
    # representation is a field and z is primitive.
    powers = []
    z = 1
    for _ in range(63):
        powers.append(z)
        z *= 2
        if z >= 64:
            z ^= 67
    require(set(powers) == set(range(1, 64)) and z == 1, 'primitive orbit')
    table = np.zeros((64, 64), dtype=np.uint8)
    inverse = np.zeros(64, dtype=np.uint8)
    for i, a in enumerate(powers):
        inverse[a] = powers[-i % 63]
        for j, b in enumerate(powers):
            table[a, b] = powers[(i + j) % 63]
    return table, inverse


PRODUCT, INVERSE = field()
BASIS = np.array([1, 2, 4, 8, 16, 32], dtype=np.uint8)
BIT_COST = [sum(int(x).bit_count() for x in PRODUCT[a, BASIS]) for a in range(64)]


LAYOUT = ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
          '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
ROUTES = ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
          '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
SPREAD = ('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz',
          '7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab')
CERTS = {'SPREAD-OWNERS.json.gz': '513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0',
         'MIXED-OWNERS.json.gz': '8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a',
         'TEMPLATES.json.gz': '6691b46a45b253e1e48f073f2114aed0c817e786b7efe7dce3dfa440c01cc73d'}
SIZES = (9,36,45)
TEMPLATE = {}
for n in SIZES:
    vals = np.arange(1,n+1,dtype=np.uint8)
    v = np.ones((n,n),dtype=np.uint8)
    for a in range(1,n):
        v[a] = PRODUCT[v[a-1],vals]
    TEMPLATE[n]=v


def literal_templates(words):
    for n in SIZES:
        encoded = words[str(n)]
        identity = [1<<i for i in range(6*n)]
        result = identity[:]
        for dst,src in encoded:
            require(0<=dst<6*n and 0<=src<6*n and dst!=src, 'ADD label')
            result[dst] ^= result[src]
        for p in range(n):
            for t in range(n):
                for b in range(6):
                    actual = sum(((result[6*p+c] >> (6*t+b)) & 1) << c for c in range(6))
                    require(actual==PRODUCT[TEMPLATE[n][p,t],1<<b], 'all-column Vandermonde transpose')
        for dst,src in reversed(encoded):
            result[dst] ^= result[src]
        require(result==identity,'exact inverse')


def all_full_columns(matrices):
    arr=np.array(matrices,dtype=np.uint8,copy=True)
    batches,h,w=arr.shape
    require(h>=w,'wide column-rank test')
    indices=np.arange(batches)
    valid=np.ones(batches,dtype=bool)
    for col in range(w):
        exists=arr[:,col:,col]!=0
        valid &= np.any(exists,axis=1)
        pivot=col+np.argmax(exists,axis=1)
        arr[indices,col],arr[indices,pivot]=arr[indices,pivot].copy(),arr[indices,col].copy()
        unit=PRODUCT[INVERSE[arr[:,col,col]][:,None],arr[:,col,col:]]
        arr[:,col+1:,col:] ^= PRODUCT[arr[:,col+1:,col,None],unit[:,None,:]]
    return valid


def geometry(layout, data):
    roots=np.array(layout['root_table'],dtype=np.int64)
    perp=(roots @ roots.T)==0
    planes=[set(h) for h in layout['A2']]
    d4=[set(d) for d in layout['D4']]
    dperp=[set(np.flatnonzero(np.all(perp[np.array(sorted(d)),:],axis=0))) for d in d4]
    natives={k:sorted(h.intersection(range(111))) for k,h in enumerate(planes)}
    donors={k:list(np.flatnonzero(np.all(perp[np.array(sorted(h)),:111],axis=0))) for k,h in enumerate(planes)}
    sites=defaultdict(dict)
    ids=set()
    for line in data.splitlines():
        phase,j,col,h,d,k,fl,term=json.loads(line)
        require(phase in ('X','Y') and j in range(111) and col in range(480), 'original index')
        f=(53280 if phase=='Y' else 0)+480*j+col
        require(f not in ids,'reused owner')
        ids.add(f)
        if k is not None:
            require(planes[k] <= dperp[d], 'physical K input from wrong D')
            sites[k][f]=(phase,d,term if phase=='X' else j)
    require(len(ids)==2*111*480,'complete atlas')
    for k,entries in sites.items():
        require(len(entries)==90 and set(Counter(d for p,d,t in entries.values()).values())=={2},
                'K receives precisely two owners on every D flag')
    return sites, natives, donors, d4


def permute_swaps(target):
    require(set(target)==set(target.values()), 'phase owner bijection')
    values={i:i for i in target}
    locations=values.copy()
    swaps=0
    for initial,final in sorted(target.items(),key=lambda x:x[1]):
        if values[final]==initial:
            continue
        here=locations[initial]
        displaced=values[final]
        values[final],values[here]=values[here],values[final]
        locations[initial],locations[displaced]=final,here
        swaps+=1
    require(all(values[dest]==src for src,dest in target.items()), 'terminal permutation replay')
    return swaps


def reconstruct(encoded, owners, native, mode, marked, templates):
    ordered=sorted(owners)
    slot={f:t for t,f in enumerate(ordered)}
    phase={p:{f for f,r in owners.items() if r[0]==p} for p in ('X','Y')}
    matrix=np.zeros((90,90),dtype=np.uint8)
    used_in=set()
    used_out=set()
    selected=defaultdict(set)
    charge=Counter()
    perms={'X':{},'Y':{}}
    for p,source,dest in encoded['stripes']:
        n=len(source)
        require(len(dest)==n and n in SIZES and (mode=='MIXED')==(n==45),'stripe type')
        require(len(set(source))==n and len(set(dest))==n and set(source)<=phase[p] and set(dest)<=phase[p],
                'physical stripe input/output owners')
        require(not used_in.intersection(source) and not used_out.intersection(dest),'overlapping stripes')
        used_in.update(source)
        used_out.update(dest)
        ds=[owners[f][1] for f in source]
        require(ds==sorted(set(ds)) and (mode=='MIXED' or all((d in marked)==(n==9) for d in ds)),
                'native D order and component')
        perms[p].update(zip(source,dest))
        matrix[np.ix_([slot[f] for f in dest],[slot[f] for f in source])]=TEMPLATE[n]
        charge['template_forward_ADD']+=len(templates[str(n)])
        for t,f in enumerate(dest):
            i=owners[f][2]
            if i in native and (len(native)!=1 or t<2*(n//3)):
                selected[i].add(f)
    require(used_in==used_out==set(ordered), 'chart coverage')
    cache=encoded['early_cache_to_late']
    require(len({e for e,l in cache})==len({l for e,l in cache})==len(cache), 'single-use snapshot pairing')
    for e,l in cache:
        require(e in phase['X'] and l in phase['Y'],'snapshot order')
        matrix[slot[l]] ^= matrix[slot[e]]
    rr=np.array([slot[f] for f in sorted(phase['X'])],dtype=int)
    ll=np.array([slot[f] for f in sorted(phase['Y'])],dtype=int)
    require(not np.any(matrix[np.ix_(rr,ll)]),'late-before-early')
    for v in perms.values():
        charge['permutation_forward_ADD']+=18*permute_swaps(v)
    charge['pure_inverse_ADD']=charge['template_forward_ADD']+charge['permutation_forward_ADD']
    for label in ('INIT','dirty_CLEAR','snapshot_write_ADD','snapshot_read_ADD'):
        charge[label]=6*len(cache)
    require(all(len(values)==30 for values in selected.values()), 'common terminal 30-subtuple')
    return matrix,slot,selected,charge


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--certs',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    base=args.repo/'research/moonshot-005-program/results'
    layout=json.loads(read_pin(base/LAYOUT[0],LAYOUT[1]))
    marked=set(json.loads(read_pin(base/SPREAD[0],SPREAD[1]))['selected_D'])
    sites,native,donors,d4=geometry(layout,read_pin(base/ROUTES[0],ROUTES[1]))
    templates=json.loads(read_pin(args.certs/'TEMPLATES.json.gz',CERTS['TEMPLATES.json.gz']))
    literal_templates(templates)
    result={}
    for mode in ('SPREAD','MIXED'):
        fname=mode+'-OWNERS.json.gz'
        words=json.loads(read_pin(args.certs/fname,CERTS[fname]))
        require(set(map(int,words))=={k for k,ns in native.items() if ns},'all nonempty K, only nonempty K')
        charges,cachehist,counts=Counter(),Counter(),Counter()
        controls={}
        for k in range(len(native)):
            receivers=native[k]
            entries=sites[k]
            if not receivers:
                require(len(entries)==90 and all(p=='X' for p,d,r in entries.values()), 'empty K passthrough')
                cachehist[0]+=1
                continue
            encoded=words[str(k)]
            matrix,slot,selected,price=reconstruct(encoded,entries,receivers,mode,marked,templates)
            charges.update(price)
            cachehist[len(encoded['early_cache_to_late'])]+=1
            inputs=np.array([[slot[owner] for owner,(_,d,out) in sorted(entries.items()) if j in d4[d]]
                             for j in donors[k]])
            require(inputs.shape==(len(donors[k]),30),'donor support')
            for i in receivers:
                rows=sorted(slot[f] for f in selected[i])
                all_rows=[slot[f] for f,(_,d,out) in entries.items() if out==i]
                tr=matrix[np.array(rows)[None,:,None],inputs[:,None,:]]
                require(np.all(all_full_columns(tr)),f'native rank loss K{k}/{i}')
                counts['native_triples']+=len(inputs)
                counts[f'actual_terminal_{len(all_rows)}']+=len(inputs)
                if len(receivers)<3 and 'remove_cache_rank_loss_K' not in controls:
                    early=np.array([slot[f] for f,(p,d,out) in entries.items() if p=='X'])
                    late=np.array([slot[f] for f,(p,d,out) in entries.items() if p=='Y'])
                    if set(rows)<=set(late):
                        broken=matrix.copy()
                        broken[np.ix_(late,early)]=0
                        bad=broken[np.array(all_rows)[None,:,None],inputs[:,None,:]]
                        require(not np.any(all_full_columns(bad)),'all-late terminal needs retained early information')
                        controls['remove_cache_rank_loss_K']=k
                        controls['remove_cache_receiver']=i
                        controls['native_donors_rejected_without_cache']=len(inputs)
            if k==370:
                bad=matrix.copy()
                col=inputs[0,0]
                bad[:,col]=0
                i=receivers[0]
                rows=sorted(slot[f] for f in selected[i])
                require(not bool(all_full_columns(bad[np.ix_(rows,inputs[0])][None,:,:])[0]),'dropped K370 input')
                controls['omitted_K370_input_detected']=True
        charges['total_ADD']=sum(v for k,v in charges.items() if k.endswith('_ADD'))
        require(counts['native_triples']==103520,'native triple total')
        result[mode]={'coverage':dict(counts),'chart_snapshot_histogram':dict(sorted(cachehist.items())),
                      'bank480_cost':dict(charges),'bank3840_cost':{k:8*v for k,v in charges.items()},
                      'controls':controls}
    result['template_bit_columns']=sum(6*n for n in SIZES)
    result['source_pins']={k:v for k,v in [LAYOUT,ROUTES,SPREAD,*CERTS.items()]}
    result['new_complete_kappa']=False
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
