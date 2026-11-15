#!/usr/bin/env python3
"""Conditional two-lane source. ADD_LANE is a new, unadmitted local service."""
import argparse,json,copy,hashlib
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
 v=0
 for r in rows:v^=r
 return v
def lift(row,lane):return sum(1<<(2*i+lane)for i in range(111)if row>>i&1)
def elimination(matrix,k):
 M=matrix[:];ops=[]
 def add(a,b):M[b]^=M[a];ops.append((a,b))
 for c in range(k):
  p=next(i for i in range(c,k)if M[i]>>c&1)
  if p!=c:add(p,c);add(c,p);add(p,c)
  for i in range(k):
   if i!=c and M[i]>>c&1:add(c,i)
 assert M==[1<<i for i in range(k)];return ops

def build(base,roots):
 K=[sum(1<<j for j,r in enumerate(roots)if i==j or sum(a*b for a,b in zip(roots[i],r))==0)for i in range(111)]
 ones=(1<<111)-1;hm=K[0]^K[4];h=[hm>>i&1 for i in range(111)];W=[row&(hm if h[i]else ones^hm)for i,row in enumerate(K)]
 W0=independent([row&(ones^hm)for row in W]);assert len(W0)==7
 coeff=independent([v for v in range(1,128)if all((v&a).bit_count()%2==0 for a in [24,32,64])]);assert len(coeff)==4
 U0=[lift(xor(W0[i]for i in range(7)if v>>i&1),0)for v in coeff]+[lift(row,1)for row in W0];assert rank(U0)==11
 W2=[lift(row,lane)for row in W for lane in range(2)];assert rank(W2)==30
 charts=base['charts']
 def ch(s):
  if s==0:return 'Hub'
  if s==255:return 'zero'
  if s.bit_count()==1:return f'F{s.bit_length()-1}'
  if s.bit_count()==7:return f'L{(255^s).bit_length()-1}'
  return f'A{s}'
 cohorts=[];cachevals={};cachecharts={}
 for old in base['cohorts']:
  g=copy.deepcopy(old);S=g['sources'];r=len(g['runs']);slots=[g['carrier']]+g['donors'];sm=sum(1<<i for i in S);mask=lift(sm,0)|lift(sm,1)
  oldrows=[sm]+[sm^(1<<i)for i in g['donors']];old2=[lift(row,a)for row in oldrows for a in range(2)]
  forms=independent([u&mask for u in U0])if h[S[0]]==0 else old2[:]
  assert len(forms)<=2*r;forms=independent(forms+old2)[:2*r];assert len(forms)==2*r
  byslot={(j,a):forms[2*t+a]for t,j in enumerate(slots)for a in range(2)};B=forms[:]
  coords=[(j,a)for j in S for a in range(2)]
  for c in coords:
   if c not in byslot:
    preferred=[c]+[x for x in coords if x!=c]
    unit=next(1<<(2*j+a)for j,a in preferred if rank(B+[1<<(2*j+a)])>len(B));byslot[c]=unit;B.append(unit)
  M=[sum(1<<t for t,(j,a)in enumerate(coords)if byslot[c]>>(2*j+a)&1)for c in coords];restore=elimination(M,2*len(S))
  g.update(block_run_rows_hex=[[hex(forms[2*t]),hex(forms[2*t+1])]for t in range(r)],local_block_matrix_rows=M,restore_lane_add_indices=[list(x)for x in restore],h_class=h[S[0]])
  cohorts.append(g)
  for t,run in enumerate(g['runs']):
   row=forms[2*t:2*t+2]
   for p,q in enumerate(run):
    n=f'C{q}_{len(run)-p}_{h[S[0]]}';oldrow=cachevals.get(n,[0,0]);cachevals[n]=[a^b for a,b in zip(oldrow,row)];cachecharts[n]=ch(sum(1<<a for a in run[p:]))
 assert len(cachevals)==80 and all(all(row)for row in cachevals.values())
 D=[v for row in cachevals.values()for v in row];assert rank(D)==80 and rank(D)+30-rank(D+W2)==19
 selected=[];B=D[:]
 for i,row in enumerate(W2):
  if rank(B+[row])>rank(B):B.append(row);selected.append(i)
 assert len(selected)==11
 ops=[];expected={}
 for i in range(111):ops.extend([['INIT',f'R{i}',f'L{i}'],['ADD',f'X{i}',f'R{i}']]);expected[f'R{i}']=[f'L{i}',[1<<(2*i),1<<(2*i+1)]]
 for n in sorted(cachevals):ops.append(['INIT',n,cachecharts[n]]);expected[n]=[cachecharts[n],cachevals[n]]
 for g in cohorts:
  S=g['sources'];start=ch(g['pattern']);slots=[g['carrier']]+g['donors'];restore=g['restore_lane_add_indices']
  for i in S:
   if start!=f'L{i}':ops.append(['MOVE',f'X{i}',start])
  for a,b in reversed(restore):ops.append(['ADD_LANE',f'X{S[a//2]}',a%2,f'X{S[b//2]}',b%2])
  for i in S:
   if i not in slots:ops.append(['MOVE',f'X{i}','Hub'])
  for i,run in zip(slots,g['runs']):
   current=start
   for p,q in enumerate(run):
    dest=ch(sum(1<<a for a in run[p:]))
    if dest!=current:ops.append(['MOVE',f'X{i}',dest]);current=dest
    ops.append(['ADD',f'X{i}',f'C{q}_{len(run)-p}_{g["h_class"]}'])
   ops.append(['MOVE',f'X{i}','Hub'])
  for a,b in restore:ops.append(['ADD_LANE',f'X{S[a//2]}',a%2,f'X{S[b//2]}',b%2])
 raw0=[[xor(row[a]for n,row in cachevals.items()if n.startswith('C0_')and n.endswith('_'+str(c)))for a in range(2)]for c in [0,1]]
 prefix=[xor(row[a]for n,row in cachevals.items()if n.startswith('C0_')and int(n.split('_')[1])<4)for a in range(2)]
 suffix=[xor(row[a]for n,row in cachevals.items()if n.startswith('C0_')and n.endswith('_1')and int(n.split('_')[1])>=4)for a in range(2)]
 targets=[suffix]+[[0,0]for _ in range(7)]
 for t,i in enumerate(selected):targets[1+t//2][t%2]=W2[i]
 modes=[[xor(row[a]for n,row in cachevals.items()if n.startswith(f'C{q}_'))for a in range(2)]for q in range(8)]
 seeds=[[1<<a^raw0[0][a]^prefix[a]for a in range(2)]]+[[targets[q][a]^modes[q][a]for a in range(2)]for q in range(1,8)]
 ops.extend([['INIT','YM0','zero'],['ADD','Y0','YM0']]);expected['YM0']=['zero',[1<<222,1<<223]]
 current='zero'
 for d in range(7,3,-1):
  n=f'C0_{d}_0'
  if n in cachevals:
   dest=cachecharts[n]
   if current!=dest:ops.append(['MOVE','Y0',dest]);current=dest
   ops.append(['ADD',n,'Y0'])
 if current!='A15':ops.append(['MOVE','Y0','A15'])
 for q in range(8):
  name=f'P{q}';ops.append(['INIT',name,'Hub'])
  for i in range(111):
   block=[[bool(seeds[q][b]>>(2*i+a)&1)for a in range(2)]for b in range(2)]
   if block[0][0]and block[1][1]:ops.append(['ADD',f'X{i}',name]);block[0][0]=block[1][1]=False
   for b in range(2):
    for a in range(2):
     if block[b][a]:ops.append(['ADD_LANE',f'X{i}',a,name,b])
  pattern=0
  for depth in range(1,9):
   pattern|=1<<((q+depth-1)%8);ops.append(['MOVE',name,ch(pattern)])
   if q==0 and depth==4:
    ops.extend([['ADD','P0','Y0'],['ADD','Y0','P0']]);yc='A15'
    for d in range(3,0,-1):
     n=f'C0_{d}_0'
     if n in cachevals:
      dest=cachecharts[n]
      if dest!=yc:ops.append(['MOVE','Y0',dest]);yc=dest
      ops.append(['ADD',n,'Y0'])
    if yc!='F0':ops.append(['MOVE','Y0','F0'])
   for c in [0,1]:
    n=f'C{q}_{depth}_{c}'
    if n in cachevals:ops.append(['ADD',n,name])
   if q==0 and depth==8:ops.append(['ADD','YM0','P0'])
  expected[name]=['zero',targets[q]]
 w={'schema':'conditional-two-lane-cohort-source-v1','record_lanes':2,'retained_compiler_admitted':False,
 'required_new_local_service':{'opcode':'ADD_LANE','semantics':'XOR one selected source half into one selected target half at the same chart','ordinary_cost':'One lane XOR over s coordinates per call at V=2s; uniform access/selector cost separately owed','new_service_count_must_be_charged':True},
 'base_word_sha256':BASE_SHA,'native_roots_sha256':ROOT_SHA,'charts':charts,'operations':ops,'expected':expected,'handoff':len(ops),'closed':False,'cohorts':cohorts,'completed_targets':[0],'order':list(range(8)),
 'W_rows_lanes_hex':[[hex(lift(row,a))for a in range(2)]for row in W],'h_coordinates':9,'W_pivot_h_hex':hex(hm),'seeds_lanes_hex':[[hex(v)for v in row]for row in seeds],
 'increment_space_dimension':80,'increment_W_intersection':19,'selected_W_quotient_rows':[{'role':i//2,'lane':i%2}for i in selected],
 'terminal_rows_hex':[[hex(v)for v in row]for row in targets],'new_complete_kappa':False}
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',n]for n in sorted(expected)]+[['MOVE',f'Y{i}',f'F{i}']for i in range(1,111)]
 return w,closed

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args()
 raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_SHA;rb=(a.repo/ROOT).read_bytes();assert hashlib.sha256(rb).hexdigest()==ROOT_SHA;a.out.mkdir(parents=True,exist_ok=True)
 for n,w in zip(['WORD','CLOSED-WORD'],build(json.loads(raw),json.loads(rb)['native_roots'])):(a.out/(n+'.json')).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_CONDITIONAL_TWO_LANE_SOURCE')
if __name__=='__main__':main()
