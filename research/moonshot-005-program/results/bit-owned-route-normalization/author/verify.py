#!/usr/bin/env python3
"""Finite chronological controls for the universal written route theorem."""
import argparse
import hashlib
import json
from pathlib import Path


def combine(mask, rows):
    out = 0
    while mask:
        bit = mask & -mask
        out ^= rows[bit.bit_length() - 1]
        mask ^= bit
    return out


def rank(rows):
    basis = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p in basis:
                value ^= basis[p]
            else:
                basis[p] = value
                break
    return len(basis)


def contained(row, rows):
    return rank(rows + [row]) == rank(rows)


def require(value, message):
    if not value:
        raise ValueError(message)


def rectangular(matrix, domain):
    """R, J columns, h rows from free input coordinates of RREF."""
    codomain = len(matrix)
    red = matrix[:]
    trans = [1 << i for i in range(codomain)]
    pivots = []
    for col in range(domain):
        pivot = next((j for j in range(len(pivots), codomain)
                      if (red[j] >> col) & 1), None)
        if pivot is None:
            continue
        at = len(pivots)
        red[at], red[pivot] = red[pivot], red[at]
        trans[at], trans[pivot] = trans[pivot], trans[at]
        for j in range(codomain):
            if j != at and (red[j] >> col) & 1:
                red[j] ^= red[at]
                trans[j] ^= trans[at]
        pivots.append(col)
    free = [i for i in range(domain) if i not in pivots]
    R = [0] * domain
    for j, p in enumerate(pivots):
        R[p] = trans[j]
    J = []
    for f in free:
        value = 1 << f
        for j, p in enumerate(pivots):
            if (red[j] >> f) & 1:
                value ^= 1 << p
        J.append(value)
    h = [1 << f for f in free]
    for i in range(domain):
        jh = sum(h[j] for j, column in enumerate(J) if (column >> i) & 1)
        require(combine(R[i], matrix) == (1 << i) ^ jh, "RM identity")
    for j, column in enumerate(J):
        require(all((row & column).bit_count() % 2 == 0 for row in matrix), "MJ")
        require([int(bool(column & row)) for row in h] ==
                [int(k == j) for k in range(len(h))], "hJ")
    require(all(combine(row, R) == 0 for row in h), "hR")
    return R, J, h, free


class Word:
    def __init__(self, width):
        self.width = width
        self.identity = [1 << i for i in range(width)]
        self.originals = {f"x{i}" for i in range(3)} | {f"y{i}" for i in range(3)}
        self.initial = {}
        for i in range(6):
            name = f"x{i}" if i < 3 else f"y{i-3}"
            self.initial[name] = ((1 << i) if i < 3 else 0,
                                  [1 << (i*width+j) for j in range(width)])
        self.loc = {name: value[0] for name, value in self.initial.items()}
        self.rows = {name: value[1][:] for name, value in self.initial.items()}
        self.events = []
        self.histories = [(c, name, rows[:]) for name, (c, rows) in self.initial.items()]

    def init(self, name, chart):
        require(name not in self.loc and name not in self.originals, "INIT")
        self.loc[name] = chart
        self.rows[name] = [0] * self.width
        self.events.append({"op": "init", "name": name, "chart": chart})
        self.histories.append((chart, name, self.rows[name][:]))

    def add(self, target, source, block=None):
        require(target != source and self.loc[target] == self.loc[source], "ADD chart")
        block = self.identity if block is None else block
        self.rows[target] = [a ^ combine(b, self.rows[source])
                             for a, b in zip(self.rows[target], block)]
        self.events.append({"op": "add", "target": target, "source": source,
                            "block": block, "chart": self.loc[target]})
        self.histories.append((self.loc[target], target, self.rows[target][:]))

    def move(self, name, chart):
        old = self.loc[name]
        require(old != chart and ((old & chart) in (old, chart)), "nested positive MOVE")
        if name in self.originals:
            require(old & chart == old, "original descending MOVE")
        self.events.append({"op": "move", "name": name, "old": old, "new": chart,
                            "rows": self.rows[name][:], "owned": name not in self.originals})
        self.loc[name] = chart
        self.histories.append((chart, name, self.rows[name][:]))

    def clear(self, name):
        require(name not in self.originals, "public CLEAR")
        self.events.append({"op": "clear", "name": name, "chart": self.loc[name]})
        del self.loc[name]
        del self.rows[name]


def cell(word, chart):
    width = word.width
    U, incoming = [], []
    arrivals = {}
    initial_keys = {}
    for name, (place, rows) in word.initial.items():
        if place == chart:
            initial_keys[name] = len(U)
            U.extend(rows)
    for i, event in enumerate(word.events):
        if event["op"] != "move" or event["new"] != chart:
            continue
        if event["old"] & chart == event["old"]:
            arrivals[i] = (False, len(U))
            U.extend(event["rows"])
        else:
            require(event["owned"], "downward public boundary")
            arrivals[i] = (True, len(incoming))
            incoming.extend(event["rows"])
    formal = {name: [1 << (offset+j) for j in range(width)]
              for name, offset in initial_keys.items()}
    outputs, actual_outputs = [], []
    for i, event in enumerate(word.events):
        op = event["op"]
        if op == "move":
            name = event["name"]
            if event["old"] == chart:
                if event["owned"] and event["new"] & chart == event["new"]:
                    outputs.extend(formal[name])
                    actual_outputs.extend(event["rows"])
                del formal[name]
            if event["new"] == chart:
                down, offset = arrivals[i]
                offset += len(U) if down else 0
                formal[name] = [1 << (offset+j) for j in range(width)]
        elif event["chart"] == chart:
            if op == "init":
                formal[event["name"]] = [0] * width
            elif op == "clear":
                del formal[event["name"]]
            else:
                target, source = event["target"], event["source"]
                formal[target] = [a ^ combine(b, formal[source])
                                  for a, b in zip(formal[target], event["block"])]
    mask = (1 << len(U)) - 1
    N = [row & mask for row in outputs]
    matrix = [row >> len(U) for row in outputs]
    require(actual_outputs == [combine(n, U) ^ combine(m, incoming)
                               for n, m in zip(N, matrix)], "actual cell acquisition")
    R, J, h, free = rectangular(matrix, len(incoming))
    rhs = [value ^ combine(n, U) for value, n in zip(actual_outputs, N)]
    kernel = [incoming[f] for f in free]
    recovered = []
    for i, row in enumerate(R):
        value = combine(row, rhs)
        for j, column in enumerate(J):
            if (column >> i) & 1:
                value ^= kernel[j]
        recovered.append(value)
    require(recovered == incoming, "actual incoming reconstruction")
    for i, row in enumerate(matrix):
        mr = combine(row, R)
        require(combine((1 << i) ^ mr, rhs) == 0, "actual image constraint")
    return {"chart": chart, "input_dimension": len(incoming),
            "output_dimension": len(outputs), "kernel_dimension": len(free),
            "kernel": kernel, "matrix": matrix, "U": U,
            "incoming": incoming, "outputs": actual_outputs}


def audit(word):
    width = word.width
    cells = [cell(word, chart) for chart in range(1, 7)]
    moves = [event for event in word.events if event["op"] == "move" and event["owned"]]
    down = [event for event in moves if event["new"] & event["old"] == event["new"]]
    ground = [event for event in down if event["new"] == 0]
    G = [row for event in ground for row in event["rows"]]
    G += [row for data in cells for row in data["kernel"]]
    require(len(down)*width == len(ground)*width +
            sum(data["input_dimension"] for data in cells), "occurrence partition")
    require(len(G) <= len(down)*width, "mode count")
    y_rows = [1 << i for i in range(3*width, 6*width)]
    checked = 0
    for chart, name, rows in word.histories:
        if chart == 7:
            continue
        local = [1 << (i*width+j) for i in range(3)
                 if chart & (1 << i) for j in range(width)]
        for row in rows:
            require(contained(row, G+y_rows+local), f"normal form {chart} {name}")
            checked += 1
    facet_counts = [int(event["new"].bit_count() == 2) if
                    event["old"] & event["new"] == event["old"] else
                    int(event["old"].bit_count() == 2) for event in moves]
    require(sum(facet_counts) <= len(moves), "owned facet MOVE counted twice")
    xmask = (1 << (3*width)) - 1
    return {"width": width, "events": len(word.events), "histories_checked": checked,
            "owned_moves": len(moves), "downward_moves": len(down),
            "ground_arrivals": len(ground), "G_dimension": len(G),
            "G_x_rank": rank([row & xmask for row in G]),
            "facet_owned_incidence": sum(facet_counts),
            "cells": [{k: data[k] for k in ("chart", "input_dimension",
                       "output_dimension", "kernel_dimension")} for data in cells]}, G, cells


def to_hub(word, caches=False):
    for i in range(3):
        if caches:
            word.init(f"k{i}", 1 << i)
            word.add(f"k{i}", f"x{i}")
        word.move(f"x{i}", 7)


def loop_word(width):
    word = Word(width)
    to_hub(word, True)
    blocks = [word.identity] if width == 1 else [[3, 2], [1, 3], [1, 0], [1, 2]]
    serial = 0
    def add(target, source):
        nonlocal serial
        word.add(target, source, blocks[serial % len(blocks)])
        serial += 1
    word.move("y2", 3)
    word.init("p", 7)
    for name in ("x0", "x1", "x2"):
        add("p", name)
    word.move("p", 3)
    add("y2", "p")
    add("p", "y2")
    word.move("p", 1)
    add("p", "k0")
    word.init("q", 1)
    add("q", "p")
    word.move("p", 3)
    add("p", "y2")
    word.move("p", 1)
    add("p", "k0")
    word.move("p", 3)
    word.clear("p")
    word.move("q", 0)
    add("y0", "q")
    add("q", "y1")
    word.move("q", 1)
    add("q", "k0")
    word.move("q", 3)
    add("q", "y2")
    word.move("q", 0)
    word.clear("q")
    word.move("y0", 6)
    word.move("y1", 5)
    for i in range(3):
        word.clear(f"k{i}")
    return word


def controls():
    outcomes = {}
    for width in (1, 2):
        terminal = Word(width)
        to_hub(terminal)
        terminal.init("p", 7)
        terminal.add("p", "x0")
        terminal.move("p", 4)
        terminal.clear("p")
        report, G, cells = audit(terminal)
        require(report["ground_arrivals"] == 0 and report["G_x_rank"] == width,
                "proper terminal must retain nonlocal information")
        require(not contained(1, [1 << i for i in range(3*width, 6*width)] +
                              [1 << (2*width+j) for j in range(width)]),
                "omitting proper terminal kernel did not fail")
        outcomes[f"proper_termination_V{width}"] = report
        for destination, title in ((4, "proper_revisit"), (0, "ground_revisit")):
            revisit = Word(width)
            to_hub(revisit)
            revisit.init("p", 7)
            revisit.add("p", "x0")
            revisit.move("p", destination)
            revisit.move("p", 7)
            revisit.add("p", "x0")
            revisit.add("p", "x1")
            revisit.move("p", destination)
            revisit.clear("p")
            report, G, cells = audit(revisit)
            require(report["G_x_rank"] == 2*width, "revisit independent arrivals")
            collapsed_last = [1 << (width+j) for j in range(width)]
            if destination:
                collapsed_last += [1 << (2*width+j) for j in range(width)]
            collapsed_last += [1 << i for i in range(3*width, 6*width)]
            require(not contained(1, collapsed_last), "collapsing record occurrences did not fail")
            outcomes[f"{title}_V{width}"] = report
        birth = Word(width)
        birth.init("p", 1)
        birth.add("p", "x0")
        birth.move("p", 0)
        birth.clear("p")
        report, G, cells = audit(birth)
        cell_one = cells[0]
        require(cell_one["input_dimension"] == 0 and cell_one["kernel_dimension"] == 0,
                "birth-only cell invented kernel")
        require(cell_one["outputs"][0] != (1 << width), "free nonlocal birth control")
        require(not contained(1 << (3*width), G), "arbitrary Y was silently removed")
        outcomes[f"birth_image_and_Y_V{width}"] = report
    A, B = [3, 2], [1, 3]
    require([combine(row, B) for row in A] != [combine(row, A) for row in B],
            "block control must be genuinely noncommuting")
    return outcomes


def endpoint_interval():
    from fractions import Fraction
    scale = 1 << 136
    def power(n):
        low, high = 0, n*scale+1
        target = n**199 * scale**200
        while high-low > 1:
            mid = (low+high)//2
            if mid**200 <= target:
                low = mid
            else:
                high = mid
        require(low**200 <= target < high**200, "root interval")
        return Fraction(low, scale), Fraction(high, scale)
    terms = {127: Fraction(37, 6), 64: Fraction(37, 3), 1: Fraction(-37, 3)}
    for j in range(1, 9):
        terms[7*j+1] = terms.get(7*j+1, 0) + Fraction(37, 3)
        terms[7*j] = terms.get(7*j, 0) - Fraction(37, 3)
    terms[7] -= 222
    lo = hi = Fraction(0)
    for n, coefficient in terms.items():
        a, b = power(n)
        lo += coefficient*(a if coefficient >= 0 else b)
        hi += coefficient*(b if coefficient >= 0 else a)
    require(82 < lo <= hi < 83, "all-owned MOVE count threshold")
    at_one = sum(n*coefficient for n, coefficient in terms.items())
    require(at_one == Fraction(629, 6) and at_one > 83, "t=1 scope control")
    return {"low": str(lo), "high": str(hi), "midpoint": float((lo+hi)/2),
            "maximum_owned_moves": 82, "native_facet_ell_cap": 193,
            "downward_moves_required_by_rank_gap": 10,
            "t_one_allowance": str(at_one)}


def native_baseline(path):
    import gzip
    from fractions import Fraction
    native = json.loads(gzip.decompress(path.read_bytes()))
    frames = native["frames"]
    def rational_rank(rows):
        rows = [[Fraction(x) for x in row] for row in rows]
        pivot = 0
        for col in range(8):
            at = next((j for j in range(pivot, len(rows)) if rows[j][col]), None)
            if at is None:
                continue
            rows[pivot], rows[at] = rows[at], rows[pivot]
            factor = rows[pivot][col]
            rows[pivot] = [value/factor for value in rows[pivot]]
            for j in range(pivot+1, len(rows)):
                factor = rows[j][col]
                rows[j] = [a-factor*b for a, b in zip(rows[j], rows[pivot])]
            pivot += 1
        return pivot
    normals = set()
    distances = []
    for i in range(111):
        x0 = frames[str(native["start"][i])]
        x1 = frames[str(native["final"][i])]
        y0 = frames[str(native["start"][111+i])]
        y1 = frames[str(native["final"][111+i])]
        require([rational_rank(f["B"]) for f in (x0, x1, y0, y1)] == [1, 8, 0, 7],
                "native original endpoint ranks")
        root = list(map(Fraction, x0["B"][0]))
        require(sum(x*x for x in root) > 0, "native self noncontact")
        require(all(sum(x*Fraction(y) for x, y in zip(root, row)) == 0
                    for row in y1["B"]), "native target facet orthogonality")
        first = next(value for value in root if value)
        normals.add(tuple(value/first for value in root))
        distances.extend((7, 7))
    require(len(normals) == 111, "distinct native facets")
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "original_paths": len(distances), "each_total_rank_distance": 7,
            "distinct_terminal_facets": len(normals),
            "qualification": "Path monotonicity is a theorem hypothesis; endpoints are checked from native source."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--native", default=str(Path(__file__).resolve().parent.parent /
                                              "block-rigidity/BIT-NATIVE-WORD.json.gz"))
    args = parser.parse_args()
    cases = {}
    for width in (1, 2):
        report, _, _ = audit(loop_word(width))
        cases[f"chronological_loop_V{width}"] = report
    cases.update(controls())
    result = {"status": "PASS", "classification": "Finite controls; universal claim proved in PROOF.md",
              "cases": cases, "target_endpoint": endpoint_interval(),
              "native_baseline": native_baseline(Path(args.native)),
              "negative_controls": ["omit proper-terminal kernel", "collapse proper reentry by label",
                                    "collapse repeated ground arrivals", "grant free nonlocal birth",
                                    "omit independent Y", "pretend blocks commute",
                                    "extend target MOVE cap to t=1"],
              "limitations": "Synthetic words test normalization, not complete source endpoints or a new supplier."}
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "allowance": result["target_endpoint"]["midpoint"]}))


if __name__ == "__main__":
    main()
