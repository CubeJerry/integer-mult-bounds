#!/usr/bin/env python3
"""Independent exact replay. No imports from source constructor/checker."""
import argparse,collections,copy,hashlib,json
from functools import lru_cache
from pathlib import Path
from fractions import Fraction
import sympy as sp

SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
MASK=(1<<222)-1

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def basis(rows):
 b={}
 for a in rows:
  x=a
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 return b

def rank(rows):return len(basis(rows))
def contains(rows,x):
 b=basis(rows)
 while x:
  j=x.bit_length()-1
  if j not in b:return False
  x^=b[j]
 return True

def dimcap(a,b):return rank(a)+rank(b)-rank(a+b)
def witnesses(rows,targets):
 b={}
 for i,a in enumerate(rows):
  x=a;c=1<<i
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j][0];c^=b[j][1]
   else:b[j]=(x,c);break
 out=[]
 for a in targets:
  x=a;c=0
  while x:
   j=x.bit_length()-1
   assert j in b,('target-not-spanned',hex(a))
   x^=b[j][0];c^=b[j][1]
  assert a==xor(rows[i] for i in range(len(rows)) if c>>i&1)
  out.append(hex(c))
 return out

def xor(xs):
 y=0
 for x in xs:y^=x
 return y

class Geometry:
 def __init__(self,charts):
  self.B={}
  for n,c in charts.items():
   r=c['rows']
   if c['kind']=='ann': cols=sp.Matrix(r).nullspace() if r else [sp.eye(8)[:,j] for j in range(8)]
   elif c['kind']=='span':cols=sp.Matrix(r).T.columnspace() if r else []
   else:raise AssertionError(c)
   self.B[n]=sp.Matrix.hstack(*cols) if cols else sp.zeros(8,0)
 @lru_cache(None)
 def sub(self,a,b):
  A,B=self.B[a],self.B[b]
  return B.row_join(A).rank()==B.cols
 @lru_cache(None)
 def same(self,a,b):return self.sub(a,b) and self.sub(b,a)
 def dim(self,a):return self.B[a].cols


@lru_cache(None)
def power_interval(r):
 S=1<<160;z=pow(r,199)*pow(S,200);lo=0;hi=r*S+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if pow(mid,200)<=z:lo=mid
  else:hi=mid
 assert pow(lo,200)<=z<pow(hi,200)
 return Fraction(lo,S),Fraction(hi,S)
def lin(d):
 lo=hi=Fraction(0)
 for r,c in d.items():
  a,b=power_interval(r)
  if c>=0:lo+=c*a;hi+=c*b
  else:lo+=c*b;hi+=c*a
 return lo,hi
def add(*xs):return tuple(sum(x[i] for x in xs) for i in (0,1))
def scale(c,a):return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])
def dec(q):
 from decimal import Decimal,localcontext
 with localcontext() as c:c.prec=65;return str(Decimal(q.numerator)/Decimal(q.denominator))
def enc(a):return {'lower':str(a[0]),'upper':str(a[1]),'decimal_lower':dec(a[0]),'decimal_upper':dec(a[1])}
def prices(profile):
 N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10});H=lin({2:1,4:25,6:1,8:410})
 P2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}))
 T2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}))
 diff=add(T2,scale(-1,P2));L=add(N,scale(-1,H),scale(Fraction(1,36),diff));Q=lin(profile);room=add(L,scale(-1,Q));m2=add(scale(18,room),scale(Fraction(1,2),diff))
 assert room[0]>0 and m2[0]>0
 return {k:enc(v) for k,v in [('Q',Q),('limiting_cap',L),('room',room),('m2_margin',m2)]}


def embed(x,b):
 return sum(1<<(2*i+b) for i in range(111) if x>>i&1)

def replay(word,roots,geom,previous_D,strict=True):
 loc={f'X{i}_b{b}':f'L{i}' for i in range(111) for b in range(2)};loc.update({f'Y{i}_b{b}':'zero' for i in range(111) for b in range(2)})
 val={f'X{i}_b{b}':1<<(2*i+b) for i in range(111) for b in range(2)};val.update({f'Y{i}_b{b}':1<<(222+2*i+b) for i in range(111) for b in range(2)})
 original=set(loc);owned=set();birth=set();counts=collections.Counter();profile=collections.Counter();history=[];seen=set();kernels={};dirty=0;handoff=None;terminal={};source_checked=False;couriers=[];feedbacks=[]
 packets=word['packets'];done={tuple(x) for x in word['feedback_roles']};assert len(packets)==19 and len(set(packets))==19
 K0=[(1<<i)^sum(1<<j for j in range(111) if i!=j and sum(a*b for a,b in zip(roots[i],roots[j]))==0) for i in range(111)]
 C=[embed(x,b) for x in K0 for b in range(2)];h=K0[0]^K0[4];W0=[K0[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)];W=[embed(x,b) for x in W0 for b in range(2)]
 assert [hex(x) for x in C]==word['canonical_rows_hex'];assert [[hex(embed(x,b)) for b in range(2)] for x in W0]==word['W_rows_lanes_hex']
 for n,op in enumerate(word['operations']):
  if n==word['source_end']:
   assert all(loc[f'X{i}_b{b}']=='Hub' and val[f'X{i}_b{b}']==1<<(2*i+b) for i in range(111) for b in range(2)),('source-end',n);source_checked=True
  if n==word['handoff']:handoff={k:[loc[k],val[k]] for k in sorted(owned)}
  t=op[0];counts[t]+=1
  if t=='INIT':
   _,a,c=op;assert a not in val and a not in birth and c in geom.B,('bad-init',n,op)
   if a in packets:assert source_checked and all(loc[f'X{i}_b{b}']=='Hub' and val[f'X{i}_b{b}']==1<<(2*i+b) for i in range(111) for b in range(2)),('source-not-restored-before-seed',n)
   loc[a]=c;val[a]=0;owned.add(a);birth.add(a)
  elif t=='ADD':
   _,a,b=op;assert a in val and b in val and a!=b,('invalid-add',n,op);assert geom.same(loc[a],loc[b]),('noncochart',n,op,loc[a],loc[b])
   if a=='SHARED01' and b in ['X2_b0','X3_b0']:couriers.append({'step':n,'target':b,'chart':loc[b],'before_hex':hex(val[b]),'shared_hex':hex(val[a]),'after_hex':hex(val[b]^val[a])})
   for i,c in done:
    if a==f'P{i}_b{c}' and b==f'Y{i}_b{c}':
     assert val[a]==C[2*i+c] and val[b]==(1<<(222+2*i+c))^C[2*i+c]^(1<<(2*i+c)),('canonical-feedback-boundary',n,i,c)
     assert geom.same(loc[a],f'F{i}');feedbacks.append({'role':[i,c],'step':n,'kernel_hex':hex(val[a]),'incoming_y_hex':hex(val[b])})
   val[b]^=val[a]
  elif t=='MOVE':
   _,a,c=op;assert a in val and c in geom.B,('bad-move',n,op);old=loc[a];assert geom.sub(old,c) if a in original else geom.sub(c,old),('wrong-direction',n,op,old)
   r=abs(geom.dim(c)-geom.dim(old));assert r>0,('zero-move',n,op);profile[r]+=1;loc[a]=c
   for i,b in done:
    if a==f'P{i}_b{b}' and c==f'F{i}':kernels[a]=val[a]&MASK
   if a in packets and c=='zero':terminal[a]=val[a]&MASK
  elif t=='CLEAR':
   _,a=op;assert a in owned and a in val,('bad-clear',n,op);dirty+=bool(val[a]);owned.remove(a);del val[a];del loc[a]
  else:raise AssertionError(('unadmitted-opcode',t))
  for a in packets:
   if a in val and geom.dim(loc[a])<8 and val[a] not in seen:seen.add(val[a]);history.append(val[a])
 if handoff is None:handoff={k:[loc[k],val[k]] for k in sorted(owned)}
 assert handoff==word['expected'];assert source_checked
 for i in range(111):
  for b in range(2):
   assert loc[f'X{i}_b{b}']=='Hub' and val[f'X{i}_b{b}']==1<<(2*i+b),('X-endpoint',i,b)
   assert val[f'Y{i}_b{b}']==(1<<(222+2*i+b))^((1<<(2*i+b)) if (i,b) in done else 0),('Y-value',i,b)
   assert geom.same(loc[f'Y{i}_b{b}'],f'F{i}' if (i,b) in done or word['closed'] else 'zero'),('Y-chart',i,b)
 assert len(owned)==(0 if word['closed'] else len(birth));assert len(birth)==325;assert set(terminal)==set(packets)
 D=[v for k,(c,v) in handoff.items() if k.startswith('FC')];assert len(D)==80 and rank(D)==80 and rank(D+previous_D)==80
 assert rank(C)==18 and rank(W)==30 and dimcap(D,W)==19
 K=[kernels[f'P{i}_b{b}'] for i,b in word['feedback_roles']];assert [hex(x) for x in K]==word['kernel_rows_hex'];assert rank(K)==3
 T=[handoff[n][1] for n in packets];assert all(x<=MASK for x in T+D);G=T+K
 assert rank(T)==19 and rank(G)==22 and dimcap(G,C)==18
 expected_shared=sum(1<<(2*j) for j in range(111) if roots[j][0]==roots[j][1]==0)
 assert handoff['SHARED01'][1]==expected_shared==int(word['shared_row_hex'],16)
 assert len(couriers)==2 and {x['target'] for x in couriers}=={'X2_b0','X3_b0'}
 for rec in couriers:
  i=int(rec['target'][1:].split('_')[0]);assert rec['chart']=='A3' and int(rec['before_hex'],16)==1<<(2*i) and int(rec['shared_hex'],16)==expected_shared
 assert len(feedbacks)==3
 # Fresh source-bound local quotient and visibility diagnostic.
 diagnostics=[];hist=collections.Counter();visfit=[]
 for i in range(111):
  L=sum(3<<(2*j) for j in range(111) if sum(a*b for a,b in zip(roots[i],roots[j]))==0);J=L|(3<<(2*i));forbidden=MASK^J
  assert rank([x&forbidden for x in C])==16
  ri=rank(G)-rank([x&forbidden for x in G])-2;hist[ri]+=1
  visible=[kernels[f'P{q}_b{a}'] for q,a in done if geom.sub(f'F{q}',f'F{i}')]
  H=T+visible;hm=MASK^L
  fits=[contains([x&hm for x in H],1<<(2*i+a)) for a in range(2)]
  assert all(contains([x&hm for x in G],1<<(2*i+a)) for a in range(2))
  if all(fits):visfit.append(i)
  diagnostics.append({'role':i,'local_quotient_dimension':ri,'visible_kernel_count':len(visible),'visible_bank_fits':fits})
 assert dict(hist)=={3:1,2:1,1:9,0:100};assert len(visfit)==28
 out={'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(r*c for r,c in profile.items()),'dirty_clears':dirty,'history_rank':rank(history),'history_y_rank':rank([x>>222 for x in history]),'history_C_intersection':dimcap(history,C),'history_W_intersection':dimcap(history,W),'D_rank':rank(D),'D_W_intersection':dimcap(D,W),'terminal_rank':rank(T),'normalized_rank':rank(G),'normalized_canonical_intersection':dimcap(G,C),'noncanonical_quotient':rank(G)-rank(C),'actual_completed':sorted(done),'couriers':couriers,'feedbacks':feedbacks,'local_quotient_histogram':dict(hist),'universal_fixed_code_chi_lower_bound':2*sum(r['local_quotient_dimension']<2 for r in diagnostics),'visible_fit_roles':visfit,'visibility_failures':111-len(visfit)}
 assert out['history_rank']==91 and out['history_y_rank']==3 and out['history_C_intersection']==18 and out['history_W_intersection']==25
 if strict and word['closed']:
  assert dict(counts)=={'INIT':325,'ADD':2095,'MOVE':871,'CLEAR':325} and dirty==325
  assert dict(profile)=={1:224,2:24,3:238,4:142,5:2,6:2,7:228,8:11}
 return out,{'rows_hex':[hex(x) for x in history],'C_rows_hex':[hex(x) for x in C],'C_history_witnesses_hex':witnesses(history,C),'D_rows_hex':[hex(x) for x in D],'D_history_witnesses_hex':witnesses(history,D),'normalized_code_rows_hex':[hex(x) for x in G],'C_from_normalized_witnesses_hex':witnesses(G,C),'diagnostics':diagnostics}

def invoice(profile):
 N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10});H=lin({2:1,4:25,6:1,8:410})
 P2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}));T2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}));diff=add(T2,scale(-1,P2));L=add(N,scale(-1,H),scale(Fraction(1,36),diff));wholeQ=lin(profile);Q=scale(Fraction(1,2),wholeQ);room=add(L,scale(-1,Q));assert room[0]>0
 # The retained affine formula is 18(m−1)*room + (T2−P2)/2, independent of m in the final term.
 margins={m:add(scale(18*(m-1),room),scale(Fraction(1,2),diff)) for m in [2,4,6]}
 assert margins[2][1]<0 and margins[4][1]<0 and margins[6][0]>0
 return {'whole_physical_Q':enc(wholeQ),'normalized_per_copy_Q':enc(Q),'normalized_limiting_room':enc(room),'normalized_even_m_margins':{str(m):enc(v) for m,v in margins.items()},'all_even_m_at_least_6_pass_by_positive_affine_slope':True}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);ap.add_argument('--predecessor',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 ns=a.repo/SOURCE;assert sha(ns)==SOURCE_SHA;assert sha(a.predecessor)=='aa9d17693c1f976625ee420e1367680e86cfec0195259d609f7eddc258eda01e';prev=json.loads(a.predecessor.read_text());pd=[v for n,(c,v) in prev['expected'].items() if n.startswith('C')]
 roots=json.loads(ns.read_text())['native_roots'];words={n:json.loads((a.package/'output'/f'{n}.json').read_text()) for n in ['WORD','CLOSED-WORD']};assert sha(a.package/'output/WORD.json')=='f20a1ff9d564382d52c6e5015638b6195408d7e99dc6c63d7af66f0a6b31d6bf';assert sha(a.package/'output/CLOSED-WORD.json')=='aee68612958ed5266f8435de499ae68d600ed3baee7c5e84c5fd4ba3ef6f4a46'
 g=Geometry(words['WORD']['charts']);res={'status':'PASS_INDEPENDENT_FACET_COLLECTOR_REVIEW','word_sha256':{n:sha(a.package/'output'/f'{n}.json') for n in words},'native_sha256':SOURCE_SHA}
 for n,w in words.items():
  res[n],hist=replay(w,roots,g,pd);(a.out/f'{n}-HISTORY.json').write_text(json.dumps(hist,indent=2)+'\n')
 res['invoice']=invoice({int(r):v for r,v in res['CLOSED-WORD']['profile'].items()})
 ctr=[]
 patterns=[('lost_shared_axis_donation',['ADD','X2_b0','SHARED01']),('lost_shared_nonsingleton_donation',['ADD','X52_b0','SHARED01']),('lost_second_courier_exchange',['ADD','SHARED01','X3_b0']),('lost_courier_inverse',['ADD','X95_b0','X3_b0']),('lost_first_point_preload',['ADD','R2_b0','Y0_b0']),('lost_second_point_preload',['ADD','R3_b0','Y1_b0']),('lost_third_feedback',['ADD','P1_b0','Y1_b0']),('lost_nineteenth_full_move',['MOVE','E2','zero']),('lost_mask_retirement',['CLEAR','YM1_b0'])]
 for label,pattern in patterns:
  ww=copy.deepcopy(words['CLOSED-WORD']);idx=ww['operations'].index(pattern);ww['operations'].pop(idx)
  for key in ['source_end','handoff']:
   if idx<ww[key]:ww[key]-=1
  try:replay(ww,roots,g,pd)
  except (AssertionError,KeyError) as e:ctr.append({'name':label,'rejected':True,'reason':str(e)[:400]})
  else:raise AssertionError(('mutant-accepted',label))
 res['independent_negative_controls']=ctr;(a.out/'RESULT.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':res['status'],'closed':res['CLOSED-WORD'],'mutants':len(ctr),'Q':res['invoice']['normalized_per_copy_Q']['decimal_lower'],'room':res['invoice']['normalized_limiting_room']['decimal_lower']},indent=2))
if __name__=='__main__':main()
