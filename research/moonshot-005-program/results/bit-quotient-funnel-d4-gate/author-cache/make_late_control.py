#!/usr/bin/env python3
from pathlib import Path
import argparse,json,copy
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();w=json.loads(a.source.read_text());late=copy.deepcopy(w);cut=w['milestones']['source_cut'];assert [o[0]for o in w['operations'][:6]]==['INIT','ADD','MOVE']*2
ops=copy.deepcopy(w['operations'][:6]);targets={int(j):int(i)for i,j in w['singleton_pivots'].items()}
for u,j in enumerate(w['early_point_helper_originals']):ops[3*u][2]=f'F{targets[j]}'
late['operations']=w['operations'][6:cut]+ops+w['operations'][cut:];late['variant']='six-late-paid-control';late['helper_chronology']='Actual helpers acquired at held facets after source acquisition instead of native points beforehand.'
a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(late,indent=2)+'\n')
