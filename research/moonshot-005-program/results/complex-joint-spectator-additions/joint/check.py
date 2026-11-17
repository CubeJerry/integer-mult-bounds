#!/usr/bin/env python3
"""Exact full-prefix all-column and local cost controls for two active inputs."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import importlib.util,json,sys
from pathlib import Path
import sympy
from sympy import QQ_I

PARENT="12217a5dd708c9adb93987eb2d10e23185e279ac3ea46fe0c68e523a370610f3"
SECOND_PROOF="49537004d25275ea22272b278e86cdba06725b87394fd36460ec9d424e935bd5"


def shear(i,j,summands):
    ops=[]
    for mon,c in summands:
        if mon:ops.append(("MONO",j,mon))
        if c!=1:ops.append(("SCALE",j,F(c)))
        ops.append(("ADD",i,j))
        if c!=1:ops.append(("SCALE",j,1/F(c)))
        if mon:ops.append(("ADJOINT",j,mon))
    return ops


def reverse(word):
    inv=[]
    for op,i,c in reversed(word):
        if op=="ADD":inv+=shear(i,c,[(None,-1)])
        elif op=="SCALE":inv.append((op,i,1/c))
        elif op=="MONO":inv.append(("ADJOINT",i,c))
        else:inv.append(("MONO",i,c))
    return inv


def make_words():
    one=[(None,F(1))];minus=[(None,F(-1))];half=F(1,2)
    had=[("ADD",0,1),("SCALE",1,F(-2)),("ADD",1,0)]
    control=had+[("MONO",1,"minus_X")]+had+[("SCALE",0,half),("SCALE",1,half)]
    old=shear(2,1,minus)+shear(1,0,one)
    return {"first_input_shear":shear(2,0,[("X",F(1))]),
            "second_interface_swap":[("SCALE",1,F(-1))]+shear(1,2,one)+shear(2,1,minus)+shear(1,2,one),
            "input_endpoint":shear(0,2,[(None,-half),("S2",-half),("X",half),("XS2",half)]),
            "physical_output_endpoint":control+shear(1,2,[(None,half),("X",half),("S",-half),("SX",-half)])+
            [("MONO",2,"minus_SX")]+old}


def check(m):
    i16=m.dm(sympy.eye(16));z16=i16*0
    half=QQ_I.from_sympy(sympy.Rational(1,2))
    xb=m.table(lambda a,b,c,d:(a,b^1,c,d))
    r=m.table(lambda a,b,c,d:(b,c,d,a),lambda a,b,c,d:2*a*b*d)
    A=(i16*QQ_I(1,1)+xb*QQ_I(1,-1))*half*r
    s=m.gp((0,1,3,2));s2=m.gp((1,0,2,3))
    def two(v):return m.lin([v,z16],[z16,v])
    one=two(i16);zero=two(z16);a=two(A);ai=m.adj(a);S=m.lin([s,z16],[z16,-s])
    X=m.lin([z16,i16],[i16,z16]);S2=m.lin([s2,z16],[z16,-s2])
    P=(one+S)*half;N=one-P;P2=(one+S2)*half;hp=(one+X)*half;hm=one-hp
    assert P2==ai**2*P*a**2 and S*X==-X*S and a*X==X*a
    l=m.lin([a,zero,zero],[one,a,zero],[zero,zero,one])
    li=m.lin([ai,zero,zero],[-ai**2,ai,zero],[zero,zero,one])
    u=m.lin([a,-a**2,zero],[zero,a,zero],[zero,zero,one])
    ui=m.lin([ai,one,zero],[zero,ai,zero],[zero,zero,one])
    c=m.lin([P,zero,-N],[P,one,-N],[N,zero,P])
    ci=m.lin([P,zero,N],[-one,one,zero],[-N,zero,P])
    o=m.lin([one,zero,zero],[one,one,zero],[zero,-one,one])
    oi=m.lin([one,zero,zero],[-one,one,zero],[-one,one,one])
    eye=m.lin([one,zero,zero],[zero,one,zero],[zero,zero,one])
    e2=m.lin([zero],[zero],[one])
    ret=two(A*m.gp((0,2,1,3))*A)
    clock=two(m.table(lambda a,b,c,d:(a,c,b,d),lambda a,b,c,d:b-c))
    tests=[]
    for tag,t0,t1 in [("first_only",X,zero),("second_only",zero,clock),("both_noncommuting",X*S,ret+S),
                      ("both_singular",P*clock*N,N*X*P)]:
        J=m.lin([one,zero,zero],[zero,one,zero],[t0,t1,one])
        ji=m.lin([one,zero,zero],[zero,one,zero],[-t0,-t1,one])
        M=l*c*J*u;Mi=ui*ji*ci*li
        assert M*Mi==Mi*M==eye
        assert m.lin([zero,P,zero])*oi*M==m.lin([P*a,zero,zero])
        assert m.lin([zero,zero,one])*Mi==m.lin([(t1-t0*P-N)*ai+t1*ai**2,-t1*ai,P-t0*N])
        for p,z,w in [(ret,clock+one,X),(P,ret-N,S2)]:
            x=P*a*p-N*(t0*a*p+t1*a*z)
            y=a*p+S*(t0*a*p+t1*a*z)
            expected=m.lin([a*x-a*(P-N*t0)*a**2*z-a*N*w],
                           [x+N*(one+t0)*a**2*z-N*w],
                           [y-S*t0*a**2*z+S*w])
            assert oi*M*m.lin([p],[z],[w])==expected
        tests.append(tag)
    J=m.lin([one,zero,zero],[zero,one,zero],[X,zero,one])
    q=m.lin([one,zero,zero],[zero,zero,one],[zero,one,zero])
    O=o*m.lin([hm,hp,zero],[hp,hm,N*(one+X)],[zero,zero,-S*X])
    Iin=m.lin([one,zero,-(one-X)*P2],[zero,one,zero],[zero,zero,one])
    D=m.lin([a**3,zero,zero],[zero,a**2,zero],[zero,zero,a**2])
    E=l*c*J*u*q*l
    assert oi*E*e2==m.lin([-(one-X)*a**3*P2],[N*(one+X)*a**2],[-S*X*a**2])
    assert E*e2==O*D*Iin*e2
    defect=E-O*D*Iin
    assert not defect.is_zero_matrix and l*c*u*q*l*e2!=E*e2
    def replay(word,skip=None):
        fields=[m.lin([one,zero,zero]),m.lin([zero,one,zero]),m.lin([zero,zero,one])]
        amps=[F(1)]*3;peak=F(1)
        monos={"minus_X":-X,"X":X,"S":S,"S2":S2,"XS2":X*S2,"SX":S*X,"minus_SX":-S*X}
        for i,(op,j,arg) in enumerate(word):
            if i==skip:continue
            if op=="ADD":fields[j]+=fields[arg];amps[j]+=amps[arg]
            elif op=="SCALE":
                fields[j]*=QQ_I.from_sympy(sympy.Rational(arg.numerator,arg.denominator));amps[j]*=abs(arg)
            else:fields[j]=(monos[arg] if op=="MONO" else m.adj(monos[arg]))*fields[j]
            peak=max(peak,*amps)
        return fields[0].vstack(*fields[1:]),peak
    target={"first_input_shear":J,"second_interface_swap":q,"input_endpoint":Iin,"physical_output_endpoint":O}
    receipts={}
    for k,word in make_words().items():
        receipts[k]={}
        for direction,ww in [("forward",word),("inverse",reverse(word))]:
            actual,peak=replay(ww)
            if direction=="forward":assert actual==target[k]
            else:assert actual*target[k]==target[k]*actual==eye
            idx=[i for i,op in enumerate(ww) if op[0]=="ADD"]
            assert all(replay(ww,i)[0]!=actual for i in idx)
            receipts[k][direction]={"counts":dict(Counter("MONO" if x[0]=="ADJOINT" else x[0] for x in ww)),
                                    "uniform_triangle_bound":str(peak),"omitted_ADD_controls":len(idx)}
    return {"full_prefix_dimension":2,"tail_dimension":16,"tested_input_columns_per_full_word":96,
            "joint_two_column_samples":tests,"all_input_defect_rank":defect.rank(),
            "completed_column_cubic_rank":((one-X)*a**3*P2).rank(),"completed_column_quadratic_rank":(-S*X*a**2).rank(),
            "benchmark_receipts":receipts,"omitted_first_shear_rejected":True}


if __name__=="__main__":
    ap=ArgumentParser();ap.add_argument("--parent",type=Path,required=True);ap.add_argument("--second",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    file=args.parent/"check.py";assert sha256(file.read_bytes()).hexdigest()==PARENT
    assert sha256((args.second/"PROOF.md").read_bytes()).hexdigest()==SECOND_PROOF
    spec=importlib.util.spec_from_file_location("joint_shared_exact",file)
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    result={"status":"PASS_JOINT_SPECTATOR_ADDITIONS_AND_CUBIC_QUADRATIC_COLUMN",
            "baseline":"e31d437b489a416446fdd7e294bc2238829c5925","parent_exact_engine_sha256":PARENT,
            "second_source_proof_sha256":SECOND_PROOF,"proven_maximum_total_independent_head":6,
            "all_ordinary_t0_t1":True,"complete_supplier":False,"new_complete_kappa":False,
            **check(m),"full_source_price_deficit":m.price()["parabolic_deficit_at_199_over_200"]}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"])
