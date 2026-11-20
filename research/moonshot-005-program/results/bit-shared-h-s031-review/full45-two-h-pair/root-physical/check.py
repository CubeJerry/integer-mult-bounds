#!/usr/bin/env python3
"""Independent joint owner binding and both full binary H words."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,why):
    if not ok: raise ValueError(why)

def read(path): return json.loads(gzip.decompress(path.read_bytes()))

def binary_rank(rows):
    pivots={}
    for value in rows:
        while value:
            p=value.bit_length()-1
            if p in pivots:value^=pivots[p]
            else:pivots[p]=value;break
    return len(pivots)

ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args();here=Path(__file__).resolve().parent;base=args.repo/'research/moonshot-005-program/results'
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
spec=importlib.util.spec_from_file_location('s030_independent',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
literal=read(here.parent/'author/output/COEFFICIENTS.json.gz');early=read(here.parent/'author/output/EARLY.json.gz');compiler=read(here.parent/'author/output/COMPILER.json.gz')
layout=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');donors=[0,45,61,62,100];owners={j:{} for j in donors};raw_H={263:[],642:[]}
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
    phase,j,x,h,d,_,source,_=json.loads(line)
    if phase=='X' and j in donors:
        need(source==j,'genuine original source');owners[j].setdefault(h,[]).append(int(x))
        if h in raw_H:raw_H[h].append((j,int(x),d))
for j in donors:
    need(sorted(x for xs in owners[j].values() for x in xs)==list(range(480)),'complete actual source-owner partition')
    saved=early['full'][str(j)];labels=[tuple(x) for x in saved['row_owners']]
    need(len(labels)==len(set(labels))==480 and set(labels)=={(h,x) for h,xs in owners[j].items() for x in xs},'one genuine early basis per donor')
all_inputs={};receipts=[]
for h,wanted_rank,wanted_ADD in [(263,90,47210),(642,88,47135)]:
    data=literal['H'][str(h)];ph=data['physical'];js=sorted(layout['A2'][h]);ports=sorted(d for d,C in enumerate(layout['D4']) if set(js)<=set(C))
    need(data['donors']==js and data['ports']==ports and len(ports)==45,'actual full H interface')
    P=np.array(data['word'],dtype=np.uint8);need(P.shape==(45,45) and g.rank(P)*2==wanted_rank,'logical provider rank')
    inputs=[(j,x) for j in js for x in sorted(owners[j][h])];all_inputs[h]=set(inputs)
    need(len(inputs)==len(set(inputs))==90 and Counter(j for j,x in inputs)==dict.fromkeys(js,30),'ninety real input owners')
    need([list(x) for x in inputs]==ph['input_owners'],'literal input owners')
    index={owner:i for i,owner in enumerate(inputs)};actual=np.zeros((90,90),dtype=np.uint8);outputs=[]
    for d in ports:
        pair=sorted((j,x) for j,x,p in raw_H[h] if p==d);need(len(pair)==2,'actual output pair at each D')
        for half,owner in enumerate(pair):
            outputs.append({'owner':list(owner),'D':d,'copy':half})
            for s in range(3):actual[index[owner],30*s+15*half:30*s+15*half+15]=P[ports.index(d),15*s:15*s+15]
    need(outputs==ph['output_owners'] and np.array_equal(actual,np.array(ph['word'],dtype=np.uint8)) and g.rank(actual)==wanted_rank,'complete actual row assignment and physical rank')
    for j in js:
        saved=early['full'][str(j)];E=np.array(saved['matrix'],dtype=np.uint8);row_labels=[tuple(x) for x in saved['row_owners']];Q=np.array(literal['source_maps'][str(j)][str(h)],dtype=np.uint8)
        need(E.shape==(480,480) and Q.shape==(15,240),'full source and early dimensions')
        for t,x in enumerate(sorted(owners[j][h])):
            expected=np.zeros(480,dtype=np.uint8);expected[240*(t//15):240*(t//15+1)]=Q[t%15]
            need(np.array_equal(E[row_labels.index((h,x))],expected),'same donor basis supplies the actual H inputs')
    d=90-wanted_rank;paid=np.array(ph['complements'],dtype=np.uint8).reshape(d,90);A=np.vstack([actual,paid])
    T=np.array(ph['extension'],dtype=np.uint8);inverse=np.array(ph['extension_inverse'],dtype=np.uint8);n=90+d;bits=6*n
    need(T.shape==(n,n) and np.array_equal(T[:,:90],A) and g.rank(A)==90,'rank-restoring owned extension')
    need(np.array_equal(g.mm(T,inverse),np.eye(n,dtype=np.uint8)) and np.array_equal(g.mm(inverse,A),np.vstack([np.eye(90,dtype=np.uint8),np.zeros((d,90),dtype=np.uint8)])),'every original restored and auxiliary zeroed')
    binary=[]
    for r in range(n):
        for bit in range(6):
            value=0
            for s in range(n):
                for k in range(6):
                    if int(g.M[T[r,s],1<<k])>>bit&1:value^=1<<(6*s+k)
            binary.append(value)
    operations=compiler[str(h)]['binary_elimination_ADDs'];need(compiler[str(h)]['dimension']==bits and len(operations)==wanted_ADD,'literal full binary word count')
    state=[1<<i for i in range(bits)]
    for target,source in reversed(operations):
        need(isinstance(target,int) and isinstance(source,int) and 0<=target<bits and 0<=source<bits and target!=source,'distinct actual binary ADD owners');state[target]^=state[source]
    need(state==binary,'complete symbolic forward word on all variables')
    for target,source in operations:state[target]^=state[source]
    need(state==[1<<i for i in range(bits)],'complete symbolic inverse word')
    mask=(1<<540)-1;signals=[r&mask for r in binary[:540]];extra=[r&mask for r in binary[540:]]
    need(binary_rank(signals)==6*wanted_rank and binary_rank(signals+extra)==540,'retained signals and full input information')
    if d:need(g.rank(A[:-1])==89 and binary_rank(signals+extra[:-1])==539,'deleted field and bit controls')
    receipts.append({'H':h,'owners':90,'signal_rank':wanted_rank,'extra_fields_per_lane':d,'binary_dimension':bits,'ADD_per_direction':wanted_ADD,'eight_lane_forward_inverse_ADD':16*wanted_ADD,'eight_lane_extra_field_exports':8*d})
need(not all_inputs[263]&all_inputs[642],'shared donor61 supplies disjoint actual owner sets to the two H maps')
need({j for j,x in all_inputs[263]}&{j for j,x in all_inputs[642]}=={61},'exact shared source identity')
need(sum(x['eight_lane_forward_inverse_ADD'] for x in receipts)==1509520 and sum(x['eight_lane_extra_field_exports'] for x in receipts)==16,'complete pair local replacement totals')
result={'status':'PASS_ROOT_FULL45_PAIR_OWNER_WORDS','centres':receipts,'single_shared_source_basis':True,'disjoint_original_H_owners':180,'pair_ADD_total':1509520,'paid_field_exports':16,'binary_INIT_MOVE_CLEAR_each':96,'paid_MOVE_gap':6,'free_owner_permutation_used':False,'later_stationary_caches_not_assumed_to_factor_through_lossy_outputs':True,'complete_source_review_separate':True,'complete_global_invoice':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],47210,47135,1509520,16,flush=True)
