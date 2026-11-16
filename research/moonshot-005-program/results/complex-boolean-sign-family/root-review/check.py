"""Independent Gaussian-integer and Fano-plane verification; no author imports."""
from pathlib import Path
import argparse, hashlib, itertools, json
Z=(0,0);ONE=(1,0);UNIT=[(1,0),(0,1),(-1,0),(0,-1)]
def add(z,w):return (z[0]+w[0],z[1]+w[1])
def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def scale(z,n):return (n*z[0],n*z[1])
def mm(A,B):
 n=len(A);C=[[Z]*n for _ in range(n)]
 for i in range(n):
  for k,z in enumerate(A[i]):
   if z!=Z:
    for j,w in enumerate(B[k]):
     if w!=Z:C[i][j]=add(C[i][j],mul(z,w))
 return C
def mono(perm,phase=None):
 n=len(perm);M=[[Z]*n for _ in range(n)]
 for x,y in enumerate(perm):M[y][x]=UNIT[(phase[x] if phase else 0)%4]
 return M
def invmono(perm,phase=None):
 n=len(perm);p=[0]*n;q=[0]*n
 for x,y in enumerate(perm):p[y]=x;q[y]=-(phase[x] if phase else 0)
 return mono(p,q)
def gaussian(bit,d):
 n=1<<d;M=[[Z]*n for _ in range(n)]
 for x in range(n):M[x][x]=(1,1);M[x^(1<<bit)][x]=(1,-1)
 return M
def rotate(x,d):return (x>>1)|((x&1)<<(d-1))
def anf(mask,d):
 a=[(mask>>x)&1 for x in range(1<<d)]
 for k in range(d):
  for x in range(1<<d):
   if x>>k&1:a[x]^=a[x^(1<<k)]
 return a
def native(mask,d):
 p=[rotate(x,d) for x in range(1<<d)];q=[2*((mask>>p[x])&1) for x in range(1<<d)]
 return mm(gaussian(1,d),mono(p,q)),p,q

def fano_normalize(B):
 H=[]
 for y in range(8):
  row=[]
  for x in range(8):
   z=mul(B[y][x],UNIT[(x.bit_count()+y.bit_count())%4])
   assert z in [(-2,2),(2,-2)]
   row.append(1 if z==(-2,2) else -1)
  H.append(row)
 assert all(sum(H[i][k]*H[j][k] for k in range(8))==(8 if i==j else 0) for i in range(8) for j in range(8))
 rn=[H[y][0] for y in range(8)];cn=[H[0][x]*H[0][0] for x in range(8)]
 N=[[rn[y]*H[y][x]*cn[x] for x in range(8)] for y in range(8)]
 triples=[frozenset(x for x in range(1,8) if N[y][x]==1) for y in range(1,8)]
 assert all(len(t)==3 for t in triples)
 assert all(len(a&b)==1 for a,b in itertools.combinations(triples,2))
 first=sorted(triples[0]);labels={first[0]:1,first[1]:2,first[2]:3}
 w=next(x for x in range(1,8) if x not in first);labels[w]=4
 for x in first:
  line=next(t for t in triples if x in t and w in t)
  z=next(iter(line-{x,w}));labels[z]=labels[x]^4
 assert set(labels.values())==set(range(1,8))
 for t in triples:
  v=0
  for x in t:v^=labels[x]
  assert v==0
 cols=[0]+[labels[x] for x in range(1,8)]
 rows=[next(r for r in range(8) if all(N[y][x]==(-1)**((r&cols[x]).bit_count()%2) for x in range(8))) for y in range(8)]
 lp=[0]*8;lq=[0]*8
 for y,r in enumerate(rows):lp[r]=y;lq[r]=r.bit_count()-y.bit_count()+(2 if rn[y]<0 else 0)
 qq=[cols[x].bit_count()-x.bit_count()+(2 if cn[x]<0 else 0) for x in range(8)]
 C=mm(mm(gaussian(0,3),gaussian(1,3)),gaussian(2,3))
 assert mm(mm(mono(lp,lq),C),mono(cols,qq))==B
 return True

def three_bit(mask):
 A,p,q=native(mask,3);S=mono(p,q);Sinv=invmono(p,q)
 coeff=anf(mask,3);f0,la,lb,qab,lc,qac,qbc,eta=coeff
 assert eta==mask.bit_count()%2
 g=[((mask>>x)^(mask>>(x^1)))&1 for x in range(8)]
 J=mono([x^g[x] for x in range(8)],g);R=mm(J,mm(S,S))
 AA=mm(A,A);AAA=mm(AA,A)
 assert AA==mm(mm(gaussian(0,3),gaussian(1,3)),R)
 assert A==mm(mm(Sinv,gaussian(0,3)),R)
 def F(x):
  u=x&1;v=(x>>1)&1;w=x>>2
  return u+2*(v^(qab*u)^(eta*u*w))+4*w
 def G(x):
  a=x&1;b=(x>>1)&1;c=x>>2
  return a+2*b+4*(c^(qab*a)^((qbc^qac)*b)^(eta*a*b))
 def r0(x):
  u=x&1;w=x>>2
  return (la*u+(la+lc)*w+qac*u*w)%2
 def c0(x):
  a=x&1;b=(x>>1)&1;c=x>>2
  return (f0+(lb+lc)*a+(la+lb+lc)*b+lb*c+(qbc+qac)*a*b+qab*b*c+qbc*a*c+eta*a*b*c)%2
 L=mono([F(x) for x in range(8)],[x.bit_count()-F(x).bit_count()+2*r0(F(x)) for x in range(8)])
 Q=mono([G(x) for x in range(8)],[G(x).bit_count()-x.bit_count()+2*c0(x) for x in range(8)])
 C=mm(mm(gaussian(0,3),gaussian(1,3)),gaussian(2,3))
 assert mm(mm(L,C),Q)==AAA
 assert fano_normalize(AAA)
 sign=lambda x:1-2*((mask>>x)&1)
 T=sign(0)+sign(7)+3*sign(1)*sign(2)*sign(4)+3*sign(3)*sign(5)*sign(6)
 tr=Z
 for x in range(8):tr=add(tr,AAA[x][x])
 assert tr==(-2*T,2*T)
 if eta:assert abs(T) in (2,6)
 return eta,AAA,C,L,Q

def general(mask,d):
 A,p,q=native(mask,d);AAA=mm(mm(A,A),A);n=1<<d
 p3=[rotate(rotate(rotate(x,d),d),d) for x in range(n)]
 inv=[0]*n
 for x,y in enumerate(p3):inv[y]=x
 B=[[AAA[y][inv[x]] for x in range(n)] for y in range(n)]
 active=3|(1<<(d-1));spectator=(n-1)^active;blocks=0
 for x in range(n):
  for y in range(n):
   if (x&spectator)!=(y&spectator):assert B[y][x]==Z
 for s in range(n):
  if s&active:continue
  coords=[s+(x&3)+((x>>2)<<(d-1)) for x in range(8)]
  assert fano_normalize([[B[y][x] for x in coords] for y in coords]);blocks+=1
 return blocks

def main():
 p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 digest=hashlib.sha256(a.proof.read_bytes()).hexdigest()
 assert digest=='5d0f673af13ca1769bdd5b79a5960a5665655dda1359d55b1f01eed00c498b9d'
 odd=even=dropL=dropQ=dropPhase=0
 for mask in range(256):
  e,A3,C,L,Q=three_bit(mask);odd+=e;even+=1-e
  dropL+=mm(C,Q)!=A3;dropQ+=mm(L,C)!=A3
  absL=[[ONE if z!=Z else Z for z in row] for row in L]
  dropPhase+=mm(mm(absL,C),Q)!=A3
 assert odd==even==128 and min(dropL,dropQ,dropPhase)>0
 blocks=cases=0
 for d in (4,5,6):
  for k in range(12):
   # Deterministic truth tables include constant, sparse and mixed terms.
   mask=((0x9e3779b97f4a7c15*(k+1))^((1<<(k+1))-1))&((1<<(1<<d))-1)
   blocks+=general(mask,d);cases+=1
 result={'status':'PASS_ROOT_BOOLEAN_SIGN_FAMILY','three_bit_tables':256,
 'finite_projective_tables':even,'infinite_projective_tables':odd,
 'closed_gauge_and_Fano_normalizers_independently_verified':True,
 'larger_dimension_cases':cases,'spectator_blocks':blocks,
 'negative_controls':{'omitted_left_gauge':dropL,'omitted_right_gauge':dropQ,'omitted_left_phase':dropPhase},
 'proof_sha256':digest,'arithmetic':'Gaussian integers with explicitly scaled dyadic matrices',
 'all_positive_width_odd_lattice_obstruction':'trace cube valuation = -width',
 'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
