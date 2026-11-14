#!/usr/bin/env python3
"""Independent B5 sparse-shadow machine, physical caller and direct CRT review.
Read-only. Retained numerical/radix components execute at their pinned boundary;
The primary adapter hardware and verifier are not imported. No predecessor
expected-output helper is called.
The parity-union-find oracle is reused from the separate frozen B4 review.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sys
import types

def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def canonical_network(permutation):
    """Canonical colors from input/output pair constraints, not source DFS."""
    n = len(permutation)
    need(n >= 2 and n & (n - 1) == 0, "dyadic oracle domain")
    need(sorted(permutation) == list(range(n)), "oracle permutation")
    if n == 2:
        return [(0, (permutation[0], permutation[0]))]
    parent, parity = list(range(n)), [0] * n
    def find(x):
        value = 0
        while parent[x] != x:
            value ^= parity[x]
            x = parent[x]
        return x, value
    def constrain(x, y):
        rx, px = find(x)
        ry, py = find(y)
        if rx == ry:
            need(px ^ py == 1, "odd canonical coloring cycle")
        else:
            parent[ry] = rx
            parity[ry] = px ^ py ^ 1
    for x in range(0, n, 2):
        constrain(x, x + 1)
    pairs = [[] for _ in range(n // 2)]
    for x, image in enumerate(permutation):
        pairs[image // 2].append(x)
    for pair in pairs:
        need(len(pair) == 2, "output pair degree")
        constrain(*pair)
    anchors, color = {}, []
    for x in range(n):
        root, value = find(x)
        if root not in anchors:
            anchors[root] = value
        color.append(value ^ anchors[root])
    first = tuple(color[x] ^ (x & 1) for x in range(n))
    last = [0] * n
    children = [[None] * (n // 2) for _ in range(2)]
    for x, image in enumerate(permutation):
        last[image] = color[x] ^ (image & 1)
        need(children[color[x]][x // 2] is None, "child input collision")
        children[color[x]][x // 2] = image // 2
    left, right = [canonical_network(child) for child in children]
    result = [(0, first)]
    for a, b in zip(left, right):
        need(a[0] == b[0], "child axis mismatch")
        result.append((a[0] + 1, tuple((a, b)[x & 1][1][x // 2] for x in range(n))))
    result.append((0, tuple(last)))
    for axis, table in result:
        need(all(table[x] == table[x ^ (1 << axis)] for x in range(n)),
             "oracle control depends on switched bit")
    for start in range(n):
        current = start
        for axis, table in result:
            current ^= table[current] << axis
        need(current == permutation[start], "independent network endpoint")
    return result

def rotation_network(h, s, a):
    n = 1 << h
    return canonical_network([(x + a) % s if x < s else x for x in range(n)])

PINS = {
    'adapter.py': '3cf2c39145adb91bcb8d40f08ff4e6f9d7ec80008f78bb34092b56effa1e6010',
    'caller.py': '055e86590e1cb03555f9ef6f1d585f8c23453a4cc10cd7feda7362c77f7bce1c',
    'inputs/switch/switch.py': '89fe721a2920943dbc58eefe7f855ac1573e653e8af3b029c9c2ef838fdeac40',
    'PROOF.md': 'a982d9e8243436a515f0a0d200c6060fe252c35b491d5ac4f7a378900bad501c',
    'SOURCE-PINS.json': 'ebf0af042033c46f4829fbb333299732094ce4b40008128660b9411cbc6ebdf6',
}
GRAPH_SHA = '2257055b689e0f88dca29532548639323dc3fa27a6e5150ea6652ed5636e07a2'
ALPHABET = set('_LR|01')

def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path.resolve())
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

def sources(directory):
    for name, digest in PINS.items():
        need(sha256((directory / name).read_bytes()).hexdigest() == digest, 'source changed: '+name)
    for pin in json.loads((directory / 'SOURCE-PINS.json').read_text())['files']:
        raw = (directory / pin['local']).read_bytes()
        need(len(raw) == pin['bytes'] and sha256(raw).hexdigest() == pin['sha256'],
             'retained source object differs from authenticated manifest: '+pin['local'])
    adapter = load(directory / 'adapter.py', 'independent_review_adapter')
    caller = load(directory / 'caller.py', 'independent_review_caller')
    base = load(directory / 'inputs/predecessor/research/encoded-crt-leaf-payload/replay.py',
                'independent_review_retained_source')
    model = base.modules()
    code, labels = adapter.compile_adapter()
    need(len(code) == 2500 and sha256(json.dumps(code, separators=(',', ':'),
         sort_keys=True).encode()).hexdigest() == GRAPH_SHA, 'emitted graph changed')
    for ins in code:
        op = ins[0]
        need(op in ('R', 'W', 'M', 'J', 'H'), 'nonliteral instruction')
        if op in ('R', 'W', 'M'):
            need(0 <= ins[1] < 20, 'physical role outside fixed graph')
        if op == 'R':
            need(set(ins[2]) == ALPHABET and all(0 <= q < len(code) for q in ins[2].values()),
                 'incomplete read alphabet/target')
        elif op == 'W':
            need(ins[2] in ALPHABET and ins[1] not in range(14, 18), 'borrowed or nonfixed write')
        elif op == 'M':
            need(ins[2] in (-1, 1), 'nonunit move')
        elif op == 'J':
            need(0 <= ins[1] < len(code), 'jump target')
        else:
            need(ins[1] in ('DONE', 'REJECT', 'MALFORMED'), 'unknown halt')
    core = load(directory / 'inputs/switch/switch.py', 'independent_review_frozen_core')
    original, old_labels = core.compile_query()
    start = labels['CORE_ENTRY']
    need(labels['CORE_DONE'] == start + len(original) and len(original) == 2096,
         'core is not a contiguous exact embedding')
    rename = {0: '0', 1: '1', 2: '_', 3: 'L', 4: '|'}
    for pc, ins in enumerate(original):
        op = ins[0]
        if op == 'R':
            branches = {rename[s]: start + q for s, q in ins[2].items()}
            branches['R'] = start + old_labels['reject']
            expected = ('R', ins[1], branches)
        elif op == 'W':
            expected = ('W', ins[1], rename[ins[2]])
        elif op == 'J':
            expected = ('J', start + ins[1])
        elif op == 'H':
            expected = ('J', labels['CORE_DONE' if ins[1] == 'DONE' else 'CORE_REJECT'])
        else:
            expected = ins
        need(code[start + pc] == expected and labels['core_'+str(pc)] == start + pc,
             'literal inherited instruction translation differs')
    return caller, base, model, code, labels

def observer_word(tape):
    need(tape.cells[0] == 'L', 'observer word origin')
    value, at = 0, 1
    while tape.cells[at] in ('0', '1'):
        value += (tape.cells[at] == '1') << (at - 1)
        at += 1
    need(tape.cells[at] in ('R', '|'), 'observer word endpoint')
    return value, at - 1

class SparsePoint:
    """Separate sparse PC engine checks and issues each actual physical action."""
    def __init__(self, code, labels, permit_wrong_bit=False, monitor=None, permit_stale_header=False):
        self.code, self.labels = code, labels
        self.calls = self.instructions = self.core_instructions = self.symbol_actions = 0
        self.permit_wrong_bit = permit_wrong_bit
        self.monitor, self.permit_stale_header = monitor, permit_stale_header
        self.runs, self.semantic_failures, self.coverage = [], [], set()

    def run(self, tapes, limit=10000000):
        count = 1 + max(ins[1] for ins in self.code if ins[0] in ('R', 'W', 'M'))
        need(len(tapes) == count and len({id(t.cells) for t in tapes}) == count,
             'distinct actual physical owners required')
        h, p = observer_word(tapes[14])
        s, ps = observer_word(tapes[15])
        a, pa = observer_word(tapes[16])
        j, pj = observer_word(tapes[17])
        x, hx = observer_word(tapes[18])
        k = tapes[19].head
        need(p == ps == pa == pj and hx == h and p >= h + 1 and 1 <= k <= h,
             'review fixture lacks matching framing')
        need(tapes[19].cells[:h + 2] == list('L'+'1' * h+'R'), 'width/header equality')
        if self.monitor is not None:
            self.monitor.before_point(p, a, self.permit_stale_header)
        before = [list(t.cells) for t in tapes]
        identities = [id(t.cells) for t in tapes]
        heads = [t.head for t in tapes]
        initial_heads = heads.copy()
        need(heads[:19] == [0] * 19, 'initial frame origins')
        ell = h.bit_length()
        maximum = [p + 1] + [h + 2] * 4 + [2, ell + 2] + [h + 3] * 7
        maximum += [p + 1, p + 1, p + 2, p + 1, h + 1, h + 1]
        if count == 21:
            maximum.append(h + 1)
        memory = {(role, pos): symbol for role, tape in enumerate(tapes)
                  for pos, symbol in enumerate(tape.cells) if symbol != '_'}
        low, high = heads.copy(), heads.copy()
        writes, guards = [0] * count, [[] for _ in tapes]
        pc = steps = core_steps = actions = 0
        produced = None
        while True:
            need(steps < limit and 0 <= pc < len(self.code), 'literal engine bound/PC')
            self.coverage.add(pc)
            if pc == self.labels['CORE_DONE']:
                symbol = memory.get((5, 1), '_')
                need(symbol in ('0', '1'), 'core returned no physical Boolean')
                produced = int(symbol)
            ins = self.code[pc]
            op = ins[0]
            core_steps += self.labels['CORE_ENTRY'] <= pc < self.labels['CORE_DONE']
            steps += 1
            pc += 1
            if op in ('R', 'W', 'M'):
                role = ins[1]
                need(tapes[role].head == heads[role] and 0 <= heads[role] <= maximum[role],
                     'physical head/window differs from sparse engine')
                actions += 1
            if op == 'R':
                symbol = memory.get((role, heads[role]), '_')
                need(tapes[role].read() == symbol, 'physical read differs from sparse memory')
                need(symbol in ins[2], 'read outside fixed alphabet')
                pc = ins[2][symbol]
            elif op == 'W':
                symbol = ins[2]
                tapes[role].write(symbol)
                writes[role] += 1
                if heads[role] == 0:
                    guards[role].append(symbol)
                if symbol == '_':
                    memory.pop((role, heads[role]), None)
                else:
                    memory[role, heads[role]] = symbol
            elif op == 'M':
                heads[role] += ins[2]
                need(0 <= heads[role] <= maximum[role], 'unit move crossed declared window')
                tapes[role].step(ins[2])
                low[role] = min(low[role], heads[role])
                high[role] = max(high[role], heads[role])
            elif op == 'J':
                pc = ins[1]
            elif op == 'H':
                status = ins[1]
                break
            else:
                raise RuntimeError('unknown fixed opcode')
        need([t.head for t in tapes] == heads == initial_heads, 'complete head return')
        need([id(t.cells) for t in tapes] == identities, 'physical point backing was replaced')
        observed_memory = {(role, pos): symbol for role, tape in enumerate(tapes)
                           for pos, symbol in enumerate(tape.cells) if symbol != '_'}
        need(observed_memory == memory, 'whole physical/sparse state differs')
        need(all(all(c == '_' for c in t.cells) for t in tapes[:14]), 'owned histories not blank')
        need(all(g == ['L', '_'] for g in guards[:14]), 'owned guards not installed/retired')
        need(all(w == 0 for w in writes[14:18]), 'borrowed numeric header write')
        changed = before[18].copy()
        if status == 'DONE':
            need(produced in (0, 1), 'missing consumed Boolean')
            changed[k] = str(int(changed[k]) ^ produced)
            need(writes[18:] == [1, 2] + ([0] if count == 21 else []), 'consume write inventory')
            overhead = 30 * p + 74 * h + 6 * ell + 10 * k + 261
            need(steps - core_steps == overhead, 'exact adapter overhead differs')
            need(steps <= 1024 * (h + 3) ** 2 + 128 * (p + h + 3), 'point bound exceeded')
            if h <= 6:
                expected = rotation_network(h, s, a)[j][1][x]
            else:
                need(s == 1 << h and a == 1 << (h - 1) and j == h - 1,
                     'large fixture must be a proved middle-row half turn')
                expected = 1
            if expected != produced:
                self.semantic_failures.append({'h': h, 's': s, 'a': a, 'j': j,
                                               'x': x, 'expected': expected, 'returned': produced})
                need(self.permit_wrong_bit, 'independent canonical point oracle mismatch')
        else:
            need(status == 'REJECT' and produced is None and writes[18] == 0 and writes[19] == 2,
                 'semantic rejection does not match stated cleanup')
        for role in range(14, count):
            need(tapes[role].cells == (changed if role == 18 else before[role]),
                 'borrowed frame/exterior or physical target changed unexpectedly')
        history = sum(len(t.cells) for t in tapes[:14])
        need(history <= sum(map(len, before[:14])) + p + 16 * (h + 4), 'retained history cap')
        run = {'status': status, 'instructions': steps, 'core_instructions': core_steps,
               'symbol_actions': actions, 'writes': writes, 'h': h, 'p': p, 's': s,
               'a': a, 'j': j, 'x': x, 'k': k, 'produced': produced,
               'retained_private_cells': history}
        self.calls += 1
        self.instructions += steps
        self.core_instructions += core_steps
        self.symbol_actions += actions
        self.runs.append(run)
        return run

def point_fixture(m, h, p, s, a, j, x, k, retained=0):
    def field(value, width, suffix='R'):
        bits = ''.join(str((value // (1 << i)) % 2) for i in range(width))
        return m.join.Tape(list('L'+bits+suffix+'_10L'))
    tapes = [m.join.Tape(['_'] * (retained + 1)) for _ in range(14)]
    tapes += [field(h, p), field(s, p), field(a, p, '|R'), field(j, p), field(x, h)]
    width = m.join.Tape(list('L'+'1' * h+'R_01L'))
    width.head = k
    return tapes + [width]

TAGS = (293, 730, 905, 3681)
WIDTHS = (3, 3, 2, 2)

def actual_fixture(m, moduli, values):
    """Independent external serializer; outside every measured caller boundary."""
    source = m.e.Port(m.w)
    fields = []
    for width, modulus, value in zip(WIDTHS, moduli, values):
        source.append(m.r.ROOT)
        for _ in range(width):
            source.append(m.w.ONE)
        source.append(m.r.WORD_END)
        for i in range(width):
            source.append((modulus // (1 << i)) % 2)
        source.append(m.r.WORD_END)
        locations = []
        for i in range(width):
            locations.append(source.head)
            source.append((value // (1 << i)) % 2)
        fields.append(tuple(locations))
        source.append(m.r.RECORD_END)
    source.append(m.w.RIGHT)
    source.rewind()
    source.cells.extend([m.w.ONE, m.w.ZERO, m.w.BLANK] * 3)
    words = [5]
    for position, tag in enumerate(TAGS):
        words.append(4096 + tag)
        words += [2 + (position // 2) % 2, 2 + position % 2]
    words.append(6)
    packet = [((word // (1 << i)) % 2) for word in words for i in range(13)]
    return source, m.bit_tape(packet), fields

def source_values(source, fields):
    return tuple(sum(source.cells[position] * (1 << i) for i, position in enumerate(field))
                 for field in fields)

def payload_values(payload):
    def word(at):
        return sum(payload.cells.get(13 * at + i, 0) * (1 << i) for i in range(13))
    need(word(0) == 5 and word(13) == 6, 'independent payload frame endpoints')
    result = []
    for item in range(4):
        at = 1 + 3 * item
        tag, high, low = word(at), word(at + 1), word(at + 2)
        need(4096 <= tag < 8192 and high in (2, 3) and low in (2, 3), 'payload/key code')
        result.append((2 * (high - 2) + low - 2, tag - 4096))
    return result

class LeaseMonitor:
    def __init__(self, m):
        self.m, self.active, self.staged, self.events, self.stale = m, {}, {}, [], []
        self.originals = (m.f.Iterator.next, m.f.NodeLease.close,
                          m.writer.Endpoint.stage, m.writer.Endpoint.commit)
        old_next, old_close, old_stage, old_commit = self.originals
        monitor = self
        def next_lease(iterator):
            lease = old_next(iterator)
            if lease is not None:
                need(iterator.live and iterator.bank.busy and not lease.closed, 'opened lease not live')
                stream = lease.actual.result['stream']
                monitor.active[id(iterator)] = (iterator, lease, bytes(iterator.source.cells),
                                               bytes(stream.cells), id(iterator.source.cells))
                monitor.events.append('open')
            return lease
        def stage(endpoint, lease):
            state = monitor.active[id(endpoint.iterator)]
            need(state[1] is lease and endpoint.iterator.live and not lease.closed,
                 'staging uses a different/retired lease')
            monitor.unchanged(state)
            answer = old_stage(endpoint, lease)
            monitor.unchanged(state)
            monitor.staged[id(endpoint.iterator)] = state
            monitor.events.append('stage')
            return answer
        def close(lease):
            iterator = lease.iterator
            need(monitor.active[id(iterator)][1] is lease and not lease.closed, 'wrong lease close')
            selected = id(iterator) in monitor.staged
            answer = old_close(lease)
            need(lease.closed and not iterator.live and not iterator.bank.busy, 'lease not fully retired')
            del monitor.active[id(iterator)]
            monitor.events.append('close_selected' if selected else 'close_skipped')
            return answer
        def commit(endpoint):
            iterator = endpoint.iterator
            state = monitor.staged[id(iterator)]
            need(state[1].closed and not iterator.live and not iterator.bank.busy,
                 'commit precedes numerical retirement')
            need(bytes(iterator.source.cells) == state[2], 'source changed before commit')
            answer = old_commit(endpoint)
            need(id(iterator.source.cells) == state[4] and not endpoint.pending,
                 'commit replaced backing or left staging pending')
            del monitor.staged[id(iterator)]
            monitor.events.append('commit')
            return answer
        m.f.Iterator.next, m.f.NodeLease.close = next_lease, close
        m.writer.Endpoint.stage, m.writer.Endpoint.commit = stage, commit

    def unchanged(self, state):
        iterator, lease, source, result, _ = state
        stream = lease.actual.result['stream']
        need(bytes(iterator.source.cells) == source and bytes(stream.cells) == result and
             iterator.source.head == 1 and stream.head == 1, 'live source/result disturbed')

    def before_point(self, p, offset, permit_stale):
        need(len(self.active) == 1, 'point requires one actual live numerical lease')
        state, = self.active.values()
        iterator, lease = state[:2]
        need(iterator.live and iterator.bank.busy and not lease.closed, 'point after retirement')
        self.unchanged(state)
        stream, guide = lease.actual.result['stream'], lease.actual.guide
        need(stream.cells[1] == self.m.r.ROOT and guide.head == 1 and
             list(guide.cells[1:p + 1]) == [self.m.w.ONE] * p and
             guide.cells[p + 1] == self.m.w.BLANK and
             iterator.counters['axis'].head == iterator.counters['half'].head == 1,
             'actual precision/offset frame and borrowed counter heads')
        bits = list(stream.cells[2:p + 2])
        need(all(b in (0, 1) for b in bits), 'actual numerical offset digits')
        actual = sum(b * (1 << i) for i, b in enumerate(bits))
        if actual != offset:
            self.stale.append({'actual_offset': actual, 'copied_offset': offset})
            need(permit_stale, 'header differs from actual live numerical result')

    def restore(self):
        self.m.f.Iterator.next, self.m.f.NodeLease.close, self.m.writer.Endpoint.stage, \
            self.m.writer.Endpoint.commit = self.originals

def actual_leg(caller, base, m, code, labels, source, payload, reverse, monitor, fault=None):
    selected = list(code)
    if fault == 'stale_wire':
        changed = []
        for pc in range(labels['COPY_X_START'], labels['COPY_X_END']):
            ins = selected[pc]
            if ins[0] in ('R', 'W', 'M') and ins[1] == 18:
                selected[pc] = (ins[0], 20, *ins[2:])
                changed.append(pc)
        need(changed, 'stale-wire emitted-table mutation changed nothing')
    point = SparsePoint(tuple(selected), labels, permit_wrong_bit=fault == 'stale_wire',
                        monitor=monitor, permit_stale_header=fault == 'stale_offset')
    start_event = len(monitor.events)
    receipt, owners = caller.run_leg(m, base, point, source, payload, reverse, fault=fault)
    events = monitor.events[start_event:]
    need(events[-3:] == ['stage', 'close_selected', 'commit'] and
         not monitor.active and not monitor.staged, 'actual final lease chronology')
    need(len(owners[0]) == 100 and len({id(v) for v in owners[0]}) == 100,
         'one hundred distinct retained actual owners')
    need(all(all(v in ('_', m.w.BLANK) for v in cells) for cells in owners[0]),
         'actual source/adapter histories not erased')
    need(all(t.head == 0 and not t.cells for t in owners[1]), 'radix buckets not returned/erased')
    need(all(machine.status == 'accept' and not any(machine.registers) for machine in owners[2]),
         'retained radix controls not retired')
    need(point.calls == 12 and point.instructions - point.core_instructions == 7012,
         'whole four-tag point bill')
    need(receipt['literal_query_instructions'] == point.instructions and
         receipt['query_symbol_actions_included_in_literal_bill'] == point.symbol_actions,
         'caller point bill differs from independent census')
    if fault is None:
        row_order = [2, 1, 0] if reverse else [0, 1, 2]
        for position in range(4):
            run = point.runs[3 * position:3 * position + 3]
            need([r['j'] for r in run] == row_order and [r['k'] for r in run] == [1, 2, 1],
                 'row/target route differs from exact palindrome')
            current = position
            for row in run:
                need(row['x'] == current and (row['h'], row['p'], row['s'], row['a']) == (2, 5, 3, 2),
                     'current wire or fresh current source headers differ')
                current ^= row['produced'] << (row['k'] - 1)
            expected = (position + (-2 if reverse else 2)) % 3 if position < 3 else position
            need(current == expected, 'direct CRT wire destination')
    return receipt, owners, point, events

def main():
    directory = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    caller, base, m, code, labels = sources(directory)
    point_records = []
    for h, p, s, a, j, x, k, history in (
        (1, 2, 1, 0, 0, 1, 1, 0),
        (3, 4, 8, 7, 4, 7, 1, 0),
        (5, 257, 17, 9, 6, 23, 3, 79),
        (3, 6, 5, 1, 1, 5, 3, 3),
        (17, 18, 1 << 17, 1 << 16, 16, (1 << 17) - 1, 17, 0),
        (2, 5, 0, 0, 0, 0, 1, 0),
    ):
        point = SparsePoint(code, labels)
        result = point.run(point_fixture(m, h, p, s, a, j, x, k, history))
        point_records.append({key: value for key, value in result.items() if key != 'writes'})
    monitor = LeaseMonitor(m)
    moduli, values = (5, 7, 2, 3), (3, 2, 1, 1)
    offset = values[2] * pow(moduli[2], -1, moduli[3]) % moduli[3]
    destinations = [(i + offset) % 3 if i < 3 else i for i in range(4)]
    expected_tags = sorted(zip(destinations, TAGS))
    source, payload, fields = actual_fixture(m, moduli, values)
    original = (bytes(source.cells), source.head, dict(payload.cells), payload.head)
    identities = id(source.cells), id(payload.cells)
    try:
        forward, fowners, fp, fevents = actual_leg(caller, base, m, code, labels,
                                                   source, payload, False, monitor)
        need(offset == 2 and payload_values(payload) == expected_tags and
             source_values(source, fields) == (3, 2, 1, 0), 'direct current CRT/tag oracle')
        inverse, iowners, ip, ievents = actual_leg(caller, base, m, code, labels,
                                                   source, payload, True, monitor)
        need((bytes(source.cells), source.head, dict(payload.cells), payload.head) == original and
             (id(source.cells), id(payload.cells)) == identities, 'whole physical two-sided restoration')
        histories = (*fowners[0], *iowners[0])
        need(len(histories) == 200 and len({id(c) for c in histories}) == 200,
             'both actual owner inventories remain charged')
        controls = []
        for fault in ('stale_offset', 'stale_wire'):
            src, pay, locs = actual_fixture(m, moduli, values)
            stale_before = len(monitor.stale)
            receipt, owners, machine, events = actual_leg(caller, base, m, code, labels,
                                                          src, pay, False, monitor, fault)
            wrong = payload_values(pay)
            need(wrong != expected_tags and source_values(src, locs) == (3, 2, 1, 0),
                 'returning mutation escaped direct CRT/tag oracle')
            if fault == 'stale_wire':
                need(machine.semantic_failures, 'stale wire did not change a predicate')
            else:
                need(len(monitor.stale) - stale_before == 12, 'stale offset not detected against live lease')
            controls.append({'fault': fault, 'returned_payload': wrong,
                'queries': machine.calls, 'canonical_predicate_mismatches': machine.semantic_failures,
                'live_lease_header_mismatches': len(monitor.stale) - stale_before,
                'all_owned_histories_and_heads_retired': True, 'events': events})
        src, pay, locs = actual_fixture(m, moduli, values)
        before_src, before_payload = bytes(src.cells), dict(pay.cells)
        actual_leg(caller, base, m, code, labels, src, pay, False, monitor)
        receipt, owners, machine, events = actual_leg(caller, base, m, code, labels,
                                                      src, pay, True, monitor, 'forward_rows_in_inverse')
        need(bytes(src.cells) == before_src and source_values(src, locs) == values and
             dict(pay.cells) != before_payload, 'wrong inverse order escaped full payload oracle')
        controls.append({'fault': 'forward_rows_in_inverse', 'source_fully_restored': True,
                         'payload_fully_restored': False, 'queries': machine.calls,
                         'all_owned_histories_and_heads_retired': True})
        src, pay, locs = actual_fixture(m, (5, 7, 3, 1), (3, 2, 1, 0))
        point = SparsePoint(code, labels, monitor=monitor)
        try:
            caller.run_leg(m, base, point, src, pay, False)
        except ValueError as error:
            need(str(error) == 'CRT modulus exceeds one' and point.calls == 0,
                 'wrong actual-source admission failure')
        else:
            raise RuntimeError('unit modulus unexpectedly passed retained source admission')
        controls.append({'fault': 'unit_modulus_source', 'message': 'CRT modulus exceeds one',
                         'point_calls': 0, 'scope': 'point permits unit modulus; actual source excludes it'})
        result = {'status': 'PASS', 'graph_sha256': GRAPH_SHA, 'locations': len(code), 'tapes': 20,
            'literal_core_embedding_checked_instructions': 2096,
            'independent_semantics': 'separate sparse state/PC engine checks and issues every actual Tape action',
            'independent_oracle': 'parity-union-find canonical network; modular inverse and independent 13-bit tag parser',
            'standalone_point_fixtures': point_records,
            'actual_moduli': moduli, 'actual_input': values, 'actual_offset': offset,
            'forward_destinations': destinations, 'forward_payload': expected_tags,
            'forward': forward, 'inverse': inverse,
            'forward_chronology': fevents, 'inverse_chronology': ievents,
            'full_source_payload_key_bytes_and_identities_restored': True,
            'both_retained_symbol_owners': len(histories),
            'both_retained_symbol_cells': sum(map(len, histories)),
            'source_retained_cells': len(source.cells), 'payload_retained_extent': payload.extent,
            'returning_controls': controls,
            'scope': 'Uniform point proof plus bounded actual caller review. Source and radix providers are pinned retained code, not independently reimplemented. Mixed cost vector; no new kappa.'}
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        monitor.restore()

if __name__ == '__main__':
    main()
