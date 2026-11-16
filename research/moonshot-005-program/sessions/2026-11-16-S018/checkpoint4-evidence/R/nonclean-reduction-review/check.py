#!/usr/bin/env python3
"""Independent free-product isolation and paid wrapper implementation checks."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args();o.out.mkdir(parents=True,exist_ok=True)
def add(*xs):
 z={}
 for d in xs:
  for k,v in d.items():z[k]=z.get(k,0)+v
 return{k:v for k,v in z.items()if v}
def mul(a,b):return add(*({k+l:v*w}for k,v in a.items()for l,w in b.items()))
def neg(a):return{k:-v for k,v in a.items()}
def w(*x):return{tuple(x):1}
def mm(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def backward(d):
 r={}
 for k,v in d.items():
  k=list(k)
  for i in range(len(k)-1):
   if k[i:i+2]==['b','a']:k[i:i+2]=['a','beta']
  key=tuple(k);r[key]=r.get(key,0)+v
 return{k:v for k,v in r.items()if v}
z={};one=w();a=w('a');L=[[a,z,z],[one,a,z],[z,z,one]];U=[[a,neg(w('a','a')),z],[z,a,z],[z,z,one]]
C=[[one,w('b'),z],[z,one,one],[w('u'),add(w('f'),w('u','b')),z]]
QA=[[w('p'),w('q')],[w('r'),w('t')]];Q=[[w('p'),w('q'),z],[w('r'),w('t'),z],[neg(add(w('p'),w('beta','r'))),neg(add(w('q'),w('beta','t'))),one]]
E=[[backward(v)for v in row]for row in mm(mm(mm(mm(L,C),U),Q),L)]
assert E[1]==[z,z,a]and E[0][2]==E[2][2]==z
B=[[one,w('b')],[w('u'),add(w('f'),w('u','b'))]];LA=[[a,z],[one,a]];UA=[[a,neg(w('a','a'))],[z,a]]
M=mm(mm(mm(mm([[a,z],[z,one]],B),UA),QA),LA);M=[[backward(v)for v in row]for row in M]
assert M==[[E[i][j]for j in [0,1]]for i in [0,2]]

# Literal services, independently derived from the native source.
I=s.eye(16);R=s.zeros(16);D=s.eye(16);Xs=[s.zeros(16)for _ in range(4)]
for j in range(16):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)];R[(j>>1)|((j&1)<<3),j]=1;D[j,j]=(-1)**(aa*cc*dd)
 for k in range(4):Xs[k][j^(1<<k),j]=1
tidy=lambda M:M.applyfunc(s.expand);S=D*R;A=tidy(((1+s.I)*I+(1-s.I)*Xs[1])*S/2)
Ds=[s.diag(*[s.I**((j>>k)&1)for j in range(16)])for k in range(4)]
bb=Ds[2];beta=Ds[3];uu=S.adjoint()*Ds[1];ff=Xs[0]
assert tidy(A.adjoint()*bb*A)==beta
assert bb*uu!=uu*bb
support=lambda M:sorted({sum(v!=0 for v in row)for row in M.tolist()})
assert support(tidy(A*uu*A.adjoint()))==[4]
# The beta wrapper itself is outside the square class in this b=D_c case.
beta_square=tidy(A*A*beta*(A*A).adjoint());assert support(beta_square)==[2]
services={'b':bb,'beta':beta,'u':uu,'f':ff,'q':S.adjoint(),'r':Ds[0]}
for name,M0 in list(services.items()):services[name+'^-1']=M0.adjoint()
def inv(name):return name[:-3]if name.endswith('^-1')else name+'^-1'
def shear(dst,src,name=None,sign=1):
 out=[]
 if name:out.append(['MONOMIAL',src,name])
 if sign==-1:out.append(['SCALE',src,'-1'])
 out.append(['ADD',src,dst])
 if sign==-1:out.append(['SCALE',src,'-1'])
 if name:out.append(['MONOMIAL',src,inv(name)])
 return out
def swap(i,j):return[['ADD',j,i],['SCALE',j,'-1'],['ADD',i,j],['SCALE',i,'-1'],['ADD',j,i],['SCALE',i,'-1']]
Cword=shear(0,1,'b')+swap(1,2)+shear(1,2)+[['MONOMIAL',2,'f']]+shear(2,0,'u')
Ciword=shear(2,0,'u',-1)+[['MONOMIAL',2,'f^-1']]+shear(1,2,sign=-1)+swap(1,2)+shear(0,1,'b',-1)
QAword=shear(1,0,'r')+shear(0,1,'q');QAiword=shear(0,1,'q',-1)+shear(1,0,'r',-1)
wrapper=shear(2,1,'beta',-1)+shear(2,0,sign=-1);wrapper_inverse=shear(2,0)+shear(2,1,'beta')
Qword=QAword+wrapper;Qiword=wrapper_inverse+QAiword
def replay(word):
 M=s.eye(48);bounds=[1,1,1];peak=1
 for op in word:
  if op[0]=='ADD':src,dst=op[1:];M[16*dst:16*(dst+1),:]=M[16*dst:16*(dst+1),:]+M[16*src:16*(src+1),:];bounds[dst]+=bounds[src]
  elif op[0]=='SCALE':M[16*op[1]:16*(op[1]+1),:]=-M[16*op[1]:16*(op[1]+1),:]
  else:M[16*op[1]:16*(op[1]+1),:]=services[op[2]]*M[16*op[1]:16*(op[1]+1),:]
  peak=max(peak,*bounds)
 return tidy(M),dict(Counter(op[0]for op in word)),peak
CM,cc,cp=replay(Cword);CiM,cic,cip=replay(Ciword);QM,qc,qp=replay(Qword);QiM,qic,qip=replay(Qiword)
Z=s.zeros(16);actualC=I.row_join(bb).row_join(Z).col_join(Z.row_join(I).row_join(I)).col_join(uu.row_join(ff+uu*bb).row_join(Z))
assert CM==actualC and tidy(CM*CiM)==tidy(CiM*CM)==s.eye(48)
qv,rv=services['q'],services['r'];pv=I+qv*rv;tv=I
actualQ=pv.row_join(qv).row_join(Z).col_join(rv.row_join(tv).row_join(Z)).col_join((-pv-beta*rv).row_join(-qv-beta*tv).row_join(I))
assert QM==actualQ and tidy(QM*QiM)==tidy(QiM*QM)==s.eye(48)
LL=A.row_join(Z).row_join(Z).col_join(I.row_join(A).row_join(Z)).col_join(Z.row_join(Z).row_join(I));UU=A.row_join(-A*A).row_join(Z).col_join(Z.row_join(A).row_join(Z)).col_join(Z.row_join(Z).row_join(I))
actualE=tidy(LL*CM*UU*QM*LL);assert actualE[16:32,:]==Z.row_join(Z).row_join(A)
assert actualE[0:16,32:48]==actualE[32:48,32:48]==Z
assert cc=={'MONOMIAL':5,'ADD':6,'SCALE':3}and cic=={'MONOMIAL':5,'SCALE':9,'ADD':6}
negative=[]
for word,label in [(Cword,'C'),(Qword,'Q')]:
 bad=list(word);k=next(i for i,op in enumerate(bad)if op[0]=='ADD');bad.pop(k)
 assert replay(bad)[0]!=(CM if label=='C'else QM);negative.append({'word':label,'omitted_ADD_rejected':True})
# Actual table metadata preserves the primitive monomial phases.
tables={}
for name,M0 in services.items():
 table=[]
 for j in range(16):
  nz=[i for i in range(16)if M0[i,j]!=0];assert len(nz)==1;i=nz[0];phase=next(e for e in range(4)if s.expand(M0[i,j]-s.I**e)==0);table.append([i,phase])
 tables[name]=table
words={'C':Cword,'C-INVERSE':Ciword,'Q':Qword,'Q-INVERSE':Qiword};word_pins={}
for name,word in words.items():
 data=(json.dumps({'schema':'independent-nonclean-idle-wrapper-control-v1','word':word,'literal_services':tables,'whole_field_owner_births':0},indent=2)+'\n').encode();(o.out/(name+'-WORD.json')).write_bytes(data);word_pins[name]=hashlib.sha256(data).hexdigest()
result={'status':'PASS_ROOT_NONCLEAN_TWO_BANK_REDUCTION_AND_PAID_WRAPPERS','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'free_noncommuting_exact_isolated_middle_row':True,'remaining_two_bank_equation_exact':True,'actual_b_beta':['D_c','D_d'],'actual_u':'S^-1 D_b','actual_f':'X_a','nonclean_forward_u_support':[4],'outside_square_beta_support':[2],'C_counts':cc,'C_inverse_counts':cic,'Q_counts_including_two_shear_QA':qc,'Q_inverse_counts_including_two_shear_QA':qic,'width_independent_coefficient_bound_by_triangle_inequality':{'C':cp,'C_inverse':cip,'Q':qp,'Q_inverse':qip},'word_sha256':word_pins,'negative_controls':negative,'scope':'Formal identities reviewed for every width; literal48-dimensional controls and actual primitive words are not a42 endpoint. The separately reviewed inverse-support cut excludes any independent rank4 remainder for every ordinary B and Q_A in this wrapper. All foundations and costs remain.'}
(o.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
