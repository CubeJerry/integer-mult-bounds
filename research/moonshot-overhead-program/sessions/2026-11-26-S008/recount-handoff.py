#!/usr/bin/env python3
"""Replay physical moves of the S008 AQ-P open handoff on distinct one-head tapes.

Machine operations decide from the current finite-control phase and scanned
symbols only. Absolute indices, full tape images, Python iteration over test
words, and the closed-form invoices are used only by the independent driver.
"""
from dataclasses import dataclass, field
from itertools import product
import json
import random

BLANK, LEFT, RIGHT, BOTTOM = "_", "[", "]", "#"
BITS = ("0", "1")
MARK = {"0": "a", "1": "b"}
UNMARK = {"a": "0", "b": "1"}
PARK = {"left": "L", "inside": "I", "right": "R"}
CONTRACT, FULL = "c", "f"


@dataclass
class Tape:
    cells: dict[int, str] = field(default_factory=dict)
    head: int = 0
    low: int = 0
    high: int = 0

    @classmethod
    def bank(cls, bits="", cursor=0):
        cells = dict(enumerate(LEFT + bits + RIGHT))
        return cls(cells, cursor, cursor, cursor)

    @classmethod
    def stack(cls, prefix=""):
        cells = dict(enumerate(BOTTOM + prefix))
        top = len(cells)
        return cls(cells, top, top, top)

    def read(self):
        return self.cells.get(self.head, BLANK)

    def apply(self, symbol, move):
        assert move in (-1, 0, 1)
        if symbol == BLANK:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = symbol
        self.head += move
        self.low = min(self.low, self.head)
        self.high = max(self.high, self.head)

    def image(self):
        return self.cells.copy(), self.head


class Rule:
    def __init__(self):
        self.steps = 0

    def step(self, *ops):
        # OpenAI TM.advance reads the old tuple, then applies one write/move
        # on each tape. All undeclared tapes keep their symbols and heads.
        assert len({id(tape) for tape, _, _ in ops}) == len(ops)
        self.steps += 1
        for tape, symbol, move in ops:
            tape.apply(symbol, move)

    def park(self, bank, stack):
        start = bank.read()
        kind = "left" if start == LEFT else "right" if start == RIGHT else "inside"
        self.step((bank, MARK[start] if kind == "inside" else start, 0))
        while bank.read() != RIGHT:
            self.step((bank, bank.read(), 1))
        self.step((bank, BLANK, -1), (stack, PARK[kind], 1))
        while bank.read() != LEFT:
            self.step((stack, bank.read(), 1), (bank, BLANK, -1))
        self.step((bank, LEFT, 1))
        self.step((bank, RIGHT, -1))

    def unpark(self, bank, stack):
        self.step((bank, LEFT, 1), (stack, BLANK, -1))
        while stack.read() in BITS or stack.read() in UNMARK:
            self.step((bank, stack.read(), 1), (stack, BLANK, -1))
        where = stack.read()
        if where == PARK["right"]:
            self.step((bank, RIGHT, 0), (stack, BLANK, 0))
            return
        assert where in (PARK["left"], PARK["inside"])
        self.step((bank, RIGHT, -1), (stack, BLANK, 0))
        while bank.read() in BITS:
            self.step((bank, bank.read(), -1))
        assert (where == PARK["left"] and bank.read() == LEFT) or (
            where == PARK["inside"] and bank.read() in UNMARK
        )
        self.step((bank, UNMARK.get(bank.read(), bank.read()), 0))

    def move_word(self, src, dst):
        self.step((src, LEFT, 1), (dst, LEFT, 1))
        first = True
        while src.read() in BITS:
            self.step((dst, src.read(), 1), (src, RIGHT if first else BLANK, 1))
            first = False
        assert src.read() == RIGHT
        self.step((src, RIGHT if first else BLANK, -1), (dst, RIGHT, -1))
        while dst.read() != LEFT:
            self.step((src, src.read(), -1), (dst, dst.read(), -1))
        self.step((src, LEFT, 0), (dst, LEFT, 0))

    def remember(self, control_stack, kind):
        self.step((control_stack, kind, 1))

    def resume(self, control_stack):
        self.step((control_stack, BLANK, -1))
        kind = control_stack.read()
        assert kind in (CONTRACT, FULL)
        self.step((control_stack, BLANK, 0))
        return kind

    def home(self, bank):
        while bank.read() != LEFT:
            self.step((bank, bank.read(), -1))
        self.step((bank, LEFT, 0))

    def discard(self, bank):
        while bank.read() != RIGHT:
            self.step((bank, bank.read(), 1))
        self.step((bank, BLANK, -1))
        while bank.read() != LEFT:
            self.step((bank, BLANK, -1))
        self.step((bank, LEFT, 1))
        self.step((bank, RIGHT, -1))

    def adversarial_child(self, active, independent):
        # A legal body supplied only for finite tests. The independently
        # initialized reply stream has the same length as A. Its bill is
        # excluded from every wrapper equality below.
        self.step((active, LEFT, 1), (independent, LEFT, 1))
        while independent.read() in BITS:
            assert active.read() in BITS
            self.step((active, independent.read(), 1), (independent, independent.read(), 1))
        assert independent.read() == active.read() == RIGHT
        self.step((active, RIGHT, -1), (independent, RIGHT, -1))
        while active.read() != LEFT:
            self.step((active, active.read(), -1), (independent, independent.read(), -1))
        self.step((active, LEFT, 0), (independent, LEFT, 0))


def words(length):
    yield from ("".join(values) for values in product(BITS, repeat=length))


def is_bank(tape, bits, cursor=0):
    return tape.image() == Tape.bank(bits, cursor).image()


def check_single(word, offset, prefix):
    rule = Rule()
    bank, stack = Tape.bank(word, offset), Tape.stack(prefix)
    old_bank, old_stack = bank.image(), stack.image()
    rule.park(bank, stack)
    expected_push = 2 * len(word) + 5 - offset
    assert rule.steps == expected_push and is_bank(bank, "")
    assert stack.head == len(prefix) + len(word) + 2
    rule.unpark(bank, stack)
    assert rule.steps - expected_push == 2 * len(word) + 3 - offset
    assert bank.image() == old_bank and stack.image() == old_stack
    assert (bank.low, bank.high) == (0, len(word) + 1)
    assert (stack.low, stack.high) == (len(prefix) + 1, len(prefix) + len(word) + 2)
    # Discard is paid separately when the main word leaves live arrays at a
    # reserve call. It must also handle end cursors on an empty word.
    cleanup = Rule()
    cleanup.discard(bank)
    assert cleanup.steps == 2 * len(word) + 4 - offset
    assert is_bank(bank, "")


def check_transfer(word):
    rule, src, dst = Rule(), Tape.bank(word), Tape.bank()
    rule.move_word(src, dst)
    assert rule.steps == 2 * len(word) + 3
    assert is_bank(src, "") and is_bank(dst, word)
    for tape in (src, dst):
        assert (tape.low, tape.high) == (0, len(word) + 1)


def check_contracted(rows, control_rows, request, reply, stack_prefix):
    rule = Rule()
    occupied = [Tape.bank(w, d) for w, d in rows]
    control = [Tape.bank(w, d) for w, d in control_rows]
    handoff, other = Tape.bank(request), Tape.bank(reply)
    payload_stack = Tape.stack(stack_prefix)
    control_stack = Tape.stack(stack_prefix[::-1])
    old_payload = payload_stack.image()
    old_control = control_stack.image()
    initial_banks = [t.image() for t in occupied + control]

    # All loops over bank names below stand for an unrolled fixed finite list
    # of tapes for this machine; each macro ends by entering the next state.
    for tape in occupied:
        rule.park(tape, payload_stack)
    for tape in control:
        rule.park(tape, control_stack)
    rule.move_word(handoff, occupied[0])
    rule.remember(control_stack, CONTRACT)
    before_child = rule.steps
    rule.adversarial_child(occupied[0], other)
    child_time = rule.steps - before_child
    assert rule.resume(control_stack) == CONTRACT
    rule.move_word(occupied[0], handoff)
    for tape in reversed(control):
        rule.unpark(tape, control_stack)
    for tape in reversed(occupied):
        rule.unpark(tape, payload_stack)

    pairs = rows + control_rows
    formula = sum(4 * len(w) + 8 - 2 * d for w, d in pairs) + 4 * len(request) + 9
    assert rule.steps - child_time == formula
    assert child_time == 2 * len(request) + 3
    assert [t.image() for t in occupied + control] == initial_banks
    assert is_bank(handoff, reply) and is_bank(other, reply)
    assert payload_stack.image() == old_payload and control_stack.image() == old_control
    for stack, frame, header in [(payload_stack, rows, 0), (control_stack, control_rows, 1)]:
        start = len(stack_prefix) + 1
        assert (stack.low, stack.high) == (start, start + sum(1 + len(w) for w, _ in frame) + header)
    return formula


def check_reserve(word, reply, descriptors, prefix, displaced):
    rule = Rule()
    active, other = Tape.bank(word, displaced), Tape.bank(reply)
    neutral, payload_stack = Tape.bank(), Tape.stack(prefix)
    control_stack = Tape.stack(prefix)
    control = [Tape.bank(w, d) for w, d in descriptors]
    before = [t.image() for t in control]
    rule.home(active)
    assert rule.steps == displaced + 1
    optional_home = rule.steps
    for tape in control:
        rule.park(tape, control_stack)
    rule.remember(control_stack, FULL)
    before_child = rule.steps
    rule.adversarial_child(active, other)
    child_time = rule.steps - before_child
    assert rule.resume(control_stack) == FULL
    for tape in reversed(control):
        rule.unpark(tape, control_stack)
    normalized = sum(4 * len(w) + 8 - 2 * d for w, d in descriptors) + 3
    assert rule.steps - child_time - optional_home == normalized
    assert is_bank(active, reply) and is_bank(neutral, "")
    assert [t.image() for t in control] == before
    assert (neutral.low, neutral.high) == (0, 0)
    assert (payload_stack.low, payload_stack.high) == (len(prefix) + 1, len(prefix) + 1)
    assert control_stack.image() == Tape.stack(prefix).image()
    return normalized


def alternating(rule, active, handoff, scatter):
    """Finite-state odd-lane gather or in-place scatter, outside wrapper bills."""
    rule.step((active, LEFT, 1), (handoff, LEFT, 1))
    chosen = False
    while active.read() in BITS:
        if chosen and scatter:
            rule.step((active,handoff.read(),1),(handoff,handoff.read(),1))
        elif chosen:
            rule.step((active,active.read(),1),(handoff,active.read(),1))
        else:
            rule.step((active,active.read(),1))
        chosen = not chosen
    rule.step((handoff,RIGHT,0))
    rule.home(active)
    rule.home(handoff)
    if scatter:
        rule.discard(handoff)


def flip(rule, bank):
    rule.step((bank, LEFT, 1))
    while bank.read() in BITS:
        rule.step((bank, "1" if bank.read()=="0" else "0", 1))
    rule.home(bank)


def mixed_path():
    # A deterministic host fixture chooses the open call tree. Every actual
    # tape movement, including test gathers, scatters and leaf flips, is
    # performed by the one-head rule. The wrapper toll is measured separately.
    rule = Rule()
    payload = "1001101"*14
    active, spectator = Tape.bank(payload), Tape.bank("001011",3)
    handoff = Tape.bank()
    control = Tape.bank("10110",2)
    stack, cs = Tape.stack("L11"),Tape.stack("I100")
    initial_aux = spectator.image(),control.image(),stack.image(),cs.image()
    base_top, base_ctop = stack.head,cs.head
    high = [base_top, base_ctop]
    totals = [0,0,0,0]
    def word_length(t):
        return next(i-1 for i,s in t.cells.items() if s==RIGHT)
    def visit(plan,depth=0):
        for command,body in plan:
            if command=="flip":
                flip(rule,active)
                continue
            is_c = command=="C"
            if is_c:
                alternating(rule,active,handoff,False)
                # Every contracted caller deliberately loses canonical home.
                rule.step((active,LEFT,1))
            else:
                assert is_bank(spectator,"")
            q = word_length(handoff) if is_c else 0
            rows = ([active,spectator] if is_c else []) + [control]
            forecast = sum(4*word_length(t)+8-2*t.head for t in rows) + (4*q+6 if is_c else 0) + 3
            expected_top = stack.head + (sum(1+word_length(t) for t in (active,spectator)) if is_c else 0)
            expected_ctop = cs.head + word_length(control)+2
            high[0],high[1] = max(high[0],expected_top),max(high[1],expected_ctop)
            initial = rule.steps
            if is_c:
                rule.park(active,stack)
                rule.park(spectator,stack)
            rule.park(control,cs)
            if is_c:
                rule.move_word(handoff,active)
            rule.remember(cs, CONTRACT if is_c else FULL)
            before = rule.steps
            assert (stack.head,cs.head)==(expected_top,expected_ctop)
            visit(body,depth+1)
            after = rule.steps
            assert rule.resume(cs)==(CONTRACT if is_c else FULL)
            if is_c:
                rule.move_word(active,handoff)
            rule.unpark(control,cs)
            if is_c:
                rule.unpark(spectator,stack)
                rule.unpark(active,stack)
            own = before-initial + rule.steps-after
            assert own == forecast
            totals[0]+=own
            totals[1]+=int(is_c)
            totals[2]+=int(not is_c)
            totals[3]=max(totals[3],depth+1)
            if is_c:
                rule.home(active)
                alternating(rule,active,handoff,True)

    leaf = [("flip",[])]
    child = leaf
    for j in range(25):
        # Five contractions interspersed with long full-volume runs.
        child = [("C" if j%5==0 else "F",child)]
    plan = [("C",child+child+[("F",leaf)]),("C",child)]
    def result(w,ops):
        for op,body in ops:
            if op=="flip":
                w="".join("1" if b=="0" else "0" for b in w)
            elif op=="F":
                w=result(w,body)
            else:
                out=list(w)
                out[1::2]=result(w[1::2],body)
                w="".join(out)
        return w
    visit(plan)
    assert is_bank(active,result(payload,plan)) and is_bank(handoff,"")
    assert initial_aux==(spectator.image(),control.image(),stack.image(),cs.image())
    assert (stack.high,cs.high)==tuple(high)
    return dict(zip(("mixed_toll","mixed_contracted","mixed_full","mixed_depth",
                     "payload_frame_peak","control_frame_peak"),totals+[high[0]-base_top,high[1]-base_ctop]))


def main():
    counts = {"park_cursor_cases": 0, "move_word_cases": 0,
              "contracted_receipts": 0, "reserve_receipts": 0, "max_contracted_toll": 0}
    for n in range(8):
        for word in words(n):
            check_transfer(word)
            counts["move_word_cases"] += 1
            for pos in range(n + 2):
                check_single(word, pos, "")
                check_single(word, pos, "Ib10fL")
                counts["park_cursor_cases"] += 2

    for n in range(4):
        for req, rep in product(words(n), repeat=2):
            for parent in words(2):
                for d in range(4):
                    rows = [(parent, d), ("", 1), ("01", 0)]
                    ctrl = [("101", 2)]
                    bill = check_contracted(rows, ctrl, req, rep, "L1Ib")
                    counts["max_contracted_toll"] = max(bill, counts["max_contracted_toll"])
                    counts["contracted_receipts"] += 1
            for d in range(n + 2):
                check_reserve(req, rep, [("101", 2)], "fIR0", d)
                counts["reserve_receipts"] += 1

    rng = random.Random(8675309)
    def random_word(n):
        return "".join(rng.choice(BITS) for _ in range(n))

    for _ in range(128):
        rows = []
        for _ in range(5):
            n = rng.randrange(40)
            rows.append((random_word(n), rng.randrange(n + 2)))
        n = rng.randrange(65)
        req, rep = random_word(n), random_word(n)
        bill = check_contracted(rows[:3], rows[3:], req, rep, "L0" * 19)
        counts["contracted_receipts"] += 1
        counts["max_contracted_toll"] = max(bill, counts["max_contracted_toll"])
        check_reserve(req, rep, rows[3:], "L0" * 19, rng.randrange(n + 2))
        counts["reserve_receipts"] += 1
    counts.update(mixed_path())
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
