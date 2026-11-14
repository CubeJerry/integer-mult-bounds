#!/usr/bin/env python3
"""Independent dense-history reconstruction and exact finite certificates."""
import argparse,gzip,hashlib,json,importlib.util
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
def need(x,s):
 if not x:raise ValueError(s)
def read(p,pin=None):
 b=p.read_bytes();need(pin is None or hashlib.sha256(b).hexdigest()==pin,'pin '+str(p));return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def summ(a,b,c):
 r=dict(a)
 for j,x in b.items():
  r[j]=r.get(j,F(0))+c*x
  if not r[j]:del r[j]
 return r
class Basis:
 def __init__(self,order):self.order=order;self.b={}
 def reduce(self,r):
  r=dict(r)
  for p in self.order:
   if p in r and p in self.b:r=summ(r,self.b[p],-r[p])
  return r
 def add(self,r):
  r=self.reduce(r)
  if not r:return False
  p=next(p for p in self.order if p in r);c=r[p];self.b[p]={j:x/c for j,x in r.items()};return True
def canonical(r):
 if not r:return ()
 c=r[min(r)];return tuple((j,str(r[j]/c)) for j in sorted(r))
def det(A,p=104729):
 A=[[int(F(x).numerator*pow(F(x).denominator,-1,p))%p for x in row] for row in A];ans=1
 for k in range(len(A)):
  i=next((i for i in range(k,len(A)) if A[i][k]),None)
  if i is None:return 0
  if i!=k:A[i],A[k]=A[k],A[i];ans=-ans
  v=A[k][k];ans=ans*v%p;inv=pow(v,-1,p)
  for i in range(k+1,len(A)):
   c=A[i][k]*inv%p
   for j in range(k+1,len(A)):A[i][j]=(A[i][j]-c*A[k][j])%p
 return ans%p
def run(a):
 spec=importlib.util.spec_from_file_location('independent_dense',a.engine);eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng)
 native=read(a.native,'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883');parent=read(a.parent,'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc')
 word=parent if a.variant=='parent' else read(a.four,'20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f')
 ops=parent['program'][:parent['consumer']['begin']] if a.variant=='parent' else [o for o,t in zip(word['program'],word['parent_event_of_output']) if t is None or t<parent['consumer']['begin']]
 q=dict(word);q['program']=ops;spaces=list(map(eng.span,q['frames']));roles={int(k):v for k,v in parent['source_role_map'].items()}
 host=sorted((native['live'][i],roles[b],roles[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2']));D={d for _,_,d in host}
 cap={t:(str(t),[o[1]]) for t,o in enumerate(ops) if o[0]!='CLEAR'}
 final,den,loc,bill,snaps=eng.run(q,spaces,capture_after=cap)
 order=sorted(set(range(400))-D)+sorted(D);H=Basis(order)
 for i in sorted(loc,reverse=True):
  if loc[i]==127:H.add({j:F(x,den) for j,x in enumerate(final[i]) if x})
 need(len(H.b)==200,'Hub rank');need(all(H.reduce({j:F(1)})=={j:F(1)} for j in D),'unchanged D quotient')
 triples=sorted((x,y,x^y) for x in range(1,512) for y in range(x+1,512) if y<(x^y));need(len(triples)==43435,'C2 census')
 lookup={frozenset((0,)+t):i for i,t in enumerate(triples)};elig={}
 def eligible(c,d):
  key=(c,d)
  if key in elig:return elig[key]
  lo,hi=sorted((spaces[c],spaces[d]),key=len);answer=[]
  if lo<=hi and len(lo)<=4<=len(hi):
   if len(lo)==4:answer=[lookup[lo]]
   elif len(lo)==2:
    x=next(iter(lo-{0}));answer=sorted({lookup[frozenset((0,x,y,x^y))] for y in hi-lo})
   else:
    nz=sorted(hi-{0});answer=[lookup[frozenset((0,x,y,x^y))] for x in nz for y in nz if x<y<(x^y)]
  elig[key]=answer;return answer
 pools=[set() for _ in triples];table={};hubchecks=0
 def observe(row,c,targets):
  nonlocal hubchecks
  reduced=H.reduce(row)
  if c==127:need(not reduced,'historical Hub containment');hubchecks+=1
  if not targets or not reduced:return
  key=canonical(reduced);table[key]=dict((j,F(x)) for j,x in key)
  for i in targets:pools[i].add(key)
 for i,c in enumerate(q['initial']):observe({i:F(1)},c,eligible(c,c))
 for t,o in enumerate(ops):
  if o[0]=='CLEAR':continue
  dd,rr,ll=snaps[str(t)];i=o[1];c=ll[i]
  target=eligible(o[2],o[3]) if o[0]=='MOVE' else eligible(c,c)
  observe({j:F(x,dd) for j,x in enumerate(rr[i]) if x},c,target)
 need(len(table)==298,'projective history rows')
 authrows=[{int(j):F(x) for j,x in r.items()} for r in read(a.bundle/'ROWS.json.gz')];authkeys=[canonical(r) for r in authrows]
 need(set(authkeys)==set(table),'independent reduced rows agree')
 authpools=read(a.bundle/'POOLS.json.gz');need(all(p=={authkeys[j] for j in ids} for p,ids in zip(pools,authpools)),'all43435 independently reconstructed pools')
 # The second part verifies the exact rank witnesses in these actual pools.
 def root(h):
  z=native['frames'][native['initial'][h]][0];ones=[i for i in range(9) if z>>i&1]
  if len(ones)==3:return [2 if i in ones else -1 for i in range(9)]
  zeros=[i for i in range(9) if i not in ones];need(len(zeros)==2,'source root shape')
  return [3*(int(i==zeros[0])-int(i==zeros[1])) for i in range(9)]
 frame=[5,56,65,69,77,96,100,103];roots={h:root(h) for h,_,_ in host}
 gram=[{d:F(sum(x*y for x,y in zip(roots[h],roots[k])),18) for k,_,d in host if sum(x*y for x,y in zip(roots[h],roots[k]))} for h in frame]
 need(all(gram[i].get(next(d for k,_,d in host if k==h),0)==int(i==j) for i in range(8) for j,h in enumerate(frame)),'orthonormal frame')
 kinds=[];units={};nuisance=set()
 for i,r in enumerate(authrows):
  if set(r)<=D:
   kinds.append('D' if len(r)==1 else 'M')
   if len(r)==1:units[i]=next(iter(r))
  else:
   need(len(r)==1 and next(iter(r)) not in nuisance,'independent nuisance coordinates');nuisance.update(r);kinds.append('Y')
 need(len(nuisance)==104,'104 nuisance directions')
 distinct=set()
 for ids in authpools:
  known=tuple(sorted(units[i] for i in ids if kinds[i]=='D'));mixed=tuple(sorted(i for i in ids if kinds[i]=='M'));distinct.add((known,mixed))
 clean=read(a.bundle/'CLEAN-MINORS.json.gz');mixed=read(a.bundle/'MIXED-MINORS.json.gz');seen=set();prime_fallbacks=0
 for entry in clean+mixed:
  known=tuple(entry['known_D_roles']);mi=tuple(entry.get('mixed_rows',[]));key=(known,mi);need(key in distinct and key not in seen,'exact certificate coverage');seen.add(key)
  keep=D-set(known);cols=entry['minor_original_columns'];need(set(cols)<=keep and len(set(cols))==len(cols),'minor outside known coordinates')
  extra=[{j:x for j,x in authrows[i].items() if j in keep} for i in mi]
  B=Basis(sorted(D,reverse=True))
  for row in reversed(extra):B.add(row)
  r=entry.get('exact_mixed_rank',0);need(len(B.b)==r,'exact rational extra rank')
  chosen=[extra[i] for i in entry.get('chosen_mixed_indices',[])];need(len(chosen)==r and len(cols)==8+r,'minor dimensions')
  mat=[[row.get(j,0) for j in cols] for row in chosen+gram]
  z=det(mat)
  if not z:z=det(mat,1000003);prime_fallbacks+=1
  need(z!=0,'nonzero characteristic-zero minor')
 need(seen==distinct,'every unique local pool certified')
 need(len(clean)==40963 and len(mixed)==2062,'source certificate case counts')
 # A granted Gram row invalidates the tight independence certificate.
 need(det([[gram[0].get(j,0) for j in sorted(D)[:8]]]*8)==0,'dependent minor control')
 control=Basis(sorted(D));control.add(gram[0]);need(len(control.b)==1,'free Gram row nonzero')
 for row in gram:control.add(row)
 need(len(control.b)==8 and 1+8-len(control.b)==1,'free Gram observation creates intersection')
 E=Basis(list(range(400)))
 for _,b,d in host:
  row={j:F(x,den) for j,x in enumerate(final[b]) if x};row=summ(row,{b:F(1),d:F(-1)},F(-1));E.add(row)
 need(len(E.b)==82,'actual reverse debt82')
 out={'status':'PASS_INDEPENDENT_DENSE_PRETERMINAL_HISTORY','variant':a.variant,'engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),'history_Hub_rows_checked':hubchecks,'all_historical_Hub_rows_in_final_span':True,'actual_Hub_rank':len(H.b),'actual_reverse_rank':len(E.b),'C2_pools_reconstructed':len(pools),'projective_history_rows':len(table),'nuisance_directions':104,'mixed_exact_rank_and_minor_cases':len(mixed),'pure_coordinate_minors':len(clean),'different_prime':104729,'fallbacks_to_author_prime':prime_fallbacks,'source_bill':bill,'negative_controls':['duplicate Gram minor vanishes','granting a Gram row defeats zero-intersection dimension inequality'],'independence':'Reuses pinned prior independently authored dense common-denominator engine, not the new author sparse engine. New actual-history collection, geometric refinement enumeration, rational rank checks and determinant verification. Witness minors are author-supplied data, not assumed results.','scope':'Exact source histories and characteristic-zero tensor conclusion; fixed-history model only. No new supplier or kappa.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','parent','four','engine','bundle','output']:p.add_argument('--'+k,type=Path,required=True)
 p.add_argument('--variant',choices=['parent','four'],required=True);run(p.parse_args())
