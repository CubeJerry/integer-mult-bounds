#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json,subprocess,tempfile
def mask(q):return sum(1<<i for i in q)
def bits(z):
    while z:
        e=z&-z;yield e.bit_length()-1;z^=e
def hist(seq):return dict(sorted(Counter(seq).items()))
def rank(rows):
    piv={}
    for x in rows:
        while x and x.bit_length() in piv:x^=piv[x.bit_length()]
        if x:piv[x.bit_length()]=x
    return len(piv)
def input_data(layout,factor):
    raw=gzip.decompress(layout.read_bytes());assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    f=factor.read_bytes();assert sha256(f).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
    w=json.loads(raw);R=w['root_table'];A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));N=(1<<111)-1
    F=[mask(j for j,s in enumerate(R) if sum(a*b for a,b in zip(r,s))==0) for r in R]
    di={d:k for k,d in enumerate(D)};dual=[]
    for d in D:
        e=(1<<120)-1
        for j in bits(d):e&=F[j]
        dual.append(di[e])
    Hd=[[k for k,h in enumerate(A) if h&d==h] for d in D]
    assert all(len(x)==16 for x in Hd) and all(dual[dual[d]]==d for d in range(len(D)))
    assert set(Counter(h for hs in Hd for h in hs).values())=={45}
    f=json.loads(f);adds=dict(f['factors']);assert f['denominator']==2
    n=[(a&N).bit_count() for a in A];he=[(12//m if m else 0)+adds.get(k,0) for k,m in enumerate(n)]
    sy=[max(8-x,0) for x in he];hx=[m*x for m,x in zip(n,he)]
    dx=[sum(hx[h] for h in hs) for hs in Hd]
    assert all(dx[k]+dx[l]>=384 for k,l in enumerate(dual))
    locality=[max(n),max((d&N).bit_count() for d in D),max(sum(h&f==h for f in F[:111]) for h in A),max((x&N).bit_count() for x in F[:111])]
    return A,D,dual,Hd,F,he,sy,hx,locality
def run(layout,factor,cache):
    A,D,dual,Hd,F,he,sy,hx,locality=input_data(layout,factor)
    base=[];picked={};N=(1<<111)-1
    with tempfile.TemporaryDirectory() as temp:
        exe=Path(temp)/'flow'
        subprocess.run(['c++','-std=c++17','-O3',str(Path(__file__).with_name('dinic.cpp')),'-o',str(exe)],check=True)
        for j in range(111):
            n=set(bits(F[j]&N));dg=len(n);p={h for h,q in enumerate(A) if q&(1<<j)}
            assert len(p)==28 and sum(45*he[h] for h in p)==5760
            ids={('source',):0,('sink',):1};edges=[]
            def ix(x,z):
                node=(x,z)
                if node not in ids:ids[node]=len(ids)
                return ids[node]
            def put(u,v,c):
                if c:edges.append((u,v,c))
            ks=set()
            for d,rm in enumerate(D):
                if not rm&(1<<j):continue
                for h in p.intersection(Hd[d]):put(ix('h',h),ix('d',d),24-hx[h])
                for k in Hd[dual[d]]:
                    if hx[k]:put(ix('d',d),ix('k',k),hx[k]);ks.add(k)
            for k in ks:
                for i in set(bits(A[k]))&n:put(ix('k',k),ix('i',i),45*he[k])
            cap=sum(45*sy[h] for h in p)
            bs=max(45*(24-hx[h]-sy[h]) for h in p)
            options=[None]+([h for h in sorted(p) if 45*(24-hx[h]-sy[h])==bs] if cache else [])
            for hc in options:
                avail=cap+(bs if hc is not None else 0);target=avail//dg
                assert hc is None or target<=45*he[hc]
                b=[(0,ix('h',h),45*((24-hx[h]) if h==hc else sy[h])) for h in p]
                b.extend((ix('i',i),1,target) for i in n)
                arcs=edges+[(u,v,c) for u,v,c in b if c]
                case=f'{j} {len(ids)} {len(arcs)} {target}\n'+''.join(f'{u} {v} {c}\n' for u,v,c in arcs)
                x,y,f=map(int,subprocess.check_output([str(exe)],input=case,text=True).split());assert x==j and y==target
                if hc is None:
                    assert f==target*dg;base.append([j,dg,cap,target,f])
                elif f==target*dg:
                    picked[j]=[hc,avail,target,f];break
    if cache:assert len(picked)==111
    O=[f&N for f in F[:111]];K=[o^(1<<i) for i,o in enumerate(O)]
    rank_O,rank_K=rank(O),rank(K);line_visits=sum(row[2] for row in base)
    assert (rank_O,rank_K,line_visits)==(108,9,481500)
    return {'base_histogram':hist(row[3] for row in base),'base_primal_with_source_upper_cut':base,
            'one_plane_cache_witnesses':picked,'one_plane_cache_histogram':hist(v[2] for v in picked.values()),
            'native_max_at_H_D_K_F':locality,'individual_degree_with_site_determinant':max(locality)+1,
            'binary_ranks_O_K':[rank_O,rank_K],'genuine_line_Y_visits':line_visits,
            'extra_fixed_K_linear_transfer_dimension':rank_O*5760-line_visits,
            'extra_arbitrary_K_information_slots':(111-rank_K)*5760-line_visits}
if __name__=='__main__':
    ap=ArgumentParser();ap.add_argument('layout',type=Path);ap.add_argument('factor',type=Path);ap.add_argument('--cache',action='store_true');q=ap.parse_args()
    print(json.dumps(run(q.layout,q.factor,q.cache),indent=2))
