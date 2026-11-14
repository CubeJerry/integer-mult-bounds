#!/usr/bin/env python3
"""Independent SymPy exact matrix verification; no worker implementation."""
import json,itertools
import sympy as s

def order(n,d,l):
 seen=set();xs=[];starts=[];lengths=[]
 for x in itertools.product(range(n),repeat=d):
  if x in seen:continue
  starts.append(len(xs));y=x
  while y not in seen:
   seen.add(y);xs.append(y);y=y[1:l]+(n-1-y[0],)+y[l:]
  if y!=x:raise ValueError('orbit closure')
  lengths.append(len(xs)-starts[-1])
 return xs,starts,lengths

def disp(h):
 z=s.zeros(h.rows)
 for i in range(1,h.rows):z[i,i-1]=1
 return h-z*h*z.T

def supported(e,starts):return all(e[i,j]==0 for i in range(e.rows) for j in range(e.cols) if i not in starts and j not in starts)

def main():
 rows=[]
 for n,d,q in [(2,1,s.Rational(1,2)),(2,2,s.Rational(1,2)),(2,3,s.Rational(1,2)),(2,4,s.Rational(1,2)),(4,2,s.Rational(1,2)),(2,4,s.Rational(2,3))]:
  l=1<<(d.bit_length()-1);xs,starts,lengths=order(n,d,l)
  if set(lengths)!={2*l}:raise ValueError('uniform orbit')
  h=s.Matrix([[q**sum((a-b)**2 for a,b in zip(x,y)) for y in xs] for x in xs]);hi=h.inv();ranks=[]
  for a in (h,hi):
   e=disp(a)
   if not supported(e,starts):raise ValueError('Stein support')
   if any(sum(e[i-k,j-k] for k in range(min(i,j)+1))!=a[i,j] for i in range(a.rows) for j in range(a.cols)):raise ValueError('telescoping')
   r=e.rank()
   if r>2*len(starts):raise ValueError('rank bound')
   ranks.append(r)
  rows.append(dict(n=n,d=d,q=str(q),ell=l,orbits=len(starts),ranks=ranks,bound=2*len(starts)))
 controls=[]
 for n,d,l,label in [(2,3,3,'nonpower cycle'),(3,2,2,'odd alphabet')]:
  ls=order(n,d,l)[2]
  if set(ls)=={2*l}:raise ValueError('orbit control escaped')
  controls.append(dict(control=label,lengths=sorted(set(ls)),detected=True))
 xs,starts,_=order(2,4,4)
 for qs,ys,label in [([s.Rational(1,2)]*3+[s.Rational(1,3)],xs,'unequal factors'),([s.Rational(1,2)]*4,[xs[0],xs[2],xs[1]]+xs[3:],'interior order mutation')]:
  h=s.Matrix([[s.prod(q**((a-b)**2) for q,a,b in zip(qs,x,y)) for y in ys] for x in ys])
  if supported(disp(h),starts):raise ValueError('symmetry control escaped')
  controls.append(dict(control=label,detected=True))
 print(json.dumps(dict(status='PASS_INDEPENDENT_ORBIT_EXACT',sympy=s.__version__,cases=rows,controls=controls),indent=2))
if __name__=='__main__':main()
