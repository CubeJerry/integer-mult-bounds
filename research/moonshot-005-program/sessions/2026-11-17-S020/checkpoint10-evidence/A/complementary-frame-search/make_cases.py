"""All three cross-frame matching schedules, modulo first-round relabelling."""
import itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent
perms=list(itertools.permutations(range(4)))
cases=[];schedule_count=0
for p2 in perms:
 for p3 in perms:
  masks=[1<<i for i in range(8)]
  for p in [tuple(range(4)),p2,p3]:
   for i,j in enumerate(p):masks[i]=masks[4+j]=masks[i]|masks[4+j]
  if any(m.bit_count()!=6 for m in masks):continue
  schedule_count+=1;allowed=[255]*8
  for i,j in enumerate(p3):
   missing=(1<<i)|(1<<(4+j))
   for k in range(8):allowed[k]&=255^missing if masks[i]>>k&1 else missing
  def visit(seed,used):
   k=len(seed)
   if k==8:
    cases.append({'round2':p2,'round3':p3,'seeds':seed,'reach_masks':masks});return
   for j in range(8):
    if (allowed[k]&~used)>>j&1:visit(seed+[j],used|(1<<j))
  visit([],0)
out={'normalized_schedule_candidates':24**2,'six_dimensional_final_schedules':schedule_count,'cases':cases}
(P/'CASES.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'CASES.txt').open('w')as f:
 f.write(str(len(cases))+'\n')
 for c in cases:f.write(' '.join(map(str,list(c['round2'])+list(c['round3'])+c['seeds']))+'\n')
print('legal schedule/seed cases',len(cases),'from',schedule_count,'rank6 schedules')
