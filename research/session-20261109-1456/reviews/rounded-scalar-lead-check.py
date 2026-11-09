"""Independent exact oracle against frozen literal rounded scalar tables.

Uses heterogeneous field widths and coefficients outside the author's small
ADD set; drives the unchanged primitive directly, not its test wrapper.
Prepared for @CubeJerry with substantial OpenAI assistance.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
from random import Random
import sys
from types import SimpleNamespace

ROOT=Path('/workspace/scratch/a365d332d434/worker-rounded-scalar')
PKG=ROOT/'research/current-rounded-scalar-tables'
sys.path.insert(0,str(PKG))
from tables import compile_rounded
from physical import M,Tape,RowCounter

def encode(values,widths):
    result=[]
    for value,width in zip(values,widths):
        for sym in [(value>>j)&1 for j in range(width)]+[2]:
            result.extend(((sym>>2)&1,(sym>>1)&1,sym&1))
    return result

def decode(tape,widths):
    bits=tape.body();symbols=[4*bits[i]+2*bits[i+1]+bits[i+2] for i in range(0,len(bits),3)]
    result=[];offset=0
    for width in widths:
        digit=symbols[offset:offset+width]
        assert len(digit)==width and symbols[offset+width]==2
        assert all(z in (0,1) for z in digit)
        result.append(sum(z*(1<<i) for i,z in enumerate(digit))-(digit[-1]<<width));offset+=width+1
    assert offset==len(symbols)
    return tuple(result)

rng=Random(202611092017);cases=successes=controls=0;max_ratio=F(0)
cache={};coefficient_set=[F(7,96),F(-31,80),F(17,24),F(-5,384),F(9,128),F(-257,512),F(3),F(1,1024)]
for op in ('SCALE','ADD'):
    for coefficient in coefficient_set:
        table,receipt=compile_rounded(op,coefficient);cache[op,coefficient]=(table,receipt)
        for case in range(30):
            widths=([1,2,3,4] if case==0 else [rng.randrange(1,25) for _ in range(2 if case%2 else 6)])
            x=[];y=[]
            for width in widths:
                bound=1<<(width-1)
                choices=[-bound,bound-1,0,rng.randrange(-bound,bound)]
                x.append(choices[case%4]);y.append(choices[(case+1)%4])
            public=[Tape(encode(x,widths),101)]
            if op=='ADD':public.append(Tape(encode(y,widths),1001,True))
            work=[Tape((1,0)*17,2001),Tape((0,1)*31,3001)]
            work[0].pos+=13;work[1].pos+=61
            contexts=[Tape((1,0,0,1),4001,True)]
            before=[t.body() for t in public+contexts]
            A=sum(len(t.body()) for t in work);allports=public+work+contexts
            rows=RowCounter(table)
            controller=SimpleNamespace(payloads=tuple(allports),primitive_work=(len(public),len(public)+1),primitive_context=(len(allports)-1,),services={('lead',):rows})
            a,b=coefficient.numerator,coefficient.denominator
            expected=[]
            for xx,yy in zip(x,y if op=='ADD' else x):
                numerator=a*yy+b//2
                nearest=numerator//b
                expected.append(nearest+(xx if op=='ADD' else 0))
            admit=all(-(1<<(w-1))<=z<(1<<(w-1)) for z,w in zip(expected,widths))
            error=None
            try:M.Controller.primitive(controller,('lead',),tuple(range(len(public))))
            except ValueError as exc:error=str(exc)
            assert (error is None)==admit,(op,str(coefficient),widths,x,y,error,expected)
            if admit:
                assert decode(public[0],widths)==tuple(expected)
                assert all(t.pos==t.origin for t in allports)
                assert all(t.blank() for t in work)
                S=sum(w+1 for w in widths);R=len(widths);d=receipt['denominator_twos']
                cost=sum(t.actions for t in allports)+rows.steps
                budget=512*(S+1)+64*d*R+7*A+16
                assert rows.steps<=37*S+3*d*R+32
                assert cost<=budget
                max_ratio=max(max_ratio,F(cost,budget));successes+=1
            else:assert public[0].body()==before[0]
            if op=='ADD':assert public[1].body()==before[1]
            assert contexts[0].body()==before[-1]
            assert all(t.protected() for t in allports)
            cases+=1

# Cancellation requires retaining the numerator rather than rounding a narrow
# product in a separate same-width field. Three times 3 does not fit W4, but
# (-8)+3*3=1 does. This drives the literal direct ADD path.
table,_=cache['ADD',F(3)]
public=[Tape(encode((-8,0),(4,4)),101),Tape(encode((3,0),(4,4)),1001,True)]
work=[Tape((),2001),Tape((),3001)]
controller=SimpleNamespace(payloads=tuple(public+work),primitive_work=(2,3),primitive_context=(),services={('lead',):table})
M.Controller.primitive(controller,('lead',),(0,1))
assert decode(public[0],(4,4))==(1,0);controls+=1

helper=Path('/workspace/scratch/a365d332d434/query-optimum/scripts');sys.path.insert(0,str(helper))
spec=importlib.util.spec_from_file_location('gate',helper/'check_research_commit.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
gate.check(ROOT,'research/current-rounded-scalar-tables','HEAD',False,True)
result={'local_commit':'c80bb044e76ed2883c12aaa5c145eb3b1217dcad','proof_sha256':hashlib.sha256((PKG/'PROOF.md').read_bytes()).hexdigest(),'table_sha256':hashlib.sha256((PKG/'tables.py').read_bytes()).hexdigest(),'heterogeneous_width_cases':cases,'successes':successes,'correct_overflow_rejections':cases-successes,'cancellation_control':controls,'max_combined_cost_over_bound':str(max_ratio),'new_coefficients':[str(q) for q in coefficient_set],'byte_gate':True,'limitations':['fixed rational coefficients','canonical contiguous field and scratch premises','no full caller or supplier tariff admission','no new kappa']}
Path(__file__).with_name('rounded-scalar-lead-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
