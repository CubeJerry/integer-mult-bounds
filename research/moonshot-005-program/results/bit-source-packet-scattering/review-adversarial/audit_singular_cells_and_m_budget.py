#!/usr/bin/env python3
"""Independent GF(2) local controls and directed fixed-even-m move budget."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def add(A, B):
    return [[a ^ b for a, b in zip(x, y)] for x, y in zip(A, B)]


def mul(A, B):
    return [[sum(x[k] * B[k][j] for k in range(len(B))) & 1
             for j in range(len(B[0]))] for x in A]


def rank(A):
    basis = {}
    for row in A:
        v = sum(int(a) << i for i, a in enumerate(row))
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return len(basis)


def all_mats(r, c):
    return [
        [[(mask >> (i * c + j)) & 1 for j in range(c)] for i in range(r)]
        for mask in range(1 << (r * c))
    ]


def vecs(n):
    return [[(mask >> i) & 1 for i in range(n)] for mask in range(1 << n)]


def pick_reflexive_inverse(D):
    for R in all_mats(2, 2):
        if mul(mul(D, R), D) == D and mul(mul(R, D), R) == R:
            return R
    raise AssertionError("finite-dimensional reflexive inverse absent")


def factor_projection(H):
    """Factor H=Jh by selecting image columns and their coefficients."""
    n = len(H)
    columns = [[H[i][j] for i in range(n)] for j in range(n)]
    chosen = []
    for c in columns:
        if rank([[v[k] for v in chosen + [c]] for k in range(n)]) > len(chosen):
            chosen.append(c)
    nu = len(chosen)
    J = [[chosen[j][i] for j in range(nu)] for i in range(n)]
    h = [[0 for _ in range(n)] for _ in range(nu)]
    for j, c in enumerate(columns):
        # Uniqueness of coefficients in the independent columns of J.
        choices = [z for z in itertools.product([0, 1], repeat=nu)
                   if [sum(J[i][k] * z[k] for k in range(nu)) & 1 for i in range(n)] == c]
        need(len(choices) == 1, ("projection image coordinates", H, c))
        for k, bit in enumerate(choices[0]):
            h[k][j] = bit
    return J, h


def check_local_algebra():
    I = [[1, 0], [0, 1]]
    count = {0: 0, 1: 0, 2: 0}
    compatible_cases = incompatible_controls = 0
    for D in all_mats(2, 2):
        R = pick_reflexive_inverse(D)
        nu = 2 - rank(D)
        count[nu] += 1
        RD = mul(R, D)
        DR = mul(D, R)
        H = add(I, RD)  # minus is plus over GF(2)
        J, h = factor_projection(H)
        zeros = [[0, 0], [0, 0]]
        need(mul(H, H) == H, ("H idempotent", D, R))
        need(mul(D, H) == zeros, ("D H=0", D, R))
        need(add(RD, H) == I, ("RD=I-Jh", D, R))
        need(mul(DR, DR) == DR, ("DR projection", D, R))
        if nu:
            need(mul(J, h) == H and mul(h, J) == [[1 if i == j else 0 for j in range(nu)] for i in range(nu)],
                 ("projection factorization", D, H, J, h))
            need(mul(D, J) == [[0] * nu for _ in range(2)], ("DJ=0", D, J))
            need(mul(h, R) == [[0, 0] for _ in range(nu)], ("hR=0", D, R, h))
        else:
            need(H == zeros, ("zero-kernel projection", D, H))

        # Exhaust every two-column packet input P. W=DP is compatible and
        # P=R W+J hP reconstructs it; this checks the actual kernel coordinate.
        for P in all_mats(2, 2):
            W = mul(D, P)
            compat = add(I, DR)
            need(mul(compat, W) == zeros, ("compatible W", D, W))
            kernel_part = mul(J, mul(h, P)) if nu else [[0, 0], [0, 0]]
            recovered = add(mul(R, W), kernel_part)
            need(recovered == P, ("kernel-complete reconstruction", D, P, R, J, h))
            compatible_cases += 1

        # Every singular D has a concrete incompatible codomain vector.
        if nu:
            image = {tuple(mul(D, [[v[0]], [v[1]]])[i][0] for i in range(2)) for v in vecs(2)}
            bad = next(v for v in vecs(2) if tuple(v) not in image)
            Wbad = [[bad[0]], [bad[1]]]
            compat_bad = add(I, DR)
            need(mul(compat_bad, Wbad) != [[0], [0]], ("incompatible-image rejection", D, R, bad))
            incompatible_controls += 1
    need(count == {0: 6, 1: 9, 2: 1}, ("nullity census", count))
    return {
        "matrices_checked": 16,
        "nullity_counts": {str(k): v for k, v in sorted(count.items())},
        "packet_input_matrices_reconstructed": compatible_cases,
        "singular_image_compatibility_negative_controls": incompatible_controls,
        "kernel_factorization_and_hR_controls": "PASS",
        "scope": "Finite GF(2), 2x2 controls only; general theorem follows from complement construction in the review note.",
    }


def directed_power(rank_value, bits=192):
    den = 1 << bits
    target = rank_value ** 199 * den ** 200
    lo, hi = 0, rank_value * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, ("200th root bracket", rank_value))
    up = lo if lo ** 200 == target else lo + 1
    return F(lo, den), F(up, den)


def profile_moment(profile, powers):
    lo = hi = F(0)
    for k, coeff in profile.items():
        a, b = powers[int(k)]
        if coeff >= 0:
            lo += coeff * a
            hi += coeff * b
        else:
            lo += coeff * b
            hi += coeff * a
    return lo, hi


def add_interval(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale_interval(c, a):
    return (c * a[0], c * a[1]) if c >= 0 else (c * a[1], c * a[0])


def sub_interval(a, b):
    return a[0] - b[1], a[1] - b[0]


def fmt(a):
    return {"lower": str(a[0]), "upper": str(a[1])}


def budget_check(path):
    raw = path.read_bytes()
    budget = json.loads(raw)
    powers = {k: directed_power(k) for k in range(1, 128)}
    n = {int(k): int(v) for k, v in budget["native_paid"].items()}
    h = {int(k): int(v) for k, v in budget["helper_target"].items()}
    p2 = {int(k): int(v) for k, v in budget["paired_paid"].items()}
    t2 = {int(k): int(v) for k, v in budget["paired_target"].items()}
    q = {int(k): int(v) for k, v in budget["Q_paid"].items()}
    nh = {k: n.get(k, 0) - h.get(k, 0) for k in set(n) | set(h)}
    d = {k: t2.get(k, 0) - p2.get(k, 0) for k in set(t2) | set(p2)}
    base = profile_moment(nh, powers)
    delta = profile_moment(d, powers)
    q_cost = profile_moment(q, powers)
    need(delta[1] < 0, ("paired margin is negative", delta))
    target = F(1618)
    e = scale_interval(F(36), sub_interval(base, (target, target)))
    dmag = (-delta[1], -delta[0])
    denom = sub_interval(e, dmag)
    need(e[0] > 0 and denom[0] > 0, ("finite threshold exists", e, dmag, denom))
    m_threshold = (e[0] / denom[1], e[1] / denom[0])
    by_m = {}
    for m in (2, 4, 6, 8, 10, 12, 16, 32):
        coefficient = F(m, 36 * (m - 1))
        allowance = add_interval(base, scale_interval(coefficient, delta))
        by_m[str(m)] = {
            "allowance_interval": fmt(allowance),
            "margin_over_1618": fmt((allowance[0] - target, allowance[1] - target)),
            "movement_profile_1618_fits": allowance[0] >= target,
        }
    allowance4 = tuple(F(x) for x in by_m["4"]["allowance_interval"].values())
    allowance6 = tuple(F(x) for x in by_m["6"]["allowance_interval"].values())
    need(allowance4[1] < target, ("m=4 fails exact movement comparison", allowance4))
    need(allowance6[0] > target, ("m=6 passes exact movement comparison", allowance6))
    # The coefficient m/(36(m-1)) strictly decreases in m; delta<0, so
    # allowance increases with m. This excludes m=2 and proves m=6 first.
    exact_bgt = budget["at_t_199_over_200"]
    fixed = exact_bgt["fixed_even_m_remaining_completion_room"]
    for m in (2, 4, 6, 8, 16, 32):
        room = fixed[str(m)]
        room_interval = (F(room["exact_lower"]), F(room["exact_upper"]))
        derived_room = sub_interval(add_interval(base, scale_interval(F(m, 36*(m-1)), delta)), q_cost)
        need(room_interval[0] <= derived_room[0] <= derived_room[1] <= room_interval[1],
             ("match pinned budget room", m, derived_room, room_interval))
    return {
        "budget_sha256": sha(raw),
        "t": "199/200",
        "moment_components": {
            "(N-H)_t": fmt(base),
            "(T2-P2)_t": fmt(delta),
            "Q_t": fmt(q_cost),
            "delta_strictly_negative": delta[1] < 0,
        },
        "movement_target": 1618,
        "criterion": "(N-H)_t + m/(36(m-1))*(T2-P2)_t >= 1618",
        "criterion_derivation": "The complete fixed-even-m caller's Q allowance is (N-H)_t + m/(36(m-1))*(T2-P2)_t. Compare this movement-only allowance directly with the all-unit MOVE moment 1618.",
        "equivalent_real_threshold": "m >= 36*((N-H)_t-1618)/(36*((N-H)_t-1618)-(-(T2-P2)_t))",
        "equivalent_real_threshold_interval": fmt(m_threshold),
        "even_m_directed_checks": by_m,
        "first_even_m_passing_this_movement_comparison": 6,
        "m4_deficit_lower": str(target - allowance4[1]),
        "m6_margin_lower": str(allowance6[0] - target),
        "fixed_Q_room_rederived_from_histograms": "PASS for m=2,4,6,8,16,32",
        "scope": "Movement-budget comparison only. Rank-one MOVE tariff is one, so the specified fully unit-split route family has moment 1618. This is neither a lower bound for other schedules (rank-q tariff q^(199/200) is sublinear) nor a full algorithm, sufficiency proof, or kappa result; all ADD/INIT/cache/compatibility/restoration/physical obligations remain.",
    }


def main(args):
    local = check_local_algebra()
    budget = budget_check(args.budget)
    out = {
        "status": "PASS_INDEPENDENT_LOCAL_SINGULAR_CELL_CONTROLS_AND_M6_MOVEMENT_THRESHOLD",
        "local_algebra_controls": local,
        "budget_review": budget,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": out["status"],
        "local_controls": local,
        "first_even_m": budget["first_even_m_passing_this_movement_comparison"],
        "m4_deficit_lower": budget["m4_deficit_lower"],
        "m6_margin_lower": budget["m6_margin_lower"],
    }, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--budget", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
