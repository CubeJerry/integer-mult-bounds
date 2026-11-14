#!/usr/bin/env python3
"""Exact noncommuting controls and full two-call correction allowance."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
def need(v,msg):
    if not v:raise ValueError(msg)
def bracket(x):
    scale=10**28;target=x**199*scale**200;lo,hi=0,x*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    return F(lo,scale),F(hi,scale)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    I=s.eye(2);Z=s.zeros(2);a=s.Matrix([[1,2],[0,1]]);b=s.Matrix([[1,0],[3,1]]);D1=s.Matrix([[2,1],[1,1]]);D2=s.Matrix([[1,4],[1,5]])
    U=lambda x:s.BlockMatrix([[I,x],[Z,I]]).as_explicit();L=lambda x:s.BlockMatrix([[I,Z],[x,I]]).as_explicit();delta=lambda x:s.diag(x,x)
    c=b.inv()*D1*a.inv()*D1.inv();d=D2*b.inv()*D2.inv();swap=s.BlockMatrix([[Z,-I],[I,Z]]).as_explicit();F1=delta(D1)*U(a);F2=delta(D2)*L(-b)
    expected=s.diag(D2*D1*a.inv(),D2*b.inv()*D1)
    need(swap*U(d)*F2*s.diag(c,I)*F1==expected,'generic noncommuting extraction')
    need(swap*U(d)*F2*s.diag(b.inv()*a.inv(),I)*F1!=expected,'omit interstage body conjugation')
    need(swap*U(b.inv())*F2*s.diag(c,I)*F1!=expected,'omit final body conjugation')
    # Independently solve all four c entries from the exact zero-block equations.
    symbols=s.symbols('c0:4');C=s.Matrix(2,2,symbols);equations=list(D1-b*C*D1*a)
    solution=s.solve(equations,symbols,dict=True);need(len(solution)==1 and C.subs(solution[0])==c,'unique scoped interstage correction')
    terms=[(448,17),(-224,1)]+[(-448,r)for r in [2,3,5,6]];lo=hi=F(0)
    for coefficient,x in terms:
        lower,upper=bracket(x)
        if coefficient<0:lower,upper=upper,lower
        lo+=coefficient*lower;hi+=coefficient*upper
    entropy=bracket(448);need(0<lo<hi<entropy[0],'strict full-invoice unitary gate')
    out={'status':'PASS_EXACT_NONCOMMUTING_EXTRACTION_AND_PRICE','noncommuting_matrix_dimensions':2,'independent_inputs':4,'c':[[str(x)for x in row]for row in c.tolist()],'d':[[str(x)for x in row]for row in d.tolist()],'controls':['missing_interstage_body_conjugation','missing_final_body_conjugation'],'unique_c_in_declared_template':True,'whole_two_bank_allowance':[str(lo),str(hi)],'unitary_joint_two_bank_asymptotic_lower_bound':[str(x)for x in entropy],'strict_gap_lower':str(entropy[0]-hi),'scope':'Generic block proof is universal; this exact finite noncommuting instance tests order and uniqueness. Actual C geometry separately certified. No general caller exclusion or new kappa.'}
    args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'allowance':float(lo),'unitary_lower':float(entropy[0])}))
if __name__=='__main__':main()
