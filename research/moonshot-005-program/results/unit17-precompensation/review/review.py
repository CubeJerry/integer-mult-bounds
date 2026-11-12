#!/usr/bin/env python3
"""Independent all-input interpreter; imports no author implementation."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
WORD='c75f595393d32f0ddefed906e9dab02e6e09b764730684541375d6979c6c349c'
DONORS=[77,103,22,109,20,46,41,106,26,24,107,58,28,92,57,7,8]
def require(ok,message):
    if not ok:raise ValueError(message)
def subspace(frame):
    values={0}
    for vector in frame:values.update(v^vector for v in tuple(values))
    return frozenset(values)
def plus(target,source,scalar):
    for k,v in tuple(source.items()):
        value=target.get(k,Q(0))+scalar*v
        if value:target[k]=value
        elif k in target:del target[k]
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
b=args.source.read_bytes();require(hashlib.sha256(b).hexdigest()==SOURCE,'source bytes');native=json.loads(gzip.decompress(b));b=args.word.read_bytes();require(hashlib.sha256(b).hexdigest()==WORD,'word bytes');word=json.loads(gzip.decompress(b));require(word['source_sha256']==SOURCE,'word source pin')
frames=list(map(subspace,native['frames']));mains=sorted(set(native['live'])|{x+112 for x in native['live']}|set(native['hosted']['X2'])|set(native['hosted']['Y2']));raw={j:1480+i for i,j in enumerate(mains)}
require(word['difference_role_map']=={str(j):raw[j] for j in mains},'actual second-input map');require(word['public']==1880 and len(word['initial'])==1880,'1880 independent inputs');require(word['initial']==native['initial']+[native['initial'][j] for j in mains],'initial charts');require(word['completed_second_shear_donors']==DONORS,'17 donor set')
def remap_common(x):
    x=x[:];op=x[0]
    if x[1]>=1480:x[1]+=400
    if op in ('ADD','COPY') and x[2]>=1480:x[2]+=400
    return x
marks=word['marks'];program=word['program'];require(len(marks)==len(program),'mark count');require([x for x,m in zip(program,marks) if m=='original_common_word']==list(map(remap_common,native['program'])),'complete native common subsequence')
reservations=word['funded_raw_reservations'];expected_moves={i for i,x in enumerate(native['program']) if x[0]=='MOVE' and x[1] in raw}
def check_reservations(res):
    seen=set();positions=set()
    for a in res:
        event=a['source_event'];position=a['physical_event'];require(event not in seen and position not in positions,'duplicate funded reservation');seen.add(event);positions.add(position)
        x=native['program'][event];require(x[0]=='MOVE' and x[1] in raw,'source main MOVE');require(a['logical_role']==x[1],'reservation logical role');require(program[position]==['MOVE',raw[x[1]],x[2],x[3],False],'reservation physical MOVE');require(marks[position]=='funded_raw_MOVE','reservation mark')
    require(seen==expected_moves,'all1710 reservations exactly once');require(positions=={i for i,m in enumerate(marks) if m=='funded_raw_MOVE'},'all raw MOVE marks accounted')
check_reservations(reservations)
target={j:{j:Q(1)} for j in range(1880)}
for i,x in enumerate(native['live']):
    y=x+112
    if i in native['hosted']['Dports']:target[y]={y:Q(1),x:Q(1)}
    else:target[x]={x:Q(1),y:Q(-1)};target[y]={x:Q(1,2),y:Q(1,2)}
for x,y in zip(native['hosted']['X2'],native['hosted']['Y2']):target[x]={x:Q(1),y:Q(-1)}
for x in DONORS:target[raw[x+112]]={raw[x+112]:Q(1),raw[x]:Q(1)}

def replay(mutate=False):
    state={j:{j:Q(1)} for j in range(1880)};locations=dict(enumerate(word['initial']));counts=Counter();histogram=Counter();peak=0;owned=0;packets=[];mutated=False;non_dyadic=0
    for step,(instruction,mark) in enumerate(zip(program,marks)):
        x=instruction[:];op=x[0];a=x[1]
        if mutate and not mutated and mark=='raw_initial_gain_correction':x[3]='0';mutated=True
        counts[op]+=1
        if op=='INIT':
            require(a>=1880 and a not in state,'INIT ownership/freshness');require(a<1880+word['owned_fields'],'declared owned range');state[a]={};locations[a]=x[2];owned+=1;peak=max(peak,owned)
        elif op=='CLEAR':
            require(a>=1880 and a in state and frames[locations[a]]==frames[x[2]],'CLEAR ownership/chart');del state[a];del locations[a];owned-=1
        elif op=='MOVE':
            require(a in state and frames[locations[a]]==frames[x[2]],'MOVE source chart');require(bool(x[4])==(a>=1880),'MOVE owned flag');source,target_frame=frames[x[2]],frames[x[3]];require(source<=target_frame or (a>=1880 and target_frame<=source),'nested MOVE direction');rank=abs(len(native['frames'][x[2]])-len(native['frames'][x[3]]));require(rank>0,'positive MOVE rank');histogram[rank]+=1
            if mark=='new_rank1_debt_packet':
                require(a>=1880 and rank==1 and not native['frames'][x[3]],'new rank1 packet geometry');matches=[j for j in DONORS if state[a]=={raw[j]:Q(1),j:Q(-1)}];require(len(matches)==1,'actual q packet');packets.append(matches[0])
            locations[a]=x[3]
        elif op=='SCALE':
            require(a in state and frames[locations[a]]==frames[x[3]],'SCALE chart');q=Q(x[2]);require(q,'nonzero SCALE');state[a]={j:v*q for j,v in state[a].items()};non_dyadic+=(q.denominator&(q.denominator-1))!=0
        elif op in ('ADD','COPY'):
            b=x[2];require(a in state and b in state and a!=b,'ADD active/distinct');require(frames[locations[a]]==frames[locations[b]]==frames[x[4]],'ADD cochart');q=Q(x[3]);non_dyadic+=(q.denominator&(q.denominator-1))!=0
            if op=='COPY':require(a>=1880 and not state[a],'COPY zero owned destination')
            plus(state[a],state[b],q)
        else:raise ValueError(op)
    require(set(state)==set(range(1880)) and not owned,'all owned lifetimes closed');require(sorted(packets)==sorted(DONORS),'exact17 q packet set')
    for j in range(1480):require(frames[locations[j]]==frames[native['final'][j]],'common final chart')
    for j in mains:require(frames[locations[raw[j]]]==frames[native['final'][j]],'second final chart')
    wrong=[j for j in range(1880) if state[j]!=target[j]]
    if not mutate:require(not wrong,'full1880 endpoint rows')
    else:require(mutated and wrong,'gain-correction mutant must fail')
    return dict(operations=dict(sorted(counts.items())),move_histogram=dict(sorted(histogram.items())),peak_owned=peak,non_dyadic_scalar_operations=non_dyadic,wrong_rows=wrong,new_q_packets=packets)

normal=replay();mutant=replay(True)
bad=[dict(x) for x in reservations];bad[1]['source_event']=bad[0]['source_event'];rejected=False
try:check_reservations(bad)
except ValueError:rejected=True
require(rejected,'duplicate-reservation mutant')
out=dict(schema='independent-unit17-physical-word-review-v1',source_sha256=SOURCE,word_compressed_sha256=WORD,word_payload_sha256=hashlib.sha256(gzip.decompress(args.word.read_bytes())).hexdigest(),public_input_domain=1880,expected_complete_common_rows=1480,completed_second_shears=17,preserved_other_second_inputs=383,independent_source_main_map=True,common_word_events=71261,funded_raw_moves=len(expected_moves),physical_instruction_count=len(program),normal=normal,negative_controls=dict(dropped_one_raw_gain_correction_wrong_rows=mutant['wrong_rows'],duplicate_funded_reservation_rejected=rejected),status='PASS: independent full1880-input exact symbolic typed replay, lineage and negative controls.',scope='Partial restored native word;17 new rank1 calls. No complete supplier, no new kappa, no saving over direct17-channel delivery. Non-dyadic scalar admission and all programme foundations remain.')
args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
