#!/usr/bin/env python3
"""Independent exact replay. No imports from source constructor/checker."""
import argparse,collections,copy,hashlib,json
from functools import lru_cache
from pathlib import Path
from fractions import Fraction
import sympy as sp

SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
MASK=(1<<111)-1

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

def replay(word,roots,geom,strict=True):
 loc={f'X{i}':f'L{i}' for i in range(111)};loc.update({f'Y{i}':'zero' for i in range(111)})
 val={f'X{i}':1<<i for i in range(111)};val.update({f'Y{i}':1<<(111+i) for i in range(111)})
 original=set(loc);owned=set();birth=set();counts=collections.Counter();profile=collections.Counter();history=[];histseen=set();kernels={};capture={};dirty=0;handoff=None;terminals={};initial_at_chart={};source_checked=False
 for n,op in enumerate(word['operations']):
  if n==word['handoff']:
   handoff={k:[loc[k],val[k]] for k in owned}
  t=op[0];counts[t]+=1
  if t=='INIT':
   _,a,c=op; assert a not in val and a not in birth,('double-birth',n,a);assert c in geom.B
   if a.startswith('P') and a[1:].isdigit() and not source_checked:
    assert all(loc[f'X{i}']=='Hub' and val[f'X{i}']==1<<i for i in range(111)),('source-not-restored',n)
    source_checked=True
   loc[a]=c;val[a]=0;owned.add(a);birth.add(a)
  elif t=='ADD':
   _,a,b=op;assert a in val and b in val and a!=b,('invalid-add',n,op)
   assert geom.same(loc[a],loc[b]),('noncochart',n,op,loc[a],loc[b])
   if b.startswith('PURE'):capture[b]=val[a]
   val[b]^=val[a]
  elif t=='MOVE':
   _,a,c=op;assert a in val and c in geom.B,('invalid-move',n,op)
   old=loc[a]
   if a in original:assert geom.sub(old,c),('original-downward',n,op,old)
   else:assert geom.sub(c,old),('owner-upward',n,op,old)
   d=abs(geom.dim(c)-geom.dim(old));assert d>0,('zero-rank-move',n,op);profile[d]+=1;loc[a]=c
   if (a,c) in [('P0','A15'),('P1','A30')]:kernels[a]=val[a]&MASK;initial_at_chart[a]=val[a]
   if a.startswith('P') and a[1:].isdigit() and c=='zero':terminals[a]=val[a]&MASK
  elif t=='CLEAR':
   _,a=op;assert a in owned and a in val,('bad-clear',n,a)
   dirty+=bool(val[a]);owned.remove(a);del val[a];del loc[a]
  else:raise AssertionError(t)
  for a in ('P0','P1','P2','P3','P4','P5','P6','P7'):
   if a in val and geom.dim(loc[a])<8 and val[a] not in histseen:
    histseen.add(val[a]);history.append(val[a])
 if handoff is None:handoff={k:[loc[k],val[k]] for k in owned}
 assert handoff==word['expected'],('handoff-mismatch',set(handoff)^set(word['expected']))
 done=word['completed_targets']
 for i in range(111):
  assert val[f'X{i}']==1<<i and loc[f'X{i}']=='Hub',('X-endpoint',i)
  target=(1<<(111+i))^((1<<i) if i in done else 0)
  assert val[f'Y{i}']==target,('Y-value',i,hex(val[f'Y{i}']^target))
  expected_chart=f'F{i}' if i in done or word['closed'] else 'zero'
  assert geom.same(loc[f'Y{i}'],expected_chart),('Y-chart',i,loc[f'Y{i}'],expected_chart)
 assert len(owned)==(0 if word['closed'] else len(birth)),('owner-end',len(owned))
 assert set(terminals)=={f'P{i}' for i in range(8)}
 # Actual raw cache rows at the handoff and actual pure captures.
 raw=[v for k,(c,v) in handoff.items() if k.startswith('C')]
 K=[(1<<i)^sum(1<<j for j in range(111) if i!=j and sum(a*b for a,b in zip(roots[i],roots[j]))==0) for i in range(111)]
 h=K[0]^K[4]
 W=[K[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)]
 assert [hex(x) for x in W]==word['W_rows_hex']
 assert rank(W)==15 and rank(K)==9 and rank(raw)==40 and dimcap(raw,W)==8
 assert capture=={'PURE0_A192':1,'PURE0_F7':1,'PURE7_F6':128},capture
 assert kernels['P0']==int(word['kernel_x_hex'],16)
 assert kernels['P1']==int(word['stationary_kernel']['row_hex'],16)==W[8]^225
 assert handoff['P1']==['zero',225]
 # Ground X parts are unchanged by the actual subsequent public-y unmask.
 T=[terminals[f'P{i}'] for i in range(8)];G=T+list(kernels.values())
 fit=[]
 for i in range(111):
  local=[1<<j for j in range(111) if sum(a*b for a,b in zip(roots[i],roots[j]))==0]
  if contains(G+local,1<<i):fit.append(i)
 wh=witnesses(history,W)
 out={'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(k*v for k,v in profile.items()),'dirty_clears':dirty,'history_rank':rank(history),'history_rows':len(history),'history_pure_X_dimension':rank(history)-rank([x>>111 for x in history]),'W_history_dimension':dimcap(history,W),'terminal_rank':rank(T),'terminal_W_intersection':dimcap(T,W),'normalized_rank':rank(G),'normalized_W_intersection':dimcap(G,W),'normalized_canonical_intersection':dimcap(G,K),'global_free_access_fits':fit,'actual_completed':done,'kernels_hex':{k:hex(v) for k,v in kernels.items()},'terminal_hex':{k:hex(v) for k,v in terminals.items()},'pure_capture_hex':{k:hex(v) for k,v in capture.items()}}
 if strict:
  assert out['actual_completed']==[0,5,6,7]
  assert out['history_rank']==48 and out['history_pure_X_dimension']==47 and out['W_history_dimension']==15
  assert out['terminal_rank']==8 and out['terminal_W_intersection']==6
  assert out['normalized_rank']==10 and out['normalized_W_intersection']==7 and out['normalized_canonical_intersection']==0
  assert fit==[0,4,5,6,7,8,14,19,22,30,35,38,59,66,69]
  if word['closed']:
   assert dict(counts)=={'INIT':204,'ADD':960,'MOVE':502,'CLEAR':204}
   assert dict(profile)=={1:190,2:12,3:119,4:72,5:2,7:107}
   assert dirty==204
 return out,{'rows_hex':[hex(x) for x in history],'W_witnesses_hex':wh,'W_rows_hex':[hex(x) for x in W]}

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

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 src=a.repo/SOURCE;assert sha(src)==SOURCE_SHA;roots=json.loads(src.read_text())['native_roots']; words={n:json.loads((a.package/'output'/f'{n}.json').read_text()) for n in ['WORD','CLOSED-WORD']};g=Geometry(words['WORD']['charts']);result={'status':'PASS_INDEPENDENT_FOUR_AXIS_REVIEW','source_sha256':SOURCE_SHA,'word_file_sha256':{n:sha(a.package/'output'/f'{n}.json') for n in words}}
 for n,w in words.items():
  result[n],hist=replay(w,roots,g);(a.out/f'{n}-HISTORY.json').write_text(json.dumps(hist,indent=2)+'\n')
 result['price']=prices({int(k):v for k,v in result['CLOSED-WORD']['profile'].items()})
 controls=[]
 # Independently chosen removals break acquisition, feedback, cancellation or ownership.
 for label,pattern in [('lost_retained_capture',['ADD','P1','KEEP_P1_A30']),('lost_reset',['ADD','KEEP_P1_A30','P1']),('lost_pure0_A192',['ADD','X0','PURE0_A192']),('lost_pure7_F6',['ADD','X7','PURE7_F6']),('lost_y6_correction',['ADD','PURE0_A192','Y6']),('lost_y0_unmask',['ADD','YM0','P0']),('lost_retirement',['CLEAR','KEEP_P1_A30'])]:
  w=copy.deepcopy(words['CLOSED-WORD']);i=w['operations'].index(pattern);w['operations'].pop(i)
  if i<w['handoff']:w['handoff']-=1
  try:replay(w,roots,g)
  except (AssertionError,KeyError) as e:controls.append({'name':label,'rejected':True,'reason':str(e)[:400]})
  else:raise AssertionError(('mutant-accepted',label))
 result['independent_negative_controls']=controls
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'closed_counts':result['CLOSED-WORD']['counts'],'normalized_rank':result['CLOSED-WORD']['normalized_rank'],'mutants_rejected':len(controls),'Q':result['price']['Q']['decimal_lower'],'room':result['price']['room']['decimal_lower']},indent=2))
if __name__=='__main__':main()
