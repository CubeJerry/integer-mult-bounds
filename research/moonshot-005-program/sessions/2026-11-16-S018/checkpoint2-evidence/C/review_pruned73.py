#!/usr/bin/env python3
"""Independent review of A's released73 pruning and preserved live interface."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from release_projection import N, binary_basis, chart, replay, require
from price_projection import moment, record

BASE="01f93ac753a468829921a7a41fc4f49122c6e94e5a1ede0b2352459de13fca80"
WORD="e593a4ead404879ee3b5b74a66556af022c7c3b0bd58a77a2c69d5aad0a3e1b6"


def interface(w,tr):
    cut=w["carrier_interface_before_operation"]
    return tr[cut]


def check_interface(w,tr,expected,carriers):
    v,a=interface(w,tr)
    for n,row in expected.items():
        require(n in v and v[n]==row and not chart(w["charts"][a[n]]), ("actual common field",n))
    for d in carriers:
        require(v[f"X{d}"]==1<<d and a[f"X{d}"]==f"L{d}", ("released raw native original",d))
    return True


def main():
    ap=argparse.ArgumentParser()
    for name in ("repo","base","word","out"):
        ap.add_argument("--"+name,type=Path,required=True)
    a=ap.parse_args()
    bb=a.base.read_bytes();wb=a.word.read_bytes()
    require(hashlib.sha256(bb).hexdigest()==BASE,"base pin")
    require(hashlib.sha256(wb).hexdigest()==WORD,"word pin")
    old,new=json.loads(bb),json.loads(wb)
    require(old["charts"]==new["charts"],"immutable inherited chart definitions")
    src=(a.repo/new["source_path"]).read_bytes()
    require(hashlib.sha256(src).hexdigest()==new["source_sha256"],"native source pin")
    roots=json.loads(src)["native_roots"]
    for i,r in enumerate(roots):
        require(chart(new["charts"][f"L{i}"])==chart({"kind":"span","rows":[r]}),("native line",i))
        require(chart(new["charts"][f"F{i}"])==chart({"kind":"ann","rows":[r]}),("native facet",i))
    before,bt,bl=replay(old,collect=True)
    after,nt,nl=replay(new,collect=True)
    bv,ba=interface(old,bt)
    owned={o[1] for o in old["operations"] if o[0]=="INIT"}
    expected={n:z for n,z in bv.items() if n in owned and z and not chart(old["charts"][ba[n]])}
    require(set(expected)==set(new["preserved_common_fields"]),"complete actual common-field inventory")
    require(len(expected)==len(binary_basis(expected.values()))==25,"25 independent actual common fields")
    carriers=new["released_carriers"]
    require(carriers==old["released_carriers"] and len(carriers)==73,"same73 originals")
    check_interface(new,nt,expected,carriers)
    require(new["targets"]==old["targets"] and len(new["targets"])==46,"same46 endpoints")
    require(after["counts"]=={"INIT":94,"ADD":411,"MOVE":363,"CLEAR":94},"independent counts")
    require(after["movement_profile"]=={1:98,2:18,3:40,4:8,5:23,6:12,7:164},"independent movement profile")
    require(after["dirty_CLEAR"]==after["peak_owned"]==94,"independent owner accounting")
    Q=moment(after["movement_profile"]);oldQ=moment(before["movement_profile"])
    gate={127:37,64:74,1:-74}
    for j in range(1,9):
        gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    L=tuple(q/6 for q in moment(gate));room=L[0]-Q[1],L[1]-Q[0]
    controls=[]
    # Endpoint-preserving ground corruption demonstrates why the source
    # interface must be checked separately from the final original map.
    bad=copy.deepcopy(new);k=bad["carrier_interface_before_operation"]
    bad["operations"].insert(k,["ADD","COMMON_RAW2","P3"])
    bad["carrier_interface_before_operation"]+=1
    bs,tt,ll=replay(bad,collect=True)
    try:check_interface(bad,tt,expected,carriers)
    except ValueError as e:controls.append({"control":"changed actual common field after all old readers","all222_endpoints_still_pass":True,"interface_rejected":str(e)})
    else:raise ValueError("accepted common-field mutation")
    # Endpoint-preserving early original return destroys released custody.
    bad=copy.deepcopy(new);op=["MOVE","X0","Hub"];bad["operations"].remove(op)
    k=bad["carrier_interface_before_operation"]
    bad["operations"].insert(k,op);bad["carrier_interface_before_operation"]+=1
    bs,tt,ll=replay(bad,collect=True)
    try:check_interface(bad,tt,expected,carriers)
    except ValueError as e:controls.append({"control":"carrier returned before declared open interface","all222_endpoints_still_pass":True,"interface_rejected":str(e)})
    else:raise ValueError("accepted lost carrier custody")
    for op in (["CLEAR","P3"],["ADD","ADDED_RAW50","Y50"]):
        bad=copy.deepcopy(new);bad["operations"].remove(op)
        try:replay(bad)
        except (ValueError,KeyError) as e:controls.append({"omitted":op,"rejected":str(e)})
        else:raise ValueError(("accepted endpoint/lifetime mutation",op))
    result={"status":"PASS_C_INDEPENDENT_PRUNED73_INTERFACE_REVIEW",
        "base_word_sha256":BASE,"word_sha256":WORD,"native_source_sha256":new["source_sha256"],
        "method":"Separate exact rational chart and222-column interpreter; no A code imported. Actual native source pinned, all25 common values and73 native originals reconstructed at declared cut. Independent integer-root price and endpoint-preserving interface controls.",
        "before":before,"after":after,"interface_index":new["carrier_interface_before_operation"],
        "actual_common_fields":{n:hex(z) for n,z in expected.items()},"common_rank":25,
        "all73_originals_native_raw":True,"target_count":46,
        "price":{"moment":record(Q),"before_moment":record(oldQ),
                 "change":record((Q[0]-oldQ[1],Q[1]-oldQ[0])),"necessary_limiting_room":record(room)},
        "controls":controls,
        "scope":"Actual endpoint and named common-interface preservation; old higher-chart source/history claims are not inherited. Formal native all-width identity, not complete supplier admission or a new kappa."}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"],result["price"]["moment"]["decimal"],result["price"]["necessary_limiting_room"]["decimal"])


if __name__=="__main__":main()
