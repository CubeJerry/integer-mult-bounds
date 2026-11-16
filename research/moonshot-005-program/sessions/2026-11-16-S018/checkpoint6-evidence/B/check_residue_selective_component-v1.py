#!/usr/bin/env python3
"""Parity-uniform exterior-i selective quartic component and paid ordinary words."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,itertools
import sympy as sp
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();WORK=o.work.resolve();BASE=WORK/'B';ROOT=WORK/'R'/'pure-prefix-review'
src=(BASE/'check_aligned_selective_component-v2.py').read_text();start=src.index('tidy=lambda');stop=src.index("jdata=json.loads")
exec(compile(src[start:stop],str(BASE/'check_aligned_selective_component-v2.py'),'exec'))
Z=sp.zeros(16);Id=sp.eye(48)
def blk(M):return sp.BlockMatrix(M).as_explicit()
def diag(X,Y,Z0):return sp.diag(X,Y,Z0)
def route(G):
 T=(I+G)/2
 return blk([[I-T,T,Z],[T,I-T,Z],[Z,Z,I]])
C=tidy(diag(I,J,I)*route(F));Ci=tidy(route(F)*diag(I,J.conjugate().T,I))
Q=tidy(diag(I,S,I)*route(sp.I*H)*diag(I,S.conjugate().T,I));Qi=tidy(diag(I,S,I)*route(-sp.I*H)*diag(I,S.conjugate().T,I))
O=tidy(route(Fhat)*diag(I,K.conjugate().T,I));Oi=tidy(diag(I,K,I)*route(Fhat))
Tb=(I+sp.I*Fback)/2;Tbi=I-sp.I*Fback;Tmi=I+sp.I*Fback
assert tidy(Tb*Tbi)==I and tidy((I-Tb)*Tmi)==I
Dn=diag(Tbi,Tmi,I);Dni=diag(Tb,I-Tb,I)
R=tidy(Dn*route(Fback));Ri=tidy(route(Fback)*Dni)
quartic=blk([[-tidy(A*C[r*16:(r+1)*16,:16]*A2*Q[16:32,c*16:(c+1)*16]*A)if c<2 else Z for c in range(3)]for r in range(3)])
assert tidy(O*quartic*R)==blk([[-B2,-A4,Z],[Z,Z,Z],[Z,Z,Z]])
Kprefix=sp.Matrix.vstack(tidy(A*C[:16,:16]*A),tidy(A*C[16:32,:16]*A),Z)
OK=tidy(O*Kprefix);assert OK[16:,:]==sp.zeros(32,16)
assert tidy(Kprefix.conjugate().T*Kprefix)==I and tidy(OK[:16,:].conjugate().T*OK[:16,:])==I
Pi=tidy(Oi*diag(I,Z,Z)*O);assert tidy(Pi*Pi)==Pi and tidy(Pi*Kprefix)==Kprefix
# Exact Gaussian class check includes rectangular support components, equal norm,
# fourth-root gauges, and binary Walsh row closure; support alone is insufficient.
def gaussian_rank(M):
 groups={}
 for r in range(16):groups.setdefault(tuple(c for c in range(16)if M[r,c]!=0),[]).append(r)
 sizes={len(c)for c in groups};assert len(sizes)==1;n=next(iter(sizes));rr=n.bit_length()-1;assert n==1<<rr
 seen=set()
 for cols,rows in groups.items():
  assert len(rows)==n and not(seen&set(cols));seen.update(cols);r0,c0=rows[0],cols[0];vals=[];z0=M[r0,c0]
  for r in rows:
   bits=0
   assert sp.expand(M[r,c0]/z0)in(1,sp.I,-1,-sp.I)
   for k,c in enumerate(cols):
    assert sp.expand(M[r,c]*sp.conjugate(M[r,c]))==sp.Rational(1,n)
    assert sp.expand(M[r0,c]/z0)in(1,sp.I,-1,-sp.I)
    q=sp.simplify(M[r,c]*z0/(M[r,c0]*M[r0,c]));assert q in(1,-1)
    if q==-1:bits|=1<<k
   vals.append(bits)
  assert len(set(vals))==n and all(x^y in vals for x,y in itertools.product(vals,repeat=2))
 return rr
classes={'aJa':gaussian_rank(tidy(A*J*A)),'aJa2':gaussian_rank(tidy(A*J*A2)),'B2':gaussian_rank(B2),'a4':gaussian_rank(A4)}
assert classes=={'aJa':2,'aJa2':3,'B2':2,'a4':4}
jdata=json.loads((ROOT/'ORDINARY-WORDS.json').read_text())
def sc(bank,z):
 z=sp.expand(z);re,im=z.as_real_imag();den=sp.ilcm(sp.denom(re),sp.denom(im))
 return {'op':'SCALE','bank':bank,'factor':[int(re*den),int(im*den),int(den)]}
def mo(bank,name):return {'op':'MONO','bank':bank,'table':name}
def ad(src,dst):return {'op':'ADD','src':src,'dst':dst}
def convert(word):return [dict(x,factor=[x['factor'][0],0,x['factor'][1]])if x['op']=='SCALE'else x.copy()for x in word]
def monshear(src,dst,terms):
 ops=[]
 for name,coef in terms:
  if name!='I':ops.append(mo(src,name))
  if coef!=1:ops.append(sc(src,coef))
  ops.append(ad(src,dst))
  if coef!=1:ops.append(sc(src,1/coef))
  if name!='I':ops.append(mo(src,name))
 return ops
# All monomials in these shears are involutions.
def wword(t,ti):return monshear(1,0,t)+monshear(0,1,[(n,-v)for n,v in ti])+monshear(1,0,t)
minus_w=wword([('I',sp.Integer(-1))],[('I',sp.Integer(-1))])
t=[('I',sp.Integer(1)),('Fback',-sp.I)];ti=[('I',sp.Rational(1,2)),('Fback',sp.I/2)]
Dword=minus_w+wword(t,ti)+[sc(1,2)]
Diword=[sc(1,sp.Rational(1,2))]+minus_w+wword(ti,t)
Hword=[ad(1,0),sc(1,-2),ad(0,1)];Hiword=Hword+[sc(0,sp.Rational(1,2)),sc(1,sp.Rational(1,2))]
def qword(sign):return [mo(1,'Sinv')]+Hword+[mo(1,'H'),sc(1,sign*sp.I)]+Hiword+[mo(1,'S')]
words={'C':convert(jdata['words']['C']),'C_inverse':convert(jdata['words']['C_inverse']),'Q':qword(-1),'Q_inverse':qword(1),'output_decoder':convert(jdata['words']['output_decoder']),'output_decoder_inverse':convert(jdata['words']['output_decoder_inverse']),'input_decoder':convert(jdata['words']['input_decoder'])+Dword,'input_decoder_inverse':Diword+convert(jdata['words']['input_decoder_inverse'])}
expected={'C':C,'C_inverse':Ci,'Q':Q,'Q_inverse':Qi,'output_decoder':O,'output_decoder_inverse':Oi,'input_decoder':R,'input_decoder_inverse':Ri}
def replay(word):
 rows=[Id[16*r:16*(r+1),:]for r in range(3)];weights=[sp.Integer(1)]*3;bound=sp.Integer(1)
 for op in word:
  if op['op']=='ADD':
   i,j=op['dst'],op['src'];rows[i]+=rows[j];weights[i]+=weights[j]
  elif op['op']=='SCALE':
   i=op['bank'];re,im,de=op['factor'];z=(sp.Integer(re)+sp.I*im)/de;rows[i]*=z;weights[i]*=abs(z)
  else:
   i=op['bank'];rows[i]=mons[op['table']]*rows[i]
  bound=max(bound,*weights)
 return tidy(sp.Matrix.vstack(*rows)),bound
receipts={};negatives=0
for name,word in words.items():
 M,bound=replay(word);assert M==expected[name],name
 for j,op in enumerate(word):
  if op['op']=='ADD':assert replay(word[:j]+word[j+1:])[0]!=M;negatives+=1
 receipts[name]={'operation_counts':dict(Counter(x['op']for x in word)),'prefix_bound':str(bound)}
for x,y in [('C','C_inverse'),('Q','Q_inverse'),('output_decoder','output_decoder_inverse'),('input_decoder','input_decoder_inverse')]:assert tidy(expected[x]*expected[y])==Id and tidy(expected[y]*expected[x])==Id
for f in(1,-1):
 tt=(1+sp.I*f)/2;assert sp.expand(tt*(1-sp.I*f))==1 and sp.expand((1-tt)*(1+sp.I*f))==1
 Rf=sp.Matrix([[1-tt,tt],[tt,1-tt]]);assert sp.simplify(Rf*Rf.conjugate().T)==sp.eye(2)
 assert sp.simplify((1-sp.I*f)*(1+sp.I*f))==2
assert (1+sp.I)/2!=0 and (1+sp.I**2)/2==0
paths=[BASE/'RESIDUE-SELECTIVE-COMPONENT-v1.md',BASE/'check_aligned_selective_component-v2.py',BASE/'ALIGNED-SELECTIVE-COMPONENT-v1.md',ROOT/'ORDINARY-WORDS.json',BASE/'PURE-PREFIX-IMAGE-GATE-v3.md',BASE/'INVERSE-CUT-SUPPORT-GATE-v2.md']
result={'status':'PASS_AUTHOR_PARITY_UNIFORM_RESIDUE_COMPONENT','arithmetic':'Exact Gaussian rationals with symbolic collective-involution proof.','aligned_quartic_row':['-B2','-a4','0'],'source_gaussian_classes':classes,'rank4_component_full_field_rank':True,'rank2_residue_full_field_rank':True,'native_prefix_range_ordinary':True,'parity':'Every positive width; exterior i is not tensor-lifted. Even-width phase-collapse negative control rejected.','primitive_words':receipts,'omitted_ADD_negative_controls':negatives,'scope':'Positive component and paid ordinary unit words. Ordinary-prefix-range theorem excludes independent421 completion for this fixed first C column.','dependencies':{str(p.relative_to(WORK)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}
o.out.mkdir(parents=True,exist_ok=True)
(o.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(o.out/'WORDS.json').write_text(json.dumps({'words':words,'scalar_format':'factor=[real numerator,imaginary numerator,positive common denominator]; external field scalar','tables_dependency':'R/pure-prefix-review/ORDINARY-WORDS.json','all_width_rule':'All MONO symbols are literal table tensor powers. The imaginary scalar i is exterior and remains i at every width.'},indent=2)+'\n');print(result['status']);print(receipts)
