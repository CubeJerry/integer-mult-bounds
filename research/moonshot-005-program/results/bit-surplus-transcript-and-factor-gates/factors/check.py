#!/usr/bin/env python3
"""Check the union-of-two-flat bound and prices for a one-scalar factor excess."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

P=Path('research/moonshot-005-program')
R=P/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
C=P/'results/bit-induced95-equality-rigidity/author/FULL-SUPPORT-CERTIFICATE.json'
M=P/'results/bit-low-exterior-formation-gate/author/output/RESULT.json'
PRIVATE={14,17,19,20,96,99,101,102}
U=sorted(set(range(111))-set(range(8))-PRIVATE)

def checked(path,digest):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError(str(path))
    return json.loads(raw)

def main(repo):
    roots=checked(repo/R,'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e')['native_roots']
    code=checked(repo/C,'012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963')['canonical_vectors']
    room=checked(repo/M,'befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145')['sources'][0]['normalized_room']['rational']
    xi=[sum(v<<k for k,v in enumerate(code[str(j)])) for j in U]
    weights={k:sum((k&x).bit_count()%2 for x in xi) for k in range(1,512)}
    light={k:w for k,w in weights.items() if w<=40}
    payload=''.join(' '.join(map(str,(j,x,*roots[j])))+'\n' for j,x in zip(U,xi))
    with tempfile.TemporaryDirectory() as temp:
        binary=Path(temp)/'five'
        subprocess.run([os.environ.get('CXX','c++'),'-std=c++20','-O3',str(Path(__file__).with_name('flat_five.cpp')),'-o',str(binary)],check=True)
        output=subprocess.check_output([str(binary)],input=payload,text=True)
    flats={}; hits={}
    for line in output.splitlines():
        tag,k,*vals=line.split()
        if tag=='F':
            flats[int(k)]={int(a):int(n) for a,n in (x.split(':') for x in vals)}
        elif tag=='W':
            hits[int(k)]=list(map(int,vals))
        else:raise ValueError(line)
    assert len(hits)==6 and max(flats[5])==20
    assert {k:z[0] for k,z in hits.items()}==light
    assert all(2*r<w for w,r in hits.values())
    f=[Q(1),Q(24589,25000),Q(1),Q(95,108),Q(95,108)]
    allowance=Q(9651,10000)
    five=9*sum(f)+8-8*allowance
    trial={'canonical_input_one_extra_output':five-9*f[0],'canonical_output_one_extra_input_at_V1':five-sum(f)}
    assert min(trial.values())>Q(room[1])
    return {'rational_low_scope_ternary_enclosures':flats,'canonical_words_weight_at_most_40_and_max_hits_per_flat':hits,
            'all_511_nonzero_word_weight_counts':dict(sorted(Counter(weights.values()).items())),
            'inherited_five_layer_tariff':str(five),'one_dimensional_lower_bounds':{n:str(x) for n,x in trial.items()},
            'scalar_normalized_room_upper':room[1], 'price_positive_gaps':{n:str(x-Q(room[1])) for n,x in trial.items()}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args()
    print(json.dumps(main(a.repo),indent=2))
