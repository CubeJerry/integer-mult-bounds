#!/usr/bin/env python3
"""Independent rational source/ordinary-word review of the routed same-plus column."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,hashlib,json
import sympy as sp
I=sp.I

def need(x,s):
 if not x:raise ValueError(s)
def clean(M):return sp.ImmutableSparseMatrix(M.applyfunc(sp.expand))
def tab(fn):
 entries={}
 for j in range(16):
  x=tuple((j>>k)&1 for k in range(4));out,p=fn(*x);entries[sum(b<<k for k,b in enumerate(out)),j]=I**(p%4)
 return sp.ImmutableSparseMatrix(16,16,entries)
def block(M):
 n=M[0][0].rows;data={}
 for i,row in enumerate(M):
  for j,B in enumerate(row):
   for (r,c),v in B.todok().items():
    if v:data[i*n+r,j*n+c]=v
 return sp.ImmutableSparseMatrix(n*len(M),n*len(M[0]),data)
def minus(A):return clean(-A)
def dictionary(M):
 rows=[{}for _ in range(M.rows)]
 for (r,c),v in M.todok().items():
  need(sp.im(v)==0,'ordinary unit real rational');rows[r][c]=Fraction(int(sp.re(v).p),int(sp.re(v).q))
 return rows
def serial(M):return{'rows':M.rows,'columns':M.cols,'nonzero_entries':[[r,c,str(sp.re(v)),str(sp.im(v))]for (r,c),v in sorted(M.todok().items())if v]}

def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/B/sameplus-routed-endpoint-column'));p.add_argument('--out',type=Path,default=Path(__file__).with_name('output'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 pins={f:hashlib.sha256((a.author/f).read_bytes()).hexdigest()for f in ['PROOF.md','check.py','output/WORDS.json']}
 need(pins['PROOF.md']=='904a4a1b2d859661a3d3a832e476977f78e64907bce4aafb02e8a63d7fe6ea1a','frozen author proof')
 need(pins['check.py']=='92e1cf3bb50f15a9611c23d49473082001efcfb37b09200eb46708c70fd0f3b3','frozen author checker')
 need(pins['output/WORDS.json']=='d6383fa3551678acd25850900b9bb87945cd8d7cf39dfc4e6d5a0aca661f94cf','frozen words')
 E16=sp.ImmutableSparseMatrix(sp.eye(16));E2=sp.ImmutableSparseMatrix(sp.eye(2))
 R=tab(lambda aa,b,c,d:((b,c,d,aa),2*aa*b*d));Xb=tab(lambda aa,b,c,d:((aa,b^1,c,d),0))
 A=clean(((1+I)*E16+(1-I)*Xb)*R/2)
 s=tab(lambda aa,b,c,d:((aa,b,d,c),0));s1=tab(lambda aa,b,c,d:((d,b,c,aa),0));s2=tab(lambda aa,b,c,d:((b,aa,c,d),0))
 R2=tab(lambda aa,b,c,d:((c,d,aa,b),2*aa*b*(c+d)))
 need(clean(A.conjugate().T*s*A)==s1,'first literal conjugation');need(clean((A.conjugate().T)**2*s*A**2)==s2,'second literal conjugation')
 need(clean(R*R)==R2 and clean(s*R2)==clean(R2*s2),'literal square address and cubic phase')
 need(clean(s*A*R)==clean(A*R*s2),'additional source transport, with phase retained')
 Zsigma=sp.ImmutableSparseMatrix([[1,0],[0,-1]]);Xsigma=sp.ImmutableSparseMatrix([[0,1],[1,0]])
 tail=clean(sp.kronecker_product(E2,A));R0=clean(sp.kronecker_product(E2,R));S=clean(sp.kronecker_product(Zsigma,s));S2=clean(sp.kronecker_product(Zsigma,s2));X=clean(sp.kronecker_product(Xsigma,E16))
 d=32;E=sp.ImmutableSparseMatrix(sp.eye(d));Z=sp.ImmutableSparseMatrix(sp.zeros(d));P=clean((E+S)/2);N=clean((E-S)/2);P2=clean((E+S2)/2);N2=clean((E-S2)/2)
 t2=clean(tail**2);t4=clean(tail**4);pp=clean(R0*N2);zz=clean(X*P2)
 need(clean(S*X)==clean(-X*S)and clean(S2*X)==clean(-X*S2),'genuine fixed prefix anticommutation')
 need(clean(P*tail*pp)==Z and clean(P*t2*zz)==Z,'exact killed source supports')
 need(clean(N*tail*pp)==clean(tail*pp)and clean(N*t2*zz)==clean(t2*zz),'exact retained source supports')
 need(clean(pp.conjugate().T*pp)==N2 and clean(zz.conjugate().T*zz)==P2,'orthogonal initial-domain split retained in full')
 need(clean(pp.conjugate().T*pp+zz.conjugate().T*zz)==E,'entire arbitrary bank retained')
 def shear(i,j,c):
  m=[[E if r==c0 else Z for c0 in range(3)]for r in range(3)];m[i][j]=clean(c*E);return block(m)
 def diagonal(xs):return block([[xs[i]if i==j else Z for j in range(3)]for i in range(3)])
 def swap(i,j,Pj):
  m=[[E if r==c else Z for c in range(3)]for r in range(3)];m[i][i]=m[j][j]=clean(E-Pj);m[i][j]=m[j][i]=Pj;return block(m)
 C=block([[P,Z,minus(N)],[P,E,minus(N)],[N,Z,P]])
 Q=clean(diagonal([R0,X,E])*swap(1,2,P2)*swap(0,2,N2));O=clean(shear(1,0,1)*shear(2,1,-1));In=clean(diagonal([E,X,R0])*swap(1,2,P2))
 invC=clean(block([[P,Z,N],[Z,E,Z],[minus(N),Z,P]])*shear(1,0,-1));invQ=clean(swap(0,2,N2)*swap(1,2,P2)*diagonal([R0.T,X,E]));invO=clean(shear(2,1,1)*shear(1,0,-1));invIn=clean(swap(1,2,P2)*diagonal([E,X,R0.T]))
 goals={'C':(C,invC),'Q0':(Q,invQ),'O':(O,invO),'I0':(In,invIn)}
 need(Q[:,2*d:3*d]==block([[pp],[zz],[Z]]),'actual full Q last column');need(In[:,2*d:3*d]==block([[Z],[zz],[pp]]),'actual independent endpoint input column')
 L=block([[tail,Z,Z],[E,tail,Z],[Z,Z,E]]);U=block([[tail,minus(t2),Z],[Z,tail,Z],[Z,Z,E]])
 middle=clean(L*C*U);source=clean(middle*Q*L);endpoint=clean(O*diagonal([t4,t2,tail])*In)
 transformed=clean(invO*middle)
 expected=block([[clean(tail*P*tail),minus(clean(tail*P*t2)),minus(clean(tail*N))],[clean(P*tail),clean(N*t2),minus(N)],[tail,Z,S]])
 need(transformed==expected,'entire changed middle-source identity')
 fullcol=block([[Z],[clean(t2*zz)],[clean(tail*pp-t2*zz)]])
 need(clean(shear(1,0,-1)*middle*Q)[:,2*d:3*d]==fullcol,'complete source column with no omitted classes')
 need(source[:,2*d:3*d]==endpoint[:,2*d:3*d],'whole arbitrary last-bank endpoint identity')
 delta=clean(source-endpoint);defects=[sum(bool(v)for (r,c),v in delta.todok().items()if j*d<=c<(j+1)*d)for j in range(3)]
 need(defects==[1786,1753,0],'all source defects remain explicit on the two uncompleted banks')
 # Independent literal ordinary-word interpreter: sparse rational rows.
 monos={'S':S,'S2':S2,'minus_S2':minus(S2),'X':X,'R0':R0,'R0_inverse':R0.T}
 tables={}
 for name,M in monos.items():
  destinations=[];signs=[]
  for j in range(d):
   items=[(r,M[r,j])for r in range(d)if M[r,j]];need(len(items)==1 and items[0][1]in[-1,1],'real signed monomial')
   r,z=items[0];destinations.append(r);signs.append(int(z))
  tables[name]=(destinations,signs)
 words=json.loads((a.author/'output/WORDS.json').read_bytes())['primitive_words']
 def replay(word,omit=None):
  rows=[{j:Fraction(1)}for j in range(3*d)];norms=[Fraction(1)]*3;peak=Fraction(1)
  for n,op in enumerate(word):
   if n==omit:continue
   if op['op']=='ADD':
    ti,si=op['target']*d,op['source']*d
    for r in range(d):
     dest=rows[ti+r].copy()
     for c,v in rows[si+r].items():dest[c]=dest.get(c,Fraction(0))+v
     rows[ti+r]={c:v for c,v in dest.items()if v}
    norms[op['target']]+=norms[op['source']]
   elif op['op']=='SCALE':
    bank=op['bank'];v=Fraction(op['coefficient'])
    for r in range(bank*d,(bank+1)*d):rows[r]={c:v*x for c,x in rows[r].items()if v*x}
    norms[bank]*=abs(v)
   elif op['op']=='MONO':
    off=op['bank']*d;ds,ss=tables[op['name']];old=rows[off:off+d]
    for j in range(d):rows[off+ds[j]]={c:ss[j]*v for c,v in old[j].items()}
   else:raise ValueError('unknown primitive')
   peak=max(peak,*norms)
  return rows,peak
 receipts={};rejected=[];identity_rows=[{j:Fraction(1)}for j in range(3*d)]
 for name,dirs in words.items():
  receipts[name]={}
  for num,direction in enumerate(['forward','inverse']):
   word=dirs[direction];rows,peak=replay(word);goal=dictionary(goals[name][num]);need(rows==goal,'all96 literal unit columns '+name+' '+direction)
   receipts[name][direction]={'counts':dict(Counter(o['op']for o in word)),'uniform_triangle_prefix_bound':str(peak)}
   for index,op in enumerate(word):
    if op['op']=='ADD':need(replay(word,index)[0]!=goal,'omitted ADD must fail');rejected.append([name,direction,index])
  need(replay(dirs['forward']+dirs['inverse'])[0]==identity_rows and replay(dirs['inverse']+dirs['forward'])[0]==identity_rows,'both actual primitive inverse orders')
 need(len(rejected)==38,'all38 independent ADD omissions')
 need(clean(P*tail*N2)!=Z,'R0 routing is required');need(clean(P*t2*P2)!=Z,'fixed prefix flip is required')
 result={'status':'PASS_INDEPENDENT_SAMEPLUS_ROUTED_COLUMN','author_pins':pins,'arithmetic':'independent SymPy rational sparse matrices and own sparse Fraction primitive interpreter',
  'all_unit_columns':96,'retained_complete_input_column_dimension':32,'both_inverse_orders_checked':True,
  'source_transports_checked':['A^-1 SWAP_cd A=SWAP_ad','A^-2 SWAP_cd A^2=SWAP_ab','R^2 literal phase','SWAP_cd A R=A R SWAP_ab'],
  'genuine_fixed_prefix_anticommutation':True,'entire_source_column_identity':True,'entire_gauged_middle_matrix_identity':True,
  'full_endpoint_defect_counts_by_bank':defects,'full_endpoint_not_established':True,'quartic_component_of_retained_column_is_zero':True,
  'primitive_receipts':receipts,'all_ADD_omission_controls':rejected,'omitted_R0_and_X_rejected':True,
  'scope':'Exact all-tail identity follows from checked one-column transports, genuine fixed prefix flip, and projector/unit algebra. Finite width1 complete unit/source checks corroborate it. Other input banks, full independent endpoint, normalization/target restoration and full caller costs remain open.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'SOURCE-IDENTITIES.json').write_text(json.dumps({'R':serial(R),'A':serial(A),'S':serial(S),'S2':serial(S2),'gauged_middle':serial(transformed),'last_source_column':serial(source[:,2*d:3*d])},indent=2)+'\n')
 print(result['status'],'all96columns,38controls,defects',defects,flush=True)
if __name__=='__main__':main()
