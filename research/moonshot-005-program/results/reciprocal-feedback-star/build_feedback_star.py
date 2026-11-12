#!/usr/bin/env python3
"""Source-pinned reciprocal feedback star; finite word, not a supplier."""
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT_PIN = 'bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17'
PARENT_PAYLOAD_PIN = 'bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a'
FRAME = [5,56,65,69,77,96,100,103]
def need(q,m):
    if not q: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def root(v):
    S=[i for i in range(9) if v>>i&1]
    if len(S)==3: return [2*int(k in S) for k in range(8)] if 8 in S else [1 if k in S else -1 for k in range(8)]
    need(len(S)==7,'root weights');i,j=[k for k in range(9) if k not in S]
    return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def add(a,b,c=F(1)):
    r=a.copy()
    for k,v in b.items():
        z=r.get(k,F(0))+c*v
        if z:r[k]=z
        else:r.pop(k,None)
    return r
def rank(A):
    if not A:return 0
    M=[list(map(F,r)) for r in A];p=0
    for j in range(len(M[0])):
        k=next((k for k in range(p,len(M)) if M[k][j]),None)
        if k is None:continue
        M[p],M[k]=M[k],M[p];c=M[p][j];M[p]=[x/c for x in M[p]]
        for k in range(p+1,len(M)):
            if M[k][j]:c=M[k][j];M[k]=[x-c*y for x,y in zip(M[k],M[p])]
        p+=1
        if p==len(M):break
    return p

def main(a):
    recon=a.repo/'research/moonshot-005-program/results/cohort-reconstruction'
    sys.path.insert(0,str(recon))
    spec=importlib.util.spec_from_file_location('retained_cohort_build',recon/'build.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();pb=(a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz').read_bytes()
    need(sha(sb)==SOURCE_PIN and sha(pb)==PARENT_PIN and sha(gzip.decompress(pb))==PARENT_PAYLOAD_PIN,'exact immutable inputs')
    s=json.loads(gzip.decompress(sb));p=json.loads(gzip.decompress(pb));raw={int(x):r for x,r in p['private_role_map'].items()}
    hosted={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    roots={x:root(s['frames'][s['initial'][x]][0]) for x in s['live']}
    gram=lambda x,y:F(sum(i*j for i,j in zip(roots[x],roots[y])),8)
    need(all(gram(b,c)==(b==c) for b in FRAME for c in FRAME),'exact orthogonal frame')
    need(a.receiver in hosted and a.receiver not in FRAME and all(b in hosted for b in FRAME),'independent hosted banks; coupled ports excluded')
    t=a.receiver;y=t+112;d=hosted[t][1];facet=s['final'][y]
    need(s['initial'][d]==3 and s['final'][d]==facet,'authentic receiver Y2 shares endpoint facet')
    contacts={b:gram(b,t) for b in FRAME if gram(b,t)}
    need(len(contacts)==4 and all(abs(c)==F(1,2) for c in contacts.values()) and sum(c*c for c in contacts.values())==1,'four normalized frame contacts')
    need(str(y) not in p['corrections'],'avoid already modified forward receiver')
    roles=list(contacts)+[hosted[b][0] for b in contacts]+[d]
    oldmoves={}
    for r in roles:
        moves=[i for i,e in enumerate(p['program']) if e[0]=='MOVE' and e[1]==raw[r]]
        need(len(moves)==1,'one authentic direct source route')
        i=moves[0];need(p['program'][i]==['MOVE',raw[r],s['initial'][r],s['final'][r],False],'direct original ascent')
        need(400<=i<p['marks']['common_starts'],'unspent prefix route')
        oldmoves[r]=i
    ymoves=[i for i,e in enumerate(p['program']) if e[0]=='MOVE' and e[1]==raw[y] and e[3]==facet]
    need(len(ymoves)==1,'first Y actual facet arrival');arrival=ymoves[0]
    collector=1880+p['owned_fields'];ops=[];lineage=[];mapping={};boundary={};events={};skip=set(oldmoves.values())
    def emit(e,parent=None):
        i=len(ops);ops.append(e);lineage.append(parent);return i
    def move(r,x,z):
        mapping.setdefault(oldmoves[r],len(ops));return emit(['MOVE',raw[r],x,z,False],oldmoves[r])
    for i,e in enumerate(p['program']):
        if i==400:
            events['begin']=len(ops);emit(['INIT',collector,facet]);events['receiver_Y2_move']=move(d,3,facet)
            events['forward_reads']=[];events['reverse_reads']=[]
            for b,c in contacts.items():
                move(b,s['initial'][b],facet);j=emit(['ADD',collector,raw[b],str(-c),facet]);events['forward_reads'].append(j);move(b,facet,127)
            for b,c in contacts.items():
                r=hosted[b][0];move(r,s['initial'][r],facet);j=emit(['ADD',raw[r],raw[d],str(c),facet]);events['reverse_reads'].append(j);move(r,facet,127)
            events['end']=len(ops)
        boundary[i]=len(ops)
        if i in skip:continue
        mapping[i]=len(ops);emit(copy.deepcopy(e),i)
        if i==arrival:
            events['collector_consumed']=emit(['ADD',raw[y],collector,'1',facet]);emit(['CLEAR',collector,facet])
    need(len(mapping)==len(p['program']),'every parent instruction or route accounted')
    w=copy.deepcopy(p);w['parent_paired_collection_provenance']=w.pop('paired_collection')
    w.update(schema='moonshot-S009-four-contact-feedback-star-v1',program=ops,owned_fields=p['owned_fields']+1,parent_event_of_output=lineage,parent_word_sha256=sha(pb),marks={k:boundary[v] for k,v in p['marks'].items()},native_event_to_physical=[mapping[v] for v in p['native_event_to_physical']])
    w['marks']['feedback_star_collector_consumed']=events['collector_consumed']+1
    w['corrections'][str(y)]=[[b,str(-c)] for b,c in contacts.items()]
    for b,c in contacts.items():
        r=hosted[b][0];need(str(r) not in w['paired_reverse_corrections'],'selected frame reverse carrier unused')
        w['paired_reverse_corrections'][str(r)]=[[d,str(c)]]
    w['feedback_star']={'frame':FRAME,'receiver_firstX':t,'receiver_firstY':y,'receiver_hostedY2':d,'facet':facet,'contact_coefficients':{str(b):str(c) for b,c in contacts.items()},'collector':collector,'events':events,'replaced_routes':{str(r):i for r,i in oldmoves.items()},'scope':'One compatible feedback star on the committed paired word. No completed new forward or reverse pair.'}
    before,loc0=base.interpret_prefix(s,p);after,loc1=base.interpret_prefix(s,w)
    need(loc0==loc1 and set(before)==set(after),'same common-entry coordinates/charts')
    q={r:{raw[r]:F(1),r:F(-1)} for r in raw};changes={raw[y]:{}}
    for b,c in contacts.items():
        changes[raw[y]]=add(changes[raw[y]],q[b],-c)
        changes[raw[hosted[b][0]]]=add({},q[d],c)
    for r,row in before.items():need(after[r]==add(row,changes.get(r,{})),'all1880 exact prefix columns')
    need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'literal common suffix')
    tail=w['program'][w['marks']['common_starts']:]
    for r in [y]+[hosted[b][0] for b in contacts]:
        uses=[e for e in tail if e[1]==raw[r] or e[0] in ('ADD','COPY') and e[2]==raw[r]]
        need(uses==[['ADD',raw[r],r,'1',s['final'][r]]],'changed value has no later feedback')
    for b,c in contacts.items():need(add(after[raw[hosted[b][0]]],after[raw[d]],-c)==q[hosted[b][0]],'explicit hosted inverse')
    need(add(after[raw[y]],changes[raw[y]],-1)==before[raw[y]],'explicit forward inverse relative to parent')
    bill=base.typed(s,w);oldbill=base.typed(s,p);need(bill.pop('final_locations')==oldbill.pop('final_locations'),'final public charts')
    H=list(hosted);X=[hosted[h][0] for h in H];Y=[hosted[h][1] for h in H];idx={r:i for i,r in enumerate(Y)}
    RR=[[F(0) for _ in H] for _ in H]
    for i,x in enumerate(X):
        declared={int(z):F(c) for z,c in w['paired_reverse_corrections'].get(str(x),[])}
        for j,z in enumerate(Y):RR[i][j]=after[raw[x]].get(raw[z],F(0))
        need({z:RR[i][j] for j,z in enumerate(Y) if RR[i][j]}==declared,'actual source rows equal declared reverse coefficients')
        expected=q[x]
        for j,z in enumerate(Y):expected=add(expected,q[z],RR[i][j])
        need(after[raw[x]]==expected,'all1880 input coefficients of actual hosted reverse row')
    residual=[[F(i==j)+RR[i][j] for j in range(96)] for i in range(96)]
    need(rank(residual)==95,'exact reverse residual rank95')
    kernel={h:F(0) for h in H};kernel[t]=1
    for b,c in contacts.items():kernel[b]=-c
    for h in H:
        if h not in FRAME and h!=t:kernel[h]=sum(gram(h,b)*c for b,c in contacts.items())
    kv=[kernel[h] for h in H]
    need(all(sum(x*y for x,y in zip(row,kv))==0 for row in residual),'explicit exact right kernel')
    need(1-sum(c*c for c in contacts.values())==0,'one-star Schur zero')
    missing=next(iter(contacts));need(1-sum(c*c for b,c in contacts.items() if b!=missing)==F(1,4),'missing-contact Schur negative control')
    other=next(z for z in H if z!=t and z not in FRAME and gram(t,z));g=gram(t,other)
    need(g in (F(-1,2),F(1,2)) and -g*g==F(-1,4),'two-star nonorthogonal Schur determinant')
    invoice=json.loads((a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_text())
    R=Counter(bill['raw_histogram']);Rold=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
    T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
    for r in R.keys()|Rold.keys():P[r]+=18*(R[r]-Rold[r])
    P[9]+=18*8;need(all(n>=0 for n in P.values()),'nonnegative whole caller');lo,hi=base.interval({r:T[r]-P[r] for r in T.keys()|P.keys()})
    a.output.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();wb=gzip.compress(payload,mtime=0,compresslevel=9);(a.output/'WORD.json.gz').write_bytes(wb)
    result={'status':'PASS_FINITE_FEEDBACK_STAR_RANK95','source_sha256':SOURCE_PIN,'parent_word_sha256':PARENT_PIN,'word_sha256':sha(wb),'word_payload_sha256':sha(payload),'receiver_firstX':t,'frame':FRAME,'contacts':{str(b):str(c) for b,c in contacts.items()},'independent_input_coordinates':1880,'reverse_residual_rank':95,'explicit_reverse_kernel':{str(h):str(c) for h,c in kernel.items() if c},'forward_residual_coefficients':4597,'newly_completed_pairs':0,'coupled_ports_changed':0,'reverse_coefficients':sum(len(v) for v in w['paired_reverse_corrections'].values()),'bill':bill,'increment_over_paired_parent':{k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()},'conditional_caller':{'P_partial':dict(sorted(P.items())),'T4':dict(sorted(T.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'remaining_moment_per_native_decimal':float(lo/18),'all_eight_rank9_packets_retained':True},'negative_controls':{'missing_basis_contact':missing,'missing_contact_Schur':'1/4','second_nonorthogonal_receiver':other,'two_star_Schur_determinant':'-1/4'},'scope':'Source-compatible partial finite word. Reverse rank95 is an algebraic residual dimension; no completed new pair, full supplier or new kappa.'}
    (a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','contacts','reverse_residual_rank','forward_residual_coefficients','bill','increment_over_paired_parent','conditional_caller']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--receiver',type=int,default=0);main(p.parse_args())
