#!/usr/bin/env python3
"""Exact interface controls and rigorous H4 packet ceiling; no source algorithm claim."""
import argparse,hashlib,json
from fractions import Fraction as Q
from pathlib import Path

def need(p,m):
    if not p: raise RuntimeError(m)
def mat(a): return [[Q(x) for x in r] for r in a]
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def plus(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a): return [[-x for x in r] for r in a]
def text(a): return [[str(x) for x in r] for r in a]
def main():
    p=argparse.ArgumentParser();p.add_argument('--tariff',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=a.tariff.read_bytes();need(hashlib.sha256(raw).hexdigest()=='8c4c9781a72926bbce2ac8c0a920241a609eeac0c291c3c595c068da1404370d','tariff pin')
    z=json.loads(raw);D=int(z['power_denominator']);lo,hi=map(int,z['power_bounds']['9'])
    need(lo**200<=9**199*D**200<=hi**200,'exact power bracket')
    L,U=map(int,z['profiles']['H4_no_second_owned']['margin_numerator_bounds'])
    profiles={}
    for r in (8,9,10,11):
        lb=L-18*(8*D+r*hi);ub=U-18*(8*D+r*lo)
        profiles[str(r)]={'margin_numerator_bounds':[str(lb),str(ub)],'denominator':str(18*D),'strict_positive':lb>0}
    need(profiles['10']['strict_positive'] and int(profiles['11']['margin_numerator_bounds'][1])<0,'ceiling')
    T=mat([[Q(1,2),0],[3,-1]]);Ti=mat([[2,0],[6,-1]]);I=mat([[1,0],[0,1]])
    need(mm(T,Ti)==I,'inverse')
    H=mat([[1,0,0],[0,1,0]]);Fo=mat([[0,0,2]]);V=mat([[0],[0],[Q(1,2)]])
    A=mat([[1,0,5]]);B=mat([[1,-1]]);R=mat([[1,0]]);Zo=mat([[1,2]])
    need(mm(H,V)==mat([[0],[0]]) and mm(Fo,V)==mat([[1]]),'right inverse and no feedback')
    J=mm(Zo,Ti);K=neg(mm(V,J));E=plus(plus(R,neg(mm(B,Ti))),mm(mm(A,V),J))
    need(plus(mm(Fo,K),mm(Zo,Ti))==mat([[0,0]]),'endpoint repair')
    need(plus(plus(mm(A,K),mm(B,Ti)),E)==R,'receiver repair')
    badE=plus(R,neg(mm(B,Ti)))
    need(plus(plus(mm(A,K),mm(B,Ti)),badE)!=R,'missing AV term must fail')
    d=mat([[1],[7]])
    need(mm(J,d)==mat([[0]]) and mm(E,d)==mat([[-2]]),'debt-only packet fails gain')
    need(plus(mm(Fo,K),mm(Zo,Ti))==mat([[0,0]]),'COPY guard positive')
    need(mm(Fo,K)!=mat([[0,0]]),'wrong guard must fail')
    pure=mat([[1,0],[3,1]])
    need(mm(pure,Ti)!=I,'pure-overwrite normalization must fail')
    out={'status':'PASS_EXACT_INTERFACE_CONTROLS_AND_PACKET_CEILING','tariff_sha256':hashlib.sha256(raw).hexdigest(),'profiles':profiles,'example':{'T':text(T),'J':text(J),'E':text(E),'debt_invisible_displacement':text(d)},'negative_controls':['omit A V J','send debt-only packet while receiver deficit independent','drop COPY response','replace scaled-control T by I+L'],'scope':'Fixed right inverse, controls, decoder and H4 optimistic invoice; no complete source construction or new kappa.'}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':main()
