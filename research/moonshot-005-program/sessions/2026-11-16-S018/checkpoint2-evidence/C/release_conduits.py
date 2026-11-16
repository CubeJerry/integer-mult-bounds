#!/usr/bin/env python3
"""Protect existing native-to-ground packet suffixes and release78 originals.

Five existing packets have a zero state at their final native-point load,
then read only their own output.  Their native raw caches and final suffixes
can be protected while every other old use of those coordinates is projected.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from release_projection import BACKUPS, PIN, N, binary_basis, replay, require, same_span

CONDUITS = {
    7: ("RAW7", "P0", []),
    11: ("RAW11", "P1", []),
    12: ("RAW12", "P2", ["E77"]),
    19: ("HRAW19", "P6", ["E75", "E77", "E79"]),
    27: ("HRAW27", "P7", ["E1", "E73", "E75", "E79"]),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a = ap.parse_args()
    path = a.repo/"research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json"
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,"base pin")
    w=json.loads(raw)
    before, old_trace, old_live = replay(w,collect=True)
    mutable={int(o[2][1:]) for o in w["operations"] if o[0]=="ADD" and o[2].startswith("X")}
    ds=(set(range(N))-set(w["targets"])-mutable)|set(BACKUPS)|set(CONDUITS)
    require(len(ds)==78 and not ds&mutable,"78 immutable originals")
    captures={**BACKUPS, **{d:r for d,(r,p,mask) in CONDUITS.items()}}
    protected=set(captures.values())
    cuts={}
    for d,(r,p,mask) in CONDUITS.items():
        require([o for o in w["operations"] if o[0]=="ADD" and o[2]==r]==[["ADD",f"X{d}",r]],"pure native conduit cache")
        require([o for o in w["operations"] if o[0]=="INIT" and o[1]==r]==[["INIT",r,f"L{d}"]],"native conduit birth")
        require(not any(o[0]=="MOVE" and o[1]==r for o in w["operations"]),"stationary native cache")
        load=next(k for k,o in enumerate(w["operations"]) if o==["ADD",r,p])
        read=next(k for k,o in enumerate(w["operations"]) if o==["ADD",p,f"Y{d}"])
        require(old_trace[load][0][p]==0,"actual packet zero before native protected load")
        require(all(o==["ADD",p,f"Y{d}"] for o in w["operations"][load+1:] if o[0]=="ADD" and o[1]==p),"protected suffix has only own output reader")
        require(old_trace[read][1][p]==old_trace[read][1][f"Y{d}"]=="zero","actual ground conduit reader")
        value=old_trace[read][0][p]
        for b in mask:
            require(old_trace[read][1][b]=="zero","actual ground mask available")
            value^=old_trace[read][0][b]
        require(value==1<<d,"actual pure raw extraction recipe")
        cuts[d]={"native_load_old_index":load,"own_reader_old_index":read,"native_owner":r,"packet":p,"ground_mask":mask}
    new_ops=[]; mapping={};removed=[];inserted=[];repaired=set();interface=None
    for k,o in enumerate(w["operations"]):
        op,n,*q=o
        if op=="MOVE" and n.startswith("X") and int(n[1:]) in ds:
            removed.append({"index":k,"operation":o,"reason":"free original route"});continue
        if op=="ADD" and n.startswith("X") and int(n[1:]) in ds:
            d=int(n[1:])
            if q[0]!=captures.get(d):
                removed.append({"index":k,"operation":o,"reason":"projected original read"});continue
        if op=="ADD" and n in protected:
            permitted=any(k==c["native_load_old_index"] for c in cuts.values())
            if not permitted:
                removed.append({"index":k,"operation":o,"reason":"projected protected-cache read"});continue
        if op=="MOVE" and n.startswith("Y") and int(n[1:]) in BACKUPS:
            d=int(n[1:])
            if d not in repaired:
                z=["ADD",BACKUPS[d],n]
                inserted.append({"index":len(new_ops),"operation":z,"reason":"independent native backup endpoint repair"})
                new_ops.append(z);repaired.add(d)
        if op=="CLEAR" and interface is None:
            interface=len(new_ops)
            for d in sorted(ds):
                z=["MOVE",f"X{d}","Hub"]
                inserted.append({"index":len(new_ops),"operation":z,"reason":"raw carrier closure control"})
                new_ops.append(z)
        mapping[k]=len(new_ops)
        new_ops.append(o)
    new={k:copy.deepcopy(w[k]) for k in ("source_path","source_sha256","charts","targets")}
    new.update(schema="protected-native-conduit-source-projection-v1",base_word_sha256=PIN,
               released_carriers=sorted(ds),protected_native_ground_backups={str(k):v for k,v in BACKUPS.items()},
               protected_native_conduits={str(k):v for k,v in cuts.items()},
               carrier_interface_before_operation=interface,operations=new_ops,
               scope="All46 endpoints/all222 columns preserved,78 immutable original routes detached;15 completed carriers have actual protected native-to-ground data through10 dedicated returns and5 existing packet suffixes. Higher source/history values are projected.63 released unfinished input directions still need new acquisition/delivery. No new complete supplier or kappa.")
    after,tr,live=replay(new,collect=True)
    dm=sum(1<<d for d in ds);xnames={f"X{d}" for d in ds};checks=0
    for oldk,newk in mapping.items():
        ov,oa=old_trace[oldk];nv,na=tr[newk]
        for n,row in ov.items():
            if n in xnames or n in protected:continue
            want=row&~dm
            if n.startswith("Y") and n[1:].isdigit():
                d=int(n[1:])
                if d in BACKUPS and (na[n]!="zero" or new_ops[newk][0:2]==["MOVE",n]):want^=1<<d
                if d in cuts and oldk>cuts[d]["own_reader_old_index"]:want^=1<<d
            for d,c in cuts.items():
                if n==c["packet"] and oldk>c["native_load_old_index"]:want^=1<<d
            require(nv[n]==want,("covariance",oldk,newk,n,hex(nv[n]),hex(want)))
            require(oa[n]==na[n],("unchanged location",oldk,n))
            checks+=1
    cv,ca=tr[interface]
    require(all(cv[f"X{d}"]==1<<d and ca[f"X{d}"]==f"L{d}" for d in ds),"actual78 native carriers")
    require(all(cv[f"X{i}"]==1<<i and ca[f"X{i}"]=="Hub" for i in set(range(N))-ds),"other33 rawHub")
    old_ground=[z for n,z in old_live[1].items() if old_live[2][n]=="zero" and z>>N==0]
    new_ground=[z for n,z in cv.items() if ca[n]=="zero" and z>>N==0]
    require(same_span(old_ground,new_ground),"same actual25-dimensional common source")
    actual_raw={}
    for d,c in cuts.items():
        names=[c["packet"]]+c["ground_mask"]
        z=0
        for n in names:
            require(ca[n]=="zero","joint extraction fields")
            z^=cv[n]
        require(z==1<<d,"joint exact raw extraction")
        actual_raw[d]=names
    controls=[]
    for d in CONDUITS:
        c=cuts[d]
        for op in (["ADD",f"X{d}",c["native_owner"]],
                   ["ADD",c["native_owner"],c["packet"]],
                   ["ADD",c["packet"],f"Y{d}"]):
            bad=copy.deepcopy(new);bad["operations"].remove(op)
            try:replay(bad)
            except (ValueError,KeyError) as e:controls.append({"omitted":op,"rejected":str(e)})
            else:raise ValueError(("accepted omission",op))
    a.out.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(new,indent=2)+"\n").encode();(a.out/"WORD.json").write_bytes(data)
    result={"status":"PASS_PROTECTED_NATIVE_CONDUITS_RELEASE78","base_word_sha256":PIN,
            "word_sha256":hashlib.sha256(data).hexdigest(),"native_source_sha256":w["source_sha256"],
            "released_carriers":sorted(ds),"before":before,"after":after,
            "retained_covariant_state_checks":checks,"target_count":46,
            "carrier_interface_before_operation":interface,"all78_originals_raw_native":True,
            "other_originals_raw_Hub":33,"actual_common_rank":len(binary_basis(new_ground)),
            "actual_common_space_unchanged":True,"actual_new_protected_raw_recipes":actual_raw,
            "native_conduit_certificates":cuts,"removed":removed,"inserted":inserted,
            "controls":controls,"scope":new["scope"],"new_complete_kappa":False}
    (a.out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","word_sha256","after","retained_covariant_state_checks","actual_common_rank")}))


if __name__=="__main__":main()
