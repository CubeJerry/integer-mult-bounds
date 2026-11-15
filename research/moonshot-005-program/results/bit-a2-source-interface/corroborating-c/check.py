from pathlib import Path
import json,itertools
root=Path(__file__).parent
def span(rows):
 S={0}
 for r in rows:S|={s^r for s in tuple(S)}
 return frozenset(S)
def partitions(n):
 if n==0:yield [];return
 for p in partitions(n-1):
  yield p+[[n-1]]
  for i in range(len(p)):yield p[:i]+[p[i]+[n-1]]+p[i+1:]
def spaces(n):
 seen={frozenset({0})};queue=list(seen)
 for S in queue:
  for v in range(1,1<<n):
   if v in S:continue
   U=span(list(S)+[v])
   if U not in seen:seen.add(U);queue.append(U)
 return queue
count=0
for n in range(1,5):
 for R in spaces(n):
  for groups in partitions(n):
   masks=[sum(1<<j for j in g)for g in groups];local=[r for r in R if r==0 or any(r&~m==0 for m in masks)];synth=span(local);dimsum=sum((len([r for r in R if r&~m==0])).bit_length()-1 for m in masks)
   assert(synth==R)==(dimsum==len(R).bit_length()-1);count+=1
# Proper image at one joint chart succeeds; the same diagonal across separate charts fails.
diag=span([3]);assert span([r for r in diag if r&~3==0])==diag;assert span([r for r in diag if r&~1==0 or r&~2==0])!=diag
columns_checked=0
for r in range(1,4):
 for n in range(1,5):
  for cols in itertools.product(range(1,1<<r),repeat=n):
   E=span([sum(((v>>k)&1)<<j for j,v in enumerate(cols))for k in range(r)]);local=span([v for v in E if v.bit_count()<=1]);independent=len(span(cols))==1<<n;assert(local==E)==independent;columns_checked+=1
out={'status':'PASS_FINITE_CONTROLS_FOR_WRITTEN_ALL_FIELD_PROOF','all_binary_subspaces_up_to_dimension':4,'chart_partition_cases':count,'nonzero_column_cases':columns_checked,'positive_controls':['full held projection','proper diagonal image at one shared chart'],'negative_controls':['same diagonal split over two charts','dependent nonzero evaluation columns'],'scope':'Finite controls only; the written linear argument supplies universal quantifiers.','new_complete_kappa':False};(root/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
