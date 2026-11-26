"""Compare the literal Lean machine with an independent five-tape modular arithmetic oracle."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
import json
from random import Random


BLANK, HOME, ZERO, ONE, END, MARK = range(6)
# The machine can temporarily store two candidate bits in one physical symbol.
PAIRS = (BLANK, MARK, ZERO, ONE)
DECODE = {symbol: divmod(i, 2) for i, symbol in enumerate(PAIRS)}


def local(state, cells):
    a, b, m, sum_symbol, diff_symbol = cells
    if state < 16:
        if (a, b, m) == (END,) * 3:
            reduce_sum = (state >> 3) or not ((state >> 1) & 1)
            return 16 + 2 * reduce_sum + ((state >> 2) & 1), -1, cells
        if not (ZERO <= a <= ONE and ZERO <= b <= ONE and ZERO <= m <= ONE):
            return None
        a, b, m = a - ZERO, b - ZERO, m - ZERO
        raw_sum = a + b + (state >> 3)
        raw_diff = a - b - ((state >> 2) & 1)
        reduced_sum = (raw_sum & 1) - m - ((state >> 1) & 1)
        corrected_diff = (raw_diff & 1) + m + (state & 1)
        next_state = (8 * (raw_sum >= 2) + 4 * (raw_diff < 0) +
                      2 * (reduced_sum < 0) + (corrected_diff >= 2))
        s = PAIRS[2 * (raw_sum & 1) + (reduced_sum & 1)]
        d = PAIRS[2 * (raw_diff & 1) + (corrected_diff & 1)]
        return next_state, 1, (a + ZERO, b + ZERO, m + ZERO, s, d)
    if state < 20:
        if a == HOME:
            return 20, 1, cells
        if a in (ZERO, ONE) and sum_symbol in DECODE and diff_symbol in DECODE:
            s = ZERO + DECODE[sum_symbol][(state - 16) >> 1]
            d = ZERO + DECODE[diff_symbol][state & 1]
            return state, -1, (a, b, m, s, d)
    return None


def table(source):
    hasher = sha256()
    count = nonhalt = 0
    for state in range(21):
        for word in product(range(6), repeat=5):
            tr = local(state, word)
            if tr is None:
                line = b"-\n"
            else:
                next_state, move, writes = tr
                nonhalt += 1
                opcodes = (3 * letter + move + 1 for letter in writes)
                line = (" ".join(map(str, (next_state, *opcodes))) + "\n").encode()
            if source:
                assert source.readline() == line, (state, word, line)
            hasher.update(line)
            count += 1
    if source:
        assert not source.read(1)
    return {"rows": count, "nonhalting_rows": nonhalt, "table_sha256": hasher.hexdigest()}


def stream_local(state, cells):
    a = cells[0]
    if 1 <= state <= 21:
        result = local(state - 1, cells)
        if result is not None:
            nxt, shift, writes = result
            return 1 + nxt, (shift,) * 5, writes
        if state == 21:
            return 22, (0,) * 5, cells
        return None
    if state == 0 and a in (ZERO, ONE, END):
        next_state, shift = 1, 0
    elif state == 0 and a == MARK:
        next_state, shift = 24, -1
    elif state == 22 and a in (ZERO, ONE):
        next_state, shift = 22, 1
    elif state == 22 and a == END:
        next_state, shift = 23, 1
    elif state == 23 and a == HOME:
        next_state, shift = 0, 1
    elif state == 24:
        next_state, shift = (25, 1) if a == MARK else (24, -1)
    elif state == 25:
        next_state, shift = 26, 1
    else:
        return None
    return next_state, (shift, shift, 0, shift, shift), cells


def stream_table(source):
    digest = sha256()
    count = legal = 0
    for state in range(27):
        for symbols in product(range(6), repeat=5):
            step = stream_local(state, symbols)
            if step:
                nxt, moves, writes = step
                opcodes = (3 * x + m + 1 for x, m in zip(writes, moves))
                line = (" ".join(map(str, (nxt, *opcodes))) + "\n").encode()
                legal += 1
            else:
                line = b"-\n"
            count += 1
            digest.update(line)
            if source:
                assert source.readline() == line, (state, symbols, line)
    if source:
        assert not source.read(1)
    return {"stream_rows": count, "stream_nonhalting_rows": legal, "stream_table_sha256": digest.hexdigest()}


def batch(width, n, rng):
    homes = [rng.randrange(-30, 31) for _ in range(5)]
    m = rng.randrange(1, 1 << width) if width else 0
    pairs = [(rng.randrange(m), rng.randrange(m)) if m else (0, 0) for _ in range(n)]
    length = n * (width + 2)
    before = [[rng.randrange(6) for _ in range((width if t == 2 else length) + 9)] for t in range(5)]
    before[0][1], before[0][2], before[0][3 + length] = MARK, HOME, MARK
    for t, value in ((0, lambda j: pairs[j][0]), (1, lambda j: pairs[j][1])):
        for j in range(n):
            lo = 3 + j * (width + 2)
            before[t][lo:lo + width] = [ZERO + ((value(j) >> i) & 1) for i in range(width)]
            before[t][lo + width] = END
            if t == 0:
                before[t][lo + width + 1] = HOME
    if n:
        before[2][3:3 + width] = [ZERO + ((m >> i) & 1) for i in range(width)]
        before[2][3 + width] = END
    wanted = [bank.copy() for bank in before]
    if width:
        for j, (a, b) in enumerate(pairs):
            lo = 3 + j * (width + 2)
            for t, v in ((3, (a + b) % m), (4, (a - b) % m)):
                wanted[t][lo:lo + width] = [ZERO + ((v >> i) & 1) for i in range(width)]
    banks = [s.copy() for s in before]
    heads = homes.copy()
    visited = {(t, x) for t, x in enumerate(heads)}
    state = count = 0
    while True:
        offsets = [h - p + 3 for h, p in zip(heads, homes)]
        step = stream_local(state, tuple(banks[t][i] for t, i in enumerate(offsets)))
        if step is None:
            break
        state, moves, writes = step
        for t in range(5):
            banks[t][offsets[t]] = writes[t]
            heads[t] += moves[t]
            visited.add((t, heads[t]))
        count += 1
        assert count <= n * (4 * width + 8) + 4
    assert state == 26 and count == n * (4 * width + 8) + 4 and banks == wanted and heads == homes
    assert len(visited) == 4 * (length + 3) + (width + 2 if n else 1)
    return count


def run(width, m, left, right, random):
    homes = [random.randrange(-104, 105) for _ in range(5)]
    before = [[random.randrange(6) for _ in range(width + 8)] for _ in homes]
    for t, value in enumerate((left, right, m)):
        for j in range(width):
            before[t][3 + j] = ZERO + ((value >> j) & 1)
        before[t][3 + width] = END
    before[0][2] = HOME
    actual = [layer.copy() for layer in before]
    heads = homes.copy()
    visited = {(t, h) for t, h in enumerate(heads)}
    state = steps = 0
    while True:
        offsets = [h - start + 3 for h, start in zip(heads, homes)]
        action = local(state, tuple(actual[t][i] for t, i in enumerate(offsets)))
        if action is None:
            break
        state, move, writes = action
        for t, (cell, w) in enumerate(zip(offsets, writes)):
            actual[t][cell] = w
            heads[t] += move
            visited.add((t, heads[t]))
        steps += 1
        assert steps <= 2 * width + 2
    assert state == 20 and heads == homes and steps == 2 * width + 2
    assert visited == {(t, h + off) for t, h in enumerate(homes) for off in range(-1, width + 1)}
    assert actual[:3] == before[:3]
    for t, value in ((3, (left + right) % m), (4, (left - right) % m)):
        expected = before[t].copy()
        expected[3:3 + width] = [ZERO + ((value >> j) & 1) for j in range(width)]
        assert actual[t] == expected
    return steps


def experiment(extended):
    random = Random(0x20261126)
    count = steps = largest = 0
    for w in range(1, 7 if extended else 6):
        for m in range(1, 1 << w):
            for a, b in product(range(m), repeat=2):
                steps += run(w, m, a, b, random)
                count += 1
    for w in (1, 2, 5, 7, 8, 15, 16, 31, 32, 63, 64, 127, 128, 257, 512, 1024):
        for m in (1, (1 << w) - 1, 1 << (w - 1), min((1 << (w - 1)) + 1, (1 << w) - 1),
                  random.randrange(1, 1 << w)):
            for a, b in ((0, 0), (m - 1, m - 1), (m - 1, 0), (0, m - 1),
                         (random.randrange(m), random.randrange(m))):
                steps += run(w, m, a, b, random)
                count += 1
                largest = max(largest, w)
    return {"complete_runs": count, "physical_transitions": steps, "largest_bits": largest}


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("--table")
    p.add_argument("--stream-table")
    p.add_argument("--extended", action="store_true")
    args = p.parse_args()
    if args.table:
        with open(args.table, "rb") as f:
            rows = table(f)
    else:
        rows = table(None)
    if args.stream_table:
        with open(args.stream_table, "rb") as f:
            rows.update(stream_table(f))
    else:
        rows.update(stream_table(None))
    rng = Random(454647)
    shapes = [(w, n) for w in range(0, 11) for n in range(0, 22)]
    shapes.extend((w, n) for w in (16, 32, 63, 129, 257, 512, 1024) for n in (0, 1, 3, 5, 11, 17))
    stream_steps = sum(batch(w, n, rng) for w, n in shapes)
    print(json.dumps({**rows, **experiment(args.extended), "stream_runs": len(shapes),
                      "stream_transitions": stream_steps}, sort_keys=True))
