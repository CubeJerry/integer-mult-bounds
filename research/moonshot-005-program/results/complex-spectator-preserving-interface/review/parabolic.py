#!/usr/bin/env python3
"""Separate physical-row and two-factor checks for nontriangular active changes."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json
import sympy as sp
from sympy import QQ_I as E
from check import dm,block,matrix_action,swaporder,require,support


def run():
    pts=list(product(range(2),repeat=4));I=dm(sp.eye(16));Z=I*E.zero;half=E(1,0)/E(2,0)
    SW=lambda i,j:matrix_action(pts,lambda p:(swaporder(p,i,j),1))
    R=matrix_action(pts,lambda p:((p[1],p[2],p[3],p[0]),(-1)**(p[0]*p[1]*p[3])))
    X=matrix_action(pts,lambda p:((p[0],p[1]^1,p[2],p[3]),1));a=(I*E(1,1)+X*E(1,-1))*half*R;ai=dm(a.to_Matrix().H)
    s=SW(2,3);h=SW(0,1);t=SW(1,2);k=SW(0,3)
    L=block([[a,Z,Z],[I,a,Z],[Z,Z,I]]);U=block([[a,-a**2,Z],[Z,a,Z],[Z,Z,I]])
    # Two opposite elementary shears make an ordinary, invertible, nontriangular B.
    B00=I+h*t; B01=h; B10=t; B11=I
    K=block([[B00,B01,h+t],[B10,B11,h],[Z,Z,k]])
    Ki=block([[I,-h,-(h+t-h*h)*k],[-t,I+t*h,-(-t*(h+t)+(I+t*h)*h)*k],[Z,Z,k]])
    E3=block([[I,Z,Z],[Z,I,Z],[Z,Z,I]])
    require(Ki*K==K*Ki==E3,'ordinary parabolic unit with mixed active lower block')
    for sg in [-1,1]:
        sign=E(sg,0);P=(I+s*sign)*half;N=I-P;C=block([[P,Z,-N],[P,I,-N],[N,Z,P]])
        M=L*C*K*U;f=block([[Z,Z,P]]);e=block([[Z,Z,I]])
        require(f*M==block([[Z,Z,P*k]]),'projected physical forward row')
        require(block([[-k*N*ai,Z,k*P]])*M==e,'physical inverse row')
        # A true spectator-to-active swap changes the first identity and the stated class.
        flip=block([[Z,Z,I],[Z,I,Z],[I,Z,Z]])
        require(f*L*C*K*flip*U!=block([[Z,Z,P*k]]),'changing spectator row invalidates the probe')
    quartic=a**4
    checks=0
    for first in [I,h,t,k]:
        for second in [I,h,t,k]:
            T=ai*first*ai*second*quartic
            require(all(sp.expand(x*sp.conjugate(x))<=sp.Rational(1,4) for x in T.to_Matrix()),'two inverse factors on quartic are small'); checks+=1
    require(support(ai**3*quartic)==2,'three inverse factors can restore rank one')
    return {'status':'PASS_INDEPENDENT_PHYSICAL_PARABOLIC_PROBES','prefix_signs':[-1,1],
            'mixed_active_lower_block':True,'quartic_two_inverse_exact_controls':checks,
            'negative_controls':['active–spectator exchange destroys forward identity','three inverse factors reduce quartic to rank one'],
            'all_Gl2_claim_verified_by':'source block identities and finite-catalogue proof in PARABOLIC-REVIEW.md'}

if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
