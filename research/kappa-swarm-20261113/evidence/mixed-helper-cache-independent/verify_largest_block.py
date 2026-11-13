#!/usr/bin/env python3
"""Fresh exact audit of the 14-zero/two-cache largest mixed component."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip,importlib.util,json,sys,time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PIN="acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
K=Q(19,5000)
ZERO_EVENTS=[32681,39855,39857,39859,45659,45661,45663,45698,45701,45706,51637,57989,58936,76469]
REQ=[45659,45661,45663,58936]

def need(ok,msg):
    if not ok:raise ValueError(msg)
def add(a,b,c=Q(1)):
    for h,x in b.items():
        z=a.get(h,Q(0))+c*x
        if z:a[h]=z
        else:a.pop(h,None)
def decode(row):return {int(h):Q(x) for h,x in row.items() if Q(x)}
def reduce(row,basis):
    v=row.copy()
    for p in sorted(basis):
        if v.get(p):add(v,basis[p],-v[p])
    return v
def insert(basis,row):
    v=reduce(row,basis)
    if not v:return False
    p=min(v);a=v[p];basis[p]={h:x/a for h,x in v.items()};return True
def encbasis(b):return {str(p):{str(h):str(x) for h,x in sorted(r.items())} for p,r in sorted(b.items())}

def quotient_system(rows,events):
    basis={};expressions={}
    for row,event in zip(rows,events):
        v=row.copy();rep={event:Q(1)}
        for p in sorted(basis):
            if v.get(p):
                c=-v[p];add(v,basis[p],c);add(rep,expressions[p],c)
        if v:
            p=min(v);c=1/v[p];basis[p]={h:c*x for h,x in v.items()};expressions[p]={e:c*x for e,x in rep.items()}
    return basis,expressions

def express(target,basis,expressions):
    v=target.copy();rep={}
    for p in sorted(basis):
        if v.get(p):
            c=v[p];add(v,basis[p],-c);add(rep,expressions[p],c)
    return v,{e:c for e,c in rep.items() if c}

def main():
    t0=time.monotonic()
    raw=(ROOT/"reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(raw).hexdigest()==PIN,"exact native word bytes")
    w=json.loads(gzip.decompress(raw))
    replay=json.loads((ROOT/"worker-c/combined-one-relation-review/ARRANGEMENT-REPLAY.json").read_text())
    need(replay["source_sha256"]==PIN,"fresh source replay pin")
    comp=json.loads((HERE/"UNION-CERTIFICATE.json").read_text())
    block=next(x for x in comp["cache_components"] if x["cache_sites"]==[35152,45656])
    need(block["zero_events"]==ZERO_EVENTS,"fresh component event list")
    rows={r["event"]:r for r in replay["mainfree_MOVEs"]}
    need(all(e in rows for e in ZERO_EVENTS),"all block zero MOVE rows source-derived")
    zero=[decode(rows[e]["row"]) for e in ZERO_EVENTS]
    paid={e:int(rows[e]["rank"]) for e in ZERO_EVENTS}
    need(len(set(ZERO_EVENTS))==14 and all(rows[e]["owned"]==False for e in ZERO_EVENTS),"zero MOVE event uniqueness and ownership metadata")
    mains=set(w["live"])|{h+112 for h in w["live"]}|set(w["hosted"]["X2"])|set(w["hosted"]["Y2"])
    helpers=set(range(w["public"]))-mains
    T={h:abs(len(w["frames"][w["initial"][h]])-len(w["frames"][w["final"][h]])) for h in helpers}
    zrank={}
    zsupport={}
    zspace={}
    for e,row in zip(ZERO_EVENTS,zero):
        need(row and set(row)<=helpers,"zero row is nonzero and helper-only")
        zrank[e]=rows[e]["rank"];zsupport[e]=sorted(row)
        need(all(T[h]>=zrank[e] for h in row),"every zero-row support target rank dominates paid rank")
        insert(zspace,row)
    need(len(zspace)==14,"all fourteen zero rows independent")
    need(all(T[h]>=4 for row in zero for h in row),"all zero-row support target ranks at least four")

    sites={int(e):s for e,s in replay["site_spaces"].items()}
    pspaces={e:{int(p):decode(r) for p,r in s["history_basis"].items()} for e,s in sites.items()}
    cache_targets={e:decode(sites[e]["target_row"]) for e in (35152,45656)}
    cache_ranks={e:int(sites[e]["target_rank"]) for e in (35152,45656)}
    cache_L={e:{int(p):decode(r) for p,r in sites[e]["helper_extension_basis"].items()} for e in (35152,45656)}
    support_min={e:min(T[int(h)] for h in sites[e]["support"]) for e in (35152,45656)}
    need(cache_ranks=={35152:2,45656:1},"cache native MOVE ranks")
    need(support_min=={35152:3,45656:4},"fresh individual L support target ranks")
    lunion={}
    for e in (35152,45656):
        for row in cache_L[e].values():insert(lunion,row)
    need(len(lunion)==19,"fresh cache-space sum rank")
    l_union_min=min(T[h] for row in lunion.values() for h in row)
    need(l_union_min==3,"fresh L union least support target rank")

    # Exact quotient histories and source rows; enumerate all 2^14 zero sets
    # to verify A(S), not just the all-zero endpoint.
    qrows={e:reduce(row,pspaces[45656]) for e,row in zip(ZERO_EVENTS,zero)}
    target_residual=reduce(cache_targets[45656],pspaces[45656])
    q351=reduce(cache_targets[35152],pspaces[35152])
    q351rows=[reduce(row,pspaces[35152]) for row in zero]
    q456rows=[qrows[e] for e in ZERO_EVENTS]
    enabled_masks={35152:[],45656:[]}
    seen=0
    for mask in range(1<<14):
        i=(mask&-mask).bit_length()-1 if mask else None
        parent=mask^(1<<i) if i is not None else 0
        # Dynamic subset row-space basis over the already history-quotiented
        # vectors, independently for each cache's destination chart.
        if mask==0:
            b351={};b456={}
        else:
            b351={p:r.copy() for p,r in spaces351[parent].items()}
            b456={p:r.copy() for p,r in spaces456[parent].items()}
            insert(b351,q351rows[i]);insert(b456,q456rows[i])
        if mask==0:
            spaces351={0:b351};spaces456={0:b456}
        else:
            spaces351[mask]=b351;spaces456[mask]=b456
        if not reduce(q351,b351):enabled_masks[35152].append(mask)
        if not reduce(target_residual,b456):enabled_masks[45656].append(mask)
        seen+=1
    need(seen==16384,"all zero-row subsets")
    need(not enabled_masks[35152],"site35152 never enabled by zero rows")
    required_mask=sum(1<<ZERO_EVENTS.index(e) for e in REQ)
    need(enabled_masks[45656]==[m for m in range(1<<14) if m&required_mask==required_mask],
         "site45656 zero-enabled iff all four necessary rows are present")
    basis,expr=quotient_system(q456rows,ZERO_EVENTS)
    rem,witness=express(target_residual,basis,expr)
    need(not rem and set(witness)==set(REQ),"exact 45656 zero-history witness support")
    essential=[]
    for e in REQ:
        other=[(row,ev) for row,ev in zip(q456rows,ZERO_EVENTS) if ev!=e]
        b,ex=quotient_system([x[0] for x in other],[x[1] for x in other])
        rr,_=express(target_residual,b,ex)
        need(rr,"each of the four zero rows is essential")
        essential.append({"event":e,"target_residual_without_event":{str(h):str(x) for h,x in sorted(rr.items())}})

    # Mandatory disjoint unit columns for the already-enabled case.
    unit_events=[45659,45661,45663]
    unit_coords=[]
    for e in unit_events:
        row=rows[e]["row"]
        need(len(row)==1,"mandatory row is unit")
        h=int(next(iter(row)))
        need(Q(next(iter(row.values())))==1 and T[h]==4 and paid[e]==1,"unit row has rank1 credit and rank4 target")
        need(all(h not in zero[j] for j,ev in enumerate(ZERO_EVENTS) if ev!=e),"unit coordinate is absent from all other rows")
        unit_coords.append(h)
    need(len(set(unit_coords))==3,"three mandatory unit target columns are disjoint")
    need(paid[58936]==5 and all(T[h]>=5 for h in zero[ZERO_EVENTS.index(58936)]),
         "fourth indispensable zero row rank5 is funded at target rank at least5")

    # Directed prices for the case refinements.
    pp=ROOT/"budget_price.py";need(sha256(pp.read_bytes()).hexdigest()=="527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb","price code pin")
    sp=importlib.util.spec_from_file_location("largest_block_price",pp);P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
    expressions={
        "case0_no_cache":{},
        "case0_cache45656":{1:4,4:-3},
        "new45656_grant_both_caches":{1:1,2:1,4:-1},
        "new35152_only":{2:1,3:-1},
        "new35152_after_case0_cache45656":{2:1,3:-1},
    }
    price_bounds={name:P.display(P.moment(hist,K)) for name,hist in expressions.items()}
    need(all(Q(v["exact"][1])<0 for name,v in price_bounds.items() if name!="case0_no_cache"),"all refined nonzero branches negative at .0038")
    need(4**99>3**100,"uniform 0..0.01 comparison 4^.99>3")

    result={"status":"FRESH_SOURCE_AUDIT_OF_14_ZERO_TWO_CACHE_REFINEMENT",
        "source_sha256":PIN,"source_payload_sha256":replay["source_payload_sha256"],
        "union_certificate_sha256":sha256((HERE/"UNION-CERTIFICATE.json").read_bytes()).hexdigest(),
        "zero_events":ZERO_EVENTS,"zero_move_row_rank":len(zspace),"zero_paid_ranks":{str(e):paid[e] for e in ZERO_EVENTS},
        "zero_support_min_target_rank_by_event":{str(e):min(T[h] for h in row) for e,row in zip(ZERO_EVENTS,zero)},
        "all_zero_support_target_ranks_at_least_four":True,"zero_credit_supported_by_matching":True,
        "mandatory_unit_events":unit_events,"mandatory_unit_helper_coordinates":unit_coords,
        "four_zero_events_required_for_cache45656":REQ,"cache45656_exact_zero_witness":{str(e):str(q) for e,q in witness.items()},
        "each_required_event_nonmembership_when_removed":essential,
        "all_zero_sets_checked":seen,"zero_enabled_masks":{"35152":len(enabled_masks[35152]),"45656":len(enabled_masks[45656])},
        "cache_35152_never_enabled_by_Z":True,"cache_45656_enabled_iff_all_four_required":True,
        "cache_MOVE_ranks":{str(e):cache_ranks[e] for e in cache_ranks},
        "cache_L_support_target_rank_minima":{str(e):support_min[e] for e in support_min},
        "L_union_rank":len(lunion),"L_union_support_minimum_target_rank":l_union_min,
        "price_branch_signed_profiles":{k:{str(r):c for r,c in v.items()} for k,v in expressions.items()},
        "price_branch_intervals_0038":price_bounds,"uniform_interval":["0","1/100"],
        "largest_component_upper_bound":0,
        "scope":"Fourteen-zero/two-cache component only; scalar-linear helper relations, unchanged original strict destination histories; zero-MOVE and cache upper bounds only. No physical relation or supplier.",
        "elapsed_seconds":time.monotonic()-t0}
    (HERE/"LARGEST-BLOCK-REVIEW.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
