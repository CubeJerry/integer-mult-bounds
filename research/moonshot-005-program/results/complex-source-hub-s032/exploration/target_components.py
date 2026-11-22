from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import importlib.util,json,time
R=Path(__file__).resolve().parents[2]
src=R/'complex-native-funded-donor-cuts/inputs/7833-construction.py'
spec=importlib.util.spec_from_file_location('native',src);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
g=S.compensated(S.load_word(src.with_name('DOUBLE-CANDIDATE.json.gz')),True)
V=S.all_public_rows(g)
ends=sorted(g.terminals);E=[]
for e in ends:
 d,row=V[e];E.append({j:Q(v,d)for j,v in row.items()})
adj=[set()for _ in range(2578)]
for i,row in enumerate(E):
 for j in row:adj[j].add(1289+i);adj[1289+i].add(j)
seen=set();parts=[]
for start in range(2578):
 if start in seen:continue
 component={start};todo=[start];seen.add(start)
 while todo:
  for v in adj[todo.pop()]-seen:seen.add(v);component.add(v);todo.append(v)
 js=sorted(v for v in component if v<1289);ts=sorted(v-1289 for v in component if v>=1289)
 assert len(js)==len(ts) and len(js)in {1,2}
 if len(js)==2:
  det=E[ts[0]].get(js[0],0)*E[ts[1]].get(js[1],0)-E[ts[0]].get(js[1],0)*E[ts[1]].get(js[0],0);assert det
 parts.append(dict(inputs=js,outputs=[ends[i]for i in ts],input_charts=[g.inputs[~j]for j in js],output_charts=[g.terminals[ends[i]]for i in ts],matrix=[[str(E[i].get(j,0))for j in js]for i in ts]))
print('parts',Counter(len(x['inputs'])for x in parts))
pairs=[x for x in parts if len(x['inputs'])==2]
print('same external chart',sum(sorted(x['input_charts'])==sorted(x['output_charts'])for x in pairs))
print('samples',pairs[:6])
print('single locations',Counter((x['input_charts'][0]==3,x['output_charts'][0]==127,x['input_charts'][0]==x['output_charts'][0])for x in parts if len(x['inputs'])==1))
(Path(__file__).resolve().parent/'TARGET-COMPONENTS.json').write_text(json.dumps(parts,indent=2)+'\n')
