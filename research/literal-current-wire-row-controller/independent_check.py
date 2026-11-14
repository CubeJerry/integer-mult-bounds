#!/usr/bin/env python3
"""Separate sparse physical interpreter for the complete literal row controller.
Read-only default; no author hardware/verifier/oracle imported. The canonical
parity-union-find oracle and external fixture serializer are reused verbatim
from the independently reviewed B5 checker (SHA 0d405f3621e50a71c1990f59c246268b11fdf4d3a32312500538fbfb5b24a8a7).
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from collections import Counter
from hashlib import sha256, sha1
from pathlib import Path
import argparse
import ast
import json
import sys
import types


def need(ok, reason):
    if not ok:
        raise ValueError(reason)

TAGS = (293, 730, 905, 3681)
WIDTHS = (3, 3, 2, 2)

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


PINS = {
    'controller.py':'efc3d8b0d089a56765f3eb6a2cc2a641a99f257a58f069a4d26fe5c912b1abd3',
    'hardware.py':'8870da2142377a891ff9730a7868616e3eb1cf2b20a39440cc540548feceb10e',
    'join.py':'95f4d2bd4f2ae2a761381eee0c36c9b8d2aa6140ba9cbb0830bca2794c88df9d',
    'PROOF.md':'33f4340322be07b7000ef3ac089e25c3a853a7a8ca2f9f2aecabe6e230856bba',
    'inputs/point/adapter.py':'3cf2c39145adb91bcb8d40f08ff4e6f9d7ec80008f78bb34092b56effa1e6010',
    'inputs/point/caller.py':'055e86590e1cb03555f9ef6f1d585f8c23453a4cc10cd7feda7362c77f7bce1c',
}
GRAPH = 'f8f0bd615531c914efc110d8a9d5ce2fafa2b00c8a568bdbfb86bf24868a0ef7'
ALPHABET = set('_LR|01')


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path.resolve())
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def sources(directory):
    for name, digest in PINS.items():
        need(sha256((directory/name).read_bytes()).hexdigest() == digest, 'Frozen source '+name)
    pins = json.loads((directory/'SOURCE-PINS.json').read_bytes())['files']
    for pin in pins:
        data = (directory/pin['local']).read_bytes()
        need(len(data) == pin['bytes'] and sha256(data).hexdigest() == pin['sha256']
             and sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == pin['git_blob'], 'Retained input integrity')
    constructor = load(directory/'controller.py', '_review_row_constructor')
    code, labels, metadata = constructor.compile_controller()
    need(len(code) == 10123 and constructor.digest(code) == GRAPH, 'Exact emitted graph')
    point = constructor.point_source()
    old, old_labels = point.compile_adapter()
    need(len(old) == 2500 and point.digest(old) == constructor.POINT_GRAPH, 'Exact predecessor graph')
    need(metadata['entries'] == {'FORWARD':0,'INVERSE':13} and metadata['tapes'] == 20, 'Entry/owner inventory')
    covered = set()
    for mode, place in metadata['point_copies'].items():
        start, after = place['start'], place['after']
        need(place['length'] == len(old), 'Complete point range')
        for i, ins in enumerate(old):
            if ins[0] == 'R':
                expected = ('R', ins[1], {s:start+target for s,target in ins[2].items()})
            elif ins[0] == 'J':
                expected = ('J', start+ins[1])
            elif ins == ('H','DONE'):
                expected = ('J', after)
            else:
                expected = ins
            need(code[start+i] == expected, 'Literal point translation: '+mode)
            need(start+i not in covered, 'Disjoint fixed control copies')
            covered.add(start+i)
    need(covered == set(range(123,10123)), 'Exactly 123 controller locations')
    for ins in code:
        need(ins[0] in ('R','W','M','J','H'), 'Literal opcode')
        if ins[0] in ('R','W','M'):
            need(type(ins[1]) is int and 0 <= ins[1] < 20, 'Static physical port')
        if ins[0] == 'R':
            need(set(ins[2]) == ALPHABET and all(0 <= k < len(code) for k in ins[2].values()), 'Total fixed read branches')
        elif ins[0] == 'M':
            need(ins[2] in (-1,1), 'Unit move')
        elif ins[0] == 'W':
            need(ins[2] in ALPHABET and ins[1] not in (14,15,16), 'Borrowed input preservation')
        elif ins[0] == 'J':
            need(0 <= ins[1] < len(code), 'Fixed jump')
    join = load(directory/'join.py', '_review_row_join')
    joined = join.bind()
    original = (directory/'inputs/point/caller.py').read_text()
    before, tail = original.split('def route_address(',1)
    removed, after = tail.split('def prepare_keys(',1)
    adapted = before+join.REPLACEMENT+'def prepare_keys('+after
    old_ast, new_ast = ast.parse(original), ast.parse(adapted)
    def retained(tree):
        return [ast.dump(n,include_attributes=False) for n in tree.body
                if not (isinstance(n,ast.FunctionDef) and n.name == 'route_address')]
    need(retained(old_ast) == retained(new_ast), 'Only the declared caller function changed')
    return code, labels, metadata, joined, len(pins)


class Tape:
    """Independent physical list owner; single-action interface only."""
    def __init__(self, cells, head=0):
        self.cells, self.head = list(cells), head
    def read(self):
        return self.cells[self.head]
    def write(self, value):
        self.cells[self.head] = value
    def step(self, direction):
        self.head += direction
        need(self.head >= 0, 'Physical left boundary')
        if self.head == len(self.cells):
            self.cells.append('_')


def field(value, width, suffix='R'):
    return list('L'+''.join(str((value >> i)&1) for i in range(width))+suffix)


def fixture(h, p, s, a, x, history=0, translated=False):
    tapes = []
    for role in range(20):
        prefix = list('R01L'*(1+role%3)) if translated else []
        origin = len(prefix)
        if role < 14:
            body = ['_']*max(history,p+h+10) if history or translated else ['_']
        elif role == 14: body = field(h,p)
        elif role == 15: body = field(s,p)
        elif role == 16: body = field(a,p,'|R')
        elif role == 17: body = list('L'+''.join(str((i+role)%2) for i in range(p))+'R')
        elif role == 18: body = field(x,h)
        else: body = list('L'+'1'*h+'R')
        suffix = list('_R|10L') if role >= 14 or history or translated else []
        tapes.append(Tape(prefix+body+suffix,origin))
    return tapes


def value(cells, origin, width):
    need(cells[origin] == 'L' and all(x in '01' for x in cells[origin+1:origin+width+1]), 'Observer field framing')
    return sum((cells[origin+1+i] == '1') << i for i in range(width))


def width(cells, origin):
    i = origin+1
    while cells[i] in '01':
        i += 1
    need(cells[i] in ('R','|'), 'Observer field end')
    return i-origin-1


class SparseController:
    def __init__(self, code, labels, metadata, permit_semantic_fault=False):
        self.code, self.labels, self.meta = code, labels, metadata
        self.permit_semantic_fault = permit_semantic_fault
        self.calls = self.routes = self.instructions = self.core_instructions = 0
        self.symbol_actions = self.point_instructions = 0
        self.records = []

    def run(self, tapes, direction='FORWARD', limit=20000000):
        need(direction in ('FORWARD','INVERSE'), 'Known direction')
        count = 1+max(ins[1] for ins in self.code if ins[0] in ('R','W','M'))
        need(len(tapes) == count and len({id(t.cells) for t in tapes}) == count, 'Distinct owner objects')
        origins = [t.head for t in tapes]
        before = [list(t.cells) for t in tapes]
        backing = [id(t.cells) for t in tapes]
        p = width(before[14],origins[14])
        h = value(before[14],origins[14],p)
        s, a = [value(before[i],origins[i],p) for i in (15,16)]
        x = value(before[18],origins[18],h)
        need(h >= 1 and p >= h+1 and before[19][origins[19]:origins[19]+h+2] == list('L'+'1'*h+'R'), 'Successful header/width fixture domain')
        need(all(width(before[i],origins[i]) == p for i in (15,16,17)), 'Matching p-bit fields')
        rows = rotation_network(h,s,a) if 1 <= s <= 1<<h and 0 <= a < s else None
        lengths = [p+2]+[h+3]*4+[3,h.bit_length()+3]+[h+4]*7
        lengths += [p+2,p+2,p+3,p+2,h+2,h+2]
        lengths += [h+2]*(count-20)
        cap = [o+n-1 for o,n in zip(origins,lengths)]
        heads = origins.copy()
        high = origins.copy()
        memory = {(i,j):x for i,t in enumerate(tapes) for j,x in enumerate(t.cells) if x != '_'}
        starts = {v['start']:k for k,v in self.meta['point_copies'].items()}
        after = {v['after']:k for k,v in self.meta['point_copies'].items()}
        inner = self.meta['point_labels']
        core_entries = {v['start']+inner['CORE_ENTRY'] for v in self.meta['point_copies'].values()}
        core_done = {v['start']+inner['CORE_DONE'] for v in self.meta['point_copies'].values()}
        core_ranges = [(v['start']+inner['CORE_ENTRY'],v['start']+inner['CORE_DONE']) for v in self.meta['point_copies'].values()]
        core_at = tuple(any(lo <= pc < hi for lo,hi in core_ranges) for pc in range(len(self.code)))
        pc = self.meta['entries'][direction]
        steps = actions = point_steps = core_steps = 0
        writes = [0]*count
        visits, faults = [], []
        pending = None
        expected_current = x
        def observe(ok, reason):
            if not ok:
                faults.append(reason)
                need(self.permit_semantic_fault, reason)
        while True:
            need(steps < limit and 0 <= pc < len(self.code), 'Bounded literal run')
            if pc in starts:
                r = len(visits)
                wanted_j = r if direction == 'FORWARD' else 2*h-2-r
                actual_j = value(tapes[17].cells,origins[17],p)
                actual_x = value(tapes[18].cells,origins[18],h)
                k = tapes[19].head-origins[19]
                observe(0 <= wanted_j < 2*h-1, 'Query count exceeded Q')
                observe(actual_j == wanted_j, 'Wrong encoded row at query')
                observe(k == 1+min(r,2*h-2-r), 'Wrong physical target cursor')
                observe(actual_x == expected_current, 'Wrong current address at query')
                observe(starts[pc] == direction+('_ASC' if r < h else '_DESC'), 'Wrong direction/mode')
                need(heads[:19] == origins[:19], 'Point entry heads')
                want_bit = rows[wanted_j][1][expected_current] if rows is not None and 0 <= wanted_j < len(rows) else None
                pending = {'row':actual_j,'wire':actual_x,'target':k,'mode':starts[pc],
                           'wanted_row':wanted_j,'wanted_wire':expected_current,'want_bit':want_bit,
                           'point_bit':rows[actual_j][1][actual_x] if rows is not None and 0 <= actual_j < len(rows) else None,
                           'begin':steps}
                visits.append(pending)
            if pc in core_entries:
                need(pending is not None, 'Core has point entry')
                observe(value(tapes[3].cells,origins[3],h+1) == pending['row'], 'Wrong copied query row')
                observe(value(tapes[4].cells,origins[4],h+1) == pending['wire'], 'Stale copied current wire')
            if pc in core_done:
                got = tapes[5].cells[origins[5]+1]
                need(got in ('0','1') and pending is not None, 'Physical Boolean produced')
                pending['bit'] = int(got)
                observe(pending['point_bit'] == int(got), 'Wrong canonical switch result')
            if pc in after:
                need(pending is not None and 'bit' in pending, 'Point returned through successful continuation')
                expected_current ^= pending['want_bit'] << (1+min(pending['wanted_row'],2*h-2-pending['wanted_row'])-1)
                observe(value(tapes[18].cells,origins[18],h) == expected_current, 'Wrong address after Boolean consumption')
                pending['instructions'] = steps-pending.pop('begin')
                need(pending['instructions'] <= 1024*(h+3)**2+128*(p+h+3), 'Each complete point call is charged')
                need(heads[:19] == origins[:19] and heads[19] == origins[19]+pending['target'], 'Point complete head return')
                for i in range(14):
                    need(tapes[i].cells[:len(before[i])] == before[i] and all(x == '_' for x in tapes[i].cells[len(before[i]):]), 'Point blank/private/exterior reentry')
                pending = None
            ins = self.code[pc]
            op = ins[0]
            steps += 1
            point_steps += pc >= 123
            core_steps += core_at[pc]
            pc += 1
            if op in ('R','W','M'):
                role = ins[1]
                need(tapes[role].head == heads[role] and origins[role] <= heads[role] <= cap[role], 'Sparse/physical head or granted window')
                actions += 1
            if op == 'R':
                symbol = memory.get((role,heads[role]),'_')
                need(tapes[role].read() == symbol, 'Physical read differs from sparse map')
                pc = ins[2][symbol]
            elif op == 'W':
                symbol = ins[2]
                tapes[role].write(symbol)
                writes[role] += 1
                if symbol == '_': memory.pop((role,heads[role]),None)
                else: memory[role,heads[role]] = symbol
            elif op == 'M':
                heads[role] += ins[2]
                need(origins[role] <= heads[role] <= cap[role], 'Unit move left supplied interval')
                high[role] = max(high[role],heads[role])
                tapes[role].step(ins[2])
            elif op == 'J': pc = ins[1]
            elif op == 'H':
                status = ins[1]
                break
            else: raise ValueError('Unknown opcode')
        need([id(t.cells) for t in tapes] == backing and all(len(t.cells) >= len(old) for t,old in zip(tapes,before)), 'Retained physical backing')
        actual_memory = {(i,j):x for i,t in enumerate(tapes) for j,x in enumerate(t.cells) if x != '_'}
        need(actual_memory == memory, 'Complete physical/sparse memory')
        if status == 'DONE':
            need(heads == origins, 'Whole-route head return')
            observe(len(visits) == 2*h-1 and pending is None, 'Complete Q point calls')
            need(sum(v['instructions'] for v in visits) == point_steps, 'Complete instruction sum across point calls')
            wanted = (x+(a if direction == 'FORWARD' else -a)) % s if x < s else x
            observe(value(tapes[18].cells,origins[18],h) == wanted, 'Complete padded rotation endpoint')
            for role,tape in enumerate(tapes):
                old = list(before[role])
                if role == 17: old[origins[role]+1:origins[role]+p+1] = ['0']*p
                elif role == 18: old[origins[role]+1:origins[role]+h+1] = tape.cells[origins[role]+1:origins[role]+h+1]
                need(tape.cells[:len(old)] == old and all(c == '_' for c in tape.cells[len(old):]), 'Whole body/frame/exterior retirement')
            P = (2*h-2).bit_count()
            expected_driver = 14*p+36*h-12-7*P if direction == 'FORWARD' else 14*p+72*h-38-14*P
            observe(steps-point_steps == expected_driver, 'Exact controller count')
            need(sum(high[i]-origins[i]+1 for i in range(14)) <= p+11*h+h.bit_length()+48, 'Repeated-query historical union')
            need(steps <= (2*h-1)*(1024*(h+3)**2+128*(p+h+3))+14*p+72*h, 'Complete point plus controller bound')
            need(writes[14:17] == [0,0,0], 'No borrowed header writes')
        self.calls += len(visits)
        self.routes += 1
        self.instructions += steps
        self.core_instructions += core_steps
        self.symbol_actions += actions
        self.point_instructions += point_steps
        result = {'status':status,'instructions':steps,'controller_instructions':steps-point_steps,
                  'point_instructions':point_steps,'point_calls':len(visits),'core_instructions':core_steps,
                  'h':h,'p':p,'s':s,'a':a,'input':x,'direction':direction,
                  'output':value(tapes[18].cells,origins[18],h),'faults':faults,'visits':visits,
                  'private_history_union':sum(high[i]-origins[i]+1 for i in range(14)),
                  'new_private_cells':sum(len(t.cells)-len(old) for t,old in zip(tapes[:14],before[:14]))}
        self.records.append(result)
        return result


def compact(result):
    out = {k:v for k,v in result.items() if k != 'visits'}
    out['trace_sha256'] = sha256(json.dumps(result['visits'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    out['rows'] = [v['row'] for v in result['visits']]
    out['targets'] = [v['target'] for v in result['visits']]
    out['wires'] = [v['wire'] for v in result['visits']]
    return out


def mutated(code, labels, metadata, fault):
    out = list(code)
    if fault == 'lost_row_increment':
        out[labels['FORWARD_ASC_UPDATE']] = ('J',labels['FORWARD_ASC_POINT_0'])
    elif fault == 'inverse_uses_forward_rows':
        out[metadata['entries']['INVERSE']] = ('J',metadata['entries']['FORWARD'])
    elif fault == 'premature_cursor_reversal':
        pc = labels['FORWARD_ASC_AFTER']+1
        need(out[pc][0:2] == ('R',19), 'Cursor-read mutation site')
        branches = dict(out[pc][2])
        branches['1'] = labels['FORWARD_TURN']
        out[pc] = ('R',19,branches)
    elif fault == 'stale_wire':
        for place in metadata['point_copies'].values():
            start = place['start']
            for pc in range(start+metadata['point_labels']['COPY_X_START'],start+metadata['point_labels']['COPY_X_END']):
                ins = out[pc]
                if ins[0] in ('R','W','M') and ins[1] == 18:
                    out[pc] = (ins[0],20,*ins[2:])
    else:
        raise ValueError('Unknown explicit semantic mutation')
    need(out != list(code), 'Mutation changed graph')
    return tuple(out)


def actual_join(directory, joined, code, labels, metadata):
    # Execute the unchanged providers; never call their expected-output helpers.
    base = load(directory/'inputs/point/inputs/predecessor/research/encoded-crt-leaf-payload/replay.py', '_row_review_retained_providers')
    model = base.modules()
    moduli, values = (5,7,2,3), (3,2,1,1)
    source, payload, locations = actual_fixture(model,moduli,values)
    original = bytes(source.cells),source.head,dict(payload.cells),payload.head
    owners = id(source.cells),id(payload.cells)
    left, modulus = moduli[-2:]
    offset = values[-1]*pow(left,-1,modulus) % modulus
    destinations = [(x+offset)%modulus if x < modulus else x for x in range(4)]
    expected = sorted(zip(destinations,TAGS))
    machine = SparseController(code,labels,metadata)
    bills, histories = [], []
    for reverse in (False,True):
        before_routes, before_points = machine.routes,machine.point_instructions
        bill, retained = joined.run_leg(model,base,machine,source,payload,reverse)
        bill['complete_routes'] = machine.routes-before_routes
        bill['literal_point_instructions'] = machine.point_instructions-before_points
        bill['literal_controller_instructions'] = bill['literal_query_instructions']-bill['literal_point_instructions']
        need(bill['complete_routes'] == 4 and bill['literal_query_calls'] == 12, 'Actual four-wire/Q inventory')
        need(bill['literal_controller_instructions'] == 4*(162 if reverse else 123), 'Actual complete controller invoice')
        need(len(retained[0]) == 100 and all(all(x in ('_',model.w.BLANK) for x in cells) for cells in retained[0]), 'All actual acquired histories retired and counted')
        histories.extend(retained[0])
        bills.append(bill)
        if not reverse:
            need(payload_values(payload) == expected, 'Direct CRT/tag forward oracle')
            need(source_values(source,locations) == (3,2,1,0), 'Selected source coordinate update')
    need((bytes(source.cells),source.head,dict(payload.cells),payload.head) == original, 'Entire source/key/payload inverse')
    need((id(source.cells),id(payload.cells)) == owners, 'Actual source/payload backing identity')
    need(len(histories) == len({id(cells) for cells in histories}) == 200, 'All source/adapter histories counted across legs')
    return {'moduli':moduli,'values':values,'offset':offset,'destinations':destinations,
            'forward_key_tags':expected,'directions':bills,'retained_symbol_owners':len(histories),
            'retained_symbol_cells':sum(map(len,histories)),
            'all_eight_literal_routes_checked':True,'providers':'Exact retained source/radix components; mixed cost vector retained.'}


def run(directory):
    code, labels, metadata, joined, pinned_files = sources(directory)
    cases = [
        (1,2,1,0,(0,1),False,0),
        (1,2,2,1,(0,1),False,0),
        (2,5,3,2,(0,1,2,3),False,0),
        (3,4,5,3,(0,2,4,7),False,0),
        (4,5,9,8,(0,8,15),False,0),
        (5,6,17,6,(0,5,16,31),False,0),
        (5,97,32,16,(17,),True,193),
        (8,9,255,127,(254,255),False,0),
        (9,10,257,129,(0,256,511),True,0),
    ]
    routes = []
    for h,p,s,a,starts,translated,history in cases:
        for x in starts:
            for direction in ('FORWARD','INVERSE'):
                tapes = fixture(h,p,s,a,x,history,translated)
                r = SparseController(code,labels,metadata).run(tapes,direction)
                need(r['status'] == 'DONE' and not r['faults'], 'Focused successful route')
                routes.append(compact(r)|{'translated':translated,'earlier_private_extent':history})
    controls = []
    for fault in ('lost_row_increment','inverse_uses_forward_rows','premature_cursor_reversal','stale_wire'):
        table = mutated(code,labels,metadata,fault)
        tapes = fixture(2,5,3,2,0)
        if fault == 'stale_wire':
            tapes.append(Tape(field(0,2)+list('_R|10L')))
        direction = 'INVERSE' if fault == 'inverse_uses_forward_rows' else 'FORWARD'
        result = SparseController(table,labels,metadata,True).run(tapes,direction)
        need(result['status'] == 'DONE' and result['faults'], 'Returning semantic corruption detected')
        want = 1 if direction == 'INVERSE' else 2
        need(result['output'] != want, 'Returning control must also change mathematical endpoint')
        controls.append(compact(result)|{'fault':fault,'owners':len(tapes),'all_heads_and_nonresult_bodies_returned':True})
    # A point-domain rejection is not silently upgraded to full-route rollback.
    rejected_tapes = fixture(2,5,0,0,0)
    rejected = SparseController(code,labels,metadata).run(rejected_tapes)
    need(rejected['status'] == 'REJECT' and rejected_tapes[19].head == 1,
         'Rejected route has only the stated inherited failure boundary')
    actual = actual_join(directory,joined,code,labels,metadata)
    return {'status':'PASS_INDEPENDENT_COMPLETE_ROW_REVIEW','source_sha256':PINS,
            'graph_sha256':GRAPH,'static_point_instructions_checked':10000,'controller_locations':123,
            'retained_source_files_checked':pinned_files,'source_caller_seam':joined.exact_seam,
            'focused_routes':routes,'route_count':len(routes),'point_calls':sum(x['point_calls'] for x in routes),
            'literal_instructions':sum(x['instructions'] for x in routes),'returning_controls':controls,
            'failure_boundary':{'status':rejected['status'],'width_head_after_rejection':rejected_tapes[19].head,
                                'whole_failure_rollback_claimed':False},
            'actual_caller':actual,'scope':'Literal per-wire controller plus retained-provider finite join; no source dispatcher, allocator, runtime gain or kappa claim.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',nargs='?',type=Path,default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(run(args.package),sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
