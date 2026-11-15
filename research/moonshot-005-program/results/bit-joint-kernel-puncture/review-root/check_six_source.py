#!/usr/bin/env python3
"""Independent full six-output replay, using only the reviewer's geometry."""
import argparse,copy,json,hashlib
from pathlib import Path
from collections import Counter
from functools import lru_cache
import sympy as s
from check import chart,rank,dot
@lru_cache(None)
def sub(A,B):
 if not A:return True
 if not B:return False
 return s.Matrix(list(B)+list(A)).rank()==len(B)
def replay(w,roots):
 C={n:chart(v)for n,v in w['charts'].items()};v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':C[f'L{i}']for i in range(111)}|{f'Y{i}':C['zero']for i in range(111)}
 cnt=Counter();prof=Counter();hist=set();dirty=0;born=False
 for op in w['operations']:
  t=op[0];cnt[t]+=1
  if t=='INIT':
   n=op[1];assert n not in v
   if n=='P0'and not born:assert all(v[f'X{i}']==1<<i and loc[f'X{i}']==C['Hub']for i in range(111));born=True
   v[n]=0;loc[n]=C[op[2]]
  elif t=='ADD':x,y=op[1:];assert loc[x]==loc[y];v[y]^=v[x]
  elif t=='MOVE':
   n,d=op[1:];A=loc[n];B=C[d];assert (sub(A,B)if n[0]in'XY'and n[1:].isdigit()else sub(B,A)), (op,len(A),len(B))
   r=abs(len(A)-len(B));assert r>0;prof[r]+=1;loc[n]=B
  elif t=='CLEAR':
   n=op[1];assert not(n[0]in'XY'and n[1:].isdigit());dirty+=bool(v[n]);del v[n];del loc[n]
  else:raise AssertionError(op)
  for q in range(8):
   n=f'P{q}'
   if n in v and loc[n]!=C['Hub']:hist.add(v[n])
 for i in range(111):
  assert v[f'X{i}']==1<<i and loc[f'X{i}']==C['Hub']
  assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in [0,1,2,5,6,7]else 0) and loc[f'Y{i}']==C[f'F{i}']
 assert len(v)==222
 K=[sum(1<<j for j in range(111)if i==j or dot(roots[i],roots[j])==0)for i in range(111)];h=K[0]^K[4];W=[K[i]&sum(1<<j for j in range(111)if (h>>i&1)==(h>>j&1))for i in range(111)]
 assert rank(W)==15 and rank(list(hist))==48 and rank(list(hist)+W)==48
 assert cnt=={'INIT':206,'ADD':966,'MOVE':502,'CLEAR':206} and dirty==206
 assert dict(prof)=={1:190,2:12,3:119,4:72,5:2,7:107}
 return {'counts':dict(cnt),'dirty_clear':dirty,'movement_profile':dict(prof),'history_rank':48,'W_rank_and_intersection':15,'completed':[0,1,2,5,6,7]}
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 f=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(f.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(f.read_text())['native_roots'];w=json.loads(a.word.read_text());r=replay(w,roots);controls={}
 for name,op in [('reset',['ADD','KEEP_P2_L1','P2']),('receiver',['ADD','P3','Y2']),('retirement',['CLEAR','KEEP_P3_L2'])]:
  bad=copy.deepcopy(w);bad['operations'].remove(op)
  try:replay(bad,roots)
  except(AssertionError,KeyError):controls[name]=True
  else:raise AssertionError(name)
 out={'status':'PASS_ROOT_FULL_SIX_AXIS_PARTIAL_SOURCE','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'receipt':r,'negative_controls':controls,'scope':'Literal all222-column construction; complete fixed template excluded separately by arbitrary puncture; no new kappa'};a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
