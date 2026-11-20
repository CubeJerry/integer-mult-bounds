#!/usr/bin/env python3
"""Replay every funded-donor pulse by a literal forward sweep; derive exterior backwards."""
import argparse,gzip,hashlib,importlib.util,json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
def require(v,m):
    if not v:raise ValueError(m)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sources',type=Path,required=True);p.add_argument('--witness',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    src=a.sources/'7833-construction.py';spec=importlib.util.spec_from_file_location('literal_public',src);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    w=S.load_word(a.sources/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);shadow,=set(g.routes)-set(w.routes)
    top=len(g.schedule);clock={t:k for k,t in enumerate(g.schedule)};sources={e:g.source(e)for e in g.schedule}
    # True receipts with native clocks. Gift the original shadow to 282 at birth.
    received=defaultdict(list)
    for e,site in g.inputs.items():received[site].append((-2,e))
    received[282].append((-1,shadow))
    for e,(src,dst)in g.routes.items():
        if e!=shadow:received[dst].append((clock[e],e))
    for rows in received.values():rows.sort()
    donors={e for e in w.schedule if e in w.routes and w.routes[e][0]==3 and w.clock[e]<min(w.clock[t]for t in w.readers(90369))and w.grade(w.routes[e])>=3 and e not in (94019,90369)}
    raw=gzip.decompress(a.witness.read_bytes());ws=json.loads(raw);require({q['donor']for q in ws}==donors and len(ws)==len(donors)==181,'entire legal donor roster')
    n=0;complete=0;deg=[];sigs=hashlib.sha256()
    for t in ws:
        pulse={~i:Q(x)for i,x in t['original_input']};d=t['donor'];target=t['terminal']
        # Native linear forms are evaluated directly from the specified originals.
        # For a row, only nonzero partial values need enter the rational sum.
        vals=dict(pulse)
        for e in g.schedule:
            q=sum((v*vals[o]for o,v in g.forms[e].items()if o in vals),Q(0))
            if q:vals[e]=q
        check=vals.get(target,Q(0));require(check==Q(t['terminal_value']) and check,'nonzero intended public endpoint')
        # Earliest possible reach of an arbitrary dependent send. From the public
        # target expand every allowed previously received value at a reached site;
        # a clean send terminates the backwards search at that actual exterior row.
        arrival={w.routes[d][1]:clock[d]}
        for e in g.schedule[clock[d]+1:clock[target]]:
            if e!=shadow and e in g.routes and sources[e] in arrival:
                dest=g.routes[e][1];arrival.setdefault(dest,clock[e])
        require(sources[target]in arrival and arrival[sources[target]]<clock[target],'causal public terminal')
        todo=[target];visited=set();outside=set()
        while todo:
            x=todo.pop()
            if x in visited:continue
            visited.add(x)
            if x==d:continue
            if x<0 or x==shadow or arrival.get(sources[x],top)>=clock[x]:
                outside.add(x);continue
            for now,o in received[sources[x]]:
                if now>=clock[x]:break
                if o!=d:todo.append(o)
        require(all(e not in vals for e in outside),'all exterior publicly zero')
        digest=hashlib.sha256(json.dumps(sorted(outside),separators=(',',':')).encode()).hexdigest()
        require(digest==t['exterior_sha256']and len(outside)==t['exterior_size'],'full causal exterior pin')
        sigs.update(digest.encode());n+=len(outside);complete+=1;deg.append(w.grade(w.routes[d]))
    answer={'fully_replayed_original_pulses':complete,'checked_exterior_zero_records':n,'separate_native_grade_range':[min(deg),max(deg)],'witness_set_sha256':hashlib.sha256(raw).hexdigest(),'ordered_exterior_receipt_sha256':sigs.hexdigest(),'reached_nonzero_true_public_terminals':complete};a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(answer,indent=2)+'\n');print(answer)
if __name__=='__main__':main()
