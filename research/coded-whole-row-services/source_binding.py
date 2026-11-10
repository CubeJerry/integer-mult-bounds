"""Authenticate retained source bytes and execute those exact bytes, without pyc."""
from hashlib import sha1, sha256
from pathlib import Path
from types import ModuleType
import json
import sys

PACKAGE = Path(__file__).resolve().parent


def authenticate():
    manifest = json.loads((PACKAGE / 'DEPENDENCIES.json').read_text())
    authenticated = {}
    for pin in manifest['files']:
        raw = (PACKAGE / pin['local_path']).read_bytes()
        blob = sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if (len(raw) != pin['bytes'] or sha256(raw).hexdigest() != pin['sha256']
                or blob != pin['git_blob']):
            raise ValueError('retained source mismatch: ' + pin['local_path'])
        authenticated[pin['local_path']] = raw
    return authenticated


def modules():
    raw = authenticate()
    loaded = []
    for stem in ('machine', 'stack', 'exact_scalar_tables'):
        path = PACKAGE / 'retained' / (stem + '.py')
        name = 'coded_whole_row_retained_' + stem
        module = ModuleType(name)
        module.__file__ = str(path)
        sys.modules[name] = module
        exec(compile(raw['retained/' + stem + '.py'], str(path), 'exec'), module.__dict__)
        loaded.append(module)
    return tuple(loaded)
