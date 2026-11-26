"""Test physical fixed-rule routines against independent address oracles."""
import itertools
import json
from pathlib import Path
import random
import runpy
TM=runpy.run_path(str(Path(__file__).with_name("node-tapes.py")))
counts={}
rng=random.Random(3471129)

def bits(n):
    return "".join(rng.choice("01") for _ in range(n))

def run(name, machine, inp, expected, bill, space):
    sim=TM["Simulation"](machine,inp).execute(bill)
    assert sim.visited<=space and all(pos==0 for pos in sim.head.values())
    for t in sim.tapes:
        assert sim.contents(t)==expected.get(t,inp.get(t,"")),(name,t)
    row=counts.setdefault(name,{"cases":0,"max_steps":0,"max_visited":0,
                             "states":len(machine[0].rules),"tapes":len(machine[1])})
    row["cases"]+=1
    row["max_steps"]=max(sim.steps,row["max_steps"])
    row["max_visited"]=max(sim.visited,row["max_visited"])

def binary(**kwargs):
    return {t:format(n,"b") for t,n in kwargs.items()}

def test_pack():
    for inv in (False,True):
        machine=TM["build_pack"](inverse=inv)
        for p,k,t in itertools.product((1,3),(0,1,2,3),(1,3,4,7)):
            h=2**k; v=p*h*t; a=bits(v)
            index=(lambda row,j,y: (row*t+y)*h+j) if inv else (lambda row,y,j: (row*h+j)*t+y)
            dims=(p,h,t) if inv else (p,t,h)
            z="".join(a[index(*xyz)] for xyz in itertools.product(*(range(d) for d in dims)))
            run("unpack" if inv else "pack",machine,{"A":a,**binary(K=k,T=t)},
                {"A":z},128*(k+1)*v,27*v)

def test_pad():
    for inv in (False,True):
        machine=TM["build_padding"](inverse=inv)
        for p,w,u in itertools.product((1,3),(1,2,3,4,5,8,9,10,17,27,28),(1,3)):
            b=1
            while b<w:
                b*=3
            c=(b+w-1)//w*w
            if inv:
                a=bits(p*c*u); z="".join(a[j*c*u:(j*c+b)*u] for j in range(p))
            else:
                a=bits(p*b*u); z="".join(a[j*b*u:(j+1)*b*u]+"0"*((c-b)*u) for j in range(p))
            v=len(a)+len(z)
            run("unpad" if inv else "pad",machine,{"A":a,**binary(W=w,U=u)},
                {"Y":z},256*v,27*v)

def test_tag():
    for inv in (False,True):
        machine=TM["build_tag"](inverse=inv)
        for p,t,g,s,h in [(1,1,1,1,1),(1,3,3,1,2),(2,3,2,3,4),(1,9,2,2,5),
                           (2,1,4,2,7),(2,5,1,2,2)]:
            q=p*t*t*g*s; v=q*h; a=bits(v); o=[]
            for row in range(q):
                x=(row//(g*t*s))%t; y=(row//s)%t
                trit=1 if x<y else 2 if x>y else 0
                o.append(a[row*h:(row+1)*h]+format((-trit)%3 if inv else trit,"02b"))
            inp={**binary(T=t,G=g,S=s,H=h),"A":a}
            run("tag_inverse" if inv else "tag",machine,inp,{"Y":"".join(o)},512*v,44*v)

if __name__=="__main__":
    test_pack()
    test_pad()
    test_tag()
    print(json.dumps(counts,indent=2,sort_keys=True))
