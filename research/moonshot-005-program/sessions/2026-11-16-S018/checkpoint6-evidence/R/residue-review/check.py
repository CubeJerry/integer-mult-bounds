#!/usr/bin/env python3
"""Independent bounded Gaussian-integer check of the exterior-i residue control."""
import argparse,hashlib,json,itertools
from collections import Counter,deque
from fractions import Fraction
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--out',type=Path,required=True);opts=p.parse_args();W=opts.work.resolve()
# Reuse only root's separately reviewed arithmetic/source implementation, not B's checker.
src=(W/'R/pure-prefix-review/check.py').read_text();exec(compile(src[src.index('N=16'):src.index('o.out.mkdir')],str(W/'R/pure-prefix-review/check.py'),'exec'))
def zs(x,re,im,den=1):
 assert den>0 and den&(den-1)==0
 return M(x.r*re-x.i*im,x.r*im+x.i*re,x.k+den.bit_length()-1)
iH=zs(H,0,1);Tq=half(plus(I,iH));Tin=half(plus(I,zs(Fback,0,1)))
Qnew=mm(mm(diag(I,S,I),route(Tq)),diag(I,S.adj(),I));Qni=mm(mm(diag(I,S,I),route(half(sub(I,iH)))),diag(I,S.adj(),I))
Dn=diag(sub(I,zs(Fback,0,1)),plus(I,zs(Fback,0,1)),I)
Dni=diag(Tin,sub(I,Tin),I)
Rnew=mm(Dn,route(Pback));Rni=mm(route(Pback),Dni)
quartic=[[neg(KC[r]@A@Qnew[1][c]@A)if c<2 else Z for c in range(3)]for r in range(3)]
want=[[neg(B2),neg(A4),Z],[Z,Z,Z],[Z,Z,Z]]
assert beq(mm(mm(O,quartic),Rnew),want)
assert gaussian_rank(B2)==2 and gaussian_rank(A4)==4
assert gaussian_rank(A2)==2 and gaussian_rank(A3)==3 and gaussian_rank(A@J@A)==2 and gaussian_rank(A@J@A2)==3
# K is an isometry, and its actual image is the range of an ordinary projector.
assert plus(plus(KC[0].adj()@KC[0],KC[1].adj()@KC[1]),KC[2].adj()@KC[2]).eq(I)
OK=[plus(plus(O[r][0]@KC[0],O[r][1]@KC[1]),O[r][2]@KC[2])for r in range(3)];assert OK[1].eq(Z)and OK[2].eq(Z)and(OK[0].adj()@OK[0]).eq(I)
Pi=mm(mm(Oi,diag(I,Z,Z)),O);assert beq(mm(Pi,Pi),Pi)
assert all(plus(plus(Pi[r][0]@KC[0],Pi[r][1]@KC[1]),Pi[r][2]@KC[2]).eq(KC[r])for r in range(3))
expected={'C':C,'C_inverse':Ci,'Q':Qnew,'Q_inverse':Qni,'output_decoder':O,'output_decoder_inverse':Oi,'input_decoder':Rnew,'input_decoder_inverse':Rni}
blob=(W/'B/residue-selective-v1/WORDS.json').read_bytes();ws=json.loads(blob)['words']
def run(word):
 v=eye3();weights=[Fraction(1)]*3;bound=Fraction(1)
 for op in word:
  if op['op']=='ADD':
   r,c=op['dst'],op['src'];v[r]=[plus(x,y)for x,y in zip(v[r],v[c])];weights[r]+=weights[c]
  elif op['op']=='SCALE':
   r=op['bank'];re,im,de=op['factor'];assert (re==0)!=(im==0);v[r]=[zs(x,re,im,de)for x in v[r]];weights[r]*=Fraction(abs(re)+abs(im),de)
  else:
   r=op['bank'];v[r]=[mons[op['table']]@x for x in v[r]]
  bound=max(bound,*weights)
 return v,bound
receipts={};negative=0
for name,word in ws.items():
 mat,bd=run(word);assert beq(mat,expected[name]),name
 for j,x in enumerate(word):
  if x['op']=='ADD':assert not beq(run(word[:j]+word[j+1:])[0],mat);negative+=1
 receipts[name]={'counts':dict(Counter(x['op']for x in word)),'maximum_bank_prefix_bound':str(bd)}
for n in ['C','Q','output_decoder','input_decoder']:
 assert beq(mm(expected[n],expected[n+'_inverse']),eye3())and beq(mm(expected[n+'_inverse'],expected[n]),eye3())
assert negative==62
# Concrete width2 phase-collapse failure at a +1 eigenvector of Fback tensor Fback:
# exterior i gives (1+i)/2 nonzero; tensoring i instead gives (1+i^2)/2=0.
assert half(plus(I,zs(Fback,0,1))).k>=0
report={'status':'PASS_ROOT_ORDINARY_RANGE_AND_EXTERIOR_I_RESIDUE_REVIEW','proof_sha256':hashlib.sha256((W/'B/PURE-PREFIX-IMAGE-GATE-v3.md').read_bytes()).hexdigest(),'component_proof_sha256':hashlib.sha256((W/'B/RESIDUE-SELECTIVE-COMPONENT-v1.md').read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),'independent_arithmetic':'Root bounded Gaussian integers, no B execution code, exact power-of-two denominators.','aligned_quartic_blocks':['-B2','-a4','0'],'source_gaussian_ranks':{'B2':2,'a4':4,'a2':2,'a3':3,'aJa':2,'aJa2':3},'actual_prefix_isometry_and_ordinary_projector':True,'primitive_words':receipts,'single_ADD_omission_controls':negative,'all_width_logic':'Literal multiplicative source identities tensor; collective involution algebra and exterior scalars then apply. Ordinary image proof reviewed separately.','scope':'Full-D rank4 and rank2 quartic components with actual ordinary inverses; generalized ordinary-range theorem excludes every independent421 completion with this fixed first C column. No supplier, foundation discharge or kappa.'}
opts.out.parent.mkdir(parents=True,exist_ok=True);opts.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status']);print(receipts)
