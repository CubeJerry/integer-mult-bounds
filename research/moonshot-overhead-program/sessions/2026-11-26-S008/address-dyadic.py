#!/usr/bin/env python3
"""Replay the fixed-tape dyadic address program. The driver alone indexes arrays."""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import json
import random

LEFT, RIGHT, BLANK = "[", "]", "_"
BITS = "01"
NAMES = ("A", "B", "E", "O", "Pword", "Gword", "Sword", "fword",
         "aword", "jword", "P", "G", "S", "M", "half", "cut", "tmp", "counter")


class Tape:
    def __init__(self, word: str | None):
        layout = LEFT if word is None else LEFT + word + RIGHT
        self.cells = dict(enumerate(layout))
        self.head = self.high = 0

    def scanned(self):
        return self.cells.get(self.head, BLANK)

    def write(self, char):
        if char == BLANK:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = char


class Machine:
    """Every sense or act is one transition. Only the driver inspects head indices."""

    def __init__(self, contents):
        self.t = {name: Tape(contents.get(name)) for name in NAMES}
        self.steps = 0

    def see(self, name):
        self.steps += 1
        return self.t[name].scanned()

    def act(self, moves=(), writes=(), copies=()):
        self.steps += 1
        actions = [(dst, self.t[src].scanned()) for src, dst in copies]
        for name, value in actions + list(writes):
            self.t[name].write(value)
        for name, direction in moves:
            assert direction in (-1, 1)
            tape = self.t[name]
            tape.head += direction
            assert tape.head >= 0
            tape.high = max(tape.high, tape.head)

    def advance(self, name, direction=1):
        self.act(moves=((name, direction),))

    def home(self, name):
        while self.see(name) != LEFT:
            self.advance(name, -1)

    def first(self, name):
        self.home(name)
        self.advance(name)

    def append_unit(self, name):
        self.act(moves=((name, 1),), writes=((name, "u"),))

    def counted(self, word, body):
        """Run body for the unsigned, MSB-first word; scratch counter is LSB-first."""
        c = "counter"
        while self.see(word) in BITS:
            self.advance(word)
        self.advance(word, -1)
        while self.see(word) in BITS:
            self.act(moves=((word, -1), (c, 1)), copies=((word, c),))
        self.advance(word)
        self.first(c)
        while True:
            while self.see(c) == "0":
                self.act(moves=((c, 1),), writes=((c, "1"),))
            if self.see(c) != "1":
                self.advance(c, -1)
                while self.see(c) != LEFT:
                    self.act(moves=((c, -1),), writes=((c, BLANK),))
                self.advance(c)
                return
            self.act(writes=((c, "0"),))
            self.first(c)
            body()

    def unary(self, name, body):
        while self.see(name) == "u":
            body()
            self.advance(name)
        self.first(name)

    def triple(self):
        while self.see("M") == "u":
            self.act(moves=(("M", 1), ("tmp", 1)), writes=(("M", BLANK), ("tmp", "u")))
            self.append_unit("tmp")
            self.append_unit("tmp")
        self.first("M")
        self.first("tmp")
        while self.see("tmp") == "u":
            self.act(moves=(("M", 1), ("tmp", 1)), writes=(("M", "u"), ("tmp", BLANK)))
        self.first("M")
        self.first("tmp")

    def setup(self, paired):
        for n in NAMES:
            self.advance(n)
        for n in (("P", "G", "S") if paired else ("P", "S")):
            self.counted(n+"word", lambda: self.append_unit(n))
            self.first(n)
        self.append_unit("M")
        self.first("M")
        self.counted("fword", self.triple)
        odd = True
        while self.see("M") == "u":
            if not odd:
                self.append_unit("half")
            odd = not odd
            self.advance("M")
        self.first("M")
        self.first("half")

    def block(self, src, dst, read_direction=1, erase=False):
        while self.see("S") == "u":
            self.act(moves=((src, read_direction), (dst, 1), ("S", 1)),
                     writes=((src, BLANK),) if erase else (), copies=((src, dst),))
        self.first("S")

    def append_bank(self, src, dst):
        self.first(src)
        while self.see(src) in BITS:
            self.act(moves=((src, 1), (dst, 1)), copies=((src, dst),),
                     writes=((src, BLANK),))
        self.first(src)

    def begin_cut(self, positive):
        first = True
        while self.see("M") == "u":
            self.act(moves=(("M", 1), ("cut", 1)),
                     writes=(("cut", "C" if (first and not positive) else "c"),))
            first = False
        self.act(writes=(("cut", "Z" if positive else "z"),))
        self.first("M")
        self.first("cut")

    def shift_cut(self, positive):
        while self.see("cut") not in ("C", "Z"):
            self.advance("cut")
        was_end = self.see("cut") == "Z"
        self.act(moves=(("cut", -1 if positive else 1),),
                 writes=(("cut", "z" if was_end else "c"),))
        at_end = self.see("cut") == "z"
        self.act(writes=(("cut", "Z" if at_end else "C"),))
        self.first("cut")

    def erase_from_first(self, name):
        while self.see(name) != BLANK:
            self.act(moves=((name, 1),), writes=((name, BLANK),))
        self.first(name)

    def shear_fibre(self):
        while self.see("cut") == "c":
            self.block("A", "E")
            self.advance("cut")
        while self.see("cut") in ("C", "c"):
            self.block("A", "B")
            self.advance("cut")
        self.first("cut")
        self.append_bank("E", "B")

    def double_fibre(self):
        self.block("A", "E")
        self.unary("half", lambda: self.block("A", "E"))
        self.unary("half", lambda: self.block("A", "O"))
        self.first("E")
        self.first("O")

        def pair():
            self.block("E", "B", erase=True)
            self.block("O", "B", erase=True)

        self.unary("half", pair)
        self.block("E", "B", erase=True)
        self.first("E")
        self.first("O")

    def halve_fibre(self):
        def pair():
            self.block("A", "E")
            self.block("A", "O")

        self.unary("half", pair)
        self.block("A", "E")
        self.append_bank("E", "B")
        self.append_bank("O", "B")

    def negate_fibre(self):
        self.block("A", "B")

        def store_pair():
            self.block("A", "E")
            self.block("A", "E")

        self.unary("half", store_pair)
        self.advance("E", -1)

        def out_one():
            self.block("E", "O", read_direction=-1, erase=True)
            self.advance("O", -1)
            self.block("O", "B", read_direction=-1, erase=True)
            self.advance("O")

        def out_pair():
            out_one()
            out_one()

        self.unary("half", out_pair)
        self.advance("E")

    def commit(self):
        self.first("A")
        self.append_bank("B", "A")
        self.first("A")

    def stage(self, opcode, paired):
        if opcode in ("+", "-"):
            assert paired
            plus = opcode == "+"

            def one_p():
                self.begin_cut(plus)

                def one_x():
                    self.unary("G", self.shear_fibre)
                    self.shift_cut(plus)

                self.unary("M", one_x)
                self.erase_from_first("cut")

            self.unary("P", one_p)
        else:
            fibre = {"D": self.double_fibre, "I": self.halve_fibre,
                     "N": self.negate_fibre}[opcode]
            if paired:
                self.unary("P", lambda: self.unary("M", lambda: self.unary("G", fibre)))
            else:
                self.unary("P", fibre)
        self.commit()

    def run(self, opcode):
        self.setup(opcode in ("+", "-"))
        if opcode in ("+", "-"):
            self.counted("jword", lambda: self.stage("D", True))
            while self.see("aword") in BITS:
                self.stage("I", True)
                self.advance("aword")
            self.first("aword")
            while self.see("aword") in BITS:
                bit = self.see("aword")
                self.stage("D", True)
                if bit == "1":
                    self.stage(opcode, True)
                self.advance("aword")
            self.first("aword")
            self.counted("jword", lambda: self.stage("I", True))
        else:
            self.stage(opcode, False)
        for n in ("P", "G", "S", "M", "half"):
            self.erase_from_first(n)
        for n in NAMES:
            self.home(n)


def check_case(P, f, G, S, num, j, opcode, rng):
    M = 3**f
    positive = opcode == "+"
    paired = opcode in ("+", "-")
    V = P*G*M*M*S if paired else P*M*S
    payload = "".join(rng.choices(BITS, k=V))
    words = {"A": payload, "Pword": bin(P)[2:], "Gword": bin(G)[2:],
             "Sword": bin(S)[2:], "fword": bin(f)[2:],
             "aword": bin(num)[2:], "jword": bin(j)[2:]}
    machine = Machine(words)
    machine.run(opcode)
    oracle = ["?"]*V
    if paired:
        q = num * (1 if positive else -1) * pow(pow(2, j, M), -1, M)
        for p, x, gap, y, suffix in product(range(P), range(M), range(G), range(M), range(S)):
            i = (((p*M+x)*G+gap)*M + y)*S+suffix
            target = (y+q*x) % M
            oracle[(((p*M+x)*G+gap)*M + target)*S+suffix] = payload[i]
    else:
        scalar = {"D": 2, "I": pow(2, -1, M), "N": -1}[opcode]
        for p, y, suffix in product(range(P), range(M), range(S)):
            oracle[(p*M + scalar*y % M)*S + suffix] = payload[(p*M+y)*S+suffix]
    for n in NAMES:
        expected = "".join(oracle) if n == "A" else words.get(n)
        layout = LEFT if expected is None else LEFT + expected + RIGHT
        assert machine.t[n].cells == dict(enumerate(layout)), (n, P, f, G, S, opcode)
        assert machine.t[n].head == 0
    visited = sum(t.high+1 for t in machine.t.values())
    l = len(words["aword"])
    J = len(words["jword"])
    stages = (2*j + 2*l + num.bit_count()) if paired else 1
    time_bound = 512*(1+stages)*V + 128*(l+J+1)
    space_bound = 24*V + 4*(l+J+1) + 96
    assert machine.steps <= time_bound
    assert visited <= space_bound
    return machine.steps, visited, V, stages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended", action="store_true")
    arg = parser.parse_args()
    rng = random.Random(80321)
    totals = Counter()
    maxima = Counter()
    cases = []
    for f, p, g, s in product((0,1,2), (1,2), (1,2), (1,3)):
        for num, j in ((0,0), (1,0), (2,1), (3,2), (5,3)):
            for op in ("+", "-"):
                cases.append((p,f,g,s,num,j,op))
        for op in ("D", "I", "N"):
            cases.append((p,f,g,s,0,0,op))
    if arg.extended:
        for _ in range(75):
            cases.append((rng.randrange(1,4), rng.randrange(1,4), rng.randrange(1,4),
                          rng.randrange(1,6), rng.randrange(32), rng.randrange(5),
                          rng.choice(("+","-"))))
    for args in cases:
        steps, space, volume, stages = check_case(*args, rng)
        totals["cases"] += 1
        totals["steps"] += steps
        totals["bits"] += volume
        totals["stages"] += stages
        maxima["visited"] = max(maxima["visited"], space)
        maxima["steps"] = max(maxima["steps"], steps)
    print(json.dumps({"totals": dict(totals), "maxima": dict(maxima)}, sort_keys=True))


if __name__ == "__main__":
    main()
