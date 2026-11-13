#!/usr/bin/env python3
"""Independent signed-Pauli and exact-state check of 23 chart recipes.

This does not import the author's compiler or map checker. A tableau equality
plus equality on |0> fixes a Clifford operator including its global phase.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path


WORD_SHA = "20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f"
PARENT_SHA = "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc"


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def parity(x: int) -> int:
    return x.bit_count() & 1


def transpose(m: tuple[int, ...]) -> tuple[int, ...]:
    n = len(m)
    return tuple(sum(((row >> j) & 1) << i for i, row in enumerate(m)) for j in range(n))


def matmul_vec(m: tuple[int, ...], x: int) -> int:
    return sum(parity(row & x) << i for i, row in enumerate(m))


def inverse(m: tuple[int, ...]) -> tuple[int, ...]:
    n = len(m)
    a = [row | (1 << (n + i)) for i, row in enumerate(m)]
    for j in range(n):
        p = next((i for i in range(j, n) if (a[i] >> j) & 1), None)
        need(p is not None, "singular binary chart basis")
        a[j], a[p] = a[p], a[j]
        for i in range(n):
            if i != j and (a[i] >> j) & 1:
                a[i] ^= a[j]
    need([row & ((1 << n) - 1) for row in a] == [1 << i for i in range(n)], "bad binary inverse")
    return tuple(row >> n for row in a)


def extend(vectors: tuple[int, ...], n: int) -> tuple[int, ...]:
    cols: list[int] = []
    pivots: dict[int, int] = {}
    for value in vectors + tuple(1 << i for i in range(n)):
        reduced = value
        while reduced:
            j = reduced.bit_length() - 1
            if j not in pivots:
                pivots[j] = reduced
                cols.append(value)
                break
            reduced ^= pivots[j]
    need(len(cols) == n, "frame did not extend to basis")
    return tuple(cols)


def adjoint(circuit: tuple[tuple, ...]) -> tuple[tuple, ...]:
    out = []
    for g in reversed(circuit):
        if g[0] == "P":
            out.append(("P", inverse(g[1])))
        elif g[0] == "D":
            out.append(("D", g[1], tuple((-v) % 4 for v in g[2])))
        elif g[0] == "C":
            out.append(("C", g[1], -g[2]))
        elif g[0] == "phase":
            out.append(("phase", (-g[1]) % 4))
        else:
            need(g[0] == "X", "unknown Clifford gate")
            out.append(g)
    return tuple(out)


def fourier(rank: int) -> tuple[tuple, ...]:
    return tuple(("C", 1 << i, 1) for i in range(rank))


def frame(vectors0: list[int], n: int = 9) -> tuple[tuple, ...]:
    vectors = tuple(vectors0)
    rank = len(vectors)
    if rank == 0:
        return ()
    if rank == n:
        return fourier(n)
    matrix = transpose(extend(vectors, n))
    columns = transpose(inverse(matrix))
    quadratic = tuple(
        (1 << i) ^ sum(parity(a & b) << j for j, b in enumerate(columns))
        for i, a in enumerate(columns)
    )
    diagonal = tuple((row >> i) & 1 for i, row in enumerate(quadratic))
    chart = (("P", matrix), ("D", quadratic, diagonal))
    return adjoint(chart) + fourier(rank) + chart


def monomial(rec: dict) -> tuple[tuple, ...]:
    return (
        ("D", tuple(rec["quadratic_rows"]), tuple(rec["linear_Z4"])),
        ("P", tuple(rec["matrix_rows"])),
        ("X", rec["offset"]),
        ("phase", rec["phase"]),
    )


def recipe(rec: dict) -> tuple[tuple, ...]:
    r = rec["rank"]
    if r == 0:
        need(rec["right"] is None, "rank zero recipe right factor")
        return monomial(rec["left"])
    return monomial(rec["right"]) + fourier(r) + monomial(rec["left"])


def tableau(circ: tuple[tuple, ...], n: int = 9) -> tuple[tuple[int, int, int], ...]:
    rows = [(1 << i, 0, 0) for i in range(n)] + [(0, 1 << i, 0) for i in range(n)]
    for g in circ:
        typ = g[0]
        invt = transpose(inverse(g[1])) if typ == "P" else None
        out = []
        for x, z, ph in rows:
            if typ == "P":
                x, z = matmul_vec(g[1], x), matmul_vec(invt, z)
            elif typ == "X":
                ph += 2 * parity(z & g[1])
            elif typ == "C":
                if parity(z & g[1]):
                    x ^= g[1]
                    ph += 3 * g[2]
            elif typ == "D":
                q, linear = g[1:]
                ph += sum(linear[i] for i in range(n) if (x >> i) & 1)
                ph += 2 * sum(parity((q[i] >> (i + 1)) & (x >> (i + 1))) for i in range(n) if (x >> i) & 1)
                z ^= matmul_vec(q, x)
            else:
                need(typ == "phase", "unknown tableau gate")
            out.append((x, z, ph % 4))
        rows = out
    return tuple(rows)


def rotate(pair: tuple[int, int], power: int) -> tuple[int, int]:
    a, b = pair
    return ((a, b), (-b, a), (-a, -b), (b, -a))[power % 4]


def apply_state(circ: tuple[tuple, ...], basis: int = 0, n: int = 9) -> tuple[dict[int, tuple[int, int]], int]:
    state: dict[int, tuple[int, int]] = {basis: (1, 0)}
    den = 0
    for g in circ:
        typ = g[0]
        out: dict[int, tuple[int, int]] = {}
        if typ == "C":
            direction, sign = g[1:]
            for addr, (a, b) in state.items():
                for target, pair in (
                    (addr, (a - sign * b, b + sign * a)),
                    (addr ^ direction, (a + sign * b, b - sign * a)),
                ):
                    old = out.get(target, (0, 0))
                    out[target] = (old[0] + pair[0], old[1] + pair[1])
            den += 1
        else:
            for addr, pair in state.items():
                if typ == "P":
                    target = matmul_vec(g[1], addr)
                elif typ == "X":
                    target = addr ^ g[1]
                else:
                    target = addr
                    if typ == "D":
                        q, linear = g[1:]
                        power = sum(linear[i] for i in range(n) if (addr >> i) & 1)
                        power += 2 * sum(parity((q[i] >> (i + 1)) & (addr >> (i + 1))) for i in range(n) if (addr >> i) & 1)
                        pair = rotate(pair, power)
                    else:
                        need(typ == "phase", "unknown state gate")
                        pair = rotate(pair, g[1])
                need(target not in out, "noninjective monomial address map")
                out[target] = pair
        state = {addr: pair for addr, pair in out.items() if pair != (0, 0)}
        while den and all((a & 1) == 0 and (b & 1) == 0 for a, b in state.values()):
            den -= 1
            state = {addr: (a // 2, b // 2) for addr, (a, b) in state.items()}
    return state, den


def exact_equal(a: tuple[tuple, ...], b: tuple[tuple, ...]) -> bool:
    return tableau(a) == tableau(b) and apply_state(a) == apply_state(b)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    word_blob = (args.package / "output/rail-cross-four.json.gz").read_bytes()
    parent_blob = (args.package / "source-evidence/rail-consumer.json.gz").read_bytes()
    word = json.loads(gzip.decompress(word_blob))
    parent = json.loads(gzip.decompress(parent_blob))
    cert = json.loads((args.package / "CHART-MAPS.json").read_text())
    need(hashlib.sha256(word_blob).hexdigest() == WORD_SHA, "word pin")
    need(hashlib.sha256(parent_blob).hexdigest() == PARENT_SHA, "parent pin")
    old = {(o[2], o[3]) for o in parent["program"] if o[0] == "MOVE"}
    actual_pairs = {(o[2], o[3]) for o in word["program"] if o[0] == "MOVE"} - old
    certified = {(m["source"], m["target"]) for m in cert["maps"]}
    need(actual_pairs == certified and len(certified) == 23, "certificate covers exactly 23 new move pairs")
    checks = []
    for m in cert["maps"]:
        src, dst = m["source"], m["target"]
        f, g = word["frames"][src], word["frames"][dst]
        need(f == m["source_frame"] and g == m["target_frame"], f"frame bytes for {src}->{dst}")
        need(m["rank"] == len(g) - len(f) or m["rank"] == len(f) - len(g), f"rank for {src}->{dst}")
        need(m["recipe"]["rank"] == m["rank"], f"recipe rank for {src}->{dst}")
        expected = adjoint(frame(f)) + frame(g)
        actual = recipe(m["recipe"])
        need(exact_equal(actual, expected), f"exact signed map and phase {src}->{dst}")
        badrec = json.loads(json.dumps(m["recipe"]))
        badrec["left"]["phase"] = (badrec["left"]["phase"] + 1) % 4
        bad = recipe(badrec)
        need(tableau(bad) == tableau(actual), f"phase control tableau {src}->{dst}")
        need(apply_state(bad) != apply_state(expected), f"phase-only mutation was not caught {src}->{dst}")
        checks.append({"source": src, "target": dst, "rank": m["rank"], "signed_tableau_equal": True, "global_phase_equal": True, "phase_control_rejected": True})
    result = {
        "status": "PASS_INDEPENDENT_23_CHART_PHASE_REVIEW",
        "word_sha256": hashlib.sha256(word_blob).hexdigest(),
        "parent_sha256": hashlib.sha256(parent_blob).hexdigest(),
        "method": "Separate exact GF(2) frame construction; signed Pauli tableau plus dyadic Gaussian vacuum state pins global phase.",
        "maps": checks,
        "all_23": True,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
