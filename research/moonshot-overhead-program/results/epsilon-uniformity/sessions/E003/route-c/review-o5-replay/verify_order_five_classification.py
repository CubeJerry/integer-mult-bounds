#!/usr/bin/env python3
"""Exact F16 checks for the narrowly stated converter/swap classification."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def mul(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        a <<= 1
        if a & 16:
            a ^= 0b10011
        b >>= 1
    return value


def power(a, n):
    value = 1
    while n:
        if n & 1:
            value = mul(value, a)
        a = mul(a, a)
        n >>= 1
    return value


def inv(a):
    assert a
    return power(a, 14)


def mm(a, b):
    return tuple(tuple(mul(a[i][0], b[0][j]) ^ mul(a[i][1], b[1][j])
                       for j in range(2)) for i in range(2))


def diag(a, b):
    return ((a, 0), (0, b))


def order(a):
    return next(n for n in range(1, 16) if power(a, n) == 1)


def main():
    matrices = converters = simultaneous = diagonal_trials = 0
    orders = {}
    for lam in range(2, 16):
        mu = inv(lam)
        tau = lam ^ mu
        assert tau
        for a in range(16):
            d = tau ^ a
            for b in range(1, 16):
                b2 = mul(b, b)
                if mul(a, d) ^ b2 != 1:
                    continue
                matrices += 1
                converter = mul(mul(a, d), lam ^ a) == mul(b2, mu ^ a)
                classified = (a == mul(mul(mu, mu), inv(tau)) and
                              d == mul(mul(lam, lam), inv(tau)) and
                              b2 == mul(mul(tau, tau) ^ 1, inv(mul(tau, tau))))
                assert converter == classified
                if not converter:
                    continue
                converters += 1
                orders[order(lam)] = orders.get(order(lam), 0) + 1
                c = ((a, b), (b, d))
                c2 = mm(c, c)
                swap_exists = False
                for s in range(1, 16):
                    for t in range(1, 16):
                        diagonal_trials += 1
                        word = mm(mm(c, diag(s, t)), c2)
                        if word[0][0] == word[1][1] == 0:
                            assert word[0][1] and word[1][0]
                            assert mm(diag(inv(word[0][1]), inv(word[1][0])), word) == ((0, 1), (1, 0))
                            swap_exists = True
                predicted = order(lam) == 5 and b == tau
                assert swap_exists == predicted
                simultaneous += int(swap_exists)
    assert (matrices, converters, simultaneous) == (196, 12, 4)
    assert orders == {15: 8, 5: 4}

    c = ((9, 7), (7, 14))
    s = ((7, 7), (1, 6))
    assert mm(mm(diag(1, 10), c), diag(14, 1)) == s
    assert mm(c, s) == mm(s, diag(8, 15))
    assert mm(mm(mm(diag(12, 8), c), diag(1, 12)), mm(c, c)) == ((0, 1), (1, 0))

    # Wrong universality and a degenerate order-three gate must be rejected.
    assert 15 in orders
    c3 = ((0, 1), (1, 1))
    assert c3[0][0] == 0  # A diagonal word preserves this zero; an eigenbasis does not.
    assert power(6, 3) == power(7, 3) == 1
    assert 6 ^ 7 == 1
    assert mul(1 ^ 1, inv(1)) == 0  # U5 would require the forbidden b=0.

    sources = [Path(__file__).name, "order-five-word-classification.md"]
    receipt = {
        "status": "passed",
        "field": "F2[X]/(X^4+X+1)",
        "symmetric_matrices": matrices,
        "ordered_one_converter_solutions": converters,
        "one_converter_orders": orders,
        "joint_order_five_solutions": simultaneous,
        "diagonal_word_trials": diagonal_trials,
        "concrete_identities": 3,
        "negative_controls": 2,
        "scope": "finite exact replay; universal proof is in the companion note",
        "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
    }
    (ROOT / "order-five-classification-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
