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

# Independent noncommutative polynomial arithmetic: words are tuples;
# the sole reduction is adjacent t*t=t.
def pa(*xs):
 out={}
 for x in xs:
  for w,c in x.items():out[w]=out.get(w,0)+c
 return {w:c for w,c in out.items()if c}
def pn(x):return {w:-c for w,c in x.items()}
def pm(*xs):
 out={():1}
 for x in xs:
  ans={}
  for u,c in out.items():
   for v,d in x.items():
    w=[]
    for s in u+v:
     if s!='t' or not w or w[-1]!='t':w.append(s)
    w=tuple(w);ans[w]=ans.get(w,0)+c*d
  out={w:c for w,c in ans.items()if c}
 return out
def pmat(X,Y):return [[pa(*(pm(X[i][k],Y[k][j])for k in range(len(Y))))for j in range(len(Y[0]))]for i in range(len(X))]
def formal_check():
 o,z={():1},{};a,t=[{(s,):1}for s in['a','t']];n=pa(o,pn(t));a2=pm(a,a);rr=[[{('r'+str(i)+str(j),):1}for j in range(2)]for i in range(2)]
 L=[[a,z,z],[o,a,z],[z,z,o]];U=[[a,pn(a2),z],[z,a,z],[z,z,o]];C=[[t,n,z],[z,o,o],[n,t,z]];Ci=[[t,z,n],[n,z,t],[pn(n),o,pn(t)]];Y=[[o,z,z],[z,o,o],[z,z,o]]
 Q=rr+[[pn(pa(rr[0][j],rr[1][j]))for j in range(2)]];Q=[row+[o if i==2 else z]for i,row in enumerate(Q)]
 B=[[pm(a,t,a),pa(pn(pm(a,t,a2)),pm(a,n,a))],[pm(n,a),pa(pn(pm(n,a2)),pm(t,a))]];ER=pmat(pmat(B,rr),[[a,z],[o,a]])
 lhs=L
 for M in[Q,U,C,L,Y]:lhs=pmat(M,lhs)
 rhs=[[ER[0][0],ER[0][1],z],[z,z,a],[ER[1][0],ER[1][1],z]];need(lhs==rhs,'formal identity');Id=[[o if i==j else z for j in range(3)]for i in range(3)];need(pmat(C,Ci)==Id and pmat(Ci,C)==Id,'formal inverse')
 need(pmat(pmat([[a,z],[z,o]],[[t,n],[n,t]]),[[a,pn(a2)],[z,a]])==B,'formal B factorization');return sum(len(x)for row in rhs for x in row)
def invert_word(word,monos):
 out=[]
 for p in reversed(word):
  if p['op']=='ADD':out.extend([{'op':'SCALE','bank':p['target'],'coefficient':'-1'},dict(p),{'op':'SCALE','bank':p['target'],'coefficient':'-1'}])
  elif p['op']=='SCALE':out.append(dict(p,coefficient=str(1/Fraction(p['coefficient']))))
  else:
   name=p['name']+'_inverse';monos[name]=star(monos[p['name']]);out.append(dict(p,name=name))
 return out

def main():
 global E,Z
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();E=ey(16);Z=zz(16)
 names=['PROOF.md','WORDS.json','GAUSSIAN-GAUGES.json','FORMAL-IDENTITY.json','RESULT.json'];raw={n:(a.package/n).read_bytes()for n in names};pins={n:hashlib.sha256(b).hexdigest()for n,b in raw.items()};author=json.loads(raw['RESULT.json']);need(pins['PROOF.md']==author['proof_sha256'],'author proof pin');source_pins={}
 for p,h in author['source_pins'].items():
  b=(a.repo/p).read_bytes();need(hashlib.sha256(b).hexdigest()==h,('literal source pin',p));source_pins[p]=h
 formal_terms=formal_check();need(formal_terms==28,'formal28 term check')
 rot=mono(tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d));R2=mono(tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d)));Xb=mono([(j^2,0)for j in range(16)]);A=mul(sc(add(sc(E,1+I),sc(Xb,1-I)),Rational(1,2)),rot);A2=pw(A,2);Ai=star(A);need(mul(A,Ai)==E,'source unitarity')
 Ts=mono(tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0));Sab=mono(tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0));Sad=mono(tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0));T=sc(add(E,Ts),Rational(1,2));N=sub(E,T);p1=sc(add(E,Sad),Rational(1,2));m1=sub(E,p1);p2=sc(add(E,Sab),Rational(1,2));m2=sub(E,p2)
 need(mul(Ai,Ts,A)==Sad and mul(pw(A,-2),Ts,A2)==Sab,'source transport identities');need(mul(N,A2)==mul(A2,m2),'bottom kernel transport')
 B=[[mul(A,T,A),add(sc(mul(A,T,A2),-1),mul(A,N,A))],[mul(N,A),add(sc(mul(N,A2),-1),mul(T,A))]];Bexpected=[[mul(A2,p1),add(sc(mul(pw(A,3),p2),-1),mul(A2,m1))],[mul(A,m1),add(sc(mul(A2,m2),-1),mul(A,p1))]];need(B==Bexpected,'all four transported B entries')
 C=[[T,N,Z],[Z,E,E],[N,T,Z]];Ci=[[T,Z,N],[N,Z,T],[sc(N,-1),E,sc(T,-1)]];F=[[E,Z,Z],[Z,E,Z],[sc(E,-1),sc(E,-1),E]];Fi=[[E,Z,Z],[Z,E,Z],[E,E,E]];Y=[[E,Z,Z],[Z,E,E],[Z,Z,E]];Yi=[[E,Z,Z],[Z,E,sc(E,-1)],[Z,Z,E]];Swap=[[E,Z,Z],[Z,Z,E],[Z,E,Z]]
 expected={'C_T':C,'C_T_inverse':Ci,'F':F,'F_inverse':Fi,'Y':Y,'Y_inverse':Yi,'output_swap12':Swap,'output_swap12_inverse':Swap};wd=json.loads(raw['WORDS.json']);monos={k:mono(v)for k,v in wd['monomial_tables'].items()};need(monos=={'Ts':Ts,'S_ab':Sab,'S_ad':Sad},'fresh literal monomial tables');receipts={};negative=0
 for name,want in expected.items():
  word=wd['words'][name];got,bound=replay(word,monos);need(same(got,want),('literal arbitrary-bank action',name));rec={'counts':dict(Counter(x['op']for x in word)),'prefix_bound':bound};need(rec==wd['invoices'][name],('literal price and bound',name));receipts[name]=rec
  for j,p in enumerate(word):
   if p['op']=='ADD':need(not same(replay(word[:j]+word[j+1:],monos)[0],got),('ADD omission rejected',name,j));negative+=1
 for f,g in [('C_T','C_T_inverse'),('F','F_inverse'),('Y','Y_inverse'),('output_swap12','output_swap12_inverse')]:need(same(bm(expected[f],expected[g]),blocks_identity())and same(bm(expected[g],expected[f]),blocks_identity()),('two-sided ordinary inverse',f))
 need(negative==28,'28 omitted ADD controls')
 L=[[A,Z,Z],[E,A,Z],[Z,Z,E]];U=[[A,sc(A2,-1),Z],[Z,A,Z],[Z,Z,E]];controls={};finite_lower_ranks={}
 for name,word in wd['R_control_words'].items():
  R,_=replay(word,monos);Ri,_=replay(invert_word(word,monos),monos);need(same(bm(R,Ri),blocks_identity())and same(bm(Ri,R),blocks_identity()),('actual two-sided R inverse',name));Q,_=replay(word+wd['words']['F'],monos);Qi,_=replay(wd['words']['F_inverse']+invert_word(word,monos),monos);need(same(Q,bm(F,R))and same(bm(Q,Qi),blocks_identity())and same(bm(Qi,Q),blocks_identity()),('Q unit and actual inverse',name))
  B3=[[B[0][0],B[0][1],Z],[B[1][0],B[1][1],Z],[Z,Z,E]];ER=bm(bm(B3,R),L);want=[ER[0],[Z,Z,A],ER[1]];got=bm(bm(bm(bm(bm(Y,L),C),U),Q),L);need(same(got,want),('arbitrary-bank Gaussian1 identity',name));need(any(Q[2][j]!=Z for j in range(2)),'Q retains input-dependent subtraction');controls[name]={'R_and_Q_two_sided_inverse':True,'isolated_exact_A_on_arbitrary_third_input':True}
 Db=mono(tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:b));B2=mul(pw(A,3),Sab,A);gexpected={'A2_R2inv_A':(mul(A2,star(R2),A),1),'A2_R2inv_Db_A':(mul(A2,star(R2),Db,A),2),'A4':(pw(A,4),4),'B2':(B2,2)};gauges=json.loads(raw['GAUSSIAN-GAUGES.json']);need(set(gauges)==set(gexpected),'all gauge heads');targets={}
 for r in [1,2,4]:
  G=E
  for b in range(r):G=mul(G,sc(add(sc(E,1+I),sc(mono([(j^(1<<b),0)for j in range(16)]),1-I)),Rational(1,2)))
  targets[r]=G
 for name,(W,r)in gexpected.items():
  g=gauges[name];need(g['rank']==r and mul(mono(g['left']),targets[r],mono(g['right']))==W,('exact Gaussian gauge with phases',name));need(all(sum(W.to_Matrix()[i,j]!=0 for i in range(16))==2**r for j in range(16)),('exact support channel',name))
 need(mul(N,A2)!=Z and tr(m2)==4,'nonzero annihilating row in pure-cubic gate');need(mul(Sab,Sad,Sab)==mul(Sad,Sab,Sad),'braid relation')
 # Independent S3 character and projector calculations, including a width2 guard.
 group=[E];seen={str(E.to_Matrix())}
 for g in group:
  for h in [Sab,Sad]:
   z=mul(g,h);key=str(z.to_Matrix())
   if key not in seen:seen.add(key);group.append(z)
 need(len(group)==6,'S3 literal order');Sym=sc(sumdm(group),Rational(1,6));W=sub(p2,Sym);need(mul(W,W)==W and star(W)==W and tr(W)==4,'standard-component projector');need(mul(p1,m2)!=Z and mul(m1,p2)!=Z,'opposite eigenspace noncommuting products not zero')
 result={'status':'PASS_INDEPENDENT_TWO_BANK_REDUCTION','author_package_pins':pins,'source_pins':source_pins,'engine':'Fresh formal word arithmetic and independent SymPy QQ(i), no author engine imported','formal_reduced_terms':formal_terms,'literal_receipts':receipts,'actual_R_controls':controls,'ADD_omission_controls_rejected':negative,'exact_phase_preserving_Gaussian_gauges':4,'pure_cubic_gate_nonzero_annihilating_row':True,'S3_projector_W':{'formula':'R2plus-Sym(S3)','rank_all_widths':'q^2(q^2-1)/3, q=2^V','rank_width1':4,'rank_width2':80,'common_minus_dimension_all_widths':'q*binomial(q,3)','common_minus_width1':0,'common_minus_width2':16,'opposite_sign_common_eigenspaces':'zero by braid, all widths'},'scope':'Exact sufficient algebraic reduction and restricted finite-catalogue pure-cubic obstruction. No ordinary R with independent(4,2) endpoints established; finite rank28 searches do not prove universal impossibility.','no_new_kappa':True}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
