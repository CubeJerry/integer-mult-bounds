"""Canonical-pattern padding controls; arbitrary callee semantics stay explicit."""
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


p=load("pattern_padding")
f=load("fixture_tools")


def case(c,rows,stock,pattern,payload=None):
    j=len(pattern)
    payload=payload if payload is not None else "".join(str((i^(i//5))&1) for i in range(c*rows*j))
    ports=f.ports(p.TAPES,shifted=True)
    ports[p.source.SOURCE].load(payload)
    for port,value in ((p.source.PD,c),(p.source.RD,rows),(p.source.SD,stock),(p.source.BD,j)):
        ports[port].load(f.binary(value))
    ports[p.ZERO_ROW].load(pattern)
    m=p.Machine(ports)
    p.source.need(m.run()=="call","root callee boundary")
    padded_rows=((rows+stock-1)//stock)*stock
    expected="".join(payload[cursor*rows*j:(cursor+1)*rows*j]+pattern*(padded_rows-rows)
                     for cursor in range(c))
    p.source.need(ports[p.source.PAD].word()==expected,"whole canonical zero rows")
    p.source.need(ports[p.source.ROWS].word()==f.binary(padded_rows),"encoded padded count")
    ports[p.source.RETURN].load(expected)  # declared identity callee, outside machine
    p.source.need(m.run()=="done","completed restriction")
    p.source.need(ports[p.source.OUTPUT].word()==payload,"genuine complete rows")
    p.source.need(ports[p.ZERO_ROW].word()==pattern,"borrowed pattern preserved")
    p.source.need(all(t.head==t.marker+1 for t in ports),"pad all origins")
    owned=(p.source.P,p.source.R,p.source.S,p.source.B,p.source.D,p.source.TEMP,
           p.source.ROWS,p.source.PAD,p.source.RETURN)
    p.source.need(all(not ports[t].word() for t in owned),"pad owned erase")
    volume=len(payload)
    p.source.need(m.steps<=4096*volume+4096,"conservative full pad invoice")
    return m.steps


def rejects(callback):
    try:callback()
    except ValueError:return
    raise ValueError("negative padding control accepted")


def mutation_raw_zero():
    ports=f.ports(p.TAPES)
    rows,stock,pattern=5,3,"000010000010"
    ports[p.source.SOURCE].load("0"*(rows*len(pattern)))
    for port,value in ((p.source.PD,1),(p.source.RD,rows),(p.source.SD,stock),(p.source.BD,len(pattern))):
        ports[port].load(f.binary(value))
    ports[p.ZERO_ROW].load(pattern)
    m=p.Machine(ports)
    p.source.need(m.run()=="call","mutant call")
    # Wrong all-zero byte suffix has right length but malformed component codes.
    ports[p.source.RETURN].load("0"*(6*len(pattern)))
    m.run()


def check():
    cases=0
    maximum=0
    for c in (1,2,3):
        for rows in (1,2,3,5,7,8,15,16,17):
            for stock in (1,2,3,5):
                if stock>rows:continue
                for pattern in ("0","1","010","000010000010"):
                    maximum=max(maximum,case(c,rows,stock,pattern))
                    cases+=1
    rejects(lambda:case(1,2,3,"010"))
    rejects(mutation_raw_zero)
    return {"cases":cases,"maximum_steps":maximum,"rejections":["stock_exceeds_rows","literal_zero_bytes_replace_numeric_zero"]}


def main():
    print(check())
    print("PASS_CANONICAL_PATTERN_PADDING")


if __name__=="__main__":main()
