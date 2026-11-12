import gzip,json,time,hashlib,sys,runpy
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
B=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds');O=Path(__file__).resolve().parent;start=time.monotonic();source_path=Path(sys.argv[1]) if len(sys.argv)>1 else B/'research/shared-wire-split-composition/data/final.json.gz';source=source_path.read_bytes();w=json.loads(gzip.decompress(source));hp=O/'CERTIFICATE.json.gz';payload=gzip.decompress(hp.read_bytes());h=json.loads(payload);P=w['program'];n=w['public'];z=F(0);C=[];sp=[];seen={}
if hashlib.sha256(source).hexdigest()!=h['source_sha256']:raise ValueError('sourcepin')
for k,fr in enumerate(w['frames']):
 s={0}
 for b in fr:s.update(t^b for t in tuple(s))
 s=frozenset(s);seen.setdefault(s,k);C.append(seen[s]);sp.append(s)
derived=runpy.run_path(str(O/'derive_quotient.py'))['res']
for got,want in zip(derived['receivers'],h['receivers']):
 for key in ['receiver_X2','donor_Y2','receiver_route','donor_route','initial_observation_count','known_offhub_coordinate_count','nonhub_arrival_count','quotient_arrival_rank']:
  if got[key]!=want[key]:raise ValueError(('quotient metadata',key))
 if len(got['null_relations'])!=len(want['null_relations']):raise ValueError('kernel completeness rank')
 for ga,wa in zip(got['null_relations'],want['null_relations']):
  if ga['arrival_terms']!=wa['arrival_terms'] or ga['initial_terms']!=wa['initial_terms']:raise ValueError('regenerated kernel basis')
recs=h['receivers'];rels=[];owners=[];local=[];obs=defaultdict(list);a=[{} for _ in range(n+w['owned_fields'])];allowed=[set(r['donor_route']) for r in recs];ports=[w['ports'][r['port_index']] for r in recs]
for i,r in enumerate(recs):
 port=ports[i];H=frozenset(v for v in range(512) if (v&port).bit_count()%2==0)
 if port.bit_count()%2!=1 or sp[w['initial'][r['receiver_X2']]]!=frozenset((0,port)) or sp[w['final'][r['donor_Y2']]]!=H:raise ValueError('source odd-port endpoints')
 if not all(sp[c]<=H for c in r['donor_route']):raise ValueError('donor hyperplane itinerary')
 if not all(port in sp[c] for c in r['receiver_route']):raise ValueError('receiver upward itinerary')
for e in P:
 if e[0]!='MOVE' and C[e[-1]]==127:
  if e[0] not in ('ADD','SCALE') or e[1]>=n or (e[0]=='ADD' and e[2]>=n):raise ValueError('invertible public hub scalar map')
for i,r in enumerate(recs):
 for k,rel in enumerate(r['null_relations']):
  label=len(rels);rels.append(rel);owners.append(i);local.append(k)
  for it in rel['final_hub_terms']:a[it['role']][label]=F(it['coefficient'])
  for it in rel['arrival_terms']:obs[it['after_event']].append((it['role'],label,F(it['coefficient'])))
loc=dict(enumerate(w['final']));checks=0;outside={};station_bad=[];support=[set() for _ in recs]
def add(a,b,c):
 for k,v in tuple(b.items()):
  q=a.get(k,z)+c*v
  if q:a[k]=q
  else:a.pop(k,None)
def inspect(j,t):
 global checks
 if j not in loc or not a[j]:return
 c=C[loc[j]]
 for k,v in a[j].items():
  i=owners[k];support[i].add(c);checks+=1
  if c in allowed[i]:station_bad.append({'receiver':recs[i]['receiver_X2'],'donor':recs[i]['donor_Y2'],'relation':local[k],'before_event':t,'role':j,'chart':loc[j],'response':str(v)})
  if ports[i] not in sp[c]:outside.setdefault((i,c),{'receiver':recs[i]['receiver_X2'],'donor':recs[i]['donor_Y2'],'relation':local[k],'before_event':t,'role':j,'chart':loc[j],'response':str(v)})
for j in loc:inspect(j,len(P))
for t in range(len(P)-1,-1,-1):
 for j,k,v in obs.get(t,[]):
  q=a[j].get(k,z)+v
  if q:a[j][k]=q
  else:a[j].pop(k,None)
 e=P[t];op,j=e[:2]
 if op=='ADD':add(a[e[2]],a[j],F(e[3]));inspect(e[2],t)
 elif op=='SCALE':q=F(e[2]);a[j]={k:q*v for k,v in a[j].items()};inspect(j,t)
 elif op=='COPY':add(a[e[2]],a[j],F(e[3]));a[j]={};inspect(e[2],t)
 elif op=='MOVE':loc[j]=e[2];inspect(j,t)
 elif op=='CLEAR':loc[j]=e[2];a[j]={}
 elif op=='INIT':loc.pop(j);a[j]={}
if outside:raise ValueError(('upper cone support',list(outside.values())[:2]))
if station_bad:raise ValueError(('donor-route response',station_bad[:2]))
extra={'receiver':recs[0]['receiver_X2'],'donor':recs[0]['donor_Y2'],'before_event':0,'role':recs[0]['receiver_X2'],'chart':w['initial'][recs[0]['receiver_X2']],'relation':0,'response':str(a[recs[0]['receiver_X2']].get(0,z))}
if not F(extra['response']):raise ValueError('extra-chart sensitivity control')
for k,r in enumerate(rels):
 for it in r['initial_terms']:
  j=it['role'];q=a[j].get(k,z)+F(it['coefficient'])
  if q:a[j][k]=q
  else:a[j].pop(k,None)
if any(a):raise ValueError('complete common baseline identity')
# An omitted nonzero initial observation coefficient breaks the first relation.
first=rels[0]['initial_terms'][0];omitted={'mutation':'omit first initial-history term','input_role':first['role'],'source_input_residual':str(-F(first['coefficient']))}
if not F(omitted['source_input_residual']):raise ValueError('bad mutation control')
# The hub arrival map is square and local; no operation transports data out.
hub_moves=[(t,e) for t,e in enumerate(P) if e[0]=='MOVE' and C[e[3]]==127];leaves=[(t,e) for t,e in enumerate(P) if e[0]=='MOVE' and C[e[2]]==127]
if leaves or len(hub_moves)!=1022 or any(e[4] for t,e in hub_moves):raise ValueError('absorbing public hub')
out={'status':'PASS_ALL96_REVERSE_HISTORY_DIRECT_ADJOINTS','source_sha256':h['source_sha256'],'complete_history_payload_sha256':hashlib.sha256(payload).hexdigest(),'receiver_count':96,'relations':len(rels),'nonhub_arrivals':h['nonhub_arrival_count'],'nonzero_adjoint_entries_checked':checks,'forbidden_donor_route_entries':len(station_bad),'all_baseline_null_identities_verified':True,'hub_arrivals':1022,'hub_departures':0,'upper_cone_exceptions':list(outside.values()),'support_charts':[{'receiver_X2':r['receiver_X2'],'donor_Y2':r['donor_Y2'],'port':ports[i],'charts':sorted(support[i])} for i,r in enumerate(recs)],'negative_controls':[extra,omitted],'claim':'Every one of1859 complete original reverse receiver-history null relations has adjoint support only on charts containing its receiver port. In particular it has zero response at every live native role and every source cut on any chart contained in that port orthogonal hyperplane, including every original or monotonically retargeted donorY2 route. Thus q-only additive controls at those charts, including arbitrary chart3 precompensation, cannot create a new clean history gain once all common endpoints are restored. All actual prehub route observations are included.','scope':'Fixed common-input observation map. Common-dependent replacement, dirty swaps, mixedraw records, remapped raw carriers or a changed native are outside this claim. The direct adjoint identity needs no COPY-guard assumption.'}
(O/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print({'relations':len(rels),'checked':checks,'forbidden':len(station_bad),'upper_cone_exceptions':len(outside),'exception_examples':list(outside.values())[:3],'negative':extra,'seconds':round(time.monotonic()-start,3)},flush=True)
