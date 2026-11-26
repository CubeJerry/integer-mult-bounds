#!/usr/bin/env python3
"""Check the sharp external schoolbook clock with an independent table interpreter."""
from pathlib import Path
from random import Random
from runpy import run_path

source = run_path(str(Path(__file__).with_name("schoolbook.py")))
program, labels, start = source["machine"]()
blank = source["BLANK"]


def check(n, x, y):
    clocks = []
    for j in range(n):
        carried = x*(y % (1 << (j+1))) >= (1 << (n+j))
        clocks.append(3 + ((4*n+4) if (y >> j) & 1 else 0) + int(carried))
    expected = 7*n+8 + sum(clocks)
    upper = 4*n*n + 15*n + 7
    raw = f"{x:0{n}b}|{y:0{n}b}"
    rows = {name: {} for name in labels}
    rows["I"] = dict(enumerate(raw))
    heads = {name: 0 for name in labels}
    ranges = {name: [0, 0] for name in labels}
    pc = start
    for _ in range(expected):
        assert pc >= 0
        rule = program.rules[pc]
        action = rule.default
        if rule.tape:
            name = rule.tape
            action = rule.cases.get(rows[name].get(heads[name], blank), action)
        assert action is not None
        for name, symbol in action.writes:
            assert isinstance(symbol, str)
            rows[name][heads[name]] = symbol
        for name, delta in action.moves:
            heads[name] += delta
            ranges[name][0] = min(ranges[name][0], heads[name])
            ranges[name][1] = max(ranges[name][1], heads[name])
        pc = action.target
    assert pc == source["HALT"]
    assert expected <= upper and rows["I"] == dict(enumerate(raw))
    assert rows["O"] == dict(enumerate(f"{x*y:0{2*n}b}"))
    assert sum(hi-lo+1 for lo, hi in ranges.values()) == 8*n+9
    if x == y == (1 << n)-1:
        assert expected == upper
    return expected


def main():
    count = 0
    for n in range(1, 7):
        for x in range(1<<n):
            for y in range(1<<n):
                check(n, x, y)
                count += 1
    rng = Random(81723)
    for n in (8, 11, 16, 31, 64, 129):
        for x, y in [(0,0), ((1<<n)-1, (1<<n)-1),
                     *[(rng.getrandbits(n), rng.getrandbits(n)) for _ in range(4)]]:
            check(n, x, y)
            count += 1
    print(f"{count} exact transition traces, exact product words, and exact visited-cell counts")
    print("all-ones worst cases attain 4n^2+15n+7 transitions and 8n+9 cells")


if __name__ == "__main__":
    main()
