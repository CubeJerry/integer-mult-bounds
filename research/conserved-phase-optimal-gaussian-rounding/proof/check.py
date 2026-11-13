#!/usr/bin/env python3
"""Exact integer challenge of the proposed complex-pair rounding map."""

from __future__ import annotations

import itertools
import json


H = ((1, 1), (1, -1))
J = ((0, -1), (1, 0))
Q = ((0, 1), (-1, 0))  # -J
CONJ = ((1, 0), (0, -1))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matvec(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(2))
                 for i in range(2))


def parity(value):
    return value & 1


def norm2(vector):
    return sum(value * value for value in vector)


def score2(value, kind):
    magnitude = abs(value)
    require(magnitude % 2 == 1, "mixed branch needs doubled half-integers")
    if kind == 0:
        return 4 * ((magnitude - 1) // 4) + 1
    if magnitude == 1:
        return 0
    return 4 * ((magnitude - 3) // 4) + 3


def pair_toggle(value, kind):
    magnitude = abs(value)
    score = score2(value, kind)
    if kind == 1 and magnitude == 1:
        return -value
    high = score + 2
    require(magnitude in (score, high), "coordinate misses its pair")
    sign = 1 if value > 0 else -1
    return sign * (high if magnitude == score else score)


def m2(twice_t, p):
    types = (0, 1) if p == 0 else (1, 0)
    scores = [score2(twice_t[i], types[i]) for i in range(2)]
    index = min(range(2), key=lambda i: (scores[i], i))
    result = list(twice_t)
    result[index] = pair_toggle(result[index], types[index])
    return tuple(result)


def difference_map(s, d, phase_mutant=False):
    same_parity = parity(s[0]) == parity(s[1])
    if same_parity:
        return matvec(J, d)
    p = parity(s[0])
    jd = matvec(J, d)
    twice_t = matvec(H, jd)
    require(all(value % 2 == 1 for value in twice_t),
            "mixed parity must produce a half-integer T J d")
    if phase_mutant and p == 1:
        use_p = 0
    else:
        use_p = p
    twice_m = m2(twice_t, use_p)
    h_m = matvec(H, twice_m)
    require(all(value % 2 == 0 for value in h_m),
            "H times doubled half-grid vector must be even")
    return tuple(value // 2 for value in h_m)


def map_pair(pair, phase_mutant=False):
    u, v = pair
    s = (u[0] + v[0], u[1] + v[1])
    d = (u[0] - v[0], u[1] - v[1])
    dp = difference_map(s, d, phase_mutant)
    numer_u = (s[0] + dp[0], s[1] + dp[1])
    numer_v = (s[0] - dp[0], s[1] - dp[1])
    require(all(value % 2 == 0 for value in numer_u + numer_v),
            "exact sum and parity must give Gaussian integer outputs")
    return (
        (numer_u[0] // 2, numer_u[1] // 2),
        (numer_v[0] // 2, numer_v[1] // 2),
    )


def inverse_pair(pair):
    u, v = pair
    s = (u[0] + v[0], u[1] + v[1])
    dp = (u[0] - v[0], u[1] - v[1])
    if parity(s[0]) == parity(s[1]):
        d = matvec(tuple(tuple(-value for value in row) for row in J), dp)
    else:
        p = parity(s[0])
        twice_t = matvec(H, dp)
        require(all(value % 2 == 1 for value in twice_t),
                "inverse mixed branch must recover half-grid t")
        twice_m = m2(twice_t, p)
        h_m = matvec(H, twice_m)
        require(all(value % 2 == 0 for value in h_m),
                "inverse must produce integer Jd")
        jd = tuple(value // 2 for value in h_m)
        d = matvec(tuple(tuple(-value for value in row) for row in J), jd)
    numer_u = (s[0] + d[0], s[1] + d[1])
    numer_v = (s[0] - d[0], s[1] - d[1])
    require(all(value % 2 == 0 for value in numer_u + numer_v),
            "inverse reconstruction must be Gaussian integral")
    return (
        (numer_u[0] // 2, numer_u[1] // 2),
        (numer_v[0] // 2, numer_v[1] // 2),
    )


def phase_i(pair):
    return matvec(J, pair[0]), matvec(J, pair[1])


def conjugate(pair):
    return matvec(CONJ, pair[0]), matvec(CONJ, pair[1])


def swap(pair):
    return pair[1], pair[0]


def exact_half_sqrt2_slack(m, n):
    d = 2 * m + 2 * n - 1
    return d <= 0 or d * d <= 16 * m * n


def pair_data(pair):
    u, v = pair
    return (u[0] * u[0] + u[1] * u[1]
            + v[0] * v[0] + v[1] * v[1])


def target_error_squared_num(pair, out):
    u, v = pair
    s = (u[0] + v[0], u[1] + v[1])
    d = (u[0] - v[0], u[1] - v[1])
    ideal_d = matvec(J, d)
    out_d = (out[0][0] - out[1][0], out[0][1] - out[1][1])
    # Combined pair error squared is |out_d - i*d|^2/2.
    return norm2((out_d[0] - ideal_d[0], out_d[1] - ideal_d[1]))


def check_pair(pair):
    out = map_pair(pair)
    require(inverse_pair(out) == pair, f"inverse failure: {pair} -> {out}")
    require(inverse_pair(pair) == conjugate(map_pair(conjugate(pair))),
            "conjugation-as-inverse identity fails")
    s0 = (pair[0][0] + pair[1][0], pair[0][1] + pair[1][1])
    s1 = (out[0][0] + out[1][0], out[0][1] + out[1][1])
    require(s0 == s1, "exact complex sum changed")
    err_num = target_error_squared_num(pair, out)
    require(err_num in (0, 2), "candidate error exceeds one")
    require(exact_half_sqrt2_slack(pair_data(pair), pair_data(out)),
            "bilateral pair radial slack exceeds 1/sqrt(2)")
    require(map_pair(phase_i(pair)) == phase_i(out),
            "global i-phase covariance fails")
    require(map_pair(swap(pair)) == swap(out),
            "wire-swap covariance fails")
    return out


def exhaustive():
    values = range(-2, 3)
    count = 0
    conjugation_inverse_failures = []
    conjugation_equivariance_example = None
    fourth_power_failures = []
    phase_mutant_failures = 0
    conjugate_covariance_failures = 0
    wire_swap_failures = 0
    for values4 in itertools.product(values, repeat=4):
        pair = ((values4[0], values4[1]), (values4[2], values4[3]))
        out = check_pair(pair)
        # Candidate property under review: inverse = conjugation F conjugation.
        cfc = conjugate(map_pair(conjugate(pair)))
        if inverse_pair(pair) != cfc:
            if len(conjugation_inverse_failures) < 3:
                conjugation_inverse_failures.append({
                    "input": pair,
                    "inverse": inverse_pair(pair),
                    "conjugate_F_conjugate": cfc,
                })
        if map_pair(pair, phase_mutant=True) != out:
            phase_mutant_failures += 1
        if map_pair(conjugate(pair)) != conjugate(out):
            conjugate_covariance_failures += 1
            if conjugation_equivariance_example is None:
                conjugation_equivariance_example = {
                    "input": pair,
                    "F_conjugate_input": map_pair(conjugate(pair)),
                    "conjugate_F_input": conjugate(out),
                }
        if map_pair(swap(pair)) != swap(out):
            wire_swap_failures += 1
        power = pair
        for _ in range(4):
            power = map_pair(power)
        if power != pair and not fourth_power_failures:
            fourth_power_failures.append({
                "input": pair,
                "fourth_power": power,
                "first_power": out,
            })
        count += 1
    return {
        "input_pairs_checked": count,
        "conjugation_as_inverse_failures": conjugation_inverse_failures,
        "conjugation_equivariance_failure_count": conjugate_covariance_failures,
        "conjugation_equivariance_example": conjugation_equivariance_example,
        "wire_swap_failure_count": wire_swap_failures,
        "wrong_phase_rule_differing_cases": phase_mutant_failures,
        "fourth_power_counterexample": fourth_power_failures[0]
        if fourth_power_failures else None,
    }


def large_cases():
    cases = []
    for exponent in (0, 1, 8, 64, 512):
        n = 1 << exponent
        for pair in (
            ((n, 1), (-n, 0)),
            ((n, 0), (0, n)),
            ((n + 1, n), (0, 1)),
            ((n, n + 1), (1, 0)),
        ):
            out = check_pair(pair)
            cases.append({
                "exponent": exponent,
                "input": [[str(x) for x in z] for z in pair],
                "output": [[str(x) for x in z] for z in out],
                "inverse_ok": inverse_pair(out) == pair,
            })
    return cases


def lower_bound_witnesses():
    witnesses = []
    for a in (1, 2, 8, 64, 512):
        s = (1, 0)
        d = (2 * a + 1, 0)
        pair = (
            ((s[0] + d[0]) // 2, (s[1] + d[1]) // 2),
            ((s[0] - d[0]) // 2, (s[1] - d[1]) // 2),
        )
        for first in (-1, 1):
            for second in (2 * a, 2 * a + 2):
                dprime = (first, second)
                out = (
                    ((s[0] + dprime[0]) // 2, (s[1] + dprime[1]) // 2),
                    ((s[0] - dprime[0]) // 2, (s[1] - dprime[1]) // 2),
                )
                error_num = target_error_squared_num(pair, out)
                if error_num <= 2:
                    input_norm = pair_data(pair)
                    output_norm = pair_data(out)
                    if output_norm < input_norm:
                        gap = f"sqrt({input_norm})-sqrt({output_norm})"
                    else:
                        gap = f"sqrt({output_norm})-sqrt({input_norm})"
                    witnesses.append({
                        "a": a,
                        "input_difference": list(d),
                        "output_difference": list(dprime),
                        "squared_pair_error": error_num // 2,
                        "input_pair_norm_squared": input_norm,
                        "output_pair_norm_squared": output_norm,
                        "exact_radial_gap": gap,
                    })
    return witnesses


def phase_pair_noncommutation():
    for t in itertools.product(range(-9, 10, 2), repeat=2):
        m0_then_m1 = m2(m2(t, 0), 1)
        m1_then_m0 = m2(m2(t, 1), 0)
        if m0_then_m1 != m1_then_m0:
            return {
                "doubled_half_input": list(t),
                "M1_after_M0": list(m0_then_m1),
                "M0_after_M1": list(m1_then_m0),
            }
    return None


def main():
    sample = exhaustive()
    cases = large_cases()
    lower = lower_bound_witnesses()
    noncommutation = phase_pair_noncommutation()
    require(sample["conjugation_as_inverse_failures"] == [],
            "conjugation-as-inverse failed in exhaustive domain")
    require(sample["conjugation_equivariance_failure_count"] > 0,
            "expected non-equivariance control did not distinguish covariance")
    require(sample["wire_swap_failure_count"] == 0,
            "wire swap should commute with candidate")
    require(sample["wrong_phase_rule_differing_cases"] > 0,
            "wrong-phase mutant was not detected")
    require(sample["fourth_power_counterexample"] is not None,
            "expected F^4 nonidentity control was not found")
    require(noncommutation is not None,
            "expected M0/M1 noncommutation example was not found")
    print(json.dumps({
        "status": "PASS",
        "operator": "C_+(u,v)=((s+i*d)/2,(s-i*d)/2)",
        "exhaustive_small_domain": sample,
        "large_cases": cases,
        "fixed_sum_error_one_lower_bound_examples": lower,
        "M0_M1_noncommutation_example": noncommutation,
        "exact_slack_filter": "D=2m+2n-1; accept iff D<=0 or D^2<=16mn",
        "scope": "exact sum, global i covariance, inverse, conjugation, wire swap, and asymptotic lower-bound challenge",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
