"""Compress explicit valid cuts to a small cover; cover optimality is not used."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
prefix=(HERE/'screen.py').read_text().split("print('D'")[0]
for e in [43,89777,96404,96513]:
 sys.argv=[str(HERE/'screen.py'),str(e)]
 c={'__file__':str(HERE/'screen.py'),'__name__':'compaction'}
 exec(compile(prefix,str(HERE/'screen.py'),'exec'),c)
 initial=[]
 for cut,A in zip(c['base'],c['initial']):
  outgoing=sorted(k for k,(u,v)in c['routes'].items()if k not in c['D']and A>>u&1 and not(A>>v&1))
  initial.append({'canonical_bank_mask':hex(A),'source_axes':cut['source_axes'],'terminal_slots':cut['terminal_slots'],'rank':cut['rank'],'old_exports':outgoing,'parent_minor':cut['id']})
 cutpool=json.loads((HERE/('swap-'+str(e))/'CUT-CERTIFICATES.json').read_text())
 eligible=[z[:2]for z in c['eligible']];index={z:i for i,z in enumerate(eligible)}
 pairs=[(index[a],index[b])for a,b in c['fixed']]
 covers={}
 for cut in cutpool:
  A=int(cut['canonical_bank_mask'],16);shortfall=cut['rank']-len(cut['old_exports']);mask=sum(bool(A>>u&1 and not(A>>v&1))<<i for i,(u,v)in enumerate(eligible))
  cover=0
  for i,(u,v)in enumerate(pairs):
   if (mask>>u&1)+(mask>>v&1)<shortfall:cover|=1<<i
  if not cover:continue
  if cover not in covers or A.bit_count()<int(covers[cover]['canonical_bank_mask'],16).bit_count():covers[cover]=cut
 remaining=(1<<len(pairs))-1;selected=[];new_counts=[]
 while remaining:
  cover=max(covers,key=lambda k:(k&remaining).bit_count());new=(cover&remaining).bit_count();assert new
  selected.append(covers.pop(cover));new_counts.append(new);remaining&=~cover
  if not covers:assert not remaining
 out={'deleted':sorted(c['D']),'replaced_grade4_occurrence':e,'initial_cuts':initial,'separating_cuts':selected,'initial_source_route_count':len(eligible),'fixed_pairs':len(pairs),'selected_cut_new_rejections':new_counts,'scope':'Explicit valid cut cover only; greedy selection is not claimed minimal.'}
 (HERE/('swap-'+str(e))/'COMPACT-CUTS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(e,'pool',len(cutpool),'distinctcovers',len(covers)+len(selected),'compact',len(selected),'counts',new_counts,flush=True)
