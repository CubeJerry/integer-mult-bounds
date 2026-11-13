"""Independent dense integer dyadic engine, copied from our admitted kernel review."""
import collections
from fractions import Fraction as F
if not __debug__:raise SystemExit("Exact checks require Python without -O")
def span(f):
 a={0}
 for x in f:
  assert 0<x<512;a|={z^x for z in tuple(a)}
 assert len(a)==1<<len(f);return frozenset(a)
def eqrow(a,da,b,db):
 d=max(da,db);return all((x<<(d-da))==(y<<(d-db)) for x,y in zip(a,b))
def run(w,spaces,capture_before=None,capture_after=None,purity=None):
 n=w['public'];assert n==400 and len(w['initial'])==n and all(0<=c<len(spaces) for c in w['initial']);loc=dict(enumerate(w['initial']));rows={i:[int(i==j) for j in range(n)] for i in range(n)};D=0
 cnt=collections.Counter();paid=collections.Counter();life=peak=cleared_nonzero=rescalings=0;snap={};capture_before=capture_before or {};capture_after=capture_after or {};purity=purity or [];expected={}
 def save(label,ids):snap[label]=(D,{i:rows[i].copy() for i in ids},{i:loc[i] for i in ids})
 def scale_all(k):
  nonlocal D,rescalings
  D+=k;rescalings+=1
  for i in rows:rows[i]=[v<<k for v in rows[i]]
 for t,e in enumerate(w['program']):
  if t in capture_before:
   label,ids=capture_before[t];save(label,ids)
  op,i=e[:2];assert 0<=i<n+w['owned_fields'];cnt[op]+=1
  if op=='INIT':
   assert i>=n and i not in loc and 0<=e[2]<len(spaces);loc[i]=e[2];rows[i]=[0]*n;life+=1
  elif op=='CLEAR':
   assert i>=n and i in loc and loc[i]==e[2];cleared_nonzero+=any(rows[i]);del rows[i];del loc[i]
  elif op=='MOVE':
   a,b,owned=e[2:];assert 0<=a<len(spaces) and 0<=b<len(spaces);assert type(owned)is bool and owned==(i>=n) and loc.get(i)==a
   assert spaces[a]<spaces[b] or owned and spaces[b]<spaces[a];paid[abs(len(spaces[a]).bit_length()-len(spaces[b]).bit_length())]+=1;loc[i]=b
  elif op in ('ADD','COPY'):
   j,c,at=e[2:];assert i!=j and loc.get(i)==loc.get(j)==at
   if op=='COPY':assert not any(rows[i])
   c=F(c);den=c.denominator;assert den&(den-1)==0
   if any((c.numerator*v)%den for v in rows[j]):scale_all(den.bit_length()-1)
   rows[i]=[x+c.numerator*y//den for x,y in zip(rows[i],rows[j])]
  elif op=='SCALE':
   c=F(e[2]);assert c and loc.get(i)==e[3];den=c.denominator;assert den&(den-1)==0
   if any((c.numerator*v)%den for v in rows[i]):scale_all(den.bit_length()-1)
   rows[i]=[c.numerator*v//den for v in rows[i]]
  else:raise AssertionError(op)
  peak=max(peak,len(loc)-n)
  for r,begin,end,chart,coeff in purity:
   if begin<=t<end:
    assert loc.get(r)==chart
    key=(D,tuple(sorted(coeff.items())))
    if key not in expected:expected[key]=[int(coeff.get(j,0))<<D for j in range(n)]
    assert rows[r]==expected[key],('pure-original functional',t,r)
  if t in capture_after:
   label,ids=capture_after[t];save(label,ids)
 assert set(loc)==set(rows)==set(range(n))
 return rows,D,loc,{'instructions':len(w['program']),'counts':dict(cnt),'moves':dict(sorted(paid.items())),'lifetimes':life,'peak':peak,'nonzero_owned_clears':cleared_nonzero,'common_dyadic_exponent':D,'global_rescalings':rescalings},snap
