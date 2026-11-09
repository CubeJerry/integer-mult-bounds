"""Independent sparse-hardware observer for the current native symbol boundary.

The dictionary hardware has no dense-array or host rewind primitive. This
checks the newly composed 4-by-3 symbol codec and its ownership guards; it is
not an independent verification of the predecessor Compact/B1 theorem.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
from types import SimpleNamespace


def require(ok, message):
    if not ok:
        raise ValueError(message)


class SparseHardware:
    def __init__(self, origin):
        self.origin = self.head = origin
        self.storage = {origin-1: 2}
        self.high = origin
        self.actions = 0
        self.seen = set()

    def read(self):
        self.actions += 1
        self.seen.add(self.head)
        return self.storage.get(self.head, 6)

    def write(self, value):
        require(type(value) is int and 0 <= value < 7, 'physical alphabet')
        self.actions += 1
        self.seen.add(self.head)
        self.high = max(self.high, self.head+1)
        if value == 6:
            self.storage.pop(self.head, None)
        else:
            self.storage[self.head] = value

    def move(self, direction):
        require(direction in (-1, 1), 'unit physical head movement')
        self.actions += 1
        self.head += direction
        require(self.head >= 0, 'one-sided physical head')


def twelve_bits(symbol):
    # Separate arithmetic definition: each old bit is the literal 000 or 001
    # word in the seven-symbol interface, big-endian in both layers.
    return tuple(d for shift in (3, 2, 1, 0)
                 for d in (0, 0, (symbol >> shift) & 1))


def reject(call, label, controls):
    try:
        call()
    except ValueError:
        controls.append(label)
    else:
        raise ValueError('negative control accepted: '+label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--package', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    package = Path(args.package).resolve()
    sys.path.insert(0, str(package))
    from codec import SymbolPort, ParkingAdapter, OriginHead, A
    cases = 0
    maxima = dict(read=0, write=0, step=0)
    receipt = sha256()
    controls = []
    for origin in (1, 7, 19):
        for left, middle, right in itertools.product(range(14), repeat=3):
            raw = SparseHardware(origin)
            port = SymbolPort(raw)
            port.initialize()
            for value in (left, middle, right):
                before = raw.actions
                port.write(value)
                maxima['write'] = max(maxima['write'], raw.actions-before)
                at = raw.head
                require(tuple(raw.storage.get(at+i, 6) for i in range(12)) == twelve_bits(value),
                        'literal independent 12-bit encoding')
                before = raw.actions
                require(port.read() == value, 'local symbol value')
                maxima['read'] = max(maxima['read'], raw.actions-before)
                require(raw.head == at, 'read/write restore exact physical cursor')
                before = raw.actions
                port.step(1)
                maxima['step'] = max(maxima['step'], raw.actions-before)
                require(raw.head == at+12, 'one old symbol is twelve unit positions')
            for value in (right, middle, left):
                port.step(-1)
                require(port.read() == value, 'independent reverse traversal')
            require(raw.head == origin+12, 'origin is after encoded native LEFT')
            require(OriginHead(SimpleNamespace(native_port=port)) == 1, 'literal native origin guard')
            A.retire(raw)
            require(raw.storage == {origin-1: 2} and raw.head == origin,
                    'entire contiguous encoded body physically erased')
            receipt.update(bytes((origin, left, middle, right)))
            cases += 1
    # Crossing fresh blank materializes a complete old blank; repeated blank
    # movement must preserve the contiguous physical body needed by retire.
    blank_raw = SparseHardware(17)
    blank_port = SymbolPort(blank_raw)
    blank_port.initialize()
    for _ in range(32):
        before = blank_raw.actions
        blank_port.step(1)
        maxima['step'] = max(maxima['step'], blank_raw.actions-before)
    blank_port.rewind()
    require(blank_raw.head == 29, 'blank-run rewind stops at local encoded origin')
    A.retire(blank_raw)
    require(blank_raw.storage == {16: 2}, 'encoded blank high-water body erased')
    # The finite maximum is observational, not the asymptotic B1 tariff.
    for value in (14, 15):
        raw = SparseHardware(3)
        raw.storage.update({3+i: bit for i, bit in enumerate(twelve_bits(value))})
        port = SymbolPort(raw)
        reject(port.read, 'unused native symbol '+str(value), controls)
    for body, label in [((1, 1, 1), 'unused seven-symbol word'),
                        ((0, 0, 0), 'incomplete old symbol')]:
        raw = SparseHardware(5)
        raw.storage.update({5+i: bit for i, bit in enumerate(body)})
        reject(SymbolPort(raw).read, label, controls)
    # Repeated work with larger historical reach must not scan that old reach.
    short_costs = []
    for prior in (0, 53):
        raw = SparseHardware(11)
        port = SymbolPort(raw)
        if prior:
            port.initialize()
            for _ in range(prior):
                port.write(13)
                port.step(1)
            A.retire(raw)
        before = raw.actions
        port.initialize()
        for v in (1, 0):
            port.write(v)
            port.step(1)
        A.retire(raw)
        short_costs.append(raw.actions-before)
        require(raw.storage == {10: 2}, 'no retained nonblank history')
    require(short_costs[0] == short_costs[1], 'current work independent of historical reach')
    ports = tuple(SymbolPort(SparseHardware(x)) for x in (5, 13))
    machine = SimpleNamespace(tapes=[{}, {}])
    owner = SimpleNamespace(machine=machine)
    adapter = ParkingAdapter(owner, ports)
    adapter.initialize()
    require(machine.tapes == [{}, {}], 'initial stack/packet baselines')
    ports[0].write(1)
    ports[0].step(1)
    require(not (machine.tapes[0] == {}), 'blank stack top is insufficient without origin marker')
    controls.append('nonempty stack with blank top')
    ports[0].step(-1)
    ports[0].write(4)
    ports[1].step(-1)
    ports[1].write(5)
    ports[1].step(1)
    require(machine.tapes == [{}, {0: '^'}], 'marked packet baseline')
    ports[1].step(1)
    require(not (machine.tapes[1] == {0: '^'}), 'wrong packet origin rejected')
    controls.append('shifted packet head')
    ports[1].step(-1)
    ports[1].write(0)
    require(not (machine.tapes[1] == {0: '^'}), 'dirty packet rejected')
    controls.append('dirty packet at original head')
    report = dict(status='PASS_INDEPENDENT_NATIVE_CODEC',
        scope='new 4-by-3 codec and local completed-boundary guards on independent sparse hardware',
        triple_cases=cases, old_symbols=14, physical_bits_per_old_symbol=12,
        consecutive_blank_extension_steps=32,
        maxima_observed_unit_actions=maxima, transcript_sha256=receipt.hexdigest(),
        short_call_actions_after_fresh_and_large_history=short_costs,
        negative_controls=controls,
        codec_sha256=sha256((package/'codec.py').read_bytes()).hexdigest())
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
