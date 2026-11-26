#!/usr/bin/env python3
"""Check the occupied-fat-lane tensor compiler against its original native arrays."""
import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass


def coordinates(shape):
    return itertools.product(*(range(side) for side in shape))


def rank(point, shape):
    number = 0
    for coordinate, side in zip(point, shape):
        number = number * side + coordinate
    return number


def gf4_product(a, b):
    # F2[w] / (w^2+w+1), independent scalar reference.
    raw = (a if b & 1 else 0) ^ (a << 1 if b & 2 else 0)
    return raw ^ (7 if raw & 4 else 0)


def gf4_inverse(a):
    return (0, 1, 3, 2)[a]


def scaleword(word, scalar, even_mask):
    if scalar == 1:
        return word
    if scalar == 0:
        return 0
    low = word & even_mask
    high = word ^ low
    by_w = (high >> 1) ^ (low << 1) ^ high
    return by_w if scalar == 2 else by_w ^ word


@dataclass
class Layout:
    native: tuple
    strip: int
    missing: int

    def __post_init__(self):
        self.d = len(self.native)
        self.full = tuple(1 << (x * self.d - 1).bit_length() for x in self.native)
        self.m = tuple(f // a for f, a in zip(self.full, self.native))
        self.all_lanes = self.strip * math.prod(self.m)
        self.lanes = self.all_lanes - self.missing
        assert 0 < self.lanes <= self.all_lanes and self.missing < self.strip
        self.mask = sum(1 << (2 * lane) for lane in range(self.strip))
        self.native_mask = sum(1 << (2 * lane) for lane in range(self.all_lanes))
        self.full_points = list(coordinates(self.full))
        self.native_points = list(coordinates(self.native))
        self.genuine = []
        for row, point in enumerate(self.full_points):
            if all(y < a * copies for y, a, copies in zip(point, self.native, self.m)):
                x = tuple(y % a for y, a in zip(point, self.native))
                s = tuple(y // a for y, a in zip(point, self.native))
                self.genuine.append((row, rank(x, self.native), rank(s, self.m)))
        assert len(self.genuine) == math.prod(self.native) * math.prod(self.m)
        assert math.prod(self.full) <= math.e * math.prod(self.native) * math.prod(self.m)

    def read_native(self, rows):
        by_point = [0] * math.prod(self.native)
        for physical, native, bank in self.genuine:
            by_point[native] |= rows[physical] << (2 * self.strip * bank)
        return by_point


def new_monomial(shape, rng):
    permutations, factors = [], []
    for a in shape:
        digits = list(range(a))
        rng.shuffle(digits)
        permutations.append(digits)
        factors.append([rng.randrange(1, 4) for _ in range(a)])
    return ('monomial', (permutations, factors))


def new_shear(shape, counts, rng):
    pairs = []
    for a, count in zip(shape, counts):
        digits = list(range(a))
        rng.shuffle(digits)
        pairs.append(list(zip(digits[::2], digits[1::2]))[:count])
    return ('shear', pairs)


def inverse_letter(letter):
    kind, data = letter
    if kind == 'shear':
        return letter
    perms, factors = data
    inverse_perm, inverse_factor = [], []
    for perm, scalars in zip(perms, factors):
        p, s = [0] * len(perm), [0] * len(perm)
        for a, b in enumerate(perm):
            p[b], s[b] = a, gf4_inverse(scalars[a])
        inverse_perm.append(p)
        inverse_factor.append(s)
    return ('monomial', (inverse_perm, inverse_factor))


def native_letter(rows, layout, letter):
    # Ground truth performs one original logical axis at a time. It never sees encoded digits.
    kind, data = letter
    for axis in range(layout.d):
        result = rows.copy()
        if kind == 'monomial':
            perm, scalars = data[0][axis], data[1][axis]
            for src, point in enumerate(layout.native_points):
                old = point[axis]
                dest = point[:axis] + (perm[old],) + point[axis + 1:]
                result[rank(dest, layout.native)] = scaleword(rows[src], scalars[old], layout.native_mask)
        else:
            changes = dict(data[axis])
            for dest, point in enumerate(layout.native_points):
                old = point[axis]
                if old in changes:
                    src = point[:axis] + (changes[old],) + point[axis + 1:]
                    result[dest] ^= rows[rank(src, layout.native)]
        rows = result
    return rows


def physical_monomial(rows, layout, data):
    perm, scalars = data
    result = [None] * len(rows)
    for src, point in enumerate(layout.full_points):
        dest, multiplier = [], 1
        for g, y in enumerate(point):
            bank, x = divmod(y, layout.native[g])
            if bank < layout.m[g]:
                dest.append(perm[g][x] + bank * layout.native[g])
                multiplier = gf4_product(multiplier, scalars[g][x])
            else:
                dest.append(y)
        dest = rank(dest, layout.full)
        assert result[dest] is None
        result[dest] = scaleword(rows[src], multiplier, layout.mask)
    return result


def mask_pascal(inputs, active):
    # Literal subset formula after stable grouping of passive and active low positions.
    result = []
    for output in range(len(inputs)):
        free = active & ~output
        subset, value = free, inputs[output]
        while subset:
            value ^= inputs[output | subset]
            subset = (subset - 1) & free
        result.append(value)
    return result


def unconditional_pascal(values, d):
    outputs = values.copy()
    for g in range(d):
        step = 1 << g
        for low in range(1 << d):
            if not (low & step):
                outputs[low] ^= outputs[low + step]
    return outputs


def unconditional_pair_gate(inputs, active, layout):
    # Tensor of D(s) U D(s)^-1 D(t) U D(t)^-1, read from right to left.
    s = [2 if active & (1 << g) else 1 for g in range(layout.d)]
    t = [3 if active & (1 << g) else 1 for g in range(layout.d)]
    diagonals = ([gf4_inverse(b) for b in t],
                 [gf4_product(gf4_inverse(a), b) for a, b in zip(s, t)], s)
    rows = inputs.copy()
    for stage, coefficients in enumerate(diagonals):
        for low, word in enumerate(rows):
            factor = 1
            for g, value in enumerate(coefficients):
                if not (low & (1 << g)):
                    factor = gf4_product(factor, value)
            rows[low] = scaleword(word, factor, layout.mask)
        if stage != 2:
            rows = unconditional_pascal(rows, layout.d)
    return rows


def physical_shear(rows, layout, pairs, mode, stats):
    new_to_old, thresholds = [], []
    for g, native_pairs in enumerate(pairs):
        a = layout.native[g]
        first = [a * bank + x for bank in range(layout.m[g])
                 for pair in native_pairs for x in pair]
        active_slots = set(first)
        assert len(first) == len(active_slots)
        new_to_old.append(first + [y for y in range(layout.full[g]) if y not in active_slots])
        thresholds.append(len(native_pairs) if mode == 'omit_copies' else len(first) // 2)

    outputs = [None] * len(rows)
    for high in coordinates(tuple(f // 2 for f in layout.full)):
        active = sum(1 << g for g, h in enumerate(high) if h < thresholds[g])
        if mode == 'all_pairs':
            active = (1 << layout.d) - 1
        stats.add((layout.d, active))
        canonical = [rank(tuple(new_to_old[g][2 * h + ((low >> g) & 1)]
                                for g, h in enumerate(high)), layout.full)
                     for low in range(1 << layout.d)]
        inputs = [rows[i] for i in canonical]
        values = (unconditional_pair_gate(inputs, active, layout) if mode == 'diagonals'
                  else mask_pascal(inputs, active))
        for i, value in zip(canonical, values):
            assert outputs[i] is None
            outputs[i] = value
    return outputs


def physical_letter(rows, layout, letter, mode, stats):
    if letter[0] == 'monomial':
        return physical_monomial(rows, layout, letter[1])
    return physical_shear(rows, layout, letter[1], mode, stats)


def logical_mismatch(left, right, lanes):
    keep = (1 << (2 * lanes)) - 1
    return sum(((left_slot ^ right_slot) & keep).bit_count() for left_slot, right_slot in zip(left, right))


def fixture(layout, schedule, rng, direct_borrow=None):
    actual_rows = {i for i, _, _ in layout.genuine}
    raw = [rng.getrandbits(2 * layout.strip) for _ in layout.full_points]
    for i in set(range(len(raw))) - actual_rows:
        raw[i] = raw[i] or 1
    ground = layout.read_native(raw)
    alternate = [x if i in actual_rows else x ^ 1 for i, x in enumerate(raw)]
    assert layout.read_native(alternate) == ground
    a = raw.copy()
    b = raw.copy()
    stats = set()
    num_checks = len(ground) * layout.all_lanes
    ground_steps = 0
    for slot in schedule:
        ground = native_letter(ground, layout, slot)
        a = physical_letter(a, layout, slot, 'mask', stats)
        b = physical_letter(b, layout, slot, 'diagonals', stats)
        alternate = physical_letter(alternate, layout, slot, 'mask', stats)
        assert a == b
        assert layout.read_native(a) == ground == layout.read_native(alternate)
        ground_steps += 1
    if direct_borrow is not None:
        collapsed = layout.read_native(raw)
        for slot in direct_borrow:
            collapsed = native_letter(collapsed, layout, slot)
        assert collapsed == ground

    # Both endpoints may be arbitrary, independently of a preceding forward pass.
    inverses = [inverse_letter(slot) for slot in schedule[::-1]]
    for slot in inverses:
        a = physical_letter(a, layout, slot, 'mask', stats)
        b = physical_letter(b, layout, slot, 'diagonals', stats)
    assert a == b == raw
    independent_output = [rng.getrandbits(2 * layout.strip) for _ in layout.full_points]
    inverse_reference = layout.read_native(independent_output)
    back = independent_output.copy()
    for slot in inverses:
        back = physical_letter(back, layout, slot, 'diagonals', stats)
        inverse_reference = native_letter(inverse_reference, layout, slot)
        assert layout.read_native(back) == inverse_reference
        ground_steps += 1
    for slot in schedule:
        back = physical_letter(back, layout, slot, 'mask', stats)
    assert back == independent_output

    mutation_counts = {}
    for mode in ('omit_copies', 'all_pairs'):
        bad = raw.copy()
        for slot in schedule:
            bad = physical_letter(bad, layout, slot, mode, set())
        mutation_counts[mode] = logical_mismatch(ground, layout.read_native(bad), layout.lanes)

    if direct_borrow is not None:
        bad = layout.read_native(raw)
        # Keep the concurrent other native groups, but omit the fourth scratch update on group zero.
        for k, (kind, data) in enumerate(schedule):
            use = (kind, [[], *data[1:]]) if k == 3 else (kind, data)
            bad = native_letter(bad, layout, use)
        mutation_counts['incomplete_borrow_restore'] = logical_mismatch(ground, bad, layout.lanes)
        assert mutation_counts['incomplete_borrow_restore'] > 0

    byte_width = (2 * layout.all_lanes + 7) // 8
    digest = hashlib.sha256(b''.join(x.to_bytes(byte_width, 'little') for x in ground)).hexdigest()
    return {'native_shape': layout.native, 'full_binary_shape': layout.full,
            'lane_copies_per_axis': layout.m, 'residual_lanes_per_row': layout.strip,
            'original_lanes': layout.lanes, 'padded_lanes': layout.all_lanes,
            'true_points': math.prod(layout.native), 'full_address_rows': len(layout.full_points),
            'nonzero_dummy_rows': len(raw) - len(actual_rows), 'synchronized_slots': len(schedule),
            'active_masks_seen': sorted(m for _, m in stats),
            'native_GF4_comparisons_across_steps_and_both_directions': ground_steps * num_checks,
            'mutation_wrong_bits_on_original_lanes': mutation_counts, 'logical_output_sha256': digest}


def gate_on_all_masks():
    # Every matrix column is tested over GF4 on all spectator masks and both bit planes.
    cases = 0
    for d in range(1, 5):
        simple = Layout((2,) * d, 1, 0)
        for mask in range(1 << d):
            for k in range(1 << d):
                for value in (1, 2):
                    basis = [0] * (1 << d)
                    basis[k] = value
                    assert unconditional_pair_gate(basis, mask, simple) == mask_pascal(basis, mask)
                    cases += 1
    return cases


def main():
    seed = 26071119
    rng = random.Random(seed)
    results = []
    for native, strip, missing, count_rows in (
        ((3,), 3, 1, [[1], [0], [1]]),
        ((3, 5), 4, 2, [[1, 2], [0, 1], [1, 0]]),
        ((3, 5, 7), 3, 1, [[1, 2, 3], [1, 0, 2], [0, 1, 0]]),
        ((4, 3, 5), 2, 1, [[2, 1, 1], [1, 0, 2], [0, 1, 0]]),
    ):
        layout = Layout(native, strip, missing)
        schedule = [new_monomial(native, rng)]
        for counts in count_rows:
            schedule.append(new_shear(native, counts, rng))
            schedule.append(new_monomial(native, rng))
        results.append(fixture(layout, schedule, rng))

    # Two fully occupied three-register fibres in native block zero. The second borrow uses
    # the first fibre's already transformed output. Block one's unrelated word stays active.
    layout = Layout((6, 5), 4, 3)
    dirty = [(3, 0), (1, 3), (3, 0), (1, 3), (1, 3), (4, 1), (1, 3), (4, 1)]
    slots, collapsed = [], [('shear', [[(1, 0), (4, 3)], []])]
    for index, operation in enumerate(dirty):
        other = new_shear((5,), [index % 3], rng)[1][0]
        slots.append(('shear', [[operation], other]))
        collapsed.append(('shear', [[], other]))
    results.append(fixture(layout, slots, rng, collapsed))

    totals = {key: sum(row['mutation_wrong_bits_on_original_lanes'].get(key, 0) for row in results)
              for key in ('omit_copies', 'all_pairs', 'incomplete_borrow_restore')}
    assert all(value > 0 for value in totals.values())
    payload = {'seed': seed, 'field': 'F2[w]/(w^2+w+1)',
               'all_mask_basis_columns': gate_on_all_masks(), 'cases': results,
               'total_native_GF4_comparisons': sum(row['native_GF4_comparisons_across_steps_and_both_directions']
                                                   for row in results),
               'mutation_wrong_bits': totals}
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
