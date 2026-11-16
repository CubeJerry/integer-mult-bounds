"""Semantic omissions for the literal D4 words; retained interpreter is credited reuse."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'))
    ap.add_argument('--word', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    path = a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py'
    sp = importlib.util.spec_from_file_location('control_engine', path)
    e = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(e)
    raw = a.word.read_bytes()
    w = json.loads(raw)
    sr = (a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(sr).hexdigest() == w['source_sha256']
    R = json.loads(sr)['native_roots']
    _, _, report = e.replay(w, R)
    operations = w['operations']
    before_decode = w['cohort']['decode_begin']
    cases = [('raw_cache_capture', k) for k, o in enumerate(operations)
             if o[0] == 'ADD' and o[2].startswith('D4_RAW_')]
    cases += [('source_quartet_term', k) for k, o in enumerate(operations[:before_decode])
              if o[0] == 'ADD' and o[1].startswith('X')
              and int(o[1][1:]) in w['cohort']['targets']
              and o[2] in {'P3', 'P4', 'P5'}]
    cases += [('proper_field_descent', k) for k, o in enumerate(operations)
              if o[0] == 'MOVE' and o[1] in w['cohort']['fields']
              and o[2] == w['cohort']['meet']]
    cases += [('principal_reset', k) for k, o in enumerate(operations)
              if o[0] == 'ADD' and o[1] in w['cohort']['fields']
              and o[2] in {'P3', 'P4', 'P5'}]
    rejected = []
    for kind, k in cases:
        bad = copy.deepcopy(w)
        del bad['operations'][k]
        try:
            e.replay(bad, R)
        except (AssertionError, KeyError) as ex:
            rejected.append({'kind': kind, 'operation_index': k,
                             'omitted_operation': operations[k],
                             'failure': str(ex)[:240] or 'native endpoint identity'})
        else:
            raise AssertionError(('accepted semantic omission', kind, k))
    assert len(rejected) == 54
    out = {'status': 'PASS_COHORT_54_SEMANTIC_OMISSIONS',
           'word_sha256': hashlib.sha256(raw).hexdigest(),
           'baseline_replay': report, 'rejected_count': len(rejected),
           'rejected': rejected,
           'scope': 'Author validation using the retained native interpreter; '
                    'independent review is separate. Omission controls complement '
                    'the all-field symbolic construction proof.'}
    a.out.write_text(json.dumps(out, indent=2)+'\n')
    print(out['status'], out['word_sha256'])


if __name__ == '__main__':
    main()
