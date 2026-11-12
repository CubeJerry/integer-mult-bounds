#!/usr/bin/env python3
"""Independent exact completeness and source-cone audit for96 reverse histories."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
import gzip,json,hashlib,time
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'worker-budget/reverse-history-cone';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';CPIN='e7e0de229e3b096d0ea9474ea8d9e325f3ef5d3e9e1f89c72be824765fc8783d'
def need(b,s):
 if not b:raise ValueError(s)
def add(a,b,c=F(1)):
 for k,v in b.items():
  x=a.get(k,F(0))+c*v
  if x:a[k]=x
  else:a.pop(k,None)
def space(fr):
 a={0}
 for v in fr:a.update(x^v for x in tuple(a))
 need(len(a)==2**len(fr),'independent binary chart frame')
 return frozenset(a)
def reduce(row,basis):
 row=row.copy()
 for p in sorted(basis):
  if p in row:add(row,basis[p],-row[p])
 return row
def basis_of(rows):
 basis={}
 for a in rows:
  row=reduce(a,basis)
  if row:
   p=min(row);c=row[p];basis[p]={k:v/c for k,v in row.items()}
 return basis

def main():
 start=time.monotonic();sb=(REPO/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(sb).hexdigest()==SPIN,'source pin')
 source=json.loads(gzip.decompress(sb));payload=gzip.decompress((PACK/'CERTIFICATE.json.gz').read_bytes());need(hashlib.sha256(payload).hexdigest()==CPIN,'complete history certificate payload')
 cert=json.loads(payload);need(cert['source_sha256']==SPIN,'certificate source');proofpin=hashlib.sha256((PACK/'PROOF.md').read_bytes()).hexdigest()
 P=source['program'];n=source['public'];need(n==1480,'actual public size');frames=list(map(space,source['frames']));first={};canonical=[first.setdefault(a,i) for i,a in enumerate(frames)]
 need(frames[127]==frozenset(range(512)) and frames[3]==frozenset({0}),'full hub and zero chart')
 pairs=list(zip(source['hosted']['Dports'],source['hosted']['X2'],source['hosted']['Y2']));need(len(pairs)==96 and len(set(pairs))==96,'all96 actual hosted pairs')
 recs=cert['receivers'];need([(r['port_index'],r['receiver_X2'],r['donor_Y2']) for r in recs]==pairs,'complete actual pair coverage and order')
 routes={j:[canonical[source['initial'][j]]] for _,x,y in pairs for j in (x,y)}
 for o in P:
  if o[0]=='MOVE' and o[1] in routes:routes[o[1]].append(canonical[o[3]])
 hubfields={j for j,c in enumerate(source['final']) if canonical[c]==127};off=set(range(n))-hubfields;need(len(hubfields)==1022 and len(off)==458,'actual endpoint hub partition')
 need(not any(canonical[c]==127 for c in source['initial']),'hub initially empty of public fields')
 ports=[];historyevents=[];initials=[];watch=defaultdict(set);allowed=[]
 for i,(portindex,x,y) in enumerate(pairs):
  a=source['ports'][portindex];H=frozenset(v for v in range(512) if (a&v).bit_count()%2==0);ports.append(a)
  need(a.bit_count()%2==1 and a not in H,'odd-port cone direction a not in a-perp')
  need(frames[source['initial'][x]]==frozenset({0,a}) and canonical[source['final'][x]]==127,'receiver endpoints')
  need(canonical[source['initial'][y]]==3 and frames[source['final'][y]]==H,'donor endpoints')
  need(routes[x]==recs[i]['receiver_route'] and routes[y]==recs[i]['donor_route'],'actual full receiver and donor itineraries')
  need(all(a in frames[c] for c in routes[x]) and all(frames[c]<=H and a not in frames[c] for c in routes[y]),'opposite receiver and donor cones')
  for j in (x,y):need(all(frames[c]<frames[d] for c,d in zip(routes[j],routes[j][1:])),'strict monotone original routes')
  R=set(routes[x]);ini={j for j,c in enumerate(source['initial']) if canonical[c] in R};initials.append(ini)
  ev={e for e,o in enumerate(P) if o[0]=='MOVE' and canonical[o[3]] in R-{127}};historyevents.append(ev)
  for e in ev:watch[e].add(i)
  allowed.append({c for c in range(len(frames)) if a not in frames[c]})
  need(len(ini)==recs[i]['initial_observation_count'] and len(ev)==recs[i]['nonhub_arrival_count'],'complete initial and nonhub-arrival observations')
 need(sum(map(len,historyevents))==cert['nonhub_arrival_count']==3397,'all3397 nonhub observations with receiver multiplicity')
 # Explicit458-dimensional input test family. It is validated by the complete
 # source replay below; no assumed inverse native formula is used as evidence.
 rows=[({j:F(1)} if j in off else {}) for j in range(n)];D=set(source['hosted']['Dports'])
 for i,x in enumerate(source['live']):
  if i not in D:
   y=x+112;need(x in hubfields and y in off,'nonhosted first-pair output partition');rows[x]={y:F(1)}
 for _,x,y in pairs:need(x in hubfields and y in off,'hosted reverse output partition');rows[x]={y:F(1)}
 initial_rows=[r.copy() for r in rows];observed={};loc=dict(enumerate(source['initial']));arrived=[];guards=[]
 for e,o in enumerate(P):
  kind,j=o[:2]
  if kind=='INIT':need(j>=n and j not in loc,'owned initialization');loc[j]=o[2];rows.extend({} for _ in range(max(0,j+1-len(rows))));rows[j]={}
  elif kind=='CLEAR':need(j>=n and loc.get(j)==o[2],'owned CLEAR at its actual chart');del loc[j];rows[j]={}
  elif kind=='MOVE':
   need(loc.get(j)==o[2],'native current MOVE source');loc[j]=o[3]
   if canonical[o[2]]==127:raise ValueError('hub departure')
   if canonical[o[3]]==127:
    need(j<n and not o[4] and j not in arrived,'distinct public-only hub arrival');arrived.append(j);need(not rows[j],'every hub arrival annihilates all458 test columns')
  elif kind in ('ADD','COPY'):
   need(j!=o[2] and loc.get(j)==loc.get(o[2])==o[4],'native cochart arithmetic')
   if kind=='COPY':need(not rows[j],'original COPY guard on458 test columns');guards.append(e);rows[j]={}
   add(rows[j],rows[o[2]],F(o[3]))
  elif kind=='SCALE':need(loc.get(j)==o[3] and F(o[2]),'nonzero native SCALE');rows[j]={k:F(o[2])*v for k,v in rows[j].items()}
  else:raise ValueError(kind)
  if kind!='MOVE' and canonical[o[-1]]==127:need(kind in ('ADD','SCALE') and j<n and (kind!='ADD' or o[2]<n),'hub operations are invertible public ADD/SCALE')
  if e in watch:observed[e]=rows[j].copy()
  if e%20000==0:print('TEST_FAMILY_REPLAY',e,'seconds',round(time.monotonic()-start,2),flush=True)
 need(set(loc)==set(range(n)) and list(loc[j] for j in range(n))==source['final'],'complete final location interface')
 need(set(arrived)==hubfields and len(arrived)==1022,'square complete absorbing hub arrival/final interface')
 need(all(rows[j]==({j:F(1)} if j in off else {}) for j in range(n)),'all458 exact test input vectors have independent offhub-unit endpoints and zero hub endpoints')
 # Completeness sandwich: the test-family quotient rank lower bound matches
 # the upper bound from independent exact full-input history identities.
 completeness=[];relations=[];owners=[];timed=defaultdict(list)
 for i,r in enumerate(recs):
  ibasis=basis_of(initial_rows[j] for j in sorted(initials[i]))
  projected=[reduce(observed[e],ibasis) for e in sorted(historyevents[i])];qdim=len(basis_of(projected))
  need(len(ibasis)==r['known_offhub_coordinate_count'] and qdim==r['quotient_arrival_rank'],'independent quotient ranks on458 exact input directions')
  arrrows=[]
  for relation in r['null_relations']:
   k=len(relations);relations.append(relation);owners.append(i);coeff={}
   for t in relation['arrival_terms']:
    e=t['after_event'];o=P[e];need(e in historyevents[i] and o[1]==t['role'] and o[3]==t['chart'] and F(t['coefficient']),'actual permitted arrival term')
    add(coeff,{e:F(t['coefficient'])});timed[e].append((t['role'],k,F(t['coefficient'])))
   for t in relation['initial_terms']:need(t['role'] in initials[i] and source['initial'][t['role']]==t['chart'] and F(t['coefficient']),'actual permitted initial term')
   for t in relation['final_hub_terms']:need(t['role'] in hubfields and F(t['coefficient']),'actual final hub coordinate')
   arrrows.append(coeff)
  nr=len(r['null_relations']);need(len(basis_of(arrrows))==nr==len(historyevents[i])-qdim,'complete independent arrival projections of stored null relations')
  completeness.append({'receiver':r['receiver_X2'],'donor':r['donor_Y2'],'initial_observations':len(initials[i]),'initial_test_rank':len(ibasis),'nonhub_arrivals':len(historyevents[i]),'test_quotient_rank':qdim,'independent_relations':nr})
 need(len(relations)==cert['relations_count']==1859 and sum(r['test_quotient_rank'] for r in completeness)==1538,'complete global rank census')
 # Fresh full1480-input simultaneous adjoints. Inspect both sides of each
 # post-MOVE sample capture, in addition to every changed source role/cut.
 adj=[{} for _ in range(n+source['owned_fields'])];loc=dict(enumerate(source['final']))
 for k,r in enumerate(relations):
  for t in r['final_hub_terms']:add(adj[t['role']],{k:F(t['coefficient'])})
 checks=0;inspections=0;support=[set() for _ in recs];bad=[]
 def inspect(j,cut,phase):
  nonlocal checks,inspections
  inspections+=1
  if j not in loc:return
  c=canonical[loc[j]]
  for k,v in adj[j].items():
   need(v,'sparse adjoint has no zero entries');i=owners[k];checks+=1;support[i].add(c)
   if ports[i] not in frames[c]:bad.append({'receiver':recs[i]['receiver_X2'],'relation_global':k,'role':j,'chart':loc[j],'cut':cut,'phase':phase,'coefficient':str(v)})
 for j in loc:inspect(j,len(P),'final_cut')
 for e in range(len(P)-1,-1,-1):
  for j,k,c in timed.get(e,[]):add(adj[j],{k:c})
  for j in {t[0] for t in timed.get(e,[])}:inspect(j,e,'after_MOVE_before_sample')
  o=P[e];kind,j=o[:2]
  if kind=='MOVE':loc[j]=o[2];inspect(j,e,'before_source_event')
  elif kind=='ADD':add(adj[o[2]],adj[j],F(o[3]));inspect(o[2],e,'before_source_event')
  elif kind=='COPY':add(adj[o[2]],adj[j],F(o[3]));adj[j]={};inspect(o[2],e,'before_source_event');inspect(j,e,'before_source_event')
  elif kind=='SCALE':adj[j]={k:F(o[2])*v for k,v in adj[j].items()};inspect(j,e,'before_source_event')
  elif kind=='CLEAR':loc[j]=o[2];adj[j]={};inspect(j,e,'before_source_event')
  elif kind=='INIT':del loc[j];adj[j]={}
  else:raise ValueError(kind)
  if e%20000==0:print('FULL_NULL_CONE_ADJOINT',e,'seconds',round(time.monotonic()-start,2),'nonzero_entries',checks,flush=True)
 need(not bad,'upper-cone support failure '+str(bad[:2]))
 need(set(loc)==set(range(n)) and list(loc[j] for j in range(n))==source['initial'],'backward initial physical state')
 before_initial={j:a.copy() for j,a in enumerate(adj) if a}
 for k,r in enumerate(relations):
  for t in r['initial_terms']:add(adj[t['role']],{k:F(t['coefficient'])})
 need(all(not a for a in adj),'all1859 exact identities on every original1480 common input')
 # A forbidden initial-line control is independently checked by chronological
 # one-column source replay, distinct from the backward adjoint implementation.
 pulse_x=recs[0]['receiver_X2'];pulse={pulse_x:F(1)};relation=relations[0];lookup={t['after_event']:F(t['coefficient']) for t in relation['arrival_terms']};value=F(0)
 for e,o in enumerate(P):
  kind,j=o[:2]
  if kind in ('INIT','CLEAR'):pulse.pop(j,None)
  elif kind in ('ADD','COPY'):
   v=(pulse.get(j,F(0)) if kind=='ADD' else F(0))+F(o[3])*pulse.get(o[2],F(0))
   if v:pulse[j]=v
   else:pulse.pop(j,None)
  elif kind=='SCALE':
   if j in pulse:pulse[j]*=F(o[2])
  elif kind!='MOVE':raise ValueError(kind)
  if e in lookup:value+=lookup[e]*pulse.get(j,F(0))
 for t in relation['final_hub_terms']:value+=F(t['coefficient'])*pulse.get(t['role'],F(0))
 need(value==before_initial[pulse_x][0]==1 and ports[0] in frames[source['initial'][pulse_x]],'extra-cone control changes first completed history relation by1')
 missing=relations[0]['initial_terms'][0];need(F(missing['coefficient']),'nonzero omitted initial term')
 need(all(not (set(r['donor_route'])&support[i]) for i,r in enumerate(recs)),'all original donor charts outside support')
 author=json.loads((PACK/'RESULT.json').read_text())
 need(author['complete_history_payload_sha256']==CPIN and author['receiver_count']==96 and author['relations']==1859 and author['nonhub_arrivals']==3397,'author receipt interface')
 need([sorted(s) for s in support]==[r['charts'] for r in author['support_charts']],'independent exact chart supports agree')
 result={'status':'PASS_INDEPENDENT_ALL96_REVERSE_HISTORY_CONE','source_sha256':SPIN,'certificate_payload_sha256':CPIN,'reviewed_proof_sha256':proofpin,'receiver_count':96,'full_nonhub_arrivals_with_receiver_multiplicity':3397,'unique_nonhub_arrival_events':len(watch),'all_initial_cochart_values_included':True,'full_hub_arrivals':1022,'final_hub_fields':1022,'hub_departures':0,'hub_local_map_invertible_by_instruction_structure':True,'exact_test_input_columns':458,'test_endpoint_offhub_unit_matrix_verified':True,'all_test_hub_arrivals_zero':True,'quotient_rank_total':1538,'complete_independent_relations':1859,'all1480_input_baseline_identities_verified':True,'current_role_phase_inspections':inspections,'nonzero_adjoint_entries_checked':checks,'upper_cone_exceptions':0,'original_donor_route_support_intersections':0,'cone_direction':'Every nonzero adjoint lies at a chart U containing its receiver port a. Admitted control sites satisfy a not in U. All monotone Y2 routes ending in H=a-perp are admitted because odd a has a dot a=1 and therefore a not in H.','history_completeness_method':'Exact458-column input test family yields a lower bound on quotient arrival rank;1859 independent full-input identities give the matching upper bound. Additional relations involving only initial observations and final hub outputs have zero private response under the endpoint-restoration premise. No full native inverse is assumed.','receivers':completeness,'support_charts':[{'receiver':r['receiver_X2'],'donor':r['donor_Y2'],'port':ports[i],'charts':sorted(support[i])} for i,r in enumerate(recs)],'negative_controls':{'forbidden_initial_receiver_line_control':{'role':pulse_x,'chart':source['initial'][pulse_x],'before_event':0,'first_relation_response':str(value)},'omitted_first_initial_term':{'role':missing['role'],'exact_input_residual':str(-F(missing['coefficient']))}},'COPY_guards_on_test_family':guards,'scope':'Fixed original common-input observation matrix, initial observations captured before controls, independent additive raw-q controls only at charts missing the receiver port, and complete common endpoint restoration. Exact source identities hold for arbitrary realized increments at those sites, but no pure-gain conclusion extends to common-dependent replacement or mixed records changing the observation baseline. No numeric paid-call or whole-system lower bound is asserted.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('receivers','support_charts')},indent=2))
if __name__=='__main__':main()
