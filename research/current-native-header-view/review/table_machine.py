"""Independent local-symbol interpreter for the native header review.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
This is reviewer hardware and an observer, not a production supplier or tariff.
It imports no author's tape, table executor, encoder, or expected-output code.
"""
from collections import Counter


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Tape:
    def __init__(self, body="", origin=0, readonly=False):
        require(type(origin) is int and origin >= 0, "nonnegative translated origin")
        require(set(body) <= {"0", "1"}, "binary fixture body")
        self.origin = origin
        self.position = origin
        self.cells = {origin - 1: "|"}
        self.cells.update({origin + i: bit for i, bit in enumerate(body)})
        self.prefix = {origin - 3: "prefix-A", origin - 2: "prefix-B"}
        self.cells.update(self.prefix)
        self.readonly = readonly
        self.counts = Counter()
        self.visited_maximum = origin + len(body)
        self.written_maximum = origin + len(body)

    def read(self):
        require(self.position >= self.origin - 1, "read crossed local marker")
        self.counts["read"] += 1
        return self.cells.get(self.position, "_")

    def write(self, value):
        require(not self.readonly, "write to borrowed descriptor")
        require(self.position >= self.origin, "write to marker or ancestor")
        require(value in ("0", "1", "_"), "binary physical alphabet")
        self.counts["write"] += 1
        self.written_maximum = max(self.written_maximum, self.position + 1)
        if value == "_":
            self.cells.pop(self.position, None)
        else:
            self.cells[self.position] = value

    def move(self, direction):
        require(direction in (-1, 1), "unit local movement")
        require(self.position + direction >= self.origin - 1, "move crossed local marker")
        self.position += direction
        self.visited_maximum = max(self.visited_maximum, self.position + 1)
        self.counts["move"] += 1

    def inspect(self):
        """Observer only: require a complete contiguous binary body."""
        offset = self.origin
        chars = []
        while self.cells.get(offset, "_") != "_":
            value = self.cells[offset]
            require(value in ("0", "1"), "nonbinary observed body")
            chars.append(value)
            offset += 1
        require(all(pos < self.origin or pos < offset for pos in self.cells),
                "nonblank cells after current frontier")
        return "".join(chars)

    def quiescent(self, expected=""):
        require(self.position == self.origin, "unrestored local head")
        require(self.cells.get(self.origin - 1) == "|", "changed local marker")
        require(all(self.cells.get(k) == v for k, v in self.prefix.items()),
                "changed protected predecessor cells")
        require(self.inspect() == expected, "wrong complete observed body")


def execute(table, tapes, step_cap=50_000_000):
    """Interpret the emitted finite graph, without the production run routine."""
    pc = 0
    counts = Counter()
    for _ in range(step_cap):
        require(type(pc) is int and 0 <= pc < len(table), "control target outside table")
        row = table[pc]
        opcode = row[0]
        counts[opcode] += 1
        if opcode == "done":
            return dict(counts)
        if opcode in ("reject", "quarantine"):
            raise ValueError("table terminal " + opcode)
        if opcode == "goto":
            require(len(row) == 2, "goto arity")
            pc = row[1]
            continue
        require(opcode in ("read", "write", "move"), "unknown table opcode")
        require(len(row) == 3 and type(row[1]) is int and 0 <= row[1] < len(tapes),
                "local operation arity and role")
        target = tapes[row[1]]
        if opcode == "read":
            value = target.read()
            require(value in row[2], "incomplete local-symbol branch")
            pc = row[2][value]
        elif opcode == "write":
            target.write(row[2])
            pc += 1
        else:
            target.move(row[2])
            pc += 1
    raise ValueError("independent observer step cap")


SCHEMA = (
    "outer", "rows", "stock", "row_bits", "within_bits", "record_bits", "p", "d",
    "K", "G", "H", "q0", "qF", "qB", "D", "f", "rho", "active_start",
    "back_start", "selected_axes", "entry_start", "remainder", "cutoff",
)


def encode(values):
    words = []
    for name in SCHEMA:
        value = values[name]
        require(type(value) is int and value >= 0, "observer natural header value")
        digits = format(value, "b")[::-1]
        words.append("1" * len(digits) + "0" + digits)
    return "".join(words)


def decode(bits):
    """An independent host observer; never called by production control."""
    position = 0
    result = {}
    for name in SCHEMA:
        length = 0
        while position < len(bits) and bits[position] == "1":
            length += 1
            position += 1
        require(length > 0 and position < len(bits) and bits[position] == "0",
                "positive length prefix")
        position += 1
        digits = bits[position:position + length]
        require(len(digits) == length and set(digits) <= {"0", "1"}, "complete binary value")
        require(length == 1 or digits[-1] == "1", "canonical binary value")
        result[name] = int(digits[::-1], 2)
        position += length
    require(position == len(bits), "exact complete header frontier")
    return result


def expected_view(parent):
    result = dict(parent)
    result["selected_axes"] = 9 * parent["f"]
    result["entry_start"] = parent["active_start"]
    result["remainder"] = 0
    return result
