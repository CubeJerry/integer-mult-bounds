#!/usr/bin/env python3
"""Independent exact Gaussian-integer review of the pure-prefix and aligned channel identities."""
import argparse,hashlib,json,itertools
from collections import Counter,deque
from fractions import Fraction
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);o=p.parse_args()
N=16
class M:
 def __init__(self,r,i=None,k=0):
  self.r=np.array(r,dtype=np.int64);self.i=np.zeros((N,N),dtype=np.int64)if i is None else np.array(i,dtype=np.int64);self.k=k
  while self.k and np.all(self.r%2==0)and np.all(self.i%2==0):self.r//=2;self.i//=2;self.k-=1
 def __matmul__(self,b):
  ar=max(int(np.max(np.abs(self.r))),int(np.max(np.abs(self.i))));br=max(int(np.max(np.abs(b.r))),int(np.max(np.abs(b.i))))
  assert 2*N*ar*br<2**62
  return M(self.r@b.r-self.i@b.i,self.r@b.i+self.i@b.r,self.k+b.k)
 def adj(self):return M(self.r.T,-self.i.T,self.k)
 def key(self):return(self.k,self.r.tobytes(),self.i.tobytes())
 def eq(self,b):return self.key()==b.key()
 def pow(self,n):
  a=self;v=I
  for _ in range(n):v=v@a
  return v
def mono(g):
 r=np.zeros((N,N),dtype=np.int64);i=r.copy()
 for c,(dst,ph)in enumerate(zip(*g)):
  r[dst,c]=[1,0,-1,0][ph];i[dst,c]=[0,1,0,-1][ph]
 return M(r,i)
def extract(A):
 assert A.k==0;dst=[];phase=[]
 for j in range(N):
  ix=np.flatnonzero((A.r[:,j]!=0)|(A.i[:,j]!=0));assert len(ix)==1;x=int(ix[0]);z=(int(A.r[x,j]),int(A.i[x,j]));assert z in [(1,0),(0,1),(-1,0),(0,-1)];dst.append(x);phase.append([(1,0),(0,1),(-1,0),(0,-1)].index(z))
 assert len(set(dst))==N
 return(tuple(dst),tuple(phase))
def gp(g,h):return(tuple(g[0][h[0][j]]for j in range(N)),tuple((h[1][j]+g[1][h[0][j]])%4 for j in range(N)))
ident=(tuple(range(N)),(0,)*N);I=mono(ident)
def group(gs):
 seen={ident};q=deque([ident])
 while q:
  x=q.popleft()
  for g in gs:
   z=gp(g,x)
   if z not in seen:seen.add(z);q.append(z)
 return seen
X=mono((tuple(j^2 for j in range(N)),(0,)*N));P=mono((tuple((j>>1)|((j&1)<<3)for j in range(N)),(0,)*N))
D=mono((tuple(range(N)),tuple(2*((j&1)*((j>>2)&1)*((j>>3)&1))for j in range(N))))
A=M(I.r+X.r,I.r-X.r,1)@D@P;Ai=A.adj();assert(A@Ai).eq(I)
A2=A@A;A3=A2@A;Ai2=Ai@Ai
Da=mono((tuple(range(N)),tuple(j&1 for j in range(N))));Db=mono((tuple(range(N)),tuple((j>>1)&1 for j in range(N))))
Ha=Ai2@Da.pow(2)@A2;Hb=Ai2@Db.pow(2)@A2
dst=[];ph=[]
for j in range(N):
 a,b,c,d=[(j>>k)&1 for k in range(4)];dst.append((c^(a*b))+2*d+4*a+8*b);ph.append((a*b+2*a*b*(c+d))%4)
R2=mono((tuple(dst),tuple(ph)))
Ba=mono((tuple(((j&1)<<1)|((j&2)>>1)|(j&12)for j in range(N)),(0,)*N))
J=R2.adj()@Ba@R2;Jg=extract(J)
core=mono((tuple((j&3)+4*(0,3,2,1)[j>>2]for j in range(N)),(0,)*N))
Qc=R2.adj()@core@R2;CZ=mono((tuple(range(N)),tuple(2*int((j&3)==3)for j in range(N))))
gens=[extract(T)for T in [Ha,Hb,Da,Db,CZ,Qc]];H=group(gens);G=group(gens+[Jg]);assert len(H)==256 and len(G)==512
assert H.isdisjoint({gp(g,Jg)for g in H})and H|{gp(g,Jg)for g in H}==G
assert len({(g[0],tuple((x-g[1][0])%4 for x in g[1]))for g in G})==512
def gaussian_rank(T):
 supports={}
 for r in range(N):
  cols=tuple(j for j in range(N)if T.r[r,j]or T.i[r,j]);supports.setdefault(cols,[]).append(r)
 sizes={len(c)for c in supports};assert len(sizes)==1;size=next(iter(sizes));rank=size.bit_length()-1
 assert size==1<<rank and len(supports)==N//size
 seen=set()
 for cols,rows in supports.items():
  assert len(rows)==size and not(seen&set(cols));seen.update(cols)
  vals=[];r0=rows[0];c0=cols[0]
  for r in rows:
   bits=0
   for k,c in enumerate(cols):
    x,y=int(T.r[r,c]),int(T.i[r,c]);assert x*x+y*y==1<<(2*T.k-rank)
    ar,ai=int(T.r[r0,c0]),int(T.i[r0,c0]);br,bi=int(T.r[r,c0]),int(T.i[r,c0]);cr,ci=int(T.r[r0,c]),int(T.i[r0,c])
    left=(x*ar-y*ai,x*ai+y*ar);right=(br*cr-bi*ci,br*ci+bi*cr)
    assert left==right or left==(-right[0],-right[1])
    if left!=right:bits|=1<<k
   vals.append(bits)
  span={0}
  for row in vals:
   if row not in span:span|={x^row for x in list(span)}
  assert set(vals)==span and len(span)==1<<rank
 return rank

Dc=mono((tuple(range(N)),tuple((j>>2)&1 for j in range(N))))
classes=[]
for j in range(4):
 d=Dc.pow(j);assert gaussian_rank(A@d@A)==2 and gaussian_rank(A@d@A2)==3
 census=Counter(gaussian_rank(A@d@A2@mono(g)@A) for g in sorted(G));assert census=={4:512}
 classes.append({'quarter_c_power':j,'rank2_prefix':2,'rank3_prefix':3,'rank4_words':512})
for j in range(4):assert (A@Db.pow(j)).eq(Da.pow(j)@A)

def plus(x,y):
 k=max(x.k,y.k);return M(x.r*(1<<(k-x.k))+y.r*(1<<(k-y.k)),x.i*(1<<(k-x.k))+y.i*(1<<(k-y.k)),k)
def neg(x):return M(-x.r,-x.i,x.k)
def sub(x,y):return plus(x,neg(y))
def half(x):return M(x.r,x.i,x.k+1)
Z=M(np.zeros((N,N),dtype=np.int64));A4=A3@A;Ai3=Ai2@Ai
F=Da.pow(2);H=Ai2@F@A2;assert H.eq(Ha)
proj=half(plus(I,F));T=half(plus(I,H));Fhat=A@F@Ai;Fback=Ai@H@A
extract(Fhat);extract(Fback);Phat=half(plus(I,Fhat));Pback=half(plus(I,Fback))
S=Ba;K=A@J@A2@S@Ai3;Ktable=extract(K)
dst=[];phase=[]
for j in range(N):
 a,b,c,d=[(j>>k)&1 for k in range(4)];dst.append(a+2*(b^(a*d))+4*(c^(a*d))+8*d);phase.append(2*a*d)
assert K.eq(mono((tuple(dst),tuple(phase))))
assert (K@Fhat).eq(Fhat@K)
B2=A3@S@A;assert gaussian_rank(B2)==2
assert (A@J@A3).eq(K@B2)
assert (B2@Fback).eq(Fhat@B2) and (A4@Fback).eq(Fhat@A4)
assert (J@F).eq(F@J) and (S@H).eq(H@S)

def eye3():return [[I if r==c else Z for c in range(3)]for r in range(3)]
def mm(X,Y):
 return [[plus(plus(X[r][0]@Y[0][c],X[r][1]@Y[1][c]),X[r][2]@Y[2][c]) for c in range(3)]for r in range(3)]
def diag(*xs):return [[xs[r]if r==c else Z for c in range(3)]for r in range(3)]
def beq(X,Y):return all(X[r][c].eq(Y[r][c])for r in range(3)for c in range(3))
def route(P):return [[sub(I,P),P,Z],[P,sub(I,P),Z],[Z,Z,I]]
C=mm(diag(I,J,I),route(proj));Ci=mm(route(proj),diag(I,J.adj(),I))
Q=mm(mm(diag(I,S,I),route(T)),diag(I,S.adj(),I));Qi=Q
assert C[0][0].eq(sub(I,proj)) and C[1][0].eq(J@proj)
assert Q[1][0].eq(S@T) and Q[1][1].eq(sub(I,T))
assert beq(mm(C,Ci),eye3()) and beq(mm(Ci,C),eye3()) and beq(mm(Q,Qi),eye3())
KC=[A@C[0][0]@A,A@C[1][0]@A,Z]
quartic=[[neg(KC[r]@A@Q[1][c]@A)if c<2 else Z for c in range(3)]for r in range(3)]
expect=[[Z,neg(sub(I,Phat)@A4),Z],[neg(Phat@K@A4),Z,Z],[Z,Z,Z]]
assert beq(quartic,expect)
O=mm(route(Phat),diag(I,K.adj(),I));Oi=mm(diag(I,K,I),route(Phat));R=route(Pback)
aligned=mm(mm(O,quartic),R);want=[[Z,neg(A4),Z],[Z,Z,Z],[Z,Z,Z]]
assert beq(aligned,want) and beq(mm(O,Oi),eye3()) and beq(mm(Oi,O),eye3()) and beq(mm(R,R),eye3())
# Literal ordinary primitive controls. Scalars stay outside tensor monomials.
mons={'F':F,'H':H,'Fhat':Fhat,'Fback':Fback,'J':J,'Jinv':J.adj(),'S':S,'Sinv':S.adj(),'K':K,'Kinv':K.adj()}
def mono_op(bank,name):return {'op':'MONO','bank':bank,'table':name}
def shear(src,dst,name,sign):
 return [{'op':'SCALE','bank':src,'factor':[sign,2]},{'op':'ADD','src':src,'dst':dst},mono_op(src,name),{'op':'ADD','src':src,'dst':dst},mono_op(src,name),{'op':'SCALE','bank':src,'factor':[2*sign,1]}]
def rword(name):
 return shear(1,0,name,1)+shear(0,1,name,-1)+shear(1,0,name,1)+[mono_op(1,name),{'op':'SCALE','bank':1,'factor':[-1,1]}]
words={'C':rword('F')+[mono_op(1,'J')],'C_inverse':[mono_op(1,'Jinv')]+rword('F'),'Q':[mono_op(1,'Sinv')]+rword('H')+[mono_op(1,'S')],'Q_inverse':[mono_op(1,'Sinv')]+rword('H')+[mono_op(1,'S')],'output_decoder':[mono_op(1,'Kinv')]+rword('Fhat'),'output_decoder_inverse':rword('Fhat')+[mono_op(1,'K')],'input_decoder':rword('Fback'),'input_decoder_inverse':rword('Fback')}
def scale(x,s):
 assert s.denominator&(s.denominator-1)==0
 return M(x.r*s.numerator,x.i*s.numerator,x.k+s.denominator.bit_length()-1)
def replay(word):
 v=eye3();weights=[Fraction(1)]*3;bound=Fraction(1)
 for op in word:
  if op['op']=='ADD':
   i,j=op['dst'],op['src'];v[i]=[plus(x,y)for x,y in zip(v[i],v[j])];weights[i]+=weights[j]
  elif op['op']=='SCALE':
   i=op['bank'];s=Fraction(*op['factor']);v[i]=[scale(x,s)for x in v[i]];weights[i]*=abs(s)
  else:
   i=op['bank'];v[i]=[mons[op['table']]@x for x in v[i]]
  bound=max(bound,*weights)
 return v,bound
wanted={'C':C,'C_inverse':Ci,'Q':Q,'Q_inverse':Qi,'output_decoder':O,'output_decoder_inverse':Oi,'input_decoder':R,'input_decoder_inverse':R}
receipts={};controls=0
for name,word in words.items():
 mat,bound=replay(word);assert beq(mat,wanted[name])
 for i,op in enumerate(word):
  if op['op']=='ADD':assert not beq(replay(word[:i]+word[i+1:])[0],mat);controls+=1
 receipts[name]={'operations':dict(Counter(x['op']for x in word)),'prefix_row_sum_bound':str(bound),'exact_operator_and_inverse':True}
o.out.mkdir(parents=True,exist_ok=True)
tables={name:{'destination':list(extract(v)[0]),'quarter_phase':list(extract(v)[1])}for name,v in mons.items()}
(o.out/'ORDINARY-WORDS.json').write_text(json.dumps({'words':words,'one_column_tables':tables,'tensor_rule':'Each MONO is the tensor power of its listed literal table. SCALE is an external scalar, not absorbed into each one-column phase.','physical_scope':'Each MONO and SCALE acts on a complete field and is charged, as is every ADD. No owned record, free decoder, free source or precision assumption.'},indent=2)+'\n')
res={'status':'PASS_ROOT_PURE_PREFIX_AND_ALIGNED_CHANNEL_REVIEW','pure_prefix_proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'arithmetic':'Bounded Gaussian integers / powers of two, independently retained engine; no modular samples or floating tolerance.','coefficient_algebra_instance':classes,'four_source_words_checked':2048,'ordinary_Db_transport':True,'aligned_word_identities':{'K_literal_toffoli_phase':True,'B2_rank':2,'J_channel_equals_K_B2':True,'B2_and_A4_intertwine_Fback_Fhat':True,'K_commutes_Fhat':True,'entire_quartic_prefix_pure4':True,'full_rank4_ordinary_alignment':True},'all_width_justification':'Literal multiplicative one-column identities tensor exactly; projector and route algebra is applied to collective involutions with external dyadic scalars. Pure-prefix image/cut theorem separately read, not inferred from finite unit checks.','primitive_words':receipts,'omitted_ADD_controls':controls,'scope':'Positive aligned rank4 component and exact unit controls; pure-prefix theorem excludes all independent421 completions of this fixed prefix. No full caller, supplier, new kappa, or foundation discharge.'}
(o.out/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(res['status']);print(receipts)
