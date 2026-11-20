#!/usr/bin/env python3
"""Independent actual-owner reconstruction and packed-binary compiler review."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import gzip, hashlib, importlib.util, json
import numpy as np

def need(ok,why):
    if not ok: raise ValueError(why)

def read(path): return json.loads(gzip.decompress(path.read_bytes()))

def binary_rank(rows):
    pivots={}
    for value in rows:
        while value:
            p=value.bit_length()-1
            if p in pivots: value^=pivots[p]
            else: pivots[p]=value; break
    return len(pivots)

ap=ArgumentParser(); ap.add_argument('--repo',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args(); here=Path(__file__).resolve().parent; base=args.repo/'research/moonshot-005-program/results'
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
spec=importlib.util.spec_from_file_location('independent_gf64',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
literal=read(here.parent/'author/output/COEFFICIENTS.json.gz'); early=read(here.parent/'author/output/EARLY.json.gz'); compiler=read(here.parent/'author/output/COMPILER.json.gz')
H,donors=642,[45,61,100]; layout=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
ports=sorted(d for d,C in enumerate(layout['D4']) if set(layout['A2'][H])<=set(C))
need(literal['H']==H and literal['donors']==donors and literal['ports']==ports and len(ports)==45,'actual full local port set')
P=np.array(literal['word'],dtype=np.uint8); need(P.shape==(45,45) and g.rank(P)==44,'full-width signal rank')
rows=[]; owners={j:{} for j in donors}
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
    phase,j,x,h,d,_,source,_=json.loads(line)
    if phase=='X' and j in donors:
        need(source==j,'initial owner equals source'); owners[j].setdefault(h,[]).append(int(x))
        if h==H: rows.append((j,int(x),d))
inputs=[(j,x) for j in donors for x in sorted(owners[j][H])]
need(len(inputs)==len(set(inputs))==90 and Counter(j for j,x in inputs)=={45:30,61:30,100:30},'ninety distinct real H input owners')
need([list(x) for x in inputs]==literal['physical_owner_inputs'],'input labels match raw routes')
index={owner:i for i,owner in enumerate(inputs)}; actual=np.zeros((90,90),dtype=np.uint8); labels=[]
for d in ports:
    exits=sorted((j,x) for j,x,p in rows if p==d); need(len(exits)==2,'two actual output owners at every D')
    for half,owner in enumerate(exits):
        labels.append({'owner':list(owner),'D':d,'copy':half})
        for s in range(3): actual[index[owner],30*s+15*half:30*s+15*half+15]=P[ports.index(d),15*s:15*s+15]
need(labels==literal['physical_owner_outputs'] and np.array_equal(actual,np.array(literal['physical_word'],dtype=np.uint8)),'provider rows tied to actual unchanged output routes')
need(g.rank(actual)==88,'both half-providers retained')
for j in donors:
    need(sorted(x for xs in owners[j].values() for x in xs)==list(range(480)),'every source coordinate owned exactly once')
    saved=early['full'][str(j)]; E=np.array(saved['matrix'],dtype=np.uint8); row_labels=[tuple(x) for x in saved['row_owners']]
    need(E.shape==(480,480) and len(row_labels)==len(set(row_labels))==480,'full early basis with distinct labels')
    need(set(row_labels)=={(h,x) for h,xs in owners[j].items() for x in xs},'all early rows have actual owners')
    Q=np.array(literal['source_maps'][str(j)][str(H)],dtype=np.uint8); need(Q.shape==(15,240),'full logical H source quotient')
    for t,x in enumerate(sorted(owners[j][H])):
        expected=np.zeros(480,dtype=np.uint8); expected[240*(t//15):240*(t//15+1)]=Q[t%15]
        need(np.array_equal(E[row_labels.index((H,x))],expected),'actual input carries the specified half-quotient row')
paid=np.zeros((2,90),dtype=np.uint8); paid[0,0]=paid[1,15]=1
need(np.array_equal(paid,np.array(literal['physical_complements'],dtype=np.uint8)),'two real complement coordinates')
A=np.vstack([actual,paid]); T=np.array(literal['physical_extension'],dtype=np.uint8); inverse=np.array(literal['physical_extension_inverse'],dtype=np.uint8)
need(g.rank(A)==90 and T.shape==(92,92) and np.array_equal(T[:,:90],A),'square extension adds two initialized fields')
need(np.array_equal(g.mm(T,inverse),np.eye(92,dtype=np.uint8)),'full field inverse')
need(np.array_equal(g.mm(inverse,A),np.vstack([np.eye(90,dtype=np.uint8),np.zeros((2,90),dtype=np.uint8)])),'all actual originals restored and new owners zeroed')
need(g.rank(A[:-1])==89,'deleting one complement field loses information')
# Packed integer rows independently test the full552-variable transformation.
binary=[]
for r in range(92):
    for bit in range(6):
        value=0
        for s in range(92):
            for k in range(6):
                if int(g.M[T[r,s],1<<k])>>bit&1: value^=1<<(6*s+k)
        binary.append(value)
operations=compiler['binary_elimination_ADDs']; need(compiler['dimension']==552 and len(operations)==13582,'literal ADD count')
state=[1<<i for i in range(552)]
for target,source in reversed(operations):
    need(isinstance(target,int) and isinstance(source,int) and 0<=target<552 and 0<=source<552 and target!=source,'distinct actual ADD owners'); state[target]^=state[source]
need(state==binary,'complete forward word on every original and auxiliary input')
for target,source in operations: state[target]^=state[source]
need(state==[1<<i for i in range(552)],'complete inverse word')
mask=(1<<540)-1; signals=[r&mask for r in binary[:540]]; complements=[r&mask for r in binary[540:]]
need(binary_rank(signals)==528 and binary_rank(signals+complements)==540,'twelve real binary complement coordinates')
need(binary_rank(signals+complements[:-1])==539 and binary_rank(signals+complements[:6])==534,'deleted bit and field controls')
result={'status':'PASS_ROOT_FULL45_ACTUAL_OWNER_COMPILER','H':H,'ports':45,'actual_two_half_owners':90,'provider_rank':88,'extra_fields_per_lane':2,'field_extension_dimension':92,'binary_word_dimension':552,'ADD_per_direction':13582,'eight_lane_forward_inverse_ADD':217312,'physical_H_fields':720,'physical_signal_rank':704,'paid_field_exports':16,'binary_INIT_MOVE_CLEAR_each':96,'paid_MOVE_gap':6,'free_owner_permutation_used':False,'complete_field_and_binary_inverse_verified':True,'source_readout_review_is_separate':True,'full_global_invoice':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True); (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],90,88,92,13582,217312,16,flush=True)
