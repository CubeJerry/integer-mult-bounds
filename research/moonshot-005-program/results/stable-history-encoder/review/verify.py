#!/usr/bin/env python3
"""Independent source-row recovery and receiver-endpoint containment."""
import argparse, gzip, hashlib, json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(a,m):
 if not a: raise ValueError(m)
def add(a,b,c=Q(1)):
 for j,x in b.items():
  v=a.get(j,Q(0))+c*x
  if v:a[j]=v
  else:a.pop(j,None)
def span(a):
 s={0}
 for x in a:s.update(x^v for v in tuple(s))
 return frozenset(s)
def basis(rows):
 out={}
 for row in rows:
  z=row.copy()
  while z:
   p=max(z)
   if p not in out:
    c=z[p];out[p]={j:v/c for j,v in z.items()};break
   add(z,out[p],-z[p])
 return out
def reduce(row,b):
 z=row.copy()
 for p in sorted(b,reverse=True):
  if p in z:add(z,b[p],-z[p])
 return z
def intersection(rows,b):
 rb={};out=[]
 for row in basis(rows).values():
  z=reduce(row,b);x=row.copy()
  while z:
   p=max(z)
   if p not in rb:
    c=z[p];rb[p]=({j:v/c for j,v in z.items()},{j:v/c for j,v in x.items()});break
   zz,xx=rb[p];c=-z[p];add(z,zz,c);add(x,xx,c)
  if not z and x:out.append(x)
 return list(basis(out).values())
def serial(rows):return [{str(j):str(x) for j,x in sorted(row.items())} for row in rows]
def stable_lift(w,C,R,keys):
 lookup={tuple(k):i for i,k in enumerate(keys)};loc=dict(enumerate(w['initial']));lift={j:{lookup[-1,j]:Q(1)} for j,f in loc.items() if C[f] in R}
 for k,e in enumerate(w['program']):
  op,j=e[:2]
  if op=='INIT':
   loc[j]=e[2]
   if C[loc[j]] in R:lift[j]={}
  elif op=='CLEAR':loc.pop(j);lift.pop(j,None)
  elif op=='ADD':
   if C[loc[j]] in R:add(lift[j],lift[e[2]],Q(e[3]))
  elif op=='COPY':
   if C[loc[j]] in R:lift[j]={i:Q(e[3])*v for i,v in lift[e[2]].items()}
  elif op=='SCALE':
   if C[loc[j]] in R:lift[j]={i:Q(e[2])*v for i,v in lift[j].items()}
  elif op=='MOVE':
   loc[j]=e[3]
   if C[loc[j]] in R:lift[j]={lookup[k,j]:Q(1)}
   else:lift.pop(j,None)
 z=lift[189].copy();add(z,{lookup[-1,189]:Q(1)},Q(-1));return z
def run(source,output):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin');w=json.loads(gzip.decompress(raw));P=w['program'];n=w['public'];C=list(map(span,w['frames']));T=C[127];R={C[w['initial'][189]]}|{C[e[3]] for e in P if e[0]=='MOVE' and e[1]==189};need(len(R)==4,'receiver four chart spaces');rows={j:{j:Q(1)} for j in range(n)};loc=dict(enumerate(w['initial']));history=[];initial=[];keys=[];E=None;eroles=[]
 for j,f in loc.items():
  if C[f] in R:initial.append(rows[j].copy());history.append(rows[j].copy());keys.append([-1,j])
 for k,e in enumerate(P):
  if k==29098:
   eroles=[j for j,f in loc.items() if C[f]==C[71]];E=[rows[j].copy() for j in eroles]
  op,j=e[:2]
  if op=='INIT':need(j not in rows,'INIT absent');rows[j]={};loc[j]=e[2]
  elif op=='CLEAR':need(j>=n,'owned CLEAR');rows.pop(j);loc.pop(j)
  elif op=='ADD':need(C[loc[j]]==C[loc[e[2]]],'ADD cochart');add(rows[j],rows[e[2]],Q(e[3]))
  elif op=='COPY':need(not rows[j],'COPY zero');need(C[loc[j]]==C[loc[e[2]]],'COPY cochart');rows[j]={i:Q(e[3])*v for i,v in rows[e[2]].items()}
  elif op=='SCALE':rows[j]={i:Q(e[2])*v for i,v in rows[j].items()}
  elif op=='MOVE':
   need(C[loc[j]]==C[e[2]],'MOVE actual source');loc[j]=e[3]
   if C[e[3]] in R:history.append(rows[j].copy());keys.append([k,j])
  else:raise ValueError(op)
 need(E is not None,'encoder cut reached');need(set(rows)==set(range(n)),'all owned retired');need(all(C[loc[j]]==C[w['final'][j]] for j in rows),'all public final charts')
 W=[row for j,row in rows.items() if C[loc[j]]==T];receiver_end=[row for j,row in rows.items() if C[loc[j]] in R and C[loc[j]]!=T];rb=basis(history);wb=basis(W);local=basis(E);D=intersection(intersection(E,wb),rb);neutral=initial+receiver_end;nb=basis(neutral);remainders=[reduce(row,nb) for row in D]
 need(len(history)==1065 and len(rb)==1056,'complete receiver initial/arrival history dimensions');need(all(not reduce(row,rb) for row in receiver_end),'final receiver rows in history span')
 need(D==[{77:Q(1)}],'exact sole recoverable encoder mode');need(rows[189]=={77:Q(1),189:Q(1)},'actual receiver endpoint identity');need(C[loc[189]]!=T,'receiver endpoint offhub');stable=stable_lift(w,C,R,keys);decoded={}
 for i,c in stable.items():add(decoded,history[i],c)
 need(decoded=={77:Q(1)},'literal receiver-chart stable lift');need(bool(reduce({77:Q(1)},basis(initial))),'negative control: initial observations alone do not contain u77');need(bool(reduce({847:Q(1)},wb)),'negative control: cochart u847 is not terminal recoverable');stable_terms=[{'after_event':keys[i][0],'role':keys[i][1],'coefficient':str(c)} for i,c in sorted(stable.items())]
 result={'status':'PASS_INDEPENDENT_SOURCE_ROW_INTERSECTION_AND_CONTAINMENT' if not any(remainders) else 'INDEPENDENT_CONTAINMENT_NOT_ESTABLISHED','native_sha256':PIN,'encoder_cut_before_event':29098,'encoder_chart':71,'encoder_actual_live_roles':eroles,'encoder_rows':serial(E),'encoder_rank':len(local),'terminal_row_count':len(W),'terminal_rank':len(wb),'receiver_history_rows':len(history),'receiver_history_rank':len(rb),'receiver_initial_row_count':len(initial),'receiver_final_offhub_rows':len(receiver_end),'neutral_baseline_span_rank':len(nb),'E_intersect_terminal_rank':len(intersection(E,wb)),'D_rank':len(D),'D_basis':serial(D),'D_mod_neutral_remainders':serial(remainders),'D_in_neutral_baseline_span':not any(remainders),'conditional_control_conclusion':'Requires existing complete nine-relation additive annihilation and controls only at source chart spaces disjoint from receiver itinerary, with offhub endpoint and COPY neutrality. Final receiver-chart histories have a control-insensitive lift by local linear execution.','new_complete_kappa':None};result.update({'stable_identity':'u77 = original common final189 - original common initial189','stable_history_lift':stable_terms,'negative_controls':['u77 not in initial receiver rows alone','cochart u847 not terminal recoverable']});output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('encoder_rows','D_basis','D_mod_neutral_remainders')},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
