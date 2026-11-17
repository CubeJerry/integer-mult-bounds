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

def ga(*xs):
 out={}
 for x in xs:
  for g,c in x.items():out[g]=out.get(g,Fraction(0))+c
 return {g:c for g,c in out.items()if c}
def gc(x,c):return {g:a*c for g,a in x.items()if a*c}
def gm(*xs):
 out={(0,0):Fraction(1)}
 for x in xs:
  nxt={}
  for (k,e),a in out.items():
   for (l,f),b in x.items():
    g=((k+(-1)**e*l)%4,(e+f)%2);nxt[g]=nxt.get(g,Fraction(0))+a*b
  out={g:c for g,c in nxt.items()if c}
 return out
def main():
 global E,Z
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();E=ey(16);Z=zz(16)
 files=['PROOF.md','check.py','output/RESULT.json'];pins={n:hashlib.sha256((a.package/n).read_bytes()).hexdigest()for n in files}
 unit={(0,0):Fraction(1)};f={(0,1):Fraction(1)};t={(3,1):Fraction(1)};z=gm(f,t,f,t);p=gc(ga(unit,f),Fraction(1,2));m=ga(unit,gc(p,-1));T=gc(ga(unit,t),Fraction(1,2));zp=gc(ga(unit,z),Fraction(1,2));zm=ga(unit,gc(zp,-1));ranges=[]
 for q in [p,m]:
  qt=gm(q,T);rr=gm(q,ga(zm,gm(zp,T)));yy=ga(gc(gm(zm,q),2),zp);need(gm(rr,rr)==rr and gm(rr,qt)==qt and gm(qt,yy)==rr,'abstract exact range and both witnesses');ranges.append(rr)
 missing=gm(zp,ga(unit,gc(T,-1)));need(ga(*ranges,missing)==unit and gm(missing,missing)==missing,'abstract missing projector');need(missing==gc(ga(unit,z,gc(t,-1),gc(gm(z,t),-1)),Fraction(1,4)),'exact trace polynomial');need(gm(ranges[0],ranges[1])=={},'orthogonal ranges')
 rot=mono(tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d));R2=mono(tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d)));Xb=mono([(j^2,0)for j in range(16)]);A=mul(sc(add(sc(E,1+I),sc(Xb,1-I)),Rational(1,2)),rot);Ai=star(A);F=mono(tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*a));S=mono(tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0));Ts=mono(tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0));Zc=mono(tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*c));J=mul(star(R2),S,R2);need(mul(J,J)==E and mul(J,F)==mul(F,J),'pinned J conditions')
 def literal(A):
  M=A.to_Matrix();out=[]
  for j in range(16):
   nz=[i for i in range(16)if M[i,j]!=0]
   if len(nz)!=1 or M[nz[0],j]not in[1,I,-1,-I]:return None
   out.append([nz[0],[1,I,-1,-I].index(M[nz[0],j])])
  return out if len(set(x[0]for x in out))==16 else None
 def evalga(coeff,rr):return sumdm(sc(mul(pw(rr,k),pw(F,e)),v)for (k,e),v in coeff.items())
 apps={}
 for name,TT in [('unphased',S),('phase_balanced',mul(S,Zc))]:
  rr=mul(F,TT);need(pw(rr,4)==E,'literal D8 relation');maps={(k,e):mul(pw(rr,k),pw(F,e))for k in range(4)for e in range(2)};need(len({str(x.to_Matrix())for x in maps.values()})==8,'eight literal group matrices');chars={g:int(tr(x))for g,x in maps.items()};outs=[literal(mul(A,TT,Ai)),literal(mul(A,J,TT,J,Ai))];need(all(x is not None for x in outs),'both required ordinary forward conjugates');tabr={}
  for V in [1,2,4,6,8]:
   ranks=[sum(c*chars[g]**V for g,c in q.items())for q in ranges];defect=sum(c*chars[g]**V for g,c in missing.items());need(sum(ranks)+defect==16**V,'collective rank identity');need(defect>0 if V>=2 else defect>=0,'width-sensitive defect');tabr[str(V)]={'row_ranks':[int(x)for x in ranks],'defect':int(defect)}
  if name=='unphased':need(tabr['1']['row_ranks']==[8,8]and tabr['2']['row_ranks']==[112,112],'unphased actual character control')
  else:need(all(tabr[str(V)]['row_ranks']==[3*16**V//8]*2 for V in[1,2,4,6,8]),'regular case specialization')
  apps[name]={'group_traces':{str(g):v for g,v in chars.items()},'forward_conjugates':outs,'collective_ranks':tabr}
 need(literal(mul(A,Ts,Ai))is None and literal(mul(A,J,Ts,J,Ai))is None,'spectator outside conjugate hypothesis');need(16**6-2*14**6==1718144,'uniform even-width lower numerator')
 result={'status':'PASS_INDEPENDENT_NONREGULAR_DIHEDRAL_RANGE','package_pins':pins,'engine':'Independent exact rational D8 group arithmetic and SymPy QQ(i), no root or author checker imported','abstract_projectors_and_range_witnesses':True,'missing_dimension_formula':'(d^V+tr(z)^V-tr(t)^V-tr(zt)^V)/4','nonscalar_trace_bound':'both t and zt have |trace|<=d-2','uniform_d16_V6_defect_lower_bound':429536,'source_applications':apps,'spectator_scope_control':True,'scalar_even_width_defect_control':0,'scope':'All sufficiently large even widths under fixed finite catalogue and both ordinary forward-conjugate premises; no full supplier or new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
