"""Audit fixture only: execute unchanged #6968 tables and #5356 table engine."""
from fractions import Fraction
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tables
import machine


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Tape:
    def __init__(self, body=(), capacity=4096):
        self.cells = [machine.LEFT] + list(body) + [machine.BLANK] * (capacity - len(body))
        self.pos, self.actions, self.highwater = 1, 0, 1

    def read(self):
        self.actions += 1
        return self.cells[self.pos]

    def write(self, value):
        need(self.pos > 0, "preserve physical origin marker")
        self.actions += 1
        self.cells[self.pos] = value

    def move(self, direction):
        need(direction in (-1, 1), "unit move")
        self.actions += 1
        self.pos += direction
        need(0 <= self.pos < len(self.cells), "supplied backed interval")
        self.highwater = max(self.highwater, self.pos)


class Counted:
    def __init__(self, rows):
        self.rows, self.steps = rows, 0

    def __getitem__(self, pc):
        self.steps += 1
        return self.rows[pc]


def encode(values, width):
    virtual = [symbol for value in values for symbol in
               [*((value >> j) & 1 for j in range(width)), 2]]
    return [((symbol >> j) & 1) for symbol in virtual for j in (2, 1, 0)]


def decode(tape, width, count):
    bits = tape.cells[1:1+3*count*(width+1)]
    virtual = [4*bits[i] + 2*bits[i+1] + bits[i+2] for i in range(0, len(bits), 3)]
    result = []
    for i in range(0, len(virtual), width+1):
        v = virtual[i:i+width]
        need(virtual[i+width] == 2 and set(v) <= {0, 1}, "signed component frame")
        result.append(sum(bit << j for j, bit in enumerate(v)) - (v[-1] << width))
    return result


def run(rows, width, values, expected, dirty):
    data = Tape(encode(values, width))
    work = [Tape([1] * dirty), Tape([0] * (dirty+3 if dirty else 0))]
    extents = [len(t.cells) for t in [data, *work]]
    table = Counted(rows)
    for t in work:
        machine.retire(t)
    machine.execute_table(table, (data, *work))
    for t in work:
        machine.retire(t)
    need(decode(data, width, len(values)) == expected, "exact signed fixed-D result")
    need(all(t.pos == 1 for t in [data, *work]), "all physical heads returned")
    need(all(all(x == machine.BLANK for x in t.cells[1:]) for t in work), "complete work retirement")
    need([len(t.cells) for t in [data, *work]] == extents, "historical backing retained")
    need(all(t.cells[0] == machine.LEFT for t in [data, *work]), "origin owner identity")
    need(all((a > 0) - (a < 0) == (b > 0) - (b < 0) for a, b in zip(values, expected)), "positive D preserves sign")
    length = len(values) * (width+1)
    debt = 2*dirty+3 if dirty else 0
    bill = sum(t.actions for t in [data, *work]) + table.steps
    need(bill <= 2048*(length+1) + 7*debt + 16*2, "full published physical/control ceiling")
    return bill


def main():
    reports = []
    packets = total = 0
    for divisor in (1, 3, 5, 15, 105, 1125):
        for name, coefficient in (("multiply", Fraction(divisor)), ("divide", Fraction(1, divisor))):
            rows, metadata = tables.compile_scalar("SCALE", coefficient)
            report = {"D": divisor, "operation": name, "rows": len(rows),
                      "states": metadata["states"], "carry_bound": metadata["carry_bound"]}
            for width in (1, 4, 9, 32, 129):
                limit = (1 << (width-1)) - 1
                base = min(limit // divisor, 12345)
                pair = [base, -base]
                values, expected = (pair, [x*divisor for x in pair]) if name == "multiply" else ([x*divisor for x in pair], pair)
                for dirty in (0, 157):
                    total += run(rows, width, values, expected, dirty)
                    packets += 1
            reports.append(report)
    # Exact division rejects a nonmultiple before any public installation.
    rows, _ = tables.compile_scalar("SCALE", Fraction(1, 3))
    data, work = Tape(encode([1, -1], 4)), [Tape(), Tape()]
    before = list(data.cells)
    try:
        machine.execute_table(rows, (data, *work))
    except ValueError:
        need(data.cells == before, "inexact division preserves public contents")
    else:
        raise ValueError("nonmultiple accepted")
    print(json.dumps({"status": "PASS_EXISTING_FIXED_D_BINDING", "packets": packets,
                      "physical_actions_plus_rows": total, "catalogue": reports,
                      "nonmultiple_rejected_before_install": True,
                      "scope": "Unchanged #6968 table generator/executor; supplied coded fields and backed intervals. No new arithmetic implementation."}, indent=2))


if __name__ == "__main__":
    main()
