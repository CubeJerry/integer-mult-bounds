"""Root reviewer: separate sparse hardware and exact signed-word oracle.

No author Tape, encoder, expected-value function or test fixture is imported.
The proposed physical primitive functions are the subjects under test.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

SOURCE = Path(__file__).resolve().with_name('machine.py')
SOURCE_BYTES = SOURCE.read_bytes()
spec = importlib.util.spec_from_file_location('reviewed_lifecycle', SOURCE)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
exec(compile(SOURCE_BYTES, str(SOURCE), 'exec'), module.__dict__)


def require(value, message):
    if not value:
        raise ValueError(message)


class SparseHardware:
    """Absolute coordinates, protected prefix, independent read/write/move bill."""
    def __init__(self, body=(), origin=7, marker=2):
        self.origin = origin
        self.head = origin + 1
        self.storage = {i: (i % 2) for i in range(origin)}
        self.storage[origin] = marker
        self.storage.update({origin + 1 + i: bit for i, bit in enumerate(body)})
        self.prefix = dict(self.storage)
        self.actions = 0
        self.maximum = self.head

    def read(self):
        self.actions += 1
        require(self.head >= self.origin, 'read entered protected ancestor')
        self.maximum = max(self.maximum, self.head)
        return self.storage.get(self.head, 6)

    def write(self, value):
        self.actions += 1
        require(self.head > self.origin and value in range(7), 'illegal write')
        self.storage[self.head] = value
        self.maximum = max(self.maximum, self.head)

    def move(self, direction):
        self.actions += 1
        require(direction in (-1, 1), 'unit move required')
        self.head += direction
        require(self.head >= self.origin, 'move entered protected ancestor')
        self.maximum = max(self.maximum, self.head)

    def bytes(self):
        return tuple(self.storage.get(i, 6) for i in range(self.origin + 1, self.maximum + 1))

    def body(self):
        data = self.bytes()
        try:
            end = data.index(6)
        except ValueError:
            end = len(data)
        require(all(v == 6 for v in data[end:]), 'live bytes beyond first physical blank')
        return data[:end]

    def guard(self):
        require(all(self.storage.get(i, 6) == self.prefix[i] for i in range(self.origin + 1)), 'protected prefix changed')


def code(symbol):
    return (symbol // 4, symbol // 2 % 2, symbol % 2)


def encode(values, width):
    out = []
    for value in values:
        for place in range(width):
            out.extend(code((value // 2**place) % 2))
        out.extend(code(2))
    return tuple(out)


def run():
    legal = rejected = initialized = 0
    for width in range(1, 7):
        bound = 2 ** (width - 1)
        for a in range(-bound, bound):
            for b in range(-bound, bound):
                left = SparseHardware(encode((a,), width), origin=3 + width)
                right = SparseHardware(encode((b,), width), origin=8 + width)
                left_snapshot = dict(left.storage)
                in_range = -bound <= a+b < bound
                try:
                    module.copy_as_add(right, left)
                except ValueError as exc:
                    require(not in_range and str(exc) == 'signed addition overflow', ('unexpected rejection', width, a, b, str(exc)))
                    rejected += 1
                else:
                    require(in_range, 'overflow accepted')
                    require(right.body() == encode((a+b,), width), ('signed sum', width, a, b))
                    require(left.storage == left_snapshot, 'borrowed source changed')
                    require(left.head == left.origin+1 and right.head == right.origin+1, 'addition origin return')
                    legal += 1
                left.guard(); right.guard()
        for values in ((-bound, bound-1), (0, -1, 1 if bound > 1 else 0)):
            shape = SparseHardware(encode(values, width), origin=11)
            target = SparseHardware((1, 1, 0, 1, 0, 0, 1) * (width+1), origin=4)
            before = dict(shape.storage)
            module.initialize(target, shape)
            require(target.body() == encode((0,)*len(values), width), 'complete encoded zero including delimiters')
            require(shape.storage == before and shape.head == shape.origin+1, 'shape preserved')
            target.guard(); shape.guard()
            module.retire(target)
            require(target.body() == () and target.head == target.origin+1, 'retirement including former history')
            initialized += 1

    # Directly check independently derived affine scan bills at translated origins.
    bill_cases = 0
    for size in (0, 1, 2, 3, 7, 19, 51):
        bits = tuple(i % 2 for i in range(size))
        source, target = SparseHardware(bits, 14), SparseHardware((), 5)
        module.transfer(source, target)
        require(source.actions + target.actions == 8*size+14, 'transfer scan bill')
        before = target.actions
        module.retire(target)
        require(target.actions-before == 5*size+7, 'retire scan bill')
        bill_cases += 1

    # Moving over unused virtual cells writes coded blank100; physical blank6
    # cannot appear inside the occupied coded body.
    tape = SparseHardware(origin=13)
    view = module.CodedPort(tape)
    require(view.read() == 4, 'virtual blank convention')
    view.move(1); view.move(1); view.write(6)
    require(tape.body() == code(4)+code(4)+code(6), 'coded logical blank continuity')
    view.move(-1); view.move(-1)
    try:
        view.move(-1)
    except ValueError as exc:
        require(str(exc) == 'native routine crossed its local origin', 'boundary diagnostic')
    else:
        raise ValueError('native crossed protected origin')
    tape.guard()
    print(json.dumps(dict(status='PASS_ROOT_LIFECYCLE_PRIMITIVE_REVIEW',
                          legal_signed_pairs=legal, overflow_rejections=rejected,
                          initialized_formats=initialized, scan_bill_cases=bill_cases,
                          source_sha256=hashlib.sha256(SOURCE_BYTES).hexdigest()), sort_keys=True))


if __name__ == '__main__':
    run()
