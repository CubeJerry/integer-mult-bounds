#!/usr/bin/env python3
"""Literal finite-source meet funnel; all principal fields are explicitly acquired."""
from pathlib import Path
import argparse,json,hashlib,itertools
from collections import defaultdict,Counter

def rank(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return len(B)

def independent(rows):
 B={}; out=[]
 for j,v in enumerate(rows):
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;out.append(j);break
 return out

def encode_basis(rows,target):
 B={}
 for j,v in enumerate(rows):
  c=1<<j
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p][0];c^=B[p][1]
   else:B[p]=(v,c);break
 c=0
 while target:
  p=target.bit_length()-1
  if p not in B:raise ValueError('not in span')
  target^=B[p][0];c^=B[p][1]
 return c

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--variant',choices=['four','six'],required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 source=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));T=[0,3,76,80]if a.variant=='four'else[1,3,73,76,77,80]
 K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];bi=independent(K);assert len(bi)==9;kb=[K[i]for i in bi]
 cohorts=defaultdict(list)
 for j in range(111):cohorts[tuple(i for i in T if dot(R[i],R[j])==0)].append(j)
 singleton={s[0]:js for s,js in cohorts.items()if len(s)==1}; mixed={s:js for s,js in cohorts.items()if len(s)>1}
 if a.variant=='four':pivots={0:3,3:14,76:60,80:59}
 else:pivots={i:singleton[i][0]for i in T};assert all(len(singleton[i])==1 for i in T)
 assert all(pivots[i]in singleton[i]for i in T)
 charts={'Hub':{'kind':'span','rows':[[int(i==j)for i in range(8)]for j in range(8)]},'zero':{'kind':'span','rows':[]},'Meet':{'kind':'ann','rows':[R[i]for i in T]}}
 for j,r in enumerate(R):charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
 cache=[];where={}
 for z,(s,js)in enumerate(sorted(mixed.items())):
  name=f'C{z}';charts[name]={'kind':'ann','rows':[R[i]for i in s]};cache.append({'name':f'A{z}','chart':name,'receivers':list(s),'roles':js})
  for j in js:where[j]=name
 for i,js in singleton.items():
  for j in js:where[j]=f'F{i}'
 ops=[];loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};val={f'X{j}':1<<j for j in range(111)};dual=val.copy()
 def emit(o):
  ops.append(o)
  if o[0]=='INIT':loc[o[1]]=o[2]
  if o[0]=='MOVE':loc[o[1]]=o[2]
  if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'):val[o[2]]^=val[o[1]];dual[o[1]]^=dual[o[2]]
 # Derive the actual cut without early helpers; inserts do not change X.
 for c in cache:emit(['INIT',c['name'],c['chart']])
 source_prefix_start=len(ops)
 for j in range(111):
  n=f'X{j}'
  if j not in where:emit(['MOVE',n,'Hub']);continue
  emit(['MOVE',n,where[j]])
  ss=next(s for s,js in cohorts.items()if j in js)
  if len(ss)>1:
   c=next(c for c in cache if j in c['roles']);emit(['ADD',n,c['name']]);emit(['MOVE',n,'Hub'])
 # All singleton originals now share receiver facets. Aggregate into actual pivot.
 for i,js in sorted(singleton.items()):
  p=pivots[i]
  for j in js:
   if j!=p:emit(['ADD',f'X{j}',f'X{p}']);emit(['MOVE',f'X{j}','Hub'])
 # Owned caches descend to the actual common meet; zero-rank duplicate chart move omitted later.
 import sympy as sp
 def canon(c):
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8)
  rows=M.rowspace()if c['kind']=='span'else M.nullspace()
  return sp.Matrix.vstack(*[v.T for v in rows]).rref()[0]if rows else sp.zeros(0,8)
 # Comparing rowspaces with sympy nullspace row convention.
 def dim(c):return sp.Matrix(c['rows']).rank()if c['kind']=='span'else 8-sp.Matrix(c['rows']).rank()
 for c in cache:
  if dim(charts[c['chart']])!=dim(charts['Meet']):emit(['MOVE',c['name'],'Meet'])
  else:
   # Equivalent named spaces are genuine co-location, no movement.
   pass
 cut=len(ops);held=[j for j in range(111)if loc[f'X{j}']!='Hub'];assert set(held)==set(pivots.values());h=len(held)
 rows=[]
 for v in kb:
  cur=sum(((v&dual[f'X{j}']).bit_count()%2)<<j for j in range(111));pr=sum(((cur>>j)&1)<<z for z,j in enumerate(held));rows.append((v,cur,pr))
 p=rank([x[2]for x in rows]);E=[];span=[x[2]for x in rows]
 for z,j in enumerate(held):
  e=1<<z
  if rank(span+[e])>rank(span):E.append(z);span.append(e)
 assert len(E)==h-p and rank(span)==h
 # Only early helper coordinates that actually remain pure originals are admitted here.
 for z in E:assert val[f'X{held[z]}']==1<<held[z]
 early=[]
 for u,z in enumerate(E):
  j=held[z];early += [['INIT',f'E{u}',f'L{j}'],['ADD',f'X{j}',f'E{u}'],['MOVE',f'E{u}','zero']]
 ops=early+ops;cut+=len(early)
 # Enumerate all fixed scalar codewords; choose valid chart-unit principal rows.
 candidates=[]
 for mask in range(1,1<<9):
  original=cur=pr=0
  for k in range(9):
   if mask>>k&1:original^=rows[k][0];cur^=rows[k][1];pr^=rows[k][2]
  cost=sum((cur>>j)&1 for j in range(111)if j not in held)
  candidates.append((cost,mask,original,cur,pr))
 candidates.sort();em=sum(1<<z for z in E);chosen=[]
 for z in range(h):
  if z in E:continue
  chosen.append(next(c for c in candidates if c[4]&~em==1<<z))
 kernel=[];masks=[]
 for c in candidates:
  if c[4]:continue
  if rank(masks+[c[1]])>len(masks):kernel.append(c);masks.append(c[1])
  if len(kernel)==9-p:break
 assert len(kernel)==9-p;chosen+=kernel;assert len(chosen)==9 and rank([c[1]for c in chosen])==9
 seedmeta=[]
 for q,(cost,mask,original,cur,pr)in enumerate(chosen):
  n=f'P{q}';hub=[j for j in range(111)if j not in held and cur>>j&1];missing=[z for z in range(h)if z not in E and pr>>z&1];assert len(missing)<=1
  ops += [['INIT',n,'Hub']]+[['ADD',f'X{j}',n]for j in hub]
  if missing:
   j=held[missing[0]];ops += [['MOVE',n,loc[f'X{j}']],['ADD',f'X{j}',n],['MOVE',n,'zero']]
  else:ops.append(['MOVE',n,'zero'])
  corrections=[u for u,z in enumerate(E)if pr>>z&1];ops += [['ADD',f'E{u}',n]for u in corrections]
  seedmeta.append({'packet':n,'canonical_row_hex':hex(original),'held_projection_hex':hex(pr),'Hub_reads':hub,'held_queries':[held[z]for z in missing],'early_point_corrections':corrections})
 marks={'source_cut':cut,'canonical9_before_Y':len(ops)};preloads=[]
 for i in T:
  coeff=encode_basis([c[2]for c in chosen],K[i]);qs=[q for q in range(9)if coeff>>q&1];ops += [['ADD',f'P{q}',f'Y{i}']for q in qs];preloads.append({'receiver':i,'principal_indices':qs})
  ops.append(['MOVE',f'Y{i}','Meet'])
  for c in cache:
   if i in c['receivers']:ops.append(['ADD',c['name'],f'Y{i}'])
  ops += [['MOVE',f'Y{i}',f'F{i}'],['ADD',f'X{pivots[i]}',f'Y{i}'],['MOVE',f'X{pivots[i]}','Hub']]
  marks[f'completed_{i}']=len(ops)
 # Restore aggregate pivots with all actual original coordinates at Hub.
 for i,js in sorted(singleton.items()):
  p0=pivots[i]
  for j in js:
   if j!=p0:ops.append(['ADD',f'X{j}',f'X{p0}'])
 marks['all_X_restored']=len(ops)
 ops += [['MOVE',f'Y{i}',f'F{i}']for i in range(111)if i not in T]
 owners=[f'E{u}'for u in range(len(E))]+[c['name']for c in cache]+[f'P{q}'for q in range(9)]
 ops += [['CLEAR',n]for n in owners]
 out={'schema':'actual-meet-funnel-source-v1','variant':a.variant,'source_path':str(source.relative_to(a.repo)),'source_sha256':sha,'targets':T,'copies':1,'charts':charts,'cohorts':[{'receivers':list(s),'roles':js}for s,js in sorted(cohorts.items())],'singleton_pivots':pivots,'cache_metadata':cache,'held_originals':held,'canonical_projection_rank':p,'early_point_helper_originals':[held[z]for z in E],'canonical_seeds':seedmeta,'canonical_preloads':preloads,'milestones':marks,'operations':ops,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'targets':T,'counts':dict(Counter(o[0]for o in ops)),'held':held,'canonical_projection_rank':p,'early_point_helpers':[held[z]for z in E]}))
if __name__=='__main__':main()
