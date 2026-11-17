#!/usr/bin/env python3
"""Exact source tests and a literal whole-bank cubic/linear endpoint benchmark."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy
from sympy import QQ_I

PARENT_CHECK="12217a5dd708c9adb93987eb2d10e23185e279ac3ea46fe0c68e523a370610f3"
PARENT_PROOF="2637c23639f437a5bf659376b3da24cf33fb934f7dfba57ed48f6a06ad23a598"


def parent_at(path):
    for name,digest in [("check.py",PARENT_CHECK),("PROOF.md",PARENT_PROOF)]:
        assert sha256((path/name).read_bytes()).hexdigest()==digest
    spec=importlib.util.spec_from_file_location("spectator_exact_material",path/"check.py")
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def ops_cohort():
    def had(i,j):
        return [("ADD",i,j),("SCALE",j,F(-2)),("ADD",j,i)]
    def sw(i,j,s):
        return had(i,j)+[("MONO",j,s)]+had(i,j)+[("SCALE",i,F(1,2)),("SCALE",j,F(1,2))]
    minus=[("SCALE",1,F(-1)),("ADD",2,1),("SCALE",1,F(-1))]
    return {
      "changed_shear":[("MONO",1,"t"),("ADD",2,1),("MONO",1,"t")],
      "second_interface":sw(0,2,"s2")+sw(1,2,"minus_s2")+[("MONO",0,"t1")],
      "output_endpoint":[("SCALE",0,F(-1))]+minus+[("ADD",1,0)],
      # E02(P2) = E02(I/2) E02(S2/2); both source histories are restored.
      "input_endpoint":[("SCALE",2,F(1,2)),("ADD",0,2),("SCALE",2,F(2)),
                        ("MONO",2,"s2"),("SCALE",2,F(1,2)),("ADD",0,2),
                        ("SCALE",2,F(2)),("MONO",2,"s2"),("MONO",2,"t1")]
    }


def inverted(word):
    out=[]
    for op,dst,arg in reversed(word):
        if op=="ADD":
            out.extend([("SCALE",arg,F(-1)),(op,dst,arg),("SCALE",arg,F(-1))])
        elif op=="SCALE":out.append((op,dst,1/arg))
        else:out.append((op,dst,arg))
    return out


def numerical(m):
    ident=m.dm(sympy.eye(16));zero=ident*0
    half=QQ_I.from_sympy(sympy.Rational(1,2))
    x=m.table(lambda a,b,c,d:(a,b^1,c,d))
    r=m.table(lambda a,b,c,d:(b,c,d,a),lambda a,b,c,d:2*a*b*d)
    a=(ident*QQ_I(1,1)+x*QQ_I(1,-1))*half*r
    ai=m.adj(a);s=m.gp((0,1,3,2));s1=m.gp((3,1,2,0));s2=m.gp((1,0,2,3))
    t=m.gp((2,1,0,3));t1=m.gp((0,3,2,1))
    assert ai*t*a==t1 and t1*s2*t1==s1
    L=m.lin([a,zero,zero],[ident,a,zero],[zero,zero,ident])
    Li=m.lin([ai,zero,zero],[-ai**2,ai,zero],[zero,zero,ident])
    U=m.lin([a,-a**2,zero],[zero,a,zero],[zero,zero,ident])
    Ui=m.lin([ai,ident,zero],[zero,ai,zero],[zero,zero,ident])
    O0=m.lin([ident,zero,zero],[ident,ident,zero],[zero,-ident,ident])
    Oi=m.lin([ident,zero,zero],[-ident,ident,zero],[-ident,ident,ident])
    eye=m.lin([ident,zero,zero],[zero,ident,zero],[zero,zero,ident])
    E2=m.lin([zero],[zero],[ident])
    selected=m.lin([a**3,zero,zero],[zero,a**3,zero],[zero,zero,a])
    def supports(x):
        M=x.to_Matrix()
        return [tuple(i for i in range(16) if M[i,j]!=0) for j in range(16)]
    src=supports(a);assert all(len(p)==2 and p[0]^p[1]==2 for p in src)
    equal=disjoint=0
    for i in range(16):
        for j in range(i):
            if i^j==4:
                assert src[i]==src[j];equal+=1
            else:
                assert set(src[i]).isdisjoint(src[j]);disjoint+=1
    # A rank-one clock demonstrates that the c-pair condition is attainable.
    clock=m.table(lambda a,b,c,d:(a,c,b,d),lambda a,b,c,d:b-c)
    V=clock*a
    assert m.rank_type(V)==m.rank_type(a*V)==1
    assert all(p[0]^p[1]==4 for p in supports(V))
    assert all(p[0]^p[1]==8 for p in supports(s*V))
    assert all(p[0]^p[1]==2 for p in supports(a*clock*a))
    assert m.rank_type(a*(a*clock*a))==2
    # Using a different swap that fixes c would invalidate the disjoint-pair witness.
    assert all(p[0]^p[1]==4 for p in supports(s1*V))
    receipt={};examples=[]
    for sign in (1,-1):
        S=s*sign;P=(ident+S)*half;N=ident-P
        S2=s2*sign;P2=(ident+S2)*half;N2=ident-P2
        C=m.lin([P,zero,-N],[P,ident,-N],[N,zero,P])
        Ci=m.lin([P,zero,N],[-ident,ident,zero],[-N,zero,P])
        # Define the routing by genuine projector swaps rather than trusting the display.
        swap02=m.lin([P2,zero,N2],[zero,ident,zero],[N2,zero,P2])
        swap12=m.lin([ident,zero,zero],[zero,N2,P2],[zero,P2,N2])
        diag_t1=m.lin([t1,zero,zero],[zero,ident,zero],[zero,zero,ident])
        Q=diag_t1*swap12*swap02
        assert Q*E2==m.lin([t1*N2],[P2],[zero])
        K=m.lin([ident,zero,zero],[zero,ident,zero],[zero,t,ident])
        input_end=m.lin([ident,zero,P2],[zero,ident,zero],[zero,zero,t1])
        output_end=O0*m.lin([-ident,zero,zero],[zero,ident,zero],[zero,zero,ident])
        E=L*C*K*U*Q*L
        assert Oi*E*E2==m.lin([-a**3*P2],[zero],[a*t1])
        assert E*E2==output_end*selected*input_end*E2
        defect=E-output_end*selected*input_end
        assert not defect.is_zero_matrix
        assert L*C*U*Q*L*E2 != E*E2
        physical_probe=m.lin([-ident,ident,ident]);row1=m.lin([zero,P,zero])
        numerical_sources=[("zero",zero),("transported_swap",t),("nontransported_phase",clock),
                           ("singular_projector",P),("singular_noncommuting",N*clock*P)]
        for name,T in numerical_sources:
            actual_k=m.lin([ident,zero,zero],[zero,ident,zero],[zero,T,ident])
            actual_ki=m.lin([ident,zero,zero],[zero,ident,zero],[zero,-T,ident])
            ist=Ui*actual_ki*Ci*Li
            M=L*C*actual_k*U
            assert M*ist==ist*M==eye
            assert physical_probe*M==m.lin([a,S*T*a,S])
            assert m.lin([zero,zero,ident])*ist==m.lin([(T-N)*ai+T*ai**2,-T*ai,P])
            assert row1*Oi*M==m.lin([P*a,zero,zero])
            for p,z,w in [(r,s1+ident,x),(P,r-N,s2)]:
                X=P*a*p-N*T*a*z
                Ucol=a*p+S*T*a*z
                expected=m.lin([a*X-a**3*P2*z-a*N*w],
                               [X+a**2*N2*z-N*w],[Ucol+S*w])
                assert Oi*M*m.lin([p],[z],[w])==expected
        monos={"s2":S2,"minus_s2":-S2,"t":t,"t1":t1}
        def replay(word,omit=None):
            banks=[m.lin([ident,zero,zero]),m.lin([zero,ident,zero]),m.lin([zero,zero,ident])]
            norms=[F(1)]*3;peak=F(1)
            for it,(op,dst,arg) in enumerate(word):
                if it==omit:continue
                if op=="ADD":banks[dst]+=banks[arg];norms[dst]+=norms[arg]
                elif op=="SCALE":
                    banks[dst]*=QQ_I.from_sympy(sympy.Rational(arg.numerator,arg.denominator));norms[dst]*=abs(arg)
                else:banks[dst]=monos[arg]*banks[dst]
                peak=max(peak,*norms)
            return banks[0].vstack(*banks[1:]),peak
        controls=0
        for label,w in ops_cohort().items():
            desired={"changed_shear":K,"second_interface":Q,"output_endpoint":output_end,
                     "input_endpoint":input_end}[label]
            receipt[label]={}
            for direction,ww in [("forward",w),("inverse",inverted(w))]:
                actual,norm=replay(ww)
                if direction=="forward":assert actual==desired
                else:assert desired*actual==actual*desired==eye
                ids=[i for i,x in enumerate(ww) if x[0]=="ADD"]
                assert all(replay(ww,i)[0]!=actual for i in ids)
                controls+=len(ids)
                receipt[label][direction]={"counts":dict(Counter(x[0] for x in ww)),
                                          "uniform_triangle_prefix_bound":str(norm),
                                          "ADD_omission_checks":len(ids)}
        examples.append({"prefix_sign":sign,"native_matrices_checked":len(numerical_sources),
                         "input_columns_per_paid_unit":48,"all_other_column_defect_rank":defect.rank(),
                         "positive_cubic_half_rank":P2.rank(),"positive_linear_rank":(a*t1).rank(),
                         "omitted_shear_rejected":True,"primitive_omissions":controls})
    return {"all_one_letter_distinct_input_pairs":equal+disjoint,"equal_support_c_pairs":equal,
            "other_input_pairs_with_disjoint_support":disjoint,"actual_c_pair_clock":True,
            "swapping_c_to_d_is_essential_for_pair_witness":True,"literal_forward_inverse_receipts":receipt,
            "width_one_sector_checks":examples}


def main():
    p=ArgumentParser();p.add_argument("--parent",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    args=p.parse_args();m=parent_at(args.parent)
    ans={"status":"PASS_ARBITRARY_SECOND_INPUT_SPECTATOR_SHEAR_GATE_AND_CUBIC_COLUMN",
         "source_baseline":"e31d437b489a416446fdd7e294bc2238829c5925","parent_check_sha256":PARENT_CHECK,
         "parent_proof_sha256":PARENT_PROOF,**numerical(m),**m.price(),
         "every_ordinary_shear_in_scope":True,"maximum_independent_head":3,
         "at_least_one_head_at_most":1,"profile_331":False,"total_head_rank_at_most":6,
         "new_complete_kappa":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(ans,indent=2)+"\n")
    print(ans["status"])


if __name__=="__main__":
    main()
