"""Exact source-bound observation DAG; graph pruning is not a full paid native."""
from __future__ import annotations
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PATH='research/shared-wire-split-composition/data/final.json.gz'

def need(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def scale(a,c):return {j:v*c for j,v in a.items() if v*c}
def source_default():
 return next((base/PATH for p in Path(__file__).resolve().parents for base in (p,p/'moonshot') if (base/PATH).is_file()),Path(PATH))
def load_source(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source SHA256');return json.loads(gzip.decompress(raw))

def build(w,cut):
 need(0<=cut<=len(w['program']),'source cut')
 mains=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));ms=set(mains);rows=[{i:F(1)} if i in ms else {} for i in range(w['public']+w['owned_fields'])];cur=w['initial'][:]+[None]*w['owned_fields'];bases=collections.defaultdict(dict);nodes=[];main_roots=[]
 def decomp(row,frame):
  v=row.copy();expr={}
  for p,(b,e) in bases[frame].items():
   if v.get(p):
    c=v[p];add(v,b,-c);add(expr,e,c)
  return expr,v
 def insert(row,frame,kind,parents,idx,owner,rank=0,source_chart=None):
  ident=len(nodes);nodes.append({'id':ident,'frame':frame,'kind':kind,'parents':[[k,str(c)] for k,c in sorted(parents.items())],'source_event':idx,'virtual_owner':owner,'rank':rank,'source_chart':source_chart,'row':[[k,str(c)] for k,c in sorted(row.items())]});v=row.copy();expr={ident:F(1)}
  for p,(b,e) in bases[frame].items():
   if v.get(p):
    c=v[p];add(v,b,-c);add(expr,e,-c)
  if v:
   p=min(v);c=v[p];bases[frame][p]=(scale(v,1/c),scale(expr,1/c))
  return ident
 for r in mains:insert(rows[r],cur[r],'input',{},-1,r)
 for k,e in enumerate(w['program'][:cut]):
  op,r=e[:2]
  if op in ('ADD','COPY'):add(rows[r],rows[e[2]],F(e[3]))
  elif op=='SCALE':rows[r]=scale(rows[r],F(e[2]))
  elif op=='INIT':rows[r]={};cur[r]=e[2]
  elif op=='CLEAR':rows[r]={};cur[r]=None
  elif op=='MOVE':
   src,dst=e[2:4];expr,rem=decomp(rows[r],src);need(not rem,('potential source availability',k))
   if r in ms:main_roots.append(insert(rows[r],dst,'main',expr,k,r,0,src))
   elif rows[r]:
    _,rem=decomp(rows[r],dst)
    if rem:insert(rows[r],dst,'aux',expr,k,r,abs(len(w['frames'][src])-len(w['frames'][dst])),src)
   cur[r]=dst
  else:raise ValueError(op)
 outputs=[]
 for r in mains:
  expr,rem=decomp(rows[r],cur[r]);need(not rem,('main boundary availability',r));outputs.append(insert(rows[r],cur[r],'output',expr,cut,r))
 keep=set();todo=list(main_roots)+outputs
 while todo:
  node=todo.pop()
  if node in keep:continue
  keep.add(node);todo.extend(j for j,c in nodes[node]['parents'])
 # Verify each graph edge's exact row, source chart and time directly.
 for node in nodes:
  if node['kind']=='input':continue
  r={};f=node['source_chart'] if node['kind'] in ('main','aux') else node['frame']
  for parent,c in node['parents']:
   p=nodes[parent];need(parent<node['id'] and p['frame']==f,'causal cochart parent')
   add(r,{j:F(v) for j,v in p['row']},F(c))
  need(r=={j:F(v) for j,v in node['row']},'exact parent expression')
 hist=collections.Counter(n['rank'] for n in nodes if n['id'] in keep and n['kind']=='aux');allhist=collections.Counter(n['rank'] for n in nodes if n['kind']=='aux')
 result={'source_sha256':PIN,'cut':cut,'candidate_nodes':len(nodes),'kept_nodes':len(keep),'main_roots':len(main_roots),'boundary_main_roots':len(outputs),'candidate_paid_histogram':dict(sorted(allhist.items())),'kept_paid_histogram':dict(sorted(hist.items())),'kept_aux_count':sum(hist.values()),'scope':'Exact fixed-expression graph closure. Literal physical implementation and all final costs require separate evidence.'}
 return {'result':result,'nodes':nodes,'kept_ids':sorted(keep),'output_ids':outputs,'main_roots':main_roots,'mains':mains,'source_current_charts':cur}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=source_default());ap.add_argument('--cut',type=int,default=71261);ap.add_argument('--output',type=Path);a=ap.parse_args();g=build(load_source(a.source),a.cut);s=json.dumps(g['result'],indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
