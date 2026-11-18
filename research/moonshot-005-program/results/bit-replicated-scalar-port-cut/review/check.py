#!/usr/bin/env python3
"""Independent port-union census and common-function controls."""
import argparse,gzip,json
from collections import Counter
from hashlib import sha256
from pathlib import Path

def require(ok,msg):
 if not ok:raise ValueError(msg)
class Union:
 def __init__(self,items):self.p={v:v for v in items}
 def find(self,x):
  while self.p[x]!=x:self.p[x]=self.p[self.p[x]];x=self.p[x]
  return x
 def join(self,a,b):self.p[self.find(a)]=self.find(b)
 def groups(self):return len({self.find(v)for v in self.p})
def rank(rows):
 basis={}
 for row in rows:
  while row:
   p=(row&-row).bit_length()-1
   if p in basis:row^=basis[p]
   else:basis[p]=row;break
 return len(basis)
def controls():
 spaces=sorted({tuple(sorted({0,a,b,a^b}))for a in range(1,8)for b in range(1,8)if a!=b})+[(0,a)for a in range(1,8)]
 cases=0
 for a in spaces:
  for b in spaces:
   u=Union(range(8))
   for s in (a,b):
    seen={}
    for x in range(8):
     y=tuple((v&x).bit_count()%2 for v in s)
     if y in seen:u.join(x,seen[y])
     else:seen[y]=x
   require(u.groups()==len(set(a)&set(b)),'common-function quotient');cases+=1
 require(len(set((0,1,2,3))&set((0,2,4,6)))==2,'intermediate array intersection remains possible')
 require(Union([0,1]).groups()==2,'private ports do not collapse')
 return {'subspace_pairs':cases,'intermediate_array_intersection_allowed':True,'private_port_negative_control':True}
def main():
 ap=argparse.ArgumentParser()
 for name in ['repo','author-result','proof','out']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();pg=a.repo/'research/moonshot-005-program'
 lr=gzip.decompress((pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
 fr=(pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json').read_bytes()
 require(sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
 require(sha256(fr).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7','factor pin')
 o=json.loads(lr);roots=o['root_table'];planes=list(map(set,o['A2']));ds=list(map(set,o['D4']));native=set(range(111))
 orth=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots[:111]]
 visible=[{i for i in range(111)if H<=orth[i]}for H in planes];dv=[{i for i in range(111)if D<=orth[i]}for D in ds]
 fac=dict(json.loads(fr)['factors']);cap=[[0]*111 for _ in range(111)]
 for h,H in enumerate(planes):
  J=H&native;m=len(J)
  if not m:continue
  b=45*max(8,12//m+fac.get(h,0))
  for i in visible[h]:
   for j in J:cap[i][j]+=b
 tight=[{j for j in range(111)if cap[i][j]==5760}for i in range(111)]
 require(sum(map(len,tight))==6110,'tight pair census')
 kr=rank([(1<<i)^sum(1<<j for j in orth[i]if j<111)for i in range(111)]);require(kr==9,'canonical rank')
 raw=a.author_result.read_bytes()
 if a.author_result.suffix=='.gz':raw=gzip.decompress(raw)
 author=json.loads(raw);witness={v['plane']:v for v in author['planes']};hist=Counter();count=edges=0;full=[]
 for h,H in enumerate(planes):
  J=H&native
  if len(J)<2:continue
  rec={i for i in visible[h]if J<=tight[i]};ports={d for d,D in enumerate(ds)if H<=D}
  require(len(ports)==45 and rec,'plane geometry');u=Union(rec);covered=set()
  for d in ports:
   group=sorted(rec&dv[d])
   if group:covered.add(d)
   for i in group[1:]:u.join(group[0],i)
  require(u.groups()==1,'port-union connectivity')
  for i in rec:require(sum(i in dv[d]for d in ports)==15,'fifteen visible ports')
  w=witness[h];require(set(w['native_donors'])==J and set(w['joint_tight_receivers'])==rec,'witness vertices');wu=Union(rec)
  for i,j,d in w['spanning_tree_with_D4_witnesses']:
   require(d in ports and {i,j}<=rec&dv[d],'tree port witness');wu.join(i,j);edges+=1
  require(wu.groups()==1,'published tree connectivity');unused=ports-covered
  require(set(w['uncovered_D4_ports'])==unused,'uncovered ports')
  hist[len(unused)]+=1;count+=1;full.append([h,sorted(rec),sorted(unused)])
 require(count==1108 and dict(hist)=={5:260,0:834,9:4,10:10},'global port census')
 uncovered=sum(k*v for k,v in hist.items());capacity=count*360+uncovered*24+11*540;need=(111-kr)*5760
 require(uncovered==1436 and capacity==439284 and need==587520 and capacity<need,'information contradiction')
 result={'status':'PASS_INDEPENDENT_REPLICATED_SCALAR_PORT_CUT','reviewed_proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),'author_result_uncompressed_sha256':sha256(raw).hexdigest(),'ordinary_planes':count,'independently_connected_port_graphs':count,'verified_author_tree_edges':edges,'uncovered_port_histogram':dict(sorted(hist.items())),'uncovered_ports':uncovered,'information_capacity':capacity,'required_input_dimension':need,'strict_deficit':need-capacity,'geometry_sha256':sha256(json.dumps(full,separators=(',',':')).encode()).hexdigest(),'common_function_controls':controls(),'new_complete_kappa':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
