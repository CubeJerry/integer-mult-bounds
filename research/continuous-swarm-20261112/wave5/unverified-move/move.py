"""One complete selected MOVE24472 leaf as a fixed local transition graph.

Prepared for Jerry Chen / CubeJerry with substantial OpenAI assistance.
Apache-2.0. Source algebra, component tables and protected staging are credited
predecessors. Construction-time relabeling is absent from runtime control.
"""
from pathlib import Path
import hashlib
import importlib.util
import sys

HERE = Path(__file__).resolve().parent
PINS = {
    'components/c/leaf.py': 'bb46c1a55f1119957a52cd61f2cd957f3f7ad1e9b818c54a852bde09a0773744',
    'components/phase/phase.py': '2be149aa1be504509bb480f85396f0be302082d638e81422f747daee5a3c1ce7',
    'components/translation/translate.py': 'e2750fef8c2b9c8019d67285df3ca0d04340cd241782c7845665b7de621ca3bd',
    'components/linear/linear.py': 'd56704082b82e37d4a360b8aad7e0af63499f4160c6bbcfd338804453c46fa33',
}
for path, expected in PINS.items():
    if hashlib.sha256((HERE/path).read_bytes()).hexdigest() != expected:
        raise ValueError('frozen component source drift: '+path)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, HERE/path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


C = module('move_positive_C', 'components/c/leaf.py')
Q = module('move_quadratic_phase', 'components/phase/phase.py')
X = module('move_translation', 'components/translation/translate.py')
G = module('move_linear_maps', 'components/linear/linear.py')
Builder, Machine, Tape = C.Builder, C.Machine, C.Tape
BLANK, ONE, MARK = C.BLANK, C.ONE, C.MARK
HEADER, DATA, SHADOW = C.HEADER, C.DATA, C.A
ALPHABET = (BLANK, '0', ONE, MARK)

# These are fixed construction constants, not packet-dependent roles.
COHORTS = (
    ('right_phase', 29, 21),
    ('right_linear', 50, 25),
    ('right_translation', 75, 23),
    ('positive_C', 98, 27),
    ('left_phase', 125, 21),
    ('left_linear', 146, 25),
)
TAPE_COUNT = 171
PRIVATE = tuple(range(2, TAPE_COUNT))
LEFT_LINEAR = (2,) + (0,)*8
LEFT_ROWS = (0,)*9


def components():
    """Compile six fixed selected factors; runtime inputs never enter here."""
    return (
        Q.compile_phase(),
        G.compile_linear('right'),
        X.compile_translation(),
        C.compile_leaf(),
        Q.compile_phase(LEFT_LINEAR, LEFT_ROWS, 0),
        G.compile_linear('left'),
    )


def include(a, name, start, count, table, after):
    """Relabel each literal instruction once, preserving one-step prices."""
    code, alphabet = table
    if alphabet != ALPHABET:
        raise ValueError('component alphabet')
    ports = (HEADER, SHADOW) + tuple(range(start, start+count))
    if sum(instruction[0] == 'halt' for instruction in code) != 1:
        raise ValueError('component requires one successful halt')
    for pc, instruction in enumerate(code):
        a.mark(name+'_'+str(pc))
        op, *args = instruction
        if op == 'read':
            a.op(op, ports[args[0]],
                 {symbol: name+'_'+str(target) for symbol, target in args[1].items()})
        elif op in ('write', 'move'):
            a.op(op, ports[args[0]], args[1])
        elif op == 'goto':
            a.op(op, name+'_'+str(args[0]))
        elif op == 'halt':
            a.op('goto', after)
        else:
            raise ValueError('nonlocal component opcode')


def compile_move():
    """Fixed m9 MOVE24472 graph; no shape, source or recipe arguments."""
    a = Builder()
    for tape in C.PRIVATE:
        a.op('move', tape, -1)
        a.op('write', tape, MARK)
        a.op('move', tape, 1)
    C.gamma(a, C.F, (C.FBIN, C.FLEN))
    for tape in (C.R, C.P, C.S, C.WIDTH):
        C.gamma(a, tape)
    C.gamma_binary(a)
    C.trace_return(a, HEADER, C.HTRACE)
    C.cutoff_guard(a)
    for index in range(2):
        a.op('read', C.WIDTH, {ONE: 'outer_width'+str(index)})
        a.mark('outer_width'+str(index))
        a.op('move', C.WIDTH, 1)
    a.rewind(C.WIDTH, (ONE,))
    C.geometry(a)
    C.clone_source(a)
    for tape in (C.F, C.WIDTH, C.PREFIX, C.SUFFIX):
        C.clear(a, tape)
    tables = components()
    for index, ((name, start, count), table) in enumerate(zip(COHORTS, tables)):
        after = COHORTS[index+1][0]+'_0' if index+1 < len(COHORTS) else 'outer_commit'
        include(a, name, start, count, table, after)
    a.mark('outer_commit')
    C.commit(a, SHADOW)
    for tape in C.PRIVATE:
        a.op('move', tape, -1)
        a.op('write', tape, BLANK)
        a.op('move', tape, 1)
    a.op('halt')
    a.mark('reject')
    a.op('read', HEADER, {})
    return a.finish(ALPHABET)
