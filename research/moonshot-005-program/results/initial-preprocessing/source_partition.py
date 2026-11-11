#!/usr/bin/env python3
"""Exact chart-cut certificate for initial-only four-return preloads."""
import argparse,gzip,hashlib,json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='d46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b'
def need(v,s):
 if not v:raise ValueError(s)
def rank(rows):
 B={}
 for src in rows:
  a=dict(src)
  while a:
   p=min(a)
   if p not in B:
    c=a[p];B[p]={k:v/c for k,v in a.items()};break
   c=a[p]
   for k,v in B[p].items():
    a[k]=a.get(k,Q(0))-c*v
    if not a[k]:del a[k]
 return len(B)
def add(a,b,c):
 for k,v in b.items():
  a[k]=a.get(k,Q(0))+c*v
  if not a[k]:del a[k]
def span(f):
 s={0}
 for v in f:s|={x^v for x in s}
 return tuple(sorted(s))
def run(source,certificate):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source SHA256');cr=certificate.read_bytes();need(hashlib.sha256(cr).hexdigest()==CERT,'certificate SHA256');w=json.loads(gzip.decompress(raw));cs=json.loads(cr);want={c['event']:c for c in cs};p=w['public'];n=p+w['owned_fields'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400,'400 difference inputs');F=list(map(span,w['frames']));initial={r:F[w['initial'][r]] for r in M};rows=[{r:Q(1)} if r in M else {} for r in range(n)];cur=w['initial'][:]+[None]*(n-p);live=set(range(p));visits={r:{initial[r]:-1} for r in M};found=[]
 for i,e in enumerate(w['program']):
  op,r=e[:2]
  if i in want:
   c=want[i];need(e==['MOVE',c['owner'],c['from'],c['to'],True],'pinned return');target={int(k):Q(v) for k,v in c['target_row'].items()};need(rows[r]==target,'source-derived return');entry={k:v for k,v in target.items() if initial[k]==(0,)};distributed={k:v for k,v in target.items() if initial[k]!=(0,)};dest=F[c['to']];missing=[k for k in distributed if dest not in visits[k]];found.append({'event':i,'owner':r,'destination':c['to'],'row':{str(k):str(v) for k,v in target.items()},'support':len(target),'entry_support':len(entry),'distributed_support':len(distributed),'distributed_initial_charts':len({initial[k] for k in distributed}),'raw_q_target_visits':len(distributed)-len(missing),'missing_raw_q_roles':sorted(missing)})
  if op=='INIT':need(r>=p and r not in live,'INIT');live.add(r);rows[r]={};cur[r]=e[2]
  elif op=='CLEAR':need(r>=p and r in live and cur[r]==e[2],'CLEAR');live.remove(r);rows[r]={};cur[r]=None
  elif op=='MOVE':
   need(r in live and cur[r]==e[2] and e[4]==(r>=p),'MOVE ownership/chart');a,b=set(F[e[2]]),set(F[e[3]]);need(a<b or r>=p and b<a,'MOVE nesting');cur[r]=e[3]
   if r in M:visits[r].setdefault(F[e[3]],i)
  elif op in ('ADD','COPY'):
   s=e[2];need(r!=s and r in live and s in live and cur[r]==cur[s]==e[4],'scalar cochart/live')
   if op=='COPY':need(not rows[r],'COPY zero')
   add(rows[r],rows[s],Q(e[3]))
  elif op=='SCALE':need(r in live and cur[r]==e[3],'SCALE chart');rows[r]={k:v*Q(e[2]) for k,v in rows[r].items()}
  else:raise ValueError(op)
 need(len(found)==4 and not live-set(range(p)),'four returns and cleanup');full=[{int(k):Q(v) for k,v in c['row'].items()} for c in found];D=[{k:v for k,v in a.items() if initial[k]!=(0,)} for a in full];E=[{k:v for k,v in a.items() if initial[k]==(0,)} for a in full];groups=defaultdict(set)
 for r in M:groups[initial[r]].add(r)
 cuts=[]
 for f,inputs in sorted(groups.items()):
  restrict=[{k:v for k,v in a.items() if k in inputs} for a,c in zip(full,found) if F[c['destination']]!=f];rho=rank(restrict)
  if rho:cuts.append({'initial_chart_span':list(f),'rank':rho,'input_roles':sorted(set().union(*(set(a) for a in restrict)))})
 need(rank(D)==4 and rank(E)==4,'four independent distributed and entry forms');need(sum(c['rank'] for c in cuts)==105,'chart-cut floor105');need(len([c for c in cuts if c['initial_chart_span']!=[0]])==101,'101 nonempty source charts');need(all(c['raw_q_target_visits']==0 for c in found),'zero raw-q destination contacts');need(full[0].get(4)==Q(-3,4) and initial[4]!=(0,),'chart3-only q4 negative control');need(rank([D[0]]*4)==1 and rank([{}]*4)==0,'duplicate/zero controls')
 return {'status':'PASS_EXACT_INITIAL_CHART_CUT_CERTIFICATE','source_sha256':PIN,'historical_certificate_sha256':CERT,'events_replayed':len(w['program']),'independent_difference_inputs':400,'returns':found,'distributed_rank':4,'entry_rank':4,'nonentry_union_support':len(set().union(*(set(a) for a in D))),'chart_cuts':cuts,'initial_only_preload_departure_floor':105,'negative_controls':{'chart3_only_q4_target_value':'-3/4','duplicate_output_component_rank':1,'zero_component_rank':0},'scope':'These four full returned rows must be constructed at their destinations before any source instruction. Arbitrary dynamic aggregation using funded source moves and the full joint code remain open. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();d=run(a.source,a.certificate);s=json.dumps(d,sort_keys=True,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in d.items() if k not in ('returns','chart_cuts')},sort_keys=True,indent=2))
