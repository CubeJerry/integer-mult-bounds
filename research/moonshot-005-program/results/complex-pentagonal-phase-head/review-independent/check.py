from pathlib import Path
import hashlib,json
import sympy as s
I=s.eye(4);ii=s.I
X=lambda a:s.Matrix(4,4,lambda r,c:int(r==(c^a)))
C=lambda a:((1+ii)*I+(1-ii)*X(a))/2
Ca,Cb=C(1),C(2)
P=s.zeros(4)
for j,k in enumerate([0,3,1,2]):P[k,j]=1
S=s.diag(1,1,1,-1)*P;R=(Ca.inv()*S*Cb*S).applyfunc(s.simplify)
B=(ii*Cb*S).applyfunc(s.simplify);G1=ii*S;G2=-R;H2=-ii*S.inv()
eq=lambda a,b:all(s.simplify(x-y)==0 for x,y in zip(a,b))
need=lambda x:None if x else (_ for _ in ()).throw(ValueError('exact identity failed'))
need(eq(B**5,I));need(eq(B.conjugate().T,B**4))
need([s.simplify(s.trace(B**k)) for k in range(1,5)]==[-1]*4)
need(eq(Cb*G1,B));need(eq(H2*G1,I));need(eq(H2*Ca*G2,B));need(eq(Ca*Cb*G2,B**2))
need(eq(R,s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,-ii,0],[0,-ii,0,0]])))
widths=[]
for V in [1,2,3]:
 lift=lambda M:s.kronecker_product(*([M]*V))
 bv,ca,cb,g1,g2,h2=map(lift,[B,Ca,Cb,G1,G2,H2]);identity=s.eye(4**V)
 need(eq(cb*g1,bv));need(eq(h2*g1,identity));need(eq(h2*ca*g2,bv));need(eq(ca*cb*g2,bv*bv))
 widths.append({'V':V,'dimension':4**V,'all_four_input_columns':True})
B2=s.kronecker_product(B,B);total=sum([B2**k for k in range(5)],s.zeros(16)).applyfunc(s.simplify)
need(eq(total*total,5*total));need(s.simplify(s.trace(total))==20);need(total.rank()==4)
need(not eq(total,s.zeros(16)));need(not eq(s.kronecker_product(-B**2,-B**2),-B2**2))
wrong=(ii*Cb*P).applyfunc(s.simplify);need(not eq(wrong**5,I))
result={'status':'PASS_INDEPENDENT_PENTAGONAL_NATIVE_GAUGE','engine':'independent SymPy matrices; no author imports','sympy_version':s.__version__,'width_controls':widths,'cyclic_width2_projector_rank':4,'source_minus_tensored_control_rejected':True,'quadratic_phase_omission_rejected':True,'phase_lift':'whole-field source minus retained outside tensor power','no_new_kappa':True}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
