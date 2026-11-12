#!/usr/bin/env python3
"""Exact1880-input E8 prefix with seven simultaneous weighted history corrections.

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

PREFIX_PIN='52123f6dbe9488835b4aaa9eeb22cd721a8aab0197f17489fb7393d2b2e2865e'
CONTROLLER_PIN='bcc2bf5e5297dd3b81c24789e8b06035cc72466ce860be150fe9f6a24b297486'

def root(v):
    bits=[i for i in range(9) if v>>i&1]
    if len(bits)==3:return [2*(i in bits) for i in range(8)] if 8 in bits else [1 if i in bits else -1 for i in range(8)]
    need(len(bits)==7,'source root weight')
    i,j=[i for i in range(9) if i not in bits]
    return [1 if k==i else -1 for k in range(8)] if j==8 else [2*((k==i)-(k==j)) for k in range(8)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def prefix_targets(w,p,raw):
    xs=sorted(w['live']);ports=[w['frames'][w['initial'][r]][0] for r in xs];roots=[root(v) for v in ports]
    need(xs==p['donor_roles'] and ports==p['ports'] and roots==p['roots'],'source prefix roots')
    coupled=set(range(104))-set(w['hosted']['Dports']);weights={r:F(1,2) if i in coupled else F(1) for i,r in enumerate(xs)}
    need({str(r):str(c) for r,c in weights.items()}==p['receiver_weights'],'source prefix weights')
    q={r:{rid:F(1),r:F(-1)} for r,rid in raw.items()};out={r:q[r].copy() for r in raw};residuals={}
    for i,x in enumerate(xs):
        out[x+112]=scale(q[x+112],weights[x])
        for j,d in enumerate(xs):
            c=weights[x]*dot(roots[i],roots[j])/8
            if c:out[x+112]=add(out[x+112],q[d],c)
            if c and d!=x:residuals[x+112,d]=c
    return out,q,weights,residuals

def source_certificate(w,cert):
    families=cert['families'];weighted=cert['weighted_partial_E8_construction'];decoders=weighted['decoders']
    ds=[f['donor'] for f in families];scalings={int(d):F(c) for d,c in weighted['donor_control_scalings'].items()}
    need(ds==[36,37,47,110,111],'exact five-donor family')
    controls=defaultdict(list);observations=defaultdict(list);baseline={i:{i:F(1)} for i in range(1480)}
    pulses={i:{} for i in range(1480)};loc=dict(enumerate(w['initial']));base_dec={};gain_dec={};guards=[]
    for f in families:
        d=f['donor'];need(f['chart']==w['initial'][d],'controller at actual donor initial chart')
        for x in f['controls']:controls[x['before_event']].append((d,x))
    for dec in decoders:
        r=dec['receiver'];base_dec[r]={};gain_dec[r]={}
        for x in dec['initial_terms']:
            need(x['chart']==w['initial'][x['role']]==3,'actual initial decoder term at chart3')
            base_dec[r]=add(base_dec[r],baseline[x['role']],F(x['coefficient']))
        for x in dec['arrival_terms']:observations[x['after_event']].append((r,x))
    for t,e in enumerate(w['program']):
        for d,x in controls[t]:
            need(loc[x['role']]==x['chart']==w['initial'][d],'actual control source cut')
            pulses[x['role']]=add(pulses[x['role']],{d:F(1)},scalings[d]*F(x['coefficient']))
        op,r=e[:2]
        if op=='INIT':baseline[r]={};pulses[r]={};loc[r]=e[2]
        elif op=='CLEAR':baseline.pop(r);pulses.pop(r);loc.pop(r)
        elif op=='MOVE':need(loc[r]==e[2],'native MOVE source chart');loc[r]=e[3]
        elif op=='SCALE':baseline[r]=scale(baseline[r],F(e[2]));pulses[r]=scale(pulses[r],F(e[2]))
        elif op in ('ADD','COPY'):
            if op=='COPY':need(not baseline[r] and not pulses[r],'actual joint COPY guard');guards.append({'event':t,'responses':ser(pulses[r])})
            baseline[r]=add(baseline[r],baseline[e[2]],F(e[3]));pulses[r]=add(pulses[r],pulses[e[2]],F(e[3]))
        else:raise ValueError('native opcode')
        for y,x in observations[t]:
            need(loc[x['role']]==x['chart'],'actual source history cut')
            base_dec[y]=add(base_dec[y],baseline[x['role']],F(x['coefficient']))
            gain_dec[y]=add(gain_dec[y],pulses[x['role']],F(x['coefficient']))
    T=declared_endpoints(w);need(baseline==T,'all1480 native endpoints')
    Z={r:row for r,row in pulses.items() if row}
    need(all(w['final'][r]==127 for r in Z),'all joint terminal common debt at hub')
    for f in families:
        d=f['donor'];actual={r:row[d] for r,row in Z.items() if d in row}
        expected={int(r):scalings[d]*F(c) for r,c in f['hub_response'].items()}
        need(actual==expected,'exact scaled full source endpoint response for donor '+str(d))
    for dec in decoders:
        y=dec['receiver'];need(not base_dec[y],'complete1480-input baseline decoder zero')
        gain=scale(gain_dec[y],F(dec['decoder_scale']))
        need(gain=={int(d):F(c) for d,c in dec['resulting_private_row'].items()},'complete joint selected decoder private row')
    need(sum(len(row) for row in Z.values())==1014 and sum(len(f['controls']) for f in families)==10,'exact common repair/control counts')
    return T,Z,decoders,scalings,guards

def build(w,p,cert,Z,decoders,scalings):
    raw={int(r):rid for r,rid in p['difference_role_map'].items()};mains=sorted(raw);families=cert['families'];ds=[f['donor'] for f in families]
    need(len(raw)==400 and raw=={r:1480+i for i,r in enumerate(mains)},'canonical400 raw roles')
    targets,q,weights,residuals=prefix_targets(w,p,raw)
    corrections={x['receiver']:{int(d):weights[x['receiver']-112]*F(c) for d,c in x['resulting_private_row'].items()} for x in decoders}
    need(sum(map(len,corrections.values()))==7,'seven simultaneous specified terms')
    for y,row in corrections.items():
        for d,c in row.items():need(residuals[y,d]+c==0,'actual weighted E8 cancellation')
    caches={d:1880+w['owned_fields']+1+i for i,d in enumerate(ds)}
    ops=[];reservations=[];marks={};prefix_map={};native_map=[];controls=defaultdict(list);last={};observations=defaultdict(list)
    prefix_marks={x['physical_event']:x['purpose'] for x in p['marks']};prefix_res={x['physical_event']:x for x in p['reservations']}
    decoder_by_y={x['receiver']:x for x in decoders};selected=set(decoder_by_y);deferred=defaultdict(list);raw_loc={y:3 for y in selected};cursor={y:0 for y in selected};read_stages={}
    for f in families:
        d=f['donor'];last[d]=max(x['before_event'] for x in f['controls'])
        for x in f['controls']:controls[x['before_event']].append((d,x))
    for dec in decoders:
        y=dec['receiver'];arr=sorted(dec['arrival_terms'],key=lambda x:x['after_event']);route=dec['causal_original_route'];indices=[route.index(x['chart']) for x in arr]
        need(indices==sorted(indices),'causal selected history order')
        stages=[]
        for x in arr:
            observations[x['after_event']].append((y,x))
            if not stages or stages[-1]['chart']!=x['chart']:stages.append(dict(chart=x['chart'],last_event=x['after_event']))
            else:stages[-1]['last_event']=x['after_event']
        read_stages[y]=stages
    def reserve(t,r,op,pi=None):
        record=dict(source_event=t,physical_event=len(ops),role=r)
        if pi is not None:record['prefix_event']=pi
        reservations.append(record);ops.append(op.copy())
    initial_done=False
    for i,op in enumerate(p['program']):
        if i==400:
            need(all(prefix_marks[j]=='form_actual_difference' for j in range(400)),'all actual differences formed before caches')
            marks['cache_acquisitions']=len(ops)
            for d in ds:ops.extend([['INIT',caches[d],w['initial'][d]],['ADD',caches[d],raw[d],'1',w['initial'][d]]])
        if not initial_done and prefix_marks[i]=='funded_receiver_route':
            marks['initial_decoders']=len(ops)
            for dec in decoders:
                y=dec['receiver'];a=weights[y-112]*F(dec['decoder_scale'])
                for x in dec['initial_terms']:ops.append(['ADD',raw[y],x['role'],str(a*F(x['coefficient'])),3])
            initial_done=True
        if i in prefix_res:
            rr=prefix_res[i];r=rr['logical_role']
            if r in selected:deferred[r].append((i,op,rr));continue
            prefix_map[str(i)]=len(ops);reserve(rr['source_event'],r,op,i)
        else:prefix_map[str(i)]=len(ops);ops.append(op.copy())
    need(initial_done,'initial decoder insertion after all packet mixtures')
    def advance(y,to):
        while raw_loc[y]!=to:
            k=cursor[y];need(k<len(deferred[y]),'required chart occurs later on receiver route')
            i,op,rr=deferred[y][k];need(op[2]==raw_loc[y],'causal raw receiver MOVE')
            prefix_map[str(i)]=len(ops);reserve(rr['source_event'],y,op,i);raw_loc[y]=op[3];cursor[y]+=1
    for y in sorted(selected):advance(y,read_stages[y][0]['chart'])
    marks['prefix_scheduled']=len(ops)
    active=set(w['live'])|{x+112 for x in w['live']}
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1] in raw and e[1] not in active:reserve(t,e[1],['MOVE',raw[e[1]],e[2],e[3],False])
    marks['common_starts']=len(ops);stage_index={y:0 for y in selected}
    for t,e in enumerate(w['program']):
        for d,x in controls[t]:
            marks['control_'+str(d)+'_'+str(t)]=len(ops)
            ops.append(['ADD',x['role'],caches[d],str(scalings[d]*F(x['coefficient'])),x['chart']])
        for d in ds:
            if t==last[d]:ops.append(['CLEAR',caches[d],w['initial'][d]])
        actual=e.copy();actual[1]+=400 if actual[1]>=1480 else 0
        if actual[0] in ('ADD','COPY'):actual[2]+=400 if actual[2]>=1480 else 0
        native_map.append(len(ops));ops.append(actual)
        for y,x in observations[t]:
            a=weights[y-112]*F(decoder_by_y[y]['decoder_scale'])
            marks['observation_'+str(y)+'_'+str(t)]=len(ops)
            ops.append(['ADD',raw[y],x['role'],str(a*F(x['coefficient'])),x['chart']])
        for y in sorted(selected):
            k=stage_index[y]
            if k<len(read_stages[y]) and t==read_stages[y][k]['last_event']:
                stage_index[y]+=1
                if k+1<len(read_stages[y]):advance(y,read_stages[y][k+1]['chart'])
                else:
                    marks['receiver_corrected_'+str(y)]=len(ops);advance(y,w['final'][y])
    marks['common_finished']=len(ops)
    for r,row in sorted(Z.items()):
        for d,c in sorted(row.items()):ops.append(['ADD',r,raw[d],str(-c),127])
    marks['common_restored']=len(ops)
    for r in mains:ops.append(['ADD',raw[r],r,'1',w['final'][r]])
    expected={t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in raw}
    need(len(reservations)==1710 and {x['source_event'] for x in reservations}==expected and len(expected)==1710,'all1710 original reservations exactly once')
    for r in mains:need([x['source_event'] for x in reservations if x['role']==r]==[t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]==r],'unchanged per-raw route order')
    need(len(prefix_map)==len(p['program'])==2362 and all(ops[prefix_map[str(i)]]==op for i,op in enumerate(p['program'])),'all frozen prefix operations retained once')
    need(sum('prefix_event' in x for x in reservations)==890,'all890 prefix reservations retained once')
    word=dict(schema='moonshot-eight-packet-seven-history-corrections-v1',source_sha256=PIN,prefix_decompressed_sha256=PREFIX_PIN,controller_certificate_sha256=CONTROLLER_PIN,public=1880,owned_fields=w['owned_fields']+6,initial=p['initial'],private_role_map=p['difference_role_map'],program=ops,raw_reservations=reservations,marks=marks,prefix_event_to_physical=prefix_map,native_event_to_physical=native_map,donor_caches={str(d):r for d,r in caches.items()},corrections={str(y):ser(row) for y,row in corrections.items()},all400_entry_and_final_recouplings_included=True)
    return word,raw,targets,q,corrections,residuals,caches

def execute(w,p,word,raw,T,Z,targets,q,corrections,caches):
    rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(word['initial']));spaces=list(map(space,w['frames']))
    bill=Counter();ranks=Counter();life=peak=0;peak_events=[];end_targets={r:row.copy() for r,row in targets.items()}
    for y,row in corrections.items():
        for d,c in row.items():end_targets[y]=add(end_targets[y],q[d],c)
    checkpoints={v:int(k.split('_')[-1]) for k,v in word['marks'].items() if k.startswith('receiver_corrected_')}
    for t,e in enumerate(word['program']):
        op,r=e[:2];bill[op]+=1;need(0<=r<1880+word['owned_fields'],'declared physical role')
        if op=='INIT':need(r>=1880 and r not in loc,'fresh owned INIT');loc[r]=e[2];rows[r]={};life+=1
        elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'owned CLEAR');loc.pop(r);rows.pop(r)
        elif op=='MOVE':
            x,y,owned=e[2:];need(loc.get(r)==x and type(owned)is bool and owned==(r>=1880),'typed MOVE source and ownership')
            need(spaces[x]<spaces[y] or owned and spaces[y]<spaces[x],'proper nested complete MOVE')
            ranks[abs(len(w['frames'][y])-len(w['frames'][x]))]+=1;loc[r]=y
        elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'nonzero cochart SCALE');rows[r]=scale(rows[r],F(e[2]))
        elif op in ('ADD','COPY'):
            s,c,at=e[2:];need(r!=s and loc.get(r)==loc.get(s)==at,'cochart arithmetic at physical event '+str(t))
            if op=='COPY':need(not rows[r],'actual all1880-input COPY guard')
            rows[r]=add(rows[r],rows[s],F(c))
        else:raise ValueError('physical opcode')
        n=len(loc)-1880
        if n>peak:peak=n;peak_events.append(dict(physical_event=t,live=n,caches_live=[d for d,rr in caches.items() if rr in loc]))
        if t+1==word['marks']['common_starts']:
            need(all(rows[i]=={i:F(1)} and loc[i]==w['initial'][i] for i in range(1480)),'all common inputs untouched before source')
            for d,rr in caches.items():need(rows[rr]==q[d] and loc[rr]==w['initial'][d] and rows[raw[d]]==q[d] and loc[raw[d]]==127,'actual stationary cache and actual original donor at hub')
        if t+1 in checkpoints:
            y=checkpoints[t+1];need(rows[raw[y]]==end_targets[y],'actual simultaneous weighted receiver correction at '+str(y))
        if t+1==word['marks']['common_finished']:
            for i in range(1480):
                target=T[i].copy()
                for d,c in Z.get(i,{}).items():target=add(target,q[d],c)
                need(rows[i]==target,'all1480 pre-repair joint common rows')
            need(all(rows[raw[r]]==row for r,row in end_targets.items()),'all400 unrecoupled joint private rows')
        if t+1==word['marks']['common_restored']:
            need(all(rows[i]==T[i] for i in range(1480)),'all1480 common fields restored')
    for i in range(1480):need(rows[i]==T[i] and loc[i]==w['final'][i],'final common value and chart')
    unrecoupled={}
    for r,rid in raw.items():
        need(rows[rid]==add(T[r],end_targets[r]) and loc[rid]==w['final'][r],'complete final private value and chart')
        unrecoupled[r]=add(rows[rid],T[r],F(-1))
    need(set(rows)==set(range(1880)) and len(loc)==1880,'all owned lifetimes retired')
    recovered={r:row.copy() for r,row in unrecoupled.items()};xs=p['donor_roles'];roots=p['roots']
    for i,x in enumerate(xs):
        y=x+112;c=F(p['receiver_weights'][str(x)]);row=unrecoupled[y].copy()
        for j,d in enumerate(xs):
            g=dot(roots[i],roots[j])
            if g:row=add(row,unrecoupled[d],-c*g/8)
        for d,k in corrections.get(y,{}).items():row=add(row,unrecoupled[d],-k)
        recovered[y]=scale(row,1/c)
    need(recovered==q,'explicit inverse of all400 actual private difference rows')
    return dict(instructions=len(word['program']),opcode_counts=dict(sorted(bill.items())),move_rank_histogram=dict(sorted(ranks.items())),owned_lifetimes=life,peak_owned=peak,final_owned=0,peak_increase_events=peak_events)

def main(a):
    b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'source SHA256');w=json.loads(gzip.decompress(b))
    cb=(a.packet/'INPUT-CONTROLLERS.json').read_bytes();need(hashlib.sha256(cb).hexdigest()==CONTROLLER_PIN,'controller certificate SHA256');cert=json.loads(cb)
    pb=gzip.decompress((a.packet/'INPUT-PREFIX.json.gz').read_bytes());need(hashlib.sha256(pb).hexdigest()==PREFIX_PIN,'prefix payload SHA256');p=json.loads(pb)
    T,Z,decoders,scalings,guards=source_certificate(w,cert);word,raw,targets,q,corrections,residuals,caches=build(w,p,cert,Z,decoders,scalings)
    bill=execute(w,p,word,raw,T,Z,targets,q,corrections,caches)
    base=Counter(e[0] for e in w['program']);base['MOVE']+=1710;base['ADD']+=800
    increment={k:bill['opcode_counts'][k]-base[k] for k in sorted(base)}
    need(increment==dict(ADD=2247,CLEAR=13,COPY=0,INIT=13,MOVE=8,SCALE=8),'complete finite invoice')
    need(bill['instructions']==76060 and bill['owned_lifetimes']==67,'complete instruction and lifetime count')
    corrected={(y,d) for y,row in corrections.items() for d in row};remaining={k:c for k,c in residuals.items() if k not in corrected}
    need(len(residuals)==4992 and len(corrected)==7 and len(remaining)==4985,'exact residual coefficient census')
    need(all(any(y==x+112 for y,d in remaining) for x in p['donor_roles']),'no firstY receiver completed')
    record=dict(schema='moonshot-eight-packet-seven-history-corrections-result-v1',status='PASS_ACTUAL1880_INPUT_JOINT_SEVEN_WEIGHTED_CORRECTIONS_COMMON_RESTORED',source_sha256=PIN,prefix_decompressed_sha256=PREFIX_PIN,controller_certificate_sha256=CONTROLLER_PIN,independent_physical_inputs=1880,donor_order=cert['donor_order'],corrected_residuals=[dict(receiver=y,donor=d,original_coefficient=str(residuals[y,d]),applied_correction=str(corrections[y][d]),final_coefficient='0') for y,d in sorted(corrected)],joint_receiver172_correction=ser(corrections[172]),joint_selected_history_private_rank=4,bill=bill,added_ordinary=increment,increment_beyond_common_raw_boundaries_and_E8=dict(ADD=1207,CLEAR=5,COPY=0,INIT=5,MOVE=0,SCALE=0),control_adds=10,history_adds=178,hub_repair_adds=1014,cache_acquisition_adds=5,stationary_caches={str(d):dict(role=r,chart=w['initial'][d],moves=0) for d,r in caches.items()},new_paid_move_histogram={9:8},new_paid_moment='8 * 9^(199/200)',correction_added_recursive_moment='0',prefix_operations_retained_once=2362,prefix_raw_reservations_retained_once=890,other_source_raw_reservations_completed=820,all_original_raw_reservations_used_once=1710,all400_entry_and_final_recouplings_included=True,common_all1480_rows_restored=True,common_endpoint_debt_support=len(Z),COPY_guards=guards,private_difference_inverse_checked=True,original_weighted_residual_terms=4992,corrected_weighted_residual_terms=7,remaining_weighted_residual_terms=4985,all_other_residual_coefficients_unchanged=True,remaining_at_selected_receivers={str(y):sum(yy==y for yy,d in remaining) for y in corrections},completed_firstY_receivers=0,scope='Actual joint composition of five initial-line controllers and six causal history decoders with the retained eight-packet prefix. Seven specified weighted residual coefficients vanish; all4985 others are unchanged. Entire common native restored and all raw endpoints recoupled. Other residual and private reverse duties remain open; no complete new kappa.',new_complete_kappa=None)
    a.output.mkdir(parents=True,exist_ok=True);wb=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode()
    (a.output/'WORD.json.gz').write_bytes(gzip.compress(wb,mtime=0));record['word_decompressed_sha256']=hashlib.sha256(wb).hexdigest()
    (a.output/'RESULT.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='bill'},indent=2));print(json.dumps({k:v for k,v in bill.items() if k!='peak_increase_events'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
