#!/usr/bin/env python3
"""Exact finite controls for the all-field four-type parity proof."""
import argparse,itertools,json
from collections import Counter
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1;b>>=1
  if a&4:a^=7
 return c

def dot(a,b):
 x=0
 for u,v in zip(a,b):x^=mul(u,v)
 return x

def reduce(M,ncols):
 A=[list(r) for r in M];piv=[];k=0
 for j in range(ncols):
  q=next((r for r in range(k,len(A)) if A[r][j]),None)
  if q is None:continue
  A[k],A[q]=A[q],A[k];z=next(x for x in (1,2,3) if mul(x,A[k][j])==1)
  A[k]=[mul(z,x) for x in A[k]]
  for r in range(len(A)):
   if r!=k and A[r][j]:
    z=A[r][j];A[r]=[x^mul(z,y) for x,y in zip(A[r],A[k])]
  piv.append(j);k+=1
 return A,piv

def kernel(M,ncols):
 A,piv=reduce(M,ncols);out=[]
 for j in range(ncols):
  if j not in piv:
   v=[0]*ncols;v[j]=1
   for r,p in enumerate(piv):v[p]=A[r][j]
   out.append(v)
 return out

def solve(M,b):
 ncols=len(M[0]);A,piv=reduce([r+[x] for r,x in zip(M,b)],ncols)
 if any(not any(r[:ncols]) and r[-1] for r in A):return None
 x=[0]*ncols
 for r,p in enumerate(piv):x[p]=A[r][-1]
 return x

def project(v):
 z=next((x for x in v if x),None)
 if z is None:return None
 inv=next(x for x in (1,2,3) if mul(x,z)==1)
 return tuple(mul(inv,x) for x in v)

def phi(U):
 return [[(U[r][j] if j<3 else 0) if t==0 else (U[r][j-1] if j else 0)
          for j in range(4)] for r in range(2) for t in range(2)]

def in_span(v,rows):
 return len(reduce(rows,4)[1])==len(reduce(rows+[list(v)],4)[1])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 conic=[(1,t,mul(t,t)) for t in range(4)]+[(0,0,1)]
 gamma=[[1,t,mul(t,t),mul(t,mul(t,t))] for t in range(4)]+[[0,0,0,1]]
 need(all(len(reduce([gamma[j] for j in S],4)[1])==4 for S in itertools.combinations(range(5),4)),'every four cubic points independent')
 maps=[];census=Counter()
 for flat in itertools.product(range(4),repeat=6):
  U=[list(flat[:3]),list(flat[3:])];KU=kernel(U,3)
  if len(KU)!=1:continue
  P=phi(U);KP=kernel(P,4);line=project(KU[0]);typ=conic.index(line) if line in conic else None
  need(len(KP)==int(typ is not None),'conic rank defect')
  if typ is not None:need(project(KP[0])==project(gamma[typ]),'cubic kernel')
  a=solve(P,[1,0,0,1])
  if a is None:continue
  need(len(reduce([[a[0],a[1],a[2]],[a[1],a[2],a[3]]],3)[1])==2,'identity preimage Hankel rank2')
  maps.append((U,typ,a));census['nonexceptional' if typ is None else str(typ)]+=1
 checks=0;coverage=Counter();boundary=None
 for chosen in itertools.combinations(range(5),4):
  pairs=list(itertools.combinations(chosen,2))
  for U,typ,a in maps:
   covered=[];missed_planes=0
   for i,j in pairs:
    P=[gamma[i],gamma[j]];inside=in_span(a,P);missed_planes+=inside
    local=(typ is None or in_span(gamma[typ],P))
    covered.append(local and not inside)
    annihilator=kernel(P,4);need(len(annihilator)==2,'pair annihilator dimension2')
    need(all(dot(c,a)==0 for c in annihilator)==inside,'generic annihilator nonvanishing criterion')
    if typ is not None:need(all(dot(c,gamma[typ])==0 for c in annihilator)==local,'generic locality criterion')
   n=sum(covered);checks+=1
   if typ is None:need(n>=5 and missed_planes<=1,'nonexceptional five-of-six cover')
   elif typ in chosen:need(n==3,'chosen exceptional type covered by its three pairs')
   else:
    need(n==0,'omitted fifth type lies outside this generic cover')
    if boundary is None:boundary={'chosen_types':list(chosen),'omitted_type':typ,'U':U,'identity_preimage':a,'coverage':covered}
   coverage[str(n)]+=1
 weights=[]
 for a,b,c in itertools.product(range(15),repeat=3):
  d=28-a-b-c
  if not 0<=d<=14:continue
  w=(a,b,c,d)
  if all(w[i]+w[j]<=14 for i,j in itertools.combinations(range(4),2)):weights.append(w)
 need(weights==[(7,7,7,7)] and not any(all(x%2==0 for x in w) for w in weights),'unique odd equality weights contradict even scalar equality rows')
 five=[6,6,6,6,4];need(sum(five)==28 and all(five[i]+five[j]<=14 for i,j in itertools.combinations(range(5),2)),'five-type abstract capacity boundary remains feasible')
 result={'status':'PASS_FOUR_TYPE_CHAIN_PARITY_CONTROLS','field':'F4 with alpha^2=alpha+1','identity_admitting_selectors':len(maps),'selector_type_census':dict(census),
         'four_type_sets':5,'selector_set_checks':checks,'generic_cover_histogram':dict(coverage),'unique_weight_solution_without_evenness':weights,
         'even_weight_solution_count':0,'omitted_type_boundary':boundary,'abstract_five_type_weights':five,
         'universal_proof':'PROOF.md; finite field controls do not prove the all-field statement','claim':'At most four exceptional types imply chi>=195, using the scalar equality classification','new_kappa':None}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','identity_admitting_selectors','selector_set_checks','generic_cover_histogram','even_weight_solution_count']}))
if __name__=='__main__':main()

