"""Exact canonical carving/source-exposure checks, separate from numerical replay.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import sys
PACKAGE = Path(__file__).resolve().parent
sys.path[:0] = [str(PACKAGE), str(PACKAGE/'retained/inverse_window')]
from runtime_sources import authenticate
from fixture_tools import need
from verify_transport import stable
from source_carve import partition
import reference_source
import source_window
import independent_oracle


def independently_check_partition(reference, origin, length, band, cap, blocks, receipt):
    pieces = receipt['pieces']
    cover = [None] * length
    for piece in pieces:
        need(piece['kind'] in ('B', 'I'), 'declared carve piece kind')
        for x in range(piece['start'], piece['stop']):
            need(0 <= x < length and cover[x] is None, 'independent disjoint carve coverage')
            cover[x] = piece['kind']
        if piece['kind'] == 'I':
            coordinates = list(range(origin+piece['start'], origin+piece['stop']))
            sources = [reference.source_at.get(x) for x in coordinates]
            need(all(x is not None for x in sources), 'no source hole in an interior')
            need(sources == list(range(sources[0], sources[0]+len(sources))),
                 'original source coordinates consecutive')
            need(len({reference.phases[x] for x in sources}) == 1,
                 'one original source phase per interior')
            need(len(sources) <= cap and len(sources)&(len(sources)-1) == 0,
                 'bounded dyadic original-source interior')
    need(all(value is not None for value in cover), 'complete independent partition cover')
    expected = [tuple(range(piece['start'],piece['stop'])) for piece in pieces if piece['kind']=='I']
    need(list(blocks) == expected, 'actual source interiors equal declared pieces')
    for left, right in zip(blocks, blocks[1:]):
        need(right[0]-left[-1] > band, 'actual separator at least source band')
    holes = [x for x in range(length) if reference.source_at.get(origin+x) is None]
    need(all(cover[x] == 'B' for x in holes), 'every original source hole is boundary')
    return dict(complete_coverage=True, holes=holes,
                interiors=len(blocks),interior_coordinates=sum(map(len,blocks)),
                phases=sorted({piece['phase'] for piece in pieces if piece['phase'] is not None}))


def run():
    raw = authenticate()
    reference = reference_source.make_reference(raw,(251,5,2,1,3,32))
    rows = []
    try:
        for origin, length, numerical in ((80,40,True),(12,90,False)):
            blocks, receipt = partition(raw,reference,origin,length,8)
            checked = independently_check_partition(reference,origin,length,4,8,blocks,receipt)
            row = dict(partition=receipt,independent_geometry=checked)
            if numerical:
                window = source_window.make_window(reference,origin=origin,length=length,
                    interior_blocks=blocks,band=4,cap=8,block=8,precision=32,width=48)
                checked_source = independent_oracle.check_source(reference,window)
                interior = set(x for block in blocks for x in block)
                boundary = set(range(length))-interior
                matrix = tuple(tuple(reference.entry('narrow',origin+i,origin+j).value
                                     for j in range(length)) for i in range(length))
                # Rebuild E from original off-diagonal incidents, without the producer's helper.
                incident = {i for i in interior if any(matrix[i][j] or matrix[j][i] for j in boundary)}
                expected_e = tuple(sorted(boundary|incident))
                need(window.E == expected_e and tuple(window.J) == tuple(sorted(boundary)),
                     'independent original-coordinate exposure and boundary')
                need(window.total_error <= Fraction(1,1 << window.target),
                     'exact source admission error target')
                need(blocks and incident and len(window.E) < length,
                     'nonempty production carve, actual exposed interior and inactive coordinates')
                row.update(scope='exact same-Reference source admission; no physical numerical run',
                           source=window.receipt(),original_source_review=checked_source,
                           independent_exposed=expected_e)
            else:
                need(checked['holes'] and len(checked['phases']) > 1 and blocks,
                     'clipped source test crosses holes and original phases with a nonempty interior')
                row['scope']='canonical carve geometry across original holes/phases only'
            rows.append(row)
        return dict(marker='PASS_CANONICAL_CARVE_SOURCE_PROVENANCE',cases=rows,
                    reference=reference_source.source_receipt(reference),
                    numerical_replay_scope='verify_source.py uses separately labelled admitted partitions',
                    no_new_kappa=True)
    finally:
        reference_source.clear_reference(reference)


def main():
    sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser();parser.add_argument('--write-result',action='store_true')
    parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    result=stable(run());target=PACKAGE/'CARVE-RESULT.json'
    if args.write_result:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    elif not args.emit:
        need(result==json.loads(target.read_text()),'exact canonical carve source receipt')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
