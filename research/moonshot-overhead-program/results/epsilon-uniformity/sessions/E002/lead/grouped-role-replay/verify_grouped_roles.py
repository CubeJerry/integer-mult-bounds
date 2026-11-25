#!/usr/bin/env python3
"""Exact finite role-layout checks; no tape runtime or asymptotic claim."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "f4_helpers", ROOT / "f4-replay/verify_spectral_repair.py")
f4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f4)


def move_one_bit(data, prefix, gap, tail):
    assert len(data) == prefix * 2 * gap * tail
    return [data[(((p * 2 + bit) * gap + g) * tail) + t]
            for p in range(prefix) for g in range(gap)
            for bit in range(2) for t in range(tail)]


def undo_one_bit(data, prefix, gap, tail):
    return [data[(((p * gap + g) * 2 + bit) * tail) + t]
            for p in range(prefix) for bit in range(2)
            for g in range(gap) for t in range(tail)]


def group_roles(data, prefix, roles, gap):
    padded = 1 << (roles - 1).bit_length()
    work = []
    for p in range(prefix):
        for role in range(padded):
            work.extend(data[(p * roles + role) * gap:
                             (p * roles + role + 1) * gap]
                        if role < roles else [None] * gap)
    before = work[:]
    remaining, moved = padded, 1
    history = []
    while remaining > 1:
        dims = prefix * (remaining // 2), gap, moved
        history.append(dims)
        work = move_one_bit(work, *dims)
        remaining //= 2
        moved *= 2
    out = [work[(p * gap + g) * padded + role]
           for p in range(prefix) for g in range(gap)
           for role in range(roles)]
    for dims in reversed(history):
        work = undo_one_bit(work, *dims)
    assert work == before
    return out, padded


def ungroup_roles(data, prefix, roles, gap):
    return [data[(p * gap + g) * roles + role]
            for p in range(prefix) for role in range(roles)
            for g in range(gap)]


def address_labels(m, q):
    for point in itertools.product(range(q), repeat=2*m):
        yield tuple(0 if point[j] == point[m+j]
                    else 1 if point[j] < point[m+j] else 2
                    for j in range(m))


def main():
    rng = random.Random(202611252220)
    omega = next(a for a in range(2, 16)
                 if f4.power(a, 2) ^ a ^ 1 == 0)
    small = [0, 1, omega, f4.power(omega, 2)]
    counts = dict(grouped_layouts=0, grouped_vector_repairs=0,
                  mask_budget_checks=0, exact_zero_symbols=0,
                  wrong_role_order_rejections=0)
    for m, q, modules, prefix in itertools.product(
            range(1, 4), range(2, 4), (1, 2, 4), (1, 2)):
        labels = list(address_labels(m, q))
        for roles in (2*m+1, 2*m+2, 4*m+1):
            if roles > 16:
                continue
            gap = modules * len(labels)
            data = [rng.randrange(16) for _ in range(prefix*roles*gap)]
            grouped, padded = group_roles(data, prefix, roles, gap)
            expected = [data[(p*roles+r)*gap+g]
                        for p in range(prefix) for g in range(gap)
                        for r in range(roles)]
            assert grouped == expected
            assert ungroup_roles(grouped, prefix, roles, gap) == data
            assert padded < 2*roles
            assert prefix*gap*(4*roles+2*m) <= 2*4*len(data)
            counts["mask_budget_checks"] += 1
            counts["exact_zero_symbols"] += data.count(0)
            counts["grouped_layouts"] += 1
            h = [[f4.power(node, i) for node in range(roles)]
                 for i in range(2)]
            output = []
            for p in range(prefix):
                for g in range(gap):
                    lab = labels[g % len(labels)]
                    z = f4.power(omega, sum(lab) % 3)
                    js = sorted({sum(lab) % roles,
                                 (sum(lab)+1) % roles})
                    predictor = [z]*roles
                    for j in js:
                        predictor[j] = small[(sum(lab)+j) % 4]
                    start = (p*gap+g)*roles
                    x = grouped[start:start+roles]
                    repaired = f4.repair(h, predictor, z, js, x)
                    target = [f4.mul(z, value) for value in x]
                    assert repaired == target
                    output.extend(repaired)
                    counts["grouped_vector_repairs"] += 1
            restored = ungroup_roles(output, prefix, roles, gap)
            target_rows = [f4.mul(
                f4.power(omega, sum(labels[g % len(labels)]) % 3),
                data[(p*roles+r)*gap+g])
                for p in range(prefix) for r in range(roles)
                for g in range(gap)]
            assert restored == target_rows
            wrong = []
            for start in range(0, len(output), roles):
                wrong.extend(reversed(output[start:start+roles]))
            if ungroup_roles(wrong, prefix, roles, gap) != target_rows:
                counts["wrong_role_order_rejections"] += 1
    assert counts["wrong_role_order_rejections"] > 0
    report = {
        "status": "PASS_EXACT_GROUPED_ROLE_LAYOUTS",
        "counts": counts,
        "field": "F16, modulus x^4+x+1; unchanged across role sizes",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": (
            "Exact short-coordinate regrouping, inverse, padding, one mask "
            "per grouped block, and small spectral repair after regrouping. "
            "Repair helper reused from lead checker; regrouping independently "
            "coded here. Toy check dimension two, not the asymptotic 1/16 "
            "invoice. No physical tape runtime, full interchanger, or "
            "asymptotic proof is tested."),
    }
    (ROOT/"grouped-role-verification.json").write_text(
        json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
