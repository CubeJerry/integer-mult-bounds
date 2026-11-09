"""Root reviewer: flat-index oracle for the proposed physical union router.

This file imports no author fixture encoder or expected-result oracle.  The
unchanged physical runtime and supplied endpoint-NAND service are the subjects
under test; the dense reference uses arithmetic strides, not union classes.
"""
from pathlib import Path
import hashlib
import json
import sys
import time

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE))
from runtime_sources import physical_runtime


def require(value, message):
    if not value:
        raise ValueError(message)


def little(value, width):
    value %= 2 ** width
    return bytes((value // (2 ** k)) % 2 for k in range(width))


def variable(value):
    return little(value, max(1, value.bit_length())) + bytes([3])


def high(value, width):
    return little(value, width)[::-1]


def dense_reference(values, side, exposed, backwards=False):
    """One completed axis at a time, with explicit arithmetic line strides."""
    result = [list(v) for v in values]
    axes = range(len(exposed)-1, -1, -1) if backwards else range(len(exposed))
    for axis in axes:
        rows = exposed[axis]
        if not rows:
            continue
        stride = side ** (len(exposed) - axis - 1)
        # Disjoint axis lines permit in-place updates during this axis.
        for address in range(len(result)):
            if (address // stride) % side != rows[0]:
                continue
            tail = address + (rows[-1] - rows[0]) * stride
            low = 1 - (result[address][0] % 2) * (result[tail][0] % 2)
            result[address][0] += low - result[address][0] % 2
    return [tuple(v) for v in result]


def encode_bank(context, exposed, width, coord_bits):
    raw = bytearray(context + bytes([5]))
    for rows in exposed:
        size = len(rows)
        raw.append(6)
        raw.extend(variable(size) + variable(size) + variable(2))
        for x in rows:
            raw.extend(high(x, coord_bits))
        raw.append(5)
        raw.extend(bytes([1]) * size)
        raw.append(5)
        blocks = (size + 1) // 2
        for role in range(8):
            extent = max(0, blocks - role % 2) * 4 * width
            raw.extend(bytes(extent))
            raw.append(5)
        raw.append(7)
    return bytes(raw)


def run():
    cases = [
        (2, ((),), 5),
        (4, ((3,),), 4),
        (5, ((0, 2, 4), (1,)), 5),
        (3, ((0, 1, 2), (), (1, 2)), 4),
        (4, ((1, 2, 3), (0, 3), (0, 1, 2, 3)), 4),
        (3, ((0, 2), (1,), (0, 1), (2,)), 5),
        (5, ((0, 1, 2, 3, 4), (0, 2, 4)), 4),
    ]
    results = []
    with physical_runtime():
        from records import Tape
        from cardinal_counts import Count
        from control_service import ControlService
        from physical_router import UnionRouter
        from check_support import no_decode
        from words import BLANK

        def put(tape, raw):
            for symbol in raw:
                tape.append(symbol)
            tape.rewind()

        # The same fixed owner is reused at varying dimensions and lengths.
        child = ControlService()
        owner = UnionRouter(child)
        for number, (side, exposed, width) in enumerate(cases):
            start = time.monotonic()
            axes, coord_bits = len(exposed), (side - 1).bit_length()
            context = bytes((i + number) % 2 for i in range(1 + 17 * number))
            values = [((11*i + 7) % (2**width) - 2**(width-1),
                       (7*i + 1) % (2**width) - 2**(width-1))
                      for i in range(side**axes)]
            source, catalogue = Tape(), Tape()
            data = context + bytes([5]) + b''.join(little(x, width) for v in values for x in v)
            put(source, data)
            put(catalogue, encode_bank(context, exposed, width, coord_bits))
            metadata = tuple(Count.literal(v) for v in
                             (axes, side, coord_bits, axes.bit_length(), width, 0))
            borrowed = (source, catalogue, *(v.tape for v in metadata))
            saved = [(bytes(t.cells), t.head) for t in borrowed]
            visits_before, lines_before = owner.visits, child.lines
            with no_decode():
                output = owner.run(source, catalogue, *metadata)
            expected_values = dense_reference(values, side, exposed)
            expected = context + bytes([5]) + b''.join(little(x, width) for v in expected_values for x in v)
            require(bytes(output.cells[1:1+len(expected)]) == expected, 'independent flat-stride output')
            require(all(s == BLANK for s in output.cells[1+len(expected):]), 'output has no extra live tail')
            require(owner.visits - visits_before == sum(map(len, exposed)) * side**(axes-1), 'exact incidence count')
            require(child.lines - lines_before == sum(bool(e) for e in exposed) * side**(axes-1), 'all complete axis lines exactly once')
            with no_decode():
                owner.consume()
            require([(bytes(t.cells), t.head) for t in borrowed] == saved, 'full borrowed bytes and heads')
            require(all(t.head == 1 and all(s == BLANK for s in t.cells)
                        for t in owner.forbidden()), 'all owned roles including history erased')
            for value in metadata:
                value.close()
            results.append(dict(side=side, axes=axes, exposed=exposed, width=width,
                                records=len(values), incidences=owner.visits-visits_before,
                                order_control_diff=sum(a != b for a,b in zip(expected_values,
                                    dense_reference(values, side, exposed, True))),
                                elapsed_seconds=round(time.monotonic()-start, 3)))
            print(json.dumps(results[-1], sort_keys=True), flush=True)
    pins = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PACKAGE.glob('*.py')}
    print(json.dumps(dict(status='PASS_ROOT_FLAT_INDEX_UNION_REVIEW', cases=results, sources=pins), sort_keys=True))


if __name__ == '__main__':
    run()
