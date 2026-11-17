from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
# Rational D8 algebra: r^k f^e, with f r f = r^-1.
def norm(x):return {g:v for g,v in x.items()if v}
def add(*xs):
 z={}
 for x in xs:
  for g,v in x.items():z[g]=z.get(g,0)+v
 return norm(z)
def scale(x,c):return norm({g:v*c for g,v in x.items()})
def mul(x,y):
 z={}
 for(k,e),v in x.items():
  for(l,h),w in y.items():
   g=((k+(-1)**e*l)%4,(e+h)%2);z[g]=z.get(g,0)+v*w
 return norm(z)
one={(0,0):Q(1)};f={(0,1):Q(1)};t={(1,1):Q(1)};z=mul(mul(f,t),mul(f,t));assert mul(z,z)==one and mul(z,f)==mul(f,z)and mul(z,t)==mul(t,z)
half=lambda x:scale(x,Q(1,2));minus=lambda x:add(one,scale(x,-1));P=half(add(one,f));M=minus(P);T=half(add(one,t));Zp=half(add(one,z));Zm=minus(Zp);S0=add(Zm,mul(Zp,T));Rp=mul(P,S0);Rm=mul(M,S0);missing=mul(Zp,minus(T));identities=0
for R,B in [(Rp,P),(Rm,M)]:
 BT=mul(B,T)
 assert mul(R,R)==R;identities+=1
 assert mul(R,BT)==BT;identities+=1
 assert mul(BT,add(scale(mul(Zm,B),2),Zp))==R;identities+=1
assert mul(Rp,Rm)=={} and add(Rp,Rm,missing)==one and mul(missing,missing)==missing;identities+=3
assert missing==scale(add(one,z,scale(t,-1),scale(mul(z,t),-1)),Q(1,4));identities+=1
# Literal matrices built directly; no construction-author engine imported.
I=s.eye(16);i=s.I;clean=lambda X:X.applyfunc(s.expand)
def mono(tab):
 X=s.zeros(16)
 for col,(row,phase)in enumerate(tab):X[row,col]=i**(phase%4)
 return X
def table(fn):return[fn(*[(x>>j)&1 for j in range(4)])for x in range(16)]
rot=mono(table(lambda a,b,c,d:(b+2*c+4*d+8*a,2*a*b*d)));A=clean(((1+i)*I+(1-i)*mono([(x^2,0)for x in range(16)]))*rot/2)
R2=mono(table(lambda a,b,c,d:((c^(a*b))+2*d+4*a+8*b,a*b*(1+2*c+2*d))));Sab=mono(table(lambda a,b,c,d:(b+2*a+4*c+8*d,0)));J=clean(R2.H*Sab*R2);F=mono([(x,2*(x&1))for x in range(16)]);Fh=mono([(x,2*((x>>3)&1))for x in range(16)]);Zc=mono([(x,2*((x>>2)&1))for x in range(16)]);Scd=mono(table(lambda a,b,c,d:(a+2*b+4*d+8*c,0)))
assert clean(A*F*A.H)==Fh and F*J==J*F

def root4mono(X):
 out=[]
 for c in range(16):
  nz=[(r,X[r,c])for r in range(16)if X[r,c]!=0]
  if len(nz)!=1 or nz[0][1]not in [1,i,-1,-i]:return None
  out.append((nz[0][0],[1,i,-1,-i].index(nz[0][1])))
 return out if len(set(r for r,p in out))==16 else None
literal={}
for label,tau in [('unphased',Sab),('phase_balanced',Sab*Zc)]:
 rr=F*tau;zz=rr**2;group=[rr**k*F**e for k in range(4)for e in range(2)];assert len({tuple(x)for x in group})==8 and rr**4==I
 traces=[int(s.trace(x))for x in group];out0=clean(A*tau*A.H);out1=clean(A*J*tau*J*A.H);assert root4mono(out0)is not None and root4mono(out1)is not None
 PP=(I+F)/2;MM=I-PP;TT=(I+tau)/2;zp=(I+zz)/2;zm=I-zp;rp=PP*(zm+zp*TT);rm=MM*(zm+zp*TT)
 assert rp**2==rp and rm**2==rm and rp*PP*TT==PP*TT and rm*MM*TT==MM*TT
 formula=[]
 for V in [1,2,4,6,8]:
  D=16**V;defect=Q(D+int(s.trace(zz))**V-int(s.trace(tau))**V-int(s.trace(zz*tau))**V,4);assert defect.denominator==1
  if label=='unphased':assert D-defect==Q(3*D,4)+Q(8**V,2)
  else:assert D-defect==Q(3*D,4)
  formula.append({'V':V,'D':D,'row_range':int(D-defect),'missing':int(defect)})
 literal[label]={'traces':traces,'one_column_row_ranks':[int(s.trace(rp)),int(s.trace(rm))],'collective_rank_controls':formula,'forward_monomial_tables':[root4mono(out0),root4mono(out1)]}
assert literal['unphased']['one_column_row_ranks']==[8,8]and literal['unphased']['collective_rank_controls'][1]['row_range']==224
assert literal['phase_balanced']['one_column_row_ranks']==[6,6]
assert root4mono(clean(A*Scd*A.H))is None and root4mono(clean(A*J*Scd*J*A.H))is None
for sign in [1,-1]:
 for V in [2,4,6,8]:assert Q(16**V+16**V-(16*sign)**V-(16*sign)**V,4)==0
assert (16**6-2*14**6)//4==429536 and 16**6>2*14**6
assert max(abs(16-2*k)for k in range(1,16))==14
result={'status':'PASS_GENERAL_DIHEDRAL_ROW_RANGE','abstract_group_algebra_identities':identities,'literal_controls':literal,'universal_missing_rank':'(d^V+tr(z)^V-tr(t)^V-tr(zt)^V)/4','even_width_lower_bound':'(d^V-2(d-2)^V)/4','d16_first_uniform_even_width':6,'d16_bound_at_V6':429536,'negative_controls':{'unphased_V1_full_range_but_V2_defect':True,'unphased_zero_trace_claim_rejected':True,'scalar_t_hypothesis_essential':True,'spectator_forward_monomial_hypothesis_rejected':True},'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'scope':'Universal range proof plus exact retained-source application; fixed finite ordinary tensor catalogue and faithful large widths. No complete supplier or new kappa.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
