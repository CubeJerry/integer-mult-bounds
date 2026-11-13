#!/usr/bin/env python3
"""Independent subset and finite zero-MOVE-direction recheck.

Inputs are the fresh native replay in ARRANGEMENT-REPLAY.json plus pinned
native ROWS and invoice. A/B outputs are read only for final comparison.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip, importlib.util, json, sys, time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PIN="acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
ROWS_PIN="15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834"
CALLER_PIN="255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc"
EVENTS=[30581,30593,35152,35448,35452,36346,36358,39875,39884,41646,42487,42500,44253,45656]
K=Q(19,5000)
OUT=HERE/"ONE-RELATION-RECHECK.json"

def need(ok,msg):
    if not ok: raise ValueError(msg)
def add(a,b,c=Q(1)):
    for h,x in b.items():
        z=a.get(h,Q(0))+c*x
        if z:a[h]=z
        else:a.pop(h,None)
def reduce(v,basis):
    v=v.copy()
    for p in sorted(basis):
        if v.get(p): add(v,basis[p],-v[p])
    return v
def insert(basis,row):
    v=reduce(row,basis)
    if not v:return False
    p=min(v);q=v[p]
    basis[p]={h:x/q for h,x in v.items()}
    return True
def decode(obj):return {int(h):Q(x) for h,x in obj.items()}
def dbasis(obj):return {int(p):decode(row) for p,row in obj.items()}
def enc(row):return tuple((h,x/row[min(row)]) for h,x in sorted(row.items())) if row else ()
def plus_basis(a,b):
    z={p:r.copy() for p,r in a.items()}
    for r in b.values():insert(z,r)
    return z
def intersect(a,b):
    # Kernel of reduction A -> V/B, retaining exact lift rows.
    im={};imlift={};ker={}
    for orig in a.values():
        v=reduce(orig,b); lift=orig.copy()
        for p in sorted(im):
            if v.get(p):
                q=-v[p];add(v,im[p],q);add(lift,imlift[p],q)
        if v:
            p=min(v);q=1/v[p]
            im[p]={h:q*x for h,x in v.items()}
            imlift[p]={h:q*x for h,x in lift.items()}
        else:insert(ker,lift)
    return ker
def info_subspace(a):
    return {"dim":len(a),"support":sorted(set().union(*(set(r) for r in a.values())) if a else set())}

def main():
    t0=time.monotonic()
    replay=json.loads((HERE/"ARRANGEMENT-REPLAY.json").read_text())
    need(replay["source_sha256"]==PIN,"fresh arrangement source binding")
    wordraw=(ROOT/"reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(wordraw).hexdigest()==PIN,"word byte pin")
    word=json.loads(gzip.decompress(wordraw))
    need(replay["source_payload_sha256"]==sha256(json.dumps(word,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"source payload binding")
    sites={int(e):s for e,s in replay["site_spaces"].items()}
    site_bases={e:dbasis(s["helper_extension_basis"]) for e,s in sites.items()}
    histories={e:dbasis(s["history_basis"]) for e,s in sites.items()}
    site_rank={e:int(s["target_rank"]) for e,s in sites.items()}
    T={h:abs(len(word["frames"][word["initial"][h]])-len(word["frames"][word["final"][h]]))
       for h in range(word["public"]) if h not in (set(word["live"])|{x+112 for x in word["live"]}|set(word["hosted"]["X2"])|set(word["hosted"]["Y2"]))}

    # Exhaust all 16,383 subsets, using the fresh L_E bases above.
    subset_spaces={0:{}}
    eligible=[];zero=0;hist_blocked=0
    for mask in range(1,1<<len(EVENTS)):
        bit=mask&-mask
        i=bit.bit_length()-1;ev=EVENTS[i];parent=mask^bit
        space=site_bases[ev] if not parent else intersect(subset_spaces[parent],site_bases[ev])
        subset_spaces[mask]=space
        if not space:
            zero+=1;continue
        member_events=[EVENTS[j] for j in range(len(EVENTS)) if mask>>j&1]
        not_contained=[]
        for e in member_events:
            if any(reduce(v,histories[e]) for v in space.values()):not_contained.append(e)
        if not not_contained:
            hist_blocked+=1;continue
        support=set().union(*(set(v) for v in space.values()))
        need(support<=set(T),"helper support only")
        cheapest=min(T[h] for h in support)
        eligible.append({"mask":mask,"events":member_events,"dim":len(space),
            "support_count":len(support),"cheapest_target_rank":cheapest,
            "site_move_ranks":[site_rank[e] for e in member_events]})
    need((zero,hist_blocked,len(eligible))==(16366,0,17),"complete subset eligibility census")
    need([x["events"] for x in eligible if len(x["events"])>1]==[
        [35448,35452],[39875,39884],[35152,45656]],"only three eligible pairs")
    need(all(len(x["events"])<=2 for x in eligible),"no eligible larger subset")

    # Directed price engine is used only after the exact vector census.
    pricepath=ROOT/"budget_price.py"
    pricehash=sha256(pricepath.read_bytes()).hexdigest()
    need(pricehash=="527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb","price engine pin")
    spec=importlib.util.spec_from_file_location("one_relation_price",pricepath)
    P=importlib.util.module_from_spec(spec);sys.modules[spec.name]=P;spec.loader.exec_module(P)
    invoice_raw=P.INVOICE.read_bytes();need(sha256(invoice_raw).hexdigest()==P.PIN,"invoice byte pin")
    invoice=json.loads(invoice_raw)
    need(sha256(json.dumps(word,sort_keys=True,separators=(",",":")).encode()).hexdigest()==invoice["new_native"],"current native invoice binding")
    caller_raw=(ROOT/"reference/pr7481/CALLER-EXACT.json").read_bytes()
    need(sha256(caller_raw).hexdigest()==CALLER_PIN,"exact caller byte pin")
    caller=json.loads(caller_raw)
    calls=sum(event[0]=="J" for event in caller["events"])
    need(calls==caller["stages"]==17,"full signed invoice 17-call binding")
    Tinv,Pinv=invoice["after"]["T"],invoice["after"]["P"]
    baseline={int(r):Tinv.get(r,0)-Pinv.get(r,0) for r in Tinv.keys()|Pinv.keys()}
    baseline=P.moment(baseline,K)

    def price_linear(coeffs):
        lo=hi=Q(0)
        for rank,count in coeffs.items():
            pl,ph=P.price(rank,K)
            if count>=0:lo+=count*pl;hi+=count*ph
            else:lo+=count*ph;hi+=count*pl
        return lo,hi
    codim_bound=price_linear({5:1,1:1,4:-1})
    needed=(-baseline[1]/17,-baseline[0]/17)
    need_gap=(needed[0]-codim_bound[1],needed[1]-codim_bound[0])
    codim_complete=(baseline[0]+17*codim_bound[0],baseline[1]+17*codim_bound[1])
    need(replay["site_group_dimension_sum"]==96==replay["site_group_joint_rank"] and
         replay["site_groups_direct_sum"],"independent 11-group direct-sum receipt")
    codim_summary={"assumption":"Homogeneous scalar-linear helper rowspace with surjective retained-coordinate projection; unchanged strict same-chart histories; cache-only, no zero-MOVE credits.",
        "sum_site_dimensions":replay["sum_dimensions"],"global_site_rank":replay["global_rank"],
        "group_count":len(replay["site_groups"]),"group_dimension_sum":replay["site_group_dimension_sum"],
        "group_joint_rank":replay["site_group_joint_rank"],"groups":replay["site_groups"],
        "net_upper_bound_expression":"f(5)+f(1)-f(4)","net_upper_bound":P.display(codim_bound),
        "required_native_saving":P.display(needed),"required_minus_bound":P.display(need_gap),
        "17_call_complete_moment_upper_bound":P.display(codim_complete),
        "actual_lost_price":"at least the minimum priced coordinate basis beta(U); beta(U) is a lower bound, not an asserted equality"}
    one_rows=[]
    for rec in eligible:
        gain=Counter(site_rank[e] for e in rec["events"])
        gain[rec["cheapest_target_rank"]]-=1
        gain={int(r):c for r,c in gain.items() if c}
        nativ=P.moment(gain,K)
        complete=P.moment({r:baseline_count+17*gain.get(r,0) for r,baseline_count in
                           ({int(r):Tinv.get(r,0)-Pinv.get(r,0) for r in Tinv.keys()|Pinv.keys()}).items()},K)
        rec.update({"rank_gain_profile":{str(r):c for r,c in sorted(gain.items())},
            "native_saving":P.display(nativ),"complete_moment":P.display(complete),
            "complete_positive":complete[0]>0})
        one_rows.append(rec)
    best=max(one_rows,key=lambda x:Q(x["native_saving"]["exact"][0]))
    need(best["events"]==[41646],"best one-relation no-zero-MOVE site")
    need(not any(r["complete_positive"] for r in one_rows),"one-relation cache subsets do not clear complete deficit")

    # Reconstruct B's 468 main-free move rows from this replay, then scan the
    # 1101 coordinate-unit + all row-direction classes against fresh P_E.
    rowsraw=(ROOT/"worker-b/helper-graph/ROWS.json").read_bytes()
    need(sha256(rowsraw).hexdigest()==ROWS_PIN,"independent ROWS snapshot pin")
    author_rows=json.loads(rowsraw)
    own_rows=replay["mainfree_MOVEs"]
    need(len(own_rows)==468==author_rows["main_free_moves"],"complete main-free MOVE census")
    author_by_event={r["event"]:r for r in author_rows["records"]}
    need(len(author_by_event)==468,"unique author row event IDs")
    for r in own_rows:
        a=author_by_event[r["event"]]
        need(all(r[k]==a[k] for k in ("event","owner","owned","rank","row")),"fresh replay vs 468-row record")
    helpers=sorted(T)
    directions={enc({h:Q(1)}):{"unit":h,"moves":[]} for h in helpers}
    for r in own_rows:
        key=enc(decode(r["row"]))
        directions.setdefault(key,{"unit":None,"moves":[]})["moves"].append(r)
    need(len(directions)==1425,"unit plus normalized MOVE direction classes")
    target_rows={e:decode(s["target_row"]) for e,s in sites.items()}
    queries={}
    for e in EVENTS:
        p=histories[e]
        tr=reduce(target_rows[e],p)
        need(tr,"all 14 full targets outside full history")
        queries[e]=(p,tr)
    # Check exact quotient proportionality in the fresh spaces. A direction
    # enables a cache only when its own history residual is nonzero and the
    # target residual is a nonzero scalar multiple of it.
    def enable(e,u):
        p,tr=queries[e]
        ur=reduce(u,p)
        if not ur or enc(ur)!=enc(tr): return None
        return tr[min(tr)]/ur[min(ur)]
    candidates=[];native_positive=[];complete_positive=[];cache_hits=0;multi_hits=0
    best_b=None
    for idx,(key,meta) in enumerate(directions.items()):
        u=dict(key)
        hits=[]
        for e in EVENTS:
            alpha=enable(e,u)
            if alpha is not None:
                hits.append({"event":e,"rank":site_rank[e],"alpha":str(alpha)})
        benefits={r["event"]:r for r in meta["moves"]}
        for hit in hits:
            if hit["event"] in benefits:
                need(benefits[hit["event"]]["rank"]==hit["rank"],"cache/zero-MOVE event has same original rank")
            benefits[hit["event"]]=hit
        # A direction with no enabled event is retained: its sole optimistic
        # effect is still charged for one demoted helper target.
        h=min(u,key=lambda z:(T[z],z))
        profile=Counter(int(r["rank"]) for r in benefits.values())
        profile[T[h]]-=1
        profile={r:c for r,c in profile.items() if c}
        nativ=P.moment(profile,K)
        complete=P.moment({r:(Tinv.get(str(r),0)-Pinv.get(str(r),0))+17*profile.get(r,0)
                           for r in set(map(int,Tinv))|set(map(int,Pinv))|set(profile)},K)
        rec={"id":idx,"direction_dimension":1,"unit":meta["unit"],
            "direction":{str(z):str(v) for z,v in key},
            "zero_MOVE_events":[r["event"] for r in meta["moves"]],
            "cache_events":[x["event"] for x in hits],"lost_helper":h,
            "lost_helper_rank":T[h],"gain_profile":{str(r):c for r,c in sorted(profile.items())},
            "native_saving":P.display(nativ),"complete_moment":P.display(complete),
            "complete_positive":complete[0]>0,
            "all_support_matching_boundaries":len({(word["initial"][z],word["final"][z]) for z in u})==1}
        candidates.append(rec)
        if hits:cache_hits+=1
        if len(hits)>1:multi_hits+=1
        if nativ[0]>0:native_positive.append(idx)
        if complete[0]>0:complete_positive.append(idx)
        if best_b is None or complete[0]>best_b[0]:best_b=(complete[0],rec)
    need(cache_hits==5 and multi_hits==0,"B exact cache direction census")
    need(len(native_positive)==1,"single native-positive direction")
    need(not complete_positive,"no finite zero-MOVE direction clears full gate")
    best_positive_native=candidates[native_positive[0]]
    need(best_positive_native["zero_MOVE_events"] and best_positive_native["cache_events"]==[42500],"positive direction includes original zero MOVE and one site")
    # Whole one-relation completeness partition: either u is proportional to
    # at least one native main-free MOVE (covered by the 468 rows above), or
    # it earns no zero-MOVE deletion and the arbitrary-space subset proof
    # above handles every enabled-cache set.
    row_direction_keys={enc(decode(r["row"])) for r in own_rows}
    need(len(row_direction_keys)<=468 and len(row_direction_keys)>0,"finite zero-MOVE direction representatives")

    result={"status":"INDEPENDENT_ONE_RELATION_AND_ANY_CODIM_CACHE_ONLY_RECHECK",
        "source_sha256":PIN,"source_payload_sha256":replay["source_payload_sha256"],
        "arrangement_receipt_sha256":sha256((HERE/"ARRANGEMENT-REPLAY.json").read_bytes()).hexdigest(),
        "row_snapshot_sha256":ROWS_PIN,"price_engine_sha256":pricehash,"invoice_sha256":P.PIN,
        "caller_sha256":CALLER_PIN,"native_calls":calls,
        "all_nonempty_subsets":16383,"zero_intersections":zero,"history_blocked_nonzero_subsets":hist_blocked,
        "eligible_subsets":len(eligible),"eligible":one_rows,
        "one_relation_best":best,"one_relation_any_complete_positive":False,
        "B_direction_count":len(directions),"B_cache_enabling_directions":cache_hits,
        "B_multisite_directions":multi_hits,"B_native_positive_directions":native_positive,
        "B_complete_positive_directions":complete_positive,
        "B_best_complete_direction":best_b[1],"B_positive_native_direction":best_positive_native,
        "B_direction_census":candidates,"baseline_complete_moment":P.display(baseline),
        "codimension_cache_only_bound":codim_summary,
        "one_relation_scope":"Any single homogeneous helper-only relation. A covers every no-zero-MOVE direction through the exact 16,383-subset census; the independent 468-row replay covers every direction proportional to a paid main-free MOVE, with original event credits unioned once. Only strict earlier same-chart original histories; no changed providers or imported cross-chart observations.",
        "codimension_scope":"Cache-only arbitrary relation subspace, no additional zero-MOVE event credits. Cached MOVE gains use the 14 unchanged-history sites; helper relation target loss is bounded below by minimum priced coordinate basis.",
        "elapsed_seconds":time.monotonic()-t0}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="B_direction_census"},indent=2))
if __name__=="__main__":main()
