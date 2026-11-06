#!/usr/bin/env python3
"""Bounded Posa-rotation discovery; exact verification is in separate programs.

@CubeJerry with OpenAI Codex assistance; Apache-2.0.
"""
import json
import math
from pathlib import Path
import random


def discover(k, seed=43, cap=3_000_000):
    rng = random.Random(seed)
    n = 1 << k
    path = [i ^ (i >> 1) for i in range(n)]
    counts = [1 << (k - 1 - j) for j in range(k)]
    positions = [0] * n
    for i, vertex in enumerate(path):
        positions[vertex] = i
    goal = (n - 2) // k + 1
    for iteration in range(cap):
        axis = rng.randrange(k)
        pivot = positions[path[-1] ^ (1 << axis)]
        if pivot >= n - 2:
            continue
        removed = (path[pivot] ^ path[pivot + 1]).bit_length() - 1
        delta = 2 * (counts[axis] - counts[removed] + 1)
        temperature = 1 if iteration % 100_000 < 80_000 else 8
        if delta > 0 and rng.random() > math.exp(-delta / temperature):
            continue
        path[pivot + 1:] = reversed(path[pivot + 1:])
        for i in range(pivot + 1, n):
            positions[path[i]] = i
        counts[removed] -= 1
        counts[axis] += 1
        if max(counts) <= goal:
            return {'dimension': k, 'seed': seed, 'iterations': iteration + 1,
                    'max_flip_count': max(counts), 'flip_counts': counts,
                    'transitions': [(a ^ b).bit_length() - 1
                                    for a, b in zip(path, path[1:])]}
    raise RuntimeError(f'bounded search exhausted at dimension {k}; no impossibility claim')


def main():
    result = {'schema': 'cube-covering-open-walk-v1',
              'walks': [discover(k) for k in (6, 9, 10)]}
    expected = json.loads(Path(__file__).with_name('WITNESSES.json').read_text())
    if result != expected:
        raise RuntimeError('regenerated witness differs; exact checkers remain authoritative')
    print('PASS_OPEN_PATH_REGENERATION ' + json.dumps(
        [{'dimension': w['dimension'], 'iterations': w['iterations']}
         for w in result['walks']], sort_keys=True))


if __name__ == '__main__':
    main()
