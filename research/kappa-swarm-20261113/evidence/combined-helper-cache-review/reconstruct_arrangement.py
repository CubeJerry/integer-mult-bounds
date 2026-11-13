#!/usr/bin/env python3
"""Fresh exact native replay and 14-site helper-extension arrangement check.

The source word is the only source of target rows and earlier destination
histories. This script does not consume A/B residual-space outputs.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip, json, time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "ARRANGEMENT-REPLAY.json"
WORD = ROOT / "reference/pr7481/WORD.json.gz"
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
EXPECTED = [30581,30593,35152,35448,35452,36346,36358,39875,39884,41646,42487,42500,44253,45656]

def need(ok, label):
    if not ok:
        raise ValueError(label)

def plus(a, b, c=Q(1)):
    for h, x in b.items():
        z = a.get(h, Q(0)) + c*x
        if z:
            a[h] = z
        else:
            a.pop(h, None)

def reduce(v, basis):
    v = v.copy()
    for p in sorted(basis):
        if v.get(p):
            plus(v, basis[p], -v[p])
    return v

def insert(basis, row):
    v = reduce(row, basis)
    if not v:
        return False
    p = min(v)
    scale = v[p]
    basis[p] = {h:x/scale for h,x in v.items()}
    return True

def plus_basis(a,b):
    out={p:r.copy() for p,r in a.items()}
    for row in b.values():insert(out,row)
    return out

def frame_key(frame):
    span = {0}
    for v in frame:
        span |= {x ^ v for x in span}
    return tuple(sorted(span))

def encoded_basis(basis):
    return {str(p):{str(h):str(x) for h,x in sorted(v.items())}
            for p,v in sorted(basis.items())}

def decode_basis(obj):
    return {int(p):{int(h):Q(x) for h,x in row.items()}
            for p,row in obj.items()}

def kernel_lifts(rows, project):
    image = {}
    image_lifts = {}
    kernel = {}
    for original in rows:
        v = project(original)
        lift = original.copy()
        for p in sorted(image):
            if v.get(p):
                q = -v[p]
                plus(v, image[p], q)
                plus(lift, image_lifts[p], q)
        if v:
            p = min(v)
            q = 1/v[p]
            image[p] = {h:q*x for h,x in v.items()}
            image_lifts[p] = {h:q*x for h,x in lift.items()}
        else:
            insert(kernel, lift)
    return kernel, len(image)

def intersect(a, b):
    space, quotient_rank = kernel_lifts(list(a.values()), lambda r:reduce(r,b))
    need(len(space) + quotient_rank == len(a), "intersection kernel rank-nullity")
    need(all(not reduce(r,a) and not reduce(r,b) for r in space.values()),
         "intersection containment")
    joined = {}
    for r in list(a.values()) + list(b.values()):
        insert(joined,r)
    need(len(space) == len(a)+len(b)-len(joined), "intersection dimension identity")
    return space

def main():
    started = time.monotonic()
    raw = WORD.read_bytes()
    need(sha256(raw).hexdigest() == PIN, "exact #7481 compressed source pin")
    w = json.loads(gzip.decompress(raw))
    frames = list(map(frame_key,w["frames"]))
    n = w["public"]
    mains = set(w["live"]) | {h+112 for h in w["live"]} | set(w["hosted"]["X2"]) | set(w["hosted"]["Y2"])
    helpers = set(range(n)) - mains
    need((len(mains),len(helpers)) == (400,1101), "source main/helper partition")
    cuts = {i:e for i,e in enumerate(w["program"]) if e[0] == "MOVE" and e[4]}
    need(len(cuts)==47, "all owned MOVE cuts")
    target_frames = {frames[e[3]] for e in cuts.values()}
    arrivals = {f:[] for f in target_frames}
    # All input variables begin as independent coordinate rows.
    rows = [{h:Q(1)} for h in range(n)] + [None]*w["owned_fields"]
    charts = w["initial"].copy() + [None]*w["owned_fields"]
    for h, f in enumerate(w["initial"]):
        if frames[f] in arrivals:
            arrivals[frames[f]].append((-1,rows[h].copy()))
    cuts_at = {}
    mainfree_moves = []
    op_counts = Counter()
    for event, ins in enumerate(w["program"]):
        op_counts[ins[0]] += 1
        op, a = ins[:2]
        if op == "MOVE":
            old,new = ins[2:4]
            need(charts[a] == old and rows[a] is not None, "MOVE source chart/value")
            if rows[a] and set(rows[a]) <= helpers:
                mainfree_moves.append({"event":event,"owner":a,"owned":bool(ins[4]),
                    "rank":abs(len(w["frames"][old])-len(w["frames"][new])),
                    "row":{str(h):str(x) for h,x in sorted(rows[a].items())}})
            if ins[4]:
                cuts_at[event] = (a,old,new,rows[a].copy())
            charts[a] = new
            if frames[new] in arrivals:
                arrivals[frames[new]].append((event,rows[a].copy()))
        elif op == "INIT":
            need(a >= n and charts[a] is None and rows[a] is None, "owned INIT lifecycle")
            charts[a], rows[a] = ins[2], {}
        elif op == "CLEAR":
            need(a >= n and charts[a] == ins[2] and rows[a] is not None, "owned CLEAR lifecycle")
            charts[a], rows[a] = None, None
        elif op == "SCALE":
            need(charts[a] == ins[3] and rows[a] is not None, "SCALE coframe")
            q = Q(ins[2]); need(q, "nonzero scale")
            rows[a] = {h:q*x for h,x in rows[a].items() if q*x}
        elif op in ("ADD","COPY"):
            b = ins[2]
            need(a != b and charts[a] == charts[b] == ins[4], "coframed ordinary contact")
            if op == "COPY":
                need(a >= n and not rows[a], "COPY begins at zero owned destination")
            plus(rows[a],rows[b],Q(ins[3]))
        else:
            raise ValueError("unknown op: "+repr(ins))
    need(charts == w["final"]+[None]*w["owned_fields"], "final owner chart map")
    need(set(cuts_at)==set(cuts), "owned source cuts recorded")

    # Prefix history P_E consists of initial and MOVE-arrival values at E's
    # destination chart strictly before E. Local ADD/SCALE/COPY outputs stay
    # in that span; INIT contributes zero.
    sites = {}
    projected_survivors = []
    full_misses = []
    all_owned_summary = []
    for event,(owner,source,destination,target) in cuts_at.items():
        destkey = frames[destination]
        old = {}
        for t,row in arrivals[destkey]:
            if t < event:
                insert(old,row)
        full_rem = reduce(target,old)
        old_main = {}
        for row in old.values():
            insert(old_main,{h:x for h,x in row.items() if h in mains})
        target_main = {h:x for h,x in target.items() if h in mains}
        main_rem = reduce(target_main,old_main)
        full_misses.append(event) if full_rem else None
        if target_main and not main_rem:
            projected_survivors.append(event)
        all_owned_summary.append({"event":event,"owner":owner,"source":source,"destination":destination,
            "target_rank":abs(len(w["frames"][source])-len(w["frames"][destination])),
            "target_nonzero_main":bool(target_main),"strict_history_rank":len(old),
            "target_outside_full_history":bool(full_rem),"target_main_in_history_projection":bool(target_main and not main_rem)})
        if event not in EXPECTED:
            continue
        need(w["program"][event] == ["MOVE",owner,source,destination,True], "literal owned MOVE binding")
        need(target_main and not main_rem, f"selected cut is not a main-projection hit event={event}")
        need(full_rem, "selected target is outside full strict history")
        # H_E = (P_E + <x_E>) intersect helper coordinates.
        extended = {p:r.copy() for p,r in old.items()}
        need(reduce(target,extended), "selected target nonmembership")
        insert(extended,target)
        lifted,mainrank = kernel_lifts(list(extended.values()),lambda r:{h:x for h,x in r.items() if h in mains})
        need(len(lifted) == len(extended)-mainrank, "helper kernel dimension")
        need(all(set(row)<=helpers for row in lifted.values()), "helper-only lift")
        sites[event] = {"event":event,"owner":owner,"source":source,"destination":destination,
            "target_rank":abs(len(w["frames"][source])-len(w["frames"][destination])),
            "target_row":{str(h):str(x) for h,x in sorted(target.items())},
            "strict_history_rank":len(old),"history_basis":encoded_basis(old),
            "helper_extension_dim":len(lifted),"helper_extension_basis":encoded_basis(lifted),
            "support":sorted(set().union(*(set(row) for row in lifted.values())))}
    need(sorted(projected_survivors)==EXPECTED,"47-to-14 main-projection survivor set")
    need(len(full_misses)==47,"each owned target misses its whole strict history")
    need(len(sites)==14,"14 independently reconstructed spaces")

    # Exact global arrangement and all pairwise intersections, from fresh
    # rational bases only.
    dimensions = {e:len(decode_basis(s["helper_extension_basis"])) for e,s in sites.items()}
    total_dim = sum(dimensions.values())
    global_space = {}
    for s in sites.values():
        for row in decode_basis(s["helper_extension_basis"]).values():
            insert(global_space,row)
    pair_intersections = []
    for pos,e in enumerate(EXPECTED):
        for f in EXPECTED[pos+1:]:
            meet = intersect(decode_basis(sites[e]["helper_extension_basis"]),
                             decode_basis(sites[f]["helper_extension_basis"]))
            if meet:
                pair_intersections.append({"sites":[e,f],"dimension":len(meet),
                    "basis":encoded_basis(meet),
                    "support":sorted(set().union(*(set(row) for row in meet.values()))),
                    "min_helper_target_rank":min(abs(len(w["frames"][w["initial"][h]])-
                        len(w["frames"][w["final"][h]])) for row in meet.values() for h in row)})
    need(total_dim==99 and len(global_space)==96,"full sum rank and nullity")
    need([(x["sites"],x["dimension"]) for x in pair_intersections] == [
        ([35152,45656],1),([35448,35452],1),([39875,39884],1)], "only three pair intersections")
    # The eleven groups are eight unpaired sites and the sums of the three
    # paired sites. Their dimensions must add to the independently computed
    # rank 96; this proves the group sum is direct.
    for pair in pair_intersections:
        line = next(iter(decode_basis(pair["basis"]).values()))
        left,right = pair["sites"]
        need(line and not reduce(line,decode_basis(sites[left]["helper_extension_basis"])) and
             not reduce(line,decode_basis(sites[right]["helper_extension_basis"])), "pair line membership")
    pair_site_sets = [set(x["sites"]) for x in pair_intersections]
    need(all(a.isdisjoint(b) for i,a in enumerate(pair_site_sets) for b in pair_site_sets[i+1:]),
         "three disjoint pair supports")
    paired_events=set().union(*pair_site_sets)
    groups=[]
    for e in EXPECTED:
        if e not in paired_events:
            groups.append({"sites":[e],"dimension":dimensions[e]})
    for p in pair_intersections:
        a,b=p["sites"]
        g=plus_basis(decode_basis(sites[a]["helper_extension_basis"]),
                     decode_basis(sites[b]["helper_extension_basis"]))
        groups.append({"sites":[a,b],"dimension":len(g)})
    group_basis={}
    for g in groups:
        if len(g["sites"])==1:
            gb=decode_basis(sites[g["sites"][0]]["helper_extension_basis"])
        else:
            gb={}
            for e in g["sites"]:
                gb=plus_basis(gb,decode_basis(sites[e]["helper_extension_basis"]))
        for row in gb.values():insert(group_basis,row)
    need(len(groups)==11 and sum(g["dimension"] for g in groups)==96 and
         len(group_basis)==96==len(global_space),"11 site groups form direct sum")

    ranks = {h:abs(len(w["frames"][w["initial"][h]])-len(w["frames"][w["final"][h]])) for h in helpers}
    site_prices = []
    for event,s in sites.items():
        support=s["support"]
        minrank=min(ranks[h] for h in support)
        site_prices.append({"event":event,"move_rank":s["target_rank"],"L_dim":s["helper_extension_dim"],
            "min_supported_helper_target_rank":minrank,
            "support_rank_multiset":sorted({ranks[h] for h in support}),"support_count":len(support)})
    line_prices = []
    for line in pair_intersections:
        line_prices.append({"sites":line["sites"],"dimension":line["dimension"],
            "min_supported_helper_target_rank":line["min_helper_target_rank"],
            "helper_support":line["support"]})

    result={"status":"FRESH_EXACT_NATIVE_14_SITE_ARRANGEMENT_REPLAY",
        "source_sha256":PIN,"source_payload_sha256":sha256(json.dumps(w,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
        "program_events":len(w["program"]),"owned_MOVEs":len(cuts_at),
        "mainfree_MOVE_count":len(mainfree_moves),"mainfree_MOVEs":mainfree_moves,
        "op_counts":dict(op_counts),"main_count":len(mains),"helper_count":len(helpers),
        "main_projection_survivors":sorted(projected_survivors),"full_history_misses":len(full_misses),
        "independent_owned_cut_summary":all_owned_summary,"site_dimensions":dimensions,
        "sum_dimensions":total_dim,"global_rank":len(global_space),"global_nullity":total_dim-len(global_space),
        "pair_intersections":pair_intersections,"disjoint_pair_site_supports":True,
        "site_groups":groups,"site_group_dimension_sum":sum(g["dimension"] for g in groups),
        "site_group_joint_rank":len(group_basis),"site_groups_direct_sum":True,
        "site_support_price_floors":site_prices,"shared_line_price_floors":line_prices,
        "site_spaces":sites,"elapsed_seconds":time.monotonic()-started,
        "history_rule":"Strict earlier same-chart public initial rows and MOVE arrivals; all intervening local linear operations stay within their span. No cross-chart import or changed provider history.",
        "scope":"Information-space arrangement only. Does not claim physical cache admission, multi-constraint supplier or kappa."}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("independent_owned_cut_summary","site_spaces")},indent=2))

if __name__=="__main__": main()
