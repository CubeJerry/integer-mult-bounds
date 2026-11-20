#!/usr/bin/env python3
"""Extend the independently reconstructed frozen response by all external inputs."""
from argparse import ArgumentParser
from pathlib import Path
import json,runpy,sys
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
checker=Path(__file__).resolve().with_name('check.py')
sys.argv=[str(checker),'--repo',str(args.repo),'--out',str(args.out/'interface')]
s=runpy.run_path(str(checker))
b={k:v.copy()for k,v in s['Cbasis'].items()}
for j in s['Y']:s['basis_add'](b,s['Ncols'][j])
r=len(b);F=s['F'];J=[]
for k in range(7):
 row={k:F(1)}
 for j,q in s['P'][k].items():s['add'](row,{a:(-v if a<7 else v)for a,v in s['TH'][j].items()},q)
 J.append(row)
rj=s['rank'](J)
assert r==1288 and rj==6 and r==1289-7+rj
out={'rank_CN':r,'endpoint_rank_deficiency':1289-r,'small_left_kernel_matrix_rank':rj,'small_left_kernel_matrix':[[str(row.get(j,0))for j in range(8)]for row in J]}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'TOTAL-RANK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS_FROZEN_TOTAL_CONTROL_INPUT_RANK',r,rj,flush=True)
