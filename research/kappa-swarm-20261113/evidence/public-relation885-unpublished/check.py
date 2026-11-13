#!/usr/bin/env python3
"""All-cut exact #7481 audit for u=-e1459-e705+e885 only."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict,Counter
from hashlib import sha256
import argparse,gzip,json,math,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
U={1459:Q(-1),705:Q(-1),885:Q(1)}
PRIME=1000033
def need(ok,label):
    if not ok:raise ValueError(label)
def add(a,b,q):
    for h,v in b.items():
        z=a.get(h,0)+q*v
        if z:a[h]=z
        else:a.pop(h,None)
def framekey(frame):
    s={0}
    for u in frame:
        need(0<u<512 and u not in s,'independent frame basis');s|={v^u for v in s}
    return tuple(sorted(s))
def quotient(row):
    v=row.copy();q=v.pop(1459,Q(0))
    if q:add(v,{885:Q(1),705:Q(-1)},q)
    return v
def column_rank(columns,expected):
    """Full-size modular minor certificate; exact row-count is the Q upper bound."""
    basis={};pivots=[]
    for h,col in sorted(columns.items(),key=lambda x:(len(x[1]),x[0])):
        v=col.copy()
        while v:
            p=max(v)
            if p not in basis:
                a=v[p];iv=pow(a,PRIME-2,PRIME);basis[p]={j:t*iv%PRIME for j,t in v.items()};pivots.append([h,p,a]);break
            q=v[p]
            for j,t in basis[p].items():
                z=(v.get(j,0)-q*t)%PRIME
                if z:v[j]=z
                else:v.pop(j,None)
        if len(basis)==expected:break
    return {'rank_mod':len(basis),'literal_row_upper_bound':expected,'full_row_rank':len(basis)==expected,'pivot_columns_rows_values':pivots}
def exact_expression(bank,target):
    basis={};lifts={}
    for i,o in enumerate(bank):
        v=o['row'].copy();w={i:Q(1)}
        for p in sorted(basis,reverse=True):
            if v.get(p):q=v[p];add(v,basis[p],-q);add(w,lifts[p],-q)
        need(v,'original coframe rows exactly independent')
        p=max(v);q=1/v[p];basis[p]={h:a*q for h,a in v.items()};lifts[p]={j:a*q for j,a in w.items()}
    v=target.copy();answer={}
    for p in sorted(basis,reverse=True):
        if v.get(p):q=v[p];add(v,basis[p],-q);add(answer,lifts[p],q)
    need(not v,'modular candidate must receive an exact rational expression')
    actual={}
    for i,q in answer.items():add(actual,bank[i]['row'],q)
    need(actual==target,'direct rational identity verifies expression')
    return answer
def encode(row):return {str(h):str(a) for h,a in sorted(row.items())}
def run(source,output):
    start=time.monotonic();raw=source.read_bytes();need(sha256(raw).hexdigest()==PIN,'exact source bytes')
    need(all(PRIME%d for d in range(2,math.isqrt(PRIME)+1)),'certificate prime')
    w=json.loads(gzip.decompress(raw));classes=list(map(framekey,w['frames']));aliases=defaultdict(list)
    for f,k in enumerate(classes):aliases[k].append(f)
    n=w['public'];mains=set(w['live'])|{h+112 for h in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);helpers=set(range(n))-mains
    need(set(U)<=helpers and len(mains)==400 and len(helpers)==1101,'relation only on independent helper inputs')
    target_ranks={h:abs(len(w['frames'][w['initial'][h]])-len(w['frames'][w['final'][h]])) for h in U}
    need(target_ranks=={1459:1,705:8,885:8},'actual sacrificed and donor target ranks')
    rows=[{h:Q(1)} for h in range(n)]+[None]*w['owned_fields'];cur=w['initial'].copy()+[None]*w['owned_fields'];banks=defaultdict(list);moves={};zeros=[];ops=Counter();observed=set()
    def observe(event,a,f,kind):
        observed.add(f);o={'event':event,'owner':a,'frame':f,'kind':kind,'row':rows[a].copy()};banks[classes[f]].append(o)
    for h,f in enumerate(w['initial']):observe(-1,h,f,'initial')
    for event,e in enumerate(w['program']):
        if event%256==0:need(time.monotonic()-start<120,'bounded fresh replay')
        op,a=e[:2];ops[op]+=1
        if op=='MOVE':
            old,new=e[2:4];need(cur[a]==old and rows[a] and bool(e[4])==(a>=n),'actual nonzero live MOVE')
            left,right=set(classes[old]),set(classes[new]);need(left<right if a<n else left<right or right<left,'strict nesting')
            rank=abs(len(w['frames'][old])-len(w['frames'][new]));need(rank>0,'positive paid rank')
            moves[event]={'event':event,'literal':e,'rank':rank,'row':rows[a].copy()}
            if not quotient(rows[a]):zeros.append(event)
            cur[a]=new;observe(event,a,new,'arrival')
        elif op=='INIT':
            need(a>=n and cur[a] is None and rows[a] is None,'fresh owned INIT');cur[a]=e[2];rows[a]={}
        elif op=='CLEAR':
            need(a>=n and cur[a]==e[2] and rows[a] is not None,'owned CLEAR');cur[a]=None;rows[a]=None
        elif op=='SCALE':
            need(cur[a]==e[-1] and Q(e[2]),'coframed nonzero SCALE');q=Q(e[2]);rows[a]={h:q*v for h,v in rows[a].items()}
        elif op in ['ADD','COPY']:
            b=e[2];need(a!=b and cur[a]==cur[b]==e[-1],'coframed scalar contact')
            if op=='COPY':need(a>=n and not rows[a],'COPY into zero')
            add(rows[a],rows[b],Q(e[3]))
        else:raise ValueError(op)
    need(cur==w['final']+[None]*w['owned_fields'],'complete endpoints/lifetimes')
    need(len(moves)==6279 and sum(map(len,banks.values()))==7780,'all cuts and observations')
    replay_seconds=time.monotonic()-start
    print(json.dumps({'phase':'fresh_Q_replay_complete','MOVEs':len(moves),'coframes':len(banks),'seconds':replay_seconds}),flush=True)
    inverses={};records=[];hits=[];rank_total=0;aug_rank_total=0;all_independent=True
    def mod(q):
        if q.denominator not in inverses:
            need(q.denominator%PRIME,'all rational denominators invertible');inverses[q.denominator]=pow(q.denominator%PRIME,PRIME-2,PRIME)
        return q.numerator*inverses[q.denominator]%PRIME
    for key,bank in sorted(banks.items(),key=lambda x:aliases[x[0]][0]):
        need(time.monotonic()-start<120,'bounded matrix certificate')
        columns=defaultdict(dict);m=len(bank);digest=sha256()
        for i,o in enumerate(bank):
            digest.update((json.dumps([{k:v for k,v in o.items() if k!='row'},encode(o['row'])],sort_keys=True,separators=(',',':'))+'\n').encode())
            for h,q in o['row'].items():
                value=mod(q)
                if value:columns[h][i]=value
        original=column_rank(columns,m);need(original['full_row_rank'],'original coframe exact rank equals row-count upper bound');rank_total+=m
        augmented={h:v.copy() for h,v in columns.items()}
        for h,q in U.items():augmented.setdefault(h,{})[m]=mod(q)
        augmented_cert=column_rank(augmented,m+1);aug_rank_total+=augmented_cert['rank_mod']
        doc={'frame_ids':aliases[key],'observed_frame_ids':sorted(set(o['frame'] for o in bank)),'row_count':m,'exact_matrix_sha256':digest.hexdigest(),'original_full_row_rank_certificate':original,'augmented_certificate':augmented_cert}
        need(len(doc['observed_frame_ids'])==1,'no used nonidentical frame alias is silently pooled')
        if not augmented_cert['full_row_rank']:
            need(augmented_cert['rank_mod']==m,'one appended relation loses at most one rank')
            expression=exact_expression(bank,U)
            witness=[{'observation':{k:v for k,v in bank[i].items() if k!='row'},'coefficient':str(q),'row':encode(bank[i]['row'])} for i,q in sorted(expression.items())]
            last=max(expression,key=lambda i:(bank[i]['event'],i));last_o=bank[last]
            doc['relation_in_final_span_exact']=True;doc['unique_expression']=witness
            if last_o['kind']=='arrival':
                e=last_o['event'];q=expression[last];providers=[]
                for i,a in expression.items():
                    if i!=last:
                        need(bank[i]['event']<e,'all exact providers strictly precede target')
                        providers.append({'observation':{k:v for k,v in bank[i].items() if k!='row'},'coefficient':str(-a/q),'row':encode(bank[i]['row'])})
                residual=moves[e]['row'].copy()
                for provider in providers:add(residual,{int(h):Q(a) for h,a in provider['row'].items()},-Q(provider['coefficient']))
                need(residual=={h:a/q for h,a in U.items()},'direct target = strict history + relation witness')
                hit={'event':e,'literal':moves[e]['literal'],'rank':moves[e]['rank'],'zero':e in zeros,'target_row':encode(moves[e]['row']),'relation_coefficient':str(1/q),'providers':providers}
                hits.append(hit);doc['last_support_MOVE']=e
        else:doc['relation_in_final_span_exact']=False
        records.append(doc)
    need(rank_total==7780 and len(records)==len(banks),'complete exact original rank certificates')
    eligible=sorted(set(zeros)|{h['event'] for h in hits});credit=Counter(moves[e]['rank'] for e in eligible)
    signed=credit.copy();signed.subtract({1:1,8:1});signed={r:a for r,a in signed.items() if a}
    need(not zeros and eligible==[40710] and signed=={1:-1},'complete exact candidate list and cancelling budget')
    need(set(zeros)<={h['event'] for h in hits},'zero targets included in relation circuit census')
    # A dependent modular history can have a false modular nonmembership.
    # It cannot receive our full-row-count certificate.
    bad_columns={0:{0:1,1:1},1:{2:1}}
    fake_history=[{'row':{0:Q(1)}},{'row':{0:Q(1),1:Q(PRIME)}}]
    need(exact_expression(fake_history,{1:Q(1)})=={0:-Q(1,PRIME),1:Q(1,PRIME)},'rational target belongs to a rank-dropped modular history')
    need(not column_rank(bad_columns,3)['full_row_rank'],'bare modular miss without rational upper rank rejected')
    need(quotient(U)=={} and quotient({885:Q(1)}),'one relation only; no independent coordinate-zero shortcut')
    try:exact_expression([{'row':{0:Q(1),1:Q(-1)}}],{0:Q(1)})
    except ValueError:pass
    else:raise ValueError('early circuit member falsely gets history credit')
    need(exact_expression([{'row':{0:Q(1)}},{'row':{0:Q(1),1:Q(-1)}}],{1:Q(1)})=={0:Q(1),1:Q(-1)},'only last circuit member is enabled')
    if 40710 in eligible:
        h=next(h for h in hits if h['event']==40710)
        need(all(p['observation']['event']<40710 for p in h['providers']),'strict earlier provider control')
        need(w['program'][40710]==['MOVE',885,3,189,False],'actual motivating event')
        bad=moves[40710]['row'].copy()
        for i,p in enumerate(h['providers']):add(bad,{int(j):Q(v) for j,v in p['row'].items()},Q(p['coefficient']) if i==0 else -Q(p['coefficient']))
        need(bad!={j:q*Q(h['relation_coefficient']) for j,q in U.items()},'wrong provider sign rejected by direct source identity')
    out={'status':'COMPLETE_EXACT_SINGLE_RELATION_ALL_MOVE_HISTORY_CENSUS','source_sha256':PIN,'source_payload_sha256':sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'promise':encode(U),'all_other_inputs_arbitrary':True,'prime':PRIME,'original_MOVEs':len(moves),'original_observations':rank_total,'coframe_count':len(records),'original_all_prefixes_independent':True,'zero_MOVE_events':sorted(zeros),'new_history_reconstructible_events':sorted(h['event'] for h in hits),'eligible_MOVE_events_union':eligible,'credit_histogram':dict(credit),'lost_target':{'helper':1459,'rank':1},'known_minimum_preparation_transport_rank':8,'optimistic_native_gain_profile':signed,'hits':hits,'coframes':records,'distinct_denominators':len(inverses),'controls':{'wrong_coordinate_zero_substitution':'REJECTED','bare_modular_miss_without_full_row_rank':'REJECTED','target_arrival_not_a_strict_provider':'PASS','earlier_circuit_member':'REJECTED','wrong_provider_coefficient_sign':'REJECTED'},'replay_seconds':replay_seconds,'seconds':time.monotonic()-start,'scope':'Only this helper promise, unchanged exact source operations/coframes and all strict original destination histories. Complete all-role/all-rank whole MOVE census. Physical cache/interface, preparation witness, ordinary/storage/return and all foundational assumptions remain separate; known rank8 import lower cost is debited.'}
    output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ['status','zero_MOVE_events','new_history_reconstructible_events','credit_histogram','optimistic_native_gain_profile','seconds']},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=ROOT/'reference/pr7481/WORD.json.gz');ap.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=ap.parse_args();run(a.source,a.output)
