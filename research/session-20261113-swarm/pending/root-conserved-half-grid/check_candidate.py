"""Independent integer checking of the sum-preserving two-dimensional matching variant."""
from itertools import product
from fractions import Fraction
import json,random

def need(ok,msg):
 if not ok:raise ValueError(msg)
def J(x):return(-x[1],x[0])
def B(x):return(x[0]+x[1],x[0]-x[1])
def norm(x):return sum(t*t for t in x)
def pair2(v,phase):
 need(v.denominator==2,'strict half coordinate')
 a=abs(v);sgn=1 if v>0 else -1
 if phase==1 and a==Fraction(1,2):return Fraction(0),-v
 index=(a-Fraction(1 if phase==0 else 3,2))//2
 lower=2*index+Fraction(1 if phase==0 else 3,2)
 need(lower>0 and a in [lower,lower+1],'line pairing')
 return lower,sgn*(lower+1 if a==lower else lower)
def M(v,p):
 cells=[pair2(v[0],p),pair2(v[1],1-p)]
 need(cells[0][0]!=cells[1][0],'cross-phase score uniqueness')
 i=0 if cells[0][0]<cells[1][0] else 1
 z=list(v);z[i]=cells[i][1];return tuple(z)
def transform(x,inverse=False):
 s=(x[0]+x[2],x[1]+x[3]);d=(x[0]-x[2],x[1]-x[3]);p=s[0]%2
 if s[0]%2==s[1]%2:
  z=J(d);z=tuple(-a for a in z) if inverse else z
 else:
  if not inverse:
   j=J(d);t=tuple(Fraction(a,2) for a in B(j));z=B(M(t,p))
  else:
   t=tuple(Fraction(a,2) for a in B(d));z=tuple(-a for a in J(B(M(t,p))))
 out=tuple(Fraction(s[i]+sign*z[i],2) for sign in [1,-1] for i in range(2))
 need(all(a.denominator==1 for a in out),'integer outputs')
 return tuple(int(a) for a in out)
def ip(x):return(-x[1],x[0],-x[3],x[2])
def conj(x):return(x[0],-x[1],x[2],-x[3])
def swap(x):return(x[2],x[3],x[0],x[1])
C2=((1,-1,1,1),(1,1,-1,1),(1,1,1,-1),(-1,1,1,1))
def check(x):
 y=transform(x)
 need(transform(y,True)==x and transform(transform(x,True))==x,'both inverse identities')
 need((x[0]+x[2],x[1]+x[3])==(y[0]+y[2],y[1]+y[3]),'complex sum')
 need(transform(ip(x))==ip(y),'global i covariance')
 need(transform(conj(x))==conj(transform(x,True)),'conjugation relates inverse')
 need(transform(swap(x))==swap(y),'wire swap')
 ideal2=tuple(sum(a*b for a,b in zip(row,x)) for row in C2)
 err4=sum((2*a-b)**2 for a,b in zip(y,ideal2))
 need(err4==(0 if (x[0]+x[2])%2==(x[1]+x[3])%2 else 4),'sharp error by sum parity')
 m,n=norm(y),norm(x);D=2*m+2*n-1;need(D<=0 or D*D<=16*m*n,'bilateral radius1/sqrt2')
 return y

def main():
 count=0;images=set();counter=None
 for x in product(range(-4,5),repeat=4):
  images.add(check(x));count+=1
  if counter is None:
   z=x
   for _ in range(4):z=transform(z)
   if z!=x:counter={'x':x,'fourth_power':z}
 need(len(images)==count,'finite injectivity')
 rng=random.Random(20261113);large=0
 for digits in [1,10,100,400]:
  for j in range(15):
   x=tuple(rng.randrange(-10**digits,10**digits) for _ in range(4));check(x);large+=1
 print(json.dumps({'status':'PASS_ROOT_CONSERVED_PHASE_COVARIANT_CANDIDATE','cube_cases':count,'large_cases':large,'max_decimal_digits':400,'seed':20261113,'distinct_images':len(images),'fourth_power_failure':counter,'scope':'finite corroboration of explicit proof candidate; no selected caller or tape tariff'},indent=2))
if __name__=='__main__':main()
