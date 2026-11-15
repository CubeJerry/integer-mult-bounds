#!/usr/bin/env python3
"""Independent exact native stars, whole cells and input punctures."""
import argparse,json,hashlib
from pathlib import Path
from collections import defaultdict
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
def chart(d):
 M=s.Matrix(d['rows']) if d['rows'] else s.zeros(0,8);v=M.nullspace()if d['kind']=='ann'else[s.Matrix(x)for x in d['rows']]
 if not v:return ()
 A=s.Matrix.hstack(*v).T.rref()[0]
 return tuple(tuple(x for x in A.row(i))for i in range(A.rows)if any(A.row(i)))
def check_star(t,roots):
 E=set(t['deleted_roles']);P=t['point_roles'];edges=t['edges'];assert len(P)==8 and len(set(P))==8 and not E.intersection(P)
 assert all(dot(roots[P[i]],roots[P[j]])!=0 for i in range(8)for j in range(i))
 seen=set();deg=[0]*8;checks=0
 for e in edges:
  i=e['role'];p=e['point_indices'];assert i not in E and i not in P and i not in seen;seen.add(i)
  assert len(p)==2 and [j for j,q in enumerate(P)if dot(roots[i],roots[q])==0]==p
  for j in p:deg[j]+=1
 for i,e in enumerate(edges):
  for f in edges[:i]:
   if set(e['point_indices'])&set(f['point_indices']):assert dot(roots[e['role']],roots[f['role']])!=0;checks+=1
 assert min(deg)>=4 and deg==t['degrees']
 J=[i for i in range(111)if i not in E];K=[sum(1<<j for j in J if i==j or dot(roots[i],roots[j])==0)for i in J];assert rank(K)==9
 return {'edges':len(edges),'degrees':deg,'incidence_checks':checks,'retained_ports':len(J),'canonical_rank':9}
def replay(word,roots):
 keys={n:chart(d)for n,d in word['charts'].items()};zero=keys['zero'];hub=keys['Hub']
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 where={f'X{i}':keys[f'L{i}']for i in range(111)}|{f'Y{i}':zero for i in range(111)}
 formal=defaultdict(dict);incoming=defaultdict(dict);outgoing=defaultdict(dict);first={}
 for op in word['operations']:
  typ=op[0]
  if typ=='INIT':vals[op[1]]=0;where[op[1]]=keys[op[2]];formal[where[op[1]]][op[1]]=0
  elif typ=='ADD':
   x,y=op[1:];C=where[x];assert C==where[y];vals[y]^=vals[x];formal[C][y]=formal[C].get(y,0)^formal[C].get(x,0)
  elif typ=='MOVE':
   n=op[1];C=where[n];D=keys[op[2]];is_p=n.startswith('P')and n[1:].isdigit()
   if C!=D:
    if is_p and C not in [zero,hub]:outgoing[C][n]=formal[C].get(n,0)
    if is_p and D not in [zero,hub]:incoming[D][n]=vals[n];formal[D][n]=1<<int(n[1:])
    else:formal[D][n]=0
    if is_p and D==zero and n not in first:first[n]=vals[n]
   where[n]=D
  elif typ=='CLEAR':del vals[op[1]];del where[op[1]]
  else:raise AssertionError(op)
 cells=[]
 for C,ins in incoming.items():
  names=sorted(ins,key=lambda n:int(n[1:]));outs=[outgoing[C][n]for n in names];null=len(names)-rank(outs)
  if null:
   assert len(names)==1 and null==1 and outs==[0]
   cells.append({'chart':C,'packet':names[0],'row':ins[names[0]],'visible':[i for i in range(111)if all(dot(roots[i],v)==0 for v in C)]})
 return [first[f'P{i}']for i in range(8)],cells,len(incoming)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--four',type=Path,required=True);ap.add_argument('--six',type=Path,required=True);ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 p=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(p.read_text())['native_roots'];cert=json.loads(a.certificate.read_text());out={'status':'PASS_ROOT_JOINT_PUNCTURE_AND_CELL_REVIEW','sources':{},'new_complete_kappa':False};mask=(1<<111)-1
 for label,path in [('four',a.four),('six',a.six)]:
  c=cert['sources'][label];w=json.loads(path.read_text());Z,cells,ncells=replay(w,roots);Tx=[x&mask for x in Z];K=[x['row']&mask for x in cells]
  assert Z==[int(x,16)for x in c['actual_first_ground_rows_hex']]
  assert sorted(K)==sorted(int(x['x_row_hex'],16)for x in c['singular_cells']) and len(cells)==(2 if label=='four'else 4)
  for cell in cells:
   ref=next(x for x in c['singular_cells']if x['packet']==cell['packet']);assert cell['visible']==ref['visible_receiver_roles']
  E=c['arbitrary_puncture_star']['deleted_roles'];keep=mask^sum(1<<i for i in E);vanish=[i for i,x in enumerate(Tx)if not x&keep]
  assert vanish==c['vanishing_terminal_indices'] and 8-len(vanish)+len(cells)==8
  assert rank(Tx)==8 and rank(Tx+K)==(10 if label=='four'else 12) and rank([x&keep for x in Tx+K])==8
  assert rank([x&(keep|(1<<52))for x in Tx+K])==9
  completed=w['completed_targets'];cm=mask^sum(1<<i for i in completed);assert rank([x&cm for x in Tx+K])==9
  invisible=[i for i in range(111)if not any(i in x['visible']for x in cells)];assert invisible==c['kernel_invisible_receiver_roles']
  receipt={'word_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'proper_geometric_cells':ncells,'singular_cells':len(cells),'vanishing_slots':vanish,'normalized_rank':rank(Tx+K),'punctured_rank':8,'star':check_star(c['arbitrary_puncture_star'],roots),'completed_only_rank':9,'omitting_support52_rank':9,'invisible_roles':invisible}
  if 'placement_star'in c:receipt['placement_star']=check_star(c['placement_star'],roots)
  out['sources'][label]=receipt
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
