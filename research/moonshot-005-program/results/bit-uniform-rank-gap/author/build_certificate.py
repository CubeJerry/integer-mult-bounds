"""Find a compact witness set; mathematical verification is separate."""
import itertools,json
from pathlib import Path
from collections import Counter
D=Path(__file__).parent
raw=json.loads((D.parent/'block-rigidity/frames.json').read_text());x=raw['vectors'];frames=raw['frames']
K=[sum(((u&v).bit_count()%2)<<j for j,v in enumerate(x)) for u in x]
configs={};allpairs=set()
for F in frames:
 ed={}
 for j in range(111):
  if j in F:continue
  ends=tuple(a for a,i in enumerate(F) if K[i]>>j&1)
  if len(ends)==2:ed[ends]=j
 for omitted in range(8):
  ss=tuple(i for i in range(8) if i!=omitted)
  if any(e not in ed for e in itertools.combinations(ss,2)):continue
  pairs=frozenset(tuple(sorted((F[at],ed[e]))) for e in itertools.combinations(ss,2) for at in e)
  configs.setdefault(pairs,{'frame':F,'omitted_index':omitted})
  allpairs.update(pairs)
remaining=set(allpairs);chosen=[]
while remaining:
 pairs=max(configs,key=lambda z:len(z&remaining))
 gain=len(pairs&remaining)
 assert gain
 chosen.append(configs[pairs]);remaining-=pairs
 del configs[pairs]
coverage=Counter(i for e in allpairs for i in e)
obj={'source_native_sha256':'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','status':'finite exact witness selection, no search-completeness premise','configurations':chosen,'unordered_contacts':len(allpairs),'row_guaranteed_supports':[coverage[i] for i in range(111)],'arrival_lower_bound':sum((coverage[i]>36)+(coverage[i]>52) for i in range(111))}
(D/'CERTIFICATE.json').write_text(json.dumps(obj,indent=2)+'\n')
print(len(chosen),len(allpairs),obj['arrival_lower_bound'],dict(Counter(coverage.values())))
