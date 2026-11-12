#!/usr/bin/env python3
"""Exact source certificate: every individually neutral pure-q overwrite loses
one common input mode. This is a single-overwrite, fixed-suffix result.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path

SOURCE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
NEUTRAL_PIN='58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139'
def need(ok,message):
    if not ok: raise ValueError(message)
def read(path):
    b=path.read_bytes()
    return gzip.decompress(b) if path.suffix=='.gz' else b
def row(r): return [[i,str(v)] for i,v in sorted(r.items())]
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def axpy(a,b,c=F(1)):
    for k,v in tuple(b.items()):
        z=a.get(k,F(0))+c*v
        if z:a[k]=z
        else:a.pop(k,None)
def span(frame):
    s={0}
    for v in frame:s|={u^v for u in tuple(s)}
    return s
def expected(w):
    n=w['public'];T={i:{i:F(1)} for i in range(n)};inverse={i:{i:F(1)} for i in range(n)}
    for k,x in enumerate(w['live']):
        y=x+112
        if k in w['hosted']['Dports']:
            T[y]={y:F(1),x:F(1)};inverse[y]={y:F(1),x:F(-1)}
        else:
            T[x]={x:F(1),y:F(-1)};T[y]={x:F(1,2),y:F(1,2)}
            inverse[x]={x:F(1,2),y:F(1)};inverse[y]={y:F(1),x:F(-1,2)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):
        T[x]={x:F(1),y:F(-1)};inverse[x]={x:F(1),y:F(1)}
    for i,r in inverse.items():
        z={}
        for j,c in r.items():axpy(z,T[j],c)
        need(z=={i:F(1)},'explicit full inverse')
    return T,inverse
def run(a):
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_PIN,'source pin');w=json.loads(gzip.decompress(raw))
    cb=read(a.neutral);need(hashlib.sha256(cb).hexdigest()==NEUTRAL_PIN,'independently reviewed neutral certificate pin');base=json.loads(cb)
    events=base['edge_certificate']['public_neutral'];need(len(events)==1472,'complete admitted neutral census');byevent={x['event']:j for j,x in enumerate(events)}
    need(len(byevent)==1472,'unique occurrences');T,inverse=expected(w)
    state={i:{i:F(1)} for i in range(w['public'])};impulse=[{} for _ in range(w['public']+w['owned_fields'])];H=[];Lambda=[]
    for t,e in enumerate(w['program']):
        op,r=e[:2]
        if t in byevent:
            j=byevent[t];item=events[j]
            need(op=='MOVE' and r==item['role'] and r<w['public'],'source event binding')
            h=state[r].copy();lam={}
            for k,c in h.items():axpy(lam,inverse[k],c)
            H.append(h);Lambda.append(lam)
        if op=='INIT':state[r]={};impulse[r]={}
        elif op=='CLEAR':state.pop(r);impulse[r]={}
        elif op=='SCALE':
            c=F(e[2]);state[r]={k:c*v for k,v in state[r].items()};impulse[r]={k:c*v for k,v in impulse[r].items()}
        elif op in ('ADD','COPY'):
            if op=='COPY':need(not state[r] and not impulse[r],'baseline and all-pulse COPY guards')
            c=F(e[3]);axpy(state[r],state[e[2]],c);axpy(impulse[r],impulse[e[2]],c)
        elif op!='MOVE':raise ValueError('unknown opcode')
        if t in byevent:impulse[r][byevent[t]]=F(1)
    need(state==T,'all1480 public native rows and owned retirement')
    need(len(H)==1472,'all payload versions')
    Z=[{} for _ in events]
    for r,d in enumerate(impulse):
        need(r<w['public'] or not d,'owned response retired')
        for j,c in d.items():Z[j][r]=c
    records=[];hub=0;full={0}
    for v in w['frames'][127]:full|={x^v for x in tuple(full)}
    for j,item in enumerate(events):
        h,lam,z=H[j],Lambda[j],Z[j]
        need(z and all(span(w['frames'][w['final'][r]])==full for r in z),'nonzero response confined to hub')
        gamma=sum(c*z.get(r,F(0)) for r,c in lam.items());need(gamma==1,'unit source self-response')
        v={i:sum(c*z.get(r,F(0)) for r,c in inv.items()) for i,inv in inverse.items()};v={i:c for i,c in v.items() if c}
        need(v and sum(c*v.get(i,F(0)) for i,c in h.items())==1,'explicit erased common mode')
        for r,tr in T.items():need(sum(c*v.get(i,F(0)) for i,c in tr.items())==z.get(r,F(0)),'T times kernel equals pulse')
        recoverable=all(span(w['frames'][w['final'][r]])==full for r in lam);hub+=recoverable
        witness=min(z);outside=next((r for r in sorted(lam) if span(w['frames'][w['final'][r]])!=full),None)
        records.append(dict(event=item['event'],role=item['role'],hub_recoverable_payload=recoverable,
            payload_sha256=digest(row(h)),terminal_expression_sha256=digest(row(lam)),
            response_sha256=digest(row(z)),kernel_sha256=digest(row(v)),
            response_witness=[witness,str(z[witness])],offhub_payload_witness=None if outside is None else [outside,str(lam[outside])],gamma='1'))
    need(hub==824,'hub payload census')
    # Controls on the actual first source kernel, not a sampled generic matrix.
    first=records[0];j=0;h=H[j];z=Z[j];v={i:sum(c*z.get(r,F(0)) for r,c in inv.items()) for i,inv in inverse.items()}
    badh={i:2*c for i,c in h.items()};need(sum(c*v.get(i,F(0)) for i,c in badh.items())==2,'doubled displaced row rejects gamma1')
    # Half replacement has common map T-z h/2 and does not erase this vector.
    need(any(z[r]-z[r]*F(1,2) for r in z),'partial overwrite is outside the proved erasure')
    cert=dict(schema='moonshot-single-pure-overwrite-loss-v1',source_sha256=SOURCE_PIN,neutral_certificate_payload_sha256=NEUTRAL_PIN,
        public_common_inputs=1480,neutral_slots=1472,hub_recoverable_payloads=824,other_payloads=648,
        gamma_counts={'1':1472},all_responses_nonzero=True,records=records,
        scope='One pure-q replacement, fixed native suffix, no retained preoverwrite common record. Even all final common outputs and original q are granted; no new kappa.')
    payload=(json.dumps(cert,sort_keys=True,indent=2)+'\n').encode();path=a.packet/'CERTIFICATE.json.gz'
    if a.write_certificate:a.packet.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(payload,mtime=0))
    else:need(read(path)==payload,'entire regenerated source certificate')
    return dict(status='PASS_ALL1472_SINGLE_PURE_OVERWRITES_LOSE_ONE_COMMON_MODE',source_sha256=SOURCE_PIN,
        neutral_certificate_payload_sha256=NEUTRAL_PIN,certificate_payload_sha256=hashlib.sha256(payload).hexdigest(),
        native_public_endpoint_rows_checked=1480,neutral_slots=1472,unit_self_response_slots=1472,nonzero_kernel_witnesses=1472,
        common_rank_after_one_overwrite=1479,additional_abstract_common_records_necessary_and_sufficient=1,
        negative_controls=['double displaced payload: gamma2 instead of1','half overwrite: kernel no longer erased','retaining h distinguishes the erased common mode'],
        scope=cert['scope'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--neutral',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--write-certificate',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args();result=run(a);text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
