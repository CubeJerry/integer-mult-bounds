#!/usr/bin/env python3
"""Color-separated eight-query source with a singular Y0 feedback cell.

The h pivot is B(r0+r4, .). Seven freely seeded terminals complete actual
W15 history; one coupled packet finishes Y0. No complete supplier is claimed.
"""
import copy
import core as p

def configure(repo):
 global c
 result=p.configure(repo);c=p.c
 return result

def build_coloured(h_coordinate=9,coupled=True,closed=True):
 if h_coordinate!=9:raise ValueError('This frozen construction uses pivot9 only')
 hm=p.K[0]^p.K[4];h=[hm>>i&1 for i in range(111)];ones=(1<<111)-1
 W=[row&(hm if h[i]else ones^hm)for i,row in enumerate(p.K)]
 seedbase=p.build(closed=False);w=p.build(A=seedbase['offsets'],closed=False)
 values={};cachecharts={}
 for group in w['cohorts']:
  S=group['sources'];zs={h[j]for j in S};assert len(zs)==1;z=next(iter(zs))
  groupvalues=[c.mask(S)]+[c.mask(S)^(1<<j)for j in group['donors']]
  for run,row in zip(group['runs'],groupvalues):
   for pos,q in enumerate(run):
    old=f'C{q}_{len(run)-pos}';name=old+f'_{z}'
    values[name]=values.get(name,0)^row;cachecharts[name]=w['expected'][old][0]
 values={n:v for n,v in values.items()if v}
 D=list(values.values());basis=list(D);selected=[]
 for i,row in enumerate(W):
  if c.rank_f2(basis+[row])>c.rank_f2(basis):basis.append(row);selected.append(i)
 assert len(selected)==7
 raw0=[0,0]
 for n,v in values.items():
  if n.startswith('C0_'):raw0[int(n.split('_')[2])]^=v
 raw_modes=[0]*8
 for n,v in values.items():raw_modes[int(n.split('_')[0][1:])]^=v
 seeds=[(1<<0)^raw0[0]]+[W[i]^raw_modes[q]for q,i in enumerate(selected,1)]
 raw=w['operations'];ops=[]
 for op in raw:
  kind,n,*rest=op
  if kind=='INIT'and n.startswith('C'):
   for z in[0,1]:
    nn=n+f'_{z}'
    if nn in values:ops +=[['INIT',nn,rest[0]]]
  elif kind=='ADD'and rest[0].startswith('C'):
   assert n.startswith('X');nn=rest[0]+f'_{h[int(n[1:])]}'
   assert nn in values;ops +=[['ADD',n,nn]]
  elif kind=='ADD'and n.startswith('C'):
   for z in[0,1]:
    nn=n+f'_{z}'
    if nn in values:ops +=[['ADD',nn,rest[0]]]
  else:
   ops.append(op)
   if kind=='INIT'and n.startswith('P'):
    seed=seeds[int(n[1:])]
    for j in range(111):
     if seed>>j&1:ops +=[['ADD',f'X{j}',n]]
 w['expected']={n:v for n,v in w['expected'].items()if not n.startswith('C')}
 w['expected'].update({n:(cachecharts[n],v)for n,v in values.items()})
 for q in range(8):
  row=seeds[q]
  for n,v in values.items():
   if n.startswith(f'C{q}_'):row^=v
  w['expected'][f'P{q}']=('zero',row)
 if coupled:
  at=next(i for i,o in enumerate(ops)if o==['INIT','P0','Hub'])
  pre=[['INIT','YM0','zero'],['ADD','Y0','YM0']]
  for length in range(7,0,-1):
   name=f'C0_{length}_0'
   if name in values:pre +=[['MOVE','Y0',cachecharts[name]],['ADD',name,'Y0']]
  ops[at:at]=pre
  first=next(i for i,o in enumerate(ops)if o==['MOVE','P0','F0'])+1
  ops[first:first]=[['ADD','P0','Y0'],['ADD','Y0','P0']]
  last=next(i for i,o in enumerate(ops)if o==['MOVE','P0','zero'])+1
  ops[last:last]=[['ADD','YM0','P0']]
  w['expected']['P0']=('zero',raw0[1]);w['expected']['YM0']=('zero',1<<111)
 w['handoff']=len(ops);w['closed']=closed
 if closed:
  for n in w['expected']:ops +=[['CLEAR',n]]
  for j in range(111):
   if not coupled or j!=0:ops +=[['MOVE',f'Y{j}',f'F{j}']]
 w['schema']='colored-eight-query-h9-source-v1';w['new_complete_kappa']=False;w['operations']=ops;w['seeds']=seeds;w['W_pivot_h_hex']=hex(hm);w['h_coordinates']=h_coordinate;w['W_rows_hex']=[hex(x)for x in W];w['terminal_W_roles']=[None]+selected;w['coupled']=coupled;w['completed_targets']=[0]if coupled else[]
 w['increment_space_dimension']=c.rank_f2(D);w['increment_W_intersection']=c.rank_f2(D)+15-c.rank_f2(D+W);w['raw_class_zero_query0_hex']=hex(raw0[0]);w['raw_class_one_query0_hex']=hex(raw0[1])
 return w,W

def replay(word,W):
 result=p.replay(word,W)
 if result['history_W']!=15:raise ValueError('Full W history missing')
 if result['eligible']!=list(range(111)):raise ValueError('Positive packet-chart coverage lost')
 return result
