#!/usr/bin/env python3
"""Exact single two-helper correlation census on frozen #7481."""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import argparse,gzip,hashlib,json,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
CALLER_PIN='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc'
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
def space(basis):
    s={0}
    for v in basis:s|={x^v for x in s}
    need(len(s)==2**len(basis),'independent source frame');return frozenset(s)
def gain(P,R,d):
    return [sum(c*min(r,k) for r,c in P.items())-min(R,k)-min(d,k) for k in range(1,10)]
def helper_pair(row,mains):return len(row)==2 and not(set(row)&mains)
def controls():
    need(gain({2:1},2,0)==[0]*9,'matching-boundary neutral control')
    need(gain({1:1},2,1)==[-1]+[-2]*8,'cleanup debit control')
    need(Q(2)*3-6==0 and Q(2)*2-6!=0,'forced q/wrong q control')
    need(not helper_pair({0:Q(1),1:Q(2)},{0}),'nonzero main coefficient rejected')
    need(helper_pair({1:Q(1),2:Q(2)},{0}),'pure helper pair accepted')
    need(-Q(-3)/2==-Q(-6)/4,'proportional rows share q')
    return dict(target_debit=True,cleanup_debit=True,forced_q=True,wrong_q_rejected=True,
                main_support_rejected=True,proportional_rows_share_family=True)
def run(source,output,seconds,caller):
    start=time.monotonic();tested=controls();raw=source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'exact source pin')
    callerraw=caller.read_bytes();need(hashlib.sha256(callerraw).hexdigest()==CALLER_PIN,'actual caller pin')
    cw=json.loads(callerraw);calls=sum(e[0]=='J' for e in cw['events'])
    need(calls==cw['stages']==17,'actual 17 native calls')
    w=json.loads(gzip.decompress(raw));n=w['public']
    mains=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    helpers=set(range(n))-mains
    need(len(mains)==400 and len(helpers)==1101,'main/helper partition')
    spaces=[space(b) for b in w['frames']]
    rows=[{i:Q(1)} for i in range(n)]+[None]*w['owned_fields']
    charts=w['initial']+[None]*w['owned_fields'];fresh=set()
    families=defaultdict(list);mainfree=twohelper=0;paid=Counter();exclusions=Counter();aliases=[];excluded=[]
    for event,e in enumerate(w['program']):
        if event%128==0 and time.monotonic()-start>seconds:raise TimeoutError('incomplete exact replay')
        op,a=e[:2]
        if op=='MOVE':
            need(charts[a]==e[2] and bool(e[4])==(a>=n),'MOVE chart and ownership')
            need(spaces[e[2]]<spaces[e[3]] or e[4] and spaces[e[3]]<spaces[e[2]],'native MOVE nesting')
            r=abs(len(w['frames'][e[3]])-len(w['frames'][e[2]]));paid[r]+=1
            support=set(rows[a])
            need(bool(support),'no unconditional exact-zero MOVE')
            if not support&mains:
                mainfree+=1
                if helper_pair(rows[a],mains):
                    twohelper+=1;h,g=sorted(support)
                    need(h in helpers and g in helpers,'only helper support')
                    ih,ig=w['initial'][h],w['initial'][g];fh,fg=w['final'][h],w['final'][g]
                    if ih!=ig:
                        exclusions['different_initial_ID']+=1
                        excluded.append(dict(event=event,h=h,g=g,initial=[ih,ig],reason='different_initial_frame_ID'))
                        if spaces[ih]==spaces[ig]:aliases.append(dict(event=event,h=h,g=g,initial=[ih,ig]))
                    elif not(spaces[fh]<=spaces[fg] or spaces[fg]<=spaces[fh]):
                        exclusions['incomparable_final_spaces']+=1
                        excluded.append(dict(event=event,h=h,g=g,final=[fh,fg],reason='incomparable_final_spaces'))
                    else:
                        q=-rows[a][g]/rows[a][h]
                        families[h,g,q].append(dict(event=event,owner=a,owned=bool(e[4]),rank=r,
                            coefficients={str(h):str(rows[a][h]),str(g):str(rows[a][g])}))
            charts[a]=e[3];fresh.discard(a)
        elif op=='INIT':
            need(a>=n and charts[a] is None,'owned fresh INIT');rows[a],charts[a]={},e[2];fresh.add(a)
        elif op=='CLEAR':
            need(a>=n and charts[a]==e[2],'owned CLEAR');rows[a],charts[a]=None,None;fresh.discard(a)
        elif op=='SCALE':
            need(charts[a]==e[-1],'SCALE chart');q=scalar(e[2]);need(q!=0,'nonzero scalar')
            rows[a]={k:q*v for k,v in rows[a].items() if q*v};fresh.discard(a)
        elif op in ('ADD','COPY'):
            b=e[2];need(charts[a]==charts[b]==e[-1],'cocharted scalar operands')
            if op=='COPY':need(a>=n and a in fresh and not rows[a],'owned fresh-zero COPY')
            add(rows[a],rows[b],scalar(e[3]));fresh.discard(a)
        else:raise ValueError(op)
    need(charts==w['final']+[None]*w['owned_fields'],'all endpoint/lifetime charts')
    need(all(rows[h]=={h:Q(1)} for h in helpers),'every helper endpoint is own unit row')
    need(all(not(set(rows[r])&helpers) for r in mains),'main endpoints independent of helper inputs')
    candidates=[]
    for (h,g,q),events in sorted(families.items(),key=lambda t:(t[0][0],t[0][1],t[0][2])):
        P=Counter(e['rank'] for e in events)
        for demoted,kept,value in ((h,g,q),(g,h,1/q)):
            f0,fd,fk=w['initial'][demoted],w['final'][demoted],w['final'][kept]
            R=abs(len(w['frames'][fd])-len(w['frames'][f0]));d=abs(len(w['frames'][fd])-len(w['frames'][fk]))
            need(R>0,'original helper productive rank positive')
            v=gain(P,R,d)
            need(all(Q(e['coefficients'][str(demoted)])*value+Q(e['coefficients'][str(kept)])==0 for e in events),
                 'oriented correlation cancels every grouped row')
            candidates.append(dict(demoted=demoted,kept=kept,q=str(value),initial_frame=f0,
                demoted_final=fd,kept_final=fk,matching_boundary=fd==fk,lost_target_rank=R,cleanup_rank=d,
                removed_paid=dict(P),removed_moves=events,vertices_min_r_k=v,cone_dominated=max(v)<=0,
                signed17_vertices_min_r_k=[calls*x for x in v],
                single_removed_rank_dominated=sum(P.values())==1 and next(iter(P))<=R))
    need(len({e['event'] for es in families.values() for e in es})==sum(map(len,families.values())),
         'each MOVE assigned to exactly one family')
    result=dict(status='COMPLETE_EXACT_TWO_HELPER_CORRELATION_CENSUS',source_sha256=PIN,
        caller_sha256=CALLER_PIN,native_calls=calls,
        instructions=len(w['program']),moves=sum(paid.values()),mainfree_moves=mainfree,
        exact_two_helper_moves=twohelper,excluded_two_helper_moves=dict(exclusions),excluded_rows=excluded,
        equal_initial_space_different_ID=aliases,
        correlation_families=len(families),removable_moves=sum(map(len,families.values())),oriented_candidates=len(candidates),
        matching_boundary_candidates=sum(c['matching_boundary'] for c in candidates),
        cone_dominated_candidates=sum(c['cone_dominated'] for c in candidates),
        all_nine_integer_tariffs_nonpositive=all(c['cone_dominated'] for c in candidates),
        all_single_removed_ranks_dominated=all(c['single_removed_rank_dominated'] for c in candidates),
        matching_boundary_neutral_candidates=sum(c['matching_boundary'] and not any(c['vertices_min_r_k']) for c in candidates),
        helper_endpoints_verified=True,main_endpoints_independent_of_helpers=True,controls=tested,
        candidates=candidates,seconds=time.monotonic()-start,
        scope='One h=q*g; identical entrance chart ID, nested final spaces; unchanged native scalars. Debit h target and final cleanup child. All pricing checks exact integers; no changed word emitted.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='candidates'},indent=2))
    print('unequal_boundary',json.dumps([c for c in candidates if not c['matching_boundary']],indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'reference/pr7481/WORD.json.gz')
    p.add_argument('--caller',type=Path,default=ROOT/'reference/pr7481/CALLER-EXACT.json')
    p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--seconds',type=float,default=60)
    a=p.parse_args();run(a.source,a.output,a.seconds,a.caller)
