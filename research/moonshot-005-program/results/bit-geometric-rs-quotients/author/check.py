from pathlib import Path
import importlib.util,gzip,json
from collections import Counter
import numpy as np
from argparse import ArgumentParser
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True);repo=args.repo;b=repo/'research/moonshot-005-program/results'
def mod(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
from hashlib import sha256
pin_doc=json.loads((Path(__file__).resolve().parents[1]/'SOURCE-PINS.json').read_text())
for pin_path,entry in pin_doc['files'].items():
 raw=(args.repo/pin_path).read_bytes()
 if len(raw)!=entry['bytes'] or sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Source pin '+pin_path)
s=mod(b/'bit-orthogonal-spread-port-allocation/review/check.py','spread');f=mod(b/'bit-single-rs-anchor-obstruction/author/check.py','gf')
g=json.loads(gzip.decompress((b/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((b/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());cols=B['lattice_basis_columns'];iv=s.inv([[cols[j][i]for j in range(8)]for i in range(8)]);change={s.xor(B['hyperbolic_basis_masks'][k]for k in range(8)if x>>k&1):x for x in range(256)}
roots=[]
for r in g['root_table']:
 c=[sum(x*y for x,y in zip(row,r))for row in iv];roots.append(change[sum((int(x)&1)<<k for k,x in enumerate(c))])
H=[set(p)for p in g['A2']];stars={j:[h for h,p in enumerate(H)if j in p]for j in range(111)};real=np.array(g['root_table']);orth=real@real.T==0;vis={h:{i for i in range(111)if all(orth[i,j]for j in p)}for h,p in enumerate(H)}
def power(a,n):
 v=1
 for _ in range(n):v=int(f.M[v,a])
 return v
def q6(x):
 v=power(x,9)^power(x,18)^power(x,36)
 if v not in(0,1):raise ValueError(('qvalue',v))
 return v
qtab={x:q6(x)for x in range(64)};print('FIELD_QUADRATIC_ZEROS',sum(v==0 for v in qtab.values()),flush=True)
def witt(V,q):
 basis=[];V=set(V)
 while len(V)>1:
  polar=lambda x,y:q(x^y)^q(x)^q(y)
  zero=sorted(x for x in V if x and not q(x))
  if zero:
   e=zero[0];ff=next(x for x in zero if polar(e,x));basis +=[e,ff]
  else:
   e=min(V-{0});ff=min(V-{0,e});basis +=[e,ff]
  V={x for x in V if not polar(x,e)and not polar(x,ff)}
 return basis
std=witt(range(64),lambda x:qtab[x]);need=lambda x:None if x else (_ for _ in()).throw(ValueError('failed'))
records=json.loads(gzip.decompress((b/'bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz').read_bytes()))['witnesses'];ans=[];sources=[];record_map={x['anchor']:x for x in records}
for j in range(111):
 record=record_map.get(j);h0=stars[j][0];u0=roots[next(v for v in H[h0]if v!=j)];vj=roots[j]
 V={x for x in range(256)if not s.polar(x,u0)and not s.polar(x,vj)};basis=witt(V,s.q)
 need(len(basis)==6)
 mp={s.xor(basis[k]for k in range(6)if mask>>k&1):s.xor(std[k]for k in range(6)if mask>>k&1)for mask in range(64)}
 need(all(s.q(x)==qtab[y] for x,y in mp.items()))
 nodes={}
 for h in stars[j]:
  u=roots[next(v for v in H[h]if v!=j)];w=u^u0^(vj if s.polar(u0,u) else 0);need(w in V and not s.q(w));nodes[h]=mp[w]
 need(len(set(nodes.values()))==28 and set(nodes.values())=={x for x,q in qtab.items()if not q})
 parameters={}
 for i in range(120):
  if not orth[i,j]:continue
  epsilon=s.polar(u0,roots[i]);v=roots[i]^(vj if epsilon else 0);need(v in V and v);parameter=mp[v];parameters[i]=parameter
  actual={h for h in stars[j]if all(orth[i,k]for k in H[h])};formula={h for h,a in nodes.items()if (q6(parameter^a)^q6(parameter)^q6(a))==(1^q6(parameter))};need(actual==formula and len(actual)==16)
 need(len(parameters)==63 and set(parameters.values())==set(range(1,64)))
 sources.append({'anchor':j,'base_H':h0,'nodes':nodes,'receiver_parameters':parameters})
 if record is None:continue
 ranks=[];fullranks=[]
 for edge in record['propagations']:
  h=edge['centre']
  for e in edge['quotient_propagations']:
   pol=lambda r:f.polynomial([nodes[q]for q in stars[j]if q!=h and r in vis[q]])
   ranks.append(f.rank(np.array([pol(r)for r in e['receivers']])))
   rr=sorted((vis[h]&vis[e['leaf_plane']]&vis[e['anchor_plane']])-{80})
   fullranks.append(f.rank(np.array([pol(r)for r in rr])))
 item={'anchor':j,'base_H':h0,'nodes':nodes,'selected_rank_histogram':dict(Counter(ranks)),'full_rank_histogram':dict(Counter(fullranks)),'obstructed':all(r==15 for r in fullranks)};ans.append(item)
 print(j,dict(Counter(ranks)),dict(Counter(fullranks)),flush=True)
 (args.out/'NODE-CHECKS.json').write_text(json.dumps(ans,indent=2)+'\n')
print('DONE',sum(r['obstructed']for r in ans),len(ans),flush=True)

(args.out/'NODES.json').write_text(json.dumps(sources,sort_keys=True,indent=2)+'\n')
need(len(sources)==111 and len(ans)==99 and all(set(map(int,x['selected_rank_histogram']))=={5} and set(map(int,x['full_rank_histogram']))=={5} for x in ans))
result={'status':'PASS_GEOMETRIC_QUADRIC_RS_QUOTIENTS','source_donors':111,'geometric_source_views':6993,'native_source_views':sum(sum(int(i)<111 for i in row['receiver_parameters']) for row in sources),'anchor_certificates':99,'selected_and_all_native_propagations':2970,'propagation_span':5,'physical_source_word':False,'complete_H_word':False,'new_complete_kappa':False}
need(result['native_source_views']==6470)
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],flush=True)
