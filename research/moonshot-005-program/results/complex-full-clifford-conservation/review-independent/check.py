import itertools,json,hashlib
from pathlib import Path
import sympy as s

def dot(a,b):return (a&b).bit_count()%2
def symp(a,b):return dot(a&3,b>>2)^dot(a>>2,b&3)
def act(cols,v):
 z=0
 for k in range(4):
  if (v>>k)&1:z^=cols[k]
 return z
def q(v,t):return dot(v&3,v>>2)^dot(v,t)
odd=[t for t in range(16) if dot(t&3,t>>2)]
truth={tuple(q(v,t) for v in range(16)):i for i,t in enumerate(odd)}
def perm(cols):
 # Pull-forward q'(g v)=q(v), so rho(g)rho(h)=rho(gh).
 inv={act(cols,v):v for v in range(16)}
 return [truth[tuple(q(inv[v],t) for v in range(16))] for t in odd]
def pm(p):return s.Matrix(6,6,lambda i,j:int(i==p[j]))
Pperm=[next(j for j,u in enumerate(odd) if u!=t and u>>2==t>>2) for t in odd]
P=pm(Pperm);I=s.eye(6);Z=s.zeros(6)
def grank(cols):
 a,b=cols[2]&3,cols[3]&3
 return 0 if a==b==0 else (1 if a==0 or b==0 or a==b else 2)
hist={};ordinary=[];allg=[];pair_correspondence=[]
for w in range(1,16):
 ids=[i for i,t in enumerate(odd) if q(w,t)==0]
 assert len(ids)==2
 ta,tb=(odd[i] for i in ids)
 assert all(q(v,ta)^q(v,tb)==symp(w,v) for v in range(16))
 pair_correspondence.append({'pauli_vector':w,'odd_form_pair':ids})
assert len({tuple(e['odd_form_pair']) for e in pair_correspondence})==15
std=[1,2,4,8]
for cols in itertools.product(range(1,16),repeat=4):
 if any(symp(cols[i],cols[j])!=symp(std[i],std[j]) for i in range(4) for j in range(i+1,4)):continue
 r=grank(cols);p=perm(cols);M=pm(p);d=(M-P*M*P).rank();assert d==2*r,(cols,r,d)
 # The matching for gL shares exactly one edge per nonzero vector in L cap gL.
 moved={act(cols,v) for v in [0,4,8,12]};common=len(moved.intersection({0,4,8,12}))-1
 gp=[p[Pperm[p.index(i)]] for i in range(6)]
 edges=lambda a:{tuple(sorted((i,a[i]))) for i in range(6)}
 assert len(edges(Pperm).intersection(edges(gp)))==common
 hist[(r,d)]=hist.get((r,d),0)+1;allg.append(cols)
 if r==0:ordinary.append(cols);assert P*M==M*P
def physical_B(v):
 x=v&3;z=v>>2
 # P:(xa,xb)->(xa+xb,xa), z -> (zb,za+zb).
 xa,xb=x&1,x>>1;za,zb=z&1,z>>1
 xa,xb=xa^xb,xa;za,zb=zb,za^zb
 # CZ then square-root X_b.
 za,zb=za^xb,zb^xa
 xb^=zb
 return xa+2*xb+4*za+8*zb
Bcols=tuple(physical_B(v) for v in std);Bperm=perm(Bcols);R=pm(Bperm)
assert R**5==I
PP=s.diag(P,P);native=[]
for sigma,epsilon,c in itertools.product([-1,1],repeat=3):
 N=(R**sigma).row_join(c*R**(sigma+epsilon)).col_join(Z.row_join(R**sigma))
 d=(N-PP*N*PP).rank();assert d==4;native.append([sigma,epsilon,c,d])
 R0=R**sigma;R1=P*R0*P;A=R0-R1
 if sigma==epsilon:
  D=A.row_join(Z).col_join(Z.row_join(A))
  left=I.row_join(c*R1).col_join(Z.row_join(I))
  right=I.row_join(c*R0).col_join(Z.row_join(I))
  assert N-PP*N*PP==left*D*right
 else:assert N-PP*N*PP==A.row_join(Z).col_join(Z.row_join(A))
# Faithful-width negative control: a four-dimensional accidental relation
# cannot be pushed through the group-algebra representation at width one.
ii=s.I;I4=s.eye(4);Xb=s.Matrix(4,4,lambda i,j:int(i==(j^2)))
Cb=((1+ii)*I4+(1-ii)*Xb)/2
gl=s.Matrix(4,4,lambda i,j:int(i==[0,3,1,2][j]))
B=(ii*Cb*s.diag(1,1,1,-1)*gl).applyfunc(s.simplify)
assert sum([B**k for k in range(5)],s.zeros(4)).applyfunc(s.simplify)==s.zeros(4)
aux_trace=s.simplify(sum(s.trace(R**k)*s.trace(B**k) for k in range(5)))
assert aux_trace==20
assert P*R!=R*P
sharp_plus=R.row_join(R**2).col_join(Z.row_join(R))
sharp_minus=R.row_join(-R**2).col_join(Z.row_join(R))
assert sharp_plus*sharp_minus==(R**2).row_join(Z).col_join(Z.row_join(R**2))
assert (sharp_plus*sharp_minus-PP*sharp_plus*sharp_minus*PP).rank()==8
out={'status':'PASS_INDEPENDENT_FULL_CLIFFORD_MATCHING_CONSERVATION','engine':'independent odd-form enumeration and SymPy exact rational ranks; no author imports','sympy_version':s.__version__,'odd_forms':odd,'matching':Pperm,'group_order':len(allg),'ordinary_order':len(ordinary),'rank_histogram':{str(k):v for k,v in hist.items()},'B_columns':Bcols,'B_permutation':Bperm,'native_ranks':native,'pair_correspondence':pair_correspondence,'native_factorization_verified':True,'group_column_list_sha256':hashlib.sha256(json.dumps(allg,separators=(',',':')).encode()).hexdigest(),'sharp_two_native_rank':8,'negative_controls':{'incorrect_width_one_algebra_transfer_rejected_aux_trace':str(aux_trace),'paid_B_cannot_be_declared_ordinary':True},'full_all_width_proof':'finite matching identity plus faithful Clifford tensor algebra and auxiliary representation; computational controls are separated from universal invoice proof','new_kappa':False}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
