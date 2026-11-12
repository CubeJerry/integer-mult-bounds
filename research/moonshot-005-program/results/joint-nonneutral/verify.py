#!/usr/bin/env python3
"""Exact joint impulse screen for the103 prescribed source cases,58 cuts."""
import argparse,gzip,hashlib,json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def check(v,s):
    if not v:raise ValueError(s)
def axpy(a,b,c=F(1)):
    for k,v in tuple(b.items()):
        z=a.get(k,F(0))+c*v
        if z:a[k]=z
        else:a.pop(k,None)
def encode(r):return [[k,str(v)] for k,v in sorted(r.items())]
def rank_certificate(columns):
    basis={};pivots=[];coefficients=[]
    for label,column in columns:
        z=dict(column)
        for p,b in basis.items():
            if p in z:axpy(z,b,-z[p])
        if z:
            p=min(z);c=z[p];basis[p]={k:v/c for k,v in z.items()};pivots.append([label,p]);coefficients.append(str(c))
    return dict(rank=len(basis),pivot_column_and_output=pivots,pivot_coefficients=coefficients)
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--cases',type=Path,required=True);p.add_argument('--observations',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
raw=args.source.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw))
C=json.loads(args.cases.read_text());O=json.loads(args.observations.read_text());check(C['native_sha256']==PIN and O['source_sha256']==PIN,'input source pins');cases=C['cases'];obs=O['observations']
cuts=sorted({(a['event'],a['helper']) for a in cases});check(len(cuts)==58,'cut census');index={event:i for i,(event,_) in enumerate(cuts)}
scalars={}
def coef(s):
    if s not in scalars:scalars[s]=F(s)
    return scalars[s]
# Independently reconstruct all baseline departure payloads by backward rows.
H=[]
for event,helper in cuts:
    check(w['program'][event][0]=='MOVE' and w['program'][event][1]==helper,'literal cut');a={helper:F(1)}
    for x in reversed(w['program'][:event]):
        op,d,s=x[:3]
        if op=='ADD' and d in a:
            z=a.get(s,F(0))+coef(x[3])*a[d]
            if z:a[s]=z
            else:a.pop(s,None)
        elif op=='SCALE' and d in a:
            a[d]*=coef(s)
            if not a[d]:del a[d]
        elif op=='COPY':
            if d in a:
                v=a.pop(d);z=a.get(s,F(0))+coef(x[3])*v
                if z:a[s]=z
                else:a.pop(s,None)
        elif op in ('INIT','CLEAR'):a.pop(d,None)
    check(all(k<w['public'] for k in a),'owned input after backward replay');H.append(a)
hist=defaultdict(list)
for i,a in enumerate(obs):
    k=index[a['event']];check(H[k]=={int(j):F(v) for j,v in a['hrow'].items()},'predecessor payload reproduced')
    for term in a['historical_decoder']:
        if term['after_event']>=0:hist[term['after_event']].append((i,term['role'],F(term['coefficient'])))
# All58 independent additive impulses propagate simultaneously.
R=[{} for _ in range(w['public']+w['owned_fields'])];L=[];B=[{} for _ in obs];guards=[]
for event,x in enumerate(w['program']):
    op,d,s=x[:3]
    if event in index:
        k=index[event];check(cuts[k][1]==d,'cut role');L.append(dict(R[d]));R[d][k]=R[d].get(k,F(0))+1;check(all(j<k for j in L[-1]),'chronological L')
    if op=='ADD':axpy(R[d],R[s],coef(x[3]))
    elif op=='SCALE':R[d]={j:coef(s)*v for j,v in R[d].items() if coef(s)*v}
    elif op=='COPY':guards.append(dict(event=event,response=encode(R[d])));R[d]={j:coef(x[3])*v for j,v in R[s].items() if coef(x[3])*v}
    elif op in ('INIT','CLEAR'):R[d]={}
    elif op!='MOVE':raise ValueError(op)
    for i,role,c in hist[event]:axpy(B[i],R[role],c)
hub={j for j in range(w['public']) if set(w['frames'][w['final'][j]])=={1,2,4,8,16,32,64,128,256}}
check(len(hub)==1022,'hub output count');Z=[{} for _ in cuts]
for role,row in enumerate(R[:w['public']]):
    if role not in hub:
        for k,v in row.items():Z[k][role]=v
for a,row in zip(obs,B):
    k=index[a['event']];check(row.get(k,F(0))==F(a['decoder_sensitivity']),'individual sensitivity');check(Z[k]=={int(j):F(v) for j,v in a['offhub_suffix_rows'].items()},'predecessor response reproduced')
first=set(w['live']);unit=[k for k,h in enumerate(H) if len(h)==1 and next(iter(h.values()))==1 and next(iter(h)) in first];obscols=[index[a['event']] for a in obs];unitobs=[k for k in obscols if k in unit];firstcols=[k for k,(event,_) in enumerate(cuts) if any(a['event']==event and a['donor'] in first for a in cases)]
families={name:rank_certificate([(k,Z[k]) for k in family]) for name,family in [('all58',list(range(len(cuts)))),('first_donor_events',firstcols),('admitted31',obscols),('unit_payload_first_donors',unit),('admitted_unit_payloads',unitobs)]}
Ds=[];T=[]
for i,a in enumerate(obs):
    k=index[a['event']];t={j:L[k].get(j,F(0)) for j in obscols if L[k].get(j,F(0))};t[k]=F(1)/F(a['gain']);d={j:v for j,v in B[i].items() if j in obscols};axpy(d,t,-1);T.append(t);Ds.append(d)
cross=rank_certificate([(i,r) for i,r in enumerate(Ds)])
receipt=dict(schema='joint-prescribed-nonneutral-pulse-screen-v1',source_sha256=PIN,case_file_sha256=hashlib.sha256(args.cases.read_bytes()).hexdigest(),observation_file_sha256=hashlib.sha256(args.observations.read_bytes()).hexdigest(),cuts=[dict(index=k,event=e,helper=h,first_donors=sorted({a['donor'] for a in cases if a['event']==e and a['donor'] in first})) for k,(e,h) in enumerate(cuts)],H=[encode(h) for h in H],chronological_L=[encode(l) for l in L],offhub_columns=[encode(z) for z in Z],copy_guards=guards,family_rank_certificates=families,unit_payload_indices=unit,admitted_observer_donors=[a['donor'] for a in obs],admitted_observer_cut_indices=obscols,admitted_decoder_B=[encode(b) for b in B],admitted_joint_encoder_T=[encode(t) for t in T],admitted_decoder_mismatch_B_minus_T=[encode(d) for d in Ds],admitted_decoder_mismatch_rank=cross,status='Exact finite-family joint impulse accounting; no complete restored source construction and no new kappa.')
payload=(json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(gzip.compress(payload,mtime=0) if args.output.suffix=='.gz' else payload)
print(json.dumps(dict(family_ranks={k:v['rank'] for k,v in families.items()},unit_payload_count=len(unit),joint31_decoder_mismatch_rank=cross['rank'],copy_guard_support=[len(g['response']) for g in guards]),sort_keys=True))
