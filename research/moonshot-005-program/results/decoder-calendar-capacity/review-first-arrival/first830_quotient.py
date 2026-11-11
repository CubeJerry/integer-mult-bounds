#!/usr/bin/env python3
"""Independent two-coordinate quotient certificate for the first 830 route."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(v,msg):
 if not v:raise ValueError(msg)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];cut=25489
 mains=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));M=set(mains);carrier={r:n+i for i,r in enumerate(mains)}
 rows=[{r:F(1)} for r in range(n)]+[{} for _ in range(w['owned_fields'])];cur=w['initial']+[None]*w['owned_fields'];ver=[-1]*len(rows)
 for i,e in enumerate(w['program'][:cut]):
  op,r=e[:2]
  need(op not in ('INIT','CLEAR'),'prefix has no source ownership changes')
  if op=='MOVE':need(r not in M,'prefix has no main movement');cur[r]=e[3]
  elif op=='SCALE':rows[r]={j:F(e[2])*v for j,v in rows[r].items()};ver[r]=i
  else:add(rows[r],rows[e[2]],F(e[3]));ver[r]=i
 move=w['program'][cut];need(move==['MOVE',830,3,56,False],'first route');dest=56
 common=[r for r,f in enumerate(cur) if f==dest and r!=830];qs=[r for r in mains if w['initial'][r]==dest]
 need(common==[60] and qs==[60],'all current destination holders')
 S=[rows[r] for r in common]+[{carrier[r]:F(1),r:F(-1)} for r in qs];c=rows[830];d={}
 for r,v in c.items():
  if r in M:d[carrier[r]]=v;d[r]=-v
 need(d=={carrier[172]:F(-1,2),172:F(1,2)},'exact difference target')
 h=830;y=carrier[172];need(y==1639,'second172 physical coordinate')
 need(all(not row.get(h) and not row.get(y) for row in S),'both dual coordinates vanish on destination span')
 need(c.get(h)==-1 and not c.get(y) and not d.get(h) and d.get(y)==F(-1,2),'independent quotient directions')
 need(bool(rows[60]) and all(j<n for j in rows[60]) and S[1].get(carrier[60])==1,'destination span rank2')
 enc=lambda row:[[j,str(v)] for j,v in sorted(row.items())]
 return {'status':'PASS_EXACT_TWO_COORDINATE_QUOTIENT','source_sha256':PIN,'cut_before_event':cut,'move':move,'state_contract':'Exact reference prefix plus400 raw initial input-difference carriers; no owned sidecars or previous main MOVEs.','current_common_observers':common,'current_raw_difference_carriers':qs,'destination_rows':[enc(row) for row in S],'common_target':enc(c),'difference_target':enc(d),'current_common_versions':{str(r):ver[r] for r in common},'dual_coordinates':[{'input':'entering helper830','column':h,'on_common':'-1','on_difference':'0'},{'input':'second main172','column':y,'on_common':'0','on_difference':'-1/2'}],'ranks':[2,3,4],'quotient_rank':2,'scope':'One scalar-coded complete-field arrival cannot make both targets simultaneously decodable under this exact pre-route state. Delayed demands, changed earlier coding and other routes are outside scope.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k not in ('common_target','destination_rows')},indent=2,sort_keys=True))
