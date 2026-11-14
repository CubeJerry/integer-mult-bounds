from pathlib import Path
from fractions import Fraction
from collections import deque,Counter
from math import lcm
import json,numpy as np

p=Path(__file__).resolve().parent
s=json.loads((p/'SPECTRAL-SCREEN.json').read_text())
patterns=[tuple(x['bits'])for x in s['results']]
origin=(0,)*8;distance={origin:0};previous={};todo=deque([origin])
while todo:
    a=todo.popleft()
    for i,b in enumerate(patterns):
        c=tuple((x+y)%4 for x,y in zip(a,b))
        if c not in distance:distance[c]=distance[a]+1;previous[c]=(a,i);todo.append(c)
R=np.array([[int(2*Fraction(x))for x in row]for row in s['R0']],dtype=object)
I=np.eye(8,dtype=object);Z=np.zeros((8,8),dtype=object)
phases=[(1,0),(0,1),(-1,0),(0,-1)]
results=[];maxden=0
for t,bits in enumerate(sorted(distance)):
    ar=np.array([phases[z][0]for z in bits],dtype=object)[:,None]*R
    ai=np.array([phases[z][1]for z in bits],dtype=object)[:,None]*R
    br=I.copy();bi=Z.copy();d=0;found=None
    for k in range(1,241):
        br,bi=br@ar-bi@ai,br@ai+bi@ar;d+=1
        while d>0 and all(x%2==0 for x in br.flat)and all(x%2==0 for x in bi.flat):br//=2;bi//=2;d-=1
        maxden=max(maxden,d)
        if np.array_equal(br,I*(2**d))and not any(bi.flat):found=k;break
    results.append({'phase':list(bits),'minimum_width':distance[bits],'order_through240':found})
    if t%256==0:print('checked',t,'of',len(distance),flush=True)
orders=Counter(x['order_through240']for x in results)
if None in orders:period=None
else:period=lcm(*orders)
out={'status':'EXACT_ADDITIVE_CHARACTER_CLOSURE_SCREEN','class_ports':s['class_ports'],'labels':s['labels'],'additive_phase_count':len(distance),'minimum_width_histogram':dict(Counter(distance.values())),'max_matrix_denominator_power':maxden,'order_histogram':dict(orders),'common_period_if_all_orders_found':period,'results':results,'scope':'Normalized scalar-port matrix diag(i^phase)R0 only. Additive phases cover every width for this fixed class. Actual stage adapters and ordinary realizability remain separate.'}
(p/'PHASE-CLOSURE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='results'}))
