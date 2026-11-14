#!/usr/bin/env python3
"""Independent equality-component reconstruction of arbitrary class extensions."""
import argparse,json,gzip,hashlib,itertools
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
def need(x,s):
 if not x:raise ValueError(s)
def main(a):
 b=a.native.read_bytes();need(hashlib.sha256(b).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');n=json.loads(gzip.decompress(b));b=a.partition.read_bytes();need(hashlib.sha256(b).hexdigest()=='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117','partition pin');G=json.loads(b)['groups'];need(sorted(sum(G,[]))==list(range(111)),'partition')
 r=[[F(x) for x in n['frames'][str(n['start'][i])]['B'][0]] for i in range(111)];N=[{j for j in range(111) if sum(x*y for x,y in zip(r[i],r[j]))!=0} for i in range(111)]
 need(all(N[i]&set(g) for i in range(111) for g in G),'every forbidden row meets every class');need(all(N[i]&set(g)=={i} for g in G for i in g),'orthogonal own classes')
 def components(classes):
  out=[]
  for g in G:
   p={i:i for i in g}
   def find(i):
    while p[i]!=i:p[i]=p[p[i]];i=p[i]
    return i
   for c in classes:
    for i in G[c]:
     z=sorted(N[i]&set(g))
     for j in z[1:]:p[find(j)]=find(z[0])
   blocks={}
   for i in g:blocks.setdefault(find(i),[]).append(i)
   out.append(sorted(blocks.values()))
  return out
 single=[components([i]) for i in range(15)];dims=[]
 for i,cs in enumerate(single):
  need([len(c) for c in cs]==[len(g) if j==i else 2 for j,g in enumerate(G)],'exact own/two-part component structure');dims.append(sum(len(c)-1 for c in cs));need(dims[-1]==len(G[i])+13,'quotient dimension')
 lines=set();pair={}
 for c,d in itertools.combinations(range(15),2):
  cs=components([c,d]);support=tuple(i for i,t in enumerate(cs) if len(t)>1);need(len(support)==3 and c in support and d in support and all(len(t)<=2 for t in cs),'three pair quotient lines');lines.add(support);pair[c,d]=next(i for i in support if i not in (c,d))
 triples=Counter()
 for triple in itertools.combinations(range(15),3):
  cs=components(triple);dim=sum(len(t)-1 for t in cs);need(dim==(3 if triple in lines else 0),'every triple intersection');triples[dim]+=1
 need(len(lines)==35 and triples=={3:35,0:420},'complete pair/triple census')
 # Independently recognize PG(3,2) using its complete elementary abelian group.
 def add(x,y):
  if x==15:return y
  if y==15:return x
  if x==y:return 15
  return pair[tuple(sorted((x,y)))]
 need(all(add(add(x,y),z)==add(x,add(y,z)) for x in range(16) for y in range(16) for z in range(16)),'associative binary projective labels')
 labels={15:0};bit=1
 while len(labels)<16:
  x=next(i for i in range(15) if i not in labels);old=dict(labels)
  for y,v in old.items():labels[add(x,y)]=v|bit
  bit*=2
 need(bit==16 and set(labels.values())==set(range(16)),'four independent labels');need(all(labels[c]^labels[d]^labels[e]==0 for c,d,e in lines),'line labels')
 def local(v,i):return all(len({int(j in v) for j in N[i]&set(g)})==1 for g in G)
 def enabled(v):return [c for c,g in enumerate(G) if all(local(v,i) for i in g)]
 v={8,10,12,13};en=enabled(v);need(sorted(min(G[c]) for c in en)==[0,8,9],'three-class half witness');need(sum(len(G[c]) for c in en)==22,'22 enabled receivers in those classes')
 dirs=[{0},{1},{0,1}];single_enabled=[enabled(v) for v in dirs];c0=next(c for c,g in enumerate(G) if 0 in g);need(single_enabled==[[c0]]*3,'each coordinate direction enables only coordinate class')
 covered={i for i in range(111) if any(local(v,i) for v in dirs)};whole=[c for c,g in enumerate(G) if set(g)<=covered];need(len(covered)==88 and sorted(min(G[c]) for c in whole)==[0,8,9,14,15,38,39,46,47],'receiverwise higher-dimensional counterexample')
 # Verify the stronger E01 quotient application directly on all noncoordinate facets.
 for i in range(8,111):
  for v in dirs:
   if local(v,i):need(v.isdisjoint(N[i]),'every E01 local representative is already local, no nonzero class correction')
 controls=dict(pairwise_disjoint_guess_refuted=all(sum(len(t)-1 for t in components(pair))==3 for pair in itertools.combinations(range(15),2)),binary_direction_count_for_h2_refuted=len(whole)>len(dirs),wrong_maximum_two_enabled_refuted=len(en)==3,removed_own_forbidden_entry_breaks_every_class_hit=not((N[0]-{0})&set(G[c0])))
 need(all(controls.values()),'negative controls')
 out=dict(status='PASS_INDEPENDENT_CLASS_ENABLING_ARRANGEMENT',native_sha256=hashlib.sha256(a.native.read_bytes()).hexdigest(),groups=G,quotient_dimensions=dims,pairs_checked=105,triple_dimension_histogram={str(k):v for k,v in triples.items()},lines=[list(t) for t in sorted(lines)],projective_labels_by_class=labels,half_witness_enabled_class_minima=sorted(min(G[c]) for c in en),higher_extension_enabled_classes=sorted(min(G[c]) for c in whole),higher_extension_receivers=len(covered),negative_controls=controls,scope='Equality-component proof gives arbitrary-field arrangement; cut consequences require declared historical normalization and physical routes. Fixed scalar tensors are distinguished from arbitrary operator extensions.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'pairs':105,'triples':455,'half_enabled':3,'E01_enabled':len(whole)}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','partition','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
