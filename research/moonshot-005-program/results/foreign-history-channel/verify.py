#!/usr/bin/env python3
"""Exact1880-input q47-to-q172 history channel with full common restoration.

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

def build(w, Z, dec):
    mains=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    raw={r:1480+i for i,r in enumerate(mains)};need(len(raw)==400,'all400 mains')
    ops=[];reservations=[];marks={};moves=defaultdict(list)
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1] in raw:moves[e[1]].append((t,e))
    def raw_move(t,e):
        reservations.append({'source_event':t,'physical_event':len(ops),'role':e[1]})
        ops.append(['MOVE',raw[e[1]],e[2],e[3],False])
    for r in mains:ops.append(['ADD',raw[r],r,'-1',w['initial'][r]])
    for x in dec['initial_terms']:ops.append(['ADD',raw[RECEIVER],x['role'],str(-F(x['coefficient'])),3])
    need([e[2:4] for t,e in moves[RECEIVER]]==[[3,404],[404,524],[524,920],[920,183]],'receiver itinerary')
    for t,e in moves[RECEIVER][:2]:raw_move(t,e)
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1] in raw and e[1] not in (DONOR,RECEIVER):raw_move(t,e)
    observations=defaultdict(list)
    for x in dec['arrival_terms']:observations[x['after_event']].append(x)
    for t,e in enumerate(w['program']):
        if t==EVENT:
            marks['control']=len(ops);ops.append(['ADD',HELPER,raw[DONOR],'1',43])
            for tt,ee in moves[DONOR]:raw_move(tt,ee)
        actual=e.copy();actual[1]+=400 if actual[1]>=1480 else 0
        if actual[0] in ('ADD','COPY'):actual[2]+=400 if actual[2]>=1480 else 0
        ops.append(actual)
        for x in observations[t]:
            marks['observation_'+str(t)]=len(ops)
            ops.append(['ADD',raw[RECEIVER],x['role'],str(-F(x['coefficient'])),524])
        if t==36811:
            marks['receiver_decoded']=len(ops)
            for tt,ee in moves[RECEIVER][2:]:raw_move(tt,ee)
    marks['common_finished']=len(ops)
    for r,c in sorted(Z.items()):ops.append(['ADD',r,raw[DONOR],str(-c),HUB])
    marks['common_restored']=len(ops)
    for r in mains:ops.append(['ADD',raw[r],r,'1',w['final'][r]])
    expected={t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in raw}
    need(len(reservations)==1710 and {r['source_event'] for r in reservations}==expected and len({r['source_event'] for r in reservations})==len(reservations),'each funded raw reservation used once')
    for r in mains:
        need([x['source_event'] for x in reservations if x['role']==r]==[t for t,e in moves[r]],'each raw itinerary order unchanged')
    return dict(schema='moonshot-neutral-foreign-history-word-v1',source_sha256=PIN,public=1880,owned_fields=w['owned_fields'],initial=w['initial']+[w['initial'][r] for r in mains],private_role_map={str(r):q for r,q in raw.items()},program=ops,raw_reservations=reservations,marks=marks,all400_entry_and_final_recouplings_included=True),raw

def execute(w, word, raw, T, Z):
    rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(word['initial']));spaces=list(map(space,w['frames']))
    bill=Counter();ranks=Counter();peak=life=0;q={raw[DONOR]:F(1),DONOR:F(-1)}
    for t,e in enumerate(word['program']):
        op,r=e[:2];bill[op]+=1;need(0<=r<1880+word['owned_fields'],'declared role')
        if op=='INIT':need(r>=1880 and r not in loc,'owned INIT');loc[r]=e[2];rows[r]={};life+=1
        elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'owned CLEAR');loc.pop(r);rows.pop(r)
        elif op=='MOVE':
            a,b,owned=e[2:];need(loc.get(r)==a and type(owned)is bool and owned==(r>=1880),'typed MOVE')
            need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'proper nested complete chart MOVE')
            ranks[abs(len(w['frames'][b])-len(w['frames'][a]))]+=1;loc[r]=b
        elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'nonzero cochart SCALE');rows[r]=scale(rows[r],F(e[2]))
        elif op in ('ADD','COPY'):
            s,c,at=e[2:];need(r!=s and loc.get(r)==loc.get(s)==at,'actual cochart arithmetic')
            if op=='COPY':need(not rows[r],'actual1880-input COPY guard')
            rows[r]=add(rows[r],rows[s],F(c))
        else:raise ValueError('physical opcode')
        peak=max(peak,len(loc)-1880)
        if t+1==word['marks']['receiver_decoded']:
            need(rows[raw[RECEIVER]]==add({raw[RECEIVER]:F(1),RECEIVER:F(-1)},q),'actual receiver q172+q47 gain')
        if t+1==word['marks']['common_finished']:
            for i in range(1480):need(rows[i]==add(T[i],q,Z.get(i,F(0))),'all1480 pre-repair common identities')
            for i,rid in raw.items():
                target={rid:F(1),i:F(-1)}
                if i==RECEIVER:target=add(target,q)
                need(rows[rid]==target,'all400 unrecoupled private identities')
        if t+1==word['marks']['common_restored']:
            for i in range(1480):need(rows[i]==T[i],'all1480 common fields restored')
    for i in range(1480):need(rows[i]==T[i] and loc[i]==w['final'][i],'final common identity/location')
    for i,rid in raw.items():
        target=add(T[i],{rid:F(1),i:F(-1)})
        if i==RECEIVER:target=add(target,q)
        need(rows[rid]==target and loc[rid]==w['final'][i],'final recoupled private identity/location')
    need(set(rows)==set(range(1880)) and len(loc)==1880,'all owned lifetimes retired')
    return dict(instructions=len(word['program']),opcode_counts=dict(sorted(bill.items())),move_rank_histogram=dict(sorted(ranks.items())),owned_lifetimes=life,peak_owned=peak,final_owned=0)

def main(a):
    b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(b))
    cb=(a.packet/'INPUT-CERTIFICATE.json').read_bytes();need(hashlib.sha256(cb).hexdigest()==CERT_PIN,'discovery certificate pin');cert=json.loads(cb)
    T,Z,dec,guards,snapshots=source_certificate(w,cert);word,raw=build(w,Z,dec);bill=execute(w,word,raw,T,Z)
    base=Counter(e[0] for e in w['program']);base['MOVE']+=1710;base['ADD']+=800
    increment={k:bill['opcode_counts'][k]-base[k] for k in sorted(base)}
    need(increment=={'ADD':143,'CLEAR':0,'COPY':0,'INIT':0,'MOVE':0,'SCALE':0},'complete ordinary increment')
    need(bill['instructions']==73914 and bill['peak_owned']==43 and bill['owned_lifetimes']==54,'full word counts and lifetime bound')
    late=add(snapshots[36812,1197],snapshots[36811,1197],F(-1));need(late,'late-read contamination witness')
    record=dict(schema='moonshot-neutral-foreign-history-channel-v1',status='PASS_ACTUAL1880_INPUT_CHANNEL_WITH_NO_ADDED_MOVE_OR_LIFETIME',source_sha256=PIN,discovery_certificate_sha256=CERT_PIN,discovery_parent_sha256=cert['discovery_receipt_sha256'],donor=DONOR,receiver=RECEIVER,control_before_event=EVENT,control_role=HELPER,control_chart=43,initial_decoder_terms=107,actual_history_reads=dec['arrival_terms'],baseline_decoder_common_row_zero=True,decoder_pulse_gain='-1',receiver_applied_gain='1',common_response_support=33,offhub_response_support=0,common_hub_response=ser(Z),COPY_guard_responses=guards,bill=bill,added_ordinary=increment,added_complete_recursive_calls=0,added_recursive_moment='0',original_raw_reservations_used_once=1710,all400_entry_and_final_recouplings_included=True,negative_controls=[dict(change='omit initial coefficient at common34',receiver_error=[[34,'1']]),dict(change='read1197 after36812 instead of36811',receiver_error=ser(scale(late,F(-1)))),dict(change='omit hub correction at common3',common_error_output=3,private_input=raw[DONOR],coefficient=str(Z[3])),dict(change='use gain sign+1 instead of-1',receiver_private_input=raw[DONOR],coefficient_error='-2')],scope='One fully restored cross-coordinate private shear, beyond the declared pure-payload routing edge grant. The other private-native dependencies, composition, suppliers and all physical/recursive/compiler obligations remain open. No new kappa.',new_complete_kappa=None)
    a.output.mkdir(parents=True,exist_ok=True)
    wb=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode()
    (a.output/'WORD.json.gz').write_bytes(gzip.compress(wb,mtime=0));record['word_decompressed_sha256']=hashlib.sha256(wb).hexdigest()
    (a.output/'RESULT.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('common_hub_response','negative_controls')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
