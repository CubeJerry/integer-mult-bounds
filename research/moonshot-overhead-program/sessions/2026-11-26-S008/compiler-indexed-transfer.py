"""Replay the three-tape indexed load/store and compare its entire finite rule with Lean."""
import argparse
from hashlib import sha256
from itertools import product
from pathlib import Path
from random import Random
import json

BLANK, HOME, BIT0, BIT1, END, COUNT = range(6)
CHECK, SCAN, SEEK_DONE, COPY, HOME_BANK, HOME_INDEX, HOME_VALUE, DONE = range(8)
BANK, INDEX, VALUE = range(3)
LEFT, STAY, RIGHT = -1, 0, 1


def action(store, state, symbols):
    bank, index, value = symbols
    moves = [STAY, STAY, STAY]
    writes = list(symbols)
    target = state
    if state == CHECK:
        if index == COUNT:
            target = SCAN
        elif index == END:
            target = SEEK_DONE
        else:
            return None
    elif state == SCAN:
        if bank in (BIT0, BIT1):
            moves[BANK] = RIGHT
        elif bank == END:
            target = CHECK
            moves[BANK] = moves[INDEX] = RIGHT
        else:
            return None
    elif state == SEEK_DONE:
        target = COPY
    elif state == COPY:
        if bank in (BIT0, BIT1) and value in (BIT0, BIT1):
            writes[BANK] = writes[VALUE] = value if store else bank
            moves[BANK] = moves[VALUE] = RIGHT
        elif bank == value == END:
            target = HOME_BANK
        else:
            return None
    elif HOME_BANK <= state <= HOME_VALUE:
        selected = state - HOME_BANK
        if symbols[selected] == HOME:
            target += 1
            moves[selected] = RIGHT
        else:
            moves[selected] = LEFT
    else:
        return None
    return target, writes, moves


def encoded_table():
    rows = []
    for mode, state, a, i, v in product((False, True), range(8), range(6), range(6), range(6)):
        instruction = action(mode, state, (a, i, v))
        if instruction is None:
            rows.append("-")
        else:
            target, writes, moves = instruction
            output = [target] + [3 * w + m + 1 for w, m in zip(writes, moves)]
            rows.append(" ".join(map(str, output)))
    return "\n".join(rows) + "\n"


def bit_letters(bits):
    return [BIT0 + int(x) for x in bits]


def check_case(store, words, i, word, origins):
    b = len(word)
    body = [x for w in words for x in bit_letters(w) + [END]]
    data = [body, [COUNT] * i + [END], bit_letters(word) + [END]]
    # Independently occupied exterior cells on *both* sides of all three tapes.
    original = []
    for axis, origin in enumerate(origins):
        live = {origin + j: value for j, value in enumerate(data[axis])}
        live[origin - 1] = HOME
        live[origin - 2] = BIT1
        live[origin - 4] = COUNT
        live[origin + len(data[axis]) + 1] = BIT0
        original.append(live)
    bank = [t.copy() for t in original]
    heads = list(origins)
    visited = {(t, p) for t, p in enumerate(heads)}
    state = CHECK
    steps = 0
    bill = i * (2 * b + 4) + 3 * b + 9
    while True:
        reads = tuple(bank[t].get(p, BLANK) for t, p in enumerate(heads))
        rule = action(store, state, reads)
        if rule is None:
            break
        assert steps < bill
        state, writes, moves = rule
        for t, pos in enumerate(heads):
            if writes[t] == BLANK:
                bank[t].pop(pos, None)
            else:
                bank[t][pos] = writes[t]
            heads[t] += moves[t]
            visited.add((t, heads[t]))
        steps += 1
    assert state == DONE and steps == bill and tuple(heads) == origins
    start = origins[BANK] + i * (b + 1)
    expected = [t.copy() for t in original]
    if store:
        expected[BANK].update({start + j: value for j, value in enumerate(bit_letters(word))})
    else:
        expected[VALUE].update({origins[VALUE] + j: value
                                for j, value in enumerate(bit_letters(words[i]))})
    assert expected == bank
    assert len(visited) == i * (b + 2) + 2 * b + 6
    return steps, len(visited)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=Path, help="the actual finite rules exported from Lean")
    table_path = parser.parse_args().table
    table = encoded_table()
    if table_path:
        assert table.encode() == table_path.read_bytes()
    rng = Random(14259011)
    totals = dict(cases=0, steps=0, max_steps=0, max_visited=0,
                  rule_rows=len(table.splitlines()), table_sha256=sha256(table.encode()).hexdigest(),
                  compared_with_lean=bool(table_path))

    def run(mode, words, index, value):
        origins = tuple(rng.randrange(-30, 31) for _ in range(3))
        steps, visited = check_case(mode, words, index, value, origins)
        totals["cases"] += 1
        totals["steps"] += steps
        totals["max_steps"] = max(steps, totals["max_steps"])
        totals["max_visited"] = max(visited, totals["max_visited"])

    for b in range(3):
        alphabet = [tuple(bits) for bits in product(range(2), repeat=b)]
        for count in (1, 2, 3):
            for group in product(alphabet, repeat=count):
                for mode, i, value in product((False, True), range(count), alphabet):
                    run(mode, group, i, value)
    for _ in range(160):
        b = rng.randrange(20)
        n = rng.randrange(1, 33)
        words = [tuple(rng.randrange(2) for _ in range(b)) for _ in range(n)]
        value = tuple(rng.randrange(2) for _ in range(b))
        for mode in (False, True):
            run(mode, words, rng.randrange(n), value)
    print(json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
