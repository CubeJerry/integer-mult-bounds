"""Independent rational price engine, integer bisection instead of Newton."""
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
SCALE=10**30
@lru_cache(None)
def power(r):
 if r==0:return F(0),F(0)
 value=r**199*SCALE**200;lo=0;hi=1<<((value.bit_length()+199)//200)
 while hi-lo>1:
  x=(lo+hi)//2
  if x**200<=value:lo=x
  else:hi=x
 assert lo**200<=value<(lo+1)**200
 return F(lo,SCALE),F(lo if lo**200==value else lo+1,SCALE)
def combine(*items):
 ans=Counter()
 for a,p in items:
  for r,n in p.items():ans[int(r)]+=a*n
 return {r:a for r,a in ans.items()if a}
def moment(profile):
 lo=hi=F(0)
 for r,a in profile.items():
  l,u=power(int(r));lo+=a*(l if a>=0 else u);hi+=a*(u if a>=0 else l)
 return lo,hi
def budget(profile):
 B={127:F(37,6),64:F(74,6),1:F(-74,6)}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,F(0))+F(74,6);B[7*j]=B.get(7*j,F(0))-F(74,6)
 gap=moment(combine((1,B),(-1,profile)));N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
 def margin(m):return moment(combine((18*m,B),(-18,N),(18,H),(-18*(m-1),profile)))
 first=None
 if gap[0]>0:
  hi=2
  while margin(hi)[0]<=0:hi*=2
  lo=0
  while hi-lo>2:
   x=2*((hi+lo)//4)
   if margin(x)[0]>0:hi=x
   else:assert margin(x)[1]<=0;lo=x
  first=hi
  if first>2:assert margin(first-2)[1]<0
 def enc(z):return {'lower_fraction':str(z[0]),'upper_fraction':str(z[1]),'display_lower':format(float(z[0]),'.16f'),'display_upper':format(float(z[1]),'.16f')}
 return {'moment':enc(moment(profile)),'limiting_room':enc(gap),'first_positive_even_m':first,'first_margin':enc(margin(first))if first else None,'method':'integer bisection of200th roots at scale10^30; displays noncertifying'}
