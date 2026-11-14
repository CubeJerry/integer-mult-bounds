#!/usr/bin/env python3
"""Exact full-halfclass quotient gate premises; universal proof in PROOF.md."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def members(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x^=b
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def normalize(r):
 r=list(map(Fraction,r));s=(2 if dot(r,r)==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
 z=[x*s for x in r];need(all(x.denominator==1 for x in z),'integer normalization');z=tuple(map(int,z));need(dot(z,z)==4,'norm4');return z
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
def basis(rows):
 piv={};out=[]
 for v in rows:
  x=v
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;out.append(v);break
 return out
def rank(rows):return len(basis(rows))
def xor_words(rows):
 out=0
 for r in rows:out^=r
 return out
def words(B):
 out=[0]
 for b in B:out += [x^b for x in list(out)]
 return out
def support(r):return tuple(j for j,x in enumerate(r) if x)
def quad_matrix(q):
 M=[[0]*7 for _ in range(7)]
 for c,(i,j) in zip(q,itertools.combinations_with_replacement(range(7),2)):
  M[i][j]=2*c if i==j else c
  if i!=j:M[j][i]=c
 return M
def norm_quad(r,P):
 p=next(i for i,x in enumerate(r) if x);free=[i for i in range(8) if i!=p]
 sigma=[1 if i in P else -1 for i in range(8)]
 M=[[Fraction(sigma[a]*int(a==b))+sigma[p]*Fraction(r[a]*r[b],r[p]*r[p]) for b in free] for a in free]
 q=[M[a][b]*(1 if a==b else 2) for a,b in itertools.combinations_with_replacement(range(7),2)]
 need(all(x.denominator==1 for x in q),'integral restricted split-norm form')
 return list(map(int,q))
def trim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def add(a,b):
 z=[0]*max(len(a),len(b))
 for i,x in enumerate(a):z[i]+=x
 for i,x in enumerate(b):z[i]+=x
 return trim(z)
def mult(a,b):
 z=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 return trim(z)
def det_pencil3(A,B,rows,cols):
 out=[0]
 for perm in itertools.permutations(range(3)):
  parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));p=[(-1)**parity]
  for i,j in enumerate(perm):p=mult(p,[A[rows[i]][cols[j]],B[rows[i]][cols[j]]])
  out=add(out,p)
 return out
def minor_certificate(R,i,points,expected):
 p=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=p];mons=list(itertools.combinations_with_replacement(range(7),2))
 rows=[[R[j][free[a]]*R[j][free[b]] for a,b in mons] for j in points]
 chosen=mod_basis(rows,509);need(len(chosen)==expected,'exact lower quadratic rank')
 selected=[rows[j] for j in chosen];cols=mod_basis(list(map(list,zip(*selected))),509);need(len(cols)==expected,'square minor columns')
 value=mod_det([[row[j] for j in cols] for row in selected],509);need(value!=0,'exact nonzero integer minor')
 return {'receiver':i,'points':points,'facet_free_coordinates':free,'minor_roots':[points[j] for j in chosen],
         'minor_columns':cols,'determinant_mod509':value,'rank':expected},rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw))
 R=[normalize(n['frames'][str(n['start'][i])]['B'][0]) for i in range(111)]
 need([i for i,r in enumerate(R) if len(support(r))==1]==list(range(8)) and all(R[i]==tuple(2*int(i==j) for j in range(8)) for i in range(8)),'eight exact coordinate roots')
 K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(R)) for i,r in enumerate(R)]
 C=basis(K);code=words(C);need(len(C)==9 and len(set(code))==512 and min(x.bit_count() for x in code if x)==48,'canonical rank9 and distance48')
 distances=[min(x.bit_count() for x in {c&~k for c in code} if x) for k in K]
 need(Counter(distances)=={18:7,19:24,20:52,21:16,22:11,23:1},'all forbidden restriction distances')
 groups={}
 for i,r in enumerate(R):groups.setdefault((support(r),sum(x<0 for x in r)%2),[]).append(i)
 groups=list(groups.values());hs=[sum(1<<j for j in g) for g in groups];B=basis(C+hs)
 need(len(groups)==36 and max(map(len,groups))==4 and len(B)==39,'full halfclass reservoir')
 RC=[c for c in code if all(len({(c>>j)&1 for j in g})==1 for g in groups)]
 need(len(RC)==64 and rank(RC)==6,'canonical indicator intersection dimension6')
 Gi=[sum(int(not(h&~k))<<g for g,h in enumerate(hs)) for k in K]
 local_support=[xor_words(hs[g] for g in members(x)) for x in Gi];local_records=[]
 for i,k in enumerate(K):
  L=[hs[g] for g in members(Gi[i])];dimension=39-rank([b&~k for b in B]);expected=len(L)+int(i>=8)
  need(dimension==expected and rank(L+[k])==expected,'complete local span identity')
  need((k in RC)==(i<8),'canonical row is group-constant precisely at coordinate ports')
  local_records.append({'receiver':i,'local_groups':list(members(Gi[i])),'local_dimension':dimension,'local_source_support':list(members(local_support[i]))})
 need(max(x.bit_count() for x in local_support[8:])==20,'maximum literal noncoordinate local support20')
 patterns=sorted({support(r) for r in R[8:]});families=[(P,tuple(j for j in range(8) if j not in P)) for P in patterns if P<tuple(j for j in range(8) if j not in P)]
 need(len(patterns)==14 and len(families)==7 and families[0]==((0,1,2,3),(4,5,6,7)),'seven complementary families')
 family={i:next(f for f,pair in enumerate(families) if support(R[i]) in pair) for i in range(8,111)}
 Wgroups=[g for g,G in enumerate(groups) if len(G) in (1,2)];Wmask=sum(1<<g for g in Wgroups);X=xor_words(hs[g] for g in Wgroups)
 need(Wgroups==[0,1,2,3,4,5,6,7,9,18] and list(members(X))==[0,1,2,3,4,5,6,7,9,11,46,50],'small common support W')
 max_union=0;cross=0
 for i,j in itertools.combinations(range(8,111),2):
  max_union=max(max_union,(local_support[i]|local_support[j]).bit_count())
  if family[i]!=family[j]:cross+=1;need(not(Gi[i]&Gi[j]&~Wmask),'every cross-family local intersection lies in W')
 need(max_union==34 and cross==4543,'exact pair union and cross-family counts')
 family_records=[];six=[];coordinate_subcodes=[]
 for f,pair in enumerate(families):
  fg=[g for g,G in enumerate(groups) if support(R[G[0]]) in pair];need(len(fg)==4,'four halfclasses per family')
  bg=sorted(set(Wgroups)|set(fg));XF=xor_words(hs[g] for g in bg);pts=[i for i in range(8,111) if family[i]==f]
  need(XF.bit_count()<48 and all(not(Gi[i]&~sum(1<<g for g in bg)) for i in pts),'all local family spaces lie in B_F')
  family_records.append({'family':f,'coordinate_supports':[list(x) for x in pair],'groups':fg,'enlarged_groups':bg,'actual_source_support':list(members(XF))})
  for S in itertools.combinations(pts,6):
   if not all(K[i]>>j&1 for i,j in itertools.combinations(S,2)):continue
   common=(1<<36)-1
   for i in S:common&=Gi[i]
   cg=list(members(common));need(len(cg)==2,'six-row common literal span has two groups')
   union=set(groups[cg[0]])|set(groups[cg[1]])
   need(set(S)<=union and all(set(S)&set(groups[g]) for g in cg),'six rows meet and lie in both common groups')
   need({support(R[groups[g][0]]) for g in cg}==set(pair),'common groups have complementary supports')
   six.append({'family':f,'receivers':list(S),'common_groups':cg})
  for i in range(8):
   permitted=[c for c in RC if not(c&~K[i]&~XF)]
   need(set(permitted)=={0,K[i]},'coordinate canonical subcode outside enlarged family is exactly K_i')
   coordinate_subcodes.append({'family':f,'receiver':i,'allowed_codewords_hex':list(map(hex,permitted))})
 need(len(six)==501 and [len(e['actual_source_support']) for e in family_records]==[26,27,28,27,28,23,24],'complete common-six and enlarged supports')
 print(json.dumps({'stage':'algebra','rank_C':9,'rank_C_plus_U':39,'rank_R':6,'local_max':20,'pair_union_max':34,'cross_family_pairs':cross,'common_six_cases':len(six)}),flush=True)
 verify_geometry(a,R,K,C,groups,hs,Gi,local_support,X,local_records,family_records,six,coordinate_subcodes,distances)
def verify_geometry(a,R,K,C,groups,hs,Gi,local_support,X,local_records,family_records,six,coordinate_subcodes,distances):
 need(all(509%d for d in range(2,23)),'modulus509 is prime')
 certs=[];first_full=None;pencils=[]
 for i in range(8,111):
  points=[j for j in members(K[i]&~local_support[i]) if j!=i]
  cert,rows=minor_certificate(R,i,points,27);q=norm_quad(R[i],support(R[i]));M=quad_matrix(q)
  need(all(dot(row,q)==0 for row in rows) and mod_det(M,509)!=0,'unique rank7 split-norm quadratic')
  need(len(mod_basis([R[j] for j in points],509))==7,'linear rank7 geometric false-positive control')
  cert.update({'kind':'noncoordinate_local','quadratic_kernel':q,'symmetric_matrix_determinant_mod509':mod_det(M,509)})
  certs.append(cert)
 for i in range(111):
  points=[j for j in members(K[i]&~X) if j!=i];cert,rows=minor_certificate(R,i,points,28)
  cert['kind']='outside_W';certs.append(cert)
  if first_full is None:first_full=[rows[points.index(j)] for j in cert['minor_roots']]
 need(mod_det([first_full[0]]+first_full[:-1],509)==0,'duplicate-row negative control')
 rank_census=Counter()
 for family in family_records:
  f=family['family'];P=family['coordinate_supports'][0];XF=sum(1<<j for j in family['actual_source_support'])
  for i in range(8):
   points=[j for j in members(K[i]&~XF) if j!=i];expected=26 if f==0 and i in (0,3) else 27
   cert,rows=minor_certificate(R,i,points,expected);rank_census[expected]+=1
   cert.update({'kind':'coordinate_family','family':f})
   if expected==27:
    q=norm_quad(R[i],P);M=quad_matrix(q);need(all(dot(row,q)==0 for row in rows) and mod_det(M,509)!=0,'coordinate split-norm unique rank7 kernel')
    cert.update({'quadratic_kernel':q,'symmetric_matrix_determinant_mod509':mod_det(M,509)})
   else:
    q0=[0]*28;q0[1 if i==0 else 8]=1;q0[21]=-1;q0[23]=1
    q1=[0]*28
    for j in (0,7,13):q1[j]=-1
    for j in (18,22,25,27):q1[j]=1
    need(all(dot(row,q0)==dot(row,q1)==0 for row in rows) and len(mod_basis([q0,q1],509))==2,'exact two-dimensional quadratic kernel')
    A,B=quad_matrix(q0),quad_matrix(q1);need(mod_det(B,509)!=0 and len(mod_basis(A,509))==6,'pencil endpoint ranks6 and7')
    ra,ca,rb,cb=((0,1,3),(0,1,6),(0,2,3),(0,2,3)) if i==0 else ((1,2,3),(1,2,6),(0,1,3),(0,1,3))
    p,q=det_pencil3(A,B,ra,ca),det_pencil3(A,B,rb,cb)
    need(p==[1,0,-4] and q==[0,0,0,8] and add(mult([1,0,4],p),mult([0,2],q))==[1],'exact Bezout identity rules out every rank<=2 pencil member')
    item={'family':f,'receiver':i,'quadratic_basis':[q0,q1],'minor_p':{'rows':ra,'columns':ca,'coefficients':p},
          'minor_q':{'rows':rb,'columns':cb,'coefficients':q},'bezout_multipliers':[[1,0,4],[0,2]],'bezout_result':[1],
          'infinity_matrix_determinant_mod509':mod_det(B,509)}
    pencils.append(item);cert['pencil_index']=len(pencils)-1
   certs.append(cert)
 need(len(certs)==270 and rank_census=={27:54,26:2},'complete exact geometric certificate domain')
 S1=[54,56,57,59,61,63,64];S2=[52,53,55,58,60,62,65]
 need(not(set(S1)&set(S2)) and all(all(K[i]>>j&1 for i,j in itertools.combinations(S,2)) for S in (S1,S2)),'two disjoint native seven-cliques')
 h=[sum(1<<j for j in S) for S in (S1,S2)]
 need(all(all(len({(x>>j)&1 for j in g})==1 for g in groups) for x in h),'boundary directions lie in complete halfclass reservoir')
 def lift(word,t):return sum(((word>>j)&1)<<(2*j+t) for j in range(111))
 AR=[]
 for i,k in enumerate(K):
  word=h[0] if i in S1 else h[1] if i in S2 else k
  need(word>>i&1 and not(word&~k),'dimension4 boundary fitting')
  AR += [lift(word,t) for t in range(2)]
 CV=[lift(c,t) for c in C for t in range(2)]
 need(rank(AR+CV)-18==4 and all(len(mod_basis([R[j] for j in S if j!=i],509))==6 for S in (S1,S2) for i in S),'exact quotient4 chi194 boundary')
 result={'status':'PASS_FULL_HALFCLASS_QUOTIENT3_GATE_PREMISES','native_sha256':PIN,
         'dimensions':{'C':9,'U':36,'C_plus_U':39,'C_intersect_U':6,'reservoir_quotient':30},
         'canonical_minimum_distance':48,'forbidden_distance_histogram':dict(sorted(Counter(distances).items())),
         'noncoordinate_local_support_maximum':20,'noncoordinate_pair_union_maximum':34,'noncoordinate_pairs':5253,'cross_family_pairs':4543,
         'small_support_X':list(members(X)),'family_support_sizes':[len(e['actual_source_support']) for e in family_records],
         'common_six_cases':len(six),'coordinate_family_subcode_cases':len(coordinate_subcodes),'quadratic_certificates':len(certs),
         'noncoordinate_quadratic_rank':27,'outside_X_quadratic_rank':28,'coordinate_family_quadratic_rank_census':dict(rank_census),
         'nonfactorable_pencils':2,'controls':{'duplicate_full_minor_is_zero':True,'forced_gamma1_support_has_exact_chi2':True,
          'quotient4_target_boundary':{'first_clique':S1,'second_clique':S2,'canonical_quotient_dimension':4,'exact_chi':194}},
         'claim':'Every native width2 fitting with canonical quotient dimension<=3 inside the full halfclass reservoir has chi>=196; universal proof in PROOF.md; independent review pending',
         'new_kappa':None}
 evidence={'groups':groups,'canonical_basis_hex':list(map(hex,C)),'local_spaces':local_records,'families':family_records,'common_six':six,
           'coordinate_family_subcodes':coordinate_subcodes,'quadratic_minors':certs,'nonfactorable_pencils':pencils}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.output/'EVIDENCE.json.gz').write_bytes(gzip.compress((json.dumps(evidence,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
 print(json.dumps({k:result[k] for k in ['status','common_six_cases','quadratic_certificates','nonfactorable_pencils','new_kappa']}))
if __name__=='__main__':main()
