"""Complete corners and exact radical intervals; independent of prior code.
Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
from itertools import product
from collections import Counter
from math import isqrt
from pathlib import Path
import argparse,json

H=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))
def need(ok,message):
 if not ok:raise ValueError(message)
def norm2(v):return sum(x*x for x in v)
def parity(v):return sum(v)%2
def image2(v):return tuple(sum(a*b for a,b in zip(row,v)) for row in H)
def error4(x,y):return sum((2*b-a)**2 for a,b in zip(image2(x),y))
def corners(x):
 h=image2(x);need(all(t%2 for t in h),'half-integer image')
 return list(product(*[(t//2,t//2+1) for t in h]))
def gap_interval(m,n,bits):
 if m==n:return (0,0)
 hi,lo=max(m,n),min(m,n);a=isqrt(hi<<(2*bits));b=isqrt(lo<<(2*bits))
 return (max(0,a-b-1),a-b+1)
def unique_minimum(norms,n):
 for bits in (32,64,128,256,512,1024,2048,4096):
  spans={m:gap_interval(m,n,bits) for m in norms}
  winner=min(spans,key=lambda m:spans[m][1])
  if all(spans[winner][1]<lo for m,(lo,hi) in spans.items() if m!=winner):return winner,bits
 raise ValueError('radical comparison did not separate')
def mul(p,q):
 r=[0]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):r[i+j]+=x*y
 return r
def sub(p,q):
 r=[(p[i] if i<len(p) else 0)-(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))]
 while len(r)>1 and r[-1]==0:r.pop()
 return r
def matmul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)) for i in range(4))

def verify():
 need(matmul(H,H)==tuple(tuple(4*(i==j) for j in range(4)) for i in range(4)),'orthogonality')
 # Ascending polynomial coefficients, independent exact expansion.
 n=[3,0,4];m=[7,-2,4];l=[1,2,4]
 need(sub(mul(m,l),mul([2,0,4],[2,0,4]))==[3,12,12],'minimum comparison identity')
 need(sub(mul([0,0,16],m),mul(mul([-1,4],[-1,4]),n))==[-3,24,60],'derivative identity')
 R=((1,0,0,0),(0,-1,0,0),(0,0,1,0),(0,0,0,1))
 L=((1,0,0,0),(0,0,1,0),(0,0,0,-1),(0,1,0,0))
 C=((1,-1,1,1),(1,1,-1,1),(1,1,1,-1),(-1,1,1,1))
 need(matmul(matmul(L,C),R)==H,'Gaussian-pair signed transfer')
 cases=list(range(2,129))+[10**3,10**6,10**12,10**30,10**100];records=[];maxbits=0
 for a in cases:
  x=(2*a,1,1,1);n0=norm2(x);allpoints=corners(x)
  need(len(allpoints)==16 and all(error4(x,y)==4 for y in allpoints),'complete error-one corners')
  legal=[y for y in allpoints if parity(y)==parity(x)]
  need(len(legal)==8,'parity has eight corners')
  counts=Counter(map(norm2,legal));expected={n0-2*a:3,n0-2*a+4:1,n0+2*a-2:1,n0+2*a+2:3}
  need(counts==expected,'four exact squared norms/multiplicities')
  best,bits=unique_minimum(counts,n0);maxbits=max(maxbits,bits)
  ym=(a+2,a-1,a-1,a-1)
  need(best==n0-2*a+4 and counts[best]==1 and ym in legal,'exact unique inward minimum')
  need(error4(ym,x)==4,'inverse edge error')
  if a>2:need(best<n0,'local minimum does not force forward outward slack')
  v=(a+1,a,a,a-1);w=(a+2,a,a-1,a-1)
  need(error4(x,v)==4 and norm2(v)==n0-1 and parity(v)!=parity(x),'parity-free closer corner')
  need(error4(x,w)==4 and norm2(w)==n0+3 and parity(w)!=parity(x),'previous parity-flipping escape')
  if a>=3:need(norm2(v)>best,'dropping parity destroys local mu bound')
  if a>=4:
   need(gap_interval(norm2(w),n0,bits)[1]<gap_interval(best,n0,bits)[0],'escape gap below mu')
  if a in (2,3,4,8,128,10**6,10**30,10**100):records.append({'a':a,'n':n0,'minimum_squared_norm':best,
    'norm_multiplicities':[[k,counts[k]] for k in sorted(counts)],'radical_comparison_bits':bits,
    'minimum_radial_sign':0 if a==2 else -1})
 x=(6,1,1,1);legal=[y for y in corners(x) if parity(y)==parity(x)];ym=(5,2,2,2)
 remaining=[y for y in legal if y!=ym]
 need(len(remaining)==7,'missing-minimum mutation')
 false_minimum,_=unique_minimum(set(map(norm2,remaining)),norm2(x))
 need(false_minimum==43 and false_minimum!=norm2(ym),'missing corner did not change the inferred minimum')
 need(all(error4(x,y)>=4 for y in corners(x)),'strict-error-cap control')
 return {'marker':'PASS_PARITY_BILATERAL_GAUSSIAN_RADIUS','cases':len(cases),'range':[2,128],
  'large_a':[10**3,10**6,10**12,10**30,10**100],'maximum_radical_comparison_bits':maxbits,'records':records,
  'symbolic_identities':{'minimum_margin':[3,12,12],'derivative_margin':[-3,24,60]},
  'controls':['a2 minimum is zero','omitting the unique inward corner leaves seven candidates and changes the inferred minimum','parity-free n-1 corner beats mu for a>=3',
    'previous parity-flipping escape gap tends to zero','both edges need inclusive error cap1','local minimizing edge is inward and its inverse outward'],
  'scope':'Parity-preserving total maps have supremum absolute radial change at least1/2. For bijections this is a bilateral outward bound; no forward-only bound or global attainment is claimed.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();r=verify();dest=Path(__file__).with_name('RESULT.json')
 if args.write:dest.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 else:need(json.loads(dest.read_text())==r,'receipt drift')
 print('PASS_PARITY_BILATERAL_GAUSSIAN_RADIUS: complete eight-corner minimum and bilateral scope checked.')
