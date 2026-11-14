#!/usr/bin/env python3
"""Independent exact fitting/cover verifier, with a different residue prime."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
 if not c:raise ValueError(m)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(a,p):
 a=[[int(x)%p for x in row]for row in a];r=0
 for j in range(len(a[0])if a else 0):
  k=next((i for i in range(r,len(a))if a[i][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][j],-1,p);a[r]=[v*x%p for x in a[r]]
  for i in range(r+1,len(a)):
   c=a[i][j];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
  r+=1
 return r
def brank(words):
 d={}
 for w in words:
  while w:
   j=w.bit_length()-1
   if j in d:w^=d[j]
   else:d[j]=w;break
 return len(d)
def run(repo,cert):
 raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));roots=[]
 for i in range(111):
  r=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));c=F(2)if dot(r,r)==1 else F(1)
  if next(x for x in r if x)<0:c=-c
  r=[c*x for x in r];need(dot(r,r)==4 and all(x.denominator==1 for x in r),'root normalization');roots.append(list(map(int,r)))
 K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(roots))for i,r in enumerate(roots)];h=K[92];A=[r&(h if h>>i&1 else ~h)for i,r in enumerate(K)]
 need(brank(K)==9 and brank(A)==15 and brank(A+K)==16,'exact fitting/enlargement ranks')
 data=json.loads(cert.read_text());need(len(data['rows'])==111,'all receivers');chi=[]
 for i,entry in enumerate(data['rows']):
  need(entry['receiver']==i and A[i]>>i&1 and not(A[i]&~K[i]),'fitting row')
  S=[j for j in range(111)if j!=i and A[i]>>j&1];need(S==entry['foreign_support'],'literal support')
  drop=next(j for j,x in enumerate(roots[i])if x);vec=[[x for j,x in enumerate(roots[t])if j!=drop]for t in S]
  need(rank(vec,103)==7,'full rational foreign rank from103minor')
  if entry['chi']==1:
   left,right=entry['cover'];need(set(left)|set(right)==set(S),'cover union')
   if i==92:raise ValueError('incorrect pivot cover')
   if dot(roots[i],roots[92])==0:
    need(right==[92]and all(dot(roots[t],roots[92])==0 for t in left),'common-flat cover');need(rank([roots[i],roots[92]],103)==2,'proper common flat')
   else:
    z,v=entry['normals'];need(rank([roots[i],z],103)==rank([roots[i],v],103)==2,'proper cover normals');need(all(dot(roots[t],z)==0 for t in left)and all(dot(roots[t],v)==0 for t in right),'exact rational cover membership')
  else:
   need(entry['chi']==2,'chi category');quad=[[x[a]*x[b]for a in range(7)for b in range(a,7)]for x in vec];qr=rank(quad,103)
   if i==92:need(qr==28,'no nonzero vanishing quadratic')
   else:
    need(qr==27 and len(S)==27,'one-dimensional vanishing-quadric kernel');r=roots[92];s=roots[i];need(dot(r,s)**2==4,'projected norm3');need(all(dot(roots[t],roots[t])==dot(r,roots[t])**2 for t in S),'explicit rank7 vanishing form')
  chi.append(entry['chi'])
 need(sum(chi)==120 and [i for i,x in enumerate(chi)if x==2]==[21,33,45,51,68,76,84,92,99],'exact total')
 return{'status':'PASS_INDEPENDENT_PIVOT92_PROPER_COVER_CERTIFICATE','native_sha256':PIN,'certificate_sha256':hashlib.sha256(cert.read_bytes()).hexdigest(),'independent_minor_prime':103,'fitting_rank':15,'canonical_enlargement_rank':16,'chi':120,'positive_rational_covers':102,'negative_quadratic_certificates':9,'physical_source':False,'no_new_kappa':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repo,a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
