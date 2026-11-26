#!/usr/bin/env python3
"""Replay finite and spatial Walsh address joins on arbitrary replaced records."""

from array import array
from itertools import product
import json
import random


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
    print(json.dumps(dict(finite_two_arm_cases=finite_cases, finite_return_records=finite_records,
                          nested_spatial_cases=spatial_cases, spatial_records=spatial_records,
                          replaced_selected_records=changed), sort_keys=True))


if __name__ == '__main__':
    main()
