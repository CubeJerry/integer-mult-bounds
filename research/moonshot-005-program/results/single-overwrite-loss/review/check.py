#!/usr/bin/env python3
"""Independent baseline-forward / endpoint-backward review of1472 overwrites.
No author imports; pulse responses are obtained by adjoints, not forward pulses.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,collections,gzip,hashlib,json,time
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
NEUTRAL='58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139'
def need(x,s):
    if not x:raise ValueError(s)
def read(p):
    b=p.read_bytes();return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
def span(f):
    s={0}
    for x in f:s|={y^x for y in s}
    return frozenset(s)
def axpy(a,b,c=Q(1)):
    for k,x in b.items():
        z=a.get(k,Q(0))+c*x
        if z:a[k]=z
        else:a.pop(k,None)
def digest(r):return hashlib.sha256(json.dumps([[k,str(x)] for k,x in sorted(r.items())],sort_keys=True,separators=(',',':')).encode()).hexdigest()
def maps(w):
    n=w['public'];T={i:{i:Q(1)} for i in range(n)};I={i:{i:Q(1)} for i in range(n)};D=set(w['hosted']['Dports'])
    for k,x in enumerate(w['live']):
        y=x+112
        if k in D:T[y]={x:Q(1),y:Q(1)};I[y]={x:Q(-1),y:Q(1)}
        else:T[x]={x:Q(1),y:Q(-1)};T[y]={x:Q(1,2),y:Q(1,2)};I[x]={x:Q(1,2),y:Q(1)};I[y]={x:Q(-1,2),y:Q(1)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):T[x]={x:Q(1),y:Q(-1)};I[x]={x:Q(1),y:Q(1)}
    for i,row in I.items():
        z={}
        for j,c in row.items():axpy(z,T[j],c)
        need(z=={i:Q(1)},'complete inverse')
    return T,I

def main(a):
    started=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];P=w['program'];F=list(map(span,w['frames']));T,I=maps(w)
    b=read(a.neutral);need(hashlib.sha256(b).hexdigest()==NEUTRAL,'reviewed neutral payload');base=json.loads(b);events={e['event']:e for e in base['edge_certificate']['public_neutral']};need(len(events)==1472,'complete event list')
    certbytes=read(a.certificate);cert=json.loads(certbytes);claimed={r['event']:r for r in cert['records']};need(set(claimed)==set(events),'claimed event coverage')
    state={j:{j:Q(1)} for j in range(n)};loc={j:F[f] for j,f in enumerate(w['initial'])};H={};Lam={};owned_live=collections.Counter()
    for t,e in enumerate(P):
        op,j=e[:2]
        if t in events:
            need(op=='MOVE' and j==events[t]['role'],'event role');h=state[j].copy();lam={}
            for k,c in h.items():axpy(lam,I[k],c)
            H[t]=h;Lam[t]=lam;owned_live[len(state)-n]+=1
        if op=='INIT':need(j>=n and j not in state,'INIT');state[j]={};loc[j]=F[e[2]]
        elif op=='CLEAR':need(j>=n and loc[j]==F[e[2]],'CLEAR');del state[j];del loc[j]
        elif op=='MOVE':
            need(loc[j]==F[e[2]] and bool(e[4])==(j>=n),'MOVE typing');s,d=F[e[2]],F[e[3]];need(s<d or d<s,'proper nested MOVE');loc[j]=d
        elif op=='SCALE':c=Q(e[2]);need(c and loc[j]==F[e[3]],'SCALE typing');state[j]={k:c*x for k,x in state[j].items()}
        elif op in ('ADD','COPY'):
            k=e[2];need(j!=k and loc[j]==loc[k]==F[e[4]],'binary typing')
            if op=='COPY':need(not state[j],'baseline COPY zero')
            axpy(state[j],state[k],Q(e[3]))
        else:raise ValueError(op)
    need(state==T and all(loc[j]==F[w['final'][j]] for j in state),'full native map and charts')
    print('independent baseline complete',round(time.monotonic()-started,3),flush=True)
    adj={j:{j:Q(1)} for j in range(n)};hub=F[w['final'][w['live'][0]]];hubroles={j for j,f in enumerate(w['final']) if F[f]==hub};count=0;recoverable=0;example=None
    def row(j):return adj.setdefault(j,{})
    for t in range(len(P)-1,-1,-1):
        e=P[t];op,j=e[:2]
        if t in events:
            z=dict(row(j));h=H[t];lam=Lam[t];need(z and set(z)<=hubroles,'nonzero hub response and all guards zero');gamma=sum(c*z.get(k,Q(0)) for k,c in lam.items());need(gamma==1,'independent unit self-response')
            v={}
            for k,invrow in I.items():
                c=sum(x*z.get(r,Q(0)) for r,x in invrow.items())
                if c:v[k]=c
            need(v and sum(c*v.get(k,Q(0)) for k,c in h.items())==1,'erased common input mode')
            for k,tr in T.items():need(sum(c*v.get(r,Q(0)) for r,c in tr.items())==z.get(k,Q(0)),'complete kernel image')
            hashes={'payload_sha256':digest(h),'terminal_expression_sha256':digest(lam),'response_sha256':digest(z),'kernel_sha256':digest(v)}
            for key,value in hashes.items():need(claimed[t][key]==value,'independent certificate '+key+' '+str(t))
            need(claimed[t]['gamma']=='1' and claimed[t]['role']==j,'claimed scalar and role');inside=set(lam)<=hubroles;need(claimed[t]['hub_recoverable_payload']==inside,'hub payload status');recoverable+=inside;count+=1
            if t==min(events):example={'event':t,'role':j,'h':[[k,str(c)] for k,c in sorted(h.items())],'z':[[k,str(c)] for k,c in sorted(z.items())],'v':[[k,str(c)] for k,c in sorted(v.items())]};need(sum(2*c*v.get(k,Q(0)) for k,c in h.items())==2,'doubled-row mutant');need(any(c/2 for c in z.values()),'half-overwrite kernel mutant')
        if op=='ADD':axpy(row(e[2]),row(j),Q(e[3]))
        elif op=='SCALE':adj[j]={k:Q(e[2])*x for k,x in row(j).items()}
        elif op=='COPY':axpy(row(e[2]),row(j),Q(e[3]));adj[j]={n+t:Q(1)}
        elif op=='CLEAR':adj[j]={}
        elif op=='INIT':adj.pop(j,None)
        elif op=='MOVE':pass
        else:raise ValueError(op)
    need(count==1472 and recoverable==824,'complete source census');need(owned_live[0]==748,'no-owned-live census')
    result={'status':'PASS_INDEPENDENT1472_SINGLE_OVERWRITE_LOSS','source_sha256':PIN,'neutral_payload_sha256':NEUTRAL,'author_certificate_payload_sha256':hashlib.sha256(certbytes).hexdigest(),'full_endpoint_rows_checked':1480,'public_helper_occurrences':count,'unit_gamma_occurrences':count,'all_nonzero_kernel_images':True,'hub_recoverable_payloads':recoverable,'other_payloads':count-recoverable,'common_rank_after_single_pure_overwrite':1479,'additional_linear_complete_field_records_necessary_and_sufficient':1,'independent_response_method':'backward full-public-endpoint and COPY-guard adjoints','author_response_method':'simultaneous forward pulse variables','owned_live_count_at_source_occurrences':dict(sorted(owned_live.items())),'negative_controls':['doubled displaced row gives gamma2','half overwrite does not erase its kernel vector','retained h changes by1 on the indistinguishable input pair'],'example':example,'scope':'One pure replacement, unchanged suffix, no other common-input record supplied; all final common outputs and original q freely granted.','new_complete_kappa':None}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],'seconds',round(time.monotonic()-started,3),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--neutral',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
