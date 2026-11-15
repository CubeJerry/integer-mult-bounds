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

def replay(word,roots,geom,strict=True):
 loc={f'X{i}_b{b}':f'L{i}' for i in range(111) for b in range(2)}
 loc.update({f'Y{i}_b{b}':'zero' for i in range(111) for b in range(2)})
 val={f'X{i}_b{b}':1<<(2*i+b) for i in range(111) for b in range(2)}
 val.update({f'Y{i}_b{b}':1<<(222+2*i+b) for i in range(111) for b in range(2)})
 original=set(loc);owned=set();birth=set();counts=collections.Counter();profile=collections.Counter();history=[];seen=set();kernels={};dirty=0;handoff=None;terminals={};source_checked=False
 packets=[f'P{i}_b{b}' for i in range(8) for b in range(2)]
 for n,op in enumerate(word['operations']):
  if n==word['handoff']:handoff={k:[loc[k],val[k]] for k in owned}
  t=op[0];counts[t]+=1
  if t=='INIT':
   _,a,c=op;assert a not in val and a not in birth,('double-birth',n,a);assert c in geom.B
   if a in packets and not source_checked:
    assert all(loc[f'X{i}_b{b}']=='Hub' and val[f'X{i}_b{b}']==1<<(2*i+b) for i in range(111) for b in range(2)),('source-not-restored-before-packets',n)
    source_checked=True
   loc[a]=c;val[a]=0;owned.add(a);birth.add(a)
  elif t=='ADD':
   _,a,b=op;assert a in val and b in val and a!=b,('invalid-add',n,op)
   assert geom.same(loc[a],loc[b]),('noncochart',n,op,loc[a],loc[b]);val[b]^=val[a]
  elif t=='MOVE':
   _,a,c=op;assert a in val and c in geom.B,('invalid-move',n,op)
   old=loc[a]
   assert geom.sub(old,c) if a in original else geom.sub(c,old),('wrong-direction',n,op,old)
   d=abs(geom.dim(c)-geom.dim(old));assert d>0,('zero-rank-move',n,op);profile[d]+=1;loc[a]=c
   if a in ['P0_b0','P0_b1'] and c=='A15':kernels[a]=val[a]&MASK
   if a in packets and c=='zero':terminals[a]=val[a]&MASK
  elif t=='CLEAR':
   _,a=op;assert a in owned and a in val,('bad-clear',n,a)
   dirty+=bool(val[a]);owned.remove(a);del val[a];del loc[a]
  else:raise AssertionError(('unadmitted-opcode',t))
  for a in packets:
   if a in val and geom.dim(loc[a])<8 and val[a] not in seen:seen.add(val[a]);history.append(val[a])
 if handoff is None:handoff={k:[loc[k],val[k]] for k in owned}
 assert handoff==word['expected'],('handoff-mismatch',set(handoff)^set(word['expected']))
 done={tuple(x) for x in word['completed_targets']}
 for i in range(111):
  for b in range(2):
   assert val[f'X{i}_b{b}']==1<<(2*i+b) and loc[f'X{i}_b{b}']=='Hub',('X-endpoint',i,b)
   target=(1<<(222+2*i+b))^((1<<(2*i+b)) if (i,b) in done else 0)
   assert val[f'Y{i}_b{b}']==target,('Y-value',i,b,hex(val[f'Y{i}_b{b}']^target))
   target_chart=f'F{i}' if (i,b) in done or word['closed'] else 'zero'
   assert geom.same(loc[f'Y{i}_b{b}'],target_chart),('Y-chart',i,b)
 assert len(owned)==(0 if word['closed'] else len(birth)),('owner-end',len(owned))
 assert set(terminals)==set(packets)
 raw=[v for k,(c,v) in handoff.items() if k.startswith('C')]
 assert len(raw)==160
 K0=[(1<<i)^sum(1<<j for j in range(111) if i!=j and sum(a*b for a,b in zip(roots[i],roots[j]))==0) for i in range(111)]
 h=K0[0]^K0[4];W0=[K0[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)]
 W=[embed(x,b) for x in W0 for b in range(2)];K=[embed(x,b) for x in K0 for b in range(2)]
 assert [[hex(embed(x,b)) for b in range(2)] for x in W0]==word['W_rows_lanes_hex']
 assert rank(W)==30 and rank(K)==18 and rank(raw)==80 and dimcap(raw,W)==19
 assert rank(raw+W)==91
 T=[handoff[a][1] for a in packets];G=T+list(kernels.values())
 assert all(not(x>>222) for x in T+raw)
 wh=witnesses(history,W);cw=witnesses(history,raw)
 out={'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(k*v for k,v in profile.items()),'dirty_clears':dirty,'owners_born':len(birth),'history_rank':rank(history),'history_rows':len(history),'history_pure_X_dimension':rank(history)-rank([x>>222 for x in history]),'W_history_dimension':dimcap(history,W),'terminal_rank':rank(T),'terminal_W_intersection':dimcap(T,W),'normalized_rank':rank(G),'normalized_W_intersection':dimcap(G,W),'actual_completed':sorted(done),'kernels_hex':{k:hex(v) for k,v in kernels.items()},'actual_increment_rank':rank(raw),'actual_increment_W_intersection':dimcap(raw,W),'zero_packets':[a for a in packets if handoff[a][1]==0]}
 if strict:
  assert done=={(0,0),(0,1)} and len(birth)==400
  assert out['history_rank']==93 and out['history_pure_X_dimension']==91 and out['W_history_dimension']==30
  assert out['terminal_rank']==13 and out['terminal_W_intersection']==11
  assert out['zero_packets']==['P6_b1','P7_b0','P7_b1']
  if word['closed']:
   assert dict(counts)=={'INIT':400,'ADD':2126,'MOVE':990,'CLEAR':400}
   assert dict(profile)=={1:366,2:24,3:238,4:142,7:220} and dirty==397
 return out,{'rows_hex':[hex(x) for x in history],'W_witnesses_hex':wh,'W_rows_hex':[hex(x) for x in W],'actual_raw_increment_rows_hex':[hex(x) for x in raw],'actual_raw_increment_witnesses_hex':cw}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 src=a.repo/SOURCE;assert sha(src)==SOURCE_SHA;roots=json.loads(src.read_text())['native_roots'];words={n:json.loads((a.package/'output'/f'{n}.json').read_text()) for n in ['WORD','CLOSED-WORD']};g=Geometry(words['WORD']['charts']);result={'status':'PASS_INDEPENDENT_TWO_COPY_SCALAR_REVIEW','source_sha256':SOURCE_SHA,'word_file_sha256':{n:sha(a.package/'output'/f'{n}.json') for n in words}}
 assert words['WORD']['operations']==words['CLOSED-WORD']['operations'][:words['WORD']['handoff']]
 assert words['WORD']['charts']==words['CLOSED-WORD']['charts']
 for n,w in words.items():
  result[n],hist=replay(w,roots,g);(a.out/f'{n}-HISTORY.json').write_text(json.dumps(hist,indent=2)+'\n')
 profile={int(k):v for k,v in result['CLOSED-WORD']['profile'].items()};assert all(v%2==0 for v in profile.values())
 result['per_copy_price']=prices({r:v//2 for r,v in profile.items()})
 result['whole_two_copy_price']={k:enc(scale(2,(Fraction(v['lower']),Fraction(v['upper'])))) for k,v in result['per_copy_price'].items()}
 controls=[]
 patterns=[('lost_cross_copy_formation',['ADD','X86_b1','X82_b0'],'first'),('lost_cross_copy_restoration',['ADD','X37_b1','X31_b0'],'last'),('lost_first_copy_source_capture',['ADD','X0_b0','R0_b0'],'first'),('lost_second_copy_feedback',['ADD','P0_b1','Y0_b1'],'first'),('lost_second_copy_mask',['ADD','YM0_b1','P0_b1'],'first'),('lost_first_raw_packet_read',['ADD','C0_1_0_b0','P0_b0'],'first'),('lost_second_copy_move',['MOVE','P7_b1','zero'],'first'),('lost_zero_owner_retirement',['CLEAR','P7_b1'],'first')]
 for label,pattern,which in patterns:
  w=copy.deepcopy(words['CLOSED-WORD']);positions=[i for i,op in enumerate(w['operations']) if op==pattern];assert positions,(label,pattern);i=positions[0] if which=='first' else positions[-1];w['operations'].pop(i)
  if i<w['handoff']:w['handoff']-=1
  try:replay(w,roots,g)
  except (AssertionError,KeyError) as e:controls.append({'name':label,'rejected':True,'reason':str(e)[:400]})
  else:raise AssertionError(('mutant-accepted',label))
 result['independent_negative_controls']=controls
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'closed':result['CLOSED-WORD'],'mutants_rejected':len(controls),'per_copy_Q':result['per_copy_price']['Q']['decimal_lower']},indent=2))
if __name__=='__main__':main()
