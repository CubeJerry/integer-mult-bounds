#!/usr/bin/env python3
"""Exact finite premises and controls; the universal proof is PROOF.md."""
import argparse,gzip,hashlib,itertools,json,random
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
EXTERNAL='a2a0b79545a1857aea0bc9ac4beb9f222aa50984c9383053e9163af8e33a4802'
FRAME=[0,16,17,32,36,38,67,71]
def need(ok,why):
 if not ok:raise ValueError(why)
def basis(rows):
 b={};chosen=[]
 for index,row in enumerate(rows):
  while row:
   p=row.bit_length()-1
   if p in b:row^=b[p]
   else:b[p]=row;chosen.append(index);break
 return b,chosen
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zeros(m,n):return [[0]*n for _ in range(m)]
def tr(a):return list(map(list,zip(*a)))
def add(a,b,p):return [[(x+y)%p for x,y in zip(u,v)] for u,v in zip(a,b)]
def mul(a,b,p):return [[sum(x*y for x,y in zip(u,v))%p for v in tr(b)] for u in a]
def rank(a,p):
 a=[row[:] for row in a];r=0
 if not a:return 0
 for c in range(len(a[0])):
  q=next((i for i in range(r,len(a)) if a[i][c]%p),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r];z=pow(a[r][c],-1,p);a[r]=[x*z%p for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    z=a[i][c];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def inv(a,p):
 n=len(a);a=[a[i][:]+eye(n)[i] for i in range(n)]
 for c in range(n):
  q=next((i for i in range(c,n) if a[i][c]%p),None);need(q is not None,'gauge invertible')
  a[c],a[q]=a[q],a[c];z=pow(a[c][c],-1,p);a[c]=[x*z%p for x in a[c]]
  for i in range(n):
   if i!=c and a[i][c]:
    z=a[i][c];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[c])]
 return [row[n:] for row in a]
def gl(n,p,rng):
 while True:
  a=[[rng.randrange(p) for _ in range(n)] for _ in range(n)]
  if rank(a,p)==n:return a

def actual(raw):
 need(hashlib.sha256(raw).hexdigest()==NATIVE,'native exact source')
 s=json.loads(gzip.decompress(raw));ff={int(i):f for i,f in s['frames'].items()}
 roots=[[F(t) for t in ff[s['start'][i]]['B'][0]] for i in range(111)]
 dot=lambda a,b:sum(x*y for x,y in zip(a,b));v=[]
 for i,r in enumerate(roots):
  nn=dot(r,r);need(nn in (1,4),'root norm');vv=[x*(2 if nn==1 else 1) for x in r]
  need(all(x.denominator==1 for x in vv),'integral roots');v.append(list(map(int,vv)))
  facet=ff[s['final'][111+i]];need(facet['dim']==7,'facet dimension')
  need(all(dot(r,list(map(F,z)))==0 for z in facet['B']),'actual facet')
 K=[]
 for i,u in enumerate(v):
  row=0
  for j,w in enumerate(v):
   z=dot(u,w);need(z%2==0,'even Gram');bit=1^((z//2)%2)
   need(i==j or bit==int(z==0),'actual contact mask');row|=bit<<j
  K.append(row)
 bit=lambda i,j:K[i]>>j&1
 need(all(bit(i,j)==int(i==j) for i in FRAME for j in FRAME),'identity frame')
 b=[sum(bit(i,j)<<a for a,j in enumerate(FRAME)) for i in range(111)]
 pivot=next(i for i in range(111) if i not in FRAME and b[i].bit_count()%2==0)
 x=[b[i]|((bit(i,pivot)^((b[i]&b[pivot]).bit_count()%2))<<8) for i in range(111)]
 need(all((x[i]&x[j]).bit_count()%2==bit(i,j) for i in range(111) for j in range(111)),'all factor products')
 ed={i:tuple(a for a in range(8) if x[i]>>a&1) for i in range(111) if x[i]>>8&1 and (x[i]&255).bit_count()==2}
 need(len(ed)==27 and set(ed.values())==set(itertools.combinations(range(8),2))-{(0,4)},'exact seed')
 degrees=[sum(a in e for e in ed.values()) for a in range(8)]
 need(Counter(degrees)=={6:2,7:6},'strict degree surplus')
 need(all(bit(i,j)==int(not(set(ed[i])&set(ed[j]))) for i in ed for j in ed if i!=j),'star edge mask')
 seed=sorted(set(FRAME)|set(ed));anchors=[]
 for i in range(111):
  if i in seed:continue
  aa=[j for j in seed if not bit(i,j)];bb,ch=basis([x[j] for j in aa]);need(len(bb)==8,'anchor rank eight')
  jj=[aa[t] for t in ch];need(x[i].bit_count()%2==1,'unit self pairing')
  need(all((x[i]&x[j]).bit_count()%2==0 for j in jj),'anchor annihilator')
  need(len(basis([x[j] for j in jj[:-1]])[0])==7,'seven anchor control')
  anchors.append({'role':i,'eight_noncontact_seed_roles':jj})
 need(len(anchors)==76,'all anchors')
 need(len(basis(K)[0])==9,'rank nine');need(len(basis([z^(1<<i) for i,z in enumerate(K)])[0])==108,'residual rank')
 foreign=sum(z.bit_count()-1 for z in K);need(foreign==6470,'foreign blocks')
 return {'frame':FRAME,'edges':[{'role':i,'ends':e} for i,e in ed.items()],'degrees':degrees,'anchors':anchors,'factor_vectors':x,'foreign_blocks':foreign,'rank':9,'residual_rank':108}

def metrics(n,edges,V,j,C,R,p):
 dim=n*V+j
 for e in edges:
  allowed=set(range(e[0]*V,(e[0]+1)*V))|set(range(e[1]*V,(e[1]+1)*V))|set(range(n*V,dim))
  need(all(C[e][i][a]==0 and R[e][a][i]==0 for i in range(V) for a in range(dim) if a not in allowed),'star support')
  for f in edges:
   if e==f:need(mul(C[e],R[f],p)==eye(V),'identity diagonal')
   elif set(e)&set(f):need(mul(C[e],R[f],p)==zeros(V,V),'adjacent zero')
 S={};g={}
 for e in edges:
  S[e]=mul([row[n*V:] for row in C[e]],R[e][n*V:],p)
  for a in e:
   alpha=mul([row[a*V:(a+1)*V] for row in C[e]],R[e][a*V:(a+1)*V],p)
   g[e,a]=rank(add(alpha,S[e],p),p)
 deg=[sum(a in e for e in edges) for a in range(n)]
 G=[sum(g[e,a] for e in edges if a in e) for a in range(n)]
 for e in edges:
  for a in e:need(G[a]+V<=j+2*sum(g[e,b] for b in e),'LR')
 lhs=sum((deg[a]-4)*G[a] for a in range(n));rhs=2*len(edges)*(j-V)
 need(lhs<=rhs,'summed stability')
 defect=sum(rank(add(eye(V),S[e],p),p) for e in edges);need(defect<=sum(G),'Schur stability')
 return {'G':G,'lhs':lhs,'rhs':rhs,'defect':defect,'S':S}
def assignment(n,edges,assign,extra,V):
 dim=(n+extra)*V;C={};R={}
 for e in edges:
  c=zeros(V,dim)
  for t in range(V):c[t][assign[e]*V+t]=1
  C[e]=c;R[e]=tr(c)
 return C,R,extra*V

def controls():
 rng=random.Random(113715);out=[];noncommuting=0
 for n,missing in [(6,None),(8,(0,4))]:
  edges=[e for e in itertools.combinations(range(n),2) if e!=missing]
  for p in (2,3,5):
   for V in (1,2,3):
    C={};R={};gauges={}
    for e in edges:
     u=gl(V,p,rng);iv=inv(u,p);gauges[e]=u;c=zeros(V,(n+1)*V);r=zeros((n+1)*V,V)
     for a,sign in [(e[0],1),(e[1],1),(n,-1)]:
      for i in range(V):
       for t in range(V):c[i][a*V+t]=u[i][t];r[a*V+i][t]=sign*iv[i][t]%p
     C[e]=c;R[e]=r
    q=metrics(n,edges,V,V,C,R,p);need(q['G']==[0]*n,'saturated G zero')
    neg=[[-int(i==t)%p for t in range(V)] for i in range(V)]
    need(all(s==neg for s in q['S'].values()),'Schur minus I')
    noncommuting+=sum(mul(gauges[e],gauges[f],p)!=mul(gauges[f],gauges[e],p) for e,f in itertools.combinations(edges,2))
    damaged={e:[row[:] for row in c] for e,c in C.items()};damaged[edges[0]]=zeros(V,(n+1)*V)
    try:metrics(n,edges,V,V,damaged,R,p)
    except ValueError:pass
    else:raise ValueError('broken diagonal accepted')
    out.append({'n':n,'field':p,'width':V,'kind':'saturated gauge'})
    assign={e:n+i-1 for i,e in enumerate(edges) if i};assign[edges[0]]=edges[0][0]
    cc,rr,j=assignment(n,edges,assign,len(edges)-1,V);q=metrics(n,edges,V,j,cc,rr,p)
    need(sum(q['G'])>0 and q['defect']>0,'nonzero defect test')
    out.append({'n':n,'field':p,'width':V,'kind':'rank excess','lhs':q['lhs'],'rhs':q['rhs'],'Schur_defect':q['defect']})
 edges=list(itertools.combinations(range(4),2));assign={(0,1):1,(0,2):0,(0,3):4,(1,2):4,(1,3):3,(2,3):2}
 for p in (2,3,5):
  c,r,j=assignment(4,edges,assign,1,1);q=metrics(4,edges,1,j,c,r,p)
  need(sum(s==[[0]] for s in q['S'].values())==4,'degree-three singular witness')
  need(sum(q['G'])>0,'strict-degree premise control')
 need(noncommuting>0,'noncommuting gauges covered')
 return {'representations':out,'noncommuting_gauge_pairs':noncommuting,'degree_three_counterexample_fields':[2,3,5],'negative_controls':['source byte mutation','broken identity diagonal','seven-anchor rank loss','degree-three singular Schur fitting']}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path);p.add_argument('--native',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 native=a.native or a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
 ext=Path(__file__).with_name('PR7114-THEOREM.md');need(hashlib.sha256(ext.read_bytes()).hexdigest()==EXTERNAL,'credited source bytes')
 raw=native.read_bytes();data=actual(raw)
 try:actual(raw+b' ')
 except ValueError:pass
 else:raise ValueError('source mutation accepted')
 checks=controls();result={'status':'PASS_SATURATED_STAR_RIGIDITY_FINITE_PREMISES','native_sha256':NATIVE,'external_source_sha256':EXTERNAL,'actual_source':data,'controls':checks,'universal_claim_basis':'PROOF.md Sections 2-4, not finite checks','complete_kappa':None}
 a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'seed_edges':len(data['edges']),'anchors':len(data['anchors']),'representations':len(checks['representations']),'noncommuting_gauge_pairs':checks['noncommuting_gauge_pairs']}))
if __name__=='__main__':main()
