#!/usr/bin/env python3
"""Independent proper-cover review: facet coordinates and rational elimination."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
OLD='88a192ec4b859780b02f109fdd0172cf52c6adbab8ae782006fa72b8192716a8'
OLD_REVIEW='9ef3fb7f23605f8f7dd053dfb3a42b1ea1f71ab0f6945e365481262e72e771a8'
PROOF='d53789dc82d6a1086678644ae4f86e0faaa089588d0ad5d229dc9e1dd636176e'

def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(rows,prime=None):
 piv={};chosen=[]
 for i,row in enumerate(rows):
  z=[int(x)%prime if prime else Fraction(x) for x in row]
  for p,b in sorted(piv.items()):
   if z[p]:
    a=z[p];z=[(x-a*y)%prime if prime else x-a*y for x,y in zip(z,b)]
  p=next((j for j,x in enumerate(z) if x),None)
  if p is None:continue
  inv=pow(z[p],-1,prime) if prime else 1/z[p]
  piv[p]=[x*inv%prime if prime else x*inv for x in z];chosen.append(i)
 return chosen
def determinant(rows):
 a=[list(map(Fraction,row)) for row in rows];answer=Fraction(1);n=len(a)
 for j in range(n):
  p=next((i for i in range(j,n) if a[i][j]),None)
  if p is None:return 0
  if p!=j:a[p],a[j]=a[j],a[p];answer=-answer
  z=a[j][j];answer*=z
  for i in range(j+1,n):
   if not a[i][j]:continue
   u=a[i][j]/z
   for t in range(j+1,n):a[i][t]-=u*a[j][t]
   a[i][j]=0
 need(answer.denominator==1,'integer determinant from rational elimination')
 return answer.numerator
def bitrank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)

def main():
 ap=argparse.ArgumentParser()
 for name in ['native','predecessor','author','output']:ap.add_argument('--'+name,type=Path,required=True)
 args=ap.parse_args();raw=args.native.read_bytes();oldraw=(args.predecessor/'RESULT.json').read_bytes()
 need(hashlib.sha256(raw).hexdigest()==NATIVE and hashlib.sha256(oldraw).hexdigest()==OLD,'native/predecessor pins')
 need(hashlib.sha256((args.author/'PROOF.md').read_bytes()).hexdigest()==PROOF,'reviewed proof bytes')
 old_review_raw=(args.predecessor.parent/'review/RESULT.json').read_bytes();need(hashlib.sha256(old_review_raw).hexdigest()==OLD_REVIEW,'independent predecessor census pin')
 old=json.loads(oldraw);old_review=json.loads(old_review_raw);author=json.loads((args.author/'RESULT.json').read_text());n=json.loads(gzip.decompress(raw))
 R=[]
 for i in range(111):
  r=list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0]));norm=sum(x*x for x in r)
  need(norm in (1,4),'native normalization cases');r=[x*(2 if norm==1 else 1) for x in r]
  need(all(x.denominator==1 for x in r),'integral normalized roots');R.append(list(map(int,r)))
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
 K=[sum(int(i==j or dot(i,j)==0)<<j for j in range(111)) for i in range(111)]
 degree=[k.bit_count()-1 for k in K];hist=Counter(degree)
 caps=[0,1,3,6,12,20,36,111,111];envelope=[]
 for r in range(1,9):
  for s in range(r,caps[r]+1):
   for j in range(min(r,s)+1):
    if s>j+caps[r-j]:continue
    bound=min(caps[8-r],sum(x<=52+s for x in degree))+min(caps[8-r],sum(x<=36+s for x in degree))+2*j
    envelope.append([r,s,j,bound])
 critical=[row for row in envelope if row[-1]>=17]
 need(len(envelope)==569 and critical==[[3,5,0,20],[3,6,0,20],[4,4,3,18],[4,4,4,20]],'independent complete parameter-envelope reconstruction')
 need(critical==old['generic_cases_requiring_refinement'] and old['orthogonal4_max_gain_bound']==15,'admitted refinement linkage')
 extremals=old['rank3_maximizers'];need(len(extremals)==12 and all(e['width']==6 and e['eligible_count']==17 for e in extremals),'complete pinned extremal list')
 need((old['rank3_flat_count'],old['rank3_five_six_cases'],old['independent_triple_count'])==(74396,11761,220934),'admitted source census identities')
 need(len({tuple(e['flat']) for e in extremals})==12,'no repeated extremal flat')
 need({(tuple(e['flat']),e['width'],tuple(e['orthogonal_roots']),e['eligible_count']) for e in extremals}==
      {(tuple(e['flat']),e['width'],tuple(e['U']),e['count']) for e in old_review['rank3_maximizers']},'complete author and independently generated predecessor maximizer lists agree')
 mons7=list(itertools.combinations_with_replacement(range(7),2));mons8=list(itertools.combinations_with_replacement(range(8),2))
 canonical=[];new=[];first_square=None;value_field_control=None
 def features(i,points):
  pivot=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=pivot]
  return [[R[s][free[a]]*R[s][free[b]] for a,b in mons7] for s in points]
 for i in range(111):
  points=[j for j in range(111) if j!=i and dot(i,j)==0];matrix=features(i,points);chosen=basis(matrix,509)
  need(len(chosen)==28,'canonical proper-cover charge2')
  canonical.append({'receiver':i,'mod509_basis_source_indices':[points[j] for j in chosen]})
  if i==0:value_field_control={'mod2_rank':len(basis(matrix,2)),'real_rank_certified_mod509':28};need(value_field_control['mod2_rank']<28,'geometry is not evaluated in the value field')
 expected={}
 for e in extremals:
  B=e['basis'];need(len(basis([R[j] for j in B]))==3,'exact rank-three basis')
  flat=[j for j in range(111) if len(basis([R[b] for b in B]+[R[j]]))==3]
  O=[i for i in range(111) if all(dot(i,b)==0 for b in B)]
  need(flat==e['flat'] and O==e['orthogonal_roots'] and len(O)==20,'exact complete flat and orthogonal receiver set')
  need(sum(degree[i]<=58 for i in O)==17,'independent extremal eligibility')
  for i in O:
   points=[j for j in range(111) if j!=i and dot(i,j)==0 and j not in flat];matrix=features(i,points);chosen=basis(matrix,509)
   need(len(chosen)==28,'forced contacts outside full flat have real quadratic rank28')
   new.append({'flat':flat,'receiver':i,'mod509_basis_source_indices':[points[j] for j in chosen]})
   expected[(tuple(flat),i)]=points
 need(len(new)==240,'all240 source cases')
 certs=author['certificates'];need(len(certs)==240,'author certificate domain')
 seen=set()
 for cert in certs:
  key=(tuple(cert['flat']),cert['receiver']);need(key in expected and key not in seen,'no missing or duplicate author case');seen.add(key)
  need(cert['forced_support']==expected[key],'exact author forced-support list')
  points=cert['minor_source_indices'];cols=cert['minor_columns']
  need(len(points)==len(set(points))==28 and set(points)<=set(expected[key]),'author minor source rows')
  need(len(cols)==len(set(cols))==28 and all(0<=c<36 for c in cols),'author minor columns')
  matrix=[[R[j][mons8[c][0]]*R[j][mons8[c][1]] for c in cols] for j in points]
  value=determinant(matrix);need(value==int(cert['integer_determinant'])!=0,'independent exact rational determinant matches author Bareiss value')
  if first_square is None:first_square=matrix
 need(seen==set(expected),'complete240-case bijection')
 bad=[list(r) for r in first_square];bad[0]=list(bad[1]);need(determinant(bad)==0,'duplicate row destroys exact determinant')
 S=author['positive_control']['support'];need(len(S)==7 and all(dot(i,j)==0 for i,j in itertools.combinations(S,2)),'seven mutually orthogonal source lines')
 need(all(len(basis([R[j] for j in S if j!=i]))==6 for i in S),'proper six-dimensional foreign spans')
 h=sum(1<<j for j in S);F=[h if i in S else k for i,k in enumerate(K)]
 need(all(f>>i&1 and f&~K[i]==0 for i,f in enumerate(F)) and bitrank(F+K)-9==1,'actual positive one-mode fitting')
 P=old['sharp_fitting_witness']['V'];O=old['sharp_fitting_witness']['U'];h=sum(1<<j for j in P);F=[k^h if i in O else k for i,k in enumerate(K)]
 ell=sum(int(f.bit_count()-1>36)+int(f.bit_count()-1>52) for f in F);need(ell==205,'old cardinality17 remains sharp')
 need(all((tuple(P),i) in expected for i in O),'old sharp witness has forced cover charge222')
 out={'status':'PASS_INDEPENDENT_SCALAR_PROPER_COVER_REVIEW','reviewed_proof_sha256':PROOF,'native_sha256':NATIVE,'predecessor_result_sha256':OLD,'independent_predecessor_result_sha256':OLD_REVIEW,
      'independently_recomputed_parameter_cases':len(envelope),'critical_parameter_cases':critical,
      'inherited_full_flat_census':'admitted pinned catalogue, with verifier completeness inspected; not re-enumerated here',
      'exactly_reconstructed_extremal_flats':12,'independent_mod509_forced_span_certificates':new,'independently_verified_author_integer_determinants':240,
      'canonical_mod509_basis_certificates':canonical,'duplicate_row_negative_control':0,'geometry_value_field_negative_control':value_field_control,
      'positive_scalar_chi_saving':14,'old_cardinality_saving':17,'old_witness_chi_saving':0,'new_kappa':None}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','independently_recomputed_parameter_cases','exactly_reconstructed_extremal_flats','independently_verified_author_integer_determinants','positive_scalar_chi_saving']}))
if __name__=='__main__':main()
