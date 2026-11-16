"""Literal known-support resets of the completed D4 cohort interfaces.

This instantiates the root's source-reset theorem for the actual no-ADD closure
suffix. Every copied coordinate is completed, including61/67 in the S54 case.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

PINS = {
    'dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf',
    'bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987',
}

def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'))
    ap.add_argument('--word', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(); raw = a.word.read_bytes()
    assert hashlib.sha256(raw).hexdigest() in PINS
    w = json.loads(raw)
    source = (a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(source).hexdigest() == w['source_sha256']
    R = json.loads(source)['native_roots']
    e = load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py', 'reset_benchmark_engine')
    author = load(Path(__file__).with_name('build_d4_cohort.py'), 'cohort_trace')
    C, _, old_report = e.replay(w, R)
    cut = w['cohort']['continuation_before_operation']
    v, at = author.trace(w['operations'])[cut]
    owned = sorted({o[1] for o in w['operations'][:cut] if o[0] == 'INIT'})
    assert not any(o[0] == 'CLEAR' for o in w['operations'][:cut])
    suffix = copy.deepcopy(w['operations'][cut:])
    assert not any(o[0] == 'ADD' for o in suffix)
    S = sorted({i for n in owned for i in range(111) if v[n] >> i & 1})
    assert set(w['targets']) <= set(S)
    assert all(v[f'X{i}'] == 1 << i for i in range(111))
    assert all(at[f'X{i}'] in {f'L{i}', 'Hub'} for i in range(111))
    assert all(at[f'Y{i}'] in {'zero', f'F{i}'} for i in range(111))
    ops = []
    for i in S:
        n = f'KNOWN_NATIVE_{i}'
        ops += [['INIT', n, f'L{i}'], ['ADD', f'X{i}', n], ['MOVE', n, 'zero']]
    ops += [['INIT', n, at[n]] for n in owned]
    ops += [['ADD', f'KNOWN_NATIVE_{i}', f'Y{i}'] for i in S]
    for i in range(111):
        if at[f'X{i}'] != f'L{i}': ops.append(['MOVE', f'X{i}', at[f'X{i}']])
        if at[f'Y{i}'] != 'zero': ops.append(['MOVE', f'Y{i}', at[f'Y{i}']])
    interface = len(ops)
    ops += suffix
    ops += [['CLEAR', f'KNOWN_NATIVE_{i}'] for i in S]
    nw = {
        'source_path': w['source_path'], 'source_sha256': w['source_sha256'],
        'charts': w['charts'], 'targets': S, 'operations': ops,
        'schema': 'literal-known-support-reset-D4-closure-v1',
        'base_word_sha256': hashlib.sha256(raw).hexdigest(),
        'known_support': S, 'reset_interface_before_operation': interface,
        'reset_owner_count': len(owned),
        'scope': 'Every native ground-copied coordinate is completed. Old owners '
                 'are genuinely zero-initialized at their old cut charts. The actual '
                 'no-ADD closure suffix is appended verbatim. This benchmarks the '
                 'current source only and supplies no unpriced future acquisition.'}
    _, _, report = e.replay(nw, R)
    a.out.mkdir(parents=True, exist_ok=True)
    b = (json.dumps(nw, indent=2)+'\n').encode()
    (a.out/'WORD.json').write_bytes(b)
    result = {'status': 'PASS_LITERAL_D4_KNOWN_SUPPORT_RESET',
              'word_sha256': hashlib.sha256(b).hexdigest(),
              'base_word_sha256': hashlib.sha256(raw).hexdigest(),
              'old_partial_word': old_report, 'reset_word': report,
              'completed_count': len(S), 'completed_targets': S,
              'reset_owner_count': len(owned), 'reset_interface': interface,
              'old_suffix_operation_count': len(suffix),
              'old_suffix_contains_ADD': False, 'scope': nw['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))

if __name__ == '__main__': main()
