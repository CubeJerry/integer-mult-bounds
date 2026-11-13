#!/usr/bin/env python3
"""Independent exact rank and coarsened-component check for mixed bound.

Uses the fresh source replay from Wave31, not A's or root's exploratory
L-space bases. Recomputes the 567-row rank, fundamental circuits and
coarsened components using exact Q row operations.
"""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip,json,time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
REPLAY=ROOT/"worker-c/combined-one-relation-review/ARRANGEMENT-REPLAY.json"
WORD=ROOT/"reference/pr7481/WORD.json.gz"
ROWS=ROOT/"worker-b/helper-graph/ROWS.json"
PIN="acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
ROWSPIN="15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834"
OUT=HERE/"UNION-CERTIFICATE.json"

def need(ok,msg):
    if not ok:raise ValueError(msg)
def add(a,b,c=Q(1)):
    for h,x in b.items():
        z=a.get(h,Q(0))+c*x
        if z:a[h]=z
        else:a.pop(h,None)
def decode(r):return {int(h):Q(v) for h,v in r.items()}
def reduce(v,basis):
    v=v.copy()
    for p in sorted(basis):
        if v.get(p):add(v,basis[p],-v[p])
    return v
def encode(r):return {str(h):str(x) for h,x in sorted(r.items())}
def sha(path):return sha256(path.read_bytes()).hexdigest()

class DSU:
    def __init__(self,n):self.parent=list(range(n));self.size=[1]*n
    def find(self,x):
        while self.parent[x]!=x:
            self.parent[x]=self.parent[self.parent[x]];x=self.parent[x]
        return x
    def union(self,a,b):
        a=self.find(a);b=self.find(b)
        if a==b:return
        if self.size[a]<self.size[b]:a,b=b,a
        self.parent[b]=a;self.size[a]+=self.size[b]

def main():
    started=time.monotonic()
    wordraw=WORD.read_bytes();need(sha(WORD)==PIN,"native WORD byte pin")
    word=json.loads(gzip.decompress(wordraw))
    replay=json.loads(REPLAY.read_text())
    need(replay["source_sha256"]==PIN,"fresh replay source binding")
    payload=sha256(json.dumps(word,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    need(payload==replay["source_payload_sha256"],"canonical native payload binding")
    rowraw=ROWS.read_bytes();need(sha(ROWS)==ROWSPIN,"independent 468 row receipt pin")
    author=json.loads(rowraw);fresh=replay["mainfree_MOVEs"]
    need(len(fresh)==468==author["main_free_moves"],"all main-free source MOVE rows")
    ar={x["event"]:x for x in author["records"]}
    need(len(ar)==468,"unique row receipt event identities")
    for x in fresh:
        y=ar[x["event"]]
        need(all(x[k]==y[k] for k in ("event","owner","owned","rank","row")),"fresh/source cross-check for main-free row")

    # Ground-set order: all zero-MOVE occurrences, then each independently
    # generated L_E basis row in fixed site/pivot order.
    labels=[];rows=[]
    for x in sorted(fresh,key=lambda r:r["event"]):
        labels.append({"kind":"zero_move","event":x["event"],"owner":x["owner"],"rank":x["rank"]})
        rows.append(decode(x["row"]))
    sites={int(e):s for e,s in replay["site_spaces"].items()}
    expected_sites=[30581,30593,35152,35448,35452,36346,36358,39875,39884,41646,42487,42500,44253,45656]
    need(list(sites)==expected_sites,"site order in fresh replay")
    site_member_idxs=defaultdict(list)
    for e in expected_sites:
        basis=sites[e]["helper_extension_basis"]
        for pivot,row in sorted(basis.items(),key=lambda kv:int(kv[0])):
            idx=len(rows)
            labels.append({"kind":"cache_basis","site":e,"pivot":int(pivot)})
            rows.append(decode(row));site_member_idxs[e].append(idx)
    need(len(rows)==567 and sum(len(s["helper_extension_basis"]) for s in sites.values())==99,"567=468+99 ground set")

    # Build an exact echelon basis with explicit expressions over selected
    # original ground-set rows. A dependent row's unique expression is its
    # fundamental circuit relative to the selected basis.
    pivots={};pivot_expr={};basis_ground=[];circuits=[];dsu=DSU(len(rows))
    for i,row in enumerate(rows):
        v=row.copy();expr={i:Q(1)}
        for p in sorted(pivots):
            c=v.get(p)
            if c:
                add(v,pivots[p],-c)
                add(expr,pivot_expr[p],-c)
        if v:
            p=min(v);scale=v[p]
            pivots[p]={h:x/scale for h,x in v.items()}
            pivot_expr[p]={j:x/scale for j,x in expr.items()}
            basis_ground.append(i)
        else:
            need(expr.get(i)==1,"dependent row has unit own coefficient")
            support=sorted(j for j,c in expr.items() if c)
            need(i in support and len(support)>=2,"nontrivial fundamental circuit")
            for j in support:
                if j!=i:dsu.union(i,j)
            circuits.append({"dependent_row":i,"support":support})
    rank=len(basis_ground);need(rank==525 and len(circuits)==42,"exact 567-row rank525/nullity42")
    # Coarsen matroid components by forcing all rows of a cache-site basis
    # into the same component, then aggregate original zero event IDs.
    for indices in site_member_idxs.values():
        for i in indices[1:]:dsu.union(indices[0],i)
    components=defaultdict(list)
    for i in range(len(rows)):components[dsu.find(i)].append(i)
    comp_records=[]
    comp_rank_sum=0
    for members in components.values():
        site_ids=sorted({labels[i]["site"] for i in members if labels[i]["kind"]=="cache_basis"})
        zero_events=sorted(labels[i]["event"] for i in members if labels[i]["kind"]=="zero_move")
        b={}
        for i in members:
            v=reduce(rows[i],b)
            if v:
                p=min(v);z=v[p];b[p]={h:x/z for h,x in v.items()}
        comp_rank_sum+=len(b)
        comp_records.append({"cache_sites":site_ids,"zero_events":zero_events,
            "row_count":len(members),"rank":len(b),"ground_rows":sorted(members)})
    comp_records.sort(key=lambda c:(not bool(c["cache_sites"]),c["cache_sites"],c["zero_events"]))
    cache_components=[c for c in comp_records if c["cache_sites"]]
    zero_only=[c for c in comp_records if not c["cache_sites"]]
    need(len(cache_components)==11,"eleven components contain cache spaces")
    need(sum(c["row_count"] for c in comp_records)==567 and sum(c["rank"] for c in comp_records)==525,
         "coarsened component ranks compose exactly")
    need(comp_rank_sum==rank,"component row spaces are a direct sum")

    # Compare exact cache-component event/site partition with the exploration
    # hint only after deriving it from fresh rows and fresh L spaces.
    exploratory=json.loads((ROOT/"cache-zero-arrangement-exploration.json").read_text())
    expected={tuple(sorted(x["cache_sites"])):tuple(sorted(x["zero_events"]))
              for x in exploratory["components_with_cache_spaces"]}
    actual={tuple(f"cache:{e}" for e in c["cache_sites"]):tuple(c["zero_events"])
            for c in cache_components}
    need(actual==expected,"coarsened partition matches exploratory hint")

    # Compact exact provenance for the input row multiset and the zero-only
    # components delegated to the separate helper-funding theorem.
    row_doc=[{"label":labels[i],"row":encode(rows[i])} for i in range(len(rows))]
    union_sha=sha256(json.dumps(row_doc,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    zhist=Counter((c["row_count"],c["rank"]) for c in zero_only)
    z_events=sorted(labels[i]["event"] for c in zero_only for i in c["ground_rows"])

    result={"status":"FRESH_EXACT_567_ROW_UNION_AND_COARSENED_COMPONENT_CERTIFICATE",
        "source_sha256":PIN,"source_payload_sha256":payload,
        "fresh_arrangement_sha256":sha(REPLAY),"mainfree_rows_sha256":ROWSPIN,
        "row_count":len(rows),"union_rows_canonical_sha256":union_sha,
        "zero_MOVE_rows":len(fresh),"L_basis_rows":len(rows)-len(fresh),
        "exact_rank":rank,"nullity":len(rows)-rank,"fundamental_circuit_count":len(circuits),
        "coarsened_component_count":len(comp_records),"components_with_cache_spaces":len(cache_components),
        "zero_only_components":len(zero_only),"component_rank_sum":comp_rank_sum,
        "cache_components":[{k:c[k] for k in ("cache_sites","zero_events","row_count","rank")}
                             for c in cache_components],
        "zero_only_component_row_rank_histogram":[{"rows":a,"rank":b,"components":n}
            for (a,b),n in sorted(zhist.items())],
        "zero_only_event_ids":z_events,
        "scope":"Only certifies the source-bound row union rank and coarsened direct-sum component partition. It does not certify local mixed subset prices or a source gain.",
        "elapsed_seconds":time.monotonic()-started}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
