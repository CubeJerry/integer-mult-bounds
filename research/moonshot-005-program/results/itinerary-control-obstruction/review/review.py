"""Separate offline interval-join checker for the prescribed-pulse duals."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def space(b):
 out={0}
 for v in b:out|={x^v for x in tuple(out)}
 return frozenset(out)
def run(repo,packet):
 pins=json.loads(Path(__file__).with_name('REVIEWED-FILES.json').read_text())
 for name,pin in pins.items():need(hashlib.sha256((packet/name).read_bytes()).hexdigest()==pin,'reviewed '+name)
 cert=json.loads((packet/'CERTIFICATE.json').read_text());raw=(repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE,'source pin');w=json.loads(gzip.decompress(raw));P=w['program'];N=len(P);C=list(map(space,w['frames']))
 M=set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 routes={j:[C[w['initial'][j]]] for j in M};loc=dict(enumerate(w['initial']));starts={j:0 for j in loc};life=collections.defaultdict(list)
 coeff={k:F(o[3] if o[0] in ('ADD','COPY') else o[2]) for k,o in enumerate(P) if o[0] in ('ADD','COPY','SCALE')}
 for k,o in enumerate(P):
  tag,j=o[:2]
  if tag=='MOVE':
   need(loc[j]==o[2],'source route location');life[j].append((starts[j],k+1,C[loc[j]]));loc[j]=o[3];starts[j]=k+1
   if j in M:routes[j].append(C[o[3]])
  elif tag=='INIT':need(j not in loc,'source lifetime fresh');loc[j]=o[2];starts[j]=k+1
  elif tag=='CLEAR':life[j].append((starts[j],k+1,C[loc[j]]));del loc[j];del starts[j]
 for j,c in loc.items():life[j].append((starts[j],N+1,C[c]))
 def adjoint_intervals(ell):
  values=collections.defaultdict(F,ell);ends=collections.defaultdict(lambda:N+1);out=collections.defaultdict(list)
  for k in range(N-1,-1,-1):
   o=P[k];tag,j=o[:2];updates={}
   if tag=='ADD':updates[o[2]]=values[o[2]]+coeff[k]*values[j]
   elif tag=='SCALE':updates[j]=coeff[k]*values[j]
   elif tag=='COPY':need(j!=o[2],'distinct COPY');updates[o[2]]=values[o[2]]+coeff[k]*values[j];updates[j]=F(0)
   elif tag in ('INIT','CLEAR'):updates[j]=F(0)
   for r,v in updates.items():
    old=values[r]
    if v==old:continue
    if old:out[r].append((k+1,ends[r],old))
    ends[r]=k+1;values[r]=v
  for r,v in values.items():
   if v:out[r].append((0,ends[r],v))
  return {r:sorted(rows) for r,rows in out.items()}
 def overlap(segments,stations,cut):
  for role,ss in segments.items():
   ll=life[role];i=j=0
   while i<len(ss) and j<len(ll):
    a,b,v=ss[i];c,d,chart=ll[j]
    if chart in stations and max(a,c,cut)<min(b,d):return(role,max(a,c,cut),v)
    if b<=d:i+=1
    else:j+=1
  return None
 def at(segments,role,cut):
  return next((v for a,b,v in segments.get(role,[]) if a<=cut<b),F(0))
 cache={};records=[]
 for case in cert['cases']:
  k=case['event'];x=case['donor'];h=case['helper'];o=P[k];need(o[0]=='MOVE' and o[1]==h and h<w['public'] and h not in M,'actual public helper departure');need(x in M and routes[x][-1]==C[127],'main donor ends at hub');start=routes[x].index(C[o[2]]);stations=set(routes[x][start:]);cut=k+1
  ell={int(j):F(v) for j,v in case['dual_final_output_functional'].items()};need(1<=len(ell)<=3,'small endpoint functional');need(all(j<w['public'] and C[w['final'][j]]!=C[127] for j in ell),'off-hub support')
  key=tuple(sorted(ell.items()))
  if key not in cache:cache[key]=adjoint_intervals(ell)
  segments=cache[key];need(at(segments,h,cut)==1,'unit uncancellable response');need(overlap(segments,stations,cut) is None,'all future station/cut adjoints vanish')
  need(overlap(segments,stations|{C[o[3]]},cut) is not None,'new destination access breaks premise')
  records.append({'event':k,'donor':x,'helper':h,'endpoint_terms':len(ell),'pulse_response':'1','future_station_intersection_empty':True})
 need(len(records)==103 and len({(r['event'],r['donor']) for r in records})==103,'103 distinct cases');need(len({r['event'] for r in records})==58,'58 departures')
 return {'status':'PASS_INDEPENDENT_INTERVAL_JOIN_103_PULSE_DUALS','source_sha256':SOURCE,'reviewed_files':pins,'cases':records,'case_count':len(records),'departure_events':58,'distinct_endpoint_functionals':len(cache),'method':'Independent backward adjoint intervals, separately built forward source location/lifetime intervals, then offline intersection for all future stations. No author/search code imported.','negative_control':'Adding each actual destination creates a nonzero adjoint intersection.','scope':'103 prescribed-pulse/donor cases, not a global or joint-initial-pulse impossibility.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repository',type=Path,required=True);a.add_argument('--packet',type=Path,required=True);a.add_argument('--output',type=Path,required=True);x=a.parse_args();r=run(x.repository,x.packet);x.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
