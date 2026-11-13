from pathlib import Path
import argparse,gzip,hashlib,json,collections,itertools
from fractions import Fraction as F
if not __debug__:raise SystemExit('Assertions required')
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def rank(rows):
 piv={}
 for row in rows:
  while row:
   j=row.bit_length()-1
   if j in piv:row^=piv[j]
   else:piv[j]=row;break
 return len(piv)
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;s=json.loads(gzip.decompress(raw));roots=[]
 for i in range(111):
  r=[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]];norm=sum(x*x for x in r);r=[x*(2 if norm==1 else 1) for x in r]
  if next(x for x in r if x)<0:r=[-x for x in r]
  assert all(x.denominator==1 for x in r);r=list(map(int,r));assert sum(x*x for x in r)==4;roots.append(r)
 support=lambda r:tuple(j for j,x in enumerate(r) if x)
 patterns=sorted({support(r) for r in roots if len(support(r))==4});assert len(patterns)==14
 comp=lambda S:tuple(i for i in range(8) if i not in S)
 assert all(comp(S) in patterns for S in patterns)
 pairs=[(S,comp(S)) for S in patterns if S<comp(S)];assert len(pairs)==7
 groups=[[] for _ in range(15)]
 for i,r in enumerate(roots):
  S=support(r)
  if len(S)==1:g=0
  else:
   b=next(j for j,(U,V) in enumerate(pairs) if S in (U,V));parity=sum(x<0 for x in r)%2;g=1+2*b+parity
  groups[g].append(i)
 assert sorted(i for g in groups for i in g)==list(range(111)) and all(groups)
 dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
 for g in groups:
  assert len(g)<=8 and all(dot(i,j)==0 for i,j in itertools.combinations(g,2))
 masks=[sum(1<<i for i in g) for g in groups];A=[next(m for m in masks if m>>i&1) for i in range(111)]
 K=[sum(1<<j for j in range(111) if i==j or dot(i,j)==0) for i in range(111)]
 assert rank(A)==15 and rank(K)==9
 assert all((A[i]>>i)&1 and A[i]&~K[i]==0 for i in range(111))
 qdim=rank(A+K)-rank(K);intersect=rank(A)+rank(K)-rank(A+K)
 basis=[]
 for row in K:
  if rank(basis+[row])>len(basis):basis.append(row)
 assert len(basis)==9
 code={0}
 for row in basis:code|={x^row for x in list(code)}
 common=[r for r in code if all((r&m) in [0,m] for m in masks)]
 assert len(code)==512 and len(common)==32 and rank(common)==intersect==5 and qdim==10
 commonbasis=[]
 for row in sorted(common):
  if rank(commonbasis+[row])>len(commonbasis):commonbasis.append(row)
 full_class_rows=sum(len(g) for g in groups if len(g)==8);assert full_class_rows==72
 ell=sum(int((r.bit_count()-1)>36)+int((r.bit_count()-1)>52) for r in A);assert ell==0
 full=[]
 for S,V in pairs:
  for par in range(2):
   g=[]
   for U in [S,V]:
    for signs in itertools.product([-1,1],repeat=3):
     r=[0]*8;r[U[0]]=1
     for j,v in zip(U[1:],signs):r[j]=v
     if sum(x<0 for x in r)%2==par:g.append(r)
   assert len(g)==8 and all(sum(x*y for x,y in zip(r,t))==0 for r,t in itertools.combinations(g,2));full.append(g)
 assert len(full)==14
 result={'status':'PASS_EXACT_ORTHOGONAL_CLASS_FITTING_ONLY','native_sha256':PIN,'groups':groups,'group_sizes':[len(g) for g in groups],'orthogonal_full_basis_classes':sum(len(g)==8 for g in groups),'class_indicator_rows_hex':[hex(m) for m in masks],'rank_A':15,'rank_C':9,'rank_A_plus_C':rank(A+K),'quotient_dimension':qdim,'intersection_dimension':intersect,'maximum_foreign_support':max(r.bit_count()-1 for r in A),'arrival_proxy_sum':ell,'exact_geometric_additional_arrival_floor':full_class_rows,'canonical_codewords_checked':len(code),'intersection_codewords':len(common),'intersection_basis_hex':[hex(x) for x in commonbasis],'changed_coefficients_from_K':sum((r^k).bit_count() for r,k in zip(A,K)),'all111_fitting_rows':True,'physical_source_constructed':False,'conditional_q8_historical_kernel_dimension_at_least':7,'scope':'Exact algebraic fitting and complete15-class partition of actual111 source, inherited from15 orthogonal bases of120 completion. Zero proxy does not construct any source/cache or free class-sum acquisition; fixedq8 physical code remains open.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['groups','class_indicator_rows_hex']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
