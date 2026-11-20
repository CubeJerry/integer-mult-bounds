#!/usr/bin/env python3
"""Forward all eight physical lanes on actual owner IDs, including singleton controls."""
import argparse,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from transfer import Atlas,TABLE,BODY,rank_fast
from build import power,require,grouped_sources
from rs_source import source_slot,coefficients
from terminal import k_row

def field_dot(a,b):
    return np.bitwise_xor.reduce(TABLE[np.asarray(a,dtype=np.uint8),b])

def full_forward(atlas,i,j,x):
    # Raw native donor and facet bases have the identical (n, copy,channel,power) order.
    raw={};t=0
    for n in (9,36):
        for ell in range(8):
            for c in range(2*(n//3)):
                raw[n,ell,c]=x[t:t+16]
                t+=16
    h_values={}
    for h in atlas.ks[j]:
        if not atlas.H[h]<=atlas.orth[i]:continue
        p=atlas.phase[str(h)];donors=sorted(atlas.H[h]&set(range(111)))
        q={int(d):v for d,v in p["donor_early"].items()}
        # True input holder groups and true H output-port holder sets are independent.
        possible=defaultdict(list)
        for ds in atlas.h_ports[h]:
            for d in ds:
                for phase in ("X","Y"):
                    for owner in atlas.left_flags[h,d,phase]:
                        source=atlas.route[owner][6]
                        possible[phase,source].extend(owner*8+b for b in range(8))
        for group in possible.values():group.sort()
        for phase,tag in (("X","early"),("Y","late")):
            nc=p[tag]*8;used=Counter()
            if not nc:continue
            for ds in atlas.h_ports[h]:
                n=len(ds);k=n//3;local=np.zeros((n,nc),dtype=np.uint8)
                source_groups=grouped_sources(phase,donors,p["m"],k,q)
                # Fill actual source outputs, then read the physical H preshuffle.
                actual={}
                for degree,dj in enumerate(source_groups):
                    for b in range(nc):
                        owner=possible[phase,dj][used[dj]];used[dj]+=1
                        if dj!=j:actual[owner]=0;continue
                        ell,c,der,scale=source_slot(phase,h,dj,degree,b,n,p,atlas.colours[j],q[j])
                        actual[owner]=field_dot(coefficients(atlas.nodes[j,h],der,scale),raw[n,ell,c])
                        require(owner%8==ell,"true source holder copy")
                end=used.copy()
                for degree,dj in enumerate(source_groups):
                    end[dj]-=nc
                for degree,dj in enumerate(source_groups):
                    for b in range(nc):
                        owner=possible[phase,dj][end[dj]];end[dj]+=1
                        local[degree,b]=actual[owner]
                z=atlas.ops.matmul(atlas.V[n],local)
                if phase=="X":
                    h_values[h,n]=local
                elif p["m"] in (1,2):
                    C=atlas.deriv[n].copy()
                    if p["m"]==2:C[:,2*k:]=0
                    z^=atlas.ops.matmul(C,h_values[h,n])
                for pos,d in enumerate(ds):
                    names=[u*8+b for u in atlas.left_flags[h,d,phase] for b in range(8)]
                    for uu,val in zip(names,z[pos]):h_values[uu]=val
    k_inputs={}
    for d,S in enumerate(atlas.D):
        if j not in S or i not in atlas.D[atlas.dual[d]]:continue
        M,owners=atlas.middle_matrix(d)
        mat=np.array([[h_values.get(u*8+b,0)for b in range(8)]for u in owners],dtype=np.uint8)
        out=atlas.ops.matmul(M,mat)
        for u,row in zip(owners,out):k_inputs[u]=row
    answer=np.zeros(3840,dtype=np.uint8); zero=np.zeros(8,dtype=np.uint8)
    for h in atlas.ks[i]:
        p=atlas.phase[str(h)];chart=atlas.kr[str(h)];kv={};counts=Counter()
        for phase,ins,outs in chart["stripes"]:
            z=atlas.ops.matmul(atlas.V[len(ins)].T,np.stack([k_inputs.get(u,zero)for u in ins]))
            for u,v in zip(outs,z):kv[u]=v
        for a,b in chart["early_cache_to_late"]:kv[b]^=kv[a]
        for phase,ins,outs in chart["stripes"]:
            n=len(ins);s=counts[phase,n];counts[phase,n]+=1; chan=2*(n//3)
            for deg,u in enumerate(outs):
                rt=atlas.route[u];dest=rt[1] if phase=="Y"else rt[7]
                if dest!=i:continue
                for b in range(8):
                    ell,c,der,scale=k_row(phase,p["m"],p["donor_early"][str(i)],i,deg,n,h in atlas.colours[i]["first"],s,b)
                    rr=(0 if n==9 else 768)+(ell*chan+c)*16
                    co=np.array(coefficients(atlas.nodes[i,h],der,scale),dtype=np.uint8)
                    answer[rr:rr+16]^=TABLE[int(kv[u][b]),co]
    return answer

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("repo","k-words","d-charts","out"):p.add_argument("--"+key,type=Path,required=True)
    p.add_argument("--library",type=Path)
    a=p.parse_args();atlas=Atlas(a.repo,a.k_words,a.d_charts,a.library)
    copy=np.asarray(atlas.raw_to_copy_base);states={}
    for i,j in [(27,28),(49,31),(97,8)]:
        B=atlas.block(i,j);require(rank_fast(B)==480,"base block rank")
        rx=np.array([[(7*r+13*c)^((r*c)>>3) for c in range(8)]for r in range(480)],dtype=np.uint32)
        for tag,batch in [("all_lanes",(rx%64).astype(np.uint8)),
                          ("one_lane",np.where(np.arange(8)==3,(rx%64).astype(np.uint8),0))]:
            whole=batch[copy[:,1],copy[:,0]]
            got=full_forward(atlas,i,j,whole);z=atlas.ops.matmul(B,batch)
            want=z[copy[:,1],copy[:,0]]
            require(np.array_equal(got,want),"physical eight-copy full-vector replay")
            states[f"{i},{j}/{tag}"]=hashlib.sha256(got.tobytes()).hexdigest()
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"FULL-COPY-CHECK.json").write_text(json.dumps(states,indent=2,sort_keys=True)+"\n")
    print(states)
if __name__=="__main__":main()
