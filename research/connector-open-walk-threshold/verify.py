#!/usr/bin/env python3
"""Exact certificates and full dirty-action checks; no external dependencies.

@CubeJerry with OpenAI Codex assistance; Apache-2.0. The infinite theorem is
proved in README.md; arithmetic checks below are finite regression evidence.
"""
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path

from connector import (audit_events, compile_block, events, inspect_walk,
                       literal_prefix_audit, path_bounds, require)

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent.parent


def source_digest(data, expected):
    require(hashlib.sha256(data).hexdigest() == expected, 'source SHA256 drift')


def rejects(call):
    try:
        call()
    except ValueError:
        return 1
    raise RuntimeError('negative control unexpectedly accepted')


def main():
    sources = json.loads((PACKAGE / 'SOURCES.json').read_text())
    inputs = [row for row in sources['files'] if row['usage'] == 'input']
    for row in inputs:
        raw = (ROOT / row['path']).read_bytes()
        source_digest(raw, row['sha256'])
        rejects(lambda: source_digest(raw + b'\n', row['sha256']))
    # Compare theorem casework with direct ceilings, with no floating point.
    gaps = 0
    for k in range(1, 4097):
        lower = ((1 << k) - 1 + k - 1) // k
        lo, hi, case = path_bounds(k)
        require(lo == lower, 'lower bound arithmetic')
        if k == 1:
            require(hi == 1, 'dimension one')
            continue
        closed = 2 * (((1 << (k - 1)) + k - 1) // k)
        r = (1 << (k - 1)) % k
        if r == 1:
            require(hi == closed - 1 == lower, 'unique maximal coordinate case')
        elif r == 0 or 2 * r - 1 > k:
            require(hi == closed == lower, 'counting exact case')
        else:
            require(hi == closed == lower + 1, 'one unit gap case')
            gaps += 1
    primes = [k for k in range(3, 257, 2)
              if all(k % d for d in range(2, k))]
    for k in primes:
        require(path_bounds(k)[0] == path_bounds(k)[1], 'odd prime exactness')
    bundle = json.loads((PACKAGE / 'WITNESSES.json').read_text())
    require(bundle['schema'] == 'cube-covering-open-walk-v1', 'schema')
    require([w['dimension'] for w in bundle['walks']] == [6, 9, 10], 'fixture inventory')
    certificates = []
    controls = len(inputs)
    for witness in bundle['walks']:
        k = witness['dimension']
        c = witness['max_flip_count']
        word = witness['transitions']
        flips, _, _, _, endpoint = inspect_walk(k, word)
        require(len(word) == (1 << k) - 1, 'Hamilton path length')
        require(list(flips) == witness['flip_counts'], 'declared flips')
        require(max(flips) == c == path_bounds(k)[0], 'sharp threshold')
        require(endpoint.bit_count() == {6: 3, 9: 7, 10: 5}[k], 'nonadjacent endpoints')
        block = compile_block(k, c, word)
        masks = literal_prefix_audit(block)
        calls = audit_events(block, events(block))
        # Universal conversion also works at larger characteristic.
        larger = compile_block(k, c + 1, word)
        literal_prefix_audit(larger)
        audit_events(larger, events(larger))
        controls += rejects(lambda: compile_block(k, c - 1, word))
        controls += rejects(lambda: inspect_walk(k, [k] + word[1:]))
        controls += rejects(lambda: inspect_walk(k, word[:-1]))
        damaged = list(block.source_word)
        damaged[0] = (damaged[0] + 1) % k
        controls += rejects(lambda: literal_prefix_audit(replace(block, source_word=tuple(damaged))))
        # Deleting a source or padding event must fail exact complete execution.
        complete = list(events(block))
        omit_source = next(i for i, call in enumerate(complete) if call[0] == 'B')
        omit_output = next(i for i, call in enumerate(complete) if call[0] == 'A')
        controls += rejects(lambda: audit_events(block, complete[:omit_source] + complete[omit_source + 1:]))
        controls += rejects(lambda: audit_events(block, complete[:omit_output] + complete[omit_output + 1:]))
        certificates.append({'k': k, 'c': c, 'masks': masks, 'complete_calls': calls,
                             'flip_counts': list(flips)})
    # A non-Hamilton covering walk is a positive control for the broader theorem.
    repeated = [0, 1, 0, 1, 0]
    block = compile_block(2, 3, repeated)
    literal_prefix_audit(block)
    audit_events(block, events(block))
    small = compile_block(1, 2, [0])
    literal_prefix_audit(small)
    audit_events(small, events(small))
    exact = {k: path_bounds(k)[0] for k in range(1, 14)
             if path_bounds(k)[0] == path_bounds(k)[1]}
    exact.update({x['k']: x['c'] for x in certificates})
    require(set(exact) == set(range(1, 14)), 'all dimensions one through thirteen')
    expected = [1, 2, 3, 4, 7, 11, 19, 32, 57, 103, 187, 342, 631]
    require([exact[k] for k in range(1, 14)] == expected, 'threshold table')
    require(9 * (57 // 2) + 2 == 254 and 10 * (103 // 2) + 2 == 512, 'block arithmetic')
    print('PASS_OPEN_PATH_THRESHOLD ' + json.dumps({
        'certificates': certificates, 'negative_controls': controls,
        'formula_dimensions_checked': 4096, 'odd_primes_checked': len(primes),
        'open_formula_gaps_in_test_domain': gaps, 'exact_thresholds_1_to_13': expected,
        'source_inputs_checked': len(inputs)}, sort_keys=True))


if __name__ == '__main__':
    main()
