#!/usr/bin/env python3
"""External binary/ternary address-range adapter with a fixed transition table."""
from itertools import product
from pathlib import Path
import argparse
import json
import random
import runpy

node = runpy.run_path(str(Path(__file__).with_name("node-tapes.py")))
Builder, Action = node["Builder"], node["Action"]
BLANK, MARK, HOME = node["BLANK"], node["MARK"], node["HOME"]
recount = runpy.run_path(str(Path(__file__).with_name("recount-node.py")))
execute = recount["execute"]


def increment(b, nxt):
    """Increment the LSB-first native-width counter; blank is the initial zero."""
    carry = b.label("increment width")
    done = Action(b.rewind("el", nxt), (("el", "1"),))
    return b.sel(carry, "el", {BLANK: done, "0": done,
                               "1": Action(carry, (("el", "0"),), (("el", 1),))})


def export_width(b, nxt):
    end = b.rewind("E", nxt)
    emit = b.label("export native width")
    give = Action(emit, (("el", BLANK), ("E", ("copy", "el"))),
                  (("el", -1), ("E", 1)))
    b.sel(emit,"el",{"0":give, "1":give,
                     HOME:Action(end, moves=(("el", 1),))})
    seek = b.label("seek width high bit")
    right = Action(seek, moves=(("el", 1),))
    b.sel(seek,"el",{"0":right, "1":right,
                     BLANK:Action(emit, moves=(("el", -1),))})
    return b.sel(b.label("zero or positive width"), "el",
                 {BLANK: Action(nxt, (("E", "0"),)), "0":right, "1":right})


def build_range(inverse=False):
    b = Builder()
    tapes = ("A","Y","U","G","S","E","u","g","s","n","ny","t","r","tmp","el")
    finish = node["shared_clean"](b,tapes,("u","g","s","n","ny","t","r"),("A","Y"))
    top = b.label("next external prefix")

    def copy_block(nxt):
        return node["plain_copy"](b,"s","A","Y",nxt)

    def padding_block(nxt):
        if inverse:
            return b.run("s",nxt,moves=(("A",1),))
        return b.run("s",nxt,writes=(("Y","0"),),moves=(("Y",1),))

    def padded_x(nxt):
        return b.unary_loop("g",lambda n:b.unary_loop("t",padding_block,n),nxt)

    def genuine_x(nxt):
        def gap(n):
            return b.unary_loop("ny",copy_block,b.unary_loop("r",padding_block,n))
        return b.unary_loop("g",gap,nxt)

    outer = b.unary_loop("n",genuine_x,b.unary_loop("r",padded_x,top))
    b.sel(top,"A",{BLANK:Action(finish)},Action(outer))
    width_to_user = export_width(b,top)
    copy_n = b.transfer("n","ny",b.reset_group(("n","ny"),width_to_user),keep=True)
    tail = b.transfer("t","r",b.reset_group(("n","t","r"),copy_n),keep=True)

    compare_n = b.label("test binary extent")
    compare_t = b.label("test ternary extent")
    grow = b.reset_group(("n","t"),
                         b.scale_unary("t","tmp",3,0,increment(b,compare_n)))
    b.sel(compare_n,"n",{BLANK:Action(tail),MARK:Action(compare_t)})
    b.sel(compare_t,"t",{BLANK:Action(grow),
                         MARK:Action(compare_n,moves=(("n",1),("t",1)))})
    doubles = b.unary_loop("u",lambda nxt:b.scale_unary("n","tmp",2,0,nxt),compare_n)
    start = b.op(doubles,writes=(("n",MARK),("t",MARK)))
    for desc,work in reversed((("U","u"),("G","g"),("S","s"))):
        start = b.unary_from_binary(desc,work,"tmp",start)
    return b,tapes,node["boundaries"](b,tapes,start,close=False)


def values(u):
    n,t,e = 1 << u,1,0
    while t < n:
        t *= 3
        e += 1
    return n,t,e


def exact(p,g,s,u):
    n,t,e = values(u)
    r = t-n
    v,w = p*g*s*n*n,p*g*s*t*t
    def numeral(z):
        return 11*z - 6*z.bit_count() + 12*max(1,z.bit_length()) + 3
    start = 4 + sum(map(numeral,(u,g,s))) + 1
    binary_rows = 11*(n-1)+10*u+(3*u+3)
    ternary_search = 10*(t-1) + 21*e - 2*e.bit_count() + n+3*t+8
    duplicate_n = 3*n+5
    export = 1 if e == 0 else 3*e.bit_length()+4
    loop = p*(g*t*t*(2*s+6)+g*(6*t+3*n)+6*t+7)+1
    finish = v+w+4 + 2*(u+g+s+2*n+t+r)+21
    clock = start+binary_rows+ternary_search+duplicate_n+export+loop+finish
    return clock,v,w,e


def exact_space(p,g,s,u):
    n,t,e = values(u)
    v,w = p*g*s*n*n,p*g*s*t*t
    return (v+w+max(1,u.bit_length())+g.bit_length()+s.bit_length()+2*e.bit_length()
            +u+g+s+n+2*t+max(g,s,t)+30)


def expected(word,p,g,s,u,inverse):
    n,t,_ = values(u)
    out = []
    for outer,x,gap,y in product(range(p),range(t),range(g),range(t)):
        genuine = x<n and y<n
        if genuine:
            side = t if inverse else n
            i = ((outer*side+x)*g+gap)*side*s + y*s
            out.append(word[i:i+s])
        elif not inverse:
            out.append("0"*s)
    return "".join(out)


def trials(extended):
    rng=random.Random(83008)
    machines={inv:build_range(inv) for inv in (False,True)}
    direct=node["build_direct"]()
    cases = compositions = total = converted = padded_cells = 0
    fixtures = [(p,g,s,u) for p,g,s,u in product((1,2),(1,2),(1,2),(0,1,2,3))]
    if extended:
        fixtures.extend(((1,1,1,4),(1,2,2,4),(1,1,1,5),(1,1,1,6)))
    for p,g,s,u in fixtures:
        clock,v,w,e=exact(p,g,s,u)
        assert clock <= 152*v
        for inv in (False,True):
            length = w if inv else v
            words = (map("".join,product("01",repeat=length)) if length<=4
                     else ("".join(rng.choices("01",k=length)),
                           "".join("01"[i%2] for i in range(length))))
            for word in words:
                fields = {k:bin(z)[2:] for k,z in zip(("U","G","S"),(u,g,s))}
                inp={"A":word,**fields}
                final,visited = execute(machines[inv],inp,clock)
                assert final=={**inp,"Y":expected(word,p,g,s,u,inv),"E":bin(e)[2:]}
                assert visited == exact_space(p,g,s,u) <= 41*v
                cases += 1
                total += clock
                converted += length
                padded_cells = max(padded_cells,w)
            if inv:
                continue
            if u<=3:
                a="".join(rng.choices("01",k=v))
                left,_=execute(machines[False],{"A":a,**fields},clock)
                middle={"A":left["Y"],"G":fields["G"],"S":fields["S"],"E":left["E"]}
                midclock=recount["direct_clock"](p,e,g,s)
                native,_=execute(direct,middle,midclock)
                last,_=execute(machines[True],{"A":native["A"],**fields},clock)
                target="".join(a[((o*(1<<u)+y)*g*(1<<u)+z*(1<<u)+x)*s:
                                  ((o*(1<<u)+y)*g*(1<<u)+z*(1<<u)+x+1)*s]
                               for o,x,z,y in product(range(p),range(1<<u),range(g),range(1<<u)))
                assert last["Y"]==target
                total += 2*clock+midclock
                compositions += 1
    return {"adapter_cases":cases,"complete_binary_swaps":compositions,"input_bits":converted,
            "largest_padded_volume":padded_cells,"checked_transitions":total,
            "table_states":{str(inv):len(machines[inv][0].rules) for inv in machines}}


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--extended",action="store_true")
    print(json.dumps(trials(ap.parse_args().extended),sort_keys=True))
