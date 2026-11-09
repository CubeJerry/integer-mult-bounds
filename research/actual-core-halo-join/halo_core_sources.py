"""Exact retained Core/halo closure; only source locations are rebound.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from hashlib import sha1, sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = HERE / 'retained/core'
HALO = HERE / 'retained/halo'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def authenticate():
    checked = {}
    for name, key, root in (('SOURCES.json', 'path', ROOT),
                            ('DEPENDENCIES.json', 'retained', HERE)):
        for row in json.loads((HERE / name).read_text())['files']:
            if row.get('usage', 'input') != 'input':
                continue
            path = root / row[key]
            need(path.is_file() and not path.is_symlink(), 'regular input ' + row[key])
            raw = path.read_bytes()
            need(sha256(raw).hexdigest() == row['sha256'], 'SHA256 ' + row[key])
            need(sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                 == row['git_blob'], 'Git blob ' + row[key])
            checked[row[key]] = row['sha256']
    return checked


def load(name, path):
    need(name not in sys.modules, 'cold module ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def core_sources():
    authenticate()
    sys.path.insert(0, str(CORE))
    module = load('join_sources', CORE / 'join_sources.py')
    module.ROOT = ROOT
    return module


def halo_sources():
    authenticate()
    return load('attached_first_face', HALO / 'first-face-reference-join/join.py')
