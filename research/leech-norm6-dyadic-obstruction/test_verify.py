#!/usr/bin/env python3
"""Independent arithmetic, input-mutation and standalone CLI controls."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
namespace = {"__name__": "package_verify_tests", "__file__": str(HERE / "verify.py")}
exec(compile((HERE / "verify.py").read_bytes(), str(HERE / "verify.py"), "exec"), namespace)
v = namespace
m, f = v["model"], v["rank5"]


def plain_rank(matrix):
    a = [[int(x) % 5 for x in row] for row in matrix]
    rank = 0
    for col in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = pow(a[rank][col], -1, 5)
        a[rank] = [scale * x % 5 for x in a[rank]]
        for i in range(rank + 1, len(a)):
            scale = a[i][col]
            a[i] = [(x - scale * y) % 5 for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def unpack(a, width):
    return [sum(((a[b] >> i) & 1) << b for b in range(3)) for i in range(width)]


def tree_hashes(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file()}


class Controls(unittest.TestCase):
    def test_scalar_truth_tables(self):
        for a, b in itertools.product(range(5), repeat=2):
            self.assertEqual(unpack(f.plus(f.pack([a]), f.pack([b])), 1), [(a + b) % 5])
            self.assertEqual(unpack(f.mul(f.pack([a]), b), 1), [a * b % 5])
        for a in range(5):
            self.assertEqual(unpack(f.neg(f.pack([a])), 1), [-a % 5])

    def test_mixed_columns_and_word_boundaries(self):
        rng = random.Random(31)
        a = [rng.randrange(5) for _ in range(4097)]
        b = [rng.randrange(5) for _ in range(4097)]
        self.assertEqual(unpack(f.plus(f.pack(a), f.pack(b)), len(a)),
                         [(x + y) % 5 for x, y in zip(a, b)])
        self.assertEqual(unpack(f.neg(f.pack(a)), len(a)), [-x % 5 for x in a])

    def test_exhaustive_two_by_two_ranks(self):
        for entries in itertools.product(range(5), repeat=4):
            rows = [entries[:2], entries[2:]]
            self.assertEqual(f.rank(rows)[0], plain_rank(rows))

    def test_seeded_rank_differential(self):
        rng = random.Random(31)
        for _ in range(200):
            height, width = rng.randrange(1, 21), rng.randrange(1, 25)
            rows = [[rng.randrange(5) for _ in range(width)] for _ in range(height)]
            self.assertEqual(f.rank(rows)[0], plain_rank(rows))
        self.assertEqual(f.rank([])[0], 0)
        self.assertEqual(f.rank([[], []])[0], 0)

    def test_arithmetic_input_rejections(self):
        for row in ([-1], [5], [True], [1.0]):
            with self.assertRaises(ValueError):
                f.pack(row)
        with self.assertRaises(ValueError):
            f.rank([[1], [1, 2]])
        with self.assertRaises(ValueError):
            f.mul((0, 0, 0), True)
        with self.assertRaises(ValueError):
            m.coordinates([0] * 23)
        with self.assertRaises(ValueError):
            m.features([0] * 24)

    def test_schema_and_witness_mutations(self):
        cert = v["read_json"](HERE / "CERTIFICATE.json")
        for key, value in (("prime", 2), ("prime", True), ("target_line_index", 1),
                           ("target_residue", 4), ("source_rank_mod5", 2600)):
            changed = copy.deepcopy(cert)
            changed[key] = value
            with self.assertRaises(ValueError):
                v["read_certificate"](changed)
        changed = copy.deepcopy(cert)
        changed["annihilator_digits"] = ["0" * 100] * 26
        with self.assertRaises(ValueError):
            v["read_certificate"](changed)
        changed = copy.deepcopy(cert)
        changed["verdict"] = "PASS"
        with self.assertRaises(ValueError):
            v["read_certificate"](changed)
        with self.assertRaises(ValueError):
            json.loads('{"prime":5,"prime":2}', object_pairs_hook=v["unique_object"])

    def test_direction_payload_rejections(self):
        data = v["read_json"](HERE / "DIRECTIONS.json")
        for key, value in (("count", 2600), ("count", True), ("format", "other"),
                           ("payload_sha256", "0" * 64), ("payload_base64", "!!!")):
            changed = dict(data)
            changed[key] = value
            with self.assertRaises((ValueError, TypeError)):
                v["read_pairs"](changed)
        changed = dict(data)
        changed["payload_base64"] += "A" * 20001
        with self.assertRaises(ValueError):
            v["read_pairs"](changed)

    def test_relocated_read_only_cli_and_file_mutations(self):
        with tempfile.TemporaryDirectory(prefix="leech proof with spaces ") as tmp:
            folder = Path(tmp) / "standalone package"
            shutil.copytree(HERE, folder, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            before = tree_hashes(folder)
            cmd = [sys.executable, "-I", "-O", "-B", str(folder / "verify.py"), "--json"]
            run = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=180)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(run.stdout)
            self.assertEqual((result["source_rank"], result["exchange_rank"]), (2599, 2600))
            self.assertEqual(result["support_minors"], 2)
            self.assertEqual(tree_hashes(folder), before)
            certificate = folder / "CERTIFICATE.json"
            original = certificate.read_bytes()
            certificate.unlink()
            run = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=20)
            self.assertNotEqual(run.returncode, 0)
            certificate.write_bytes(b'{"prime":5,"prime":2}')
            run = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=20)
            self.assertNotEqual(run.returncode, 0)
            certificate.write_bytes(original)
            payload = folder / "DIRECTIONS.json"
            original = payload.read_bytes()
            payload.write_text("not json", encoding="utf-8")
            run = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=20)
            self.assertNotEqual(run.returncode, 0)
            payload.write_bytes(original)
            self.assertEqual(tree_hashes(folder), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
