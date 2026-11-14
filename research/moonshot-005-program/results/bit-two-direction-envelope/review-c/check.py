#!/usr/bin/env python3
"""Independent controls for the arbitrary two-direction envelope theorem."""
import argparse, gzip, hashlib, itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PROOF = '346ed8024ce966b7962a00cf2cb8f43bb91b7fafc2d35837bd0873d83acda8fd'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def basis(rows):
    pivots = {}
    for x in rows:
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return list(pivots.values())


def span(rows):
    values = [0]
    for x in rows:
        values += [y ^ x for y in list(values)]
    return sorted(set(values))


def lift(word, channel, width=2, n=3):
    return sum(((word >> j) & 1) << (width*j+channel) for j in range(n))


def multiply4(a, b):
    # Polynomial multiplication modulo x^2+x+1, independently implemented.
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def fitting_directions(i, zero_mask, order):
    directions = [(1, a, 0) for a in range(order)] + [(0, 1, 0)]
    good = []
    for t, h in enumerate(directions):
        for a, b in itertools.product(range(order), repeat=2):
            row = [a ^ multiply4(b, x) for x in h]
            if row[i] == 1 and all(not (zero_mask >> j & 1) or row[j] == 0 for j in range(3)):
                good.append(t)
                break
    return sum(1 << t for t in good)


def zeros(rows):
    return sum(int(all(((x >> (2*j)) & 3) == 0 for x in rows)) << j for j in range(3))


def small_control():
    I = ((1, 0), (0, 1))
    O = ((0, 0), (0, 0))
    blocks = [[I, O, ((1, 0), (1, 1))],
              [((0, 0), (1, 0)), I, O],
              [O, ((1, 1), (0, 1)), I]]
    A = [sum(blocks[i][j][r][t] << (2*j+t) for j in range(3) for t in range(2))
         for i in range(3) for r in range(2)]
    CV = [lift(7, t) for t in range(2)]
    W = basis(A+CV)
    require(len(basis(A)) == 5 and len(W) == 5, 'literal rank five')
    words = span(W)
    full_lines = []
    for h in (1, 2, 3):
        if all(lift(h, t) in words for t in range(2)):
            full_lines.append(h)
    require(not full_lines, 'no full scalar tensor line over F2')
    # The full-line condition is a kernel of a binary linear map; its zero
    # dimension persists after arbitrary scalar extension, as reviewed.
    z = [zeros(A[2*i:2*i+2]) for i in range(3)]
    require(z == [2, 4, 1], 'literal directed zero pattern')
    m2 = [fitting_directions(i, z[i], 2) for i in range(3)]
    m4 = [fitting_directions(i, z[i], 4) for i in range(3)]
    require(m2[0] & m2[1] & m2[2] == 0, 'base F2 domination really fails')
    common4 = m4[0] & m4[1] & m4[2]
    require(common4 != 0, 'F4 domination succeeds')

    # Every identity-normalized row in the fixed total code is enumerated.
    row_options = []
    for i in range(3):
        one = [x for x in words if (x >> (2*i)) & 3 == 1]
        two = [x for x in words if (x >> (2*i)) & 3 == 2]
        require(len(one) == len(two) == 8, 'eight affine rows per own value')
        row_options.append([(fitting_directions(i, zeros((a, b)), 2),
                             fitting_directions(i, zeros((a, b)), 4))
                            for a in one for b in two])
    count = 0
    failures2 = 0
    minimum4 = 5
    for selected in itertools.product(*row_options):
        count += 1
        allowed2 = selected[0][0] & selected[1][0] & selected[2][0]
        allowed4 = selected[0][1] & selected[1][1] & selected[2][1]
        failures2 += not bool(allowed2)
        require(allowed4 != 0, 'all fixed-code fittings dominated over F4')
        minimum4 = min(minimum4, allowed4.bit_count())
    require(count == 64**3 and failures2 > 0, 'complete nontrivial finite domain')

    # At the strict d=2V boundary, diagonal identity cannot fit in scalar
    # dimension two. The finite F4 enumeration corroborates that rank proof.
    diag = [1 << j for j in range(6)]
    require(len(basis(diag+CV))-2 == 4, 'boundary quotient equals 2V')
    diag_masks = [7 ^ (1 << i) for i in range(3)]
    allowed = [fitting_directions(i, diag_masks[i], 4) for i in range(3)]
    require(allowed[0] & allowed[1] & allowed[2] == 0, 'strict-boundary counterexample')
    return {'ordinary_rank': 5, 'total_code_rank': 5, 'canonical_quotient': 3,
            'full_scalar_lines_over_F2': full_lines, 'literal_zero_masks': z,
            'literal_F2_common_directions': 0,
            'literal_F4_common_direction_indices': [t for t in range(5) if common4 >> t & 1],
            'normalized_choices_per_receiver': 64, 'complete_fittings_checked': count,
            'F2_domination_failures': failures2, 'F4_domination_failures': 0,
            'minimum_F4_dominating_directions': minimum4,
            'strict_dimension_boundary_rejected': True}


def native_control(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == NATIVE, 'native bytes')
    n = json.loads(gzip.decompress(raw))
    roots = [list(map(Fraction, n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
    K = [sum(int(i == j or sum(a*b for a, b in zip(x, y)) == 0) << j
             for j, y in enumerate(roots)) for i, x in enumerate(roots)]
    C = basis(K)
    require(len(C) == 9, 'native canonical rank')
    mask = (1 << 111)-1
    restrictions = [len(basis([c & (mask ^ k) for c in C])) for k in K]
    require(set(restrictions) == {8}, 'all native rigidity restrictions')
    S1, S2 = [2, 9, 12, 30, 38, 42], [2, 26, 63, 65, 81, 87]
    h1, h2 = [sum(1 << j for j in S) for S in (S1, S2)]
    I1 = {i for i, row in enumerate(K) if h1 & ~row == 0 and not (h1 >> i & 1) and row.bit_count()-1 <= 58}
    I2 = {i for i, row in enumerate(K) if h2 & ~row == 0 and not (h2 >> i & 1) and row.bit_count()-1 <= 58}
    require(len(I1) == len(I2) == 17 and len(I1 & I2) == 5, 'native patch beneficiary geometry')
    F = [k ^ (h1 if i in I1 else h2 if i in I2 else 0) for i, k in enumerate(K)]
    require(all(f >> i & 1 and f & ~K[i] == 0 for i, f in enumerate(F)), 'native fitted support')
    ell = sum(int(f.bit_count()-1 > 36)+int(f.bit_count()-1 > 52) for f in F)
    require(ell == 193 and len(basis(F+C))-9 == 2, 'native strict-boundary scalar control')
    tensors = []
    for V in (1, 2, 3, 5):
        av = [lift(f, t, V, 111) for f in F for t in range(V)]
        cv = [lift(c, t, V, 111) for c in C for t in range(V)]
        quotient = len(basis(av+cv))-9*V
        require(quotient == 2*V, 'native exact tensor boundary')
        tensors.append({'width': V, 'quotient': quotient, 'ell': ell})
    return {'canonical_rank': 9, 'rigidity_receivers': len(restrictions),
            'forbidden_rank_census': dict(Counter(restrictions)),
            'strict_boundary_controls': tensors}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--proof', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    proof_hash = hashlib.sha256(a.proof.read_bytes()).hexdigest()
    require(proof_hash == PROOF, 'reviewed proof bytes')
    out = {'status': 'PASS_INDEPENDENT_TWO_DIRECTION_ENVELOPE_CONTROLS',
           'proof_sha256': proof_hash, 'native_sha256': NATIVE,
           'author_checker_imported': False, 'small_field_boundary': small_control(),
           'native_rigidity_and_strict_boundary': native_control(a.native),
           'classification': 'independent mathematical review plus precisely finite controls; no physical source or new kappa',
           'new_kappa': None}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'fixed_code_fittings': out['small_field_boundary']['complete_fittings_checked'],
                      'F2_failures': out['small_field_boundary']['F2_domination_failures'], 'F4_failures': 0,
                      'native_boundary_ell': 193}))


if __name__ == '__main__':
    main()
