import gzip,json,time,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
B=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds');O=Path(__file__).resolve().parent;start=time.monotonic();z=F(0);source=Path(sys.argv[1]) if len(sys.argv)>1 else B/'research/shared-wire-split-composition/data/final.json.gz';w=json.loads(gzip.decompress(source.read_bytes()));P=w['program'];n=w['public'];C=[];seen={}
for k,f in enumerate(w['frames']):
 s={0}
 for v in f:s.update(t^v for t in tuple(s))
 s=frozenset(s);seen.setdefault(s,k);C.append(seen[s])
host=w['hosted'];pairs=list(zip(host['Dports'],host['X2'],host['Y2']));routes={j:[C[w['initial'][j]]] for _,x,y in pairs for j in [x,y]}
for e in P:
 if e[0]=='MOVE' and e[1] in routes:routes[e[1]].append(C[e[3]])
H=set(host['Dports']);off={j for j,c in enumerate(w['final']) if C[c]!=127};tin=[{j:F(1)} for j in range(n)]
for i,x in enumerate(w['live']):
 y=x+112
 if i in H:tin[y]={y:F(1),x:F(-1)}
 else:tin[x]={x:F(1,2),y:F(1)};tin[y]={x:F(-1,2),y:F(1)}
for x,y in zip(host['X2'],host['Y2']):tin[x]={x:F(1),y:F(1)}
rows=[{k:v for k,v in t.items() if k in off} for t in tin]+[{} for _ in range(w['owned_fields'])];rch=[set(routes[x]) for _,x,y in pairs];by=defaultdict(list);known=[];initial=[];records=[[] for _ in pairs]
for i,R in enumerate(rch):
 for c in R-{127}:by[c].append(i)
 ini=[j for j,c in enumerate(w['initial']) if C[c] in R];initial.append(ini);km={}
 for j in ini:
  vals=rows[j];
  if vals:
   if len(vals)!=1:raise ValueError('nonsingleton known initial projection')
   k,v=next(iter(vals.items()));km.setdefault(k,(j,v))
 known.append(km)
def add(a,b,c):
 for k,v in tuple(b.items()):
  q=a.get(k,z)+c*v
  if q:a[k]=q
  else:a.pop(k,None)
for t,e in enumerate(P):
 op,j=e[:2]
 if op=='ADD':add(rows[j],rows[e[2]],F(e[3]))
 elif op=='SCALE':q=F(e[2]);rows[j]={k:q*v for k,v in rows[j].items()}
 elif op=='COPY':rows[j]={k:F(e[3])*v for k,v in rows[e[2]].items()}
 elif op in('INIT','CLEAR'):rows[j]={}
 elif op=='MOVE':
  if C[e[3]]==127:
   if rows[j]:raise ValueError('hub arrival has offhub-final source component')
  else:
   for i in by[C[e[3]]]:records[i].append({'after_event':t,'role':j,'chart':e[3],'row':rows[j].copy()})
for j in range(n):
 if rows[j]!=({j:F(1)} if j in off else{}):raise ValueError(('inverse source transform',j))
out=[]
for i,(port,x,y) in enumerate(pairs):
 basis={};relations=[]
 for k,r in enumerate(records[i]):
  a={j:v for j,v in r['row'].items() if j not in known[i]};combo={k:F(1)}
  while a:
   p=min(a);q=a[p]
   if p not in basis:basis[p]=({j:v/q for j,v in a.items()},{j:v/q for j,v in combo.items()});break
   br,bc=basis[p];add(a,br,-q);add(combo,bc,-q)
  if not a:
   projected={}
   for k,c in combo.items():add(projected,records[i][k]['row'],c)
   if any(j not in known[i] for j in projected):raise ValueError('known-coordinate quotient relation')
   it=[{'role':known[i][j][0],'chart':w['initial'][known[i][j][0]],'coefficient':str(-v/known[i][j][1])} for j,v in sorted(projected.items())]
   at=[{'after_event':records[i][k]['after_event'],'role':records[i][k]['role'],'chart':records[i][k]['chart'],'coefficient':str(c)} for k,c in sorted(combo.items())]
   relations.append({'arrival_terms':at,'initial_terms':it,'final_hub_completion':'Unique common hub-output linear combination remains to be reconstructed if a witness is used.'})
 out.append({'port_index':port,'receiver_X2':x,'donor_Y2':y,'receiver_route':routes[x],'donor_route':routes[y],'initial_observation_count':len(initial[i]),'known_offhub_coordinate_count':len(known[i]),'nonhub_arrival_count':len(records[i]),'quotient_arrival_rank':len(basis),'null_relations':relations})
res={'status':'EXACT_HOSTED_REVERSE_HISTORY_QUOTIENT','source_sha256':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','common_hub_arrivals':1022,'common_hub_final_fields':n-len(off),'offhub_final_coordinates':len(off),'hub_arrival_offhub_coordinate_rows_all_zero':True,'source_inverse_transform_checked_on_all_offhub_coordinates':True,'receivers':out,'scope':'All actual nonhub X2-route MOVE-arrival histories and all initial cochart common values, modulo the complete1022-dimensional common hub-output span. Native hub is absorbing and contains no owned transport, so its1022 arrival histories are an invertible local linear reparameterization of its final common fields. Complete relation coefficients at finalhub are not yet reconstructed.'}
(O/'DERIVED-QUOTIENT.json').write_text(json.dumps(res,indent=2)+'\n');print({'receivers':len(out),'nonhub_arrivals':sum(x['nonhub_arrival_count'] for x in out),'null_relations':sum(len(x['null_relations']) for x in out),'rank_hist':dict(Counter(x['quotient_arrival_rank'] for x in out)),'null_hist':dict(Counter(len(x['null_relations']) for x in out)),'seconds':round(time.monotonic()-start,2)},flush=True)
