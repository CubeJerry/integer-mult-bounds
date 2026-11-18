#!/usr/bin/env python3
"""Exact full-column sharp quartic control and complete movement enclosure."""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sympy as sp
from sympy import QQ_I

ENGINE = '12217a5dd708c9adb93987eb2d10e23185e279ac3ea46fe0c68e523a370610f3'

def interval(n):
    scale = 10**44
    top = n ** 199 * scale ** 200
    lo, hi = 0, n * scale + 1
    while hi-lo > 1:
        m = (hi+lo)//2
        if m**200 <= top:lo = m
        else:hi = m
    assert lo**200 <= top < hi**200
    return Fraction(lo,scale), Fraction(hi,scale)

def deficit():
    terms = [(3,1),(6,7),(3,8),(-1,25),(-1,23),(-1,21)]
    bounds = [sum(f*interval(n)[(f<0)^i] for f,n in terms) for i in (0,1)]
    assert 0 < bounds[0] < bounds[1]
    return [str(x) for x in bounds]

def verify(m):
    one=m.dm(sp.eye(16));z=one*0
    xb=m.table(lambda a,b,c,d:(a,b^1,c,d))
    rot=m.table(lambda a,b,c,d:(b,c,d,a),lambda a,b,c,d:2*a*b*d)
    a=(one*QQ_I(1,1)+xb*QQ_I(1,-1))*QQ_I.from_sympy(sp.Rational(1,2))*rot
    ai=m.adj(a)
    assert ai*a==a*ai==one
    ranks=[m.rank_type(a**j) for j in range(5)]
    assert ranks==list(range(5))
    def lift(v):return m.lin([v,z],[z,v])
    a,ai,one,z=map(lift,(a,ai,one,z))
    eye=m.lin([one,z,z],[z,one,z],[z,z,one]);l=m.lin([a,z,z],[one,a,z],[z,z,one])
    li=m.lin([ai,z,z],[-ai**2,ai,z],[z,z,one]);u=m.lin([a,-a**2,z],[z,a,z],[z,z,one])
    ui=m.lin([ai,one,z],[z,ai,z],[z,z,one])
    assert l*li==li*l==u*ui==ui*u==eye
    e=l*u*l;einv=li*ui*li
    actual=m.lin([z,-a**4,z],[a**2,z,z],[z,z,one])
    assert e==actual and e*einv==einv*e==eye
    ports=[m.lin([one],[z],[z]),m.lin([z],[one],[z]),m.lin([z],[z],[one])]
    rr=[m.adj(p) for p in ports]
    assert rr[0]*e*ports[1]==-a**4 and rr[0]*e*ports[2]==rr[2]*e*ports[1]==z
    assert rr[2]*e*ports[2]==one and (e*ports[1]).rank()==32
    add01=m.lin([one,one,z],[z,one,z],[z,z,one]);add10=m.lin([one,z,z],[one,one,z],[z,z,one])
    neg0=m.lin([-one,z,z],[z,one,z],[z,z,one]);ops=(add01,neg0,add10,neg0,add01)
    target=m.lin([a**2,z,z],[z,a**4,z],[z,z,one])
    def run(omit):
        out=e
        for i,op in enumerate(ops):
            if omit!=i:out=op*out
        return out
    assert run(None)==target and all(run(i)!=target for i in range(5))
    plus=m.lin([a,a**2,z],[z,a,z],[z,z,one])
    assert l*plus*l!=actual
    h=m.lin([one,z,z],[z,one,one],[z,z,one]);w=m.lin([one,z,z],[z,one,z],[one,z,one])
    shifted=l*h*u*w*l
    assert rr[1]*shifted*ports[2]==a and rr[2]*shifted*ports[0]==a
    dropped=actual-ports[2]*rr[2]
    assert dropped.rank()==64 and e.rank()==96 and dropped*ports[1]==e*ports[1]
    return {'literal_classes':ranks,'full_bank_dimension':32,'tested_arbitrary_source_columns':96,
            'full_source_rank':e.rank(),'isolated_quartic_rank':(e*ports[1]).rank(),
            'sharp_source_interstages':'ordinary identity on all three banks',
            'original_order_restoration':{'ADD':3,'SCALE_minus_one':2,'rejected_primitive_omissions':5},
            'wrong_middle_sign_rejected':True,'forbidden_active_spectator_class_one_controls':2,
            'deleted_spectator_rank':dropped.rank()}

def main():
    p=ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();src=args.engine/'check.py';assert sha256(src.read_bytes()).hexdigest()==ENGINE
    spec=importlib.util.spec_from_file_location('retained_exact_engine',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    result={'status':'PASS_UNRESTRICTED_TWO_STAGE_QUARTIC_FLAGS_AND_SHARP_ALL_INPUT_420',
            'baseline':'e31d437b489a416446fdd7e294bc2238829c5925','exact_engine_sha256':ENGINE,
            'profile_cap_conditional_on_a_quartic':[4,2,0],'sharp_deficit_199_over_200':deficit(),
            'nonquartic_endpoint_cap_proved_by_this_gate':False,'complete_supplier':False,'new_kappa':False,**verify(m)}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])
if __name__=='__main__':main()
