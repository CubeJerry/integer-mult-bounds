#!/usr/bin/env python3
"""Compile two physical GF64 F decoders against actual whole-K word payloads."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip, hashlib, json
from pathlib import Path
from build import (COPIES, DEGREE, PRODUCT, PINNED, bit_rows, compile_binary,
                   field_rank, power, require, swap_cycles, unpack)
from rs_source import coefficients, row_cost

# Scales for physical right D ordering and truncated singleton cross; n=9,36,45.
SCALE = {49:(2,1,2),97:(2,1,2),53:(1,1,3),77:(1,2,1),93:(1,1,1),
         8:(1,1,2),82:(1,1,1),58:(1,1,2),106:(4,1,1),31:(1,1,1),105:(1,1,1)}
SCALE_INDEX = {9:0,36:1,45:2}
K_PINS={"spread":"513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0",
        "mixed":"8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a",
        "template":"6691b46a45b253e1e48f073f2114aed0c817e786b7efe7dce3dfa440c01cc73d"}

def payload(path, expected):
    raw = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == expected, "K pin " + path.name)
    return json.loads(raw)

def k_row(phase, size, quota, i, t, n, first_half, stripe, copy):
    """Functional assigned to one actual terminal output in the algebraic dual."""
    k=n//3
    if size==3 and quota==30:
        require(phase=="Y","selected K late-only")
        return copy,t%k + stripe*k,False,1
    if size==2 and quota==30:
        require(phase=="Y" and t<2*k,"asymmetric large receiver")
        return copy,t,False,1
    if size==1:
        require(phase=="Y","singleton sees actual late Ys")
        if t<2*k:
            return copy,t,False,1
        return copy,t-2*k,True,SCALE[i][SCALE_INDEX[n]]
    first=first_half if phase=="Y" else not first_half
    return copy,t%k+(0 if first else k),False,1

def jet(nodes,k,multiplier):
    matrix=[]
    for early in (True,False):
        for z in nodes:
            row=[]
            for t in range(2*k):
                if early:
                    value=power(z,t-1) if t%2 else 0
                else:
                    value=power(z,t)
                    if t<k:
                        value ^= PRODUCT[multiplier][power(z,2*k+t)]
                row.append(value)
            matrix.append(row)
    return matrix

@lru_cache(None)
def compile_Et(desc):
    rows=[list(coefficients(*d)) for d in desc]
    require(len(rows)==16 and field_rank(rows)==16,"true Y confluent basis")
    code=compile_binary(bit_rows([list(row) for row in zip(*rows)]))
    return len(code),hashlib.sha256(bytes(v for pair in code for v in pair)).hexdigest()

def variants(args):
    base=args.repo/"research/moonshot-005-program/results"
    geo=json.loads(unpack(base,"geometry"))
    phases=json.loads(unpack(base,"phases"))
    marked=set(json.loads(unpack(base,"spread"))["selected_D"])
    orig=[json.loads(line) for line in unpack(base,"routes").splitlines()]
    H=list(map(frozenset,geo["A2"])); D=list(map(frozenset,geo["D4"]))
    dual=geo["dual_D4"]; roots=geo["root_table"]; native=set(range(111))
    orth=[{j for j,y in enumerate(roots) if sum(a*b for a,b in zip(x,y))==0} for x in roots]
    ks={i:[h for h,plane in enumerate(H) if i in plane] for i in native}
    nodes={(i,k):s+1 for i,charts in ks.items() for s,k in enumerate(charts)}
    single={}; first_half={}
    for i in native:
        singles=[h for h in ks[i] if phases[str(h)]["m"]==1]
        require(len(singles)==int(i in SCALE),"actual singletons")
        single[i]=singles[0] if singles else None
        half=[h for h in ks[i] if phases[str(h)]["donor_early"][str(i)]==15]
        require(len(half)==(25 if singles else 24),"half-late K counts")
        first_half[i]=set(half[:12])
    def fid(r):
        return (53280 if r[0]=="Y" else 0)+480*r[1]+r[2]
    route={fid(r):r for r in orig}
    expected=json.loads((args.k_words/"RESULT.json").read_text())
    require(expected["field_modulus"]==0x43,"common field")
    require(expected["template_payload"]==K_PINS["template"] and all(
            expected[t]["word_payload"]==K_PINS[t] for t in ("spread","mixed")),"fixed K digests")
    templates=payload(args.k_words/"TEMPLATES.json.gz",expected["template_payload"])
    for key,code in templates.items():
        n=int(key); binary=[1<<t for t in range(DEGREE*n)]
        for dst,src in code:
            binary[dst] ^= binary[src]
        require(binary==bit_rows([[power(p+1,t) for p in range(n)] for t in range(n)]),
                "physical row word equals field-transposed V")
    all_results={}
    args.out.mkdir(parents=True,exist_ok=True)
    for variant,groups in [("spread",(9,36)),("mixed",(45,))]:
        right=payload(args.k_words/(variant.upper()+"-OWNERS.json.gz"),expected[variant]["word_payload"])
        rows=defaultdict(list); costs=Counter(); early_hash=hashlib.sha256(); late_hash=hashlib.sha256()
        actual_Y=defaultdict(set); seen_terminal=set(); input_ds={}; per_F_early=Counter()
        for key,chart in right.items():
            h=int(key); size=len(H[h]&native); p=phases[key]
            expected_cache=set(); counts=Counter(); used=defaultdict(set); early_by_n={}
            for phase,inputs,outputs in chart["stripes"]:
                n=len(inputs); k=n//3; stripe=counts[phase,n]; counts[phase,n]+=1
                require(n in groups and len(outputs)==n,"stripe width")
                ds=tuple(route[t][4] for t in inputs)
                require(ds==tuple(sorted(set(ds))) and all(H[h]<=D[dual[d]] for d in ds),
                        "physical incoming D order")
                require(input_ds.setdefault((h,n),ds)==ds,"same nodes per phase and stripe")
                if variant=="spread":
                    require(all((d in marked)==(n==9) for d in ds),"actual spread")
                require(all(route[t][0]==phase and route[t][5]==h for t in inputs+outputs),"co-location")
                require(not used[phase]&set(outputs),"distinct terminal/closure owners")
                used[phase].update(outputs)
                if phase=="X":
                    early_by_n[n]=outputs
                elif size<3:
                    expected_cache.update((early_by_n[n][t-1],outputs[t]) for t in range(1,2*k,2))
                for t,holder in enumerate(outputs):
                    r=route[holder]; i=r[1] if phase=="Y" else r[7]
                    # Authenticate the consecutive rows used in the ordinary dual-rank proof.
                    receivers = sorted(H[h] & native)
                    if size == 3:
                        target = receivers[t//k]
                    elif size == 2:
                        small = next(u for u in receivers if p["donor_early"][str(u)] == 15)
                        large = next(u for u in receivers if u != small)
                        target = small if t >= 2*k else (large if phase == "Y" else None)
                    else:
                        target = receivers[0] if phase == "Y" else None
                    require(i == target, "authentic K receiver/closure row and phase order")
                    if i is None:
                        continue
                    require(i in H[h]&native and holder not in seen_terminal,"genuine terminal owner")
                    seen_terminal.add(holder)
                    quota=p["donor_early"][str(i)]
                    if phase=="X":
                        per_F_early[i]+=1
                    for copy in range(COPIES):
                        lane,c,der,scale=k_row(phase,size,quota,i,t,n,h in first_half[i],stripe,copy)
                        require(0<=c<2*k,"channel index")
                        if phase=="Y":
                            actual_Y[i].add(holder)
                            rows[i,n,lane,c].append((h,der,scale,holder*COPIES+copy))
                        else:
                            require(not der and scale==1,"early response to ordinary evaluations")
                            early_hash.update(f"{holder}/{copy}/{i}/{h}/{n}/{lane}/{c}\n".encode())
                            costs["early_to_late_ADD"]+=row_cost(nodes[i,h],False,1)
                            costs["stationary_capture_ADD_INIT_dirty_CLEAR"]+=DEGREE
            require(set(map(tuple,chart["early_cache_to_late"]))==expected_cache,
                    "actual K derivative reads precisely odd t below 2k")
        require(seen_terminal=={fid(r) for r in orig if r[5] is not None and
                               (r[0]=="Y" or r[7] is not None)},"every true F-visited X and Y")
        require(all(len(w)==480 for w in actual_Y.values()),"480 Y owners at every F")
        hashes={}
        for i in sorted(native):
            perm=[]
            for n in groups:
                for lane in range(COPIES):
                    for c in range(2*(n//3)):
                        desc=sorted(rows[i,n,lane,c])
                        coeffs=tuple((nodes[i,h],der,scale) for h,der,scale,_ in desc)
                        count,digest=compile_Et(coeffs)
                        hashes[digest]=count; costs["late_basis_ADD"]+=count
                        perm.extend(w-(53280+480*i)*COPIES for _,_,_,w in desc)
            require(len(perm)==3840,"all final native Y coordinates")
            costs["actual_Y_permutation_ADD"]+=swap_cycles(perm)*3*DEGREE
            late_hash.update(b"".join(t.to_bytes(2,"big") for t in perm))
        ordinary=special=triples=0
        minors=[]; failures=[]
        for i in sorted(native):
            for j in sorted(orth[i]&native):
                charts=[h for h in ks[i] if H[h]<=orth[j]]
                require(len(charts)==len({nodes[i,h] for h in charts})==16,"actual 16 K nodes")
                for h in charts:
                    for n in groups:
                        ds=input_ds[h,n]
                        z=tuple(p+1 for p,d in enumerate(ds) if j in D[d])
                        require(len(z)==n//3 and len(set(z)-{0})==n//3,"k distinct nonzero nodes")
                    triples+=1
                h=single[i]
                if h not in charts:
                    ordinary+=1
                    continue
                special+=1; x0=nodes[i,h]; ratio=0
                for u in charts:
                    if u!=h:
                        ratio^=power(x0^nodes[i,u],62)
                for n in groups:
                    ds=input_ds[h,n]; z=tuple(t+1 for t,d in enumerate(ds) if j in D[d])
                    k=n//3; delta=SCALE[i][SCALE_INDEX[n]]
                    rank=field_rank(jet(z,k,PRODUCT[ratio][delta]))
                    require(rank==2*k,"actual right singleton residual kernel")
                    minors.append([i,j,h,n,ratio,delta,list(z),rank])
                    if len(failures)<2 and delta!=1:
                        wrong=field_rank(jet(z,k,ratio))
                        if wrong<2*k:
                            failures.append([i,j,h,n,wrong,2*k])
        require((ordinary,special,triples)==(6110,360,103520),"complete right-rank coverage")
        require(len(minors)==360*len(groups) and failures,"right finite minors and controls")
        captures=costs["stationary_capture_ADD_INIT_dirty_CLEAR"]
        require(captures==40125*COPIES*DEGREE,"true F snapshots")
        pure=costs["late_basis_ADD"]+costs["actual_Y_permutation_ADD"]
        forward=pure+costs["early_to_late_ADD"]+captures
        result={"status":"PASS_ALL_FOREIGN_NATIVE_K_TO_F_RANKS","variant":variant,
                "field":"GF(2)[z]/(z^6+z+1)","right_minor_rank_all_pairs":3840,
                "ordinary_foreign_pairs":ordinary,"singleton_foreign_pairs":special,
                "right_visible_K_projections":triples,"actual_singleton_minors":len(minors),
                "chosen_singleton_scales_by_9_36_45":SCALE,
                "actual_early_X_F_visits_at_bank3840":40125*COPIES,
                "actual_late_Y_F_owners_at_bank3840":111*3840,
                "distinct_transposed_word_hashes":len(hashes),
                "early_capture_assignments_sha256":early_hash.hexdigest(),
                "actual_Y_permutations_sha256":late_hash.hexdigest(),
                "pins":{"K_word_payload":expected[variant]["word_payload"],
                        "K_template_payload":expected["template_payload"],
                        **{v[0]:v[1] for v in PINNED.values()}},
                "costs":{**dict(costs),"forward_ADD":forward,"ground_pure_Y_inverse_ADD":pure,
                         "forward_plus_pure_inverse_ADD":forward+pure,
                         "INIT":captures,"dirty_CLEAR":captures,
                         "extra_peak_per_F":max(per_F_early.values())*COPIES*DEGREE,
                         "extra_peak_all_F":captures,"extra_MOVE":0},
                "negative_controls":{"all_singleton_scales_one_fails":failures},
                "endpoint_inverse_equality":False,"new_kappa":False}
        all_results[variant]=result
        (args.out/(variant.upper()+"-SINGLETON-MINORS.json")).write_text(json.dumps(minors,separators=(",",":"))+"\n")
        (args.out/(variant.upper()+"-WORD-HASHES.json")).write_text(json.dumps(hashes,sort_keys=True,indent=2)+"\n")
        print(json.dumps({k:result[k] for k in ("status","variant","costs","negative_controls")}),flush=True)
    (args.out/"RESULT.json").write_text(json.dumps(all_results,indent=2,sort_keys=True)+"\n")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--k-words",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    variants(p.parse_args())
