"""Independent inverse-column check of one literal-chart repair obstruction."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def run(path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'source hash')
    w = json.loads(gzip.decompress(raw))
    hosted = w['hosted']
    mains = (set(w['live']) | {i+112 for i in w['live']}
             | set(hosted['X2']) | set(hosted['Y2']))
    ops = []
    for e in w['program']:
        if e[1] not in mains:
            continue
        need(e[0] not in ('COPY', 'INIT', 'CLEAR'), 'no main overwrite or lifetime operation')
        if e[0] == 'SCALE':
            need(F(e[2]) != 0, 'invertible main SCALE')
            ops.append(e)
        elif e[0] in ('ADD', 'COPY') and e[2] in mains:
            need(e[0] == 'ADD', 'no main-only COPY assumed')
            ops.append(e)
    need(len(mains) == 400 and len(ops) == 3769, 'main-only dimensions')
    def apply(values, program, inverse):
        z = dict(values)
        for e in program:
            d = e[1]
            if e[0] == 'SCALE':
                q = F(e[2])
                z[d] *= 1/q if inverse else q
            else:
                z[d] += (-1 if inverse else 1)*F(e[3])*z[e[2]]
        return z

    unit = {r: F(r == 129) for r in mains}
    inverse_column = apply(unit, reversed(ops), True)
    need(apply(inverse_column, ops, False) == unit, 'M0 inverse-column direct forward check')
    wrong = apply(unit, ops, True)
    need(apply(wrong, ops, False) != unit, 'wrong inverse-order control')
    i = w['live'].index(17)
    if i in hosted['Dports']:
        expected_row = {17: F(1)}
    else:
        expected_row = {17: F(1), 129: F(-1)}
    coefficient = sum(q*inverse_column[r] for r, q in expected_row.items())
    need(coefficient == -3, 'C[17,129] exact coefficient')
    a, b = w['final'][17], w['final'][129]
    need((a, b) == (127, 143), 'witness final chart labels')
    need((len(w['frames'][a]), len(w['frames'][b])) == (9, 8), 'distinct witness ranks')
    return {'status': 'PASS_INDEPENDENT_SELECTOR_REPAIR_WITNESS', 'source_sha256': PIN,
            'method': 'Reverse inverse-word action on e129, then selected E row17; direct forward composition checks the inverse column',
            'main_fields': len(mains), 'main_only_scalar_operations': len(ops),
            'output': 17, 'source': 129, 'coefficient': str(coefficient),
            'output_final_frame': a, 'source_final_frame': b,
            'output_final_rank': 9, 'source_final_rank': 8,
            'E_output_row': {str(r): str(q) for r, q in expected_row.items()},
            'inverse_column_nonzero': {str(r): str(q) for r, q in sorted(inverse_column.items()) if q},
            'negative_controls': ['chronological rather than reverse inverse-column order'],
            'scope': 'One exact off-chart postrepair coefficient; no full defect rank, general repair-cost lower bound or arbitrary-program obstruction.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--word', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/data/final.json.gz')
    args = p.parse_args()
    print(json.dumps(run(args.word), indent=2))
