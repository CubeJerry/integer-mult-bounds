"""Independent complete high-saving catalog; perpendicular-mask geometry."""
import argparse,collections,gzip,hashlib,itertools,json,math,time
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit("Exact checks require Python without -O")
P=257;INV=[0]+[pow(i,P-2,P) for i in range(1,P)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def canon(r):return tuple(r if next(x for x in r if x)>0 else [-x for x in r])
def bits(m):
 while m:
  z=m&-m;yield z.bit_length()-1;m^=z
def mbasis(rows,stop=8):
 b={}
 for rr in rows:
  v=[x%P for x in rr]
  for p,row in sorted(b.items()):
   c=v[p]
   if c:
    for j in range(p,8):v[j]=(v[j]-c*row[j])%P
  if not any(v):continue
  p=next(j for j,x in enumerate(v) if x);iv=INV[v[p]];v=[x*iv%P for x in v];b[p]=v
  if len(b)==stop:break
 return b
def independent(v,b):
 v=list(v)
 for p,row in sorted(b.items()):
  c=v[p]
  if c:
   for j in range(p,8):v[j]=(v[j]-c*row[j])%P
 return any(v)
def brank(rows):
 b={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in b:v^=b[p]
   else:b[p]=v;break
 return len(b)
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(raw));fr={int(k):v for k,v in s['frames'].items()};R=[]
 for i in range(111):
  v=[F(x) for x in fr[s['start'][i]]['B'][0]];n=dot(v,v);assert n in [1,4];v=[int(x*(2 if n==1 else 1)) for x in v];assert dot(v,v)==4;R.append(canon(v))
 O=[sum(1<<j for j,v in enumerate(R) if dot(u,v)==0) for u in R];T=[m|(1<<i) for i,m in enumerate(O)];deg=[m.bit_count() for m in O];full111=(1<<111)-1;low={n:sum(1<<i for i,d in enumerate(deg) if d<=52+n) for n in range(1,9)}
 basis=[]
 for row in T:
  if brank(basis+[row])>len(basis):basis.append(row)
 assert len(basis)==9;words=[0]
 for row in basis:words += [v^row for v in words]
 assert len(set(words))==512 and min(w.bit_count() for w in words if w)==48
 punctured=[]
 for i in range(111):
  restrictions={w&(full111^T[i]) for w in words};assert len(restrictions)==256;punctured.append(min(w.bit_count() for w in restrictions if w))
 assert min(punctured)==18
 supports={tuple(j for j,x in enumerate(v) if x) for v in R if sum(bool(x) for x in v)==4};full={tuple(2*int(i==j) for j in range(8)) for i in range(8)}
 for S in supports:
  for signs in itertools.product([-1,1],repeat=4):
   v=[0]*8
   for j,c in zip(S,signs):v[j]=c
   full.add(canon(v))
 full=sorted(full);assert len(full)==120 and all(v in full for v in R);OF=[sum(1<<j for j,v in enumerate(full) if dot(u,v)==0) for u in full];OFa=[OF[full.index(v)] for v in R];RM=[[x%P for x in v] for v in R];flats={};indep=0
 for i in range(109):
  for j in range(i+1,110):
   b=mbasis([RM[i],RM[j]])
   for k in range(j+1,111):
    if independent(RM[k],b):
     indep+=1;m=OFa[i]&OFa[j]&OFa[k]
     if m not in flats:flats[m]=(i,j,k)
 assert indep==220934 and len(flats)==74396
 for m in flats:assert len(mbasis([full[k] for k in bits(m)],stop=5))==5
 catalog={};calls=0;family_calls=collections.Counter()
 def add(v,family):
  nonlocal calls
  calls+=1;family_calls[family]+=1;size=len(v);assert 4<=size<=8 and len(set(v))==size;mask=0;m=full111
  for i in v:mask|=1<<i;m&=T[i]
  two=m&mask;one=(m&~mask)&low[size];gain=2*two.bit_count()+one.bit_count()
  if gain>=13:catalog[mask]=(one,two,gain)
 for m,b in flats.items():
  V=[i for i,oi in enumerate(OFa) if oi&m==m]
  if len(V)<4:continue
  js=list(bits(O[b[0]]&O[b[1]]&O[b[2]]))
  for size in range(4,len(V)+1):
   for sub in itertools.combinations(V,size):
    add(sub,'rank3')
    for j in js:add(sub+(j,),'rank3_plus_isolated')
 print('Independent flat families complete',flush=True)
 for j in range(111):
  for sub in itertools.combinations(list(bits(O[j])),3):add(sub+(j,),'isolated_quad')
 clique_counts=collections.Counter()
 def walk(prefix,cand):
  while cand:
   bit=cand&-cand;i=bit.bit_length()-1;cand^=bit;new=prefix+(i,);clique_counts[len(new)]+=1
   if len(new)>=5:add(new,'orthogonal_clique')
   if len(new)<8:walk(new,cand&O[i])
 walk((),full111)
 assert calls==6329841 and len(catalog)==38324
 hist=dict(sorted(collections.Counter(x[2] for x in catalog.values()).items()));assert hist=={13:20290,14:9988,15:6912,16:1122,17:12}
 assert [clique_counts[i] for i in range(1,9)]==[111,3235,29939,90079,77003,35667,9443,1094]
 # Primary finite envelope13 coverage, including the r6/j5 and r7/j6 edge cases.
 N={0:0,1:1,2:3,3:6,4:12,5:20,6:36,7:111,8:111};ehist=collections.Counter(deg);envelope=[];critical=[]
 for r in range(1,9):
  for size in range(r,N[r]+1):
   for j in range(min(r,size)+1):
    if size>j+N[r-j]:continue
    gain=min(N[8-r],sum(n for d,n in ehist.items() if d<=52+size))+min(N[8-r],sum(n for d,n in ehist.items() if d<=36+size))+2*j;envelope.append([r,size,j,gain])
    if gain>=13:
     family=('rank3' if r==3 and 4<=size<=6 else 'isolated_quad' if r==4 and size==4 and j>=1 else 'rank3_plus_isolated' if r==4 and 5<=size<=7 and j>=1 else 'orthogonal_clique' if r==size and 5<=size<=8 and j>=r-1 else None)
     assert family is not None,(r,size,j,gain);critical.append([r,size,j,gain,family])
 assert len(envelope)==569 and any(row[:3]==[6,6,5] for row in critical) and any(row[:3]==[7,7,6] for row in critical)
 # Compare every source-derived class and its exact masks with the frozen author data.
 manraw=(a.root_bundle/'MANIFEST.json').read_bytes();assert hashlib.sha256(manraw).hexdigest()=='1c727243747e684b7d633fe4d76bc723c823909d4a221cfdb66fbe38565897e7'
 man=json.loads(manraw)
 for name,pin in man['artifacts'].items():assert hashlib.sha256((a.root_bundle/name).read_bytes()).hexdigest()==pin
 auth=json.loads(gzip.decompress((a.root_bundle/'CATALOG.json.gz').read_bytes()));expected={}
 for row in auth['rows']:
  mask=int(row['mask'],16);one=sum(1<<i for i in row['one_saving_rows']);two=sum(1<<i for i in row['two_saving_rows']);expected[mask]=(one,two,row['gain'])
 assert catalog==expected
 a.output.mkdir(parents=True,exist_ok=True);lines=[str(len(catalog))]
 for mask,(one,two,gain) in sorted(catalog.items()):lines.append(' '.join(map(str,[mask>>64,mask&((1<<64)-1),one>>64,one&((1<<64)-1),two>>64,two&((1<<64)-1),gain])))
 text='\n'.join(lines)+'\n';(a.output/'catalog-input.txt').write_text(text)
 out={'status':'PASS_INDEPENDENT_COMPLETE_BINARY_HIGH_GAIN_CATALOG','method':'PurePython full120 perpendicular-mask closures with Hadamard-certifiedF257 ranks; no author numpy/Gram-adjugate generator imported','source_sha256':hashlib.sha256(raw).hexdigest(),'root_manifest_sha256':hashlib.sha256(manraw).hexdigest(),'independent_triples':indep,'rank3_flats':len(flats),'candidate_calls':calls,'family_calls':dict(family_calls),'clique_counts':dict(clique_counts),'catalog_size':len(catalog),'gain_histogram':hist,'binary_code_distance':48,'minimum_zero_restriction_code_distance':18,'every_small_support_availability_exact_common_closed_neighborhood':True,'all38324_masks_gains_and_rowmasks_match_frozen_author':True,'envelope_cases':len(envelope),'all_cases_with_bound_at_least13':critical,'catalog_input_sha256':hashlib.sha256(text.encode()).hexdigest(),'scope':'Exact fixed-source binary high-coset catalogue; proof and independent cap screen needed for quotientdim4 conclusion.'}
 (a.output/'CATALOG-REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','candidate_calls','family_calls','catalog_size','gain_histogram','all_cases_with_bound_at_least13']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--root-bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
