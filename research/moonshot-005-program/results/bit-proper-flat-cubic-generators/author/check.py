#!/usr/bin/env python3
"""Exact fixed-source certificate for proper-flat cubic generators."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--geometry-check',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.geometry_check is None:
        candidates=[Path(__file__).resolve().parents[2]/name/'author/check.py' for name in ('quadratic-exterior','bit-quadratic-exterior')]
        args.geometry_check=next((p for p in candidates if p.is_file()),None)
    need(args.geometry_check is not None,'supply credited native geometry loader')
    spec=importlib.util.spec_from_file_location('credited_quadratic_geometry',args.geometry_check)
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    R,K=g.load_native(args.repo);N=len(R)
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    blocks=sorted({tuple(j for j,x in enumerate(r) if x) for r in R if sum(bool(x) for x in r)==4})
    roots=[tuple(2*int(a==b) for a in range(8)) for b in range(8)]
    for block in blocks:
        for signs in itertools.product((-1,1),repeat=3):
            r=[0]*8;r[block[0]]=1
            for j,s in zip(block[1:],signs):r[j]=s
            roots.append(tuple(r))
    need(len(roots)==len(set(roots))==120 and set(R)<=set(roots),'native full real completion')
    need(all(dot(r,r)==4 for r in roots),'root norms')
    need(all(dot(r,s) in (-2,0,2) for r,s in itertools.combinations(roots,2)),'exact full root angles')
    adj=[sum(int(i!=j and dot(r,s)==0)<<j for j,s in enumerate(roots)) for i,r in enumerate(roots)]
    cliques=[((i,),adj[i]) for i in range(120)]
    for size in range(1,8):
        cliques=[(S+(j,),a&adj[j]) for S,a in cliques for j in g.members(a&~((1<<(S[-1]+1))-1))]
    F=[sum(1<<i for i in S) for S,_ in cliques]
    need(len(F)==2025,'all full orthogonal frames')
    native_index={r:i for i,r in enumerate(R)}
    native=lambda mask:sum(1<<native_index[roots[i]] for i in g.members(mask) if roots[i] in native_index)
    C=g.basis(K);Q2=g.basis([a&b for a in C for b in C]);Q3=g.basis([a&b&c for a in C for b in C for c in C])
    need((len(C),len(Q2),len(Q3))==(9,36,84),'independent native Schur code ranks')
    need(len(g.basis([native(f) for f in F]))==84,'frame incidence rank84')
    need(len(g.basis(Q3+[native(f) for f in F]))==84,'all frame indicators are cubic')
    half={}
    for i,r in enumerate(R):
        key=(tuple(j for j,v in enumerate(r) if v),sum(v<0 for v in r)%2)
        half[key]=half.get(key,0)|(1<<i)
    CU=g.basis(C+list(half.values()));need(len(half)==36 and len(CU)==39,'canonical/full-halfclass source rank')
    degrees=[0]*2025;edges=[];seen={};basis_masks=[];basis_witnesses=[];candidate=None
    pivot=92;full_pivot=roots.index(R[pivot])
    for a,b in itertools.combinations(range(len(F)),2):
        common=F[a]&F[b]
        if common.bit_count()!=4:continue
        edges.append((a,b));degrees[a]+=1;degrees[b]+=1
        full_difference=F[a]^F[b]
        if full_difference in seen:continue
        m=native(full_difference);normals=[roots[i] for i in g.members(common)]
        changed=[R[i] for i in g.members(m)]
        need(5<=len(changed)<=8 and all(dot(x,n)==0 for x in changed for n in normals),'proper common-normal chart')
        need(g.mod_rank(changed,101)==4 and g.mod_rank(normals,101)==4,'upper and lower real rank4')
        need(len(g.basis(Q3+[m]))==84,'difference belongs to native Q3')
        witness=dict(full_frame0=list(g.members(F[a])),full_frame1=list(g.members(F[b])),native_difference=list(g.members(m)),common_real_normals=normals)
        seen[full_difference]=m
        if len(g.basis(basis_masks+[m]))>len(basis_masks):
            basis_masks.append(m);basis_witnesses.append(witness)
        if m==sum(1<<i for i in (1,56,73,81,95)):
            candidate=witness
    need(len(edges)==28350 and set(degrees)=={28},'frame adjacency graph')
    need(len(seen)==9450 and len(basis_masks)==84,'proper-chart difference basis')
    need(len(g.basis([f|(1<<120) for f in F]))==85,'odd frame relation exists')
    need(candidate is not None,'chosen five-input witness')
    m=sum(1<<i for i in candidate['native_difference'])
    need(not(m>>pivot&1) and not(m&~K[pivot]),'mode is purely foreign-local at receiver92')
    need(len(g.basis(Q2+[m]))==37,'mode is outside entire Q2')
    need(len(g.basis(CU+[m]))==40,'mode is outside entire canonical-plus-halfclass reservoir')
    changed=[R[i] for i in g.members(m)]
    real_basis=[]
    for r in changed:
        if g.mod_rank(real_basis+[r],101)>len(real_basis):real_basis.append(r)
    accessible=[i for i,r in enumerate(R) if all(dot(r,t)==0 for t in changed)]
    need(accessible==[0,15,20,39,44,57,68,69,83,92,106,107],'actual cache/facet incidences')
    need(len(g.basis(Q3+[m^(1<<pivot)]))==85,'own-coordinate mutation is not cubic')
    need(g.mod_rank([R[i] for i in g.members(m)]+[R[pivot]],101)==5,'invalid receiver input leaves chart')
    profile={1:53,3:7,4:7,6:52,7:164}
    need(sum(profile.values())==283 and sum(r*c for r,c in profile.items())==1562,'derived partial source profile')
    candidate.update(real_basis=real_basis,cache_receiver_facets=accessible,canonical_plus_halfclass_dimension=39,augmented_halfclass_dimension=40,quadratic_dimension=36,augmented_quadratic_dimension=37,derived_closed_partial_profile=profile,literal_source_replay_in_this_checker=False)
    out=dict(status='PASS_AUTHOR_PROPER_FLAT_CUBIC_GENERATORS',native_sha256=g.PIN,credited_geometry_sha256=hashlib.sha256(args.geometry_check.read_bytes()).hexdigest(),full_roots=roots,full_frames=2025,adjacent_frame_pairs=28350,degree28=True,distinct_differences=9450,native_difference_weight_histogram=dict(sorted(Counter(x.bit_count() for x in seen.values()).items())),cubic_dimension=84,proper_chart_dimension=4,independent_generators=basis_witnesses,chosen_five_input_mode=candidate,negative_controls=['own coordinate breaks cubic membership','receiver root breaks proper chart'],new_complete_kappa=False,complete_source=False)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('full_roots','independent_generators','chosen_five_input_mode')}))

if __name__=='__main__':main()
