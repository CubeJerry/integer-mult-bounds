#!/usr/bin/env python3
"""Exact controls for the ordinary-character gate; the universal proof is PROOF.md."""
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

P=half(I+F);M=half(I+neg(F));Ph=half(I+Fh);Mh=half(I+neg(Fh))
Zc=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*c)
Pi=m.diagonal([Mh,Ph,Z]);O=m.block([[Mh,Ph,Z],[Ph,Mh,Z],[Z,Z,I]])
assert O@Pi@O==m.diagonal([I,Z,Z]) and O@O==I3
Cold=m.block([[M,P,Z],[J@P,J@M,Z],[Z,Z,I]])
Qseed=m.block([[Z,I,Z],[I,Z,Z],[Z,Z,I]])
Kold=m.block([[A@M@A,Z,Z],[A@J@P@A,Z,Z],[Z,Z,Z]])
assert Kold.star()@Kold==m.diagonal([I,Z,Z])
all_words={};all_invoices={};case_results={};all_gauges={};omitted=0
for case,T0 in [('failed_JZa',J@F),('surviving_SZc',S@Zc)]:
 T=half(I+T0);N=half(I+neg(T0));assert T0@T0==I and T0.trace()==(0,0) and T@T==T and T.trace()==(8,0)
 Rt=m.block([[T,Z,N],[Z,I,Z],[N,Z,T]])
 Cn=Cold@Rt;assert Cn==m.block([[M@T,P,M@N],[J@P@T,J@M,J@P@N],[N,Z,T]])
 K=m.block([[A@M@T@A,Z,Z],[A@J@P@T@A,Z,Z],[Z,Z,Z]])
 assert Pi@K==K
 B=A@(M+J@P)@T@A
 assert O@K==m.block([[B,Z,Z],[Z,Z,Z],[Z,Z,Z]])
 assert K.star()@K==m.diagonal([A.star()@T@A,Z,Z])
 H0=A.star()@T0@A;H2=A.power(-2)@T0@A.power(2)
 def nonmono_witness(X):
  j=next(j for j in range(16)if sum(X.a[i][j]!=m.Z for i in range(16))>1)
  return {'column':j,'nonzero_entries':sum(X.a[i][j]!=m.Z for i in range(16))}
 record={'rank_K_fraction':'1/2','rank_Pi_fraction':'1','all_width_free_range':True,'H0_nonmonomial':nonmono_witness(H0)}
 if case=='failed_JZa':
  record['H2_nonmonomial']=nonmono_witness(H2)
  assert J@P@T==P@T and B==A@T@A
  H=Fh@Kd;assert A@T@A.power(3)==half(A.power(4)+H@B2)
  W=m.block([[neg(A@M@T@A.power(3)),Z,Z],[neg(A@J@P@T@A.power(3)),Z,Z],[Z,Z,Z]])
  E4=m.diagonal([neg(half(A.power(4))),Z,Z]);E2=m.diagonal([neg(half(H@B2)),Z,Z]);assert O@W==E4+E2
  quarterI=m.M(I.a,2).norm();assert E4@E4.star()==m.diagonal([quarterI,Z,Z]) and E2@E2.star()==m.diagonal([quarterI,Z,Z])
  record['component_control']='Full-D ordinarily aligned rank4/rank2 components, total rankD/2; source-column family nevertheless excluded by ordinary-kernel lemma.'
 else:
  assert H2==J@F and H2@H2==I
  H2p=half(I+H2);H2m=half(I+neg(H2));assert H2m@H2m==H2m and H2m.trace()==(8,0)
  assert B@A@H2m==Z and B@H2m!=Z
  record['H2_table']=mono_table(H2);record['actual_nonzero_ordinary_Ka_kernel_rank_fraction']='1/2';record['K_does_not_annihilate_that_control']=True
  record['next_interface']='q12 must be nonzero and q12=(I-(JZa)^tensor V)/2 q12'
 source_words=[('A2',A.power(2),2),('AJA',A@J@A,2),('A3',A.power(3),3),('AJA2',A@J@A.power(2),3),('AT0A',A@T0@A,2),('AJT0A',A@J@T0@A,2),('AT0A2',A@T0@A.power(2),3),('AJT0A2',A@J@T0@A.power(2),3)]
 if case=='surviving_SZc':source_words.append(('H0',H0,2))
 all_gauges[case]={name:gauges(X,r)for name,X,r in source_words}
 monos={'F':F,'Fhat':Fh,'J':J,'T0':T0,'S':S,'Kdec':Kd}
 words={'C_new':route_minus(0,2,'T0')+route_plus(0,1,'F')+[mon(1,'J')],'C_new_inverse':[mon(1,'J')]+route_plus(0,1,'F')+route_minus(0,2,'T0'),'Q_seed':swap(0,1),'Q_seed_inverse':swap(0,1),'O':route_plus(0,1,'Fhat'),'O_inverse':route_plus(0,1,'Fhat')}
 expected={'C_new':Cn,'Q_seed':Qseed,'O':O};stats={}
 for name in expected:
  X,b=replay(words[name]);Xi,bi=replay(words[name+'_inverse']);assert X==expected[name] and X@Xi==I3 and Xi@X==I3
  for nm in (name,name+'_inverse'):
   X,b=replay(words[nm]);stats[nm]={'counts':dict(Counter(x['op']for x in words[nm])),'prefix_bound':b}
   for j,x in enumerate(words[nm]):
    if x['op']=='ADD':assert replay(words[nm][:j]+words[nm][j+1:])[0]!=X;omitted+=1
 all_words[case]={'monomial_tables':{n:mono_table(x)for n,x in monos.items()},'words':words};all_invoices[case]=stats;case_results[case]=record
(args.out/'WORDS.json').write_text(json.dumps({'cases':all_words,'invoices':all_invoices},indent=2)+'\n')
(args.out/'GAUSSIAN-GAUGES.json').write_text(json.dumps(all_gauges,indent=2)+'\n')
result={'status':'PASS_CORRECT_CHARACTER_AND_ORDINARY_KERNEL_BRIDGE','scope':'Actual all-width C_new/free ambient ranges, singular K, a universal ordinary-kernel exclusion for JZa, and an explicit nonzero kernel interface for SZc. No full421 caller.','cases':case_results,'proof_basis':'Written faithful finite-word kernel separation and source transport proof; not numerical nullspace inference.','invoices':all_invoices,'omitted_ADD_negative_controls':omitted,'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'source_pins':{str(engine.relative_to(repo)):hashlib.sha256(engine.read_bytes()).hexdigest(),'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md':hashlib.sha256((repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md').read_bytes()).hexdigest()},'remaining':'Choose q12 through the actual nonzero SZc kernel, complete ordinary Q and C, cancel residue, preserve independent21, and pay full caller/source costs.','no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'negative_controls':omitted,'cases':case_results},indent=2))
