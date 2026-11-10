"""Fixed seven-symbol tables for the actual Controller's complete-row ABI.

The only compilation parameter is the fixed productive width w. Runtime row
count, format length, recursion depth and numerical values stay on tapes.
Prepared for Jerry Chen / CubeJerry with substantial OpenAI assistance.
Apache-2.0. See PROOF.md for supplied-format and homogeneous-geometry premises.
"""
ZERO, ONE, LEFT, SEP, END, BASE, BLANK = range(7)


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Builder:
    def __init__(self):
        self.code = {'reject': ('reject', 'coded whole-row contract')}

    def put(self, label, row):
        need(label not in self.code, 'unique finite label')
        self.code[label] = row
        return label

    def read(self, label, port, edges):
        return self.put(label, ('read', port, dict(edges), 'reject'))

    def actions(self, label, actions, following):
        for i, operation in enumerate(actions):
            after = label + ':' + str(i + 1) if i + 1 < len(actions) else following
            self.put(label + ':' + str(i), (*operation, after))
        return label + ':0'

    def rewind(self, label, port, marker, following):
        self.put(label + ':left', ('move', port, -1, label + ':read'))
        self.read(label + ':read', port,
                  {ZERO: label + ':left', ONE: label + ':left', marker: label + ':right'})
        self.put(label + ':right', ('move', port, 1, following))
        return label + ':left'

    def copy(self, label, source, target, source_marker, target_marker, following):
        """Copy one positive raw binary descriptor, preserving both heads."""
        end = self.rewind(label + ':target-rewind', target, target_marker, following)
        end = self.rewind(label + ':source-rewind', source, source_marker, end)
        edges = {}
        for bit in (ZERO, ONE):
            name = label + ':bit' + str(bit)
            start = self.actions(name + ':copy',
                                 [('write', target, bit), ('move', target, 1),
                                  ('move', source, 1)], label + ':loop')
            edges[bit] = self.read(name + ':blank', target, {BLANK: start})
        self.read(label + ':loop', source, {**edges, BLANK: end})
        return self.read(label + ':entry', source, edges)

    def row(self, label, source, guide, target, following):
        """One complete row, checked against its canonical zero-format guide.

Virtual0 has physical code000, virtual1 code001, component separator010.
Guide numeric codes must be000. Source numeric codes admit000/001. Every
component is nonempty and the row ends exactly after a complete separator.
target=None implements the same checked scan without producing output.
"""
        initial = (0, False, False, '')
        pending, seen = [initial], set()
        done = self.rewind(label + ':guide-rewind', guide, LEFT, following)

        def key(state):
            return label + ':state:' + ':'.join(map(str, state))

        while pending:
            state = pending.pop()
            if state in seen:
                continue
            seen.add(state)
            phase, inside, completed, kind = state
            options = {}
            if phase == 0:
                options[ZERO] = {ZERO: (1, inside, completed, '')}
            elif phase == 1:
                options[ZERO] = {ZERO: (2, inside, completed, 'bit')}
                if inside:
                    options[ONE] = {ONE: (2, inside, completed, 'separator')}
            elif kind == 'bit':
                options[ZERO] = {bit: (0, True, completed, '') for bit in (ZERO, ONE)}
            else:
                options[ZERO] = {ZERO: (0, False, True, '')}
            guide_edges = {}
            for guide_bit, source_options in options.items():
                source_edges = {}
                for source_bit, after in source_options.items():
                    pending.append(after)
                    name = key(state) + ':g' + str(guide_bit) + ':s' + str(source_bit)
                    actions = []
                    if target is not None:
                        actions += [('write', target, source_bit), ('move', target, 1)]
                    actions += [('move', source, 1), ('move', guide, 1)]
                    start = self.actions(name + ':actions', actions, key(after))
                    if target is not None:
                        start = self.read(name + ':blank', target, {BLANK: start})
                    source_edges[source_bit] = start
                guide_edges[guide_bit] = self.read(key(state) + ':source' + str(guide_bit),
                                                  source, source_edges)
            if phase == 0 and not inside and completed:
                guide_edges[BLANK] = done
            self.read(key(state), guide, guide_edges)
        return key(initial)


def compile_rows(width):
    """Return one fixed graph and four entry states, independent of B and R."""
    need(type(width) is int and width >= 2, 'fixed productive width at least two')
    guide, bridge, header = width, width + 1, width + 2
    b = Builder()
    b.put('done', ('halt', 'done'))
    b.put('leaf', ('halt', 'leaf'))
    b.put('inner', ('halt', 'inner'))
    ends = {value: b.rewind('classify:' + value, 0, LEFT, value)
            for value in ('leaf', 'inner')}
    frontier = b.read('classify:frontier', 0,
                      {BLANK: ends['leaf'], ZERO: ends['inner'], ONE: ends['inner']})
    classify = b.row('classify:row', 0, guide, None, frontier)
    prepare = b.copy('prepare', guide, header, LEFT, BASE, 'done')

    def finish(label):
        after = b.rewind(label + ':bridge', bridge, BASE, 'done')
        for port in reversed(range(width)):
            after = b.rewind(label + ':field' + str(port), port, LEFT, after)
        return after

    installed = finish('install:finish')
    next_row = 'install:loop'
    for port in reversed(range(width)):
        next_row = b.row('install:field' + str(port), bridge, guide, port, next_row)
    b.read('install:entry', bridge, {ZERO: next_row, ONE: next_row})
    b.read('install:loop', bridge, {ZERO: next_row, ONE: next_row, BLANK: installed})
    install = b.copy('install:format', header, guide, BASE, LEFT, 'install:entry')

    collected = finish('collect:finish')
    for port in reversed(range(1, width)):
        collected = b.read('collect:end' + str(port), port, {BLANK: collected})
    next_row = 'collect:loop'
    for port in reversed(range(width)):
        next_row = b.row('collect:field' + str(port), port, guide, bridge, next_row)
    collect = b.read('collect:entry', 0, {ZERO: next_row, ONE: next_row})
    b.read('collect:loop', 0, {ZERO: next_row, ONE: next_row, BLANK: collected})
    entries = dict(classify=classify, prepare=prepare, install=install, collect=collect)
    validate(b.code, entries, width + 3)
    return b.code, entries


def validate(code, entries, ports):
    need(all(label in code for label in entries.values()), 'closed entry labels')
    for row in code.values():
        op = row[0]
        if op in ('halt', 'reject'):
            need(len(row) == 2, 'terminal arity')
            continue
        need(op in ('read', 'write', 'move'), 'local finite instruction')
        need(type(row[1]) is int and 0 <= row[1] < ports, 'fixed physical port')
        if op == 'read':
            need(all(type(s) is int and 0 <= s < 7 for s in row[2]), 'seven-symbol alphabet')
            targets = (*row[2].values(), row[3])
        else:
            need(row[2] in ((-1, 1) if op == 'move' else range(7)), 'local action')
            targets = (row[3],)
        need(all(label in code for label in targets), 'closed transition graph')


def execute(code, entry, tapes, observer=None):
    """Literal finite-graph emulator. steps and observer never choose a branch."""
    state, steps = entry, 0
    while True:
        row = code[state]
        steps += 1
        if observer is not None:
            observer(state, row)
        op = row[0]
        if op == 'halt':
            return row[1], steps
        if op == 'reject':
            raise ValueError(row[1])
        tape = tapes[row[1]]
        if op == 'read':
            state = row[2].get(tape.read(), row[3])
        else:
            if op == 'write':
                tape.write(row[2])
            else:
                tape.move(row[2])
            state = row[3]


class RowServices:
    """Bind the exact Controller callback signatures to one static graph.

`payloads[format_role]` is a protected nondata role of that Controller, included
in its Stack bank. Header and bridge are the Controller's existing outer ports.
Structural identity tests are fixed ABI validation, not a snapshot admission.
"""
    def __init__(self, payloads, public_count, format_role, bridge, child_header, observe=None):
        need(type(format_role) is int and public_count <= format_role < len(payloads),
             'separate protected format role')
        self.public = tuple(payloads[:public_count])
        self.guide, self.bridge, self.header = payloads[format_role], bridge, child_header
        self.tapes = self.public + (self.guide, bridge, child_header)
        need(len({id(t) for t in self.tapes}) == len(self.tapes), 'distinct row-service ports')
        self.code, self.entries = compile_rows(public_count)
        self.observe = observe  # Optional checker; absent from the machine theorem.

    def invoke(self, name):
        value, steps = execute(self.code, self.entries[name], self.tapes)
        if self.observe is not None:
            self.observe(name, steps)
        return value

    def is_leaf(self, token):
        return self.invoke('classify') == 'leaf'

    def prepare(self, token, child_header):
        need(child_header is self.header, 'actual staged header')
        self.invoke('prepare')

    def install(self, bridge, child_header, productive):
        need(bridge is self.bridge and child_header is self.header
             and len(productive) == len(self.public)
             and all(a is b for a, b in zip(productive, self.public)), 'actual install ports')
        self.invoke('install')

    def collect(self, productive, bridge):
        need(len(productive) == len(self.public)
             and all(a is b for a, b in zip(productive, self.public))
             and bridge is self.bridge, 'actual collect ports')
        self.invoke('collect')


def costs(width, row_bits, rows):
    """Analysis only: runtime services never call this function."""
    need(width >= 2 and row_bits >= 1 and rows >= width and rows % width == 0,
         'complete nonleaf rows')
    length = row_bits * rows
    return dict(classify=8 * row_bits + 9, prepare=9 * row_bits + 8,
                install=13 * length + 4 * rows + rows // width + 9 * row_bits + 3 * width + 12,
                collect=13 * length + 4 * rows + rows // width + 4 * width + 4)
