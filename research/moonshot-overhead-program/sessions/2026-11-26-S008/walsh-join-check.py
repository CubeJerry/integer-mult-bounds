#!/usr/bin/env python3
"""Replay finite and spatial Walsh address joins on arbitrary replaced records."""

from array import array
from itertools import product
import json
from pathlib import Path
import random
import runpy


def checksum_record(value, offset, stage):
    """Deterministic, invertible-in-value replacement depending on the true address."""
    return ((value * 6364136223846793005 + 1442695040888963407 + 1009 * offset + stage)
            & ((1 << 64) - 1))


def finite_case(rng, copies, labels, seeds, leading, prefix, axis, suffix):
    """Construct each check arm in parent order, replay child interpretation and true return."""
    assert copies % 8 == 0 and seeds % 16 == 0
    rank = seeds // 16
    row_bits = prefix * axis * suffix  # one fixture cell is an arbitrary 64-bit numerical record
    rows = copies * labels * 2 * rank
    tensor = []
    for L, c, lab, arm, h in product(range(leading), range(copies), range(labels), range(2), range(rank)):
        tensor.extend(rng.getrandbits(64) for _ in range(row_bits))
    incoming = array('Q', tensor)
    visits = 0
    for stage in (1, 2):
        # The child's actual c',lab',i' loops see a contiguous file. No payload repack is performed.
        reply = array('Q')
        cursor = 0
        for L, child_c, child_label, child_seed in product(
                range(leading), range(copies // 8), range(labels), range(seeds)):
            child_tag = stage + 3 * L + 13 * child_c + 29 * child_label + 53 * child_seed
            for old_p, new_x, old_z in product(range(prefix), range(axis), range(suffix)):
                old_x = (new_x + stage) % axis
                old_offset = (old_p * axis + old_x) * suffix + old_z
                new_offset = (old_p * axis + new_x) * suffix + old_z
                reply.append(checksum_record(incoming[cursor + old_offset], new_offset, child_tag))
            cursor += row_bits
        assert cursor == len(incoming) == len(reply)
        # Independent parent traversal uses the original arm and rank tuple after child mutation.
        for L, c, lab, arm, h, p, x, z in product(
                range(leading), range(copies), range(labels), range(2), range(rank),
                range(prefix), range(axis), range(suffix)):
            coarse = ((c * labels + lab) * 2 + arm) * rank + h
            child_c, residual = divmod(coarse, labels * seeds)
            child_lab, child_seed = divmod(residual, seeds)
            assert (0 <= child_c < copies // 8 and 0 <= child_lab < labels
                    and 0 <= child_seed < seeds)
            oracle_offset = (p * axis + x) * suffix + z
            reference_row = L * rows + coarse
            oracle_input = reference_row * row_bits + (p * axis + (x + stage) % axis) * suffix + z
            assert reply[reference_row * row_bits + oracle_offset] == checksum_record(
                incoming[oracle_input], oracle_offset,
                stage + 3 * L + 13 * child_c + 29 * child_lab + 53 * child_seed)
            visits += 1
        incoming = reply
    return visits


def extract_parent_row(bank, leading, roles, role, extent):
    result = array('Q')
    for outer in range(leading):
        at = (outer * roles + role) * extent
        result.extend(bank[at:at + extent])
    return result


def restore_parent_row(bank, replacement, leading, roles, role, extent):
    result = array('Q', bank)
    for outer in range(leading):
        at = (outer * roles + role) * extent
        result[at:at + extent] = replacement[outer * extent:(outer + 1) * extent]
    return result


def spatial_case(rng, W1, W2, outer, prefix, axis, suffix, first, second):
    """Two genuine extractions must consume fresh leading digits and preserve all old extents."""
    leading = outer * W2
    extent = prefix * axis * suffix
    bank = array('Q', (rng.getrandbits(64) for _ in range(leading * W1 * extent)))
    selected = extract_parent_row(bank, leading, W1, first, extent)
    next_role = extract_parent_row(selected, outer, W2, second, extent)
    changed = array('Q')
    for L, p, x, z in product(range(outer), range(prefix), range(axis), range(suffix)):
        old_index = ((L * prefix + p) * axis + (x ^ (axis - 1))) * suffix + z
        changed.append(checksum_record(next_role[old_index], (p * axis + x) * suffix + z, 7))
    selected = restore_parent_row(selected, changed, outer, W2, second, extent)
    restored = restore_parent_row(bank, selected, leading, W1, first, extent)
    changed_count = 0
    for j, output in enumerate(restored):
        row, wordpos = divmod(j, extent)
        L, original_role = divmod(row, W1)
        if original_role == first and L % W2 == second:
            p, remainder = divmod(wordpos, axis * suffix)
            x, z = divmod(remainder, suffix)
            source_index = row * extent + (p * axis + (x ^ (axis - 1))) * suffix + z
            assert output == checksum_record(bank[source_index], wordpos, 7)
            changed_count += 1
        else:
            assert output == bank[j]
    assert changed_count == outer * extent
    return len(bank), changed_count


def physical_role_copy(machine, program, source, destination, leading, src_count, dst_count,
                       src_role, dst_role, run_bits):
    """Execute the fixed 15-head role copier. Its controls receive only binary descriptors."""
    source_width = src_count * run_bits
    destination_width = dst_count * run_bits
    assert len(source) == leading * source_width
    assert len(destination) == leading * destination_width
    inputs = {"A": source, "Y": destination}
    for tape, number in (("J", src_count), ("K", dst_count), ("I", src_role),
                         ("D", dst_role), ("S", run_bits)):
        inputs[tape] = format(number, 'b')
    volume = len(source) + len(destination)
    sim = machine(program, inputs).execute(103 * volume)
    expected = bytearray(destination, 'ascii')
    for prefix in range(leading):
        start = prefix * source_width + src_role * run_bits
        target = prefix * destination_width + dst_role * run_bits
        expected[target:target + run_bits] = source[start:start + run_bits].encode('ascii')
    copied = sim.contents('Y')
    assert copied == expected.decode('ascii')
    for tape in sim.tapes:
        assert sim.head[tape] == 0
        if tape != 'Y':
            assert sim.contents(tape) == inputs.get(tape, '')
    assert sim.visited <= 30 * volume
    return copied, sim.steps, sim.visited


def physical_spatial_cases(rng):
    """Return arbitrary changed children twice through genuine nested head scans."""
    library = runpy.run_path(str(Path(__file__).with_name('node-tapes.py')))
    program = library['build_role'](xor=False)
    machine = library['Simulation']
    shapes = ((1, 2, 2, 1, 2, 1, 7, 0, 1), (3, 4, 2, 2, 4, 1, 8, 3, 0),
              (2, 2, 4, 1, 4, 3, 11, 1, 2), (1, 4, 4, 2, 4, 3, 13, 0, 3),
              (1, 8, 4, 1, 4, 1, 100, 5, 2), (1, 4, 8, 1, 2, 3, 73, 3, 6),
              (1, 16, 8, 1, 2, 1, 9, 11, 3), (3, 1, 2, 3, 2, 1, 5, 0, 1))
    calls = steps = parent_records = changed_records = max_cells = 0
    for outer, first_count, second_count, pre, axis, post, width, first, second in shapes:
        row_records = pre * axis * post
        run_bits = row_records * width
        def random_bits(count):
            return format(rng.getrandbits(count), f'0{count}b')
        original = random_bits(outer * second_count * first_count * run_bits)
        def copy(src, dst, p, J, K, i, d):
            nonlocal steps, calls, max_cells
            result, elapsed, visited = physical_role_copy(machine, program, src, dst, p, J, K,
                                                         i, d, run_bits)
            steps += elapsed
            calls += 1
            max_cells = max(max_cells, visited)
            return result
        first_bank = copy(original, random_bits(outer * second_count * run_bits),
                          outer * second_count, first_count, 1, first, 0)
        second_bank = copy(first_bank, random_bits(outer * run_bits),
                           outer, second_count, 1, second, 0)
        # The reply reflects every active axis, then complements its fixed-width word.
        # Its old prefix, suffix, and the independent leading reserve stay in place.
        changed = []
        expected = bytearray(original, 'ascii')
        for p, prefix, x, suffix in product(range(outer), range(pre), range(axis), range(post)):
            offset = ((p * pre + prefix) * axis + (axis - 1 - x)) * post + suffix
            word = second_bank[offset * width:(offset + 1) * width]
            new_word = ''.join('0' if v == '1' else '1' for v in word)
            changed.append(new_word)
            old_role = (p * second_count + second) * first_count + first
            start = (old_role * row_records + (prefix * axis + x) * post + suffix) * width
            expected[start:start + width] = new_word.encode('ascii')
        restored_first = copy(''.join(changed), first_bank, outer, 1, second_count, 0, second)
        restored_parent = copy(restored_first, original, outer * second_count,
                               1, first_count, 0, first)
        assert restored_parent == expected.decode('ascii')
        parent_records += len(original) // width
        changed_records += len(changed)
    return dict(physical_cases=len(shapes), physical_calls=calls,
                physical_head_transitions=steps, physical_peak_cells=max_cells,
                physical_parent_records=parent_records, physical_selected_records=changed_records)


def main():
    rng = random.Random(51083)
    finite_records = finite_cases = spatial_records = changed = spatial_cases = 0
    for copies, labels, seeds in product((8, 64), (1, 4), (16, 32, 64)):
        leading, prefix, axis, suffix = rng.choice((1, 3)), rng.choice((1, 3)), 4, rng.choice((1, 3))
        finite_records += finite_case(rng, copies, labels, seeds, leading, prefix, axis, suffix)
        finite_cases += 1
    for W1, W2 in product((2, 4, 8), (2, 4, 8)):
        for first, second in product(range(W1), range(W2)):
            records, count = spatial_case(rng, W1, W2, 3, 2, 4, 3, first, second)
            spatial_records += records
            changed += count
            spatial_cases += 1
    results = dict(finite_two_arm_cases=finite_cases, finite_return_records=finite_records,
                   nested_spatial_cases=spatial_cases, spatial_records=spatial_records,
                   replaced_selected_records=changed)
    results.update(physical_spatial_cases(rng))
    print(json.dumps(results, sort_keys=True))


if __name__ == '__main__':
    main()
