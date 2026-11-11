#!/usr/bin/env python3
"""Source-bound exact current-cochart differential delivery witnesses.

No physical observer availability or new supplier is inferred from this replay.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
RELATIVE_SOURCE='research/shared-wire-split-composition/data/final.json.gz'
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(p,msg):
 if not p:raise ValueError(msg)
def default_source():
 for base in HERE.parents:
  for q in (base/RELATIVE_SOURCE,base/'moonshot'/RELATIVE_SOURCE):
   if q.is_file():return q
 return Path(RELATIVE_SOURCE)
def add(row,other,c):
 for j,v in other.items():
  x=row.get(j,F(0))+c*v
  if x:row[j]=x
  else:row.pop(j,None)
def decode(row):return {int(j):F(c) for j,c in row if F(c)}
def span(frame):
 s={0}
 for r in frame:s|={x^r for x in s}
 return frozenset(s)
def reverse_form(word,cut,form):
 row=dict(form)
 for e in reversed(word['program'][:cut]):
  op,d=e[:2]
  if op in ('INIT','CLEAR'):row.pop(d,None)
  elif op in ('ADD','COPY') and d in row:
   s=e[2];x=row.get(s,F(0))+F(e[3])*row[d]
   if x:row[s]=x
   else:row.pop(s,None)
  elif op=='SCALE' and d in row:
   row[d]*=F(e[2])
   if not row[d]:del row[d]
 return row
def run(source,certificate):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');need(hashlib.sha256(raw+b'!').hexdigest()!=PIN,'source drift control')
 cert_raw=certificate.read_bytes();cert=json.loads(cert_raw);need(cert['source_sha256']==PIN,'certificate source pin')
 w=json.loads(gzip.decompress(raw));n=w['public'];M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need((len(M),n-len(M))==(400,1080),'actual owner partition')
 rows=[{} for _ in range(n+w['owned_fields'])]
 for r in M:rows[r]={r:F(1)}
 frames=list(map(span,w['frames']));need(all(len(s)==2**len(f) for s,f in zip(frames,w['frames'])),'independent frame bases')
 current=w['initial'][:]+[None]*w['owned_fields'];versions=[-1]*len(rows);prior_rows=[{} for _ in rows];wanted={a['before_event']:a for a in cert['witnesses']};need(len(wanted)==10,'ten distinct event witnesses')
 checked=[];ranks=Counter();ordinary_terms=0;observer_counts=Counter();coefficient_controls=0;dirty_controls=0;actual_stale_controls=0
 for i,e in enumerate(w['program']):
  op,d=e[:2]
  if i in wanted:
   a=wanted[i];need(e==a['move'] and op=='MOVE' and d>=n,'named owned MOVE');need(current[d]==e[2],'source entry chart');need(versions[d]==a['source_last_value_event'],'source current value version')
   need(decode(a['target_row'])==rows[d],'complete homogeneous target row')
   need(frames[e[2]]!=frames[e[3]],'distinct transport subspaces')
   rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));need(rank==a['rank'] and rank>0,'paid child rank')
   need(frames[e[2]]<=frames[e[3]] or frames[e[3]]<=frames[e[2]],'nested source MOVE')
   got={};form={d:F(1)};version_map={};kind_map={}
   for r,co in a['witness']:
    c=F(co);need(c!=0 and r!=d and current[r] is not None,'live distinct observer')
    need(frames[current[r]]==frames[e[3]],'CURRENT destination cochart observer')
    need(current[r]==a['observer_current_frames'][str(r)],'observer exact frame version')
    need(versions[r]==a['observer_last_value_events'][str(r)],'observer current scalar version')
    need(rows[r]==decode(a['observer_rows'][str(r)]),'observer exact homogeneous row')
    kind='main' if r in M else 'helper' if r<n else 'owned';need(kind==a['observer_kinds'][str(r)],'observer actual role kind')
    add(got,rows[r],c);form[r]=form.get(r,F(0))-c;observer_counts[kind]+=1
   need(got==rows[d],'exact differential delivery identity')
   residual=reverse_form(w,i,form);need(residual==decode(a['common_value_residual_on_entering_helpers']),'full arbitrary-input reverse identity')
   need(residual and all(r<n and r not in M for r in residual),'nonzero common residual supported only on entering shared helpers')
   # Each identity remains true for arbitrary shared dirty h because this
   # residual is the SAME for both virtual copies. It is not an ordinary value equality.
   seed=next(iter(residual));need(residual[seed]!=0,'dirty-helper ordinary-equality control');dirty_controls+=1
   first=a['witness'][0][0];bad=dict(got);add(bad,rows[first],F(1));need(bad!=rows[d],'wrong coefficient control');coefficient_controls+=1
   need(a['observer_last_value_events'][str(first)]+1!=versions[first],'stale-version metadata control')
   for stale,co in a['witness']:
    if prior_rows[stale]!=rows[stale]:
     bad=dict(got);add(bad,rows[stale],-F(co));add(bad,prior_rows[stale],F(co));need(bad!=rows[d],'actual stale-row control');actual_stale_controls+=1;break
   ranks[rank]+=1;ordinary_terms+=len(a['witness']);checked.append(i)
  if op in ('INIT','CLEAR','SCALE','ADD','COPY'):prior_rows[d]=rows[d].copy()
  if op=='INIT':need(d>=n and current[d] is None,'INIT guard');current[d]=e[2];rows[d]={};versions[d]=i
  elif op=='CLEAR':need(d>=n and current[d]==e[2],'CLEAR guard');current[d]=None;rows[d]={};versions[d]=i
  elif op=='MOVE':need(current[d]==e[2],'MOVE chart');current[d]=e[3]
  elif op=='SCALE':need(current[d]==e[3],'SCALE chart');c=F(e[2]);need(c!=0,'nonzero SCALE');rows[d]={j:c*v for j,v in rows[d].items()};versions[d]=i
  elif op in ('ADD','COPY'):
   need(d!=e[2] and current[d]==current[e[2]]==e[4],'cochart scalar');c=F(e[3]);need(c!=0,'nonzero ADD')
   if op=='COPY':need(not rows[d],'COPY-zero homogeneous guard')
   add(rows[d],rows[e[2]],c);versions[d]=i
  else:raise ValueError('unknown opcode')
 need(checked==sorted(wanted),'all witness cuts checked');need(current[:n]==w['final'] and all(x is None for x in current[n:]),'source final charts/owned')
 need(ranks==Counter({1:6,2:1,3:1,4:1,6:1}) and ordinary_terms==32,'witness inventory')
 return {'status':'PASS_TEN_CURRENT_COCHART_OWNED_DIFFERENCE_DELIVERIES','source_sha256':PIN,'certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),'source_events':len(w['program']),'events':checked,'removed_differential_move_histogram':dict(sorted(ranks.items())),'virtual_observer_terms':ordinary_terms,'observer_kind_terms':dict(observer_counts),'controls':{'coefficient_mutants':coefficient_controls,'dirty_helper_common_equality_failures':dirty_controls,'source_hash_mutation':1,'stale_observer_version_pins':10,'actual_stale_observer_rows':actual_stale_controls},'scope':'Ten exact current-source differential identities and conditional delivery substitutions. Physical helper/owned difference observations remain premises; no H4 native or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=default_source());p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json');p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.certificate);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
