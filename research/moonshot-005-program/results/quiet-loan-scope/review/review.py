#!/usr/bin/env python3
"""Independent geometric sandwich review of quiet-loan endpoint scope."""
import argparse,gzip,hashlib,json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,m):
 if not c:raise ValueError(m)
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return frozenset(s)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,Q(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def run(source,author,loan_audit):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));M=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));ms=set(M);fs=list(map(span,w['frames']));cur=w['initial']+[None]*w['owned_fields'];rows=[{r:Q(1)} if r in ms else {} for r in range(len(cur))]
 groups=defaultdict(set);reach={r:{r} for r in M}
 for r in M:groups[cur[r]].add(r)
 def spread(f):
  u=set().union(*(reach[r] for r in groups[f]))
  for r in groups[f]:reach[r]=u.copy()
 for f in list(groups):spread(f)
 nmove=0
 for e in w['program']:
  op,r=e[:2]
  if op in ('ADD','COPY'):
   need(cur[r]==cur[e[2]]==e[4],'source scalar cochart')
   if op=='COPY':need(not rows[r],'homogeneous COPYzero')
   add(rows[r],rows[e[2]],Q(e[3]))
  elif op=='SCALE':need(cur[r]==e[3],'source scale chart');rows[r]={j:v*Q(e[2]) for j,v in rows[r].items()}
  elif op in ('INIT','CLEAR'):rows[r]={};cur[r]=e[2] if op=='INIT' else None
  elif op=='MOVE':
   a,b=e[2:4];need(cur[r]==a,'source MOVE frame')
   if r in ms:
    need(fs[a]<fs[b],'every actual main route is a strict geometric inclusion');groups[a].remove(r);groups[b].add(r);spread(b);nmove+=1
   cur[r]=b
  else:raise ValueError(op)
 required=[];forbidden=[];missing=[]
 for r in M:
  need(all(fs[w['initial'][j]]<=fs[cur[r]] for j in reach[r]),'main reachability obeys containment')
  for j,c in sorted(rows[r].items()):
   if j==r:continue
   rec={'output':r,'input':j,'coefficient':str(c),'input_frame':w['initial'][j],'output_frame':cur[r]};required.append(rec)
   if not fs[w['initial'][j]]<=fs[cur[r]]:forbidden.append(rec)
   if j not in reach[r]:missing.append(rec)
 need(len(required)==208 and len(forbidden)==104 and missing==forbidden,'exact endpoint sandwich')
 # Even the no-stationary-cache main graph reaches every nonforbidden coefficient.
 # Every eligible quiet loan goes from a main donor's current chart to its later
 # chart, so strict main ascents imply it preserves the same containment bound.
 a=json.loads(author.read_text());need(a['source_sha256']==PIN and a['source_main_moves']==nmove,'author source and route count');need(a['forbidden_terms']==forbidden and a['blocked_terms']==forbidden,'author full endpoint lists');need(a['optimistic_reachable_without_loans']==a['optimistic_reachable_with_loans']==104 and not a['newly_reachable_terms'],'author reachability counts')
 c=json.loads(loan_audit.read_text());need(c['source_sha256']==PIN and c['status']=='PASS_EXACT_RAW_QUIET_CONTACT_REDUNDANCY','independent interval audit');need(c['quiet_single_MOVE_loans']==a['quiet_loans']==354,'independent quiet census')
 # A constant empty-chart source passes containment for every output; the
 # geometric failure is specific to noncontained input frames, not all routing.
 empty=next(f for f,s in enumerate(fs) if s==frozenset({0}));need(all(fs[empty]<=fs[cur[r]] for r in M),'empty-chart positive control')
 return {'status':'PASS_INDEPENDENT_QUIET_ENDPOINT_SCOPE','source_sha256':PIN,'formal_main_input_columns':len(M),'source_main_moves':nmove,'required_offdiagonal_terms':len(required),'independently_geometrically_forbidden_terms':len(forbidden),'already_reachable_in_main_only_current_holder_relaxation':len(required)-len(missing),'quiet_loans_from_independent_interval_census':c['quiet_single_MOVE_loans'],'all_author_endpoint_rows_match':True,'scope':'Geometric sandwich checks exact finite endpoint census. Individual reachability is not simultaneous code feasibility. The inherited monotone obstruction excludes these104 terms for main plus ascending quiet loans only, not arbitrary descending coded routes.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author-result',type=Path,required=True);p.add_argument('--independent-loan-audit',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.author_result,a.independent_loan_audit);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
