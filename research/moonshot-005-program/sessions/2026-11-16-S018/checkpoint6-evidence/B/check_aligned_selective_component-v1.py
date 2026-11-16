#!/usr/bin/env python3
"""Independent SymPy reconstruction and replay of source/aligned ordinary words."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import json,hashlib,itertools
import sympy as sp
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent/'R'/'pure-prefix-review'
tidy=lambda M:M.applyfunc(sp.expand)
I=sp.eye(16);Z=sp.zeros(16);X=sp.zeros(16);P=sp.zeros(16);D=sp.eye(16)
for x in range(16):
 X[x^2,x]=1;P[(x>>1)|((x&1)<<3),x]=1;D[x,x]=(-1)**(((x>>0)&1)*((x>>2)&1)*((x>>3)&1))
A=tidy(((1+sp.I)*I+(1-sp.I)*X)*D*P/2);Ai=A.conjugate().T
A2=tidy(A*A);A3=tidy(A2*A);A4=tidy(A3*A);Ai2=tidy(Ai*Ai);Ai3=tidy(Ai2*Ai)
F=sp.diag(*[(-1)**(x&1)for x in range(16)])
H=tidy(Ai2*F*A2);Fhat=tidy(A*F*Ai);Fback=tidy(Ai*H*A)
S=sp.zeros(16);J=sp.zeros(16);Kdirect=sp.zeros(16)
for x in range(16):
 a,b,c,d=[(x>>j)&1 for j in range(4)]
 S[b+2*a+4*c+8*d,x]=1
 J[a+2*b+4*(d^(a*b))+8*(c^(a*b)),x]=1
 Kdirect[a+2*(b^(a*d))+4*(c^(a*d))+8*d,x]=(-1)**(a*d)
K=tidy(A*J*A2*S*Ai3);B2=tidy(A3*S*A)
assert K==Kdirect and tidy(K*K)==I and tidy(K*Fhat)==tidy(Fhat*K)
assert tidy(A*J*A3)==tidy(K*B2)
assert tidy(B2*Fback)==tidy(Fhat*B2) and tidy(A4*Fback)==tidy(Fhat*A4)
assert tidy(J*F)==tidy(F*J) and tidy(S*H)==tidy(H*S)
mons={'F':F,'H':H,'Fhat':Fhat,'Fback':Fback,'J':J,'Jinv':J.conjugate().T,'S':S,'Sinv':S.conjugate().T,'K':K,'Kinv':K.conjugate().T}
roots=[1,sp.I,-1,-sp.I]
def table(M):
 out=[]
 for j in range(16):
  entries=[(i,M[i,j])for i in range(16)if M[i,j]!=0]
  assert len(entries)==1 and entries[0][1]in roots
  out.append((entries[0][0],roots.index(entries[0][1])))
 assert len({i for i,e in out})==16
 return out
for n in('F','H','Fhat','Fback'):assert tidy(mons[n]*mons[n])==I
jdata=json.loads((ROOT/'ORDINARY-WORDS.json').read_text())
for name,M in mons.items():
 got=table(M);given=jdata['one_column_tables'][name]
 assert [i for i,e in got]==given['destination'] and [e for i,e in got]==given['quarter_phase']
def blk(M):return sp.BlockMatrix(M).as_explicit()
def diag(X,Y,Z0):return sp.diag(X,Y,Z0)
def route(F0):
 P0=(I+F0)/2
 return blk([[I-P0,P0,Z],[P0,I-P0,Z],[Z,Z,I]])
Id=sp.eye(48)
C=tidy(diag(I,J,I)*route(F));Ci=tidy(route(F)*diag(I,J.conjugate().T,I))
Q=tidy(diag(I,S,I)*route(H)*diag(I,S.conjugate().T,I))
O=tidy(route(Fhat)*diag(I,K.conjugate().T,I));Oi=tidy(diag(I,K,I)*route(Fhat));R=route(Fback)
quartic=blk([[-tidy(A*C[r*16:(r+1)*16,:16]*A2*Q[16:32,c*16:(c+1)*16]*A)if c<2 else Z for c in range(3)]for r in range(3)])
assert tidy(O*quartic*R)==blk([[Z,-A4,Z],[Z,Z,Z],[Z,Z,Z]])
expected={'C':C,'C_inverse':Ci,'Q':Q,'Q_inverse':Q,'output_decoder':O,'output_decoder_inverse':Oi,'input_decoder':R,'input_decoder_inverse':R}
def replay(word):
 rows=[sp.eye(48)[16*r:16*(r+1),:]for r in range(3)];weights=[Fraction(1)]*3;bound=Fraction(1)
 for op in word:
  if op['op']=='ADD':
   i,j=op['dst'],op['src'];rows[i]+=rows[j];weights[i]+=weights[j]
  elif op['op']=='SCALE':
   i=op['bank'];f=Fraction(*op['factor']);rows[i]*=sp.Rational(f.numerator,f.denominator);weights[i]*=abs(f)
  else:
   i=op['bank'];rows[i]=mons[op['table']]*rows[i]
  bound=max(bound,*weights)
 return tidy(sp.Matrix.vstack(*rows)),bound
receipts={};negatives=0
for name,word in jdata['words'].items():
 M,bound=replay(word);assert M==expected[name] and bound<=5
 for j,op in enumerate(word):
  if op['op']=='ADD':assert replay(word[:j]+word[j+1:])[0]!=M;negatives+=1
 receipts[name]={'operation_counts':dict(Counter(x['op']for x in word)),'prefix_bound':str(bound)}
for x,y in [('C','C_inverse'),('Q','Q_inverse'),('output_decoder','output_decoder_inverse'),('input_decoder','input_decoder_inverse')]:assert tidy(expected[x]*expected[y])==Id and tidy(expected[y]*expected[x])==Id
# Universal collective-involution primitive proof: both sectors of Q[F]/(F^2-1).
for f,eps in itertools.product((1,-1),(1,-1)):
 src,dst=sp.symbols('x y');x,y=src,dst
 x*=sp.Rational(eps,2);y+=x;x*=f;y+=x;x*=f;x*=2*eps
 assert sp.expand(x-src)==0 and sp.expand(y-dst-eps*(1+f)*src/2)==0
 for ff in(1,-1):
  pp=sp.Rational(1+ff,2);M=sp.eye(2);E01=sp.Matrix([[1,pp],[0,1]]);E10=sp.Matrix([[1,0],[-pp,1]])
  assert sp.diag(1,-ff)*E01*E10*E01==sp.Matrix([[1-pp,pp],[pp,1-pp]])
paths=[BASE/'ALIGNED-SELECTIVE-COMPONENT-v1.md',BASE/'PURE-PREFIX-IMAGE-GATE-v2.md',BASE/'INVERSE-CUT-SUPPORT-GATE-v2.md',ROOT/'ORDINARY-WORDS.json',ROOT/'check.py',BASE/'check_selective_rank4_controls.py',BASE/'SELECTIVE-RANK4-CONTROLS-RESULT.json']
result={'status':'PASS_AUTHOR_ALIGNED_COMPONENT_AND_INDEPENDENT_PRIMITIVE_REVIEW','arithmetic':'Independent exact SymPy Gaussian rationals; literal source rebuilt; formal involution sector proof.','full_D_rank4_alignment':True,'entire_quartic_prefix_pure4':True,'lower_quartic_cross_terms_zero':True,'primitive_words':receipts,'omitted_ADD_negative_controls':negatives,'all_width_logic':'Multiplicative literal identities tensor; involution algebra uses collective operators and external scalars. No parity collapse.','scope':'Positive ordinary-aligned rank4 component only. Universal pure-prefix theorem excludes independent421 completion of these fixed entries.','dependencies':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}
(BASE/'ALIGNED-SELECTIVE-COMPONENT-RESULT-v1.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print(hashlib.sha256(paths[0].read_bytes()).hexdigest())
