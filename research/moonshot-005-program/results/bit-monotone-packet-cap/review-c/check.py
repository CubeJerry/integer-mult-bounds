#!/usr/bin/env python3
"""Independent dyadic power brackets and signed-profile audit."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

PIN='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def combine(*terms):
    out={}
    for multiplier, profile in terms:
        for rank, coefficient in profile.items():
            out[rank]=out.get(rank,F(0))+multiplier*coefficient
    return {r:c for r,c in out.items() if c}


def bracket(rank, bits=128):
    scale=1<<bits
    target=pow(rank,199)*pow(scale,200)
    left,right=0,rank*scale+1
    while right-left>1:
        midpoint=(left+right)//2
        if pow(midpoint,200)<=target:
            left=midpoint
        else:
            right=midpoint
    require(pow(left,200)<=target<pow(right,200), 'outward dyadic endpoint')
    return F(left,scale),F(right,scale)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--author-result',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    raw=args.source.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'exact receipt bytes')
    z=json.loads(raw)
    n,h,p,t=({int(r):F(c) for r,c in z[k].items()}
             for k in ('native_paid','helper_target','paired_paid','paired_target'))
    # Build the paired terms from direct loops, independently of the author.
    pe={r:36*c for r,c in n.items()};pe[1]=pe.get(1,0)+444
    for j in range(1,9):pe[7*j]=pe.get(7*j,0)+444
    te={r:36*c for r,c in h.items()};te[127]=te.get(127,0)+222
    for j in range(1,10):te[7*j+1]=te.get(7*j+1,0)+444
    require(pe==p and te==t,'paired profile identities')
    signed=combine((F(1,36),t),(F(-1,36),p))
    limit=combine((1,n),(-1,h),(1,signed))
    explicit={127:F(37,6),64:F(37,3),1:F(-37,3)}
    for j in range(1,9):
        explicit[7*j+1]=explicit.get(7*j+1,0)+F(37,3)
        explicit[7*j]=explicit.get(7*j,0)-F(37,3)
    require(limit==explicit,'native cancellation')
    # Check the complete fixed-m allowance as a signed profile for several
    # adversarial m, and a symbolic identity in the written review.
    for m in (2,4,6,100,1000000):
        direct=combine((F(m,36*(m-1)),t),(F(-m,36*(m-1)),p),(1,n),(-1,h))
        require(direct==combine((1,limit),(F(1,m-1),signed)),'fixed-m allowance profile')
    diff=combine((1,h),(-1,n))
    require(all(c<0 and r<=7 or c>0 and r==8 for r,c in diff.items()),'finite-m monotonicity signs')
    powers={r:bracket(r) for r in set(limit)|set(signed)|{7,8}}
    def evaluate(profile):
        low=high=F(0)
        for r,c in profile.items():
            a,b=powers[r]
            low+=c*(a if c>=0 else b);high+=c*(b if c>=0 else a)
        return low,high
    si=evaluate(signed);m10=evaluate(combine((1,limit),(-1,{7:222,8:10})))
    m11=evaluate(combine((1,limit),(-1,{7:222,8:11})))
    require(si[1]<0 and m11[1]<0 and m10[0]>0,'target signs')
    a=json.loads(args.author_result.read_text())
    checks=[('S',si,list(map(F,a['finite_m_correction_S']))),
            ('q10',m10,list(map(F,a['limiting_margins_by_q']['10']))),
            ('q11',m11,list(map(F,a['limiting_margins_by_q']['11'])))]
    for label,(lo,hi),(alo,ahi) in checks:
        require(alo<=lo<hi<=ahi,'independent interval inside author interval: '+label)
    require(F(37,3)-F(88,49)==F(1549,147)>0,'derivative margin')
    t1=sum(F(r)*c for r,c in limit.items())-222*7-11*8
    require(t1==F(101,6)>0,'out-of-interval control')
    result={'status':'PASS_INDEPENDENT_MONOTONE_PACKET_CAP','source_sha256':PIN,
            'independent_dyadic_bits':128,'author_code_imported':False,
            'S_interval':list(map(str,si)),'q10_margin_interval':list(map(str,m10)),
            'q11_margin_interval':list(map(str,m11)),
            'author_interval_containment':'all3passed','fixed_m_profile_cases':[2,4,6,100,1000000],
            't1_q11_control':str(t1),'new_kappa':None}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'S_approx':float(si[0]),
                      'q11_margin_approx':float(m11[0]),'q10_margin_approx':float(m10[0])}))


if __name__=='__main__':main()
