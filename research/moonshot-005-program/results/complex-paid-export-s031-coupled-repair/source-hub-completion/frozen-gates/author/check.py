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
print('small gate dims',{'rank_K0':K0.rank(),'nullity_K0':len(ns),'rank_G':G.rank(),'rank_C_exact':909-(len(ns)-G.rank()),'pinned_quotient_defect_rank':defect.rank(),'pinned_failed_count':len(failed),'failed_first':failed[:20]},flush=True)
witnesses=[]
for k,j in enumerate(eligible):
 for a in range(Lambda.rows):
  if defect[a,k]:witnesses.append({'terminal':ends[j],'output_coordinate':j,'annihilator':[str(v)for v in Lambda[a,:]],'payload_in_inverse_output_coordinate':[str(v)for v in Qall[:,j]],'nonzero_pairing':str(defect[a,k])});break
 if len(witnesses)>=3:break

# Exact source-only subgate and small rank certificates.
pure=[j for j in eligible if not any(Rinv[k].get(j)for k in Y)]
qpure=Qall.extract(list(range(m)),pure);puredef=Lambda*qpure
purefailed=[ends[j]for k,j in enumerate(pure)if any(puredef[:,k])]
assert len(pure)==272 and puredef.rank()==1 and purefailed==[155100]
assert Qall.extract(list(range(m)),fixed).rank()==0
assert K0.rank()==7 and len(ns)==1 and G.rank()==1
assert defect.rank()==5 and len(failed)==103
assert K[:,0]==sp.Matrix([0,0,0,0,sp.Rational(1,4),1,0,0])
assert G[:,0]==sp.Matrix([0,0,0,0,sp.Rational(1,4),0,0])
minor_k_rows=list(K0.T.rref()[1]);minor_k_cols=list(K0.extract(minor_k_rows,list(range(8))).rref()[1]);minor_k=K0.extract(minor_k_rows,minor_k_cols)
minor_d_cols=list(defect.rref()[1]);minor_d_rows=list(defect.extract(list(range(defect.rows)),minor_d_cols).T.rref()[1]);minor_d=defect.extract(minor_d_rows,minor_d_cols)
factor={}
for j in J:
 aa=2*delta[154885].get(j,Q(0));bb=2*delta[154880].get(j,Q(0))-aa
 factor[j]=[str(aa),str(bb)]
 for e,row in delta.items():assert row.get(j,Q(0))==row.get(0,Q(0))*aa+row.get(4,Q(0))*bb
assert len(J)==73 and len(delta)==75 and 29 in J and 691 not in J
assert sp.Matrix([[str(delta[e].get(j,Q(0)))for j in [0,4]]for e in [154880,154885]]).det()==-sp.Rational(1,4)
# Every other target column is unchanged outside; all affected columns are retained explicitly.
changed_ancestors=set(delta)
for e in reversed(g.schedule):
 if e in changed_ancestors:changed_ancestors.update(f for f in g.forms[e]if f>=0)
protected=set(A)-set(delta)
for e in reversed(g.schedule):
 if e in protected:protected.update(f for f in g.forms[e]if f>=0)
def matrix(M):return [[str(v)for v in M.row(i)]for i in range(M.rows)]
result={
 'status':'PASS_EXACT_FROZEN_SOURCE_GATES',
 'scope':'Frozen D1 non-source forms; neither proposed second new route is installed. Free existing source-3 exports and an arbitrary final chart-127 decoder are allowed. No endpoint-pair exclusion or positive supplier.',
 'deleted':D,'source_word_sha256':S.WORD,
 'outside_external_defect':{'rank':len(rank.rows),'affected_input_axes':J,'input_charts':{str(j):g.inputs[~j]for j in J},'affected_terminal_slots':sorted(delta),'column_basis_axes':[0,4],'column_basis':{str(j):cols[j]for j in [0,4]},'column_coefficients':factor,'rank_two_minor':{'terminal_rows':[154880,154885],'input_columns':[0,4],'determinant':'-1/4'},'affected_external_columns_outside_chart27':sorted(set(J)-{29,691}),'changed_terminal_ancestor_slots':sorted(changed_ancestors),'unchanged_terminal_ancestor_slots':sorted(protected)},
 'pinned_gate':{'rank_K0':K0.rank(),'kernel_K0':matrix(K),'rank_K0_minor':{'external_input_rows':[Y[i]for i in minor_k_rows],'control_columns':minor_k_cols,'matrix':matrix(minor_k),'determinant':str(minor_k.det())},'Z':matrix(Z),'G':matrix(G),'rank_G':G.rank(),'rank_C_exact':909-(len(ns)-G.rank()),'quotient_annihilator':matrix(Lambda),'quotient_rank':defect.rank(),'quotient_rank_minor':{'annihilator_rows':minor_d_rows,'outside_terminals':[ends[eligible[j]]for j in minor_d_cols],'matrix':matrix(minor_d),'determinant':str(minor_d.det())},'quotient_left_kernel':[matrix(v)for v in defect.T.nullspace()],'failed_terminals':failed,'failed_count':len(failed),'first_witnesses':witnesses,'pure_source_only_outside_count':len(pure),'pure_source_only_quotient_rank':puredef.rank(),'pure_source_only_failed_terminals':purefailed,'fixed_outside_deleted_payload_rank':0},
 'complete_supplier_constructed':False,'new_kappa':False}
out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],'external rank 2 on 73 columns; pinned quotient rank 5 with 103 failed memberships; pure-source-only quotient rank 1.')
