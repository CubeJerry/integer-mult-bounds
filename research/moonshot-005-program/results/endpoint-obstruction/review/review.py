#!/usr/bin/env python3
"""Independent backward-time graph and reverse-adjoint endpoint audit."""
import argparse,bisect,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,m):
 if not c:raise ValueError(m)
def span(v):
 s={0}
 for x in v:s|={x^y for y in tuple(s)}
 return frozenset(s)
def add(row,k,v):
 a=row.get(k,F(0))+v
 if a:row[k]=a
 else:row.pop(k,None)
def adjoint(P,o):
 a={o:F(1)}
 for e in reversed(P):
  op,d=e[:2];c=a.get(d,F(0))
  if op=='ADD':
   if c:add(a,e[2],c*F(e[3]))
  elif op=='SCALE':
   if c:a.pop(d);add(a,d,c*F(e[2]))
  elif op=='COPY':
   a.pop(d,None)
   if c:add(a,e[2],c*F(e[3]))
  elif op in ('INIT','CLEAR'):a.pop(d,None)
  else:need(op=='MOVE','recognized operator')
 return a
def backward(edges,sink,preloads):
 A={sink}
 for _,s,d in reversed(edges):
  if d in A:A.add(s)
 if any(d in A for _,s,d in preloads):
  A.update(s for _,s,d in preloads if d in A)
 return A
def run(source,packet,preloads):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 w=json.loads(gzip.decompress(raw));P=w['program'];end=len(P);N=w['public']
 M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 C=[span(f) for f in w['frames']];need(len(M)==400 and len(set(C))==1094,'source census')
 entry_grants=[(-1,C[3],C[d]) for d in (470,431,394,520)]
 # Independent main event-indexed itineraries and subsequent matching arrivals.
 times={r:[-1] for r in M};locations={r:[C[w['initial'][r]]] for r in M}
 touches={r:[] for r in range(N+w['owned_fields'])}
 for k,e in enumerate(P):
  touches[e[1]].append(k)
  if e[0] in ('ADD','COPY'):touches[e[2]].append(k)
  if e[0]=='MOVE' and e[1] in M:times[e[1]].append(k);locations[e[1]].append(C[e[3]])
 loans=[]
 for k,e in enumerate(P):
  if e[0]!='MOVE' or e[1] in M:continue
  h,src,dst=e[1:4];t=touches[h];at=bisect.bisect_right(t,k);deadline=t[at] if at<len(t) else end
  for r in sorted(M):
   j=bisect.bisect_left(times[r],k)-1
   if locations[r][j]!=C[src]:continue
   for close,loc in zip(times[r][j+1:],locations[r][j+1:]):
    if close>=deadline:break
    if close>k and loc==C[dst]:loans.append((k,close,h,r,src,dst,deadline))
 starts={a[0] for a in loans};need(len(loans)==354 and len(starts)==141,'independent quiet census')
 funded=[(k,C[e[2]],C[e[3]]) for k,e in enumerate(P) if e[0]=='MOVE' and (e[1] in M or e[4])]
 augmented=[(k,C[e[2]],C[e[3]]) for k,e in enumerate(P) if e[0]=='MOVE' and (e[1] in M or e[4] or k in starts)]
 all_edges=[(k,C[e[2]],C[e[3]]) for k,e in enumerate(P) if e[0]=='MOVE'];need(len(funded)==1757,'funded grants')
 cert=json.loads((packet/'CERTIFICATE.json').read_text());pairs=cert['witness_pairs'];K={x['input'] for x in pairs}
 need(len(K)==len({x['output'] for x in pairs})==len(pairs)==46,'distinct square witness')
 rows=[];det=F(1)
 for q in pairs:
  o,x=q['output'],q['input'];dest=C[w['final'][o]]
  need(w['final'][o]==q['target_chart'] and len(C[w['initial'][x]])==2,'endpoint and initial input')
  for edges,pre in ((funded,[]),(augmented,[]),(augmented,entry_grants)):
   A=backward(edges,dest,pre);need(all(C[w['initial'][j]] not in A for j in K),'all46 directions absent at every selected sink')
  actual={j:a for j,a in adjoint(P,o).items() if j in M};restricted={j:a for j,a in actual.items() if j in K}
  need(restricted=={x:F(q['coefficient'])},'reverse diagonal restriction');need(F(q['coefficient']) in (F(1),F(1,2)),'coefficient')
  det*=F(q['coefficient']);rows.append({'output':o,'row':{str(j):str(a) for j,a in sorted(actual.items())}})
  need(C[w['initial'][x]] in backward(all_edges,dest,[]),'all-helper escape breaks exclusion')
 need(det==F(1,8),'rank46 determinant')
 pre=json.loads(preloads.read_text())
 for p in pre['preloads']:need(all(j not in K for j,a in p['row'] if F(a)),'existing preloads project tozero')
 wrong=F(pairs[0]['coefficient'])+1;need(wrong!=F(rows[0]['row'][str(pairs[0]['input'])]),'wrong coefficient control')
 need(all(C[w['initial'][j]] in set(C) for j in K),'global input grants defeat exclusion')
 encoded=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode()
 return {'status':'PASS_INDEPENDENT_BACKWARD_ENDPOINT_46','source_sha256':PIN,'certificate_sha256':hashlib.sha256((packet/'CERTIFICATE.json').read_bytes()).hexdigest(),'selected_endpoint_rows_reversed':46,'selected_sink_input_exclusions_checked_per_graph':2116,'graph_variants':3,'quiet_windows':len(loans),'quiet_start_events':len(starts),'funded_main_owned_events':len(funded),'rank_lower_bound':46,'determinant':str(det),'preload_projection_rank':0,'all_helper_escape_sink_controls':46,'selected_rows_sha256':hashlib.sha256(encoded).hexdigest(),'method':'Backward temporal ancestors and independent reverse adjoints; no author implementation imported.','scope':'Endpoint-only bound on granted graph;46 is not claimed optimal and outside transmissions need not all be new paid jobs.'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ('source','packet','preloads','output'):p.add_argument('--'+key,type=Path,required=True)
 a=p.parse_args();r=run(a.source,a.packet,a.preloads);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
