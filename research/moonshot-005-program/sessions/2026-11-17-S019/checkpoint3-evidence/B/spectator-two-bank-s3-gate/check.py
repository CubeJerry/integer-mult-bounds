#!/usr/bin/env python3
"""Exact local/group controls for the universal spectator S3 gate; the universal proof is PROOF.md."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,importlib.util,sys,json,hashlib,random,itertools
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();args.out.mkdir(parents=True,exist_ok=True)
engine=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
spec=importlib.util.spec_from_file_location('fixed_gaussian_dyadic_arithmetic',engine);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
I=m.eye(16);Z=m.zero(16);I3=m.eye(48)
def neg(M):return M.scale((-1,0))
def half(M):return m.M(M.a,M.k+1).norm()
def tab(dest,phase):return m.monomial([dest(*[(x>>j)&1 for j in range(4)])for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
rot=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
Xb=m.monomial([x^2 for x in range(16)],[0]*16)
A=half(I.scale((1,1))+Xb.scale((1,-1)))@rot
R2=tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
S=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
J=R2.star()@S@R2
F=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*a)
Fh=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*d)
G=tab(lambda a,b,c,d:a+2*b+4*c+8*(d^1),lambda a,b,c,d:0)
Kd=tab(lambda a,b,c,d:a+2*(b^(a*d))+4*(c^(a*d))+8*d,lambda a,b,c,d:2*a*d)
B2=A.power(3)@S@A
assert A@F@A.star()==Fh and J@F==F@J and Kd@Fh==Fh@Kd
assert A@J@A.power(3)==Kd@B2
assert A@J@A.power(2)@S@A==Kd@A.power(4)
assert G@Fh==neg(Fh@G)
for x in (F,Fh,G,J,S,Kd):assert x@x==I
roots=((1,0),(0,1),(-1,0),(0,-1))
def mono_table(X):
 assert X.k==0
 out=[]
 for j in range(X.n):
  rs=[i for i in range(X.n)if X.a[i][j]!=m.Z];assert len(rs)==1
  out.append([rs[0],roots.index(X.a[rs[0]][j])])
 return out
# Exact constructive Gaussian gauges, including rank3 prefixes.
def gauges(X,r):
 size=1<<r;groups={}
 for i,row in enumerate(X.a):groups.setdefault(tuple(j for j,z in enumerate(row)if z!=m.Z),[]).append(i)
 assert len(groups)==16//size
 target=I
 for bit in range(r):
  xb=m.monomial([x^(1<<bit)for x in range(16)],[0]*16)
  target=target@half(I.scale((1,1))+xb.scale((1,-1)))
 assert X.k==target.k
 base=target.a[0][0]
 def phase(z):return next(k for k,u in enumerate(roots)if m.gm(base,u)==z)
 ld=[None]*16;lp=[None]*16;rd=[None]*16;rp0=[None]*16
 for block,(cols,rows)in enumerate(sorted(groups.items())):
  assert len(cols)==len(rows)==size
  es=[[phase(X.a[i][j])for j in cols]for i in rows]
  rp=[es[i][0]for i in range(size)];cp=[(es[0][j]-es[0][0])%4 for j in range(size)]
  masks=[]
  for i in range(size):
   dd=[(es[i][j]-rp[i]-cp[j])%4 for j in range(size)];assert all(z in(0,2)for z in dd)
   masks.append(sum((z//2)<<j for j,z in enumerate(dd)))
  basis=[];span={0:0}
  for z in masks:
   if z not in span:
    bit=1<<len(basis);basis.append(z);span.update({x^z:c|bit for x,c in list(span.items())})
  assert len(basis)==r and set(masks)==set(span)
  ri=[span[z]for z in masks];ci=[sum(((basis[k]>>j)&1)<<k for k in range(r))for j in range(size)];assert sorted(ci)==list(range(size))
  for i,row in enumerate(rows):ld[block*size+ri[i]]=row;lp[block*size+ri[i]]=(rp[i]+ri[i].bit_count())%4
  for j,col in enumerate(cols):rd[col]=block*size+ci[j];rp0[col]=(cp[j]+ci[j].bit_count())%4
 L=m.monomial(ld,lp);R=m.monomial(rd,rp0);assert L@target@R==X
 return {'rank':r,'left':mono_table(L),'right':mono_table(R)}
def add(s,t):return {'op':'ADD','source':s,'target':t}
def scale(b,c):return {'op':'SCALE','bank':b,'coefficient':str(Fraction(c))}
def mon(b,n):return {'op':'MONO','bank':b,'name':n}
def h2(i,j):return [add(j,i),scale(j,-2),add(i,j)]
def h2inv(i,j):return h2(i,j)+[scale(i,Fraction(1,2)),scale(j,Fraction(1,2))]
def route_minus(i,j,n):return h2(i,j)+[mon(j,n)]+h2inv(i,j)
def route_plus(i,j,n):return h2(i,j)+[mon(j,n),scale(j,-1)]+h2inv(i,j)
def swap(i,j):return [add(i,j),scale(j,-1),add(j,i),scale(j,-1),add(i,j),scale(i,-1)]
def replay(word):
 X=I3;bounds=[Fraction(1)]*3;mx=Fraction(1)
 for op in word:
  blocks=[[I if r==c else Z for c in range(3)]for r in range(3)]
  if op['op']=='ADD':blocks[op['target']][op['source']]=I;bounds[op['target']]+=bounds[op['source']]
  elif op['op']=='MONO':blocks[op['bank']][op['bank']]=monos[op['name']]
  else:
   c=Fraction(op['coefficient']);blocks[op['bank']][op['bank']]=m.M(I.scale((c.numerator,0)).a,c.denominator.bit_length()-1).norm();bounds[op['bank']]*=abs(c)
  X=m.block(blocks)@X;mx=max(mx,*bounds)
 return X,str(mx)


Ts=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
r=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);s=S
assert A@s@A.star()==r and A@r@A.star()==Ts and A.power(2)@s@A.power(-2)==Ts
Hr3=A.power(3)@r@A.power(-3);mono_table(Hr3)
assert Hr3@Hr3==I and Hr3.trace()==(8,0)
# Local support statement covers every possible ordinary monomial, including nonlinear ones.
col_support=[frozenset(i for i in range(16)if A.a[i][j]!=m.Z)for j in range(16)]
assert all(len(x)==2 for x in col_support)
for j,k in itertools.combinations(range(16),2):
 assert (col_support[j]==col_support[k])==(j^k==4)
 assert (not(col_support[j]&col_support[k]))==(j^k!=4)
Xa=m.monomial([x^1 for x in range(16)],[0]*16);Xb=m.monomial([x^2 for x in range(16)],[0]*16)
Ca=half(I.scale((1,1))+Xa.scale((1,-1)));Cb=half(I.scale((1,1))+Xb.scale((1,-1)));C2=Ca@Cb
assert A.power(2)==C2@R2
pair_cases=four_cases=eight_cases=two_cases=0
for j,k in itertools.combinations(range(16),2):
 for omega in roots:
  vec=[m.ga(m.gm(C2.a[i][j],(1,1)),m.gm(m.gm(C2.a[i][k],(1,-1)),omega))for i in range(16)]
  supp=[i for i,z in enumerate(vec)if z!=m.Z];pair_cases+=1
  if j//4 != k//4:assert len(supp)==8;eight_cases+=1
  elif len(supp)==4:
   assert len({i//4 for i in supp})==1;four_cases+=1
   vv=[m.Z]*16
   for i in range(16):
    for l in supp:vv[i]=m.ga(vv[i],m.gm(A.a[i][l],vec[l]))
   assert sum(z!=m.Z for z in vv)==8
  else:assert len(supp)==2;two_cases+=1
assert pair_cases==480 and four_cases and two_cases
GG=[I];seen={I}
for h in GG:
 for g in (s,r):
  w=g@h
  if w not in seen:seen.add(w);GG.append(w)
assert len(GG)==6
idx={g:i for i,g in enumerate(GG)}
Ls=[[Fraction(int(g==s@h))for h in GG]for g in GG];Lr=[[Fraction(int(g==r@h))for h in GG]for g in GG]
def madd(X,Y):return[[x+y for x,y in zip(a,b)]for a,b in zip(X,Y)]
def mscale(X,c):return[[c*x for x in row]for row in X]
def mulq(X,Y):return[[sum(a*b for a,b in zip(row,col))for col in zip(*Y)]for row in X]
Id6=[[Fraction(int(i==j))for j in range(6)]for i in range(6)]
Ps=mscale(madd(Id6,Ls),Fraction(1,2));Ms=madd(Id6,mscale(Ps,-1));Pr=mscale(madd(Id6,Lr),Fraction(1,2));Mr=madd(Id6,mscale(Pr,-1));Sig=[[Fraction(1,6)]*6 for _ in range(6)];WW=madd(Ps,mscale(Sig,-1))
assert mulq(WW,WW)==WW and mulq(Sig,Sig)==Sig
# All possible C/E memberships on one free left S3 coefficient orbit.
def invariant(mask,gen):return all(bool(mask>>j&1)==bool(mask>>idx[gen@g]&1)for j,g in enumerate(GG))
def rref(rows):
 piv={}
 for rr in rows:
  rr=[Fraction(x)for x in rr]
  for j,row in sorted(piv.items()):
   if rr[j]:
    f=rr[j];rr=[x-f*y for x,y in zip(rr,row)]
  j=next((j for j,x in enumerate(rr)if x),None)
  if j is None:continue
  f=rr[j];rr=[x/f for x in rr]
  for i,row in list(piv.items()):
   if row[j]:
    f=row[j];piv[i]=[x-f*y for x,y in zip(row,rr)]
  piv[j]=rr
 return piv

def reduce_row(row,piv):
 row=[Fraction(x)for x in row]
 for j,rr in sorted(piv.items()):
  if row[j]:
   f=row[j];row=[x-f*y for x,y in zip(row,rr)]
 return row

def constraints(cm,em):
 rows=[]
 for i in range(6):
  if not(cm>>i&1):rows.append(Pr[i]+Mr[i]);rows.append([Fraction(0)]*6+Ms[i])
  if not(em>>i&1):rows.append([Fraction(0)]*6+Ps[i])
 return rows

cases=0
for cm in range(64):
 if not invariant(cm,s):continue
 for em in range(64):
  if not invariant(em,r)or cm&em:continue
  piv=rref(constraints(cm,em));assert all(not any(reduce_row([0]*6+row,piv))for row in WW);cases+=1

def witness(cm,em):
 piv=rref(constraints(cm,em));free=[j for j in range(12)if j not in piv]
 for j in free:
  v=[Fraction(0)]*12;v[j]=1
  for k,row in piv.items():v[k]=-row[j]
  wz=[sum(WW[i][j]*v[6+j]for j in range(6))for i in range(6)]
  if any(wz):return {'C_mask':cm,'E_mask':em,'p':[str(x)for x in v[:6]],'z':[str(x)for x in v[6:]],'Wz':[str(x)for x in wz]}
 return None
controls={}
for name,pred in [('drop_E_r_invariance',lambda c,e:invariant(c,s)and not invariant(e,r)and not(c&e)),('drop_disjointness',lambda c,e:invariant(c,s)and invariant(e,r)and bool(c&e))]:
 found=None
 for cm in range(64):
  for em in range(64):
   if pred(cm,em):
    found=witness(cm,em)
    if found:break
  if found:break
 assert found is not None;controls[name]=found
# Exact all-width trace formulas; the alternating sector must not be discarded.
signs={I:1};todo=[I]
for h in todo:
 for g in (s,r):
  w=g@h
  if w not in signs:signs[w]=-signs[h];todo.append(w)
  else:assert signs[w]==-signs[h]
trace_cases=[]
for V in (1,2,3,4,8):
 q=2**V;D=q**4
 tr_sig=sum(g.trace()[0]**V for g in GG)//6;tr_ps=(D+s.trace()[0]**V)//2
 expected=q*q*(q*q-1)//3
 assert tr_ps-tr_sig==expected and tr_sig==q*q*(q+2)*(q+1)//6
 tr_alt=sum(signs[g]*g.trace()[0]**V for g in GG)//6
 assert tr_alt==q*q*(q-1)*(q-2)//6
 trace_cases.append({'V':V,'q':q,'D':D,'rank_W':expected,'rank_symmetric':tr_sig,'rank_alternating':tr_alt})
assert trace_cases[0]['rank_alternating']==0 and trace_cases[1]['rank_alternating']==16
result={'status':'PASS_UNIVERSAL_SPECTATOR_S3_GATE_CONTROLS','scope':'Universal written source-coset proof of (0,W)R=0 for all fixed finite ordinary catalogues when B_T R L2 has only Gaussian2/4 classes; exact source/local/group controls, no inference from failed caller searches.',
 'literal_source_identities':4,'all_two_point_phase_patterns':pair_cases,'four_point_fiber_cases':four_cases,'two_support_cases':two_cases,'eight_support_cases':eight_cases,'abstract_S3_membership_cases_exhausted':cases,'abstract_negative_controls':controls,'all_width_trace_cases':trace_cases,'alternating_sector_retained':True,
 'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'source_pins':{str(engine.relative_to(repo)):hashlib.sha256(engine.read_bytes()).hexdigest(),'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md':hashlib.sha256((repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md').read_bytes()).hexdigest()},'supersedes':'Feasibility of the simplified C_T/Q_R rank1-isolating reduction only; its algebraic identity/receipts remain valid. General three-bank two-kernel caller remains open.','no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(args.out/'SOURCE-GROUP-TABLES.json').write_text(json.dumps({'monomials':{'S_ab':mono_table(s),'S_ad':mono_table(r),'S_cd':mono_table(Ts),'A3_Sad_Aminus3':mono_table(Hr3)},'S3_group':[mono_table(g)for g in GG],'S3_traces':[g.trace()for g in GG],'A_column_supports':[sorted(x)for x in col_support]},indent=2)+'\n')
print(json.dumps({'status':result['status'],'local_cases':pair_cases,'abstract_S3_cases':cases,'negative_controls':len(controls),'W_ranks':[x['rank_W']for x in trace_cases[:3]],'alternating_rank_V2':trace_cases[1]['rank_alternating']},indent=2))
