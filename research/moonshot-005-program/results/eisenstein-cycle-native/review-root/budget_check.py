#!/usr/bin/env python3
"""Independent coarse rational enclosures for two all-arm price exclusions."""
import argparse,json
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
S=10**18
def need(c,m):
    if not c:raise ValueError(m)
def power(n):
    with localcontext() as c:
        c.prec=55;k=int((Decimal(n)**(Decimal(199)/200))*S)
    z=n**199*S**200
    while k**200>z:k-=1
    while (k+1)**200<=z:k+=1
    need(k**200<=z<(k+1)**200,'integer-power authentication')
    return F(k,S),F(k+1,S)
def plus(*xs):return sum(x[0] for x in xs),sum(x[1] for x in xs)
def mul(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
def delta(n):return plus(power(n+1),mul(-1,power(n)))
def W(a):return plus(mul(2,power(16*a+1)),mul(4,power(8*a+1)),(-F(4),-F(4)),*(mul(4,delta(8*j)) for j in range(1,a)))
def H(a):return plus(mul(a,W(a+1)),mul(-a-1,W(a)))
def enc(x):return {'rational_interval':list(map(str,x)),'midpoint':float(sum(x)/2)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    cost=mul(240,plus(power(1),power(7),power(8)));allow=mul(10,W(6));room=plus(allow,mul(-1,cost))
    direct=mul(240,power(2));entropy=power(480);head3=plus(mul(2,power(3)),mul(4,power(6)));per=mul(F(1,120),cost)
    need(H(5)[0]>0 and H(6)[1]<0,'unique all-arm maximizer a6 after strict concavity proof')
    need(direct[0]>room[1] and entropy[0]>room[1],'both modular service price gates')
    need(head3[1]<per[0],'all-arm fixed-three-head gate')
    d={'status':'PASS_INDEPENDENT_RATIONAL_CALLER_PRICE_GATES','method':'Decimal seeds only; every bound authenticated by exact 200th powers; rewritten telescoping surplus','native':enc(cost),'allowance_a6':enc(allow),'H5':enc(H(5)),'H6':enc(H(6)),'room':enc(room),'direct_two_bank':enc(direct),'restricted_joint_unitary_floor':enc(entropy),'fixed_three_head_all_arm_upper':enc(head3),'native_per_port':enc(per),'no_general_caller_lower_bound':True,'no_new_kappa':True}
    a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
