#!/usr/bin/env python3
"""Exact weaker decoder calendar bounds; necessary counts, not constructions."""
from scan import *
def explore(source):
    raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public']
    m=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    need((n,len(m))==(1480,400),'source input census')
    canonical={};keys=[canonical.setdefault(span(f),i) for i,f in enumerate(w['frames'])]
    c=[{r:F(1)} for r in range(n)]+[{} for _ in range(w['owned_fields'])]
    d=[({r:F(1)} if r in m else {}) for r in range(n)]+[{} for _ in range(w['owned_fields'])]
    current=w['initial'][:]+[None]*w['owned_fields'];cb=defaultdict(dict)
    modes=('all_main_current','main_departure_and_endpoint','endpoint_only');db={k:defaultdict(dict) for k in modes}
    balances={(k,o):Counter() for k in modes for o in (1,2)};peaks={k:Counter() for k in balances};witnesses={k:{} for k in balances}
    records={k:[] for k in modes}
    def account(mode,f,amount,event,what):
        if amount:records[mode].append([event,f,amount,what])
        for o in (1,2):
            key=(mode,o);balances[key][f]+=amount
            if balances[key][f]>peaks[key][f]:peaks[key][f]=balances[key][f];witnesses[key][f]=event
    for r in range(n):
        f=keys[current[r]];insert(c[r],cb[f])
        for mode in modes:insert(d[r],db[mode][f])
    for i,e in enumerate(w['program']):
        op,r=e[:2]
        if op=='INIT':
            need(r>=n and current[r] is None,'INIT guard');current[r]=e[2];c[r]={};d[r]={}
        elif op=='CLEAR':
            need(r>=n and current[r]==e[2],'CLEAR guard');current[r]=None;c[r]={};d[r]={}
        elif op=='MOVE':
            need(current[r]==e[2] and e[4]==(r>=n),'typed MOVE guard')
            src=keys[e[2]];f=keys[e[3]];kind='main' if r in m else 'owned' if r>=n else 'helper'
            if r in m:
                mode='main_departure_and_endpoint';account(mode,src,insert(d[r],db[mode][src]),i,'departure')
            common=insert(c[r],cb[f]);current[r]=e[3]
            for mode in modes:
                for o in (1,2):balances[(mode,o)][f]-=2 if kind=='main' else o if kind=='owned' else 1
                delta=insert(d[r],db[mode][f]) if r in m and mode=='all_main_current' else 0
                account(mode,f,common+delta,i,'arrival')
        elif op=='SCALE':
            need(current[r]==e[3] and F(e[2])!=0,'SCALE guard')
            c[r]={j:F(e[2])*x for j,x in c[r].items()};d[r]={j:F(e[2])*x for j,x in d[r].items()}
        elif op in ('ADD','COPY'):
            need(r!=e[2] and current[r]==current[e[2]]==e[4] and F(e[3])!=0,'cochart scalar guard')
            if op=='COPY':need(not c[r] and not d[r],'COPY zero guard')
            add(c[r],c[e[2]],F(e[3]));add(d[r],d[e[2]],F(e[3]))
            if r in m:
                mode='all_main_current';f=keys[current[r]];account(mode,f,insert(d[r],db[mode][f]),i,'main-update')
        else:raise ValueError('unknown opcode')
    need(current[:n]==w['final'] and all(f is None for f in current[n:]),'source endpoint')
    for r in sorted(m):
        f=keys[current[r]]
        for mode in modes:account(mode,f,insert(d[r],db[mode][f]),len(w['program']),'endpoint')
    floors={mode:{str(o):sum(peaks[(mode,o)].values()) for o in (1,2)} for mode in modes}
    need(floors=={'all_main_current':{'1':913,'2':902},'main_departure_and_endpoint':{'1':106,'2':106},'endpoint_only':{'1':0,'2':0}},'exact weaker calendar floors')
    return {'status':'PASS_WEAKER_DECODER_CALENDAR_BOUNDS','source_sha256':PIN,'extra_arrival_floors':floors,'by_chart':{mode:{str(o):{str(f):[v,witnesses[(mode,o)][f]] for f,v in sorted(peaks[(mode,o)].items()) if v>0} for o in (1,2)} for mode in modes},'records':records,'scope':'Every common source state still decoded; varying difference demands. Fixed funded destination/time calendar; arbitrary payloads. Endpoint zero is no obstruction here, not feasibility or a construction.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    source=a.source or next((base/REL for base in Path(__file__).resolve().parents if (base/REL).is_file()),None)
    need(source is not None,'provide --source or place inside repository');r=explore(source)
    if a.output:a.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('by_chart','records')},indent=2))
