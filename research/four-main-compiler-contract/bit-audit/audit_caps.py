"""Second exact BIT ambient-cap comparison, using the reviewer's log core.
@CubeJerry, substantial OpenAI assistance, Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, importlib.util, json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reviewer_ambient',HERE.parent/'ambient_bounds.py')
L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)

def need(ok,message):
    if not ok:raise ValueError(message)

def run():
    result={}
    for p in [596,602,603]:
        x=L.bounds(Q('.00376670'),ambient=134,power=768,
                   theta_numerator=42,theta_denominator=43,log_power=p)
        need(x['log_base_margin'][0]>0,'base case comparison')
        if p==603:need(x['log_complement_margin'][0]>0,'603 sufficient')
        else:need(x['log_complement_margin'][1]<0,'lower powers fail comparison')
        result[str(p)]={k:L.show(v) for k,v in x.items()}
    need(15**43<16**42,'strict exit ratio')
    need(2*15**(768*43)<=134**(768*42),'shifted exit')
    j=28970;step=10**10
    need((step*j+1)**603<2**j,'winning integer grid')
    need((step*(j-1)+1)**603>=2**(j-1),'preceding integer grid fails')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args()
    result=run()
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads((HERE/'CAP-REVIEW.json').read_text()),'exact cap receipt')
    print('PASS_INDEPENDENT_BIT_AMBIENT_CAP')
