"""Independent integer dynamic-programming check of the depth-27 relaxation.

No author code imported. This checks the finite reduced optimization; the
rank-map domination theorem and lattice realization need their written proofs.
Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
"""
from itertools import combinations_with_replacement
A, B, D = (51008161, 50979600, 50983170)
N = 27
candidate = 3 * A * B ** 26 + 12 * A ** 2 * B ** 25

def optimum(exponents, count):
    dp = [None] * (count + 1)
    dp[0] = 0
    for e in exponents:
        costs = [D ** e * B ** (N - e) * A ** x * B ** (count - x) for x in range(count + 1)]
        nxt = [None] * (count + 1)
        for used, old in enumerate(dp):
            if old is None:
                continue
            for x in range(count - used + 1):
                val = old + costs[x]
                if nxt[used + x] is None or val < nxt[used + x]:
                    nxt[used + x] = val
        dp = nxt
    value = dp[count]
    if not value % B ** count == 0:
        raise ValueError('independent DP obligation line 31')
    return value // B ** count

def main():
    if not A * B ** 7 < D ** 8:
        raise ValueError('independent DP obligation line 35')
    if not 15 ** 15 * A ** 23 * D ** 32 * B ** 350 > candidate ** 15:
        raise ValueError('independent DP obligation line 36')
    seen = 0
    minima = []
    for y in range(4):
        best = None
        for forms in combinations_with_replacement(range(1, 16), y):
            exponents = [sum(((p & v).bit_count() % 2 for p in forms)) for v in range(1, 16)]
            value = optimum(exponents, N - y)
            best = value if best is None else min(best, value)
            seen += 1
        minima.append(best)
    if not seen == 816:
        raise ValueError('independent DP obligation line 48')
    if not minima[0] == candidate:
        raise ValueError('independent DP obligation line 49')
    if not all((x > candidate for x in minima[1:])):
        raise ValueError('independent DP obligation line 50')
    lower = A ** 27 + 15 * B ** 27
    zero_optimum = A ** 27 + candidate
    upper = 16 * A ** 27
    if not 2 ** 695 < lower <= zero_optimum <= upper < 2 ** 696:
        raise ValueError('independent DP obligation line 54')
    print('PASS_ROOT_RECOVERY_DP cases=816 zero_optimum=', zero_optimum, 'packed_bits=696', sep='')
if __name__ == '__main__':
    main()
