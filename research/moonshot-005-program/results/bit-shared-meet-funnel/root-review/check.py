#!/usr/bin/env python3
"""Independent root word replay; no imports of author's code."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
from copy import deepcopy

def rr(rows):
 a=[[F(v)for v in row]for row in rows];lead=0
 for col in range(8):
  p=next((i for i in range(lead,len(a))if a[i][col]),None)
  if p is None:continue
  a[lead],a[p]=a[p],a[lead];z=a[lead][col];a[lead]=[v/z for v in a[lead]]
  for i in range(len(a)):
   if i!=lead and a[i][col]:
    z=a[i][col];a[i]=[v-z*w for v,w in zip(a[i],a[lead])]
  lead+=1
 return tuple(tuple(row)for row in a[:lead])

def null(rows):
 a=rr(rows);piv=[next(i for i,v in enumerate(row)if v)for row in a];out=[]
 for free in range(8):
  if free in piv:continue
  v=[F(0)]*8;v[free]=F(1)
  for row,p in zip(a,piv):v[p]=-row[free]
  out.append(v)
 return rr(out)

def rank(rows):
 d={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in d:v^=d[p]
   else:d[p]=v;break
 return len(d)

def need(ok,msg):
 if not ok:raise ValueError(msg)

def replay(w,R,marks=True):
 C={n:rr(c['rows'])if c['kind']=='span'else null(c['rows'])for n,c in w['charts'].items()}
 need(C['Hub']==rr([[int(i==j)for i in range(8)]for j in range(8)])and C['zero']==(),'extreme charts')
 for j,r in enumerate(R):need(C[f'L{j}']==rr([r])and C[f'F{j}']==null([r]),'native charts')
 @lru_cache(None)
 def movement(a,b,owned):
  small,large=(b,a)if owned else(a,b)
  need(len(rr(C[small]+C[large]))==len(C[large]),'illegal movement direction')
  return abs(len(C[a])-len(C[b]))
 v={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)}
 loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)}
 orig=set(v);ever=set(v);owned=set();arrived=set();first=[];hist=[];peak=dirty=0;counts=Counter();profile=Counter();snap={}
 K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
 need(rank(K)==9,'canonical rank');cut=w['milestones'].get('canonical9_before_Y')
 for k,o in enumerate(w['operations'],1):
  op=o[0];counts[op]+=1
  if op=='INIT':
   _,n,c=o;need(n not in ever and c in C,'initialization');ever.add(n);owned.add(n);v[n]=0;loc[n]=c;peak=max(peak,len(owned))
  elif op=='ADD':
   _,a,b=o;need(a in v and b in v and a!=b,'ADD fields');need(C[loc[a]]==C[loc[b]],'nonlocal ADD');v[b]^=v[a]
   if b.startswith('P'):hist.append(v[b])
  elif op=='MOVE':
   _,n,c=o;need(n in v and c in C,'MOVE fields');profile[movement(loc[n],c,n in owned)]+=1;loc[n]=c
   if n in owned and C[c]==()and n not in arrived:arrived.add(n);first.append(v[n])
  elif op=='CLEAR':
   _,n=o;need(n in owned,'CLEAR fields');dirty+=bool(v[n]);owned.remove(n);del v[n];del loc[n]
  else:raise ValueError('unknown operation')
  if marks and k==cut:
   rows=[v[f'P{q}']for q in range(9)];need(rank(rows)==rank(rows+K)==9,'canonical code');need(all(C[loc[f'P{q}']]==()for q in range(9)),'canonical place')
   need(all(v[f'Y{j}']==1<<(111+j)and C[loc[f'Y{j}']]==()for j in range(111)),'premature receiver')
   snap={'canonical_rank':9,'arrival_rank':rank(first),'literal_principal_history_rank':rank(hist)}
 for j in range(111):
  need(v[f'X{j}']==1<<j and C[loc[f'X{j}']]==C['Hub'],'X restoration')
  need(v[f'Y{j}']==((1<<(111+j))^((1<<j)if j in w['targets']else 0)),'Y endpoint')
  need(C[loc[f'Y{j}']]==C[f'F{j}'],'Y chart')
 need(not owned and set(v)==orig,'retirement')
 return {'columns':222,'targets':w['targets'],'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'peak_owners':peak,'dirty_clears':dirty,'canonical_cut':snap}

def late_helpers(w):
 o=deepcopy(w);ops=o['operations'];helpers={}
 for j in w['early_point_helper_originals']:
  n=f'E{len(helpers)}';helpers[n]=j
  need(ops[:3]==[['INIT',n,f'L{j}'],['ADD',f'X{j}',n],['MOVE',n,'zero']],'early prefix');ops=ops[3:]
 idx=next(k for k,x in enumerate(ops)if x[:2]==['INIT','P0']);loc={f'X{j}':f'L{j}'for j in range(111)}
 for x in ops[:idx]:
  if x[0]=='MOVE'and x[1]in loc:loc[x[1]]=x[2]
 insert=[]
 for n,j in helpers.items():insert.extend([['INIT',n,loc[f'X{j}']],['ADD',f'X{j}',n],['MOVE',n,'zero']])
 o['operations']=ops[:idx]+insert+ops[idx:];o['milestones']={};return o

def main():
 from budget import budget
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();reports={}
 for variant in ['four','six']:
  raw=(a.author/variant/'WORD.json').read_bytes();w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();need(hashlib.sha256(source).hexdigest()==w['source_sha256'],'source pin');R=json.loads(source)['native_roots'];r=replay(w,R);r['word_sha256']=hashlib.sha256(raw).hexdigest();r['budget']=budget(r['movement_profile']);controls=[]
  preds=[('cache capture',lambda o:o[0]=='ADD'and o[2].startswith('A')),('cache descent',lambda o:o[0]=='MOVE'and o[1].startswith('A')),('canonical source',lambda o:o[0]=='ADD'and o[2].startswith('P')),('held query',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('P')and int(o[1][1:])in w['held_originals']),('singleton delivery',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('Y')),('retirement',lambda o:o[0]=='CLEAR')]
  if variant=='six':preds += [('early capture',lambda o:o[0]=='ADD'and o[2].startswith('E')),('ground repair',lambda o:o[0]=='ADD'and o[1].startswith('E'))]
  for label,pred in preds:
   x=deepcopy(w);i=next(i for i,op in enumerate(x['operations'])if pred(op));del x['operations'][i]
   try:replay(x,R,False)
   except ValueError as e:controls.append({'control':label,'rejected':str(e)})
   else:raise AssertionError('accepted mutant:'+label)
  r['independent_semantic_controls']=controls
  if variant=='six':
   lr=replay(late_helpers(w),R,False);lr['budget']=budget(lr['movement_profile']);need(lr['budget']['first_positive_even_m']is None,'late price');r['valid_late_helper_control']=lr
  reports[variant]=r
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_MEET_FUNNEL_REPLAY','reports':reports,'new_complete_kappa':False},indent=2)+'\n')
 print(json.dumps({k:{'counts':v['counts'],'first_positive_even_m':v['budget']['first_positive_even_m'],'Q':v['budget']['moment']['display_lower']}for k,v in reports.items()}))

if __name__=='__main__':main()
