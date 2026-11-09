"""Bounded cold replay; expensive sparse8 preparation has an explicit long command.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile
PACKAGE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k not in ('seconds','elapsed_seconds')}
    if isinstance(value,(tuple,list)):
        return [stable(v) for v in value]
    return value


def child(script, arguments=()):
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env.pop('PYTHONPATH',None)
    with tempfile.TemporaryDirectory(prefix='union-cold-bytecode-') as directory:
        command=[sys.executable,'-I','-B','-X','pycache_prefix='+directory]
        if sys.flags.optimize:
            command.append('-O')
        command.extend((str(PACKAGE/script),*arguments))
        print('REPLAY '+script+' '+' '.join(arguments),file=sys.stderr,flush=True)
        completed=subprocess.run(command,stdout=subprocess.PIPE,text=True,env=env,
                                 timeout=580,check=True)
    if script=='independent_flat_oracle.py':
        return stable(json.loads(completed.stdout.splitlines()[-1]))
    return stable(json.loads(completed.stdout))


def source_admission(result):
    """Independent observer checks connecting the finite words to the radius bill."""
    source=result['source']; transport=result['transport']; grid=result['grid_review']
    g=len(result['context']['axis_keys']); L=source['window'][1]-source['window'][0]
    a=len(source['E']); n=len(source['J']); b=source['block']; p=source['precision']
    need(g==2 and a>0,'declared two-axis numerical fixture')
    need(grid['maximum_incoming_l1_numerator'] <= Fraction(source['radius'])*(1<<p),
         'every actual-current oracle line fits the admitted complex-l1 radius')
    need(Fraction(source['total_error']) <= Fraction(1,1<<source['target']),
         'exact inherited local numerical error target')
    need(Fraction(source['root_record_radius']) < Fraction(1<<source['width'],2*(1<<p)),
         'source intermediate record radius fits the signed physical carrier')
    need(transport['visits']==grid['visited_records']==2*a*L,
         'exact source-bound global incidence count')
    # Direct two-axis class count, separate from the physical routing algorithm.
    lines=(L,L) if a==L else (L,L-a,a)
    ke=(a+b-1)//b; kj=(n+b-1)//b
    matrix_calls=(2*(2*ke-1)+2*(2*kj-1))*sum((2*m+b-1)//b for m in lines)
    scalar_calls=matrix_calls*7**(b.bit_length()-1)
    need(transport['scalar_products']==scalar_calls and transport['substreams']==len(lines),
         'independent exact source matrix/scalar-call invoice including every ceiling')
    return dict(admitted_current_radius=True,local_error_target=True,carrier_bound=True,
                substream_lines=lines,matrix_calls=matrix_calls,scalar_products=scalar_calls)


def run(write=False):
    regen=('--write-result',) if write else ()
    transport=child('verify_transport.py',regen)
    review=child('independent_flat_oracle.py')
    expected_review=PACKAGE/'ROOT-REVIEW-RESULT.json'
    if write:
        expected_review.write_text(json.dumps(review,indent=2,sort_keys=True)+'\n')
    else:
        need(review==json.loads(expected_review.read_text()),'stable independent flat-index receipt')
    tape_review=child('review/a_review_union.py')
    need(tape_review==json.loads((PACKAGE/'review/a_review_union.normal.log').read_text()),
         'independent local-scan and short-metadata receipt')
    carve=child('verify_carve.py',regen)
    source=child('verify_source.py',('--case','admitted4',*regen))
    admission=source_admission(source)
    return dict(marker='PASS_PHYSICAL_WHOLE_UNION_PACKAGE',
                transport_marker=transport['marker'],transport_cases=len(transport['cases']),
                rejection_controls=sorted(transport['rejection_controls']),
                independent_review_marker=review['status'],independent_review_cases=len(review['cases']),
                source_carve_marker=carve['marker'],source_carve_cases=len(carve['cases']),
                numerical_marker=source['marker'],numerical_case=source['fixture_case'],
                numerical_admission=admission,numerical_transport=source['transport'],
                no_new_kappa=True,
                long_replay='verify_source.py --case sparse8; excluded from the bounded generic hook')


def main():
    sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser();parser.add_argument('--write-result',action='store_true')
    args=parser.parse_args(); result=stable(run(args.write_result)); target=PACKAGE/'RESULT.json'
    if args.write_result:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(result==json.loads(target.read_text()),'stable complete bounded package receipt')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
