"""Integer-only independent target-budget check."""
from pathlib import Path
from fractions import Fraction as F
import json,argparse
HERE=Path(__file__).resolve().parent
R=HERE.parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--invoice',type=Path,default=R/'research/shared-wire-split-composition/FULL-RESULT.json')
args=parser.parse_args()
j=json.loads(args.invoice.read_text())
rows=json.loads((HERE/'review/RESULT.json').read_text())
D=10**15
def root(r):
    n=r**199*D**200
    a,b=0,r*D+1
    while b-a>1:
        m=(a+b)//2
        if m**200<=n:a=m
        else:b=m
    if not a**200<=n<(a+1)**200:raise ValueError('root bracket')
    return F(a,D),F(a if a**200==n else a+1,D)
def moment(hist):
    a=b=F(0)
    for r,c in hist.items():
        lo,hi=root(int(r));a+=c*lo;b+=c*hi
    return a,b
t0,t1=moment(j['invoice']['T']);p0,p1=moment(j['invoice']['P'])
r0,r1=moment(rows['histogram'])
original=(t0-p1,t1-p0)
free=(original[0]+18*r0,original[1]+18*r1)
if not original[1]<0<free[0]:raise ValueError('budget sign')
print(json.dumps({'status':'PASS_INDEPENDENT_OWNED_BUDGET',
 'original':[str(x) for x in original],'free_rises':[str(x) for x in free],
 'free_midpoint':float(sum(free)/2)},indent=2))
