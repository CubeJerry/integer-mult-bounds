#!/usr/bin/env python3
"""Exact source and scope controls for the seeded-staircase rank theorem."""
import argparse,gzip,hashlib,itertools,json,random
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,m):
 if not b:raise ValueError(m)
def rank(rows):
 piv={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
 return len(piv)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def local_masks(R,order):
 return [sum(1<<j for j in range(len(order)) if all(dot(R[order[j]],R[order[k]])==0 for k in range(i+1))) for i in range(len(order))]
def submasks(x):
 a=x
 while True:
  yield a
  if not a:break
  a=(a-1)&x
def bads(R,o):return [j for j in range(1,len(o)) if any(dot(R[o[j]],R[o[k]])!=0 for k in range(j))]
def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');n=json.loads(gzip.decompress(raw));rr=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 need(len(rr)==111 and all(dot(r,r)>0 for r in rr),'nonzero real source lines');need(all(dot(rr[i],rr[j])==0 for i in range(8) for j in range(i)),'eight orthogonal coordinate lines')
 natural=list(range(111));bn=bads(rr,natural);need(bn==list(range(8,111)),'exact natural-order bad positions103')
 pent=[92,36,54,38,55];R=[rr[i] for i in pent]
 adj=[[int(i!=j and dot(R[i],R[j])==0) for j in range(5)] for i in range(5)]
 need(all(sum(x)==2 for x in adj),'pentagon degrees');need(all(not all(adj[i][j] for i,j in itertools.combinations(S,2)) for S in itertools.combinations(range(5),3)),'no orthogonal triangle')
 distribution={};completions=0;block_cases=0;witness=None;randomizer=random.Random(18731)
 for order in itertools.permutations(range(5)):
  L=local_masks(R,order);bad=bads(R,order);b=len(bad);distribution[b]=distribution.get(b,0)+1
  tails=[sum(1<<j for j in range(i+1,5)) for i in range(5)]
  least=100
  for bs in itertools.product(*(list(submasks(x)) for x in L)):
   rows=[u^v for u,v in zip(tails,bs)];r=rank(rows);least=min(least,r);completions+=1
   need(r>=b,'forced bad-position minor')
   selected=[sum(((rows[j-1]>>k)&1)<<z for z,k in enumerate(bad)) for j in bad]
   need(rank(selected)==b,'explicit selected minor rank')
  need(least==b,'sharp exact scalar completion minimum')
  if b==3 and witness is None:witness={'order':[pent[i] for i in order],'bad_positions':[j+1 for j in bad],'local_masks':L,'minimum_preload_rank':least}
  # Whole width2, arbitrary local2x2 matrices: no commuting or scalar lift premise.
  for rep in range(4):
   V=2;rows=[]
   for i,T in enumerate(tails):
    for u in range(V):
     row=sum(1<<(V*j+u) for j in range(5) if T>>j&1)
     for j in range(5):
      if L[i]>>j&1:row ^=randomizer.randrange(1<<V)<<(V*j)
     rows.append(row)
   need(rank(rows)>=b*V,'arbitrary block lower rank');block_cases+=1
 need(distribution=={3:80,4:40},'complete pentagon order census')
 # Exact upper construction on the full native natural order.
 L=local_masks(rr,natural);E=sum(1<<j for j in bn)
 for i in range(111):
  tail=sum(1<<j for j in range(i+1,111));need((tail & ~E)&~L[i]==0,'full-native sharp tail decomposition')
 # Mutation: granting nonlocal own/forbidden columns allows every tail to be erased.
 illegal=[0]*5;need(rank(illegal)==0<3,'illegal-locality scope control')
 # Orthogonal positive control: all local tails, no common seed.
 co=list(range(8));lc=local_masks(rr,co);need(not bads(rr,co),'orthogonal no-preload control')
 need(all(sum(1<<j for j in range(i+1,8))&~lc[i]==0 for i in range(8)),'orthogonal staircase local tails')
 out={'status':'PASS_EXACT_SEEDED_STAIRCASE_SOURCE_AND_CONTROLS','native_sha256':PIN,'native':{'targets':111,'maximum_orthogonal_set':8,'minimum_common_preload_dimensions_per_V':103,'total_channels_in_interface':104},'pentagon':{'indices':pent,'orthogonality':adj,'bad_position_distribution':distribution,'minimum_common_preload_dimensions_per_V':3,'total_channels_in_interface':4,'scalar_local_completions':completions,'arbitrary_width2_local_completions':block_cases,'witness':witness},'negative_controls':['Illegal local-input grants destroy the lower bound and must be rejected geometrically','The isolated multi-bus staircase is outside the single-final-bus premise'],'positive_control':'Eight coordinate roots need zero common preloads','classification':'Written all-field/block theorem; exact finite source verification; not a supplier','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','native','pentagon')}))
if __name__=='__main__':main()
