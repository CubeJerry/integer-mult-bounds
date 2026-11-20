"""Exact vector arithmetic modulo 65521, one coefficient in each 64-bit lane."""
from functools import cache

PRIME = 65521
RADIX = 1 << 64
LOW = (1 << 16) - 1


@cache
def inverse(x):
    return pow(x, -1, PRIME)


def first(vector):
    return ((vector & -vector).bit_length() - 1) // 64


def coefficient(vector, j):
    return (vector >> (64*j)) & LOW


def unit(j):
    return 1 << (64*j)


def coordinates(vector):
    while vector:
        j = first(vector)
        c = coefficient(vector, j)
        yield j, c
        vector -= c * unit(j)


class Field:
    def __init__(self, size):
        self.size = size
        self.ones = ((1 << (64*size)) - 1) // (RADIX - 1)
        self.low = self.ones * LOW
        self.high = self.ones * ((1 << 48) - 1)

    def reduce(self, value, folds=2):
        # For a product plus one field word, every lane starts below 2^32.
        # A sum of at most 2048 products starts below 2^43 and uses three folds.
        # 2^16 = 15 in this field. After folding, each lane lies in [0,2p).
        for _ in range(folds):
            value = (value & self.low) + 15 * ((value >> 16) & self.high)
        carry = ((value + 15*self.ones) >> 16) & self.ones
        return value - PRIME*carry

    def eliminate(self, row, pivot, scalar):
        return self.reduce(row + (PRIME-scalar)*pivot)

    def basis(self, rows):
        pivots = {}
        for row in rows:
            row = self.remainder(row, pivots)
            if row:
                j = first(row)
                pivots[j] = self.reduce(inverse(coefficient(row,j))*row)
        return pivots

    def remainder(self, row, pivots):
        # This partial reduction suffices when constructing an echelon basis.
        while row:
            j = first(row)
            if j not in pivots:
                break
            row = self.eliminate(row, pivots[j], coefficient(row,j))
        return row

    def quotient(self, row, pivots):
        # Eliminate every pivot coordinate, including pivots after a free column.
        for j in sorted(pivots):
            c = coefficient(row,j)
            if c:
                row = self.eliminate(row, pivots[j], c)
        return row
