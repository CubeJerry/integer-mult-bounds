#!/usr/bin/env python3
"""Produce kernel-verifiable short cuts of arbitrary-input symbolic physical runs."""

from argparse import ArgumentParser
from pathlib import Path
import json
import runpy

HERE = Path(__file__).resolve().parent
NODE = runpy.run_path(str(HERE / "node-tapes.py"))
CASES = {
    "nine": ("direct", "input9", "result9", 296, 59, (1,1,1,1)),
    "seventytwo": ("direct", "input72", "result72", 1086, 190, (2,1,2,2)),
    "eightyone": ("direct", "input81", "result81", 2521, 211, (1,2,1,1)),
    "copy": ("copyRole", "role28", "(roleOutput 2 3 4 2 1 2 false descriptors)", 490, 86, None),
    "xor": ("xorRole", "role28", "(roleOutput 2 3 4 2 1 2 true descriptors)", 490, 86, None),
}
GLYPHS = {".": "bl", "^": "homeL", "*": "markL", "0": "zero", "1": "one"}


def variable(i):
    return ("v", i)


def data(start, n):
    return tuple(variable(start+i) for i in range(n))


def observed(w):
    return w[2][0] if w[2] else "."


def move(w, sym, delta):
    pos, pre, post = w
    left_symbol = pre[0] if pre else "."
    if delta == -1:
        return pos-1, pre[1:], (left_symbol,sym)+post[1:]
    if delta == 1:
        return pos+1, (sym,)+pre, post[1:]
    return pos, pre, (sym,)+post[1:]


def symbolic_run(name, cut):
    table, _, _, clock, cells, geometry = CASES[name]
    if table == "direct":
        p,e,g,s = geometry
        inp = {"A": data(0, p*9**e*g*s), "E": tuple(f"{e:b}"),
               "G":tuple(f"{g:b}"), "S":tuple(f"{s:b}")}
        built = NODE["build_direct"]()
    else:
        inp = {"A": data(0,12), "Y": data(12,16), "J":tuple("11"), "K":tuple("100"),
               "I":tuple("10"), "D":tuple("1"), "S":tuple("10")}
        built = NODE["build_role"](xor=table=="xorRole")
    b,tapes,pc = built
    ix = {t:i for i,t in enumerate(tapes)}
    ws = tuple((0,(),inp.get(t,())) for t in tapes)
    lo = [0]*len(tapes)
    hi = lo.copy()
    saved=[]
    for step in range(1,clock+1):
        assert pc != -1
        row=b.rules[pc]
        if row.tape is None:
            action=row.default
        else:
            val=observed(ws[ix[row.tape]])
            if isinstance(val,tuple):
                assert "0" not in row.cases and "1" not in row.cases
                action=row.default
            else:
                action=row.cases.get(val,row.default)
        assert action is not None
        writes={}
        for t,op in action.writes:
            if isinstance(op,str):
                val=op
            elif op[0]=="copy":
                val=observed(ws[ix[op[1]]])
            else:
                assert op[0]=="xor"
                a,bb=(observed(ws[ix[q]]) for q in op[1:])
                assert all(isinstance(q,tuple) or q in "01" for q in (a,bb))
                val=("x",a,bb)
            assert t not in writes
            writes[t]=val
        moves=dict(action.moves)
        ws=tuple(move(w,writes.get(t,observed(w)),moves.get(t,0)) for t,w in zip(tapes,ws))
        for i,w in enumerate(ws):
            lo[i]=min(lo[i],w[0]);hi[i]=max(hi[i],w[0])
        pc=action.target
        if step%cut==0 or step==clock:
            saved.append((step,len(b.rules) if pc==-1 else pc,ws,tuple(lo),tuple(hi)))
    assert pc==-1 and sum(y-x+1 for x,y in zip(lo,hi))==cells
    return built, saved


def frm(x):
    if not isinstance(x, tuple):
        assert x in ("0","1")
        return "(.bit "+("true" if x=="1" else "false")+")"
    if x[0]=="v":
        return f"(.input {x[1]})"
    assert x[0]=="x"
    return f"(.xor {frm(x[1])} {frm(x[2])})"


def glyph(x):
    if isinstance(x,str):
        return GLYPHS[x]
    if x[0]=="v":
        return f"v {x[1]}"
    return ".bits "+frm(x)


def lst(xs):
    return "["+",".join(xs)+"]"


def vec(xs):
    return "(#"+lst(xs)+").toVector"


def tree(leaves, k, state_count, prog):
    if len(leaves)==1:
        return leaves[0]
    mid=len(leaves)//2
    left, initial, middle, t = tree(leaves[:mid],k,state_count,prog)
    right, middle2, final, u = tree(leaves[mid:],k,state_count,prog)
    assert middle==middle2
    proof=f"(@S008.Symbolic.join {k} {state_count} {prog} {initial} {middle} {final} {t} {u} {left} {right})"
    return proof,initial,final,t+u


MICRO_GLYPHS = """private abbrev v (i : ℕ) : Glyph := .bits (.input i)
private abbrev bl : Glyph := .fixed .blank
private abbrev homeL : Glyph := .fixed .left
private abbrev markL : Glyph := .fixed .parkLeft
private abbrev zero : Glyph := .fixed (.bit false)
private abbrev one : Glyph := .fixed (.bit true)
"""


def micro_segment(case, built, each, cut, idx):
    table, start, _, clock, _, _ = CASES[case]
    program, tapes, entry = built
    k, states = len(tapes), len(program.rules)
    begin, stop = idx*cut, min(clock,(idx+1)*cut)
    left = f"(initial {entry} {start})" if idx == 0 else f"cut{idx-1}"
    first = left
    definitions, obligations, leaves, windows = [], [], [], {}
    for j in range(begin+1,stop+1):
        if j == stop:
            right = f"cut{idx}"
        else:
            _,pc,ws,lo,hi = each[j-1]
            indices=[]
            for w in ws:
                if w not in windows:
                    label=f"m{idx}w{len(windows)}"
                    windows[w]=label
                    pos,pre,post=w
                    definitions.append(f"private def {label} : WindowS := ⟨{pos},{lst(map(glyph,pre))},{lst(map(glyph,post))}⟩")
                indices.append(windows[w])
            right=f"m{idx}t{j}"
            definitions.append(f"private def {right} : State {k} {states} := ⟨{pc},{vec(indices)},{vec(map(str,lo))},{vec(map(str,hi))}⟩")
        sub=f"m{idx}step{j}"
        obligations.append(f"private theorem {sub} : run {table} {left} 1=some {right} := by decide +kernel")
        leaves.append((sub,left,right,1))
        left=right
    derivation=tree(leaves,k,states,table)[0]
    final=f"theorem seg{idx} : run {table} {first} {stop-begin}=some cut{idx} :=\n  {derivation}"
    return "\n".join([*definitions,*obligations,final])


def emit(name, cut, path, part_size):
    sym, start, expected, clock, cells, _ = CASES[name]
    (p,tapes,entry), snapshots = symbolic_run(name,cut)
    k, s = len(tapes), len(p.rules)
    pool={}
    windows=[]
    frames=[]
    segments=[]
    leaves=[]
    left=f"(initial {entry} {start})"
    at=0
    for z, (j,pc,ws,lo,hi) in enumerate(snapshots):
        indices=[]
        for w in ws:
            if w not in pool:
                i=len(pool)
                pool[w]=f"win{i}"
                pos,pre,post=w
                windows.append(f"private def win{i} : WindowS := ⟨{pos},{lst(map(glyph,pre))},{lst(map(glyph,post))}⟩")
            indices.append(pool[w])
        right=f"cut{z}"
        frames.append(f"private def {right} : State {k} {s} := "
                f"⟨{pc},{vec(indices)},{vec(map(str,lo))},{vec(map(str,hi))}⟩")
        segments.append(f"private theorem seg{z} : run {sym} {left} {j-at}=some {right} := by decide +kernel")
        leaves.append((f"seg{z}",left,right,j-at))
        left,at=right,j
    chain=tree(leaves,k,s,sym)[0]
    cert=f"""attribute [local irreducible] S008.Symbolic.run

theorem checked_run : run {sym} (initial {entry} {start}) {clock}=some {left} :=
  {chain}

private theorem final_ready : (decide ({left}.pc.val={s} ∧
    (∑ i : Fin {k}, ({left}.high[i]+1-{left}.low[i]).toNat)={cells} ∧
    ∀ i : Fin {k}, S008.Symbolic.same {left}.windows[i] {expected}[i]) : Bool)=true :=
  by decide +kernel

theorem verified : check {sym} {entry} {start} {clock} {cells} {expected}=true :=
  S008.Symbolic.check_from_run {sym} {entry} {start} {clock} {cells} {expected} {left} checked_run final_ready

theorem certified : Outcome {sym} {entry} {start} {clock} {cells} {expected} :=
  S008.Symbolic.check_sound {sym} {entry} {start} {clock} {cells} {expected} verified

theorem exact_cells (v : ℕ → Bool) :
    (OAI.Computability.NearSquareRoot.visitedCells (S008.NodeSource.rule {sym})
       (S008.NodeSource.physical ((initial {entry} {start}).eval v)) {clock}).ncard={cells} :=
  S008.ExactCells.symbolic_exact {sym} {entry} {start} {clock} {cells} {expected} v verified
"""
    head=f"""import NodeSymbolicCases
import NodeExactCells

namespace S008.Certified.{name}
open S008.NodeTables (direct copyRole xorRole)
open S008.Symbolic S008.SymbolicCases
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000
private abbrev v (i : ℕ) : Glyph := .bits (.input i)
private abbrev bl : Glyph := .fixed .blank
private abbrev homeL : Glyph := .fixed .left
private abbrev markL : Glyph := .fixed .parkLeft
private abbrev zero : Glyph := .fixed (.bit false)
private abbrev one : Glyph := .fixed (.bit true)
"""
    end=f"end S008.Certified.{name}\n"
    if part_size:
        base=path.stem
        assert base.isidentifier() and base.isascii()
        datamod=base+"Data"
        datafile=path.with_name(datamod+".lean")
        roots=[]
        stem=f"namespace S008.Certified.{name}\nopen S008.NodeTables (direct copyRole xorRole)\nopen S008.Symbolic S008.SymbolicCases\nset_option maxRecDepth 20000\nset_option maxHeartbeats 12000000\n"
        public_frames=[x.replace("private def ","def ",1) for x in frames]
        if len(frames)<=360 and len(windows)<=512:
            datafile.write_text("\n".join([head,*windows,*public_frames,end]))
        else:
            win_modules=[]
            for j in range(0,len(windows),64):
                label=base+"Wins"+str(j//64).zfill(4)
                data=[x.replace("private def ","def ",1) for x in windows[j:j+64]]
                path.with_name(label+".lean").write_text("\n".join([head,*data,end]))
                win_modules.append(label)
            frame_modules=[]
            for j in range(0,len(frames),64):
                label=base+"Frames"+str(j//64).zfill(4)
                path.with_name(label+".lean").write_text("\n".join(
                    [*(f"import {w}" for w in win_modules),stem,*public_frames[j:j+64],end]))
                frame_modules.append(label)
            datafile.write_text("\n".join(f"import {f}" for f in frame_modules)+"\n")
        use_micro = name in ("seventytwo","eightyone")
        if use_micro:
            micro_program, micro_states = symbolic_run(name,1)
        for block in range(0,len(segments),part_size):
            label=base+"Part"+str(block//part_size).zfill(4)
            roots.append(label)
            subs=[x.replace("private theorem ","theorem ",1) for x in segments[block:block+part_size]]
            if use_micro:
                indices=range(block,min(block+part_size,len(segments)))
                subs=[MICRO_GLYPHS,*[micro_segment(name,micro_program,micro_states,cut,i) for i in indices]]
            path.with_name(label+".lean").write_text("\n".join([f"import {datamod}",stem,*subs,end]))
        path.write_text("\n".join(["import NodeExactCells",*(f"import {r}" for r in roots),stem,cert,end]))
    else:
        path.write_text("\n".join([head,*windows,*frames,*segments,cert,end]))
    print(json.dumps(dict(case=name,clock=clock,cells=cells,cut_size=cut,
                          windows=len(windows),segments=len(segments),parts=(len(segments)+part_size-1)//part_size if part_size else 0)))



def main():
    p=ArgumentParser()
    p.add_argument("case", choices=CASES)
    p.add_argument("output", type=Path)
    p.add_argument("--cut",type=int,default=None)
    p.add_argument("--part-size",type=int,default=None,help="independent obligations per source module, zero writes one monolithic file")
    args=p.parse_args()
    if args.cut is None:
        args.cut=3 if args.case=="eightyone" else 4
    if args.part_size is None:
        args.part_size=1 if args.case=="seventytwo" else (2 if args.case=="eightyone" else 4)
    if not 1<=args.cut<=8:
        p.error("--cut must be between 1 and 8")
    if args.part_size<0:
        p.error("--part-size must be nonnegative")
    emit(args.case,args.cut,args.output,args.part_size)


if __name__=="__main__":
    main()
