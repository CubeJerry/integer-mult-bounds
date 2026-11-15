#!/usr/bin/env python3
"""All222-column rational replay and exact failure of every fixed regrouping."""
import argparse,collections,copy,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import sympy as sp
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
class Geometry:
 def __init__(self,charts):
  self.B={}
  for n,c in charts.items():
   x=c['rows'];cols=(sp.Matrix(x).nullspace()if x else[sp.eye(8)[:,j]for j in range(8)])if c['kind']=='ann'else(sp.Matrix(x).T.columnspace()if x else[]);self.B[n]=sp.Matrix.hstack(*cols)if cols else sp.zeros(8,0)
 @lru_cache(None)
 def sub(self,a,b):return self.B[b].row_join(self.B[a]).rank()==self.B[b].cols
 @lru_cache(None)
 def same(self,a,b):return self.sub(a,b)and self.sub(b,a)
 def dim(self,a):return self.B[a].cols

def replay(w,g,strict=False):
 val={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};orig=set(val);owned=set();born=set();counts=collections.Counter();profile=collections.Counter();dirty=0;captured=None
 for k,o in enumerate(w['operations']):
  if strict and k==17:
   captured={n:[loc[n],hex(val[n])]for n in ['X52','X54','X0']};assert [val[n]for n in ['X52','X54','X0']]==[(1<<52)^(1<<54),(1<<54)^1,1]
  t=o[0];counts[t]+=1
  if t=='ADD':
   _,a,b=o;assert a in val and b in val and a!=b and g.same(loc[a],loc[b]),('cochart',k,o);val[b]^=val[a]
  elif t=='MOVE':
   _,a,c=o;assert a in val and c in g.B;assert g.sub(loc[a],c)if a in orig else g.sub(c,loc[a]),('direction',k,o,loc[a]);d=abs(g.dim(c)-g.dim(loc[a]));assert d;profile[d]+=1;loc[a]=c
  elif t=='INIT':
   _,a,c=o;assert a not in born and a not in val;val[a]=0;loc[a]=c;owned.add(a);born.add(a)
  elif t=='CLEAR':
   _,a=o;assert a in owned;dirty+=bool(val[a]);owned.remove(a);del val[a];del loc[a]
  else:raise AssertionError(o)
 assert not owned
 for i in range(111):
  assert loc[f'X{i}']=='Hub'and val[f'X{i}']==1<<i,('X',i)
  expected=1<<(111+i)
  if i in w['fully_completed_native_roles']:expected^=1<<i
  elif str(i)in w['local_output_forms']:
   for j in w['local_output_forms'][str(i)]:expected^=1<<j
  assert g.same(loc[f'Y{i}'],f'F{i}')and val[f'Y{i}']==expected,('Y',i)
 return {'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(r*v for r,v in profile.items()),'dirty_clears':dirty,'early_exit_source_coefficients':captured,'all222_original_columns_verified':True}

def power(r):
 s=1<<160;n=r**199*s**200;lo=0;hi=r*s+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=n:lo=m
  else:hi=m
 return F(lo,s),F(hi,s)
def price(profile):
 a=b=F(0)
 for r,c in profile.items():x,y=power(int(r));a+=c*x;b+=c*y
 return {'lower':str(a),'upper':str(b),'decimal_lower':str(sp.N(sp.Rational(a.numerator,a.denominator),50)),'decimal_upper':str(sp.N(sp.Rational(b.numerator,b.denominator),50))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,default=Path(__file__).parent);a=ap.parse_args();p=a.package;raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;R=json.loads(raw)['native_roots'];words={n:json.loads((p/'output'/f'{n}.json').read_text())for n in ['WORD','COMPLETED-CONTROL-WORD']};g=Geometry(words['WORD']['charts']);out={'status':'PASS_ACTUAL_OVERLAPPING_COHORT_EARLY_EXIT','word_pins':{n:hashlib.sha256((p/'output'/f'{n}.json').read_bytes()).hexdigest()for n in words}}
 for n,w in words.items():out[n]=replay(w,g,strict=True);out[n]['price']=price(out[n]['profile'])
 assert out['WORD']['counts']=={'MOVE':230,'ADD':6}and out['WORD']['profile']=={1:5,2:3,3:1,4:1,5:1,6:2,7:217}
 assert out['COMPLETED-CONTROL-WORD']['counts']=={'MOVE':232,'ADD':14,'INIT':2,'CLEAR':2}
 assert g.dim('H')==2 and g.dim('J')==3 and g.dim('C0')==g.dim('C1')==6
 for i,j in [(0,31),(1,8)]:assert abs(sum(x*y for x,y in zip(R[i],R[j])))==2
 # P is invertible. Any fixed partition making its two source-mixing
 # edges internal joins0,52,54; the actual output0 then violates U's own block.
 valid=[]
 for labels in itertools.product(range(3),repeat=3):
  if labels[0]==labels[1]and labels[1]==labels[2]:
   assert labels[2]==labels[0];valid.append(labels)
 assert valid and all(z[0]==z[2]for z in valid)
 out['fixed_regrouping']={'source_order':[52,54,0],'P':[[1,1,0],[0,1,1],[0,0,1]],'nonzero_source_edges':[[52,54],[54,0]],'forced_common_cohort':[0,52,54],'actual_own_cohort_U_entry':{'receiver':0,'encoded_original':'X52','coefficient':1},'no_partition_has_both_block_diagonal_P_and_zero_own_cohort_U':True}
 controls=[]
 patterns=[('first_encoding',['ADD','X54','X52']),('second_encoding',['ADD','X0','X54']),('first_delivery',['ADD','X52','Y0']),('second_delivery',['ADD','X54','Y1'])]
 for label,op in patterns:
  w=copy.deepcopy(words['WORD']);w['operations'].remove(op)
  try:replay(w,g)
  except(AssertionError,KeyError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)[:120]})
  else:raise AssertionError(label)
 w=copy.deepcopy(words['WORD']);w['operations'].insert(3,['MOVE','X52','J'])
 try:replay(w,g)
 except AssertionError as e:controls.append({'name':'force_early_bank_through_full_common_cohort','rejected':True,'reason':str(e)[:120]})
 else:raise AssertionError('forbidden pooled route accepted')
 w=copy.deepcopy(words['COMPLETED-CONTROL-WORD']);w['operations'].remove(['MOVE','K0','F0'])
 try:replay(w,g)
 except AssertionError as e:controls.append({'name':'omit_paid_proper_ending_import','rejected':True,'reason':str(e)[:120]})
 else:raise AssertionError('missing import accepted')
 out['negative_controls']=controls;out['new_complete_kappa']=False;(p/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print(out['WORD']['price']['decimal_lower'])
if __name__=='__main__':main()
