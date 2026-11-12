#!/usr/bin/env python3
"""Independent exhaustive finite-field controls for the mixed-swap theorem."""
import argparse
from itertools import product
import json
from pathlib import Path


def rank(rows, p, width=2):
    rows = [[x % p for x in row] for row in rows]
    r = 0
    for j in range(width):
        pivot = next((i for i in range(r, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][j], -1, p)
        rows[r] = [(inv * x) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r:
                c = rows[i][j]
                rows[i] = [(x - c * y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def projective_rows(p):
    return [(1, a) for a in range(p)] + [(0, 1)]


def check_family(p, hidden):
    vectors = list(product(range(p), repeat=2))
    rowspaces = [()] + [(a,) for a in projective_rows(p)] + [((1, 0), (0, 1))]
    physical_inputs = list(product(range(p), repeat=hidden + 3))
    cases = ambiguous = base_cases = wrong_l_cases = 0
    witness = None
    for lam in vectors:
        for gamma_flat in product(range(p), repeat=2 * hidden):
            gamma = (gamma_flat[:hidden], gamma_flat[hidden:])
            annihilator = [a for a in vectors if all(sum(a[i] * gamma[i][j] for i in range(2)) % p == 0 for j in range(hidden))]
            for ell in range(p):
                for z in vectors:
                    base_cases += 1
                    b = [[lam[i] * z[j] - (ell if (i, j) == (1, 0) else 0) for j in range(2)] for i in range(2)]
                    c = [[sum(a[i] * b[i][j] for i in range(2)) % p for j in range(2)] for a in annihilator]
                    wrong_b = [[lam[i] * z[j] + (ell if (i, j) == (1, 0) else 0) for j in range(2)] for i in range(2)]
                    wrong_c = [[sum(a[i] * wrong_b[i][j] for i in range(2)) % p for j in range(2)] for a in annihilator]
                    actual_min = 2
                    coordinate_min = 2
                    for returns in rowspaces:
                        cases += 1
                        predicted = rank(c + list(returns), p) == 2
                        wrong_predicted = rank(wrong_c + list(returns), p) == 2
                        seen = {}
                        collision = None
                        for physical in physical_inputs:
                            u0, *tail = physical
                            nuisance, q = tail[:hidden], tail[hidden:]
                            h = [(lam[i] * u0 + sum(gamma[i][j] * nuisance[j] for j in range(hidden))) % p for i in range(2)]
                            delta = ((q[0] - h[0]) % p, (q[1] - h[1] - ell * (q[0] - h[0])) % p)
                            y = (u0 + sum(z[i] * delta[i] for i in range(2))) % p
                            r = tuple((q[i] - delta[i]) % p for i in range(2))
                            obs = (y,) + r + tuple(sum(a[i] * q[i] for i in range(2)) % p for a in returns)
                            target = (u0,) + tuple(q)
                            old = seen.get(obs)
                            if old is not None and old[0] != target:
                                collision = (old[1], physical, obs, old[0], target)
                                break
                            seen[obs] = (target, physical)
                        actual = collision is None
                        if actual != predicted:
                            raise ValueError((p, hidden, lam, gamma, ell, z, returns, collision))
                        if actual:
                            actual_min = min(actual_min, len(returns))
                            if all(a in ((1, 0), (0, 1)) for a in returns):
                                coordinate_min = min(coordinate_min, len(returns))
                        else:
                            ambiguous += 1
                        if wrong_predicted != actual:
                            wrong_l_cases += 1
                            if witness is None:
                                witness = dict(field=p, hidden=hidden, Lambda=lam, Gamma=gamma, L21=ell, Z=z, A=returns, actual_recovery=actual, wrong_plus_L=wrong_predicted, collision=collision)
                    minimum = 2 - rank(c, p)
                    if minimum != actual_min or minimum != coordinate_min:
                        raise ValueError(('sharp dimension or coordinate attainment', p, minimum, actual_min, coordinate_min))
    return dict(field=p, hidden_common_dimension=hidden, base_cases=base_cases, return_rowspaces=len(rowspaces), observation_cases=cases, explicit_ambiguity_cases=ambiguous, inputs_per_case=len(physical_inputs), wrong_plus_L_rejected=wrong_l_cases, first_wrong_sign_witness=witness)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    families = [check_family(2, 1), check_family(2, 2), check_family(3, 1)]
    if not any(x['wrong_plus_L_rejected'] for x in families):
        raise ValueError('directed chronological-sign control did not fail')
    receipt = dict(status='PASS_INDEPENDENT_EXHAUSTIVE_FINITE_FIELD_MIXED_SWAP', scope='All specified two-swap matrices and all return row spaces; exhaustive independent-input collisions. These finite controls supplement the universal proof.', families=families, total_observation_cases=sum(x['observation_cases'] for x in families))
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'cases': receipt['total_observation_cases']}))


if __name__ == '__main__':
    main()
