"""Exact finite controls for the optional write-span lemmas (not their proof)."""
from itertools import product
import json

P=3
I=((1,0),(0,1));E=((1,1),(0,1));V=(1,1);LAM=(1,2)
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))%P for j in range(2)) for i in range(2))
def row(a,b):return tuple(sum(a[k]*b[k][j] for k in range(2))%P for j in range(2))
def mv(a,b):return tuple(sum(a[i][k]*b[k] for k in range(2))%P for i in range(2))
def det(a):return (a[0][0]*a[1][1]-a[0][1]*a[1][0])%P
def inv(a):
 d=pow(det(a),-1,P)
 return ((a[1][1]*d%P,-a[0][1]*d%P),(-a[1][0]*d%P,a[0][0]*d%P))
def sm(c,a):return tuple(tuple(c*x%P for x in r) for r in a)
def need(x,s):
 if not x:raise ValueError(s)
GL=[]
for x in product(range(P),repeat=4):
 a=(x[:2],x[2:])
 if det(a):GL.append(a)
need(len(GL)==48,'GL2 census')
checked=0
for pre in GL:
 for post in GL:
  # mu annihilates post*R; lambda annihilates R.
  mu=row(LAM,inv(post));lam_pre=row(LAM,pre)
  need(sum(mu[i]*mv(post,V)[i] for i in range(2))%P==0,'annihilator transport')
  # Required quotient equations cannot all hold for nonproportional E,I.
  need(any(sm(mu[c],E)!=sm(lam_pre[c],I) for c in range(2)),'improper span rescued by wrappers')
  checked+=1
# Necessary is not sufficient: independent write vectors may carry zero data.
need(det(((1,0),(0,1)))!=0 and I!=E,'full span does not force endpoint')
# Proportional exception: a scalar exit matrix supplies E=2M0 without core.
need(mm(sm(2,I),I)==sm(2,I) and sm(2,I)!=I,'proportional control')
# Independence matters: fixed selector F(x1,x2)=(E x1,E x1+x2-x1)
# is correct on x1=x2 while failing for independent x1=0,x2=(0,1).
for z in product(range(P),repeat=2):
 a=mv(E,z);b=tuple((a[i]+z[i]-z[i])%P for i in range(2))
 need(a==b,'diagonal-input positive control')
need((0,1)!=mv(E,(0,1)),'independent-input negative control')
# Interleaving escape with arbitrary dirty h: same raw direction e1 writes
# a shear in first bank, swap banks, repeat, then swap back.
def shear_first(banks,h):
 banks=[list(x) for x in banks];banks[0][0]-=h;h+=banks[0][1]
 banks[0][0]+=h;h-=banks[0][1]
 return tuple(tuple(x%P for x in r) for r in banks),h%P
interleaved=0
for z in product(range(P),repeat=5):
 banks=(z[:2],z[2:4]);dirty=z[4];old=banks
 banks,dirty=shear_first(banks,dirty);banks=(banks[1],banks[0])
 banks,dirty=shear_first(banks,dirty);banks=(banks[1],banks[0])
 need(banks==(mv(E,old[0]),mv(E,old[1])) and dirty==z[4],'interleaved escape')
 interleaved+=1
swap=((0,1),(1,0));e1=(1,0)
need(det((e1,mv(swap,e1)))!=0,'effective span is full')
print('PASS_INJECTION_SPAN_CONTROLS',json.dumps({'boundary_pairs':checked,'interleaved_dirty_inputs':interleaved,
 'full_span_sufficiency_rejected':True,'proportional_exception_retained':True,
 'independent_input_premise_tested':True,'raw_span_with_interleaving_rejected':True,'new_kappa':False},sort_keys=True))
