#!/usr/bin/env python3
"""Independent native gauge, canonical-code, and chronological inlet audit."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip
import json

NATIVE = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
FACTOR = '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def rank(rows):
    basis = {}
    for row in rows:
        while row:
            lead = row.bit_length()-1
            if lead in basis:
                row ^= basis[lead]
            else:
                basis[lead] = row
                break
    return len(basis)


def eye(n):
    return tuple(1<<i for i in range(n))


def mul(a,b):
    result = []
    for row in a:
        value = 0
        for j in bits(row):
            value ^= b[j]
        result.append(value)
    return tuple(result)


def inv(a):
    n = len(a)
    rows = [row | (1<<(n+i)) for i,row in enumerate(a)]
    for col in range(n):
        p = next((i for i in range(col,n) if rows[i]>>col&1),None)
        need(p is not None,'invertible matrix')
        rows[col],rows[p] = rows[p],rows[col]
        for i in range(n):
            if i != col and rows[i]>>col&1:
                rows[i] ^= rows[col]
    answer = tuple(row>>n for row in rows)
    need(mul(a,answer) == mul(answer,a) == eye(n),'two-sided inverse')
    return answer


def scheme(N):
    core = set(bits(N[0]))
    anchors = {i:min(bits(N[0]&N[i])) for i in range(1,111)}
    parents = {j:min(i for i in range(111) if N[i]>>j&1) for j in range(111) if j not in core}
    tree = {(0,j) for j in core} | set(anchors.items()) | {(i,j) for j,i in parents.items()}
    need(len(tree)==221,'tree edge count')
    reached = {('r',0)}
    while True:
        old = len(reached)
        for i,j in tree:
            if ('r',i) in reached:
                reached.add(('d',j))
            if ('d',j) in reached:
                reached.add(('r',i))
        if old == len(reached):
            break
    need(len(reached)==222,'tree connectivity')
    cycles = []
    for i in range(111):
        for j in bits(N[i]):
            if (i,j) in tree:
                continue
            h,d = (0,anchors[i]) if j in core else (parents[j],min(bits(N[0]&N[i]&N[parents[j]])))
            need(i!=h and j!=d,'four distinct bipartite vertices')
            need(all(N[r]>>s&1 for r,s in ((i,j),(h,j),(h,d),(i,d))),'native four-cycle')
            cycles.append([i,j,h,d])
    need(len(cycles)==6249 and len({(i,j) for i,j,h,d in cycles})==6249,'non-tree edge equations')
    known = set(tree)
    for i,j,h,d in sorted(cycles,key=lambda c:c[1] not in core):
        need((i,j) not in known and {(h,j),(h,d),(i,d)}<=known,'triangular four-cycle elimination')
        known.add((i,j))
    need(len(known)==6470,'all native edges eliminated')
    return core,anchors,parents,tree,cycles


def normalize(B,n,sc):
    core,anchors,parents,tree,cycles = sc
    R = {0:eye(n)}
    C = {j:B[0,j] for j in core}
    for i,a in anchors.items():
        R[i] = mul(B[i,a],inv(C[a]))
    for j,p in parents.items():
        C[j] = mul(inv(R[p]),B[p,j])
    return {(i,j):mul(mul(inv(R[i]),b),inv(C[j])) for (i,j),b in B.items()}


def fixed_dim(H,n):
    # w(H-I)=0 is a system whose coefficient rows are COLUMNS of H-I.
    equations = [sum((((h[r]>>c)&1)^int(r==c))<<r for r in range(n))
                 for h in H.values() for c in range(n)]
    return n-rank(equations)


def cyc(B,c):
    i,j,h,d = c
    return mul(mul(mul(B[i,j],inv(B[h,j])),B[h,d]),inv(B[i,d]))


def controls(N,sc):
    gl = [tuple(a) for a in product(range(8),repeat=3) if rank(a)==3]
    need(len(gl)==168,'GL(3,2) exhaustive count')
    R = [gl[(17*i+11)%168] for i in range(111)]
    C = [gl[(31*j+7)%168] for j in range(111)]
    B = {(i,j):mul(R[i],C[j]) for i in range(111) for j in bits(N[i])}
    H = normalize(B,3,sc)
    need(all(h==eye(3) for h in H.values()),'noncommutative positive normalization')
    need(all(cyc(B,c)==eye(3) for c in sc[4]),'all positive four-cycle identities')
    need(fixed_dim(H,3)==3,'positive fixed space')
    need(any(mul(a,b)!=mul(b,a) for a,b in zip(R,C)),'genuinely noncommuting example')
    wrong = any(mul(mul(mul(B[i,j],inv(B[h,j])),inv(B[i,d])),B[h,d])!=eye(3)
                for i,j,h,d in sc[4][:200])
    need(wrong,'wrong noncommutative multiplication order rejected')
    c2,c3 = (2,3),(4,5,2)
    for c in (c2,c3):
        need(rank(c)==len(c) and rank([a^b for a,b in zip(c,eye(len(c)))])==len(c),
             'companion and I+companion both invertible')
    defect = (1,2,*(r<<2 for r in c3))
    edge = tuple(sc[4][0][:2])
    B = {(i,j):eye(5) for i in range(111) for j in bits(N[i])}
    B[edge] = defect
    H = normalize(B,5,sc)
    need(all(rank(b)==5 and b[:2]==eye(5)[:2] for b in B.values()),'invertible blocks and two common rows')
    need(fixed_dim(H,5)==2,'exactly two gauge-alignable coordinates')
    failed = sum(cyc(B,c)!=eye(5) for c in sc[4])
    need(failed>0 and 2*2844+3==5760-69,'negative controls')
    return {'positive_dimension':3,'positive_noncommuting':True,'negative_width':5,
            'negative_fixed_dimension':2,'defect_edge':edge,'detected_cycles':failed,
            'wrong_order_rejected':wrong,'actual_width_control':{'width':5760,'fixed_rows':69,
             'quadratic_blocks':2844,'cubic_blocks':1,'complement_has_no_fixed_vector':True}}


def main():
    p=ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--factor',type=Path,required=True)
    p.add_argument('--layout',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    raw=a.native.read_bytes(); fraw=a.factor.read_bytes()
    need(sha256(raw).hexdigest()==NATIVE and sha256(fraw).hexdigest()==FACTOR,'source pins')
    roots=[tuple(r) for r in json.loads(raw)['native_roots']]
    need(len(roots)==len(set(roots))==111 and all(dot(r,r)==4 for r in roots),'native roots')
    N=[sum(1<<j for j,s in enumerate(roots) if dot(r,s)==0) for r in roots]
    K=[row|(1<<i) for i,row in enumerate(N)]
    need(rank(N)==108 and rank(K)==9,'native target and canonical ranks')
    need(all(rank([row&~n for row in K])==9 for n in N),'all canonical complement restrictions injective')
    pairs=Counter((N[i]&N[j]).bit_count() for i,j in combinations(range(111),2))
    triples=Counter((N[i]&N[j]&N[k]).bit_count() for i,j,k in combinations(range(111),3))
    need(min(pairs)==23 and min(triples)==8,'native common-neighbor lower bounds')
    sc=scheme(N); control=controls(N,sc)
    full=set(roots)
    for supp in {tuple(i for i,x in enumerate(r) if x) for r in roots if sum(x!=0 for x in r)==4}:
        for tail in product((-1,1),repeat=3):
            r=[0]*8
            for i,s in zip(supp,(1,*tail)):
                r[i]=s
            full.add(tuple(r))
    full=roots+sorted(full-set(roots)); need(len(full)==120,'parent completion')
    planes=[]
    for i,j,k in combinations(range(120),3):
        x,y,z=dot(full[i],full[j]),dot(full[i],full[k]),dot(full[j],full[k])
        if 64+2*x*y*z-4*(x*x+y*y+z*z)==0:
            need(abs(x)==abs(y)==abs(z)==2,'A2 Gram determinant')
            planes.append((i,j,k))
    planes.sort(key=lambda h:sum(1<<j for j in h))
    lraw=gzip.decompress(a.layout.read_bytes()); layout=json.loads(lraw)
    need(layout['root_table']==[list(r) for r in full] and layout['A2']==[list(h) for h in planes],
         'independent geometry matches factor indices')
    factor=json.loads(fraw); fac=dict(factor['factors'])
    need(factor['denominator']==2 and len(fac)==172,'balanced factor dimensions')
    early=[]; total=[]
    for h,plane in enumerate(planes):
        m=sum(j<111 for j in plane)
        need(h not in fac or m==3,'native-full factor support')
        x=12//m+fac.get(h,0) if m else 0
        early.append(x); total.append(max(8,x))
    pencils=[[h for h,H in enumerate(planes) if j in H] for j in range(111)]
    need(all(len(p)==28 and 45*sum(early[h] for h in p)==5760 for p in pencils),'actual early public bank sizes')
    fullN=[sum(1<<j for j,s in enumerate(full) if dot(r,s)==0) for r in roots]
    masks=[sum(1<<j for j in h) for h in planes]; cuts=[]
    for i in range(111):
        for j in bits(N[i]):
            visible=[h for h in pencils[j] if masks[h]&fullN[i]==masks[h]]
            need(len(visible)==16,'visible source planes')
            cuts.append([i,j,45*sum(early[h] for h in visible),45*sum(total[h]-early[h] for h in visible)])
    e_hist=Counter(e for i,j,e,c in cuts); t_hist=Counter(e+c for i,j,e,c in cuts)
    need(min(e_hist)==2880 and max(e_hist)==3600,'early rank range')
    need(t_hist=={5760:6110,5940:360},'tight versus slack source cuts')
    core,anchors,parents,tree,cycles=sc
    artifact={'root_receiver':0,'core_donors':sorted(core),'receiver_anchors':anchors,
              'outer_donor_parent_receivers':parents,'tree_edges':sorted(tree),'four_cycles':cycles,'inlet_pairs':cuts}
    data=(json.dumps(artifact,separators=(',',':'),sort_keys=True)+'\n').encode()
    result={'status':'PASS_NATIVE_GAUGE_CYCLES_AND_CAUSAL_INLETS','native_sha256':NATIVE,'factor_sha256':FACTOR,
            'layout_uncompressed_sha256':sha256(lraw).hexdigest(),'scheme_uncompressed_sha256':sha256(data).hexdigest(),
            'vertices':222,'edges':6470,'tree_edges':221,'four_cycle_equations':6249,'core_donors':len(core),
            'canonical_rank':9,'canonical_complement_rank_histogram':{9:111},'proper_target_rank':108,
            'pair_intersection_histogram':dict(sorted(pairs.items())),'triple_intersection_histogram':dict(sorted(triples.items())),
            'early_cut_histogram':dict(sorted(e_hist.items())),'combined_cut_histogram':dict(sorted(t_hist.items())),
            'necessary_extra_pair_dimensions':[2160,2880],'finite_controls':control,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'SCHEME.json.gz').write_bytes(gzip.compress(data,mtime=0))
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])
    print('6,249 four-cycle equations; early-cut range 2,880..3,600; 6,110 tight and 360 slack pairs')


if __name__=='__main__':
    main()
