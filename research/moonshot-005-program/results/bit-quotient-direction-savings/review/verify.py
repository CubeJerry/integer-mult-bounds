"""Independent exact census via perpendicular masks and certified F257 ranks."""
import argparse,collections,gzip,hashlib,itertools,json,math,time
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
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
 assert hashlib.sha256((a.root_bundle/'MANIFEST.json').read_bytes()).hexdigest()=='28ff4b32f40de703469d9f159c1674089dae36f23f6f9dbd0e52ffcb956759c9'
 man=json.loads((a.root_bundle/'MANIFEST.json').read_text())
 for name,pin in man['artifacts'].items():assert hashlib.sha256((a.root_bundle/name).read_bytes()).hexdigest()==pin
 author=json.loads((a.root_bundle/'RESULT.json').read_text());raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(raw));fr={int(k):v for k,v in s['frames'].items()};R=[]
 for i in range(111):
  v=[F(x) for x in fr[s['start'][i]]['B'][0]];n=dot(v,v);assert n in [1,4];v=[int(x*(2 if n==1 else 1)) for x in v];assert dot(v,v)==4;R.append(canon(v))
 assert len(set(R))==111
 supports={tuple(i for i,x in enumerate(v) if x) for v in R if sum(bool(x) for x in v)==4};assert len(supports)==14
 full={tuple(2*int(i==j) for j in range(8)) for i in range(8)}
 for S in supports:
  for signs in itertools.product([-1,1],repeat=4):
   v=[0]*8
   for j,c in zip(S,signs):v[j]=c
   full.add(canon(v))
 full=sorted(full);assert len(full)==120 and all(v in full for v in R)
 OF=[sum(1<<j for j,v in enumerate(full) if dot(u,v)==0) for u in full];ids=[full.index(v) for v in R];OFactual=[OF[i] for i in ids]
 O=[sum(1<<j for j,v in enumerate(R) if dot(u,v)==0) for u in R];deg=[m.bit_count() for m in O];hist=dict(sorted(collections.Counter(deg).items()));assert hist=={55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}
 # Every s-by-s integer root minor has abs(det)<=2^s<=256<257.
 # Therefore rank over F257 equals rank over R for all these root subsets.
 assert all(dot(v,v)==4 for v in full) and P>2**8
 RM=[[x%P for x in v] for v in R];flats={};indep=0
 for i in range(109):
  for j in range(i+1,110):
   b=mbasis([RM[i],RM[j]]);assert len(b)==2
   for k in range(j+1,111):
    if not independent(RM[k],b):continue
    indep+=1;m=OFactual[i]&OFactual[j]&OFactual[k]
    if m not in flats:flats[m]=(i,j,k)
 assert indep==220934 and len(flats)==74396
 print('Enumerated220934 independent triples via F257',flush=True)
 low={c:sum(1<<i for i,d in enumerate(deg) if d<=c) for c in [56,57,58]};closure_seen=set();cases=[];max3=0;maxcases=[];digest=hashlib.sha256();maxsize=0
 for m,b in flats.items():
  assert len(mbasis([full[k] for k in bits(m)],stop=5))==5
  # Perpendicular roots span the FULL real5D complement, so this closure is exact.
  closure=sum(1<<i for i,oi in enumerate(OFactual) if oi&m==m);assert closure not in closure_seen;closure_seen.add(closure);size=closure.bit_count();maxsize=max(maxsize,size);assert all(closure>>i&1 for i in b)
  u=O[b[0]]&O[b[1]]&O[b[2]];digest.update((str(b)+':'+hex(m)+':'+hex(closure)+'\n').encode())
  for width in [5,6]:
   if size<width:continue
   eligible=u&low[52+width];n=eligible.bit_count();record={'basis':list(b),'flat':list(bits(closure)),'width':width,'U':list(bits(u)),'eligible':list(bits(eligible)),'count':n};cases.append(record)
   if n>max3:max3=n;maxcases=[record]
   elif n==max3:maxcases.append(record)
 assert maxsize==6 and len(cases)==11761 and max3==17
 count4=0;max4=0;witness4=None;quad_digest=hashlib.sha256();full111=(1<<111)-1
 def higher(i):return full111^((1<<(i+1))-1)
 for i in range(111):
  ni=O[i]&higher(i)
  for j in bits(ni):
   nj=ni&O[j]&higher(j)
   for k in bits(nj):
    nk=nj&O[k]&higher(k)
    for l in bits(nk):
     count4+=1;u=O[i]&O[j]&O[k]&O[l];n=(u&low[56]).bit_count();quad_digest.update(f'{i},{j},{k},{l}:{n}\n'.encode())
     if n>max4:max4=n;witness4={'basis':[i,j,k,l],'eligible':list(bits(u&low[56]))}
 assert count4==90079 and max4==7
 print('Exact perpendicular closures and90079 orthogonal4 sets verified',flush=True)
 N={0:0,1:1,2:3,3:6,4:12,5:20,6:36,7:111,8:111};envelope=[]
 for j in range(9):
  for r in range(max(1,j),9):
   for width in range(r,min(N[r],j+N[r-j])+1):
    if j>width:continue
    u=N[8-r];h1=sum(n for d,n in hist.items() if d<=52+width);h2=sum(n for d,n in hist.items() if d<=36+width);bound=min(u,h1)+min(u,h2)+2*j;envelope.append([r,width,j,bound])
 critical=sorted(row for row in envelope if row[3]>=17);assert len(envelope)==569 and critical==[[3,5,0,20],[3,6,0,20],[4,4,3,18],[4,4,4,20]]
 V=[0,2,38,41,42,45];vm=sum(1<<j for j in V);um=full111
 for v in V:um&=O[v]
 assert um.bit_count()==20 and not um&vm
 K=[m|(1<<i) for i,m in enumerate(O)];fit=[r^(vm if um>>i&1 else 0) for i,r in enumerate(K)];weights=[r.bit_count()-1 for r in fit];vis=sum(int(w>52)+int(w>36) for w in weights)
 assert brank(K)==9 and brank(fit)==10 and vis==205 and sum((r^k).bit_count() for r,k in zip(fit,K))==120
 assert all(fit[i]>>i&1 and not(fit[i]&~K[i]) for i in range(111))
 for key,value in [('independent_triple_count',indep),('rank3_flat_count',len(flats)),('rank3_five_six_cases',len(cases)),('rank3_maximum_eligible_gain',max3),('orthogonal4_count',count4)]:assert author[key]==value
 assert author['orthogonal4_max_gain_bound']==max4+8
 # Bonus premise for the separate overlap refinement; not used for17 proof.
 assert len(maxcases)==12 and all(c['width']==6 for c in maxcases)
 overlap=min(len(set(c['eligible'])&set(d['eligible'])) for c,d in itertools.combinations(maxcases,2));assert overlap==5
 out={'status':'PASS_INDEPENDENT_17_SAVINGS_PROOF_SOURCE_PREMISES','reviewed_manifest_sha256':'28ff4b32f40de703469d9f159c1674089dae36f23f6f9dbd0e52ffcb956759c9','reviewed_proof_sha256':'8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b','method':'Pure Python perpendicular masks on independently completed120 roots; F257 rank equals real rank by Hadamard minor bound256; no Gram3 determinant/adjugate membership and no author numpy imported.','source_sha256':hashlib.sha256(raw).hexdigest(),'foreign_histogram':hist,'modular_rank_prime':257,'Hadamard_minor_absolute_upper':256,'all_perpendicular_root_sets_span_full_dimension5':True,'independent_triples':indep,'distinct_real_rank3_flats':len(flats),'flat_census_sha256':digest.hexdigest(),'relevant_width5_6_cases':len(cases),'max_rank3_eligible':max3,'rank3_maximizers':maxcases,'orthogonal4_count':count4,'max_orthogonal4_eligible':max4,'orthogonal4_witness':witness4,'quadruple_census_sha256':quad_digest.hexdigest(),'parameter_cases':len(envelope),'critical_parameter_cases':critical,'sharp_witness':{'V':V,'U':list(bits(um)),'fitting_binary_rank':10,'foreign_changes':120,'ell_sum':205,'proxy_saved_visits':17,'physical205_visits_realization_claimed':False},'all_field_scalar_proof_scope':True,'F2_F4_quotient_dimension_at_least3_scope':True,'arbitrary_rank12_bound_claimed':False,'bonus_for_separate_overlap_refinement':{'max17_cases':len(maxcases),'all_width6':True,'minimum_pair_required_set_overlap':overlap,'not_needed_for17_proof':True}}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','independent_triples','distinct_real_rank3_flats','relevant_width5_6_cases','max_rank3_eligible','orthogonal4_count','max_orthogonal4_eligible','parameter_cases','sharp_witness','bonus_for_separate_overlap_refinement']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--root-bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
