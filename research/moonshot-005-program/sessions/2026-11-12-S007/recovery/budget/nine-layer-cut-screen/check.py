#!/usr/bin/env python3
import argparse,gzip,hashlib,json
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
from decimal import Decimal,localcontext
HERE=Path(__file__).resolve().parent
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def span(b):
 s={0}
 for x in b:s.update(v^x for v in tuple(s))
 return frozenset(s)
def root_floor(v,n):
 x=1<<((v.bit_length()+n-1)//n)
 while True:
  y=((n-1)*x+v//x**(n-1))//n
  if y>=x:break
  x=y
 while (x+1)**n<=v:x+=1
 while x**n>v:x-=1
 need(x**n<=v<(x+1)**n,'integer root bound');return x
def dec(q):
 with localcontext() as c:c.prec=50;return str(Decimal(q.numerator)/Decimal(q.denominator))
def add(a,b,c):
 for k,v in tuple(b.items()):
  z=a.get(k,Q(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds'));ap.add_argument('--out',type=Path,default=HERE/'RESULT.json');args=ap.parse_args();raw=(args.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));cover=json.loads((HERE/'COVER.json').read_text());den=cover['denominator'];need(cover['source_sha256']==PIN,'cover source');ports=w['ports'];host=w['hosted'];V=list(host['Dports']);adj=[sum(1<<j for j,b in enumerate(V) if i!=j and (ports[a]&ports[b]).bit_count()%2) for i,a in enumerate(V)];frames=[];counts=Counter()
 def bk(R,A,B):
  if not A and not B:
   c=[V[i] for i in range(len(V)) if R>>i&1];counts[len(c)]+=1
   if len(c)==8:frames.append(c)
   need(len(c)<=8,'no hosted odd clique larger than eight');return
  U=A|B;u=max((i for i in range(len(V)) if U>>i&1),key=lambda i:(A&adj[i]).bit_count());C=A&~adj[u]
  while C:
   bit=C&-C;i=bit.bit_length()-1;C^=bit;bk(R|bit,A&adj[i],B&adj[i]);A^=bit;B|=bit
 bk(0,(1<<len(V))-1,0);need(len(frames)==369,'all369 hosted eight-frames')
 F=list(map(span,w['frames']));dims=list(map(len,w['frames']));n=w['public'];M=set(w['live'])|{x+112 for x in w['live']}|set(host['X2'])|set(host['Y2']);need(n==1480 and len(M)==400,'interface dimensions')
 # Authenticate the complete common target on all inputs, not selected samples.
 target=[{j:Q(1)} for j in range(n)]
 for i,x in enumerate(w['live']):
  y=x+112
  if i in host['Dports']:target[y][x]=Q(1)
  else:target[x][y]=Q(-1);target[y]={x:Q(1,2),y:Q(1,2)}
 for x,y in zip(host['X2'],host['Y2']):target[x][y]=Q(-1)
 a=[{j:Q(1)} for j in range(n)]+[{} for _ in range(w['owned_fields'])]
 for e in reversed(w['program']):
  op,j=e[:2]
  if op in ('INIT','CLEAR'):a[j]={}
  elif op=='ADD':add(a[e[2]],a[j],Q(e[3]))
  elif op=='SCALE':a[j]={k:Q(e[2])*v for k,v in a[j].items()}
  elif op=='COPY':add(a[e[2]],a[j],Q(e[3]));a[j]={}
 expected=[{} for _ in range(n)]
 for j,row in enumerate(target):
  for k,v in row.items():expected[k][j]=v
 need(a[:n]==expected,'full1480-input target');print('Full common target authenticated',flush=True)
 for e in w['program']:
  if e[0]=='MOVE' and not e[4]:need(F[e[2]]<F[e[3]],'all public paths ascend')
 for j in M:need(F[w['initial'][j]]<F[w['final'][j]] and dims[w['final'][j]]-dims[w['initial'][j]]==8,'raw endpoint increase8')
 E=[]
 for e in cover['edges']:
  u=span(e['from_frame']);v=span(e['to_frame']);r=len(e['to_frame'])-len(e['from_frame']);need(u<v and r==e['rank'] and e['coefficient_numerator']>0,'positive nested cover edge');E.append((u,v,r,e['coefficient_numerator']))
 coverage=[];records=[];removed=None;max_common_slack=0
 def flags(f,S):
  d=len(f).bit_length()-1;lo=any(a in f for a in S);hi=all(any((a&v).bit_count()%2 for v in f) for a in S);return [lo or (hi and d>=k) for k in range(1,10)]
 for j,c in enumerate(frames):
  S=[ports[i] for i in c]
  need(all((a&b).bit_count()%2 for a in S for b in S),'odd frame')
  need([i for i,a in enumerate(ports) if all((a&b).bit_count()%2 for b in S)]==c,'no additional active common odd neighbour')
  ds=[flags(f,S) for f in F];cov=[0]*9
  for ei,(u,v,r,z) in enumerate(E):
   fu=flags(u,S);fv=flags(v,S)
   for k in range(9):
    if fv[k] and not fu[k]:cov[k]+=z
  for k in range(9):
   D=[z[k] for z in ds];owned=sum(e[0]=='MOVE' and e[4] and not D[e[2]] and D[e[3]] for e in w['program']);need(owned==8,'all3321 cuts have8 inward owned MOVEs');i0={i for i,t in enumerate(w['initial']) if D[t]};ff={i for i,t in enumerate(w['final']) if D[t]};need(len(i0&M)==16 and len(ff&M)==384 and sum(i not in i0 and i in ff for i in M)==368,'private interface');need(cov[k]>=8*den,'exact fractional cover');records.append({'frame':j,'layer':k+1,'inside_initial':len(i0),'inside_final':len(ff),'common_conditional_rank':len(ff)-len(i0)+8,'private_conditional_rank':376,'owned_inward':8,'coverage_numerator':cov[k]})
  coverage.append(cov)
 # Deleting an actually used edge must expose an uncovered cut.
 for ei,(u,v,r,z) in enumerate(E):
  if removed is not None:break
  for j,c in enumerate(frames):
   S=[ports[i] for i in c];fu=flags(u,S);fv=flags(v,S)
   for k in range(9):
    if fv[k] and not fu[k] and coverage[j][k]-z<8*den:removed={'edge':ei,'frame':j,'layer':k+1,'mutated_coverage_numerator':coverage[j][k]-z};break
   if removed is not None:break
 need(removed is not None,'negative deletion control')
 pd=10**24;cost_lo=Q(0);cost_hi=Q(0);rankcoef=Counter()
 for u,v,r,z in E:
  q=root_floor(r**199*pd**200,200);lo=Q(q,pd);hi=lo if q**200==r**199*pd**200 else Q(q+1,pd);cost_lo+=Q(z,den)*lo;cost_hi+=Q(z,den)*hi;rankcoef[r]+=z
 need(cost_hi<39,'strict upper certificate below39')
 out={'status':'PASS_EXACT_NINE_LAYER_DUAL_CEILING','source_sha256':PIN,'cover_sha256':hashlib.sha256((HERE/'COVER.json').read_bytes()).hexdigest(),'hosted_maximal_clique_sizes':dict(sorted(counts.items())),'frames':frames,'cuts':records,'cover_edge_count':len(E),'cover_denominator':den,'cover_coefficients_by_rank_numerators':dict(sorted(rankcoef.items())),'cost_bounds':[str(cost_lo),str(cost_hi)],'cost_decimal_bounds':[dec(cost_lo),dec(cost_hi)],'minimum_cut_coverage_numerator':min(map(min,coverage)),'negative_control':removed,'scope':'Every nonnegative weighted combination of the369 hosted eight-frame nine-layer cuts, normalized against all nested binary-chart MOVEs, has objective at most this exact53-edge fractional cover cost. The cover is a dual-ceiling witness, not an algorithm or an attainable paid transport schedule. Formation, distribution, and physical records are not supplied.'};args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['frames','cuts']},indent=2),flush=True)
if __name__=='__main__':main()
