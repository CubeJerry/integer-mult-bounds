"""Independent all-width comparisons, finite Fourier order and actual one-group Walsh ports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
from runpy import run_path
import json
import mpmath as mp

HERE = Path(__file__).parent
DYADIC = run_path(str(HERE / "address-dyadic-caller.py"))
WALSH = run_path(str(HERE / "node-walsh-base.py"))
RNG = Random(121024247)


def bitreverse(x, width):
    bits = format(x, f"0{width}b")
    return int(bits[::-1], 2)


def fourier():
    total_coeffs = total_roots = 0
    worst = -100000
    for k in (2, 3, 4, 5, 6, 7, 8):
        n = 1 << k
        grid = DYADIC["DyadicGrid"](k)
        with mp.workprec(grid.bits + 160):
            q = mp.mpf(grid.one)
            omega = [mp.expj(2 * mp.pi * j / n) for j in range(n)]
            norm = mp.sqrt(n)
            for level, row in grid.twiddles.items():
                stride = n >> level
                for j, (re, im) in enumerate(row):
                    actual = mp.mpc(re, im) / q
                    error = abs(actual - omega[j * stride])
                    assert error < mp.mpf(2) ** (-90 * k)
                    total_roots += 1
            raw = [(RNG.randrange(-15, 16) * grid.one + RNG.randrange(-11, 12),
                    RNG.randrange(-15, 16) * grid.one + RNG.randrange(-11, 12)) for _ in range(n)]
            original = [mp.mpc(re, im) / q for re, im in raw]
            for inverse in (False, True):
                seen = grid.transform(raw, reverse=inverse)
                for i, (re, im) in enumerate(seen):
                    if inverse:
                        expected = sum(z * omega[-(i * bitreverse(a, k)) % n]
                                       for a, z in enumerate(original)) / norm
                    else:
                        expected = sum(z * omega[(a * bitreverse(i, k)) % n]
                                       for a, z in enumerate(original)) / norm
                    error = abs(mp.mpc(re, im) / q - expected)
                    assert error < mp.mpf(2) ** (-90 * k)
                    if error:
                        worst = max(worst, int(mp.ceil(mp.log(error, 2))))
                    total_coeffs += 1
    return dict(oracle_transform_entries=total_coeffs, oracle_twiddle_entries=total_roots,
                worst_tested_error_exponent=worst)


def walsh_direct():
    run = WALSH["Simulation"]
    machine = WALSH["compile_walsh"](2, False)
    little = WALSH["little"]
    steps = groups = 0
    for k in range(1, 7):
        n = 1 << k
        choices = sorted({0, 1, (1 << k) - 1, 0x15 & (n - 1), 0x2a & (n - 1)})
        for picked in choices:
            # At the controller the magnitude cap and modulus power are explicit. Smaller
            # fixtures use the same exact U=1 rule and raw two-point port on every selected bit.
            b = 5
            M = 1 + (1 << (k + b + picked.bit_count() + 2))
            K = M.bit_length() + 2
            signed = [RNG.randrange(-15, 16) for _ in range(n)]
            raw = "".join(little(x % M, K) for x in signed)
            for pos in range(k):
                if not picked & (1 << pos):
                    continue
                inp = {"A": raw, "M": little(M, K), "S": format(1 << pos, "b")}
                sim = run(machine, inp).execute((1 << 14) * len(raw))
                raw = sim.contents("A")
                steps += sim.steps
                assert all(sim.head[t] == 0 for t in sim.tapes)
                assert all(sim.contents(t) == inp.get(t, "") for t in sim.tapes if t != "A")
            for j in range(n):
                value = int(raw[j * K:(j + 1) * K][::-1], 2)
                lifted = value if 2 * value < M else value - M
                truth = sum((-1 if (j & x & picked).bit_count() % 2 else 1) * y
                            for x, y in enumerate(signed) if not (x ^ j) & ~picked)
                assert lifted == truth
            groups += 1
    return dict(one_group_masks=groups, one_group_raw_transitions=steps)


def scalar():
    # Monotone analytic inequalities in the written review reduce to these integer endpoints.
    for lower, upper, floor_phi, floor_log in ((5, 8, 3, 2), (8, 32, 5, 3), (32, 64, 8, 5)):
        assert lower * lower * floor_log >= floor_phi ** 3
        assert 170 + 5 * upper <= 71 * floor_phi
    assert 512 * 6 >= 2048 and 512 * 11 >= 4097
    assert 170 * 8 <= (71 - 40) * 64
    assert (1 << 26) < 26 * 140 ** 3
    assert 62 ** 3 > 28 * 8192 and F(4096 ** 2 * 8) >= 512 ** 3
    assert 182 + 140 + 1 <= F(3, 4) * 512
    assert 64 * 13 <= 4096
    # Shape switches require only integer leading bits; exact n from arithmetic is affordable here.
    shape_count = 0
    for j in (1, 2, 5, 16, 31, 32, 47, 48, 49, 62, 63, 255, 4096, 65537):
        for n in sorted({max(2, (1 << j) + delta) for delta in (-2, -1, 0, 1, 2)}):
            b = (n - 1).bit_length()
            h = (n + b - 1) // b
            k = (4 * h - 1).bit_length()
            if n > (1 << 48):
                assert k >= 32 and b < 2 * k and (1 << k) <= n and (1 << k) * k <= 16 * n
            assert (k.bit_length() >= 4097) == (k >= (1 << 4096))
            shape_count += 1
    return dict(actual_rounded_shape_tests=shape_count)


if __name__ == "__main__":
    print(json.dumps({**scalar(), **fourier(), **walsh_direct()}, sort_keys=True))
