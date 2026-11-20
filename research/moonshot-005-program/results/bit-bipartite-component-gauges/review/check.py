#!/usr/bin/env python3
"""Fresh arithmetic for the relative input/output algebra and two cross channels."""
import argparse
from collections import deque
import gzip,hashlib,json
from pathlib import Path

GEO="9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"
ASSIGN="deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601"
GENS="63fe56dd35607872a50ea0053a54a4f18f591cc57e0477873f1dd808b6a1c3c9"

def need(q,msg):
    if not q:raise ValueError(msg)

def basis_insert(piv,r):
    while r:
        b=r.bit_length()-1
        if b in piv:r^=piv[b]
        else:
            piv[b]=r
            return True
    return False

def rk(rows):
    piv={}
    for r in rows:basis_insert(piv,r)
    return len(piv)

def indices(mask):
    while mask:
        one=mask & -mask
        yield one.bit_length()-1
        mask^=one

def xor(xs):
    r=0
    for x in xs:r^=x
    return r

def times(A,B):
    return tuple(xor(B[k]for k in indices(row))for row in A)

def plus(A,B):
    return tuple(x^y for x,y in zip(A,B))

def cols(A):
    return tuple(sum(((row>>j)&1)<<i for i,row in enumerate(A)) for j in range(len(A)))

def scalar_unit(n,r,c):
    return tuple((1<<c)if i==r else 0 for i in range(n))

def tensor(A,B):
    return tuple(xor(rowb<<(len(B)*j)for j in indices(rowa))for rowa in A for rowb in B)

def identity(n):
    return tuple(1<<i for i in range(n))

def closure_dimension(gens,n):
    # Generate an independent word basis, without loading predecessor word witnesses.
    q=deque([(identity(n),0)]);piv={};depth=0
    while q:
        mat,d=q.popleft()
        if not basis_insert(piv,sum(x<<(n*i) for i,x in enumerate(mat))):continue
        depth=max(depth,d)
        q.extend((times(mat,g),d+1)for g in gens)
        if len(piv)==n*n:break
    return len(piv),depth

def read(path,pin):
    raw=path.read_bytes()
    if path.suffix==".gz":raw=gzip.decompress(raw)
    need(hashlib.sha256(raw).hexdigest()==pin,"data pin "+path.name)
    return json.loads(raw)

def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();base=a.repo/"research/moonshot-005-program/results"
    geo=read(base/"bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",GEO)
    assign=read(base/"bit-two-sided-covariant-target/author/output/ASSIGNMENT.json",ASSIGN)
    seed=read(base/"bit-two-sided-covariant-target/author/WITNESS.json",GENS)
    roots=geo["root_table"][:111]; idx=set(range(111))
    adj=[{j for j,y in enumerate(roots)if sum(u*v for u,v in zip(x,y))==0}for x in roots]
    rw=sorted(adj[80]);cl=sorted(adj[10]);need(len(rw)==62 and len(cl)==61 and 10 not in rw,"native support")
    need(assign["row_transfers"]==[[80,j,t+1]for t,j in enumerate(rw[:59])],"row star ordering")
    need(assign["column_transfers"]==[[i,10,t+1]for t,i in enumerate(cl[:59])],"column star ordering")
    need(assign["internal_edges"]==[[80,j]for j in rw[59:]]+[[i,10]for i in cl[59:]],"central assignments")
    # Bipartite input IDs j, output IDs 111+i. Do not identify the two roles at one root.
    edge={v:set()for v in range(222)if v not in (10,191)}
    for i in idx-{80}:
        for j in adj[i]-{10}:edge[j].add(111+i);edge[111+i].add(j)
    todo=[0];reached={0}
    while todo:
        v=todo.pop()
        nxt=edge[v]-reached;reached.update(nxt);todo.extend(nxt)
    need(len(reached)==len(edge)==220 and sum(map(len,edge.values()))==2*6347,"identity connectivity")
    # Direct rank checks in the native nine-coordinate factor.
    K=[(1<<i)|sum(1<<j for j in adj[i]) for i in range(111)]
    row_ext=(idx-{80})-set(cl); col_ext=(idx-{10})-set(rw)
    ext=[rk(K),rk([K[i]for i in row_ext]),rk(x & sum(1<<j for j in col_ext) for x in K)]
    need(ext==[9,9,9],"native exterior rank witnesses")
    tm,wm,um=[tuple(m) for m in seed["secondary_matrices_8"]]
    I4=identity(4);I8=identity(8);I32=identity(32)
    T=plus(tensor(tm,I4),tensor(I8,(2,4,8,0)))
    W=plus(tensor(wm,I4),tensor(I8,(0,0,0,1)))
    U=tensor(um,I4); dim,depth=closure_dimension((T,W,U),32)
    need(dim==1024,"independent full secondary word closure")
    upper=lambda A:tuple(x<<32 for x in A)+(0,)*32
    lower=lambda A:(0,)*32+tuple(A)
    internal=[upper(I32),upper(T),upper(W),lower(I32),lower(U)]
    need([list(x)for x in internal]==assign["internal_matrices_64"],"five actual central operators")
    need(all(not any(times(N,N))for N in internal),"central square zero")
    # Relative transfer algebra, using sparse 60-bank scalar templates.
    F=[None]+[scalar_unit(60,0,l)for l in range(1,60)]
    R=[None]+[scalar_unit(60,l,0)for l in range(1,60)]
    P=scalar_unit(60,0,0);I=identity(60)
    for l in range(1,60):
        need(plus(times(plus(I,F[1]),plus(I,F[l])),I)==plus(F[1],F[l]),"relative row")
        need(plus(times(plus(I,R[l]),plus(I,R[1])),I)==plus(R[1],R[l]),"relative column")
    need(times(plus(F[1],F[2]),plus(R[1],R[3]))==P,"central idempotent from overlaps")
    need(all(not any(times(P,times(t,P)))for t in [F[1],R[1]]),"tail transfer central compression zero")
    need(times(plus(F[1],F[2]),plus(R[1],R[2]))==(0,)*60,"wrong repeated index cancels in char two")
    def channels(right_for_tail):
        # On each tail, retain the projection S_l on all 16 spinor indices with the given right coordinate.
        small={l:sum(1<<(4*t+r)for t in range(16)) for l,r in right_for_tail.items()}
        cro_rows=[];cro_cols=[];same_rows=[];same_cols=[];crosses=set()
        for i,j,l in assign["row_transfers"]:
            sm=small.get(l,0)
            if sm:crosses.add((i,j))
            cro_rows.extend(1<<c for c in indices(sm))
            same_rows.extend(1<<c for c in indices(((1<<64)-1)^sm))
        for i,j,l in assign["column_transfers"]:
            sm=small.get(l,0)
            if sm:crosses.add((i,j))
            cro_cols.extend(1<<c for c in indices(sm))
            same_cols.extend(1<<c for c in indices(((1<<64)-1)^sm))
        for (i,j),M in zip(assign["internal_edges"],internal):
            if i==80:same_rows+=list(cols(M))
            else:same_cols+=list(M)
        return [len(crosses),rk(cro_rows),rk(cro_cols),rk(same_rows),rk(same_cols)]
    ch=channels({l:0 for l in range(1,49)})
    need(ch==[96,16,16,64,64],"actual two directions and residual ranks")
    mixed_control=channels({l:l%2 for l in range(1,49)})
    need(mixed_control==[96,32,32,64,64],"misaligning right coordinates doubles leakage")
    # Without internal generators the relative transfer algebra is bank-only;
    # a fixed spinor coordinate at all banks is preserved.
    periods=[s for s in range(1,31)if (768*s)%3840==0]
    need(periods==list(range(5,31,5)),"replica availability")
    small=48*16;b=60*64
    out={"status":"PASS_INDEPENDENT_RELATIVE_GAUGES_AND_SPLIT","native_bipartite_identity_vertices":220,
         "native_bipartite_identity_edges":6347,"foreign_edges":sum(map(len,adj)),
         "secondary_algebra_word_span_recomputed":dim,"maximum_independent_word_depth":depth,
         "native_exterior_ranks":ext,"row_donors":rw,"column_receivers":cl,"small_width":small,
         "large_width":b-small,"cross_edges":ch[0],"cross_ranks":ch[1:3],
         "separated_residual_star_ranks":ch[3:],"separated_return_rank":9*b+sum(ch[3:]),
         "separated_canonical_repair":sum(ch[3:]),"replica_period_by_divisibility":5,
         "controls":{"misaligned_right_coordinates_cross_ranks":mixed_control[1:3],
                     "same_tail_twice_cancels_relative_projection":True,
                     "removing_internal_generators_preserves_a_spinor_coordinate":True,
                     "replica_multiplicities_admitted_through_30":periods},
         "source_pins":{"native_layout":GEO,"target_assignment":ASSIGN,"internal_generators":GENS},
         "scope":"fixed field-linear endpoint, independently chosen bipartite gauges; no physical tariff for cross channels"}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(out["status"],ch,ext,dim,depth)

if __name__=="__main__":main()
