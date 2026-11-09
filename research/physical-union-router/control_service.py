"""Cheap independent physical line target used only for router controls.
The optional endpoint NAND is nonlinear and axis-order sensitive. It is not
an approximation to a Gaussian service. Prepared for @CubeJerry, OpenAI aid.
"""
from cardinal_counts import Count
from compact_counts import copy_bits
from encoded import compare, subtract
from records import Tape
from router_metadata import indices, owned
from scratch_pool import ScratchPool
from session import (OuterScope, borrowed_count, borrowed_tape, erase_marker,
                     initialize_marker, sealed_constructors)
from words import BLANK, need
from fast_boundary import origin
from window_tapes import line
from union_bits import bit, skip_bits


class ControlService:
    def __init__(self, nonlinear=True):
        self.nonlinear = nonlinear
        self.pool = ScratchPool(128); self.scope = OuterScope(self.pool)
        self.archive, self.real, self.imaginary, self.output = (Tape() for _ in range(4))
        self.closed, self.pending, self.calls, self.lines = True, False, 0, 0
        for tape in self.forbidden():
            erase_marker(tape)

    def forbidden(self):
        return (*self.pool.tapes, self.archive, self.real, self.imaginary, self.output)

    def idle(self):
        need(self.closed and not self.pending and not self.pool.live
             and self.output.read() == BLANK, 'consume physical control return')

    def consume(self):
        need(self.closed and self.pending, 'pending physical control return')
        self.output.clear(); erase_marker(self.output); self.pending = False
        self.idle()

    def run(self, source, e_table, mask, shear_pages, schur_pages,
            axes, h, tag_bits, axis, round_index, length, selected, block, width, precision):
        sources = tuple(borrowed_tape(tape) for tape in
                        (source, e_table, mask, *shear_pages, *schur_pages))
        source, e_table, mask = sources[:3]
        metadata = tuple(borrowed_count(c) for c in
                         (axes, h, tag_bits, axis, round_index, length, selected, block, width, precision))
        axes, h, tag_bits, axis, round_index, length, selected, block, width, precision = metadata
        ports = (*sources, *(value.tape for value in metadata))
        need(len(set(sources)) == len(sources) and all(t not in self.forbidden() for t in ports),
             'external distinct control ports')
        self.idle()
        for tape in ports:
            origin(tape)
        for tape in self.forbidden():
            initialize_marker(tape)
        self.closed = False; success = False
        try:
            with sealed_constructors(), self.scope.installed():
                with owned(Count.product(axes, h), Count(tag_bits),
                           Count.literal(1)) as (header_bits, tags, one):
                    header_bits.multiply_small(2); header_bits.add(axes)
                    tags.multiply_small(2); header_bits.add(tags)
                    header_bits.increment(); header_bits.increment()
                    with owned(subtract(width, one)) as (tail,):
                        while source.read() != BLANK:
                            line(source, self.archive, self.real, self.imaginary,
                                 e_table, mask, axes, h, tag_bits, axis, round_index,
                                 length, selected, width, self.pool)
                            first = last = 0
                            for ordinal in indices(length):
                                digit = bit(self.real)
                                if ordinal.zero():
                                    first = digit
                                last = digit
                                skip_bits(self.real, tail)
                            need(self.real.read() == BLANK, 'complete endpoint control words')
                            changed = 1 - (first & last)
                            self.archive.rewind()
                            for ordinal in indices(length):
                                copy_bits(self.archive, self.output, header_bits)
                                digit = bit(self.archive)
                                self.output.append(changed if self.nonlinear and ordinal.zero() else digit)
                                copy_bits(self.archive, self.output, tail)
                                copy_bits(self.archive, self.output, width)
                            need(self.archive.read() == BLANK, 'complete control return')
                            for tape in (self.archive, self.real, self.imaginary):
                                tape.clear()
                            self.lines += 1
                success = self.pending = True; self.calls += 1
        finally:
            for tape in ports:
                tape.rewind()
            for tape in (self.archive, self.real, self.imaginary):
                tape.clear()
            self.pool.empty()
            for tape in (*self.pool.tapes, self.archive, self.real, self.imaginary):
                erase_marker(tape)
            self.output.rewind()
            if not success:
                self.output.clear(); erase_marker(self.output); self.pending = False
            self.closed = True
        return self.output
