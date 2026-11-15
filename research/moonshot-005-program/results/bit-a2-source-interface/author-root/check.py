#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction

def basis(vs):
 d={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in d:v^=d[k]
   else:d[k]=v;break
 return d

def residual(d,v):
 while v:
  k=v.bit_length()-1
  if k not in d:return v
  v^=d[k]
 return 0

def qrank(rows):
 a=[list(map(Fraction,r))for r in rows];k=0
 for j in range(8):
  p=next((i for i in range(k,len(a))if a[i][j]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for i in range(k+1,len(a)):
   v=a[i][j]
   if v:a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  k+=1
 return k

def dual(rows,coordinates,target):
 eq={}
 for v,b in [(v,0)for v in rows]+[(1<<q,int(j==target))for j,q in enumerate(coordinates)]:
  while v:
   k=v.bit_length()-1
   if k in eq:v^=eq[k][0];b^=eq[k][1]
   else:eq[k]=(v,b);break
  if not v:assert b==0
 x=0
 for k,(v,b)in sorted(eq.items()):
  if ((v&x).bit_count()&1)!=b:x^=1<<k
 assert all((v&x).bit_count()%2==0 for v in rows)
 assert [((x>>q)&1)for q in coordinates]==[int(j==target)for j in range(4)]
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];wb=(a.source/'WORD.json').read_bytes();w=json.loads(wb);charts=w['charts'];dot=lambda u,v:sum(x*y for x,y in zip(u,v));where={f'X{j}_{k}':f'L{j}'for j in range(111)for k in range(4)}|{f'Y{j}_{k}':'zero'for j in range(111)for k in range(4)};values={f'X{j}_{k}':1<<(4*j+k)for j in range(111)for k in range(4)}|{f'Y{j}_{k}':0 for j in range(111)for k in range(4)}
 can=[sum(1<<(4*j+k)for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)for k in range(4)];G=basis(can);assert len(G)==36
 reach={}
 for c,d in charts.items():
  rows=d['rows'];reach[c]=[i for i in range(111)if (all(dot(r,R[i])==0 for r in rows)if d['kind']=='span'else qrank(rows+[R[i]])==qrank(rows))]
 cut=w['milestones']['canonical36_at_ground_before_all_Y_moves'];local=[set()for _ in range(111)];sourceevents=[]
 def record(name,step):
  if name.startswith('Y'):return
  v=values[name];c=where[name]
  if v:
   for i in reach[c]:local[i].add(v)
   sourceevents.append((step,name,c,hex(v)))
 for step,op in enumerate(w['operations'],1):
  tag=op[0]
  if tag=='INIT':values[op[1]]=0;where[op[1]]=op[2]
  elif tag=='MOVE':where[op[1]]=op[2]
  elif tag=='ADD':
   if not op[2].startswith('Y'):assert not op[1].startswith('Y'),'source feedback not in model'
   values[op[2]]^=values[op[1]]
  elif tag=='CLEAR':del values[op[1]];del where[op[1]]
  else:raise AssertionError(tag)
  if step==cut:
   assert all(where[f'Y{j}_{k}']=='zero'and values[f'Y{j}_{k}']==0 for j in range(111)for k in range(4));ps=[values[n]for n in values if n.startswith('P')];assert len(ps)==36 and len(basis(ps))==36 and all(residual(G,v)==0 for v in ps)
   for n in list(values):record(n,step)
  elif step>cut and tag!='CLEAR':record(op[2]if tag=='ADD'else op[1],step)
 cases=[]
 for i in range(111):
  rows=list(G.values())+sorted(local[i]);B=basis(rows);E=[1<<(4*i+k)for k in range(4)];gain=len(basis(list(B.values())+E))-len(B);ds=[]
  if i not in [3,76,80]:
   assert gain==4,(i,gain);ds=[hex(dual(list(B.values()),[4*i+k for k in range(4)],j))for j in range(4)]
  else:assert gain==0
  cases.append({'receiver':i,'source_grant_rank':len(B),'additional_local_rank':len(B)-36,'target_quotient_rank':gain,'dual_witnesses_hex':ds})
 controls={}
 i=0;rs=list(G.values())+sorted(local[i]);controls['granting_four_new_point_fields_removes_obstruction']=len(basis(rs+[1<<(4*i+k)for k in range(4)]))-len(basis(rs))==4
 controls['three_actual_completed_receivers_pass']=all(cases[i]['target_quotient_rank']==0 for i in[3,76,80]);assert all(controls.values())
 out={'status':'PASS_EXACT_FROZEN_A2_SOURCE_CONTINUATION_CERTIFICATE','source_word_sha256':hashlib.sha256(wb).hexdigest(),'canonical_cut':cut,'canonical_dimension':36,'source_history_grant':'All fixed X/owned rows at every later event whose actual chart is contained in the receiver facet, plus canonical36 granted freely. Original-Y X components are not extra source generators.','all_receivers':cases,'remaining_receivers_with_full_four_dimensional_obstruction':108,'negative_scope_controls':controls,'scope':'Frozen X/owned trajectories and values after canonical cut, no new source captures/imports. Arbitrary linear upward Y relays allowed. Not a no-go for changing or enlarging the source.','universal_statement':'Exact binary witnesses extend to every characteristic-two field and positive record width.','new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'obstructed':108,'rank_histogram':{str(k):sum(c['source_grant_rank']==k for c in cases)for k in sorted({c['source_grant_rank']for c in cases})},'word_sha256':out['source_word_sha256']}))
if __name__=='__main__':main()
