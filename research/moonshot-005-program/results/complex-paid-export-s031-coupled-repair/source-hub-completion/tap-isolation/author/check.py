#!/usr/bin/env python3
"""Exact rational frozen-baseline gates. Uses SymPy only for small matrices."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json
R=Path(__file__).resolve().parents[4]
src=R/'complex-native-funded-donor-cuts/inputs/7833-construction.py'
spec=importlib.util.spec_from_file_location('native',src);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
g=S.compensated(S.load_word(src.with_name('DOUBLE-CANDIDATE.json.gz')),True)
D={86,89777,97232,97241,97320,97323,99064}
V=S.all_public_rows(g)
forms=g.forms.copy();forms.update({e:{} for e in D})
d=S.Literal(g.schedule,forms,g.routes,g.terminals,g.inputs,g.frames)
V0=S.all_public_rows(d)
A=[e for e in sorted(g.terminals)if g.terminals[e]!=127]
Y={~e for e,c in g.inputs.items()if c!=3}
def qr(V,e):
 den,row=V[e];return {j:Q(v,den)for j,v in row.items()}
def diff(e):
 r0=qr(V0,e);r=qr(V,e);return{j:r.get(j,Q(0))-r0.get(j,Q(0))for j in (r.keys()|r0.keys())&Y if r.get(j,Q(0))!=r0.get(j,Q(0))}
delta={e:diff(e)for e in A};delta={e:r for e,r in delta.items()if r}
J=sorted(set().union(*(r.keys()for r in delta.values())))
rank=S.IntegerElimination({j:i for i,j in enumerate(J)})
for r in delta.values():
 den=S.lcm(*(v.denominator for v in r.values()));rank.add({j:int(v*den)for j,v in r.items()})
cols={j:{e:str(r[j])for e,r in delta.items()if j in r}for j in J}
import sympy as sp
ends=sorted(g.terminals);I=[j for j in range(1289)if g.inputs[~j]==3];Y=sorted(Y);outside=[i for i,e in enumerate(ends)if g.terminals[e]!=127]
E=[qr(V,e)for e in ends]
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
 parts.append((js,ts))
Rinv=[{}for _ in range(1289)]
for js,ts in parts:
 if len(js)==1:Rinv[js[0]][ts[0]]=1/E[ts[0]][js[0]]
 else:
  a,b=js;i,k=ts;aa,ab,ba,bb=E[i].get(a,Q(0)),E[i].get(b,Q(0)),E[k].get(a,Q(0)),E[k].get(b,Q(0));det=aa*bb-ab*ba
  Rinv[a]={i:bb/det,k:-ab/det};Rinv[b]={i:-ba/det,k:aa/det}
D=sorted(D);pos={e:i for i,e in enumerate(D)};m=len(D)
vals={e:[Q(0)]*(m+1)for e in g.inputs}
for e in g.schedule:
 if e in pos:
  v=[Q(0)]*(m+1);v[pos[e]]=Q(1)
 else:v=[sum((q*vals[f][j]for f,q in g.forms[e].items()),Q(0))for j in range(m+1)]
 if e==94019:v[-1]+=1
 vals[e]=v
BB=sp.Matrix([[str(x)for x in vals[e]]for e in ends])
T=sp.zeros(1289,m+1)
for j,row in enumerate(Rinv):
 for i,q in row.items():T[j,:]+=sp.Rational(str(q))*BB[i,:]
TT=T[:,:m];hh=T[:,m:]
P=sp.Matrix([[str(qr(V,e).get(j,Q(0)))for j in range(1289)]for e in D])
Qall=sp.zeros(m,1289)
for j,row in enumerate(Rinv):
 for i,q in row.items():Qall[:,i]+=sp.Rational(str(q))*P[:,j]
TY=TT.extract(Y,list(range(m)));hY=hh.extract(Y,[0]);TI=TT.extract(I,list(range(m)));hI=hh.extract(I,[0]);PI=P.extract(list(range(m)),I)
K0=TY.row_join(-hY);ns=K0.nullspace();K=sp.Matrix.hstack(*ns)if ns else sp.zeros(m+1,0)
Z=(sp.eye(m)-PI*TI).row_join(PI*hI);G=Z*K
eligible=[i for i in outside if any(Rinv[j].get(i)for j in I)]
fixed=[i for i in outside if i not in eligible]
Gcols=G.columnspace();Gbase=sp.Matrix.hstack(*Gcols)if Gcols else sp.zeros(m,0)
lambda_basis=Gbase.T.nullspace();Lambda=sp.Matrix.vstack(*(z.T for z in lambda_basis))if lambda_basis else sp.zeros(0,m)
Qp=Qall.extract(list(range(m)),eligible);defect=Lambda*Qp
failed=[ends[j]for k,j in enumerate(eligible)if any(defect[:,k])]

# A literal paid-topology-preserving partial repair.
changed=[];source_changes=[];newforms={}
for e in g.schedule:
 if e in D:continue
 row={f:q for f,q in g.forms[e].items()if f not in D}
 if e!=155100 and 48 in row:changed.append({'slot':e,'removed_operand':48,'coefficient':str(row.pop(48))})
 if e in g.routes and g.routes[e][0]==3 and e!=48 and ~332 in row:source_changes.append({'slot':e,'removed_operand':~332,'coefficient':str(row.pop(~332))})
 newforms[e]=row
one=S.Literal([e for e in g.schedule if e not in D],newforms,{e:r for e,r in g.routes.items()if e not in D},g.terminals,g.inputs,g.frames)
V1=S.all_public_rows(one)
for e in ends:
 row=qr(V1,e);old=qr(V0,e);target=qr(V,e)
 assert row.get(332,Q(0))==target.get(332,Q(0))
 assert {j:v for j,v in row.items()if j!=332}=={j:v for j,v in old.items()if j!=332}
assert len(changed)==11 and len(source_changes)==6
assert len(one.routes)==len(g.routes)-7
assert g.forms[48]=={~332:Q(-3072)}and g.forms[155100]=={48:Q(-1,3072)}
P1=P.copy();P1[:,332]=sp.zeros(7,1)
assert TT[332,:]==sp.zeros(1,7)and hh[332,:]==sp.zeros(1,1)
Z1=(sp.eye(7)-P1.extract(list(range(7)),I)*TI).row_join(P1.extract(list(range(7)),I)*hI);assert Z1==Z
Q1=Qall.copy()
for j,q in Rinv[332].items():Q1[:,j]-=sp.Rational(str(q))*P[:,332]
defect1=Lambda*Q1.extract(list(range(7)),eligible)
failed=[ends[j]for k,j in enumerate(eligible)if any(defect1[:,k])]
pure=[j for j in eligible if not any(Rinv[k].get(j)for k in Y)]
assert len(pure)==272 and not any(Lambda*Q1.extract(list(range(7)),pure))
assert defect1.rank()==5 and len(failed)==102
J1=(sp.eye(7)-P1*TT).row_join(P1*hh)
assert J1.rank()==6
outside_unchanged=all(V1[e]==V0[e]for e in A);assert outside_unchanged
patch={'retired_paid_slots':D,'drop_operand_48':changed,'remove_source_input_332_coefficients':source_changes}
result={'status':'PASS_EXACT_SINGLE_INPUT_TAP_REPAIR','input_axis':332,'retained_export':48,'target_terminal':155100,'non_source_forms_changed':len(changed),'source_export_forms_changed':len(source_changes),'retired_paid_routes':7,'new_paid_routes':0,'complete_input_332_target_column_restored':True,'all_other_endpoint_columns_equal_frozen_D1':True,'all_outside_endpoint_rows_equal_frozen_D1':True,'source_control_rank':909,'pure_source_outside_gate_count':272,'pure_source_outside_failed_count':0,'remaining_pinned_quotient_rank':5,'remaining_pinned_failed_count':102,'remaining_pinned_failed_terminals':failed,'global_response_rank':1288,'full_target_restored':False,'new_kappa':False,'source_word_sha256':S.WORD}
out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True)
(out/'PATCH.json').write_text(json.dumps(patch,indent=2)+'\n');(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],'one exact input column repaired; 272 source-only gates pass; pinned quotient still5; no full target.')
