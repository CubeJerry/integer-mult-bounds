"""Byte reproduction of the coherent 36 -> 38 -> 39 -> clique39 -> triple41 chain.

This is deterministic construction reproduction, not independent mathematical review.
The source and endpoint replay receipts are produced by each stage's verifier.
"""
from pathlib import Path
import argparse
import hashlib
import json

import build_common38
import build_common39
import build_clique39
import build_clique41


def digest(word):
    return hashlib.sha256((json.dumps(word, indent=2) + '\n').encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--base36', type=Path, required=True)
    parser.add_argument('--expected41', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    word = json.loads(args.base36.read_text())
    assert digest(word) == build_common38.BASE
    source = (args.repo / word['source_path']).read_bytes()
    assert hashlib.sha256(source).hexdigest() == word['source_sha256']
    roots = json.loads(source)['native_roots']
    rows = []
    for name, module, geometric, expected in [
        ('common38', build_common38, False, build_common39.BASE),
        ('common39', build_common39, False, build_clique39.BASE),
        ('clique39', build_clique39, True, build_clique41.BASE),
        ('clique41', build_clique41, True, '07ed37cf9dfa1da24d3518e25e46d7b29141582f71f32da1191f13fbc9b1971f'),
    ]:
        assert digest(word) == module.BASE
        word = module.build(word, roots) if geometric else module.build(word)
        observed = digest(word)
        assert observed == expected, (name, observed, expected)
        rows.append({'stage': name, 'word_sha256': observed, 'targets': len(word['targets'])})
    expected = args.expected41.read_bytes()
    assert expected == (json.dumps(word, indent=2) + '\n').encode()
    result = {'status': 'PASS_BYTE_REPRODUCTION_OF_ALL_FOUR_STAGES',
              'source_sha256': word['source_sha256'], 'stages': rows,
              'scope': 'Construction reproduction only; independent review is separately required.'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])


if __name__ == '__main__':
    main()
