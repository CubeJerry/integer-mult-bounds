"""Portable support for unreviewed exact order-fifteen synthesis screens."""
import itertools
from fractions import Fraction as F

def app(A,v):
 z=0
 for j,c in enumerate(A):
  if v>>j&1:z^=c
 return z

def mul(A,B):return tuple(app(A,c)for c in B)
def rank(vs):
 p={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j not in p:p[j]=v;break
   v^=p[j]
 return len(p)
def inv3(B):return tuple(next(v for v in range(8)if app(B,v)==1<<i)for i in range(3))
def tr3(B):return tuple(sum(((B[j]>>i)&1)<<j for j in range(3))for i in range(3))


def pa(a,b):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,0)+v
 return {k:v for k,v in c.items()if v}
def pm(a,b):
 c={}
 for k,x in a.items():
  for l,y in b.items():c[k+l]=c.get(k+l,0)+x*y
 return {k:v for k,v in c.items()if v}
def mm(A,B):
 C=[[{}for _ in range(3)]for _ in range(3)]
 for i,j,k in itertools.product(range(3),repeat=3):C[i][j]=pa(C[i][j],pm(A[i][k],B[k][j]))
 return C


def augmentation_image(rows,n):
    piv={}
    for raw in sorted(rows,key=len):
        row={k:F(v) for k,v in raw.items() if v}
        while row:
            p=min(row);v=row[p]
            if p not in piv:piv[p]={k:x/v for k,x in row.items()};break
            for k,x in piv[p].items():
                z=row.get(k,F(0))-v*x
                if z:row[k]=z
                elif k in row:del row[k]
    residues=[]
    for i in range(9):
        row={j:F(1) for j in range(i,n,9)}
        for p,rel in sorted(piv.items()):
            if p not in row:continue
            v=row[p]
            for k,x in rel.items():
                z=row.get(k,F(0))-v*x
                if z:row[k]=z
                elif k in row:del row[k]
        assert not(set(row)&set(piv));residues.append(row)
    ab=[];ap={};free_examples=[]
    for f in sorted(set().union(*(set(r) for r in residues))):
        av=[r.get(f,F(0)) for r in residues];v={j:x for j,x in enumerate(av) if x}
        while v:
            p=min(v);x=v[p]
            if p not in ap:
                ap[p]={j:z/x for j,z in v.items()};ab.append(av);free_examples.append(f);break
            for j,z in ap[p].items():
                zz=v.get(j,F(0))-x*z
                if zz:v[j]=zz
                elif j in v:del v[j]
    return ab,free_examples,piv

def lift_free(piv,free_values):
    v={k:F(x) for k,x in free_values.items() if x}
    assert not(set(v)&set(piv))
    for p,row in sorted(piv.items(),reverse=True):
        z=-sum(c*v.get(k,F(0)) for k,c in row.items() if k!=p)
        if z:v[p]=z
    return v

def determinant_polynomial(basis):
    poly={}
    for perm in itertools.permutations(range(3)):
        sg=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        options=[[(k,b[3*i+perm[i]]) for k,b in enumerate(basis) if b[3*i+perm[i]]] for i in range(3)]
        for xs in itertools.product(*options):
            key=tuple(sorted(k for k,c in xs));v=F(sg)
            for k,c in xs:v*=c
            poly[key]=poly.get(key,F(0))+v
    return {k:v for k,v in poly.items() if v}

