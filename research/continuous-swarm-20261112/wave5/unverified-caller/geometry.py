"""Exact finite address geometry; these functions do not process payloads."""
from collections import Counter


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return (x & y).bit_count() & 1


def mv(rows, x):
    return sum(dot(row, x) << i for i, row in enumerate(rows))


def transpose(rows):
    n = len(rows)
    return tuple(sum(((rows[j] >> i) & 1) << j for j in range(n))
                 for i in range(n))


def inverse(rows):
    n = len(rows)
    a = [row | (1 << (n+i)) for i, row in enumerate(rows)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if (a[i] >> j) & 1), None)
        need(pivot is not None, 'invertible binary matrix')
        a[j], a[pivot] = a[pivot], a[j]
        for i in range(n):
            if i != j and (a[i] >> j) & 1:
                a[i] ^= a[j]
    need([x & ((1 << n)-1) for x in a] == [1 << i for i in range(n)],
         'inverse elimination completed')
    return tuple(x >> n for x in a)


def phase_polynomial(terms):
    """Coefficients of sum c*parity(v.x) modulo four, including all pairs."""
    p = Counter()
    for v, c in terms:
        axes = [i for i in range(v.bit_length()) if (v >> i) & 1]
        for k, i in enumerate(axes):
            p[(i,)] += c
            for j in axes[k+1:]:
                p[(i, j)] -= 2*c
    return {key: c % 4 for key, c in p.items() if c % 4}


def translation_of(terms):
    p = phase_polynomial(terms)
    need(all(len(key) == 1 and c == 2 for key, c in p.items()),
         'complete residual is an ordinary translation')
    return sum(1 << key[0] for key in p)


def central_basis(q, basis):
    cols = (q,) + tuple(basis)
    need(len(cols) == 9 and all(0 < x < 512 for x in cols),
         'nine nonzero central directions')
    need(all(dot(x, y) == (i == j) for i, x in enumerate(cols)
             for j, y in enumerate(cols)), 'orthonormal central basis')
    rows = transpose(cols)
    need(inverse(rows) == transpose(rows), 'orthogonal inverse')
    return rows


def stage_route(q, basis):
    """17-axis involution: central coordinates first, the fresh block last.

    The returned shift corrects R*(C_all C_q^-1)*R to the positive fresh
    eight-axis job. All other ambient coordinates are fixed.
    """
    central_basis(q, basis)

    def action(v):
        result = q if dot(v & 511, q) else 0
        for i, b in enumerate(basis):
            if dot(v & 511, b):
                result ^= 1 << (9+i)
            if (v >> (9+i)) & 1:
                result ^= b
        return result

    cols = tuple(action(1 << i) for i in range(17))
    rows = transpose(cols)
    need(all(action(x) == 1 << i for i, x in enumerate(cols)), 'route involution')
    need(action(q) == q, 'route preserves q')
    # R D_native R = product C_(R e_i) C_q^-1.
    # Difference from D_stage is a translation, its own inverse.
    residual = [(cols[i], 1) for i in range(9)] + [(q, -1)]
    residual += [(1 << (9+i), -1) for i in range(8)]
    shift = translation_of(residual)
    need(not phase_polynomial(residual + [(shift, 2)]), 'corrected stage endpoint')
    return rows, shift


def axis_order(selected, ambient=153):
    """Column j of the permutation sends input axis j to order[j]."""
    selected = tuple(selected)
    need(len(set(selected)) == len(selected)
         and all(0 <= x < ambient for x in selected), 'distinct selected axes')
    return selected + tuple(i for i in range(ambient) if i not in set(selected))


def stage_axes(stages):
    stages = tuple(stages)
    need(stages and len(set(stages)) == len(stages)
         and all(1 <= s <= 18 for s in stages), 'distinct nonempty native stages')
    return tuple(i for s in stages for i in range(9+8*(s-1), 17+8*(s-1)))
