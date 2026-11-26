#!/usr/bin/env python3
"""Export actual pre-input transition tables to original-source Lean interpreters."""

from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json
import random
import runpy

HERE = Path(__file__).resolve().parent
NODE = runpy.run_path(str(HERE / "node-tapes.py"))
RECOUNT = runpy.run_path(str(HERE / "recount-node.py"))
SCHOOL = runpy.run_path(str(HERE / "schoolbook.py"))
RANGE = runpy.run_path(str(HERE / "address-range.py"))
GLYPHS = {".": ".blank", "0": "(.bit false)", "1": "(.bit true)", "^": ".left",
          "*": ".parkLeft", "@": ".parkInside", "$": ".right", "|": ".bottom",
          "u": "(.marked false)", "v": "(.marked true)"}


def array(args):
    return "#[" + ",".join(args) + "]"


def lean_list(args):
    return "[" + ",".join(args) + "]"


def quote(word):
    assert set(word) <= GLYPHS.keys()
    return json.dumps(word)


def program(name, machine):
    builder, tapes, entry = machine
    rows = builder.rules
    n = len(rows)
    assert len(tapes) == len(set(tapes)) and 0 <= entry < n
    ix = {t: i for i, t in enumerate(tapes)}

    def action(a):
        assert a.target == NODE["HALT"] or 0 <= a.target < n
        assert len(dict(a.writes)) == len(a.writes)
        assert len(dict(a.moves)) == len(a.moves)
        target = n if a.target == NODE["HALT"] else a.target
        writes = []
        for t, expr in a.writes:
            if isinstance(expr, str):
                value = ".literal " + GLYPHS[expr]
            elif len(expr) == 2 and expr[0] == "copy":
                value = f".copy {ix[expr[1]]}"
            else:
                assert len(expr) == 3 and expr[0] == "xor"
                value = f".bx {ix[expr[1]]} {ix[expr[2]]}"
            writes.append(f"({ix[t]},{value})")
        moves = []
        for t, delta in a.moves:
            assert delta in (-1, 1)
            moves.append(f"({ix[t]},{'.right' if delta == 1 else '.left'})")
        return "⟨" + ",".join([str(target), lean_list(writes), lean_list(moves)]) + "⟩"

    literals = []
    for r in rows:
        assert r.tape is not None or not r.cases
        probe = "none" if r.tape is None else f"some {ix[r.tape]}"
        cases = lean_list(f"({GLYPHS[c]},{action(a)})" for c, a in r.cases.items())
        otherwise = "none" if r.default is None else "some " + action(r.default)
        literals.append("⟨" + ",".join([probe, cases, otherwise]) + "⟩")
    k = len(tapes)
    decl = f"def {name} : Table {k} {n} := ⟨#[\n  " + ",\n  ".join(literals) + "], rfl⟩"
    return decl, (k, n, sum(len(r.cases) + (r.default is not None) for r in rows))


def fixture(name, table, machine, inp, full, clock, visits, formal):
    _, tapes, entry = machine
    data = array(quote(inp.get(t, "")) for t in tapes)
    expect = array(f"({pos},{quote(pre)},{quote(post)})" for pos, pre, post in full)
    head = f"def {name}Input := decodeWords {data}"
    output = f"def {name}Output : Vector Window {len(tapes)} := decodeWindows {expect}"
    claim = f"check {table} {entry} {name}Input {clock} {visits} {name}Output"
    lines = [head, output, f"#guard {claim}"]
    if formal:
        lines.append(f"theorem {name}_verified : {claim}=true := by decide +kernel")
        conclusion = f"""∃ c : TM.Config Letter (Fin ({len(machine[0].rules)}+1)) (Fin {len(tapes)}),
    Trace (TM.advance (rule {table})) (physical (initial {entry} {name}Input)) {clock} c ∧
    TM.advance (rule {table}) c=none ∧
    VisitsAtMost (rule {table}) (physical (initial {entry} {name}Input)) {clock} {visits} ∧
    ∀ i : Fin {len(tapes)}, c.tape i={name}Output[i].physical"""
        lines.append(f"theorem {name}_physical : {conclusion} :=\n"
                     f"  check_sound {table} {entry} {name}Input {clock} {visits} "
                     f"{name}Output {name}_verified")
    return "\n".join(lines)


def build(extras):
    programs = {"direct": NODE["build_direct"](), "copyRole": NODE["build_role"](xor=False),
                "xorRole": NODE["build_role"](xor=True), "school": SCHOOL["machine"]()}
    if extras:
        for label, method in (("pack", "build_pack"), ("pad", "build_padding"),
                              ("tag", "build_tag")):
            for inv in (False, True):
                programs[label + ("Back" if inv else "Fwd")] = NODE[method](inverse=inv)
        for inv in (False,True):
            programs["range" + ("Back" if inv else "Fwd")] = RANGE["build_range"](inv)
    declared, stats, proofs = [], {}, []
    for label, prog in programs.items():
        decl, dims = program(label, prog)
        declared.append(decl)
        stats[label] = dict(zip(("tapes", "states", "alternatives"), dims))
    rng = random.Random(2837124)

    def bits(n):
        return "".join(rng.choice("01") for _ in range(n))

    def params(**ks):
        return {key: format(x, "b") for key, x in ks.items()}

    def raw(case, label, inp, expected, clock, formal=False):
        machine = programs[label]
        answer, cells = RECOUNT["execute"](machine, inp, clock)
        assert answer == dict(inp, **expected)
        full = [(0, "", answer.get(t, "")) for t in machine[1]]
        proofs.append(fixture(case, label, machine, inp, full, clock, cells, formal))

    for ordinal, (p, e, g, s) in enumerate([(1, 0, 1, 1), (1, 1, 1, 1),
                                             (2, 1, 2, 2), (1, 2, 1, 1)]):
        a = bits(p * 9**e * g * s)
        raw(f"directExample{ordinal}", "direct", dict(A=a, **params(E=e,G=g,S=s)),
            dict(A=RECOUNT["permute"](a, p, e, g, s)), RECOUNT["direct_clock"](p,e,g,s),
            formal=ordinal == 0)
    for label, xor in (("copyRole", False), ("xorRole", True)):
        for ordinal, (p, j, k, i, d, s) in enumerate([(1,1,1,0,0,1),(2,3,4,2,1,2)]):
            a, y = bits(p*j*s), bits(p*k*s)
            raw(label + "Example" + str(ordinal), label,
                dict(A=a,Y=y,**params(J=j,K=k,I=i,D=d,S=s)),
                dict(Y=RECOUNT["role_answer"](a,y,p,j,k,i,d,s,xor)),
                RECOUNT["role_clock"](p,j,k,i,d,s))
    for ordinal, (n, x, y) in enumerate([(1,0,0),(1,1,1),(3,7,5),(5,23,25)]):
        machine = programs["school"]
        inp = dict(I=f"{x:0{n}b}|{y:0{n}b}")
        sim = NODE["Simulation"](machine, inp).execute(64*(n+1)**2)
        assert sim.tape["I"] == dict(enumerate(inp["I"]))
        assert sim.tape["O"] == dict(enumerate(f"{x*y:0{2*n}b}"))
        full = []
        for t in machine[1]:
            current = sim.head[t]
            left = min([current, *sim.tape[t]])
            right = max([current-1, *sim.tape[t]])
            pre = "".join(sim.tape[t].get(pos, ".") for pos in range(current-1, left-1, -1))
            post = "".join(sim.tape[t].get(pos, ".") for pos in range(current, right+1))
            full.append((current, pre, post))
        proofs.append(fixture("schoolExample" + str(ordinal), "school", machine, inp,
                              full, sim.steps, sim.visited, False))
    if extras:
        for label in list(programs)[4:]:
            forward = label.endswith("Fwd")
            if label.startswith("range"):
                for ordinal, (p,g,s,u) in enumerate([(1,1,1,0),(2,2,2,2)]):
                    clock, v, w, e = RANGE["exact"](p,g,s,u)
                    word = bits(v if forward else w)
                    inp = dict(A=word,**params(U=u,G=g,S=s))
                    out = dict(Y=RANGE["expected"](word,p,g,s,u,not forward),E=format(e,"b"))
                    _, visits = RECOUNT["execute"](programs[label],inp,clock)
                    assert visits == RANGE["exact_space"](p,g,s,u)
                    raw(label + "Example" + str(ordinal),label,inp,out,clock)
                continue
            if label.startswith("pack"):
                p,k,t=2,2,3
                h=2**k
                a=bits(p*h*t)
                dims=(p,t,h) if forward else (p,h,t)
                def index(row,i,j):
                    return (row*h+j)*t+i if forward else (row*t+j)*h+i
                z="".join(a[index(*xyz)] for xyz in product(*(range(d) for d in dims)))
                inp, out = dict(A=a,**params(K=k,T=t)), dict(A=z)
            elif label.startswith("pad"):
                p,w,u=2,4,2
                b=9
                c=12
                a=bits(p*(b if forward else c)*u)
                z="".join(a[j*b*u:(j+1)*b*u]+"0"*((c-b)*u) for j in range(p)) if forward else (
                  "".join(a[j*c*u:(j*c+b)*u] for j in range(p)))
                inp, out = dict(A=a,**params(W=w,U=u)), dict(Y=z)
            else:
                p,t,g,s,h=1,3,1,2,2
                a=bits(p*t*t*g*s*h)
                outbits=[]
                for row in range(p*t*t*g*s):
                    x,y=(row//(g*t*s))%t,(row//s)%t
                    value=(1 if x<y else 2 if x>y else 0)
                    outbits.append(a[row*h:(row+1)*h]+format(value if forward else -value%3,"02b"))
                inp, out = dict(A=a,**params(T=t,G=g,S=s,H=h)), dict(Y="".join(outbits))
            run = NODE["Simulation"](programs[label],inp).execute(10**6)
            raw(label+"Example",label,inp,out,run.steps)
    return declared, proofs, stats


PREAMBLE = """import NodeBridge

namespace S008.NodeTables

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter Window)
open S008.NodeSource

set_option maxRecDepth 20000
set_option maxHeartbeats 10000000

def decode (s : String) : List Letter := s.toList.map (fun c =>
  match c with
  | '0' => .bit false | '1' => .bit true | '^' => .left | '*' => .parkLeft
  | '@' => .parkInside | '$' => .right | '|' => .bottom | 'u' => .marked false | 'v' => .marked true | _ => .blank)

def decodeWords (ws : Array String) := ws.map decode

def decodeWindows {k : ℕ} (ws : Array (ℤ × String × String)) : Vector Window k :=
  Vector.ofFn (fun i => let (p,a,b) := (ws[i.val]?).getD (0,"",""); ⟨p,decode a,decode b⟩)
"""


def main():
    ap = ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("--extras", action="store_true", help="include native and external record maps")
    ap.add_argument("--split", action="store_true", help="emit separate small pre-input table modules")
    args = ap.parse_args()
    tables, checks, stats = build(args.extras)
    end = "end S008.NodeTables\n"
    if args.split:
        base = args.output.stem
        support = base + "Support"
        args.output.with_name(support + ".lean").write_text(PREAMBLE + "\n" + end)
        scopes = PREAMBLE[PREAMBLE.index("namespace S008.NodeTables"):PREAMBLE.index("def decode")]
        members = []
        for i, code in enumerate(tables):
            mod = base + "Rule" + str(i).zfill(2)
            args.output.with_name(mod + ".lean").write_text("\n\n".join(
                [f"import {support}", scopes, code, end]))
            members.append(mod)
        args.output.write_text("\n\n".join([*(f"import {mod}" for mod in members),scopes,*checks,end]))
    else:
        args.output.write_text("\n\n".join([PREAMBLE, *tables, *checks, end]))
    print(json.dumps({"programs": stats, "fixtures": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()
