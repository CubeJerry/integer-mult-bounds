#!/usr/bin/env python3
"""Delay the class-zero correction across a genuine mixed feedback cell."""
import importlib.util,sys
from pathlib import Path

def configure(repo):
 global c,source_dir
 source_dir=Path(repo)/'research/moonshot-005-program/results/bit-colored-eight-source'
 sys.path.insert(0,str(source_dir))
 spec=importlib.util.spec_from_file_location('_retained_colored_source',source_dir/'construct.py')
 c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
 return c.configure(repo)

def build(depth=4,closed=True):
 w,W=c.build_coloured(coupled=True,closed=False);prefix=0;R0=0;R1suffix=0
 for n,v in w['expected'].items():
  if n.startswith('C0_'):
   _,length,z=n.split('_');length=int(length);z=int(z)
   if length<depth:prefix^=v[1]
   if z==0:R0^=v[1]
   if z==1 and length>=depth:R1suffix^=v[1]
 seed=1^R0^prefix;dest=('A'+str((1<<depth)-1))if depth not in[1,7,8]else({1:'F0',7:'L7',8:'zero'}[depth])
 ops=[];post=[]
 for op in w['operations']:
  if op[0]=='MOVE'and op[1]=='Y0':continue
  if op[0]=='ADD'and op[-1]=='Y0':continue
  if op==['ADD','Y0','P0']:continue
  if op[0]=='ADD'and op[-1]=='P0'and op[1].startswith('X'):continue
  if op==['INIT','P0','Hub']:
   for length in range(7,depth-1,-1):
    n=f'C0_{length}_0'
    if n in w['expected']:ops +=[['MOVE','Y0',w['expected'][n][0]],['ADD',n,'Y0']]
   if not ops[-2:]==[['MOVE','Y0',dest],['ADD',f'C0_{depth}_0','Y0']]:
    # Last class-zero read can be at a deeper chart; reach the feedback chart.
    last=next(o[2]for o in reversed(ops)if o[0]=='MOVE'and o[1]=='Y0')
    if last!=dest:ops +=[['MOVE','Y0',dest]]
   ops +=[op]+[['ADD',f'X{j}','P0']for j in range(111)if seed>>j&1];continue
  ops.append(op)
  if op==['MOVE','P0',dest]:
   ops +=[['ADD','P0','Y0'],['ADD','Y0','P0']]
   for length in range(depth-1,0,-1):
    n=f'C0_{length}_0'
    if n in w['expected']:ops +=[['MOVE','Y0',w['expected'][n][0]],['ADD',n,'Y0']]
 w['expected']['P0']=('zero',R1suffix);w['seeds'][0]=seed;w['handoff']=len(ops);w['closed']=closed
 if closed:
  ops +=[['CLEAR',n]for n in w['expected']]+[['MOVE',f'Y{j}',f'F{j}']for j in range(1,111)]
 w['schema']='delayed-class-zero-mixed-feedback-v1';w['operations']=ops;w['delayed_feedback_depth']=depth;w['delayed_feedback_chart']=dest;w['kernel_x_hex']=hex(1^R0)
 return w,W