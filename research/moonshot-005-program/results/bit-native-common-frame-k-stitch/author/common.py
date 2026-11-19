#!/usr/bin/env python3
"""Shared D12: first four prescribed rows at receivers80 and1, paid word."""
import argparse,gzip,json
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from field import INV,T,reduce,mm,linear_word,add_field,swap_field
B=480;N=111;PUBLIC=2*N*B
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278'}
STAGES=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_LINE','Y_H','Y_D','Y_K','Y_F']
def fid(kind,j,c):return (0 if kind=='X'else N*B)+j*B+c
def rows80(neighbors,j):
 a=[[int(r==c)for c in range(B)]for r in range(4)];p=neighbors.index(j)
 if p==0:
  for r in range(4):a[r][r+1]^=1
 elif 2<=p<=60:
  for r in range(4):a[r][8*(p-1)+r]^=1
 return a
def coeff_add(dst,src,alpha):
 return [['ADD',5*dst+r,5*src+s]for s in range(5)for r in range(5)if T[alpha][1<<s]>>r&1]
def permutation(pairs):
 assert len(pairs)==len({d for d,s in pairs})==len({s for d,s in pairs})
 fields={f for pair in pairs for f in pair};order={f:f for f in fields};pos=order.copy();word=[]
 for dst,val in pairs:
  src=pos[val]
  if src!=dst:
   word+=swap_field(dst,src);old=order[dst];order[src],order[dst]=old,val;pos[old],pos[val]=src,dst
 assert all(order[d]==s for d,s in pairs);return word
def location(stage,f,route,caches):
 if f>=PUBLIC:return caches[f-PUBLIC]['chart']
 kind,j,c,h,d,k,line,term=route[f]
 if kind=='X':
  if stage=='X_NATIVE':return ['L',j]
  if stage=='X_H':return ['H',h]
  if stage=='X_D':return ['D',d]
  if stage=='X_K':return ['K',k]if k is not None else ['Hub']
  if stage=='X_F':return ['F',term]if term is not None else ['Hub']
  return ['Hub']
 if stage in STAGES[:7]:return ['Ground']
 if stage=='Y_LINE':return ['L',line]if line is not None else ['D',d]
 if stage=='Y_H':return ['H',h]if h is not None else ['D',d]
 if stage=='Y_D':return ['D',d]
 if stage=='Y_K':return ['K',k]
 return ['F',j]
def replay(actions,caches,route,neighbors,donors):
 symbolic={};owned=set();counts=Counter();peak=0;dirty=0
 def get(bit):return symbolic.get(bit,1<<bit)if bit<5*PUBLIC else symbolic[bit]
 for a in actions:
  for op in a['word']:
   for bit in op[1:]:assert location(a['stage'],bit//5,route,caches)==a['chart'],(a['tag'],op)
   counts[op[0]]+=1
   if op[0]=='ADD':assert op[1]!=op[2];symbolic[op[1]]=get(op[1])^get(op[2])
   elif op[0]=='INIT':assert op[1]>=5*PUBLIC and op[1]not in owned;owned.add(op[1]);symbolic[op[1]]=0;peak=max(peak,len(owned))
   elif op[0]=='CLEAR':assert op[1]in owned;dirty+=bool(get(op[1]));owned.remove(op[1]);del symbolic[op[1]]
   else:raise AssertionError(op)
 assert not owned
 ax=[b for b in symbolic if b<5*N*B];ay=[b for b in symbolic if 5*N*B<=b<5*PUBLIC];xmask=(1<<(5*N*B))-1;ymask=((1<<(5*PUBLIC))-1)^xmask
 allx=all(symbolic[b]==1<<b for b in ax);ally=all(symbolic[b]&ymask==1<<b for b in ay);targets=[];correct={}
 for i in [80,1]:
  correct[i]=True
  for t in range(4):
   fields=[fid('X',j,c)for j in donors for c,x in enumerate(rows80(neighbors,j)[t]if i==80 else [int(c==t)for c in range(B)])if x]
   for bit in range(5):
    output=5*fid('Y',i,t)+bit;expect=1<<output
    for f in fields:expect^=1<<(5*f+bit)
    correct[i]&=get(output)==expect;targets.append({'output_bit':output,'source_bit_indices':[5*f+bit for f in fields]})
 nonzero={b//5 for b in ay if symbolic[b]&xmask}
 return {'all_original_X_restored':allx,'arbitrary_original_Y_baseline_restored':ally,'target_rows_correct':correct,'ADD':counts['ADD'],'INIT':counts['INIT'],'CLEAR':counts['CLEAR'],'dirty_CLEAR':dirty,'extra_peak_binary_owners':peak,'affected_X_bits':len(ax),'affected_Y_bits':len(ay),'actual_X_dependent_output_fields':len(nonzero),'partial_word_return_rank_lower_bound_fields':N*B-len(nonzero),'target_supports':targets}
