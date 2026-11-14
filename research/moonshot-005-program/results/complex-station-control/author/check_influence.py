#!/usr/bin/env python3
"""Exact all-time original-D-station control support for two source words."""
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path

PARENT='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
FOUR='20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f'
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def require(c,s):
 if not c:raise ValueError(s)
def read(p,h):
 b=p.read_bytes();require(hashlib.sha256(b).hexdigest()==h,'source hash '+str(p));return json.loads(gzip.decompress(b))
def plus(a,b,c=F(1)):
 a=dict(a)
 for k,v in b.items():
  a[k]=a.get(k,F(0))+c*v
  if not a[k]:del a[k]
 return a
def times(a,c):return {k:c*v for k,v in a.items() if c*v}
def span(f):
 z={0}
 for v in f:z|={u^v for u in tuple(z)}
 return z
class Basis:
 def __init__(self):self.rows={}
 def add(self,row):
  row=dict(row)
  for j,r in self.rows.items():
   if j in row:row=plus(row,r,-row[j])
  if row:
   p=min(row);self.rows[p]=times(row,1/row[p]);return True
  return False

def replay(w,ops,enforce_D=True):
 rows={i:{i:F(1)} for i in range(400)};loc=dict(enumerate(w['initial']));spaces=[span(f) for f in w['frames']]
 stations={d:{loc[d]} for d in range(304,400)};moves=Counter();counts=Counter();arrivals=[];peak=0;life=0
 for t,o in enumerate(ops):
  ty,r=o[:2];counts[ty]+=1
  if ty=='INIT':require(r>=400 and r not in loc,'INIT');rows[r]={};loc[r]=o[2];life+=1
  elif ty=='CLEAR':require(r>=400 and loc.get(r)==o[2],'CLEAR');del rows[r];del loc[r]
  elif ty=='MOVE':
   a,b,owned=o[2:];require(loc.get(r)==a and owned==(r>=400),'MOVE owner/chart');require(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'proper nested MOVE');loc[r]=b;moves[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1
   if r in stations:stations[r].add(b)
   if b==127:arrivals.append([t,r,a])
  elif ty=='ADD':
   src,c,at=o[2:];require(r!=src and loc.get(r)==loc.get(src)==at,'cochart ADD');require(not enforce_D or not 304<=r<400,'D unchanged during whole word');rows[r]=plus(rows[r],rows[src],F(c))
  elif ty=='SCALE':
   c,at=o[2:];require(F(c)!=0 and loc.get(r)==at,'SCALE');require(not enforce_D or not 304<=r<400,'D unchanged during whole word');rows[r]=times(rows[r],F(c))
  else:raise ValueError('unhandled source opcode '+ty)
  peak=max(peak,len(loc)-400)
 require(set(loc)==set(range(400)),'all owned retired');require(not enforce_D or all(rows[d]=={d:F(1)} for d in stations),'D outputs original')
 return rows,loc,stations,arrivals,{'instructions':len(ops),'operations':dict(counts),'moves':dict(moves),'owned_peak':peak,'owned_lifetimes':life}

def hub_map(w,ops,arrivals):
 # Independent formal variables for public Hub arrivals, not original inputs.
 expected={t:(r,k) for k,(t,r,a) in enumerate(arrivals)};h={};loc=dict(enumerate(w['initial']));history=[];departures=[]
 require(all(c!=127 for c in loc.values()),'no initial Hub input')
 for t,o in enumerate(ops):
  ty,r=o[:2]
  if ty=='MOVE':
   a,b,owned=o[2:]
   if a==127:
    require(owned and r in h,'no public Hub departure');departures.append([t,r,b]);del h[r]
   if b==127:
    require(not owned and expected[t][0]==r,'all Hub arrivals public');h[r]={expected[t][1]:F(1)};history.append((t,r,dict(h[r])))
   loc[r]=b
  elif ty=='INIT':
   loc[r]=o[2]
   if o[2]==127:h[r]={}
  elif ty=='CLEAR':
   if o[2]==127:del h[r]
   del loc[r]
  elif ty=='ADD' and o[4]==127:
   h[r]=plus(h[r],h[o[2]],F(o[3]));history.append((t,r,dict(h[r])))
  elif ty=='SCALE' and o[3]==127:
   h[r]=times(h[r],F(o[2]));history.append((t,r,dict(h[r])))
 require(set(h)==set(range(104))|set(range(208,304)),'exact 200 final public Hub roles')
 rank=Basis()
 for row in h.values():rank.add(row)
 require(len(arrivals)==len(rank.rows)==200,'invertible formal arrival-to-final Hub map')
 # Record the full matrix for an independent arithmetic audit.
 return h,{'public_arrivals':arrivals,'public_arrival_count':200,'owned_arrival_count':0,'owned_departures':departures,'formal_Hub_map_rank':200,'Hub_history_rows_in_formal_arrival_span':len(history)}

def analyze(w,ops,native):
 rows,loc,stations,arrivals,bill=replay(w,ops);hub,hubreceipt=hub_map(w,ops,arrivals)
 B=set(range(208,304));D=set(range(304,400));require(all(127 not in cs for cs in stations.values()),'no D station at Hub')
 nuisance=set(range(104))|B;nb=Basis()
 for r in nuisance:nb.add({j:v for j,v in rows[r].items() if j in nuisance})
 require(len(nb.rows)==200,'original first-X/B nuisance coefficient block invertible')
 adj={i:({i:F(1)} if i in B else {}) for i in range(400)}
 influence={};distinct=0;nonzero=0;source_controls=[]
 def inspect(r,t):
  nonlocal distinct,nonzero
  if r in D:return
  distinct+=1;g=adj[r]
  if g:
   nonzero+=1;influence.setdefault(loc[r],{'cut':t,'role':r,'B_response':dict(g)})
 for r in sorted(loc):inspect(r,len(ops))
 for t in range(len(ops)-1,-1,-1):
  o=ops[t];ty,r=o[:2]
  if ty=='ADD':
   src,c,at=o[2:];adj[src]=plus(adj[src],adj[r],F(c));inspect(src,t)
  elif ty=='SCALE':adj[r]=times(adj[r],F(o[2]));inspect(r,t)
  elif ty=='MOVE':loc[r]=o[2];inspect(r,t)
  elif ty=='CLEAR':loc[r]=o[2];adj[r]={};inspect(r,t)
  elif ty=='INIT':del adj[r];del loc[r]
  else:raise ValueError(ty)
 require(loc==dict(enumerate(w['initial'])),'backward charts/lifetimes')
 # This authenticates the complete backward derivative against the independently replayed endpoint.
 for r in range(400):require(adj[r]=={b:rows[b][r] for b in B if r in rows[b]},'forward/adjoint match at original input '+str(r))
 protected=sorted(d for d in D if not (stations[d]&set(influence)))
 accessible=sorted(D-set(protected))
 for d in protected:require(all(d not in rows[b] for b in B),'protected original D column absent from actual B endpoints')
 roles={int(k):v for k,v in w['source_role_map'].items()}
 hosts=sorted((native['live'][k],roles[b],roles[d]) for k,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2']))
 require({b for h,b,d in hosts}==B and {d for h,b,d in hosts}==D,'actual hosted role ranges')
 port_of_D={d:h for h,b,d in hosts};B_of_D={d:b for h,b,d in hosts}
 # The target residual minor restricted to protected coordinates is +/-I.
 minor=[]
 for d in protected:
  b=B_of_D[d];minor.append({j:rows[b].get(j,F(0))+F(j==d) for j in protected if rows[b].get(j,F(0))+F(j==d)})
 require(minor==[{d:F(1)} for d in protected],'protected principal residual identity minor')
 for d in accessible:
  c=min(stations[d]&set(influence));z=influence[c]
  require(z['B_response'],'positive control: actual nonzero response at admitted donor station');source_controls.append({'D_role':d,'port':port_of_D[d],'station':c,**z})
 # A scope-changing negative control: allow foreign original D in a live D carrier at ground.
 # At least one old D input affects B; this was deliberately excluded from the controls.
 borrowed=next((r for r in D if adj[r]),None);require(borrowed is not None and w['initial'][borrowed]==3,'recoded-D escape witness')
 mutant_d=protected[0];mutant,mloc,mstations,marrivals,mbill=replay(w,[['ADD',borrowed,mutant_d,'1',3]]+ops,False)
 require(mutant[borrowed]=={borrowed:F(1),mutant_d:F(1)},'borrowed D is not restored')
 require(all(plus(mutant[b],rows[b],F(-1))==({mutant_d:adj[borrowed][b]} if b in adj[borrowed] else {}) for b in B),'actual borrowed-D mutation changes B by certified column')
 free_residual_rank=Basis()
 for h,b,d in hosts:free_residual_rank.add(plus(rows[b],{b:F(1),d:F(-1)},F(-1)))
 result={'status':'PASS_EXACT_ALL_TIME_D_STATION_B_INFLUENCE','native_sha256':NATIVE,'parent_sha256':PARENT,'word_variant':'four' if w.get('funded_cross_pair') else 'parent','actual_stripped_reverse_rank':len(free_residual_rank.rows),'protected_D_count':len(protected),'protected_D_roles':protected,'protected_native_ports':[port_of_D[d] for d in protected],'accessible_D_count':len(accessible),'accessible_D_roles':accessible,'all_time_station_grant':True,'forbidden_control_destinations':'All original D roles304..399; their values must stay unchanged. Source-dependent non-D replacement or new transport remains outside.','distinct_adjoint_field_states_checked':distinct,'nonzero_adjoint_field_states':nonzero,'B_influence_chart_count':len(influence),'B_influence_charts':sorted(influence),'actual_source_bill':bill,'Hub_structural_certificate':hubreceipt,'control_class':'Arbitrary additive forms in original D_j at every current non-D field at every original D_j station, even before its physical arrival; fixed old coefficients/routes otherwise.','original_firstX_B_nuisance_rank':200,'original_D_station_charts':{d:sorted(c) for d,c in stations.items()},'residual_identity_minor_B_roles':[B_of_D[d] for d in protected],'borrowed_D_negative_control':{'ground_chart':3,'carrier':borrowed,'final_B_response':adj[borrowed],'protected_original_D_injected':mutant_d,'actual_mutated_D_endpoint':mutant[borrowed],'nonB_restoration_failed':True},'scope':'Exact finite-source all-volume linear-control theorem; no uniform supplier and no new kappa.'}
 return result,{'Hub_map':hub,'influence_witnesses':influence,'unprotected_positive_controls':source_controls}

def enc(z):
 if isinstance(z,F):return str(z)
 if isinstance(z,dict):return {str(k):enc(v) for k,v in z.items()}
 if isinstance(z,(tuple,list)):return [enc(v) for v in z]
 return z
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--four',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 n=read(a.native,NATIVE);q=read(a.parent,PARENT);w=q;ops=q['program'][:q['consumer']['begin']]
 if a.four:
  w=read(a.four,FOUR);ops=[o for o,k in zip(w['program'],w['parent_event_of_output']) if k is None or k<q['consumer']['begin']]
 result,cert=analyze(w,ops,n);result['actual_word_sha256']=FOUR if a.four else PARENT;a.output.mkdir(parents=True,exist_ok=True)
 for name,obj in [('RESULT.json',result),('CERTIFICATE.json',cert)]:
  raw=(json.dumps(enc(obj),sort_keys=True,indent=2)+'\n').encode();(a.output/name).write_bytes(raw)
 print(json.dumps({'status':result['status'],'variant':result['word_variant'],'protected_D_count':result['protected_D_count'],'accessible_D_count':result['accessible_D_count'],'B_influence_charts':result['B_influence_chart_count'],'field_states':result['distinct_adjoint_field_states_checked']},indent=2))
