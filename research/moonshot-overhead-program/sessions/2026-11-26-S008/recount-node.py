#!/usr/bin/env python3
"""Independent interpreter, coordinate oracle and transition invoices for node-tapes."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import json
import random
import sys

spec = spec_from_file_location("fixed_node", Path(__file__).with_name("node-tapes.py"))
node = module_from_spec(spec)
sys.modules[spec.name] = node
spec.loader.exec_module(node)


def execute(compiled, initial, exact_clock):
    """Interpret the fixed table. Cells are arrays with one guard slot at -1."""
    table, labels, pc = compiled
    index = {label: t for t, label in enumerate(labels)}
    data = [[node.BLANK] + list(initial.get(label, "")) + [node.BLANK] for label in labels]
    heads = [1] * len(labels)
    low, high = heads.copy(), heads.copy()
    for _ in range(exact_clock):
        assert pc != node.HALT, "halted before the independently derived clock"
        state = table.rules[pc]
        def read(label):
            tape = index[label]
            return data[tape][heads[tape]]
        action = state.default
        if state.tape is not None:
            action = state.cases.get(read(state.tape), action)
        assert action is not None
        new = []
        for name, expr in action.writes:
            if isinstance(expr, str):
                sym = expr
            elif expr[0] == "copy":
                sym = read(expr[1])
            else:
                assert expr[0] == "xor"
                x, y = read(expr[1]), read(expr[2])
                assert x in "01" and y in "01"
                sym = "0" if x == y else "1"
            t = index[name]
            new.append((t, heads[t], sym))
        for t, head, sym in new:
            data[t][head] = sym
        for name, delta in action.moves:
            t = index[name]
            assert abs(delta) == 1
            heads[t] += delta
            assert heads[t] >= 0, "bank crossed its -1 boundary"
            if heads[t] == len(data[t]):
                data[t].append(node.BLANK)
            low[t], high[t] = min(low[t], heads[t]), max(high[t], heads[t])
        pc = action.target
    assert pc == node.HALT, "clock omitted an actual transition"
    assert heads == [1] * len(labels)
    final = {}
    for name, cells in zip(labels, data):
        assert cells[0] == node.BLANK
        live = "".join(cells[1:]).rstrip(node.BLANK)
        assert node.BLANK not in live
        if live:
            final[name] = live
    return final, sum(b - a + 1 for a, b in zip(low, high))


def binary(x):
    return format(x, "b")


def expand(x):
    return 11*x - 6*x.bit_count() + 12*len(binary(x)) + 3


def direct_clock(p, e, g, s):
    if e == 0:
        return 5
    v = p*g*s*9**e
    top_gap = 3**(e-1)*g
    setup = 4 + sum(map(expand, (e, g, s)))
    grows = sum(16*3**j*(g+s)+22 for j in range(e-1)) + 1 + (e+2)
    passes = sum(8*v + 72*(p*3**j)*top_gap + 20*p*3**j + 42 + 2 for j in range(e))
    divides = sum(10*s*3**(e-2-j)+10 for j in range(e-1))
    clean = e+2 + 2*(e+s+top_gap)+9 + 2
    return setup + grows + passes + divides + clean


def role_clock(p, j, k, i, d, s):
    setup = sum(map(expand, (j, k, i, d, s)))
    return setup + p*(s*(3*(j+k)-2) + 6*(j+k)+4) + 7*(j+k)+2*s+38


def permute(word, p, e, g, s):
    w = 3**e
    def start(t, x, z, y):
        return (((t*w + x)*g+z)*w+y)*s
    return "".join(word[start(t,x,z,y):start(t,x,z,y)+s]
                   for t, y, z, x in product(range(p),range(w),range(g),range(w)))


def role_answer(a, y, p, j, k, i, d, s, xor):
    result = list(y)
    for outer, pos in product(range(p),range(s)):
        src = a[(outer*j+i)*s+pos]
        dest = (outer*k+d)*s+pos
        result[dest] = str(int(src) ^ int(y[dest])) if xor else src
    return "".join(result)


def main():
    rng = random.Random(8102)
    def word(n):
        return "".join(rng.choice("01") for _ in range(n))
    direct = node.build_direct()
    roles = {mode: node.build_role(xor=mode) for mode in (False, True)}
    stats = {"direct_cases":0,"role_cases":0,"direct_max_steps":0,"role_max_steps":0}
    for p, e, g, s in [(1,0,1,1),(3,0,2,5),(1,1,1,1),(2,1,2,3),
                        (1,2,1,1),(3,2,2,1),(1,3,1,1),(2,3,2,3)]:
        v = p*9**e*g*s
        values = ("".join(x) for x in product("01",repeat=v)) if v <= 9 else (
            "0"*v, "1"*v, word(v), word(v))
        for a in values:
            initial = {"A":a,"E":binary(e),"G":binary(g),"S":binary(s)}
            t = direct_clock(p,e,g,s)
            final, cells = execute(direct, initial, t)
            assert final == dict(initial,A=permute(a,p,e,g,s))
            assert t <= 128*(e+1)*v and cells <= 51*v
            stats["direct_cases"] += 1
            stats["direct_max_steps"] = max(stats["direct_max_steps"],t)
    for p, j, k, s in product((1,3),(1,2,4),(1,3,5),(1,4)):
        for i,d,mode in product(range(j),range(k),(False,True)):
            a, y = word(p*j*s),word(p*k*s)
            initial = {"A":a,"Y":y,"J":binary(j),"K":binary(k),
                       "I":binary(i),"D":binary(d),"S":binary(s)}
            t = role_clock(p,j,k,i,d,s)
            final, cells = execute(roles[mode],initial,t)
            assert final == dict(initial,Y=role_answer(a,y,p,j,k,i,d,s,mode))
            w = p*s*(j+k)
            assert t <= 103*w and cells <= 30*w
            stats["role_cases"] += 1
            stats["role_max_steps"] = max(stats["role_max_steps"],t)
    print(json.dumps(stats,sort_keys=True))


if __name__ == "__main__":
    main()
