"""Independent fixture loading/observation; never imported by row programs."""
from dataclasses import dataclass, field


@dataclass
class Tape:
    cells: dict = field(default_factory=dict)
    head: int = 0
    marker: int = -1
    low: int = -1
    high: int = 0
    reads: int = 0
    writes: int = 0
    moves: int = 0

    @classmethod
    def fixture(cls, word="", origin=0, blank_tail=0):
        cells = {origin-1: "|"}
        cells.update({origin+i: bit for i, bit in enumerate(word)})
        cells.update({origin+len(word)+i: "_" for i in range(blank_tail)})
        return cls(cells, origin, origin-1, origin-1, origin)

    def _visit(self):
        self.low = min(self.low, self.head)
        self.high = max(self.high, self.head)

    def read(self):
        self._visit()
        self.reads += 1
        return self.cells.get(self.head, "_")

    def write(self, bit):
        self._visit()
        self.writes += 1
        self.cells[self.head] = bit

    def move(self, direction):
        if direction not in (-1, 1):
            raise ValueError("unit move only")
        self.head += direction
        self.moves += 1
        self._visit()

    def word(self):
        out = []
        position = self.marker + 1
        while self.cells.get(position, "_") != "_":
            out.append(self.cells[position])
            position += 1
        return "".join(out)

    def load(self, word):
        self.cells = {self.marker: "|", **{self.marker+1+i: b for i,b in enumerate(word)}}
        self.head = self.marker+1


def binary(value):
    if type(value) is not int or value < 0:
        raise ValueError("fixture nonnegative integer")
    return bin(value)[2:][::-1]


def encode_header(schema, values):
    out = []
    for name, _ in schema:
        bits = binary(values[name])
        out.append("1"*len(bits)+"0"+bits)
    return "".join(out)


def decode_header(schema, word):
    result = {}
    at = 0
    for name, _ in schema:
        length = 0
        while at < len(word) and word[at] == "1":
            length += 1
            at += 1
        if not length or at >= len(word) or word[at] != "0":
            raise ValueError("bad fixture header prefix")
        at += 1
        digits = word[at:at+length]
        if len(digits) != length or (digits[-1] != "1" and digits != "0"):
            raise ValueError("bad fixture canonical digits")
        result[name] = int(digits[::-1], 2)
        at += length
    if at != len(word):
        raise ValueError("extra fixture header")
    return result


def values(schema, *, outer=1, rows=6, stock=6, row_bits=1):
    out = {name: 0 for name, _ in schema}
    out.update(outer=outer, rows=rows, stock=stock, row_bits=row_bits,
               within_bits=0, record_bits=row_bits, p=16, d=8, K=2,
               G=1, H=1, q0=2, qF=1, qB=1, D=8, f=1, rho=1,
               active_start=2, back_start=6, selected_axes=2)
    return out


def ports(count, *, shifted=False):
    return [Tape.fixture(origin=(7*i-40 if shifted else 0), blank_tail=i%5)
            for i in range(count)]
