#!/usr/bin/env python3
"""Independent punctured-star and frozen-access certificate audit."""
import argparse,json,hashlib
from pathlib import Path
from functools import lru_cache
import sympy as s

def rank(rows):
 b={}
 for x in rows:
  while x:
   i=x.bit_length()-1
   if i in b:x^=b[i]
   else:b[i]=x;break
 return len(b)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(native.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 roots=json.loads(native.read_text())['native_roots'];w=json.loads(a.word.read_text());cert=json.loads(a.certificate.read_text());star=cert['punctured_star'];points=star['point_roles'];edges=star['edges'];assert len(points)==8 and 0 not in points and len(set(points))==8
 for i in range(8):
  for j in range(i):assert dot(roots[points[i]],roots[points[j]])!=0
 degrees=[0]*8;edgechecks=0
 for e in edges:
  r=e['role'];ij=e['point_indices'];assert r!=0 and r not in points and len(ij)==2
  assert [j for j,q in enumerate(points)if dot(roots[r],roots[q])==0]==ij
  for j in ij:degrees[j]+=1
 for e in edges:
  for f in edges:
   if e['role']<f['role']and set(e['point_indices'])&set(f['point_indices']):assert dot(roots[e['role']],roots[f['role']])!=0;edgechecks+=1
 assert degrees==[6,7,6,7,7,7,7,7]
 K=[sum(1<<j for j in range(1,111)if i==j or dot(roots[i],roots[j])==0)for i in range(1,111)];assert rank(K)==9
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};where={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};hist=set();mask=(1<<111)-1
 for op in w['operations']:
  if op[0]=='INIT':vals[op[1]]=0;where[op[1]]=op[2]
  elif op[0]=='ADD':vals[op[2]]^=vals[op[1]]
  elif op[0]=='MOVE':where[op[1]]=op[2]
  elif op[0]=='CLEAR':del vals[op[1]];del where[op[1]]
  for q in range(8):
   n=f'P{q}'
   if n in vals and where[n]!='Hub':hist.add((q,where[n],vals[n]))
 T=[vals[f'P{q}']&mask for q in range(8)]
 @lru_cache(None)
 def inside(ch,i):
  if ch=='zero':return True
  if ch=='Hub':return False
  d=w['charts'][ch];M=s.Matrix(d['rows'])
  basis=M.nullspace()if d['kind']=='ann'else[s.Matrix(x)for x in d['rows']]
  return all(dot(roots[i],v)==0 for v in basis)
 local=[sum(1<<j for j in range(111)if dot(roots[i],roots[j])==0)for i in range(111)]
 records={e['receiver']:e for e in cert['frozen_access']['receiver_records']};congruences=0;duals=0;fits=[]
 for i in range(1,111):
  obs=[]
  for q,ch,row in hist:
   if inside(ch,i):
    x=row&mask;assert ((x^T[q])&~local[i])==0;obs.append(x);congruences+=1
  projected=[r&~local[i]for r in T];fit=rank(projected+[1<<i])==rank(projected);assert fit==records[i]['full_fits']
  if fit:fits.append(i)
  else:
   d=int(records[i]['dual_input_hex'],16);assert(d>>i)&1 and d&local[i]==0
   assert all((d&r).bit_count()%2==0 for r in T+obs);duals+=1
 assert len(fits)==11 and duals==99
 # Scope controls: exceptional F0 history is not terminal-local, and a star may not use a deleted vertex.
 assert any(inside(ch,0)and ((row&mask)^T[q])&~local[0]for q,ch,row in hist)
 badpoints=[0]+points[1:];assert not all(dot(roots[badpoints[i]],roots[badpoints[j]])!=0 for i in range(8)for j in range(i))
 out={'status':'PASS_ROOT_PUNCTURED_STAR_AND_FROZEN_DUALS','point_roles':points,'edges':len(edges),'edge_incidence_checks':edgechecks,'degrees':degrees,'punctured_canonical_rank':9,'unique_history_states':len(hist),'terminal_congruences_checked':congruences,'independent_dual_exclusions':duals,'relaxed_fitting_roles':fits,'scope_controls':['F0 has nonterminal history, so it cannot be included in the normalization assertion','Deleted-point replacement invalidates the star premises'],'proof_scope':'Native witness and all99 dual certificates independently checked; universal all-field rank/cell proof reviewed separately','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'new_complete_kappa':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
