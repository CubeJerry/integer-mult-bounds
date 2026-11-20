#!/usr/bin/env python3
"""Exact source interface for the conditional hub-completion criterion."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import importlib.util,json,hashlib
RESULTS=Path(__file__).resolve().parents[3]
source=RESULTS/'complex-native-funded-donor-cuts/inputs/7833-construction.py'
spec=importlib.util.spec_from_file_location('native_source',source)
S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
w=S.load_word(source.with_name('DOUBLE-CANDIDATE.json.gz'));g=S.compensated(w,True)
V=S.all_public_rows(g);W=S.all_public_rows(w);ends=sorted(g.terminals)
def row(e):
 d,r=V[e];return {j:Q(v,d)for j,v in r.items()}
assert all(V[e]==W[e]for e in ends)
E=[row(e)for e in ends]
# Exact bipartite endpoint components.
adj=[set()for _ in range(2578)]
for i,r in enumerate(E):
 for j in r:adj[j].add(1289+i);adj[1289+i].add(j)
seen=set();parts=[];R={j:{}for j in range(1289)}
for start in range(2578):
 if start in seen:continue
 A={start};todo=[start];seen.add(start)
 while todo:
  for v in adj[todo.pop()]-seen:seen.add(v);A.add(v);todo.append(v)
 J=sorted(v for v in A if v<1289);T=sorted(v-1289 for v in A if v>=1289)
 assert len(J)==len(T) and len(J)in {1,2}
 if len(J)==1:
  R[J[0]][T[0]]=1/E[T[0]][J[0]]
 else:
  a,b=E[T[0]].get(J[0],Q(0)),E[T[0]].get(J[1],Q(0));c,d=E[T[1]].get(J[0],Q(0)),E[T[1]].get(J[1],Q(0));det=a*d-b*c;assert det
  R[J[0]].update({T[0]:d/det,T[1]:-b/det});R[J[1]].update({T[0]:-c/det,T[1]:a/det})
 parts.append([J,T])
assert Counter((len(j),len(t))for j,t in parts)=={(1,1):889,(2,2):200}
I=[j for j in range(1289)if g.inputs[~j]==3];Y=[j for j in range(1289)if g.inputs[~j]!=3]
A=[i for i,e in enumerate(ends)if g.terminals[e]!=127];B=[i for i,e in enumerate(ends)if g.terminals[e]==127]
assert (len(I),len(Y),len(A),len(B))==(908,381,387,902)
types=Counter((len(js),sum(j in I for j in js),sum(t in A for t in ts))for js,ts in parts)
assert types=={(2,1,1):200,(1,1,0):532,(1,1,1):176,(1,0,0):170,(1,0,1):11}
for i,erow in enumerate(E):
 product={}
 for j,c in erow.items():
  for k,v in R[j].items():product[k]=product.get(k,Q(0))+c*v
 assert {k:v for k,v in product.items()if v}=={i:Q(1)}

assert all(a!=127 for a,b in g.routes.values()) and not any(b==3 for a,b in g.routes.values())
eligible=[];fixed=[]
for t in A:
 support=[j for j in I if R[j].get(t)]
 assert len(support)<=1
 if support:eligible.append({'outside_coordinate':t,'terminal':ends[t],'input_axis':support[0],'inverse_coefficient':str(R[support[0]][t])})
 else:fixed.append({'outside_coordinate':t,'terminal':ends[t]})
assert len(eligible)==376 and len(fixed)==11 and len({z['input_axis']for z in eligible})==376
free=sorted(set(I)-{z['input_axis']for z in eligible});free_inside=[]
for j in free:
 assert len(R[j])==1
 t=next(iter(R[j]));assert t in B
 assert all(not E[i].get(j)for i in A)
 free_inside.append({'input_axis':j,'inside_coordinate':t,'terminal':ends[t],'inverse_coefficient':str(R[j][t])})
assert len(free)==532 and len({z['inside_coordinate']for z in free_inside})==532
fixed_inside=sorted(set(B)-{z['inside_coordinate']for z in free_inside});assert len(fixed_inside)==370
old=[e for e,(a,b)in w.routes.items()if a==3];new=[e for e,(a,b)in g.routes.items()if a==3]
assert sum(c==3 for c in w.inputs.values())==908 and not any(b==3 for a,b in w.routes.values()) and not any(c==3 for c in w.terminals.values())
assert len(old)==908 and len(new)==909 and all(f<0 for e in old for f in w.forms[e])
permutation={e:e for e in new if e!=94019};permutation[90369]=94019;permutation[156057]=90369
assert set(permutation.values())==set(old)
assert all(g.forms[e]==w.forms[permutation[e]]for e in permutation)
assert len([e for e,(a,b)in g.routes.items()if b==127])==902
result={'status':'PASS_EXACT_SOURCE_HUB_COMPLETION_INTERFACE','complete_supplier_constructed':False,'scope':'Source block pattern and an exact conditional linear-algebra completion criterion; no candidate code is certified.','input_chart_3_axes':I,'other_input_axes':Y,'outside_127_terminal_slots':[ends[i]for i in A],'chart_127_terminal_slots':[ends[i]for i in B],'outside_coordinates_with_one_chart_3_input':eligible,'outside_coordinates_without_chart_3_input':fixed,'free_chart_3_singleton_columns':free_inside,'fixed_inside_coordinates':fixed_inside,'control_basis':{'original_source_3_payload_columns':908,'additional_channel':94019,'additional_scale':'1/845660160','rank_argument':'Removing row 94019 leaves the original 908 source-3 sends with their payloads permuted; full endpoint invertibility forces their input matrix invertible.'},'source_word_sha256':S.WORD}
out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status']);print('Source inputs 908 + 381; outputs 387 + 902; pinned/free own-input columns 376 + 532; fixed inside columns 370.')
