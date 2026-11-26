"""Independent five-tape interpreter for physically binary-addressed load and store."""
import argparse
from hashlib import sha256
from itertools import product
from pathlib import Path
from random import Random
from runpy import run_path
import json

HERE = Path(__file__).parent
SHORT = run_path(str(HERE / "compiler-indexed-transfer.py"))
BLANK, HOME, BIT0, BIT1, END, COUNT = range(6)
BANK, DIGITS, VALUE, INDEX, WORK = range(5)
LEFT, STAY, RIGHT = -1, 0, 1
CONVERTED, TRANSFER, TRANSFERRED, ERASE, BACK, DONE = 11, 12, 19, 20, 21, 22


def instruction(store, state, symbols):
    moves = [STAY] * 5
    writes = list(symbols)
    if state == 0:
        word = symbols[DIGITS]
        if word == END:
            state = 6
        elif word in (BIT0, BIT1):
            state = 1 + (word - BIT0)
            moves[DIGITS] = RIGHT
        else:
            return None
    elif state in (1, 2):
        digit = state - 1
        if symbols[INDEX] == COUNT:
            state += 2
            writes[INDEX], writes[WORK] = BLANK, COUNT
            moves[INDEX] = moves[WORK] = RIGHT
        elif symbols[INDEX] == BLANK:
            state = 7
            if digit:
                writes[WORK], moves[WORK] = COUNT, RIGHT
        else:
            return None
    elif state in (3, 4):
        state -= 2
        writes[WORK], moves[WORK] = COUNT, RIGHT
    elif state == 5:
        if symbols[WORK] == COUNT:
            writes[INDEX], moves[INDEX] = COUNT, RIGHT
            writes[WORK], moves[WORK] = BLANK, LEFT
        elif symbols[WORK] == HOME:
            state, moves[WORK] = 8, RIGHT
        else:
            return None
    elif state == 6:
        if symbols[INDEX] == COUNT:
            moves[INDEX] = RIGHT
        elif symbols[INDEX] == BLANK:
            state, writes[INDEX] = 9, END
        else:
            return None
    elif state in (7, 8, 9, 10):
        active = DIGITS if state == 10 else INDEX
        if symbols[active] == HOME:
            moves[active] = RIGHT
            if state == 7:
                moves[WORK] = LEFT
            state = (5, 0, 10, 11)[state - 7]
        else:
            moves[active] = LEFT
    elif state == CONVERTED:
        state = TRANSFER
    elif TRANSFER <= state < TRANSFERRED:
        wires = (BANK, INDEX, VALUE)
        local = SHORT["action"](store, state - TRANSFER, tuple(symbols[w] for w in wires))
        if local is None:
            return None
        where, altered, motion = local
        state = TRANSFER + where
        for i, w in enumerate(wires):
            writes[w], moves[w] = altered[i], motion[i]
    elif state == TRANSFERRED:
        state = ERASE
    elif state == ERASE:
        if symbols[INDEX] == COUNT:
            writes[INDEX], moves[INDEX] = BLANK, RIGHT
        elif symbols[INDEX] == END:
            state, writes[INDEX], moves[INDEX] = BACK, BLANK, LEFT
        else:
            return None
    elif state == BACK:
        if symbols[INDEX] == HOME:
            state, moves[INDEX] = DONE, RIGHT
        else:
            moves[INDEX] = LEFT
    else:
        return None
    return state, writes, moves


def check_table(path):
    digest = sha256()
    with path.open("rb") if path else open("/dev/null", "rb") as inp:
        for mode, state, *r in product((False, True), range(23), *(range(6) for _ in range(5))):
            act = instruction(mode, state, r)
            if act is None:
                line = b"-\n"
            else:
                target, writes, moves = act
                opcodes = [3 * w + m + 1 for w, m in zip(writes, moves)]
                line = (" ".join(map(str, [target] + opcodes)) + "\n").encode()
            digest.update(line)
            if path:
                assert inp.readline() == line, (mode, state, r)
        if path:
            assert not inp.read(1)
    return digest.hexdigest()


def run(mode, words, i, word, binary, p, q):
    b = len(word)
    n = len(binary)
    assert int("".join(map(str, binary)) or "0", 2) == i
    body = [x for w in words for x in [BIT0 + x for x in w] + [END]]
    origins = (p, 0, q, 0, 0)
    blocks = [body, [BIT0 + x for x in binary] + [END], [BIT0 + x for x in word] + [END], [], []]
    original = []
    for t, (origin, block) in enumerate(zip(origins, blocks)):
        data = {origin - 1: HOME}
        data.update({origin + j: v for j, v in enumerate(block)})
        if t in (BANK, DIGITS, VALUE):
            data[origin - 4] = COUNT
            data[origin + len(block) + 2] = BIT1
        original.append(data)
    tapes = [d.copy() for d in original]
    head = list(origins)
    visited = {(t, p) for t, p in enumerate(head)}
    state = steps = 0
    limit = i * (2 * b + 15) + 3 * b + 8 * n + 19 - 5 * i.bit_count()
    saw_ready = saw_return = False
    while True:
        if state == CONVERTED:
            assert tapes[INDEX] == {-1: HOME, i: END, **dict.fromkeys(range(i), COUNT)}
            assert head == list(origins)
            saw_ready = True
        elif state == TRANSFERRED:
            assert head == list(origins)
            saw_return = True
        rule = instruction(mode, state, [tapes[t].get(pos, BLANK) for t, pos in enumerate(head)])
        if rule is None:
            break
        assert steps < limit
        state, writes, moves = rule
        for t, pos in enumerate(head):
            if writes[t] == BLANK:
                tapes[t].pop(pos, None)
            else:
                tapes[t][pos] = writes[t]
            head[t] += moves[t]
            visited.add((t, head[t]))
        steps += 1
    assert state == DONE and saw_ready and saw_return
    assert head == list(origins) and steps == limit
    expected = [d.copy() for d in original]
    if mode:
        k = p + i * (b + 1)
        expected[BANK].update({k + j: BIT0 + bit for j, bit in enumerate(word)})
    else:
        expected[VALUE].update({q + j: BIT0 + bit for j, bit in enumerate(words[i])})
    assert tapes == expected
    space = i * (b + 3) + 2 * b + n + 10 - int(n == 0)
    assert len(visited) == space
    return steps, space


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=Path)
    opt = parser.parse_args()
    rng = Random(61202412)
    totals = dict(cases=0, steps=0, max_steps=0, max_visited=0, compared_with_lean=bool(opt.table),
                  rule_rows=2 * 23 * 6 ** 5, table_sha256=check_table(opt.table))

    def sample(mode, words, i, word, binary):
        time, space = run(mode, words, i, word, binary, rng.randrange(-33, 34), rng.randrange(-33, 34))
        totals["cases"] += 1
        totals["steps"] += time
        totals["max_steps"] = max(totals["max_steps"], time)
        totals["max_visited"] = max(totals["max_visited"], space)

    for b in range(3):
        alphabet = list(product(range(2), repeat=b))
        for n in (1, 2, 3):
            for words in product(alphabet, repeat=n):
                for mode, i, word in product((False, True), range(n), alphabet):
                    binary = tuple(map(int, format(i, "b")))
                    sample(mode, words, i, word, binary)
                    sample(mode, words, i, word, (0, 0) + binary)
                    if i == 0:
                        sample(mode, words, i, word, ())
    for _ in range(120):
        n = rng.randrange(1, 70)
        b = rng.randrange(34)
        words = [tuple(rng.randrange(2) for _ in range(b)) for _ in range(n)]
        i = rng.randrange(n)
        word = tuple(rng.randrange(2) for _ in range(b))
        binary = tuple(map(int, format(i, "b").rjust(i.bit_length() + rng.randrange(8), "0")))
        for mode in (True, False):
            sample(mode, words, i, word, binary)
    print(json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
