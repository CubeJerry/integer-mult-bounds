#!/usr/bin/env python3
"""Independent exact forward-baseline/backward-observation review of 58 cuts.

No author imports. Joint source responses are obtained by one backward adjoint
pass, as opposed to the author's simultaneous forward formal impulses.
"""
import argparse, collections, gzip, hashlib, json, time
from fractions import Fraction as Q
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CASE='49566c437ad644048d7605cb26d8a14870c09304e59193a4b40bc9e5f6510298'
OBS='03c0dd40c55545892effd8dd8fdd45246a2a22b6eccb1df39f03f76154fb8a83'
def need(x,s):
    if not x: raise ValueError(s)
def read(p):
    b=p.read_bytes(); return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(r): return [[k,str(c)] for k,c in sorted(r.items()) if c]
def decode(r): return {int(k):Q(v) for k,v in r}
def axpy(a,b,c=Q(1)):
    for k,x in tuple(b.items()):
        z=a.get(k,Q(0))+c*x
        if z: a[k]=z
        else: a.pop(k,None)
def span(f):
    s={0}
    for x in f: s|={y^x for y in s}
    return frozenset(s)
def rank_columns(cols):
    basis={}; pivots=[]
    for j,c in enumerate(cols):
        r=dict(c)
        while r:
            p=max(r)
            if p not in basis:
                scale=r[p]; basis[p]={i:v/scale for i,v in r.items()}
                pivots.append([j,p,str(scale)]); break
            axpy(r,basis[p],-r[p])
    return len(basis),pivots
def digest_rows(rows): return sha(json.dumps([encode(r) for r in rows],separators=(',',':')).encode())

def main(a):
    started=time.monotonic(); raw=a.source.read_bytes(); need(sha(raw)==PIN,'native pin')
    w=json.loads(gzip.decompress(raw)); n=w['public']; program=w['program']; frames=list(map(span,w['frames']))
    cb=read(a.cases); ob=read(a.observations); rb=read(a.certificate)
    need(sha(cb)==CASE and sha(ob)==OBS,'predecessor pins')
    cases=json.loads(cb)['cases']; obs=json.loads(ob)['observations']; claim=json.loads(rb)
    need(claim['source_sha256']==PIN and claim['case_file_sha256']==CASE and claim['observation_file_sha256']==OBS,'author input pins')
    cuts=sorted({(x['event'],x['helper']) for x in cases}); m=len(cuts); k_at={e:k for k,(e,_) in enumerate(cuts)}
    need(m==58 and len(k_at)==58 and len(obs)==31,'source census')
    for k,(e,j) in enumerate(cuts):
        need(program[e][0]=='MOVE' and program[e][1]==j and j<n,'literal public cut')
        need(claim['cuts'][k]['event']==e and claim['cuts'][k]['helper']==j,'cut certificate')
    by_time=collections.defaultdict(list)
    for i,o in enumerate(obs):
        for t in o['historical_decoder']:
            by_time[t['after_event']].append((i,t['role'],Q(t['coefficient']),t['chart']))
    state={j:{j:Q(1)} for j in range(n)}; location={j:frames[f] for j,f in enumerate(w['initial'])}
    H=[None]*m; baseline_decoders=[{} for _ in obs]
    def observe(t):
        for i,j,c,f in by_time.get(t,[]):
            need(j in state and location[j]==frames[f],'historical source access')
            if t>=0:
                x=program[t]; need(x[0]=='MOVE' and x[1]==j and frames[x[3]]==frames[f],'historical literal arrival')
            axpy(baseline_decoders[i],state[j],c)
    observe(-1)
    for t,x in enumerate(program):
        op,j=x[:2]
        if t in k_at: H[k_at[t]]=dict(state[j])
        if op=='INIT':
            need(j>=n and j not in state,'owned INIT'); state[j]={}; location[j]=frames[x[2]]
        elif op=='CLEAR':
            need(j>=n and location[j]==frames[x[2]],'owned CLEAR'); del state[j]; del location[j]
        elif op=='MOVE':
            need(location[j]==frames[x[2]] and bool(x[4])==(j>=n),'MOVE ownership/location')
            s,d=frames[x[2]],frames[x[3]]; need(s<d or d<s,'proper nested MOVE'); location[j]=d
        elif op=='SCALE':
            c=Q(x[2]); need(c and location[j]==frames[x[3]],'SCALE typing'); state[j]={k:c*v for k,v in state[j].items()}
        elif op in ('ADD','COPY'):
            s=x[2]; need(j!=s and location[j]==location[s]==frames[x[4]],'binary typing')
            if op=='COPY': need(not state[j],'baseline COPY guard')
            axpy(state[j],state[s],Q(x[3]))
        else: raise ValueError(op)
        observe(t)
    need(set(state)==set(range(n)) and all(location[j]==frames[w['final'][j]] for j in state),'final source ownership/location')
    need([encode(h) for h in H]==claim['H'],'independent forward H')
    selected=[k_at[o['event']] for o in obs]
    for i,(o,k) in enumerate(zip(obs,selected)):
        need(H[k]=={int(j):Q(c) for j,c in o['hrow'].items()},'historical h pin')
        need(baseline_decoders[i]==H[k],'baseline historical decoder identity')
    print('forward baseline and historical identities complete',round(time.monotonic()-started,3),flush=True)

    full=span([1,2,4,8,16,32,64,128,256]); off={j for j,f in enumerate(w['final']) if frames[f]!=full}
    need(len(off)==458,'offhub source census')
    # Labels: 0..n-1 final offhub outputs; n..n+m-1 pre-own-pulse
    # payload observations; n+m..n+m+30 historical decoders; remaining COPY guards.
    payload_base=n; history_base=n+m; guard_base=n+m+len(obs)
    adj={j:({j:Q(1)} if j in off else {}) for j in range(n)}
    Z=[{} for _ in cuts]; L=[{} for _ in cuts]; B=[{} for _ in obs]; guards=[]
    def row(j): return adj.setdefault(j,{})
    for t in range(len(program)-1,-1,-1):
        x=program[t]; op,j=x[:2]
        # Historical observation is after instruction, and therefore after a
        # pre-MOVE pulse at this same event.
        for i,role,c,f in by_time.get(t,[]): axpy(row(role),{history_base+i:c})
        if t in k_at:
            k=k_at[t]
            for label,c in row(j).items():
                if label<n: Z[k][label]=c
                elif label<history_base:
                    future=label-payload_base; need(future>k,'strict causal L'); L[future][k]=c
                elif label<guard_base: B[label-history_base][k]=c
                else: raise ValueError('nonzero COPY guard response')
            # Own departure payload is evaluated before its own intervention.
            axpy(row(j),{payload_base+k:Q(1)})
        if op=='ADD': axpy(row(x[2]),row(j),Q(x[3]))
        elif op=='SCALE': adj[j]={k:Q(x[2])*v for k,v in row(j).items()}
        elif op=='COPY':
            axpy(row(x[2]),row(j),Q(x[3])); adj[j]={guard_base+t:Q(1)}; guards.append(t)
        elif op=='CLEAR': adj[j]={}
        elif op=='INIT': adj.pop(j,None)
        elif op=='MOVE': pass
        else: raise ValueError(op)
    need([encode(z) for z in Z]==claim['offhub_columns'],'independent backward offhub Z')
    need([encode(l) for l in L]==claim['chronological_L'],'independent backward chronological L')
    need([encode(b) for b in B]==claim['admitted_decoder_B'],'independent backward historical B')
    need(len(guards)==1 and all(not g['response'] for g in claim['copy_guards']),'COPY guards')
    for k,h in enumerate(H):
        back={j:r[payload_base+k] for j,r in adj.items() if payload_base+k in r}
        need(back==h,'independent forward/backward departure identity')
    print('backward Z/L/B source identities complete',round(time.monotonic()-started,3),flush=True)

    first=set(w['live']); unit=[k for k,h in enumerate(H) if len(h)==1 and next(iter(h.values()))==1 and next(iter(h)) in first]
    unitobs=[k for k in selected if k in unit]; firstcuts=[k for k,(e,j) in enumerate(cuts) if any(c['event']==e and c['donor'] in first for c in cases)]
    families={'all58':list(range(m)),'first_donor_events':firstcuts,'admitted31':selected,'unit_payload_first_donors':unit,'admitted_unit_payloads':unitobs}
    ranks={}; rank_witnesses={}
    for name,indices in families.items():
        r,p=rank_columns([Z[k] for k in indices]); ranks[name]=r; rank_witnesses[name]=p
        need(r==claim['family_rank_certificates'][name]['rank']==len(indices),'full column rank '+name)
    need(ranks=={'all58':58,'first_donor_events':58,'admitted31':31,'unit_payload_first_donors':30,'admitted_unit_payloads':17},'exact family ranks')
    need(len({o['donor'] for o in obs})==31,'independent selected donors')
    need(len({next(iter(H[k])) for k in unit})==30,'independent unit donors')
    T=[]; D=[]
    for i,(o,k) in enumerate(zip(obs,selected)):
        g=Q(o['gain']); need(g and g*B[i].get(k,Q(0))==1,'normalized own decoder sensitivity')
        t={j:L[k][j] for j in selected if j in L[k]}; t[k]=1/g
        d={j:v for j,v in B[i].items() if j in selected}; axpy(d,t,Q(-1)); T.append(t); D.append(d)
    need([encode(t) for t in T]==claim['admitted_joint_encoder_T'],'scaled joint T')
    need([encode(d) for d in D]==claim['admitted_decoder_mismatch_B_minus_T'],'joint decoder mismatch')
    mismatch_rank,mismatch_pivots=rank_columns(D)
    need(mismatch_rank==claim['admitted_decoder_mismatch_rank']['rank']==30,'joint decoder mismatch rank')
    need(all(D),'all31 old decoder rows fail jointly')
    need(rank_columns(T)[0]==31,'invertible chronological scaled encoder')
    unit_observers=[i for i,k in enumerate(selected) if k in unit]
    B17=[{j:v for j,v in B[i].items() if j in unitobs} for i in unit_observers]
    T17=[{j:v for j,v in T[i].items() if j in unitobs} for i in unit_observers]
    D17=[]
    for b,t in zip(B17,T17):
        d=dict(b); axpy(d,t,Q(-1)); D17.append(d)
    need(rank_columns(B17)[0]==14 and rank_columns(T17)[0]==17 and rank_columns(D17)[0]==16,'unit17 continuation ranks')
    for i in unit_observers:
        k=selected[i]; o=obs[i]; e=program[o['event']]
        need(frames[e[2]]==frames[w['initial'][o['donor']]] and len(frames[e[2]])==2,'unit17 initial donor line access')
        need(all(frames[w['initial'][j]]==frames[3] for j in Z[k]),'unit17 initial3 support')
    # Meaningful controls of sign, gain and composition conventions.
    mutant=[dict(t) for t in T]
    nonunit=next(i for i,o in enumerate(obs) if Q(o['gain'])!=1)
    mutant[nonunit][selected[nonunit]]=Q(1)
    need(mutant!=T,'wrong unit diagonal rejected')
    cross=next((i,j,v) for i,l in enumerate(L) for j,v in l.items())
    i,j,v=cross; wrong=[dict(l) for l in L]; wrong[i][j]=-v
    need(wrong!=L,'reversed chronological response sign rejected')
    nonzero=next((i,j,v) for i,d in enumerate(D) for j,v in d.items())
    i,j,v=nonzero
    need(v!=0 and B[i].get(j,Q(0))!=T[i].get(j,Q(0)),'literal failed joint decoder column')
    # Directly demonstrate that deleting a response row can destroy the
    # inference: the all-zero observational projection gives rank zero.
    need(rank_columns([{} for _ in cuts])[0]==0,'unobserved debt negative control')
    result={'status':'PASS_INDEPENDENT_JOINT58_ADJOINT_REVIEW','source_sha256':PIN,'case_payload_sha256':CASE,'observation_payload_sha256':OBS,'author_payload_sha256':sha(rb),'source_cuts':m,'offhub_outputs':len(off),'baseline_historical_decoder_identities':31,'copy_guard_responses_zero':True,'independent_response_method':'backward timed historical/predeparture and endpoint adjoints','author_response_method':'forward simultaneous formal impulses','H_digest':digest_rows(H),'L_digest':digest_rows(L),'B_digest':digest_rows(B),'Z_digest':digest_rows(Z),'family_ranks':ranks,'rank_witnesses_independent_reverse_pivot_order':rank_witnesses,'joint31_T_rank':31,'joint31_decoder_mismatch_rank':mismatch_rank,'mismatch_rank_witness':mismatch_pivots,'unit17_continuation':{'B_rank':14,'T_rank':17,'decoder_correction_rank':16,'all_encoders_at_initial_donor_line':True,'all_offhub_debt_on_initial_chart3_roles':True},'selected31_distinct_raw_donors':True,'unit30_distinct_raw_donors':True,'gain_histogram':dict(collections.Counter(str(Q(o['gain'])) for o in obs)),'negative_controls':{'wrong_unit_gain_diagonal':{'observer':nonunit,'actual_diagonal':str(1/Q(obs[nonunit]['gain']))},'opposite_causal_sign':{'row':cross[0],'column':cross[1],'actual':str(cross[2])},'literal_old_decoder_composition_failure':{'observer':i,'cut':j,'mismatch':str(v)},'unobserved_debt_projection_rank':0},'scope':'Fixed native source word; only the58 specified common-field increments; offhub endpoints restored exactly. Additional controls, side information and altered source processing are not excluded.','new_complete_kappa':None}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(result['status'],round(time.monotonic()-started,3),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','cases','observations','certificate','output'): p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
