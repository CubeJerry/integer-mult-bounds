"""Root reviewer: different table interpreter and nested flat-index oracle.

Only the author's finite table generators are imported.  Hardware, interpreter,
descriptor codecs and expected nested routing are separately implemented here.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

SOURCE = Path(__file__).resolve().parents[1] / 'row_programs.py'
spec = importlib.util.spec_from_file_location('review_row_tables', SOURCE)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Hardware:
    """Dense numeric cells with translated marker and immutable buried prefix."""
    symbols = '_|01'
    def __init__(self, value='', offset=3):
        self.origin = offset
        self.cells = bytearray([2+(i % 2) for i in range(offset)] + [1])
        self.cells.extend(self.symbols.index(x) for x in value)
        self.head = offset+1
        self.prefix = bytes(self.cells[:offset+1])
        self.high = self.head

    def read(self):
        require(self.head >= self.origin, 'read crossed ancestor')
        self.high = max(self.high, self.head)
        return self.symbols[self.cells[self.head]] if self.head < len(self.cells) else '_'

    def write(self, symbol):
        require(self.head > self.origin, 'write crossed ancestor')
        self.cells.extend(bytes(max(0, self.head+1-len(self.cells))))
        self.cells[self.head] = self.symbols.index(symbol)
        self.high = max(self.high, self.head)

    def move(self, direction):
        require(direction in (-1, 1), 'unit move required')
        self.head += direction
        require(self.head >= self.origin, 'move crossed ancestor')
        self.high = max(self.high, self.head)

    def text(self):
        data = self.cells[self.origin+1:]
        end = data.find(bytes([0]))
        if end < 0:
            end = len(data)
        require(not any(data[end:]), 'live tail behind blank')
        return ''.join(self.symbols[x] for x in data[:end])

    def check(self):
        require(bytes(self.cells[:self.origin+1]) == self.prefix, 'buried prefix changed')
        require(self.head == self.origin+1, 'origin not restored')


def interpret(code, ports, stop_limit=10_000_000):
    pc = 0
    for tick in range(stop_limit):
        require(0 <= pc < len(code), 'finite control address')
        instruction = code[pc]
        op = instruction[0]
        if op == 'done':
            return tick+1
        if op in ('reject', 'quarantine'):
            raise ValueError('machine rejected')
        if op == 'goto':
            pc = instruction[1]
        elif op == 'read':
            pc = instruction[2][ports[instruction[1]].read()]
        else:
            port = ports[instruction[1]]
            if op == 'write':
                port.write(instruction[2])
            elif op == 'move':
                port.move(instruction[2])
            else:
                raise ValueError(('unexpected table instruction', instruction))
            pc += 1
    raise ValueError('reviewer bounded-run limit')


def digits(n):
    require(type(n) is int and n >= 0, 'nonnegative fixture integer')
    return ''.join(str(n // (2**k) % 2) for k in range(max(1, n.bit_length())))


def encode(values):
    parts = []
    for name, _ in r.SCHEMA:
        word = digits(values[name])
        parts.extend(('1'*len(word), '0', word))
    return ''.join(parts)


def decode(text):
    result = {}
    cursor = 0
    for name, _ in r.SCHEMA:
        start = cursor
        while cursor < len(text) and text[cursor] == '1':
            cursor += 1
        width = cursor-start
        require(width > 0 and cursor < len(text) and text[cursor] == '0', 'header length')
        cursor += 1
        value = text[cursor:cursor+width]
        require(len(value) == width and (value == '0' or value[-1] == '1'), 'canonical digits')
        result[name] = sum((v == '1') * (2**k) for k,v in enumerate(value))
        cursor += width
    require(cursor == len(text), 'exact schema extent')
    return result


def prepare_and_split(divisor, header, payload):
    ports = [Hardware(offset=2+(i % 7)) for i in range(r.FIRST_ROLE+divisor)]
    ports[r.HEADER] = Hardware(encode(header), offset=11)
    saved_header = ports[r.HEADER].text()
    interpret(r.compile_prepare(divisor), ports)
    child = decode(ports[r.CHILD_HEADER].text())
    expected = dict(header, rows=header['rows']//divisor, stock=header['stock']//divisor)
    require(child == expected and ports[r.HEADER].text() == saved_header, 'exact row-only child descriptor')
    ports[r.HEADER] = Hardware(encode(child), offset=9)
    ports[r.CHILD_HEADER] = Hardware(offset=4)
    ports[r.SOURCE] = Hardware(payload, offset=13)
    interpret(r.compile_router(divisor), ports)
    fields = [ports[r.FIRST_ROLE+w].text() for w in range(divisor)]
    for port in ports:
        port.check()
    return child, fields


def merge(divisor, header, fields):
    ports = [Hardware(offset=1+(i % 11)) for i in range(r.FIRST_ROLE+divisor)]
    ports[r.HEADER] = Hardware(encode(header), offset=10)
    for w, field in enumerate(fields):
        ports[r.FIRST_ROLE+w] = Hardware(field, offset=4+w)
    interpret(r.compile_router(divisor, True), ports)
    for port in ports:
        port.check()
    require(all(ports[r.FIRST_ROLE+w].text() == '' for w in range(divisor)), 'consumed child roles')
    return ports[r.OUTPUT].text()


def run():
    results = []
    for first, second, quotient, outer, row_bits in ((2,3,2,2,7), (3,2,1,3,11),
                                                     (5,7,1,1,6), (6,4,2,2,3)):
        rows = first*second*quotient
        header = {name: (i*7) % 19 for i,(name,_) in enumerate(r.SCHEMA)}
        header.update(outer=outer, rows=rows, stock=first*second, row_bits=row_bits)
        payload = ''.join(str((i*i+3*i+(i//5)) % 2) for i in range(outer*rows*row_bits))
        child, fields = prepare_and_split(first, header, payload)
        chosen = first-1
        grandchild, grandfields = prepare_and_split(second, child, fields[chosen])
        for w, field in enumerate(grandfields):
            # One known rowwise transformation, including nonbinary-code-shaped bits.
            grandfields[w] = ''.join(str(int(v) ^ ((j % row_bits == 0) and (w % 2 == 0)))
                                     for j,v in enumerate(field))
        fields[chosen] = merge(second, grandchild, grandfields)
        actual = merge(first, child, fields)
        expected = list(payload)
        for coordinate in range(outer*rows):
            row = coordinate % rows
            if row % first == chosen and (row // first) % second % 2 == 0:
                position = coordinate*row_bits
                expected[position] = str(1-int(expected[position]))
        require(actual == ''.join(expected), 'nested row transform at exact arithmetic address')
        bad = dict(header, stock=max(first,second))
        try:
            c_bad, bad_fields = prepare_and_split(first, bad, payload)
            prepare_and_split(second, c_bad, bad_fields[chosen])
        except ValueError:
            pass
        else:
            raise ValueError('max stock admitted in place of product')
        results.append(dict(first=first, second=second, quotient=quotient, outer=outer,
                            row_bits=row_bits, bits=len(payload)))
    try:
        r.compile_prepare(2, kind=r.MATCHED)
    except ValueError:
        pass
    else:
        raise ValueError('matched occurrence consumed rows')
    print(json.dumps(dict(status='PASS_ROOT_INDEPENDENT_NESTED_ROW_DISPATCH', cases=results,
                          source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest()), sort_keys=True))


if __name__ == '__main__':
    run()
