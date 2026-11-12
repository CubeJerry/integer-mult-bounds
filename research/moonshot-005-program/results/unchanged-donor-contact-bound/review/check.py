#!/usr/bin/env python3
"""Independent small exact audit; no all-chart enumeration."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,m):
 if not b:raise ValueError(m)
def root(v):
 s=[i for i in range(9) if v>>i&1]
 if len(s)==3:return [2*int(i in s) for i in range(8)] if 8 in s else [1 if i in s else -1 for i in range(8)]
 need(len(s)==7,'port weight');i,j=[k for k in range(9) if k not in s]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def det(M):
 a=[[F(x) for x in r] for r in M];d=F(1)
 for k in range(len(a)):
  p=next((i for i in range(k,len(a)) if a[i][k]),None)
  if p is None:return F(0)
  if p!=k:a[p],a[k]=a[k],a[p];d=-d
  v=a[k][k];d*=v
  for i in range(k+1,len(a)):
   c=a[i][k]/v
   for j in range(k+1,len(a)):a[i][j]-=c*a[k][j]
 return d
def witness(A,ids):
 piv={};keep=[]
 for rowid in ids:
  r={j:F(v) for j,v in enumerate(A[rowid]) if v}
  while r:
   j=min(r)
   if j not in piv:
    z=r[j];piv[j]={k:v/z for k,v in r.items()};keep.append(rowid);break
   z=r[j]
   for k,v in piv[j].items():
    x=r.get(k,F(0))-z*v
    if x:r[k]=x
    else:r.pop(k,None)
 return keep,sorted(piv)
def q(x):return ((x.bit_count()*(x.bit_count()-1)//2)&1)
def main(a):
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));ports=w['ports'];A=[root(v) for v in ports];records=[]
 for i,v in enumerate(ports):
  blocked=[j for j,t in enumerate(ports) if j!=i and (v&t).bit_count()%2]
  neighbors=[j for j,t in enumerate(ports) if not (v&t).bit_count()%2]
  selected,columns=witness(A,blocked);d=det([[A[j][k] for k in columns] for j in selected]);n=abs(d.numerator)
  need(len(blocked)==55 and len(neighbors)==48 and len(selected)==len(columns)==7,'source geometric partition and rank7')
  need(d.denominator==1 and n and n&(n-1)==0,'rank witness survives every odd characteristic')
  need(all(sum(A[i][k]*A[j][k] for k in range(8))==0 for j in blocked),'kernel contains own root')
  need(sum(x*x for x in A[i])==8,'self root norm')
  need(all(abs(sum(A[i][k]*A[j][k] for k in range(8)))==4 for j in neighbors),'every required side coefficient survives odd characteristic')
  records.append({'receiver':i,'source_role':w['live'][i],'blocked':blocked,'neighbors':neighbors,'minor_rows':selected,'minor_columns':columns,'minor_determinant':str(d)})
 E=[x for x in range(512) if x.bit_count()%2==0]
 need(len(E)==256 and sum(q(x)==0 for x in E)==136 and sum(q(x)==1 for x in E)==120,'quadratic plus type')
 need(all(sum((-1)**(q(x)+((x&z).bit_count()%2)) for x in E)==16*(-1)**q(z) for z in E),'finite Fourier sign corroboration')
 cases=[]
 for polar_rank,us,ds in [(0,[0,8],[0,8,-8]),(2,[0,4,-4],[0,4,-4])]:
  for U in us:
   for D in ds:
    donors=(8-D)//2;receivers=12-donors-U//2
    need(donors>=0 and receivers>=0 and 5*donors*receivers<=8*donors+24*receivers,'analytic Gauss-case bound')
    cases.append({'polar_rank':polar_rank,'S_U':U,'S_D':D,'D':donors,'R':receivers})
 levels=[104,208,416,3328//5,3328//5,416,208,104]
 need(sum(levels)==2786,'root analytic contact bound')
 # Exact small integer relaxation using only the analytically allowed rectangles.
 pareto=[(2,12),(4,10),(6,8),(8,4)]
 profiles=[(d,r) for d in range(1,9) for r in range(1,13) if any(d<=D and r<=R for D,R in pareto)]
 N=104;dp=[[-1]*(N+1) for _ in range(N+1)];dp[0][0]=0;parent={}
 for d in range(N+1):
  for r in range(N+1):
   if dp[d][r]<0:continue
   for x,y in profiles:
    if d+x<=N and r+y<=N and dp[d][r]+x*y>dp[d+x][r+y]:
     dp[d+x][r+y]=dp[d][r]+x*y;parent[d+x,r+y]=(d,r,x,y)
 optimum=max((dp[d][r],d,r) for d in range(N+1) for r in range(N+1));need(optimum==(656,104,104),'integer rectangle relaxation optimum')
 value,d,r=optimum;groups=[]
 while (d,r)!=(0,0):
  d0,r0,x,y=parent[d,r];groups.append((x,y));d,r=d0,r0
 need(sum(x for x,y in groups)==sum(y for x,y in groups)==104 and sum(x*y for x,y in groups)==656,'abstract attaining multiplicities')
 # Independent state recurrence: split a final rectangle off each nonempty state.
 reverse=[[0]*(N+1) for _ in range(N+1)]
 for d in range(N+1):
  for r in range(N+1):
   reverse[d][r]=max([0]+[reverse[d-x][r-y]+x*y for x,y in profiles if x<=d and y<=r])
 need(reverse[104][104]==656 and all(max(dp[x][y] for x in range(d+1) for y in range(r+1))==reverse[d][r] for d,r in [(0,0),(8,12),(32,32),(103,104),(104,104)]),'second recurrence and boundary controls')
 general=lambda n:sum(min(n*2**(8-d),104*2**(d-1)) for d in range(1,9))
 need(general(252)==4988<4992<=general(253)==4995,'root trajectory253 threshold')
 blocked0=records[0]['blocked'];bad=next(j for j in blocked0 if A[j][0]);wrong=[F(v,8)+F(k==0) for k,v in enumerate(A[0])];bad_coefficient=sum(c*v for c,v in zip(wrong,A[bad]));need(bad_coefficient!=0,'perturbed packet decoder leaks inaccessible input')
 missing=records[0]['neighbors'][0];uncancelled=F(sum(c*v for c,v in zip(A[0],A[missing])),8);need(uncancelled!=0,'omitting one required direct cancellation fails')
 controls=[{'claim':'perturb first packet coefficient by one','receiver':0,'inaccessible_column':bad,'nonzero_error':str(bad_coefficient)},{'claim':'omit one nonzero side cancellation','receiver':0,'omitted_column':missing,'nonzero_error':str(uncancelled)},{'claim':'rectangle relaxation bounded by655','counterexample_value':sum(x*y for x,y in groups)},{'claim':'negative Gauss sign at zero','claimed':-16,'actual':sum((-1)**q(x) for x in E)}]
 receipt={'status':'PASS_INDEPENDENT_CONTACT_AND_UNIQUE_DECODER_AUDIT','source_sha256':PIN,'unique_decoder_witnesses':records,'minor_histogram':dict(Counter(r['minor_determinant'] for r in records)),'coefficient_fields':'every field of characteristic other than2; arbitrary positive whole-field coordinate dimension','quadratic_Gauss_cases':cases,'root_level_bounds':levels,'root_contact_bound':2786,'integer_rectangle_level_optimum':656,'integer_relaxation_witness':[{ 'D':d,'R':r,'multiplicity':n} for (d,r),n in Counter(groups).items()],'sharpened_contact_bound':2768,'required_fixed_E8_side_pairs':4992,'terms_outside_sharpened_direct_contact_scope':2224,'basic_extra_trajectory_necessary_bound':253,'negative_controls':controls,'scope':'Direct unchanged original-value carrier paths, one monotone Y path per receiver, donor-only stationary caches, no interreceiver relay or extra coded carriers. Integer rectangle optimum is a finite relaxation, not a realizable schedule or paid MOVE count. No new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps({k:receipt[k] for k in ['status','minor_histogram','root_contact_bound','integer_rectangle_level_optimum','sharpened_contact_bound','basic_extra_trajectory_necessary_bound']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())

