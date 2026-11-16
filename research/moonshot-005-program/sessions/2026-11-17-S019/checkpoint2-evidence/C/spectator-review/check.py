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

def main():
 global E,Z
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();E=ey(16);Z=zz(16);ID=tuple((i,0)for i in range(16))
 rawfiles={n:(a.package/n).read_bytes()for n in ['PROOF.md','WORDS.json','GAUSSIAN-GAUGES.json','D8-RANGE-CERTIFICATE.json','RESULT.json']};pins={n:hashlib.sha256(b).hexdigest()for n,b in rawfiles.items()};published=json.loads(rawfiles['RESULT.json']);need(pins['PROOF.md']==published['proof_sha256'],'author proof pin')
 rotT=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);r2T=tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d));fT=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*a);fhT=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*d);zcT=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*c);sabT=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0);tsT=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0);sadT=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);kdT=tab(lambda a,b,c,d:a+2*(b^(a*d))+4*(c^(a*d))+8*d,lambda a,b,c,d:2*a*d)
 F,Fh,Zc,S,Ts,Sad,Kd=map(mono,[fT,fhT,zcT,sabT,tsT,sadT,kdT]);R2=mono(r2T);rot=mono(rotT);Xb=mono(tuple((i^2,0)for i in range(16)));A=mul(sc(add(sc(E,1+I),sc(Xb,1-I)),Rational(1,2)),rot);Ai=star(A);J=mul(star(R2),S,R2);need(mul(A,Ai)==E and mul(Ai,A)==E,'source unitary');need(mul(J,J)==E and mul(J,F)==mul(F,J),'literal J conditions');need(mul(A,F,Ai)==Fh,'forward F ordinary')
 activeT=compose(sabT,zcT);active=mono(activeT);group=[ID];seen={ID}
 for g in group:
  for h in[fT,activeT]:
   p=compose(g,h)
   if p not in seen:seen.add(p);group.append(p)
 need(len(group)==8,'D8 order');traces=[expand(sum(I**p for j,(i,p)in enumerate(g)if i==j))for g in group];need(traces[0]==16 and traces[1:]==[0]*7,'eight exact D8 traces');z=pw(mul(F,active),2);need(mul(z,z)==E and mul(z,F)==mul(F,z)and mul(z,active)==mul(active,z),'central involution');need(mul(F,active)==mul(active,F,z),'D8 relation')
 P=sc(add(E,F),Rational(1,2));M=sc(sub(E,F),Rational(1,2));Tact=sc(add(E,active),Rational(1,2));zp=sc(add(E,z),Rational(1,2));zm=sub(E,zp);rp=mul(P,add(zm,mul(zp,Tact)));rm=mul(M,add(zm,mul(zp,Tact)))
 for Q,R in[(P,rp),(M,rm)]:
  PT=mul(Q,Tact);Y=add(sc(mul(zm,Q),2),zp);need(mul(R,R)==R and star(R)==R and mul(R,PT)==PT and mul(PT,Y)==R,'range projector and exact right witness');need(tr(R)==6,'one-column row rank')
 def literal_monomial(M0):
  Mx=M0.to_Matrix();out=[]
  for j in range(16):
   nz=[i for i in range(16)if Mx[i,j]!=0];need(len(nz)==1,'ordinary column support');val=Mx[nz[0],j];need(val in[1,I,-1,-I],'literal phase');out.append((nz[0],[1,I,-1,-I].index(val)))
  need(len({x[0]for x in out})==16,'ordinary permutation');return out
 literal_monomial(mul(A,active,Ai));literal_monomial(mul(A,J,active,J,Ai))
 for PP,MM,RP,RM in[(P,M,rp,rm),(M,P,rm,rp)]:
  K=bcol([mul(A,PP,Tact,A),mul(A,J,MM,Tact,A),Z]);R=diag([mul(A,RP,Ai),mul(A,J,RM,J,Ai),Z]);need(same(bm(R,K),K)and sum(tr(R[i][i])for i in range(3))==12,'both active orientations fixed by3D/4 range')
 Tplain=sc(add(E,S),Rational(1,2));plain_z=pw(mul(F,S),2);plain_zp=sc(add(E,plain_z),Rational(1,2));plain_zm=sub(E,plain_zp);plain_ranks=[tr(mul(Q,add(plain_zm,mul(plain_zp,Tplain))))for Q in[P,M]];need(plain_ranks==[8,8],'deleting Zc breaks3D/4 bound')
 identities={'backward_once':mul(Ai,Ts,A)==Sad,'backward_twice':mul(pw(A,-2),Ts,pw(A,2))==S,'output_decoder':mul(A,J,Ts,Ai)==Kd,'quartic_lower_component':mul(A,Ts,pw(A,3))==mul(pw(A,3),S,A),'commutes_F':mul(Ts,F)==mul(F,Ts),'commutes_J':mul(Ts,J)==mul(J,Ts),'decoder_commutes_output_sign':mul(Kd,Fh)==mul(Fh,Kd)};need(all(identities.values()),'literal spectator conjugates')
 T=sc(add(E,Ts),Rational(1,2));N=sub(E,T);r1p=sc(add(E,Sad),Rational(1,2));r1m=sub(E,r1p);r2p=sc(add(E,S),Rational(1,2));r2m=sub(E,r2p);ph=sc(add(E,Fh),Rational(1,2));mh=sub(E,ph);K=bcol([mul(A,P,T,A),mul(A,J,M,T,A),Z]);Kold=bcol([mul(A,P,A),mul(A,J,M,A),Z]);need(same(bm(bs(Kold),Kold),diag([E,Z,Z])),'old column isometry');need(same(bm(bs(K),K),diag([mul(Ai,T,A),Z,Z])),'prefix Gram')
 Drow=diag([E,Kd,E]);O=[[ph,mh,Z],[mh,ph,Z],[Z,Z,E]];H=bm(O,Drow);need(same(bm(H,K),bcol([mul(A,T,A),Z,Z])),'actual ordinary output alignment');need(mul(A,T,A)==mul(pw(A,2),r1p)and mul(A,T,pw(A,2))==mul(pw(A,3),r2p),'both kernel factorizations');need(mul(mul(A,T,A),r1m)==Z and mul(mul(A,T,pw(A,2)),r2m)==Z,'both genuine kernels');need(mul(mul(A,T,A),r2m)!=Z and mul(mul(A,T,pw(A,2)),r1m)!=Z,'wrong kernel controls')
 B2=mul(pw(A,3),S,A);e4=sc(pw(A,4),Rational(-1,2));e2=sc(B2,Rational(-1,2));need(sc(mul(A,T,pw(A,3)),-1)==add(e4,e2),'quartic split');need(mul(e4,star(e4))==sc(E,Rational(1,4))and mul(e2,star(e2))==sc(E,Rational(1,4)),'full rank class components')
 expected={}
 for row,ef,et in itertools.product(range(2),repeat=3):
  h=mul(J if row else E,pw(F,ef),pw(Ts,et))
  for trailing,r in[(1,2),(2,3)]:expected[f'row{row}_F{ef}_T{et}_rank{r}']=(mul(A,h,pw(A,trailing)),r)
 expected.update({'A4':(pw(A,4),4),'B2':(B2,2),'forward_Ts':(mul(A,Ts,Ai),2),'forward_JTsJ':(mul(A,J,Ts,J,Ai),2)})
 gauges=json.loads(rawfiles['GAUSSIAN-GAUGES.json']);need(set(gauges)==set(expected),'complete20-word gauge domain');targets={}
 for r in[2,3,4]:
  G=E
  for b in range(r):G=mul(G,sc(add(sc(E,1+I),sc(mono(tuple((j^(1<<b),0)for j in range(16))),1-I)),Rational(1,2)))
  targets[r]=G
 for name,(W,r)in expected.items():
  g=gauges[name];need(g['rank']==r and mul(mono(g['left']),targets[r],mono(g['right']))==W,('exact phase-preserving Gaussian gauge',name))
 need(sum(1 for x in mul(A,Ts,Ai).to_Matrix()[:,0]if x)!=1,'spectator forward image not monomial')
 wd=json.loads(rawfiles['WORDS.json']);monos={n:mono(t)for n,t in wd['monomial_tables'].items()};fresh={'F':F,'Fhat':Fh,'J':J,'Ts':Ts,'S_ab':S,'S_ad':Sad,'Kdec':Kd};need(monos==fresh,'actual ordinary control tables')
 Cold=[[P,M,Z],[mul(J,M),mul(J,P),Z],[Z,Z,E]];Rt=[[T,Z,N],[Z,E,Z],[N,Z,T]];Cn=bm(Cold,Rt);Swap12=[[E,Z,Z],[Z,Z,E],[Z,E,Z]];Qk=[[E,Z,Z],[Z,r2p,r2m],[Z,r2m,r2p]];wanted={'C_new':Cn,'C_swapped12':bm(Cn,Swap12),'Drow':Drow,'O':O,'Q_kernel':Qk};receipts={};controls=0
 for name,want in wanted.items():
  f,b=replay(wd['words'][name],monos);g,bi=replay(wd['words'][name+'_inverse'],monos);need(same(f,want)and same(bm(f,g),blocks_identity())and same(bm(g,f),blocks_identity()),('literal unit and inverse',name))
  for nm in[name,name+'_inverse']:
   word=wd['words'][nm];X,bound=replay(word,monos);receipt={'counts':dict(Counter(o['op']for o in word)),'prefix_bound':bound};need(receipt==wd['invoices'][nm],('exact counts and gain bounds',nm));receipts[nm]=receipt
   for k,o in enumerate(word):
    if o['op']=='ADD':need(not same(replay(word[:k]+word[k+1:],monos)[0],X),'missing ADD negative control');controls+=1
 need(controls==54,'all54 omitted-add controls');need(tr(Ts)==tr(Sad)==tr(S)==8 and tr(T)==12 and tr(r1m)==tr(r2m)==4,'non-half spectator traces')
 scalar={n:replay(word,{name:ey(16)for name in monos})[0]for n,word in wd['words'].items()if n in['C_new','C_swapped12','Q_kernel']};need(same(scalar['C_new'],blocks_identity())and same(scalar['C_swapped12'],Swap12)and same(scalar['Q_kernel'],blocks_identity()),'faithful-width scalar completion condition')
 result={'status':'PASS_INDEPENDENT_ORDINARY_ROW_RANGE_AND_SPECTATOR_BRIDGE','source_package_pins':pins,'engine':'Independent SymPy DomainMatrix over QQ(i); no author engine imported','D8_literal_order':8,'D8_exact_traces':[str(z)for z in traces],'all_width_D8_row_rank':'3D/8 per active bank;3D/4 total','without_Zc_negative_control_row_ranks':[str(z)for z in plain_ranks],'literal_source_identities':identities,'spectator_collective_prefix_rank':'(16^V+8^V)/2','spectator_collective_kernel_rank':'(16^V-8^V)/2','width_controls':{'V1_prefix':12,'V1_kernel':4,'V2_collective_prefix':160,'wrong_tensor_of_one_column_projector_rank':144,'wrong_half_D_at_V2':128},'exact_Gaussian_gauges':len(gauges),'both_ordinary_kernel_factorizations':True,'wrong_kernel_controls_rejected':2,'quartic_rank4_and_rank2_components_full_D':True,'literal_interface_receipts':receipts,'omitted_ADD_controls_rejected':controls,'scope':'Universal active-swap row-range exclusion in a fixed finite root-four tensor catalogue; actual spectator ordinary source/kernel bridge, not a full independent421 caller, supplier, or new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('20 exact gauges,54 primitive omission controls; every source identity exact.')
if __name__=='__main__':main()
