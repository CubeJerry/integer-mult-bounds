#!/usr/bin/env python3
"""Reachability of all true pre-K owners from complementary native donors."""
import argparse
from collections import Counter
import ctypes
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

ROWS_12 = (13,22,28,37,43,48,55,65,72,81,90,101)
ROWS_19 = (0,5,16,26,32,34,36,38,39,42,51,58,63,71,94,99,103,107,108)

def load(name,path):
    sys.path.insert(0,str(path.parent.resolve()))
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def selected_weights(counts,budget):
    total=0
    for n,w in enumerate(sorted(counts,reverse=True),1):
        total+=w
        if total>=budget:return n
    return None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("repo","replay","engine","h-words","d-words","stream-lib","out"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--sector",choices=("small","large"),required=True)
    p.add_argument("--rows",choices=("12","19"),default="19")
    p.add_argument("--batch",type=int,default=64)
    a=p.parse_args()
    alg=load("native_cascade",a.replay/"check.py")
    engine=load("exact_field_stream",a.engine/"check.py").Engine(a.stream_lib)
    alg.mm=engine.mm
    nat=alg.Native(a)
    rows=ROWS_12 if a.rows=="12" else ROWS_19
    donors=[j for j in range(111) if j not in rows]
    planes={h for i in rows for h in nat.planes[i]}
    marks=a.sector=="small";s,w=(0,96) if marks else (96,384)
    all_owners=sorted(t for t,route in nat.rt.items() if route[5] in planes)
    owners=[t for t in all_owners if (nat.rt[t][4] in nat.mark)==marks]
    n=len(owners)
    alg.need(len(all_owners)==90*len(planes) and n==(18 if marks else 72)*len(planes),"K input owner census")
    lookup={t:k for k,t in enumerate(owners)}
    counts=Counter(nat.rt[t][4] for t in all_owners)
    hcounts=Counter(r[3] for r in nat.rt.values() if r[3] is not None and r[4] in counts)
    engine.lib.pivot_columns.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    engine.lib.pivot_columns.restype=None
    state=engine.lib.begin(n);alg.need(state,"stream allocation")
    payload=hashlib.sha256();steps={};column_count=0
    a.out.mkdir(parents=True,exist_ok=True)
    try:
        for j in donors:
            vals=nat.through_d(j,rows,marks)
            relevant=[t for t in vals if t in lookup]
            packet=np.zeros((w,n),dtype=np.uint8)
            if relevant:
                packet[:,[lookup[t] for t in relevant]]=np.stack([vals[t][s:s+w] for t in relevant]).T
            # The D marking fixes the H source sector independently of the K maps.
            outside=slice(96,480) if marks else slice(0,96)
            alg.need(all(not vals[t][outside].any() for t in relevant),"off-sector zeros")
            payload.update(memoryview(packet))
            for pos in range(0,w,a.batch):
                part=packet[pos:pos+a.batch]
                alg.need(engine.lib.consume(state,part.ctypes.data,len(part)),"streamed input columns")
            column_count+=w
            rank=engine.lib.present_rank(state);steps[j]=rank
            if len(steps)%12==0 or rank==n:
                print(a.rows,a.sector,"donors",len(steps),"rank",rank,"target",n,flush=True)
            if rank==n:break
        rank=engine.lib.present_rank(state);det=int(engine.lib.determinant(state))
        chosen=np.empty(rank,dtype=np.uint32);engine.lib.pivot_columns(state,chosen.ctypes.data)
        alg.need(len(set(map(int,chosen)))==rank and max(chosen,default=0)<column_count,"selected native columns")
        if rank==n:alg.need(det!=0,"invertible minor")
        # Store the indices in the chronological input sequence donor then source field coordinate.
        piv=json.dumps(chosen.tolist(),separators=(",",":")).encode()
        (a.out/f"{a.sector.upper()}-PIVOTS.json.gz").write_bytes(gzip.compress(piv,mtime=0))
        nr=len(rows);g=max(0,(nr-9)*480-16)
        result={"rows":list(rows),"donors":donors,"touched_K":len(planes),"sector":a.sector,"source_width":w,
                "all_K_inputs":len(all_owners),"actual_K_inputs_this_sector":n,"read_source_columns":column_count,
                "rank":rank,"row_deficiency":n-rank,"certificate_minor_determinant":det,
                "transpose_prefix_sha256":payload.hexdigest(),"selected_columns_sha256":hashlib.sha256(piv).hexdigest(),
                "rank_after_donor":steps,"owners_indices_sha256":hashlib.sha256(np.asarray(owners,dtype='>u4').tobytes()).hexdigest(),
                "D_region_holder_histogram":dict(sorted(Counter(counts.values()).items())),
                "D_charts_to_affect_for_m870_if_full_reach":selected_weights(counts.values(),g),
                "H_region_holder_histogram":dict(sorted(Counter(hcounts.values()).items())),
                "H_charts_to_affect_for_m870_if_full_reach":selected_weights(hcounts.values(),g),
                "donor_banks_to_affect_for_m870_if_full_reach":(g+479)//480,
                "pins":{"source_geometry":alg.PINS["layout"][1],"native_routes":alg.PINS["routes"][1],
                        "word_H":alg.H_WORD[1],"word_D":alg.D_CHARTS[1]}}
        (a.out/(a.sector.upper()+".json")).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        print(a.rows,a.sector,"rank",rank,"minor",det,flush=True)
    finally:
        engine.lib.finish(state)

if __name__=="__main__":main()
