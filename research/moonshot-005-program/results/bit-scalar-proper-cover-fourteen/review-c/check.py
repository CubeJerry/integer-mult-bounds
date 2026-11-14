#!/usr/bin/env python3
"""Independent sharp14 census and exact CRT determinant review."""
import argparse,gzip,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PROOF='fb861bffc473928cd872a8248096b092e85c657969459147b0cef5821ab83da2'
CASES='7567810dd8eab8add727a5d2e4371cb6af588d4e61630e62c43a07f7f5b45932'
MINORS='50672f8b51043afd72b9f35d3880a94e253679995a9eb03970c809aad7dc19fc'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def members(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x^=b
def mod_basis(rows,p,stop=None):
 piv={};chosen=[]
 for i,row in enumerate(rows):
  z=[x%p for x in row]
  for j,b in sorted(piv.items()):
   if z[j]:v=z[j];z=[(x-v*y)%p for x,y in zip(z,b)]
  j=next((a for a,x in enumerate(z) if x),None)
  if j is None:continue
  v=pow(z[j],-1,p);piv[j]=[x*v%p for x in z];chosen.append(i)
  if stop and len(chosen)==stop:break
 return chosen
def mod_det(rows,p):
 a=[[x%p for x in row] for row in rows];value=1;n=len(a)
 for c in range(n):
  i=next((j for j in range(c,n) if a[j][c]),None)
  if i is None:return 0
  if i!=c:a[i],a[c]=a[c],a[i];value=-value
  pivot=a[c][c];value=value*pivot%p;inverse=pow(pivot,-1,p);tail=a[c][c+1:]
  for j in range(c+1,n):
   if a[j][c]:
    v=a[j][c]*inverse%p;a[j][c+1:]=[(x-v*y)%p for x,y in zip(a[j][c+1:],tail)];a[j][c]=0
 return value%p
def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
def normalize(r):
 r=list(map(Fraction,r));s=(2 if sum(x*x for x in r)==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
 z=[x*s for x in r];need(all(x.denominator==1 for x in z),'integer root normalization');z=tuple(map(int,z));need(sum(x*x for x in z)==4,'root norm4');return z
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def rank3_census(R,adj,degree):
 patterns=sorted({tuple(i for i,x in enumerate(r) if x) for r in R if sum(x!=0 for x in r)==4})
 complete=[tuple(2*int(i==j) for i in range(8)) for j in range(8)]
 for S in patterns:
  for signs in itertools.product((-1,1),repeat=3):
   z=[0]*8;z[S[0]]=1
   for j,s in zip(S[1:],signs):z[j]=s
   complete.append(tuple(z))
 need(len(complete)==len(set(complete))==120 and set(R)<=set(complete),'completed120-root source')
 full_perp=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(complete)) for r in R]
 native_perp=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(R)) for r in complete]
 gram=[[dot(r,s) for s in R] for r in R];spaces={};independent=0
 for a,b,c in itertools.combinations(range(111),3):
  x,y,z=gram[a][b],gram[a][c],gram[b][c];det=64-4*(x*x+y*y+z*z)+2*x*y*z
  need(det>=0,'positive semidefinite real Gram matrix')
  if not det:continue
  independent+=1;mask=full_perp[a]&full_perp[b]&full_perp[c];spaces.setdefault(mask,(a,b,c))
 need(independent==220934 and len(spaces)==74396,'independent completed-root perpendicular census')
 critical=[];flat_masks=set();width_cases=0
 for mask,triple in spaces.items():
  perpendicular=list(members(mask));chosen=mod_basis([complete[j] for j in perpendicular],257,5)
  need(len(chosen)==5,'complete perpendicular roots span the full dimension5')
  flat=(1<<111)-1
  for j in chosen:flat&=native_perp[perpendicular[j]]
  flat_masks.add(flat);S=list(members(flat));need(3<=len(S)<=6 and all(flat>>j&1 for j in triple),'exact native double-perpendicular flat')
  if len(S)<5:continue
  common=adj[triple[0]]&adj[triple[1]]&adj[triple[2]];O=list(members(common))
  for width in (5,6):
   if width>len(S):continue
   width_cases+=1;eligible=[i for i in O if degree[i]<=52+width]
   if len(eligible)>=15:critical.append({'flat':S,'width':width,'orthogonal_roots':O,'eligible_count':len(eligible)})
 need(len(flat_masks)==74396 and width_cases==11761,'complete actual-flat/width domain')
 need(len(critical)==94 and Counter(e['eligible_count'] for e in critical)=={15:54,16:28,17:12} and all(e['width']==6 for e in critical),'complete new threshold15 catalogue')
 return critical,{'independent_triples':independent,'actual_rank3_flats':len(flat_masks),'width_cases':width_cases,'threshold15_cases':len(critical)}

def clique_census(adj,degree):
 current=[((i,),adj[i]) for i in range(111)];counts={};maxcommon={};critical4=[];critical7=[]
 for size in range(1,9):
  counts[size]=len(current)
  if size in (5,6):maxcommon[size]=max(common.bit_count() for S,common in current)
  for S,common in current:
   if size==4:
    eligible=[i for i in members(common) if degree[i]<=56];need(len(eligible)<=7,'orthogonal4 common eligible cap7')
    if len(eligible)==7:critical4.append({'support':list(S),'eligible_receivers':eligible,'orthogonal_roots':list(members(common))})
   if size==7:
    need(common.bit_count()<=1,'orthogonal7 has at most one native perpendicular line')
    eligible=[i for i in members(common) if degree[i]<=59]
    if eligible:critical7.append({'support':list(S),'eligible_receivers':eligible})
  if size<8:
   current=[(S+(j,),common&adj[j]) for S,common in current for j in members(common&~((1<<(S[-1]+1))-1))]
 need(counts=={1:111,2:3235,3:29939,4:90079,5:77003,6:35667,7:9443,8:1094},'complete iterative clique census')
 need(maxcommon=={5:3,6:2} and len(critical4)==2 and len(critical7)==6856,'orthogonal exceptional domains')
 mixed=0;maximum=0;witness=None
 for a,b in itertools.combinations(range(111),2):
  if adj[a]>>b&1:continue
  common=adj[a]&adj[b]
  for i in members(common):
   for j in members(common&adj[i]&~((1<<(i+1))-1)):
    mixed+=1;n=(common&adj[i]&adj[j]).bit_count()
    if n>maximum:maximum=n;witness=[i,j,a,b]
 need(mixed==663805 and maximum==6,'complete reversed-role mixed census')
 return critical4,critical7,{'orthogonal_counts':counts,'max_common':maxcommon,'mixed_configurations':mixed,'mixed_max_common':maximum,'mixed_witness':witness}

def main():
 ap=argparse.ArgumentParser()
 for name in ['native','author','output']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin')
 need(hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()==PROOF,'frozen proof pin')
 cr=(a.author/'output/CASES.json.gz').read_bytes();mr=(a.author/'output/MINORS.json.gz').read_bytes()
 need(hashlib.sha256(cr).hexdigest()==CASES and hashlib.sha256(mr).hexdigest()==MINORS,'exact author evidence pins')
 cases=json.loads(gzip.decompress(cr));certs=json.loads(gzip.decompress(mr));n=json.loads(gzip.decompress(raw))
 R=[normalize(n['frames'][str(n['start'][i])]['B'][0]) for i in range(111)]
 adj=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(R)) for r in R];degree=[x.bit_count() for x in adj]
 caps=[0,1,3,6,12,20,36,111,111];envelope=[]
 for r in range(1,9):
  for s in range(r,caps[r]+1):
   for j in range(min(r,s)+1):
    if s>j+caps[r-j]:continue
    bound=min(caps[8-r],sum(x<=52+s for x in degree))+min(caps[8-r],sum(x<=36+s for x in degree))+2*j
    envelope.append([r,s,j,bound])
 critical=[x for x in envelope if x[-1]>=15]
 need(len(envelope)==569 and critical==[[3,5,0,20],[3,6,0,20],[4,4,2,16],[4,4,3,18],[4,4,4,20],[4,5,2,16],[5,5,5,16],[6,6,6,15],[7,7,7,15],[8,8,8,16]],'all ten analytic cases')
 rank3,r3summary=rank3_census(R,adj,degree);print(json.dumps({'stage':'rank3','cases':len(rank3)}),flush=True)
 c4,c7,csummary=clique_census(adj,degree);print(json.dumps({'stage':'cliques','critical4':len(c4),'critical7':len(c7)}),flush=True)
 rowkey=lambda e:(tuple(e['flat']),e['width'],tuple(e['orthogonal_roots']),e['eligible_count'])
 need({rowkey(e) for e in rank3}=={rowkey(e) for e in cases['rank3']['critical']},'complete independent rank3 catalogue matches author')
 key4=lambda e:(tuple(e['support']),tuple(e['orthogonal_roots']),tuple(e['eligible_receivers']))
 key7=lambda e:(tuple(e['support']),tuple(e['eligible_receivers']))
 need({key4(e) for e in c4}=={key4(e) for e in cases['cliques']['critical_orthogonal4']},'complete independent orthogonal4 catalogue')
 need({key7(e) for e in c7}=={key7(e) for e in cases['cliques']['critical_orthogonal7']},'complete independent orthogonal7 catalogue')
 domains=[('rank3',e['flat'],e['orthogonal_roots']) for e in rank3]+[('orthogonal4',e['support'],e['orthogonal_roots']) for e in c4]+[('orthogonal7',e['support'],e['eligible_receivers']) for e in c7]
 expected={(kind,tuple(S),i) for kind,S,O in domains for i in O};need(len(expected)==len(certs)==8737,'exact required minor domain')
 verify_minors(a,R,adj,expected,certs,critical,r3summary,csummary)

def verify_minors(a,R,adj,expected,certs,critical,r3summary,csummary):
 primes=[1000000007,1000000009];bound=4**28
 need(all(prime(p) for p in primes) and math.prod(primes)>2*bound,'CRT modulus exceeds twice exact Hadamard bound')
 mons8=list(itertools.combinations_with_replacement(range(8),2));mons7=list(itertools.combinations_with_replacement(range(7),2))
 Q=[[r[b]*r[c] for b,c in mons8] for r in R];seen=set();fresh=[];first=None
 for number,cert in enumerate(certs,1):
  kind,S,i=cert['kind'],cert['deleted'],cert['receiver'];key=(kind,tuple(S),i)
  need(key in expected and key not in seen,'no missing or repeated exceptional case');seen.add(key)
  points=[j for j in members(adj[i]) if j not in S];need(all(adj[i]>>j&1 for j in S),'deleted support orthogonal to receiver')
  rows,cols=cert['minor_rows'],cert['minor_columns'];need(len(rows)==len(set(rows))==28 and set(rows)<=set(points),'author minor source support')
  need(len(cols)==len(set(cols))==28 and all(0<=c<36 for c in cols),'author minor monomial columns')
  matrix=[[Q[j][c] for c in cols] for j in rows];value=int(cert['determinant'])
  need(0<abs(value)<=bound and all(sum(x*x for x in row)<=16 for row in matrix),'exact determinant range and Hadamard premise')
  need(all(mod_det(matrix,p)==value%p for p in primes),'independent exact determinant via CRT and Hadamard uniqueness')
  pivot=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=pivot]
  projected=[[R[j][free[b]]*R[j][free[c]] for b,c in mons7] for j in points]
  chosen=mod_basis(projected,509,28);need(len(chosen)==28,'fresh seven-dimensional facet quadratic minor')
  fresh.append({'kind':kind,'deleted':S,'receiver':i,'mod509_facet_basis':[points[j] for j in chosen]})
  if first is None:first=matrix
  if number%1000==0:print(json.dumps({'stage':'exact_minors','checked':number}),flush=True)
 need(seen==expected,'exact8737-case completeness')
 duplicate=[list(r) for r in first];duplicate[0]=list(duplicate[1]);need(all(mod_det(duplicate,p)==0 for p in primes),'duplicate-row negative control')
 altered=int(certs[0]['determinant'])+1;need(any(mod_det(first,p)!=altered%p for p in primes),'changed determinant rejected')
 canonical=[]
 for i in range(111):
  pivot=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=pivot];points=list(members(adj[i]))
  projected=[[R[j][free[b]]*R[j][free[c]] for b,c in mons7] for j in points]
  chosen=mod_basis(projected,509,28);need(len(chosen)==28,'all canonical rows have exact cover charge2')
  canonical.append({'receiver':i,'mod509_facet_basis':[points[j] for j in chosen]})
 S=[54,56,57,59,61,63,64];need(all(adj[i]>>j&1 for i,j in itertools.combinations(S,2)),'sharp seven-line support')
 need(all(len(mod_basis([R[j] for j in S if j!=i],509))==6 for i in S),'proper rank-six foreign supports')
 a.output.mkdir(parents=True,exist_ok=True)
 blob=gzip.compress(json.dumps({'exceptional':fresh,'canonical':canonical},sort_keys=True,separators=(',',':')).encode(),mtime=0)
 (a.output/'INDEPENDENT-MINORS.json.gz').write_bytes(blob)
 out={'status':'PASS_INDEPENDENT_SHARP_PROPER_COVER_FOURTEEN','reviewed_proof_sha256':PROOF,'native_sha256':PIN,
      'author_cases_sha256':CASES,'author_minors_sha256':MINORS,'analytic_parameter_cases':569,'ten_critical_cases':critical,
      'independent_rank3_census':r3summary,'independent_clique_and_mixed_census':csummary,
      'exact_integer_determinants_verified':len(certs),'CRT_primes':primes,'determinant_absolute_Hadamard_bound':str(bound),
      'independent_facet_minors_sha256':hashlib.sha256(blob).hexdigest(),'canonical_quadratic_rank28_cases':111,
      'sharp_positive_chi_saving':14,'negative_controls':['duplicated source row','altered claimed determinant'],
      'classification':'complete independent finite source premises plus separately reviewed all-field proof; no new kappa','new_kappa':None}
 (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'exact_minors':len(certs)}),flush=True)

if __name__=='__main__':main()
