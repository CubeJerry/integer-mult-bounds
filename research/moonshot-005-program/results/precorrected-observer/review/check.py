#!/usr/bin/env python3
"""Independent typed1880-input replay. No author or predecessor imports."""
import argparse,collections,gzip,hashlib,json,time
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
    if not x:raise ValueError(s)
def read(p):
    b=p.read_bytes();return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
def span(f):
    s={0}
    for x in f:s|={y^x for y in s}
    return frozenset(s)
def axpy(a,b,c=Q(1)):
    for k,v in tuple(b.items()):
        x=a.get(k,Q(0))+c*v
        if x:a[k]=x
        else:a.pop(k,None)
def common(w):
    t={i:{i:Q(1)} for i in range(1480)};hosted=set(w['hosted']['Dports'])
    for k,x in enumerate(w['live']):
        y=x+112
        if k in hosted:t[y]={x:Q(1),y:Q(1)}
        else:t[x]={x:Q(1),y:Q(-1)};t[y]={x:Q(1,2),y:Q(1,2)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):t[x]={x:Q(1),y:Q(-1)}
    return t
def main(a):
    started=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));frames=list(map(span,w['frames']));expected=common(w)
    M=sorted(set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));need(len(M)==400,'raw source ports');qm={j:1480+i for i,j in enumerate(M)};results=[]
    for route in ('source','hub'):
        wp=a.packet/('WORD-'+route.upper()+'.json.gz');payload=read(wp);word=json.loads(payload);receipt=json.loads((a.packet/('RESULT-'+route.upper()+'.json')).read_text())
        need(word['source_sha256']==PIN and word['packet_route']==route,'word pin/route');need(word['public']==1880 and word['owned_fields']==53,'dimensions')
        need(word['initial']==w['initial']+[w['initial'][j] for j in M],'initial charts');need(word['raw_role_map']=={str(j):v for j,v in qm.items()},'independent raw map')
        need(hashlib.sha256(payload).hexdigest()==receipt['word_payload_sha256'],'payload hash')
        ops=word['program'];reserved={r['physical_event']:r for r in word['raw_reservations']};need(len(reserved)==7 and len({r['source_event'] for r in reserved.values()})==7,'unique reservations')
        for physical,r in reserved.items():
            e=w['program'][r['source_event']];need(e[0]=='MOVE' and e[1]==r['main_role'] and e[1] in (77,189),'funded source role');need(ops[physical]==['MOVE',qm[e[1]],e[2],e[3],False],'funded physical move')
        need({r['source_event'] for r in reserved.values()}=={t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in (77,189)},'complete once-only raw itineraries')
        native_moves=[];paid=[]
        for t,e in enumerate(ops):
            if e[0]!='MOVE' or t in reserved:continue
            if e[1]==1932:paid.append((t,e));continue
            f=list(e);f[1]-=400 if f[1]>=1880 else 0;native_moves.append(f)
        need(native_moves==[e for e in w['program'] if e[0]=='MOVE'],'unchanged native MOVE invoice');need(len(paid)==1,'one paid move');s=71 if route=='source' else 127
        need(paid[0][1]==['MOVE',1932,s,3,True],'paid packet route');need(frames[3]==frozenset({0}),'empty target');paid_rank=(len(frames[s])//len(frames[3])).bit_length()-1;need(paid_rank==(1 if route=='source' else 9),'paid rank')
        state={j:{j:Q(1)} for j in range(1880)};loc={j:frames[f] for j,f in enumerate(word['initial'])};counts=collections.Counter();peak=0;lifetimes=0;nonzero_clear=0;checkpoint={};marks={v:k for k,v in word['marks'].items()};q={qm[77]:Q(1),77:Q(-1)}
        for t,e in enumerate(ops):
            if t in marks:
                name=marks[t]
                if name=='initial_history_start':
                    need(state[qm[77]]==q,'knownq before snapshots')
                    for j,c in word['precorrection']:
                        target={j:Q(1)};axpy(target,q,Q(c));need(state[j]==target,'initial precompensation row')
                    checkpoint['corrected_initial_fields']=len(word['precorrection'])
                elif name=='native_start':need(loc[qm[189]]==frames[198],'receiver hoisted before common word');checkpoint['early_receiver_hoist']=True
                elif name=='encoder_start':
                    need(state[287]=={77:Q(1)} and state[1931]=={qm[77]:Q(1)},'helper u77 and originalv77 cache');need(loc[287]==loc[1931]==frames[71],'encoder cochart');checkpoint['causal_cache_and_encoder']=True
            op,j=e[:2];counts[op]+=1
            if op=='INIT':need(1880<=j<1933 and j not in state,'owned INIT');state[j]={};loc[j]=frames[e[2]];lifetimes+=1
            elif op=='CLEAR':need(j>=1880 and j in state and loc[j]==frames[e[2]],'owned CLEAR');nonzero_clear+=bool(state[j]);del state[j];del loc[j]
            elif op=='MOVE':
                need(j in state and bool(e[4])==(j>=1880) and loc[j]==frames[e[2]],'MOVE typing');s,d=frames[e[2]],frames[e[3]];need(s<d or d<s,'proper nested MOVE');loc[j]=d
            elif op=='SCALE':c=Q(e[2]);need(j in state and c and loc[j]==frames[e[3]],'SCALE typing');state[j]={k:c*v for k,v in state[j].items()}
            elif op in ('ADD','COPY'):
                k=e[2];need(j!=k and j in state and k in state and loc[j]==loc[k]==frames[e[4]],'cochart access')
                if op=='COPY':need(not state[j],'zero-target COPY guard')
                axpy(state[j],state[k],Q(e[3]))
            else:raise ValueError(op)
            peak=max(peak,len(state)-1880)
        need(set(state)==set(range(1880)),'owned retirement and public retention')
        for j in range(1480):need(state[j]==expected[j] and loc[j]==frames[w['final'][j]],'full common target '+str(j))
        for j,label in qm.items():
            target={label:Q(1)}
            if j==189:target[qm[77]]=Q(1)
            need(state[label]==target,'full raw target '+str(j));need(loc[label]==frames[w['final'][j] if j in (77,189) else w['initial'][j]],'raw target chart '+str(j))
        need(counts==collections.Counter(receipt['bill']['counts']) and peak==receipt['bill']['peak_owned'] and lifetimes==receipt['bill']['owned_lifetimes'],'independent operation invoice')
        pre={j:Q(c) for j,c in word['precorrection']};j=min(pre);missing=expected[j].get(j,Q(0))*pre[j];need(missing,'omitted precompensation endpoint witness')
        reads=[e for e in ops[word['marks']['initial_history_start']:word['marks']['native_start']] if e[0]=='ADD'];early=sum((Q(e[3])*pre.get(e[2],Q(0)) for e in reads),Q(0));need(early==1,'premature snapshot defect')
        need(max(r['physical_event'] for r in reserved.values() if r['main_role']==189)<word['marks']['native_start'],'funded receiver hoist')
        results.append({'packet_route':route,'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'word_compressed_sha256':hashlib.sha256(wp.read_bytes()).hexdigest(),'common_rows_restored':1480,'raw_shears_completed':1,'raw_identity_outputs':399,'other_raw_fields_retained_initially':398,'new_paid_call_rank':paid_rank,'funded_raw_moves':7,'native_moves':6310,'operation_counts':dict(counts),'owned_lifetimes':lifetimes,'peak_owned':peak,'nonzero_owned_clears':nonzero_clear,'checkpoints':checkpoint,'negative_controls':{'omitted_correction_role':j,'omitted_correction_endpoint_coefficient':str(missing),'premature_snapshot_raw_error_coefficient':str(-early)}})
        print('independent',route,'PASS',round(time.monotonic()-started,3),flush=True)
    result={'status':'PASS_INDEPENDENT_1880_INPUT_PRECORRECTED77_WORDS','source_sha256':PIN,'method':'standalone exact1880-variable typed replay without author or predecessor imports','variants':results,'all_volumes':'literal rational row identities tensor with identity','scope':'One completed raw second-copy shear; all1480 common endpoints restored;398 other raw ports retained initially. No complete400-port lift.','assumptions':'Owned erasure, compiler and precision assumptions remain. The one-rank1 single-pair version offers no price saving over direct delivery.','new_complete_kappa':None}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],round(time.monotonic()-started,3),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
