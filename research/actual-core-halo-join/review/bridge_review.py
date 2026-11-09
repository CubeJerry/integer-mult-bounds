"""Independent physical endpoint review of the frozen Core/halo bit bridge.

Separate sparse payload hardware, retained physical Count arithmetic and an
independent signed oracle; no author fixture or expected-output import.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import importlib.machinery
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

EXPECTED_BRIDGE = '037dd2265e637f92c6f51320409fb348b148ce9a5e873a353aba053a5c94d1d3'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, path):
    module = ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


class SparseNative:
    blank = left = maximum = None
    constructed = 0

    def __init__(self, origin=17):
        self.origin = self.head = origin
        self._cells = {i: i % 2 for i in range(origin - 1)}
        self._cells[origin - 1] = self.left
        self.meter = SimpleNamespace(reads=0, writes=0, moves=0)
        self.high = origin
        self.readonly = False
        type(self).constructed += 1

    def read(self):
        self.meter.reads += 1
        return self._cells.get(self.head, self.blank)

    def write(self, symbol):
        need(not self.readonly, 'write to immutable native observer port')
        need(type(symbol) is int and 0 <= symbol <= self.maximum, 'native symbol')
        self.meter.writes += 1
        self.high = max(self.high, self.head + 1)
        if symbol == self.blank:
            self._cells.pop(self.head, None)
        else:
            self._cells[self.head] = symbol

    def step(self, direction):
        need(direction in (-1, 1), 'native unit step')
        self.head += direction
        need(self.head >= self.origin - 1, 'native local ownership guard')
        self.high = max(self.high, self.head + 1)
        self.meter.moves += 1

    def append(self, symbol):
        need(self.read() == self.blank, 'native append at blank frontier')
        self.write(symbol)
        self.step(1)

    def rewind(self):
        self.step(-1)
        while self.read() != self.left:
            self.step(-1)
        self.step(1)

    def clear(self):
        self.rewind()
        while self.read() != self.blank:
            self.write(self.blank)
            self.step(1)
        self.rewind()

    def install(self, body):
        self._cells = {i: i % 2 for i in range(self.origin - 1)}
        self._cells[self.origin - 1] = self.left
        self._cells.update((self.origin + i, bit) for i, bit in enumerate(body))
        self.head = self.origin
        self.high = max(self.high, self.origin + len(body))

    def body(self):
        last = max((i for i in self._cells if i >= self.origin), default=self.origin - 1)
        return tuple(self._cells.get(i, self.blank) for i in range(self.origin, last + 1))

    def actions(self):
        return self.meter.reads + self.meter.writes + self.meter.moves


class SparseTransport:
    def __init__(self, body, origin=23, readonly=False, final=True):
        self.origin = self.head = origin
        self._cells = {i: str(i % 2) for i in range(origin - 1)}
        self._cells[origin - 1] = '^'
        self._cells.update((origin + i, x) for i, x in enumerate(body))
        if final:
            self._cells[origin + len(body)] = '!'
        self.readonly = readonly
        self.actions = 0
        self.high = origin + len(body) + int(final)

    def read(self):
        self.actions += 1
        return self._cells.get(self.head, '_')

    def write(self, symbol):
        need(not self.readonly, 'write to immutable transport observer port')
        need(type(symbol) is str and len(symbol) == 1, 'transport symbol')
        self.actions += 1
        self.high = max(self.high, self.head + 1)
        if symbol == '_':
            self._cells.pop(self.head, None)
        else:
            self._cells[self.head] = symbol

    def move(self, direction):
        need(direction in (-1, 1), 'transport unit step')
        self.actions += 1
        self.head += direction
        need(self.head >= self.origin - 1, 'transport local ownership guard')
        self.high = max(self.high, self.head + 1)

    def body(self):
        ends = [i for i, value in self._cells.items() if i >= self.origin and value == '!']
        need(len(ends) == 1, 'one observed transport end marker')
        end, = ends
        need(not any(i > end for i in self._cells), 'no hidden live transport tail')
        return ''.join(self._cells.get(i, '_') for i in range(self.origin, end))

    def prefix(self):
        return tuple(self._cells.get(i, '_') for i in range(self.origin))


def run(package):
    package = package.resolve()
    here = Path(__file__).resolve().parent
    oracle = load('_review_signed_oracle', here / 'signed_oracle.py')
    frozen = package / 'format_bridge.py'
    need(sha256(frozen.read_bytes()).hexdigest() == EXPECTED_BRIDGE, 'frozen bridge source')
    importlib.machinery.SourceFileLoader.get_code = lambda self, name: compile(
        self.get_data(self.get_filename(name)), self.get_filename(name), 'exec')
    bindings = load('halo_core_sources', package / 'halo_core_sources.py')
    source = bindings.core_sources()
    transport = load('_review_retained_transport', package /
                     'retained/halo/sparse-halo-tape-transaction/tapes.py')
    cases, rejected = [], []
    with source.physical():
        from cardinal_counts import Count
        from check_support import no_decode
        from words import BLANK, LEFT
        import records
        SparseNative.blank, SparseNative.left, SparseNative.maximum = BLANK, LEFT, records.RETURN
        bridge_code = load('_review_frozen_format_bridge', frozen)
        bridge_code.Tape = SparseNative

        def control(values):
            ports = tuple(Count.literal(value) for value in values)
            before = tuple((bytes(p.tape.cells), p.tape.head) for p in ports)
            return ports, before

        def close_control(ports, before):
            need(tuple((bytes(p.tape.cells), p.tape.head) for p in ports) == before,
                 'unchanged borrowed encoded Count ports')
            for port in ports:
                port.close()

        def empty(owner, protected_input=False):
            need(not owner.pool.live and owner.scratch.body() == (), 'no live scratch roles')
            for tape in owner.forbidden():
                if tape is owner.input and protected_input:
                    continue
                if isinstance(tape, SparseNative):
                    need(tape.head == tape.origin and tape.body() == ()
                         and tape._cells.get(tape.origin - 1, BLANK) == BLANK,
                         'erased owned sparse payload and marker')
                else:
                    need(tape.head == 1 and all(value == BLANK for value in tape.cells),
                         'erased Count pool body and marker')

        def lift_case(name, pairs, halo_width, core_width, q, precision, shift_sum):
            owner = bridge_code.FormatBridge(transport)
            body = oracle.transport_encode(pairs, halo_width)
            incoming = SparseTransport(body, origin=31, readonly=True)
            target = SparseTransport('101001#' * 7, origin=19)
            before_in = dict(incoming._cells)
            prefix = target.prefix()
            ports, before = control((halo_width, core_width, q, precision,
                                     precision + shift_sum - q))
            constructed = SparseNative.constructed
            with no_decode():
                lifted = owner.lift(incoming, *ports[:4])
            expected = tuple(tuple(x * 2 ** (precision - q) for x in pair) for pair in pairs)
            need(oracle.core_decode(lifted.body(), core_width) == expected,
                 'independent exact lifted endpoint')
            need(incoming._cells == before_in and incoming.head == incoming.origin,
                 'borrowed incoming body and origin')
            empty(owner, protected_input=True)
            saved = dict(lifted._cells)
            with no_decode():
                owner.normalized_return(lifted, target, ports[0], ports[1], ports[4])
            wanted = tuple(tuple(oracle.toward_zero(x, shift_sum) for x in pair) for pair in pairs)
            need(oracle.transport_decode(target.body(), halo_width) == wanted,
                 'independent composed normalized endpoint')
            need(lifted._cells == saved and lifted.head == lifted.origin,
                 'protected native input reused read-only')
            need(target.prefix() == prefix and target.head == target.origin,
                 'transport target origin/prefix')
            with no_decode():
                owner.clear_input()
            empty(owner)
            need(SparseNative.constructed == constructed, 'no online payload role allocation')
            close_control(ports, before)
            cases.append(dict(name=name, records=len(pairs), halo_width=halo_width,
                              core_width=core_width, input_shift=precision-q,
                              normalizer_shift=shift_sum, payload_actions=(incoming.actions
                                  + target.actions + owner.input.actions() + owner.scratch.actions()),
                              private_roles=len(owner.forbidden())))

        for width in range(2, 9):
            bound = 2 ** (width - 1) - 1
            values = sorted(set(x for x in (-bound, -bound+1, -7, -3, -1,
                                           0, 1, 3, 7, bound-1, bound)
                                if -bound <= x <= bound))
            lift_case('signed-width-' + str(width), tuple(zip(values, reversed(values))),
                      width, width+3, 2, 5, 3)
        lift_case('production-dimensions', ((1, -3), (-(2**27)+1, 2**27-1), (0, 0)),
                  31, 270, 28, 246, 1)
        lift_case('equal-grid-no-normalizer', ((-7, 3), (0, -1), (7, 7)), 4, 4, 9, 9, 0)

        def return_case(name, pairs, width, halo_width, drop, owner=None):
            if owner is None:
                owner = bridge_code.FormatBridge(transport)
            native = SparseNative(origin=37)
            native.install(oracle.core_encode(pairs, width))
            native.readonly = True
            target = SparseTransport('0101#' * 4, origin=29)
            native_before, target_prefix = dict(native._cells), target.prefix()
            ports, before = control((halo_width, width, drop))
            constructed = SparseNative.constructed
            start = owner.scratch.actions()
            with no_decode():
                owner.normalized_return(native, target, *ports)
            wanted = tuple(tuple(oracle.toward_zero(x, drop) for x in pair) for pair in pairs)
            need(oracle.transport_decode(target.body(), halo_width) == wanted,
                 'independent direct return endpoint')
            need(native._cells == native_before and native.head == native.origin,
                 'read-only native return and origin')
            need(target.prefix() == target_prefix and target.head == target.origin,
                 'translated output origin')
            empty(owner)
            need(SparseNative.constructed == constructed, 'no direct-return allocation')
            close_control(ports, before)
            actions = native.actions() + target.actions + owner.scratch.actions() - start
            cases.append(dict(name=name, records=len(pairs), core_width=width,
                              halo_width=halo_width, drop=drop, payload_actions=actions,
                              scratch_historical_extent=owner.scratch.high-owner.scratch.origin))
            return owner, actions

        for drop in (0, 1, 2, 8, 9, 10, 19):
            return_case('minimum-and-odd-drop-' + str(drop),
                        ((-256, 255), (-3, 3), (-1, 0)), 9, 10, drop)
        reused, _ = return_case('large-history', ((-2**149, 2**149-1),), 150, 151, 0)
        old_high = reused.scratch.high
        reused, old_actions = return_case('short-after-large', ((-3, 1),), 4, 5, 1, reused)
        fresh, new_actions = return_case('fresh-short', ((-3, 1),), 4, 5, 1)
        need(old_actions == new_actions and reused.scratch.high == old_high
             and reused.scratch.high > fresh.scratch.high,
             'current cleanup versus historical backing')

        def reject_lift(name, text, halo_width, core_width, q=2, precision=5, final=True):
            owner = bridge_code.FormatBridge(transport)
            incoming = SparseTransport(text, origin=41, readonly=True, final=final)
            saved = dict(incoming._cells)
            ports, before = control((halo_width, core_width, q, precision))
            try:
                with no_decode():
                    owner.lift(incoming, *ports)
            except ValueError as error:
                reason = str(error)
            else:
                raise ValueError('invalid lift accepted: ' + name)
            need(incoming._cells == saved and incoming.head == incoming.origin,
                 'rejected lift borrowed-source restoration')
            empty(owner)
            close_control(ports, before)
            rejected.append(dict(name=name, reason=reason))

        valid = oracle.transport_encode(((3, -1),), 4)
        reject_lift('negative-zero-late', valid + '10000000#', 4, 7)
        reject_lift('malformed-signmag-digit', valid + '0000000x#', 4, 7)
        reject_lift('missing-record-delimiter', '00000000', 4, 7)
        reject_lift('missing-stream-end', valid, 4, 7, final=False)
        reject_lift('insufficient-lift-carrier', valid, 4, 6)
        reject_lift('unfunded-coarser-grid', valid, 4, 7, q=6, precision=5)

        for name, pair, halo_width in (('positive-return-overflow',(32,0),6),
                                       ('negative-return-overflow',(-32,0),6),
                                       ('minimum-return-overflow',(-64,0),7)):
            owner = bridge_code.FormatBridge(transport)
            native = SparseNative(origin=43)
            native.install(oracle.core_encode((pair,), 7)); native.readonly = True
            saved = dict(native._cells)
            target = SparseTransport(valid * 3, origin=47)
            prefix = target.prefix()
            ports, before = control((halo_width, 7, 0))
            try:
                with no_decode():
                    owner.normalized_return(native, target, *ports)
            except ValueError as error:
                reason = str(error)
            else:
                raise ValueError('return overflow accepted')
            need(native._cells == saved and native.head == native.origin,
                 'overflow native-source restore')
            need(target.body() == '' and target.head == target.origin and target.prefix() == prefix,
                 'failed target cleared, not rolled back')
            empty(owner); close_control(ports, before)
            rejected.append(dict(name=name, reason=reason))

    need(sha256(frozen.read_bytes()).hexdigest() == EXPECTED_BRIDGE,
         'bridge stable through review')
    return dict(status='INDEPENDENT_CORE_HALO_BRIDGE_PASS',
                scope='Frozen signed/grid bridge endpoints on independent sparse payload hardware; retained Count arithmetic, no full Core/halo fixture replay.',
                executed_cases=cases, rejection_controls=rejected,
                independent_hardware=True, negative_zero_canonical=True,
                current_cleanup_history_independent=True, historical_backing_retained=True,
                source_sha256={
                    'format_bridge.py': EXPECTED_BRIDGE,
                    'halo_core_sources.py': sha256((package/'halo_core_sources.py').read_bytes()).hexdigest(),
                    'retained_transport': sha256((package/'retained/halo/sparse-halo-tape-transaction/tapes.py').read_bytes()).hexdigest(),
                    'signed_oracle.py': sha256((here/'signed_oracle.py').read_bytes()).hexdigest(),
                    'bridge_review.py': sha256((here/'bridge_review.py').read_bytes()).hexdigest()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(args.package), sort_keys=True, indent=2)+'\n')
