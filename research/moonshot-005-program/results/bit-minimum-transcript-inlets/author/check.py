#!/usr/bin/env python3
"""Proof inputs for the paid exterior-inlet theorem; standard library plus C++17."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

P = Path("research/moonshot-005-program")
BASE = P / "sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
CODES = P / "results/bit-induced95-equality-rigidity/author/FULL-SUPPORT-CERTIFICATE.json"
ROOMS = P / "results/bit-low-exterior-formation-gate/author/output/RESULT.json"
AXES = set(range(8))
PRIVATE = {14,17,19,20,96,99,101,102}
U = sorted(set(range(111))-AXES-PRIVATE)
SOURCE = [
    (1,P/"sessions/2026-11-17-S020/checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json",
     "a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc",1985,410),
    (2,P/"results/bit-two-copy-field-compiler/author/output/WORD.json",
     "9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550",4010,812),
    (3,P/"results/bit-three-copy-field-compiler/author/output/WORD.json",
     "9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6",6119,1218)]
GAMMA = Q(95,9)
LAYER = (Q(1),Q(24589,25000),Q(1),Q(95,108),Q(95,108))
PUBLIC_ALLOWANCE = Q(9651,10000)


def need(test, why):
    if not test:raise ValueError(why)


def read(path, digest):
    data=path.read_bytes()
    need(hashlib.sha256(data).hexdigest()==digest,f"dependency hash {path}")
    return json.loads(data)


def rref(rows):
    a=[list(map(Q,r))for r in rows];piv=[]
    for col in range(8):
        i=len(piv)
        j=next((j for j in range(i,len(a)) if a[j][col]),None)
        if j is None:continue
        a[i],a[j]=a[j],a[i]
        fac=a[i][col];a[i]=[x/fac for x in a[i]]
        for h in range(len(a)):
            if h!=i and a[h][col]:
                fac=a[h][col];a[h]=[x-fac*y for x,y in zip(a[h],a[i])]
        piv.append(col)
    return tuple(tuple(row) for row in a[:len(piv)]),piv


def space(spec):
    rows,piv=rref(spec["rows"])
    if spec["kind"]=="span":return rows
    need(spec["kind"]=="ann","chart kind")
    basis=[]
    for j in range(8):
        if j in piv:continue
        x=[Q(0)]*8;x[j]=1
        for p,r in zip(piv,rows):x[p]=-r[j]
        basis.append(x)
    return rref(basis)[0]


def source_cut(repo, entry, roots):
    b,rel,pin,cut,nfields=entry
    word=read(repo/rel,pin)
    need(word["carrier_interface_before_operation"]==cut,"exact interface")
    spaces={n:space(s) for n,s in word["charts"].items()}
    name=lambda c,t,i: (f"C{c}__" if b>1 else "")+t+str(i)
    live={name(c,t,i):[1<<(222*c+111*z+i),"zero" if z else f"L{i}"]
          for c in range(b) for z,t in enumerate("XY") for i in range(111)}
    publics=set(live)
    for op,k,*x in word["operations"][:cut]:
        if op=="INIT":
            need(k not in live,"fresh owner");live[k]=[0,x[0]]
        elif op=="ADD":
            need(spaces[live[k][1]]==spaces[live[x[0]][1]],"cochart add");live[x[0]][0]^=live[k][0]
        elif op=="MOVE":live[k][1]=x[0]
        elif op=="CLEAR":del live[k]
        else:raise ValueError(op)
    need(len(live)==nfields,"field inventory")
    one_U=sum(1<<i for i in U)
    Ucols=sum(one_U<<(222*c) for c in range(b))
    def facet_set(B):
        return [i for i in U if all(sum(vj*rj for vj,rj in zip(v,roots[i]))==0 for v in B)]
    lowclasses={}
    informative=Counter()
    for k,(val,loc) in live.items():
        B=spaces[loc]
        if len(B)>5 or not (val&Ucols):continue
        if loc not in lowclasses:lowclasses[loc]=facet_set(B)
        need(lowclasses[loc],"informative low field outside D_U: "+k)
        informative[len(B)]+=1
    for c in range(b):
        for i in range(111):
            need(len(spaces[live[name(c,"X",i)][1]])==8,"every original X is already at Hub")
        for i in AXES:
            row,loc=live[name(c,"Y",i)]
            need(len(spaces[loc])==0 and row==((1<<(222*c+i)) | (1<<(222*c+111+i))),"completed unraised coordinate Y")
        for i in PRIVATE:
            need(len(spaces[live[name(c,"Y",i)][1]])==6,"private Y already rank six")
    suffix_moves={}
    for op,k,*x in word["operations"][cut:]:
        if op=="CLEAR":continue
        need(op=="MOVE" and k in publics,"retained suffix contains a paid owner or other operation")
        suffix_moves.setdefault(k,[]).append(x[0])
    for c in range(b):
        for i in AXES:
            moves=suffix_moves[name(c,"Y",i)]
            need(len(moves)==1 and spaces[moves[0]]==spaces[f"F{i}"] and len(spaces[moves[0]])==7,
                 "prepaid direct axis endpoint")
    return {"copies":b,"source":pin,"all_original_columns":222*b,"cut":cut,"live_fields":nfields,
            "U_sensitive_initial_fields_at_or_below_rank_five_by_rank":dict(sorted(informative.items())),
            "such_fields_outside_D_U":0,"low_input_charts_with_a_verified_U_normal":len(lowclasses),
            "eligible_public_axis_records":8*b,"their_prepaid_route":"one rank-0 to rank-7 public MOVE each",
            "source_suffix_owned_moves":0}


def geometry(roots):
    source=Path(__file__).with_name("flat_four.cpp")
    lines="".join(" ".join(map(str,roots[i]))+"\n" for i in U)
    with tempfile.TemporaryDirectory() as tmp:
        executable=Path(tmp)/"geom"
        subprocess.run([os.environ.get("CXX","c++"),"-std=c++17","-O2",str(source),"-o",str(executable)],check=True)
        run=subprocess.run([str(executable)],input=lines,text=True,capture_output=True,check=True)
    maximum,axis,counts=[list(map(int,line.split())) for line in run.stdout.splitlines()]
    need(maximum==[1,3,6,12] and axis==[11]*8,"native root-space sizes")
    need(counts==[95,4465,137882,3125924],"independent ternary native subsets")
    return maximum,axis,counts


def code_density(code):
    vectors=[sum(bit<<j for j,bit in enumerate(code["canonical_vectors"][str(i)]))for i in U]
    weights=sorted(sum((xi&l).bit_count()%2 for xi in vectors)for l in range(1,512))
    short=[(sum(weights[:2**k-1])+2**(k-1)-1)//2**(k-1)for k in range(1,10)]
    need(short==[35,55,68,75,80,83,85,88,95],"all nine shortened-support lower dimensions")
    need(all(Q(value)>=GAMMA*k for k,value in enumerate(short,1)),"uniform basis-polytope density")
    return short


def root_price(g,scale=10**36):
    if g in (0,1):return Q(g),Q(g)
    target=g**199*scale**200;lo=0;hi=8*scale+1
    while hi-lo>1:
        z=(lo+hi)//2
        if z**200<=target:lo=z
        else:hi=z
    need(lo**200<=target<hi**200,"outward tariff")
    return Q(lo,scale),Q(hi,scale)


def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    roots=read(a.repo/BASE,"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e")["native_roots"]
    code=read(a.repo/CODES,"012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963")
    prior=read(a.repo/ROOMS,"befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145")
    maxroot,axis,counts=geometry(roots);short=code_density(code);sources=[source_cut(a.repo,e,roots) for e in SOURCE]
    prices=[root_price(g) for g in range(9)]
    downhill=[]
    for s in range(1,9):
        for d in range(s):
            load=sum(w for r,w in enumerate(LAYER,1) if d<=r<s)
            need(load**200 <= (s-d)**199,f"downward price for {s} to {d}")
            downhill.append([s,d,str(load)])
    owned=[];public=[];credit_without_premium=[]
    for s in range(1,6):
        W=sum(LAYER[s-1:])
        for origin in range(s):
            own_demand=Q(([0]+maxroot)[origin])*W/GAMMA
            need(own_demand**200 <= (s-origin)**199,"paid owned upward exit")
            owned.append([origin,s,str(own_demand)])
            axis_cap=(0,1,3,6,max(axis))[origin]
            public_demand=Q(axis_cap)*W/GAMMA
            premium=prices[origin][0]+prices[s-origin][0]+prices[7-s][0]-prices[7][1]
            need(public_demand <= PUBLIC_ALLOWANCE+premium, "axis split allowance")
            public.append([origin,s,str(public_demand),str(premium)])
            if public_demand>PUBLIC_ALLOWANCE:credit_without_premium.append([origin,s])
    need([3,4] in credit_without_premium,"removing the rank-three exit split must defeat this certificate")
    bill=9*sum(LAYER)+8-8*PUBLIC_ALLOWANCE
    result={"status":"PASS_UNRESTRICTED_MINIMUM_TRANSCRIPT_WEIGHTED_SOURCE_EXCLUSION",
            "source_cut_replays":sources,"minimum_downset_events_assumed":"9b","exterior_event_count_restriction":False,
            "maximum_native_roles_by_rank_1_2_3_4":maxroot,"maximum_rank_four_role_count_within_each_native_axis_facet":axis,
            "independent_native_subsets_over_F3_by_rank":counts,"shortening_support_lower_bounds":short,
            "minimum_total_projection_rank_per_dimension":str(GAMMA),"layer_weights":list(map(str,LAYER)),
            "maximum_public_inlet_allowance_after_split_premium":str(PUBLIC_ALLOWANCE),
            "downward_dual_loads":downhill,"owned_exit_dual_loads":owned,
            "axis_exit_dual_load_and_lower_premium":public,"controls_failing_when_premium_omitted":credit_without_premium,
            "normalized_lower_bill":str(bill),"normalized_strict_deficits":[]}
    for s in prior["sources"]:
        lo,hi=map(Q,s["normalized_room"]["rational"])
        need(bill>hi,"strict deficit vs limiting caller")
        result["normalized_strict_deficits"].append({"copies":s["copies"],"room":[str(lo),str(hi)],
            "excess":[str(bill-hi),str(bill-lo)]})
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(f"PASS all minimum linear transcripts, paid exits and public premiums; normalized lower bill {float(bill):.12f}")


if __name__=="__main__":main()
