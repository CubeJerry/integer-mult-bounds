"""Controlled real quotient edits preserving four receiver cuts and H cores."""
from pathlib import Path
import importlib.util,gzip,json,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';prev=base/'bit-simultaneous-d1509-s032';here=Path(__file__).parent
s=importlib.util.spec_from_file_location('s032sg',prev/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
g,a,ff,Ks,C=m.common_data(repo);gg=m.ex.read(prev/'output/CONSTRAINED-GAUGES.json.gz');L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];target=95
fib=m.ex.read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz')
records={}
for j in [61]:
 G=np.array(gg['gauges'][str(j)],dtype=np.uint8);U=a.mm(g.inverse(G,a),ff[j][target]);N=m.null(np.hstack([L,U]),g,a);K=a.mm(U,N[32:]);assert K.shape==(96,4)and a.rank(K)==4
 KH=m.basis(np.hstack([Ks[h]for h in Ks if j in a.planes[h]]),g,a);rows=[]
 for h in a.by_donor[j]:
  if not a.planes[h]<=a.adj[target]:continue
  visible=[r for r in R if a.planes[h]<=a.adj[r]]
  constraints=[]
  for center,rr in fib.items():
   if j not in a.planes[int(center)]:continue
   for receiver,z in rr.items():
    if int(center)!=h and not a.planes[h]<=a.adj[int(receiver)]:continue
    K0=np.array(z['kernel'],dtype=np.uint8)[:48,:3];Z0=np.zeros_like(K0);constraints.append(np.block([[K0,Z0],[Z0,K0]]))
  B=m.basis(np.hstack(constraints+[L[:,8*R.index(r):8*R.index(r)+8]for r in visible]),g,a)
  ann=m.null(B.T,g,a).T;rank=a.rank(a.mm(ann,K))
  rows.append({'H':h,'inside_D':a.planes[h]<=a.charts[1509],'old_receivers_seeing_H':visible,'fixed_span_rank':B.shape[1],'allowed_collision_rank':rank})
 records[j]={'old_collision_rank':4,'collision':K.tolist(),'H_core':KH.tolist(),'quotients':rows};print('DONOR',j,[(z['H'],z['old_receivers_seeing_H'],z['allowed_collision_rank'])for z in rows],flush=True)
here.mkdir(parents=True,exist_ok=True);(here/'LOCAL-VISIBILITY-95.json').write_text(json.dumps(records,sort_keys=True,indent=2)+'\n')
