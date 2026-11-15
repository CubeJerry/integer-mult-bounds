#!/usr/bin/env python3
"""Literal native eight-query cyclic source core; no receiver theorem by itself."""
from pathlib import Path
from collections import Counter
import sys

def configure(repo):
 global c,roots,h,pins,K,W
 source=Path(repo)/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a'
 sys.path.insert(0,str(source))
 import shared_facet_source as c
 import full_singular_history as f
 import eight_packet_source as e
 c.runs=f.runs;c.price=e.price
 roots,h,pins=c.source_geometry(Path(repo))
 K=[c.mask(j for j,r in enumerate(roots)if j==i or c.dot(r,roots[i])==0)for i in range(111)]
 W=[c.mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or c.dot(r,roots[i])==0))for i in range(111)]
 return roots,h,pins

def build(order=tuple(range(8)),A=None,closed=True):
 norms=[roots[i]for i in order];k=8
 assert c.rank_q(norms)==8
 charts={'Hub':{'kind':'ann','rows':[]},'zero':{'kind':'span','rows':[]}}
 for j,r in enumerate(roots):charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
 def ch(s):
  if s==0:return 'Hub'
  if s==255:return 'zero'
  if s.bit_count()==1:return f'F{order[s.bit_length()-1]}'
  if s.bit_count()==7:return f'L{order[(255^s).bit_length()-1]}'
  return f'A{s}'
 for s in range(1,255):
  name=ch(s)
  if name not in charts:charts[name]={'kind':'ann','rows':[r for i,r in enumerate(norms)if s>>i&1]}
 ops=[];expected={};cachecharts={};cachevals={}
 for j in range(111):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']];expected[f'R{j}']=(f'L{j}',1<<j)
 for q in range(8):
  pattern=0
  for length in range(1,9):
   pattern|=1<<((q+length-1)%8);name=f'C{q}_{length}';cachecharts[name]=ch(pattern);cachevals[name]=0;ops +=[['INIT',name,ch(pattern)]]
 groups={p:[]for p in range(256)}
 for j,r in enumerate(roots):groups[sum(int(c.dot(r,n)==0)<<i for i,n in enumerate(norms))].append(j)
 offsets=[0]*8;cohorts=[]
 for pattern,S in groups.items():
  if not S:continue
  if pattern==0:
   for j in S:ops += [['MOVE',f'X{j}','Hub']]
   continue
  rs=sorted(c.runs(pattern,8),key=lambda r:-len(r));carrier=S[0];donors=S[1:len(rs)];others=S[1:]
  if len(rs)>len(S):raise ValueError('Insufficient cohort donors')
  start=ch(pattern)
  for j in S:
   if start!=f'L{j}':ops += [['MOVE',f'X{j}',start]]
  for j in others:ops += [['ADD',f'X{j}',f'X{carrier}']]
  for j in others:
   if j not in donors:ops += [['MOVE',f'X{j}','Hub']]
  for j in donors:ops += [['ADD',f'X{carrier}',f'X{j}']]
  values=[(carrier,c.mask(S))]+[(j,c.mask(S)^(1<<j))for j in donors]
  for run,(j,value)in zip(rs,values):
   current=start
   for pos in range(len(run)):
    suffix=run[pos:];dest=ch(sum(1<<q for q in suffix))
    if dest!=current:ops +=[['MOVE',f'X{j}',dest]];current=dest
    name=f'C{run[pos]}_{len(suffix)}';assert cachecharts[name]==dest
    ops +=[['ADD',f'X{j}',name]];cachevals[name]^=value
   ops +=[['MOVE',f'X{j}','Hub']]
  for j in donors:ops +=[['ADD',f'X{carrier}',f'X{j}']]
  for j in others:ops +=[['ADD',f'X{j}',f'X{carrier}']]
  for donor,run in zip(donors,rs[1:]):
   for q in run:offsets[q]^=1<<donor
  cohorts.append({'pattern':pattern,'sources':S,'runs':rs,'carrier':carrier,'donors':donors})
 expected.update({n:(cachecharts[n],v)for n,v in cachevals.items()})
 modes=[c.mask(j for j,r in enumerate(roots)if c.dot(r,n)==0)for n in norms]
 A=A or [0]*8;seeds=[a^e for a,e in zip(A,offsets)];histories=[]
 for q,seed in enumerate(seeds):
  n=f'P{q}';ops +=[['INIT',n,'Hub']]
  for j in range(111):
   if seed>>j&1:ops +=[['ADD',f'X{j}',n]]
  pattern=0
  for length in range(1,9):
   pattern|=1<<((q+length-1)%8);ops +=[['MOVE',n,ch(pattern)],['ADD',f'C{q}_{length}',n]]
  expected[n]=('zero',A[q]^modes[q])
 marker=len(ops)
 if closed:
  for n in expected:ops +=[['CLEAR',n]]
  for j in range(111):ops +=[['MOVE',f'Y{j}',f'F{j}']]
 return {'charts':charts,'operations':ops,'expected':expected,'offsets':offsets,'modes':modes,'seeds':seeds,'cohorts':cohorts,'order':order,'closed':closed,'handoff':marker}

def replay(w,W):
 charts=w['charts'];dims={n:c.rank_q(s['rows'])if s['kind']=='span'else 8-c.rank_q(s['rows'])for n,s in charts.items()}
 def sub(a,b):
  x,y=charts[a],charts[b]
  if x['kind']==y['kind']=='ann':return c.rank_q(x['rows']+y['rows'])==c.rank_q(x['rows'])
  if x['kind']==y['kind']=='span':return c.rank_q(x['rows']+y['rows'])==c.rank_q(y['rows'])
  if x['kind']=='span'and y['kind']=='ann':return all(c.dot(v,r)==0 for v in x['rows']for r in y['rows'])
  raise ValueError('Unsupported inclusion')
 records={f'X{j}':[f'L{j}',1<<j,False]for j in range(111)}|{f'Y{j}':['zero',1<<(111+j),False]for j in range(111)}
 counts=Counter();profile=Counter();history=[];pcharts=set();dirty=0
 for step,o in enumerate(w['operations']):
  kind,n,*rest=o;counts[kind]+=1
  if kind=='INIT':
   assert n not in records;records[n]=[rest[0],0,True]
   if n.startswith('P'):assert all(records[f'X{j}']==['Hub',1<<j,False]for j in range(111))
  elif kind=='ADD':
   d=rest[0];assert records[n][0]==records[d][0];records[d][1]^=records[n][1]
  elif kind=='MOVE':
   dest=rest[0];src,value,owned=records[n];assert sub(dest,src)if owned else sub(src,dest)
   delta=abs(dims[src]-dims[dest]);assert delta;profile[delta]+=1;records[n][0]=dest
   if n.startswith('P')and dest!='zero':pcharts.add(dest)
  elif kind=='CLEAR':assert records[n][2];dirty+=bool(records[n][1]);del records[n]
  for p in range(8):
   name=f'P{p}'
   if name in records and records[name][0]!='Hub':history.append(records[name][1])
  if step+1==w['handoff']:
   assert {n:(x[0],x[1])for n,x in records.items()if x[2]}==w['expected']
 for j in range(111):
  assert records[f'X{j}']==['Hub',1<<j,False]
  assert records[f'Y{j}']==[f'F{j}'if(w['closed']or j in w.get('completed_targets',[]))else'zero',(1<<(111+j))^((1<<j)if j in w.get('completed_targets',[])else 0),False]
 rh=c.rank_f2(history)
 eligible=[i for i in range(111)if any(sub(ch,f'F{i}')for ch in pcharts)]
 terminal=[w['expected'][f'P{q}'][1]for q in range(8)];tr=c.rank_f2(terminal)
 assert not any(v>>111 for v in terminal)
 return {'terminal_rank':tr,'terminal_W_intersection':tr+15-c.rank_f2(terminal+W),'history_public_y_rank':c.rank_f2([v>>111 for v in history]),'counts':dict(counts),'profile':dict(profile),'dirty_clears':dirty,'history_rank':rh,'history_W':rh+15-c.rank_f2(history+W),'history_K':rh+9-c.rank_f2(history+K),'need_W_seeds':c.rank_f2(history+W)-rh,'need_K_seeds':c.rank_f2(history+K)-rh,'eligible':eligible,'history':history}
