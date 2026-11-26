#!/usr/bin/env python3
"""Literal finite-head extraction of the binary Fourier kernel's query sign word."""

import itertools
import json
from pathlib import Path
import random
import runpy


TAPES = runpy.run_path(str(Path(__file__).with_name('node-tapes.py')))
Builder, Action, Simulation = (TAPES[n] for n in ('Builder', 'Action', 'Simulation'))
BLANK, HALT = TAPES['BLANK'], TAPES['HALT']


def compile_key():
    """Input C, MX, MZ, Q. Output U. R is the independent second address head."""
    b = Builder()
    tapes = ('C', 'R', 'MX', 'MZ', 'Q', 'U')
    done = TAPES['boundaries'](b, tapes, HALT, close=True)
    done = b.reset_group(('MX', 'MZ', 'Q', 'U'), b.erase('R', done))
    entry = [b.label('next slot pair') for _ in range(2)]
    states = tuple(itertools.product(range(2), repeat=3))
    scan_x = {st: b.label('seek first operand') for st in states}
    scan_z = {(common, query, parity, x): b.label('seek second operand')
              for common, query, parity in states for x in range(2)}
    for common, query, parity in states:
        st = (common, query, parity)
        if query:
            emit = b.op(entry[common], (('U', str(common ^ parity)),),
                        (('U', 1), ('Q', 1)), 'one distinguished query')
        else:
            emit = b.op(entry[common ^ parity], moves=(('Q', 1),), name='common auxiliary')
        end_pair = b.reset_group(('C', 'R'), emit)
        flush_z = b.label('finish second mask extent')
        b.sel(flush_z, 'R', {BLANK: Action(end_pair)},
              Action(flush_z, moves=(('R', 1), ('MZ', 1))))
        x_value = b.label('remember one address bit')
        b.sel(x_value, 'C', {str(x): Action(scan_z[common, query, parity, x],
              moves=(('C', 1), ('MX', 1))) for x in range(2)})
        x_mask = b.label('first slot mask')
        b.sel(x_mask, 'MX', {'0': Action(scan_x[st], moves=(('C', 1), ('MX', 1))),
                             '1': Action(x_value)})
        b.sel(scan_x[st], 'C', {BLANK: Action(flush_z)}, Action(x_mask))
        for x in range(2):
            pair = b.label('accumulate scalar product')
            b.sel(pair, 'R', {str(z): Action(scan_x[common, query, parity ^ (x & z)],
                  moves=(('R', 1), ('MZ', 1))) for z in range(2)})
            zstate = scan_z[common, query, parity, x]
            b.sel(zstate, 'MZ', {'0': Action(zstate, moves=(('R', 1), ('MZ', 1))),
                                 '1': Action(pair)})
    for common in range(2):
        b.sel(entry[common], 'Q', {BLANK: Action(done),
              '0': Action(scan_x[common, 0, 0]), '1': Action(scan_x[common, 1, 0])})
    clone = b.label('copy the current full counter once')
    b.sel(clone, 'C', {BLANK: Action(b.reset_group(('C', 'R'), entry[0]))},
          Action(clone, (('R', ('copy', 'C')),), (('C', 1), ('R', 1))))
    return b, tapes, TAPES['boundaries'](b, tapes, clone, close=False)


def fixture(program, address, distinguished, auxiliaries, columns, leading, trailing, interleaved):
    d = distinguished + auxiliaries
    k = leading + 2*d*columns + trailing
    assert len(address) == k
    def position(half, slot, column):
        if interleaved:
            return leading + (column*2 + half)*d + slot
        return leading + (half*d + slot)*columns + column
    paired_slots = tuple(range(distinguished, d)) + tuple(range(distinguished))
    masks = []
    for half in range(2):
        table = []
        for slot in paired_slots:
            word = ['0']*k
            for column in range(columns):
                word[position(half, slot, column)] = '1'
            table.append(''.join(word))
        masks.append(''.join(table))
    inputs = dict(C=address, MX=masks[0], MZ=masks[1], Q='0'*auxiliaries+'1'*distinguished)
    sim = Simulation(program, inputs).execute(32*(d+1)*(k+2))
    def dot(slot):
        return sum((address[position(0, slot, c)] == '1') and (address[position(1, slot, c)] == '1')
                   for c in range(columns)) % 2
    common = sum(dot(i) for i in range(distinguished, d)) % 2
    correct = ''.join(str(common ^ dot(j)) for j in range(distinguished))
    assert sim.contents('U') == correct
    for tape in sim.tapes:
        assert sim.head[tape] == 0
        if tape != 'U':
            assert sim.contents(tape) == inputs.get(tape, '')
    assert sim.visited <= 2*d*k + 2*k + d + distinguished + 12
    return sim.contents('U'), sim.steps, sim.visited


def main():
    program = compile_key()
    rng = random.Random(0x508)
    cases = steps = max_cells = 0
    shapes = ((1, 0, 1, 0, 3), (1, 1, 1, 1, 0), (3, 0, 1, 0, 0),
              (3, 1, 1, 0, 0), (3, 1, 2, 3, 2), (7, 2, 4, 2, 3),
              (15, 4, 3, 1, 2), (63, 3, 2, 1, 3))
    for m, aux, f, pre, post in shapes:
        k = pre + 2*(m+aux)*f + post
        if k <= 8:
            words = [format(n, f'0{k}b') for n in range(1 << k)]
        else:
            words = ['0'*k, '1'*k, ''.join(str(i % 2) for i in range(k))]
            words += [format(rng.getrandbits(k), f'0{k}b') for _ in range(7)]
        for layout in (False, True):
            for address in words:
                key, elapsed, cells = fixture(program, address, m, aux, f, pre, post, layout)
                assert len(key) == m
                cases += 1
                steps += elapsed
                max_cells = max(max_cells, cells)
    print(json.dumps(dict(cases=cases, head_transitions=steps, peak_cells=max_cells,
                          states=len(program[0].rules), tapes=len(program[1])), sort_keys=True))


if __name__ == '__main__':
    main()
