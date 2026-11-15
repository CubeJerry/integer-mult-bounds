from pathlib import Path
import itertools,json
import sympy as s

I=s.eye(8);ii=s.I
X=lambda a:s.Matrix(8,8,lambda i,j:int(i==(j^a)))
C=lambda a:((1+ii)*I+(1-ii)*X(a))/2
Ca,Cb,Cc=C(1),C(2),C(4)
S=s.Matrix(8,8,lambda i,j:int(i==[0,4,1,5,2,6,3,7][j]))
eq=lambda a,b:all(s.simplify(x-y)==0 for x,y in zip(a,b))
B=Cb*S
assert eq(S**3,I) and eq(S*Cb*S.inv(),Ca)
assert eq(Ca.inv()*S*Cb*S,S**2)
assert eq(Cb*S,B) and eq(S.inv()*Ca*S**2,B)
assert eq(S.inv()*S,I) and eq(Ca*Cb*S**2,B**2)
assert eq(B**3,Ca*Cb*Cc) and eq(B**6,X(1)*X(2)*X(4)) and eq(B**12,I)
powers=[]
for k in range(12):
 M=(B**k).applyfunc(s.simplify)
 counts={sum(x!=0 for x in M.row(i)) for i in range(8)}
 assert len(counts)==1
 support=counts.pop();rank={1:0,2:1,4:2,8:3}[support]
 assert rank==[0,1,2,3,2,1][k%6]
 powers.append({'power':k,'nonzero_entries_per_row':support,'gaussian_rank':rank})
# Root's independent odd-form reflection potential for the three-head escape.
def dot(a,b):return (a&b).bit_count()%2
def q(t,v):return dot(v&7,v>>3)^dot(t,v)
def act(cols,v):
 z=0
 for k in range(6):
  if (v>>k)&1:z^=cols[k]
 return z
odd=[t for t in range(64) if dot(t&7,t>>3)];assert len(odd)==28
truth={tuple(q(t,v) for v in range(64)):i for i,t in enumerate(odd)}
def perm(cols):
 inv={act(cols,v):v for v in range(64)}
 return [truth[tuple(q(t,inv[v]) for v in range(64))] for t in odd]
def pm(p):return s.Matrix(28,28,lambda i,j:int(i==p[j]))
P=s.Matrix(28,28,lambda i,j:s.Rational(1,2)*int(odd[i]>>3==odd[j]>>3)-int(i==j))
assert P*P==s.eye(28)
potential=[]
for r in range(4):
 cols=[1<<i for i in range(6)]
 for k in range(r):cols[k],cols[k+3]=cols[k+3],cols[k]
 M=pm(perm(cols));d=(M-P*M*P).rank()
 assert d==[0,6,10,12][r]
 potential.append({'gaussian_rank':r,'reflection_difference_rank':d})
# Ordinary generators: GL3 elementary additions and all symmetric phase axes.
ordinary=[]
for a,b in itertools.permutations(range(3),2):
 cols=[1<<i for i in range(6)];cols[b]^=1<<a;cols[a+3]^=1<<(b+3);ordinary.append(cols)
for a in range(3):
 cols=[1<<i for i in range(6)];cols[a]^=1<<(a+3);ordinary.append(cols)
for a,b in itertools.combinations(range(3),2):
 cols=[1<<i for i in range(6)];cols[a]^=1<<(b+3);cols[b]^=1<<(a+3);ordinary.append(cols)
for cols in ordinary:
 M=pm(perm(cols));assert P*M==M*P
# Two columns expose incorrect treatment of the field-level source minus.
lift=lambda M:s.kronecker_product(M,M)
assert eq(lift(Ca)*lift(Cb)*lift(S**2),lift(B)**2)
assert not eq(lift(-B**2),-lift(B)**2)
out={'status':'PASS_INDEPENDENT_THREE_HEAD_GAUGE_AND_ODD_REFLECTION','engine':'SymPy exact Gaussian-rational matrices; binary odd-form action; no author imports','sympy_version':s.__version__,'source_identities_checked':True,'rank_powers':powers,'ordinary_gauge_permutations_per_half':3,'new_gaussian_calls':0,'spectator_volume_factor':'2^V retained in source and target','field_level_minus_negative_control':True,'odd_forms':28,'ordinary_generator_checks':len(ordinary),'reflection_potential':potential,'potential_scope':'all-group extension uses the parabolic double-coset/partition proof, not these four representatives alone','no_new_kappa':True}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
