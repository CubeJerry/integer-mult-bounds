#!/usr/bin/env python3
"""Exact rational full authorized side-stock cut for every grouped P104 relay."""
import argparse,gzip,hashlib,json,time
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import cache,reduce
from math import gcd,lcm
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
raw=gzip.decompress(a.source.read_bytes());assert hashlib.sha256(raw).hexdigest()=='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48';w=json.loads(raw)
first=w['first_output'];moves={e:(a,b)for e,a,b in w['moves']};qcache={};forms={}
for e,terms in w['forms']:
 co={}
 for j,s in terms:
  if s not in qcache:qcache[s]=Q(s)
  co[j]=qcache[s]
 forms[e]=co
n=len(w['initial']);dim=list(map(len,w['frames']));inc=defaultdict(list);out=defaultdict(list);edge=defaultdict(list)
for e,(a0,b)in moves.items():inc[b].append(e);out[a0].append(e);edge[a0,b].append(e)
for i,(a0,b)in enumerate(zip(w['initial'],w['final'])):inc[a0].append(~i);out[b].append(first+i)
vals={~i:({i:1},1)for i in range(n)}
for e in w['schedule']:
 terms=forms[e];d=lcm(*(vals[j][1]*c.denominator for j,c in terms.items()));v={}
 for j,c in terms.items():
  coeff=c.numerator*(d//(c.denominator*vals[j][1]))
  for k,s in vals[j][0].items():v[k]=v.get(k,0)+coeff*s
 v={k:s for k,s in v.items() if s};g=reduce(gcd,v.values(),d)
 vals[e]=({k:s//g for k,s in v.items()},d//g)
print('source rows',len(vals),'nonzero integer coordinates',sum(len(v) for v,d in vals.values()),flush=True)

def primitive(v):
 v={k:s for k,s in v.items()if s};d=reduce(gcd,v.values(),0)
 return {k:s//d for k,s in v.items()} if d>1 else v

def cancel(v,r,c):
 a,b=v[c],r[c];g=gcd(a,b);a//=g;b//=g
 if b!=1:v={k:x*b for k,x in v.items()}
 for k,x in r.items():
  z=v.get(k,0)-a*x
  if z:v[k]=z
  else:v.pop(k,None)
 return primitive(v)

def append_basis(row,base,width):
 v=row
 while v:
  c=min(v)
  if c>=width:return v
  if c not in base:base[c]=v;return None
  v=cancel(v,base[c],c)
 return {}

def tagged(v,coord,weight,extra):
 row={k:weight*x for k,x in v.items()};row.update({coord+k:x for k,x in extra.items() if x});return row

@cache
def chart_basis(c):
 rows={};bank=inc[c]
 if c==127:
  # At the large sink the physically available final values have very sparse
  # representations in originals; retain their exact original incoming charts.
  loc={e:j for j,e in enumerate(bank)}
  for t in out[c]:
   val,d=vals[t];co=forms[t];den=lcm(d,*(v.denominator for v in co.values()));locrow={loc[e]:v.numerator*(den//v.denominator) for e,v in co.items()}
   assert append_basis(tagged(val,n,den//d,locrow),rows,n) is None
 else:
  for j,e in enumerate(bank):
   v,d=vals[e];assert append_basis(tagged(v,n,1,{j:d}),rows,n) is None
 assert len(rows)==len(bank)
 return sorted(rows.items())

@cache
def intersect(a0,c):
 if len(inc[a0])>len(inc[c]) or (len(inc[a0])==len(inc[c]) and a0>c):return [(y,x) for x,y in intersect(c,a0)]
 large=chart_basis(c);small_piv={};rels=[];l=len(inc[c]);K=n+l
 for j,e in enumerate(inc[a0]):
  v,d=vals[e];r=tagged(v,K,1,{j:d})
  for col,b in large:
   if col in r:r=cancel(r,b,col)
  r=append_basis(r,small_piv,n)
  if r is not None:
   small={k-K:x for k,x in r.items()if k>=K};big={k-n:-x for k,x in r.items()if n<=k<K};assert small and big
   rels.append((small,big))
 return rels

def relations(rows,width):
 piv={};rr=[]
 for j,row in enumerate(rows):
  den=lcm(*(z.denominator for z in row.values()));r={k:int(x*den)for k,x in row.items()if x};r[width+j]=den
  z=append_basis(r,piv,width)
  if z is not None:rr.append({k-width:x for k,x in z.items()})
 return rr

def rank(rows,width):return len(rows)-len(relations(rows,width))

def combine(q,rows):
 r={}
 for i,s in q.items():
  for j,c in rows[i].items():r[j]=r.get(j,0)+s*c
 return primitive(r)

stats=Counter();deficiencies=Counter();samples=[];begin=time.monotonic();outputs=[]
for (aa,b),X in edge.items():
 for c in {moves[e][1] for e in out[b] if e in moves}:
  if (dim[aa]-dim[b])*(dim[b]-dim[c])<=0:continue
  Y=edge[b,c];ys=set(Y);W=[f for f in out[b] if f not in ys];l=len(Y);k=len(X)
  ker=relations([{i:forms[f][x]for i,f in enumerate(W)if x in forms[f]}for x in X],len(W))
  if not ker:stats['full_middle']+=1;continue
  assert len(ker)==1,('higher-dimensional middle kernel',aa,b,c,len(ker));stats['one_middle_direction']+=1
  yidx=[inc[c].index(e)for e in Y];xidx=[inc[b].index(e)for e in X]
  project=lambda q:{j:q[x]for j,x in enumerate(yidx)if x in q}
  D=[project(v)for _,v in intersect(aa,c)];rd=rank(D,l)
  if not rd:stats['no_authorized_direct']+=1;continue
  bc=intersect(b,c);constraint=[{t:sum(v.get(xidx[i],0)*s for i,s in row.items())for t,row in enumerate(ker)}for v,_ in bc]
  ann=relations(constraint,len(ker));rc=[project(v) for _,v in bc];R=[combine(x,rc)for x in ann];rr=rank(R,l);joint=rank(D+R,l)
  outputs.append([aa,b,c,k,l,rd,rr,joint]);deficiencies[l-joint]+=1
  assert rd<1 or rr<l-1 or joint<l,('AUTHORIZED EXTERNAL FIT',outputs[-1]);stats['insufficient_full_external']+=1
  if len(outputs)%25==0:print('exact',len(outputs),'triples',aa,b,c,'seconds',round(time.monotonic()-begin,1),flush=True)
assert sum(stats[k] for k in ('full_middle','one_middle_direction'))==6959
receipt={'exact_native_rational':True,'source_rows':len(vals),'chart_triples':6959,'statistics':stats,
         'joint_dimension_deficit_among_direct_candidates':deficiencies,'eligible':[],'positive_direct_triple_ranks':outputs}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'SIDE-STOCK.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n');print(stats,deficiencies,flush=True)
