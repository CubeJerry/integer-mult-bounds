#!/usr/bin/env python3
"""Exact native equality14 premises; the all-field argument is in PROOF.md."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
OLD='7567810dd8eab8add727a5d2e4371cb6af588d4e61630e62c43a07f7f5b45932'
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
def complete_roots(R):
 patterns=sorted({tuple(i for i,x in enumerate(r) if x) for r in R if sum(x!=0 for x in r)==4})
 full=[tuple(2*int(i==j) for i in range(8)) for j in range(8)]
 for S in patterns:
  for signs in itertools.product((-1,1),repeat=3):
   z=[0]*8;z[S[0]]=1
   for j,s in zip(S[1:],signs):z[j]=s
   full.append(tuple(z))
 need(len(full)==len(set(full))==120 and set(R)<=set(full),'full120 domain')
 signed=set(full)|{tuple(-x for x in r) for r in full}
 for r,s in itertools.product(full,repeat=2):
  d=dot(r,s);need(d%2==0,'crystallographic angles')
  need(tuple(x-d*y//2 for x,y in zip(r,s)) in signed,'reflection closure')
 return full
def rank3_cases(R,full,adj,degree,old):
 perp=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(full)) for r in R]
 nativeperp=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(R)) for r in full]
 D=[[dot(r,s) for s in R] for r in R];spaces={};count=0
 for a,b,c in itertools.combinations(range(111),3):
  x,y,z=D[a][b],D[a][c],D[b][c];det=64-4*(x*x+y*y+z*z)+2*x*y*z
  need(det>=0,'nonnegative Gram determinant')
  if det:count+=1;spaces.setdefault(perp[a]&perp[b]&perp[c],(a,b,c))
 need(count==220934 and len(spaces)==74396,'complete rank3 domain')
 equal=[];larger=[];width_cases=0;flat_masks=set()
 for mask,B in spaces.items():
  O=list(members(mask));basis=mod_basis([full[j] for j in O],257,5);need(len(basis)==5,'full complementary rank5')
  flat=(1<<111)-1
  for j in basis:flat&=nativeperp[O[j]]
  flat_masks.add(flat);P=list(members(flat));outside=list(members(adj[B[0]]&adj[B[1]]&adj[B[2]]))
  need(3<=len(P)<=6 and all(flat>>j&1 for j in B),'exact double-perpendicular flat')
  if len(P)<5:continue
  for s in (5,6):
   if s>len(P):continue
   width_cases+=1;eligible=[i for i in outside if degree[i]<=52+s]
   row={'support':P,'width':s,'outside':outside,'eligible':eligible}
   if len(eligible)==14:equal.append(row)
   if len(eligible)>14:larger.append(row)
 need(len(flat_masks)==74396 and width_cases==11761 and len(equal)==94,'complete equality14 width cases')
 key=lambda S,w,O,n:(tuple(S),w,tuple(O),n)
 need({key(e['support'],e['width'],e['outside'],len(e['eligible'])) for e in larger}==
      {key(e['flat'],e['width'],e['orthogonal_roots'],e['eligible_count']) for e in old['rank3']['critical']},'all larger cases covered by inherited certificates')
 return equal,{'independent_triples':count,'rank3_flats':len(flat_masks),'flat_width_cases':width_cases,
               'equal14_cases':len(equal),'equal14_width_histogram':dict(Counter(e['width'] for e in equal)),'inherited_larger_cases':len(larger)}
def clique_cases(R,full,adj,degree,old):
 cur=[((i,),adj[i]) for i in range(111)];counts={};equal4=[];d4={};two_outside=0;extension_links=[]
 native=set(R);cross=[[dot(r,s) for s in R] for r in full]
 old4={tuple(e['support']) for e in old['cliques']['critical_orthogonal4']}
 old7={(tuple(e['support']),i) for e in old['cliques']['critical_orthogonal7'] for i in e['eligible_receivers']}
 found4=set();found7=set()
 for size in range(1,9):
  counts[size]=len(cur)
  for S,common in cur:
   if size==4:
    eligible=[i for i in members(common) if degree[i]<=56];need(len(eligible)<=7,'orthogonal4 cap7')
    if len(eligible)==7:found4.add(S)
    if len(eligible)==6:equal4.append({'support':list(S),'outside':list(members(common)),'eligible':eligible,'width':4})
    P=tuple(j for j in range(120) if sum(cross[j][b]**2 for b in S)==16)
    if len(P)==12 and all(full[j] in native for j in P) and P not in d4:
     O=[j for j in range(120) if all(dot(full[j],R[b])==0 for b in S)]
     nc=[sum(i!=j and dot(full[i],full[j])==0 for j in O) for i in O]
     need(len(O)==12 and nc==[3]*12,'full native D4 dual has three perpendicular neighbors')
     d4[P]={'frame':list(S),'native_D4':sorted(R.index(full[j]) for j in P),'full_dual':O,'dual_orthogonal_counts':nc}
   if size==6:
    need(common.bit_count()<=2,'orthogonal6 outside cap2')
    if common.bit_count()==2:
     i,j=list(members(common));two_outside+=1;need(adj[i]>>j&1,'two outside roots mutually orthogonal')
     for a,b in [(i,j),(j,i)]:
      if degree[a]<=58:
       T=tuple(sorted(S+(b,)));need((T,a) in old7,'eligible six-case reduces to reviewed seven-case')
       extension_links.append({'six':list(S),'blocked_receiver':a,'added_root':b,'seven':list(T)})
   if size==7:
    need(common.bit_count()<=1,'orthogonal7 outside cap1')
    for i in members(common):
     if degree[i]<=59:found7.add((S,i))
  if size<8:cur=[(S+(j,),C&adj[j]) for S,C in cur for j in members(C&~((1<<(S[-1]+1))-1))]
 need(counts=={1:111,2:3235,3:29939,4:90079,5:77003,6:35667,7:9443,8:1094},'complete clique counts')
 need(found4==old4 and found7==old7,'inherited orthogonal certificates exactly cover larger cases')
 need(len(equal4)==9 and len(d4)==1121 and two_outside==30632,'new clique premises')
 return equal4,list(d4.values()),extension_links,{'clique_counts':counts,'equal14_orthogonal4':len(equal4),'full_native_D4':len(d4),'six_with_two_outside':two_outside,'nonorthogonal_outside_pairs':0,'old_seven_links':len(extension_links)}
def main():
 ap=argparse.ArgumentParser()
 for name in ['native','sharp14-cases','output']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin')
 oldraw=a.sharp14_cases.read_bytes();need(hashlib.sha256(oldraw).hexdigest()==OLD,'reviewed sharp14 catalogue pin')
 old=json.loads(gzip.decompress(oldraw));n=json.loads(gzip.decompress(raw))
 R=[normalize(n['frames'][str(n['start'][i])]['B'][0]) for i in range(111)]
 adj=[sum(int(dot(r,s)==0)<<j for j,s in enumerate(R)) for r in R];degree=[x.bit_count() for x in adj]
 need(Counter(degree)=={55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1},'native degree histogram')
 caps=[0,1,3,6,12,20,36,111,111];envelope=[]
 for r in range(1,9):
  for s in range(r,caps[r]+1):
   for j in range(min(r,s)+1):
    if s>j+caps[r-j]:continue
    bound=min(caps[8-r],sum(x<=52+s for x in degree))+min(caps[8-r],sum(x<=36+s for x in degree))+2*j
    envelope.append([r,s,j,bound])
 equal=[x for x in envelope if x[-1]==14]
 need(len(envelope)==569 and equal==[[3,4,1,14],[4,4,1,14],[4,5,1,14],[4,6,1,14],[4,7,1,14],[5,5,4,14],[8,8,7,14]],'complete new parameter cases')
 low=[i for i,d in enumerate(degree) if d<=56];lb=mod_basis([R[i] for i in low],509)
 need(len(low)==12 and len(lb)==7,'low-degree span rank at least7')
 selected=[R[low[j]] for j in lb];cols=mod_basis(list(map(list,zip(*selected))),509)
 ld=mod_det([[r[j] for j in cols] for r in selected],509);need(ld!=0,'explicit low-degree7 minor')
 null=[0,-1,1,0,1,0,0,1];need(all(dot(R[i],null)==0 for i in low),'low-degree exact upper rank7')
 full=complete_roots(R);r3,r3summary=rank3_cases(R,full,adj,degree,old)
 print(json.dumps({'stage':'rank3','equal14_cases':len(r3)}),flush=True)
 c4,d4,links,csummary=clique_cases(R,full,adj,degree,old)
 print(json.dumps({'stage':'cliques',**csummary}),flush=True)
 mon=list(itertools.combinations_with_replacement(range(7),2));Q=[];freecoords=[]
 for i in range(111):
  p=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=p];freecoords.append(free)
  Q.append([[r[free[b]]*r[free[c]] for b,c in mon] for r in R])
 certs=[];first=None
 for kind,records in [('rank3',r3),('orthogonal4',c4)]:
  for row in records:
   S=row['support'];found=None
   for i in row['eligible']:
    points=[j for j in members(adj[i]) if j not in S];basis=mod_basis([Q[i][j] for j in points],509,28)
    if len(basis)==28:
     roots=[points[j] for j in basis];matrix=[Q[i][j] for j in roots];d=mod_det(matrix,509);need(d!=0,'nonzero exact obstruction minor')
     found={'kind':kind,'support':S,'width':row['width'],'blocked_receiver':i,'facet_coordinates':freecoords[i],'minor_roots':roots,'determinant_mod509':d}
     if first is None:first=matrix
     break
   need(found is not None,'every equality14 case has one blocked eligible receiver');certs.append(found)
 need(len(certs)==103 and mod_det([first[0]]+first[:-1],509)==0,'duplicate-row negative control')
 canonical=[]
 for i in range(111):
  points=list(members(adj[i]));b=mod_basis([Q[i][j] for j in points],509,28);need(len(b)==28,'canonical chi2')
  canonical.append({'receiver':i,'minor_roots':[points[j] for j in b]})
 S=[54,56,57,59,61,63,64];need(all(adj[i]>>j&1 for i,j in itertools.combinations(S,2)),'sharp orthogonal7 control')
 need(all(len(mod_basis([R[j] for j in S if j!=i],509))==6 for i in S),'six independent foreign roots')
 T=list(range(8));need(all(adj[i]>>j&1 for i,j in itertools.combinations(T,2)),'eight-root boundary control')
 need(all(len(mod_basis([R[j] for j in T if j!=i],509))==7 for i in T),'eight-root foreign rank7 prevents double saving')
 result={'status':'PASS_SCALAR_EQUALITY14_SOURCE_PREMISES','native_sha256':PIN,'sharp14_cases_sha256':OLD,
         'new_envelope_equal14_cases':equal,'rank3':r3summary,'cliques':csummary,'new_quad28_minors':len(certs),
         'low_degree_rank':7,'controls':{'duplicate_minor_rank_defect':True,'seven_support':S,'seven_exact_chi':208,'six_used_rows_exact_chi':210,'eight_support':T,'eight_exact_chi':214},
         'claim':'Every scalar proper-cover saving14 fitting has exactly seven double-saving rows on an orthogonal7 support; universal proof in PROOF.md; independent review pending','new_kappa':None}
 evidence={'rank3_equal14':r3,'orthogonal4_equal14':c4,'full_native_D4':d4,'six_to_seven_links':links,'obstruction_minors':certs,'canonical_minors':canonical,
           'low_degree_minor':{'roots':[low[j] for j in lb],'columns':cols,'determinant_mod509':ld,'annihilator':null,'all_low_degree_roots':low}}
 a.output.mkdir(parents=True,exist_ok=True)
 (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.output/'EVIDENCE.json.gz').write_bytes(gzip.compress((json.dumps(evidence,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
 print(json.dumps({'status':result['status'],'minors':len(certs),'rank3_equal14':len(r3),'orthogonal4_equal14':len(c4),'full_native_D4':len(d4),'new_kappa':None}))
if __name__=='__main__':main()
