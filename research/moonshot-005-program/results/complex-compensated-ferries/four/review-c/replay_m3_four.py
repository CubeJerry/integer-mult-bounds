#!/usr/bin/env python3
"""Independent exact check of the three-copy funded-cross-four lift."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


M3_WORD_SHA = "3df717ae5d6081ed8c19de677751426597b26473169a8f072f92aac22f39a741"
RAIL_SHA = "20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f"
SOURCE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
FULL_PIN = "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7"
RAW = {1: 990, 2: 360, 3: 105, 4: 112, 5: 133, 6: 8, 7: 2}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def readgz(path: Path) -> tuple[bytes, dict]:
    blob = path.read_bytes()
    return blob, json.loads(gzip.decompress(blob))


def moment_interval(profile: dict[int, int], places: int = 30) -> tuple[F, F]:
    """Rigorous rational enclosure for sum c_r r^(199/200)."""
    den = 10 ** places
    lo = hi = F(0)
    for r, count in profile.items():
        if not r or not count:
            continue
        n = r ** 199 * den ** 200
        left, right = 0, 1 << ((n.bit_length() + 199) // 200)
        while right - left > 1:
            mid = (left + right) // 2
            if mid ** 200 <= n:
                left = mid
            else:
                right = mid
        exact = left ** 200 == n
        low_root = F(left, den)
        high_root = low_root if exact else F(left + 1, den)
        if count > 0:
            lo += count * low_root
            hi += count * high_root
        else:
            lo += count * high_root
            hi += count * low_root
    return lo, hi


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    replay_path = Path(__file__).resolve().parent.parent / "funded-cross-pair-review" / "replay.py"
    spec = importlib.util.spec_from_file_location("worker_c_exact_replay", replay_path)
    replay_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay_mod)

    m3_blob, m3 = readgz(args.package / "m3/WORD.json.gz")
    q_blob, q = readgz(args.package / "output/rail-cross-four.json.gz")
    source_blob = (args.source / "research/shared-wire-split-composition/data/final.json.gz").read_bytes()
    source = json.loads(gzip.decompress(source_blob))
    full_blob = (args.source / "research/shared-wire-split-composition/FULL-RESULT.json").read_bytes()
    full = json.loads(full_blob)
    result = json.loads((args.package / "m3/RESULT.json").read_text())
    need(sha(m3_blob) == M3_WORD_SHA, "m3 word pin")
    need(sha(q_blob) == RAIL_SHA and sha(source_blob) == SOURCE_SHA and sha(full_blob) == FULL_PIN, "input pins")
    need(m3["source_sha256"] == SOURCE_SHA and m3["rail_sha256"] == RAIL_SHA and m3["copies"] == 3, "composition provenance")
    need(m3["public"] == 2280 and len(m3["initial"]) == 2280, "m3 full domain")

    actual, aloc, abill = replay_mod.replay(m3)
    # The two factors are independently replayed in their own native domains.
    frames = m3["frames"]
    common_word = dict(source)
    common_word["frames"] = frames
    common, cloc, cbill = replay_mod.replay(common_word)
    private, ploc, pbill = replay_mod.replay(q)
    need(m3["initial"] == source["initial"] + q["initial"] * 2, "literal input chart interface")

    roles = {int(k): int(v) for k, v in q["source_role_map"].items()}
    rev = {v: k for k, v in roles.items()}
    need(len(roles) == 400 and set(rev) == set(range(400)), "bijection between Q rows and source private roles")
    need(q["initial"] == [source["initial"][rev[i]] for i in range(400)], "Q starts at native private role charts")
    need(q["frames"][:len(source["frames"])] == source["frames"], "shared chart identifiers")
    need(all(actual[i] == common[i] and aloc[i] == cloc[i] for i in range(1480)), "all 1480 common outputs")
    checks = 0
    for copy_index in range(2):
        base = 1480 + 400 * copy_index
        for i in range(400):
            expected = dict(common[rev[i]])
            for k, c in private[i].items():
                expected[base + k] = expected.get(base + k, F(0)) + c
                if not expected[base + k]:
                    del expected[base + k]
                expected[rev[k]] = expected.get(rev[k], F(0)) - c
                if not expected[rev[k]]:
                    del expected[rev[k]]
            need(actual[base + i] == expected, f"copy {copy_index+1}, endpoint {i}: exact composed map")
            need(aloc[base + i] == ploc[i] == source["final"][rev[i]], f"copy {copy_index+1}, endpoint {i}: final chart")
            checks += 1

    # Count/profile replay independently from the frozen word.
    need(abill["instructions"] == 85489, "m3 instruction count")
    need(abill["op_counts"] == {"ADD": 72084, "CLEAR": 858, "COPY": 1, "INIT": 858, "MOVE": 8022, "SCALE": 3666}, "m3 opcode profile")
    need(abill["lifetimes"] == 858 and abill["peak"] == 43, "m3 owner schedule")
    need(abill["move_ranks"] == {1: 4523, 2: 1092, 3: 1003, 4: 281, 5: 718, 6: 19, 7: 36, 8: 350}, "m3 movement profile")
    need(abill["instructions"] == cbill["instructions"] + 2 * (pbill["instructions"] + 800), "composition event count")
    need(abill["lifetimes"] == cbill["lifetimes"] + 2 * pbill["lifetimes"], "composition owner count")
    need(abill["peak"] == max(cbill["peak"], pbill["peak"]), "serial owned peak")

    # Reconstruct the pinned complete caller's m=3 T/P profiles with exact
    # integer coefficients before evaluating any fractional movement cost.
    T = {int(k): int(v) for k, v in full["invoice"]["T"].items()}
    P = {int(k): int(v) for k, v in full["invoice"]["P"].items()}
    H = {int(k): int(v) for k, v in full["native"]["helpers"].items()}
    N = {int(k): int(v) for k, v in full["native"]["paid"].items()}
    Q = {int(k): int(v) for k, v in pbill["move_ranks"].items()}
    tm = {r: 3 * T.get(r, 0) - 36 * H.get(r, 0) for r in set(T) | set(H)}
    pm = {
        r: 3 * P.get(r, 0) - 36 * (N.get(r, 0) - RAW.get(r, 0)) + 36 * (Q.get(r, 0) - RAW.get(r, 0))
        for r in set(P) | set(N) | set(Q) | set(RAW)
    }
    tm = {r: v for r, v in tm.items() if v}
    pm = {r: v for r, v in pm.items() if v}
    need(all(v >= 0 for v in tm.values()) and all(v >= 0 for v in pm.values()), "nonnegative paid/target profiles")
    need(tm == {int(k): int(v) for k, v in result["T"].items()}, "m3 target profile")
    need(pm == {int(k): int(v) for k, v in result["P"].items()}, "m3 paid profile")
    signed = {r: tm.get(r, 0) - pm.get(r, 0) for r in set(tm) | set(pm)}
    lo, hi = moment_interval(signed)
    perrail = (lo / 36, hi / 36)
    saved_lower = sum(r * c for r, c in signed.items())
    need(sum(tm.values()) == result["productive_count"] == 31296, "productive count")
    need(sum(pm.values()) == result["paid_count"] == 156492, "paid count")
    need(saved_lower == result["rank_surplus"] == 4380, "integer rank surplus")
    published = tuple(F(x) for x in result["moment_bounds"])
    published_perrail = tuple(F(x) for x in result["per_rail_moment_bounds"])
    # The published checker rounds rank 1 upward by one 1e-30 unit even though
    # 1^(199/200) is exact. For its negative coefficient this makes the lower
    # bound slightly more conservative; verify its interval contains ours.
    need(published[0] <= lo <= hi <= published[1], "published interval contains independently tightened interval")
    need(published_perrail == (published[0] / 36, published[1] / 36), "published per-rail bounds")
    need(float(perrail[0]) > 10.08199220, "displayed per-rail margin lower bound")
    need(result["complete_endpoint"] is False, "no complete endpoint inferred")

    out = {
        "status": "PASS_INDEPENDENT_M3_CROSS_FOUR_MAP_AND_INVOICE_REPLAY",
        "m3_word_sha256": sha(m3_blob),
        "rail_sha256": sha(q_blob),
        "source_sha256": sha(source_blob),
        "full_caller_sha256": sha(full_blob),
        "input_directions": 2280,
        "separate_endpoint_comparisons": 2280,
        "common_outputs": 1480,
        "private_outputs": checks,
        "ordinary_bill": {
            "instructions": abill["instructions"],
            "op_counts": abill["op_counts"],
            "move_ranks": abill["move_ranks"],
            "lifetimes": abill["lifetimes"],
            "peak": abill["peak"],
        },
        "productive_count": sum(tm.values()),
        "paid_count": sum(pm.values()),
        "rank_surplus": saved_lower,
        "moment_bounds": [str(lo), str(hi)],
        "per_rail_moment_bounds": [str(perrail[0]), str(perrail[1])],
        "per_rail_moment_lower_decimal": float(perrail[0]),
        "published_moment_bounds": [str(published[0]), str(published[1])],
        "published_per_rail_bounds": [str(published_perrail[0]), str(published_perrail[1])],
        "published_bounds_contain_independent_tight_interval": True,
        "complete_endpoint": False,
        "scope": "Exact three-copy lift and invoice for the frozen rank-54 partial rail; no full supplier or endpoint completion claimed.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
