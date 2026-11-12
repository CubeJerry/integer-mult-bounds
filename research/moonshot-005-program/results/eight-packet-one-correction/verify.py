#!/usr/bin/env python3
"""Exact1880-input E8 prefix with one physical weighted residual correction.

The discovery and decoder belong to the programme budget/foreign-control
worker. This independently reconstructs their source rows and lowers a literal
physical word, using the programme's earlier typed-word conventions.
OpenAI assistance disclosed. No complete shared native or new kappa.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip, hashlib, json
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT_PIN = '546ca7bf0ab8a958c7269d94143f3ec315e12e96eddbebed129b435ac59239e6'
EVENT, HELPER, DONOR, RECEIVER, HUB = 31460, 1193, 47, 172, 127

def need(ok, message):
    if not ok: raise ValueError(message)

def add(a, b, c=F(1)):
    out = a.copy()
    for i, value in b.items():
        value = out.get(i, F(0)) + c*value
        if value: out[i] = value
        else: out.pop(i, None)
    return out

def scale(row, c): return {i:c*v for i,v in row.items() if c*v}
def ser(row): return [[i,str(v)] for i,v in sorted(row.items())]
def space(frame):
    out = {0}
    for v in frame: out |= {x^v for x in tuple(out)}
    return frozenset(out)

def declared_endpoints(w):
    T = {i:{i:F(1)} for i in range(1480)}
    inverse = {i:{i:F(1)} for i in range(1480)}
    for k,x in enumerate(w['live']):
        y = x+112
        if k in w['hosted']['Dports']:
            T[y]={y:F(1),x:F(1)}; inverse[y]={y:F(1),x:F(-1)}
        else:
            T[x]={x:F(1),y:F(-1)};T[y]={x:F(1,2),y:F(1,2)}
            inverse[x]={x:F(1,2),y:F(1)};inverse[y]={y:F(1),x:F(-1,2)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):
        T[x]={x:F(1),y:F(-1)};inverse[x]={x:F(1),y:F(1)}
    for i,row in inverse.items():
        check={}
        for j,c in row.items():check=add(check,T[j],c)
        need(check=={i:F(1)},'explicit complete native inverse')
    return T

def source_certificate(w, cert):
    channel=cert['candidate_channels'][0]
    need((channel['donor'],channel['receiver'],channel['gain'])==(DONOR,RECEIVER,'-1'),'selected discovered channel')
    dec=channel['best_relation'];obs=defaultdict(list)
    for x in dec['arrival_terms']:obs[x['after_event']].append(x)
    baseline={i:{i:F(1)} for i in range(1480)};pulse={i:F(0) for i in range(1480)}
    locations=dict(enumerate(w['initial']));decoded={};gain=F(0);guards=[];snapshots={}
    for x in dec['initial_terms']:
        need(w['initial'][x['role']]==x['chart']==3,'actual initial cochart term')
        decoded=add(decoded,baseline[x['role']],F(x['coefficient']))
    for t,e in enumerate(w['program']):
        op,r=e[:2]
        if t==EVENT:
            need(e==['MOVE',HELPER,43,502,False],'actual injection boundary')
            pulse[r]+=1
        if op=='INIT':baseline[r]={};pulse[r]=F(0);locations[r]=e[2]
        elif op=='CLEAR':baseline.pop(r);pulse.pop(r);locations.pop(r)
        elif op=='MOVE':need(locations[r]==e[2],'source MOVE location');locations[r]=e[3]
        elif op=='SCALE':baseline[r]=scale(baseline[r],F(e[2]));pulse[r]*=F(e[2])
        elif op in ('ADD','COPY'):
            if op=='COPY':
                need(not baseline[r] and not pulse[r],'actual baseline and pulse COPY guard')
                guards.append({'event':t,'response':str(pulse[r])})
            baseline[r]=add(baseline[r],baseline[e[2]],F(e[3]));pulse[r]+=F(e[3])*pulse[e[2]]
        else:raise ValueError('source opcode')
        for x in obs[t]:
            need(locations[x['role']]==x['chart']==524,'actual arrival cochart')
            decoded=add(decoded,baseline[x['role']],F(x['coefficient']))
            gain+=F(x['coefficient'])*pulse[x['role']]
            snapshots[t,x['role']]=baseline[x['role']].copy()
        if t==36812:snapshots[t,1197]=baseline[1197].copy()
    T=declared_endpoints(w);need(baseline==T,'all1480 native endpoints')
    need(not decoded and gain==-1,'complete1480-input zero relation and actual private gain')
    Z={i:c for i,c in pulse.items() if c}
    need(Z=={int(i):F(c) for i,c in cert['full_endpoint_response'].items()},'complete endpoint response identity')
    need(len(Z)==33 and all(w['final'][i]==HUB for i in Z),'exact33 hub-only common disturbances')
    need(len(dec['initial_terms'])==107 and len(dec['arrival_terms'])==2,'actual decoder count')
    need(snapshots[36812,1197]!=snapshots[36811,1197],'late-read mutant has nonzero baseline error')
    return T,Z,dec,guards,snapshots

PREFIX_PIN='52123f6dbe9488835b4aaa9eeb22cd721a8aab0197f17489fb7393d2b2e2865e'

def root(v):
    bits=[i for i in range(9) if v>>i&1]
    if len(bits)==3:return [2*(i in bits) for i in range(8)] if 8 in bits else [1 if i in bits else -1 for i in range(8)]
    need(len(bits)==7,'root source port weight')
    i,j=[i for i in range(9) if i not in bits]
    return [1 if k==i else -1 for k in range(8)] if j==8 else [2*((k==i)-(k==j)) for k in range(8)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def prefix_targets(w,p,raw):
    xs=sorted(w['live']);need(xs==p['donor_roles'],'prefix donor order')
    ports=[w['frames'][w['initial'][r]][0] for r in xs]
    roots=[root(v) for v in ports];need(ports==p['ports'] and roots==p['roots'],'source-derived prefix root data')
    coupled=set(range(104))-set(w['hosted']['Dports'])
    weights={r:F(1,2) if i in coupled else F(1) for i,r in enumerate(xs)}
    need({str(r):str(c) for r,c in weights.items()}==p['receiver_weights'],'source-derived prefix weights')
    q={r:{rid:F(1),r:F(-1)} for r,rid in raw.items()}
    out={r:q[r].copy() for r in raw};residuals=[]
    for i,x in enumerate(xs):
        out[x+112]=scale(q[x+112],weights[x])
        for j,d in enumerate(xs):
            g=dot(roots[i],roots[j]);c=weights[x]*g/8
            if c:out[x+112]=add(out[x+112],q[d],c)
            if c and d!=x:residuals.append((x+112,d,c))
    i=xs.index(RECEIVER-112);j=xs.index(DONOR);coefficient=weights[xs[i]]*dot(roots[i],roots[j])/8
    need(coefficient==F(1,4),'actual q47 residual at coupled receiver172')
    return out,q,coefficient,residuals

def build(w,p,Z,dec):
    raw={int(r):rid for r,rid in p['difference_role_map'].items()};mains=sorted(raw)
    need(len(raw)==400 and raw=={r:1480+i for i,r in enumerate(mains)},'complete canonical raw bank')
    xs=set(w['live']);ys={x+112 for x in xs};cache=1880+w['owned_fields']+1
    targets,q,a,residuals=prefix_targets(w,p,raw)
    ops=[];reservations=[];marks={};prefix_map={};native_map=[];deferred=[]
    pmarks={x['physical_event']:x['purpose'] for x in p['marks']}
    pres={x['physical_event']:x for x in p['reservations']}
    need(len(pres)==890 and len(pmarks)==len(p['program'])==2362,'pinned prefix sizes')
    def reserve(source_event,role,op,prefix_event=None):
        item=dict(source_event=source_event,physical_event=len(ops),role=role)
        if prefix_event is not None:item['prefix_event']=prefix_event
        reservations.append(item);ops.append(op.copy())
    initial_done=False
    for i,op in enumerate(p['program']):
        if i==400:
            need(all(pmarks[j]=='form_actual_difference' for j in range(400)),'prefix difference boundary')
            marks['cache_acquired']=len(ops)
            ops.extend([['INIT',cache,43],['ADD',cache,raw[DONOR],'1',43]])
        if not initial_done and pmarks[i]=='funded_receiver_route':
            marks['initial_decoder']=len(ops)
            for x in dec['initial_terms']:ops.append(['ADD',raw[RECEIVER],x['role'],str(a*F(x['coefficient'])),3])
            initial_done=True
        if i in pres:
            r=pres[i]
            if r['logical_role']==RECEIVER and r['source_event'] in (40965,42097):
                deferred.append((i,op,r));continue
            prefix_map[str(i)]=len(ops);reserve(r['source_event'],r['logical_role'],op,i)
        else:
            prefix_map[str(i)]=len(ops);ops.append(op.copy())
    need(initial_done and len(deferred)==2,'actual receiver waits at524')
    marks['prefix_scheduled']=len(ops)
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1] in raw and e[1] not in xs|ys:
            reserve(t,e[1],['MOVE',raw[e[1]],e[2],e[3],False])
    marks['common_starts']=len(ops)
    observations=defaultdict(list)
    for x in dec['arrival_terms']:observations[x['after_event']].append(x)
    for t,e in enumerate(w['program']):
        if t==EVENT:
            marks['control']=len(ops);ops.append(['ADD',HELPER,cache,'1',43]);ops.append(['CLEAR',cache,43])
        actual=e.copy();actual[1]+=400 if actual[1]>=1480 else 0
        if actual[0] in ('ADD','COPY'):actual[2]+=400 if actual[2]>=1480 else 0
        native_map.append(len(ops));ops.append(actual)
        for x in observations[t]:
            marks['observation_'+str(t)]=len(ops)
            ops.append(['ADD',raw[RECEIVER],x['role'],str(a*F(x['coefficient'])),524])
        if t==36811:
            marks['receiver_corrected']=len(ops)
            for i,op,r in deferred:
                prefix_map[str(i)]=len(ops);reserve(r['source_event'],r['logical_role'],op,i)
    marks['common_finished']=len(ops)
    for r,c in sorted(Z.items()):ops.append(['ADD',r,raw[DONOR],str(-c),HUB])
    marks['common_restored']=len(ops)
    for r in mains:ops.append(['ADD',raw[r],r,'1',w['final'][r]])
    expected={t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in raw}
    need(len(reservations)==1710 and {r['source_event'] for r in reservations}==expected and len(expected)==1710,'all raw reservations used once')
    for r in mains:need([x['source_event'] for x in reservations if x['role']==r]==[t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]==r],'unchanged per-raw itinerary')
    need(len(prefix_map)==2362 and all(ops[prefix_map[str(i)]]==e for i,e in enumerate(p['program'])),'every pinned prefix operation retained once')
    need(sum('prefix_event' in r for r in reservations)==890,'all890 prefix raw reservations retained once')
    word=dict(schema='moonshot-eight-packet-one-history-correction-v1',source_sha256=PIN,prefix_decompressed_sha256=PREFIX_PIN,public=1880,owned_fields=w['owned_fields']+2,initial=p['initial'],private_role_map=p['difference_role_map'],program=ops,raw_reservations=reservations,marks=marks,prefix_event_to_physical=prefix_map,native_event_to_physical=native_map,donor_cache=cache,corrected_residual=dict(receiver=RECEIVER,donor=DONOR,coefficient=str(a)),all400_entry_and_final_recouplings_included=True)
    return word,raw,targets,q,a,residuals

def execute(w,word,raw,T,Z,targets,q,a,p):
    rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(word['initial']));spaces=list(map(space,w['frames']))
    bill=Counter();ranks=Counter();peak=life=0;cache=word['donor_cache'];extra=[0,0];peak_events=[]
    for t,e in enumerate(word['program']):
        op,r=e[:2];bill[op]+=1;need(0<=r<1880+word['owned_fields'],'declared role')
        if op=='INIT':need(r>=1880 and r not in loc,'owned INIT');loc[r]=e[2];rows[r]={};life+=1
        elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'owned CLEAR');loc.pop(r);rows.pop(r)
        elif op=='MOVE':
            x,y,owned=e[2:];need(loc.get(r)==x and type(owned)is bool and owned==(r>=1880),'typed MOVE')
            need(spaces[x]<spaces[y] or owned and spaces[y]<spaces[x],'proper nested complete chart MOVE')
            ranks[abs(len(w['frames'][y])-len(w['frames'][x]))]+=1;loc[r]=y
        elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'nonzero cochart SCALE');rows[r]=scale(rows[r],F(e[2]))
        elif op in ('ADD','COPY'):
            s,c,at=e[2:];need(r!=s and loc.get(r)==loc.get(s)==at,'actual cochart arithmetic at physical event '+str(t))
            if op=='COPY':need(not rows[r],'actual1880-input COPY guard')
            rows[r]=add(rows[r],rows[s],F(c))
        else:raise ValueError('physical opcode')
        live=len(loc)-1880
        if live>peak:peak=live;peak_events.append(dict(event=t,live=live,cache_live=cache in loc))
        if t+1==word['marks']['common_starts']:
            need(all(rows[i]=={i:F(1)} and loc[i]==w['initial'][i] for i in range(1480)),'all common fields unchanged before source')
            need(rows[cache]==q[DONOR] and loc[cache]==43,'actual retained original q47 cache')
            need(loc[raw[DONOR]]==127 and rows[raw[DONOR]]==q[DONOR],'original raw donor retained at hub')
            need(loc[raw[RECEIVER]]==524,'actual receiver delayed at observation chart')
        if t==word['marks']['control']:
            need(rows[cache]==q[DONOR] and loc[cache]==43,'actual q47 source at control cut')
        if t+1==word['marks']['receiver_corrected']:
            need(rows[raw[RECEIVER]]==add(targets[RECEIVER],q[DONOR],-a),'actual one-quarter residual removed')
        if t+1==word['marks']['common_finished']:
            for i in range(1480):need(rows[i]==add(T[i],q[DONOR],Z.get(i,F(0))),'all1480 pre-repair common rows')
            for i,rid in raw.items():
                target=add(targets[i],q[DONOR],-a) if i==RECEIVER else targets[i]
                need(rows[rid]==target,'complete400-row unrecoupled E8-plus-one-correction identity')
        if t+1==word['marks']['common_restored']:
            for i in range(1480):need(rows[i]==T[i],'all1480 common fields restored')
    for i in range(1480):need(rows[i]==T[i] and loc[i]==w['final'][i],'final common identity/location')
    unrecoupled={}
    for i,rid in raw.items():
        target=add(T[i],targets[i]);target=add(target,q[DONOR],-a) if i==RECEIVER else target
        need(rows[rid]==target and loc[rid]==w['final'][i],'final recoupled private identity/location')
        unrecoupled[i]=add(rows[rid],T[i],F(-1))
    need(set(rows)==set(range(1880)) and len(loc)==1880,'all owned lifetimes retired')
    xs=p['donor_roles'];roots=p['roots'];recovered={r:unrecoupled[r].copy() for r in raw}
    for i,x in enumerate(xs):
        c=F(p['receiver_weights'][str(x)]);row=unrecoupled[x+112].copy()
        for j,d in enumerate(xs):
            g=dot(roots[i],roots[j])
            if g:row=add(row,unrecoupled[d],-c*g/8)
        if x+112==RECEIVER:row=add(row,unrecoupled[DONOR],a)
        recovered[x+112]=scale(row,1/c)
    need(recovered==q,'explicit inverse of all400 actual private difference rows')
    return dict(instructions=len(word['program']),opcode_counts=dict(sorted(bill.items())),move_rank_histogram=dict(sorted(ranks.items())),owned_lifetimes=life,peak_owned=peak,final_owned=0,peak_increase_events=peak_events)

def main(a):
    b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(b))
    cb=(a.packet/'INPUT-CERTIFICATE.json').read_bytes();need(hashlib.sha256(cb).hexdigest()==CERT_PIN,'discovery certificate pin');cert=json.loads(cb)
    pb=gzip.decompress((a.packet/'INPUT-PREFIX.json.gz').read_bytes());need(hashlib.sha256(pb).hexdigest()==PREFIX_PIN,'frozen actual prefix pin');p=json.loads(pb)
    T,Z,dec,guards,snapshots=source_certificate(w,cert);word,raw,targets,q,c,residuals=build(w,p,Z,dec)
    bill=execute(w,word,raw,T,Z,targets,q,c,p)
    base=Counter(e[0] for e in w['program']);base['MOVE']+=1710;base['ADD']+=800
    increment={k:bill['opcode_counts'][k]-base[k] for k in sorted(base)}
    need(increment==dict(ADD=1184,CLEAR=9,COPY=0,INIT=9,MOVE=8,SCALE=8),'complete prefix-and-correction increment')
    need(bill['instructions']==74989 and bill['owned_lifetimes']==63,'complete instruction/lifetime count')
    need(sum(r==RECEIVER and d==DONOR for r,d,_ in residuals)==1,'one original weighted residual selected')
    remaining=[(r,d,k) for r,d,k in residuals if (r,d)!=(RECEIVER,DONOR)]
    need(all(sum(r==x+112 for r,d,k in remaining)>0 for x in p['donor_roles']),'every receiver still has uncorrected residual terms')
    record=dict(schema='moonshot-eight-packet-one-history-correction-result-v1',status='PASS_ACTUAL1880_INPUT_E8_PREFIX_ONE_WEIGHTED_RESIDUAL_REMOVED_COMMON_RESTORED',source_sha256=PIN,prefix_decompressed_sha256=PREFIX_PIN,discovery_certificate_sha256=CERT_PIN,independent_physical_inputs=1880,corrected_residual=dict(receiver=RECEIVER,donor=DONOR,original_coefficient=str(c),history_applied_coefficient=str(c),history_gain='-1',final_coefficient='0'),bill=bill,added_ordinary=increment,increment_beyond_common_raw_boundaries_and_E8=dict(ADD=144,CLEAR=1,COPY=0,INIT=1,MOVE=0,SCALE=0),new_paid_move_histogram={9:8},new_paid_moment='8 * 9^(199/200)',correction_added_recursive_moment='0',prefix_operations_retained_once=len(p['program']),prefix_raw_reservations_retained_once=890,remaining_source_raw_reservations_completed=820,all_original_raw_reservations_used_once=1710,all400_entry_and_final_recouplings_included=True,common_all1480_rows_restored=True,common_hub_repair_terms=len(Z),COPY_guard_responses=guards,private_difference_inverse_checked=True,original_weighted_residual_terms=len(residuals),remaining_weighted_residual_terms=len(remaining),remaining_at_receiver172=sum(r==RECEIVER for r,d,k in remaining),completed_private_receivers=0,actual_original_q47_cache=dict(role=word['donor_cache'],chart=43,moves=0,lifetimes=1),scope='Actual composed forward E8 prefix plus one weighted cross-coordinate correction and complete common restoration. All other residual corrections and hosted/coupled reverse duties remain open. No new complete kappa.',new_complete_kappa=None)
    a.output.mkdir(parents=True,exist_ok=True);wb=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode()
    (a.output/'WORD.json.gz').write_bytes(gzip.compress(wb,mtime=0));record['word_decompressed_sha256']=hashlib.sha256(wb).hexdigest()
    (a.output/'RESULT.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='bill'},indent=2));print(json.dumps({k:v for k,v in bill.items() if k!='peak_increase_events'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
