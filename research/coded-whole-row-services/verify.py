"""Bounded source-bound corroboration; scientific control never reads observers."""
from pathlib import Path
from types import ModuleType
import itertools
import json
import sys

P = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(stem):
    path = P / (stem + '.py')
    module = ModuleType('coded_rows_' + stem)
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


rows = load('rows')
binding = load('source_binding')
machine, stack, scalar = binding.modules()


class Tape(stack.Tape):
    """Hardware and verification-only history, not an executable input decoder."""
    def __init__(self, body=(), marker=stack.LEFT, prefix=(), warm=0):
        super().__init__(prefix, marker)
        self.cells.extend(body)
        self.cells.extend([stack.BLANK] * warm)
        self.initial_origin = self.head
        self.events = []
        self.high = self.head

    def read(self):
        value = super().read()
        self.events.append(('r', self.head, value))
        self.high = max(self.high, self.head)
        return value

    def write(self, value):
        self.events.append(('w', self.head, value))
        self.high = max(self.high, self.head)
        super().write(value)

    def move(self, direction):
        self.events.append(('m', self.head, direction))
        super().move(direction)
        self.high = max(self.high, self.head)


def encode(symbols):
    return [bit for symbol in symbols for bit in ((symbol >> 2) & 1,
                                                 (symbol >> 1) & 1, symbol & 1)]


def format_bits(widths):
    return encode([s for width in widths for s in ([0] * width + [2])])


def encode_row(values, widths):
    need(len(values) == len(widths), 'one value per signed component')
    symbols = []
    for value, width in zip(values, widths):
        need(-(1 << (width - 1)) <= value < (1 << (width - 1)), 'signed fixture range')
        symbols.extend((value >> j) & 1 for j in range(width))
        symbols.append(2)
    return encode(symbols)


def current(tape, marker=stack.LEFT):
    """Checker-only current body; no scientific transition uses this routine."""
    origin = tape.head
    while origin > 0 and tape.cells[origin - 1] != marker:
        origin -= 1
    need(origin > 0, 'observer locates marker')
    stop = origin
    while stop < len(tape.cells) and tape.cells[stop] != stack.BLANK:
        stop += 1
    return origin, tuple(tape.cells[origin:stop])


def make_tapes(width, formats, fields=None, bridge=(), header=(), warm=0):
    fields = fields if fields is not None else [()] * width
    result = [Tape(body, prefix=[(i + j) & 1 for j in range(i + 2)], warm=warm)
              for i, body in enumerate(fields)]
    result.append(Tape(formats, prefix=(1, 0, 1, 1), warm=warm))
    result.append(Tape(bridge, stack.BASE, (0, 1, 1), warm))
    result.append(Tape(header, stack.BASE, (1, 1, 0, 0, 1), warm))
    return result


def run_checked(code, entry, tapes):
    starts = []
    for index, tape in enumerate(tapes):
        marker = stack.BASE if index >= len(tapes) - 2 else stack.LEFT
        origin, _ = current(tape, marker)
        starts.append((origin, tuple(tape.cells[:origin]), len(tape.events)))
    raw_before = sum(t.counts.total for t in tapes)
    value, steps = rows.execute(code, entry, tapes)
    need(sum(t.counts.total for t in tapes) - raw_before == steps - 1,
         'one local action per nonterminal transition')
    for tape, (origin, prefix, begin) in zip(tapes, starts):
        need(tuple(tape.cells[:origin]) == prefix, 'all ancestor bytes and delimiter preserved')
        need(tape.head == origin, 'each touched row port returns to local origin')
        need(all(event[1] >= origin - 1 for event in tape.events[begin:]),
             'trace stays within current segment and its marker')
    return value, steps


def service_cases():
    count, canonical_bits = 0, 0
    static = {}
    for width in range(2, 6):
        code, entries = rows.compile_rows(width)
        static[width] = len(code)
        for widths in ((1,), (2,), (1, 3), (2, 3, 1)):
            fmt = format_bits(widths)
            for cycles in range(1, 5):
                number = width * cycles
                values = [tuple((r + i) % (1 << h) - (1 << (h - 1))
                                for i, h in enumerate(widths)) for r in range(number)]
                parts = [encode_row(value, widths) for value in values]
                data = [bit for part in parts for bit in part]
                bill = rows.costs(width, len(fmt), number)
                parent = make_tapes(width, fmt, [data] * width, warm=17)
                value, steps = run_checked(code, entries['classify'], parent)
                need(value == 'inner' and steps == bill['classify'], 'actual nonleaf classification bill')
                value, steps = run_checked(code, entries['prepare'], parent)
                need(value == 'done' and steps == bill['prepare'], 'actual staged-format bill')
                need(current(parent[-1], stack.BASE)[1] == tuple(fmt), 'staged format exact')
                child = make_tapes(width, (), bridge=data, header=fmt, warm=19)
                value, steps = run_checked(code, entries['install'], child)
                need(value == 'done' and steps == bill['install'], 'actual installation bill')
                for i in range(width):
                    expected = tuple(bit for part in parts[i::width] for bit in part)
                    need(current(child[i])[1] == expected, 'complete row stripe')
                need(current(child[width])[1] == tuple(fmt), 'child guide actually installed')
                machine.retire(child[-2], stack.BASE)
                machine.retire(child[-1], stack.BASE)
                value, steps = run_checked(code, entries['collect'], child)
                need(value == 'done' and steps == bill['collect'], 'actual collection bill')
                need(current(child[-2], stack.BASE)[1] == tuple(data), 'complete row inverse')
                canonical_bits += len(data)
                count += 1
            one = make_tapes(width, fmt, [encode_row((0,) * len(widths), widths)] * width)
            value, steps = run_checked(code, entries['classify'], one)
            need(value == 'leaf' and steps == 8 * len(fmt) + 9, 'actual one-row frontier')
    return {'cases': count, 'total_canonical_bits': canonical_bits,
            'graph_states': static, 'leaf_cases': 16}


def controller_case(width, depth, widths, prefix_length, dirty_length):
    """Run the actual Controller/Stack/scalar code; all extra state is observer-only."""
    count, fmt = width ** depth, format_bits(widths)
    values = []
    data, expected = [], []
    for field in range(width):
        field_values = []
        for row in range(count):
            current_values = []
            for component, h in enumerate(widths):
                bound = (1 << (h - 1)) - 1
                current_values.append((row + 2 * field + component) % (2 * bound + 1) - bound)
            field_values.append(tuple(current_values))
        values.append(field_values)
        data.append([bit for value in field_values for bit in encode_row(value, widths)])
        expected.append(tuple(bit for value in field_values
                              for bit in encode_row(tuple(-x for x in value), widths)))
    q, guide_role = width + 3, width
    bodies = data + [fmt, [i & 1 for i in range(dirty_length)],
                     [(i + 1) & 1 for i in range(dirty_length + 1)]]
    payloads = [Tape(body, prefix=tuple((i + j) & 1 for j in range(prefix_length + i)), warm=13)
                for i, body in enumerate(bodies)]
    outer = [Tape(marker=stack.BASE, prefix=tuple((i + j) & 1 for j in range(prefix_length + 2 * i)),
                  warm=17) for i in range(4)]
    control, descriptor, bridge, header = outer
    tapes = payloads + outer
    initial_prefixes = [tuple(t.cells[:t.initial_origin]) for t in tapes]
    observations, boundary_receipts, restored_parents = [], [], []
    pending = []

    class ObservedRows(rows.RowServices):
        def invoke(self, name):
            value, steps = run_checked(self.code, self.entries[name], self.tapes)
            observations.append((name, steps))
            return value

    class ObservedStack(stack.Stack):
        """Snapshots are checks; the inherited stack never receives them."""
        def push(self, present):
            snapshot = [(t.head, tuple(t.cells[:t.head]), current(t)[1]) for t in self.payloads]
            super().push(present)
            restored_parents.append(snapshot)

        def pop(self):
            snapshot = restored_parents.pop()
            result = super().pop()
            for tape, (head, prefix, body) in zip(self.payloads, snapshot):
                need(tape.head == head and tuple(tape.cells[:head]) == prefix,
                     'actual Stack parent heads and protected prefix')
                need(current(tape)[1] == body, 'actual Stack every suspended owner restored')
            return result

    def total():
        return sum(t.counts.total for t in tapes)

    class ObservedController(machine.Controller):
        def descend(self, pc):
            event = self.program[pc]
            before, event_start = total(), len(observations)
            parent_total = sum(len(current(t)[1]) for t in self.payloads)
            incoming = len(current(self.payloads[event.ports[0]])[1])
            need(observations[-1] == ('classify', 8 * len(fmt) + 9), 'paid classification before descent')
            super().descend(pc)
            row_steps = observations[event_start:]
            need(tuple(name for name, _ in row_steps) == ('prepare', 'install'), 'actual descent callbacks')
            admin = total() - before - sum(steps - 1 for _, steps in row_steps)
            pending.append((parent_total, incoming, admin, row_steps, observations[event_start - 1]))
            need(current(self.payloads[guide_role])[1] == tuple(fmt), 'current child format survived push')
            need(all(len(current(t)[1]) == incoming // width for t in self.payloads[:width]),
                 'every productive child field installed')

        def ascend(self):
            parent_total, incoming, descend_admin, down_rows, classification = pending.pop()
            before, event_start = total(), len(observations)
            child_total = sum(len(current(t)[1]) for t in self.payloads)
            outgoing = sum(len(current(t)[1]) for t in self.payloads[:width])
            pc = super().ascend()
            up_rows = observations[event_start:]
            need(tuple(name for name, _ in up_rows) == ('collect',), 'actual collect before ascent')
            admin = descend_admin + total() - before - sum(steps - 1 for _, steps in up_rows)
            written = machine.boundary_actions(q, self.pc_bits, parent_total, child_total,
                                               incoming, outgoing, len(fmt))
            need(admin == written, 'all original Controller administrative terms retained')
            all_rows = [classification, *down_rows, *up_rows]
            bill = rows.costs(width, len(fmt), incoming // len(fmt))
            need(all(steps == bill[name] for name, steps in all_rows), 'complete actual callback invoice')
            combined = (4 * parent_total + 5 * child_total + 57 * incoming
                        + 8 * (incoming // len(fmt)) + 2 * (incoming // len(fmt) // width)
                        + 31 * len(fmt) + 38 * q + 27 * self.pc_bits + 7 * width + 136)
            need(incoming == outgoing and admin + sum(steps for _, steps in all_rows) == combined,
                 'independent expanded administrative-plus-row invoice')
            boundary_receipts.append({'incoming': incoming, 'outgoing': outgoing,
                                      'parent_total': parent_total, 'child_total': child_total,
                                      'administrative_actions': admin, 'complete_boundary': combined})
            return pc

    row_services = ObservedRows(payloads, width, guide_role, bridge, header)
    table, table_info = scalar.compile_scalar('SCALE', -1)
    program = tuple(machine.Instruction('PAID', (i,), ('homogeneous', i)) for i in range(width))
    program += (machine.Instruction('RET'),)
    services = {('leaf', 'homogeneous', i): table for i in range(width)}
    controller = ObservedController(program, width, payloads, control, descriptor, bridge, header,
                                    row_services, services, ObservedStack,
                                    protected_ports=(guide_role,), primitive_work=(width + 1, width + 2),
                                    primitive_context=(guide_role,))
    controller.run()
    need(not pending and not restored_parents, 'all observed recursion frames retired')
    for i in range(width):
        need(current(payloads[i])[1] == expected[i], 'actual complete nested scalar endpoint')
    need(current(payloads[guide_role])[1] == tuple(fmt), 'root protected format preserved')
    for tape in payloads[width + 1:]:
        need(current(tape)[1] == (), 'root native scratch physically retired')
    for tape in outer:
        need(current(tape, stack.BASE)[1] == (), 'control, PC, bridge and header retired')
    for index, tape in enumerate(tapes):
        need(tape.head == tape.initial_origin, 'all root heads restored')
        need(tuple(tape.cells[:tape.initial_origin]) == initial_prefixes[index], 'outer ancestor bytes exact')
        marker = stack.BASE if index >= q else stack.LEFT
        _, body = current(tape, marker)
        need(all(c == stack.BLANK for c in tape.cells[tape.head + len(body):]),
             'entire historical tail blank after root return')
    expected_boundaries = sum(width ** j for j in range(1, depth + 1))
    need(len(boundary_receipts) == expected_boundaries, 'complete finite recursion tree')
    return {'width': width, 'depth': depth, 'component_widths': list(widths),
            'row_bits': len(fmt), 'root_rows': count, 'prefix_length': prefix_length,
            'initial_dirty_work': [dirty_length, dirty_length + 1],
            'ordinary_boundaries': len(boundary_receipts), 'row_callbacks': len(observations),
            'raw_actions': total(), 'row_transition_steps': sum(s for _, s in observations),
            'scalar_rows': table_info['rows'],
            'boundary_administrative_sum': sum(x['administrative_actions'] for x in boundary_receipts),
            'complete_boundary_sum': sum(x['complete_boundary'] for x in boundary_receipts),
            'retained_cells': sum(len(t.cells) for t in tapes)}


def controller_cases():
    return [controller_case(w, d, widths, prefix, dirty)
            for w, d, widths, prefix, dirty in
            ((2, 0, (2, 2), 0, 5), (2, 1, (3, 3), 7, 3),
             (2, 2, (3, 3), 19, 17), (2, 3, (2, 2, 2, 2), 37, 11),
             (3, 1, (4, 4), 9, 7), (3, 2, (3, 3), 31, 13),
             (4, 2, (3, 3), 47, 5))]


def direct_format_accepts(guide, data):
    """Independent complete-word specification, not the runtime state graph."""
    if not guide or len(guide) != len(data) or len(guide) % 3:
        return False
    g = [4 * guide[i] + 2 * guide[i + 1] + guide[i + 2] for i in range(0, len(guide), 3)]
    x = [4 * data[i] + 2 * data[i + 1] + data[i + 2] for i in range(0, len(data), 3)]
    if g[-1] != 2 or any(s not in (0, 2) for s in g):
        return False
    pieces = []
    begin = 0
    for i, symbol in enumerate(g):
        if symbol == 2:
            pieces.append(g[begin:i])
            begin = i + 1
    if any(not piece for piece in pieces):
        return False
    return all(s in (0, 1) if f == 0 else s == 2 for f, s in zip(g, x))


def exhaustive_format_check():
    code, entries = rows.compile_rows(2)
    cases, accepted = 0, 0
    for size in (3, 6):
        words = list(itertools.product((0, 1), repeat=size))
        for guide in words:
            for data in words:
                tapes = make_tapes(2, guide, [data, ()])
                try:
                    outcome, _ = rows.execute(code, entries['classify'], tapes)
                    observed = outcome == 'leaf'
                except ValueError:
                    observed = False
                expected = direct_format_accepts(guide, data)
                need(observed == expected, 'independent full-word format specification')
                accepted += observed
                cases += 1
    return {'physical_lengths': [3, 6], 'guide_data_pairs': cases, 'accepted_pairs': accepted}


def negative_controls():
    code, entries = rows.compile_rows(2)
    fmt = format_bits((2, 2))
    first = encode_row((0, 1), (2, 2))
    second = encode_row((1, -1), (2, 2))
    caught = []

    def rejects(label, action):
        try:
            action()
        except ValueError:
            caught.append(label)
        else:
            raise ValueError('negative control survived: ' + label)

    def collect(fields, guide=fmt):
        tapes = make_tapes(2, guide, fields)
        rows.execute(code, entries['collect'], tapes)
        return current(tapes[-2], stack.BASE)[1]

    rejects('short_last_returned_field', lambda: collect([first + second, first]))
    rejects('long_last_returned_field', lambda: collect([first, first + second]))
    rejects('partial_last_codeword', lambda: collect([first, second[:-1]]))
    rejects('literal_zero_bytes_are_not_a_zero_row', lambda: collect([first, [0] * len(fmt)]))
    changed = list(second)
    changed[-2] = 0
    rejects('lost_component_terminator', lambda: collect([first, changed]))
    same_length_guide = format_bits((1, 1))
    other_layout = encode_row((0,), (3,))
    rejects('different_layout_with_same_length', lambda: collect([other_layout, other_layout], same_length_guide))
    nonzero_guide = list(fmt)
    nonzero_guide[2] = 1
    rejects('nonzero_format_digit', lambda: collect([first, second], nonzero_guide))
    rejects('empty_format', lambda: collect([first, second], []))
    foreign = list(second)
    foreign[0] = stack.END
    rejects('foreign_physical_symbol', lambda: collect([first, foreign]))
    split_tapes = make_tapes(2, (), bridge=first * 3, header=fmt)
    rejects('incomplete_productive_batch', lambda: rows.execute(code, entries['install'], split_tapes))

    tapes = make_tapes(2, fmt, [first, second])
    rejects('aliased_format_role',
            lambda: rows.RowServices([tapes[0], tapes[1], tapes[0]], 2, 2, tapes[-2], tapes[-1]))
    rejects('aliased_productive_roles',
            lambda: rows.RowServices([tapes[0], tapes[0], tapes[2]], 2, 2, tapes[-2], tapes[-1]))
    rejects('aliased_outer_relays',
            lambda: rows.RowServices(tapes[:3], 2, 2, tapes[-2], tapes[-2]))

    # A valid-shape mutant reverses the field order; local shape checks alone
    # cannot substitute for the source-bound endpoint proof.
    swapped = dict(code)
    for label, instruction in code.items():
        if (label.startswith('collect:') and instruction[0] in ('read', 'write', 'move')
                and instruction[1] in (0, 1)):
            swapped[label] = (instruction[0], 1 - instruction[1], *instruction[2:])
    mutated_tapes = make_tapes(2, fmt, [first, second])
    rows.execute(swapped, entries['collect'], mutated_tapes)
    rejects('swapped_complete_fields_endpoint',
            lambda: need(current(mutated_tapes[-2], stack.BASE)[1] == tuple(first + second),
                         'correct field order'))

    # The extra-field end guard is an actual discriminator, not decorative.
    unchecked = dict(code)
    instruction = unchecked['collect:end1']
    target = instruction[2][stack.BLANK]
    unchecked['collect:end1'] = ('read', 1, {0: target, 1: target, stack.BLANK: target}, 'reject')
    unchecked_tapes = make_tapes(2, fmt, [first, second + first])
    rows.execute(unchecked, entries['collect'], unchecked_tapes)
    rejects('omitted_returned_field_frontier_check',
            lambda: need(len(current(unchecked_tapes[0])[1]) == len(current(unchecked_tapes[1])[1]),
                         'complete equal returned fields'))
    rejects('omitted_format_installation_cost',
            lambda: need(rows.costs(2, len(fmt), 2)['install']
                         == 13 * 2 * len(fmt) + 8 + 1 + 6 + 5,
                         'complete paid header copy'))
    return caught


def partial_failure_example():
    code, entries = rows.compile_rows(2)
    fmt = format_bits((2, 2))
    first = encode_row((0, 1), (2, 2))
    tapes = make_tapes(2, fmt, [first + first, first])
    try:
        rows.execute(code, entries['collect'], tapes)
    except ValueError:
        _, copied = current(tapes[-2], stack.BASE)
        need(len(copied) >= len(first) and tapes[-2].head != tapes[-2].initial_origin,
             'failed collection is deliberately not rollback')
        return {'rejection_preserves_partial_output_cells': len(copied),
                'bridge_head_restored': False, 'rollback_claimed': False}
    raise ValueError('short-field failure example unexpectedly accepted')


def main():
    result = {'status': 'PASS_CODED_WHOLE_ROW_SERVICES', 'services': service_cases(),
              'controllers': controller_cases(), 'format_exhaustion': exhaustive_format_check(),
              'negative_controls': negative_controls(), 'kappa_change': None,
              'partial_failure_example': partial_failure_example(),
              'conditional_homogeneous_geometry': True}
    result = json.loads(json.dumps(result))
    if '--write-result' in sys.argv:
        (P / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads((P / 'RESULT.json').read_text()), 'frozen typed receipt')
    print(result['status'], result['services']['cases'], len(result['controllers']),
          result['format_exhaustion']['guide_data_pairs'], len(result['negative_controls']))


if __name__ == '__main__':
    main()
