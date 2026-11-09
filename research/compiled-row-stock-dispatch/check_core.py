"""Smoke/exhaustive row-interface checks; source-aware suite is verify.py."""
from pathlib import Path
import importlib.util
import sys


def load(name):
    path=Path(__file__).resolve().parent/(name+".py")
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


r=load("row_programs")
f=load("fixture_tools")


def check_one(g, c, q, j, shifted=False):
    pp=f.ports(r.FIRST_ROLE+g,shifted=shifted)
    parent=f.values(r.SCHEMA,outer=c,rows=g*q,stock=g,row_bits=j)
    header=f.encode_header(r.SCHEMA,parent)
    pp[r.HEADER].load(header)
    steps_p=r.run(r.compile_prepare(g),pp)
    child=f.decode_header(r.SCHEMA,pp[r.CHILD_HEADER].word())
    expected=dict(parent,rows=q,stock=1)
    r.need(child==expected,"exact child header")
    r.need(pp[r.HEADER].word()==header,"parent header retained")
    text="".join(str(((i*17)^(i//3)^(i//7))&1) for i in range(c*g*q*j))
    pp[r.HEADER].load(pp[r.CHILD_HEADER].word())
    pp[r.CHILD_HEADER].load("")
    pp[r.SOURCE].load(text)
    steps_s=r.run(r.compile_router(g),pp)
    rows=[text[i:i+j] for i in range(0,len(text),j)]
    for w in range(g):
        r.need(pp[r.FIRST_ROLE+w].word()=="".join(rows[w::g]),"whole row role order")
    steps_m=r.run(r.compile_router(g,True),pp)
    r.need(pp[r.OUTPUT].word()==text,"literal whole row inverse")
    r.need(pp[r.SOURCE].word()==text,"borrowed source preserved")
    r.need(all(t.head==t.marker+1 for t in pp),"all local origins")
    keep={r.SOURCE,r.OUTPUT,r.HEADER}
    r.need(all(not t.word() for i,t in enumerate(pp) if i not in keep),"owned scratch/roles erased")
    return steps_p,steps_s,steps_m


def check():
    cases=0
    maxima=[0,0,0]
    for g in (1,2,3,5):
        for c in (1,2):
            for q in (1,2,3,7):
                for j in (1,2,3,7,16):
                    result=check_one(g,c,q,j,cases%2==1)
                    maxima=[max(a,b) for a,b in zip(maxima,result)]
                    cases+=1
    return {"cases":cases,"maximum_steps":maxima}


def main():
    print(check())
    print("PASS_LITERAL_ROW_CORE")


if __name__=="__main__":main()
