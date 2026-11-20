#!/usr/bin/env python3
"""Independently recover the pooled old exteriors with a freely available fifth linear field."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
def need(v,m):
    if not v:raise ValueError(m)
def main():
    q=argparse.ArgumentParser(description=__doc__);q.add_argument('--sources',type=Path,required=True);q.add_argument('--witness',type=Path,required=True);q.add_argument('--out',type=Path,required=True);a=q.parse_args()
    sp=importlib.util.spec_from_file_location('physical',a.sources/'7833-construction.py');P=importlib.util.module_from_spec(sp);sp.loader.exec_module(P)
    w=P.load_word(a.sources/'DOUBLE-CANDIDATE.json.gz');g=P.compensated(w,True);shadow,=set(g.routes)-set(w.routes)
    clock={e:i for i,e in enumerate(g.schedule)};src={e:g.source(e)for e in g.schedule};stock=defaultdict(list)
    for k,chart in g.inputs.items():stock[chart].append((-1,k))
    for e,(_,chart)in g.routes.items():
        if e!=shadow:stock[chart].append((clock[e],e))
    for vals in stock.values():vals.sort()
    donors={e for e,rt in w.routes.items()if rt[0]==3 and w.clock[e]<min(w.clock[r]for r in w.readers(90369))and w.grade(rt)>=3 and e not in (94019,90369)}
    def eval0(graph,pulse):
        hold={~int(i):Q(v)for i,v in pulse}
        for e in graph.schedule:
            z=sum((c*hold[t]for t,c in graph.forms[e].items()if t in hold),Q())
            if z:hold[e]=z
        return hold
    raw=gzip.decompress(a.witness.read_bytes());tests=json.loads(raw);need(len(tests)==181 and {g0['donor']for g0 in tests}==donors,'full native roster');pulsecount=0;zeros=0;kinds=Counter()
    for case in tests:
        donor=case['donor'];targets=case['terminals'];bound=case['available_extra_scalars'];reached={282:-1}
        independently_fed={282:-1}
        for e in g.schedule:
            if e==shadow:continue
            if e==donor:reached.setdefault(g.routes[e][1],clock[e]);continue
            if e not in g.routes:continue
            x,y=g.routes[e]
            if x in reached:reached.setdefault(y,clock[e])
            if x in independently_fed:independently_fed.setdefault(y,clock[e])
        need(all(reached.get(src[e],10**10)<clock[e]for e in targets),'physically affected target');local=any(independently_fed.get(src[e],10**10)<clock[e]for e in targets)
        need(local==bound and len(targets)==bound+1,'one freely received field has the stated causal access')
        queue=list(targets);seen=set();outside=set()
        while queue:
            e=queue.pop()
            if e in seen:continue
            seen.add(e)
            if e in (shadow,donor):continue
            if e<0 or reached.get(src[e],10**10)>=clock[e]:outside.add(e);continue
            for time,slot in stock[src[e]]:
                if time>=clock[e]:break
                if slot!=donor:queue.append(slot)
        h=hashlib.sha256(json.dumps(sorted(outside),separators=(',',':')).encode()).hexdigest();need(h==case['exterior_sha256']and len(outside)==case['exterior_size'],'pooled backwards exterior')
        for j,p in enumerate(case['stimuli']):
            pulse=p['original_input'];v=eval0(g,pulse);baseline=eval0(w,pulse);need(all(e not in v for e in outside),'true exterior zero');want=Q(p['diagonal_value']);need(want,'nonzero diagonal')
            need(all(baseline.get(e,0)==v.get(e,0)==(want if i==j else 0)for i,e in enumerate(targets)),'native and compensated target matrix')
            pulsecount+=1;zeros+=len(outside)
        kinds[bound]+=1
    need((pulsecount,kinds[0],kinds[1])==(271,91,90),'emitted schema')
    out={'single_donor_cases':181,'no_reachable_extra_cases':kinds[0],'one_extra_two_independent_public_targets':kinds[1],'tested_original_integer_pulses':pulsecount,'true_exterior_zero_checks':zeros,'witness_sha256':hashlib.sha256(raw).hexdigest(),'scope':'the arbitrary fifth scalar on the two-dimensional witness plane is a rational linear observation'};a.out.mkdir(exist_ok=True,parents=True);(a.out/'FLEXIBLE.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
if __name__=='__main__':main()
