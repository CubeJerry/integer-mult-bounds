#!/usr/bin/env python3
"""Independent native contraction-union and common-amplitude reconstruction."""
from argparse import ArgumentParser
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import numpy as np


def need(ok,why):
    if not ok:
        raise ValueError(why)


ap=ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
here=Path(__file__).resolve().parent
base=args.repo/'research/moonshot-005-program/results'
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
spec=importlib.util.spec_from_file_location('s030_independent',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
roots=g.roots_from_files(layout,json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text()))
H,D=list(map(set,layout['A2'])),list(map(set,layout['D4']))
adj=[{i for i,y in enumerate(roots) if i!=j and not g.b(x,y)} for j,x in enumerate(roots)]
old=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
raw=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz').read_bytes()))
cert=json.loads(gzip.decompress((here.parent/'output/CERTIFICATE.json.gz').read_bytes()))
maps={int(j):{int(h):np.array(A,dtype=np.uint8) for h,A in row.items()} for j,row in raw['maps'].items()}
views={j:{i:sorted(h for h in maps[j] if H[h]<=adj[i]) for i in sorted(adj[j])} for j in (0,61,45)}


def basis(A):
    return A[:,g.echelon(A)[1]]


def fibres(j,h):
    return {i:g.null(np.vstack([maps[j][q] for q in visible if q!=h])) for i,visible in views[j].items() if i<111 and i!=80 and h in visible}


A,B,C=fibres(0,263),fibres(61,642),fibres(0,116)
need([len(A),len(B),len(C)]==[33,34,32],'complete native anchor families')
forced={}
for q in maps[45]:
    cols=[K for h,family in [(642,B),(116,C)] for i,K in family.items() if q!=h and H[q]<=adj[i]]
    forced[q]=basis(np.hstack(cols)) if cols else np.zeros((48,0),dtype=np.uint8)
ann={q:g.null(Z.T).T for q,Z in forced.items()}
kernels={i:g.null(np.vstack([ann[q] for q in visible])) for i,visible in views[45].items() if i<111}
union=basis(np.hstack(list(kernels.values())))
defects={i:K.shape[1] for i,K in kernels.items() if K.shape[1]}
need(len(kernels)==59 and len(defects)==29 and set(defects.values())=={3} and union.shape==(48,15),'exact frozen native loss union')
need(g.rank(np.hstack([union,np.array(cert['frozen_union_basis'],dtype=np.uint8)]))==15,'literal frozen union spans the same source space')
for i,K in kernels.items():
    for q in views[45][i]:
        need(g.rank(np.hstack([forced[q],K]))==forced[q].shape[1],'actual invariant translation directions')

# New bases and nullspace solve, without using the saved author equation matrix.
SA,Sb=basis(np.hstack(list(A.values()))),basis(np.hstack(list(B.values())))
U=basis(np.hstack([SA,Sb]))
need([SA.shape[1],Sb.shape[1],U.shape[1]]==[22,18,30],'native core dimensions')
rows=g.echelon(U.T)[1]
Ui=g.invert(U[rows])
P=np.array(old['Hwords']['263'],dtype=np.uint8)
ports=[110,132,720,810,1509,1735,1994,2621,2836]
eq=[]
for i in reversed(sorted(A)):
    K=g.mm(Ui,A[i][rows])
    visible=[p for p,d in enumerate(ports) if D[d]<=adj[i]]
    need(len(visible)==3,'actual H263 receiver packet rows')
    for j in (2,1):
        for p in reversed(visible):
            for t in range(3):
                row=np.zeros((3,3,30),dtype=np.uint8)
                row[0]=g.M[P[p,:3,None],K[None,:,t]]
                row[j]=g.M[P[p,3*j:3*j+3,None],K[None,:,t]]
                eq.append(row.reshape(-1))
retained=0
for i,K0 in B.items():
    if 263 not in views[61][i]:
        continue
    retained+=1
    K=g.mm(Ui,K0[rows])
    for u in range(3):
        for t in range(3):
            row=np.zeros((3,3,30),dtype=np.uint8)
            row[1,u]=K[:,t]
            eq.append(row.reshape(-1))
Eq=np.array(eq,dtype=np.uint8)
N=g.null(Eq)
need(retained==19 and Eq.shape==(765,270) and N.shape==(270,57),'all native common-readout and retained companion equations')
scalar=np.zeros((16,6),dtype=np.uint8)
for t,e in enumerate([0,1,3,7,13,15]):
    scalar[e,t]=1
scalar[4,4]=1
S0=np.kron(scalar,np.eye(3,dtype=np.uint8))
coordinates=g.mm(Ui,S0[rows])
need(np.array_equal(g.mm(U,coordinates),S0),'entire old core lies in coordinate space')
image=np.column_stack([np.concatenate([g.mm(Q,coordinates).reshape(-1) for Q in N[:,j].reshape(3,3,30)]) for j in range(57)])
oldC=[np.array(old['maps'][str(j)]['263'],dtype=np.uint8) for j in (0,61,62)]
expected=[]
for u in range(3):
    for v in range(3):
        M=np.zeros((3,3),dtype=np.uint8)
        M[u,v]=1
        right=np.kron(np.eye(6,dtype=np.uint8),M)
        expected.append(np.concatenate([g.mm(g.mm(Q,S0),right).reshape(-1) for Q in oldC]))
expected=np.column_stack(expected)
need([g.rank(image),g.rank(expected),g.rank(np.hstack([image,expected]))]==[9,9,9],'exact full common-amplitude normal form')
need(5 in A and 116 not in views[0][5] and 642 not in views[61][5] and g.rank(g.mm(oldC[0],A[5]))==3,'full-cut witness for amplitude invertibility')
singular=np.diag(np.array([1,1,0],dtype=np.uint8))
bad_central=g.mm(oldC[0],np.kron(np.eye(16,dtype=np.uint8),singular))
need(g.rank(np.vstack([bad_central if q==263 else maps[0][q] for q in views[0][5]]))==47,'singular common amplitude fails the required full source cut')

# Rebuild the affine family after the common amplitude normalization.
I=np.eye(3,dtype=np.uint8)
baseline={int(j):{int(q):np.kron(np.array([[g.power(n,e) for e in range(16)]],dtype=np.uint8),I) for q,n in table.items()} for j,table in old['base_nodes'].items()}
for j,Q in zip((0,61,62),oldC):
    baseline[j][263]=Q
inverse={j:{i:g.invert(np.vstack([baseline[j][q] for q in visible])) for i,visible in views[j].items()} for j in (0,61)}
def column(j,i,h):
    p=views[j][i].index(h)
    return inverse[j][i][:,3*p:3*p+3]
A0={i:column(0,i,263) for i,v in views[0].items() if 263 in v}
B0={i:column(61,i,642) for i in B}
C0={i:column(0,i,116) for i in C}
ann0=g.null(S0.T).T
R=np.array(cert['effective_tail_rows'],dtype=np.uint8)
need(R.shape==(12,48) and not np.any(g.mm(R,S0)) and g.rank(g.mm(R,Sb))==12,'all effective tail restrictions')
need(all(g.rank(np.hstack([Sb,K]))==18 for family in (B0,C0) for K in family.values()),'all old companion fibres belong to Sb')
need(all(not np.any(g.mm(ann0,K)) for K in A0.values()),'all anchor inverse columns belong to S0')
coefficients={}
for i,K in C0.items():
    blocks=np.zeros((37,48,3),dtype=np.uint8)
    blocks[0]=K
    if i in A0:
        values=g.mm(R,K)
        for u in range(3):
            for v in range(12):
                blocks[1+12*u+v]=g.M[A0[i][:,u,None],values[v,None,:]]
    coefficients[i]=blocks
cache={}
for q in maps[45]:
    cols,origins=[],[]
    for i,K in B0.items():
        if q!=642 and H[q]<=adj[i]:
            block=np.zeros((37,48,3),dtype=np.uint8)
            block[0]=K
            cols.append(block)
            origins.extend([642,i,p] for p in range(3))
    for i,block in coefficients.items():
        if q!=116 and H[q]<=adj[i]:
            cols.append(block)
            origins.extend([116,i,p] for p in range(3))
    need(origins==cert['origins'][str(q)],'full native affine generator list')
    cache[q]=np.concatenate(cols,axis=2).reshape(1776,-1)
constants=[]
ranks=[]
for i in (22,24,30,32):
    witness=cert['witnesses'][str(i)]
    need(witness['planes']==views[45][i] and all(not H[h]<=adj[i] for h in (116,263,642)),'actual distant native witness')
    Y=np.array(witness['coefficient_blocks'],dtype=np.uint8)
    need(Y.shape==(37,48,3) and all(not np.any(g.mm(ann0,M)) for M in Y[1:]),'all variable witness coefficients vanish in common quotient')
    for q in views[45][i]:
        L=np.array(witness['constant_combinations'][str(q)],dtype=np.uint8)
        Z=cache[q]
        need(np.array_equal(g.mm(Z,L),Y.reshape(1776,3)),'all37 coefficient identities')
        changed=L.copy()
        changed[next(t for t in range(Z.shape[1]) if np.any(Z[:,t])),0]^=1
        need(not np.array_equal(g.mm(Z,changed),Y.reshape(1776,3)),'mutated combination rejected')
    constants.append(Y[0])
    ranks.append(g.rank(g.mm(ann0,np.hstack(constants))))
need(ranks==[3,6,9,12],'four independent constant projections force accumulated loss12')
result={'status':'PASS_ROOT_CONSTRAINED_CONTRACTION_UNION_REVIEW','native_views':59,'frozen_deficient_views':defects,
        'frozen_union_rank':15,'normal_form_equations':[765,270],'normal_form_nullity':57,'restriction_rank':9,
        'witness_receivers':[22,24,30,32],'constant_projection_ranks':ranks,'coefficient_identities':64,
        'universal_constrained_union_lower_bound':12,'changed_target_can_relax_constraints':True,
        'arbitrary_non_GF64_linear_central_changes':False,'author_executables_imported':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],15,12,57,64,flush=True)
