#!/usr/bin/env python3
"""Exact native cubic-code constructions; the all-field proof is PROOF.md."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

def need(c,m):
    if not c:raise ValueError(m)

def load_geometry(path):
    spec=importlib.util.spec_from_file_location('credited_native_geometry',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def exterior_ranks(g,m):
    n=2*m;counts=[];previous={}
    for r in range(n+1):
        dom=[sum(1<<i for i in s) for s in itertools.combinations(range(n),r)]
        cod=[sum(1<<i for i in s) for s in itertools.combinations(range(n),r+2)] if r+2<=n else []
        index={s:j for j,s in enumerate(cod)};columns=[]
        for mask in dom:
            column=0
            for j in range(m):
                pair=3<<(2*j)
                if not(mask&pair):column^=1<<index[mask|pair]
            columns.append(column)
        rank=len(g.basis(columns));cohom=len(dom)-rank-previous.get(r-2,0)
        need(cohom==(2**m if r==m else 0),'exterior complex cohomology')
        previous[r]=rank;counts.append(dict(degree=r,dimension=len(dom),rank=rank,cohomology_dimension=cohom))
    return counts

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--geometry-check',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.geometry_check is None:
        candidates=[Path(__file__).resolve().parents[2]/name/'author/check.py' for name in ('quadratic-exterior','bit-quadratic-exterior')]
        a.geometry_check=next((x for x in candidates if x.is_file()),None)
    need(a.geometry_check is not None,'supply credited quadratic geometry checker')
    g=load_geometry(a.geometry_check);R,K=g.load_native(a.repo)
    N=len(K);B=[r^((1<<N)-1) for r in K];frame=[]
    for i,row in enumerate(B):
        if len(g.basis([B[j] for j in frame]+[row]))>len(frame):frame.append(i)
    G=[sum(((B[i]>>j)&1)<<c for c,j in enumerate(frame)) for i in frame]
    coord=[g.binary_solve(G,[(B[i]>>j)&1 for i in frame],8) for j in range(N)]
    bil=lambda x,y:sum(((x>>i)&1)*(G[i]&y).bit_count() for i in range(8))%2
    pairs=list(itertools.combinations(range(8),2))
    quad=lambda x:(x.bit_count()+sum(((G[i]>>j)&1)*((x>>i)&1)*((x>>j)&1) for i,j in pairs))%2
    full=[x for x in range(256) if quad(x)];need(len(full)==120,'full quadric size120')
    # Authenticate the completed real configuration as well as its binary model.
    blocks=sorted({tuple(j for j,x in enumerate(r) if x) for r in R if sum(bool(x) for x in r)==4})
    real_full=[tuple(2*int(a==b) for a in range(8)) for b in range(8)]
    for block in blocks:
        for signs in itertools.product((-1,1),repeat=3):
            rr=[0]*8;rr[block[0]]=1
            for j,s in zip(block[1:],signs):rr[j]=s
            real_full.append(tuple(rr))
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    need(len(set(real_full))==120 and set(R)<=set(real_full),'real completion')
    real_labels=[g.binary_solve(G,[(dot(R[i],r)//2)%2 for i in frame],8) for r in real_full]
    need(set(real_labels)==set(full),'real completion equals full binary quadric')
    need(all(dot(r,s) in (-2,0,2) and bil(real_labels[i],real_labels[j])==(dot(r,s)//2)%2 for i,r in enumerate(real_full) for j,s in enumerate(real_full) if i!=j),'completed real polar pairings')
    monomials=lambda degree:[sum(1<<i for i in S) for d in range(degree+1) for S in itertools.combinations(range(8),d)]
    evaluate=lambda masks,points:[sum(int(x&m==m)<<i for i,x in enumerate(points)) for m in masks]
    fullQ2=g.basis(evaluate(monomials(2),full));fullQ3=g.basis(evaluate(monomials(3),full))
    Q2=g.basis(evaluate(monomials(2),coord));Q3=g.basis(evaluate(monomials(3),coord));C=g.basis(K)
    need(len(fullQ2)==len(Q2)==36 and len(fullQ3)==len(Q3)==84,'global ranks and puncturing injectivity')
    need(all((x&y).bit_count()%2==0 for x in fullQ2 for y in fullQ3),'full-cube orthogonality')
    need(len(g.basis(C+[x&y&z for x in C for y in C for z in C]))==84,'native Schur cube agrees')
    local=[g.shortening(Q3,row) for row in K];need(all(len(L)==36 for L in local),'all native cubic shortenings36')
    constructions=[]
    for i,point in enumerate(coord):
        e=next(x for x in range(1,256) if not quad(x) and bil(point,x))
        f=point^e;need(not quad(f) and bil(e,f)==1,'first hyperbolic pair')
        H=[e,f]
        for pair_number in range(1,4):
            U=[x for x in range(1,256) if all(not bil(x,y) for y in H)]
            ee=next(x for x in U if not quad(x))
            ff=next(x for x in U if not quad(x) and bil(ee,x))
            H.extend([ee,ff])
        need(len(g.basis(H))==8 and all(bil(H[j],H[k])==int(j//2==k//2 and j!=k) for j in range(8) for k in range(8)),'hyperbolic frame')
        transformed=lambda x:sum(bil(x,H[j^1])<<j for j in range(8))
        need(transformed(point)==3 and all(quad(x)==sum(((transformed(x)>>(2*t))&1)*((transformed(x)>>(2*t+1))&1) for t in range(4))%2 for x in range(256)),'exact hyperbolic coordinate change')
        modes=[];full_modes=[]
        for choices in itertools.product((0,1),repeat=3):
            selected=[2*(t+1)+c for t,c in enumerate(choices)]
            support=[x for x in full if all(not(transformed(x)>>j&1) for j in selected)]
            need(len(support)==8 and point in support and all(not bil(x,y) for x,y in itertools.combinations(support,2)),'explicit orthogonal8 clique')
            mask=sum(int(x in support)<<j for j,x in enumerate(coord))
            need(mask>>i&1 and not(mask&~K[i]),'actual native local own-one mode')
            need(len(g.basis(Q3+[mask]))==84,'literal cubic mode belongs')
            modes.append(mask);full_modes.append(support)
        products=g.basis([K[i]&z for z in Q2])
        need(len(products)==28 and len(g.basis(products+modes))==36,'eight independent modes beyond quadratic product')
        need(len(g.basis(local[i]+products+modes))==36,'complete constructive local span')
        constructions.append(dict(receiver=i,hyperbolic_basis=H,mode_supports=[[j for j in range(N) if m>>j&1] for m in modes],mode_charges=[int(m.bit_count()==8) for m in modes]))
    need(all(len(g.basis(C+L))==44 for L in local),'local quotient35')
    pair_hist=Counter()
    for i,j in itertools.combinations(range(N),2):
        d=70-(len(g.basis(C+local[i]+local[j]))-9)
        expected=11 if K[i]>>j&1 else 15
        need(d==expected,'native cubic pair intersection');pair_hist[(bool(K[i]>>j&1),d)]+=1
    adj=[sum(int(i!=j and not bil(x,y))<<j for j,y in enumerate(full)) for i,x in enumerate(full)]
    cliques=[((i,),adj[i]) for i in range(120)]
    for size in range(1,8):
        cliques=[(S+(j,),a&adj[j]) for S,a in cliques for j in g.members(a&~((1<<(S[-1]+1))-1))]
    full_masks=[sum(1<<i for i in S) for S,_ in cliques]
    native_masks=[sum(int(x in {full[i] for i in S})<<j for j,x in enumerate(coord)) for S,_ in cliques]
    need(len(cliques)==2025 and len(g.basis(full_masks))==len(g.basis(native_masks))==84,'complete frame incidence span')
    need(len(g.basis(fullQ3+full_masks))==84,'frame incidence equals cubic code')
    histogram=dict(Counter(m.bit_count() for m in native_masks))
    need(histogram=={8:1094,7:691,6:198,5:40,4:2},'native clique punctures')
    out=dict(status='PASS_AUTHOR_CUBIC_KOSZUL_CONSTRUCTION',source_sha256=g.PIN,credited_geometry_checker_sha256=hashlib.sha256(a.geometry_check.read_bytes()).hexdigest(),exterior_complexes={str(m):exterior_ranks(g,m) for m in (3,4)},global_dimensions=dict(C=9,Q2=36,Q3=84),native_local_dimensions=dict(cubic=36,quadratic_product=28,new_modes=8,canonical_quotient=35),pair_intersections=[dict(orthogonal=k[0],dimension=k[1],pairs=v) for k,v in sorted(pair_hist.items())],full_eight_cliques=2025,native_clique_size_histogram=histogram,local_constructions=constructions,complete_target_fitting=False,physical_word_constructed=False,new_complete_kappa=False)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('local_constructions','exterior_complexes')}))

if __name__=='__main__':main()
