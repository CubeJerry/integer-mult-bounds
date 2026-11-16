#!/usr/bin/env python3
"""Actual original-record forks retain S8 and complete fifteen receivers."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,copy

def rank(rows):
 B={}
 for v in rows:
  while v:
   q=v.bit_length()-1
   if q in B:v^=B[q]
   else:B[q]=v;break
 return len(B)
def solve(rows,v):
 B={}
 for j,r in enumerate(rows):
  c=1<<j
  while r:
   q=r.bit_length()-1
   if q in B:r^=B[q][0];c^=B[q][1]
   else:B[q]=(r,c);break
 c=0
 while v:
  q=v.bit_length()-1;assert q in B;v^=B[q][0];c^=B[q][1]
 return c
def combine(rows,c):
 v=0
 for j,r in enumerate(rows):
  if c>>j&1:v^=r
 return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()=='8b91f8e82016cd4eadac391500a2ab606d6cdf975ec8f0a752644675a25cba1e';old=json.loads(br);R=json.loads((a.repo/old['source_path']).read_text())['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=old['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];S0=[int(v,16)for v in old['seed_rows_hex']];points=old['point_targets'];forks=[]
 for i,q,d in [(3,21,1),(76,64,73),(80,65,77)]:
  G=[j for j in old['private_roles'][str(i)]if j!=q];p=next(j for j in G if j!=d);assert d in G and all(dot(R[j],R[q])==0 for j in G);assert A[i]==A[q];forks.append({'old_receiver':i,'new_receiver':q,'donor':d,'carrier':p,'group':G,'chart':f'D{i}_{q}'})
 common=next(c for c in old['cache_metadata']if c['family']==0);charts=copy.deepcopy(old['charts']);charts['M0']={'kind':'span','rows':[R[j]for j in common['roles']]};charts[common['chart']]=charts['M0']
 for f in forks:charts[f['chart']]={'kind':'ann','rows':[R[f['old_receiver']],R[f['new_receiver']]]}
 val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};ops=[]
 def emit(o):
  ops.append(o);op,n,*q=o
  if op=='INIT':val[n]=0;loc[n]=q[0]
  elif op=='MOVE':loc[n]=q[0]
  elif op=='ADD':val[q[0]]^=val[n]
  elif op=='CLEAR':del val[n],loc[n]
 def move(n,c):emit(['MOVE',n,c])
 def add(n,m):emit(['ADD',n,m])
 for j in points:emit(['INIT',f'E{j}',f'L{j}']);add(f'X{j}',f'E{j}');move(f'E{j}','zero')
 for c in old['cache_metadata']:emit(['INIT',c['name'],c['chart']])
 for j in common['roles']:move(f'X{j}',common['chart']);add(f'X{j}',common['name']);move(f'X{j}','Hub')
 for f in forks:
  i,q,d,p,G,D=[f[k]for k in ['old_receiver','new_receiver','donor','carrier','group','chart']]
  for j in G:move(f'X{j}',D)
  for j in G:
   if j!=p:add(f'X{j}',f'X{p}')
  add(f'X{p}',f'X{d}')
  for j in G:
   if j not in [p,d]:move(f'X{j}','Hub')
  move(f'X{p}',f'F{i}');move(f'X{q}',f'F{i}');add(f'X{p}',f'X{q}');move(f'X{p}','Hub');move(f'X{d}',f'F{q}');move(f'X{i}',f'F{q}');add(f'X{i}',f'X{d}');move(f'X{i}','Hub')
 h1private={int(i):js for i,js in old['private_roles'].items()if h[int(i)]==1};h1pivots={i:int(old['singleton_pivots'][str(i)])for i in h1private}
 for c in old['cohorts']:
  if c['h']!=1:continue
  if not c['receivers']:
   for j in c['roles']:move(f'X{j}','Hub')
  elif len(c['receivers'])==1:
   i=c['receivers'][0];p=h1pivots[i]
   for j in c['roles']:move(f'X{j}',f'F{i}')
   for j in c['roles']:
    if j!=p:add(f'X{j}',f'X{p}');move(f'X{j}','Hub')
  else:
   cache=next(z for z in old['cache_metadata']if z['family']==1 and z['receivers']==c['receivers'])
   for j in c['roles']:move(f'X{j}',cache['chart']);add(f'X{j}',cache['name']);move(f'X{j}','Hub')
 for c in old['cache_metadata']:
  if c['family']==1 and len(c['receivers'])==2:move(c['name'],'M1')
 marks={'source_cut':len(ops)};cut={n:{'chart':loc[n],'row_hex':hex(v)}for n,v in val.items()if not n.startswith('Y')};Hub=[f'X{j}'for j in range(111)if loc[f'X{j}']=='Hub'];E=[f'E{j}'for j in points];Q=[f"X{f['new_receiver']}"for f in forks];basis_names=Hub+E+Q;B=[val[n]for n in basis_names];assert rank(B)==111 and len(B)==111
 allrows=[(combine(S0,c),c)for c in range(256)];project=lambda v:solve(B,v)>>(len(B)-3);S=[]
 for j in range(3):S.append(next(v for v,c in allrows if project(v)==1<<j))
 for v,c in allrows:
  if project(v)==0 and rank(S+[v])>rank(S):S.append(v)
 assert len(S)==8 and rank(S+S0)==8;seed=[]
 for z,s in enumerate(S):
  c=solve(B,s);hub=[n for k,n in enumerate(Hub)if c>>k&1];early=[n for k,n in enumerate(E,len(Hub))if c>>k&1];query=[n for k,n in enumerate(Q,len(Hub)+len(E))if c>>k&1];assert len(query)==int(z<3);emit(['INIT',f'P{z}','Hub'])
  for n in hub:add(n,f'P{z}')
  if query:move(f'P{z}',loc[query[0]]);add(query[0],f'P{z}')
  move(f'P{z}','zero')
  for n in early:add(n,f'P{z}')
  assert val[f'P{z}']==s;seed.append({'field':f'P{z}','row_hex':hex(s),'S0_coefficient_hex':hex(solve(S0,s)),'Hub_reads':hub,'early_point_reads':early,'held_query':query,'query_chart':cut[query[0]]['chart']if query else None})
 marks['seed8_before_Y']=len(ops)
 for j in points:add(f'E{j}',f'Y{j}');move(f'Y{j}',f'F{j}');marks[f'completed_{j}']=len(ops)
 def preload(i,extra=None):
  c=solve(S,A[i])
  for z in range(8):
   if c>>z&1:add(f'P{z}',f'Y{i}')
  if extra:add(extra,f'Y{i}')
 for f in forks:
  i,q,d=[f[k]for k in ['old_receiver','new_receiver','donor']];preload(i);move(f'Y{i}','M0');add(common['name'],f'Y{i}');move(f'Y{i}',f'F{i}');add(f'X{q}',f'Y{i}');move(f'X{q}','Hub');marks[f'completed_{i}']=len(ops);preload(q,f'E{d}');move(f'Y{q}','M0');add(common['name'],f'Y{q}');move(f'Y{q}',f'F{q}');add(f'X{d}',f'Y{q}');move(f'X{d}','Hub');marks[f'completed_{q}']=len(ops)
 for i,p in h1pivots.items():
  preload(i);move(f'Y{i}','M1')
  for c in old['cache_metadata']:
   if c['family']==1 and i in c['receivers']:add(c['name'],f'Y{i}')
  move(f'Y{i}',f'F{i}');add(f'X{p}',f'Y{i}');move(f'X{p}','Hub');marks[f'completed_{i}']=len(ops)
 for f in forks:
  i,q,d,p,G=[f[k]for k in ['old_receiver','new_receiver','donor','carrier','group']];add(f'X{i}',f'X{d}');add(f'X{p}',f'X{d}');add(f'X{p}',f'X{q}')
  for j in G:
   if j!=p:add(f'X{j}',f'X{p}')
 for i,p in h1pivots.items():
  for j in h1private[i]:
   if j!=p:add(f'X{j}',f'X{p}')
 assert all(val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub'for j in range(111));marks['all_X_restored']=len(ops);T=sorted(old['targets']+[f['new_receiver']for f in forks])
 for i in range(111):
  if i not in T:move(f'Y{i}',f'F{i}')
  assert val[f'Y{i}']==(1<<(111+i))^((1<<i)if i in T else 0)
 for n in [f'E{j}'for j in points]+[c['name']for c in old['cache_metadata']]+[f'P{z}'for z in range(8)]:emit(['CLEAR',n])
 out={'schema':'actual-singular-fork-fifteen-v1','source_path':old['source_path'],'source_sha256':old['source_sha256'],'base_word_sha256':hashlib.sha256(br).hexdigest(),'singular_h':h,'targets':T,'point_targets':points,'forks':forks,'h1_private_roles':h1private,'h1_private_pivots':h1pivots,'cache_metadata':old['cache_metadata'],'original_seed_rows_hex':old['seed_rows_hex'],'seed_rows_hex':[hex(v)for v in S],'source_basis_names':basis_names,'source_cut':cut,'seed_metadata':seed,'charts':charts,'operations':ops,'milestones':marks,'copies':1,'new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print('counts',dict(Counter(o[0]for o in ops)),'targets',T,'basis',len(B),'queried',[(s['field'],s['held_query'])for s in seed if s['held_query']])
if __name__=='__main__':main()
