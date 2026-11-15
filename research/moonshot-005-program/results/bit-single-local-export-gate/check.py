#!/usr/bin/env python3
"""Source-bound algebraic single-export gate; no complete physical decoder.

No predecessor checker is imported. Rational chart elimination and binary
coefficient elimination are implemented here. Full-width conclusions use the
dual proof in PROOF.md, not extrapolation from scalar execution.
"""
import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS = {
    "sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json":
        "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e",
    "results/bit-coupled-singular-delivery/worker-a/two-receiver-output/COUPLED-WORD.json":
        "506b2e5be90448548e5e71d9757028962ed3c74806b328792e6e0b69a8f20ba5",
    "results/bit-coupled-singular-delivery/worker-a/two-receiver-output/UNCOPLED-WORD.json":
        "f06ea0a429fe0a2a059fec76ed390383c3ec05b93327fe4d15c1cbf00c9cdac2",
}
DONORS = [16, 19, 38, 49, 50, 56, 57]
ALL = (1 << 111) - 1


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def parity(a, b):
    return (a & b).bit_count() & 1


def support(a):
    return [j for j in range(111) if a >> j & 1]


def rational_basis(rows):
    b = {}
    for row in rows:
        a = list(map(F, row))
        for k in sorted(b):
            if a[k]:
                q = a[k]
                a = [x - q * y for x, y in zip(a, b[k])]
        if any(a):
            k = next(j for j, x in enumerate(a) if x)
            q = a[k]
            b[k] = [x / q for x in a]
    return b


def projective_remainder(row, b):
    a = list(map(F, row))
    for k in sorted(b):
        if a[k]:
            q = a[k]
            a = [x - q * y for x, y in zip(a, b[k])]
    if not any(a):
        return None
    q = next(x for x in a if x)
    return tuple(x / q for x in a)


def binary_basis(rows):
    b = {}
    for j, x in enumerate(rows):
        tag = 1 << j
        while x:
            k = x.bit_length() - 1
            if k in b:
                x ^= b[k][0]
                tag ^= b[k][1]
            else:
                b[k] = (x, tag)
                break
    return b


def solve(rows, target):
    b = binary_basis(rows)
    tag = 0
    while target:
        k = target.bit_length() - 1
        if k not in b:
            return None
        target ^= b[k][0]
        tag ^= b[k][1]
    return tag


def nullspace(rows, allowed):
    b = binary_basis(rows)
    out = []
    for j in range(111):
        if not allowed >> j & 1 or j in b:
            continue
        z = 1 << j
        for k in sorted(b):
            if parity(b[k][0], z):
                z ^= 1 << k
        need(not z & ~allowed, "dual leaves allowed coordinates")
        need(all(not parity(x, z) for x in rows), "invalid nullspace row")
        out.append(z)
    need(len(out) + len(b) == allowed.bit_count(), "nullspace dimension")
    return out


def combine(rows, tag):
    z = 0
    for j, x in enumerate(rows):
        if tag >> j & 1:
            z ^= x
    return z


def reconstruct(word):
    rows = {f"X{i}": 1 << i for i in range(111)}
    rows.update({f"Y{i}": 1 << (111 + i) for i in range(111)})
    places = {f"X{i}": f"L{i}" for i in range(111)}
    places.update({f"Y{i}": "zero" for i in range(111)})
    born = set()
    for op in word["operations"]:
        kind, name, *rest = op
        if kind == "INIT":
            need(name not in rows, "duplicate owner")
            rows[name] = 0
            places[name] = rest[0]
            born.add(name)
        elif kind == "ADD":
            target = rest[0]
            need(name != target and places[name] == places[target], "noncochart ADD")
            rows[target] ^= rows[name]
        elif kind == "MOVE":
            places[name] = rest[0]
        elif kind == "CLEAR":
            need(name in born, "original CLEAR")
            del rows[name], places[name]
        else:
            raise ValueError("unknown opcode")
    for i in range(111):
        need(rows[f"X{i}"] == 1 << i and places[f"X{i}"] == "Hub", "original restoration")
        want = (1 << (111 + i)) ^ ((1 << i) if i in [17, 34] else 0)
        need(rows[f"Y{i}"] == want, "original Y coefficient")
    for name, expected in word["expected_owned_at_handoff"].items():
        need(rows[name] == int(expected["value_hex"], 16), "frozen owner value")
        need(places[name] == expected["chart"], "frozen owner chart")
    return rows


def validate_dual(q, i, allowed, G):
    need(q >> i & 1, "dual does not see requested coordinate")
    need(not q & ~allowed, "dual support is not allowed")
    need(all(not parity(q, g) for g in G), "dual does not annihilate G")


def validate_exception(q2, q13, u13, L, outside, G):
    validate_dual(q2, 2, outside[2], G)
    validate_dual(u13, 13, outside[13], G)
    need(not q13 & ~outside[13], "second dual leaves receiver13 nonlocal set")
    need(all(not parity(q13, g) for g in G), "second dual fails G annihilation")
    need(not (q13 >> 13 & 1), "second dual sees receiver13 coordinate")
    need(q2 & L == q13 & L, "exceptional local restrictions differ")


def run_variant(word, roots):
    rows = reconstruct(word)
    G = [rows[f"P{i}"] for i in range(8)] + [1 << j for j in DONORS]
    need(len(binary_basis(G)) == 15, "G rank")
    outside = [sum(1 << j for j, s in enumerate(roots) if dot(r, s)) for r in roots]
    base = [i for i, m in enumerate(outside) if solve([g & m for g in G], 1 << i) is not None]
    need(base == sorted([16, 17, 19, 38, 49, 50, 56, 57, 59, 60] + ([] if word["coupled"] else [34])), "baseline fitting roles")
    missing = [i for i in range(111) if i not in base + [34]]
    need(len(missing) == 100, "unserved missing roles")
    all_duals = {i: next(q for q in nullspace([g & outside[i] for g in G], outside[i]) if q >> i & 1)
                 for i in missing}
    charts = sorted({v["chart"] for name, v in word["expected_owned_at_handoff"].items()
                     if name.startswith(("DC", "SC"))})
    need(len(charts) == 33, "raw source chart catalogue size")
    certs = []
    exceptions = []
    stats = Counter()
    positive = None
    for chart in charts:
        N = word["charts"][chart]["rows"]
        b = rational_basis(N)
        L = sum(1 << j for j, r in enumerate(roots) if all(not dot(r, n) for n in N))
        groups = {}
        inside_normal = []
        for i in missing:
            key = projective_remainder(roots[i], b)
            if key is None:
                inside_normal.append(i)
            else:
                groups.setdefault(key, []).append(i)
        candidates = {}
        exclusions = {}
        for i in missing:
            nonlocal_non_source = outside[i] & ~L
            tag = solve([g & nonlocal_non_source for g in G], (1 << i) & nonlocal_non_source)
            if tag is None:
                q = next(q for q in nullspace([g & nonlocal_non_source for g in G], nonlocal_non_source)
                         if q >> i & 1)
                validate_dual(q, i, nonlocal_non_source, G)
                exclusions[str(i)] = hex(q)
            else:
                g = combine(G, tag)
                z = ((1 << i) ^ g) & outside[i] & L
                need(z != 0, "missing role has zero candidate payload")
                need(not z & ~L, "payload not source-local")
                need(not (((1 << i) ^ g ^ z) & outside[i]), "candidate fitting identity")
                candidates[i] = {"payload_hex": hex(z), "G_combination_bits": tag,
                                 "local_correction_hex": hex((1 << i) ^ g ^ z)}
        need(all(i in {int(k) for k in exclusions} for i in inside_normal),
             "source-local field creates a role whose facet already contains its source")
        group_records = []
        for key, group in groups.items():
            good = [i for i in group if i in candidates]
            stats["destination_groups"] += 1
            stats[f"groups_with_{len(good)}_individually_possible_roles"] += 1
            if len(good) > 1:
                need(chart == "D4" and good == [2, 13], "unclassified possible sharing pair")
                q2 = int("d22000000000000000000004", 16)
                q13 = int("50122000000000000000000004", 16)
                u13 = all_duals[13]
                validate_exception(q2, q13, u13, L, outside, G)
                exception = {"source_chart": chart, "roles": good,
                             "q2_hex": hex(q2), "q13_hex": hex(q13),
                             "u13_hex": hex(u13), "equal_local_restriction_hex": hex(q2 & L)}
                exceptions.append(exception)
                z2, z13 = [int(candidates[i]["payload_hex"], 16) for i in good]
                need(solve([g & outside[2] for g in G + [z2, z13]], 1 << 2) is not None,
                     "two-payload control misses receiver2")
                need(solve([g & outside[13] for g in G + [z2, z13]], 1 << 13) is not None,
                     "two-payload control misses receiver13")
                need(solve([g & outside[13] for g in G + [z2]], 1 << 13) is None,
                     "single first payload unexpectedly fits both")
                need(solve([g & outside[2] for g in G + [z13]], 1 << 2) is None,
                     "single second payload unexpectedly fits both")
                positive = {"source_chart": chart, "destination_normals": N + [roots[2]],
                            "rank_drop_for_each": 1, "receiver_roles": good,
                            "payloads": {str(i): candidates[i] for i in good},
                            "scope": "Exact relaxed two-field witness; local source preparation and actual G/correction access are not constructed."}
            group_records.append({"representative": group[0], "reachable_missing_roles": group,
                                  "individually_possible_roles": good})
        certs.append({"source_chart": chart, "normal_rank": len(b),
                      "source_local_indices": support(L), "inside_source_normal_span": inside_normal,
                      "groups": group_records, "excluded_receiver_duals": exclusions,
                      "possible_receiver_witnesses": {str(i): z for i, z in candidates.items()}})
    need(len(exceptions) == 1 and positive is not None, "exception count")
    # Affected facts are deliberately broken; these reject without reusing the
    # author's search or a claim that success is equivalent to a universal proof.
    e = exceptions[0]
    L = sum(1 << i for i in next(c for c in certs if c["source_chart"] == "D4")["source_local_indices"])
    q2, q13, u13 = [int(e[k], 16) for k in ["q2_hex", "q13_hex", "u13_hex"]]
    mutants = {
        "erase_requested_dual_coordinate": (q2 ^ (1 << 2), q13, u13, L, outside, G),
        "delete_receiver13_invertibility_dual": (q2, q13, 0, L, outside, G),
        "wrong_local_restriction": (q2, q13 ^ (1 << 85), u13, L, outside, G),
        "silently_grant_receiver2_in_G": (q2, q13, u13, L, outside, G + [1 << 2]),
    }
    rejecting = {}
    for name, args in mutants.items():
        try:
            validate_exception(*args)
        except ValueError as exc:
            rejecting[name] = str(exc)
        else:
            raise ValueError("accepted negative control " + name)
    return {"formal_input_columns_reconstructed": 222, "G_rows_hex": list(map(hex, G)),
            "baseline_fitting_roles": base, "unserved_missing_roles": missing,
            "catalogue_charts": charts, "statistics": dict(stats), "chart_certificates": certs,
            "exceptional_two_role_obstruction": exceptions[0], "two_payload_positive_control": positive,
            "negative_controls": rejecting}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent)
    a = parser.parse_args()
    p = a.repo / "research/moonshot-005-program"
    data = {}
    for rel, sha in PINS.items():
        raw = (p / rel).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == sha, "source hash mismatch: " + rel)
        data[rel] = json.loads(raw)
    roots = data[next(iter(PINS))]["native_roots"]
    need(len(roots) == 111 and len({tuple(r) for r in roots}) == 111, "native source size")
    results = {}
    for variant in ["COUPLED", "UNCOPLED"]:
        rel = f"results/bit-coupled-singular-delivery/worker-a/two-receiver-output/{variant}-WORD.json"
        results[variant] = run_variant(data[rel], roots)
    cert = {"status": "PASS_SINGLE_RANK_ONE_LOCAL_EXPORT_NO_TWO_NEW_RECEIVERS",
            "source_pins": PINS, "variants": results, "new_complete_kappa": False,
            "scope": "One rank-one descent from any of 33 actual raw-cache charts; arbitrary source-local payload modulo the globally granted G; all local output corrections granted. Multi-export interaction and changed G are outside."}
    summary = {"status": cert["status"], "source_pins": PINS,
               "variants": {k: {"statistics": v["statistics"], "source_charts": len(v["catalogue_charts"]),
                                "missing_receivers": len(v["unserved_missing_roles"]),
                                "maximum_new_receivers_per_single_rank_one_export": 1,
                                "exception": v["exceptional_two_role_obstruction"],
                                "negative_control_count": len(v["negative_controls"])}
                            for k, v in results.items()},
               "classification": "Source-specific universal linear/block gate with exact finite geometric premises; no decoder construction or new kappa.",
               "new_complete_kappa": False}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "CERTIFICATE.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (a.out / "RESULT.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
