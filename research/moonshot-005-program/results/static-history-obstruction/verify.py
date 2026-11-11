#!/usr/bin/env python3
"""Source-bound static closed-cut extension of the S003 endpoint certificate."""
import argparse,bisect,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PREFIX='e87e4bfcb9772b232e6c443cf2d8ee79a7de356d381eda3aa42040e5e37003c0'
BUDGET='b5c4a118bb7e72a31d7ba90a8cd4b72884f9fa6470710850119d709ad3f21f40'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(a):
 B={}
 for x in a:
  for p,y in sorted(B.items(),reverse=True):
   if x>>p&1:x^=y
  if x:
   p=x.bit_length()-1
   for q,y in list(B.items()):
    if y>>p&1:B[q]=y^x
   B[p]=x
 return tuple(y for p,y in sorted(B.items()))
def reverse_row(w,out,main):
 a={out:F(1)}
 for e in reversed(w['program']):
  op,d=e[:2];v=a.get(d,F(0))
  if not v:continue
  if op in ('INIT','CLEAR'):a.pop(d,None)
  elif op=='SCALE':
   z=v*F(e[2])
   if z:a[d]=z
   else:a.pop(d,None)
  elif op in ('ADD','COPY'):
   s,c=e[2],F(e[3])
   if op=='COPY':a.pop(d,None)
   z=a.get(s,F(0))+v*c
   if z:a[s]=z
   else:a.pop(s,None)
 return {i:v for i,v in a.items() if i in main}
def quiet_windows(w,M,C):
 # This source census follows the pinned predecessor's touch/visit definition.
 touch=collections.defaultdict(list);visits={};current={i:(-1,w['initial'][i]) for i in M};P=w['program'];end=len(P)
 for k,e in enumerate(P):
  touch[e[1]].append(k)
  if e[0] in ('ADD','COPY'):touch[e[2]].append(k)
  if e[0]=='MOVE' and e[1] in M:
   i=e[1];a,f=current[i];need(f==e[2] and (i,C[f]) not in visits,'single monotone main visit');visits[i,C[f]]=(a,k);current[i]=(k,e[3])
 for i,(a,f) in current.items():visits[i,C[f]]=(a,end)
 ans=[]
 for k,e in enumerate(P):
  if e[0]!='MOVE' or e[1] in M:continue
  h,s,d=e[1:4];ix=bisect.bisect_right(touch[h],k);deadline=touch[h][ix] if ix<len(touch[h]) else end
  for q in sorted(M):
   x,y=visits.get((q,C[s])),visits.get((q,C[d]))
   if x and y and x[0]<k<x[1] and k<y[0]<deadline:ans.append((k,h,q,s,d,y[0],deadline))
 return ans
def closure(start,edges):
 adj=collections.defaultdict(set)
 for a,b in edges:adj[a].add(b)
 out=set(start);todo=list(out)
 for a in todo:
  for b in adj[a]:
   if b not in out:out.add(b);todo.append(b)
 return out
def rank(rows,columns):
 basis={}
 for r in rows:
  v={i:r.get(i,F(0)) for i in columns if r.get(i,F(0))}
  for i,b in sorted(basis.items()):
   if i in v:
    c=v[i]
    for j,x in b.items():
     z=v.get(j,F(0))-c*x
     if z:v[j]=z
     else:v.pop(j,None)
  if v:
   i=min(v);c=v[i];basis[i]={j:x/c for j,x in v.items()}
 return len(basis)
def check_cut(cut,edges,initial,sinks):
 need(set(initial)<=cut,'all selected initial charts lie inside cut')
 need(not cut&set(sinks),'all demanded endpoint charts lie outside cut')
 need(all(a not in cut or b in cut for a,b in edges),'allowed route cannot leave closed cut')
def run(a):
 need(digest(a.source)==NATIVE,'native pin');need(digest(a.prefix)==PREFIX,'facet prefix pin');need(digest(a.budget)==BUDGET,'full budget pin')
 w=json.load(gzip.open(a.source,'rt'));p=json.loads(a.prefix.read_text());old=json.loads(a.predecessor.read_text());price=json.loads(a.budget.read_text());need(old['source_sha256']==NATIVE,'predecessor source pin')
 M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);C=[canon(f) for f in w['frames']];rep={}
 for i,c in enumerate(C):rep.setdefault(c,i)
 need(len(M)==400 and len(rep)==1094,'canonical source census')
 pairs=old['witness_pairs'];K=[z['input'] for z in pairs];need(len(K)==len(set(K))==46,'46 distinct selected inputs');need(len({z['output'] for z in pairs})==46,'46 distinct outputs')
 L=quiet_windows(w,M,C);need(len(L)==354 and len({z[0] for z in L})==141,'all quiet windows and starts')
 main_edges=[(C[e[2]],C[e[3]]) for e in w['program'] if e[0]=='MOVE' and e[1] in M];own_edges=[(C[e[2]],C[e[3]]) for e in w['program'] if e[0]=='MOVE' and e[4]];Q={(C[z[3]],C[z[4]]) for z in L};E=set(main_edges)|set(own_edges)|Q
 need(len(main_edges)==1710 and len(own_edges)==47 and len(E)==853,'generous full original edge pool')
 initials=[C[w['initial'][i]] for i in K];sinks=[C[w['final'][z['output']]] for z in pairs];cut=closure(initials,E);need(len(cut)==220,'static source cut size');check_cut(cut,E,initials,sinks)
 # All original histories, including used and unused routes, are over-granted.
 history=0
 for e in w['program']:
  if e[0]=='MOVE' and e[1] in K:need(C[e[2]] in cut and C[e[3]] in cut,'every selected raw history stays inside');history+=1
 spent={z['source_event'] for z in p['reserved_raw_main_routes']};need(len(spent)==262,'actual spent reservations');hoisted=set(p['entry_donors'])|set(p['nonentry_donors']);need(len(hoisted)==60,'actual hoisted carriers')
 need(all(C[w['final'][i] if i in hoisted else w['initial'][i]] in cut for i in K),'actual post-prefix raw positions inside')
 need(C[127] in cut and C[541] not in cut and p['output_chart']==541,'hub and actual two-output side')
 rows={};det=F(1)
 for z in pairs:
  out,j=z['output'],z['input'];r=reverse_row(w,out,M);restriction={i:v for i,v in r.items() if i in K};need(restriction=={j:F(z['coefficient'])},'source-authenticated diagonal endpoint');need(w['final'][out]==z['target_chart'],'actual output chart');det*=restriction[j];rows[str(out)]={str(i):str(v) for i,v in sorted(r.items())}
 need(det==F(1,8),'rank46 determinant')
 rs=[{int(i):F(v) for i,v in r.items()} for r in p['output_rows']];need(len(rs)==2 and rank(rs,K)==2,'two actual initial aggregate modes')
 minor=rs[0][17]*rs[1][20]-rs[0][20]*rs[1][17];need(minor==F(-1,8),'independent aggregate minor');need(rank(rs+[{z['input']:F(z['coefficient'])} for z in pairs],K)-rank(rs,K)==44,'exact quotient rank44')
 all_edges={(C[e[2]],C[e[3]]) for e in w['program'] if e[0]=='MOVE'};full=closure(initials,all_edges);need(all(x in full for x in sinks),'all helper recoding destroys graph separation')
 escaped=[{'event':k,'helper':e[1],'source':e[2],'target':e[3],'rank':len(C[e[3]])-len(C[e[2]])} for k,e in enumerate(w['program']) if e[0]=='MOVE' and C[e[2]] in cut and C[e[3]] not in cut]
 need(len(escaped)==399 and len({x['helper'] for x in escaped})==375 and all(x['helper'] not in M and not w['program'][x['event']][4] for x in escaped),'399 nonmain public helper escape occurrences')
 head=tuple(F(x) for x in price['variants']['eight_facet_copies']['remaining_paid_moment_per_native_interval']);need(F(8)<head[0]<=head[1]<F(9),'optimistic eight-arrival ceiling')
 controls=[]
 for name,badcut,badedges in [('omit_initial_chart',cut-{initials[0]},E),('allow_one_cross_helper',cut,E|{(C[escaped[0]['source']],C[escaped[0]['target']])}),('grant_all_helper_edges',cut,all_edges)]:
  try:check_cut(badcut,badedges,initials,sinks)
  except ValueError as ex:controls.append({'mutation':name,'rejection':str(ex)})
  else:raise ValueError('negative control survived')
 need(rank(rs+rs,K)==2,'copies do not create new modes');need(rank([{j:F(1)} for j in K],K)==46,'free selected input rereads erase bound')
 certificate={'native_sha256':NATIVE,'facet_prefix_sha256':PREFIX,'predecessor_certificate_sha256':digest(a.predecessor),'canonical_cut_representatives':sorted(rep[c] for c in cut),'witness_pairs':pairs,'source_endpoint_rows':rows,'aggregate_restriction_rows':[{str(i):str(r[i]) for i in sorted(set(K)&set(r))} for r in rs],'aggregate_minor_columns':[17,20],'aggregate_minor':'-1/8','escape_occurrences':escaped}
 path=a.packet/'CERTIFICATE.json';serialized=json.dumps(certificate,indent=2,sort_keys=True)+'\n'
 if a.write_certificate:path.write_text(serialized)
 else:need(path.read_text()==serialized,'exact frozen certificate')
 return {'status':'PASS_STATIC_220_CHART_HISTORY_ROBUST_44_MESSAGE_BOUND','native_sha256':NATIVE,'facet_prefix_sha256':PREFIX,'budget_sha256':BUDGET,'certificate_sha256':digest(path),'canonical_charts':1094,'closed_cut_charts':220,'full_original_main_occurrences_granted':1710,'full_original_owned_occurrences_granted':47,'quiet_windows_granted':354,'quiet_starts_granted':141,'distinct_allowed_static_arcs':853,'selected_raw_history_MOVE_occurrences':history,'all_original_raw_histories_granted':True,'original_time_order_required':False,'actual_prefix_spent_main_occurrences':262,'selected_input_count':46,'selected_output_count':46,'endpoint_determinant':'1/8','initial_aggregate_rank':2,'aggregate_minor':'-1/8','remaining_message_lower_bound':44,'optimistic_additional_paid_arrival_ceiling':8,'additional_original_helper_crossing_field_units_needed_if_at_most8_new_paid':36,'original_helper_escape_occurrences':len(escaped),'distinct_escape_arcs':len({(C[x['source']],C[x['target']]) for x in escaped}),'distinct_escape_helpers':len({x['helper'] for x in escaped}),'escape_rank_histogram':dict(sorted(collections.Counter(x['rank'] for x in escaped).items())),'negative_controls':controls+[{'mutation':'duplicate_both_aggregates','aggregate_rank':2},{'mutation':'free_global_selected_input_rereads','aggregate_rank':46,'remaining_rank_bound':0}],'scope':'All-V linear closed-cut lower bound with arbitrary reorder/reuse of main/all-owned/quiet edges, free raw history on every original main itinerary and two global aggregate modes. Extra q-informative nonquiet helper crossings or new routes remain possible and charged. No complete native, uniform supplier or new kappa.'}
if __name__=='__main__':
 q=argparse.ArgumentParser();q.add_argument('--source',type=Path,required=True);q.add_argument('--prefix',type=Path,required=True);q.add_argument('--predecessor',type=Path,required=True);q.add_argument('--budget',type=Path,required=True);q.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);q.add_argument('--output',type=Path,required=True);q.add_argument('--write-certificate',action='store_true');a=q.parse_args();r=run(a);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
