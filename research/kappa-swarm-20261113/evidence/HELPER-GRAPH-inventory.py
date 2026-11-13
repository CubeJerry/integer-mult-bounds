#!/usr/bin/env python3
"""Fresh full main-free MOVE rows and support components; no subset search."""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import argparse,gzip,hashlib,json,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
def need(ok,label):
    if not ok:raise ValueError(label)
@lru_cache(None)
def scalar(text):return Q(text)
def add(dst,src,q):
    need(dst is not src,'distinct scalar operands')
    for k,v in src.items():
        z=dst.get(k,0)+(v if q==1 else -v if q==-1 else q*v)
        if z:dst[k]=z
        else:dst.pop(k,None)
def mainfree(row,mains):return bool(row) and not(set(row)&mains)
def run(source,seconds):
    start=time.monotonic();raw=source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'exact source pin')
    w=json.loads(gzip.decompress(raw));n=w['public']
    mains=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    helpers=set(range(n))-mains;need(len(mains)==400 and len(helpers)==1101,'input partition')
    targets={h:len(w['frames'][w['final'][h]])-len(w['frames'][w['initial'][h]]) for h in helpers}
    need(all(r>0 for r in targets.values()),'positive original helper target ranks')
    rows=[{i:Q(1)} for i in range(n)]+[None]*w['owned_fields']
    charts=w['initial']+[None]*w['owned_fields'];fresh=set();records=[];other=0
    for event,e in enumerate(w['program']):
        if event%128==0 and time.monotonic()-start>seconds:raise TimeoutError('incomplete source replay')
        op,a=e[:2]
        if op=='MOVE':
            need(charts[a]==e[2] and bool(e[4])==(a>=n),'MOVE frame and owner')
            need(bool(rows[a]),'no missing-support or unconditional-zero MOVE')
            if mainfree(rows[a],mains):
                need(set(rows[a])<=helpers,'every row coordinate is an actual helper')
                records.append(dict(event=event,owner=a,owned=bool(e[4]),
                    rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])),
                    row={str(k):str(v) for k,v in sorted(rows[a].items())}))
            else:
                need(any(k in mains and v!=0 for k,v in rows[a].items()),'excluded row has nonzero main witness');other+=1
            charts[a]=e[3];fresh.discard(a)
        elif op=='INIT':
            need(a>=n and charts[a] is None,'owned INIT');charts[a],rows[a]=e[2],{};fresh.add(a)
        elif op=='CLEAR':
            need(a>=n and charts[a]==e[2],'owned CLEAR');charts[a],rows[a]=None,None;fresh.discard(a)
        elif op=='SCALE':
            need(charts[a]==e[-1],'SCALE frame');q=scalar(e[2]);need(q!=0,'nonzero scalar')
            rows[a]={k:q*v for k,v in rows[a].items() if q*v};fresh.discard(a)
        elif op in ('ADD','COPY'):
            b=e[2];need(charts[a]==charts[b]==e[-1],'cocharted scalar operands')
            if op=='COPY':need(a>=n and a in fresh and not rows[a],'fresh owned COPY')
            add(rows[a],rows[b],scalar(e[3]));fresh.discard(a)
        else:raise ValueError(op)
    need(charts==w['final']+[None]*w['owned_fields'],'all final charts')
    need(all(rows[h]=={h:Q(1)} for h in helpers),'all independent helper endpoints')
    need(all(not(set(rows[r])&helpers) for r in mains),'mains independent of helpers')
    need(not mainfree({},mains),'empty support control')
    need(not mainfree({min(mains):Q(1),min(helpers):Q(2)},mains),'nonzero main control')
    parent={h:h for rec in records for h in map(int,rec['row'])}
    def find(h):
        while parent[h]!=h:parent[h]=parent[parent[h]];h=parent[h]
        return h
    for rec in records:
        hs=list(map(int,rec['row']));root=find(hs[0])
        for h in hs[1:]:parent[find(h)]=root
    groups=defaultdict(list)
    for rec in records:groups[find(int(next(iter(rec['row']))))].append(rec)
    components=[]
    for es in sorted(groups.values(),key=lambda es:min(e['event'] for e in es)):
        hs=sorted({h for e in es for h in map(int,e['row'])});m=len(es)
        components.append(dict(id=len(components),rows=m,columns=len(hs),events=[e['event'] for e in es],helpers=hs,
            paid_rank_counts=dict(Counter(e['rank'] for e in es)),target_rank_counts=dict(Counter(targets[h] for h in hs)),
            nonempty_subsets=str(2**m-1)))
    need(sum(c['rows'] for c in components)==len(records),'component row coverage')
    need(sum(c['columns'] for c in components)==len(parent),'disjoint helper component supports')
    out=dict(source_sha256=PIN,instructions=len(w['program']),main_free_moves=len(records),nonzero_main_moves=other,
        targets={str(h):r for h,r in sorted(targets.items())},records=records)
    (HERE/'ROWS.json').write_text(json.dumps(out,indent=2)+'\n')
    result=dict(status='COMPLETE_FULL_SUPPORT_COMPONENT_INVENTORY_NO_SUBSET_ENUMERATION',source_sha256=PIN,
        rows_sha256=hashlib.sha256((HERE/'ROWS.json').read_bytes()).hexdigest(),instructions=len(w['program']),
        main_free_moves=len(records),nonzero_main_moves=other,helper_columns_used=len(parent),
        components=len(components),size_histogram=dict(Counter(c['rows'] for c in components)),
        largest_rows=max(c['rows'] for c in components),largest_columns=max(c['columns'] for c in components),
        total_nonempty_component_subsets=str(sum(2**c['rows']-1 for c in components)),
        components_detail=components,seconds=time.monotonic()-start,
        controls=dict(empty_support_rejected=True,nonzero_main_coefficient_rejected=True,all_helpers_have_target_weights=True),
        scope='Full exact Q rows; support connectivity only. No row subsets or minimum-column-basis funding have been tested.')
    (HERE/'INVENTORY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='components_detail'},indent=2))
    print('components',json.dumps([{k:c[k] for k in ['id','rows','columns','paid_rank_counts','target_rank_counts']} for c in components],indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=ROOT/'reference/pr7481/WORD.json.gz')
    p.add_argument('--seconds',type=float,default=60);a=p.parse_args();run(a.source,a.seconds)
