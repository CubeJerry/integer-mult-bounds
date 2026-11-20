#!/usr/bin/env python3
"""Stream the actual binary owner instructions for one donor and one phase."""
import argparse
import gzip
import json
from pathlib import Path

from compile_source import BANK, DEGREE, ITEM, SCALES, binary_rows

def moves(d,s):
    for b in range(DEGREE):
        yield 'ADD',DEGREE*d+b,DEGREE*s+b
        yield 'ADD',DEGREE*s+b,DEGREE*d+b
        yield 'ADD',DEGREE*d+b,DEGREE*s+b

def add_scaled(d,s,z):
    for b,mask in enumerate(binary_rows(z)):
        for t in range(DEGREE):
            if mask & (1<<t):
                yield 'ADD',DEGREE*d+b,DEGREE*s+t

def basis(stream, order, forward):
    positions=range(0,len(stream),ITEM.size)
    if forward:
        positions=reversed(positions)
    for pos in positions:
        op,d,s,z=ITEM.unpack_from(stream,pos)
        if op==0:
            yield from add_scaled(order[d],order[s],z)
        elif op==1:
            ops=reversed(SCALES[z]) if forward else SCALES[z]
            field=order[d]
            for a,b in ops:
                yield 'ADD',DEGREE*field+a,DEGREE*field+b
        else:
            yield from moves(order[d],order[s])

def emit(out, donor, stage):
    bundle=out/'HOLDER-WORDS.json.gz'
    if not bundle.exists():
        bundle=out/f'HOLDERS-{donor}.json.gz'
    words=json.loads(gzip.decompress(bundle.read_bytes()))
    components=[words[f'{donor}-{k}'] for k in (3,12)]
    swaps=words[f'{donor}-swaps']
    if stage in ('prepare','deliver'):
        for block in components:
            for job in block['before_departure_late_parities']:
                for dst,first in job['dest_and_first_X']:
                    # This fresh stationary source cache has a distinct address
                    # from both physical phase spaces. Its index names its real Y.
                    cache=2*111*BANK+dst
                    if stage=='prepare':
                        for b in range(DEGREE):
                            yield 'INIT',DEGREE*cache+b
                        for s,z in enumerate(job['coefficients']):
                            if z:
                                yield from add_scaled(cache,first+16*s,z)
                    else:
                        for b in range(DEGREE):
                            yield 'ADD',DEGREE*dst+b,DEGREE*cache+b
                            yield 'dirty_CLEAR',DEGREE*cache+b
        return
    if stage=='inverse':
        for a,b in reversed(swaps):
            yield from moves(a,b)
    for block in components:
        stream=gzip.decompress((out/block['reduce_file']).read_bytes())
        for placement in block['original_field_placements']:
            yield from basis(stream,placement,stage=='early')
    if stage=='early':
        for a,b in swaps:
            yield from moves(a,b)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--word-dir',type=Path,default=Path(__file__).parent/'output')
    p.add_argument('--donor',type=int,required=True,help='native donor ID with a generated word')
    p.add_argument('--stage',choices=('prepare','early','deliver','inverse'),required=True)
    p.add_argument('--limit',type=int,default=None,help='maximum instructions printed')
    a=p.parse_args()
    from itertools import islice
    for op in islice(emit(a.word_dir,a.donor,a.stage),a.limit):
        print(*op)

if __name__=='__main__':
    main()
