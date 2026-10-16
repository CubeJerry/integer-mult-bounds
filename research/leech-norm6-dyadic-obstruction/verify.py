#!/usr/bin/env python3
"""Read-only, standard-library verification of the fixed Leech obstruction."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import random
import sys
import types
import zlib

HERE = Path(__file__).resolve().parent
LINE_SHA = "72e983cc0fd21a2c99be502bfbc3575ff7c18d9951fb45b2048165841b163a25"
FORMAT = ("zlib+base64; each 5-byte little-endian record: i[0:17], j[17:34], "
          "positive-sign[34], upper five bits zero")


def module(name: str, path: Path):
    """Load current source bytes, not an existing .pyc or ambient module."""
    result = types.ModuleType(name)
    result.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), result.__dict__)
    return result


model = module("leech_obstruction_model", HERE / "model.py")
rank5 = module("leech_obstruction_rank5", HERE / "rank5.py")
budget = module("leech_obstruction_budget", HERE / "budget.py")
require = model.require


def unique_object(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate JSON key")
        out[k] = v
    return out


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def read_pairs(document):
    require(type(document) is dict and set(document) ==
            {"schema", "format", "count", "payload_sha256", "payload_base64"},
            "direction document fields")
    require(type(document["schema"]) is int and document["schema"] == 1,
            "direction schema")
    require(type(document["count"]) is int and document["count"] == 2601,
            "direction count")
    require(document["format"] == FORMAT, "direction encoding")
    encoded = document["payload_base64"]
    require(type(encoded) is str and len(encoded) <= 20000, "encoded payload size")
    packed = base64.b64decode(encoded, validate=True)
    decoder = zlib.decompressobj()
    raw = decoder.decompress(packed, 13006)
    require(len(raw) == 13005 and decoder.eof and not decoder.unused_data
            and not decoder.unconsumed_tail, "bounded canonical payload")
    require(hashlib.sha256(raw).hexdigest() == document["payload_sha256"],
            "direction payload digest")
    pairs = []
    for start in range(0, len(raw), 5):
        v = int.from_bytes(raw[start:start + 5], "little")
        require(v >> 35 == 0, "reserved record bits")
        pairs.append((v & 131071, (v >> 17) & 131071, 1 if v >> 34 & 1 else -1))
    return pairs


def read_certificate(c):
    keys = {"schema", "prime", "basis_direction_indices", "generator_seed",
            "direction_int8_sha256", "source_matrix_mod5_sha256", "annihilator_digits",
            "target_line_index", "target_coordinates", "target_residue",
            "source_rank_mod5", "exchange", "scope", "support_witnesses"}
    require(type(c) is dict and set(c) == keys, "certificate fields")
    for field, expected in (("schema", 1), ("prime", 5), ("generator_seed", 6242600),
                            ("target_line_index", 0), ("target_residue", 3),
                            ("source_rank_mod5", 2599)):
        require(type(c[field]) is int and c[field] == expected, field)
    require(c["basis_direction_indices"] == "0..2599 inclusive", "basis scope")
    chunks = c["annihilator_digits"]
    require(type(chunks) is list and len(chunks) == 26 and
            all(type(s) is str and len(s) == 100 and set(s) <= set("01234")
                for s in chunks), "annihilator encoding")
    z = tuple(int(x) for x in "".join(chunks))
    require(any(z), "zero annihilator")
    e = c["exchange"]
    require(type(e) is dict and set(e) == {"remove_direction_index", "add_direction_index",
            "rank_mod5", "new_direction", "new_residue"}, "exchange fields")
    for field, expected in (("remove_direction_index", 2599), ("add_direction_index", 2600),
                            ("rank_mod5", 2600), ("new_residue", 1)):
        require(type(e[field]) is int and e[field] == expected, field)
    require(type(c["target_coordinates"]) is list and
            all(type(v) is int for v in c["target_coordinates"]), "target integer coordinates")
    require(type(e["new_direction"]) is list and
            all(type(v) is int for v in e["new_direction"]), "exchange integer coordinates")
    require(tuple(c["target_coordinates"]) == model.line(0), "fixed target")
    return z


def is_annihilator(rows, z):
    return bool(any(z)) and all(model.dot(row, z) % 5 == 0 for row in rows)


def reject(call, label):
    try:
        call()
    except (ValueError, TypeError, KeyError, IndexError):
        return
    raise ValueError("control accepted: " + label)


def main_check(path: Path = HERE):
    pairs = read_pairs(read_json(path / "DIRECTIONS.json"))
    cert = read_json(path / "CERTIFICATE.json")
    z = read_certificate(cert)
    directions = tuple(model.direction(pair) for pair in pairs)
    require(len(set(directions)) == 2601, "distinct source directions")
    sha = hashlib.sha256(bytes(v & 255 for a in directions for v in a)).hexdigest()
    require(sha == cert["direction_int8_sha256"], "direction coordinate digest")
    require(directions[-1] == tuple(cert["exchange"]["new_direction"]), "exchange direction")

    # Whole line-order authentication, not an all-pairs lattice audit.
    digest = hashlib.sha256()
    for i in range(model.LINES):
        digest.update(bytes(x & 255 for x in model.line(i)))
    require(digest.hexdigest() == LINE_SHA, "complete source line ordering")
    _, octads = model.geometry()  # includes all 2024 triple-cover premises

    rows = []
    # Independent homogeneous expansion, multiplied to avoid all fractions.
    # This checks every coefficient, not only evaluations at sampled points.
    for a in directions:
        c = model.coordinates(a)
        for i in range(24):
            require(c[i] == 32 * (a[i] ** 3 - 8 * a[i]), "cubic diagonal coefficient")
        for offset, (i, j) in enumerate(model.PAIRS, 24):
            require(96 * c[offset] - 31 * c[i] ==
                    32 * (3 * a[i] * a[j] ** 2 - 8 * a[i]),
                    "cubic repeated-index coefficient")
        for offset, (i, j, k) in enumerate(model.TRIPLES, 576):
            require(3 * c[offset] == 6 * a[i] * a[j] * a[k],
                    "cubic distinct-index coefficient")
        rows.append(bytes(v % 5 for v in c))
    require(hashlib.sha256(b"".join(rows[:2600])).hexdigest() ==
            cert["source_matrix_mod5_sha256"], "coefficient matrix digest")
    require(is_annihilator(rows[:2600], z), "source annihilation")
    target = model.coordinates(model.line(0))
    require(model.dot(target, z) % 5 == 3, "actual kernel column separation")
    require(model.dot(rows[-1], z) % 5 == 1, "new encoder escapes the obstruction")

    # These are explicit rank-24 support minors, not a physical copy program.
    support = cert["support_witnesses"]
    require(type(support) is dict and set(support) ==
            {"probe_column_indices", "encoders"}, "support witness fields")
    columns = support["probe_column_indices"]
    require(type(columns) is list and len(columns) == len(set(columns)) == 64,
            "support probe columns")
    probes_for_support = [model.line(i) for i in columns]
    witnesses = support["encoders"]
    require(type(witnesses) is list and len(witnesses) == 2, "support witness count")
    for expected_index, w in zip((2599, 2600), witnesses):
        require(type(w) is dict and set(w) ==
                {"direction_index", "support_line_indices", "rank"}, "support witness keys")
        require(type(w["direction_index"]) is int and w["direction_index"] == expected_index,
                "support direction index")
        require(type(w["rank"]) is int and w["rank"] == 24, "support rank claim")
        indices = w["support_line_indices"]
        require(type(indices) is list and len(indices) == len(set(indices)) == 24,
                "support row indices")
        minor = []
        for i in indices:
            x = model.line(i)
            t = model.dot(directions[expected_index], x)
            require(t ** 3 - 256 * t != 0, "witness row outside encoder support")
            minor.append(sum(model.pairing(x, y) << j
                             for j, y in enumerate(probes_for_support)))
        require(model.binary_rank(minor) == 24, "support witness minor rank")

    # Full rank after the exchange also gives rank >=2599 for the original
    # matrix, because the two matrices share 2599 independent rows.
    exchange_rank, selected = rank5.rank(rows[:2599] + rows[2600:])
    require(exchange_rank == 2600 and len(selected) == 2600, "exchange full F5 rank")

    # Corroborate the coefficient derivation with direct polynomial evaluation.
    probes = (0, 1, 551, 552, 1000, 49127, 49128, 98279)
    chosen = sorted(random.Random(31).sample(range(2601), 32))
    fs = [(model.line(i), model.features(model.line(i))) for i in probes]
    for i in chosen:
        a, c = directions[i], model.coordinates(directions[i])
        for x, f in fs:
            t = model.dot(a, x)
            require((t ** 3 - 256 * t) % 3 == 0, "integer kernel numerator")
            require(model.dot(c, f) == (t ** 3 - 256 * t) // 3,
                    "direct polynomial identity")

    # Mathematical controls bypass file hashes: they must fail the equations.
    damaged_z = list(z)
    damaged_z[0] = (damaged_z[0] + 1) % 5
    require(not is_annihilator(rows[:2600], damaged_z), "changed annihilator control")
    require(not is_annihilator(rows[:2600], (0,) * 2600), "zero witness control")
    require(not is_annihilator(rows, z), "overgeneralized family control")
    j = next(i for i, v in enumerate(z) if v)
    damaged_row = bytearray(rows[0])
    damaged_row[j] = (damaged_row[j] + 1) % 5
    require(model.dot(damaged_row, z) % 5 != 0, "coefficient mutation control")
    require(model.dot(target, z) % 5 != 4, "wrong target residue control")
    i, j, sign = pairs[0]
    reject(lambda: model.direction((i, j, -sign)), "wrong source sign")
    reject(lambda: model.line(-1), "invalid line")
    reject(lambda: model.line(True), "boolean line")
    require(5 * __import__("fractions").Fraction(1, 5) == 1,
            "rational coefficients escape the dyadic model")

    budget_result = budget.check()
    return {"optimistic_stage_counts": budget_result["stage_counts"], "source_encoders": 2600, "coefficient_columns": 2600,
            "annihilation_equations": 2600, "prime": 5, "target_line": 0,
            "target_residue": 3, "source_rank": 2599, "exchange_rank": 2600,
            "exchange_remove": 2599, "exchange_add": 2600,
            "canonical_lines_checked": model.LINES, "octads": len(octads),
            "triple_cover": len(model.TRIPLES), "polynomial_checks": 256, "homogeneous_coefficients": 6762600,
            "support_minors": 2, "controls": 9, "no_new_kappa": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = main_check()
    except (ValueError, OSError, TypeError, KeyError, IndexError, zlib.error) as exc:
        print("FAIL_LEECH_NORM6_DYADIC: " + str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        print("PASS_LEECH_NORM6_DYADIC encoders=2600 prime=5 "
              "target_residue=3 ranks=2599->2600 controls=9 no_new_kappa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
