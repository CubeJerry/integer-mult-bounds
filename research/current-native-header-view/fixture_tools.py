"""Fixture construction and observers; never imported by production tables.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from header_view import S, R, SCHEMA, PARENT, VIEW, PRIVATE, HeaderView
from header_sources import need


def values(f=2, remainder=13, K=2, rho=1, outer=3, rows=6, stock=3, G=1,
           extra=11, tail=3):
    need(0 <= remainder < 145 and f > 0 and 0 <= rho < K, "fixture ordinary geometry")
    e = 145 * f + remainder
    H = e * G
    entry = 2 * H + 5
    active = entry + remainder * K
    back = entry + e * K + extra
    a = back + H + tail
    b = 60
    return dict(outer=outer, rows=rows, stock=stock, row_bits=b << a,
                within_bits=a, record_bits=b, p=max(1024, e), d=e, K=K, G=G, H=H,
                q0=3, qF=4, qB=5, D=e, f=f, rho=rho, active_start=active,
                back_start=back, selected_axes=e, entry_start=entry,
                remainder=remainder, cutoff=145)


def native_values(parent):
    out = dict(parent)
    out.update(selected_axes=9 * parent["f"], entry_start=parent["active_start"], remainder=0)
    return out


def encode(values):
    out = []
    for name in SCHEMA:
        digits = [int(x) for x in bin(values[name])[2:][::-1]]
        out += [1] * len(digits) + [0] + digits
    return out


def decode(bits):
    at, result = 0, {}
    for name in SCHEMA:
        length = 0
        while at < len(bits) and bits[at] == 1:
            length += 1
            at += 1
        need(length and at < len(bits) and bits[at] == 0, "observer length prefix")
        at += 1
        digits = bits[at:at + length]
        need(len(digits) == length and all(x in (0, 1) for x in digits), "observer binary digits")
        need(length == 1 or digits[-1] == 1, "observer canonical number")
        result[name] = sum(bit << j for j, bit in enumerate(digits))
        at += length
    need(at == len(bits), "observer exact complete header")
    return result


def put(tape, bits):
    """Load fixture input without ever shrinking retained backing."""
    stop = tape.origin + len(bits)
    if len(tape.cells) < stop:
        tape.cells.extend([6] * (stop - len(tape.cells)))
    tape.cells[tape.origin:stop] = bytearray(bits)
    for j in range(stop, len(tape.cells)):
        tape.cells[j] = 6
    tape.head = tape.origin
    tape.high = max(tape.high, stop)


def body(tape):
    out = []
    ended = False
    for value in tape.cells[tape.origin:]:
        if value == 6:
            ended = True
        else:
            need(not ended and value in (0, 1), "observer complete prefix without hidden tail")
            out.append(value)
    return out


def hardware():
    owner = HeaderView()
    work = [S.codec.DenseTape(3 + i % 5) for i in PRIVATE]
    parent = S.codec.DenseTape(11)
    for tape in (*work, parent):
        for i in range(tape.origin - 1):
            tape.cells[i] = i % 2
    owner.bind(work, S.abi.BinaryContextPort(parent))
    return owner, work, parent


def snapshots(tapes):
    return [bytes(t.cells[:t.origin]) for t in tapes]


def restored(work, parent, original, ancestors):
    need(body(parent) == original and parent.head == parent.origin, "parent contents and origin")
    need(all(t.head == t.origin and all(x == 6 for x in t.cells[t.origin:]) for t in work),
         "complete private retirement and origins")
    need(snapshots((*work, parent)) == ancestors, "parked ancestor prefixes unchanged")


def source_parent(parent_values, live=False):
    """Execute the retained ordinary geometry producer before the new view.

The input/output fixture observer uses Python integers. The retained physical
program derives f, remainder and active_start entirely on encoded tapes.
"""
    b = R.Builder()
    fields = tuple(port for _, port in R.SCHEMA)
    for port in range(R.FIRST_ROLE):
        b.boundary(port)
    b.decode(PARENT, fields)
    b.derive_geometry(145, child=False)
    b.encode(fields, VIEW)
    for port in (*fields, R.LENGTH, R.TEMP, R.GUIDE_S, R.OFFSET, R.CONSTANT):
        b.clear(port)
    program = b.close()
    owner, work, parent = hardware()
    initial = dict(parent_values, f=0, remainder=0, active_start=0)
    put(parent, encode(initial))
    steps = R.run(program, owner.ports)
    result = body(owner.ports[VIEW].tape)
    need(decode(result) == parent_values, "actual retained ordinary producer endpoint")
    report = dict(source_program_instructions=len(program), source_program_steps=steps)
    if live:
        return owner.ports[VIEW].tape, owner, work, parent, report
    # The output is observer-copied as fixture input, not an uncharged runtime
    # conversion. Runtime composition borrows this same output port directly.
    owner.active = True
    owner.release()
    return result, report
