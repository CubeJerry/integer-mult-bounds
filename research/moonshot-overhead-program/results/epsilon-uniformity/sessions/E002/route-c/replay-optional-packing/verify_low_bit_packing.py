#!/usr/bin/env python3
"""Exact position-level verification of LP; not a tape-time simulator."""
from itertools import product
from math import prod
from pathlib import Path
import json


def transpose(values, shape, axes):
    assert sorted(axes) == list(range(len(shape)))
    assert len(values) == prod(shape)
    strides = [prod(shape[i+1:]) for i in range(len(shape))]
    output_shape = [shape[i] for i in axes]
    result = []
    for out_index in product(*(range(n) for n in output_shape)):
        offset = sum(out_index[j] * strides[axes[j]] for j in range(len(shape)))
        result.append(values[offset])
    return result


def packed_swap(values, P, U, G, B, t, omit_low=False, reverse_basis=False):
    d, H = 1 << t, 1 << (U-t)
    packed = transpose(values, [P,H,d,G,H,d,B], [0,1,2,3,4,6,5])
    letters = [tuple(packed[i:i+d]) for i in range(0,len(packed),d)]
    high = transpose(letters, [P,H,d,G,H,B], [0,4,2,3,1,5])
    expanded = [bit for letter in high for bit in (letter[::-1] if reverse_basis else letter)]
    unpacked = transpose(expanded, [P,H,d,G,H,B,d], [0,1,2,3,4,6,5])
    if omit_low:
        return unpacked
    return transpose(unpacked, [P,H,d,G,H,d,B], [0,1,5,3,4,2,6])


def main():
    counts = dict(shapes=0, positions=0, nontrivial_packings=0,
                  omitted_low_swap_rejected=0, reversed_basis_rejected=0)
    for U in range(1,6):
        for t in range(U+1):
            for P,G,B in product(range(1,3),range(1,4),range(1,4)):
                shape = [P,1<<U,G,1<<U,B]
                values = list(range(prod(shape)))
                expected = transpose(values, shape, [0,3,2,1,4])
                actual = packed_swap(values,P,U,G,B,t)
                assert actual == expected, (P,U,G,B,t)
                counts['shapes'] += 1
                counts['positions'] += len(values)
                if t:
                    counts['nontrivial_packings'] += 1
                    assert packed_swap(values,P,U,G,B,t,omit_low=True) != expected
                    counts['omitted_low_swap_rejected'] += 1
                    assert packed_swap(values,P,U,G,B,t,reverse_basis=True) != expected
                    counts['reversed_basis_rejected'] += 1
    receipt = {'status':'PASS','scope':'exact finite position layouts, not asymptotic tape simulation',
               'counts':counts}
    Path(__file__).with_name('low-bit-packing-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__ == '__main__':
    main()
