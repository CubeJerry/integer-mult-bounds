#!/usr/bin/env python3
"""Independent full dirty-input and dual-certificate historical row review."""
import argparse,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,m):
 if not c:raise ValueError(m)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,Q(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def enc(row):return {str(j):str(v) for j,v in sorted(row.items())}
def run(source,certificate):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));C=json.loads(certificate.read_text());need([a['event'] for a in C]==[28141,33554,34467,37597],'four exact targets')
 M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);n=w['public'];N=n+w['owned_fields'];rows=[{r:Q(1)} if r<n else {} for r in range(N)];cur=w['initial']+[None]*w['owned_fields'];ver=[-1]*N;snaps={};wanted={};targets={a['event']:a for a in C};counts={a['event']:0 for a in C};reviews=[]
 for a in C:
  for t in a['witnesses']['all']:
   o=t['observation'];key=(o['event'],o['role']);need(key not in wanted,'distinct named snapshots');wanted[key]=o
 def dot(row,a):return sum((row.get(int(j),Q(0))*Q(v) for j,v in a['owned_main_obstruction']['functional'].items()),Q(0))
 def check_history(r,i):
  if r<n and r not in M:return
  for a in C:
   if i<a['event'] and cur[r]==a['to']:
    need(dot(rows[r],a)==0,'dual kills every historical owned/main version');counts[a['event']]+=1
 for r in range(n):check_history(r,-1)
 for i,e in enumerate(w['program'][:max(targets)+1]):
  op,r=e[:2]
  if i in targets:
   a=targets[i];need(e==['MOVE',a['owner'],a['from'],a['to'],True],'target route');need(cur[r]==a['from'],'target current source chart');need(a['rank']==abs(len(w['frames'][a['from']])-len(w['frames'][a['to']])),'exact target Gaussian rank');need(enc({j:v for j,v in rows[r].items() if j in M})==a['target_row'],'independent target homogeneous row');response=dot(rows[r],a);need(response!=0 and str(response)==a['owned_main_obstruction']['target_response'],'dual nonzero target')
   residual=rows[r].copy();wrong=rows[r].copy();current=rows[r].copy();current_type_ok=True;terms=[]
   for k,t in enumerate(a['witnesses']['all']):
    o=t['observation'];key=(o['event'],o['role']);need(key in snaps and o['event']<i and o['chart']==a['to'],'earlier cochart snapshot');full=snaps[key];co=Q(t['coefficient']);add(residual,full,-co);add(wrong,full,co if k==0 else -co);add(current,rows[o['role']],-co);current_type_ok=current_type_ok and cur[o['role']]==a['to'];terms.append({'coefficient':str(co),'role':o['role'],'snapshot_after_event':o['event'],'value_version_event':o['value_version_event'],'kind':o['kind']})
   need(not any(j in M for j in residual),'all dirty-input main coefficients cancel');need(bool(residual),'ordinary common rows do not obey the difference identity');need(any(j in M for j in wrong),'wrong-sign control');need(not current_type_ok or any(j in M for j in current),'historical-to-current substitution control')
   reviews.append({'event':i,'target':r,'snapshot_terms':terms,'dirty_helper_residual':enc(residual),'nonzero_dirty_helper_counterexample':next(iter(enc(residual).items())),'historical_owned_main_versions_checked':counts[i],'owned_main_dual_response':str(response),'wrong_sign_rejected':True,'current_substitution_rejected':True,'scope':'Identity of two-copy differences with the same arbitrary helper input. Snapshot availability and lifecycle remain physical premises.'})
  if op=='MOVE':need(cur[r]==e[2],'source MOVE current chart');cur[r]=e[3]
  elif op=='INIT':need(cur[r] is None,'source init');rows[r]={};cur[r]=e[2];ver[r]=i
  elif op=='CLEAR':need(cur[r]==e[2],'source clear');rows[r]={};cur[r]=None;ver[r]=i
  elif op=='SCALE':need(cur[r]==e[3] and Q(e[2])!=0,'source scale');rows[r]={j:v*Q(e[2]) for j,v in rows[r].items()};ver[r]=i
  elif op in ('ADD','COPY'):
   need(cur[r]==cur[e[2]]==e[4],'source cochart update')
   if op=='COPY':need(not rows[r],'full dirty-input COPYzero')
   add(rows[r],rows[e[2]],Q(e[3]));ver[r]=i
  else:raise ValueError(op)
  key=(i,r)
  if key in wanted:
   o=wanted[key];need(o['phase']=='after' and cur[r]==o['chart'] and ver[r]==o['value_version_event'] and op==o['operation'],'exact snapshot event/version/chart');kind='owned' if r>=n else 'main' if r in M else 'helper';need(kind==o['kind'],'snapshot physical kind');need(enc({j:v for j,v in rows[r].items() if j in M})==o['row'],'full-source projected snapshot');snaps[key]=rows[r].copy()
  check_history(r,i)
 need(len(snaps)==9 and len(reviews)==4,'complete9term packet')
 return {'status':'PASS_INDEPENDENT_HISTORICAL_OWNED_ROWS','source_sha256':PIN,'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'formal_common_input_columns':n,'identities':len(reviews),'snapshots':len(snaps),'helper_snapshots':sum(o['kind']=='helper' for o in wanted.values()),'owned_snapshots':sum(o['kind']=='owned' for o in wanted.values()),'reviews':reviews,'scope':'Four exact finite source identities plus explicit linear-functional exclusions for prior literal owned/main histories. No current-helper oracle, snapshot-free implementation or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.certificate);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k!='reviews'},indent=2,sort_keys=True))
