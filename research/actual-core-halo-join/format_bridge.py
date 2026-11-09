"""Literal linear signed-format/grid bridge between two retained tape ABIs.

Every payload decision observes a current cell or finite carry/sign flag.
Widths and shifts are actual short Count ports. No payload integer is decoded.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from cardinal_counts import Count, positive
from encoded import compare, subtract
from router_metadata import indices, owned
from records import Tape
from scratch_pool import ScratchPool
from session import OuterScope, erase_marker, initialize_marker, sealed_constructors
from words import BLANK, need


def bbit(tape):
    value = tape.read()
    need(value in ('0', '1'), 'complete sign-magnitude digit')
    tape.move(1)
    return value == '1'


def nbit(tape):
    value = tape.read()
    need(value in (0, 1), 'complete two-complement digit')
    tape.step(1)
    return bool(value)


def complemented(bit, negative, carry):
    value = bit != negative
    return value != carry, value and carry


class FormatBridge:
    def __init__(self, binary_transport):
        self.B = binary_transport
        self.pool = ScratchPool(64)
        self.scope = OuterScope(self.pool)
        self.input = Tape()
        self.scratch = Tape()
        for tape in self.forbidden():
            erase_marker(tape)

    def forbidden(self):
        return (*self.pool.tapes, self.input, self.scratch)

    def begin(self):
        need(not self.pool.live and self.scratch.read() == BLANK,
             'quiescent format bridge')
        for tape in (*self.pool.tapes, self.scratch):
            initialize_marker(tape)

    def end(self):
        self.scratch.clear()
        self.pool.empty()
        for tape in (*self.pool.tapes, self.scratch):
            erase_marker(tape)

    def lift_word(self, source, target, halo_width, core_width, shift):
        negative = bbit(source)
        nonzero = False
        with owned(Count.literal(1)) as (one,):
            with owned(subtract(halo_width, one), Count(halo_width)) as (magnitude, used):
                positive(magnitude)
                used.add(shift)
                need(compare(used, core_width) <= 0, 'funded exact lifted signed carrier')
                for _ in indices(magnitude):
                    nonzero = bbit(source) or nonzero
                need(not negative or nonzero, 'reject sign-magnitude negative zero')
                carry = negative
                for _ in indices(shift):
                    value, carry = complemented(False, negative, carry)
                    target.append(int(value))
                source.move(-1)
                for _ in indices(magnitude):
                    value = source.read()
                    need(value in ('0', '1'), 'reverse magnitude digit')
                    digit, carry = complemented(value == '1', negative, carry)
                    target.append(int(digit))
                    source.move(-1)
                need(source.read() == ('1' if negative else '0'), 'restored sign position')
                source.move(1)
                for _ in indices(magnitude):
                    source.move(1)
                with owned(subtract(core_width, used)) as (extra,):
                    # used includes the mandatory sign digit.
                    digit, carry = complemented(False, negative, carry)
                    need(digit == negative, 'lifted signed top bit')
                    target.append(int(digit))
                    for _ in indices(extra):
                        digit, carry = complemented(False, negative, carry)
                        target.append(int(digit))

    def lift(self, source, halo_width, core_width, q, P):
        positive(halo_width); positive(core_width)
        need(compare(P, q) >= 0, 'exact incoming grid lift')
        need(self.input.read() == BLANK, 'consume prior bridge input')
        self.begin()
        initialize_marker(self.input)
        succeeded = False
        try:
            with sealed_constructors(), self.scope.installed():
                with owned(subtract(P, q)) as (shift,):
                    self.B.home(source)
                    while source.read() != '!':
                        for _ in (0, 1):
                            self.lift_word(source, self.input, halo_width, core_width, shift)
                        need(source.read() == '#', 'complete complex source record')
                        source.move(1)
                    self.B.home(source)
                    self.input.rewind()
                    succeeded = True
        finally:
            self.B.home(source)
            self.end()
            if not succeeded:
                self.input.clear(); erase_marker(self.input)
        return self.input

    def return_word(self, source, target, halo_width, core_width, drop):
        with owned(Count.literal(1)) as (one,):
            with owned(subtract(core_width, one), subtract(halo_width, one)) as (last, magnitude):
                positive(magnitude)
                for _ in indices(last):
                    source.step(1)
                sign = source.read()
                need(sign in (0, 1), 'two-complement sign digit')
                negative = bool(sign)
                for _ in indices(last):
                    source.step(-1)
                discard = drop if compare(drop, core_width) <= 0 else core_width
                with owned(subtract(core_width, discard)) as (keep,):
                    low = keep if compare(keep, magnitude) <= 0 else magnitude
                    with owned(subtract(keep, low), subtract(magnitude, low)) as (overflow, padding):
                        carry = negative
                        for _ in indices(discard):
                            _, carry = complemented(nbit(source), negative, carry)
                        nonzero = False
                        for _ in indices(low):
                            value, carry = complemented(nbit(source), negative, carry)
                            self.scratch.append(int(value)); nonzero = value or nonzero
                        for _ in indices(overflow):
                            value, carry = complemented(nbit(source), negative, carry)
                            need(not value, 'normalized sign-magnitude carrier overflow')
                        for _ in indices(padding):
                            self.scratch.append(0)
                        self.B.append(target, '1' if negative and nonzero else '0')
                        self.scratch.step(-1)
                        for _ in indices(magnitude):
                            value = self.scratch.read()
                            need(value in (0, 1), 'stored absolute-value digit')
                            self.B.append(target, '1' if value else '0')
                            self.scratch.step(-1)
                        self.scratch.step(1)
                        self.scratch.clear()

    def normalized_return(self, source, target, halo_width, core_width, drop):
        positive(halo_width); positive(core_width)
        self.begin()
        succeeded = False
        try:
            with sealed_constructors(), self.scope.installed():
                self.B.clear(target)
                source.rewind()
                while source.read() != BLANK:
                    for _ in (0, 1):
                        self.return_word(source, target, halo_width, core_width, drop)
                    self.B.append(target, '#')
                self.B.home(target); source.rewind()
                succeeded = True
        finally:
            source.rewind()
            if not succeeded:
                self.B.clear(target)
            self.B.home(target)
            self.end()

    def clear_input(self):
        self.input.clear(); erase_marker(self.input)
