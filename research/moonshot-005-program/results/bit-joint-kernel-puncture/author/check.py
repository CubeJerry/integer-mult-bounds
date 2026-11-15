#!/usr/bin/env python3
"""Exact native placement and arbitrary-puncture gates; no author imports."""
from __future__ import annotations
import argparse,copy,hashlib,json
from pathlib import Path
from collections import defaultdict
import sympy as sp
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
FOUR_SHA='2b13e0b8d534b90b3284ac93a49b5c3d7e79a6cfe0591ac7a8a1889a29fb856b'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 B={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p]
   else:B[p]=r;break
 return len(B)
def support(r):return [i for i in range(111)if r>>i&1]
def star(R,deleted,frame):
 keep=set(range(111))-set(deleted)
 need(len(frame)==8 and len(set(frame))==8 and set(frame)<=keep,'point frame is not eight distinct retained native roles')
 need(all(dot(R[i],R[j])!=0 for i in frame for j in frame),'point frame has forbidden contact')
 edges={}
 for i in sorted(keep-set(frame)):
  pair=tuple(a for a,p in enumerate(frame)if dot(R[i],R[p])==0)
  if len(pair)==2:
   need(pair not in edges,'duplicate edge role for displayed graph')
   edges[pair]=i
 deg=[sum(a in p for p in edges)for a in range(8)]
 need(min(deg)>=4,'star minimum degree below four')
 checks=[]
 for p,i in edges.items():
  for q,j in edges.items():
   if p<q and set(p)&set(q):
    d=dot(R[i],R[j]);need(d!=0,'incident edges have a forbidden contact');checks.append([i,j,d])
 K=[sum(1<<j for j in keep if i==j or dot(R[i],R[j])==0)for i in sorted(keep)]
 need(rank(K)==9,'characteristic-two punctured canonical attainment changed')
 return {'deleted_roles':sorted(deleted),'retained_count':len(keep),'point_roles':frame,
  'edges':[{'point_indices':list(p),'role':i}for p,i in sorted(edges.items())],
  'degrees':deg,'incident_noncontact_checks':checks,'characteristic_two_minimum_rank_per_width':9,
  'all_fields_minimum_rank_lower_bound_per_width':9}
def basis(chart):
 M=sp.Matrix(chart['rows'])if chart['rows']else sp.zeros(0,8)
 V=M.rowspace()if chart['kind']=='span'else M.nullspace()
 if not V:return ()
 A=sp.Matrix([list(v)for v in V]);B=A.rref()[0]
 return tuple(tuple(B[i,j]for j in range(8))for i in range(B.rows)if any(B[i,j]for j in range(8)))
def source(word,R):
 charts={name:basis(c)for name,c in word['charts'].items()}
 keys={b:[]for b in charts.values()}
 for n,b in charts.items():keys[b].append(n)
 packet={f'P{j}'for j in range(8)}
 value={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 loc={f'X{i}':charts[f'L{i}']for i in range(111)}|{f'Y{i}':()for i in range(111)}
 Z={};entries={};packets_by_cell=defaultdict(list)
 for n in packet:
  for op in word['operations']:
   if op[0]=='MOVE'and op[1]==n and 0<len(charts[op[2]])<8:
    C=charts[op[2]];need(n not in packets_by_cell[C],'packet revisits geometric cell');packets_by_cell[C].append(n)
 cell_values={C:{}for C in packets_by_cell};departures={C:{}for C in packets_by_cell}
 for step,op in enumerate(word['operations']):
  kind,n,*args=op
  if kind=='INIT':
   need(n not in value,'owner rebirth');value[n]=0;loc[n]=charts[args[0]]
   if loc[n]in cell_values:cell_values[loc[n]][n]=0
  elif kind=='ADD':
   t=args[0];need(loc[n]==loc[t],'noncochart ADD');value[t]^=value[n]
   C=loc[n]
   if C in cell_values:cell_values[C][t]=cell_values[C].get(t,0)^cell_values[C].get(n,0)
  elif kind=='MOVE':
   C=loc[n];target=charts[args[0]]
   if C in cell_values:
    if n in packet:departures[C][n]=cell_values[C].get(n,0)
    cell_values[C].pop(n,None)
   loc[n]=target
   if target in cell_values:
    cell_values[target][n]=(1<<packets_by_cell[target].index(n))if n in packet else 0
   if n in packet:
    if 0<len(target)<8:entries[(target,n)]=value[n]
    if len(target)==0:
     need(n not in Z,'packet has repeated first ground arrival');Z[n]=value[n]
  elif kind=='CLEAR':
   C=loc[n]
   if C in cell_values:cell_values[C].pop(n,None)
   del value[n],loc[n]
  else:raise ValueError(kind)
 need(set(Z)==packet,'missing actual first-ground value')
 singular=[]
 for C,names in packets_by_cell.items():
  rows=[departures[C][n]for n in names]
  nullity=len(names)-rank(rows)
  if nullity:
   need(len(names)==1 and rows==[0],'application requires single-packet zero through cell')
   n=names[0];g=entries[(C,n)]
   visible=[i for i,r in enumerate(R)if all(dot(v,r)==0 for v in C)]
   singular.append({'chart_aliases':sorted(keys[C]),'dimension':len(C),'packet':n,'nullity_per_width':1,
    'through_rows':rows,'actual_boundary_row_hex':hex(g),'x_row_hex':hex(g&((1<<111)-1)),
    'visible_receiver_roles':visible})
 singular.sort(key=lambda x:x['packet'])
 T=[Z[f'P{j}']&((1<<111)-1)for j in range(8)]
 G=T+[int(s['x_row_hex'],16)for s in singular]
 unseen=sorted(set(range(111))-set().union(*(set(s['visible_receiver_roles'])for s in singular)))
 kmask=sum(1<<i for i in unseen)
 K=[sum(1<<j for j in unseen if i==j or dot(R[i],R[j])==0)for i in unseen]
 return {'actual_first_ground_rows_hex':[hex(Z[f'P{j}'])for j in range(8)],'terminal_x_rows_hex':[hex(t)for t in T],
  'terminal_x_rank':rank(T),'singular_cells':singular,'normalized_x_rank':rank(G),
  'kernel_invisible_receiver_roles':unseen,'invisible_canonical_rank':rank(K),
  'invisible_terminal_rank':rank([t&kmask for t in T])},T,G

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--four',type=Path,required=True)
 p.add_argument('--six',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 raw=(a.repo/ROOT).read_bytes();need(hashlib.sha256(raw).hexdigest()==ROOT_SHA,'native roots pin changed');R=json.loads(raw)['native_roots']
 need(len(R)==111,'native size');out={'status':'PASS_JOINT_PLACEMENT_AND_ARBITRARY_PUNCTURE','native_sha256':ROOT_SHA,'sources':{},'new_complete_kappa':False}
 Es={'four':set([0,5,6,7]+list(range(52,59))),'six':set([0,1,2,5,6,7]+list(range(52,59)))}
 frames={'four':[1,8,9,30,37,46,73,77],'six':[3,59,62,66,68,83,104,106]}
 for tag,path in [('four',a.four),('six',a.six)]:
  wb=path.read_bytes();w=json.loads(wb);sha=hashlib.sha256(wb).hexdigest()
  if tag=='four':need(sha==FOUR_SHA,'frozen four-axis source changed')
  record,T,G=source(w,R);ns=2 if tag=='four'else 4
  need(record['terminal_x_rank']==8 and record['normalized_x_rank']==8+ns,'source dimension changed')
  need(len(record['singular_cells'])==ns,'unaccounted actual singular chart')
  need(T[0]==sum(1<<i for i in range(52,59))and T[1]==sum(1<<i for i in [0,5,6,7]),'mandatory aggregate terminals changed')
  if tag=='six':need(T[2]==2 and T[3]==4,'mandatory point terminals changed')
  E=Es[tag];mask=((1<<111)-1)^sum(1<<i for i in E)
  zero=[i for i,t in enumerate(T)if not(t&mask)]
  need(zero==list(range(ns)),'vanishing terminal count changed')
  need(rank([T[i]for i in zero])==ns,'vanishing terminal directions not independent')
  projected=rank([g&mask for g in G]);need(projected==8,'actual punctured global rank changed')
  completed=set(w['completed_targets']);cmask=((1<<111)-1)^sum(1<<i for i in completed)
  need(rank([g&cmask for g in G])==9,'completed-only positive control no longer has rank9')
  record.update(word_sha256=sha,arbitrary_puncture_star=star(R,E,frames[tag]),vanishing_terminal_indices=zero,
    actual_punctured_global_rank=projected,universal_reseeded_rank_ceiling_per_width=8,
    completed_only_puncture={'deleted_roles':sorted(completed),'actual_global_rank':9,'scope':'passes only this rank-capacity comparison; not a decoder'})
  if tag=='four':
   need(len(record['kernel_invisible_receiver_roles'])==99,'four-cell visibility changed')
   record['placement_star']=star(R,set(range(111))-set(record['kernel_invisible_receiver_roles']),[5,30,32,38,39,46,103,107])
  else:
   need(record['kernel_invisible_receiver_roles']==[8,9,10,11,12,13,46,47,48,49,50,51],'six-source invisible set changed')
   need(record['invisible_canonical_rank']==4,'six-source invisible canonical rank changed')
  out['sources'][tag]=record
 controls={}
 try:star(R,Es['four']|{1},frames['four'])
 except ValueError as e:controls['delete_displayed_point']={'rejected':True,'reason':str(e)}
 else:raise ValueError('invalid star accepted')
 w=json.loads(a.four.read_text());rec,T,G=source(w,R);wrongE=Es['four']-{52};mask=((1<<111)-1)^sum(1<<i for i in wrongE)
 need(rank([g&mask for g in G])==9,'missing support-column control')
 controls['omit_one_mandatory_support_column']={'rejected':True,'actual_global_rank':9,'reason':'P0 terminal no longer vanishes; rank8 ceiling cannot be asserted.'}
 out['negative_controls']=controls
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'four_deleted':11,'six_deleted':13,'actual_punctured_global_ranks':[8,8],
  'remaining_minrank_floors':[9,9],'four_invisible':99,'six_invisible':12},sort_keys=True))
if __name__=='__main__':main()
