#!/usr/bin/env python3
"""Independent witness enumeration, unsymmetrized Shannon sum and literal source replay."""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

P=Path('research/moonshot-005-program')
ROOTS=P/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
DUAL=P/'sessions/2026-11-17-S019/checkpoint1-evidence/R/PETERSEN-SHORT-DUAL.json'
CASES=[
  (1,P/'sessions/2026-11-17-S020/checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json','a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc',1985,410),
  (2,P/'results/bit-two-copy-field-compiler/author/output/WORD.json','9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550',4010,812),
  (3,P/'results/bit-three-copy-field-compiler/author/output/WORD.json','9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6',6119,1218)]
TAKEN={14,17,19,20,96,99,101,102}
ROLES=sorted(set(range(8,111))-TAKEN)
def require(ok,msg):
    if not ok:raise ValueError(msg)
def load(path,digest):
    data=path.read_bytes();require(hashlib.sha256(data).hexdigest()==digest,'exact dependency '+str(path));return json.loads(data)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def indices(mask):
    while mask:
        low=mask&-mask;yield low.bit_length()-1;mask^=low

def petersen(G, verts):
    # Construct the five size-four stars in KG(5,2); certify the label map
    # and every edge, independently of the enumerator's native role ordering.
    V=list(indices(verts))
    if len(V)!=10 or any((G[i]&verts).bit_count()!=3 for i in V):return None
    stars=[]
    for s in combinations(V,4):
        if all(not (G[i]>>j&1) for i,j in combinations(s,2)):stars.append(set(s))
    if len(stars)!=5:return None
    label=[frozenset(k for k,S in enumerate(stars) if i in S) for i in V]
    if any(len(p)!=2 for p in label) or len(set(label))!=10:return None
    return label if all(bool(G[i]>>j&1)==label[a].isdisjoint(label[b]) for (a,i),(b,j) in combinations(enumerate(V),2)) else None

def enumerate_witnesses(roots):
    graph=[sum(1<<j for j,v in enumerate(roots) if dot(roots[i],v)==0) for i in range(len(roots))]
    mask=sum(1<<i for i in ROLES);nind=0;n10=0;found=[];cores=set();first_graph_control=False
    pairs={(i,j):graph[i]|graph[j] for i,j in combinations(ROLES,2) if not (graph[i]>>j&1)}
    for (i,j),bad in pairs.items():
        rem=mask & ~bad & ~((1<<(j+1))-1)
        for k in indices(rem):
            last=rem & ~graph[k] & ~((1<<(k+1))-1)
            for l in indices(last):
                nind+=1;isolates=(1<<i)|(1<<j)|(1<<k)|(1<<l)
                core=mask&~(bad|graph[k]|graph[l]|isolates)
                if core.bit_count()!=10:continue
                n10+=1;label=petersen(graph,core)
                if label is None:continue
                if not first_graph_control:
                    graph2=graph.copy();u=next(indices(core));v=next(indices(graph[u]&core))
                    graph2[u]^=1<<v;graph2[v]^=1<<u
                    require(petersen(graph2,core) is None,'one Petersen edge deletion must fail')
                    first_graph_control=True
                found.append((isolates,core));cores.add(core)
    require(len(found)==838 and len({I|Q for I,Q in found})==838,'838 distinct induced witnesses')
    serial=''.join(str(I)+' '+str(Q)+'\n' for I,Q in sorted(found))
    return graph,{"independent_four_sets":nind,"ten_common_complement":n10,"certified_witnesses":len(found),
                  "distinct_ten_vertex_cores":len(cores),"native_numeric_mask_pairs_sha256":hashlib.sha256(serial.encode()).hexdigest(),
                  "edge_deletion_rejected":first_graph_control}

def dual(data,omit=-1):
    pairs=list(combinations(range(5),2));require(data['pair_labels']==[list(p) for p in pairs],'pair order')
    neigh=[sum(1<<j for j,q in enumerate(pairs) if set(p).isdisjoint(q))for p in pairs]
    acc=Counter();rhs=Fraction(0)
    for sigma in permutations(range(5)):
        perm=[pairs.index(tuple(sorted([sigma[i],sigma[j]]))) for i,j in pairs]
        transform=lambda S:sum(1<<perm[k] for k in indices(S))
        for idx,t in enumerate(data['terms']):
            if idx==omit:continue
            w=Fraction(t['multiplier'])/120;require(w>0,'positive dual term')
            kind,*z=t['inequality'];L=[]
            if kind=='initialize':L=[(1023,-1)];v=-10
            else:
                s,i,*tail=z;require(not(s>>i&1) and i<10,'first role');u=s|1<<i
                if kind=='slope':L=[(u,1),(s,-1)];v=1
                elif kind=='monotonicity':L=[(u,-1),(s,1)];v=0
                elif kind=='decode':
                    require((s&neigh[i])==neigh[i],'all Petersen neighbors supplied');L=[(u,1),(s,-1)];v=0
                elif kind=='submodularity':
                    j,=tail;require(i!=j and not(s>>j&1),'distinct additional role')
                    h=s|1<<j;L=[(s,1),(u|1<<j,1),(u,-1),(h,-1)];v=0
                else:raise ValueError(kind)
            rhs+=w*v
            for mask,coef in L:acc[transform(mask)]+=coef*w
    return {k:v for k,v in acc.items() if v},rhs

def reduced(rows):
    a=[list(map(Fraction,v)) for v in rows];j=0;piv=[]
    for h in range(8):
        k=next((i for i in range(j,len(a)) if a[i][h]),None)
        if k is None:continue
        a[j],a[k]=a[k],a[j];scale=a[j][h];a[j]=[v/scale for v in a[j]]
        for i,row in enumerate(a):
            if i!=j and row[h]:a[i]=[x-row[h]*y for x,y in zip(row,a[j])]
        j+=1;piv.append(h)
    return tuple(tuple(row) for row in a[:j]),piv

def chart(body):
    rows,piv=reduced(body['rows'])
    if body['kind']=='span':return rows
    require(body['kind']=='ann','chart kind')
    null=[]
    for j in range(8):
        if j in piv:continue
        v=[Fraction(0)]*8;v[j]=1
        for p,r in zip(piv,rows):v[p]=-r[j]
        null.append(v)
    return reduced(null)[0]

def replay(repo,case,roots,graph):
    b,path,pin,cut,expected=case;w=load(repo/path,pin)
    require(w['carrier_interface_before_operation']==cut,'source cut');charts={q:chart(s) for q,s in w['charts'].items()}
    name=lambda c,t,j:(f'C{c}__' if b>1 else '')+t+str(j)
    live={name(c,t,j):[1<<(222*c+k*111+j),'zero' if k else 'L'+str(j)] for c in range(b) for k,t in enumerate('XY') for j in range(111)}
    for op,z,*rest in w['operations'][:cut]:
        if op=='INIT':require(z not in live,'fresh name');live[z]=[0,rest[0]]
        elif op=='MOVE':live[z][1]=rest[0]
        elif op=='ADD':
            require(charts[live[z][1]]==charts[live[rest[0]][1]],'cocharted add')
            live[rest[0]][0]^=live[z][0]
        elif op=='CLEAR':del live[z]
        else:raise ValueError(op)
    require(len(live)==expected,'live count')
    # A small independent directed chart test suffices: B lies inside F_i
    # exactly when each rational generator of B is perpendicular to R_i.
    bychart={}
    for n,(coeff,loc) in live.items():
        role_support=0
        for c in range(b):role_support |= (coeff>>(222*c)) & ((1<<111)-1)
        bychart[loc]=bychart.get(loc,0)|role_support
    U=sum(1<<i for i in ROLES)
    actual={i:0 for i in ROLES};nvis=0
    for loc,s in bychart.items():
        for i in ROLES:
            if all(dot(v,roots[i])==0 for v in charts[loc]):
                nvis+=1;actual[i]|=s&U
    require(all(actual[i]==graph[i]&U for i in ROLES),'actual facet source projection equals native neighbors')
    # Confirm the independent 8b private-arrival premise from literal fields.
    pairs={}
    for i in sorted(TAKEN):
        H=charts[live[name(0,'Y',i)][1]]
        require(len(H)==6,'rank-six private chart');pairs.setdefault(H,[]).append(i)
        require(all(charts[live[name(c,'Y',i)][1]]==H for c in range(b)),'same chart every copy')
    require(len(pairs)==4 and all(len(pair)==2 for pair in pairs.values()),'four private regions')
    for H,pair in pairs.items():
        require([i for i in range(111) if all(dot(v,roots[i])==0 for v in H)]==pair,'two terminal native facets private')
        B={H,charts['F'+str(pair[0])],charts['F'+str(pair[1])]}
        names={n for n,(row,L) in live.items() if charts[L] in B}
        require(names=={name(c,'Y',i) for c in range(b) for i in pair},'only target Ys in private region')
        sub=sum(1<<(222*c+i)for c in range(b)for i in pair)
        require(all((live[n][0]&sub)==0 for n in names),'no private own input')
    return {'b':b,'word_sha256':pin,'cut':cut,'all_original_columns':222*b,'live_fields':len(live),
            'facet_locality_equalities':len(actual),'chart_subset_incidence_checks':len(bychart)*len(ROLES),
            'visible_chart_facet_incidences':nvis,'private_pairs':sorted(pairs.values())}

def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);cfg=a.parse_args()
    r=load(cfg.repo/ROOTS,'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e')['native_roots']
    d=load(cfg.repo/DUAL,'7c0e1e96f41d44a3c989906ad9c08eaa96252799a33a065746048a078e23527d')
    G,W=enumerate_witnesses(r);expected=({0:Fraction(-1)},Fraction(-5));require(dual(d)==expected,'exact unsymmetrized Shannon sum')
    require(dual(d,0)!=expected,'omitted dual term must alter certificate')
    result={'status':'PASS_838_INDUCED_PETERSEN_FAMILIES_AND_NONLINEAR_CAPACITY','witness_geometry':W,
            'dual':{'orbits_used_in_reconstruction':False,'elementary_terms':len(d['terms'])*120,'exact_rhs':'-5',
                    'only_nonzero_entropy_coefficient':'-1 times unspecialized H(transcript)','omission_rejected':True},
            'sources':[replay(cfg.repo,c,r,G) for c in CASES],
            'model':'fixed schedule; deterministic; finite whole-record alphabet; independent uniform input words for proof',
            'private_arrivals':'8b','remaining_downset_descents':'9b','misses_per_W_if_N_equals_9b_plus_s':'at most s',
            'equality':'all 9b payloads jointly uniform conditional on each fixed outside-W input'}
    cfg.out.parent.mkdir(parents=True,exist_ok=True);cfg.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS 838 witnesses, expanded 2,520 Shannon terms and three complete source cuts')
if __name__=='__main__':main()
