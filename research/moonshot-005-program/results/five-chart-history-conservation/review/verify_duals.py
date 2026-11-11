#!/usr/bin/env python3
"""Independent scalar adjoint verification of complete endpoint/history duals."""
import argparse, gzip, hashlib, json
from pathlib import Path
from check import Q, PIN, canonical_span, require

def verify_one(w,frames,du,allowed):
 P=w['program'];loc={j:frames[f] for j,f in enumerate(w['final'])}
 adj={j:-Q(c) for j,c in du['endpoint_terms']};guards={t:-Q(c) for t,c in du['guard_terms']}
 observation=du['observation_after_event'];role=du['observation_role'];checks=0
 def plus(j,c):
  v=adj.get(j,Q(0))+c
  if v:adj[j]=v
  else:adj.pop(j,None)
 def check(j,cut):
  nonlocal checks
  if j in loc and loc[j] in allowed:
   checks+=1
   if adj.get(j,Q(0)):return dict(before_event=cut,role=j,coefficient=str(adj[j]))
  return None
 for j in loc:
  fail=check(j,len(P))
  if fail:return fail,checks
 for t in range(len(P)-1,-1,-1):
  if t==observation:
   plus(role,Q(1));fail=check(role,t+1)
   if fail:return fail,checks
  e=P[t];op,j=e[:2];changed=[]
  if op=='ADD':plus(e[2],Q(e[3])*adj.get(j,Q(0)));changed=[e[2]]
  elif op=='COPY':
   plus(e[2],Q(e[3])*adj.get(j,Q(0)));adj.pop(j,None);plus(j,guards.get(t,Q(0)));changed=[e[2],j]
  elif op=='SCALE':
   z=Q(e[2])*adj.get(j,Q(0));adj.pop(j,None);plus(j,z);changed=[j]
  elif op=='MOVE':loc[j]=frames[e[2]];changed=[j]
  elif op=='CLEAR':loc[j]=frames[e[2]];adj.pop(j,None);changed=[j]
  elif op=='INIT':loc.pop(j,None);adj.pop(j,None)
  else:raise ValueError(op)
  for j in changed:
   fail=check(j,t)
   if fail:return fail,checks
 return None,checks

def main(a):
 raw=a.source.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 w=json.loads(gzip.decompress(raw));F=list(map(canonical_span,w['frames']));r=json.loads(a.certificate.read_text())
 if r.get('schema')=='donor77-receiver189-rank-one-response/1':
  require(r['donor']==77 and r['receiver']==189 and r['endpoint']=={'chart':198,'role':189},'rank-one source pair')
  r=dict(r,stations=r['station_charts'],cut=0,history_endpoint_duals=[dict(observation_after_event=x['after_event'],observation_role=x['role'],endpoint_terms=[[189,x['endpoint_coefficient']]] if Q(x['endpoint_coefficient']) else [],guard_terms=[]) for x in r['arrival_observations']])
 require(r['source_sha256']==PIN and r['stations']==[71,312,324,232,127] and r['cut']==0,'certificate source/scope')
 allowed={F[x] for x in r['stations']}
 R={F[w['initial'][189]]}|{F[e[3]] for e in w['program'] if e[0]=='MOVE' and e[1]==189}
 require(not allowed&R,'disjoint station and receiver spaces')
 expected=[(t,e[1]) for t,e in enumerate(w['program']) if e[0]=='MOVE' and F[e[3]] in R]
 require([(x['observation_after_event'],x['observation_role']) for x in r['history_endpoint_duals']]==expected,'all receiver arrivals in chronological order')
 counts=[]
 for du in r['history_endpoint_duals']:
  require(all(F[w['final'][j]]!=F[127] for j,c in du['endpoint_terms']),'dual uses only constrained offhub endpoints')
  require(all(w['program'][t][0]=='COPY' for t,c in du['guard_terms']),'dual uses only real COPY guards')
  fail,count=verify_one(w,F,du,allowed);require(fail is None,'failed station invariant '+str(fail));counts.append(count)
 mutant=json.loads(json.dumps(next(du for du in r['history_endpoint_duals'] if du['endpoint_terms'])))
 mutant['endpoint_terms'][0][1]=str(Q(mutant['endpoint_terms'][0][1])+1)
 fail,_=verify_one(w,F,mutant,allowed);require(fail is not None,'changed dual coefficient rejected')
 access_fail=None
 for du in r['history_endpoint_duals']:
  bad,_=verify_one(w,F,du,allowed|{F[3]})
  if bad:access_fail=bad;break
 require(access_fail is not None,'expanded receiver access rejects old certificate')
 chart8_fail=None
 for du in r['history_endpoint_duals']:
  bad,_=verify_one(w,F,du,allowed|{F[8]})
  if bad:chart8_fail=bad;break
 require(chart8_fail is not None,'expanded offreceiver chart8 access rejects old certificate')
 out=dict(status='PASS_INDEPENDENT_COMPLETE_HISTORY_ENDPOINT_DUALS',source_sha256=PIN,certificate_sha256=hashlib.sha256(a.certificate.read_bytes()).hexdigest(),arrival_observations=len(expected),initial_observations=sum(F[x] in R for x in w['initial']),canonical_station_count=len(allowed),native_cut_count=len(w['program'])+1,per_decoder_changed_state_checks=counts,coefficient_mutant_witness=fail,receiver_chart_access_mutant_witness=access_fail,complete_native_history_factors_through_offhub_endpoints_and_copy_guards=True,new_complete_kappa=None)
 out['additional_station_chart8_mutant_witness']=chart8_fail
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
