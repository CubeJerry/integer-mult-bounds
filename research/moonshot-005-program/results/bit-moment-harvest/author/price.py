#!/usr/bin/env python3
"""Exact optimistic caller movement screens of the two actual partial words."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from interval import need,measure,add,pack,BITS

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cubic',type=Path,required=True);ap.add_argument('--d4',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 B={127:F(37,6),64:F(37,3),1:-F(37,3)};B=add(B,{7*j+1:F(37,3) for j in range(1,9)});B=add(B,{7*j:-F(37,3) for j in range(1,9)})
 rows=[]
 for name,p,expected in [('cubic',a.cubic,{1:7,2:1,3:13,4:13,5:3,6:2,7:205}),('d4',a.d4,{1:9,2:2,3:13,4:15,5:2,6:2,7:204})]:
  raw=p.read_bytes();r=json.loads(raw);Q={int(k):v for k,v in r['closed_partial']['profile'].items()};need(Q==expected and sum(k*v for k,v in Q.items())==1562,'actual partial-word movement invoice');cases=[]
  for future in (7,8,9):cases.append({'future_bare_rank8_routes':future,'limiting_movement_room':pack(measure(add(add(B,Q,-1),{8:future},-1)))})
  rows.append({'source':name,'result_sha256':hashlib.sha256(raw).hexdigest(),'partial_movement_moment':pack(measure(Q)),'cases':cases})
 out={'status':'PASS_RIGOROUS_MOMENT_HARVEST_PRICE_SCREEN','moment_power':'199/200','binary_interval_bits':BITS,'limiting_caller_allowance':pack(measure(B)),'sources':rows,'qualification':'Partial-word baselines plus bare future routes only; no future source, decoder, compiler, uniformity or new kappa.'};a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'moments':{r['source']:r['partial_movement_moment']['lower'] for r in rows},'eight_future_room':{r['source']:r['cases'][1]['limiting_movement_room']['lower'] for r in rows}}))
if __name__=='__main__':main()
