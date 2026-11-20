"""Check all 208 public target cones in #7833's next funded-donor experiment."""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,importlib.util,json
ROOT=Path(__file__).resolve().parent

def run():
    src=ROOT/'sources';f=src/'7833-construction.py';spec=importlib.util.spec_from_file_location('p104_original',f);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    w=S.load_word(src/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);d=100187;oldsite=1098
    S.require(w.clock[d]==1010 and g.clock[d]==1011 and g.routes[d]==(3,oldsite),'live funded donor and two clock conventions')
    S.require(g.readers(d)==[100622,100222,100610,100619],'all four receiver outlets')
    impact=w.evaluate({},{d:Q(1)});targets=[e for e in w.schedule if e in w.terminals and impact[e]];S.require(len(targets)==208,'all affected original terminal coefficients')
    ids=[*g.inputs,*g.schedule];idx={e:i for i,e in enumerate(ids)};stock=defaultdict(int);reached=set();mut={}
    for e,a in g.inputs.items():stock[a]|=1<<idx[e]
    for e in g.schedule:
        a=g.source(e)
        if e==d:reached.add(oldsite);continue
        if a in reached:ext=stock[a];mut[e]=ext
        else:ext=1<<idx[e]
        if e in g.routes:
            b=g.routes[e][1];stock[b]|=ext
            if e in mut:reached.add(b)
    groups=defaultdict(list)
    for e in targets:groups[mut[e]].append(e)
    V=S.all_public_rows(g);result=[];outer=None
    for mask,es in sorted(groups.items(),key=lambda q:q[0].bit_count()):
        fixed=[e for i,e in enumerate(ids)if mask&(1<<i)];freq=Counter(x for i in fixed for x in V[i][1]);order=sorted(range(len(g.inputs)),key=lambda j:(freq[j],j));R=S.IntegerElimination({j:i for i,j in enumerate(order)})
        for e in sorted(fixed,key=lambda i:(len(V[i][1]),i)):R.add(V[e][1])
        piv=set(R.rows);outside=[]
        for e in es:
            if R.add(V[e][1]):
                outside.append(e);k,=set(R.rows)-piv;del R.rows[k]
        if 154925 in es:outer=fixed;S.require(len(fixed)==len(piv)==9 and 154925 in outside,'reported independent terminal')
        result.append({'fixed_observations':len(fixed),'fixed_rank':len(piv),'required_terminals':es,'independently_outside':outside})
    S.require(outer is not None,'terminal 154925 reached');rows=S.Equations()
    for e in outer:rows.add(g.pullback(e),(Q(0),))
    rows.add(g.pullback(154925),(Q(1),));pulse,=rows.inputs_for_right_sides(1);forward=g.evaluate(pulse);original=w.evaluate(pulse)
    S.require(all(forward[e]==0 for e in outer)and forward[154925]==original[154925]==1,'an exact public-input witness')
    return {'status':'PASS_LIVE_7833_DONOR_100187_PUBLIC_CUT','word_sha256':S.WORD,'upstream_commit':'2b3176a88b4c46d4e1dc944843859634baa18b82','source_adapter_sha256':sha256(f.read_bytes()).hexdigest(),'donor':d,'original_clock':w.clock[d],'compensated_clock':g.clock[d],'affected_terminals':len(targets),'reached_charts':len(reached),'mutable_paid_and_terminal_events':len(mut),'boundary_classes':len(groups),'individually_outside_count':sum(len(x['independently_outside'])for x in result),'cut_witness':{'terminal':154925,'full_generous_boundary':sorted(outer),'fixed_rank':9,'rank_with_target':10,'input_pulse':[[i,str(x)]for i,x in sorted(pulse.items())]},'complete_rank_groups':result}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r=run();a.out.mkdir(parents=True,exist_ok=True);(a.out/'DONOR100187.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'],r['individually_outside_count'],r['cut_witness'])
