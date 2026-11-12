#!/usr/bin/env python3
"""Independent Q9 reconstruction, sparse source replay, and full late-packet bill.
No author constructor, author audit, or cohort-reconstruction helper is imported.
"""
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
PAYLOAD='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
WORD='64582bf3eb558f46bcefb62990114487cf313094b4b0609d240d92cf2ee2aeab'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
NORMALS=[7,25,52,76,97,127,42,82]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(a):
 s={0}
 for x in a:s|={y^x for y in tuple(s)}
 return frozenset(s)
def rowplus(a,b,c=F(1)):
 r=a.copy()
 for k,v in b.items():
  q=r.get(k,F(0))+c*v
  if q:r[k]=q
  else:r.pop(k,None)
 return r
def root9(v):
 T=[i for i in range(9) if v>>i&1]
 if len(T)==3:return [2 if i in T else -1 for i in range(9)]
 need(len(T)==7,'source root type');i,j=[k for k in range(9) if k not in T]
 return [3*(int(k==i)-int(k==j)) for k in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def replay(w,spaces,stop=None,arithmetic=False):
 loc=dict(enumerate(w['initial']));rows={i:{i:F(1)} for i in range(1880)} if arithmetic else None
 count=Counter();ranks=Counter();rawranks=Counter();raw=set(w['private_role_map'].values());peak=0;lifetimes=0
 for k,e in enumerate(w['program'][:stop] if stop is not None else w['program']):
  op,r=e[:2];count[op]+=1;need(0<=r<1880+w['owned_fields'],'declared role')
  if op=='INIT':
   need(r>=1880 and r not in loc,'fresh owner');loc[r]=e[2];lifetimes+=1
   if arithmetic:rows[r]={}
  elif op=='CLEAR':
   need(r>=1880 and loc.get(r)==e[2],'owned retirement');del loc[r]
   if arithmetic:del rows[r]
  elif op=='MOVE':
   x,y,o=e[2:];need(type(o)is bool and o==(r>=1880) and loc.get(r)==x,'typed route at '+str(k));need(spaces[x]<spaces[y] or o and spaces[y]<spaces[x],'proper nested route at '+str(k))
   dim=abs((len(spaces[x]).bit_length()-1)-(len(spaces[y]).bit_length()-1));ranks[dim]+=1;rawranks[dim]+=int(r in raw);loc[r]=y
  elif op=='SCALE':
   c=F(e[2]);need(c and loc.get(r)==e[3],'nonzero local scale')
   if arithmetic:rows[r]={j:c*v for j,v in rows[r].items()}
  elif op in ('ADD','COPY'):
   z,c,at=e[2:];need(z!=r and loc.get(z)==loc.get(r)==at,'cochart read at '+str(k))
   if arithmetic:
    need(op!='COPY' or not rows[r],'COPY zero guard');rows[r]=rowplus(rows[r],rows[z],F(c))
  else:raise ValueError(op)
  peak=max(peak,len(loc)-1880)
 return rows,loc,{'instructions':sum(count.values()),'opcode_counts':dict(sorted(count.items())),'move_rank_histogram':dict(sorted(ranks.items())),'raw_histogram':dict(sorted((r,n) for r,n in rawranks.items() if n)),'owned_lifetimes':lifetimes,'peak_owned':peak,'final_owned':len(loc)-1880}
def exact_bounds(rank,precision=112):
 den=1<<precision;target=rank**199*den**200;lo=0;hi=rank*den+1
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'exact dyadic price bracket')
 return F(lo,den),F(lo if lo**200==target else lo+1,den)
def interval(coeff):
 lo=hi=F(0)
 for r,c in coeff.items():
  l,h=exact_bounds(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 return lo,hi

