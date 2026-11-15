#!/usr/bin/env python3
"""Reprogram existing cohort run carriers by reversible local linear maps."""
import argparse,json,hashlib,copy
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
BASE_SHA='4cea047c9f28a17c3379d3073a88b3a5d00e6e749214661c9d330a289824d060'

def rank(rows):
 B={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p]
   else:B[p]=r;break
 return len(B)
def independent(rows):
 B=[]
 for r in rows:
  if rank(B+[r])>len(B):B.append(r)
 return B
def xor(rows):
 s=0
 for r in rows:s^=r
 return s
def elimination(matrix,k):
 M=matrix[:];ops=[]
 def add(a,b):M[b]^=M[a];ops.append((a,b))
 for c in range(k):
  p=next(i for i in range(c,k)if M[i]>>c&1)
  if p!=c:add(p,c);add(c,p);add(p,c)
  for i in range(k):
   if i!=c and M[i]>>c&1:add(c,i)
 assert M==[1<<i for i in range(k)]
 return ops

def build(base,roots,plane=(24,32)):
 K=[sum(1<<j for j,r in enumerate(roots)if i==j or sum(a*b for a,b in zip(roots[i],r))==0)for i in range(111)]
 ones=(1<<111)-1;hm=K[0]^K[4];h=[hm>>i&1 for i in range(111)];W=[r&(hm if h[i]else ones^hm)for i,r in enumerate(K)]
 W0=independent([r&(ones^hm)for r in W]);assert len(W0)==7
 coeff=independent([v for v in range(1,128)if all((v&u).bit_count()%2==0 for u in plane)])
 U0=[xor(W0[i]for i in range(7)if v>>i&1)for v in coeff];assert len(U0)==5
 charts=base['charts']
 def ch(s):
  if s==0:return 'Hub'
  if s==255:return 'zero'
  if s.bit_count()==1:return f'F{s.bit_length()-1}'
  if s.bit_count()==7:return f'L{(255^s).bit_length()-1}'
  return f'A{s}'
 cohorts=[];cachevals={};cachecharts={}
 for old in base['cohorts']:
  g=copy.deepcopy(old);S=g['sources'];sm=sum(1<<i for i in S);r=len(g['runs']);carrier=g['carrier'];donors=g['donors'];slots=[carrier]+donors
  oldrows=[sm]+[sm^(1<<i)for i in donors]
  if h[S[0]]==0:
   rows=independent([u&sm for u in U0]);assert len(rows)<=r
   rows=independent(rows+oldrows)[:r]
  else:rows=oldrows
  assert len(rows)==r and rank(rows)==r
  # Select a systematic basis of the same run subspace. Distinct pivot
  # originals carry these rows; every nonpivot original stays pure.
  p=0;pivots=[]
  for col in S:
   hit=next((i for i in range(p,r) if rows[i]>>col&1),None)
   if hit is None:continue
   rows[p],rows[hit]=rows[hit],rows[p]
   for i in range(r):
    if i!=p and rows[i]>>col&1:rows[i]^=rows[p]
   pivots.append(col);p+=1
  assert len(pivots)==r
  slots=pivots;g['carrier']=pivots[0];g['donors']=pivots[1:]
  byslot=dict(zip(slots,rows))
  for j in S:
   if j not in byslot:byslot[j]=1<<j
  M=[sum(1<<t for t,i in enumerate(S)if byslot[j]>>i&1)for j in S];ops=elimination(M,len(S))
  g.update(run_rows_hex=[hex(row)for row in rows],local_matrix_rows=M,restore_add_indices=[list(o)for o in ops],h_class=h[S[0]])
  cohorts.append(g)
  for run,row in zip(g['runs'],rows):
   for p,q in enumerate(run):
    name=f'C{q}_{len(run)-p}_{h[S[0]]}';cachevals[name]=cachevals.get(name,0)^row;cachecharts[name]=ch(sum(1<<t for t in run[p:]))
 cachevals={n:v for n,v in cachevals.items()if v};assert len(cachevals)==80
 D=list(cachevals.values());assert rank(D)==40 and rank(D)+15-rank(D+W)==9
 selected=[];B=D[:]
 for i,row in enumerate(W):
  if rank(B+[row])>rank(B):B.append(row);selected.append(i)
 assert len(selected)==6
 ops=[];expected={}
 for i in range(111):ops.extend([['INIT',f'R{i}',f'L{i}'],['ADD',f'X{i}',f'R{i}']]);expected[f'R{i}']=[f'L{i}',1<<i]
 for n in sorted(cachevals):ops.append(['INIT',n,cachecharts[n]]);expected[n]=[cachecharts[n],cachevals[n]]
 for g in cohorts:
  S=g['sources'];start=ch(g['pattern']);slots=[g['carrier']]+g['donors'];restore=g['restore_add_indices']
  for i in S:
   if start!=f'L{i}':ops.append(['MOVE',f'X{i}',start])
  for a,b in reversed(restore):ops.append(['ADD',f'X{S[a]}',f'X{S[b]}'])
  for i in S:
   if i not in slots:ops.append(['MOVE',f'X{i}','Hub'])
  for i,run in zip(slots,g['runs']):
   current=start
   for p,q in enumerate(run):
    dest=ch(sum(1<<t for t in run[p:]))
    if dest!=current:ops.append(['MOVE',f'X{i}',dest]);current=dest
    ops.append(['ADD',f'X{i}',f'C{q}_{len(run)-p}_{g["h_class"]}'])
   ops.append(['MOVE',f'X{i}','Hub'])
  for a,b in restore:ops.append(['ADD',f'X{S[a]}',f'X{S[b]}'])
 raw0=[xor(v for n,v in cachevals.items()if n.startswith('C0_')and n.endswith('_'+str(c)))for c in [0,1]]
 prefix=xor(v for n,v in cachevals.items()if n.startswith('C0_')and int(n.split('_')[1])<4)
 class1_suffix=xor(v for n,v in cachevals.items()if n.startswith('C0_')and n.endswith('_1')and int(n.split('_')[1])>=4)
 targets=[class1_suffix]+[W[i]for i in selected]+[0]
 modes=[xor(v for n,v in cachevals.items()if n.startswith(f'C{q}_'))for q in range(8)]
 seeds=[1^raw0[0]^prefix]+[targets[q]^modes[q]for q in range(1,8)]
 ops.extend([['INIT','YM0','zero'],['ADD','Y0','YM0']]);expected['YM0']=['zero',1<<111]
 current='zero'
 for depth in range(7,3,-1):
  n=f'C0_{depth}_0'
  if n in cachevals:
   dest=cachecharts[n]
   if dest!=current:ops.append(['MOVE','Y0',dest]);current=dest
   ops.append(['ADD',n,'Y0'])
 if current!='A15':ops.append(['MOVE','Y0','A15'])
 for q in range(8):
  name=f'P{q}';ops.append(['INIT',name,'Hub']);ops.extend([['ADD',f'X{i}',name]for i in range(111)if seeds[q]>>i&1])
  pattern=0
  for depth in range(1,9):
   pattern|=1<<((q+depth-1)%8);dest=ch(pattern);ops.append(['MOVE',name,dest])
   if q==0 and depth==4:
    ops.extend([['ADD','P0','Y0'],['ADD','Y0','P0']]);yc='A15'
    for d in range(3,0,-1):
     n=f'C0_{d}_0'
     if n in cachevals:
      dd=cachecharts[n]
      if dd!=yc:ops.append(['MOVE','Y0',dd]);yc=dd
      ops.append(['ADD',n,'Y0'])
    if yc!='F0':ops.append(['MOVE','Y0','F0'])
   for c in [0,1]:
    n=f'C{q}_{depth}_{c}'
    if n in cachevals:ops.append(['ADD',n,name])
   if q==0 and depth==8:ops.append(['ADD','YM0','P0'])
  expected[name]=['zero',targets[q]]
 w=copy.deepcopy(base);w.update(schema='reprogrammed-cohort-h9-source-v1',operations=ops,expected=expected,handoff=len(ops),closed=False,cohorts=cohorts,seeds=seeds,completed_targets=[0],terminal_W_roles=[None]+selected+[None],increment_space_dimension=40,increment_W_intersection=9,raw_class_zero_query0_hex=hex(raw0[0]),raw_class_one_query0_hex=hex(raw0[1]),W_rows_hex=[hex(v)for v in W],W_pivot_h_hex=hex(hm),reprogramming={'h0_W_basis_hex':[hex(v)for v in W0],'dual_plane':list(plane),'h0_target_coefficients':coeff,'h0_target_rows_hex':[hex(v)for v in U0]},spare_packet_terminal_zero=True,new_complete_kappa=False,base_word_sha256=BASE_SHA)
 w.pop('offsets',None);w.pop('modes',None);w['actual_raw_query_modes_hex']=[hex(v)for v in modes];w['kernel_x_hex']=hex(1^raw0[0])
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',n]for n in sorted(expected)]+[['MOVE',f'Y{i}',f'F{i}']for i in range(1,111)]
 return w,closed

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args()
 rb=(a.repo/ROOT).read_bytes();assert hashlib.sha256(rb).hexdigest()==ROOT_SHA;raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_SHA;a.out.mkdir(parents=True,exist_ok=True)
 for n,w in zip(['WORD','CLOSED-WORD'],build(json.loads(raw),json.loads(rb)['native_roots'])):(a.out/(n+'.json')).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_REPROGRAMMED_COHORT_SOURCE')
if __name__=='__main__':main()
