#!/usr/bin/env python3
"""Independent complete binary source replay of the paid pair-mode repair."""
import argparse,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc',
 'parent':'6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'interpreter':'d5122fa1eed5463a1bd8c3e21cf39125d94909ab80332c74b143dd40d46d79fa'}
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser();defaults={'native':HERE.parent/'native.json',
 'word':HERE.parents[1]/'A/four-arrival-frame-repair/output/WORD.json',
 'parent':HERE.parents[1]/'A/full-half-reservoir/WORD.json',
 'arithmetic':HERE.parent/'four-plane-review/check.py','interpreter':HERE.parent/'owned-upward-half-rebase/build.py'}
 for k,v in defaults.items():p.add_argument('--'+k,type=Path,default=v)
 p.add_argument('--out',type=Path,default=HERE/'output');a=p.parse_args()
 for k,pin in PINS.items():assert hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,k
 g=load(a.arithmetic,'frame_geometry');engine=load(a.interpreter,'frame_replay')
 roots=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());parent=json.loads(a.parent.read_bytes())
 charts={n:g.chart(z) for n,z in w['charts'].items()}
 for i,r in enumerate(roots):
  assert charts[f'L{i}']==g.basis((tuple(r),)) and charts[f'F{i}']==g.kernel((tuple(r),))
 N=[sum(1<<j for j,s in enumerate(roots) if sum(x*y for x,y in zip(r,s))==0) for r in roots]
 base=[1<<i if i<8 else N[i]&255 for i in range(111)];expected=base.copy()
 A=[14,17,19,20];B=[96,101,99,102];targets=A+B
 for i in range(4):
  expected[A[i]]^=sum(1<<A[k] for k in range(4) if k!=i)^(1<<B[(i+1)%4])^(1<<B[(i+2)%4])
  expected[B[i]]^=sum(1<<B[k] for k in range(4) if k!=i)^(1<<A[i])^(1<<A[(i-1)%4])
 assert w['Y_correction_rows_hex']==list(map(hex,expected))
 stats,V,at=engine.replay(w,charts,expected,g)
 pc={n:g.chart(z) for n,z in parent['charts'].items()};ps,pv,pa=engine.replay(parent,pc,base,g)
 assert w['carrier_interface_before_operation']==1985 and len(V)==410
 assert stats['counts']=={'INIT':188,'ADD':1400,'MOVE':508,'CLEAR':188}
 assert stats['movement_profile']=={1:179,2:111,3:4,4:103,7:111}
 assert stats['owned_upward_profile']=={3:4} and stats['owned_downward_profile']=={1:36}
 for n in pv:
  if n in {f'Y{i}' for i in targets}:
   i=int(n[1:]);assert V[n]==(1<<(111+i))^expected[i]
   assert len(charts[at[n]])==6 and g.contained(charts[at[n]],charts[f'F{i}'])
  else:assert V[n]==pv[n] and charts[at[n]]==pc[pa[n]],n
 new=set(V)-set(pv);assert len(new)==4
 rows=Counter(V[n] for n in new);assert rows=={(1<<96)^(1<<99):2,(1<<101)^(1<<102):2}
 for n in new:
  assert len(charts[at[n]])==5 and V[n]>>111==0
  for j in range(111):
   if V[n]>>j&1:assert g.contained(charts[f'L{j}'],charts[at[n]])
 assert sum((expected[i]^base[i]).bit_count() for i in range(111))==40
 assert all(not(expected[i]&~N[i]) for i in range(8,111))
 assert sum(at[f'Y{i}']=='zero' for i in range(111))==103
 # All new owners are actual sources: remove each arrival or delivery.
 selected=[]
 for ix,op in enumerate(w['operations']):
  if op[1] in new and (op[0]=='MOVE' or op[0]=='ADD' and op[2].startswith('Y')):selected.append(ix)
 assert len(selected)==8
 rejected=[]
 for ix in selected:
  bad=json.loads(json.dumps(w));del bad['operations'][ix];bad['carrier_interface_before_operation']-=int(ix<1985)
  try:
   _,bv,bp=engine.replay(bad,charts,expected,g)
   assert (bv,bp)==(V,at)
  except (ValueError,AssertionError):rejected.append(ix)
  else:raise AssertionError('omitted source arrival/delivery accepted')
 Q=g.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 cap=tuple(x/6 for x in g.moment(gate));room=(cap[0]-Q[1],cap[1]-Q[0])
 out={'status':'PASS_INDEPENDENT_LITERAL_PAIR_MODE_REPAIR','pins':PINS,'cut':1985,'fields':410,
 'all_input_columns':222,'stats':stats,'completed_diagonal_values':8,'new_native_foreign_coefficients':40,
 'new_owner_names':sorted(new),'owner_pair_rows':{hex(k):v for k,v in rows.items()},
 'omitted_paid_arrival_or_delivery_controls':rejected,'moment_interval':list(map(str,Q)),
 'necessary_limiting_room_interval':list(map(str,room)),
 'scope':'Actual paid pair2-to-rank5 owned ascents before round3; no added descent, no new complete diagonal output or supplier claim.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
 (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':at[n],'rank':len(charts[at[n]]),'row_hex':hex(v)} for n,v in sorted(V.items())],indent=2)+'\n')
 print(json.dumps({'status':out['status'],'columns':222,'fields':410,'controls':len(rejected)}))
if __name__=='__main__':main()
