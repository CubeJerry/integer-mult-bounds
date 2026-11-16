#!/usr/bin/env python3
"""Add stationary filtered caches and literal principal query histories."""
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
def basis(rows):
 out=[]
 for v in rows:
  if rank(out+[v])>len(out):out.append(v)
 return out
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
def combination(rows,c):
 v=0
 for j,r in enumerate(rows):
  if c>>j&1:v^=r
 return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();base_raw=a.base.read_bytes();assert hashlib.sha256(base_raw).hexdigest()=='8b91f8e82016cd4eadac391500a2ab606d6cdf975ec8f0a752644675a25cba1e';w=json.loads(base_raw);R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=w['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];W=basis(A);S=[int(v,16)for v in w['seed_rows_hex']];points=w['point_targets'];skip=[3,4,8,74,76,78,80];query=[9,19,20,36,37];skipmask=sum(1<<j for j in skip);assert rank([v&skipmask for v in W])==rank([v&skipmask for v in S]);V=[]
 for r in W:
  c=solve([s&skipmask for s in S],r&skipmask);v=r^combination(S,c);assert not(v&skipmask)
  if rank(S+V+[v])>rank(S+V):V.append(v)
 assert len(V)==7 and rank(S+V)==15
 charts=copy.deepcopy(w['charts']);charts['Extra5']={'kind':'span','rows':[R[j]for j in query]};groups=[]
 for c in w['cohorts']:
  if not c['receivers']:continue
  if len(c['receivers'])==1:chart=f"F{c['receivers'][0]}"
  else:chart=next(q['chart']for q in w['cache_metadata']if q['family']==c['h']and q['receivers']==c['receivers'])
  groups.append({'h':c['h'],'receivers':c['receivers'],'roles':c['roles'],'chart':chart})
 groups.append({'h':1,'receivers':[],'roles':query,'chart':'Extra5'})
 fields=[]
 for g,c in enumerate(groups):
  mask=sum(1<<j for j in c['roles'])
  for k,v in enumerate(basis([r&mask for r in V])):fields.append({'name':f'H{g}_{k}','group':g,'chart':c['chart'],'row_hex':hex(v),'roles':[j for j in range(111)if v>>j&1]})
 assert rank(S+[int(c['row_hex'],16)for c in fields])>=15 and rank(S+[int(c['row_hex'],16)for c in fields]+W)==rank(S+[int(c['row_hex'],16)for c in fields])
 pair=lambda ii:next(q['chart']for q in w['cache_metadata']if q['family']==1 and q['receivers']==ii)
 routes=[['F3','M0','zero'],['F76','M0','zero'],['F80','M0','zero'],['F4',pair([4,74]),'M1','zero'],['F74',pair([74,78]),'M1','zero'],['F78',pair([4,78]),'M1','zero'],['Extra5','zero'],['zero']]
 import sympy as sp
 def equal(x,y):
  c,d=charts[x],charts[y];M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);N=sp.Matrix(d['rows'])if d['rows']else sp.zeros(0,8);B=M.rowspace()if c['kind']=='span'else M.nullspace();C=N.rowspace()if d['kind']=='span'else N.nullspace();return len(B)==len(C)and sp.Matrix([list(v)for v in B+C]).rank()==len(B)
 for c in fields:
  hits=[(p,ch)for p,route in enumerate(routes)for ch in route if equal(c['chart'],ch)];assert hits,c;c['packet'],c['read_chart']=hits[0]
 ops=[['INIT',c['name'],c['chart']]for c in fields]
 for o in w['operations'][:w['milestones']['source_cut']]:
  if o[0]=='MOVE'and o[1].startswith('X'):
   j=int(o[1][1:])
   if j in query and o[2]=='Hub':
    ops.append(['MOVE',o[1],'Extra5']);ops += [['ADD',o[1],c['name']]for c in fields if j in c['roles']];ops.append(o);continue
   ops.append(o)
   if o[2]!='Hub':ops += [['ADD',o[1],c['name']]for c in fields if j in c['roles']]
  else:ops.append(o)
 marks={'source_cut':len(ops)};seed=[];reads=[]
 for p,s in enumerate(S):
  ff=[c for c in fields if c['packet']==p];q=0
  for c in ff:q^=int(c['row_hex'],16)
  raw=s^q;hub=[j for j in range(111)if raw>>j&1 and j not in points];early=[j for j in points if raw>>j&1];ops += [['INIT',f'P{p}','Hub']]+[['ADD',f'X{j}',f'P{p}']for j in hub]
  for ch in routes[p]:
   ops.append(['MOVE',f'P{p}',ch])
   for c in ff:
    if c['read_chart']==ch:ops.append(['ADD',c['name'],f'P{p}']);reads.append({'step':len(ops),'packet':f'P{p}','cache':c['name'],'chart':ch,'row_hex':c['row_hex']})
  ops += [['ADD',f'E{j}',f'P{p}']for j in early];seed.append({'field':f'P{p}','row_hex':hex(s),'Hub_seed_row_hex':hex(raw&~sum(1<<j for j in points)),'raw_compensated_seed_row_hex':hex(raw),'query_sum_hex':hex(q),'Hub_original_reads':hub,'early_point_reads':early,'route':routes[p]})
 marks['seed8_before_Y']=len(ops);offset=len(ops)-w['milestones']['seed8_before_Y'];ops+=w['operations'][w['milestones']['seed8_before_Y']:]
 for name,step in w['milestones'].items():
  if step>w['milestones']['seed8_before_Y']:marks[name]=step+offset
 ops += [['CLEAR',c['name']]for c in fields];out=copy.deepcopy(w);out.update({'schema':'actual-singular-history-twelve-v1','base_word_sha256':hashlib.sha256(base_raw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'history_omitted_roles':skip,'history_extra_query_roles':query,'history_groups':groups,'history_cache_metadata':fields,'history_quotient_representatives_hex':[hex(v)for v in V],'principal_query_reads':reads,'seed_metadata':seed,'principal_routes':routes,'history_claim':'All111 W fitting rows lie in actual non-Hub principal packet histories; physical availability at other receivers remains open.'});a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print('history fields',len(fields),'D rank',rank([int(c['row_hex'],16)for c in fields]),'S+D rank',rank(S+[int(c['row_hex'],16)for c in fields]),'counts',dict(Counter(o[0]for o in ops)))
if __name__=='__main__':main()
