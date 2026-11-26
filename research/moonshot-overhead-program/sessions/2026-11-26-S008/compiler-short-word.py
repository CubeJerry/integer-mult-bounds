#!/usr/bin/env python3
"""Fixed physical short-word load/store and a separate finite arithmetic oracle."""

from pathlib import Path
import json
import random
import runpy

machine = runpy.run_path(str(Path(__file__).with_name('node-tapes.py')))
Builder = machine['Builder']
Action = machine['Action']
Simulation = machine['Simulation']
BLANK, HOME, HALT = machine['BLANK'], machine['HOME'], machine['HALT']
boundaries = machine['boundaries']


def build_access(store):
    """Construct a rule table once. No dimension or address enters this code."""
    b = Builder()
    tapes = ('memory', 'index', 'value', 'index_copy')
    done = boundaries(b, tapes, HALT, close=True)
    done = b.reset_group(('memory', 'value'), done)
    copy_word = b.label('selected word')
    source, target = ('value', 'memory') if store else ('memory', 'value')
    copy_actions = {
        bit: Action(copy_word, ((target, ('copy', source)),),
                    (('memory', 1), ('value', 1))) for bit in ('0', '1')
    }
    copy_actions[BLANK if store else '#'] = Action(done)
    b.sel(copy_word, source, copy_actions)

    erase = b.label('clear exhausted countdown')
    b.sel(erase, 'index_copy', {
        '1': Action(erase, (('index_copy', BLANK),), (('index_copy', -1),)),
        HOME: Action(copy_word, moves=(('index_copy', 1),)),
    })
    dec = b.label('decrement or detect zero')
    advance = b.label('skip one bank word')
    b.sel(advance, 'memory', {
        '#': Action(dec, moves=(('memory', 1),)),
        '0': Action(advance, moves=(('memory', 1),)),
        '1': Action(advance, moves=(('memory', 1),)),
    })
    b.sel(dec, 'index_copy', {
        '0': Action(dec, (('index_copy', '1'),), (('index_copy', 1),)),
        '1': Action(b.rewind('index_copy', advance), (('index_copy', '0'),)),
        BLANK: Action(erase, moves=(('index_copy', -1),)),
    })
    read_index = b.label('copy input address')
    reset = b.reset_group(('index', 'index_copy'), dec)
    b.sel(read_index, 'index', {
        BLANK: Action(reset),
        **{bit: Action(read_index, (('index_copy', bit),),
                       (('index', 1), ('index_copy', 1))) for bit in ('0', '1')},
    })
    return b, tapes, boundaries(b, tapes, read_index, close=False)


def bits(x, width):
    return format(x, f'0{width}b')[::-1]


def bank(records, width):
    return ''.join(bits(x, width) + '#' for x in records)


def test_one(program, store, width, words, index, value):
    image = {'memory': bank(words, width), 'value': bits(value, width), 'index': bits(index, width)}
    clock = index * (2 * width + 7) - 2 * index.bit_count() + 8 * width + 16
    execution = Simulation(program, image).execute(clock)
    assert execution.steps == clock
    assert clock <= 16 * (len(words) + 1) * (width + 2)
    expected = words.copy()
    if store:
        expected[index] = value
    assert execution.contents('memory') == bank(expected, width)
    assert execution.contents('value') == bits(value if store else words[index], width)
    assert execution.contents('index') == bits(index, width)
    assert execution.contents('index_copy') == ''
    assert all(cursor == 0 for cursor in execution.head.values())
    assert execution.visited == index * (width + 1) + 4 * width + 8
    return clock


def main():
    rng = random.Random(20261126)
    programs = tuple(build_access(store) for store in (False, True))
    checks = largest = 0
    for width in range(1, 9):
        for count in sorted({1, 2, min(2**width, 7), min(2**width, 32)}):
            for pattern in ('zero', 'one', 'independent'):
                words = [(0 if pattern == 'zero' else (2**width-1) if pattern == 'one'
                          else rng.randrange(2**width)) for _ in range(count)]
                for index in range(count):
                    for store, program in enumerate(programs):
                        val = rng.randrange(2**width)
                        largest = max(largest, test_one(program, store, width, words, index, val))
                        checks += 1
    print(json.dumps({'exact_head_traces': checks, 'largest_steps': largest,
                      'states_per_mode': [len(p[0].rules) for p in programs], 'tapes': 4}, sort_keys=True))


if __name__ == '__main__':
    main()
