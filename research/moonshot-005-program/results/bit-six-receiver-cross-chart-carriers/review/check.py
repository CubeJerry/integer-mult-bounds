#!/usr/bin/env python3
"""Independently audit immutable BIT schedules from original root tuples and opcodes."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import sympy
from sympy.polys.matrices import DomainMatrix

NATIVE = "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
NATIVE_SHA = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
DEFAULT_PINS = {
    "signed-points": "5a5b6fccb2a1aa76d68a6f2794194161cc25372cdecba2b8c280c5ad3e4e3141",
    "cross-chart-relay": "d3294c887cb7134e9b5449e8f89105b382aacd7cf620cec65cb4d75357e79a2a",
}


class Invalid(ValueError):
    pass


def need(cond, msg):
    if not cond:
        raise Invalid(msg)


def gf_rank(vectors):
    pivots = {}
    for row in vectors:
        v = set(row)
        while v:
            i = max(v)
            if i not in pivots:
                pivots[i] = v
                break
            v ^= pivots[i]
    return len(pivots)


@lru_cache(maxsize=None)
def rational_rank(rows):
    if not rows:
        return 0
    return DomainMatrix.from_list_sympy(len(rows), 8, [list(x) for x in rows]).rank()


def geometry(charts, roots):
    ident = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    ann = {}
    for name, chart in charts.items():
        k = chart["kind"]
        if k == "line":
            r = roots[chart["role"]]
            p = next(i for i, a in enumerate(r) if a)
            # Explicit basis of the annihilator of a line.
            ann[name] = tuple(tuple((r[p] if i == j else 0) - (r[j] if i == p else 0)
                                    for i in range(8)) for j in range(8) if j != p)
        elif k == "kernel":
            ann[name] = tuple(roots[j] for j in chart["normals"])
        elif k == "ambient":
            ann[name] = ()
        elif k == "zero":
            ann[name] = tuple(ident)
        else:
            raise Invalid("chart")
    for j in range(111):
        need(ann["F"+str(j)] == (roots[j],), "target normal")
        need(rational_rank(ann["L"+str(j)]) == 7, "initial line")
    need(len({tuple(Fraction(x,next(y for y in r if y)) for x in r) for r in roots})==111, "distinct terminal hyperplanes")
    @lru_cache(maxsize=None)
    def gap(src, dst):
        c, d = rational_rank(ann[src]), rational_rank(ann[dst])
        # The smaller annihilator must lie in the larger one.
        need(c!=d and rational_rank(ann[src]+ann[dst])==max(c,d),"strictly nested real sites")
        return c-d
    return gap


def basis_from_roots(roots):
    rows = [frozenset(j for j, s in enumerate(roots) if j==i or sum(a*b for a,b in zip(r,s))==0)
            for i,r in enumerate(roots)]
    need(gf_rank(rows)==9,"canonical binary rank")
    return rows


def local_missing(contents, sites, roots, rx):
    count=0
    for i in range(len(roots)):
        name="Y"+str(i)
        need(sites[name]=="F"+str(i),"terminal public site")
        words=[contents[x] for x in sites if sites[x]==sites[name]]
        wanted=frozenset((i,i+111))
        if gf_rank(words+[wanted])>gf_rank(words):
            count+=1
    return count


def simulate(w, rows, gap, selected, omit=None, bad=None, collect=True):
    roots=range(len(rows))
    public=["X"+str(j) for j in roots]+["Y"+str(j) for j in roots]
    orig={name:frozenset([j]) for j,name in enumerate(public)}
    val=orig.copy()
    site={name:("L"+str(j) if j<111 else "zero") for j,name in enumerate(public)}
    owners=set();ever=set();counts=Counter();hist=Counter();dirh=Counter();lifec=defaultdict(list)
    dirty=peak=0;checks={};marks={v:k for k,v in w["milestones"].items()}
    prespan=None
    for i,source in enumerate(w["operations"]):
        if i!=omit:
            op,n,*args=(bad[i] if bad and i in bad else source)
            counts[op]+=1
            if op=="INIT":
                need(n not in val and n not in ever,"fresh owner")
                val[n]=frozenset();site[n]=args[0];owners.add(n);ever.add(n)
            elif op=="ADD":
                dst=args[0]
                need(n in val and dst in val and n!=dst and site[n]==site[dst],"co-located ADD")
                val[dst]=val[dst].symmetric_difference(val[n])
            elif op=="MOVE":
                need(n in val,"live moved field")
                dest=args[0]; dist=gap(site[n],dest)
                if n in owners:
                    need(dist<0,"owned direction in this word");lifec[n].append((site[n],dest))
                else:
                    need(dist>0,"public ascent")
                hist[abs(dist)]+=1;dirh[("owned" if n in owners else "public",abs(dist))]+=1;site[n]=dest
            elif op=="CLEAR":
                need(n in owners,"owned retirement")
                dirty+=bool(val[n]);owners.remove(n);del val[n],site[n]
            else:
                raise Invalid("opcode")
            peak=max(peak,len(owners))
        if i+1 not in marks:
            continue
        name=marks[i+1]
        if name in ("source_restored","canonical_at_ground"):
            need(all(site[n]==("Hub" if n[0]=="X" else "zero") and val[n]==init for n,init in orig.items()),"raw X and pure Y milestone")
            if name=="canonical_at_ground":
                canonical=[n for n in owners if n.startswith("K")]
                need(len(canonical)==9 and len({int(n[1:]) for n in canonical})==9,"nine canonical owners")
                need(all(site[n]=="zero" and val[n]==rows[int(n[1:])] for n in canonical),"literal canonical vectors")
                need(gf_rank([val[n] for n in canonical])==9,"canonical owner coverage")
        elif name=="before_retirement" and collect:
            prespan=local_missing(val,site,roots,selected)
        if collect:
            checks[name]={"step":i+1,"owners":len(owners),"live":len(site)}
    need(not owners and set(val)==set(orig),"closed owner lifetimes")
    for j in roots:
        x,y="X"+str(j),"Y"+str(j)
        need(site[x]=="Hub" and val[x]==orig[x],"raw Hub X")
        wanted=orig[y] ^ (frozenset([j]) if j in selected else frozenset())
        need(site[y]=="F"+str(j) and val[y]==wanted,"complete native output incidence")
    if not collect:
        return
    missing=local_missing(val,site,roots,selected)
    return {"opcodes":dict(sorted(counts.items())),"movement_profile":dict(sorted(hist.items())),
            "owned_movement_profile":dict(sorted((k,d) for (src,k),d in dirh.items() if src=="owned")),
            "peak_owners":peak,"dirty_clears":dirty,"fresh_owner_lifetimes":len(ever),
            "stationary_owner_lifetimes":len(ever)-len(lifec),"milestones":checks,
            "unfinished_target_flats_missing_own_output_before_retirement":prespan,
            "unfinished_target_flats_missing_own_output_after_retirement":missing}


@lru_cache
def root_interval(n, digits=41):
    den=10**digits
    k,exact=sympy.integer_nthroot(n**199 * den**200,200)
    return Fraction(k,den),Fraction(k if exact else k+1,den)


def interval(p):
    low=high=Fraction(0)
    for n,coef in p.items():
        a,b=root_interval(n)
        low+=coef*(a if coef>=0 else b)
        high+=coef*(b if coef>=0 else a)
    return low,high


def intervals(hist):
    cap=Counter({127:37,64:74,1:-74})
    for i in range(1,9):
        cap[7*i+1]+=74;cap[7*i]-=74
    bound=interval({n:Fraction(c,6) for n,c in cap.items()})
    q=interval(hist)
    return q, (bound[0]-q[1],bound[1]-q[0])


def finite_threshold(hist):
    # Price only the movement profile as given; any completed extension must pay at least this
    # price on a literal append. It is intentionally not an admission test.
    native={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    head={2:1,4:25,6:1,8:410}
    def margin(m):
        p=Counter()
        for r,c in native.items():p[r]-=18*c
        for r,c in head.items():p[r]+=18*c
        p[1]-=222*m
        p[127]+=111*m
        for j in range(1,9):p[7*j]-=222*m
        for j in range(1,10):p[1+7*j]+=222*m
        for r,c in hist.items():p[r]-=18*(m-1)*c
        return interval(p)
    for m in range(2,300,2):
        a,b=margin(m)
        if a>0:
            assert m==2 or margin(m-2)[1]<0
            return {"first_even_m_passing_only_this_partial_movement_profile":m,
                    "margin_at_first":list(map(str,(a,b))),
                    "margin_at_preceding_even":list(map(str,margin(m-2))) if m>2 else None}
        assert b<0
    raise Invalid("threshold search")


def check(word, name, pin, roots, supplied_result, exhaustive):
    raw=word.read_bytes()
    need(sha256(raw).hexdigest()==pin,"immutable word")
    w=json.loads(raw)
    need(w["native_sha256"]==NATIVE_SHA and len(w["operations"])==len(w["operation_tags"]),"input schema")
    rows=basis_from_roots(roots);g=geometry(w["charts"],roots)
    claims=set(w["all_completed_roles"])
    audit=simulate(w,rows,g,claims)
    hist=audit["movement_profile"]
    q,room=intervals(hist)
    assert room[0]>0 and room[1]<audit["unfinished_target_flats_missing_own_output_before_retirement"]
    # Compare author after computing actual results from all input symbols.
    receipt=json.loads(supplied_result.read_bytes())
    assert receipt["counts"]==audit["opcodes"] and receipt["peak_owned"]==audit["peak_owners"]
    assert receipt["dirty_CLEAR"]==audit["dirty_clears"]
    assert {int(i):v for i,v in receipt["movement_profile"].items()}==hist
    assert set(receipt["receiver_roles"])|set(receipt["additional_paid_point_diagonals"])==claims
    for own,theirs in [(q,receipt["moment_at_199_over_200"]),(room,receipt["necessary_limiting_room"])]:
        l,h=map(Fraction,theirs["rational"]);assert l<=own[0]<=own[1]<=h
    rejected=Counter();survivors=[]
    ix=range(len(w["operations"])) if exhaustive else [next(i for i,o in enumerate(w["operations"]) if o[0]==s) for s in ("MOVE","ADD","INIT","CLEAR")]
    for i in ix:
        try:
            simulate(w,rows,g,claims,omit=i,collect=False)
        except (Invalid,KeyError):
            rejected[w["operations"][i][0]]+=1
        else:
            survivors.append([i,w["operations"][i]])
    return {"label":name,"word_sha256":pin,"native_sha256":NATIVE_SHA,
            "all_original_columns":222,"completed_roles":sorted(claims),**audit,
            "movement_moment_at_199_over_200":list(map(str,q)),"necessary_limiting_room":list(map(str,room)),
            **finite_threshold(hist),"single_opcode_deletions_rejected":dict(sorted(rejected.items())),
            "single_opcode_deletions_with_same_endpoint":survivors,"complete_supplier":False}


def main():
    p=ArgumentParser();p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--package",nargs=2,action="append",metavar=("LABEL","PACKAGE_PATH"),required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--sample",action="store_true")
    a=p.parse_args();src=(a.repo/NATIVE).read_bytes();assert sha256(src).hexdigest()==NATIVE_SHA
    roots=[tuple(v) for v in json.loads(src)["native_roots"]]
    assert len(roots)==111 and all(len(v)==8 and sum(x*x for x in v)>0 for v in roots)
    output=[]
    for label,pkg in a.package:
        base=Path(pkg)/"output"
        output.append(check(base/"WORD.json",label,DEFAULT_PINS[label],roots,base/"RESULT.json",not a.sample))
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"RESULT.json").write_text(json.dumps({"status":"PASS_C_INDEPENDENT_ALL_COLUMN_CACHE_REVIEW",
                                                   "sources":output},indent=2)+"\n")
    for x in output:
        print(x["label"],x["single_opcode_deletions_rejected"],x["single_opcode_deletions_with_same_endpoint"])


if __name__=="__main__":
    main()
