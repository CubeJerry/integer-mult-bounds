"""Independently compose the published role, tag, actual interchange and wrapper rules."""
from itertools import product
from pathlib import Path
from random import Random
from runpy import run_path
import json

HERE = Path(__file__).parent
PORT = run_path(str(HERE / "node-tapes.py"))
HANDOFF = run_path(str(HERE / "recount-handoff.py"))
COPY = PORT["build_role"](xor=False)
XOR = PORT["build_role"](xor=True)
CHILD = PORT["build_direct"]()
TAGS = {inv: PORT["build_tag"](inverse=inv) for inv in (True, False)}
RNG = Random(612877)
totals = dict(grouped_children=0, grouped_copy=0, grouped_xor=0, tag_pass=0,
              tag_pairs=0, raw_transitions=0, contracted_transitions=0,
              full_transitions=0, full_children=0, rejected_major_order=0)


def word(n):
    return "".join(RNG.choice("01") for _ in range(n))


def binary(**values):
    return {name: format(value, "b") for name, value in values.items()}


def run(program, inp, changed, budget):
    sim = PORT["Simulation"](program, inp).execute(budget)
    assert all(position == 0 for position in sim.head.values())
    for tape in sim.tapes:
        if tape != changed:
            assert sim.contents(tape) == inp.get(tape, "")
    totals["raw_transitions"] += sim.steps
    return sim.contents(changed)


def role(source, dest, *, source_count, dest_count, src, dst, suffix, xor=False):
    inp = dict(A=source, Y=dest, **binary(J=source_count, K=dest_count,
                                         I=src, D=dst, S=suffix))
    totals["grouped_xor" if xor else "grouped_copy"] += 1
    return run(XOR if xor else COPY, inp, "Y", 103 * (len(source) + len(dest)))


def grouped_child(prefix, roles, kept, gap, suffix, width, modules):
    bits_per_role = modules * 9 * gap * suffix * width
    neutral_width = len(kept)
    perm = list(reversed(range(roles)))
    RNG.shuffle(perm)
    targets = perm[:neutral_width]
    source = word(prefix * roles * bits_per_role)
    prior = word(len(source))
    gathered = "0" * (prefix * neutral_width * bits_per_role)
    for new, old in enumerate(kept):
        gathered = role(source, gathered, source_count=roles, dest_count=neutral_width,
                        src=old, dst=new, suffix=bits_per_role)
    source_offset = lambda p, r: (p * roles + r) * bits_per_role
    gather_oracle = "".join(source[source_offset(p, r):source_offset(p, r) + bits_per_role]
                            for p in range(prefix) for r in kept)
    assert gathered == gather_oracle
    wrong = "".join(source[source_offset(p, r):source_offset(p, r) + bits_per_role]
                    for r in kept for p in range(prefix))
    if prefix > 1:
        assert gathered != wrong
        totals["rejected_major_order"] += 1

    field_suffix = suffix * width
    actual = run(CHILD, dict(A=gathered, **binary(E=1, G=gap, S=field_suffix)),
                 "A", 512 * len(gathered))
    values = list(prior)
    for p, k, mod, x, g, y, z in product(range(prefix), range(neutral_width),
                                         range(modules), range(3), range(gap),
                                         range(3), range(field_suffix)):
        relative = (((mod * 3 + y) * gap + g) * 3 + x) * field_suffix + z
        target = (((mod * 3 + x) * gap + g) * 3 + y) * field_suffix + z
        old = source_offset(p, kept[k]) + relative
        new = source_offset(p, targets[k]) + target
        assert actual[(p * neutral_width + k) * bits_per_role + target] == source[old]
        values[new] = str(int(values[new]) ^ int(source[old]))

    ctrl = [(format(roles, "b"), 1), (format(gap, "b"), 0)]
    heap = [(source, len(source) // 2), (prior, len(prior) + 1), ("", 0)]
    totals["contracted_transitions"] += HANDOFF["check_contracted"](
        heap, ctrl, gathered, actual, "Ib10fL")
    out = prior
    for k, target_role in enumerate(targets):
        out = role(actual, out, source_count=neutral_width, dest_count=roles,
                   src=k, dst=target_role, suffix=bits_per_role, xor=True)
    assert out == "".join(values)
    totals["grouped_children"] += 1


def tag_pair(prefix, suffix, width, signs):
    count = prefix * 81 * suffix
    records = word(count * width)
    keyed = records
    for k, (gap, after) in enumerate(((3, 3 * suffix), (3, suffix))):
        inp = dict(A=keyed, **binary(T=3, G=gap, S=after, H=width + 2 * k))
        keyed = run(TAGS[signs[k]], inp, "Y", 512 * len(keyed))
        totals["tag_pass"] += 1
    chunks = []
    for p, x1, x2, y1, y2, s in product(range(prefix), range(3), range(3),
                                        range(3), range(3), range(suffix)):
        row = ((((p * 3 + x1) * 3 + x2) * 3 + y1) * 3 + y2) * suffix + s
        piece = records[row * width:(row + 1) * width]
        for a, b, inv in ((x1, y1, signs[0]), (x2, y2, signs[1])):
            cmp = int(a < b) - int(a > b)
            piece += format((-cmp if inv else cmp) % 3, "02b")
        chunks.append(piece)
    assert keyed == "".join(chunks)
    clean = "0" * len(records)
    for bit in range(width):
        clean = role(keyed, clean, source_count=width + 4, dest_count=width,
                     src=bit, dst=bit, suffix=1)
    assert clean == records
    totals["tag_pairs"] += 1


def reserve_chain(prefix, suffix):
    layout = (prefix, 3, 3, 3, 3, suffix)
    active = word(prefix * 81 * suffix)
    current = active
    for i, j in ((0, 2), (1, 3), (0, 1), (1, 3)):
        gap = 3 ** (j - i - 1)
        trailing = 3 ** (3 - j) * suffix
        result = run(CHILD, dict(A=current, **binary(E=1, G=gap, S=trailing)),
                     "A", 512 * len(current))
        expected = []
        for address in product(*(range(d) for d in layout)):
            changed = list(address)
            changed[1 + i], changed[1 + j] = changed[1 + j], changed[1 + i]
            index = 0
            for digit, radix in zip(changed, layout):
                index = index * radix + digit
            expected.append(current[index])
        assert result == "".join(expected)
        ctrl = [(format(gap, "b"), 1), (format(trailing, "b"), 0)]
        totals["full_transitions"] += HANDOFF["check_reserve"](
            current, result, ctrl, "fIR0", 0)
        totals["full_children"] += 1
        current = result
    assert active != current


def main():
    for p, (j, chosen), (g, s, w, module) in product(
            (1, 2, 3), ((3, (2, 0)), (5, (3, 0, 4))),
            ((1, 1, 1, 1), (2, 1, 2, 1), (1, 2, 1, 2))):
        grouped_child(p, j, chosen, g, s, w, module)
    for p, (s, w), inv in product((1, 2), ((1, 1), (2, 2)),
                                  product((False, True), repeat=2)):
        tag_pair(p, s, w, inv)
    for p, s in ((1, 1), (2, 2), (3, 1)):
        reserve_chain(p, s)
    print(json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
