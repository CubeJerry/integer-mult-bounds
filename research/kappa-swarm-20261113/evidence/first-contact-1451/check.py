#!/usr/bin/env python3
"""Exact first-use coframe history with original helper1451 removed."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from math import lcm,gcd
import argparse,gzip,json,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
RELPIN='ea6dc0cba6c36bedfe42612d5794606045b1d686339d273ebb822924d6af886e'
def need(ok,label):
    if not ok:raise ValueError(label)
@lru_cache(None)
def scalar(x):return Q(x)
def add(a,b,q):
    for h,v in b.items():
        z=a.get(h,0)+q*v
        if z:a[h]=z
        else:a.pop(h,None)
def space(frame):
    s={0}
    for v in frame:s|={x^v for x in s}
    return frozenset(s)
def contact(e,h):return e[1]==h or e[0] in ('ADD','COPY') and e[2]==h
def run(output):
    start=time.monotonic();deadline=start+60;h=1451
    wr=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(wr).hexdigest()==PIN,'word pin')
    rr=(HERE/'PAIR.json').read_bytes();need(sha256(rr).hexdigest()==RELPIN,'relation pin')
    w=json.loads(gzip.decompress(wr));rel=json.loads(rr);target={int(j):Q(v) for j,v in rel['demoted_entrance_as_linear_combination_of_other_inputs'].items()}
    first=next(i for i,e in enumerate(w['program']) if contact(e,h));need(first==36564,'first native use')
    n=w['public'];classes=[space(f) for f in w['frames']];F=w['initial'][h];need(F==595,'actual original coframe')
    rows=[{j:Q(1)} for j in range(n)]+[None]*w['owned_fields'];charts=w['initial']+[None]*w['owned_fields']
    observations=[];basis={};fresh=set();independent_checks=0
    def observe(event,owner,frame):
        if owner==h or classes[frame]!=classes[F] or not rows[owner]:return
        need(not rows[owner].get(h),'all pooled histories independent of omitted1451')
        j=len(observations);v=rows[owner].copy();rep={j:Q(1)}
        observations.append(dict(event=event,owner=owner,frame=frame,row={str(k):str(a) for k,a in sorted(v.items())}))
        for p in sorted(basis,reverse=True):
            if v.get(p):q=v[p];add(v,basis[p][0],-q);add(rep,basis[p][1],-q)
        if v:
            p=max(v);q=1/v[p];basis[p]=({k:a*q for k,a in v.items()},{k:a*q for k,a in rep.items()})
    for j,f in enumerate(w['initial']):observe(-1,j,f)
    for event,e in enumerate(w['program'][:first]):
        if event%128==0:need(time.monotonic()<deadline,'bounded prefix replay')
        need(not contact(e,h),'no earlier native use of1451');op,a=e[:2]
        if op=='MOVE':
            need(charts[a]==e[2],'MOVE chart');need(not rows[a].get(h),'mover independent of1451');independent_checks+=1
            charts[a]=e[3];observe(event,a,e[3]);fresh.discard(a)
        elif op=='INIT':need(charts[a] is None,'fresh INIT');charts[a],rows[a]=e[2],{};fresh.add(a)
        elif op=='CLEAR':need(charts[a]==e[2],'CLEAR chart');charts[a],rows[a]=None,None;fresh.discard(a)
        elif op=='SCALE':
            need(charts[a]==e[-1],'SCALE chart');q=scalar(e[2]);rows[a]={j:q*v for j,v in rows[a].items()};fresh.discard(a)
            need(not rows[a].get(h),'scaled field independent of1451');independent_checks+=1
        elif op in ('ADD','COPY'):
            b=e[2];need(charts[a]==charts[b]==e[-1],'coframed scalar')
            if op=='COPY':need(a in fresh and not rows[a],'fresh-zero COPY')
            add(rows[a],rows[b],scalar(e[3]));fresh.discard(a)
            need(not rows[a].get(h),'scalar result independent of1451');independent_checks+=1
        else:raise ValueError(op)
    need(charts[h]==595 and rows[h]=={h:Q(1)},'untouched original helper at first use')
    value=target.copy();witness={}
    for p in sorted(basis,reverse=True):
        if value.get(p):q=value[p];add(value,basis[p][0],-q);add(witness,basis[p][1],q)
    for p,(v,rep) in basis.items():
        reconstructed={}
        for j,q in rep.items():add(reconstructed,{int(k):Q(a) for k,a in observations[j]['row'].items()},q)
        need(reconstructed==v,'exact pooled basis representation')
    out=dict(source_sha256=PIN,relation_sha256=RELPIN,first_use=first,instruction=w['program'][first],
        original_entrance_frame=F,frame_basis=w['frames'][F],excluded_initial_unit=h,
        independent_of_1451_checks=independent_checks,all_observations_1451_free=True,
        target={str(j):str(q) for j,q in sorted(target.items())},observations=observations,
        observation_count=len(observations),history_rank=len(basis),target_in_history=not value,
        target_residual={str(j):str(q) for j,q in sorted(value.items())},seconds=time.monotonic()-start)
    if not value:
        check={}
        for j,q in witness.items():add(check,{int(k):Q(a) for k,a in observations[j]['row'].items()},q)
        need(check==target,'chronological history witness')
        out.update(status='DEFERRED_PREPARATION_HISTORY_HIT',provider_coefficients={str(j):str(q) for j,q in sorted(witness.items())})
    else:
        free=min(value);dual={free:Q(1)}
        for p in sorted(basis):
            q=-sum((a*dual.get(j,0) for j,a in basis[p][0].items() if j!=p),Q(0))
            if q:dual[p]=q
        den=1
        for q in dual.values():den=lcm(den,q.denominator)
        integer={j:int(q*den) for j,q in dual.items()};g=0
        for a in integer.values():g=gcd(g,abs(a))
        integer={j:a//g for j,a in integer.items()}
        dot=lambda row:sum((a*integer.get(j,0) for j,a in row.items()),Q(0))
        target_dot=dot(target)
        if target_dot<0:integer={j:-a for j,a in integer.items()};target_dot=dot(target)
        need(target_dot>0 and not integer.get(h),'dual separates target in retained input coordinates')
        checks=[]
        for obs in observations:
            a=dot({int(j):Q(q) for j,q in obs['row'].items()});need(a==0,'integer dual annihilates actual history row');checks.append(str(a))
        if basis:
            p=max(basis);bad=integer.copy();bad[p]=bad.get(p,0)+1
            need(any(sum((Q(a)*bad.get(int(j),0) for j,a in o['row'].items()),Q(0))!=0 for o in observations),'wrong dual control rejected')
        out.update(status='DEFERRED_PREPARATION_HISTORY_MISS',integer_dual={str(j):a for j,a in sorted(integer.items())},
            target_dual_value=str(target_dot),all_observation_dual_values=checks,
            controls=dict(actual_history_annihilated=True,inserted_target_provider_invalidates_dual=True,wrong_dual_rejected=bool(basis)))
    out['scope']='Unchanged native prefix, omitted1451 input, all other inputs arbitrary. Pooled strictly earlier coframe595 history; no extra incoming transport or nonlocal observation. No universal no-construction claim.'
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['target','observations']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();run(a.output)
