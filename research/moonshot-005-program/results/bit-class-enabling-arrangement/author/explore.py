#!/usr/bin/env python3
import gzip,json,itertools
from fractions import Fraction as F
from pathlib import Path
BASE=Path('/workspace/scratch/c962181f51c6')
s=json.loads(gzip.decompress((BASE/'worker-c/block-rigidity/BIT-NATIVE-WORD.json.gz').read_bytes()))
rr=[list(map(F,s['frames'][str(s['start'][i])]['B'][0])) for i in range(111)]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
K=[sum(int(i==j or dot(a,b)==0)<<j for j,b in enumerate(rr)) for i,a in enumerate(rr)]
groups={}
for i,r in enumerate(rr):
 S=tuple(j for j,x in enumerate(r) if x);sign=1 if r[S[0]]>0 else -1
 key=('coordinate',0) if len(S)==1 else (min(S,tuple(j for j in range(8) if j not in S)),sum(x*sign<0 for x in r)%2)
 groups.setdefault(key,[]).append(i)
classes=list(groups.values());U=[sum(1<<i for i in g) for g in classes]
def ba(rows):
 b={};chosen=[]
 for ix,x in enumerate(rows):
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;chosen.append(ix);break
 return b,chosen
def rem(x,b):
 for p,v in sorted(b.items(),reverse=True):
  if x>>p&1:x^=v
 return x
ub=ba(U)[0];quot=[rem(K[g[0]],ub) for g in classes];qb,ch=ba(quot);basis=[quot[j] for j in ch]
mapping={0:0}
for i,b in enumerate(basis):mapping.update({x^b:n|(1<<i) for x,n in list(mapping.items())})
labels=[mapping[q] for q in quot]
def components(which):
 parent=list(range(111))
 def root(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 def union(a,b):parent[root(a)]=root(b)
 for c in which:
  for receiver in classes[c]:
   for group in classes:
    nonlocal_ports=[j for j in group if receiver==j or dot(rr[receiver],rr[j])!=0]
    for j in nonlocal_ports[1:]:union(nonlocal_ports[0],j)
 out=[]
 for g in classes:
  parts={}
  for j in g:parts.setdefault(root(j),[]).append(j)
  out.append(list(parts.values()))
 return out
single=[components([c]) for c in range(15)]
pairs=[];lines=set()
for c,d in itertools.combinations(range(15),2):
 parts=components([c,d]);active=[a for a,p in enumerate(parts) if len(p)>1];dimension=sum(map(len,parts))-15
 assert dimension==3 and len(active)==3 and all(len(parts[a])==2 for a in active)
 assert c in active and d in active and labels[active[0]]^labels[active[1]]^labels[active[2]]==0
 line=tuple(active);lines.add(line);pairs.append({'classes':[c,d],'intersection_quotient_dimension':dimension,'active_classes':active,'components':parts})
triplehist={}
for c,d,e in itertools.combinations(range(15),3):
 dim=sum(map(len,components([c,d,e])))-15;triplehist[dim]=triplehist.get(dim,0)+1
 assert dim==(3 if labels[c]^labels[d]^labels[e]==0 else 0)
out={'classes':classes,'labels':labels,'single_components':single,'single_quotient_dimensions':[sum(map(len,p))-15 for p in single],'pair_intersections':pairs,'projective_lines':[list(x) for x in sorted(lines)],'triple_histogram':triplehist}
(BASE/'worker-c/class-enabling-arrangement/EXPLORATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'single_dimensions':out['single_quotient_dimensions'],'pairs':len(pairs),'lines':len(lines),'triples':triplehist}))
