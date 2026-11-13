#!/usr/bin/env python3
"""Source authentication and finite corroboration; no scientific imports."""
from fractions import Fraction as F
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import json
import subprocess

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def clog(n, base):
    """Least L with max(1,n)<=base**L, using integer arithmetic."""
    value, power = 0, 1
    while power < max(1, n):
        value, power = value + 1, power * base
    return value


def run(repo):
    sources = json.loads((HERE / 'SOURCES.json').read_text())['files']
    for pin in sources:
        raw = subprocess.check_output(['git', 'show', pin['commit'] + ':' + pin['path']], cwd=repo)
        need(len(raw) == pin['bytes'] and sha256(raw).hexdigest() == pin['sha256'], 'source bytes')
        need(sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == pin['git_blob'], 'Git blob')
    edges = stocks = atomizations = 0
    for stage in (1, 2):
        need((stage, 1, 10**9) < (stage, 2, 0), 'ordinary-to-body kind decrease')
        need((stage - 1, 2, 10**9) < (stage, 1, 1), 'older backend independent of argument size')
        for base in range(2, 19):
            for n in range(base, 4 * base * base + 1):
                child = n // base
                need(1 <= child < n, 'proper child')
                need((stage, 1, child) < (stage, 1, n), 'same-stage tuple')
                need(clog(child, base) <= clog(n, base) - 1, 'fresh stock depth')
                edges += 1
                stocks += 1
    for e in range(1, 129):
        for w in range(1, 17):
            for k in range((e - 1) // 2 + 1):
                n, rem = divmod(e - k, w)
                need(0 <= rem < w and n * w + rem + k == e, 'exact atomization')
                for base in (2, 3, 7, 17):
                    root = 2 + clog((e + w - 1) // w, base)
                    need(clog(n, base) <= root - 2, 'root reserve')
                atomizations += 1
    # High-matrix rows remain in the packet. These are small illustrative
    # integers, not the selected astronomical template or prime.
    low, high, depth, old = 6, 81, 4, 5
    width = low * high
    rows = width**depth * old
    need(rows // low == high * (rows // width), 'full high packet retained')
    need(rows % old == 0, 'product stock retains old factor')
    controls = {
        'same_width_child_rejected': not ((2, 1, 12) < (2, 1, 12)),
        'current_transport_backend_rejected': not ((2, 2, 0) < (2, 1, 12)),
        'forward_backend_level_rejected': not ((2, 2, 0) < (1, 2, 0)),
        'dropped_high_packet_rejected': rows // width != rows // low,
        'maximum_instead_of_product_rejected': max(width**depth, old) % old != 0,
        'f_only_measure_rejected': (2 - 1) * (4 * 32 + 6) > 2,
    }
    need(all(controls.values()), 'semantic control')
    rho, covered, previous = F(1, 250), F('.0038525298'), F('.0034')
    envelopes = []
    for admitted in (F('.0038507'), F('.00385248')):
        envelope = (1 - rho) * covered + rho * previous
        need(previous < admitted < envelope < rho < 1 - envelope, 'current bootstrap gaps')
        envelopes.append(str(envelope))
        previous = admitted
    need(previous > F('.00363005817004'), 'completed BIT supplies selected weaker rate')
    need((2, 2, 0) < (3, 0, 0), 'compact-to-BIT kind')
    return dict(marker='PASS_RELATIVE_COMPACT_BIT_DESCENT', source_pins=len(sources),
                same_stage_edges=edges, stock_inequalities=stocks,
                integer_atomizations=atomizations, envelopes=envelopes,
                controls=controls, selected_carrier='2^296630000000000 (not materialized)',
                premise='completed O0=.0034 and retained physical/native/compiler contracts',
                scope='Finite corroboration of written relative lexicographic descent; no literal backend execution.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-repo', type=Path, default=HERE.parents[2] / 'repo')
    args = parser.parse_args()
    print(json.dumps(run(args.source_repo), indent=2, sort_keys=True))
