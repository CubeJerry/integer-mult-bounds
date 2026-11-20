"""Run both portable native verifiers from any directory."""
import argparse
from fractions import Fraction
from math import ceil,floor
import json
from pathlib import Path
import subprocess
import sys


def main():
    here=Path(__file__).resolve().parent;data=here/'output'
    p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,default=here.parent.parent/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');p.add_argument('--out',type=Path,default=data);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(here/'clebsch.py'),'--layout',str(a.layout),'--dual',str(data/'CLEBSCH-DUAL.json'),'--charts',str(data/'CLEBSCH.json.gz'),'--puncture',str(data/'PUNCTURE.json'),'--puncture-dual',str(data/'PUNCTURE-STRONGER.json'),'--out',str(a.out)],check=True)
    subprocess.run([sys.executable,str(here/'upper.py'),'--layout',str(a.layout),'--witness',str(data/'UPPER.json'),'--out',str(a.out)],check=True)
    subprocess.run([sys.executable,str(here/'upper.py'),'--layout',str(a.layout),'--witness',str(data/'UPPER13.json'),'--out',str(a.out),'--receipt-name','UPPER13-RESULT.json'],check=True)
    local=json.loads((a.out/'CLEBSCH-RESULT.json').read_bytes());upper=json.loads((a.out/'UPPER-RESULT.json').read_bytes());b=3840;h=128;cap=9*b+h;prices={}
    for label,k,cnt in [('full_Clebsch','local_dual',6462),('punctured_Clebsch','punctured_dual',8)]:
        price=Fraction(local[k]['native_arc_deletion_excess_over_b']);q=9*b+ceil(price*b)
        prices[label]={'directions':cnt,'deleted_arc_floor':q,'above_34688':q-cap,'minimum_rank_at_q_34688':b-floor(h/price)}
    data={'b3840_by_actual_direction':prices,'arbitrary_one_directed_deletion_floor':min(v['deleted_arc_floor'] for v in prices.values()),'global_sharpness_ratio_at_least':'13/11','regular_sharpness_ratio_at_least':str(Fraction(upper['erased_corank'],upper['excess_over_9b']))}
    (a.out/'RESULT.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(data)

if __name__=='__main__':main()
