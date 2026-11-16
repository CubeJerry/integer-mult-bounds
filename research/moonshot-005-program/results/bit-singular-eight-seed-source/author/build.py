#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib
from collections import defaultdict,Counter

def basis_ids(rows):
 B={};ids=[]
 for j,v in enumerate(rows):
  while v:
   z=v.bit_length()-1
   if z in B:v^=B[z]
   else:B[z]=v;ids.append(j);break
 return ids

def encode(rows,target):
 B={}
 for j,v in enumerate(rows):
  c=1<<j
  while v:
   z=v.bit_length()-1
   if z in B:v^=B[z][0];c^=B[z][1]
   else:B[z]=(v,c);break
 ans=0
 while target:
  z=target.bit_length()-1;target^=B[z][0];ans^=B[z][1]
 return ans

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));omitted=[0,0,1,1,0,0,1,-1];assert omitted not in R and [-x for x in omitted]not in R
 h=[int((i!=72 and dot(R[72],r)!=0)^(dot(omitted,r)!=0))for i,r in enumerate(R)];assert Counter(h)=={0:52,1:59};K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];A=[row&sum(1<<j for j in range(111)if h[j]==h[i])for i,row in enumerate(K)];T=[1,3,4,6,73,74,75,76,77,78,79,80];active={0:[3,76,80],1:[4,74,78]};pivots={3:1,76:73,80:77,4:6,74:75,78:79};points=sorted(pivots.values());assert set(points)|set(pivots)==set(T)and set(points).isdisjoint(pivots)
 bs=[T[k]for k in basis_ids([A[i]for i in T])];S=[A[i]for i in bs];assert len(S)==8 and len(basis_ids(A))==15
 charts={'Hub':{'kind':'span','rows':[[int(i==j)for i in range(8)]for j in range(8)]},'zero':{'kind':'span','rows':[]}}
 for j,r in enumerate(R):charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
 for b,act in active.items():charts[f'M{b}']={'kind':'ann','rows':[R[i]for i in act]}
 cohorts={};cache=[];private={};where={}
 for b,act in active.items():
  cp=defaultdict(list)
  for j in range(111):
   if h[j]==b:cp[tuple(i for i in act if dot(R[i],R[j])==0)].append(j)
  cohorts[b]=cp
  for ss,js in sorted(cp.items()):
   if not ss:continue
   if len(ss)==1:
    i=ss[0];private[i]=js;assert pivots[i]in js
    for j in js:where[j]=f'F{i}'
   else:
    z=len(cache);chart=f'C{z}';charts[chart]={'kind':'ann','rows':[R[i]for i in ss]};cache.append({'name':f'Q{z}','chart':chart,'family':b,'receivers':list(ss),'roles':js})
    for j in js:where[j]=chart
 ops=[]
 for j in points:ops += [['INIT',f'E{j}',f'L{j}'],['ADD',f'X{j}',f'E{j}'],['MOVE',f'E{j}','zero']]
 for c in cache:ops.append(['INIT',c['name'],c['chart']])
 for j in range(111):
  n=f'X{j}'
  if j not in where:ops.append(['MOVE',n,'Hub']);continue
  ops.append(['MOVE',n,where[j]])
  for c in cache:
   if j in c['roles']:ops += [['ADD',n,c['name']],['MOVE',n,'Hub']];break
 for i,js in sorted(private.items()):
  for j in js:
   if j!=pivots[i]:ops += [['ADD',f'X{j}',f'X{pivots[i]}'],['MOVE',f'X{j}','Hub']]
 import sympy as sp
 for c in cache:
  if sp.Matrix(charts[c['chart']]['rows']).rank()!=sp.Matrix(charts[f"M{c['family']}"]['rows']).rank():ops.append(['MOVE',c['name'],f"M{c['family']}"])
 marks={'source_cut':len(ops)};seed=[]
 for z,row in enumerate(S):
  hub=[j for j in range(111)if row>>j&1 and j not in points];early=[j for j in points if row>>j&1];ops += [['INIT',f'P{z}','Hub']]+[['ADD',f'X{j}',f'P{z}']for j in hub]+[['MOVE',f'P{z}','zero']]+[['ADD',f'E{j}',f'P{z}']for j in early];seed.append({'field':f'P{z}','native_row':bs[z],'row_hex':hex(row),'Hub_original_reads':hub,'early_point_reads':early})
 marks['seed8_before_Y']=len(ops)
 for j in points:ops += [['ADD',f'E{j}',f'Y{j}'],['MOVE',f'Y{j}',f'F{j}']];marks[f'completed_{j}']=len(ops)
 preload=[]
 for b,act in active.items():
  for i in act:
   coeff=encode(S,A[i]);rs=[z for z in range(8)if coeff>>z&1];ops += [['ADD',f'P{z}',f'Y{i}']for z in rs];ops.append(['MOVE',f'Y{i}',f'M{b}'])
   for c in cache:
    if i in c['receivers']:ops.append(['ADD',c['name'],f'Y{i}'])
   ops += [['MOVE',f'Y{i}',f'F{i}'],['ADD',f'X{pivots[i]}',f'Y{i}'],['MOVE',f'X{pivots[i]}','Hub']];marks[f'completed_{i}']=len(ops);preload.append({'receiver':i,'seed_indices':rs})
 for i,js in sorted(private.items()):
  for j in js:
   if j!=pivots[i]:ops.append(['ADD',f'X{j}',f'X{pivots[i]}'])
 marks['all_X_restored']=len(ops);ops += [['MOVE',f'Y{i}',f'F{i}']for i in range(111)if i not in T];owners=[f'E{j}'for j in points]+[c['name']for c in cache]+[f'P{z}'for z in range(8)];ops += [['CLEAR',n]for n in owners]
 w={'schema':'actual-singular-two-funnel-eight-seed-source-v1','source_path':str(source.relative_to(a.repo)),'source_sha256':sha,'singular_h':h,'omitted_normal':omitted,'targets':T,'active_targets':active,'point_targets':points,'singleton_pivots':pivots,'private_roles':private,'cohorts':[{'h':b,'receivers':list(ss),'roles':js}for b,cp in cohorts.items()for ss,js in sorted(cp.items())],'cache_metadata':cache,'seed_basis_native_rows':bs,'seed_rows_hex':[hex(v)for v in S],'seed_rank':8,'full_fitting_rank':15,'seed_metadata':seed,'preload_witnesses':preload,'charts':charts,'operations':ops,'milestones':marks,'copies':1,'new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print('targets',T,'active',active,'pointdualduty',points,'counts',dict(Counter(o[0]for o in ops)),'basis',bs)
if __name__=='__main__':main()
