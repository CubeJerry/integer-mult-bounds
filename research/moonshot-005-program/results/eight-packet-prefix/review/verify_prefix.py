"""Independent typed 1880-input review of the S006 packet prefix.

Reads the submitted word as a certificate; imports no author verifier.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
    if not x: raise ValueError(m)
def plus(dst,src,c=F(1)):
    for k,v in list(src.items()):
        t=dst.get(k,F(0))+c*v
        if t: dst[k]=t
        else: dst.pop(k,None)
def span(frame):
    s={0}
    for b in frame: s.update(x^b for x in tuple(s))
    return s
def root(v):
    S=[i for i in range(9) if v>>i&1]
    if len(S)==3:
        return [2*int(i in S) if 8 in S else (1 if i in S else -1) for i in range(8)]
    need(len(S)==7,'port weight')
    i,j=[i for i in range(9) if i not in S]
    return [2*int(k==i)-2*int(k==j) if j<8 else (1 if k==i else -1) for k in range(8)]
def run(w,p):
    M=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    q={j:1480+i for i,j in enumerate(M)}
    need(p['public']==1880 and p['owned_fields']==52,'declared domain')
    need(p['difference_role_map']=={str(k):v for k,v in q.items()},'difference-role mapping')
    need(p['initial']==w['initial']+[w['initial'][j] for j in M],'initial physical charts')
    need(p['source_sha256']==PIN and p['ports']==w['ports'],'source binding')
    A=[root(v) for v in w['ports']]
    need(p['roots']==A,'independently reconstructed dyadic roots')
    G=[[sum(a*b for a,b in zip(x,y)) for y in A] for x in A]
    for i in range(104):
        need(G[i][i]==8,'root norm')
        for j in range(104):
            if i!=j: need(G[i][j]==0 if (w['ports'][i]&w['ports'][j]).bit_count()%2 else abs(G[i][j])==4,'Gram parity')
    C=set(w['hosted']['Dports'])
    c=[F(1) if i in C else F(1,2) for i in range(104)]
    need({int(k):F(v) for k,v in p['receiver_weights'].items()}==dict(zip(w['live'],c)),'receiver weights')
    R={j:{j:F(1)} for j in range(1880)};L=dict(enumerate(p['initial']));S=list(map(span,w['frames']))
    counters=Counter();moves=Counter();peak=active=0
    funded={x['physical_event']:x for x in p['reservations']}
    need(len(funded)==len(p['reservations'])==890,'funded reservation uniqueness')
    source_events=[];last_by_role={};new_moves=[]
    need(len(p['marks'])==len(p['program']),'marks length')
    for t,e in enumerate(p['program']):
        op,j=e[:2];counters[op]+=1
        need(p['marks'][t]['physical_event']==t,'physical event tag')
        if op=='INIT':
            need(1880<=j<1932 and j not in L and 0<=e[2]<len(S),'INIT ownership/chart')
            L[j]=e[2];R[j]={};active+=1;peak=max(peak,active)
        elif op=='CLEAR':
            need(j>=1880 and L[j]==e[2],'CLEAR ownership/chart')
            del L[j];del R[j];active-=1
        elif op=='ADD':
            s=e[2];need(j in L and s in L and L[j]==L[s]==e[4],'ADD exact cochart')
            plus(R[j],R[s],F(e[3]))
        elif op=='SCALE':
            need(j in L and L[j]==e[3] and F(e[2]),'SCALE typed nonzero')
            R[j]={k:F(e[2])*v for k,v in R[j].items()}
        elif op=='MOVE':
            need(j in L and L[j]==e[2] and e[4]==(j>=1880),'MOVE source/ownership')
            need(S[e[2]]<=S[e[3]] or S[e[3]]<=S[e[2]],'MOVE nested geometry')
            r=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));moves[r]+=1;L[j]=e[3]
            if t in funded:
                z=funded[t];se=z['source_event'];role=z['logical_role']
                need(e==['MOVE',q[role],z['source'],z['target'],False],'funded physical MOVE')
                need(w['program'][se]==['MOVE',role,z['source'],z['target'],False],'funded source MOVE')
                need(se>last_by_role.get(role,-1),'per-role funded order');last_by_role[role]=se
                source_events.append(se)
            else:
                need(e[2:]==[127,3,True] and r==9,'only new packet MOVEs')
                new_moves.append(t)
        else: raise ValueError('unsupported opcode '+op)
    need(active==0 and peak==1 and set(R)==set(range(1880)),'owned lifetime completion')
    need(len(source_events)==len(set(source_events))==890 and len(new_moves)==8,'unique source debits')
    need(counters==Counter({'ADD':1440,'MOVE':898,'SCALE':8,'INIT':8,'CLEAR':8}),'operation census')
    E={j:{j:F(1)} for j in range(1480)}
    def raw(j): return {q[j]:F(1),j:F(-1)}
    for j in M: E[q[j]]=raw(j)
    for i,x in enumerate(w['live']):
        y=x+112;r={};plus(r,raw(y),c[i])
        for j,z in enumerate(w['live']):
            if G[i][j]: plus(r,raw(z),c[i]*F(G[i][j],8))
        E[q[y]]=r
    need(R==E,'all1880 independent-input endpoint rows')
    for j in range(1480): need(L[j]==w['initial'][j],'common chart unchanged')
    for x in w['live']: need(L[q[x]]==127,'all raw donors at hub')
    for x in w['live']: need(L[q[x+112]]==w['final'][x+112],'all forward receivers at required chart')
    for j in set(M)-set(w['live'])-{x+112 for x in w['live']}:
        need(L[q[j]]==w['initial'][j],'hosted raw chart unchanged')
    # Explicit left inverse, not a sampled full-rank check.
    for i,x in enumerate(w['live']):
        y=x+112;recovered={};plus(recovered,R[q[y]],1/c[i])
        for j,z in enumerate(w['live']):
            if G[i][j]: plus(recovered,R[q[z]],-F(G[i][j],8))
        need(recovered==raw(y),'invertible raw receiver prefix')
    want_funded={t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in set(w['live'])|{x+112 for x in w['live']}}
    need(set(source_events)==want_funded,'all and only forward raw routes debited')
    residual_terms=sum(i!=j and G[i][j]!=0 for i in range(104) for j in range(104))
    return {'operation_counts':dict(sorted(counters.items())),'MOVE_histogram':dict(sorted(moves.items())),'funded_raw_MOVEs':890,'new_rank9_MOVEs':8,'unspent_other_main_MOVEs':1710-890,'owned_lifetimes':8,'peak_live_owned':peak,'public_independent_rows_checked':1880,'common_rows_and_charts_unchanged':1480,'raw_input_conversion_ADDs':400,'packet_formation_ADDs':sum(v!=0 for a in A for v in a),'packet_injection_ADDs':sum(v!=0 for a in A for v in a),'residual_offdiagonal_terms':residual_terms,'inverse_verified_for_all_forward_raw_receivers':104,'final_location_map':L}
def main(a):
    sb=a.source.read_bytes();pb=a.prefix.read_bytes();need(hashlib.sha256(sb).hexdigest()==PIN,'compressed source pin')
    w=json.loads(gzip.decompress(sb));p=json.loads(gzip.decompress(pb));result=run(w,p);negative=[]
    from copy import deepcopy
    def reject(z,label):
        try: run(w,z)
        except ValueError: negative.append(label);return
        raise ValueError('negative control accepted: '+label)
    z=deepcopy(p);idx=next(i for i,e in enumerate(z['program']) if e[0]=='ADD' and e[2]>=1880);z['program'][idx][3]=str(-F(z['program'][idx][3]));reject(z,'wrong packet-injection sign')
    z=deepcopy(p);idx=next(i for i,e in enumerate(z['program']) if e[0]=='SCALE');z['program'][idx][2]='1';reject(z,'omitted coupled half scaling')
    z=deepcopy(p);z['reservations'][1]['source_event']=z['reservations'][0]['source_event'];reject(z,'reused funded source reservation')
    z=deepcopy(p);idx=next(i for i,e in enumerate(z['program']) if e[0]=='MOVE' and e[4]);z['program'][idx][4]=False;reject(z,'packet MOVE mislabeled public')
    result.update(status='PASS_INDEPENDENT_TYPED_1880_INPUT_PACKET_PREFIX_REVIEW',source_sha256=PIN,prefix_compressed_sha256=hashlib.sha256(pb).hexdigest(),prefix_payload_sha256=hashlib.sha256(gzip.decompress(pb)).hexdigest(),negative_controls=negative,scope='A reversible physical prefix with unpaid residual and hosted completion obligations. The820 unspent reservations are not extra free calls. No full endpoint supplier or new kappa.')
    result.pop('final_location_map');a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print('residual terms',result['residual_offdiagonal_terms'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
