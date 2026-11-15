#!/usr/bin/env python3
"""Independent all-column/rational audit; imports no author implementation."""
import argparse,json,hashlib,copy
from pathlib import Path
from collections import Counter
from functools import lru_cache
import sympy as sp

def basis(rows):
 B={}
 for j,x in enumerate(rows):
  tag=1<<j
  while x:
   p=x.bit_length()-1
   if p in B:x^=B[p][0];tag^=B[p][1]
   else:B[p]=(x,tag);break
 return B
def solve(B,x):
 tag=0
 while x:
  p=x.bit_length()-1
  if p not in B:return None
  x^=B[p][0];tag^=B[p][1]
 return tag
def rank(rows):return len(basis(rows))
def xor(rows):
 x=0
 for r in rows:x^=r
 return x
def independent(rows):
 b=[]
 for r in rows:
  if rank(b+[r])>len(b):b.append(r)
 return b
def geometry(c):
 M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);v=M.rowspace()if c['kind']=='span'else M.nullspace();return tuple(tuple(z)for z in v)

def replay(w,R):
 C={n:geometry(c)for n,c in w['charts'].items()};dim={n:len(v)for n,v in C.items()}
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(C[a]+C[b]).rank()if C[a]+C[b]else 0)==dim[b]
 for i,r in enumerate(R):
  assert C[f'L{i}']==geometry({'kind':'span','rows':[r]});assert C[f'F{i}']==geometry({'kind':'ann','rows':[r]})
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 owned=set();born=set();counts=Counter();moves=Counter();hist=[];events=[];dirty=0;paths={f'P{i}':[8]for i in range(8)};helper_paths={};cocharts={(0,1):{},(2,3):{}};kernel=None;reads={};ground={}
 def restored():assert all(vals[f'X{i}']==1<<i and loc[f'X{i}']=='Hub'for i in range(111)),'original source not restored'
 for step,op in enumerate(w['operations']):
  k,n,*v=op;counts[k]+=1;changed=None
  if k=='INIT':
   assert n not in vals and n not in born;owned.add(n);born.add(n);vals[n]=0;loc[n]=v[0]
   if n in paths:restored();assert v[0]=='Hub'
   if n.startswith('AXIS_DUP'):helper_paths[n]=[dim[v[0]]];assert v[0]=='Hub'
  elif k=='ADD':
   t=v[0];assert n in vals and t in vals and n!=t
   assert sub(loc[n],loc[t])and sub(loc[t],loc[n]),('noncochart',step,op)
   if t in paths and loc[t]=='Hub':restored();assert n.startswith('X')
   if t.startswith('AXIS_DUP'):
    i=int(t.removeprefix('AXIS_DUP'));assert n==f'X{i}'and vals[n]==1<<i and loc[n]=='Hub'
   if n=='P0'and t=='Y0':kernel=vals[n];assert loc.get('P1')=='A15','P1 absent at P0 feedback'
   before=vals[t];vals[t]^=vals[n];changed=t
   if n.startswith('C')and t in paths:
    assert vals[t]^before==w['expected'][n][1];reads[n]=vals[n]
  elif k=='MOVE':
   dest=v[0];assert n in vals and dim[dest]!=dim[loc[n]]
   assert sub(dest,loc[n])if n in owned else sub(loc[n],dest),('direction',step,op)
   if n in owned:assert n in paths or n in helper_paths,'unpriced extra owned route'
   moves[abs(dim[dest]-dim[loc[n]])]+=1;loc[n]=dest;changed=n
   if n in paths:
    paths[n].append(dim[dest])
    if not dim[dest]:assert n not in ground;ground[n]=vals[n]
   if n in helper_paths:helper_paths[n].append(dim[dest])
  elif k=='CLEAR':
   assert n in owned;dirty+=bool(vals[n]);owned.remove(n);del vals[n],loc[n]
  else:raise AssertionError(k)
  if changed in paths and loc[changed]!='Hub':hist.append(vals[changed]);events.append([step,changed,loc[changed],hex(vals[changed])])
  for pair in cocharts:
   a,b=(f'P{i}'for i in pair)
   if a in loc and b in loc and loc[a]==loc[b]and 0<dim[loc[a]]<8:cocharts[pair].setdefault(loc[a],step)
  if step+1==w['handoff']:
   hand={n:[loc[n],vals[n]]for n in sorted(owned)};assert hand==w['expected'],'actual handoff mismatch'
 restored();assert len(born)==234 and len(owned)==(0 if w['closed']else 234)
 for i in range(111):
  assert vals[f'Y{i}']==(1<<(111+i))^((1<<i)if i==0 else 0),('Y value',i)
  assert loc[f'Y{i}']==(f'F{i}'if w['closed']or i==0 else'zero'),('Y location',i)
 assert paths=={f'P{i}':list(range(8,-1,-1))for i in range(8)}
 assert helper_paths=={'AXIS_DUP0':[8,7],'AXIS_DUP2':[8,7]}
 assert set(cocharts[(0,1)])=={'A3','A7','A15','A31','A63','L7'},'first shared-tail chronology'
 assert set(cocharts[(2,3)])=={'A12','A28','A60','A124','A252','L1'},'second shared-tail chronology'
 K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];h=K[0]^K[4];M=(1<<111)-1;W=[r&(h if h>>i&1 else M^h)for i,r in enumerate(K)];assert[hex(x)for x in W]==w['W_rows_hex'];D=list(reads.values());assert len(reads)==112 and rank(D)==44 and rank(D)+15-rank(D+W)==10
 HB=basis(hist);ww=[solve(HB,x)for x in W];dw=[solve(HB,x)for x in D];assert all(x is not None for x in ww+dw)
 T=[hand[f'P{i}'][1]for i in range(8)];assert rank(T)==6 and rank(T)+15-rank(T+W)==5;assert not T[6]and not T[7];assert kernel==int(w['kernel_x_hex'],16);assert rank(T+[kernel])==7
 assert rank(hist)==50 and rank([x>>111 for x in hist])==1
 if w['closed']:
  assert counts==Counter({'INIT':234,'ADD':845,'MOVE':479,'CLEAR':234})and dirty==232
  assert dict(moves)=={1:149,2:26,3:127,4:67,7:110}
 visited={ev[2]for ev in events if 0<dim[ev[2]]<8};coverage={i:[c for c in visited if sub(c,f'F{i}')]for i in range(111)};assert all(coverage.values())
 result={'status':'PASS_INDEPENDENT_PAIRED_FLAG_REPLAY','counts':dict(counts),'dirty_clears':dirty,'movement_profile':dict(sorted(moves.items())),'rank_length':sum(k*v for k,v in moves.items()),'principal_paths':paths,'helper_paths':helper_paths,'simultaneous_shared_charts':{str(p):v for p,v in cocharts.items()},'D_rank':rank(D),'D_W_intersection':rank(D)+15-rank(D+W),'history_rank':rank(hist),'history_y_rank':rank([x>>111 for x in hist]),'terminal_rank':rank(T),'normalized_rank_with_kernel':rank(T+[kernel]),'all111_chart_coverage':True}
 evidence={'history_events':events,'all111_W_witnesses':[{'row_hex':hex(r),'coefficients_hex':hex(c)}for r,c in zip(W,ww)],'all112_read_witnesses':[{'row_hex':hex(r),'coefficients_hex':hex(c)}for r,c in zip(D,dw)],'coverage':coverage}
 return result,evidence

def capacity(w,R):
 M=(1<<111)-1;K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];h=K[0]^K[4];W=[r&(h if h>>i&1 else M^h)for i,r in enumerate(K)];W0=independent([r&(M^h)for r in W]);W1=independent([r&h for r in W]);assert len(W0)==7 and len(W1)==8
 assert[hex(x)for x in W0]==w['reprogramming']['h0_W_basis_hex'];U0=[xor(W0[j]for j in range(7)if c>>j&1)for c in range(128)if(c&88).bit_count()%2==0];assert rank(U0)==6
 data=[];total=0
 assert sorted(j for g in w['cohorts']for j in g['sources'])==list(range(111))
 for g in w['cohorts']:
  S=g['sources'];assert all((h>>i&1)==g['h_class']for i in S);mask=sum(1<<j for j in S);forms=[int(x,16)for x in g['run_rows_hex']];r=rank(forms);total+=r;assert r==min(len(g['runs']),len(S));assert all(x&~mask==0 for x in forms)
  if not g['h_class']:assert rank(forms+[u&mask for u in U0])==r
  for t,run in enumerate(g['runs']):
   for q in run:
    name=f'C{q}_{g["query_depths"][str(q)]}_{g["h_class"]}_g{S[0]}';assert w['expected'][name][1]==forms[t]
  for q,depth in g['query_depths'].items():
   q=int(q);flag=w['flags'][q];actual=0
   for z in flag:
    if not g['pattern']>>z&1:break
    actual+=1
   assert actual==depth and g['query_sets'][str(q)]==sum(1<<z for z in flag[:depth])
  if S[0]in[30,81]:
   assert r==2 and rank([u&mask for u in W0])==3
   A=independent([sum(1<<j for j,u in enumerate(W0)if u>>i&1)for i in S]);span={xor(A[j]for j in range(len(A))if c>>j&1)for c in range(1<<len(A))};assert 88 in span
  data.append({'cohort':S[0],'class':g['h_class'],'independent_capacity':r,'run_count':len(g['runs']),'full_W_projection_rank':rank([u&mask for u in(W0 if not g['h_class']else W1)])})
 assert total==44
 D=[v[1]for n,v in w['expected'].items()if n.startswith('C')];assert rank(D)+7-rank(D+W0)==6 and rank(D)+8-rank(D+W1)==4
 masks=[sum(1<<j for j in g['sources'])for g in w['cohorts']if g['sources'][0]in[52,22]];assert len(masks)==2;assert all(next(g for g in w['cohorts']if sum(1<<j for j in g['sources'])==sm)['runs'].__len__()==1 for sm in masks);assert rank([u&(masks[0]|masks[1])for u in W1])==6
 groups={}
 for n,(c,r)in w['expected'].items():
  if n.startswith('C'):groups[n.rsplit('_g',1)[0]]=groups.get(n.rsplit('_g',1)[0],0)^r
 ag=list(groups.values());assert rank(ag)==36 and rank(ag)+15-rank(ag+W)==5
 return{'status':'PASS_INDEPENDENT_ALL_WIDTH_CAPACITY_10V','independent_source_rank':44,'class0_bound_and_attainment':6,'class1_bound_and_attainment':4,'class1_joint_projection_rank':6,'cohorts':data,'aggregate_shortcut_rank':36,'aggregate_shortcut_W_intersection':5}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');args=p.parse_args()
 native=args.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';nb=native.read_bytes();assert hashlib.sha256(nb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(nb)['native_roots'];args.out.mkdir(parents=True,exist_ok=True)
 for name in ['WORD','CLOSED-WORD']:
  path=args.author/'output'/f'{name}.json';raw=path.read_bytes();w=json.loads(raw)
  if name=='WORD':assert hashlib.sha256(raw).hexdigest()=='3aaabaf76bbfabccce40fe2dc56c2dfaf7242061de698d19098d64ef8821a8e5'
  r,e=replay(w,R);r['word_sha256']=hashlib.sha256(raw).hexdigest();(args.out/f'{name}-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(args.out/f'{name}-HISTORY.json').write_text(json.dumps(e,indent=2)+'\n');print(name,r['counts'],flush=True)
 cap=capacity(w,R);(args.out/'CAPACITY.json').write_text(json.dumps(cap,indent=2)+'\n');print(cap['status'],flush=True)
 labels=[('wrong_axis_duplicate_source',lambda o:o==['ADD','X0','AXIS_DUP0'],'change'),('omit_axis_duplicate_move',lambda o:o==['MOVE','AXIS_DUP2','F3'],'delete'),('omit_hub_restore',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),'delete'),('omit_y_capture',lambda o:o==['ADD','Y0','YM0'],'delete'),('omit_coupled_feedback',lambda o:o==['ADD','Y0','P0'],'delete'),('omit_last_zero_packet_route',lambda o:o==['MOVE','P7','zero'],'delete'),('omit_private_cache_read',lambda o:o[0]=='ADD'and o[1].startswith('C')and o[2]=='P1','delete')]
 controls=[]
 for name,pred,action in labels:
  bad=copy.deepcopy(w);indices=[i for i,o in enumerate(bad['operations'])if pred(o)];idx=indices[-1]if name=='omit_hub_restore'else indices[0]
  if action=='change':bad['operations'][idx][1]='X2'
  else:
   bad['operations'].pop(idx)
   if idx<bad['handoff']:bad['handoff']-=1
  try:replay(bad,R)
  except AssertionError as exc:controls.append({'name':name,'rejected':True,'reason':str(exc)})
  else:raise AssertionError(('mutant survived',name))
 # Endpoint-preserving chronological countercontrol: defer P1's complete
 # non-Hub path until P0 has finished, preserving the source and every read.
 bad=copy.deepcopy(w);defer=[];keep=[];insert=None
 for o in bad['operations']:
  if (o[0]=='MOVE'and o[1]=='P1')or(o[0]=='ADD'and o[1].startswith('C')and o[2]=='P1'):defer.append(o)
  else:
   keep.append(o)
   if o==['ADD','YM0','P0']:insert=len(keep)
 assert insert is not None;bad['operations']=keep[:insert]+defer+keep[insert:]
 try:replay(bad,R)
 except AssertionError as exc:controls.append({'name':'serialize_shared_pair_without_common_chronology','rejected':True,'reason':str(exc)})
 else:raise AssertionError('serialized common-tail mutant survived')
 (args.out/'NEGATIVE-CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n');print('independent mutants',len(controls),flush=True)
