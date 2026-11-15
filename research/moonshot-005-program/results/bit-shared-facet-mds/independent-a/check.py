#!/usr/bin/env python3
"""Independent all-888-column replay and direct signed-support atlas reconstruction."""
import argparse,collections,copy,hashlib,itertools,json,math
from functools import lru_cache
from pathlib import Path
from fractions import Fraction
import sympy as sp
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(x):
 x=tuple(x);g=math.gcd(*x);x=tuple(v//g for v in x)
 return x if next(v for v in x if v)>0 else tuple(-v for v in x)
def rank(rows):
 b={}
 for a in rows:
  while a:
   p=a.bit_length()-1
   if p in b:a^=b[p]
   else:b[p]=a;break
 return len(b)
def gf4(a,b):
 a0,a1=a&1,a>>1;b0,b1=b&1,b>>1
 return (a0*b0^a1*b1)|((a0*b1^a1*b0^a1*b1)<<1)
def gf4inv(a):
 assert a;return gf4(a,a)
def mulrow(c,rows):
 return [xor(rows[b]for b in range(2)if gf4(c,1<<b)>>k&1) for k in range(2)]
def xor(xs):
 y=0
 for x in xs:y^=x
 return y
class Geometry:
 def __init__(self,charts):
  self.B={}
  for n,c in charts.items():
   rows=c['rows']
   if c['kind']=='ann':cols=sp.Matrix(rows).nullspace()if rows else [sp.eye(8)[:,j]for j in range(8)]
   else:cols=sp.Matrix(rows).T.columnspace()if rows else []
   self.B[n]=sp.Matrix.hstack(*cols)if cols else sp.zeros(8,0)
 @lru_cache(None)
 def sub(self,a,b):return self.B[b].row_join(self.B[a]).rank()==self.B[b].cols
 @lru_cache(None)
 def same(self,a,b):return self.sub(a,b)and self.sub(b,a)
 def dim(self,c):return self.B[c].cols

def replay(w,R,g,completed=False,milestones=True):
 n=4;val={f'X{j}_{k}':1<<(4*j+k)for j in range(111)for k in range(n)}|{f'Y{j}_{k}':1<<(444+4*j+k)for j in range(111)for k in range(n)}
 loc={f'X{j}_{k}':f'L{j}'for j in range(111)for k in range(n)}|{f'Y{j}_{k}':'zero'for j in range(111)for k in range(n)}
 orig=set(val);owners=set();born=set();counts=collections.Counter();profile=collections.Counter();dirty=0;events={};foreign=[j for j in range(111)if j!=3 and dot(R[j],R[3])==0]
 A={};members={t:[]for t in range(4)};qs=[76,81,91,96]
 for j in foreign:
  ids=[t for t,q in enumerate(qs)if dot(R[j],R[q])==0][:2];assert len(ids)==2
  if milestones:assert w['source_assignments'][str(j)]==ids
  t0,t1=ids;inv=gf4inv(t0^t1);src0=[1<<(4*j+k)for k in range(2)];src1=[1<<(4*j+2+k)for k in range(2)]
  encoded=[]
  for t in [t1,t0]:
   a=mulrow(gf4(inv,t),src0);b=mulrow(inv,src1);encoded.append([a[k]^b[k]for k in range(2)])
  for s,t in enumerate(ids):A[j,s]=encoded[s];members[t].append((j,s))
 marks={v:k for k,v in w['milestones'].items()}
 def capture(step):
  if not milestones or step not in marks:return
  name=marks[step]
  if name=='all_chart_aggregates_formed':
   for t in range(4):
    for k in range(2):
     aggregate=xor(A[j,s][k]for j,s in members[t])
     if t<2:
      key=f'Y3_{2*t+k}';ypart=(1<<(444+12+2+k))^((1<<(444+12+k))if t==0 else 0);expected=ypart^aggregate
     else:
      pj,ps=w['pivot_originals'][str(t)];assert (pj,ps)in members[t];key=f'X{pj}_{2*ps+k}';expected=aggregate
     assert val[key]==expected,('aggregate',t,k);assert g.same(loc[key],f'C{t}')
   events[name]={'all_four_actual_binary_aggregate_pairs_verified':True,'foreign_count':len(foreign)}
  if name=='local_correction_completed_sources_not_yet_restored':
   for k in range(4):assert val[f'Y3_{k}']==(1<<(444+12+k))^xor(1<<(4*j+k)for j in foreign)
   events[name]={'all_four_independent_Y_originals_preserved':True}
  if name=='all_original_sources_restored':
   for j in range(111):
    for k in range(4):assert val[f'X{j}_{k}']==1<<(4*j+k)and g.same(loc[f'X{j}_{k}'],'Hub')
   events[name]={'all444_X_columns_restored':True}
 for step,o in enumerate(w['operations']):
  capture(step);t=o[0];counts[t]+=1
  if t=='INIT':
   _,n,c=o;assert n not in born and n not in val;born.add(n);owners.add(n);val[n]=0;loc[n]=c
  elif t=='ADD':
   _,a,b=o;assert a in val and b in val and a!=b;assert g.same(loc[a],loc[b]),('noncochart',step,o,loc[a],loc[b]);val[b]^=val[a]
  elif t=='MOVE':
   _,a,c=o;assert a in val and c in g.B
   assert g.sub(loc[a],c)if a in orig else g.sub(c,loc[a]),('wrong_move',step,o,loc[a]);d=abs(g.dim(c)-g.dim(loc[a]));assert d>0;profile[d]+=1;loc[a]=c
  elif t=='CLEAR':
   _,a=o;assert a in owners;dirty+=bool(val[a]);owners.remove(a);del val[a];del loc[a]
  else:raise AssertionError(o)
 capture(len(w['operations']))
 assert not owners
 for j in range(111):
  for k in range(4):
   assert val[f'X{j}_{k}']==1<<(4*j+k)and g.same(loc[f'X{j}_{k}'],'Hub'),('X_endpoint',j,k)
   target=1<<(444+4*j+k)
   if j==3:target^=(1<<(4*j+k))if completed else xor(1<<(4*l+k)for l in foreign)
   assert val[f'Y{j}_{k}']==target and g.same(loc[f'Y{j}_{k}'],f'F{j}'),('Y_endpoint',j,k)
 return {'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(r*c for r,c in profile.items()),'dirty_clears':dirty,'milestones':events,'all888_independent_columns':True,'completed_receiver3':completed}

def atlas(R,author):
 patterns=sorted({tuple(i for i,v in enumerate(r)if v)for r in R if sum(v!=0 for v in r)==4});assert len(patterns)==14
 full={tuple(2*int(i==j)for i in range(8))for j in range(8)}
 for S in patterns:
  for signs in itertools.product([-1,1],repeat=3):
   v=[0]*8;v[S[0]]=1
   for p,z in zip(S[1:],signs):v[p]=z
   full.add(tuple(v))
 full=sorted(full);assert len(full)==120 and set(map(tuple,R))<=set(full);assert full==list(map(tuple,author['full_roots']))
 assert all(dot(a,a)==4 for a in full)
 out=[]
 for i,r in enumerate(R):
  foreign=[x for x in full if dot(r,x)==0];assert len(foreign)==63
  by={}
  for q in full:
   d=dot(r,q)
   if abs(d)!=2:continue
   z=norm([4*x-d*y for x,y in zip(q,r)]);mask=sum(1<<j for j,v in enumerate(R)if dot(r,v)==dot(q,v)==0);by[z]=(q,mask)
  assert len(by)==28
  assert all(sum(dot(q,x)==0 for x in foreign)==36 for q,mask in by.values())
  assert all(sum(dot(q,x)==0 for q,mask in by.values())==16 for x in foreign)
  aa={}
  for z in author['rows'][i]['atlas']:
   q=tuple(z['normal']);d=dot(r,q);assert q in full and abs(d)==2
   key=norm([4*x-d*y for x,y in zip(q,r)]);assert key not in aa;aa[key]=int(z['native_mask_hex'],16)
  assert aa=={z:v[1]for z,v in by.items()}
  out.append({'receiver':i,'atlas_charts':28,'full_foreign_roles':63,'chart_support':36,'foreign_incidence':16})
 return {'full_roots_reconstruction':'Eight doubled axes and all eight signed lines on each of14 native four-supports; independent of author reflection closure.','full_line_count':120,'all111_atlases':out}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;R=json.loads(raw)['native_roots']
 names=['WORD','COMPLETED-CONTROL-WORD'];ws={n:json.loads((a.source/'four-chart-word'/f'{n}.json').read_text())for n in names};g=Geometry(ws['WORD']['charts']);out={'status':'PASS_INDEPENDENT_SHARED_FACET_REPLAY_AND_ATLAS','native_sha256':ROOT_SHA,'pins':{n:sha(a.source/'four-chart-word'/f'{n}.json')for n in names}}
 for n,w in ws.items():out[n]=replay(w,R,g,completed=n!='WORD')
 out['atlas']=atlas(R,json.loads((a.source/'GEOMETRY.json').read_text()))
 # Semantic controls deliberately skip positional milestone comparisons.
 base=ws['WORD'];ops=base['operations'];patterns=[]
 patterns.append(('source_encoding',next(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'))))
 patterns.append(('Y_preencoding',next(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('Y')and o[2].startswith('Y'))))
 patterns.append(('chart_aggregate',next(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X')and o[1].split('_')[0]!=o[2].split('_')[0])))
 patterns.append(('Y_chart_read',next(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('Y'))))
 patterns.append(('Y_postencoding',max(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('Y')and o[2].startswith('Y'))))
 patterns.append(('source_inverse',max(i for i,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'))))
 controls=[]
 for label,i in patterns:
  bad=copy.deepcopy(base);bad['operations'].pop(i)
  try:replay(bad,R,g,milestones=False)
  except(AssertionError,KeyError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)[:160]})
  else:raise AssertionError(('mutant accepted',label))
 for label,pattern in [('late_K_read','ADD'),('late_owner_retirement','CLEAR')]:
  bad=copy.deepcopy(ws['COMPLETED-CONTROL-WORD']);i=max(i for i,o in enumerate(bad['operations'])if o[0]==pattern);bad['operations'].pop(i)
  try:replay(bad,R,g,completed=True,milestones=False)
  except(AssertionError,KeyError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)[:160]})
  else:raise AssertionError(('mutant accepted',label))
 bad=copy.deepcopy(base);bad['charts']['C0']={'kind':'ann','rows':[R[3],R[0]]}
 try:replay(bad,R,Geometry(bad['charts']),milestones=False)
 except(AssertionError,KeyError)as e:controls.append({'name':'wrong_proper_chart_normal','rejected':True,'reason':str(e)[:160]})
 else:raise AssertionError('invalid geometry accepted')
 out['negative_controls']=controls
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print(out['WORD']);print(out['COMPLETED-CONTROL-WORD'])
if __name__=='__main__':main()
