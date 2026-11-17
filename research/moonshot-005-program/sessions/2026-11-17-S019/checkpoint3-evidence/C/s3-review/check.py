#!/usr/bin/env python3
"""Independent exact review using SymPy QQ(i), without the author engine."""
import argparse,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from sympy import Matrix,I,Rational,expand
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

def need(b,msg):
 if not b:raise ValueError(msg)
def dm(M):return DomainMatrix.from_Matrix(Matrix(M)).convert_to(QQ_I).to_dense()
def ey(n):return DomainMatrix.eye((n,n),QQ_I).to_dense()
def zz(n):return DomainMatrix.zeros((n,n),QQ_I).to_dense()
def add(A,B):return A.add(B)
def sub(A,B):return A.sub(B)
def mul(*xs):
 A=xs[0]
 for B in xs[1:]:A=A.matmul(B)
 return A
def sc(A,c):return A.scalarmul(QQ_I.from_sympy(Rational(c)if isinstance(c,(int,Fraction))else c))
def tr(A):return A.to_Matrix().trace()
def star(A):return dm(A.to_Matrix().conjugate().T)
def pw(A,n):
 if n<0:A=star(A);n=-n
 o=ey(A.shape[0])
 for j in range(n):o=mul(o,A)
 return o
def mono(table):
 n=len(table);need(sorted(x[0]for x in table)==list(range(n)),'monomial permutation');a=Matrix.zeros(n)
 for j,(i,p)in enumerate(table):a[i,j]=I**p
 return dm(a)
def tab(dest,phase):return tuple((dest(*[(x>>j)&1 for j in range(4)]),phase(*[(x>>j)&1 for j in range(4)])%4)for x in range(16))
def compose(a,b):return tuple((a[b[j][0]][0],(b[j][1]+a[b[j][0]][1])%4)for j in range(16))
def blocks_identity():return [[E if i==j else Z for j in range(3)]for i in range(3)]
def same(X,Y):return all(X[i][j]==Y[i][j]for i in range(3)for j in range(3))
def sumdm(xs):
 o=Z
 for x in xs:o=add(o,x)
 return o
def bm(X,Y):return [[sumdm(mul(X[i][k],Y[k][j])for k in range(3))for j in range(3)]for i in range(3)]
def bs(X):return [[star(X[j][i])for j in range(3)]for i in range(3)]
def bcol(col):return [[col[i]if j==0 else Z for j in range(3)]for i in range(3)]
def diag(xs):return [[xs[i]if i==j else Z for j in range(3)]for i in range(3)]
def replay(word,monos):
 X=blocks_identity();bounds=[Fraction(1)]*3;peak=Fraction(1)
 for o in word:
  if o['op']=='ADD':
   d=o['target'];s=o['source'];X[d]=[add(x,y)for x,y in zip(X[d],X[s])];bounds[d]+=bounds[s]
  elif o['op']=='SCALE':
   d=o['bank'];c=Fraction(o['coefficient']);need(c and c.denominator&(c.denominator-1)==0,'nonzero dyadic scale');X[d]=[sc(x,c)for x in X[d]];bounds[d]*=abs(c)
  elif o['op']=='MONO':
   d=o['bank'];X[d]=[mul(monos[o['name']],x)for x in X[d]]
  else:raise ValueError('unknown primitive')
  peak=max(peak,*bounds)
 return X,str(peak)

def literal(M):
 X=M.to_Matrix();out=[]
 for j in range(16):
  nz=[i for i in range(16)if X[i,j]!=0]
  if len(nz)!=1 or X[nz[0],j]not in[1,I,-1,-I]:return None
  out.append([nz[0],[1,I,-1,-I].index(X[nz[0],j])])
 return out if len({x[0]for x in out})==16 else None

def main():
 global E,Z
 from math import comb
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();E=ey(16);Z=zz(16)
 names=['PROOF.md','check.py','RESULT.json','SOURCE-GROUP-TABLES.json'];raw={n:(a.package/n).read_bytes()for n in names};pins={n:hashlib.sha256(b).hexdigest()for n,b in raw.items()};author=json.loads(raw['RESULT.json']);need(pins['PROOF.md']==author['proof_sha256'],'frozen author proof');sourcepins={}
 for p,h in author['source_pins'].items():
  need(hashlib.sha256((a.repo/p).read_bytes()).hexdigest()==h,('retained source pin',p));sourcepins[p]=h
 rot=mono(tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d));R2=mono(tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d)))
 def butterfly(b):return sc(add(sc(E,1+I),sc(mono([(j^(1<<b),0)for j in range(16)]),1-I)),Rational(1,2))
 A=mul(butterfly(1),rot);Ai=star(A);G2=mul(butterfly(0),butterfly(1));need(mul(A,A)==mul(G2,R2)and mul(A,Ai)==E,'literal source square and inverse')
 s=mono(tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0));r=mono(tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0));tau=mono(tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0));need(mul(A,s,Ai)==r and mul(A,r,Ai)==tau and mul(pw(A,2),s,pw(A,-2))==tau,'three conjugate source identities');r3=literal(mul(pw(A,3),r,pw(A,-3)));need(r3 is not None,'fourth ordinary conjugate')
 AM=A.to_Matrix();GM=G2.to_Matrix();supports=[{i for i in range(16)if AM[i,j]!=0}for j in range(16)];need(all(len(v)==2 for v in supports),'source two-point columns');need(all((supports[i]==supports[j])==(i^j==4)for i in range(16)for j in range(i+1,16)),'identical supports iff input differs in c')
 count=Counter();cases=0
 for i in range(16):
  for j in range(i+1,16):
   for phase in range(4):
    v=Matrix.zeros(16,1);v[i]=1;v[j]=I**phase;w=(GM*v).applyfunc(expand);n=sum(x!=0 for x in w);count[n]+=1;cases+=1
    if i//4!=j//4:need(n==8,'different butterfly fibers remain disjoint')
    if n==4:
     ids={k for k,x in enumerate(w)if x!=0};need(len({k//4 for k in ids})==1,'four-support word fills one a,b fiber');need(sum(x!=0 for x in (AM*w).applyfunc(expand))==8,'extra source doubles every surviving coordinate')
 need(cases==480 and dict(count)=={2:48,4:48,8:384},'complete local pair-phase domain')
 # An actual return-coset control, with no Gaussian-rank inference from rank alone.
 bc=mono(tab(lambda a,b,c,d:a+2*c+4*b+8*d,lambda a,b,c,d:0));returning=literal(mul(A,bc,A));need(returning is not None,'actual H return');need(all(literal(mul(A,g,bc,A))is not None for g in [E,s,r,mul(s,r),mul(r,s),mul(s,r,s)]),'G-invariance on an actual H orbit');need(all(sum(x!=0 for x in mul(pw(A,2),bc,A).to_Matrix()[:,j])==2 for j in range(16)),'H yields forbidden rank1 cubic channel')
 perms=list(itertools.permutations(range(3)));idx={p:i for i,p in enumerate(perms)}
 def comp(p,q):return tuple(p[q[j]]for j in range(3))
 def regular(p):
  M=Matrix.zeros(6)
  for q in perms:M[idx[comp(p,q)],idx[q]]=1
  return M
 sg,rg=(1,0,2),(2,1,0);S=regular(sg);R=regular(rg);I6=Matrix.eye(6);Ps=(I6+S)/2;Ms=I6-Ps;Pr=(I6+R)/2;Mr=I6-Pr;Sym=Matrix.ones(6)/6;W=Ps-Sym;zero=Matrix.zeros(6);target=zero.row_join(W)
 def invariant(mask,g):return all(bool(mask>>j&1)==bool(mask>>idx[comp(g,p)]&1)for j,p in enumerate(perms))
 def equations(cm,em):
  X=Pr.row_join(Mr);V=zero.row_join(Ms);Y=zero.row_join(Ps);rows=[]
  for j in range(6):
   if not(cm>>j&1):rows +=[list(X.row(j)),list(V.row(j))]
   if not(em>>j&1):rows +=[list(Y.row(j))]
  return Matrix(rows)if rows else Matrix.zeros(0,12)
 cmasks=[x for x in range(64)if invariant(x,sg)];emasks=[x for x in range(64)if invariant(x,rg)];ncase=0
 for cm in cmasks:
  for em in emasks:
   if cm&em:continue
   Q=equations(cm,em);need(Q.rank()==Q.col_join(target).rank(),'abstract column lemma over every regular-orbit membership pattern');ncase+=1
 need(ncase==18,'complete abstract membership count')
 def counter(cm,em):
  for z in equations(cm,em).nullspace():
   if target*z!=Matrix.zeros(6,1):return {'C_mask':cm,'E_mask':em,'p':[str(x)for x in z[:6]],'z':[str(x)for x in z[6:]],'Wz':[str(x)for x in target*z]}
 negatives={'drop_disjointness':counter(63,63)}
 for cm in cmasks:
  for em in range(64):
   if cm&em or invariant(em,rg):continue
   ex=counter(cm,em)
   if ex:negatives['drop_E_r_invariance']=ex;break
  if 'drop_E_r_invariance'in negatives:break
 need(all(negatives.values())and len(negatives)==2,'two actual abstract counterexamples')
 physical=[E,s,r,mul(s,r),mul(r,s),mul(s,r,s)];need(len({str(g.to_Matrix())for g in physical})==6 and mul(s,r,s)==mul(r,s,r),'literal S3 group');sigma=sc(sumdm(physical),Rational(1,6));WW=sub(sc(add(E,s),Rational(1,2)),sigma);need(mul(WW,WW)==WW and star(WW)==WW and tr(WW)==4,'physical W is a nonzero projector');widths=[]
 for V in [1,2,3,4,8]:
  q=2**V;D=q**4;sym=q*comb(q+2,3);alt=q*comb(q,3);rank=(D+q**3)//2-sym;need(rank==q*q*(q*q-1)//3 and rank>0,'all-width character formula');widths.append({'V':V,'q':q,'D':D,'W':rank,'symmetric':sym,'alternating':alt})
 # A literal six-term nonzero alternating vector at width2 (q=4).
 alt_vector=[]
 for p in perms:
  sign=(-1)**sum(p[i]>p[j]for i in range(3)for j in range(i+1,3));alt_vector.append({'a':p[0],'b':p[1],'c':0,'d':p[2],'coefficient':sign})
 av={(x['a'],x['b'],x['c'],x['d']):x['coefficient']for x in alt_vector}
 need(all(av[(b,a,c,d)]==-v and av[(d,b,c,a)]==-v for(a,b,c,d),v in av.items()),'nonzero width2 alternating control')
 result={'status':'PASS_INDEPENDENT_UNIVERSAL_S3_PENCIL_GATE','author_package_pins':pins,'retained_source_pins':sourcepins,'engine':'Independent SymPy QQ(i) source algebra, rational regular-S3 constraints, and written faithful-coset proof; no author verifier imported','ordinary_A3_Sad_Aminus3':r3,'source_pair_phase_cases':cases,'support_counts':dict(count),'same_A_support_exactly_bit_c_pairs':True,'all48_four_support_cases_expand_to_eight':True,'actual_return_monomial_A_Sbc_A':returning,'regular_orbit_membership_cases':ncase,'abstract_negative_controls':negatives,'all_width_character_samples':widths,'nonzero_width2_alternating_vector':alt_vector,'scope':'The specified B_T R L2 family with a fixed finite ordinary tensor catalogue and classes2/4 only; (0,W)R=0 at faithful widths. General coupled three-bank spectator caller remains unresolved.','no_new_kappa':True}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
