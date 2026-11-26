#!/usr/bin/env python3
"""Recount six-tape Toom on signed/interpolation boundaries using a separate tape model."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import random
import sys

spec = spec_from_file_location("fixed_toom", Path(__file__).with_name("word-toom.py"))
toom = module_from_spec(spec)
sys.modules[spec.name] = toom
spec.loader.exec_module(toom)


class Bank:
    def __init__(self, bits=()):
        # Index zero is physical -1. Independent array storage checks the
        # program never crosses the home delimiter, even on frame return.
        self.cells = [toom.HOME, *bits, toom.BLANK]
        self.pos = 1
        self.first = self.last = 1
        self.actions = 0
        self.neg_tags = 0

    def read(self):
        self.actions += 1
        return self.cells[self.pos]

    def put(self, value):
        self.actions += 1
        if isinstance(value, tuple):
            assert value[0] == "L" and value[1] in range(5) and value[2] in (0,1)
            self.neg_tags += int(value[2])
        elif isinstance(value,int):
            assert 0 <= value < 1 << 22
        else:
            assert value in (toom.BLANK,toom.RIGHT)
        self.cells[self.pos] = value

    def step(self, delta):
        self.actions += 1
        assert abs(delta) == 1
        self.pos += delta
        assert self.pos >= 0
        if self.pos == len(self.cells):
            self.cells.append(toom.BLANK)
        self.first, self.last = min(self.first,self.pos),max(self.last,self.pos)

    def check(self, bits=()):
        assert self.pos == 1 and self.cells[0] == toom.HOME
        expect = list(bits)
        assert self.cells[1:1+len(expect)] == expect
        assert all(value==toom.BLANK for value in self.cells[1+len(expect):])


def bits(value, width):
    return [(value >> i) & 1 for i in range(width)]


def run(w, x, y):
    f, a, b, out, ruler, temp = machines = [Bank(),Bank(bits(x,w)),Bank(bits(y,w)),Bank(),Bank(),Bank()]
    toom.multiply(*machines)
    out.check(bits(x*y,2*w))
    for bank in (f,a,b,ruler,temp):
        bank.check()
    clock = sum(bank.actions for bank in machines)
    space = sum(bank.last-bank.first+1 for bank in machines)
    if w <= 8:
        assert clock == 26*w+34
    p = max(1,w-6)
    # 3^7 < 5^5 implies log_3(5)>7/5. This rational check is stronger on
    # these finite samples than comparing with the proved real-power bound.
    assert (clock+(1<<23)*p)**5 <= (1<<24)**5*p**7
    assert space <= 256*(w+1)
    return clock,space,f.neg_tags


def main():
    rng = random.Random(20261126)
    values=[]
    for w in [1,4,7,8,9,10,11,12,13,16,19,25,40,82,83,84,110]:
        m = (w+2)//3
        lim = (1<<w)-1
        neg = ((1<<m)-1)<<m & lim
        pos = ((1<<m)-1) | (((1<<m)-1)<<(2*m)) & lim
        zero = (1 | (1<<m)) & lim
        cases = [(neg,pos),(pos,neg),(neg,neg),(zero,lim),(0,lim),(lim,lim)]
        if w>=40:
            cases = [(neg,pos),(lim,lim),(rng.randrange(lim+1),rng.randrange(lim+1))]
        for x,y in cases:
            values.append(run(w,x,y))
    assert sum(n for _,_,n in values)>0
    print(json.dumps({"cases":len(values),"max_steps":max(t for t,_,_ in values),
                      "max_cells":max(v for _,v,_ in values),
                      "negative_parent_reply_tags":sum(n for _,_,n in values)},sort_keys=True))


if __name__ == "__main__":
    main()
