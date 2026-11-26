#!/usr/bin/env python3
"""Independent clocks and semantic compositions for the compiled S008 tag program."""
from itertools import product
from math import prod
from pathlib import Path
import json
import random
import runpy

checked = runpy.run_path(str(Path(__file__).with_name("recount-node.py")))
run_table = checked["execute"]
build = checked["node"].build_tag


def shape_clock(p, t, g, s, h):
    q = p*t*t*g*s
    dims = (t, g, s, h)
    conversions = sum(11*n - 6*n.bit_count() + 12*n.bit_length()+3 for n in dims)
    total = (conversions + q*(4*h+10)
             + p*(6*g*t*t+6*g*t+t*t+8*t+2) + 2*sum(dims)+22)
    cells = q*(2*h+2) + sum(n.bit_length()+n for n in dims) + max(dims)+22
    return total, cells


def apply(prog, old, p, t, g, s, h, sign, spare=""):
    assert len(old) == p*t*t*g*s*h
    clock, expected_cells = shape_clock(p,t,g,s,h)
    dims = dict(zip(("T", "G", "S", "H"), (t,g,s,h)))
    start = {name: format(n, "b") for name,n in dims.items()}
    start["A"] = old
    if spare:
        start["Y"] = spare
    final, cells = run_table(prog, start, clock)
    answer = []
    for i in range(len(old)//h):
        y, x = (i//s)%t, (i//(s*t*g))%t
        trit = sign*((x < y) - (x > y))
        answer.append(old[i*h:(i+1)*h] + format(trit%3, "02b"))
    out = "".join(answer)
    assert final == {**start, "Y":out} and cells == expected_cells
    assert clock <= 147*len(old) and cells <= 35*len(old)
    return out, clock


def main():
    rng = random.Random(80325)
    both = {sgn: build(inverse=(sgn<0)) for sgn in (-1,1)}
    cases = clocks = joint = decoded = 0
    for p,t,g,s,h in product((1,2),(1,2,3),(1,2),(1,3),(1,2,5)):
        vol = p*t*t*g*s*h
        words = (map("".join,product("01",repeat=vol)) if vol <= 4
                 else ("".join(rng.choices("01",k=vol)),))
        for raw in words:
            for sign, prog in both.items():
                _,clock = apply(prog,raw,p,t,g,s,h,sign)
                clocks += clock
                cases += 1

    # The indicated axes have paired equal extents. Real occupied dimensions
    # between/around them stay in the stream throughout all m passes.
    fixtures = (
        ((2,3,2,3,2,3,3,2), ((1,5),(3,6)), 2),
        ((1,2,2,2,3,2,2,2,1), ((1,5),(2,6),(3,7)), 4),
        ((1,1,1,1,1,1,3), ((1,3),(2,4)), 3),
    )
    for dims, axes, b in fixtures:
        q = prod(dims)
        raw = "".join(rng.choices("01",k=b*q))
        counters = list(product(*(range(d) for d in dims)))
        for signs in product((-1,1),repeat=len(axes)):
            prior, stream = "", raw
            for i, ((a,z),sign) in enumerate(zip(axes,signs)):
                assert dims[a] == dims[z]
                p,t,g,s = prod(dims[:a]),dims[a],prod(dims[a+1:z]),prod(dims[z+1:])
                new,clock = apply(both[sign],stream,p,t,g,s,b+2*i,sign,spare=prior)
                clocks += clock
                prior,stream = stream,new
            width = b+2*len(axes)
            for i,v in enumerate(counters):
                row = stream[i*width:(i+1)*width]
                assert row[:b] == raw[i*b:(i+1)*b]
                key = [2*int(row[b+2*j])+int(row[b+2*j+1]) for j in range(len(axes))]
                model = [(sign*((v[a]<v[z])-(v[a]>v[z])))%3 for (a,z),sign in zip(axes,signs)]
                assert key == model
                for beta in product(range(3),repeat=len(axes)):
                    assert sum((key[j]+beta[j])%3 for j in range(len(key))) == sum(
                        ((sign*((v[a]<v[z])-(v[a]>v[z])))+shift)%3
                        for (a,z),sign,shift in zip(axes, signs, beta))
                decoded += 1
            joint += 1
    print(json.dumps({"single_cases":cases,"signed_compositions":joint,
                      "full_keys_checked":decoded,"tag_transitions":clocks},sort_keys=True))


if __name__ == "__main__":
    main()
