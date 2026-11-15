"""Independent sparse Gaussian-rational matrices, no author imports."""
from fractions import Fraction as F
Z=(F(0),F(0));O=(F(1),F(0));I=(F(0),F(1))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return(a[0],-a[1])
class M:
 def __init__(self,n,x):self.n=n;self.x={k:v for k,v in x.items()if v!=Z}
 def __eq__(self,b):return self.n==b.n and self.x==b.x
 def __add__(self,b):
  assert self.n==b.n;d=self.x.copy()
  for k,v in b.x.items():d[k]=add(d.get(k,Z),v)
  return M(self.n,d)
 def __neg__(self):return self.scale((-F(1),F(0)))
 def scale(self,z):return M(self.n,{k:mul(v,z)for k,v in self.x.items()})
 def __mul__(self,b):
  assert self.n==b.n;rows={}
  for(k,j),v in b.x.items():rows.setdefault(k,[]).append((j,v))
  out={}
  for(i,k),u in self.x.items():
   for j,v in rows.get(k,[]):out[i,j]=add(out.get((i,j),Z),mul(u,v))
  return M(self.n,out)
 def adj(self):return M(self.n,{(j,i):conj(v)for(i,j),v in self.x.items()})
 def tensor(self,b):return M(self.n*b.n,{(i*b.n+k,j*b.n+l):mul(u,v)for(i,j),u in self.x.items()for(k,l),v in b.x.items()})
 def trace(self):
  z=Z
  for i in range(self.n):z=add(z,self.x.get((i,i),Z))
  return z
 def powers(self,k):
  a=[ident(self.n)]
  for _ in range(k):a.append(a[-1]*self)
  return a
 def row_support(self):return [sum(i==r for i,j in self.x)for r in range(self.n)]
def ident(n):return M(n,{(i,i):O for i in range(n)})
def permutation(p):return M(len(p),{(p[i],i):O for i in range(len(p))})
def X(q):return permutation([i^(1<<q)for i in range(8)])
def ZZ(q):return M(8,{(i,i):((-F(1)if i>>q&1 else F(1)),F(0))for i in range(8)})
def phase(q):return M(8,{(i,i):(I if i>>q&1 else O)for i in range(8)})
def phasepower(k):return [O,I,neg(O),neg(I)][k%4]
def monomial(p,phases):return M(len(p),{(p[i],i):phasepower(phases[i])for i in range(len(p))})
def binaryrank(rows):
 B={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in B:x^=B[j]
   else:B[j]=x;break
 return len(B)
def pauli(x,z):
 return M(8,{(j^x,j):((-F(1)if (z&j).bit_count()%2 else F(1)),F(0))for j in range(8)})
def pauli_image(U,x,z):
 A=U*pauli(x,z)*U.adj();hits=[]
 for xx in range(8):
  for zz in range(8):
   B=pauli(xx,zz)
   for q in range(4):
    if A==B.scale(phasepower(q)):hits.append((xx,zz,q))
 assert len(hits)==1,hits
 return hits[0]
def mixing_rank(U):
 # Monomial unitaries preserve diagonal Z Paulis. Their X-exponent block
 # under conjugation is zero. Its exact binary rank is Gaussian rank.
 cols=[pauli_image(U,0,1<<q)[0]for q in range(3)]
 return binaryrank(cols),cols
