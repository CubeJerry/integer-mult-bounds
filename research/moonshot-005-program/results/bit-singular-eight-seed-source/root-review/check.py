#!/usr/bin/env python3
"""Independent seed reconstruction, source-cut audit and literal word replay."""
import argparse,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--seed',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--funnel-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
sys.path.insert(0,str(a.funnel_review));from check import rank,rr,replay
from budget import budget,combine,moment
d=json.loads(a.seed.read_text());raw=(a.repo/d['native_source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['native_source_sha256'];R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(i*j for i,j in zip(x,y))
B=[[int(i!=j and dot(R[i],R[j])!=0) for j in range(111)] for i in range(111)]
frame=d['binary_frame'];G=[sum(B[i][j]<<k for k,j in enumerate(frame)) for i in frame];labels=[]
polar_mask=0
assert d['singular_label']==38 and d['h_coordinate_mask']==189
for i,g in enumerate(G):
 if 38>>i&1:polar_mask^=g
assert polar_mask==189
for j in range(111):
 b=[B[i][j] for i in frame];solutions=[x for x in range(256) if all(((g&x).bit_count()%2)==z for g,z in zip(G,b))];assert len(solutions)==1;labels.append(solutions[0])
h=[(x&189).bit_count()%2 for x in labels];assert h==d['h_values'] and h.count(0)==52
K=[sum((1^z)<<j for j,z in enumerate(row)) for row in B]
W=[row&sum(1<<j for j in range(111) if h[j]==h[i]) for i,row in enumerate(K)]
assert rank(W)==15
for i,row in enumerate(W):
 assert row>>i&1
 assert all(not(row>>j&1) for j in range(111) if B[i][j])
S=[int(x,16) for x in d['seed_rows']];T=d['targets']
assert rank(S)==rank([W[i] for i in T])==rank(S+[W[i] for i in T])==8
L=[]
for e in d['proper_completion_rows']:
 row=int(e['row_hex'],16);ids=[j for j in range(111) if row>>j&1];normal=e['normal']
 assert ids==e['support'] and any(normal) and len(rr([R[j] for j in ids]))==7
 assert all(dot(normal,R[j])==0 for j in ids) and rank(W+[row])==15
 L.append(row)
assert rank(S+L)==rank(S+L+W)==15
for j in range(7):assert rank(S+L[:j]+L[j+1:])==14
span={0:0}
for j,row in enumerate(S+L):span.update({x^row:c|(1<<j) for x,c in list(span.items())})
assert len(span)==32768 and all(row in span for row in W)
wraw=a.word.read_bytes();w=json.loads(wraw);literal=replay(w,R,False);literal['budget']=budget(literal['movement_profile'])
assert w['targets']==T and set(w['point_targets']).isdisjoint(w['active_targets'])
vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j) for j in range(111)}
loc={f'X{j}':f'L{j}' for j in range(111)}|{f'Y{j}':'zero' for j in range(111)};cut={}
for step,o in enumerate(w['operations'],1):
 op,n,*rest=o
 if op=='INIT':vals[n]=0;loc[n]=rest[0]
 elif op=='ADD':vals[rest[0]]^=vals[n]
 elif op=='MOVE':loc[n]=rest[0]
 elif op=='CLEAR':del vals[n];del loc[n]
 if step in [w['milestones']['source_cut'],w['milestones']['seed8_before_Y']]:
  rows=[v for n,v in vals.items() if loc[n]!='Hub' and not n.startswith('Y')]
  assert all(vals[f'Y{j}']==1<<(111+j) for j in range(111))
  cut[str(step)]={'available_rank':rank(rows),'W_intersection':rank(rows)+15-rank(rows+W)}
  if step==w['milestones']['seed8_before_Y']:
   P=[vals[f'P{i}'] for i in range(8)];assert rank(P)==rank(P+S)==8
assert list(cut.values())==[{'available_rank':17,'W_intersection':0},{'available_rank':25,'W_intersection':8}]
control={1:12,7:222,8:8};gain=moment(combine((1,control),(-1,literal['movement_profile'])));assert gain[0]>0
out={'status':'PASS_ROOT_SINGULAR_EIGHT_SEED_SOURCE','source_sha256':d['native_source_sha256'],'seed_sha256':hashlib.sha256(a.seed.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(wraw).hexdigest(),'h_classes':[52,59],'seed_rank':8,'fitting_rank':15,'proper_complement_rank':7,'proper_row_omission_controls':7,'all111_fitting_decompositions':[span[x] for x in W],'literal':literal,'source_cuts':cut,'same_seed_point_control':budget(control),'same_seed_gain_interval':[str(v) for v in gain],'remaining_W_directions':7,'remaining_Y_endpoints':99,'new_complete_kappa':False}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'word':out['word_sha256'],'cuts':cut,'counts':literal['counts'],'first_even_m':literal['budget']['first_positive_even_m']}))
