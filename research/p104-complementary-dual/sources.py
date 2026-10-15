#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Pinned, temporary predecessor loading; no network or Git at replay time.

Prepared for @CubeJerry with substantial OpenAI Codex assistance.
"""
from contextlib import contextmanager
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def checked(raw, digest, label):
    require(sha(raw) == digest, "source digest: " + label)
    return raw


def module(name, path):
    spec = importlib.util.spec_from_file_location("p104_dual_" + name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


def inventory():
    return json.loads((HERE / "SOURCES.json").read_bytes())


def live_inputs():
    result = {}
    for item in inventory()["files"]:
        if item["usage"] == "input":
            result[item["path"]] = checked((ROOT / item["path"]).read_bytes(),
                                           item["sha256"], item["path"])
    return result


def word(name):
    raw = gzip.decompress((HERE / name).read_bytes())
    checked(raw, inventory()["word_payload_sha256"][name], name + " (decompressed)")
    result = json.loads(raw)
    require(raw == canonical(result), "noncanonical word payload")
    return result


@contextmanager
def predecessor():
    """Extract only the pinned regular-file inventory into fresh temporary storage."""
    inputs = live_inputs()
    pin = inventory()["producer_archive"]
    raw = checked((HERE / pin["path"]).read_bytes(), pin["sha256"], pin["path"])
    expected = {item["path"]: item for item in pin["members"]}
    require(len(expected) == len(pin["members"]), "duplicate archive pin")
    with tempfile.TemporaryDirectory(prefix="p104-dual-") as directory:
        root = Path(directory)
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
            members = archive.getmembers()
            require(len(members) == len(expected)
                    and {m.name for m in members} == set(expected), "archive inventory")
            for member in members:
                path = PurePosixPath(member.name)
                require(member.isfile() and not path.is_absolute() and ".." not in path.parts
                        and path.as_posix() == member.name, "unsafe archive member")
                payload = checked(archive.extractfile(member).read(),
                                  expected[member.name]["sha256"], member.name)
                target = root / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
        for name, payload in inputs.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        yield root
