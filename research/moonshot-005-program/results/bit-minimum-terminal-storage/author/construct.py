"""Construct minimum-storage terminal maps on the field and original owners of the K libraries."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError(message)


def payload(path, sha):
    data = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(data).hexdigest() == sha, str(path))
    return data


LAYOUT=('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
        '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
ROUTES=('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
        '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
K_WORDS={'SPREAD':'513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0',
         'MIXED':'8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a'}


def make_field():
    q=1; cycle=[]
    for _ in range(63):
        cycle.append(q)
        q <<= 1
        if q & 64:
            q ^= 67
    require(q==1 and set(cycle)==set(range(1,64)), 'field')
    m=np.zeros((64,64),dtype=np.uint8)
    inv=np.zeros(64,dtype=np.uint8)
    for i,x in enumerate(cycle):
        inv[x]=cycle[-i%63]
        for j,y in enumerate(cycle):
            m[x,y]=cycle[(i+j)%63]
    return m,inv


MUL,INV=make_field()
BIT_WEIGHT=np.array([sum(int(MUL[x,1<<i]).bit_count() for i in range(6)) for x in range(64)])


def product(a,b):
    require(a.shape[1]==b.shape[0], 'matrix shape')
    out=np.zeros((a.shape[0],b.shape[1]),dtype=np.uint8)
    for k in range(a.shape[1]):
        out ^= MUL[a[:,k,None],b[None,k,:]]
    return out


def rref(a, stop=None):
    a=np.array(a,dtype=np.uint8,copy=True)
    r=0;pivots=[]
    for c in range(a.shape[1] if stop is None else stop):
        if r==a.shape[0]:
            break
        choices=np.flatnonzero(a[r:,c])
        if not choices.size:
            continue
        q=r+choices[0]
        a[[q,r]]=a[[r,q]]
        a[r]=MUL[INV[a[r,c]],a[r]]
        scales=a[:,c].copy()
        scales[r]=0
        a ^= MUL[scales[:,None],a[r:r+1,:]]
        pivots.append(c)
        r+=1
    return a,pivots


def invmat(a):
    n=a.shape[0]
    z,piv=rref(np.concatenate((a,np.eye(n,dtype=np.uint8)),axis=1),n)
    require(len(piv)==n,'invertible chosen K output rows')
    return z[:,n:]


def fullrank(a):
    return len(rref(a)[1])==min(a.shape)


def kernel_line(a):
    z,piv=rref(a)
    if len(piv)!=a.shape[0]:
        return None
    free=list(set(range(a.shape[1]))-set(piv))
    require(len(free)==1,'one-dimensional quotient')
    v=np.zeros((a.shape[1],1),dtype=np.uint8)
    v[free[0]]=1
    for i,c in enumerate(piv):
        v[c]=z[i,free[0]]
    return v


def base_data(root):
    base=root/'research/moonshot-005-program/results'
    geo=json.loads(payload(base/LAYOUT[0],LAYOUT[1]))
    raw=payload(base/ROUTES[0],ROUTES[1])
    by_k=defaultdict(dict)
    for line in raw.splitlines():
        p,j,c,h,d,k,fl,i=json.loads(line)
        if k is not None:
            fid=(53280 if p=='Y' else 0)+480*j+c
            by_k[k][fid]=(p,d,j if p=='Y' else i)
    rootvec=np.array(geo['root_table'],dtype=np.int64)
    ortho=(rootvec@rootvec.T)==0
    return geo,by_k,ortho


def singleton(word, entries, d4, native_donors):
    # Reconstruct the actual 45 late rows of the selected K on its 90 original inputs.
    owners=sorted(entries)
    pos={f:n for n,f in enumerate(owners)}
    transfer=np.zeros((90,90),dtype=np.uint8)
    chosen=[]
    for phase,source,dest in word['stripes']:
        n=len(source);nodes=np.arange(1,n+1,dtype=np.uint8)
        v=np.ones((n,n),dtype=np.uint8)
        for t in range(1,n):
            v[t]=MUL[v[t-1],nodes]
        transfer[np.ix_([pos[f] for f in dest],[pos[f] for f in source])]=v
        if phase=='Y':
            chosen.extend(dest[:2*(n//3)])
    for e,l in word['early_cache_to_late']:
        transfer[pos[l]] ^= transfer[pos[e]]
    chosen=sorted(chosen)
    extra=sorted({f for f,(p,d,i) in entries.items() if p=='Y'}-set(chosen))
    require(len(chosen)==30 and len(extra)==15, 'singleton late owner decomposition')
    rel={}
    for j in native_donors:
        cols=[pos[f] for f,(_,d,i) in entries.items() if j in d4[d]]
        a=transfer[np.ix_([pos[f] for f in chosen],cols)]
        b=transfer[np.ix_([pos[f] for f in extra],cols)]
        rel[j]=product(b,invmat(a))
        require(np.array_equal(product(rel[j],a),b),'literal singleton relation')
    return chosen[:15],chosen[15:],extra,rel


def analyze(i,geo,entries,ortho,mode_words):
    planes=geo['A2']
    planes_i=[k for k,h in enumerate(planes) if i in h]
    neighbors=list(np.flatnonzero(ortho[i,:111]))
    d4=[set(d) for d in geo['D4']]
    eslots=[];lslots=[]; e_labels=[]; l_labels=[]; special=None
    for k in planes_i:
        rows=entries[k]
        early=sorted(f for f,(p,d,r) in rows.items() if p=='X' and r==i)
        late=sorted(f for f,(p,d,r) in rows.items() if p=='Y' and r==i)
        if early:
            require(len(early)==15 and len(late)==15,'two-wave receiver')
            eslots.append(early);e_labels.append(k)
        if len(late)==45:
            donors=[j for j in neighbors if ortho[j,planes[k]].all()]
            x,y,z,relations=singleton(mode_words[str(k)],rows,d4,donors)
            special=(k,len(lslots),relations)
            lslots += [x,y,z];l_labels += [k]*3
        else:
            require(len(late) in (15,30),'regular K width')
            for u in range(0,len(late),15):
                lslots.append(late[u:u+15]);l_labels.append(k)
    require(len(planes_i)==28 and len(lslots)==32 and len(eslots) in (24,25),'terminal totals')
    require(len({f for slab in eslots for f in slab})==15*len(eslots) and
            {f for slab in lslots for f in slab}==set(range(53280+i*480,53280+(i+1)*480)),
            'original terminal owner binding')
    views=[]
    for j in neighbors:
        seen={k for k in planes_i if ortho[j,planes[k]].all()}
        require(len(seen)==16,'actual supporting Ks')
        ev=[p for p,k in enumerate(e_labels) if k in seen]
        missing=[p for p,k in enumerate(l_labels) if k not in seen]
        relation=None
        if special is not None and special[0] in seen:
            relation=(special[1],special[2][j])
        require(len(missing)+(relation is not None)==len(ev),'quotient codimension')
        views.append((int(j),missing,ev,relation))
    return eslots,lslots,views


def cauchy(nrow,ncol):
    return INV[np.arange(nrow,dtype=np.uint8)[:,None] ^ np.arange(32,32+ncol,dtype=np.uint8)[None,:]]


def accepts(G,views):
    for j,missing,ev,relation in views:
        N=G[np.ix_(missing,ev)]
        if relation is None:
            if not fullrank(N):
                return False
            continue
        v=kernel_line(N)
        if v is None:
            return False
        start,T=relation
        a,b,c=product(G[np.ix_([start,start+1,start+2],ev)],v).flatten()
        test=MUL[a,T[:,:15]] ^ MUL[b,T[:,15:]] ^ MUL[c,np.eye(15,dtype=np.uint8)]
        if not fullrank(test):
            return False
    return True


def choose(i,ne,views):
    r=max(len(e) for _,_,e,_ in views)
    station=cauchy(r,ne)
    load=cauchy(32,r)
    for trial in range(10000):
        if trial==0:
            w=np.ones(r,dtype=np.uint8)
        else:
            seed=f'moonshot/S029/F/{i}/{trial}'.encode()
            w=np.array([1+b%63 for b in hashlib.shake_256(seed).digest(r)],dtype=np.uint8)
        loaded=MUL[load,w[None,:]]
        if accepts(product(loaded,station),views):
            prices={'INIT':90*r,'dirty_CLEAR':90*r,'capture_ADD':15*int(BIT_WEIGHT[station].sum()),
                    'delivery_ADD':15*int(BIT_WEIGHT[loaded].sum())}
            return w.tolist(),trial+1,prices
    raise ValueError(f'no finite certificate at receiver {i}')


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--repo',required=True,type=Path)
    cli.add_argument('--k-certs',required=True,type=Path)
    cli.add_argument('--out',required=True,type=Path)
    args=cli.parse_args()
    geo,entries,ortho=base_data(args.repo)
    result={'field_modulus':67,'layout_payload':LAYOUT[1],'routes_payload':ROUTES[1],
            'K_owner_payloads':K_WORDS,'new_complete_kappa':False}
    words={}
    for mode in ('SPREAD','MIXED'):
        kw=json.loads(payload(args.k_certs/(mode+'-OWNERS.json.gz'),K_WORDS[mode]))
        records=[];charges=Counter();sizes=Counter();tries=Counter();hist=Counter(); special=0
        for i in range(111):
            es,ls,views=analyze(i,geo,entries,ortho,kw)
            w,t,p=choose(i,len(es),views)
            records.append([i,w])
            charges.update(p);sizes[15*len(w)]+=1;tries[t]+=1
            hist.update(len(ev)*15 for j,missing,ev,rel in views)
            special+=sum(rel is not None for _,_,_,rel in views)
        charges['total_ADD']=charges['capture_ADD']+charges['delivery_ADD']
        words[mode]=records
        result[mode]={'receiver_count':111,'foreign_pairs':sum(hist.values()), 'supported_singleton_pairs':special,
                      'minimum_cache_histogram':dict(sizes),'individual_deficit_histogram':dict(hist),
                      'allocated_fields_bank480':sum(r*n for r,n in sizes.items()),'longest_selector':max(tries),
                      'bank480':dict(charges),'bank3840':{k:8*v for k,v in charges.items()},
                      'pure_F_inverse_ADD':0,'extra_MOVE':0}
    args.out.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(words,separators=(',',':')).encode()
    (args.out/'WORDS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    result['words_payload']=hashlib.sha256(raw).hexdigest()
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
