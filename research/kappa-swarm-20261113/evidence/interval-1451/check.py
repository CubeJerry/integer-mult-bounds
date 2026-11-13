#!/usr/bin/env python3
"""Finite propagated-helper correction before the first outward read."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from math import lcm,gcd
import argparse,gzip,json,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
PAIRPIN='ea6dc0cba6c36bedfe42612d5794606045b1d686339d273ebb822924d6af886e'
def need(ok,label):
    if not ok:raise ValueError(label)
@lru_cache(None)
def scalar(x):return Q(x)
def add(a,b,q):
    for h,v in b.items():
        z=a.get(h,0)+q*v
        if z:a[h]=z
        else:a.pop(h,None)
def space(f):
    s={0}
    for v in f:s|={x^v for x in s}
    return frozenset(s)
def run(output):
    start=time.monotonic();deadline=start+60;h=1451;target={146:Q(1)}
    wr=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(wr).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(wr))
    pr=(ROOT/'worker-b/deferred-pair-1451/PAIR.json').read_bytes();need(sha256(pr).hexdigest()==PAIRPIN,'pair pin')
    first_read=next(i for i,e in enumerate(w['program']) if e[0] in ('ADD','COPY') and e[2]==h and e[1]!=h)
    need(first_read==37946 and w['program'][37945]==['MOVE',1451,595,737,False],'finite outward interval')
    classes=[space(f) for f in w['frames']];selected={classes[595]:595,classes[737]:737}
    n=w['public'];rows=[{j:Q(1)} for j in range(n)]+[None]*w['owned_fields'];charts=w['initial']+[None]*w['owned_fields']
    fresh=set();observations=[];trace=[];checks=0
    def observe(event,owner,frame):
        if owner==h or classes[frame] not in selected or not rows[owner]:return
        need(not rows[owner].get(h),'history excludes missing helper and descendants')
        observations.append(dict(event=event,owner=owner,frame=frame,coframe=selected[classes[frame]],row={str(j):str(v) for j,v in sorted(rows[owner].items())}))
    for j,f in enumerate(w['initial']):observe(-1,j,f)
    for event,e in enumerate(w['program'][:first_read]):
        if event%128==0:need(time.monotonic()<deadline,'bounded prefix')
        op,a=e[:2];before=rows[h].get(h,0);oldframe=charts[h]
        if op=='MOVE':
            need(charts[a]==e[2],'MOVE chart');charts[a]=e[3];observe(event,a,e[3]);fresh.discard(a)
        elif op=='INIT':need(charts[a] is None,'fresh INIT');charts[a],rows[a]=e[2],{};fresh.add(a)
        elif op=='CLEAR':need(charts[a]==e[2],'CLEAR chart');charts[a],rows[a]=None,None;fresh.discard(a)
        elif op=='SCALE':
            need(charts[a]==e[-1],'SCALE chart');q=scalar(e[2]);rows[a]={j:q*v for j,v in rows[a].items()};fresh.discard(a)
        elif op in ('ADD','COPY'):
            b=e[2];need(b!=h,'no earlier outward scalar use');need(charts[a]==charts[b]==e[-1],'coframed scalar')
            if op=='COPY':need(a in fresh and not rows[a],'fresh COPY')
            add(rows[a],rows[b],scalar(e[3]));fresh.discard(a)
        else:raise ValueError(op)
        if a==h:
            trace.append(dict(event=event,instruction=e,frame_before=oldframe,frame_after=charts[h],old_helper_coefficient_before=str(before),old_helper_coefficient_after=str(rows[h].get(h,0))))
        elif rows[a] is not None:
            need(not rows[a].get(h),'all other produced values unaffected by missing helper');checks+=1
    need([t['event'] for t in trace]==[36564,36565,37945],'complete helper contact interval')
    need(charts[h]==737 and rows[h].get(h)==-1,'required correction at first outward read is+e146')
    def solve(ids,name):
        basis={}
        for j in ids:
            v={int(k):Q(a) for k,a in observations[j]['row'].items()};rep={j:Q(1)}
            for p in sorted(basis,reverse=True):
                if v.get(p):q=v[p];add(v,basis[p][0],-q);add(rep,basis[p][1],-q)
            if v:
                p=max(v);q=1/v[p];basis[p]=({k:a*q for k,a in v.items()},{k:a*q for k,a in rep.items()})
        v=target.copy();witness={}
        for p in sorted(basis,reverse=True):
            if v.get(p):q=v[p];add(v,basis[p][0],-q);add(witness,basis[p][1],q)
        out=dict(name=name,generator_indices=ids,history_rank=len(basis),target_in_span=not v,residual={str(k):str(a) for k,a in sorted(v.items())})
        if not v:
            chk={}
            for j,q in witness.items():add(chk,{int(k):Q(a) for k,a in observations[j]['row'].items()},q)
            need(chk==target,'exact chronological provider sum')
            out['provider_coefficients']={str(j):str(q) for j,q in sorted(witness.items())}
        else:
            dual={min(v):Q(1)}
            for p in sorted(basis):
                q=-sum((a*dual.get(k,0) for k,a in basis[p][0].items() if k!=p),Q(0))
                if q:dual[p]=q
            den=1
            for q in dual.values():den=lcm(den,q.denominator)
            integer={k:int(a*den) for k,a in dual.items()};g=0
            for a in integer.values():g=gcd(g,abs(a))
            integer={k:a//g for k,a in integer.items()};dot=lambda row:sum((a*integer.get(k,0) for k,a in row.items()),Q(0))
            value=dot(target)
            if value<0:integer={k:-a for k,a in integer.items()};value=dot(target)
            need(value>0 and not integer.get(h),'retained-input separating probe')
            for j in ids:need(dot({int(k):Q(a) for k,a in observations[j]['row'].items()})==0,'probe annihilates actual observation')
            out.update(integer_dual={str(k):a for k,a in sorted(integer.items())},target_dual_value=str(value),actual_observation_dots_all_zero=True)
        return out
    idsA=[j for j,o in enumerate(observations) if o['coframe']==595 and o['event']<37945]
    idsB=[j for j,o in enumerate(observations) if o['coframe']==737 and o['event']<37946]
    qa=solve(idsA,'595_before_MOVE37945');qb=solve(idsB,'737_before_read37946')
    joint=solve(sorted(set(idsA)|set(idsB)),'JOINT_reachable_history_allowing_split_injection')
    control_index=len(observations)
    observations.append(dict(event=37944,owner=-1,frame=595,coframe=595,row={'146':'1'}))
    need(solve(idsA+[control_index],'synthetic_target_provider')['target_in_span'],'inserted provider control must become feasible')
    observations.pop()
    if not joint['target_in_span']:
        bad={int(k):a for k,a in joint['integer_dual'].items()};p=int(next(iter(observations[0]['row'])));bad[p]=bad.get(p,0)+1
        need(any(sum((Q(a)*bad.get(int(k),0) for k,a in o['row'].items()),Q(0))!=0 for o in observations),'perturbed joint probe rejected')
    out=dict(status='JOINT_PREPARATION_HISTORY_HIT' if joint['target_in_span'] else 'JOINT_PREPARATION_HISTORY_MISS',
        source_sha256=PIN,pair_sha256=PAIRPIN,first_contact=36564,first_outward_read=first_read,
        outward_instruction=w['program'][first_read],helper_contacts=trace,
        actual_other_field_independence_checks=checks,all_other_histories_helper_free=True,
        required_injection_at_read={'146':'1'},per_coframe=[qa,qb],joint=joint,observations=observations,
        seconds=time.monotonic()-start,
        controls=dict(inserted_target_provider_accepted=True,perturbed_probe_rejected=not joint['target_in_span']),
        scope='Fixed native history through first outward read; original helper starts owned zero and performs native writes/SCALE/MOVE. Only strict prior coframe595/737 observations excluding helper; free accumulation/storage/dirty erasure. Joint pool allows partial correction on both sides of retained MOVE. No general retiming claim.')
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='observations'},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();run(a.output)
