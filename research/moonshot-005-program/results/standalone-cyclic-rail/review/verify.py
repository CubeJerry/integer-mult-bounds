#!/usr/bin/env python3
"""Independent pure-rail and fixed-m endpoint/invoice review; no author imports."""
import argparse,gzip,hashlib,json,ast,re,importlib.util,sys,copy
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
if not __debug__:raise SystemExit('Exact checks require Python without -O')
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();R=args.repo;D=args.bundle;O=args.output;O.mkdir(parents=True,exist_ok=True)
manifest_bytes=(D/'MANIFEST.json').read_bytes();assert hashlib.sha256(manifest_bytes).hexdigest()=='585d5d19c1825c27c2f0fde4cb4e1ba57822ebd85e5db99267c5963236e13e16'
manifest=json.loads(manifest_bytes);assert all(hashlib.sha256((D/k).read_bytes()).hexdigest()==v for k,v in manifest['files'].items())
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';PP='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2';QP='90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2'
def get(path,pin=None):
 b=path.read_bytes();h=hashlib.sha256(b).hexdigest()
 if pin:assert h==pin
 return json.loads(gzip.decompress(b)),h
s,_=get(R/'research/shared-wire-split-composition/data/final.json.gz',SP);p,_=get(R/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz',PP);q,_=get(D/'rail-repaired.json.gz',QP)
def span(f):
 z={0}
 for x in f:z|={a^x for a in tuple(z)}
 assert len(z)==1<<len(f)
 return z
spaces=list(map(span,q['frames']))
def plus(a,b,c):
 a=a.copy()
 for j,x in b.items():
  v=a.get(j,0)+c*x
  if v:a[j]=v
  else:a.pop(j,None)
 return a
def run(ops,initial,n,owned,rows=None):
 loc=dict(enumerate(initial));A=rows if rows is not None else {i:{i:F(1)} for i in range(n)};A={i:v.copy() for i,v in A.items()};count=Counter();moves=Counter();life=peak=0
 for e in ops:
  op,r=e[:2];assert 0<=r<n+owned;count[op]+=1
  if op=='INIT':assert r>=n and r not in loc;loc[r]=e[2];A[r]={};life+=1
  elif op=='CLEAR':assert r>=n and loc[r]==e[2];del loc[r];del A[r]
  elif op=='MOVE':
   a,b,flag=e[2:];assert type(flag)is bool and flag==(r>=n) and loc[r]==a;assert spaces[a]<spaces[b] or flag and spaces[b]<spaces[a]
   moves[abs(len(q['frames'][a])-len(q['frames'][b]))]+=1;loc[r]=b
  elif op in ('ADD','COPY'):
   z,c,at=e[2:];assert r!=z and loc[r]==loc[z]==at
   if op=='COPY':assert not A[r]
   A[r]=plus(A[r],A[z],F(c))
  elif op=='SCALE':assert loc[r]==e[3] and F(e[2]);A[r]={j:F(e[2])*x for j,x in A[r].items()}
  else:raise AssertionError(op)
  peak=max(peak,len(loc)-n)
 assert len(loc)==n
 return A,loc,{'instructions':len(ops),'counts':dict(count),'moves':dict(sorted(moves.items())),'lifetimes':life,'peak':peak}
raw={int(k):v for k,v in p['private_role_map'].items()};roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()};assert sorted(raw.values())==list(range(1480,1880))
assert p['program'][:400]==[['ADD',raw[r],r,'-1',s['initial'][r]] for r in sorted(raw)]
assert p['program'][-400:]==[['ADD',raw[r],r,'1',s['final'][r]] for r in sorted(raw)]
# Establish exact purity on common originals at the independent difference cut.
taint={i:i<1480 for i in range(1880)};end=len(p['program'])-400
for e in p['program'][400:end]:
 op,r=e[:2]
 if op=='INIT':taint[r]=False
 elif op=='CLEAR':del taint[r]
 elif op in ('ADD','COPY'):taint[r]=taint[r] or taint[e[2]]
contam=[r for r in range(1480,1880) if taint[r]];assert contam==[1587,1613,1614,1627,1628,1639]
for dst in contam:
 g={dst:F(1)}
 for e in reversed(p['program'][400:end]):
  op,r=e[:2]
  if op in ('INIT','CLEAR'):g.pop(r,None)
  elif op in ('ADD','COPY'):
   z,c=e[2:4];a=g.get(r,0)*F(c)
   if a:
    g[z]=g.get(z,0)+a
    if not g[z]:del g[z]
  elif op=='SCALE' and r in g:g[r]*=F(e[2])
 assert not any(r<1480 and a for r,a in g.items())
qa,ql,qbill=run(q['program'],q['initial'],400,q['owned_fields']);pa,pl,_=run(p['program'],p['initial'],1880,p['owned_fields'],{i:({i-1480:F(1)} if i>=1480 else {}) for i in range(1880)})
assert all(not pa[i] for i in range(1480)) and all(qa[i]==pa[i+1480] and ql[i]==pl[i+1480] for i in range(400))
# A nonzero determinant modulo65537 proves the400-input rail has full Q-rank.
qb={}
for row in qa.values():
 x={j:(v.numerator*pow(v.denominator,-1,65537))%65537 for j,v in row.items()}
 while x:
  j=min(x)
  if j not in qb:
   inv=pow(x[j],-1,65537);qb[j]={k:v*inv%65537 for k,v in x.items()};break
  c=x[j]
  for k,v in qb[j].items():
   z=(x.get(k,0)-c*v)%65537
   if z:x[k]=z
   else:x.pop(k,None)
assert len(qb)==400
# Replay the six supplied recipes with the frozen independent Pauli engine.
vp=R/'research/shared-wire-split-composition/frozen/native_verify.py';assert hashlib.sha256(vp.read_bytes()).hexdigest()=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'
spec=importlib.util.spec_from_file_location('bridge_frozen_phase',vp);phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)
maps=json.loads((D/'CHART-MAPS.json').read_text());assert maps['new_distinct_pairs']==6
for z in maps['new_maps']:
 assert z['recipe']['rank']==1;phase.equal(phase.recipe(z['recipe']),phase.adjoint(phase.frame(q['frames'][z['source']],9))+phase.frame(q['frames'][z['target']],9),'reviewed pure rail map')
mutant=copy.deepcopy(maps['new_maps'][0]);mutant['recipe']['left']['phase']=(mutant['recipe']['left']['phase']+1)%4
try:phase.equal(phase.recipe(mutant['recipe']),phase.adjoint(phase.frame(q['frames'][mutant['source']],9))+phase.frame(q['frames'][mutant['target']],9),'wrong phase')
except ValueError:pass
else:raise AssertionError('wrong global phase accepted')
common,cl,cbill=run(s['program'],s['initial'],1480,s['owned_fields'])
checks={}
for m in (2,3):
 w,wh=get(D/f'm{m}/WORD.json.gz');a,loc,bill=run(w['program'],w['initial'],w['public'],w['owned_fields']);assert w['public']==1480+400*(m-1)
 assert all(a[i]==common[i] and loc[i]==cl[i] for i in range(1480))
 for j in range(m-1):
  for i in range(400):
   want=common[rev[i]].copy()
   for k,c in qa[i].items():want=plus(want,{1480+400*j+k:F(1),rev[k]:F(-1)},c)
   assert a[1480+400*j+i]==want and loc[1480+400*j+i]==s['final'][rev[i]]
 assert bill['instructions']==71261+(m-1)*(4779+800) and bill['lifetimes']==54+(m-1)*371 and bill['peak']==43
 receipt=json.loads((D/f'm{m}/RESULT.json').read_text());assert json.loads(json.dumps(bill))==receipt['ordinary_bill'];checks[str(m)]={'input_directions':w['public'],'word_sha256':wh,'bill':bill,'endpoint_identity':'common=Ww; copy_j=pi(Ww)+L(v_j-pi(w))'}
# Independent source-bound histogram and exact threshold reconstruction.
full_bytes=(R/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert hashlib.sha256(full_bytes).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7';full=json.loads(full_bytes)
js=(R/'research/shared-core-target-obligations/exact_invoice.js').read_text();v={k:ast.literal_eval(t) for k,t in re.findall(r'const (T|P|H|G|O)=({[^;]*});',js)};T,P,H,G=[v[k] for k in ('T','P','H','G')];assert T=={int(k):n for k,n in full['invoice']['T'].items()} and P=={int(k):n for k,n in full['invoice']['P'].items()}
old=Counter();gactual=Counter();dims=list(map(len,s['frames']))
for e in s['program']:
 if e[0]=='MOVE':(old if e[1] in raw else gactual)[abs(dims[e[3]]-dims[e[2]])]+=1
hactual=Counter(dims[s['final'][i]]-dims[s['initial'][i]] for i in range(1480) if i not in raw);assert dict(gactual)==G and dict(hactual)==H
Q=qbill['moves'];ranks=set(T)|set(P)|set(H)|set(G)|set(old)|set(Q);grid=10**24
def root(n,k):
 a=1<<((n.bit_length()+k-1)//k)
 while True:
  b=((k-1)*a+n//a**(k-1))//k
  if b>=a:break
  a=b
 while (a+1)**k<=n:a+=1
 while a**k>n:a-=1
 return a
pw={r:(F(a,grid),F(a+int(a**200!=r**199*grid**200),grid)) for r in ranks for a in [root(r**199*grid**200,200)]}
def bounds(profile):
 lo=hi=F(0)
 for r,c in profile.items():
  a,b=pw[r];lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
lim=bounds({r:F(T.get(r,0)-P.get(r,0),18)+G.get(r,0)-H.get(r,0) for r in ranks});neg=bounds({r:F(P.get(r,0)-T.get(r,0),18) for r in ranks});excess=bounds({r:Q.get(r,0)-old[r] for r in ranks})
assert all(T.get(r,0)-18*H.get(r,0)>=0 and P.get(r,0)-18*G.get(r,0)+18*(Q.get(r,0)-old[r])>=0 for r in ranks)
for m in (2,3):
 rec=json.loads((D/f'm{m}/RESULT.json').read_text());tm={r:m*T.get(r,0)-18*(m-1)*H.get(r,0) for r in ranks};pm={r:m*P.get(r,0)-18*(m-1)*G.get(r,0)+18*(m-1)*(Q.get(r,0)-old[r]) for r in ranks}
 assert all(tm[r]==rec['T'].get(str(r),0) and pm[r]==rec['P'].get(str(r),0) for r in ranks)
 a,b=bounds({r:tm[r]-pm[r] for r in ranks});a/=18*(m-1);b/=18*(m-1);checks[str(m)]['per_rail_bounds']=[str(a),str(b)];checks[str(m)]['with31_return_bounds']=[str(a-31),str(b-31)]
assert F(checks['2']['with31_return_bounds'][1])<0<F(checks['3']['with31_return_bounds'][0])
out={'status':'PASS_INDEPENDENT_MULTICOPY_RAIL_ENDPOINT_AND_FORMAL_INVOICE_REVIEW','native_sha256':SP,'cyclic_sha256':PP,'pure_rail_sha256':QP,'taint_candidates_exactly_checked':contam,'author_manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),'author_files_authenticated':len(manifest['files']),'rail_rational_rank':len(qb),'six_phase_recipes_replayed':6,'wrong_phase_control_rejected':True,'pure_rail_bill':qbill,'checks':checks,'A_infinity_bounds':list(map(str,lim)),'C_bounds':list(map(str,neg)),'Q_excess_bounds':list(map(str,excess)),'all_m_histogram_slopes_nonnegative':True,'scope':'Source scalar/type endpoint identity and formal caller moment only. L is the actual partial rail map, not the full main target E. Outer/caller admission and all five foundations remain.'}
(O/'MULTICOPY-REVIEW.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
