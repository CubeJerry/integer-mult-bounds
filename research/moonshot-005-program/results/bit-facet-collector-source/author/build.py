#!/usr/bin/env python3
"""Exploratory ordinary two-copy facet collectors and three canonical feedbacks."""
import json,copy,hashlib,argparse,types
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
def independent(rows):
 b=[]
 for x in rows:
  if rank(b+[x])>len(b):b.append(x)
 return b
def xor(rows):
 v=0
 for x in rows:v^=x
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
 assert M==[1<<i for i in range(k)]
 return ops
m=types.SimpleNamespace(rank=rank,independent=independent,xor=xor,lift=lift,elimination=elimination)
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');args=p.parse_args()
source_bytes=args.source.read_bytes();assert hashlib.sha256(source_bytes).hexdigest()=='915c72ad64a259e201c17772d9a7bc1880e4baf733db955af9405553527aca87';native_bytes=(args.repo/ROOT).read_bytes();base=json.loads(source_bytes);roots=json.loads(native_bytes)['native_roots']
assert hashlib.sha256(native_bytes).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
M=(1<<222)-1;bank=[sum(1<<(2*i+a)for i in range(111))for a in range(2)];K=[sum(1<<(2*j+a)for j in range(111)if i==j or sum(x*y for x,y in zip(roots[i],roots[j]))==0)for i in range(111)for a in range(2)]
def ch(s):
 if s==0:return 'Hub'
 if s==255:return 'zero'
 if s.bit_count()==1:return f'F{s.bit_length()-1}'
 if s.bit_count()==7:return f'L{(255^s).bit_length()-1}'
 return f'A{s}'
def original(c):return f'X{c[0]}_b{c[1]}'
def singleton(c):return 1<<(2*c[0]+c[1])
def select_facet(pattern):return next(q for q in [0,1,2,4]if pattern>>q&1)
cohorts=[];cache={};corr={(0,0):[],(0,1):[],(1,0):[]};held={(2,0),(3,0)};S01=(K[0]^1)&(sum(1<<(2*j)for j in range(111)if sum(x*y for x,y in zip(roots[1],roots[j]))==0))
assert S01>>4&1 and S01>>6&1
# Original source run spaces are preserved, but individual forms are captured at final facets.
for gi,old in enumerate(base['cohorts']):
 S=old['sources'];pattern=old['pattern'];coords=[(j,a)for j in S for a in range(2)];slots=[(j,a,len(run))for j,run in zip([old['carrier']]+old['donors'],old['runs'])for a in range(2)];slots.sort(key=lambda x:(-x[2],x[0],x[1]))
 oldforms=[int(r,16)for row in old['block_run_rows_hex']for r in row];sm=sum(1<<j for j in S);full=[m.lift(sm,a)for a in range(2)]
 assert all(m.rank(oldforms+[r])==len(oldforms)for r in full)
 forms=m.independent(full+oldforms);assert len(forms)==len(slots)
 byslot={};descs=[]
 for t,(slot,row)in enumerate(zip(slots,forms)):
  j,a,length=slot;sourcebank=0 if not row&bank[1]else 1 if not row&bank[0]else None
  isfull=t<2
  q=(0 if pattern&1 else 1 if t==0 and pattern&2 else select_facet(pattern))if isfull else select_facet(pattern)
  if isfull and t==1 and pattern&1:q=0
  packetbank=t if isfull else ((t+gi)&1)
  others=[z for z in range(8)if pattern>>z&1 and z!=q]
  if t==0 and pattern&3==3:
   assert length>=2
   order=[z for z in others if z!=1][:length-2]+[1,0]
  else:order=others[:length-1]+[q]
  assert len(order)==length and len(set(order))==length
  name=f'FC{gi}_{t}';rowactual=row
  if (j,a) in held:
   assert S==[j] and row==singleton((j,a));q=0 if j==2 else 1;packetbank=0;order=[];rowactual=row^S01
  cache[name]={'chart':f'F{q}','row':rowactual,'query':q,'bank':packetbank,'source_form':row,'cohort':gi,'slot':[j,a],'full_bank':t if isfull else None}
  if isfull:
   f=t
   if pattern&1 and f==1:corr[(0,1)].append(name)
   if f==0:
    if pattern&1 and not pattern&2:corr[(0,0)].append(name)
    if pattern&2 and not pattern&1:corr[(1,0)].append(name)
  if (j,a)==(2,0):corr[(0,0)].append(name)
  if (j,a)==(3,0):corr[(1,0)].append(name)
  byslot[(j,a)]=row;descs.append({'slot':[j,a],'row':row,'actual_row':rowactual,'route':order,'cache':name,'shared_full':t==0 and pattern&3==3})
 Bs=forms[:]
 for c in coords:
  if c not in byslot:
   unit=next(singleton(z)for z in [c]+[x for x in coords if x!=c]if m.rank(Bs+[singleton(z)])>len(Bs));byslot[c]=unit;Bs.append(unit)
 mat=[sum(1<<t for t,c in enumerate(coords)if byslot[z]&singleton(c))for z in coords];restore=m.elimination(mat,len(coords));cohorts.append({'sources':S,'pattern':pattern,'coords':coords,'descs':descs,'restore':restore})
old_D=[r for n,(_,row)in base['expected'].items()if n.startswith('C')for r in row]
assert len(cache)==80 and m.rank([c['row']for c in cache.values()])==80
assert m.rank(old_D)==80 and m.rank(old_D+[c['row']for c in cache.values()])==80
# Explicit independent corrective preloads for the two shared-axis couriers.
assert m.xor(cache[n]['row']for n in corr[(0,0)])^(1<<4)==K[0]^1
assert m.xor(cache[n]['row']for n in corr[(0,1)])==K[1]^2
assert m.xor(cache[n]['row']for n in corr[(1,0)])^(1<<6)==K[2]^(1<<2)
ops=[];expected={}
for i in range(111):
 for a in range(2):
  n=f'R{i}_b{a}';ops += [['INIT',n,f'L{i}'],['ADD',f'X{i}_b{a}',n]];expected[n]=[f'L{i}',1<<(2*i+a)]
for n,c in cache.items():ops.append(['INIT',n,c['chart']]);expected[n]=[c['chart'],c['row']]
ops.append(['INIT','SHARED01','A3']);expected['SHARED01']=['A3',S01]
for c in sorted(held):ops += [['MOVE',original(c),'A3'],['ADD',original(c),'SHARED01']]
for g in cohorts:
 coords=[tuple(c)for c in g['coords']];S=g['sources'];start=ch(g['pattern']);slots={tuple(d['slot'])for d in g['descs']}
 if len(S)==1 and (S[0],0)in held:
  c=(S[0],1);d=next(d for d in g['descs']if tuple(d['slot'])==c);cur=f'L{c[0]}'
  for z in range(len(d['route'])):
   dest=ch(sum(1<<q for q in d['route'][z:]));
   if dest!=cur:ops.append(['MOVE',original(c),dest]);cur=dest
  ops += [['ADD',original(c),d['cache']],['MOVE',original(c),'Hub']];continue
 for c in coords:
  if start!=f'L{c[0]}':ops.append(['MOVE',original(c),start])
 for a,b in reversed(g['restore']):ops.append(['ADD',original(coords[a]),original(coords[b])])
 for c in coords:
  if c not in slots:ops.append(['MOVE',original(c),'Hub'])
 for d in g['descs']:
  c=tuple(d['slot']);cur=start
  for z in range(len(d['route'])):
   dest=ch(sum(1<<q for q in d['route'][z:]))
   if dest!=cur:ops.append(['MOVE',original(c),dest]);cur=dest
   if d['shared_full']and dest=='A3':ops.append(['ADD',original(c),'SHARED01'])
  ops += [['ADD',original(c),d['cache']],['MOVE',original(c),'Hub']]
 for a,b in g['restore']:ops.append(['ADD',original(coords[a]),original(coords[b])])
# Both original couriers receive the same shared row. This is an invertible
# rank-one update because the shared row contains both courier coordinates.
for c in sorted(held):
 d=next(d for g in cohorts for d in g['descs']if tuple(d['slot'])==c);ops += [['ADD','SHARED01',original(c)],['MOVE',original(c),cache[d['cache']]['chart']],['ADD',original(c),d['cache']],['MOVE',original(c),'Hub']]
a,b='X2_b0','X3_b0';ops += [['ADD',a,b],['ADD',b,a],['ADD',a,b]]
for i in range(111):
 if i not in [2,3]and S01>>(2*i)&1:ops += [['ADD',f'X{i}_b0',a],['ADD',f'X{i}_b0',b]]
source_end=len(ops)
feedback=[(0,0),(0,1),(1,0)];mandatory=[K[2*q+a]for q,a in feedback];Ccomp=[];Bspan=mandatory[:]
for row in K:
 if m.rank(Bspan+[row])>len(Bspan):Ccomp.append(row);Bspan.append(row)
assert len(Ccomp)==15
raw={(q,a):m.xor(c['row']for c in cache.values()if c['query']==q and c['bank']==a)for q in range(8)for a in range(2)}
N={qa:raw[qa]^(K[2*qa[0]+qa[1]]^(1<<(2*qa[0]+qa[1])))for qa in feedback}
extra=next(c['row']for c in cache.values()if m.rank(K+list(N.values())+[c['row']])>m.rank(K+list(N.values())))
free=[(q,a)for q in range(8)for a in range(2)if(q,a)not in feedback]+[('extra',j)for j in range(3)];assert len(free)==16
free_targets=dict(zip(free,Ccomp+[extra]));packets=[]
for q,a in feedback:
 y=f'Y{q}_b{a}';ym=f'YM{q}_b{a}';ops += [['INIT',ym,'zero'],['ADD',y,ym]];expected[ym]=['zero',1<<(222+2*q+a)]
 if(q,a)==(0,0):ops += [['MOVE',y,'L2'],['ADD','R2_b0',y]]
 if(q,a)==(1,0):ops += [['MOVE',y,'L3'],['ADD','R3_b0',y]]
 ops.append(['MOVE',y,f'F{q}']);ops += [['ADD',n,y]for n in corr[(q,a)]]
for q in range(8):
 for a in range(2):
  qa=(q,a);n=f'P{q}_b{a}';packets.append(n);target=N[qa]if qa in feedback else free_targets[qa];seed=K[2*q+a]if qa in feedback else target^raw[qa]
  ops.append(['INIT',n,'Hub']);ops += [['ADD',f'X{i}_b{b}',n]for i in range(111)for b in range(2)if seed>>(2*i+b)&1]
  cs=[z for z,c in cache.items()if c['query']==q and c['bank']==a]
  if cs or qa in feedback:
   ops.append(['MOVE',n,f'F{q}'])
   if qa in feedback:ops += [['ADD',n,f'Y{q}_b{a}'],['ADD',f'Y{q}_b{a}',n]]
   ops += [['ADD',z,n]for z in cs]
  ops.append(['MOVE',n,'zero'])
  if qa in feedback:ops.append(['ADD',f'YM{q}_b{a}',n])
  expected[n]=['zero',target]
for j in range(3):
 n=f'E{j}';packets.append(n);target=free_targets[('extra',j)];ops.append(['INIT',n,'Hub']);ops += [['ADD',f'X{i}_b{a}',n]for i in range(111)for a in range(2)if target>>(2*i+a)&1];ops.append(['MOVE',n,'zero']);expected[n]=['zero',target]
G=[v[1]for n,v in expected.items()if n in packets]+mandatory
result={'schema':'facet-collector-canonical-feedback-v1','predecessor_sha256':hashlib.sha256(source_bytes).hexdigest(),'native_sha256':hashlib.sha256(native_bytes).hexdigest(),'physical_copies':2,'scalar_word_grammar':True,'single_wide_record_claim':False,'charts':base['charts'],'cohorts':cohorts,'cache_spec':cache,'shared_row_hex':hex(S01),'correction_caches':{f'{q}_{a}':v for(q,a),v in corr.items()},'source_end':source_end,'operations':ops,'expected':expected,'handoff':len(ops),'closed':False,'feedback_roles':[list(z)for z in feedback],'packets':packets,'canonical_rows_hex':[hex(x)for x in K],'W_rows_lanes_hex':base['W_rows_lanes_hex'],'kernel_rows_hex':[hex(x)for x in mandatory],'canonical_seed_rows_hex':[hex(x)for x in Ccomp],'new_complete_kappa':False,'D_rank':m.rank([c['row']for c in cache.values()]),'G_rank':m.rank(G),'G_canonical_intersection':m.rank(G)+18-m.rank(G+K),'G_noncanonical_rank':m.rank(G+K)-18}
closed=copy.deepcopy(result);closed['closed']=True;closed['operations'] += [['CLEAR',n]for n in sorted(expected)]+[['MOVE',f'Y{i}_b{a}',f'F{i}']for i in range(111)for a in range(2)if(i,a)not in feedback]
out=args.out;out.mkdir(parents=True,exist_ok=True);(out/'WORD.json').write_text(json.dumps(result,indent=2)+'\n');(out/'CLOSED-WORD.json').write_text(json.dumps(closed,indent=2)+'\n');print({k:result[k]for k in ['D_rank','G_rank','G_canonical_intersection','G_noncanonical_rank']});print('owners',len(expected),'operations',len(closed['operations']))
