"""Source one-patch examples and independent optimistic price arithmetic."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';BP='aeb08b1200c06c5ba378ead88ca2a90b90b681dfacb17b60fd399d532c57eea4'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def brank(rows):
 b={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in b:v^=b[p]
   else:b[p]=v;break
 return len(b)
def iroot(n,k):
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//x**(k-1))//k
  if y>=x:break
  x=y
 while (x+1)**k<=n:x+=1
 while x**k>n:x-=1
 assert x**k<=n<(x+1)**k
 return x
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP;s=json.loads(gzip.decompress(raw));frames={int(k):v for k,v in s['frames'].items()};roots=[]
 for i in range(111):
  r=[F(x) for x in frames[s['start'][i]]['B'][0]];norm=dot(r,r);assert norm in [1,4];r=[int(x*(2 if norm==1 else 1)) for x in r];assert dot(r,r)==4
  if next(x for x in r if x)<0:r=[-x for x in r]
  roots.append(r)
 assert len(set(map(tuple,roots)))==111
 K=[]
 for i,r in enumerate(roots):
  row=0
  for j,t in enumerate(roots):
   z=dot(r,t);assert z%2==0;k=1^((z//2)%2);assert k==int(i==j or z==0);row|=k<<j
  K.append(row)
 assert brank(K)==9 and sum(v.bit_count()-1 for v in K)==6470
 supports={frozenset(j for j,x in enumerate(r) if x) for r in roots if sum(bool(x) for x in r)==4};assert len(supports)==14;boxes=[]
 for S in supports:
  A=[i for i,r in enumerate(roots) if all(not x for j,x in enumerate(r) if j not in S)];B=[i for i,r in enumerate(roots) if all(not x for j,x in enumerate(r) if j in S)]
  assert not set(A)&set(B) and all(dot(roots[i],roots[j])==0 for i in A for j in B);boxes.append((len(A)*len(B),sorted(S),A,B))
 area,support,A,B=max(boxes);mask=sum(1<<j for j in B);patched=[r^(mask if i in A else 0) for i,r in enumerate(K)]
 assert brank(patched)==10 and all((r>>i&1)==1 and not(r&~K[i]) for i,r in enumerate(patched));remaining=sum(r.bit_count()-1 for r in patched);assert remaining==6470-area
 j=0;act=[i for i in range(111) if i!=j and K[i]>>j&1];col=[r^((1<<j) if i in act else 0) for i,r in enumerate(K)];assert brank(col)==10 and min(r.bit_count()-1 for r in col)>=53
 budgetraw=a.reviewed_budget.read_bytes();assert hashlib.sha256(budgetraw).hexdigest()==BP;budget=json.loads(budgetraw);ceiling=list(map(F,budget['limiting_complete_Q_allowance_bounds']))
 grid=10**36;power={}
 for r in [7,8]:
  target=r**199*grid**200;z=iroot(target,200);power[r]=(F(z,grid),F(z+int(z**200!=target),grid))
 base=[222*power[7][b]+9*power[8][b] for b in [0,1]];room=[ceiling[0]-base[1],ceiling[1]-base[0]];deficit=[base[0]+30-ceiling[1],base[1]+30-ceiling[0]]
 assert room[1]<12 and deficit[0]>F('18.45799327294747')
 out={'status':'PASS_SOURCE_RANK10_PATCH_EXAMPLES_AND_CONDITIONAL_PRICE','source_sha256':SP,'accepted_budget_sha256':BP,'canonical_rank':9,'canonical_foreign_coefficients':6470,'actual_source_foreign_min':min(r.bit_count()-1 for r in K),'rank10_rectangle_example':{'coordinate_support':support,'A':A,'B':B,'rank':10,'deleted_foreign_coefficients':area,'remaining_foreign_coefficients':remaining,'unchanged_rows':111-len(A)},'rank10_single_column_example':{'column':j,'affected_rows':len(act),'rank':10,'minimum_remaining_foreign_support':min(r.bit_count()-1 for r in col)},'universal_E7_premises':{'proper_subspace_max':36,'two_proper_union_max':52},'required_visits_lower':150,'available_nine_packet_original_path_visits':120,'necessary_additional_upward_arrivals':30,'optimistic_base_bounds':list(map(str,base)),'limiting_remaining_bounds':list(map(str,room)),'extra30_deficit_bounds':list(map(str,deficit)),'extra30_deficit_decimal':float(deficit[0]),'scope':'Scalar rank-one perturbation of a vertex-gauge canonical fitting; arbitrary rank10 and noncommuting block perturbations remain open. Explicit algebraic fits are not physical constructions.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','rank10_rectangle_example','rank10_single_column_example','extra30_deficit_decimal']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--reviewed-budget',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
