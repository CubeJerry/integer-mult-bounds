"""Independent affine-fibre enumeration for root's canonical+half-sum gate.

Unlike the author check, this eliminates the complete 33-dimensional code and
enumerates each fitting fibre; it does not optimize separate half coefficients.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json


def independent_rows(rows):
    pivots = {}
    for value in rows:
        while value:
            p = (value & -value).bit_length() - 1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    return list(pivots.values())


def fibre(code, forbidden, target):
    pivots = {}; kernel = []
    for complete in code:
        restricted = complete & forbidden
        while restricted:
            p = (restricted & -restricted).bit_length() - 1
            if p in pivots:
                r, f = pivots[p]; restricted ^= r; complete ^= f
            else:
                pivots[p] = restricted, complete
                break
        if not restricted:
            kernel.append(complete)
    solution = 0
    while target:
        p = (target & -target).bit_length() - 1
        assert p in pivots, 'fitting fibre is empty'
        r, f = pivots[p]; target ^= r; solution ^= f
    assert len(independent_rows(kernel)) == len(kernel)
    assert all(k & forbidden == 0 for k in kernel)
    return solution, kernel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--author-certificate', type=Path, default=Path(__file__).resolve().parents[1]/'R/half-sum-code-gate/output/CERTIFICATE.json')
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent/'half-sum-gate-review')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    raw = (args.inputs/'SOURCE-RECOVERY.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots = json.loads(raw)['native_roots']; full = (1 << 111)-1
    neighbours = [sum(1 << j for j, s in enumerate(roots) if sum(a*b for a,b in zip(r,s)) == 0) for r in roots]
    canonical = [n ^ (1 << i) for i,n in enumerate(neighbours)]
    groups = {}
    for i,r in enumerate(roots):
        support = tuple(j for j,x in enumerate(r) if x)
        if len(support) != 4:
            continue
        a,b = support[:2]
        key = support, r[a] == r[b]
        groups.setdefault(key, []).append(i)
    halves = [sum(1 << i for i in group) for group in groups.values()]
    code = independent_rows(canonical+halves)
    assert (len(independent_rows(canonical)), len(independent_rows(halves)), len(code)) == (9,28,33)
    author = json.loads(args.author_certificate.read_text())
    claimed = {r['receiver']:r['minimum_foreign_support'] for r in author['receivers']}
    records = []; visited = 0
    for i,local in enumerate(neighbours):
        forbidden = full ^ local
        solution, kernel = fibre(code,forbidden,1 << i)
        current = solution; oldgray = 0; best = (current & local).bit_count(); witness = current
        count = 1 << len(kernel); visited += count
        for j in range(1,count):
            gray = j ^ (j >> 1); change = gray ^ oldgray
            current ^= kernel[change.bit_length()-1]; oldgray = gray
            w = (current & local).bit_count()
            if w < best:
                best, witness = w, current
        assert witness & forbidden == 1 << i
        assert best == claimed[i], (i,best,claimed[i])
        records.append({'receiver':i,'fibre_dimension':len(kernel),'enumerated_rows':count,
                        'minimum_foreign_support':best,'minimum_capped_charge':int(best>36)+int(best>52),
                        'independent_witness_hex':hex(witness)})
    total = sum(r['minimum_capped_charge'] for r in records)
    assert total == 96
    result={'status':'PASS_INDEPENDENT_FULL_AFFINE_FIBRE_ENUMERATION','source_sha256':hashlib.sha256(raw).hexdigest(),
            'author_certificate_sha256':hashlib.sha256(args.author_certificate.read_bytes()).hexdigest(),
            'ranks_C_D_sum':[9,28,33],'minimum_total_capped_charge':total,'enumerated_fitting_rows':visited,
            'fibre_dimension_histogram':dict(sorted(Counter(r['fibre_dimension'] for r in records).items())),
            'minimum_foreign_support_histogram':dict(sorted(Counter(r['minimum_foreign_support'] for r in records).items())),
            'receivers':records,
            'scope':'Independent exact binary code minimization plus reviewed scalar-projection extension to characteristic2 fields and arbitrary whole widths; physical frozen-cut consequence retains normalized-history-space hypothesis.'}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='receivers'},indent=2))


if __name__ == '__main__': main()
