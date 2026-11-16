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
P=half(I+F);M=half(I+neg(F));Ph=half(I+Fh);Mh=half(I+neg(Fh))
assert P@P==P and Ph@Ph==Ph and Ph.trace()==(8,0)
C=m.block([[P,Z,M],[J@P,I,J@M],[M,Z,P]])
Q=m.block([[Z,I,Z],[I,S,Z],[Z,Z,I]])
D=m.diagonal([I,Kd,I])
Rph=m.block([[Mh,Ph,Z],[Ph,Mh,Z],[Z,Z,I]])
Odd=Rph@m.diagonal([I,G,I])
Pi=m.diagonal([Ph,Ph,Z])
K=m.block([[A@P@A,Z,Z],[A@J@P@A,Z,Z],[Z,Z,Z]])
assert Pi@K==K and Pi@Pi==Pi and Pi.trace()==(16,0)
assert K.star()@K==m.diagonal([(A.star()@P@A).scale((2,0)),Z,Z])
W=m.block([[neg(A@P@A.power(3)),neg(A@P@A.power(2)@S@A),Z],[neg(A@J@P@A.power(3)),neg(A@J@P@A.power(2)@S@A),Z],[Z,Z,Z]])
Wn=m.block([[neg(Ph@A.power(4)),neg(Ph@B2),Z],[neg(Ph@B2),neg(Ph@A.power(4)),Z],[Z,Z,Z]])
assert D@W==Wn
E4=m.diagonal([neg(Ph@A.power(4)),neg(Ph@A.power(4)),Z])
E2=m.block([[Z,neg(Ph@B2),Z],[neg(Ph@B2),Z,Z],[Z,Z,Z]])
assert Wn==E4+E2
assert E4@E4.star()==Pi and E2@E2.star()==Pi
assert W@W.star()==(K@K.star()).scale((2,0))
assert Odd@Pi@Odd.star()==m.diagonal([Z,I,Z])
# Exact Gaussian gauges for a rank-r source, using normalized character blocks.
roots=((1,0),(0,1),(-1,0),(0,-1))
def phase(z):return roots.index(z)
def mono_table(X):
 assert X.k==0
 out=[]
 for j in range(X.n):
  rs=[i for i in range(X.n)if X.a[i][j]!=m.Z];assert len(rs)==1
  out.append([rs[0],phase(X.a[rs[0]][j])])
 return out

def even_gauges(X,r):
 assert r in (2,4) and X.k==r//2
 size=1<<r;groups={}
 for i,row in enumerate(X.a):groups.setdefault(tuple(j for j,z in enumerate(row)if z!=m.Z),[]).append(i)
 assert len(groups)==16//size
 Ldest=[None]*16;Lphase=[None]*16;Rdest=[None]*16;Rphase=[None]*16
 for block,(cols,rows)in enumerate(sorted(groups.items())):
  assert len(cols)==len(rows)==size
  es=[[phase(X.a[i][j])for j in cols]for i in rows]
  rp=[es[i][0]for i in range(size)];cp=[(es[0][j]-es[0][0])%4 for j in range(size)]
  masks=[]
  for i in range(size):
   dd=[(es[i][j]-rp[i]-cp[j])%4 for j in range(size)];assert all(x in(0,2)for x in dd)
   masks.append(sum((x//2)<<j for j,x in enumerate(dd)))
  basis=[];span={0:0}
  for x in masks:
   if x not in span:
    bit=1<<len(basis);basis.append(x);span.update({z^x:c|bit for z,c in list(span.items())})
  assert len(basis)==r and set(masks)==set(span)
  rid=[span[x]for x in masks];cid=[sum(((basis[k]>>j)&1)<<k for k in range(r))for j in range(size)];assert sorted(cid)==list(range(size))
  for i,row in enumerate(rows):Ldest[block*size+rid[i]]=row;Lphase[block*size+rid[i]]=(rp[i]-r//2+rid[i].bit_count())%4
  for j,col in enumerate(cols):Rdest[col]=block*size+cid[j];Rphase[col]=(cp[j]+cid[j].bit_count())%4
 L=m.monomial(Ldest,Lphase);R=m.monomial(Rdest,Rphase);target=I
 for bit in range(r):
  Xbit=m.monomial([x^(1<<bit)for x in range(16)],[0]*16)
  target=target@half(I.scale((1,1))+Xbit.scale((1,-1)))
 assert L@target@R==X
 return {'rank':r,'left':mono_table(L),'right':mono_table(R),'exact_Gaussian_character_structure':True}
gauges={'A4':even_gauges(A.power(4),4),'B2':even_gauges(B2,2)}
# Generic root-four fixed-vector controls, represented sparsely on the diagonal tensors.
def fixes_diagonal_tensor(table,width):return all((width*phase)%4==0 for _,phase in table) and sorted(dest for dest,_ in table)==list(range(len(table)))
monos={'F':F,'Fhat':Fh,'J':J,'S':S,'Kdec':Kd,'G':G}
random_controls=0;rng=random.Random(202611170019)
for _ in range(40):
 perm=list(range(16));rng.shuffle(perm);ph=[rng.randrange(4)for _ in range(16)]
 assert fixes_diagonal_tensor(list(zip(perm,ph)),4);random_controls+=1
for x in monos.values():assert fixes_diagonal_tensor(mono_table(x),4)
assert not fixes_diagonal_tensor(mono_table(F),1)
# If the declared alphabet were enlarged to eighth roots, width4 would fail.
assert (4*1)%8!=0
# Chronological actual primitive words.
def add(s,t):return {'op':'ADD','source':s,'target':t}
def scale(b,c):return {'op':'SCALE','bank':b,'coefficient':str(Fraction(c))}
def mon(b,n):return {'op':'MONO','bank':b,'name':n}
def h2(i,j):return [add(j,i),scale(j,-2),add(i,j)]
def h2inv(i,j):return h2(i,j)+[scale(i,Fraction(1,2)),scale(j,Fraction(1,2))]
def route_minus(i,j,n):return h2(i,j)+[mon(j,n)]+h2inv(i,j)
def route_plus(i,j,n):return h2(i,j)+[mon(j,n),scale(j,-1)]+h2inv(i,j)
def shear(i,j,n,negative=False):return [mon(j,n)]+([scale(j,-1)]if negative else[])+[add(j,i)]+([scale(j,-1)]if negative else[])+[mon(j,n)]
def swap(i,j):return [add(i,j),scale(j,-1),add(j,i),scale(j,-1),add(i,j),scale(i,-1)]
words={'C':route_minus(0,2,'F')+shear(1,0,'J'),'C_inverse':shear(1,0,'J',True)+route_minus(0,2,'F'),'Q':swap(0,1)+shear(1,0,'S'),'Q_inverse':shear(1,0,'S',True)+swap(0,1),'D': [mon(1,'Kdec')],'D_inverse':[mon(1,'Kdec')],'O_odd':[mon(1,'G')]+route_plus(0,1,'Fhat'),'O_odd_inverse':route_plus(0,1,'Fhat')+[mon(1,'G')]}
def replay(word):
 X=I3;bounds=[Fraction(1)]*3;mx=Fraction(1)
 for op in word:
  blocks=[[I if r==c else Z for c in range(3)]for r in range(3)]
  if op['op']=='ADD':
   blocks[op['target']][op['source']]=I;bounds[op['target']]+=bounds[op['source']]
  elif op['op']=='MONO':blocks[op['bank']][op['bank']]=monos[op['name']]
  else:
   f=Fraction(op['coefficient']);assert f.denominator&(f.denominator-1)==0
   blocks[op['bank']][op['bank']]=m.M(I.scale((f.numerator,0)).a,f.denominator.bit_length()-1).norm();bounds[op['bank']]*=abs(f)
  X=m.block(blocks)@X;mx=max(mx,*bounds)
 return X,str(mx)
expected={'C':C,'Q':Q,'D':D,'O_odd':Odd};stats={};neg_count=0
for name in ('C','Q','D','O_odd'):
 W0,norm=replay(words[name]);Winv,normi=replay(words[name+'_inverse']);assert W0==expected[name] and W0@Winv==I3 and Winv@W0==I3
 for tag in (name,name+'_inverse'):
  full,bound=replay(words[tag]);count=Counter(op['op']for op in words[tag]);stats[tag]={'counts':dict(count),'max_bank_row_sum_prefix_bound':bound}
  for j,op in enumerate(words[tag]):
   if op['op']=='ADD':assert replay(words[tag][:j]+words[tag][j+1:])[0]!=full;neg_count+=1
word_data={'scope':'Exact component controls only. All bank data retained; no extra owner. External scalar coefficients are not per-column phases.','monomial_tables':{n:mono_table(x)for n,x in monos.items()},'words':words,'invoices_and_prefix_bounds':stats}
(args.out/'WORDS.json').write_text(json.dumps(word_data,indent=2)+'\n')
(args.out/'GAUSSIAN-GAUGES.json').write_text(json.dumps(gauges,indent=2)+'\n')
deps=[engine,repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md',repo/'research/moonshot-005-program/results/complex-inverse-native-coset/two-native/PROOF.md',repo/'research/moonshot-005-program/results/complex-noncommuting-ordinary-compiler/ADMISSION.md']
result={'status':'PASS_ORDINARY_CHARACTER_GATE_SOURCE_AND_CONTROLS','theorem':'For fixed literal root-four ordinary templates, the first column C00=P,C10=JP cannot yield uniform independent421; exclusion at all sufficiently large V divisible by4.','universal_basis':'Written fixed-vector, invariant-subspace, character-rank and faithful finite-word proof; controls do not replace it.','source_prefix_rank_fraction':'1/2','ambient_projector_rank_fraction':'1','ambient_projector_augmentation_rank':2,'required_one_job_augmentation_rank':1,'quartic_component_rank_fractions':{'rank4':'1','rank2_residue':'1','total':'1/2'},'odd_width_decoder':'Exact all-odd-width algebra from GFhat=-FhatG; no all-width extension and no complete caller claimed','random_literal_fixed_vector_controls':random_controls,'single_ADD_omission_controls':neg_count,'invoices':stats,'source_pins':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in deps},'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'next':'Singular prefix with correct ordinary character multiplicities or larger ordinary ambient range; complementary old injective route is already excluded.','no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'negative_controls':neg_count,'invoices':stats},indent=2))
