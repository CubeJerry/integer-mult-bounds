from fractions import Fraction
from itertools import combinations
from collections import defaultdict
from pathlib import Path
import json,sys
sys.path.insert(0,'..')
from audit_cp6 import chart,subset
repo=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds');w=json.loads((repo/'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint6-evidence/A/local-canonical9-source/WORD.json').read_text());R=json.loads((repo/w['source_path']).read_text())['native_roots'];M=chart(w['charts']['M1']);U=sorted(set(range(111))-set(w['targets']))
def rr(rows):
 a=[list(map(Fraction,row))for row in rows];k=0
 for c in range(5):
  p=next((i for i in range(k,len(a))if a[i][c]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];q=a[k][c];a[k]=[x/q for x in a[k]]
  for i in range(len(a)):
   if i!=k and a[i][c]:q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[k])]
  k+=1
 return tuple(tuple(r)for r in a[:k])
classes=defaultdict(list)
for i in U:
 v=tuple(sum(x*y for x,y in zip(R[i],b))for b in M);key=rr([v])[0];classes[key].append(i)
points=sorted(classes);out={'class_groups':[classes[p]for p in points],'projective_normals':[[str(x)for x in p]for p in points],'flats':{}}
for rank in range(1,6):
 flats={}
 for ids in combinations(range(len(points)),rank):
  B=rr([points[i]for i in ids])
  if len(B)!=rank:continue
  if B in flats:continue
  hit=[i for i,p in enumerate(points)if len(rr(list(B)+[p]))==rank];flats[B]=hit
 out['flats'][rank]=[{'basis':[[str(x)for x in row]for row in B],'point_classes':hit}for B,hit in flats.items()]
 print('rank',rank,'flats',len(flats),'max',max(map(len,flats.values())),'countdist',dict((k,sum(len(v)==k for v in flats.values()))for k in sorted(set(map(len,flats.values())))),flush=True)
Path('PORT-FLATS.json').write_text(json.dumps(out,indent=2)+'\n')
