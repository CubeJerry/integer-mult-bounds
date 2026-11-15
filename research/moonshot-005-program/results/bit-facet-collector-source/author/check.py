#!/usr/bin/env python3
import json,hashlib,copy,argparse,types
import sympy as sp
from pathlib import Path
from collections import Counter
from decimal import Decimal,getcontext
from functools import lru_cache
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
def basis(rows):
 B={}
 for j,r in enumerate(rows):
  tag=1<<j
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p][0];tag^=B[p][1]
   else:B[p]=(r,tag);break
 return B
def solve(B,r):
 tag=0
 while r:
  p=r.bit_length()-1
  if p not in B:return None
  r^=B[p][0];tag^=B[p][1]
 return tag
def chart(c):
 M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);rows=M.rowspace()if c['kind']=='span'else M.nullspace()
 return tuple(tuple(v)for v in rows)
m=types.SimpleNamespace(basis=basis,solve=solve,chart=chart,sp=sp)
R=None

def replay(w):
 C={n:m.chart(c)for n,c in w['charts'].items()};dim={n:len(c)for n,c in C.items()}
 for i,r in enumerate(R):
  assert C[f'L{i}']==chart({'kind':'span','rows':[r]})
  assert C[f'F{i}']==chart({'kind':'ann','rows':[r]})
 @lru_cache(None)
 def sub(a,b):return(m.sp.Matrix(C[a]+C[b]).rank()if C[a]+C[b]else 0)==dim[b]
 X={f'X{i}_b{a}':(i,a)for i in range(111)for a in range(2)};Y={f'Y{i}_b{a}':(i,a)for i in range(111)for a in range(2)}
 val={n:1<<(2*i+a)for n,(i,a)in X.items()}|{n:1<<(222+2*i+a)for n,(i,a)in Y.items()};loc={n:f'L{i}'for n,(i,a)in X.items()}|{n:'zero'for n in Y};owned=set();born=set();counts=Counter();moves=Counter();hist=[];events=[];dirty=0;ground={};packets=set(w['packets']);feedback={tuple(z)for z in w['feedback_roles']};kernels=[]
 def restored():assert all(val[n]==1<<(2*i+a)and loc[n]=='Hub'for n,(i,a)in X.items()),'original restoration'
 for step,op in enumerate(w['operations']):
  k,n,*v=op;counts[k]+=1;changed=None
  if k=='INIT':
   assert n not in val and n not in born;val[n]=0;loc[n]=v[0];owned.add(n);born.add(n)
   if n in packets:restored();assert loc[n]=='Hub'
  elif k=='ADD':
   t=v[0];assert n in val and t in val and n!=t
   assert sub(loc[n],loc[t])and sub(loc[t],loc[n]),('cochart',step,op,loc[n],loc[t])
   if n in packets and t in Y:kernels.append(val[n])
   val[t]^=val[n];changed=t
  elif k=='MOVE':
   dest=v[0];assert n in val and dim[dest]!=dim[loc[n]]
   assert n not in owned or n in packets,('moving owned',n)
   assert sub(dest,loc[n])if n in owned else sub(loc[n],dest),('direction',op)
   moves[abs(dim[dest]-dim[loc[n]])]+=1;loc[n]=dest;changed=n
   if n in packets and dim[dest]==0:assert n not in ground;ground[n]=val[n]
  elif k=='CLEAR':
   assert n in owned;dirty+=bool(val[n]);owned.remove(n);del val[n],loc[n]
  else:raise AssertionError(k)
  if changed in packets and loc[changed]!='Hub':hist.append(val[changed]);events.append([step,changed,loc[changed],hex(val[changed])])
  if step+1==w['source_end']:restored()
  if step+1==w['handoff']:
   hand={n:[loc[n],val[n]]for n in sorted(owned)};assert hand==w['expected'],'handoff'
 restored();assert len(ground)==19
 assert kernels==[int(x,16)for x in w['kernel_rows_hex']]
 for n,(i,a)in Y.items():
  assert val[n]==(1<<(222+2*i+a))^((1<<(2*i+a))if(i,a)in feedback else 0),('Y endpoint',n)
  assert loc[n]==(f'F{i}'if w['closed']or(i,a)in feedback else'zero')
 D=[v[1]for n,v in hand.items()if n.startswith('FC')];K=[int(x,16)for x in w['canonical_rows_hex']];W=[int(x,16)for r in w['W_rows_lanes_hex']for x in r];T=[hand[n][1]for n in w['packets']];G=T+kernels;HB=m.basis(hist)
 assert len(m.basis(D))==80 and len(m.basis(K))==18
 assert all(m.solve(HB,r)is not None for r in D+K)
 rank=lambda rows:len(m.basis(rows))
 getcontext().prec=60;moment=sum(Decimal(k)**(Decimal(199)/200)*v for k,v in moves.items());allow=Decimal('1621.750880211152355246246150366995')
 result={'status':'PASS_EXPLORATORY_FACET_COLLECTOR','counts':dict(counts),'dirty_clears':dirty,'movement_profile':dict(sorted(moves.items())),'physical_moment':str(moment),'per_native_copy_moment':str(moment/2),'limiting_room':str(allow-moment/2),'D_rank':rank(D),'D_W_intersection':rank(D)+30-rank(D+W),'history_rank':rank(hist),'history_y_rank':rank([r>>222 for r in hist]),'history_W_intersection':rank(hist)+30-rank(hist+W),'history_C_intersection':rank(hist)+18-rank(hist+K),'terminal_rank':rank(T),'G_rank':rank(G),'G_C_intersection':rank(G)+18-rank(G+K),'G_noncanonical_rank':rank(G+K)-18,'new_complete_kappa':False}
 if w['closed']:
  assert counts==Counter({'INIT':325,'ADD':2095,'MOVE':871,'CLEAR':325}) and dirty==325
  assert dict(moves)=={1:224,2:24,3:238,4:142,5:2,6:2,7:228,8:11}
 return result,{'events':events,'canonical_witnesses':[{'row_hex':hex(r),'history_coefficients_hex':hex(m.solve(HB,r))}for r in K],'cache_witnesses':[{'row_hex':hex(r),'history_coefficients_hex':hex(m.solve(HB,r))}for r in D]}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word-dir',type=Path,default=Path(__file__).parent/'output');p.add_argument('--out',type=Path,default=Path(__file__).parent/'verification');a=p.parse_args()
 rb=(a.repo/ROOT).read_bytes();assert hashlib.sha256(rb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(rb)['native_roots'];out=a.out;out.mkdir(parents=True,exist_ok=True)
 for name in ['WORD','CLOSED-WORD']:
  w=json.loads((a.word_dir/f'{name}.json').read_text());r,e=replay(w);print(name,r,flush=True);(out/f'{name}-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/f'{name}-HISTORY.json').write_text(json.dumps(e,indent=2)+'\n')
 closed=json.loads((a.word_dir/'CLOSED-WORD.json').read_text());mutants=[]
 selectors=[('omit_shared_donation',lambda op:op==['ADD','X4_b0','SHARED01']),('omit_first_shared_courier_update',lambda op:op==['ADD','SHARED01','X2_b0']),('omit_hub_inverse_swap',lambda op:op==['ADD','X2_b0','X3_b0']),('omit_first_receiver_preload',lambda op:op==['ADD','R2_b0','Y0_b0']),('omit_third_receiver_preload',lambda op:op==['ADD','R3_b0','Y1_b0']),('omit_third_feedback',lambda op:op==['ADD','Y1_b0','P1_b0']),('omit_third_unmask',lambda op:op==['ADD','YM1_b0','P1_b0']),('omit_extra_principal_move',lambda op:op==['MOVE','E2','zero'])]
 for label,predicate in selectors:
  bad=copy.deepcopy(closed);idx=next(i for i,op in enumerate(bad['operations'])if predicate(op));bad['operations'].pop(idx)
  if idx<bad['source_end']:bad['source_end']-=1
  if idx<bad['handoff']:bad['handoff']-=1
  try:replay(bad)
  except AssertionError as exc:mutants.append({'name':label,'rejected':True,'reason':str(exc)})
  else:raise AssertionError(('surviving mutant',label))
 (out/'NEGATIVE-CONTROLS.json').write_text(json.dumps(mutants,indent=2)+'\n');print('negative controls',len(mutants))
