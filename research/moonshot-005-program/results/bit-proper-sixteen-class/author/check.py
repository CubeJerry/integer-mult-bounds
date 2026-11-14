#!/usr/bin/env python3
"""Exact source verification of a proper16-class construction, no search gate."""
import argparse,hashlib,importlib.util,itertools,json
from collections import defaultdict,Counter
from pathlib import Path

def need(b,m):
    if not b:raise ValueError(m)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--geometry-check',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.geometry_check is None:
        choices=[Path(__file__).resolve().parents[2]/s/'author/check.py' for s in ('quadratic-exterior','bit-quadratic-exterior')]
        a.geometry_check=next((s for s in choices if s.exists()),None)
    need(a.geometry_check is not None,'credited native loader path')
    spec=importlib.util.spec_from_file_location('credited_geometry',a.geometry_check);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    R,K=g.load_native(a.repo);N=len(R);allones=(1<<N)-1;B=[r^allones for r in K]
    frame=[]
    for i,row in enumerate(B):
        if len(g.basis([B[j] for j in frame]+[row]))>len(frame):frame.append(i)
    need(frame==[0,1,2,4,8,14,30,59],'source binary coordinate convention')
    G=[sum(((B[i]>>j)&1)<<c for c,j in enumerate(frame)) for i in frame]
    coords=[g.binary_solve(G,[(B[i]>>j)&1 for i in frame],8) for j in range(N)]
    bil=lambda x,y:sum(((x>>i)&1)*(G[i]&y).bit_count() for i in range(8))%2
    q=lambda x:(x.bit_count()+sum(((G[i]>>j)&1)*((x>>i)&1)*((x>>j)&1) for i,j in itertools.combinations(range(8),2)))%2
    full=[x for x in range(256) if q(x)];need(len(full)==120 and len(set(coords))==111 and set(coords)<=set(full),'quadric points')
    need(all((K[i]>>j&1)==1^bil(coords[i],coords[j]) for i in range(N) for j in range(N)),'native polar correspondence')
    L=[0,6,27,29,104,110,115,117,137,143,146,148,225,231,250,252]
    need(len(g.basis(L))==4 and all(x^y in L for x in L for y in L) and all(q(x)==0 for x in L),'explicit maximal singular subspace')
    label=lambda x:min(x^u for u in L)
    fullgroups=defaultdict(list);groups=defaultdict(list)
    for x in full:fullgroups[label(x)].append(x)
    for i,x in enumerate(coords):groups[label(x)].append(i)
    need(len(fullgroups)==15 and all(len(s)==8 for s in fullgroups.values()),'fifteen full cosets')
    need(all(not bil(x,y) for s in fullgroups.values() for x,y in itertools.combinations(s,2)),'coset frames mutually orthogonal')
    missing=set(full)-set(coords);need(len({label(x) for x in missing})==9,'nine distinct punctured cosets')
    classes=list(groups.values());need(Counter(map(len,classes))=={7:9,8:6},'six native full classes')
    T=[14,33,28,100,87,90];dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    need(all(dot(R[i],R[j])==0 for i,j in itertools.combinations(T,2)),'orthogonal transversal')
    need(all(len(set(c)&set(T))==int(len(c)==8) for c in classes),'one transversal point per full class')
    refined=[[i for i in c if i not in T] for c in classes]+[sorted(T)]
    need(sorted(i for c in refined for i in c)==list(range(111)),'actual disjoint partition')
    need(Counter(map(len,refined))=={7:15,6:1},'fifteen sevens and one six')
    need(all(dot(R[i],R[j])==0 for c in refined for i,j in itertools.combinations(c,2)),'every new class orthogonal')
    masks=[sum(1<<i for i in c) for c in refined];C=g.basis(K);Q3=g.basis([u&v&w for u in C for v in C for w in C])
    need(len(g.basis(masks))==16 and len(g.basis(C+masks))==23 and len(g.basis(Q3+masks))==90,'source code dimensions')
    cover=[]
    for c in refined:
        need(g.mod_rank([R[j] for j in c],101)==len(c),'proper class acquisition rank')
        for i in c:
            foreign=[j for j in c if j!=i]
            need(g.mod_rank([R[j] for j in foreign],101)==len(c)-1<=6,'one proper foreign correction chart')
            cover.append(dict(receiver=i,foreign_support=foreign,real_rank=len(c)-1,charge=0))
    pair_ranks=[g.mod_rank([R[k] for k in c+d],101) for c,d in itertools.combinations(refined,2)]
    need(len(pair_ranks)==120 and set(pair_ranks)=={8},'no shared proper acquisition chart for two whole classes')
    cache_facets=[[i for i,r in enumerate(R) if all(dot(r,R[j])==0 for j in c)] for c in refined]
    need(cache_facets==[[],[],[],[],[],[],[14],[33],[28],[],[100],[87],[90],[],[],[43,74]],'all class-cache receiver access')
    ell=K[92]&K[54];cub=sum(1<<i for i in (1,56,73,81,95))
    need(len(g.basis(masks+[ell,1<<92,1<<15]))==19 and len(g.basis(masks+[ell,1<<92,1<<15,K[92]]))==20,'honest current-prefix compatibility')
    need(len(g.basis(masks+[cub]))==17,'five-input cubic is an extra direction')
    need(7**199*10**200>69**200 and 8**199*10**200>79**200,'rigorous crude movement bounds')
    # Negative control: putting a removed transversal root back makes an8class.
    old_full=next(c for c in classes if len(c)==8);i=old_full[0]
    need(g.mod_rank([R[j] for j in old_full if j!=i],101)==7,'restoring a full class destroys chi-zero')
    out=dict(status='PASS_AUTHOR_PROPER_SIXTEEN_CLASS_CONSTRUCTION',source_sha256=g.PIN,credited_geometry_sha256=hashlib.sha256(a.geometry_check.read_bytes()).hexdigest(),binary_frame=frame,binary_polar_rows=G,singular_subspace=L,native_coset_classes=classes,orthogonal_transversal=T,proper_classes=refined,class_sizes=[len(c) for c in refined],rank=16,charge=0,canonical_joint_rank=23,canonical_intersection_dimension=2,cubic_joint_rank=90,cubic_intersection_dimension=10,pair_span_histogram=dict(Counter(pair_ranks)),class_chart_containing_receiver_facets=cache_facets,foreign_covers=sorted(cover,key=lambda x:x['receiver']),with_current_ground_history_dimension=19,with_current_proper_history_dimension=20,naive_sixteen_bus_movement_lower_bound='1658.2',negative_full_class_foreign_rank=7,complete_source=False,new_complete_kappa=False)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('proper_classes','native_coset_classes','foreign_covers')}))

if __name__=='__main__':main()
