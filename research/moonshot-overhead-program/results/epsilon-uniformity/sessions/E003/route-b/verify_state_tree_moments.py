#!/usr/bin/env python3
"""Exact finite checks for the ordered-partition state-tree profile."""
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial, isqrt
from pathlib import Path
import json
import platform
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def ordered_partitions(limit):
    row = [1]
    counts = [1]
    for n in range(1, limit + 1):
        new = [0] * (n + 1)
        for r in range(1, n + 1):
            new[r] = (row[r - 1] if r - 1 < len(row) else 0)
            if r < len(row):
                new[r] += r * row[r]
        row = new
        counts.append(sum(factorial(r) * row[r] for r in range(1, n + 1)))
    return counts


def component(L, h):
    return (h + 1) ** L - (h ** L if L % 2 == 0 else 0)


def state_count(L, t):
    return ((t + 1) ** L - (1 - t) ** L) // 2


def tree_weight(L, t):
    return state_count(L, t) - component(L, t - 1) + sum(
        (1 << (t - 1 - h)) * (component(L, h + 1) - component(L, h))
        for h in range(t - 1)
    )


def parameters(x):
    a = (x - 1).bit_length()
    b = a.bit_length() - 1
    S = a - b + 5
    L = 2 * isqrt(x // S)
    t = (2 * x + L - 1) // L + 6
    return a, b, S, L, t


def main():
    xs = sorted(set(range(64, 1025, 5)) | {1 << k for k in range(6, 15)})
    max_L = max(parameters(x)[3] for x in xs)
    counts = ordered_partitions(max(18, max_L))
    assert counts[:7] == [1, 1, 3, 13, 75, 541, 4683]
    coefficient_checks = moment_checks = two_sided = profile_checks = 0
    controls = set()
    for L in range(2, 19):
        F = counts[L]
        assert factorial(L) <= F <= L ** L
        kappa = (2 * F - 1) if L % 2 else (F - 1)
        # Eulerian numbers independently evaluate sum k^L/2^k.
        euler = [1]
        for n in range(2, L + 1):
            nxt = [0] * n
            for j in range(n):
                if j < len(euler):
                    nxt[j] += (j + 1) * euler[j]
                if j:
                    nxt[j] += (n - j) * euler[j - 1]
            euler = nxt
        A = sum(v * (1 << (L - j)) for j, v in enumerate(euler))
        assert A == 2 * F
        coefficient_checks += 1
        for t in range(2, 8 * L + 9):
            q = 1 << t
            lam = state_count(L, t)
            M = tree_weight(L, t)
            telescoped = lam + Fraction(q, 2) * (
                sum(Fraction(component(L, j), 1 << j) for j in range(1, t)) - 1
            )
            assert telescoped == M
            assert 0 <= q * kappa - M
            assert M >= lam - 1
            if t >= 8 * L:
                assert 2 * M >= q * kappa
                two_sided += 1
            if L % 2 == 0:
                D = 2 + L * (q - 2)
                assert 2 * D + 8 * M <= 10 * q * F
            if L % 2 and M > q * (F - 1):
                controls.add('odd coefficient rejects the even-parity formula')
            if M > kappa:
                controls.add('omitting the factor q is rejected')
            moment_checks += 1
    for x in xs:
        a, b, S, L, t = parameters(x)
        q = 1 << t
        N = 1 << (L * t)
        D = 2 + L * (q - 2)
        m_upper = 1 << x
        m_lower = (1 << (x - 1)) + 1
        s = L // 2
        r_charged = sum(comb(L, j) * q ** j for j in range(s + 1))
        top = Fraction(m_upper * comb(L, s), q ** s)
        assert L >= 2 and L % 2 == 0 and t >= 2
        assert m_upper * r_charged * 8 <= N
        assert top <= Fraction(1, 1 << (2 * L))
        assert L * t <= 4 * x
        assert N <= m_lower ** 5
        assert L * L * S <= 4 * x
        # log2 L <= S/2, checked without logarithms.
        assert L * L <= 1 << S
        M = tree_weight(L, t)
        free = 2 * D + 8 * M
        J = Fraction(1 + D + free) + D * top
        assert J <= 13 * q * counts[L]
        assert counts[L] <= L ** L
        root_up = isqrt(x * S)
        root_up += root_up * root_up < x * S
        assert t <= root_up + 2 * S + 7
        assert J <= 1 << (2 * root_up + 2 * S + 11)
        bad_t = max(1, (2 * x) // L - 2)
        bad_q = 1 << bad_t
        bad_N = bad_q ** L
        bad_rank = sum(comb(L, j) * bad_q ** j for j in range(s + 1))
        if m_upper * bad_rank * 8 > bad_N:
            controls.add('omitting the positive t reserve breaks the rank guard')
        profile_checks += 1
    assert len(controls) == 3
    result = {
        'status': 'pass',
        'scope': 'Exact finite state-tree moments, integer label profiles and positive invoices; no tape multiplier or numerical infinite sum.',
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'proof_sha256': sha256((ROOT / 'STATE-TREE-MOMENT-PROFILE.md').read_bytes()).hexdigest(),
        'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'coefficient_checks': coefficient_checks,
        'exact_tree_moment_checks': moment_checks,
        'two_sided_range_checks': two_sided,
        'integer_profile_checks': profile_checks,
        'maximum_x': max(xs),
        'maximum_L': max_L,
        'negative_controls': sorted(controls),
    }
    (ROOT / 'state-tree-moment-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
